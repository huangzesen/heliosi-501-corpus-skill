#!/usr/bin/env python3
"""Emit a promotion-candidate report from a fetched-PDF acquisition store.

This is the *triage* step between two existing pieces of the open-ended
literature pipeline:

  - ``scripts/run_acquisition_batch.py`` / ``scripts/probe_authorized_fulltext.py``
    populate an external acquisition store (``queue.jsonl`` + ``attempts/``
    + ``authorized_attempts/`` + ``papers/<id-or-slug>/paper.pdf``) with
    fetched PDFs. The store lives **outside** this repo by policy.
  - ``scripts/draft_paper_skill_from_candidates.py`` turns reviewed
    candidates into *quarantined* draft paper-skills under a separate
    drafts tree.

Between the two, an agent or human needs a short, auditable list of
fetched candidates worth promoting first. This script reads the store
**read-only** and emits a Markdown and/or JSON report that ranks
``status == "fetched"`` rows with transparent, simple heuristics — and
honestly reports the rest of the queue (pending / failed / no-id) in the
summary so the reader cannot mistake "fetched PDF" for "verified
paper-skill".

Read-only contract
------------------
Unless the caller asks for an output file via ``--output-md`` or
``--output-json``, this script writes nothing — not even under
``/tmp``. It never modifies ``queue.jsonl`` or any PDF, and it never
makes network calls. The store directory is opened for ``stat()`` and
``read_text()`` only; PDF files are inspected by ``Path.stat()``.

Ranking heuristics (transparent and additive)
---------------------------------------------
For each fetched row we accumulate a small integer score. Every
contributor is recorded under ``score_reasons[]`` so the report is
auditable:

  +30  PDF exists on disk and is larger than 10 kB
  +15  acquisition_route is ``official_pdf`` (authorized-probe path)
  +15  arXiv ID present
  +10  DOI present
  +10  year is within the last 5 years of ``current_year``
  +5   ``corpus_status == "new_candidate"`` (not already curated)
  +5   title contains a heliophysics keyword from a small list
  -20  attempt manifest_status is not ``"ok"``

These are intentionally crude: a fetched PDF is **not** a verified
paper-skill, and we do not want the report to pretend otherwise. The
score is a *first-pass triage signal*, not a quality metric.

Honest claim boundary
---------------------
A row in the top-N table means "this candidate looks worth eyeballing
first", not "this is paper-skill ready". Promotion still requires the
manual / agentic evidence pass run via
``scripts/draft_paper_skill_from_candidates.py`` and the per-draft
``promotion_gate`` checklist (see ``DISCOVERY_POLICY.md``).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from urllib.parse import urlparse


SCHEMA_VERSION = "heliosi-promotion-candidates/1.0"

# Routes
ROUTE_OFFICIAL_PDF = "official_pdf"
ROUTE_TIERED_FETCH = "tiered_fetch"
ROUTE_UNKNOWN = "unknown"

# Small heliophysics keyword list. Lower-case, substring match against
# the title. Intentionally short so the bonus is easy to reason about.
TITLE_KEYWORDS: Tuple[str, ...] = (
    "solar wind",
    "corona",
    "heliospher",
    "magnetic",
    "pfss",
    "switchback",
    "sep",
    "turbulence",
    "reconnection",
    "alfven",
    "cme",
    "flare",
    "plasma",
)


# ──────────────────────────────────────────────────────────
#  Slug helpers
# ──────────────────────────────────────────────────────────

def _kebab(text: str) -> str:
    """ASCII-fold ``text`` and produce a kebab-case token sequence."""
    s = unicodedata.normalize("NFKD", text or "")
    s = s.encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _disambiguator(candidate_id: str) -> str:
    # The acquisition queue uses ``cand_<16hex>`` IDs. Strip the prefix
    # and keep the first 6 hex chars so the slug is stable but readable.
    s = candidate_id or ""
    if s.startswith("cand_"):
        s = s[len("cand_"):]
    s = re.sub(r"[^a-f0-9]", "", s.lower())
    return s[:6] if s else "nocid0"


def suggested_skill_slug(candidate_id: str, *, year: Optional[int], title: str) -> str:
    """Deterministic skill-stub slug for a candidate.

    Shape: ``paper-<year-or-unknownyear>-<short-title-tokens>-<6hex>``.

    We deliberately do **not** embed an author surname: the queue row
    carries no verified author, and inventing one would silently break
    the corpus's authorship-hygiene rule (README §"Authorship fields
    are intentionally null / unverified"). Disambiguation is provided
    by the first 6 hex chars of the candidate_id instead.
    """
    year_token = str(year) if year else "unknownyear"
    title_tokens = _kebab(title).split("-") if title else []
    # Drop stop-words and very short tokens to keep the slug readable.
    stop = {"a", "an", "the", "of", "in", "on", "and", "for", "with", "to", "from", "by"}
    title_tokens = [t for t in title_tokens if t and t not in stop]
    title_tokens = title_tokens[:6]
    title_part = "-".join(title_tokens) if title_tokens else "untitled"
    return f"paper-{year_token}-{title_part}-{_disambiguator(candidate_id)}"


# ──────────────────────────────────────────────────────────
#  Store I/O (read-only)
# ──────────────────────────────────────────────────────────

def _read_jsonl(path: Path) -> List[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _load_optional_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


# ──────────────────────────────────────────────────────────
#  Route + host inference
# ──────────────────────────────────────────────────────────

def _host_of(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    try:
        netloc = urlparse(url).netloc
    except ValueError:
        return None
    return netloc.lower() or None


def infer_route_and_host(
    *,
    authorized: Optional[dict],
    attempt: Optional[dict],
) -> Tuple[str, Optional[str]]:
    """Return ``(route, host)`` from the available provenance.

    ``authorized`` is the ``authorized_attempts/<cid>.json`` payload (if
    any); ``attempt`` is the ``attempts/<cid>.json`` payload (if any).
    The function never invents a host: it returns ``None`` when the
    provenance does not name one (e.g. the tiered-fetch path goes
    through a chain of tier resolvers we do not record per attempt).
    """
    if authorized:
        source = authorized.get("source")
        if source == "official_pdf":
            host = _host_of(authorized.get("pdf_url")) or _host_of(authorized.get("landing_url"))
            return ROUTE_OFFICIAL_PDF, host
        # An authorized probe that did not yield an official PDF is
        # not "official_pdf" — fall through.

    if attempt and attempt.get("last_result") == "fetched":
        return ROUTE_TIERED_FETCH, None

    return ROUTE_UNKNOWN, None


# ──────────────────────────────────────────────────────────
#  PDF location resolution
# ──────────────────────────────────────────────────────────

def _resolve_pdf(
    store: Path,
    candidate_id: str,
    *,
    attempt: Optional[dict],
    authorized: Optional[dict],
) -> Tuple[bool, int, Optional[str]]:
    """Return ``(exists, size_bytes, pdf_path_str)`` for a candidate.

    Two layout conventions are supported:

      - ``papers/<candidate_id>/paper.pdf`` — written by the
        authorized-probe path (``probe_authorized_fulltext.py``).
      - ``papers/<manifest_slug>/paper.pdf`` — written by the tiered
        fetch path (``run_acquisition_batch.py`` via
        ``fetch_paper.py``); the slug is recorded in
        ``attempts/<cid>.json -> fetch_summary.manifest_slug``.

    A row whose queue status is ``fetched`` but whose PDF is not on
    disk is reported honestly with ``exists=False, size_bytes=0``.
    """
    candidates: List[Path] = []
    if authorized and authorized.get("pdf_path"):
        # The authorized probe records an absolute path; we only honour
        # it when it is under ``store`` to avoid following stale paths
        # out of the store after a move.
        recorded = Path(authorized["pdf_path"])
        try:
            recorded.resolve().relative_to(store.resolve())
            candidates.append(recorded)
        except ValueError:
            pass
    candidates.append(store / "papers" / candidate_id / "paper.pdf")
    if attempt:
        slug = (attempt.get("fetch_summary") or {}).get("manifest_slug")
        if slug:
            candidates.append(store / "papers" / slug / "paper.pdf")

    for c in candidates:
        try:
            st = c.stat()
        except (FileNotFoundError, OSError):
            continue
        if st.st_size > 0:
            return True, st.st_size, str(c)
    return False, 0, None


# ──────────────────────────────────────────────────────────
#  Scoring
# ──────────────────────────────────────────────────────────

def _title_keyword_hit(title: str) -> Optional[str]:
    t = (title or "").lower()
    for kw in TITLE_KEYWORDS:
        if kw in t:
            return kw
    return None


def score_candidate(c: dict, *, current_year: int) -> Tuple[int, List[dict]]:
    """Return ``(score, reasons)`` for a candidate dict.

    The dict must carry the merged provenance fields produced by
    :func:`_build_candidate`. The function is pure — it does no I/O —
    so it is straightforward to unit-test.
    """
    reasons: List[dict] = []
    score = 0

    if c.get("pdf_exists") and (c.get("pdf_bytes") or 0) > 10_000:
        score += 30
        reasons.append({"component": "pdf_on_disk", "points": 30,
                        "why": "PDF present on disk and larger than 10 kB"})

    if c.get("acquisition_route") == ROUTE_OFFICIAL_PDF:
        score += 15
        reasons.append({"component": "official_pdf_route", "points": 15,
                        "why": "Fetched via authorized-probe official PDF (stronger provenance)"})

    if c.get("arxiv_id"):
        score += 15
        reasons.append({"component": "arxiv_id_present", "points": 15,
                        "why": "arXiv ID recorded on queue row"})

    if c.get("doi"):
        score += 10
        reasons.append({"component": "doi_present", "points": 10,
                        "why": "DOI recorded on queue row"})

    year = c.get("year")
    if isinstance(year, int) and (current_year - 5) <= year <= current_year:
        score += 10
        reasons.append({"component": "recent_year", "points": 10,
                        "why": f"Year {year} is within last 5 years of {current_year}"})

    if c.get("corpus_status") == "new_candidate":
        score += 5
        reasons.append({"component": "new_candidate", "points": 5,
                        "why": "Not already curated in the 501-entry corpus"})

    kw = _title_keyword_hit(c.get("title") or "")
    if kw:
        score += 5
        reasons.append({"component": "title_keyword", "points": 5,
                        "why": f"Title contains heliophysics keyword '{kw}'"})

    if c.get("manifest_status") and c.get("manifest_status") != "ok":
        score -= 20
        reasons.append({"component": "manifest_not_ok", "points": -20,
                        "why": f"Fetch manifest status is {c['manifest_status']!r}, not 'ok'"})

    return score, reasons


# ──────────────────────────────────────────────────────────
#  Per-candidate assembly
# ──────────────────────────────────────────────────────────

def _build_candidate(store: Path, row: dict, *, current_year: int) -> dict:
    cid = row.get("candidate_id") or ""
    attempt = _load_optional_json(store / "attempts" / f"{cid}.json")
    authorized = _load_optional_json(store / "authorized_attempts" / f"{cid}.json")

    route, host = infer_route_and_host(authorized=authorized, attempt=attempt)
    pdf_exists, pdf_bytes, pdf_path = _resolve_pdf(
        store, cid, attempt=attempt, authorized=authorized,
    )

    manifest_status = None
    manifest_slug = None
    latest_attempt_result = None
    if attempt:
        latest_attempt_result = attempt.get("last_result")
        summary = attempt.get("fetch_summary") or {}
        manifest_status = summary.get("manifest_status")
        manifest_slug = summary.get("manifest_slug")

    record = {
        "candidate_id": cid,
        "title": row.get("title"),
        "year": row.get("year"),
        "doi": row.get("doi"),
        "arxiv_id": row.get("arxiv_id"),
        "bibcode": row.get("bibcode"),
        "cell": row.get("cell"),
        "source": row.get("source"),
        "corpus_status": row.get("corpus_status"),
        "queue_status": row.get("status"),
        "latest_attempt_result": latest_attempt_result,
        "manifest_status": manifest_status,
        "manifest_slug": manifest_slug,
        "pdf_exists": pdf_exists,
        "pdf_bytes": pdf_bytes,
        "pdf_path": pdf_path,
        "acquisition_route": route,
        "acquisition_host": host,
        "suggested_skill_slug": suggested_skill_slug(
            cid, year=row.get("year"), title=row.get("title") or "",
        ),
    }
    score, reasons = score_candidate(record, current_year=current_year)
    record["score"] = score
    record["score_reasons"] = reasons
    return record


# ──────────────────────────────────────────────────────────
#  Top-level report assembly
# ──────────────────────────────────────────────────────────

def build_report(store: Path, *, top: int, current_year: int) -> dict:
    """Read the store and return the report dict.

    Raises ``FileNotFoundError`` if the store directory does not exist.
    An empty queue is fine — the candidates list comes back empty.
    """
    store = Path(store)
    if not store.exists():
        raise FileNotFoundError(f"acquisition store does not exist: {store}")

    queue_path = store / "queue.jsonl"
    rows = _read_jsonl(queue_path) if queue_path.exists() else []

    fetched_rows = [r for r in rows if r.get("status") == "fetched"]
    candidates = [
        _build_candidate(store, r, current_year=current_year) for r in fetched_rows
    ]
    # Sort by score desc, then by year desc (recent first), then by
    # candidate_id for total stability.
    candidates.sort(
        key=lambda c: (-c["score"], -(c.get("year") or 0), c["candidate_id"]),
    )

    summary = {
        "queue_total": len(rows),
        "by_status": dict(Counter(r.get("status") for r in rows)),
        "fetched_ranked": len(candidates),
        "by_route": dict(Counter(c["acquisition_route"] for c in candidates)),
        "by_host": dict(Counter(
            c["acquisition_host"] for c in candidates if c["acquisition_host"]
        )),
        "by_source": dict(Counter(r.get("source") for r in fetched_rows)),
        "with_pdf_on_disk": sum(1 for c in candidates if c["pdf_exists"]),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "current_year": current_year,
        "summary": summary,
        "candidates": candidates[:top] if top is not None else candidates,
    }


# ──────────────────────────────────────────────────────────
#  Markdown rendering
# ──────────────────────────────────────────────────────────

def _truncate(text: str, length: int) -> str:
    text = (text or "").replace("\n", " ").strip()
    return text if len(text) <= length else text[: length - 1] + "…"


def render_markdown(report: dict, *, store_path_display: str) -> str:
    """Render a human-readable Markdown report.

    ``store_path_display`` is the path string we want to surface in the
    report. Callers writing the report into the repo's ``reports/``
    directory should pass a placeholder (e.g.
    ``"<acquisition-store>"``); ad-hoc local runs may pass the real
    absolute path.
    """
    summary = report["summary"]
    lines: List[str] = []
    lines.append("# Promotion-candidate triage report")
    lines.append("")
    lines.append(f"_Generated: {report['generated_at']} (UTC)_")
    lines.append(f"_Acquisition store: `{store_path_display}`_")
    lines.append("")
    lines.append(
        "> **Honest claim boundary.** Fetched PDF ≠ verified paper-skill. "
        "Ranking here is a first-pass triage signal; promotion still "
        "requires the per-draft `promotion_gate` checklist enforced by "
        "`scripts/draft_paper_skill_from_candidates.py` and "
        "`DISCOVERY_POLICY.md`."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Queue total | {summary['queue_total']} |")
    for status, n in sorted(summary["by_status"].items(), key=lambda kv: (-kv[1], str(kv[0]))):
        lines.append(f"| status: `{status}` | {n} |")
    lines.append(f"| Fetched rows entered in ranking | {summary['fetched_ranked']} |")
    lines.append(f"| Fetched rows with PDF on disk | {summary['with_pdf_on_disk']} |")
    lines.append("")

    lines.append("## Acquisition routes (ranked rows only)")
    lines.append("")
    if summary["by_route"]:
        lines.append("| Route | Count |")
        lines.append("|---|---:|")
        for route, n in sorted(summary["by_route"].items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| `{route}` | {n} |")
    else:
        lines.append("_(no fetched rows)_")
    lines.append("")

    lines.append("## Acquisition hosts (where inferable)")
    lines.append("")
    if summary["by_host"]:
        lines.append("| Host | Count |")
        lines.append("|---|---:|")
        for host, n in sorted(summary["by_host"].items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| `{host}` | {n} |")
    else:
        lines.append(
            "_(no host inferable — tiered-fetch routes do not record a "
            "single host per attempt)_"
        )
    lines.append("")

    lines.append("## Top promotion candidates")
    lines.append("")
    if report["candidates"]:
        lines.append("| Rank | candidate_id | Year | Title | Route | Host | Score | Suggested slug |")
        lines.append("|---:|---|---:|---|---|---|---:|---|")
        for i, c in enumerate(report["candidates"], start=1):
            lines.append(
                "| {rank} | `{cid}` | {year} | {title} | `{route}` | {host} | {score} | `{slug}` |".format(
                    rank=i,
                    cid=c["candidate_id"],
                    year=c.get("year") or "—",
                    title=_truncate(c.get("title") or "", 70),
                    route=c["acquisition_route"],
                    host=f"`{c['acquisition_host']}`" if c["acquisition_host"] else "—",
                    score=c["score"],
                    slug=c["suggested_skill_slug"],
                )
            )
    else:
        lines.append("_(no fetched candidates to rank)_")
    lines.append("")

    lines.append("## Next step (manual / agentic promotion pass)")
    lines.append("")
    lines.append(
        "For each candidate you choose to promote, work through the "
        "lifecycle defined in `DISCOVERY_POLICY.md` and "
        "`reports/candidate_lifecycle_demo.md`:"
    )
    lines.append("")
    lines.append(
        "1. Open the PDF at the recorded `pdf_path` and confirm title + "
        "year + first author against the queue row. The slug suggested "
        "above embeds **no** unverified surname; fill the surname in only "
        "after this check."
    )
    lines.append(
        "2. Run `python3 scripts/draft_paper_skill_from_candidates.py "
        "--from-candidates <subset.jsonl> --drafts-dir <quarantine-dir>` "
        "to scaffold a quarantined draft under `draft__…`."
    )
    lines.append(
        "3. Verify identifiers: arXiv via "
        "`python3 scripts/verify_arxiv_ids.py --only-ids <id>` if "
        "applicable; DOI via Crossref. Update the draft's "
        "`provenance.id_verifications[]` block."
    )
    lines.append(
        "4. Author Layer-1 claim + Layer-2 contract from the PDF, not "
        "from the abstract alone. Flip the relevant `promotion_gate` "
        "checklist items only when each is honestly satisfied."
    )
    lines.append(
        "5. Only after every gate item is `true` may the draft be moved "
        "into `references/corpus/<batch>/<slug>/` and validated via "
        "`bash scripts/validate.sh`."
    )
    lines.append("")
    lines.append(
        "Re-running this script after a fresh acquisition batch will "
        "re-rank from scratch — the report is **not** stateful."
    )
    lines.append("")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="select_promotion_candidates.py",
        description=__doc__.split("\n\n", 1)[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--store",
        type=Path,
        required=True,
        help="Path to the external acquisition store (contains queue.jsonl, "
             "attempts/, authorized_attempts/, papers/).",
    )
    p.add_argument(
        "--output-md",
        type=Path,
        default=None,
        help="Write the Markdown report here. Default: do not write.",
    )
    p.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Write the JSON report here. Default: do not write.",
    )
    p.add_argument(
        "--top",
        type=int,
        default=25,
        help="How many top-ranked fetched candidates to include in the "
             "report (default: 25). Summary counts always reflect the "
             "full queue.",
    )
    p.add_argument(
        "--min-score",
        type=int,
        default=None,
        help="Optional filter: drop candidates with score below this "
             "threshold from the ranked list. Default: no filter.",
    )
    p.add_argument(
        "--current-year",
        type=int,
        default=dt.date.today().year,
        help="Reference year for the 'recent_year' bonus. Default: today.",
    )
    p.add_argument(
        "--store-path-display",
        default=None,
        help="String to surface as the store path in the Markdown report. "
             "Default: the literal --store value. Use a placeholder when "
             "writing the report to a shared / committed location.",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    report = build_report(args.store, top=args.top, current_year=args.current_year)

    if args.min_score is not None:
        report["candidates"] = [
            c for c in report["candidates"] if c["score"] >= args.min_score
        ]

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.output_md:
        display = args.store_path_display or str(args.store)
        md = render_markdown(report, store_path_display=display)
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(md, encoding="utf-8")

    # Print a short summary to stdout regardless of output flags so the
    # caller has a usable record even in dry-run invocations.
    summary = report["summary"]
    print(
        f"[select_promotion_candidates] queue_total={summary['queue_total']} "
        f"fetched_ranked={summary['fetched_ranked']} "
        f"with_pdf_on_disk={summary['with_pdf_on_disk']} "
        f"in_report={len(report['candidates'])}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
