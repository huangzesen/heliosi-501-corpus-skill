#!/usr/bin/env python3
"""Resumable batch runner for the HelioSI literature acquisition queue.

Reads a queue produced by ``scripts/build_acquisition_queue.py``, picks the
first N rows whose ``status == pending``, and calls ``fetch_paper.py``
(from the academic-research utilities skill) once per row. Records the
outcome on disk so re-runs skip work that is already done.

Outputs live in an **external acquisition store** -- the directory passed
via ``--store``. The runner writes:

    store/
        queue.jsonl                  # in-place updated queue (atomic rewrite)
        queue.csv                    # CSV mirror, in-place updated
        queue.meta.json              # build metadata (unchanged here)
        attempts/<candidate_id>.json # per-row attempt manifest
        papers/<slug>/...            # downloaded PDFs (managed by fetch_paper)
        runs/<run_id>/summary.json   # one entry per batch run
        runs/<run_id>/stdout.log     # captured stdout from fetch_paper.py
        runs/<run_id>/stderr.log     # captured stderr from fetch_paper.py

Statuses written back into the queue:

    fetched                  fetch_paper.py reported status=ok
    fetch_failed             fetch_paper.py ran but reported a non-ok status
    skipped_already_done     a prior attempt was already fetched=ok
    no_supported_identifier  unchanged (the queue builder set this)
    pending                  unchanged (waiting for a future batch)

Resumability is achieved by two cheap mechanisms:

  1. Before invoking fetch_paper.py, the runner checks
     ``attempts/<candidate_id>.json`` -- if its last_result == "fetched"
     the row is marked skipped_already_done and counted, with no
     subprocess started.
  2. fetch_paper.py itself is idempotent on its ``papers/<slug>/``
     directory (manifest.json with status=ok short-circuits its tier
     loop). So even when the attempts file is missing we never
     re-download.

This script is **defense-in-depth around credentials**: it never reads,
prints, or stores secrets, never echoes environment variables, and only
forwards a single optional ``--email`` flag to fetch_paper.py. ADS
tokens are NOT used here (the queue has already been built from cached
discovery JSONL). Bibcode-only rows are passed over with status
``no_supported_identifier`` until a future ADS-resolver step lands.

Safe to re-run. Safe to interrupt -- the queue is rewritten atomically
after every row, so an interrupt at worst loses the in-flight row's
attempt manifest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Iterable, Optional


SCHEMA_VERSION = "heliosi-acquisition-run/1.0"

STATUS_PENDING = "pending"
STATUS_FETCHED = "fetched"
STATUS_FETCH_FAILED = "fetch_failed"
STATUS_SKIPPED_DONE = "skipped_already_done"
STATUS_NO_ID = "no_supported_identifier"
STATUS_DRY_RUN = "dry_run_metadata_only"  # transient -- queue row stays pending

DEFAULT_QUEUE_NAME = "queue.jsonl"
DEFAULT_CSV_NAME = "queue.csv"

# Cap the stdout/stderr we keep per row; the full log lives under runs/.
SNIPPET_CHARS = 4000


# ──────────────────────────────────────────────────────────
#  Queue read / write
# ──────────────────────────────────────────────────────────

def read_queue(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_queue_atomic(rows: list[dict], path: Path) -> None:
    """Rewrite ``queue.jsonl`` atomically (write to tmp, rename)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def write_csv_mirror(rows: list[dict], path: Path) -> None:
    """Best-effort CSV mirror; never fails the batch on CSV errors."""
    import csv
    if not rows:
        return
    fields = list(rows[0].keys())
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for row in rows:
                w.writerow(row)
        os.replace(tmp, path)
    except OSError:
        if tmp.exists():
            tmp.unlink()


# ──────────────────────────────────────────────────────────
#  Per-candidate attempt manifest
# ──────────────────────────────────────────────────────────

def attempt_path(store: Path, candidate_id: str) -> Path:
    return store / "attempts" / f"{candidate_id}.json"


