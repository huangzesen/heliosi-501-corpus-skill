#!/usr/bin/env python3
"""Resolve bibcode-only acquisition queue rows to DOIs / arXiv IDs via NASA ADS.

Reads a queue produced by ``scripts/build_acquisition_queue.py``, picks rows
whose ``status == no_supported_identifier`` and ``identifier_kind ==
bibcode_only``, and asks the NASA ADS search API to map each bibcode to a
DOI or arXiv identifier. When a usable identifier comes back, the row is
promoted to ``status=pending`` so the next ``run_acquisition_batch.py``
invocation can hand it to ``fetch_paper.py``. Rows that still cannot be
resolved are left as ``no_supported_identifier`` and recorded in a
per-row enrichment-attempt file so future runs can skip them or retry
deliberately.

Outputs live in the external acquisition store (``--store``):

    store/
        queue.jsonl                          # rewritten atomically when not --dry-run
        queue.csv                            # CSV mirror, refreshed best-effort
        enrichment_attempts/<candidate_id>.json
        runs/<run_id>-enrich/summary.json
        runs/<run_id>-enrich/log.txt         # per-row decision trail (no secrets)

Credential handling
-------------------
The ADS token is sourced from one of:

  1. ``--token-file PATH`` -- a file whose content is either the token
     itself or a small JSON object containing one of the supported token
     keys (``ADS_API_TOKEN``, ``NASA_ADS_TOKEN``, ``ADS_TOKEN``,
     ``token``, ``api_token``, ``api_key``, ``access_token``, ``key``).
  2. ``ADS_API_TOKEN`` / ``NASA_ADS_TOKEN`` / ``ADS_TOKEN`` env vars.

The token value is NEVER printed, logged, written to any artefact, or
echoed in subprocess output. The CLI exposes only the env var / option
names, not their contents. ``--dry-run`` does not require a token; without credentials it reports
``dry_run_no_token`` outcomes rather than pretending ADS had no hits.

Identifier promotion rules
--------------------------
For each selected row we issue ``q=bibcode:"<bibcode>" fl=bibcode,doi,
identifier,title,year``. The first hit's fields are consulted in order:

  1. If ``doi`` is present (and normalisable to ``10.*``), we set
     ``doi``, ``preferred_identifier=<doi>``, ``identifier_kind='doi'``,
     ``status='pending'``.
  2. Else if ``identifier`` contains a parseable arXiv id, we set
     ``arxiv_id``, ``preferred_identifier='arXiv:<id>'``,
     ``identifier_kind='arxiv'``, ``status='pending'``.
  3. Otherwise the row is left untouched. The attempt file records the
     reason (``no_doi_no_arxiv``, ``no_ads_hit``, ``http_error``, ...).

The script is safe to interrupt: the queue is rewritten atomically after
every successful promotion, and per-row attempt files are written
independently. Re-running is idempotent -- already-pending rows are
skipped by selection, and recent attempts can be honoured via
``--retry-after-seconds`` (default: retry everything). Run only one
enrichment process per acquisition store at a time; like the batch runner,
this script uses atomic rewrites but no inter-process lock.

This script is stdlib-only. No third-party HTTP library is required.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Callable, Optional


SCHEMA_VERSION = "heliosi-acquisition-enrich/1.0"

DEFAULT_QUEUE_NAME = "queue.jsonl"
DEFAULT_CSV_NAME = "queue.csv"
ATTEMPTS_DIRNAME = "enrichment_attempts"
RUNS_DIRNAME = "runs"

STATUS_PENDING = "pending"
STATUS_NO_ID = "no_supported_identifier"

PRIORITY_DOI = 10
PRIORITY_ARXIV = 20

ADS_TOKEN_ENV_VARS = ("ADS_API_TOKEN", "NASA_ADS_TOKEN", "ADS_TOKEN")
ADS_SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"
ADS_FIELDS = "bibcode,doi,identifier,title,year"

USER_AGENT = "heliosi-acquisition-enrich/1.0 (+stdlib urllib)"

# Conservative defaults for the ADS API. ADS publishes rate guidance; we
# also expose --request-pause-seconds so a caller can throttle further.
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 2
DEFAULT_RETRY_BASE_SECONDS = 2.0
DEFAULT_REQUEST_PAUSE_SECONDS = 0.2


# ──────────────────────────────────────────────────────────
#  Identifier normalisation (mirrors build_acquisition_queue)
# ──────────────────────────────────────────────────────────

_ARXIV_NEW_RE = re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b", re.IGNORECASE)
_ARXIV_OLD_RE = re.compile(r"\b([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?\b", re.IGNORECASE)


def normalize_doi(raw) -> Optional[str]:
    if not raw:
        return None
    s = str(raw).strip().lower()
    s = s.replace("https://doi.org/", "").replace("http://doi.org/", "")
    s = s.replace("doi:", "").strip()
    if not s.startswith("10."):
        return None
    return s


def normalize_arxiv_id(raw) -> Optional[str]:
    """Return a canonical arXiv id from an arbitrary identifier string.

    Accepts forms such as ``arXiv:2301.01234``, ``2301.01234v2``,
    ``astro-ph/0701123``, or a URL. Returns ``None`` if no arXiv id is
    embedded.
    """
    if not raw:
        return None
    s = str(raw).strip()
    # ADS identifier values often look like "arXiv:2301.01234". Strip a
    # leading "arxiv:" once before the regex so the regex sees only the id.
    low = s.lower()
    if low.startswith("arxiv:"):
        s = s.split(":", 1)[1]
    m = _ARXIV_NEW_RE.search(s) or _ARXIV_OLD_RE.search(s)
    if not m:
        return None
    return m.group(1).lower()


# ──────────────────────────────────────────────────────────
#  Credential resolution -- token VALUE never leaves this module
# ──────────────────────────────────────────────────────────

def _token_from_text(content: str) -> Optional[str]:
    """Extract a token from plaintext or a small JSON secret file.

    Local operator secret files are often JSON objects (for provenance and
    timestamps) rather than bare-token files. Support both forms without
    leaking the value. Unknown JSON shapes return ``None`` instead of
    accidentally using the whole JSON blob as the bearer token.
    """
    content = (content or "").strip()
    if not content:
        return None
    if content[:1] in "{[\"":
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Fall through to plaintext handling below; a token can
            # technically begin with a JSON-ish character.
            pass
        else:
            if isinstance(data, str):
                return data.strip() or None
            if isinstance(data, dict):
                keys = (
                    *ADS_TOKEN_ENV_VARS,
                    "token",
                    "api_token",
                    "api_key",
                    "access_token",
                    "key",
                )
                lowered = {str(k).lower(): v for k, v in data.items()}
                for key in keys:
                    val = data.get(key)
                    if val is None:
                        val = lowered.get(key.lower())
                    if isinstance(val, str) and val.strip():
                        return val.strip()
            return None
    return content


def resolve_token(token_file: Optional[Path], env: Optional[dict] = None) -> Optional[str]:
    """Return the ADS token, or ``None`` if no source is configured.

    Preference order: ``--token-file`` > env vars in :data:`ADS_TOKEN_ENV_VARS`.
    Token files may be plaintext or JSON secret objects. The token value is
    returned but never logged; the caller is expected to forward it only to
    :func:`build_request_headers`.
    """
    if token_file is not None:
        try:
            content = Path(token_file).read_text(encoding="utf-8")
        except OSError:
            return None
        return _token_from_text(content)
    e = env if env is not None else os.environ
    for var in ADS_TOKEN_ENV_VARS:
        val = e.get(var)
        if val:
            val = val.strip()
            if val:
                return val
    return None


def build_request_headers(token: str) -> dict:
    """Return headers for ADS. The token never appears anywhere else."""
    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }


# ──────────────────────────────────────────────────────────
#  Pure resolver (no I/O) -- consumes an ADS response dict
# ──────────────────────────────────────────────────────────

def parse_ads_response(payload: dict) -> dict:
    """Project an ADS search response into ``{doi, arxiv_id, raw_doc}``.

    ``payload`` is the decoded JSON from ADS's ``/v1/search/query``
    endpoint. Returns a dict carrying the first hit's resolved identifiers
    plus the raw doc (useful for the per-row attempt file). When there
    are no docs we return ``{"doi": None, "arxiv_id": None, "raw_doc": None}``.
    """
    docs = ((payload or {}).get("response") or {}).get("docs") or []
    if not docs:
        return {"doi": None, "arxiv_id": None, "raw_doc": None}
    doc = docs[0] or {}
    doi_list = doc.get("doi") or []
    doi = None
    if isinstance(doi_list, list):
        for cand in doi_list:
            n = normalize_doi(cand)
            if n:
                doi = n
                break
    else:
        doi = normalize_doi(doi_list)
    arxiv_id = None
    for ident in doc.get("identifier") or []:
        nid = normalize_arxiv_id(ident)
        if nid:
            arxiv_id = nid
            break
    return {"doi": doi, "arxiv_id": arxiv_id, "raw_doc": doc}


# ──────────────────────────────────────────────────────────
#  HTTP layer (polite, retry-aware, token-isolated)
# ──────────────────────────────────────────────────────────

class AdsHTTPError(RuntimeError):
    """Raised when ADS keeps returning non-2xx after all retries."""


def build_ads_query_url(bibcode: str, fields: str = ADS_FIELDS) -> str:
    """Return the ADS search URL for a single bibcode lookup."""
    params = {
        "q": f'bibcode:"{bibcode}"',
        "fl": fields,
        "rows": "1",
    }
    return f"{ADS_SEARCH_URL}?{urllib.parse.urlencode(params)}"


def _http_get_json(
    url: str,
    headers: dict,
    *,
    timeout: float,
    max_retries: int,
    retry_base_seconds: float,
    sleep: Callable[[float], None] = time.sleep,
    urlopen: Callable = urllib.request.urlopen,
) -> dict:
    """GET ``url`` and parse the JSON body, with bounded exponential backoff.

    Retries on HTTP 408/425/429/5xx and ``URLError``. Never includes any
    header value (token) in raised messages.
    """
    transient = {408, 425, 429, 500, 502, 503, 504}
    attempts = max(0, max_retries) + 1
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(attempts):
        if attempt > 0:
            sleep(retry_base_seconds * (2 ** (attempt - 1)))
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                try:
                    return json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise AdsHTTPError(f"ADS returned non-JSON body: {exc}") from exc
        except urllib.error.HTTPError as e:
            if e.code in transient and attempt < attempts - 1:
                continue
            raise AdsHTTPError(f"ADS HTTP {e.code} after {attempt + 1}/{attempts} attempts")
        except urllib.error.URLError as e:
            if attempt < attempts - 1:
                continue
            # e.reason can be a string or another exception; coerce safely.
            raise AdsHTTPError(
                f"ADS URLError after {attempt + 1}/{attempts} attempts: {e.reason!r}"
            )
        except TimeoutError as e:
            if attempt < attempts - 1:
                continue
            raise AdsHTTPError(
                f"ADS timeout after {attempt + 1}/{attempts} attempts: {e}"
            )
    raise AdsHTTPError("ADS unreachable retry path")


def make_resolver(
    token: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_MAX_RETRIES,
    retry_base_seconds: float = DEFAULT_RETRY_BASE_SECONDS,
    http_get_json: Optional[Callable[..., dict]] = None,
) -> Callable[[str], dict]:
    """Return ``resolver(bibcode) -> {doi, arxiv_id, raw_doc}``.

    Wraps :func:`_http_get_json` with the supplied token so the rest of
    the script never needs to see the token value directly.
    """
    headers = build_request_headers(token)
    fetch = http_get_json or _http_get_json

    def resolve(bibcode: str) -> dict:
        url = build_ads_query_url(bibcode)
        payload = fetch(
            url,
            headers,
            timeout=timeout,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
        )
        return parse_ads_response(payload)

    return resolve


# ──────────────────────────────────────────────────────────
#  Queue I/O
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
    """Best-effort CSV mirror; never fails the run on CSV errors."""
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
#  Row selection
# ──────────────────────────────────────────────────────────

def select_enrich_candidates(
    rows: list[dict],
    *,
    limit: Optional[int] = None,
    only_candidate_ids: Optional[set[str]] = None,
) -> list[dict]:
    """Return rows whose status is ``no_supported_identifier`` and have a bibcode.

    Filters:
        - ``identifier_kind`` must be ``bibcode_only`` (other no_id rows
          have no bibcode to look up).
        - ``only_candidate_ids`` -- restrict to a specific id set.
        - ``limit`` -- cap the returned slice.
    """
    out: list[dict] = []
    for row in rows:
        if row.get("status") != STATUS_NO_ID:
            continue
        if row.get("identifier_kind") != "bibcode_only":
            continue
        if not row.get("bibcode"):
            continue
        if only_candidate_ids is not None and row.get("candidate_id") not in only_candidate_ids:
            continue
        out.append(row)
        if limit is not None and len(out) >= limit:
            break
    return out


# ──────────────────────────────────────────────────────────
#  Per-row attempt manifest
# ──────────────────────────────────────────────────────────

def attempt_path(store: Path, candidate_id: str) -> Path:
    return store / ATTEMPTS_DIRNAME / f"{candidate_id}.json"


def read_attempt(store: Path, candidate_id: str) -> Optional[dict]:
    p = attempt_path(store, candidate_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def write_attempt(store: Path, candidate_id: str, payload: dict) -> None:
    p = attempt_path(store, candidate_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def should_skip_due_to_recent_attempt(
    prior: Optional[dict],
    retry_after_seconds: Optional[float],
    now_utc: dt.datetime,
) -> bool:
    """Return True when a prior attempt is recent enough to skip."""
    if prior is None or retry_after_seconds is None:
        return False
    ts = prior.get("attempted_at_utc")
    if not isinstance(ts, str):
        return False
    try:
        when = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return False
    return (now_utc - when).total_seconds() < retry_after_seconds


# ──────────────────────────────────────────────────────────
#  Row promotion
# ──────────────────────────────────────────────────────────

def promote_row(row: dict, resolved: dict, run_id: str) -> tuple[bool, str]:
    """Mutate ``row`` in place if ``resolved`` has a usable identifier.

    Returns ``(promoted, reason)``. ``reason`` is one of:
        - ``ads-resolved-doi:<run_id>``    -> DOI promoted
        - ``ads-resolved-arxiv:<run_id>``  -> arXiv promoted
        - ``no_ads_hit``                   -> ADS returned no docs
        - ``no_doi_no_arxiv``              -> hit but neither id usable
    """
    doi = resolved.get("doi")
    arxiv = resolved.get("arxiv_id")
    if doi:
        note = f"ads-resolved-doi:{run_id}"
        row["doi"] = doi
        row["preferred_identifier"] = doi
        row["identifier_kind"] = "doi"
        row["status"] = STATUS_PENDING
        row["priority"] = PRIORITY_DOI
        existing = row.get("notes") or ""
        row["notes"] = f"{existing}; {note}" if existing else note
        return True, note
    if arxiv:
        note = f"ads-resolved-arxiv:{run_id}"
        row["arxiv_id"] = arxiv
        row["preferred_identifier"] = f"arXiv:{arxiv}"
        row["identifier_kind"] = "arxiv"
        row["status"] = STATUS_PENDING
        row["priority"] = PRIORITY_ARXIV
        existing = row.get("notes") or ""
        row["notes"] = f"{existing}; {note}" if existing else note
        return True, note
    if resolved.get("raw_doc") is None:
        return False, "no_ads_hit"
    return False, "no_doi_no_arxiv"


# ──────────────────────────────────────────────────────────
#  Enrichment driver
# ──────────────────────────────────────────────────────────

def run_enrichment(
    store: Path,
    resolver: Callable[[str], dict],
    *,
    limit: Optional[int] = None,
    dry_run: bool = False,
    only_candidate_ids: Optional[set[str]] = None,
    retry_after_seconds: Optional[float] = None,
    request_pause_seconds: float = DEFAULT_REQUEST_PAUSE_SECONDS,
    queue_name: str = DEFAULT_QUEUE_NAME,
    csv_name: str = DEFAULT_CSV_NAME,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Run the enrichment loop and return a summary dict.

    The ``resolver`` argument is the seam tests use to avoid network: it
    must be a callable ``bibcode -> {doi, arxiv_id, raw_doc}``. The CLI
    builds it from :func:`make_resolver` (which wraps the ADS token);
    tests pass in a mock.
    """
    queue_path = store / queue_name
    csv_path = store / csv_name
    if not queue_path.exists():
        raise FileNotFoundError(f"queue not found at {queue_path}")

    rows = read_queue(queue_path)
    selected = select_enrich_candidates(
        rows,
        limit=limit,
        only_candidate_ids=only_candidate_ids,
    )

    run_id = (
        dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "-" + uuid.uuid4().hex[:6] + "-enrich"
    )
    run_dir = store / RUNS_DIRNAME / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.txt"

    by_outcome: dict[str, int] = {}
    attempts_recorded: list[dict] = []

    # Open the per-run decision log; never write the token here.
    log_fh = log_path.open("a")
    try:
        for row in selected:
            cid = row["candidate_id"]
            bibcode = row["bibcode"]
            now_utc = dt.datetime.now(dt.timezone.utc)

            prior = read_attempt(store, cid)
            if should_skip_due_to_recent_attempt(prior, retry_after_seconds, now_utc):
                outcome = "skipped_recent_attempt"
                by_outcome[outcome] = by_outcome.get(outcome, 0) + 1
                attempts_recorded.append({"candidate_id": cid, "outcome": outcome})
                log_fh.write(f"{cid} {bibcode}: {outcome}\n")
                log_fh.flush()
                continue

            try:
                resolved = resolver(bibcode)
                http_error: Optional[str] = None
            except AdsHTTPError as exc:
                resolved = {"doi": None, "arxiv_id": None, "raw_doc": None}
                http_error = str(exc)

            promoted = False
            outcome: str
            if http_error:
                outcome = "http_error"
            elif resolved.get("offline_dry_run_no_token"):
                outcome = "dry_run_no_token"
            else:
                promoted, outcome = promote_row(row, resolved, run_id)

            attempt_payload = {
                "schema_version": SCHEMA_VERSION,
                "candidate_id": cid,
                "bibcode": bibcode,
                "title": row.get("title"),
                "year": row.get("year"),
                "run_id": run_id,
                "attempted_at_utc": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "outcome": outcome,
                "promoted": bool(promoted),
                "resolved_doi": resolved.get("doi"),
                "resolved_arxiv_id": resolved.get("arxiv_id"),
                "ads_doc_present": resolved.get("raw_doc") is not None,
                "http_error": http_error,
                "options": {
                    "dry_run": dry_run,
                },
            }
            if not dry_run:
                write_attempt(store, cid, attempt_payload)
                if promoted:
                    write_queue_atomic(rows, queue_path)

            by_outcome[outcome] = by_outcome.get(outcome, 0) + 1
            attempts_recorded.append(
                {
                    "candidate_id": cid,
                    "bibcode": bibcode,
                    "outcome": outcome,
                    "promoted": bool(promoted),
                    "preferred_identifier": row.get("preferred_identifier") if promoted else None,
                    "identifier_kind": row.get("identifier_kind") if promoted else None,
                }
            )
            log_fh.write(
                f"{cid} {bibcode}: outcome={outcome} promoted={promoted}\n"
            )
            log_fh.flush()

            if request_pause_seconds > 0:
                sleep(request_pause_seconds)
    finally:
        log_fh.close()
        if not dry_run:
            write_csv_mirror(rows, csv_path)

    summary_payload = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "selected": len(selected),
        "by_outcome": by_outcome,
        "attempts": attempts_recorded,
        "options": {
            "limit": limit,
            "dry_run": dry_run,
            "retry_after_seconds": retry_after_seconds,
            "request_pause_seconds": request_pause_seconds,
        },
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary_payload, indent=2, ensure_ascii=False) + "\n"
    )
    return summary_payload


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--store",
        type=Path,
        help="external acquisition store directory containing queue.jsonl",
    )
    p.add_argument(
        "--queue",
        type=Path,
        help="explicit path to a queue.jsonl (overrides --store/--queue-name)",
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
        "--limit",
        type=int,
        default=None,
        help="cap number of rows to enrich this run",
    )
    p.add_argument(
        "--candidate-id",
        action="append",
        default=[],
        help="restrict selection to specific candidate_id values (repeatable)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=("resolve and print summary; do not mutate the queue or write attempts. "
              "With no ADS token, validates selection/plumbing only and reports dry_run_no_token"),
    )
    p.add_argument(
        "--token-file",
        type=Path,
        default=None,
        help=(
            "path to a file containing the ADS bearer token "
            "(otherwise ADS_API_TOKEN / NASA_ADS_TOKEN / ADS_TOKEN env var is consulted)"
        ),
    )
    p.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"per-request HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    p.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"transient-failure retries per request (default: {DEFAULT_MAX_RETRIES})",
    )
    p.add_argument(
        "--retry-base-seconds",
        type=float,
        default=DEFAULT_RETRY_BASE_SECONDS,
        help=f"base wait for exponential backoff (default: {DEFAULT_RETRY_BASE_SECONDS})",
    )
    p.add_argument(
        "--request-pause-seconds",
        type=float,
        default=DEFAULT_REQUEST_PAUSE_SECONDS,
        help=(
            "pause between ADS requests to stay polite "
            f"(default: {DEFAULT_REQUEST_PAUSE_SECONDS})"
        ),
    )
    p.add_argument(
        "--retry-after-seconds",
        type=float,
        default=None,
        help=(
            "skip rows whose last enrichment attempt is younger than this. "
            "Default: no skip (retry every selected row)"
        ),
    )
    return p.parse_args(argv)


