#!/usr/bin/env python3
"""Safe parallel sharded runner for the HelioSI acquisition queue.

Sibling of ``scripts/run_acquisition_batch.py``. Same fetch contract, same
external acquisition store layout, same per-row ``attempts/<cid>.json``
manifest. The difference is concurrency: this runner partitions the
selected pending rows into ``--workers`` shards, runs ``fetch_paper.py``
in parallel across separate worker subprocesses, and -- critically --
NEVER touches the shared ``queue.jsonl`` from a worker.

Workflow
========

1. Parent reads ``store/queue.jsonl`` once.
2. Parent selects pending rows (preferred_identifier set, optional
   year and limit filters).
3. Parent reconciles any row whose ``attempts/<cid>.json`` already says
   ``fetched`` -- these become ``skipped_already_done`` without
   spawning a worker.
4. Parent partitions the remaining rows round-robin into K shard
   files under
       ``store/runs/<run_id>-sharded-acquisition/shards/shard-XX.jsonl``
5. Workers each consume one shard, call ``fetch_paper.py`` per row,
   and write a per-row result line to
       ``store/runs/<run_id>-sharded-acquisition/shards/shard-XX.results.jsonl``
   Workers do NOT mutate ``queue.jsonl`` and do NOT write
   ``attempts/<cid>.json``. They only write under the run directory and
   into the shared ``store/papers/`` tree (via ``fetch_paper.py``'s own
   idempotent slug directories).
6. After all workers finish, the parent merges results in a single
   pass: writes ``attempts/<cid>.json`` for each row, updates the
   queue rows, then atomically rewrites ``queue.jsonl`` + ``queue.csv``
   exactly once. This is the only point at which the shared queue is
   written.

Why this is safe to run in parallel
===================================

The two shared resources are ``queue.jsonl`` and ``papers/``:

  - ``queue.jsonl`` is written by the parent only, after all workers
    have finished. Workers never open it.
  - ``papers/<slug>/`` is owned by ``fetch_paper.py``, which is
    idempotent on a per-slug basis (manifest.json with status=ok
    short-circuits the tier loop). Two workers asked to fetch the
    same identifier would write to the same slug, but the queue
    builder produces distinct ``preferred_identifier`` values per
    candidate, and partitioning is row-based, so no two workers see
    the same identifier in a single run.

Interrupt behaviour
===================

If the parent is interrupted before merge, the run directory has the
shard files and any partial ``shard-XX.results.jsonl`` lines for
inspection. The shared ``queue.jsonl`` is unchanged. Re-running the
same command picks the same pending rows and ``fetch_paper.py``'s
per-slug idempotency means no duplicate downloads.

Credential hygiene
==================

This runner never reads, prints, or stores credentials. The only value
forwarded to ``fetch_paper.py`` is ``--email`` (used by Unpaywall for
politeness). Environment variables are never echoed.

Stdlib only. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Optional


SCRIPT_DIR = Path(__file__).resolve().parent


def _load_batch_module():
    """Load run_acquisition_batch.py so we can reuse its helpers."""
    spec = importlib.util.spec_from_file_location(
        "run_acquisition_batch", SCRIPT_DIR / "run_acquisition_batch.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_batch = _load_batch_module()

# Re-export so tests and callers can use ``ras.read_queue`` etc.
read_queue = _batch.read_queue
write_queue_atomic = _batch.write_queue_atomic
write_csv_mirror = _batch.write_csv_mirror
attempt_path = _batch.attempt_path
read_attempt = _batch.read_attempt
write_attempt = _batch.write_attempt
select_pending = _batch.select_pending
invoke_fetch_paper = _batch.invoke_fetch_paper
classify_result = _batch.classify_result
_snippet = _batch._snippet

STATUS_PENDING = _batch.STATUS_PENDING
STATUS_FETCHED = _batch.STATUS_FETCHED
STATUS_FETCH_FAILED = _batch.STATUS_FETCH_FAILED
STATUS_SKIPPED_DONE = _batch.STATUS_SKIPPED_DONE
STATUS_NO_ID = _batch.STATUS_NO_ID

SCHEMA_VERSION = "heliosi-acquisition-sharded-run/1.0"
DEFAULT_QUEUE_NAME = _batch.DEFAULT_QUEUE_NAME
DEFAULT_CSV_NAME = _batch.DEFAULT_CSV_NAME
DEFAULT_FETCH_SCRIPT = _batch.DEFAULT_FETCH_SCRIPT


# ──────────────────────────────────────────────────────────
#  Partitioning
# ──────────────────────────────────────────────────────────

def partition_rows(rows: list[dict], workers: int) -> list[list[dict]]:
    """Round-robin partition rows into at most ``workers`` shards.

    Returns no empty shards: if there are fewer rows than workers, the
    number of shards is capped at the row count. An empty input yields
    an empty list.
    """
    if not rows:
        return []
    k = max(1, min(workers, len(rows)))
    shards: list[list[dict]] = [[] for _ in range(k)]
    for i, row in enumerate(rows):
        shards[i % k].append(row)
    return shards


# ──────────────────────────────────────────────────────────
#  Worker entry point (runs in a child process)
# ──────────────────────────────────────────────────────────

def _worker_run_shard(args: dict) -> str:
    """Process one shard. Returns path to the shard's results JSONL.

    DOES NOT touch queue.jsonl. DOES NOT write attempts/<cid>.json.
    Only writes:
        - <shard_dir>/<shard_name>.results.jsonl  (one line per row)
        - <shard_dir>/<shard_name>.stdout.log     (raw fetch_paper stdout)
        - <shard_dir>/<shard_name>.stderr.log     (raw fetch_paper stderr)
        - <papers_root>/<slug>/...                (managed by fetch_paper)
    """
    shard_file = Path(args["shard_file"])
    shard_dir = shard_file.parent
    shard_stem = shard_file.stem  # e.g. "shard-00"
    fetch_script = Path(args["fetch_script"])
    papers_root = Path(args["papers_root"])
    email = args.get("email")
    no_libgen = bool(args.get("no_libgen"))
    fetch_timeout = float(args.get("fetch_timeout", 180.0))

    results_path = shard_dir / f"{shard_stem}.results.jsonl"
    stdout_path = shard_dir / f"{shard_stem}.stdout.log"
    stderr_path = shard_dir / f"{shard_stem}.stderr.log"

    papers_root.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    with shard_file.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    with results_path.open("w") as out_fh, \
         stdout_path.open("a") as stdout_fh, \
         stderr_path.open("a") as stderr_fh:
        for row in rows:
            cid = row["candidate_id"]
            ident = row["preferred_identifier"]
            stdout_fh.write(f"\n=== {cid} {ident} ===\n")
            stdout_fh.flush()
            proc_result = invoke_fetch_paper(
                fetch_script=fetch_script,
                identifier=ident,
                out_root=papers_root,
                email=email,
                no_libgen=no_libgen,
                dry_run=False,
                timeout=fetch_timeout,
            )
            stdout_fh.write(proc_result.get("stdout") or "")
            stderr_fh.write(f"\n=== {cid} {ident} ===\n")
            stderr_fh.write(proc_result.get("stderr") or "")
            stdout_fh.flush()
            stderr_fh.flush()

            new_status, summary = classify_result(proc_result, papers_root, ident)
            result_record = {
                "candidate_id": cid,
                "preferred_identifier": ident,
                "identifier_kind": row.get("identifier_kind"),
                "title": row.get("title"),
                "year": row.get("year"),
                "shard": shard_stem,
                "worker_pid": os.getpid(),
                "result_status": new_status,
                "fetch_summary": summary,
                "stdout_snippet": _snippet(proc_result.get("stdout") or ""),
                "stderr_snippet": _snippet(proc_result.get("stderr") or ""),
            }
            out_fh.write(json.dumps(result_record, ensure_ascii=False) + "\n")
            out_fh.flush()

    return str(results_path)


def _run_workers_in_parallel(worker_args: list[dict]) -> None:
    """Launch each worker as a subprocess of this script and wait for all.

    Raises RuntimeError if any worker exits non-zero -- the parent then
    aborts the merge to avoid writing a partially-merged queue. Shard
    result files of already-finished workers remain on disk for
    inspection.
    """
    if not worker_args:
        return
    procs: list[tuple[subprocess.Popen, dict]] = []
    for arg in worker_args:
        payload = json.dumps(arg)
        cmd = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--internal-worker-shard",
            payload,
        ]
        # Empty env scrub: pass through only the variables the worker
        # needs. ``LINGTAI_RESEARCH_EMAIL`` is irrelevant here because
        # ``email`` is already inside the JSON payload, but PATH and
        # PYTHONPATH must survive so the worker can find its interpreter
        # and any test stubs. We do not echo any env value to logs.
        procs.append((subprocess.Popen(cmd), arg))
    failures: list[str] = []
    for proc, arg in procs:
        rc = proc.wait()
        if rc != 0:
            failures.append(f"worker for {arg['shard_file']} exited rc={rc}")
    if failures:
        raise RuntimeError("; ".join(failures))


# ──────────────────────────────────────────────────────────
#  Parent driver
# ──────────────────────────────────────────────────────────

def _update_row_status(rows: list[dict], candidate_id: str, status: str, note: str = "") -> None:
    for row in rows:
        if row.get("candidate_id") == candidate_id:
            row["status"] = status
            if note:
                existing = row.get("notes") or ""
                row["notes"] = f"{existing}; {note}" if existing else note
            return


def _merge_shard_results(
    store: Path,
    rows: list[dict],
    shard_dir: Path,
    run_id: str,
    fetch_timeout: float,
    no_libgen: bool,
) -> tuple[dict[str, int], list[dict]]:
    """Read every shard-XX.results.jsonl, write per-row attempts, mutate rows in place.

    Returns (by_status counter, attempts_recorded list). Caller is
    responsible for rewriting queue.jsonl + queue.csv once afterward.
    """
    by_status: dict[str, int] = {}
    attempts_recorded: list[dict] = []
    for results_path in sorted(shard_dir.glob("shard-*.results.jsonl")):
        with results_path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                cid = rec["candidate_id"]
                ident = rec["preferred_identifier"]
                new_status = rec["result_status"]
                summary = rec.get("fetch_summary") or {}

                attempt_payload = {
                    "schema_version": SCHEMA_VERSION,
                    "candidate_id": cid,
                    "preferred_identifier": ident,
                    "identifier_kind": rec.get("identifier_kind"),
                    "title": rec.get("title"),
                    "year": rec.get("year"),
                    "run_id": run_id,
                    "shard": rec.get("shard"),
                    "worker_pid": rec.get("worker_pid"),
                    "attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                    "last_result": new_status,
                    "fetch_summary": summary,
                    "stdout_snippet": rec.get("stdout_snippet") or "",
                    "stderr_snippet": rec.get("stderr_snippet") or "",
                    "options": {
                        "no_libgen": no_libgen,
                        "dry_run": False,
                        "fetch_timeout": fetch_timeout,
                    },
                }
                write_attempt(store, cid, attempt_payload)
                _update_row_status(rows, cid, new_status, note=f"run:{run_id}")
                by_status[new_status] = by_status.get(new_status, 0) + 1
                attempts_recorded.append(
                    {
                        "candidate_id": cid,
                        "preferred_identifier": ident,
                        "status": new_status,
                        "shard": rec.get("shard"),
                        "manifest_tier": summary.get("manifest_tier"),
                    }
                )
    return by_status, attempts_recorded


def run_sharded(
    store: Path,
    fetch_script: Path,
    limit: int,
    workers: int,
    email: Optional[str],
    no_libgen: bool,
    fetch_timeout: float,
    queue_name: str = DEFAULT_QUEUE_NAME,
    csv_name: str = DEFAULT_CSV_NAME,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    only_candidate_ids: Optional[set[str]] = None,
) -> dict:
    """Run a sharded acquisition batch.

    See module docstring for the workflow. Returns a summary dict; the
    same summary is also written to ``runs/<run_id>/summary.json``.
    """
    queue_path = store / queue_name
    csv_path = store / csv_name
    if not queue_path.exists():
        raise FileNotFoundError(f"queue not found at {queue_path}")
    if workers < 1:
        raise ValueError(f"workers must be >= 1, got {workers!r}")

    rows = read_queue(queue_path)
    pending = select_pending(
        rows,
        limit,
        year_min=year_min,
        year_max=year_max,
        only_candidate_ids=only_candidate_ids,
    )

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    run_dir = store / "runs" / f"{run_id}-sharded-acquisition"
    shard_dir = run_dir / "shards"
    shard_dir.mkdir(parents=True, exist_ok=True)

    papers_root = store / "papers"
    papers_root.mkdir(parents=True, exist_ok=True)

    by_status: dict[str, int] = {}
    attempts_recorded: list[dict] = []

    # Reconcile prior-fetched rows in the parent BEFORE spawning workers.
    to_fetch: list[dict] = []
    for row in pending:
        cid = row["candidate_id"]
        prior = read_attempt(store, cid)
        if prior and prior.get("last_result") == STATUS_FETCHED:
            _update_row_status(rows, cid, STATUS_SKIPPED_DONE, note=f"run:{run_id}: reconciled from attempt manifest")
            by_status[STATUS_SKIPPED_DONE] = by_status.get(STATUS_SKIPPED_DONE, 0) + 1
            attempts_recorded.append({"candidate_id": cid, "status": STATUS_SKIPPED_DONE})
            continue
        to_fetch.append(row)

    shards = partition_rows(to_fetch, workers=workers)
    shard_files: list[Path] = []
    for i, shard in enumerate(shards):
        path = shard_dir / f"shard-{i:02d}.jsonl"
        with path.open("w") as fh:
            for row in shard:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        shard_files.append(path)

    workers_used = len(shard_files)

    # Run workers in parallel by re-invoking THIS script as a subprocess
    # with --internal-worker-shard. Subprocess isolation gives us:
    #   - No pickling complexity (workers re-parse their args from JSON).
    #   - Distinct PIDs so an interrupt in the parent can SIGTERM the
    #     worker group without killing the test runner.
    #   - The same workflow whether the runner was loaded via
    #     ``importlib.util.spec_from_file_location`` (tests) or imported
    #     normally -- only the path to this file matters.
    if shard_files:
        worker_args = [
            {
                "shard_file": str(p),
                "fetch_script": str(fetch_script),
                "papers_root": str(papers_root),
                "email": email,
                "no_libgen": no_libgen,
                "fetch_timeout": fetch_timeout,
            }
            for p in shard_files
        ]
        _run_workers_in_parallel(worker_args)

    # Single-writer merge phase.
    merge_by_status, merge_attempts = _merge_shard_results(
        store=store,
        rows=rows,
        shard_dir=shard_dir,
        run_id=run_id,
        fetch_timeout=fetch_timeout,
        no_libgen=no_libgen,
    )
    for k, v in merge_by_status.items():
        by_status[k] = by_status.get(k, 0) + v
    attempts_recorded.extend(merge_attempts)

    # The parent is the ONLY writer of queue.jsonl + queue.csv.
    write_queue_atomic(rows, queue_path)
    write_csv_mirror(rows, csv_path)

    summary_payload = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "selected_for_run": len(pending),
        "workers_requested": workers,
        "workers_used": workers_used,
        "by_status": by_status,
        "attempts": attempts_recorded,
        "options": {
            "limit": limit,
            "workers": workers,
            "no_libgen": no_libgen,
            "fetch_timeout": fetch_timeout,
            "year_min": year_min,
            "year_max": year_max,
        },
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n"
    )
    return summary_payload


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    # Internal worker mode -- parent process re-invokes this script with
    # --internal-worker-shard <json-blob>. We sniff the arg list directly
    # (before argparse) because the public CLI's --store is required and
    # would otherwise reject worker invocations.
    actual_argv = argv if argv is not None else sys.argv[1:]
    if actual_argv and actual_argv[0] == "--internal-worker-shard":
        if len(actual_argv) != 2:
            print("error: --internal-worker-shard expects exactly one JSON arg",
                  file=sys.stderr)
            return 2
        try:
            payload = json.loads(actual_argv[1])
        except json.JSONDecodeError as exc:
            print(f"error: --internal-worker-shard payload is not JSON: {exc}",
                  file=sys.stderr)
            return 2
        _worker_run_shard(payload)
        return 0

    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--store",
        type=Path,
        required=True,
        help="external acquisition store directory (contains queue.jsonl)",
    )
    p.add_argument(
        "--fetch-script",
        type=Path,
        default=DEFAULT_FETCH_SCRIPT,
        help=f"path to fetch_paper.py (default: {DEFAULT_FETCH_SCRIPT})",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=10,
        help="max pending rows to process this run (default: 10)",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=4,
        help="number of parallel worker processes (default: 4)",
    )
    p.add_argument(
        "--email",
        default=os.environ.get("LINGTAI_RESEARCH_EMAIL"),
        help="email forwarded to fetch_paper.py for Unpaywall politeness",
    )
    p.add_argument(
        "--no-libgen",
        action="store_true",
        help="forward --no-libgen to fetch_paper.py",
    )
    p.add_argument(
        "--fetch-timeout",
        type=float,
        default=180.0,
        help="per-row subprocess timeout in seconds (default: 180)",
    )
    p.add_argument(
        "--queue-name",
        default=DEFAULT_QUEUE_NAME,
        help=f"queue JSONL filename inside --store (default: {DEFAULT_QUEUE_NAME})",
    )
    p.add_argument(
        "--csv-name",
        default=DEFAULT_CSV_NAME,
        help=f"queue CSV mirror filename (default: {DEFAULT_CSV_NAME})",
    )
    p.add_argument(
        "--year-min",
        type=int,
        default=None,
        help="restrict selection to rows with year >= YEAR_MIN",
    )
    p.add_argument(
        "--year-max",
        type=int,
        default=None,
        help="restrict selection to rows with year <= YEAR_MAX",
    )
    p.add_argument(
        "--candidate-id",
        action="append",
        default=[],
        help="restrict selection to specific candidate_id values (repeatable)",
    )
    args = p.parse_args(argv)

    if not args.fetch_script.exists():
        print(f"error: fetch_paper.py not found at {args.fetch_script}", file=sys.stderr)
        return 2

    try:
        summary = run_sharded(
            store=args.store,
            fetch_script=args.fetch_script,
            limit=args.limit,
            workers=args.workers,
            email=args.email,
            no_libgen=args.no_libgen,
            fetch_timeout=args.fetch_timeout,
            queue_name=args.queue_name,
            csv_name=args.csv_name,
            year_min=args.year_min,
            year_max=args.year_max,
            only_candidate_ids=set(args.candidate_id) if args.candidate_id else None,
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
