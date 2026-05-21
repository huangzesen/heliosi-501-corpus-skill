"""Tests for scripts/build_acquisition_queue.py.

Stdlib-only unittest module. No network calls; every test reads the
fixture pilot directory under ``tests/fixtures/acquisition/`` and asserts
on the normalised queue rows.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "build_acquisition_queue.py"
FIXTURE_ROOT = BUNDLE / "tests" / "fixtures" / "acquisition"


def _load_module():
    spec = importlib.util.spec_from_file_location("build_acquisition_queue", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


baq = _load_module()


class TestNormalisation(unittest.TestCase):
    def test_norm_doi_strips_url_prefix_and_lowercases(self):
        self.assertEqual(baq._norm_doi("https://doi.org/10.1029/JA073"), "10.1029/ja073")
        self.assertEqual(baq._norm_doi("doi:10.5555/X"), "10.5555/x")
        self.assertIsNone(baq._norm_doi(None))
        self.assertIsNone(baq._norm_doi(""))
        self.assertIsNone(baq._norm_doi("not-a-doi"))

    def test_norm_arxiv_strips_prefix(self):
        self.assertEqual(baq._norm_arxiv("arXiv:2301.00001"), "2301.00001")
        self.assertEqual(baq._norm_arxiv("2301.00001"), "2301.00001")
        self.assertIsNone(baq._norm_arxiv(None))

    def test_pick_identifier_prefers_doi(self):
        ident, kind, prio = baq.pick_identifier("10.5555/x", "2301.00001", "BIB")
        self.assertEqual(ident, "10.5555/x")
        self.assertEqual(kind, "doi")
        self.assertEqual(prio, baq.PRIORITY_DOI)

    def test_pick_identifier_falls_back_to_arxiv(self):
        ident, kind, _ = baq.pick_identifier(None, "2301.00001", None)
        self.assertEqual(ident, "arXiv:2301.00001")
        self.assertEqual(kind, "arxiv")

    def test_pick_identifier_bibcode_only_marks_unsupported(self):
        ident, kind, _ = baq.pick_identifier(None, None, "1960ApJ...132...50P")
        self.assertIsNone(ident)
        self.assertEqual(kind, "bibcode_only")

    def test_pick_identifier_none(self):
        ident, kind, _ = baq.pick_identifier(None, None, None)
        self.assertIsNone(ident)
        self.assertEqual(kind, "none")

    def test_candidate_id_stable_across_doi_case(self):
        a = baq.candidate_id("10.1029/ja073", None, "BIB1", "x", 1968)
        b = baq.candidate_id("10.1029/ja073", None, None, "x", 1968)
        self.assertEqual(a, b)

    def test_candidate_id_changes_when_no_doi(self):
        a = baq.candidate_id(None, "2301.00001", None, "x", 2023)
        b = baq.candidate_id(None, None, "1968JGR....73.7221H", "x", 1968)
        self.assertNotEqual(a, b)


class TestBuildQueue(unittest.TestCase):
    def test_build_dedupes_across_cells_and_drops_already_curated(self):
        rows = baq.build_queue(
            pilot_root=FIXTURE_ROOT,
            explicit_files=[],
            include_already_curated=False,
        )
        # P1 has 3 rows (1 doi, 1 bibcode-only, 1 already_curated dropped).
        # P2 has 2 rows (same doi as P1 -> deduped, 1 arxiv new).
        # Expected after dedupe + drop_curated: doi + bibcode_only + arxiv = 3.
        self.assertEqual(len(rows), 3)

        statuses = sorted(r["status"] for r in rows)
        self.assertEqual(
            statuses,
            sorted(["pending", "no_supported_identifier", "pending"]),
        )

        kinds = sorted(r["identifier_kind"] for r in rows)
        self.assertEqual(kinds, sorted(["doi", "bibcode_only", "arxiv"]))

        # The doi row should mention it was also seen in P2.
        doi_row = next(r for r in rows if r["identifier_kind"] == "doi")
        self.assertIn("P2-demo", doi_row["notes"])

    def test_include_already_curated_keeps_them_marked(self):
        rows = baq.build_queue(
            pilot_root=FIXTURE_ROOT,
            explicit_files=[],
            include_already_curated=True,
        )
        statuses = [r["status"] for r in rows]
        self.assertIn("skipped_already_done", statuses)
        self.assertEqual(len(rows), 4)

    def test_sort_priority_doi_first(self):
        rows = baq.build_queue(
            pilot_root=FIXTURE_ROOT,
            explicit_files=[],
            include_already_curated=False,
        )
        priorities = [r["priority"] for r in rows]
        self.assertEqual(priorities, sorted(priorities))
        self.assertEqual(priorities[0], baq.PRIORITY_DOI)

    def test_summary_counts_match_rows(self):
        rows = baq.build_queue(
            pilot_root=FIXTURE_ROOT,
            explicit_files=[],
            include_already_curated=True,
        )
        summary = baq.summarize(rows)
        self.assertEqual(summary["total"], len(rows))
        self.assertEqual(sum(summary["by_status"].values()), len(rows))
        self.assertEqual(sum(summary["by_identifier_kind"].values()), len(rows))


class TestWriteOutputs(unittest.TestCase):
    def test_write_jsonl_and_csv_roundtrip(self):
        rows = baq.build_queue(
            pilot_root=FIXTURE_ROOT,
            explicit_files=[],
            include_already_curated=False,
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            now = "2026-05-20T12:00:00Z"
            baq.write_queue_jsonl(rows, out / "queue.jsonl", now)
            baq.write_queue_csv(rows, out / "queue.csv", now)
            baq.write_meta({"k": "v"}, out / "queue.meta.json")

            jsonl_rows = [
                json.loads(line)
                for line in (out / "queue.jsonl").read_text().splitlines()
                if line.strip()
            ]
            self.assertEqual(len(jsonl_rows), len(rows))
            self.assertTrue(all(r["queued_at_utc"] == now for r in jsonl_rows))

            with (out / "queue.csv").open() as fh:
                csv_rows = list(csv.DictReader(fh))
            self.assertEqual(len(csv_rows), len(rows))

            meta = json.loads((out / "queue.meta.json").read_text())
            self.assertEqual(meta["k"], "v")


if __name__ == "__main__":
    unittest.main()