def _resolve_paths(args: argparse.Namespace) -> tuple[Path, Path, str]:
    """Return ``(store_dir, queue_path, queue_name)`` from parsed args.

    ``--queue`` wins over ``--store``/``--queue-name`` when both are given.
    The returned ``queue_name`` is the basename that must be passed into
    :func:`run_enrichment`; otherwise an explicit ``--queue custom.jsonl``
    would be validated here but the driver would still read the default
    ``store/queue.jsonl``.
    """
    if args.queue is not None:
        queue_path = Path(args.queue)
        store = queue_path.parent
        return store, queue_path, queue_path.name
    if args.store is None:
        raise SystemExit("error: --store or --queue is required")
    store = Path(args.store)
    return store, store / args.queue_name, args.queue_name


def main(argv: Optional[list[str]] = None) -> int:
    args = _parse_args(argv)
    store, queue_path, queue_name = _resolve_paths(args)
    if not queue_path.exists():
        print(f"error: queue not found at {queue_path}", file=sys.stderr)
        return 2

    # Resolve a token if available. A dry-run with credentials performs a
    # real ADS lookup without mutating the queue; a dry-run without
    # credentials uses a no-hit stub so callers can still validate CLI
    # plumbing and selection behaviour offline. Non-dry runs require ADS.
    resolver: Callable[[str], dict]
    token = resolve_token(args.token_file)
    if token:
        resolver = make_resolver(
            token,
            timeout=args.timeout,
            max_retries=args.max_retries,
            retry_base_seconds=args.retry_base_seconds,
        )
    elif args.dry_run:
        def resolver(_bibcode: str) -> dict:  # type: ignore[no-redef]
            return {
                "doi": None,
                "arxiv_id": None,
                "raw_doc": None,
                "offline_dry_run_no_token": True,
            }
    else:
        print(
            "error: no ADS token found. Provide --token-file PATH or set one of "
            + ", ".join(ADS_TOKEN_ENV_VARS),
            file=sys.stderr,
        )
        return 2

    only_ids: Optional[set[str]] = set(args.candidate_id) if args.candidate_id else None
    summary = run_enrichment(
        store=store,
        resolver=resolver,
        limit=args.limit,
        dry_run=args.dry_run,
        only_candidate_ids=only_ids,
        retry_after_seconds=args.retry_after_seconds,
        request_pause_seconds=args.request_pause_seconds,
        queue_name=queue_name,
        csv_name=args.csv_name,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
