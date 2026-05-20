#!/usr/bin/env python3
"""Open-ended heliophysics literature discovery (frontier / seed-expansion).

Companion to ``scripts/search_corpus.py``. Where ``search_corpus.py`` queries
the **curated** 501-entry paper-skill corpus that ships in this bundle, this
script reaches **outward** to public bibliographic backends and produces a
JSONL stream of *candidate* records that the corpus does not yet contain.

The script is the first concrete increment of HelioSI's open-ended literature
pipeline. It is intentionally narrow:

  - It DISCOVERS candidates. It does NOT compile them into paper-skills.
  - It TAGS each candidate against a heliophysics seed taxonomy.
  - It DEDUPES across backends by (doi | arxiv_id | bibcode |
    normalized-title+year).
  - It does NOT claim "all relevant heliophysics literature" — every run is a
    bounded frontier sample governed by ``--max-results`` and the query slate.

Backends
--------
The default slate is no-key:

  - arXiv API           (https://export.arxiv.org/api/query)
  - OpenAlex            (https://api.openalex.org/works)

Two are optional and only activated with explicit flags / env vars:

  - Crossref            (--enable-crossref) -- public, no key required, but
                        kept opt-in to keep default runs fast and to make
                        backend addition an explicit choice.
  - NASA ADS            (--enable-ads) -- requires ADS_API_TOKEN /
                        NASA_ADS_TOKEN / ADS_TOKEN in the environment. The
                        script runs without ADS credentials; if --enable-ads
                        is given and no token is found the run aborts loudly
                        rather than silently downgrading.

Modes
-----
``--dry-run`` (default) makes NO network calls. It exercises query building,
seed-taxonomy tagging, and dedupe by reading the local fixture file at
``tests/fixtures/discovery/sample_records.jsonl`` (a small mixed
arXiv+OpenAlex payload). This is the mode CI uses.

``--live`` issues real HTTP requests via ``urllib.request`` against the
selected backends. Rate-limited to one request at a time with a short pause
between pages (``--page-pause-seconds``). No third-party HTTP library is
required.

The HTTP layer is polite by default: every request advertises a descriptive
``User-Agent`` so backend operators can identify the client; transient
failures (HTTP 429 + 5xx, ``URLError``) trigger a bounded exponential
backoff with ``--max-retries`` attempts and a deterministic
``--retry-base-seconds`` floor between attempts. Live arXiv calls in
particular have been observed returning 429 on this host -- the backoff
keeps the script from making the situation worse, and a permanent failure
is surfaced as a structured ``summary.errors[]`` entry rather than
silently dropped.

Output
------
A JSONL file (``--output``, default stdout) with one candidate per line:

  {
    "id": "<dedupe-key>",
    "source": "arxiv" | "openalex" | "crossref" | "ads",
    "title": "...",
    "year": 2024,
    "doi": "10.xxxx/yyy" | null,
    "arxiv_id": "2401.01234" | null,
    "bibcode": "2024..." | null,
    "url": "https://...",
    "authors": ["..."],   # may be empty; never silently fabricated
    "abstract": "..." | null,
    "topic_tags": ["solar-wind", "psp", ...],
    "query": "<query string that surfaced this record>",
    "discovered_at_utc": "2026-05-19T12:34:56Z"
  }

A trailing JSON-encoded summary line is also written to stderr.

Framing (honest disclosure)
---------------------------
This is a SEED expansion. A single run is a frontier sample, not a complete
survey. The candidate JSONL is downstream feed material for the paper-skill
authoring pipeline; it is NOT itself an addition to the curated 501 corpus.

See ``reports/literature_discovery_pipeline.md`` for the wider pipeline
strategy and how candidates feed back into the curated bundle.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import hashlib
import io
import json
import os
import re
import sys
import textwrap
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

__version__ = "0.1.0"

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
FIXTURE_DIR = BUNDLE / "tests" / "fixtures" / "discovery"
DEFAULT_FIXTURE = FIXTURE_DIR / "sample_records.jsonl"
DEFAULT_CORPUS_MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"

USER_AGENT = (
    f"heliosi-discover/{__version__} "
    "(+https://github.com/huangzesen/heliosi-501-corpus-skill)"
)

# ---------------------------------------------------------------------------
# Seed taxonomy.
#
# Each entry maps a tag slug to a tuple of lowercase substring patterns that,
# when found inside title+abstract, will tag the record. This is a SEED
# taxonomy, not a final classification scheme: we expect it to grow as the
# pipeline matures. Patterns are deliberately broad so that an open-ended
# frontier sample gets useful first-pass labels.
# ---------------------------------------------------------------------------

SEED_TAXONOMY: Dict[str, Tuple[str, ...]] = {
    "solar-wind": ("solar wind", "solar-wind"),
    "corona": ("corona", "coronal "),
    "cme": (
        "coronal mass ejection",
        "cme ",
        " cme,",
        " cmes ",
        "icme",
    ),
    "magnetosphere": ("magnetosphere", "magnetospheric"),
    "ionosphere": ("ionosphere", "ionospheric"),
    "heliosphere": ("heliosphere", "heliospheric"),
    "parker-solar-probe": ("parker solar probe", " psp "),
    "solar-orbiter": ("solar orbiter", "solo "),
    "ulysses": ("ulysses",),
    "ace": (" ace ", "advanced composition explorer"),
    "wind-spacecraft": (" wind spacecraft", "wind/swe", "wind/3dp"),
    "turbulence": ("turbulence", "turbulent"),
    "heating": ("coronal heating", "solar wind heating", " heating "),
    "reconnection": ("reconnection", "reconnect"),
    "pfss": ("pfss", "potential field source surface"),
    "switchbacks": ("switchback", "switchbacks"),
    "sep": (
        "solar energetic particle",
        " sep ",
        " seps ",
        "sep event",
    ),
    "shock": ("shock", "shocks"),
    "alfven-waves": ("alfven", "alfvén", "alfvenic"),
    "flare": (" flare ", "solar flare", "x-class flare", "m-class flare"),
    "kinetic-physics": ("kinetic", "vlasov", "pic simulation"),
    "machine-learning": (
        "machine learning",
        "neural network",
        "deep learning",
        "transformer model",
    ),
}

# ---------------------------------------------------------------------------
# Query slate. Each entry pairs a backend with a human-readable label and the
# raw query token (the backend-specific URL is built later). Keeping the slate
# in code rather than in a separate JSON file makes the script self-contained
# and reproducible; users can extend it via --extra-query.
# ---------------------------------------------------------------------------

DEFAULT_QUERIES: Tuple[Tuple[str, str], ...] = (
    ("solar wind turbulence", "core-helio"),
    ("Parker Solar Probe switchbacks", "core-helio"),
    ("coronal mass ejection reconnection", "core-helio"),
    ("PFSS open flux", "core-helio"),
    ("solar energetic particle event", "core-helio"),
    ("solar wind classification machine learning", "core-helio"),
)


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

_WS_RE = re.compile(r"\s+")
_TITLE_PUNCT_RE = re.compile(r"[^\w\s]")
_ARXIV_NEW_RE = re.compile(r"^\d{4}\.\d{4,6}(v\d+)?$")
_ARXIV_OLD_RE = re.compile(r"^[a-z\-]+/\d{7}(v\d+)?$", re.IGNORECASE)


def fold_text(s: Optional[str]) -> str:
    """NFKD-fold + lowercase + collapse whitespace. Returns '' for None."""
    if not s:
        return ""
    folded = unicodedata.normalize("NFKD", s)
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return _WS_RE.sub(" ", folded).strip().lower()


def normalize_title(title: Optional[str]) -> str:
    """Aggressive title normalisation for dedupe fallback.

    Lowercase, strip combining marks, drop punctuation, collapse whitespace.
    Two titles that differ only in punctuation / case / accents will collide.
    """
    if not title:
        return ""
    folded = fold_text(title)
    folded = _TITLE_PUNCT_RE.sub(" ", folded)
    return _WS_RE.sub(" ", folded).strip()


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    if not doi:
        return None
    doi = doi.strip()
    if doi.lower().startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    elif doi.lower().startswith("http://doi.org/"):
        doi = doi[len("http://doi.org/"):]
    elif doi.lower().startswith("doi:"):
        doi = doi[4:]
    doi = doi.strip().lower()
    return doi or None


def normalize_arxiv_id(ax: Optional[str]) -> Optional[str]:
    if not ax:
        return None
    ax = ax.strip()
    for prefix in ("arXiv:", "arxiv:", "https://arxiv.org/abs/", "http://arxiv.org/abs/"):
        if ax.lower().startswith(prefix.lower()):
            ax = ax[len(prefix):]
            break
    ax = ax.strip()
    if _ARXIV_NEW_RE.match(ax) or _ARXIV_OLD_RE.match(ax):
        # Strip the version suffix for stable dedupe.
        return re.sub(r"v\d+$", "", ax, flags=re.IGNORECASE).lower()
    return None


# ---------------------------------------------------------------------------
# Dedupe key
# ---------------------------------------------------------------------------

def dedupe_key(record: Dict) -> str:
    """Deterministic dedupe key.

    Priority: DOI > arXiv ID > ADS bibcode > normalized-title + year fallback.
    The fallback hashes title+year so two backends that disagree on title
    case / punctuation still collide, while titles that differ at the word
    level do not.
    """
    doi = normalize_doi(record.get("doi"))
    if doi:
        return f"doi:{doi}"
    ax = normalize_arxiv_id(record.get("arxiv_id"))
    if ax:
        return f"arxiv:{ax}"
    bib = (record.get("bibcode") or "").strip().lower()
    if bib:
        return f"bibcode:{bib}"
    title_norm = normalize_title(record.get("title"))
    year = record.get("year") or ""
    if title_norm:
        h = hashlib.sha1(f"{title_norm}|{year}".encode("utf-8")).hexdigest()[:16]
        return f"title:{h}"
    # Last-ditch fallback so we always emit something deterministic.
    payload = json.dumps(record, sort_keys=True, default=str)
    return "hash:" + hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_topics(title: Optional[str], abstract: Optional[str]) -> List[str]:
    """Return sorted list of seed-taxonomy tag slugs that match the record."""
    haystack = " " + fold_text(title) + " " + fold_text(abstract) + " "
    hits: List[str] = []
    for slug, patterns in SEED_TAXONOMY.items():
        for pat in patterns:
            if pat in haystack:
                hits.append(slug)
                break
    return sorted(set(hits))


# ---------------------------------------------------------------------------
# Backend query-URL builders (pure functions; tested without network)
# ---------------------------------------------------------------------------

def build_arxiv_url(query: str, *, max_results: int, start: int = 0) -> str:
    params = {
        "search_query": f"all:{query}",
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)


def build_openalex_url(query: str, *, max_results: int, page: int = 1) -> str:
    # OpenAlex per-page max is 200. We cap to keep behavior predictable.
    per_page = min(max(max_results, 1), 200)
    params = {
        "search": query,
        "per-page": str(per_page),
        "page": str(page),
    }
    return "https://api.openalex.org/works?" + urllib.parse.urlencode(params)


def build_crossref_url(query: str, *, max_results: int, offset: int = 0) -> str:
    params = {
        "query": query,
        "rows": str(min(max(max_results, 1), 1000)),
        "offset": str(offset),
    }
    return "https://api.crossref.org/works?" + urllib.parse.urlencode(params)


def build_ads_url(query: str, *, max_results: int, start: int = 0) -> str:
    params = {
        "q": query,
        "rows": str(min(max(max_results, 1), 2000)),
        "start": str(start),
        "fl": "bibcode,title,author,year,doi,abstract,identifier",
    }
    return "https://api.adsabs.harvard.edu/v1/search/query?" + urllib.parse.urlencode(params)


# ---------------------------------------------------------------------------
# Backend response parsers (pure functions; tested with on-disk fixtures)
# ---------------------------------------------------------------------------

_ATOM_NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def parse_arxiv_atom(xml_bytes: bytes) -> List[Dict]:
    """Parse arXiv Atom XML into normalized candidate dicts."""
    root = ET.fromstring(xml_bytes)
    out: List[Dict] = []
    for entry in root.findall("a:entry", _ATOM_NS):
        title = (entry.findtext("a:title", default="", namespaces=_ATOM_NS) or "").strip()
        summary = (entry.findtext("a:summary", default="", namespaces=_ATOM_NS) or "").strip()
        published = entry.findtext("a:published", default="", namespaces=_ATOM_NS) or ""
        year = _year_from_iso(published)
        arxiv_id = None
        eid = (entry.findtext("a:id", default="", namespaces=_ATOM_NS) or "").strip()
        # Atom id is like https://arxiv.org/abs/2401.01234v1
        if "/abs/" in eid:
            arxiv_id = normalize_arxiv_id(eid.rsplit("/abs/", 1)[1])
        doi = None
        for link in entry.findall("a:link", _ATOM_NS):
            if link.get("title") == "doi":
                doi = normalize_doi(link.get("href"))
                break
        if doi is None:
            arxiv_doi = entry.findtext("arxiv:doi", default="", namespaces=_ATOM_NS)
            if arxiv_doi:
                doi = normalize_doi(arxiv_doi)
        authors = [
            (a.findtext("a:name", default="", namespaces=_ATOM_NS) or "").strip()
            for a in entry.findall("a:author", _ATOM_NS)
        ]
        authors = [a for a in authors if a]
        url = eid or (
            f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
        )
        out.append(
            {
                "source": "arxiv",
                "title": title,
                "year": year,
                "doi": doi,
                "arxiv_id": arxiv_id,
                "bibcode": None,
                "url": url,
                "authors": authors,
                "abstract": summary or None,
            }
        )
    return out


def parse_openalex_json(payload: Dict) -> List[Dict]:
    """Parse OpenAlex /works JSON into normalized candidate dicts."""
    out: List[Dict] = []
    for w in payload.get("results", []):
        title = (w.get("title") or w.get("display_name") or "").strip()
        year = w.get("publication_year")
        doi = normalize_doi(w.get("doi"))
        ax = None
        for sid_label, sid_val in (w.get("ids") or {}).items():
            if sid_label == "arxiv":
                ax = normalize_arxiv_id(sid_val)
                break
        # Some OpenAlex records expose arXiv via locations / open_access.
        if ax is None:
            for loc in (w.get("locations") or []):
                src = (loc or {}).get("source") or {}
                if (src.get("display_name") or "").lower() == "arxiv":
                    ax_candidate = (loc.get("landing_page_url") or "")
                    ax2 = normalize_arxiv_id(ax_candidate)
                    if ax2:
                        ax = ax2
                        break
        authors: List[str] = []
        for au in w.get("authorships") or []:
            name = ((au or {}).get("author") or {}).get("display_name")
            if name:
                authors.append(name)
        abstract = _reconstruct_openalex_abstract(w.get("abstract_inverted_index"))
        out.append(
            {
                "source": "openalex",
                "title": title,
                "year": year,
                "doi": doi,
                "arxiv_id": ax,
                "bibcode": None,
                "url": w.get("id") or "",
                "authors": authors,
                "abstract": abstract,
            }
        )
    return out


def parse_crossref_json(payload: Dict) -> List[Dict]:
    out: List[Dict] = []
    for w in (payload.get("message") or {}).get("items", []):
        titles = w.get("title") or []
        title = (titles[0] if titles else "").strip()
        year = None
        for k in ("published-print", "published-online", "issued", "created"):
            parts = ((w.get(k) or {}).get("date-parts") or [[None]])
            if parts and parts[0] and parts[0][0]:
                year = parts[0][0]
                break
        doi = normalize_doi(w.get("DOI"))
        authors: List[str] = []
        for au in w.get("author") or []:
            given = (au.get("given") or "").strip()
            family = (au.get("family") or "").strip()
            full = (f"{given} {family}").strip()
            if full:
                authors.append(full)
        out.append(
            {
                "source": "crossref",
                "title": title,
                "year": year,
                "doi": doi,
                "arxiv_id": None,
                "bibcode": None,
                "url": w.get("URL") or (f"https://doi.org/{doi}" if doi else ""),
                "authors": authors,
                "abstract": (w.get("abstract") or "").strip() or None,
            }
        )
    return out


def parse_ads_json(payload: Dict) -> List[Dict]:
    out: List[Dict] = []
    for d in ((payload.get("response") or {}).get("docs") or []):
        titles = d.get("title") or []
        title = (titles[0] if titles else "").strip()
        year = d.get("year")
        if isinstance(year, str) and year.isdigit():
            year = int(year)
        doi_list = d.get("doi") or []
        doi = normalize_doi(doi_list[0]) if doi_list else None
        ax = None
        for ident in d.get("identifier") or []:
            ax_candidate = normalize_arxiv_id(ident)
            if ax_candidate:
                ax = ax_candidate
                break
        authors = list(d.get("author") or [])
        bib = (d.get("bibcode") or "").strip() or None
        out.append(
            {
                "source": "ads",
                "title": title,
                "year": year,
                "doi": doi,
                "arxiv_id": ax,
                "bibcode": bib,
                "url": (f"https://ui.adsabs.harvard.edu/abs/{bib}/abstract"
                        if bib else ""),
                "authors": authors,
                "abstract": (d.get("abstract") or "").strip() or None,
            }
        )
    return out


def _year_from_iso(s: str) -> Optional[int]:
    if not s:
        return None
    if len(s) >= 4 and s[:4].isdigit():
        return int(s[:4])
    return None


def _reconstruct_openalex_abstract(inv_index: Optional[Dict]) -> Optional[str]:
    if not inv_index:
        return None
    # inv_index: {word: [positions...]}.  Reconstruct in position order.
    positions: List[Tuple[int, str]] = []
    for word, pos_list in inv_index.items():
        for p in pos_list or []:
            positions.append((p, word))
    if not positions:
        return None
    positions.sort()
    return " ".join(w for _, w in positions)


# ---------------------------------------------------------------------------
# Fixture loading (dry-run mode)
# ---------------------------------------------------------------------------

def load_fixture(path: Path) -> List[Dict]:
    """Load a JSONL fixture file as already-normalised candidate records.

    Each line is a JSON object using the *normalised* schema (the same shape
    the parsers emit). This lets dry-run mode exercise dedupe + classification
    + I/O without touching the network and without depending on raw
    backend-format fixtures.
    """
    out: List[Dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(
                    f"discover_heliophysics_literature: bad fixture line "
                    f"{path}:{line_no}: {e}"
                ) from None
    return out


# ---------------------------------------------------------------------------
# HTTP fetch (live mode only)
#
# Polite-by-default:
#   - identifies as USER_AGENT so backend operators can attribute traffic;
#   - retries 429 / 5xx and transient URLError with bounded exponential
#     backoff (``retries=N`` -> sleep base_seconds * 2**attempt);
#   - lets the caller inject a ``sleep`` shim so tests don't actually sleep
#     and so the backoff schedule is verifiable.
#
# Live arXiv has been observed responding 429 even to scale-estimate
# queries on this host. The retry/backoff path here is the script's
# response: it does NOT retry instantly, does NOT log credentials, and
# does NOT mask a permanent failure as success.
# ---------------------------------------------------------------------------

# HTTPError subclasses URLError, so this single tuple covers both.
_TRANSIENT_HTTP_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_RETRY_BASE_SECONDS = 1.5


class _HTTPRetryError(RuntimeError):
    """Raised after all polite retries are exhausted."""


def _http_get(
    url: str,
    *,
    timeout: float,
    headers: Optional[Dict[str, str]] = None,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_base_seconds: float = _DEFAULT_RETRY_BASE_SECONDS,
    sleep: "callable" = time.sleep,
    urlopen: "callable" = urllib.request.urlopen,
) -> bytes:
    """Polite HTTP GET with bounded exponential backoff.

    Parameters
    ----------
    url:
        The URL to fetch.
    timeout:
        Per-attempt HTTP timeout, seconds.
    headers:
        Extra headers (e.g. an ``Authorization`` bearer). ``User-Agent`` is
        always set to :data:`USER_AGENT`.
    max_retries:
        Number of *additional* attempts after the first (so total attempts
        is ``max_retries + 1``). Must be >= 0.
    retry_base_seconds:
        Base wait for the exponential backoff schedule. The wait before
        attempt ``i`` (i >= 1) is ``retry_base_seconds * 2 ** (i - 1)``.
    sleep, urlopen:
        Test seams. Defaults point at the real ``time.sleep`` and
        ``urllib.request.urlopen``.
    """
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    last_exc: Optional[Exception] = None
    attempts = max_retries + 1
    for attempt in range(attempts):
        if attempt > 0:
            sleep(retry_base_seconds * (2 ** (attempt - 1)))
        try:
            with urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_exc = e
            if e.code in _TRANSIENT_HTTP_STATUSES and attempt < attempts - 1:
                continue
            # Non-retryable, or last attempt: surface a structured error.
            raise _HTTPRetryError(
                f"HTTP {e.code} for {url} after "
                f"{attempt + 1}/{attempts} attempts: {e.reason}"
            ) from e
        except urllib.error.URLError as e:
            last_exc = e
            if attempt < attempts - 1:
                continue
            raise _HTTPRetryError(
                f"URLError for {url} after {attempt + 1}/{attempts} "
                f"attempts: {e.reason}"
            ) from e
    # Unreachable -- the loop either returns or raises.
    raise _HTTPRetryError(
        f"unreachable retry path for {url}: last_exc={last_exc!r}"
    )


# ---------------------------------------------------------------------------
# Corpus manifest novelty join
#
# A discovery candidate is "already curated" if it matches an entry in the
# curated v2 manifest (default: references/corpus_manifest_v2.json) by any
# of the canonical keys the script already uses for dedupe:
#
#   1. DOI (lowercased, resolver prefix stripped)
#   2. arXiv ID (version suffix stripped, lowercased)
#   3. ADS bibcode (lowercased) -- manifest currently exposes no bibcodes,
#      but the index tolerates them so future manifest revisions Just Work
#   4. Normalised title + year (SHA1-hashed the same way as dedupe_key)
#
# The manifest stores some arXiv values as sentinels ("not-in-local-inventory")
# or TODO placeholders ("TODO_verify", "TODO_verify_with_full_text"). Those
# strings are NOT valid arXiv IDs and must not match candidates whose arXiv
# field happens to contain the same string -- ``_manifest_arxiv_value`` runs
# them through ``normalize_arxiv_id`` which rejects anything that doesn't
# match the YYMM.NNNNN or category/YYMMNNN format.
#
# Limits (honest disclosure; mirror what the report calls out):
#   - Manifest entries without DOI / arXiv / bibcode can only be matched via
#     title+year, which is sensitive to author-supplied title differences
#     (subtitle vs no subtitle, "&" vs "and", etc.). Counts are best-effort,
#     not authoritative.
#   - The join is strictly read-only and operates ONLY on the manifest
#     metadata in references/corpus_manifest_v2.json. It does NOT crack
#     open per-entry SKILL.md / metadata.yaml frontmatter and so cannot
#     catch a paper that the curated entry advertises only in prose.
# ---------------------------------------------------------------------------


_MANIFEST_ARXIV_SENTINELS = frozenset(
    {"", "none", "n/a", "na", "not-in-local-inventory"}
)


def _manifest_arxiv_value(raw: Optional[str]) -> Optional[str]:
    """Return a normalised arXiv ID for a manifest ``arxiv:`` field value, or
    ``None`` if the value is a sentinel / TODO placeholder / unparseable."""
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip()
    if not s:
        return None
    low = s.lower()
    if low in _MANIFEST_ARXIV_SENTINELS:
        return None
    # Reject TODO/TBD placeholders before handing to normalize_arxiv_id, which
    # would also reject them but with less explicit intent.
    if re.match(r"^(?:todo|tbd)", low):
        return None
    return normalize_arxiv_id(s)


def _manifest_title_year_key(title: Optional[str], year) -> Optional[str]:
    """Reproduce the title+year branch of :func:`dedupe_key` so the manifest
    index uses an identical hash and lookups collide."""
    title_norm = normalize_title(title)
    if not title_norm:
        return None
    year_str = year if year is not None else ""
    h = hashlib.sha1(f"{title_norm}|{year_str}".encode("utf-8")).hexdigest()[:16]
    return f"title:{h}"


def build_corpus_manifest_index(path: Path) -> Dict:
    """Load a v2 corpus manifest and index it by canonical keys.

    Returns a dict with the following keys:

      - ``by_doi``       : {normalised DOI -> entry-summary dict}
      - ``by_arxiv``     : {normalised arXiv ID -> entry-summary dict}
      - ``by_bibcode``   : {lowercased bibcode -> entry-summary dict}
      - ``by_title_year``: {title-year sha1 key -> entry-summary dict}
      - ``entry_count``  : int, number of manifest rows seen
      - ``source_path``  : str, the path the index was built from

    Each entry-summary dict carries ``{"slug": ..., "title": ...}`` so the
    caller can present a human-readable provenance string back to the user.
    Sentinel arXiv values (``"not-in-local-inventory"``) and TODO/TBD
    placeholders are filtered out so they cannot create spurious matches.
    """
    with open(path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    entries = manifest.get("entries") or []
    by_doi: Dict[str, Dict] = {}
    by_arxiv: Dict[str, Dict] = {}
    by_bibcode: Dict[str, Dict] = {}
    by_title_year: Dict[str, Dict] = {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        summary = {"slug": e.get("slug"), "title": e.get("title")}
        doi = normalize_doi(e.get("doi"))
        if doi:
            by_doi.setdefault(doi, summary)
        ax = _manifest_arxiv_value(e.get("arxiv"))
        if ax:
            by_arxiv.setdefault(ax, summary)
        bib = (e.get("bibcode") or "")
        if isinstance(bib, str) and bib.strip():
            by_bibcode.setdefault(bib.strip().lower(), summary)
        tk = _manifest_title_year_key(e.get("title"), e.get("year"))
        if tk:
            by_title_year.setdefault(tk, summary)
    return {
        "by_doi": by_doi,
        "by_arxiv": by_arxiv,
        "by_bibcode": by_bibcode,
        "by_title_year": by_title_year,
        "entry_count": len(entries),
        "source_path": str(path),
    }


_NOVELTY_FIELDS_DISABLED: Dict = {
    "corpus_status": "unjoined",
    "corpus_match_via": None,
    "corpus_match_slugs": [],
    "corpus_match_titles": [],
}


def annotate_candidate_with_corpus_status(
    record: Dict, index: Optional[Dict]
) -> Dict:
    """Return a shallow copy of ``record`` with novelty-join fields filled in.

    If ``index`` is ``None``, the record is annotated as ``unjoined`` -- no
    novelty claim is made either way. Otherwise the canonical keys are tried
    in priority order (doi -> arxiv -> bibcode -> title+year) and the FIRST
    hit wins; the record reports which key produced the match so the caller
    can audit / debug the join.
    """
    out = dict(record)
    if index is None:
        out.update(_NOVELTY_FIELDS_DISABLED)
        return out

    doi = normalize_doi(record.get("doi"))
    if doi and doi in index["by_doi"]:
        m = index["by_doi"][doi]
        out["corpus_status"] = "already_curated"
        out["corpus_match_via"] = "doi"
        out["corpus_match_slugs"] = [m.get("slug")] if m.get("slug") else []
        out["corpus_match_titles"] = [m.get("title")] if m.get("title") else []
        return out

    ax = normalize_arxiv_id(record.get("arxiv_id"))
    if ax and ax in index["by_arxiv"]:
        m = index["by_arxiv"][ax]
        out["corpus_status"] = "already_curated"
        out["corpus_match_via"] = "arxiv"
        out["corpus_match_slugs"] = [m.get("slug")] if m.get("slug") else []
        out["corpus_match_titles"] = [m.get("title")] if m.get("title") else []
        return out

    bib = (record.get("bibcode") or "").strip().lower()
    if bib and bib in index["by_bibcode"]:
        m = index["by_bibcode"][bib]
        out["corpus_status"] = "already_curated"
        out["corpus_match_via"] = "bibcode"
        out["corpus_match_slugs"] = [m.get("slug")] if m.get("slug") else []
        out["corpus_match_titles"] = [m.get("title")] if m.get("title") else []
        return out

    tk = _manifest_title_year_key(record.get("title"), record.get("year"))
    if tk and tk in index["by_title_year"]:
        m = index["by_title_year"][tk]
        out["corpus_status"] = "already_curated"
        out["corpus_match_via"] = "title_year"
        out["corpus_match_slugs"] = [m.get("slug")] if m.get("slug") else []
        out["corpus_match_titles"] = [m.get("title")] if m.get("title") else []
        return out

    out["corpus_status"] = "new_candidate"
    out["corpus_match_via"] = None
    out["corpus_match_slugs"] = []
    out["corpus_match_titles"] = []
    return out


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def normalise_candidate(
    record: Dict, *, query: Optional[str], now_iso: str
) -> Dict:
    """Apply tags + dedupe key + timestamp; never mutate caller's dict."""
    out = dict(record)
    out.setdefault("authors", [])
    out["topic_tags"] = classify_topics(out.get("title"), out.get("abstract"))
    out["query"] = query
    out["discovered_at_utc"] = now_iso
    out["id"] = dedupe_key(out)
    # Stable field order is nice for diffs; not strictly required.
    canonical_keys = [
        "id",
        "source",
        "title",
        "year",
        "doi",
        "arxiv_id",
        "bibcode",
        "url",
        "authors",
        "abstract",
        "topic_tags",
        "query",
        "discovered_at_utc",
        # Novelty-join fields are filled in by the orchestrator after dedupe;
        # they are emitted on every output record so downstream consumers can
        # filter on corpus_status without an extra pass.
        "corpus_status",
        "corpus_match_via",
        "corpus_match_slugs",
        "corpus_match_titles",
    ]
    return {k: out.get(k) for k in canonical_keys}


