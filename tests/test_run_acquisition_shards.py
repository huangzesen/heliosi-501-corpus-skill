"""Tests for scripts/run_acquisition_shards.py.

The sharded runner partitions pending rows into N shards, runs fetch_paper.py
in parallel worker processes that never touch the shared queue.jsonl, and
merges shard results back into the queue from the parent process.

Tests use a stub fetch_paper.py that mirrors the real contract (writes a
papers/<slug>/manifest.json) so we exercise classify_result without a
network. Process-level parallelism is real, but workers are pointed at a
temp store so they cannot collide with anything else.
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
SCRIPT = BUNDLE / "scripts" / "run_acquisition_shards.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("run_acquisition_shards", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ras = _load_module()


# Stub fetch_paper.py. The OUTCOMES map drives ok/fail. We also append the
# pid to a shared log file so a test can prove subprocess parallelism happened
# (and that each shard ran a distinct worker process).
STUB_TEMPLATE = dedent("""\
    #!/usr/bin/env python3
    import argparse, json, os, sys, time
    from pathlib import Path

    OUTCOMES = {OUTCOMES_JSON}
    PIDLOG = {PIDLOG_LITERAL}

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

    if PIDLOG:
        with open(PIDLOG, "a") as fh:
            fh.write(json.dumps({"pid": os.getpid(), "ppid": os.getppid(), "ident": ident}) + "\\n")

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
    sys.exit(0)
