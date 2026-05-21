"""Tests for scripts/merge_acquisition_queue.py.

Stdlib-only unittest module. Every test operates inside a tmpdir; no
live acquisition store is touched.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
MERGE_SCRIPT = BUNDLE / "scripts" / "merge_acquisition_queue.py"
BUILD_SCRIPT = BUNDLE / "scripts" / "build_acquisition_queue.py"
FIXTURE_ROOT = BUNDLE / "tests" / "fixtures" / "acquisition"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


merge = _load("merge_acquisition_queue", MERGE_SCRIPT)
baq = _load("build_acquisition_queue", BUILD_SCRIPT)


# ──────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────

def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _seed_existing_queue(path: Path) -> list[dict]:
    """Seed an existing queue built from the P1 fixture but with custom state.

    Two rows: the DOI row with status=fetched and a custom note, and the
    bibcode-only row left as no_supported_identifier.
    """
    rows = baq.build_queue(
        pilot_root=None,
        explicit_files=[FIXTURE_ROOT / "P1-demo" / "candidates.jsonl"],
        include_already_curated=False,
    )
    # Stamp a queued_at and customise state, mimicking a real run.
    seeded = []
    for row in rows:
        r = dict(row)
        r["queued_at_utc"] = "2026-01-01T00:00:00Z"
        if r["identifier_kind"] == "doi":
            r["status"] = "fetched"
            r["notes"] = "preserve-me"
        seeded.append(r)
    _write_jsonl(path, seeded)
    return seeded


# ──────────────────────────────────────────────────────────
#  load_existing_queue
# ──────────────────────────────────────────────────────────

class TestLoadExisting(unittest.TestCase):
    def test_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                merge.load_existing_queue(Path(tmp) / "nope.jsonl"), []
            )

    def test_skips_blank_and_malformed_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "queue.jsonl"
            p.write_text('{"candidate_id":"a"}\n\nnot-json\n{"candidate_id":"b"}\n')
            rows = merge.load_existing_queue(p)
            self.assertEqual([r["candidate_id"] for r in rows], ["a", "b"])


# ──────────────────────────────────────────────────────────
#  merge_rows
# ──────────────────────────────────────────────────────────

class TestMergeRows(unittest.TestCase):
    def test_preserves_existing_state_and_appends_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "queue.jsonl"
            seeded = _seed_existing_queue(existing_path)

            existing = merge.load_existing_queue(existing_path)
            # New candidates: P1 (overlap) + P2 (introduces arxiv preprint).
            new = baq.build_queue(
                pilot_root=FIXTURE_ROOT,
                explicit_files=[],
                include_already_curated=False,
            )

            merged, counts = merge.merge_rows(
                existing=existing,
                new_candidates=new,
                now_iso="2026-05-20T12:00:00Z",
                annotate_resurfaced=False,
            )

            # The DOI row's fetched status and bespoke note must survive.
            doi_seed = next(r for r in seeded if r["identifier_kind"] == "doi")
            doi_merged = next(
                r for r in merged if r["candidate_id"] == doi_seed["candidate_id"]
            )
            self.assertEqual(doi_merged["status"], "fetched")
            self.assertEqual(doi_merged["notes"], "preserve-me")
            self.assertEqual(doi_merged["queued_at_utc"], "2026-01-01T00:00:00Z")

            # The arxiv row from P2 is brand new and must carry the new queued_at.
            arxiv_merged = next(
                r for r in merged if r["identifier_kind"] == "arxiv"
            )
            self.assertEqual(arxiv_merged["queued_at_utc"], "2026-05-20T12:00:00Z")
            self.assertEqual(arxiv_merged["status"], "pending")

            self.assertEqual(counts["existing_preserved"], 2)
            self.assertEqual(counts["new_appended"], 1)
            # P1 overlaps both existing rows -> 2 duplicates skipped.
            self.assertEqual(counts["duplicate_skipped"], 2)
            self.assertEqual(counts["total_after_merge"], 3)

    def test_existing_only_rows_survive_when_not_in_new(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "queue.jsonl"
            _seed_existing_queue(existing_path)
            existing = merge.load_existing_queue(existing_path)

            # New batch covers ONLY the P2 arxiv preprint. Existing P1 rows
            # should still be present.
            new = baq.build_queue(
                pilot_root=None,
                explicit_files=[FIXTURE_ROOT / "P2-demo" / "candidates.jsonl"],
                include_already_curated=False,
            )

            merged, counts = merge.merge_rows(
                existing=existing,
                new_candidates=new,
                now_iso="2026-05-20T12:00:00Z",
            )

            ids = {r["candidate_id"] for r in merged}
            existing_ids = {r["candidate_id"] for r in existing}
            self.assertTrue(existing_ids.issubset(ids))
            self.assertEqual(counts["existing_preserved"], 2)
            # P2 contributes the duplicate DOI row + new arxiv row.
            self.assertEqual(counts["duplicate_skipped"], 1)
            self.assertEqual(counts["new_appended"], 1)

    def test_annotate_resurfaced_appends_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "queue.jsonl"
            seeded = _seed_existing_queue(existing_path)
            existing = merge.load_existing_queue(existing_path)

            # Inject a fake new cell label for the same DOI candidate.
            doi_seed = next(r for r in seeded if r["identifier_kind"] == "doi")
            new = [
                {
                    **doi_seed,
                    "cell": "P9-fresh",
                    "notes": "",
                    "queued_at_utc": None,
                }
            ]

            merged, _counts = merge.merge_rows(
                existing=existing,
                new_candidates=new,
                now_iso="2026-05-20T12:00:00Z",
                annotate_resurfaced=True,
            )
            doi_merged = next(
                r for r in merged if r["candidate_id"] == doi_seed["candidate_id"]
            )
            self.assertIn("also-seen-in:P9-fresh", doi_merged["notes"])
            # Original note must remain.
            self.assertIn("preserve-me", doi_merged["notes"])

    def test_annotate_resurfaced_off_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "queue.jsonl"
            seeded = _seed_existing_queue(existing_path)
            existing = merge.load_existing_queue(existing_path)
            doi_seed = next(r for r in seeded if r["identifier_kind"] == "doi")

            new = [
                {**doi_seed, "cell": "P9-fresh", "notes": "", "queued_at_utc": None}
            ]
            merged, _ = merge.merge_rows(
                existing=existing,
                new_candidates=new,
                now_iso="2026-05-20T12:00:00Z",
                # default: annotate_resurfaced=False
            )
            doi_merged = next(
                r for r in merged if r["candidate_id"] == doi_seed["candidate_id"]
            )
            self.assertNotIn("also-seen-in", doi_merged["notes"])

    def test_summary_counts_consistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "queue.jsonl"
            _seed_existing_queue(existing_path)
            existing = merge.load_existing_queue(existing_path)
            new = baq.build_queue(
                pilot_root=FIXTURE_ROOT,
                explicit_files=[],
                include_already_curated=False,
            )
            merged, counts = merge.merge_rows(
                existing=existing,
                new_candidates=new,
                now_iso="2026-05-20T12:00:00Z",
            )
            summary = merge.summarize_merge(merged, counts)
            self.assertEqual(
                summary["merge"]["existing_preserved"]
                + summary["merge"]["new_appended"],
                summary["merge"]["total_after_merge"],
            )
            self.assertEqual(summary["total"], len(merged))
            self.assertEqual(
                sum(summary["by_status"].values()), len(merged)
            )


# ──────────────────────────────────────────────────────────
#  Atomic write
# ──────────────────────────────────────────────────────────

class TestAtomicWrite(unittest.TestCase):
    def test_success_replaces_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            queue_path = out / "queue.jsonl"
            csv_path = out / "queue.csv"
            # Pre-seed an "old" queue to prove replace happens.
            queue_path.write_text("OLD\n")
            csv_path.write_text("OLD,CSV\n")

            rows = [
                {
                    "candidate_id": "cand_x",
                    "cell": "P1",
                    "source": "ads",
                    "title": "t",
                    "year": 2000,
                    "doi": "10.x/y",
                    "arxiv_id": None,
                    "bibcode": None,
                    "corpus_status": "new_candidate",
                    "preferred_identifier": "10.x/y",
                    "identifier_kind": "doi",
                    "priority": 10,
                    "status": "pending",
                    "notes": "",
                    "queued_at_utc": "2026-05-20T12:00:00Z",
                }
            ]
            merge.atomic_write_queue(rows, queue_path, csv_path)
            self.assertNotIn("OLD", queue_path.read_text())
            self.assertNotIn("OLD,CSV", csv_path.read_text())
            with csv_path.open() as fh:
                csv_rows = list(csv.DictReader(fh))
            self.assertEqual(len(csv_rows), 1)
            # No stray .tmp files left behind.
            for p in out.iterdir():
                self.assertFalse(p.name.endswith(".tmp"), p)

    def test_failure_preserves_original_and_cleans_tmp(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            queue_path = out / "queue.jsonl"
            csv_path = out / "queue.csv"
            queue_path.write_text("ORIGINAL_JSONL\n")
            csv_path.write_text("ORIGINAL_CSV\n")

            rows = [{"candidate_id": "x"}]

            real_write_csv = merge._write_csv_rows

            def boom(_rows, _path):  # noqa: ANN001 - test helper
                raise RuntimeError("simulated csv write failure")

            with mock.patch.object(merge, "_write_csv_rows", side_effect=boom):
                with self.assertRaises(RuntimeError):
                    merge.atomic_write_queue(rows, queue_path, csv_path)

            # Originals untouched.
            self.assertEqual(queue_path.read_text(), "ORIGINAL_JSONL\n")
            self.assertEqual(csv_path.read_text(), "ORIGINAL_CSV\n")
            # No .tmp files left behind.
            for p in out.iterdir():
                self.assertFalse(p.name.endswith(".tmp"), p)
            # Sanity: the real writer still works.
            self.assertIs(merge._write_csv_rows, real_write_csv)


# ──────────────────────────────────────────────────────────
#  run_merge end-to-end + CLI
# ──────────────────────────────────────────────────────────

class TestRunMerge(unittest.TestCase):
    def test_fresh_build_when_existing_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            missing = tmp / "no-such-queue.jsonl"
            merged, summary, existing_found = merge.run_merge(
                existing_queue_path=missing,
                pilot_root=FIXTURE_ROOT,
                explicit_files=[],
                include_already_curated=False,
                annotate_resurfaced=False,
                now_iso="2026-05-20T12:00:00Z",
            )
            self.assertFalse(existing_found)
            self.assertEqual(summary["merge"]["existing_preserved"], 0)
            self.assertEqual(
                summary["merge"]["new_appended"], summary["merge"]["total_after_merge"]
            )
            self.assertGreater(len(merged), 0)

    def test_end_to_end_writes_atomic_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "store" / "queue.jsonl"
            _seed_existing_queue(existing_path)
            out_dir = tmp / "store"

            argv = [
                "--existing-queue",
                str(existing_path),
                "--pilot-root",
                str(FIXTURE_ROOT),
                "--out-dir",
                str(out_dir),
            ]
            rc = merge.main(argv)
            self.assertEqual(rc, 0)

            merged_rows = [
                json.loads(line)
                for line in (out_dir / "queue.jsonl").read_text().splitlines()
                if line.strip()
            ]
            self.assertEqual(len(merged_rows), 3)

            with (out_dir / "queue.csv").open() as fh:
                csv_rows = list(csv.DictReader(fh))
            self.assertEqual(len(csv_rows), 3)

            meta = json.loads((out_dir / "queue.meta.json").read_text())
            self.assertEqual(meta["operation"], "merge")
            self.assertTrue(meta["existing_queue_found"])
            self.assertEqual(meta["summary"]["merge"]["new_appended"], 1)
            self.assertEqual(meta["summary"]["merge"]["existing_preserved"], 2)

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            existing_path = tmp / "queue.jsonl"
            _seed_existing_queue(existing_path)
            out_dir = tmp / "out"

            argv = [
                "--existing-queue",
                str(existing_path),
                "--pilot-root",
                str(FIXTURE_ROOT),
                "--out-dir",
                str(out_dir),
                "--dry-run",
            ]
            rc = merge.main(argv)
            self.assertEqual(rc, 0)
            self.assertFalse(out_dir.exists())

    def test_cli_requires_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            argv = [
                "--existing-queue",
                str(Path(tmp) / "q.jsonl"),
                "--out-dir",
                str(Path(tmp) / "out"),
            ]
            with self.assertRaises(SystemExit):
                merge.main(argv)


if __name__ == "__main__":
    unittest.main()
