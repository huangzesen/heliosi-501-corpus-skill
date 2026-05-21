"""Tests for scripts/run_acquisition_batch.py.

No network. The runner is exercised against a stub fetch_paper.py written
into a tempdir that mirrors the real script's contract:

    - Read identifier as argv[1].
    - Resolve --out to the same papers root the runner passed in.
    - Write papers/<slug>/manifest.json with status=ok or fail depending
      on the identifier we want the stub to "fetch".

This validates the resumability path (a fetched row is rewritten as
skipped_already_done on the second run) and the failure path (fail
manifests become fetch_failed in the queue).
"""

from __future__ import annotations

import importlib.util
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from textwrap import dedent


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "run_acquisition_batch.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("run_acquisition_batch", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rab = _load_module()


STUB_TEMPLATE = dedent("""\
    #!/usr/bin/env python3
    \"\"\"Test stub mimicking fetch_paper.py's manifest contract.\"\"\"
    import argparse, json, sys, time
    from pathlib import Path

    # Identifier-to-outcome map. Used to test ok / fail paths.
    OUTCOMES = {OUTCOMES_JSON}

    p = argparse.ArgumentParser()
    p.add_argument("identifier")
    p.add_argument("--out", required=True)
    p.add_argument("--email", default=None)
    p.add_argument("--no-libgen", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    ident = args.identifier
    outcome = OUTCOMES.get(ident, "fail")

    if ident.lower().startswith("arxiv:"):
        slug = "stub-arxiv-" + ident.split(":", 1)[1]
        manifest = {
            "status": outcome,
            "tier": "arxiv" if outcome == "ok" else None,
            "arxiv_id": ident.split(":", 1)[1].lower(),
            "doi": None,
            "title": "stub",
            "ts": int(time.time()),
        }
    else:
        slug = "stub-doi-" + ident.replace("/", "_")
        manifest = {
            "status": outcome,
            "tier": "unpaywall" if outcome == "ok" else None,
            "doi": ident.lower(),
            "arxiv_id": None,
            "title": "stub",
            "ts": int(time.time()),
        }

    paper_dir = out / slug
    paper_dir.mkdir(parents=True, exist_ok=True)
    (paper_dir / "manifest.json").write_text(json.dumps(manifest))
    print(f"stub wrote manifest for {{ident}} -> {{outcome}}")
    sys.exit(0)
""")


def _write_stub(tmp: Path, outcomes: dict) -> Path:
    path = tmp / "fetch_paper_stub.py"
    path.write_text(STUB_TEMPLATE.replace("{OUTCOMES_JSON}", json.dumps(outcomes)))
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return path


def _seed_queue(store: Path, rows: list[dict]) -> None:
    store.mkdir(parents=True, exist_ok=True)
    with (store / "queue.jsonl").open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")


def _row(cid, identifier, kind="doi", status="pending"):
    return {
        "candidate_id": cid,
        "cell": "P-test",
        "source": "test",
        "title": f"title for {cid}",
        "year": 2020,
        "doi": identifier if kind == "doi" else None,
        "arxiv_id": identifier.split(":", 1)[1] if kind == "arxiv" else None,
        "bibcode": None,
        "corpus_status": "new_candidate",
        "preferred_identifier": identifier,
        "identifier_kind": kind,
        "priority": 10 if kind == "doi" else 20,
        "status": status,
        "notes": "",
        "queued_at_utc": "2026-05-20T12:00:00Z",
    }


class TestSelectPending(unittest.TestCase):
    def test_select_only_pending_with_identifier(self):
        rows = [
            _row("a", "10.1/a"),
            _row("b", "10.1/b", status="fetched"),
            {"candidate_id": "c", "status": "pending", "preferred_identifier": None},
            _row("d", "10.1/d"),
        ]
        picked = rab.select_pending(rows, limit=10)
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "d"])

    def test_limit_caps_selection(self):
        rows = [_row(f"r{i}", f"10.1/{i}") for i in range(5)]
        picked = rab.select_pending(rows, limit=2)
        self.assertEqual(len(picked), 2)

    def test_year_filters(self):
        rows = [
            {**_row("old", "10.1/old"), "year": 1960},
            {**_row("mid", "10.1/mid"), "year": 1990},
            {**_row("new", "10.1/new"), "year": 2020},
            {**_row("no-year", "10.1/n"), "year": None},
        ]
        picked = rab.select_pending(rows, limit=10, year_min=1980)
        self.assertEqual([r["candidate_id"] for r in picked], ["mid", "new"])

        picked = rab.select_pending(rows, limit=10, year_min=1980, year_max=2000)
        self.assertEqual([r["candidate_id"] for r in picked], ["mid"])

    def test_only_candidate_ids_filter(self):
        rows = [_row(f"r{i}", f"10.1/{i}") for i in range(5)]
        picked = rab.select_pending(rows, limit=10, only_candidate_ids={"r1", "r3"})
        self.assertEqual([r["candidate_id"] for r in picked], ["r1", "r3"])