def read_attempt(store: Path, candidate_id: str) -> Optional[dict]:
    p = attempt_path(store, candidate_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def write_attempt(store: Path, candidate_id: str, payload: dict) -> None:
    p = attempt_path(store, candidate_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


# ──────────────────────────────────────────────────────────
#  Row selection
# ──────────────────────────────────────────────────────────

def select_pending(
    rows: list[dict],
    limit: int,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    only_candidate_ids: Optional[set[str]] = None,
) -> list[dict]:
    """Return up to ``limit`` rows whose status is pending and that have an id.

    Optional filters:
        year_min, year_max -- inclusive year bounds; rows with year=None are dropped
        only_candidate_ids -- restrict to a specific set of candidate_id values
    """
    out = []
    for row in rows:
        if row.get("status") != STATUS_PENDING:
            continue
        if not row.get("preferred_identifier"):
            continue
        if only_candidate_ids is not None and row.get("candidate_id") not in only_candidate_ids:
            continue
        if year_min is not None or year_max is not None:
            year = row.get("year")
            if year is None:
                continue
            if year_min is not None and year < year_min:
                continue
            if year_max is not None and year > year_max:
                continue
        out.append(row)
        if len(out) >= limit:
            break
    return out


# ──────────────────────────────────────────────────────────
#  fetch_paper.py invocation
# ──────────────────────────────────────────────────────────

def _snippet(text: str, n: int = SNIPPET_CHARS) -> str:
    if text is None:
        return ""
    if len(text) <= n:
        return text
    return text[: n // 2] + f"\n...[truncated {len(text) - n} chars]...\n" + text[-n // 2 :]


def invoke_fetch_paper(
    fetch_script: Path,
    identifier: str,
    out_root: Path,
    email: Optional[str],
    no_libgen: bool,
    dry_run: bool,
    timeout: float,
) -> dict:
    """Run fetch_paper.py for one identifier. Returns a result dict.

    Never raises on subprocess failure; encodes errors in the result dict.
    Never echoes credentials -- ``email`` is the only forwarded value.
    """
    cmd = [sys.executable, str(fetch_script), identifier, "--out", str(out_root)]
    if email:
        cmd += ["--email", email]
    if no_libgen:
        cmd.append("--no-libgen")
    if dry_run:
        cmd.append("--dry-run")

    started = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok_subprocess": True,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "elapsed_seconds": round(time.time() - started, 3),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok_subprocess": False,
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "elapsed_seconds": round(time.time() - started, 3),
            "timed_out": True,
            "error": "timeout",
        }
    except OSError as exc:
        return {
            "ok_subprocess": False,
            "returncode": None,
            "stdout": "",
            "stderr": "",
            "elapsed_seconds": round(time.time() - started, 3),
            "timed_out": False,
            "error": f"oserror: {exc}",
        }


def classify_result(
    proc_result: dict, papers_root: Path, identifier: str
) -> tuple[str, dict]:
    """Translate subprocess result into a queue status + summary fragment.

    We look at fetch_paper.py's per-slug manifest.json when available --
    that file is the authoritative outcome record. If we cannot find a
    manifest (e.g., subprocess crashed before slug was known), we fall
    back to returncode.
    """
    summary: dict = {
        "returncode": proc_result.get("returncode"),
        "timed_out": proc_result.get("timed_out", False),
        "elapsed_seconds": proc_result.get("elapsed_seconds"),
    }
    if proc_result.get("error"):
        summary["subprocess_error"] = proc_result["error"]

    manifest_status = None
    manifest_tier = None
    manifest_slug = None
    if papers_root.exists():
        # fetch_paper.py prints the slug, but we don't parse stdout to
        # discover it. Instead, walk all manifests and match on the DOI or
        # arXiv id. Do not limit by mtime: fetch_paper.py is idempotent and
        # may legitimately short-circuit on an old status=ok manifest when a
        # prior attempts/<candidate_id>.json file is missing or stale.
        for manifest_path in papers_root.glob("*/manifest.json"):
            try:
                m = json.loads(manifest_path.read_text())
            except (json.JSONDecodeError, OSError):
                continue
            # Match on doi/arxiv_id if possible
            if identifier.lower().startswith("arxiv:"):
                aid = identifier.split(":", 1)[1].lower()
                if (m.get("arxiv_id") or "").lower() == aid:
                    manifest_status = m.get("status")
                    manifest_tier = m.get("tier")
                    manifest_slug = manifest_path.parent.name
                    break
            else:
                if (m.get("doi") or "").lower() == identifier.lower():
                    manifest_status = m.get("status")
                    manifest_tier = m.get("tier")
                    manifest_slug = manifest_path.parent.name
                    break

    summary["manifest_status"] = manifest_status
    summary["manifest_tier"] = manifest_tier
    summary["manifest_slug"] = manifest_slug

    if manifest_status == "ok":
        return STATUS_FETCHED, summary
    if manifest_status in {"fail", "error"}:
        return STATUS_FETCH_FAILED, summary
    # No manifest found -- if the subprocess exited cleanly assume failed,
    # since fetch_paper.py always writes a manifest on success or failure.
    if proc_result.get("ok_subprocess") and proc_result.get("returncode") == 0:
        return STATUS_FETCH_FAILED, summary
    return STATUS_FETCH_FAILED, summary


# ──────────────────────────────────────────────────────────
#  Batch driver
# ──────────────────────────────────────────────────────────

def run_batch(
    store: Path,
    fetch_script: Path,
    limit: int,
    email: Optional[str],
    no_libgen: bool,
    dry_run: bool,
    fetch_timeout: float,
    queue_name: str = DEFAULT_QUEUE_NAME,
    csv_name: str = DEFAULT_CSV_NAME,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    only_candidate_ids: Optional[set[str]] = None,
) -> dict:
    queue_path = store / queue_name
    csv_path = store / csv_name
    if not queue_path.exists():
        raise FileNotFoundError(f"queue not found at {queue_path}")

    rows = read_queue(queue_path)
    pending = select_pending(
        rows,
        limit,
        year_min=year_min,
        year_max=year_max,
        only_candidate_ids=only_candidate_ids,
    )

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    run_dir = store / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    papers_root = store / "papers"
    papers_root.mkdir(parents=True, exist_ok=True)

    stdout_log = run_dir / "stdout.log"
    stderr_log = run_dir / "stderr.log"

    by_status: dict[str, int] = {}
    attempts_recorded: list[dict] = []

    # Open run logs in append mode so an interrupt does not lose earlier rows.
    stdout_fh = stdout_log.open("a")
    stderr_fh = stderr_log.open("a")
    try:
        for row in pending:
            cid = row["candidate_id"]
            ident = row["preferred_identifier"]

            prior = read_attempt(store, cid)
            if prior and prior.get("last_result") == STATUS_FETCHED:
                # Defense in depth: queue says pending but attempts file
                # says fetched. Reconcile and skip.
                _update_row_status(rows, cid, STATUS_SKIPPED_DONE, note="reconciled from attempt manifest")
                by_status[STATUS_SKIPPED_DONE] = by_status.get(STATUS_SKIPPED_DONE, 0) + 1
                attempts_recorded.append({"candidate_id": cid, "status": STATUS_SKIPPED_DONE})
                write_queue_atomic(rows, queue_path)
                continue

            stdout_fh.write(f"\n=== {cid} {ident} ===\n")
            stdout_fh.flush()
            proc_result = invoke_fetch_paper(
                fetch_script=fetch_script,
                identifier=ident,
                out_root=papers_root,
                email=email,
                no_libgen=no_libgen,
                dry_run=dry_run,
                timeout=fetch_timeout,
            )
            stdout_fh.write(proc_result.get("stdout") or "")
            stderr_fh.write(f"\n=== {cid} {ident} ===\n")
            stderr_fh.write(proc_result.get("stderr") or "")
            stdout_fh.flush()
            stderr_fh.flush()

            new_status, summary = classify_result(proc_result, papers_root, ident)
            if dry_run:
                # Dry-run only resolves metadata; fetch_paper.py writes no
                # manifest. Record the attempt for visibility but DO NOT
                # mutate the queue row -- it stays pending for a real run.
                new_status = STATUS_DRY_RUN
            attempt_payload = {
                "schema_version": SCHEMA_VERSION,
                "candidate_id": cid,
                "preferred_identifier": ident,
                "identifier_kind": row.get("identifier_kind"),
                "title": row.get("title"),
                "year": row.get("year"),
                "run_id": run_id,
                "attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "last_result": new_status,
                "fetch_summary": summary,
                "stdout_snippet": _snippet(proc_result.get("stdout") or ""),
                "stderr_snippet": _snippet(proc_result.get("stderr") or ""),
                "options": {
                    "no_libgen": no_libgen,
                    "dry_run": dry_run,
                    "fetch_timeout": fetch_timeout,
                },
            }
            write_attempt(store, cid, attempt_payload)
            if not dry_run:
                _update_row_status(rows, cid, new_status, note=f"run:{run_id}")
            by_status[new_status] = by_status.get(new_status, 0) + 1
            attempts_recorded.append(
                {
                    "candidate_id": cid,
                    "preferred_identifier": ident,
                    "status": new_status,
                    "manifest_tier": summary.get("manifest_tier"),
                }
            )
            write_queue_atomic(rows, queue_path)
    finally:
        stdout_fh.close()
        stderr_fh.close()
        # Best-effort CSV refresh so it stays aligned with the JSONL.
        write_csv_mirror(rows, csv_path)

    summary_payload = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "started_pending": len(pending),
        "by_status": by_status,
        "attempts": attempts_recorded,
        "options": {
            "limit": limit,
            "no_libgen": no_libgen,
            "dry_run": dry_run,
            "fetch_timeout": fetch_timeout,
        },
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n"
    )
    return summary_payload


def _update_row_status(rows: list[dict], candidate_id: str, status: str, note: str = "") -> None:
    for row in rows:
        if row.get("candidate_id") == candidate_id:
            row["status"] = status
            if note:
                existing = row.get("notes") or ""
                row["notes"] = f"{existing}; {note}" if existing else note
            return


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

DEFAULT_FETCH_SCRIPT = Path(
    "/Users/huangzesen/.lingtai-tui/utilities/academic-research/scripts/fetch_paper.py"
)


def main(argv: list[str] | None = None) -> int:
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
        default=5,
        help="max pending rows to process this run (default: 5)",
    )
    p.add_argument(
        "--email",
        default=os.environ.get("LINGTAI_RESEARCH_EMAIL"),
        help="email forwarded to fetch_paper.py for Unpaywall politeness",
    )
    p.add_argument(
        "--no-libgen",
        action="store_true",
        help="forward --no-libgen to fetch_paper.py (recommended for smoke runs)",
    )
    p.add_argument(
        "--dry-run-fetch",
        action="store_true",
        help="forward --dry-run to fetch_paper.py (metadata only, no PDF download)",
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
        summary = run_batch(
            store=args.store,
            fetch_script=args.fetch_script,
            limit=args.limit,
            email=args.email,
            no_libgen=args.no_libgen,
            dry_run=args.dry_run_fetch,
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

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
