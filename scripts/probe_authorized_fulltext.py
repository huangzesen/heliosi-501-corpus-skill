#!/usr/bin/env python3
"""Probe official publisher landing pages for authorized full-text PDFs.

This script complements ``scripts/run_acquisition_batch.py`` by giving the
host -- which is on an institution-authorized network (e.g. a university
IP block) -- a second chance to retrieve PDFs whose normal fetch failed,
*using only the same network/IP authorization the host already holds*.

WHAT THIS SCRIPT DOES

For each row in the queue with ``status == fetch_failed`` (DOI-bearing
only), it:

  1. Resolves the DOI via the public DOI proxy
     (``https://doi.org/<doi>``), letting it redirect to the publisher's
     landing page using ordinary HTTP redirects.
  2. Fetches the landing page (publisher-served HTML) over plain HTTPS
     using the host's current network identity, with a polite User-Agent
     that includes the operator's contact email.
  3. Inspects ONLY the landing-page HTML for canonical PDF pointers:
     a ``<meta name="citation_pdf_url">`` tag, or anchor ``href`` values
     ending in ``.pdf`` that resolve to the same publisher host (or an
     explicitly relative path on it). Third-party hosts are ignored.
  4. In probe (default) mode: records what it would have downloaded.
  5. In ``--download`` mode: issues a single follow-up GET to the
     candidate PDF URL. If the final response is HTTP 200 with a
     ``Content-Type`` starting ``application/pdf``, the bytes are
     written to ``papers/<candidate_id>/paper.pdf`` and the queue row is
     atomically promoted to ``fetched``. Otherwise nothing is written
     and the queue row stays ``fetch_failed`` with a structured
     rejection reason.

WHAT THIS SCRIPT DOES NOT DO

  * It never consults or links to any service designed to bypass
    publisher access control.
  * It does not guess credentials, replay cookies, defeat captchas, or
    rewrite URLs through a proxy that strips access controls.
  * It does not log in. It does not POST. It does not set
    ``Cookie:`` headers other than what an ordinary redirect chain
    produces.
  * It does not echo secrets or environment variables.

The only authorization it relies on is the host's current network
identity (the campus IP block, in the deployed scenario). If a
publisher chooses to serve the institution a PDF over plain HTTPS
because the request originated from a recognized IP, that is the
publisher's policy. If the publisher serves an HTML paywall instead,
this script records "rejected_not_pdf" and moves on.

OUTPUTS (all under the external acquisition store passed via --store)

    store/
        authorized_attempts/<candidate_id>.json    per-row attempt record
        runs/<run_id>-authorized-probe/summary.json batch run summary
        papers/<candidate_id>/paper.pdf            (only on --download
                                                    success from an
                                                    official publisher PDF)
        queue.jsonl                                 atomically rewritten
                                                    ONLY for actually
                                                    fetched rows
        queue.csv                                   best-effort mirror
                                                    rewritten after
                                                    fetched promotions

Safe to interrupt. Safe to re-run -- already-fetched rows are skipped by
status filter, and the script never overwrites an existing paper.pdf.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
import uuid
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse


SCHEMA_VERSION = "heliosi-authorized-probe/1.0"

STATUS_FETCH_FAILED = "fetch_failed"
STATUS_FETCHED = "fetched"
STATUS_PROBE_ONLY = "probe_only"
STATUS_NO_LINK = "no_official_pdf_link"
STATUS_REJECTED_NOT_PDF = "rejected_not_pdf"
STATUS_HTTP_ERROR = "http_error"
# Identifier shape rules out a full-text PDF (e.g. EGU meeting abstracts on
# Copernicus, registered as DOIs but corresponding to conference abstracts
# rather than papers). Recording this as a distinct terminal status keeps the
# probe from re-trying these rows on every run.
STATUS_NON_ARTICLE = "non_article_doi"

DEFAULT_QUEUE_NAME = "queue.jsonl"
DEFAULT_CSV_NAME = "queue.csv"
ATTEMPTS_DIR = "authorized_attempts"
PAPERS_DIR = "papers"
RUNS_DIR = "runs"

DOI_PROXY = "https://doi.org/"

DEFAULT_USER_AGENT_TEMPLATE = (
    "HelioSI-AuthorizedProbe/1.0 (institutional fulltext probe; contact: {email})"
)
USER_AGENT_NO_EMAIL = (
    "HelioSI-AuthorizedProbe/1.0 (institutional fulltext probe; contact: unspecified)"
)

# Cap on bytes we will pull for a landing page or a candidate PDF.
MAX_HTML_BYTES = 4 * 1024 * 1024
MAX_PDF_BYTES = 64 * 1024 * 1024


# ──────────────────────────────────────────────────────────
#  Queue I/O (mirrors run_acquisition_batch.py contract)
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
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def write_csv_mirror(rows: list[dict], path: Path) -> None:
    """Best-effort CSV mirror; never fails the probe on CSV errors."""
    if not rows:
        return
    fields = list(rows[0].keys())
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        os.replace(tmp, path)
    except OSError:
        if tmp.exists():
            tmp.unlink()


# ──────────────────────────────────────────────────────────
#  Row selection
# ──────────────────────────────────────────────────────────

# Terminal *failure* outcomes from a prior authorized probe. These mean the
# publisher landing page resolved but did not yield a usable official PDF
# under the host's current authorization; reprobing is wasted unless the
# user explicitly opts in (e.g. because the network identity has changed).
#
# Note: ``probe_only`` is NOT in this set. A probe_only record means dry-run
# discovery succeeded (a candidate PDF URL was found); the normal workflow is
# to re-run with --download afterward, and that second run must still pick
# the row up.
TERMINAL_FAILURE_RESULTS: frozenset[str] = frozenset({
    STATUS_HTTP_ERROR,
    STATUS_NO_LINK,
    STATUS_REJECTED_NOT_PDF,
    STATUS_NON_ARTICLE,
})


def _has_terminal_authorized_failure(store: Path, candidate_id: str) -> bool:
    """True iff a prior authorized-probe attempt ended in a terminal failure.

    Looking at ``store/authorized_attempts/<candidate_id>.json``: if the file
    exists and ``last_result`` is one of the terminal failure outcomes
    (``http_error``, ``no_official_pdf_link``, ``rejected_not_pdf``), the
    candidate has already been probed under the host's current authorization
    and reprobing won't change the outcome unless something external (network
    identity, paywall rules) has changed. Callers can opt back in via
    ``retry_previous_attempts``.

    Successful or in-progress outcomes (``fetched``, ``probe_only``) are
    NOT terminal failures and do not block reselection here -- ``fetched``
    rows are already filtered out by queue status, and ``probe_only`` rows
    are expected to be re-run under ``--download``.
    """
    path = store / ATTEMPTS_DIR / f"{candidate_id}.json"
    if not path.exists():
        return False
    try:
        record = json.loads(path.read_text())
    except (OSError, ValueError):
        # Unreadable or malformed record: don't block reselection.
        return False
    return record.get("last_result") in TERMINAL_FAILURE_RESULTS


def select_failed(
    rows: list[dict],
    limit: int,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    store: Optional[Path] = None,
    retry_previous_attempts: bool = False,
) -> list[dict]:
    """Return up to ``limit`` DOI-bearing rows in ``fetch_failed`` status.

    When ``store`` is provided and ``retry_previous_attempts`` is false,
    candidates that already have a prior authorized-probe attempt with a
    terminal *failure* result on disk are skipped — repeated runs of the
    probe should not keep reselecting rows that already failed under the
    same network authorization. Prior ``probe_only`` records are not
    skipped: the canonical workflow runs a dry-run probe first and then
    re-runs with ``--download`` against the same rows.
    """
    out = []
    for row in rows:
        if row.get("status") != STATUS_FETCH_FAILED:
            continue
        if row.get("identifier_kind") != "doi":
            # arXiv / bibcode-only rows are not relevant to a
            # publisher-landing-page probe.
            continue
        if not row.get("preferred_identifier"):
            continue
        if year_min is not None or year_max is not None:
            year = row.get("year")
            if year is None:
                continue
            if year_min is not None and year < year_min:
                continue
            if year_max is not None and year > year_max:
                continue
        if (
            store is not None
            and not retry_previous_attempts
            and _has_terminal_authorized_failure(store, row.get("candidate_id", ""))
        ):
            continue
        out.append(row)
        if len(out) >= limit:
            break
    return out


# ──────────────────────────────────────────────────────────
#  HTML link extraction
# ──────────────────────────────────────────────────────────

class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.citation_pdf_url: Optional[str] = None
        self.anchor_hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_d = {k.lower(): v for k, v in attrs if v is not None}
        if tag.lower() == "meta":
            name = (attrs_d.get("name") or "").lower()
            if name == "citation_pdf_url" and not self.citation_pdf_url:
                self.citation_pdf_url = attrs_d.get("content")
        elif tag.lower() == "a":
            href = attrs_d.get("href")
            if href:
                self.anchor_hrefs.append(href)


def _same_host(landing_url: str, candidate_url: str) -> bool:
    """True iff candidate_url stays on the landing host or its subdomains.

    We intentionally avoid public-suffix guessing.  ``www.publisher.tld``
    and ``publisher.tld`` are treated as equivalent, and subdomains of
    that normalized host are accepted.  Sibling domains are rejected. This
    is conservative: it may miss some publisher CDN URLs, but it avoids
    over-accepting broad suffixes such as ``co.uk``.
    """
    lh = (urlparse(landing_url).hostname or "").lower().strip(".")
    ch = (urlparse(candidate_url).hostname or "").lower().strip(".")
    if not lh or not ch:
        return False
    if lh.startswith("www."):
        lh = lh[4:]
    if ch.startswith("www."):
        ch = ch[4:]
    return ch == lh or ch.endswith("." + lh)


def extract_pdf_link(html_bytes: bytes, *, landing_url: str) -> Optional[str]:
    """Return the absolute URL of a same-host PDF found on the landing page.

    Priority:
        1. <meta name="citation_pdf_url" content="..."> (if same host)
        2. The first anchor href ending in .pdf that resolves to the
           same publisher host.

    Returns None if nothing acceptable is found.
    """
    try:
        text = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        return None
    parser = _LinkCollector()
    try:
        parser.feed(text)
    except Exception:
        # Tolerate malformed HTML -- fall back to whatever we collected.
        pass

    if parser.citation_pdf_url:
        abs_url = urljoin(landing_url, parser.citation_pdf_url.strip())
        if _same_host(landing_url, abs_url):
            return abs_url

    for href in parser.anchor_hrefs:
        href = href.strip()
        if not href:
            continue
        # Strip URL fragment for the .pdf check.
        target = href.split("#", 1)[0]
        if not target.lower().endswith(".pdf"):
            continue
        abs_url = urljoin(landing_url, target)
        if _same_host(landing_url, abs_url):
            return abs_url
    return None


# ──────────────────────────────────────────────────────────
#  HTTP layer (overridable by tests)
# ──────────────────────────────────────────────────────────

class HttpResponse:
    __slots__ = ("status", "headers", "body", "final_url")

    def __init__(self, status: int, headers: dict, body: bytes, final_url: str) -> None:
        self.status = status
        self.headers = {k.lower(): v for k, v in headers.items()}
        self.body = body
        self.final_url = final_url


def _http_get(
    url: str,
    *,
    timeout: float,
    user_agent: str,
    accept: Optional[str] = None,
    max_bytes: Optional[int] = None,
) -> HttpResponse:
    """Plain-vanilla HTTP GET. Follows redirects via urllib's default opener.

    Tests monkeypatch the module-level ``_http_get`` symbol to avoid the
    network entirely.
    """
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", user_agent)
    if accept:
        req.add_header("Accept", accept)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            headers = {k: v for k, v in resp.headers.items()}
            cap = max_bytes if max_bytes is not None else MAX_HTML_BYTES
            body = resp.read(cap + 1)
            if len(body) > cap:
                body = body[:cap]
            final_url = resp.geturl()
            return HttpResponse(resp.status, headers, body, final_url)
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read() or b""
        except Exception:
            body = b""
        headers = {k: v for k, v in (exc.headers.items() if exc.headers else [])}
        return HttpResponse(exc.code, headers, body, url)


# ──────────────────────────────────────────────────────────
#  Source-specific routing (legal/authorized only)
# ──────────────────────────────────────────────────────────
#
# These helpers are narrow, per-registrant adaptations that
#   (a) clean malformed DOI strings observed in the queue, or
#   (b) substitute the canonical publisher landing URL for a DOI proxy
#       that demonstrably refuses the probe's User-Agent, or
#   (c) classify a DOI shape as not-a-paper before any network I/O.
#
# All three operate purely on metadata. They do not add new authentication,
# scrape login flows, or follow third-party redirects. The same-publisher-host
# rule downstream in ``extract_pdf_link`` / ``_same_host`` still gates which
# PDFs are actually saved.


def _normalize_probe_doi(doi: str) -> str:
    """Strip queue-side artefacts that make a DOI non-resolvable.

    Observed in the live queue (see analysis_*.json): ~17 A&A rows carry a
    parasitic ``/pdf`` suffix glued onto the DOI by a discovery-time
    URL-to-DOI extractor (e.g. ``10.1051/0004-6361/202039407/pdf``). The
    canonical DOI is the prefix without ``/pdf``; doi.org returns 404 for the
    suffixed form. This is pure normalisation -- the canonical DOI is
    unchanged by the strip.
    """
    if not doi:
        return doi
    s = doi.strip()
    while s.lower().endswith("/pdf"):
        s = s[: -len("/pdf")]
    return s


# Publisher-direct landing URLs. ONLY include registrants where:
#   1. The DOI proxy (doi.org) reliably refuses the probe's User-Agent
#      (HTTP 403 in the run we measured), so the probe never reaches the
#      landing page at all; AND
#   2. The publisher-direct URL is the documented canonical landing URL
#      that the DOI proxy would itself redirect to under a browser UA.
#
# This is not credential evasion: the URL is what the publisher publishes
# as the article's home, and the same authorization rules (institutional IP,
# OA flag) apply to the request. The same-host PDF rule downstream is
# unchanged, so widening the scope is impossible.
#
# Source registrants and their canonical landing pattern, from Crossref
# member metadata (verifiable at api.crossref.org/works/<doi>.URL):
#
#   10.1029 (AGU)  -> https://agupubs.onlinelibrary.wiley.com/doi/<doi>
#   10.1002 (Wiley)-> https://onlinelibrary.wiley.com/doi/<doi>
#
# We do NOT include 10.1016 (Elsevier) because the linkinghub redirect does
# succeed (HTTP 200 in the run we measured); the failure there is the absence
# of a PDF link in the rendered HTML, which is an extraction problem not a
# routing problem (and the right fix is a Crossref ``link[].URL``
# text-mining tier, not landing-URL substitution).

_PUBLISHER_LANDING_OVERRIDES: dict[str, str] = {
    "10.1029": "https://agupubs.onlinelibrary.wiley.com/doi/{doi}",
    "10.1002": "https://onlinelibrary.wiley.com/doi/{doi}",
}


# Copernicus discussion-paper / preprint DOIs follow a fully deterministic
# URL scheme that we can construct without any landing-page negotiation:
#
#   10.5194/<journal>d-<volume>-<page>-<year>
#     -> https://<journal>.copernicus.org/preprints/<volume>/<page>/<year>/<doi-suffix>.html
#
# Example: 10.5194/acpd-11-14003-2011
#       -> https://acp.copernicus.org/preprints/11/14003/2011/acpd-11-14003-2011.html
#
# The constructed landing page is the official article page. Some historical
# pages also expose PDF metadata, but live checks in 2026 showed at least one
# page had shrunk to a tiny HTML shell without ``citation_pdf_url`` while the
# same deterministic same-host PDF URL remained valid. We therefore keep the
# official landing URL for host/authorization checks and also construct the
# matching official PDF URL for this narrow DOI shape.
#
# Restricted intentionally: this helper only handles the
# ``<journal>d-<volume>-<page>-<year>`` shape (the historical preprint
# server). It does NOT attempt to construct URLs for:
#   * ``egusphere-egu*`` meeting abstracts (handled by ``_is_non_article_doi``);
#   * ``egusphere-YYYY-NN`` modern preprints (different URL scheme);
#   * ``acp-YYYY-NN`` review-thread anchors (different URL scheme);
#   * Final published articles ``<journal>-<vol>-<page>-<year>`` (the standard
#     DOI proxy + Unpaywall path already works for these -- 66/66 fetched in
#     the live queue snapshot).
#
# Leaving unsupported shapes to the default doi.org-proxy path keeps the
# helper deterministic and avoids inventing URLs for shapes we have not
# verified end-to-end.
_COPERNICUS_PREPRINT_PATTERN = re.compile(
    r"^10\.5194/(?P<journal>[a-z]+)d-(?P<volume>\d+)-(?P<page>[A-Za-z0-9]+)-(?P<year>\d{4})$",
    re.IGNORECASE,
)


def _copernicus_preprint_urls(doi: str) -> Optional[tuple[str, str]]:
    """Construct official Copernicus landing and PDF URLs for matching DOIs.

    Returns ``None`` for any DOI that does not match the
    ``<journal>d-<volume>-<page>-<year>`` shape so the caller falls back to
    the default DOI-proxy path.  Both returned URLs live on the same
    Copernicus host: the HTML landing URL is used to establish the publisher
    host, and the PDF URL is still validated by the normal PDF fetch, content
    type, PDF magic, and final-URL same-host checks before any file is saved.
    """
    if not doi:
        return None
    s = doi.strip()
    m = _COPERNICUS_PREPRINT_PATTERN.match(s)
    if not m:
        return None
    journal = m.group("journal").lower()
    volume = m.group("volume")
    page = m.group("page")
    year = m.group("year")
    # The DOI suffix (everything after the ``10.5194/`` prefix) is also the
    # filename stem on the Copernicus host. Preserve the original case of the
    # suffix to match the on-disk filename exactly.
    suffix = s.split("/", 1)[1]
    base = f"https://{journal}.copernicus.org/preprints/{volume}/{page}/{year}/{suffix}"
    return f"{base}.html", f"{base}.pdf"


def _copernicus_preprint_landing(doi: str) -> Optional[str]:
    """Construct the Copernicus preprint landing URL for matching DOIs."""
    urls = _copernicus_preprint_urls(doi)
    return urls[0] if urls else None


def _copernicus_preprint_pdf(doi: str) -> Optional[str]:
    """Construct the Copernicus preprint PDF URL for matching DOIs."""
    urls = _copernicus_preprint_urls(doi)
    return urls[1] if urls else None


def _publisher_landing_override(doi: str) -> Optional[str]:
    """Return a publisher-direct landing URL when one is preferable to doi.org.

    Returns ``None`` for any registrant we do not have an explicit override
    for, leaving the standard doi.org-proxy path intact.
    """
    if not doi:
        return None
    # Shape-specific overrides take precedence over prefix-only ones, because
    # a single registrant (10.5194) covers both meeting abstracts, modern
    # preprints, and journal articles -- only the preprint shape gets a
    # constructed URL.
    copernicus = _copernicus_preprint_landing(doi)
    if copernicus:
        return copernicus
    prefix = doi.split("/", 1)[0].lower()
    template = _PUBLISHER_LANDING_OVERRIDES.get(prefix)
    if not template:
        return None
    # The Wiley landing URL expects the DOI in its original case after the
    # ``/doi/`` segment. Use the supplied DOI as-is; doi.org canonicalisation
    # is case-insensitive but Wiley accepts either form.
    return template.format(doi=doi)


# DOI shapes that we know correspond to non-paper artefacts and so cannot be
# acquired as a publisher PDF. Today this is exclusively Copernicus
# ``egusphere-egu*`` meeting-abstract DOIs, which are short conference
# abstracts hosted on meetingorganizer.copernicus.org (no PDF, by design).
_EGU_ABSTRACT_PATTERN = re.compile(r"^10\.5194/egusphere-egu\d{2,4}-", re.IGNORECASE)


def _is_non_article_doi(doi: str) -> bool:
    """True iff the DOI shape implies a non-paper (e.g. EGU meeting abstract).

    Recording these as a distinct terminal status (``non_article_doi``) lets
    repeated runs of the probe skip them deterministically and keeps the
    failure-classification report clean.
    """
    if not doi:
        return False
    return bool(_EGU_ABSTRACT_PATTERN.match(doi.strip()))


# ──────────────────────────────────────────────────────────
#  Per-row probe
# ──────────────────────────────────────────────────────────

def _probe_one(
    row: dict,
    *,
    store: Path,
    user_agent: str,
    http_timeout: float,
    download: bool,
) -> dict:
    """Probe a single fetch_failed row. Returns an attempt record dict."""
    cid = row["candidate_id"]
    raw_doi = row["preferred_identifier"]
    # Step 0: source-specific normalisation -- strip parasitic ``/pdf``
    # suffixes observed on some A&A rows so the canonical DOI resolves.
    doi = _normalize_probe_doi(raw_doi)
    # If the DOI shape implies a non-paper artefact (EGU meeting abstracts),
    # short-circuit before any network I/O so re-runs deterministically skip
    # this row via the terminal-failure guard.
    if _is_non_article_doi(doi):
        return {
            "schema_version": SCHEMA_VERSION,
            "candidate_id": cid,
            "preferred_identifier": raw_doi,
            "doi_normalized": doi if doi != raw_doi else None,
            "identifier_kind": row.get("identifier_kind"),
            "title": row.get("title"),
            "year": row.get("year"),
            "doi_url": None,
            "landing_url": None,
            "pdf_url": None,
            "http_status": None,
            "content_type": None,
            "source": "non_article_doi_shape",
            "last_result": STATUS_NON_ARTICLE,
            "attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    # Prefer publisher-direct landing URLs for registrants where doi.org
    # refuses our User-Agent (Wiley/AGU returned 403 in the live run). The
    # override URL is the canonical landing page that the proxy would itself
    # redirect to under a browser UA; downstream same-host PDF checks are
    # unchanged.
    copernicus_pdf = _copernicus_preprint_pdf(doi)
    override = _publisher_landing_override(doi)
    if override:
        landing_entry_url = override
        landing_route = "publisher_direct"
    else:
        landing_entry_url = DOI_PROXY + doi.lstrip("/")
        landing_route = "doi_proxy"

    attempt: dict = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": cid,
        "preferred_identifier": raw_doi,
        "doi_normalized": doi if doi != raw_doi else None,
        "identifier_kind": row.get("identifier_kind"),
        "title": row.get("title"),
        "year": row.get("year"),
        "doi_url": landing_entry_url,
        "landing_route": landing_route,
        "landing_url": None,
        "pdf_url": None,
        "pdf_url_source": None,
        "http_status": None,
        "content_type": None,
        "source": None,
        "last_result": None,
        "attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Step 1: resolve DOI -> landing page.
    try:
        landing = _http_get(
            landing_entry_url,
            timeout=http_timeout,
            user_agent=user_agent,
            accept="text/html,application/xhtml+xml",
            max_bytes=MAX_HTML_BYTES,
        )
    except Exception as exc:
        attempt["last_result"] = STATUS_HTTP_ERROR
        attempt["error"] = f"{type(exc).__name__}: {exc}"
        return attempt

    attempt["landing_url"] = landing.final_url
    attempt["http_status"] = landing.status
    attempt["content_type"] = landing.headers.get("content-type")
    if landing.status >= 400:
        attempt["last_result"] = STATUS_HTTP_ERROR
        return attempt

    # Step 2: extract candidate PDF link from same publisher host.
    pdf_url = extract_pdf_link(landing.body, landing_url=landing.final_url)
    pdf_url_source: Optional[str] = "landing_page_link" if pdf_url else None
    if not pdf_url and copernicus_pdf:
        # Historical Copernicus discussion-preprint pages have deterministic
        # same-host PDF URLs. Live pages may omit the citation_pdf_url meta tag,
        # so fall back to the deterministic URL for this narrow DOI shape while
        # preserving all downstream PDF/content/final-host validation.
        pdf_url = copernicus_pdf
        pdf_url_source = "copernicus_preprint_deterministic"
    if not pdf_url:
        attempt["last_result"] = STATUS_NO_LINK
        return attempt
    attempt["pdf_url"] = pdf_url
    attempt["pdf_url_source"] = pdf_url_source
    attempt["source"] = "publisher_institutional"

    if not download:
        attempt["last_result"] = STATUS_PROBE_ONLY
        return attempt

    # Step 3: fetch the candidate PDF.
    try:
        pdf_resp = _http_get(
            pdf_url,
            timeout=http_timeout,
            user_agent=user_agent,
            accept="application/pdf",
            max_bytes=MAX_PDF_BYTES,
        )
    except Exception as exc:
        attempt["last_result"] = STATUS_HTTP_ERROR
        attempt["error"] = f"{type(exc).__name__}: {exc}"
        return attempt

    attempt["http_status"] = pdf_resp.status
    attempt["content_type"] = pdf_resp.headers.get("content-type")
    ctype = (pdf_resp.headers.get("content-type") or "").lower()
    if pdf_resp.status != 200 or not ctype.startswith("application/pdf"):
        attempt["last_result"] = STATUS_REJECTED_NOT_PDF
        return attempt
    if not pdf_resp.body.startswith(b"%PDF-"):
        attempt["last_result"] = STATUS_REJECTED_NOT_PDF
        attempt["error"] = "pdf_body_missing_magic"
        return attempt

    # Step 4: same-host check on the FINAL pdf URL (redirects may have
    # taken us off the publisher host).
    if not _same_host(landing.final_url, pdf_resp.final_url):
        attempt["last_result"] = STATUS_REJECTED_NOT_PDF
        attempt["error"] = "pdf_final_url_off_publisher_host"
        return attempt

    # Step 5: write PDF (never overwrite an existing one).
    out_dir = store / PAPERS_DIR / cid
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "paper.pdf"
    if not pdf_path.exists():
        tmp = pdf_path.with_suffix(".pdf.tmp")
        tmp.write_bytes(pdf_resp.body)
        os.replace(tmp, pdf_path)
    attempt["pdf_path"] = str(pdf_path)
    attempt["pdf_bytes"] = len(pdf_resp.body)
    attempt["source"] = "official_pdf"
    attempt["last_result"] = STATUS_FETCHED
    return attempt


# ──────────────────────────────────────────────────────────
#  Batch driver
# ──────────────────────────────────────────────────────────

def _write_attempt(store: Path, candidate_id: str, payload: dict) -> None:
    p = store / ATTEMPTS_DIR / f"{candidate_id}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def _update_row_status(rows: list[dict], cid: str, status: str, note: str) -> None:
    for row in rows:
        if row.get("candidate_id") == cid:
            row["status"] = status
            existing = row.get("notes") or ""
            row["notes"] = f"{existing}; {note}" if existing else note
            return


def _user_agent(email: Optional[str]) -> str:
    if email:
        return DEFAULT_USER_AGENT_TEMPLATE.format(email=email)
    return USER_AGENT_NO_EMAIL


def run_probe(
    *,
    store: Path,
    limit: int,
    email: Optional[str],
    year_min: Optional[int],
    year_max: Optional[int],
    download: bool,
    per_request_pause: float,
    http_timeout: float,
    queue_name: str = DEFAULT_QUEUE_NAME,
    csv_name: str = DEFAULT_CSV_NAME,
    retry_previous_attempts: bool = False,
) -> dict:
    queue_path = store / queue_name
    csv_path = store / csv_name
    if not queue_path.exists():
        raise FileNotFoundError(f"queue not found at {queue_path}")

    rows = read_queue(queue_path)
    picked = select_failed(
        rows,
        limit=limit,
        year_min=year_min,
        year_max=year_max,
        store=store,
        retry_previous_attempts=retry_previous_attempts,
    )

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    run_dir = store / RUNS_DIR / f"{run_id}-authorized-probe"
    run_dir.mkdir(parents=True, exist_ok=True)

    user_agent = _user_agent(email)
    by_status: dict[str, int] = {}
    attempts_recorded: list[dict] = []

    for idx, row in enumerate(picked):
        attempt = _probe_one(
            row,
            store=store,
            user_agent=user_agent,
            http_timeout=http_timeout,
            download=download,
        )
        attempt["run_id"] = run_id
        attempt["options"] = {
            "download": download,
            "http_timeout": http_timeout,
            "per_request_pause": per_request_pause,
        }
        _write_attempt(store, row["candidate_id"], attempt)

        if download and attempt.get("last_result") == STATUS_FETCHED:
            _update_row_status(
                rows,
                row["candidate_id"],
                STATUS_FETCHED,
                note=f"authorized-probe:{run_id}",
            )
            write_queue_atomic(rows, queue_path)
            write_csv_mirror(rows, csv_path)

        result = attempt.get("last_result") or "unknown"
        by_status[result] = by_status.get(result, 0) + 1
        attempts_recorded.append(
            {
                "candidate_id": row["candidate_id"],
                "preferred_identifier": row["preferred_identifier"],
                "last_result": result,
                "pdf_url": attempt.get("pdf_url"),
                "landing_url": attempt.get("landing_url"),
            }
        )

        if per_request_pause and idx + 1 < len(picked):
            time.sleep(per_request_pause)

    summary = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "selected": len(picked),
        "by_status": by_status,
        "attempts": attempts_recorded,
        "options": {
            "limit": limit,
            "download": download,
            "year_min": year_min,
            "year_max": year_max,
            "http_timeout": http_timeout,
            "per_request_pause": per_request_pause,
            "email_provided": bool(email),
            "retry_previous_attempts": retry_previous_attempts,
        },
    }
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    return summary


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument(
        "--store",
        type=Path,
        required=True,
        help="external acquisition store directory (contains queue.jsonl)",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=5,
        help="max fetch_failed rows to probe this run (default: 5)",
    )
    p.add_argument(
        "--email",
        default=os.environ.get("LINGTAI_RESEARCH_EMAIL"),
        help="operator contact email embedded in User-Agent (recommended)",
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
        "--download",
        action="store_true",
        help=(
            "actually download official publisher PDFs (default is dry-run "
            "probe only -- discovers candidate PDF URLs without fetching them)"
        ),
    )
    p.add_argument(
        "--per-request-pause",
        type=float,
        default=2.0,
        help="seconds to sleep between probed rows (default: 2.0)",
    )
    p.add_argument(
        "--http-timeout",
        type=float,
        default=30.0,
        help="per-request HTTP timeout in seconds (default: 30)",
    )
    p.add_argument(
        "--queue-name",
        default=DEFAULT_QUEUE_NAME,
        help=f"queue JSONL filename inside --store (default: {DEFAULT_QUEUE_NAME})",
    )
    p.add_argument(
        "--retry-previous-attempts",
        action="store_true",
        help=(
            "reselect candidates whose prior authorized attempt ended in a "
            "terminal failure (http_error / no_official_pdf_link / "
            "rejected_not_pdf). Default: skip them, so repeated runs don't "
            "keep reprobing rows that already failed under the same "
            "authorization. Prior ``probe_only`` records are always eligible "
            "for reselection (the standard workflow runs a dry-run probe "
            "first, then re-runs with --download)."
        ),
    )
    args = p.parse_args(argv)

    try:
        summary = run_probe(
            store=args.store,
            limit=args.limit,
            email=args.email,
            year_min=args.year_min,
            year_max=args.year_max,
            download=args.download,
            per_request_pause=args.per_request_pause,
            http_timeout=args.http_timeout,
            queue_name=args.queue_name,
            retry_previous_attempts=args.retry_previous_attempts,
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