class TestRunBatch(unittest.TestCase):
    def test_ok_and_fail_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            stub = _write_stub(
                tmp,
                outcomes={
                    "10.1/a": "ok",
                    "10.1/b": "fail",
                    "arxiv:2301.00001": "ok",
                },
            )
            _seed_queue(
                store,
                [
                    _row("a", "10.1/a"),
                    _row("b", "10.1/b"),
                    _row("c", "arxiv:2301.00001", kind="arxiv"),
                ],
            )
            summary = rab.run_batch(
                store=store,
                fetch_script=stub,
                limit=10,
                email=None,
                no_libgen=True,
                dry_run=False,
                fetch_timeout=30.0,
            )
            self.assertEqual(summary["started_pending"], 3)
            self.assertEqual(summary["by_status"].get("fetched"), 2)
            self.assertEqual(summary["by_status"].get("fetch_failed"), 1)

            # Queue mutated in-place.
            rows = rab.read_queue(store / "queue.jsonl")
            by_id = {r["candidate_id"]: r for r in rows}
            self.assertEqual(by_id["a"]["status"], "fetched")
            self.assertEqual(by_id["b"]["status"], "fetch_failed")
            self.assertEqual(by_id["c"]["status"], "fetched")

            # Attempt manifest is present and credential-free.
            attempt = json.loads((store / "attempts" / "a.json").read_text())
            self.assertEqual(attempt["last_result"], "fetched")
            self.assertNotIn("token", attempt["stdout_snippet"].lower())
            self.assertNotIn("token", json.dumps(attempt).lower())

    def test_resumability_skips_fetched(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            stub = _write_stub(tmp, outcomes={"10.1/a": "ok"})
            _seed_queue(store, [_row("a", "10.1/a")])

            first = rab.run_batch(
                store=store, fetch_script=stub, limit=10, email=None,
                no_libgen=True, dry_run=False, fetch_timeout=30.0,
            )
            self.assertEqual(first["by_status"].get("fetched"), 1)

            # Force the queue status back to pending to simulate a stale queue;
            # the attempts file still says fetched, so the runner should
            # reconcile and skip.
            rows = rab.read_queue(store / "queue.jsonl")
            rows[0]["status"] = "pending"
            with (store / "queue.jsonl").open("w") as fh:
                for r in rows:
                    fh.write(json.dumps(r) + "\n")

            second = rab.run_batch(
                store=store, fetch_script=stub, limit=10, email=None,
                no_libgen=True, dry_run=False, fetch_timeout=30.0,
            )
            self.assertEqual(second["by_status"].get("skipped_already_done"), 1)


class TestDryRunDoesNotMutateQueue(unittest.TestCase):
    def test_dry_run_records_attempt_but_keeps_row_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            # Stub that always writes ok (so a non-dry-run path would mutate).
            stub = _write_stub(tmp, outcomes={"10.1/a": "ok"})
            _seed_queue(store, [_row("a", "10.1/a")])

            summary = rab.run_batch(
                store=store, fetch_script=stub, limit=10, email=None,
                no_libgen=True, dry_run=True, fetch_timeout=30.0,
            )
            self.assertEqual(summary["by_status"].get(rab.STATUS_DRY_RUN), 1)

            rows = rab.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "pending")

            attempt = json.loads((store / "attempts" / "a.json").read_text())
            self.assertEqual(attempt["last_result"], rab.STATUS_DRY_RUN)


class TestClassifyResult(unittest.TestCase):
    def test_no_manifest_returns_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            papers = Path(tmp) / "papers"
            papers.mkdir()
            status, summary = rab.classify_result(
                {"ok_subprocess": True, "returncode": 0, "stdout": "", "stderr": "",
                 "elapsed_seconds": 0.1, "timed_out": False},
                papers,
                "10.1/missing",
            )
            self.assertEqual(status, "fetch_failed")
            self.assertIsNone(summary["manifest_status"])

    def test_old_matching_manifest_still_classifies_as_fetched(self):
        with tempfile.TemporaryDirectory() as tmp:
            papers = Path(tmp) / "papers"
            slug = papers / "old-success"
            slug.mkdir(parents=True)
            (slug / "manifest.json").write_text(json.dumps({
                "status": "ok",
                "tier": "unpaywall",
                "doi": "10.1/old",
                "arxiv_id": None,
            }))

            status, summary = rab.classify_result(
                {"ok_subprocess": True, "returncode": 0, "stdout": "", "stderr": "",
                 "elapsed_seconds": 0.1, "timed_out": False},
                papers,
                "10.1/old",
            )
            self.assertEqual(status, "fetched")
            self.assertEqual(summary["manifest_slug"], "old-success")


if __name__ == "__main__":
    unittest.main()
