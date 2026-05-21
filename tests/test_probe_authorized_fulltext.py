"""Tests for scripts/probe_authorized_fulltext.py.

No network. HTTP calls are stubbed via a routing table monkeypatched onto
the module's ``_http_get`` symbol. The script is exercised against
temp-dir stores so the real external acquisition store is never touched
(the parent process may be running another batch concurrently).

These tests cover:

  * selection (only ``fetch_failed`` rows, with optional filters)
  * landing-page link extraction (``citation_pdf_url`` and same-domain
    anchor hrefs ending in ``.pdf``)
  * dry-run is the default and mutates neither queue nor files
  * a successful PDF download writes to ``papers/<id>/paper.pdf`` and
    atomically promotes the queue row to ``fetched``
  * non-PDF responses and PDFs served from third-party domains are
    rejected (no file written, queue not promoted)
  * the script source itself contains no forbidden domains/terms
    (sci-hub / libgen / shadow-library names)
"""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "probe_authorized_fulltext.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("probe_authorized_fulltext", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


paf = _load_module()


def _row(cid, identifier, status="fetch_failed", year=2020, kind="doi"):
    return {
        "candidate_id": cid,
        "cell": "P-test",
        "source": "test",
        "title": f"title for {cid}",
        "year": year,
        "doi": identifier if kind == "doi" else None,
        "arxiv_id": None,
        "bibcode": None,
        "corpus_status": "new_candidate",
        "preferred_identifier": identifier,
        "identifier_kind": kind,
        "priority": 10,
        "status": status,
        "notes": "",
        "queued_at_utc": "2026-05-20T12:00:00Z",
    }


def _seed_queue(store: Path, rows: list[dict]) -> None:
    store.mkdir(parents=True, exist_ok=True)
    with (store / "queue.jsonl").open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")


class FakeResponse:
    """Minimal response object compatible with _http_get's contract."""

    def __init__(self, status, headers, body, final_url):
        self.status = status
        self.headers = {k.lower(): v for k, v in headers.items()}
        self.body = body
        self.final_url = final_url


def make_router(table):
    """Build a fake _http_get from a {url: FakeResponse} dict.

    A missing URL produces a 404 with no body, so tests can assert that
    unexpected fetches are flagged rather than silently succeeding.
    """

    def _fake(url, *, timeout, user_agent, accept=None, max_bytes=None):
        # Resolve a redirect chain: a FakeResponse with status in {301,302,303,307,308}
        # and a ``location`` header is followed up to 5 hops.
        seen = []
        current = url
        for _ in range(6):
            seen.append(current)
            resp = table.get(current)
            if resp is None:
                return FakeResponse(404, {"content-type": "text/plain"}, b"", current)
            if resp.status in (301, 302, 303, 307, 308) and resp.headers.get("location"):
                current = resp.headers["location"]
                continue
            # Rebind final_url to the last URL actually fetched.
            return FakeResponse(resp.status, resp.headers, resp.body, current)
        return FakeResponse(599, {"content-type": "text/plain"}, b"", current)

    return _fake


class TestSelectFailed(unittest.TestCase):
    def test_select_only_fetch_failed_with_identifier(self):
        rows = [
            _row("a", "10.1/a"),
            _row("b", "10.1/b", status="fetched"),
            _row("c", "10.1/c", status="pending"),
            {**_row("d", None), "preferred_identifier": None},
            _row("e", "10.1/e"),
        ]
        picked = paf.select_failed(rows, limit=10)
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "e"])

    def test_limit_caps_selection(self):
        rows = [_row(f"r{i}", f"10.1/{i}") for i in range(5)]
        picked = paf.select_failed(rows, limit=2)
        self.assertEqual(len(picked), 2)

    def test_year_filters_inclusive(self):
        rows = [
            _row("old", "10.1/old", year=1960),
            _row("mid", "10.1/mid", year=1990),
            _row("new", "10.1/new", year=2020),
            _row("noy", "10.1/n", year=None),
        ]
        picked = paf.select_failed(rows, limit=10, year_min=1980, year_max=2000)
        self.assertEqual([r["candidate_id"] for r in picked], ["mid"])

    def test_arxiv_only_rows_are_excluded(self):
        # The authorized probe is DOI-only -- arxiv identifiers go through
        # the standard fetch tier and should not be retried here.
        rows = [
            _row("a", "10.1/a"),
            {**_row("b", "arxiv:2301.00001", kind="arxiv"), "doi": None},
        ]
        picked = paf.select_failed(rows, limit=10)
        self.assertEqual([r["candidate_id"] for r in picked], ["a"])