def dedupe(records: Iterable[Dict]) -> List[Dict]:
    """Stable dedupe: first occurrence wins, ordering preserved."""
    seen = {}
    for rec in records:
        key = rec.get("id") or dedupe_key(rec)
        if key in seen:
            continue
        seen[key] = rec
    return list(seen.values())


def _utc_now_iso() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _resolve_ads_token() -> Optional[str]:
    for var in ("ADS_API_TOKEN", "NASA_ADS_TOKEN", "ADS_TOKEN"):
        val = os.environ.get(var)
        if val:
            return val.strip()
    return None


def fetch_backend(
    backend: str,
    query: str,
    *,
    max_results: int,
    timeout: float,
    ads_token: Optional[str] = None,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_base_seconds: float = _DEFAULT_RETRY_BASE_SECONDS,
) -> List[Dict]:
    """Single page fetch + parse for one backend. Returns normalised records.

    Network errors / transient HTTP failures are retried via :func:`_http_get`
    with bounded exponential backoff; permanent failure raises
    :class:`_HTTPRetryError`, which the orchestrator captures as a
    structured ``summary.errors[]`` row.
    """
    http_kwargs = {
        "timeout": timeout,
        "max_retries": max_retries,
        "retry_base_seconds": retry_base_seconds,
    }
    if backend == "arxiv":
        url = build_arxiv_url(query, max_results=max_results)
        return parse_arxiv_atom(_http_get(url, **http_kwargs))
    if backend == "openalex":
        url = build_openalex_url(query, max_results=max_results)
        return parse_openalex_json(json.loads(_http_get(url, **http_kwargs)))
    if backend == "crossref":
        url = build_crossref_url(query, max_results=max_results)
        return parse_crossref_json(json.loads(_http_get(url, **http_kwargs)))
    if backend == "ads":
        if not ads_token:
            raise RuntimeError(
                "ADS backend requested but no ADS_API_TOKEN / NASA_ADS_TOKEN "
                "/ ADS_TOKEN found in environment."
            )
        url = build_ads_url(query, max_results=max_results)
        payload = _http_get(
            url,
            headers={"Authorization": f"Bearer {ads_token}"},
            **http_kwargs,
        )
        return parse_ads_json(json.loads(payload))
    raise ValueError(f"unknown backend: {backend!r}")


