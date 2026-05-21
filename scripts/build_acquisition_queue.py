#!/usr/bin/env python3
"""Build a normalized acquisition queue from pilot discovery candidates.

Reads one or more ``candidates.jsonl`` files produced by
``scripts/discover_heliophysics_literature.py`` (the per-cell pilot runs
under e.g. ``/tmp/heliosi-ads-pilot-20260521T000245Z/P*/candidates.jsonl``)
and produces a single deduplicated acquisition queue suitable for batched
PDF retrieval by ``scripts/run_acquisition_batch.py``.

Output is written **outside the git repo** -- the queue and its derivatives
(per-candidate attempt manifests, downloaded PDFs) are pilot acquisition
artefacts, not corpus content, and we explicitly do not commit them. The
recommended store is::

    /Users/huangzesen/work/projects/lingtai-space-research/\
sioulas-reproduction/results/heliosi_acquisition/

Each queue row carries:

    candidate_id          stable hash of the preferred identifier
    cell                  pilot cell label (e.g. P1-ads-1960s-era)
    source                discovery backend (ads / crossref / openalex / arxiv)
    title, year           bibliographic display fields
    doi, arxiv_id,        raw identifiers from discovery (any may be null)
    bibcode
    corpus_status         from discovery: new_candidate | already_curated
    preferred_identifier  identifier we will hand to fetch_paper.py, or null
    identifier_kind       doi | arxiv | bibcode_only | none
    priority              integer; lower = run earlier
    status                pending | fetched | no_supported_identifier |
                          fetch_failed | skipped_already_done | skipped
    notes                 free text (e.g. dedupe trail)

By default ``corpus_status == already_curated`` rows are dropped (they live
in the corpus already and should not be re-fetched into the acquisition
store). Pass ``--include-already-curated`` to keep them with
status=skipped_already_done.

Identifier selection prefers DOI, then arXiv, then bibcode (bibcode means
the row is **not directly fetchable** today; we mark it
identifier_kind=bibcode_only and status=no_supported_identifier so the
batch runner walks past it. A future ADS-resolver step can promote those
rows once it lands).

The script is stdlib-only and never prints, logs, or stores any
credential value. The ADS token (if any) is intentionally not consulted
here -- queue building is a pure transformation of the discovery JSONL.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable, Iterator


SCHEMA_VERSION = "heliosi-acquisition-queue/1.0"

DEFAULT_QUEUE_NAME = "queue.jsonl"
DEFAULT_CSV_NAME = "queue.csv"
DEFAULT_META_NAME = "queue.meta.json"

PRIORITY_DOI = 10
PRIORITY_ARXIV = 20
PRIORITY_BIBCODE_ONLY = 90
PRIORITY_NONE = 99

STATUS_PENDING = "pending"
STATUS_NO_ID = "no_supported_identifier"
STATUS_SKIPPED_CURATED = "skipped_already_done"


# ──────────────────────────────────────────────────────────
#  Normalisation
# ──────────────────────────────────────────────────────────

def _norm_doi(raw):
    if not raw:
        return None
    s = str(raw).strip().lower()
    s = s.replace("https://doi.org/", "").replace("http://doi.org/", "")
    s = s.replace("doi:", "").strip()
    if not s.startswith("10."):
        return None
    return s


def _norm_arxiv(raw):
    if not raw:
        return None
    s = str(raw).strip().lower()
    s = s.replace("arxiv:", "").strip()
    # Strip version suffix for dedupe; preserve original casing isn't needed
    # because arXiv IDs are case-insensitive.
    return s or None


def _norm_bibcode(raw):
    if not raw:
        return None
    s = str(raw).strip()
    return s or None


def pick_identifier(doi, arxiv_id, bibcode):
    """Return (preferred_identifier, identifier_kind, priority).

    preferred_identifier is a string fetch_paper.py can accept, or None
    when no supported identifier exists.
    """
    if doi:
        return doi, "doi", PRIORITY_DOI
    if arxiv_id:
        return f"arXiv:{arxiv_id}", "arxiv", PRIORITY_ARXIV
    if bibcode:
        return None, "bibcode_only", PRIORITY_BIBCODE_ONLY
    return None, "none", PRIORITY_NONE


def candidate_id(doi, arxiv_id, bibcode, title, year) -> str:
    """Stable id for dedupe across cells.

    Prefer DOI, then arXiv, then bibcode; otherwise hash a normalized
    title+year. We deliberately do NOT mix multiple keys into the hash
    -- if two cells discover the same DOI we want the same id even when
    one cell happens to also know its bibcode and the other does not.
    """
    if doi:
        key = f"doi:{doi}"
    elif arxiv_id:
        key = f"arxiv:{arxiv_id}"
    elif bibcode:
        key = f"bibcode:{bibcode}"
    else:
        norm_title = " ".join((title or "").lower().split())
        key = f"title:{norm_title}|year:{year or 0}"
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
    return f"cand_{h}"


# ──────────────────────────────────────────────────────────
#  Row construction
# ──────────────────────────────────────────────────────────

def normalize_candidate(record: dict, cell: str) -> dict:
    """Project a discovery JSONL record into the queue row schema."""
    doi = _norm_doi(record.get("doi"))
    arxiv_id = _norm_arxiv(record.get("arxiv_id"))
    bibcode = _norm_bibcode(record.get("bibcode"))
    title = record.get("title") or ""
    year = record.get("year")
    corpus_status = record.get("corpus_status") or "unknown"
    source = record.get("source") or "unknown"

    preferred, kind, priority = pick_identifier(doi, arxiv_id, bibcode)

    if corpus_status == "already_curated":
        status = STATUS_SKIPPED_CURATED
    elif preferred is None:
        status = STATUS_NO_ID
    else:
        status = STATUS_PENDING

    return {
        "candidate_id": candidate_id(doi, arxiv_id, bibcode, title, year),
        "cell": cell,
        "source": source,
        "title": title,
        "year": year,
        "doi": doi,
        "arxiv_id": arxiv_id,
        "bibcode": bibcode,
        "corpus_status": corpus_status,
        "preferred_identifier": preferred,
        "identifier_kind": kind,
        "priority": priority,
        "status": status,
        "notes": "",
        "queued_at_utc": None,  # filled by the writer; keeps normalize pure
    }


# ──────────────────────────────────────────────────────────
#  Pilot ingestion
# ──────────────────────────────────────────────────────────

def iter_pilot_records(pilot_root: Path) -> Iterator[tuple[str, dict]]:
    """Yield ``(cell, record)`` pairs from each P*/candidates.jsonl under root."""
    for cell_dir in sorted(p for p in pilot_root.iterdir() if p.is_dir()):
        path = cell_dir / "candidates.jsonl"
        if not path.exists():
            continue
        cell = cell_dir.name
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield cell, json.loads(line)
                except json.JSONDecodeError:
                    continue


def iter_explicit_files(paths: Iterable[Path]) -> Iterator[tuple[str, dict]]:
    """Yield ``(cell, record)`` pairs from explicit ``candidates.jsonl`` paths.

    The cell label is taken from the parent directory name.
    """
    for path in paths:
        if not path.exists():
            continue
        cell = path.parent.name or path.stem
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield cell, json.loads(line)
                except json.JSONDecodeError:
                    continue


# ──────────────────────────────────────────────────────────
#  Dedup + sort
# ──────────────────────────────────────────────────────────

def dedupe_rows(rows: Iterable[dict]) -> list[dict]:
    """First-write-wins on candidate_id; record the cells that collapsed."""
    by_id: dict[str, dict] = {}
    for row in rows:
        cid = row["candidate_id"]
        existing = by_id.get(cid)
        if existing is None:
            by_id[cid] = dict(row)
            continue
        # Track that another cell also surfaced this candidate. Keep notes
        # human-readable; do not balloon the row.
        other = row["cell"]
        if other not in existing.get("notes", ""):
            note = f"also-seen-in:{other}"
            existing["notes"] = (
                f"{existing['notes']}; {note}" if existing["notes"] else note
            )
    return list(by_id.values())


def sort_rows(rows: list[dict]) -> list[dict]:
    """Stable sort by (priority asc, year asc-when-available, candidate_id)."""
    def key(r):
        return (
            r.get("priority", PRIORITY_NONE),
            r.get("year") or 9999,
            r["candidate_id"],
        )
    return sorted(rows, key=key)


# ──────────────────────────────────────────────────────────
#  Output
# ──────────────────────────────────────────────────────────

QUEUE_FIELDS = [
    "candidate_id",
    "cell",
    "source",
    "title",
    "year",
    "doi",
    "arxiv_id",
    "bibcode",
    "corpus_status",
    "preferred_identifier",
    "identifier_kind",
    "priority",
    "status",
    "notes",
    "queued_at_utc",
]


def write_queue_jsonl(rows: list[dict], path: Path, now_iso: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        for row in rows:
            stamped = dict(row)
            stamped["queued_at_utc"] = now_iso
            fh.write(json.dumps(stamped, ensure_ascii=False) + "\n")


def write_queue_csv(rows: list[dict], path: Path, now_iso: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=QUEUE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            stamped = dict(row)
            stamped["queued_at_utc"] = now_iso
            writer.writerow(stamped)


def write_meta(meta: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")


# ──────────────────────────────────────────────────────────
#  Build entry point
# ──────────────────────────────────────────────────────────

def build_queue(
    pilot_root: Path | None,
    explicit_files: list[Path],
    include_already_curated: bool,
) -> list[dict]:
    """Return the deduped, sorted queue rows (without queued_at stamping)."""
    pairs: list[tuple[str, dict]] = []
    if pilot_root is not None:
        pairs.extend(iter_pilot_records(pilot_root))
    if explicit_files:
        pairs.extend(iter_explicit_files(explicit_files))

    normalized = [normalize_candidate(rec, cell) for cell, rec in pairs]
    if not include_already_curated:
        normalized = [r for r in normalized if r["status"] != STATUS_SKIPPED_CURATED]
    deduped = dedupe_rows(normalized)
    return sort_rows(deduped)


def summarize(rows: list[dict]) -> dict:
    by_status: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    by_cell: dict[str, int] = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        by_kind[r["identifier_kind"]] = by_kind.get(r["identifier_kind"], 0) + 1
        by_cell[r["cell"]] = by_cell.get(r["cell"], 0) + 1
    return {
        "total": len(rows),
        "by_status": by_status,
        "by_identifier_kind": by_kind,
        "by_cell": by_cell,
    }


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--pilot-root",
        type=Path,
        help="root containing P*/candidates.jsonl subdirs",
    )
    p.add_argument(
        "--candidates",
        type=Path,
        action="append",
        default=[],
        help="explicit candidates.jsonl path (repeatable); cell label is parent dir name",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="external acquisition store directory (will be created)",
    )
    p.add_argument(
        "--include-already-curated",
        action="store_true",
        help="keep already_curated rows with status=skipped_already_done",
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
        help="compute and print summary; do not write any files",
    )
    args = p.parse_args(argv)

    if not args.pilot_root and not args.candidates:
        p.error("provide --pilot-root and/or --candidates")

    rows = build_queue(
        pilot_root=args.pilot_root,
        explicit_files=args.candidates,
        include_already_curated=args.include_already_curated,
    )
    summary = summarize(rows)

    now_iso = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now_iso,
        "pilot_root": str(args.pilot_root) if args.pilot_root else None,
        "explicit_candidates": [str(p) for p in args.candidates],
        "include_already_curated": args.include_already_curated,
        "summary": summary,
    }

    if args.dry_run:
        print(json.dumps(meta, indent=2, ensure_ascii=False))
        return 0

    queue_path = args.out_dir / args.queue_name
    csv_path = args.out_dir / args.csv_name
    meta_path = args.out_dir / args.meta_name

    write_queue_jsonl(rows, queue_path, now_iso)
    write_queue_csv(rows, csv_path, now_iso)
    write_meta(meta, meta_path)

    print(f"wrote {len(rows)} rows to {queue_path}")
    print(f"wrote csv mirror to {csv_path}")
    print(f"wrote meta to {meta_path}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