class TestExtractPdfLink(unittest.TestCase):
    def test_citation_pdf_url_meta_wins(self):
        html = b"""
        <html><head>
            <meta name="citation_pdf_url" content="https://publisher.example.org/article/123.pdf" />
        </head><body><a href="/other.pdf">other</a></body></html>
        """
        link = paf.extract_pdf_link(html, landing_url="https://publisher.example.org/article/123")
        self.assertEqual(link, "https://publisher.example.org/article/123.pdf")

    def test_same_domain_anchor_pdf(self):
        html = b'<html><body><a href="/full/123.pdf">PDF</a></body></html>'
        link = paf.extract_pdf_link(html, landing_url="https://publisher.example.org/article/123")
        self.assertEqual(link, "https://publisher.example.org/full/123.pdf")

    def test_www_alias_is_accepted(self):
        html = b'<html><body><a href="https://publisher.example.org/full/123.pdf">PDF</a></body></html>'
        link = paf.extract_pdf_link(html, landing_url="https://www.publisher.example.org/article/123")
        self.assertEqual(link, "https://publisher.example.org/full/123.pdf")

    def test_sibling_domain_is_rejected(self):
        html = b'<html><body><a href="https://files.example.org/full/123.pdf">PDF</a></body></html>'
        link = paf.extract_pdf_link(html, landing_url="https://publisher.example.org/article/123")
        self.assertIsNone(link)

    def test_third_party_pdf_ignored(self):
        html = b'<html><body><a href="https://sci-hub.example/foo.pdf">PDF</a></body></html>'
        link = paf.extract_pdf_link(html, landing_url="https://publisher.example.org/article/123")
        self.assertIsNone(link)

    def test_no_pdf_link_returns_none(self):
        html = b"<html><body>Subscribe for full text</body></html>"
        link = paf.extract_pdf_link(html, landing_url="https://publisher.example.org/article/123")
        self.assertIsNone(link)


class TestDryRunDefault(unittest.TestCase):
    def test_default_is_dry_run_no_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            _seed_queue(store, [_row("a", "10.1/a")])

            table = {
                "https://doi.org/10.1/a": FakeResponse(
                    302, {"location": "https://publisher.example.org/article/a", "content-type": "text/html"}, b"", "https://doi.org/10.1/a",
                ),
                "https://publisher.example.org/article/a": FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    b'<html><head><meta name="citation_pdf_url" content="https://publisher.example.org/article/a.pdf" /></head></html>',
                    "https://publisher.example.org/article/a",
                ),
                "https://publisher.example.org/article/a.pdf": FakeResponse(
                    200, {"content-type": "application/pdf"}, b"%PDF-1.4 fake bytes",
                    "https://publisher.example.org/article/a.pdf",
                ),
            }

            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store,
                limit=10,
                email="researcher@example.edu",
                year_min=None,
                year_max=None,
                download=False,
                per_request_pause=0.0,
                http_timeout=5.0,
            )

            # Queue row untouched.
            rows = paf.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "fetch_failed")

            # No PDF written under papers/.
            papers = store / "papers"
            self.assertFalse(papers.exists() and any(papers.iterdir()))

            # An attempt record is structured under authorized_attempts/.
            att_path = store / "authorized_attempts" / "a.json"
            self.assertTrue(att_path.exists())
            attempt = json.loads(att_path.read_text())
            self.assertEqual(attempt["last_result"], "probe_only")
            self.assertEqual(attempt["pdf_url"], "https://publisher.example.org/article/a.pdf")
            self.assertEqual(attempt["source"], "publisher_institutional")

            # Per-run summary.
            run_id = summary["run_id"]
            run_dir = store / "runs" / f"{run_id}-authorized-probe"
            self.assertTrue((run_dir / "summary.json").exists())

            # No secrets / forbidden terms in the attempt record.
            blob = json.dumps(attempt).lower()
            self.assertNotIn("token", blob)
            for forbidden in ("sci-hub", "scihub", "libgen", "z-library"):
                self.assertNotIn(forbidden, blob)