def run_discovery(
    *,
    queries: Sequence[Tuple[str, str]],
    backends: Sequence[str],
    max_results: int,
    live: bool,
    fixture_path: Path,
    timeout: float,
    page_pause_seconds: float,
    ads_token: Optional[str],
    now_iso: Optional[str] = None,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_base_seconds: float = _DEFAULT_RETRY_BASE_SECONDS,
    corpus_manifest_path: Optional[Path] = None,
) -> Tuple[List[Dict], Dict]:
    """Return (deduped_candidates, summary_dict).

    Pure-Python orchestration; HTTP only happens when ``live=True``.

    ``corpus_manifest_path`` enables the novelty join: when set to a readable
    v2 manifest JSON, each deduped candidate is annotated with a
    ``corpus_status`` of ``already_curated`` or ``new_candidate`` and the
    summary reports the counts. When ``None`` (or the path does not exist),
    candidates are annotated ``unjoined`` and the summary records that the
    join was disabled -- no novelty claim is made.
    """
    now_iso = now_iso or _utc_now_iso()
    raw: List[Dict] = []
    per_backend_counts: Dict[str, int] = {b: 0 for b in backends}
    per_query_counts: Dict[str, int] = {}
    errors: List[Dict] = []

    if not live:
        # Dry-run: load the fixture once, then tag every record with the FIRST
        # query so dedupe still behaves and topic tagging fires. The fixture
        # already declares its own "source" per line.
        if not fixture_path.is_file():
            raise SystemExit(
                f"discover_heliophysics_literature: fixture not found: "
                f"{fixture_path}"
            )
        fixture_records = load_fixture(fixture_path)
        default_query = queries[0][0] if queries else "dry-run"
        for rec in fixture_records:
            src = rec.get("source") or "unknown"
            if src in per_backend_counts:
                per_backend_counts[src] += 1
            raw.append(normalise_candidate(rec, query=default_query, now_iso=now_iso))
        per_query_counts[default_query] = len(fixture_records)
    else:
        for query, _label in queries:
            per_query_counts.setdefault(query, 0)
            for backend in backends:
                try:
                    records = fetch_backend(
                        backend,
                        query,
                        max_results=max_results,
                        timeout=timeout,
                        ads_token=ads_token,
                        max_retries=max_retries,
                        retry_base_seconds=retry_base_seconds,
                    )
                except (_HTTPRetryError, urllib.error.URLError, urllib.error.HTTPError, RuntimeError, ET.ParseError, json.JSONDecodeError) as e:
                    errors.append(
                        {"backend": backend, "query": query, "error": str(e)[:200]}
                    )
                    continue
                per_backend_counts[backend] = per_backend_counts.get(backend, 0) + len(records)
                per_query_counts[query] += len(records)
                for rec in records:
                    raw.append(normalise_candidate(rec, query=query, now_iso=now_iso))
                if page_pause_seconds > 0:
                    time.sleep(page_pause_seconds)

    deduped = dedupe(raw)

    # ----- Novelty join against the curated v2 manifest --------------------
    manifest_index: Optional[Dict] = None
    manifest_resolved_path: Optional[str] = None
    if corpus_manifest_path is not None:
        mp = Path(corpus_manifest_path)
        if mp.is_file():
            manifest_index = build_corpus_manifest_index(mp)
            manifest_resolved_path = str(mp)
    annotated: List[Dict] = [
        annotate_candidate_with_corpus_status(rec, manifest_index)
        for rec in deduped
    ]
    already_curated = sum(
        1 for c in annotated if c.get("corpus_status") == "already_curated"
    )
    new_candidates = sum(
        1 for c in annotated if c.get("corpus_status") == "new_candidate"
    )
    unjoined = sum(
        1 for c in annotated if c.get("corpus_status") == "unjoined"
    )
    novelty_join_summary = {
        "enabled": manifest_index is not None,
        "manifest_path": manifest_resolved_path,
        "manifest_entry_count": (
            manifest_index["entry_count"] if manifest_index is not None else 0
        ),
        "already_curated_count": already_curated,
        "new_candidate_count": new_candidates,
        "unjoined_count": unjoined,
        "match_priority": ["doi", "arxiv", "bibcode", "title_year"],
        "limits": (
            "title+year fallback is sensitive to title-string differences "
            "(subtitle vs no subtitle, '&' vs 'and', NFKD-folded accents); "
            "manifest entries without DOI/arXiv/bibcode rely on this "
            "fallback and so the join is best-effort, not authoritative. "
            "The join reads only the v2 manifest metadata -- it does not "
            "crack open per-entry SKILL.md / metadata.yaml frontmatter."
        ),
    }

    summary = {
        "mode": "live" if live else "dry-run",
        "queries": [q for q, _ in queries],
        "backends": list(backends),
        "raw_candidate_count": len(raw),
        "deduped_candidate_count": len(deduped),
        "per_backend_counts": per_backend_counts,
        "per_query_counts": per_query_counts,
        "errors": errors,
        "novelty_join": novelty_join_summary,
        "polite_http": {
            "user_agent": USER_AGENT,
            "max_retries": max_retries,
            "retry_base_seconds": retry_base_seconds,
            "retry_statuses": sorted(_TRANSIENT_HTTP_STATUSES),
        },
        "framing": (
            "frontier seed-expansion sample; not a complete survey of the "
            "heliophysics literature"
        ),
        "discovered_at_utc": now_iso,
    }
    return annotated, summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

