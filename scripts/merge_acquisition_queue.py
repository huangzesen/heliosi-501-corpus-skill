#!/usr/bin/env python3
"""Merge new discovery candidates into an existing acquisition queue.

This is the **safe** companion to ``build_acquisition_queue.py``. The
build script is a pure transform (candidates -> queue). Once the queue
has been handed to ``run_acquisition_batch.py``, individual rows acquire
state: ``status`` (e.g. ``fetched`` / ``fetch_failed``), free-text
``notes``, and ``queued_at_utc``. Re-running the build script over a
superset of candidates would clobber that state.

This merger reads an existing ``queue.jsonl``, normalises a new batch of
discovery candidates using the same helpers as the build script, then:

* preserves every existing row **bit-for-bit** (status, notes,
  queued_at_utc, and any other columns) when its ``candidate_id``
  re-appears in the new batch,
* appends rows for candidate_ids not seen in the existing queue,
* leaves existing-only rows (no longer surfaced by discovery) untouched.

Output (``queue.jsonl`` + ``queue.csv``) is written via a temp-file +
``os.replace`` pair so a partial write cannot leave a half-rewritten
queue on disk. ``queue.meta.json`` records the merge summary.

The script is stdlib-only and never prints, logs, or stores any
credential value.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = "heliosi-acquisition-queue/1.0"

DEFAULT_QUEUE_NAME = "queue.jsonl"
DEFAULT_CSV_NAME = "queue.csv"
DEFAULT_META_NAME = "queue.meta.json"


# ──────────────────────────────────────────────────────────
#  Load sibling build_acquisition_queue.py without requiring a
#  package install. Mirrors how tests/test_build_acquisition_queue.py
#  imports the script.
# ──────────────────────────────────────────────────────────

_HERE = Path(__file__).resolve().parent
_BAQ_PATH = _HERE / "build_acquisition_queue.py"


def _load_baq():
    spec = importlib.util.spec_from_file_location(
        "build_acquisition_queue", _BAQ_PATH
    )
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise RuntimeError(f"cannot load {_BAQ_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


baq = _load_baq()


# ──────────────────────────────────────────────────────────
#  Existing-queue loader
# ──────────────────────────────────────────────────────────

def load_existing_queue(path: Path) -> list[dict]:
    """Read an existing queue.jsonl.

    Missing file is treated as an empty queue (fresh-build path). Blank
    lines and JSON parse errors are skipped silently to match the
    forgiving discovery-ingest behaviour in build_acquisition_queue.
    """
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


# ──────────────────────────────────────────────────────────
#  Merge
# ──────────────────────────────────────────────────────────

def merge_rows(
    existing: list[dict],
    new_candidates: list[dict],
    now_iso: str,
    annotate_resurfaced: bool = False,
) -> tuple[list[dict], dict]:
    """Combine existing + new rows.

    Returns ``(merged_rows, counts)`` where counts has:

        existing_preserved   rows from the existing queue kept as-is
        new_appended         brand-new candidate_ids added with queued_at_utc=now
        duplicate_skipped    new candidates that collided with existing ids
        total_after_merge    len(merged_rows)

    Sort order: existing rows first (in their original order), then new
    appended rows in their normalized sort order. We deliberately do NOT
    re-sort the existing rows -- the user may rely on their current
    order, and run_acquisition_batch.py picks pending rows by status,
    not by position.
    """
    existing_by_id: dict[str, dict] = {}
    existing_order: list[str] = []
    for row in existing:
        cid = row.get("candidate_id")
        if not cid:
            continue
        if cid in existing_by_id:
            # First-write-wins; second occurrence is a malformed input.
            continue
        existing_by_id[cid] = dict(row)
        existing_order.append(cid)

    new_appended: list[dict] = []
    duplicate_skipped = 0

    for row in new_candidates:
        cid = row["candidate_id"]
        existing_row = existing_by_id.get(cid)
        if existing_row is not None:
            duplicate_skipped += 1
            if annotate_resurfaced:
                cell = row.get("cell")
                if cell and cell != existing_row.get("cell"):
                    marker = f"also-seen-in:{cell}"
                    notes = existing_row.get("notes") or ""
                    if marker not in notes:
                        existing_row["notes"] = (
                            f"{notes}; {marker}" if notes else marker
                        )
            continue
        stamped = dict(row)
        stamped["queued_at_utc"] = now_iso
        new_appended.append(stamped)

    merged = [existing_by_id[cid] for cid in existing_order] + new_appended

    counts = {
        "existing_preserved": len(existing_order),
        "new_appended": len(new_appended),
        "duplicate_skipped": duplicate_skipped,
        "total_after_merge": len(merged),
    }
    return merged, counts


# ──────────────────────────────────────────────────────────
#  Atomic write
# ──────────────────────────────────────────────────────────

def _write_jsonl_rows(rows: list[dict], path: Path) -> None:
    with path.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_csv_rows(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=baq.QUEUE_FIELDS, extrasaction="ignore"
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def atomic_write_queue(
    rows: list[dict],
    queue_path: Path,
    csv_path: Path,
) -> None:
    """Write JSONL and CSV via temp files + os.replace.

    If either temp write fails, both temp files are removed and the
    original queue/csv on disk are untouched. ``os.replace`` is atomic
    on the same filesystem on POSIX and Windows.
    """
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_jsonl = queue_path.with_suffix(queue_path.suffix + ".tmp")
    tmp_csv = csv_path.with_suffix(csv_path.suffix + ".tmp")

    try:
        _write_jsonl_rows(rows, tmp_jsonl)
        _write_csv_rows(rows, tmp_csv)
    except Exception:
        for tmp in (tmp_jsonl, tmp_csv):
            try:
                if tmp.exists():
                    tmp.unlink()
            except OSError:  # pragma: no cover - defensive
                pass
        raise

    os.replace(tmp_jsonl, queue_path)
    os.replace(tmp_csv, csv_path)


# ──────────────────────────────────────────────────────────
#  Summary
# ──────────────────────────────────────────────────────────

def summarize_merge(
    merged_rows: list[dict],
    merge_counts: dict,
) -> dict:
    """Per-status / per-kind breakdown over the merged queue."""
    base = baq.summarize(merged_rows)
    return {
        "merge": merge_counts,
        **base,
    }


# ──────────────────────────────────────────────────────────
#  Pipeline
# ──────────────────────────────────────────────────────────

def run_merge(
    existing_queue_path: Path,
    pilot_root: Path | None,
    explicit_files: list[Path],
    include_already_curated: bool,
    annotate_resurfaced: bool,
    now_iso: str,
) -> tuple[list[dict], dict, bool]:
    """Pure pipeline: returns (merged_rows, summary, existing_found)."""
    existing_found = existing_queue_path.exists()
    existing_rows = load_existing_queue(existing_queue_path)

    new_candidate_rows = baq.build_queue(
        pilot_root=pilot_root,
        explicit_files=explicit_files,
        include_already_curated=include_already_curated,
    )

    merged_rows, merge_counts = merge_rows(
        existing=existing_rows,
        new_candidates=new_candidate_rows,
        now_iso=now_iso,
        annotate_resurfaced=annotate_resurfaced,
    )
    summary = summarize_merge(merged_rows, merge_counts)
    return merged_rows, summary, existing_found


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--existing-queue",
        type=Path,
        required=True,
        help="path to existing queue.jsonl (missing file = fresh build)",
    )
    p.add_argument(
        "--pilot-root",
        type=Path,
        help="root containing P*/candidates.jsonl subdirs (new candidates)",
    )
    p.add_argument(
        "--candidates",
        type=Path,
        action="append",
        default=[],
        help="explicit candidates.jsonl path (repeatable)",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="directory for merged queue.jsonl/.csv/.meta.json",
    )
    p.add_argument(
        "--include-already-curated",
        action="store_true",
        help="keep already_curated rows with status=skipped_already_done",
    )
    p.add_argument(
        "--annotate-resurfaced",
        action="store_true",
        help="append also-seen-in:<cell> note when existing row re-surfaces in a new cell",
    )
    p.add_argument(
        "--queue-name",
        default=DEFAULT_QUEUE_NAME,
        help=f"queue JSONL filename (default: {DEFAULT_QUEUE_NAME})",
    )
    p.add_argument(
        "--csv-name",
        default=DEFAULT_CSV_NAME,
        help=f"queue CSV filename (default: {DEFAULT_CSV_NAME})",
    )
    p.add_argument(
        "--meta-name",
        default=DEFAULT_META_NAME,
        help=f"meta JSON filename (default: {DEFAULT_META_NAME})",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="compute and print summary; write no files",
    )
    args = p.parse_args(argv)
    if not args.pilot_root and not args.candidates:
        p.error("provide --pilot-root and/or --candidates")
    return args


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    now_iso = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    merged_rows, summary, existing_found = run_merge(
        existing_queue_path=args.existing_queue,
        pilot_root=args.pilot_root,
        explicit_files=args.candidates,
        include_already_curated=args.include_already_curated,
        annotate_resurfaced=args.annotate_resurfaced,
        now_iso=now_iso,
    )

    meta = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now_iso,
        "operation": "merge",
        "existing_queue": str(args.existing_queue),
        "existing_queue_found": existing_found,
        "pilot_root": str(args.pilot_root) if args.pilot_root else None,
        "explicit_candidates": [str(p) for p in args.candidates],
        "include_already_curated": args.include_already_curated,
        "annotate_resurfaced": args.annotate_resurfaced,
        "summary": summary,
    }

    if args.dry_run:
        print(json.dumps(meta, indent=2, ensure_ascii=False))
        return 0

    queue_path = args.out_dir / args.queue_name
    csv_path = args.out_dir / args.csv_name
    meta_path = args.out_dir / args.meta_name

    atomic_write_queue(merged_rows, queue_path, csv_path)
    baq.write_meta(meta, meta_path)

    print(f"merged queue written: {queue_path} ({len(merged_rows)} rows)")
    print(f"csv mirror: {csv_path}")
    print(f"meta: {meta_path}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