class TestDownloadPath(unittest.TestCase):
    def test_download_writes_pdf_and_promotes_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            _seed_queue(store, [_row("a", "10.1/a")])

            pdf_bytes = b"%PDF-1.4 fake bytes\n%%EOF"
            table = {
                "https://doi.org/10.1/a": FakeResponse(
                    302, {"location": "https://publisher.example.org/article/a", "content-type": "text/html"},
                    b"", "https://doi.org/10.1/a",
                ),
                "https://publisher.example.org/article/a": FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    b'<html><head><meta name="citation_pdf_url" content="https://publisher.example.org/article/a.pdf" /></head></html>',
                    "https://publisher.example.org/article/a",
                ),
                "https://publisher.example.org/article/a.pdf": FakeResponse(
                    200, {"content-type": "application/pdf"}, pdf_bytes,
                    "https://publisher.example.org/article/a.pdf",
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store,
                limit=10,
                email="researcher@example.edu",
                year_min=None,
                year_max=None,
                download=True,
                per_request_pause=0.0,
                http_timeout=5.0,
            )

            # PDF written under papers/<candidate_id>/paper.pdf
            pdf_path = store / "papers" / "cand_for_a" / "paper.pdf"
            # We don't know the slug rule yet -- accept any subdir as long as
            # exactly one paper.pdf exists for candidate 'a'.
            written = list((store / "papers").glob("*/paper.pdf"))
            self.assertEqual(len(written), 1, f"expected exactly one PDF, got {written}")
            self.assertEqual(written[0].read_bytes(), pdf_bytes)

            # Queue row promoted to fetched.
            rows = paf.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "fetched")

            # Attempt manifest is structured and has provenance.
            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["last_result"], "fetched")
            self.assertEqual(attempt["http_status"], 200)
            self.assertEqual(attempt["content_type"], "application/pdf")
            self.assertEqual(attempt["source"], "official_pdf")
            self.assertEqual(attempt["landing_url"], "https://publisher.example.org/article/a")
            self.assertEqual(attempt["pdf_url"], "https://publisher.example.org/article/a.pdf")

            # Summary counts the fetch.
            self.assertEqual(summary["by_status"].get("fetched"), 1)


class TestRejection(unittest.TestCase):
    def test_non_pdf_response_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            _seed_queue(store, [_row("a", "10.1/a")])

            # Landing page advertises a "PDF" link that actually returns HTML
            # (paywall page, captcha, login form).
            table = {
                "https://doi.org/10.1/a": FakeResponse(
                    302, {"location": "https://publisher.example.org/article/a", "content-type": "text/html"},
                    b"", "https://doi.org/10.1/a",
                ),
                "https://publisher.example.org/article/a": FakeResponse(
                    200, {"content-type": "text/html"},
                    b'<html><body><a href="/full/a.pdf">PDF</a></body></html>',
                    "https://publisher.example.org/article/a",
                ),
                "https://publisher.example.org/full/a.pdf": FakeResponse(
                    200, {"content-type": "text/html"},
                    b"<html>Sign in to continue</html>",
                    "https://publisher.example.org/full/a.pdf",
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            # No PDF written.
            self.assertEqual(list((store / "papers").glob("*/paper.pdf")), [])
            # Queue row stays fetch_failed.
            rows = paf.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "fetch_failed")
            # Attempt records rejection reason.
            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["last_result"], "rejected_not_pdf")
            self.assertEqual(summary["by_status"].get("rejected_not_pdf"), 1)

    def test_third_party_pdf_link_is_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = tmp / "store"
            _seed_queue(store, [_row("a", "10.1/a")])

            table = {
                "https://doi.org/10.1/a": FakeResponse(
                    302, {"location": "https://publisher.example.org/article/a", "content-type": "text/html"},
                    b"", "https://doi.org/10.1/a",
                ),
                "https://publisher.example.org/article/a": FakeResponse(
                    200, {"content-type": "text/html"},
                    b'<html><body><a href="https://other-host.example/foo.pdf">PDF</a></body></html>',
                    "https://publisher.example.org/article/a",
                ),
                "https://other-host.example/foo.pdf": FakeResponse(
                    200, {"content-type": "application/pdf"}, b"%PDF-1.4 should-not-be-fetched",
                    "https://other-host.example/foo.pdf",
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(list((store / "papers").glob("*/paper.pdf")), [])
            rows = paf.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "fetch_failed")
            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["last_result"], "no_official_pdf_link")


class TestSourceHygiene(unittest.TestCase):
    """The script source itself must not reference forbidden services."""

    FORBIDDEN = ("sci-hub", "scihub", "libgen", "z-library", "zlibrary", "shadow library")

    def test_no_forbidden_terms_in_script(self):
        text = SCRIPT.read_text().lower()
        for term in self.FORBIDDEN:
            self.assertNotIn(term, text, f"forbidden term {term!r} found in script")


if __name__ == "__main__":
    unittest.main()