EPILOG = """\
Examples:
  # Default dry-run (no network; reads tests/fixtures/discovery/...):
  python3 scripts/discover_heliophysics_literature.py --output /tmp/cand.jsonl

  # Live run, default no-key backends (arXiv + OpenAlex):
  python3 scripts/discover_heliophysics_literature.py --live --max-results 25 \\
      --output /tmp/cand.jsonl

  # Live run with the optional Crossref backend added:
  python3 scripts/discover_heliophysics_literature.py --live \\
      --enable-crossref --max-results 10

  # Live run with NASA ADS (requires ADS_API_TOKEN / NASA_ADS_TOKEN / ADS_TOKEN):
  ADS_API_TOKEN=... python3 scripts/discover_heliophysics_literature.py \\
      --live --enable-ads --max-results 20

Honest framing:
  Each run is a bounded frontier sample. The output is a CANDIDATE queue,
  not a final corpus. See reports/literature_discovery_pipeline.md for how
  candidates feed the curated 501-entry paper-skill bundle.
"""


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="discover_heliophysics_literature.py",
        description=(
            "Discover candidate heliophysics literature from public backends "
            "and emit a deduplicated, tag-classified JSONL stream."
        ),
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True,
                      help="(default) Read fixture; make NO network calls.")
    mode.add_argument("--live", action="store_true", default=False,
                      help="Issue real HTTP requests to selected backends.")

    p.add_argument("--max-results", type=int, default=10,
                   help="Max results per (backend, query) page (default: 10).")
    p.add_argument("--output", type=str, default="-",
                   help="Output JSONL path; '-' for stdout (default).")
    p.add_argument("--fixture", type=str, default=str(DEFAULT_FIXTURE),
                   help="Fixture JSONL for --dry-run mode "
                        f"(default: {DEFAULT_FIXTURE}).")
    p.add_argument("--timeout", type=float, default=20.0,
                   help="HTTP timeout in seconds (live mode only; default 20).")
    p.add_argument("--page-pause-seconds", type=float, default=1.0,
                   help="Pause between backend fetches in live mode "
                        "(default 1.0; set 0 to disable).")
    p.add_argument("--max-retries", type=int, default=_DEFAULT_MAX_RETRIES,
                   help="Per-request retry budget on HTTP 429/5xx and "
                        f"transient URL errors (default {_DEFAULT_MAX_RETRIES}).")
    p.add_argument("--retry-base-seconds", type=float,
                   default=_DEFAULT_RETRY_BASE_SECONDS,
                   help="Base wait for the exponential backoff "
                        f"(default {_DEFAULT_RETRY_BASE_SECONDS}; wait before "
                        "attempt N is base * 2^(N-1)).")

    p.add_argument("--enable-crossref", action="store_true",
                   help="Add Crossref (public, no key) to the backend slate.")
    p.add_argument("--enable-ads", action="store_true",
                   help="Add NASA ADS (requires ADS_API_TOKEN / "
                        "NASA_ADS_TOKEN / ADS_TOKEN env var) to the slate.")
    p.add_argument("--no-arxiv", action="store_true",
                   help="Drop arXiv from the backend slate.")
    p.add_argument("--no-openalex", action="store_true",
                   help="Drop OpenAlex from the backend slate.")

    p.add_argument("--extra-query", action="append", default=[],
                   help="Add an extra query string. May be repeated.")
    p.add_argument("--queries-only", action="store_true",
                   help="Print the resolved query slate as JSON and exit 0.")
    p.add_argument("--corpus-manifest", type=str, default=None,
                   help=("Path to the curated v2 corpus manifest "
                         "(default: references/corpus_manifest_v2.json if "
                         "present in the bundle; pass an explicit path to "
                         "override, or a non-existent path to disable the "
                         "novelty join). When the manifest resolves, every "
                         "emitted candidate is annotated with "
                         "corpus_status=already_curated|new_candidate and "
                         "the JSON summary reports the count."))
    p.add_argument("--no-corpus-manifest", action="store_true",
                   help=("Disable the novelty join even if the default "
                         "manifest is present. Candidates are then marked "
                         "corpus_status=unjoined."))
    p.add_argument("--version", action="version",
                   version=f"discover_heliophysics_literature {__version__}")
    return p