""")


def _write_stub(tmp: Path, outcomes: dict, pidlog: Path | None = None) -> Path:
    path = tmp / "fetch_paper_stub.py"
    body = STUB_TEMPLATE.replace("{OUTCOMES_JSON}", json.dumps(outcomes))
    # PIDLOG must render as a valid Python literal (None or "path/to/file"),
    # not JSON's null -- the stub is Python source, not JSON.
    pidlog_literal = repr(str(pidlog)) if pidlog else "None"
    body = body.replace("{PIDLOG_LITERAL}", pidlog_literal)
    path.write_text(body)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return path


def _seed_queue(store: Path, rows: list[dict]) -> None:
    store.mkdir(parents=True, exist_ok=True)
    with (store / "queue.jsonl").open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")


def _row(cid, identifier, kind="doi", status="pending", year=2020):
    return {
        "candidate_id": cid,
        "cell": "P-test",
        "source": "test",
        "title": f"title for {cid}",
        "year": year,
        "doi": identifier if (kind == "doi" and identifier) else None,
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


class TestPartitioning(unittest.TestCase):
    def test_partition_round_robin_balances_shards(self):
        rows = [_row(f"r{i}", f"10.1/{i}") for i in range(7)]
        shards = ras.partition_rows(rows, workers=3)
        self.assertEqual(len(shards), 3)
        self.assertEqual(sum(len(s) for s in shards), 7)
        # Round-robin: shard sizes differ by at most 1.
        sizes = sorted(len(s) for s in shards)
        self.assertLessEqual(sizes[-1] - sizes[0], 1)

    def test_partition_workers_capped_to_row_count(self):
        rows = [_row("r0", "10.1/0"), _row("r1", "10.1/1")]
        shards = ras.partition_rows(rows, workers=5)
        # No empty shards: at most one shard per row.
        self.assertEqual(len(shards), 2)
        self.assertTrue(all(len(s) >= 1 for s in shards))

    def test_partition_empty(self):
        self.assertEqual(ras.partition_rows([], workers=4), [])


class TestRunShardedHappyPath(unittest.TestCase):
    def test_ok_fail_merge(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            pidlog = tmp / "pids.jsonl"
            stub = _write_stub(
                tmp,
                outcomes={
                    "10.1/a": "ok",
                    "10.1/b": "fail",
                    "10.1/c": "ok",
                    "10.1/d": "fail",
                    "arxiv:2301.00001": "ok",
                },
                pidlog=pidlog,
            )
            _seed_queue(
                store,
                [
                    _row("a", "10.1/a"),
                    _row("b", "10.1/b"),
                    _row("c", "10.1/c"),
                    _row("d", "10.1/d"),
                    _row("e", "arxiv:2301.00001", kind="arxiv"),
                ],
            )
            summary = ras.run_sharded(
                store=store,
                fetch_script=stub,
                limit=10,
                workers=3,
                email=None,
                no_libgen=True,
                fetch_timeout=30.0,
            )

            self.assertEqual(summary["selected_for_run"], 5)
            self.assertEqual(summary["by_status"].get("fetched"), 3)
            self.assertEqual(summary["by_status"].get("fetch_failed"), 2)
            self.assertEqual(summary["workers_used"], 3)

            # Queue updated by parent with merged statuses.
            rows = ras.read_queue(store / "queue.jsonl")
            by_id = {r["candidate_id"]: r for r in rows}
            self.assertEqual(by_id["a"]["status"], "fetched")
            self.assertEqual(by_id["b"]["status"], "fetch_failed")
            self.assertEqual(by_id["c"]["status"], "fetched")
            self.assertEqual(by_id["d"]["status"], "fetch_failed")
            self.assertEqual(by_id["e"]["status"], "fetched")

            # Shard files exist under the run dir.
            run_dir = store / "runs" / f"{summary['run_id']}-sharded-acquisition"
            shard_dir = run_dir / "shards"
            self.assertTrue(shard_dir.is_dir(), shard_dir)
            # Use exact patterns: "shard-XX.jsonl" matches shards and results
            # both via "shard-*.jsonl", so we filter the input shard glob to
            # exclude the .results.jsonl files.
            all_jsonls = sorted(shard_dir.glob("shard-*.jsonl"))
            shard_jsonls = [p for p in all_jsonls if not p.name.endswith(".results.jsonl")]
            shard_results = sorted(shard_dir.glob("shard-*.results.jsonl"))
            self.assertEqual(len(shard_jsonls), 3, [p.name for p in all_jsonls])
            self.assertEqual(len(shard_results), 3)

            # Per-candidate attempt manifests exist and are credential-free.
            for cid in ["a", "b", "c", "d", "e"]:
                attempt = json.loads((store / "attempts" / f"{cid}.json").read_text())
                self.assertIn(attempt["last_result"], {"fetched", "fetch_failed"})
                self.assertNotIn("token", json.dumps(attempt).lower())

            # Subprocesses ran from at least 2 distinct PIDs (real parallelism).
            pids = set()
            with pidlog.open() as fh:
                for line in fh:
                    pids.add(json.loads(line)["pid"])
            self.assertGreaterEqual(len(pids), 2, f"only one pid observed: {pids}")


class TestQueueNotMutatedDuringShards(unittest.TestCase):
    """The shared queue.jsonl must not be touched until the parent merges.

    We snapshot queue.jsonl mtime + bytes right after partitioning and confirm
    that workers (which we trigger by running through run_sharded with a tiny
    stub) never wrote to it before the merge phase. We assert this indirectly
    by observing: after run_sharded() returns, the queue has exactly ONE
    rewrite generation -- not one-per-row -- so its mtime equals the merge
    step's mtime, which is later than every shard result file's mtime.
    """

    def test_queue_written_after_all_shard_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            stub = _write_stub(
                tmp,
                outcomes={f"10.1/{i}": "ok" for i in range(6)},
            )
            _seed_queue(
                store,
                [_row(f"r{i}", f"10.1/{i}") for i in range(6)],
            )

            summary = ras.run_sharded(
                store=store,
                fetch_script=stub,
                limit=10,
                workers=3,
                email=None,
                no_libgen=True,
                fetch_timeout=30.0,
            )

            run_dir = store / "runs" / f"{summary['run_id']}-sharded-acquisition"
            shard_dir = run_dir / "shards"
            shard_result_mtimes = [
                p.stat().st_mtime for p in shard_dir.glob("shard-*.results.jsonl")
            ]
            self.assertTrue(shard_result_mtimes)
            queue_mtime = (store / "queue.jsonl").stat().st_mtime
            self.assertGreaterEqual(
                queue_mtime,
                max(shard_result_mtimes),
                "queue.jsonl was written before all shard results finished -- "
                "workers may be mutating the shared queue",
            )


class TestSelectionFilters(unittest.TestCase):
    def test_limit_caps_selection_before_shard(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            stub = _write_stub(tmp, outcomes={f"10.1/{i}": "ok" for i in range(10)})
            _seed_queue(
                store,
                [_row(f"r{i}", f"10.1/{i}") for i in range(10)],
            )
            summary = ras.run_sharded(
                store=store,
                fetch_script=stub,
                limit=4,
                workers=2,
                email=None,
                no_libgen=True,
                fetch_timeout=30.0,
            )
            self.assertEqual(summary["selected_for_run"], 4)
            self.assertEqual(summary["by_status"].get("fetched"), 4)

            # Remaining 6 must still be pending.
            rows = ras.read_queue(store / "queue.jsonl")
            pending = [r for r in rows if r["status"] == "pending"]
            self.assertEqual(len(pending), 6)

    def test_year_filter_passed_through(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            stub = _write_stub(tmp, outcomes={"10.1/new": "ok", "10.1/old": "ok"})
            _seed_queue(
                store,
                [
                    {**_row("old", "10.1/old"), "year": 1990},
                    {**_row("new", "10.1/new"), "year": 2020},
                ],
            )
            summary = ras.run_sharded(
                store=store,
                fetch_script=stub,
                limit=10,
                workers=2,
                email=None,
                no_libgen=True,
                fetch_timeout=30.0,
                year_min=2000,
            )
            self.assertEqual(summary["selected_for_run"], 1)
            rows = ras.read_queue(store / "queue.jsonl")
            by_id = {r["candidate_id"]: r for r in rows}
            self.assertEqual(by_id["new"]["status"], "fetched")
            self.assertEqual(by_id["old"]["status"], "pending")

    def test_skips_no_supported_identifier_and_non_pending(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            stub = _write_stub(tmp, outcomes={"10.1/a": "ok"})
            _seed_queue(
                store,
                [
                    # candidate with no preferred_identifier -> must be skipped
                    {
                        **_row("noid", None, kind="bibcode"),
                        "status": "no_supported_identifier",
                        "preferred_identifier": None,
                    },
                    # already fetched -> must be skipped
                    _row("done", "10.1/done", status="fetched"),
                    # pending with id -> picked up
                    _row("a", "10.1/a"),
                ],
            )
            summary = ras.run_sharded(
                store=store,
                fetch_script=stub,
                limit=10,
                workers=2,
                email=None,
                no_libgen=True,
                fetch_timeout=30.0,
            )
            self.assertEqual(summary["selected_for_run"], 1)
            rows = ras.read_queue(store / "queue.jsonl")
            by_id = {r["candidate_id"]: r for r in rows}
            self.assertEqual(by_id["noid"]["status"], "no_supported_identifier")
            self.assertEqual(by_id["done"]["status"], "fetched")
            self.assertEqual(by_id["a"]["status"], "fetched")


class TestResumability(unittest.TestCase):
    def test_prior_fetched_attempt_reconciled_in_parent(self):
        """If attempts/<cid>.json says fetched, parent reconciles to
        skipped_already_done without spawning a worker for it."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            # Stub would say "ok" for both, but we want to prove "done" is NOT
            # re-invoked. We assert this by checking that the pid log only ever
            # logs the second identifier.
            pidlog = tmp / "pids.jsonl"
            stub = _write_stub(
                tmp,
                outcomes={"10.1/done": "ok", "10.1/new": "ok"},
                pidlog=pidlog,
            )
            _seed_queue(
                store,
                [
                    _row("done", "10.1/done"),
                    _row("new", "10.1/new"),
                ],
            )
            # Pre-seed an attempt manifest marking "done" as already fetched.
            attempts_dir = store / "attempts"
            attempts_dir.mkdir(parents=True, exist_ok=True)
            (attempts_dir / "done.json").write_text(
                json.dumps({"last_result": "fetched", "candidate_id": "done"})
            )

            summary = ras.run_sharded(
                store=store,
                fetch_script=stub,
                limit=10,
                workers=2,
                email=None,
                no_libgen=True,
                fetch_timeout=30.0,
            )
            self.assertEqual(summary["by_status"].get("skipped_already_done"), 1)
            self.assertEqual(summary["by_status"].get("fetched"), 1)

            # Only the "new" identifier should have been sent to the stub.
            idents = []
            with pidlog.open() as fh:
                for line in fh:
                    idents.append(json.loads(line)["ident"])
            self.assertEqual(idents, ["10.1/new"])