def _resolve_backends(args: argparse.Namespace) -> List[str]:
    out: List[str] = []
    if not args.no_arxiv:
        out.append("arxiv")
    if not args.no_openalex:
        out.append("openalex")
    if args.enable_crossref:
        out.append("crossref")
    if args.enable_ads:
        out.append("ads")
    if not out:
        raise SystemExit(
            "discover_heliophysics_literature: no backends selected after "
            "applying --no-* flags."
        )
    return out


def _resolve_queries(args: argparse.Namespace) -> List[Tuple[str, str]]:
    out = list(DEFAULT_QUERIES)
    for q in args.extra_query:
        q = q.strip()
        if q:
            out.append((q, "extra"))
    return out


def _open_output(path: str):
    if path == "-":
        return contextlib.nullcontext(sys.stdout)
    return open(path, "w", encoding="utf-8")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_parser().parse_args(argv)

    # argparse default makes --dry-run True, but --live should override it.
    live = bool(args.live)

    backends = _resolve_backends(args)
    queries = _resolve_queries(args)

    if args.queries_only:
        json.dump(
            {
                "queries": [{"q": q, "tag": tag} for q, tag in queries],
                "backends": backends,
                "mode": "live" if live else "dry-run",
            },
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    ads_token = None
    if "ads" in backends:
        ads_token = _resolve_ads_token()
        if live and not ads_token:
            sys.stderr.write(
                "discover_heliophysics_literature: --enable-ads requires "
                "ADS_API_TOKEN / NASA_ADS_TOKEN / ADS_TOKEN in env; refusing "
                "to run live ADS query without a token.\n"
            )
            return 2

    if args.max_retries < 0:
        sys.stderr.write(
            "discover_heliophysics_literature: --max-retries must be >= 0\n"
        )
        return 2
    if args.retry_base_seconds < 0:
        sys.stderr.write(
            "discover_heliophysics_literature: --retry-base-seconds must be >= 0\n"
        )
        return 2

    # Resolve the manifest path for the novelty join. Precedence:
    #   --no-corpus-manifest      -> disabled
    #   --corpus-manifest PATH    -> use PATH (missing file => disabled, no fail)
    #   (neither flag)            -> default to DEFAULT_CORPUS_MANIFEST if it
    #                                exists, else disabled.
    if args.no_corpus_manifest:
        corpus_manifest_path: Optional[Path] = None
    elif args.corpus_manifest is not None:
        corpus_manifest_path = Path(args.corpus_manifest)
    else:
        corpus_manifest_path = (
            DEFAULT_CORPUS_MANIFEST if DEFAULT_CORPUS_MANIFEST.is_file() else None
        )

    deduped, summary = run_discovery(
        queries=queries,
        backends=backends,
        max_results=args.max_results,
        live=live,
        fixture_path=Path(args.fixture),
        timeout=args.timeout,
        page_pause_seconds=args.page_pause_seconds,
        ads_token=ads_token,
        max_retries=args.max_retries,
        retry_base_seconds=args.retry_base_seconds,
        corpus_manifest_path=corpus_manifest_path,
    )

    with _open_output(args.output) as out:
        for rec in deduped:
            out.write(json.dumps(rec, ensure_ascii=False, sort_keys=False))
            out.write("\n")

    sys.stderr.write(json.dumps(summary, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