class TestArgsForwardedToFetchScript(unittest.TestCase):
    def test_email_forwarded_to_subprocess(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            # The stub records argv into a file so we can introspect.
            stub = tmp / "fetch_paper_stub.py"
            stub.write_text(dedent("""\
                #!/usr/bin/env python3
                import json, sys, os
                from pathlib import Path
                argv_log = Path(os.environ["ARGV_LOG"])
                with argv_log.open("a") as fh:
                    fh.write(json.dumps(sys.argv) + "\\n")
                # Write a manifest matching the identifier so classify_result is ok.
                import argparse
                p = argparse.ArgumentParser()
                p.add_argument("identifier")
                p.add_argument("--out", required=True)
                p.add_argument("--email", default=None)
                p.add_argument("--no-libgen", action="store_true")
                p.add_argument("--dry-run", action="store_true")
                args = p.parse_args()
                out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
                slug = "x"
                (out / slug).mkdir(exist_ok=True)
                (out / slug / "manifest.json").write_text(json.dumps({
                    "status": "ok", "tier": "unpaywall",
                    "doi": args.identifier.lower(), "arxiv_id": None,
                }))
                sys.exit(0)
            """))
            stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
            argv_log = tmp / "argv.jsonl"
            os.environ["ARGV_LOG"] = str(argv_log)
            try:
                _seed_queue(store, [_row("a", "10.1/a")])
                ras.run_sharded(
                    store=store,
                    fetch_script=stub,
                    limit=10,
                    workers=1,
                    email="researcher@example.org",
                    no_libgen=True,
                    fetch_timeout=30.0,
                )
            finally:
                del os.environ["ARGV_LOG"]

            argv = json.loads(argv_log.read_text().strip().splitlines()[0])
            self.assertIn("--email", argv)
            self.assertEqual(argv[argv.index("--email") + 1], "researcher@example.org")
            self.assertIn("--no-libgen", argv)


if __name__ == "__main__":
    unittest.main()
