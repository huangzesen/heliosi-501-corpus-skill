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


def _write_attempt_file(store: Path, candidate_id: str, last_result: str) -> Path:
    """Drop a minimal prior-attempt record under authorized_attempts/."""
    attempts_dir = store / "authorized_attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)
    path = attempts_dir / f"{candidate_id}.json"
    path.write_text(json.dumps({
        "schema_version": paf.SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "last_result": last_result,
        "attempted_at_utc": "2026-05-19T00:00:00Z",
    }) + "\n")
    return path


class TestSkipPreviousAttempts(unittest.TestCase):
    """Repeat runs must not reselect candidates with prior terminal attempts.

    The parent driver re-invokes this probe repeatedly; without this guard,
    each run reselects the same failing candidates and burns publisher fetches
    on landing pages we already know never yielded an official PDF.
    """

    TERMINAL_FAILURE_RESULTS = (
        paf.STATUS_HTTP_ERROR,
        paf.STATUS_NO_LINK,
        paf.STATUS_REJECTED_NOT_PDF,
    )

    def test_default_skips_rows_with_existing_failure_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [_row("a", "10.1/a"), _row("b", "10.1/b"), _row("c", "10.1/c")]
            # 'a' previously failed (no_official_pdf_link) -> skip;
            # 'b' previously errored (http_error) -> skip;
            # 'c' has never been attempted -> select.
            _write_attempt_file(store, "a", paf.STATUS_NO_LINK)
            _write_attempt_file(store, "b", paf.STATUS_HTTP_ERROR)
            picked = paf.select_failed(rows, limit=10, store=store)
            self.assertEqual([r["candidate_id"] for r in picked], ["c"])

    def test_default_skips_for_each_terminal_failure_result_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = []
            for i, result in enumerate(self.TERMINAL_FAILURE_RESULTS):
                cid = f"x{i}"
                rows.append(_row(cid, f"10.1/{cid}"))
                _write_attempt_file(store, cid, result)
            # Plus one fresh row with no prior attempt.
            rows.append(_row("fresh", "10.1/fresh"))
            picked = paf.select_failed(rows, limit=10, store=store)
            self.assertEqual([r["candidate_id"] for r in picked], ["fresh"])

    def test_default_does_not_skip_probe_only_records(self):
        # ``probe_only`` is not a terminal failure: the standard workflow is to
        # run a dry-run probe first (which records last_result=probe_only and a
        # discovered pdf_url) and then re-run with --download. The second run
        # must still see those rows.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [_row("a", "10.1/a"), _row("b", "10.1/b")]
            _write_attempt_file(store, "a", paf.STATUS_PROBE_ONLY)
            _write_attempt_file(store, "b", paf.STATUS_NO_LINK)
            picked = paf.select_failed(rows, limit=10, store=store)
            self.assertEqual([r["candidate_id"] for r in picked], ["a"])

    def test_retry_flag_reselects_previously_attempted_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [_row("a", "10.1/a"), _row("b", "10.1/b")]
            _write_attempt_file(store, "a", paf.STATUS_HTTP_ERROR)
            _write_attempt_file(store, "b", paf.STATUS_REJECTED_NOT_PDF)
            picked = paf.select_failed(
                rows, limit=10, store=store, retry_previous_attempts=True
            )
            self.assertEqual([r["candidate_id"] for r in picked], ["a", "b"])

    def test_attempt_file_with_null_last_result_is_not_a_completed_attempt(self):
        # Defensive: a partially-written record without a last_result should
        # not block reselection. We only skip when an authorized attempt
        # actually concluded with a terminal status.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [_row("a", "10.1/a")]
            (store / "authorized_attempts").mkdir(parents=True, exist_ok=True)
            (store / "authorized_attempts" / "a.json").write_text(json.dumps({
                "schema_version": paf.SCHEMA_VERSION,
                "candidate_id": "a",
                "last_result": None,
            }) + "\n")
            picked = paf.select_failed(rows, limit=10, store=store)
            self.assertEqual([r["candidate_id"] for r in picked], ["a"])

    def test_no_store_keeps_legacy_behavior(self):
        # Backward compat: existing callers that don't pass store= must still
        # get the old selection semantics.
        rows = [_row("a", "10.1/a"), _row("b", "10.1/b")]
        picked = paf.select_failed(rows, limit=10)
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "b"])

    def test_run_probe_skips_previously_attempted_by_default(self):
        # End-to-end check via run_probe: prior attempt file present, the
        # queue still has fetch_failed status, but the row should NOT be
        # probed again unless retry is requested.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1/a"), _row("b", "10.1/b")])
            _write_attempt_file(store, "a", paf.STATUS_NO_LINK)

            calls: list[str] = []
            base_router = make_router({
                "https://doi.org/10.1/b": FakeResponse(
                    200, {"content-type": "text/html"},
                    b"<html><body>No PDF here</body></html>",
                    "https://doi.org/10.1/b",
                ),
            })

            def recording_fake(url, **kwargs):
                calls.append(url)
                return base_router(url, **kwargs)

            paf._http_get = recording_fake

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            # Only 'b' was selected; 'a' was skipped because of its prior attempt.
            self.assertEqual(summary["selected"], 1)
            self.assertTrue(all("10.1/a" not in u for u in calls),
                            f"unexpected refetch of skipped row: {calls}")
            # 'a' attempt file was NOT overwritten (timestamp from seed remains).
            a_record = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(a_record["attempted_at_utc"], "2026-05-19T00:00:00Z")

    def test_run_probe_probe_only_record_can_proceed_to_download(self):
        # End-to-end: a previous dry-run left a ``probe_only`` record. A
        # follow-up --download run (no --retry flag) must still pick the row
        # up and actually fetch the PDF.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1/a")])
            _write_attempt_file(store, "a", paf.STATUS_PROBE_ONLY)

            pdf_bytes = b"%PDF-1.4 fake bytes\n%%EOF"
            table = {
                "https://doi.org/10.1/a": FakeResponse(
                    302, {"location": "https://publisher.example.org/article/a",
                          "content-type": "text/html"},
                    b"", "https://doi.org/10.1/a",
                ),
                "https://publisher.example.org/article/a": FakeResponse(
                    200, {"content-type": "text/html; charset=utf-8"},
                    b'<html><head><meta name="citation_pdf_url" '
                    b'content="https://publisher.example.org/article/a.pdf" /></head></html>',
                    "https://publisher.example.org/article/a",
                ),
                "https://publisher.example.org/article/a.pdf": FakeResponse(
                    200, {"content-type": "application/pdf"}, pdf_bytes,
                    "https://publisher.example.org/article/a.pdf",
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(summary["selected"], 1)
            self.assertEqual(summary["by_status"].get("fetched"), 1)
            # Queue row promoted; PDF written.
            rows = paf.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "fetched")
            self.assertEqual(list((store / "papers").glob("*/paper.pdf"))[0].read_bytes(),
                             pdf_bytes)
            # Attempt record was updated from probe_only -> fetched.
            a_record = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(a_record["last_result"], "fetched")

    def test_run_probe_retry_flag_reprobes_previously_attempted(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1/a")])
            _write_attempt_file(store, "a", paf.STATUS_NO_LINK)

            table = {
                "https://doi.org/10.1/a": FakeResponse(
                    200, {"content-type": "text/html"},
                    b'<html><head><meta name="citation_pdf_url" '
                    b'content="https://doi.org/10.1/a.pdf" /></head></html>',
                    "https://doi.org/10.1/a",
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
                retry_previous_attempts=True,
            )

            self.assertEqual(summary["selected"], 1)
            # Prior attempt was overwritten with a fresh record.
            a_record = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertNotEqual(a_record["attempted_at_utc"], "2026-05-19T00:00:00Z")
            self.assertEqual(a_record["last_result"], paf.STATUS_PROBE_ONLY)


class TestCliRetryFlag(unittest.TestCase):
    """The CLI must expose --retry-previous-attempts (default false)."""

    def test_cli_flag_propagates_to_run_probe(self):
        captured: dict = {}

        def fake_run_probe(**kwargs):
            captured.update(kwargs)
            return {"selected": 0, "by_status": {}, "attempts": [], "run_id": "x",
                    "schema_version": paf.SCHEMA_VERSION, "options": {}}

        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [])
            orig = paf.run_probe
            paf.run_probe = fake_run_probe
            try:
                # Default: flag absent -> retry disabled.
                paf.main(["--store", str(store)])
                self.assertIn("retry_previous_attempts", captured)
                self.assertFalse(captured["retry_previous_attempts"])

                # Explicit opt-in.
                captured.clear()
                paf.main(["--store", str(store), "--retry-previous-attempts"])
                self.assertTrue(captured["retry_previous_attempts"])
            finally:
                paf.run_probe = orig


class TestDoiPrefixFilter(unittest.TestCase):
    """``--doi-prefix`` restricts selection to DOI-bearing rows whose
    ``preferred_identifier`` lives under one of the named registrant prefixes.

    The motivation is operational: we want to retry only the 10.2172 (OSTI)
    rows after wiring up the OSTI API tier, without re-running the broad
    authorized probe across every terminal failure in the queue.
    """

    def test_single_prefix_filters_to_matching_doi(self):
        rows = [
            _row("a", "10.2172/abc"),
            _row("b", "10.1029/xyz"),
            _row("c", "10.2172/def"),
        ]
        picked = paf.select_failed(rows, limit=10, doi_prefixes={"10.2172"})
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "c"])

    def test_multiple_prefixes_are_unioned(self):
        rows = [
            _row("a", "10.2172/abc"),
            _row("b", "10.1029/xyz"),
            _row("c", "10.5194/foo"),
        ]
        picked = paf.select_failed(
            rows, limit=10, doi_prefixes={"10.2172", "10.1029"}
        )
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "b"])

    def test_match_is_case_insensitive(self):
        rows = [
            _row("a", "10.2172/Abc"),
            _row("b", "10.2172/DEF"),
        ]
        picked = paf.select_failed(rows, limit=10, doi_prefixes={"10.2172"})
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "b"])
        # Prefix supplied in mixed case still matches.
        picked2 = paf.select_failed(rows, limit=10, doi_prefixes={"10.2172"})
        self.assertEqual([r["candidate_id"] for r in picked2], ["a", "b"])

    def test_prefix_must_be_full_registrant_not_partial(self):
        # ``10.21`` must NOT pretend-match ``10.2172`` / ``10.21273``.
        # Matching is on the full registrant segment (the part before the
        # first ``/``), so a substring like ``10.21`` only matches a DOI whose
        # registrant is exactly ``10.21``.
        rows = [
            _row("a", "10.2172/abc"),
            _row("b", "10.21273/xyz"),
            _row("c", "10.21/legit"),
        ]
        picked = paf.select_failed(rows, limit=10, doi_prefixes={"10.21"})
        self.assertEqual([r["candidate_id"] for r in picked], ["c"])

    def test_empty_set_keeps_legacy_behavior(self):
        rows = [
            _row("a", "10.2172/abc"),
            _row("b", "10.1029/xyz"),
        ]
        picked_none = paf.select_failed(rows, limit=10, doi_prefixes=None)
        picked_empty = paf.select_failed(rows, limit=10, doi_prefixes=set())
        self.assertEqual([r["candidate_id"] for r in picked_none], ["a", "b"])
        self.assertEqual([r["candidate_id"] for r in picked_empty], ["a", "b"])

    def test_prefix_excludes_arxiv_rows_even_when_set(self):
        # arXiv rows have no DOI registrant so the prefix can never apply.
        rows = [
            _row("a", "10.2172/abc"),
            {**_row("b", "arxiv:2301.00001", kind="arxiv"), "doi": None},
        ]
        picked = paf.select_failed(rows, limit=10, doi_prefixes={"10.2172"})
        self.assertEqual([r["candidate_id"] for r in picked], ["a"])

    def test_prefix_with_retry_does_not_broaden_to_other_prefixes(self):
        # SAFETY: ``--retry-previous-attempts`` together with --doi-prefix
        # must only retry rows that match the prefix. A 10.1029 row with a
        # prior terminal failure must still be skipped when the prefix is
        # 10.2172, even with retry enabled.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [
                _row("osti", "10.2172/abc"),
                _row("wiley", "10.1029/xyz"),
            ]
            _write_attempt_file(store, "osti", paf.STATUS_NO_LINK)
            _write_attempt_file(store, "wiley", paf.STATUS_NO_LINK)
            picked = paf.select_failed(
                rows,
                limit=10,
                store=store,
                retry_previous_attempts=True,
                doi_prefixes={"10.2172"},
            )
            self.assertEqual([r["candidate_id"] for r in picked], ["osti"])

    def test_prefix_without_retry_still_skips_prior_terminal_failures(self):
        # The prefix is purely additive over the existing terminal-failure
        # guard. Without --retry-previous-attempts the prior-failure rule
        # still wins so the same row is not re-probed.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [
                _row("osti1", "10.2172/abc"),
                _row("osti2", "10.2172/def"),
            ]
            _write_attempt_file(store, "osti1", paf.STATUS_NO_LINK)
            picked = paf.select_failed(
                rows,
                limit=10,
                store=store,
                doi_prefixes={"10.2172"},
            )
            self.assertEqual([r["candidate_id"] for r in picked], ["osti2"])

    def test_run_probe_threads_prefix_through(self):
        # End-to-end via run_probe: only the 10.2172 row should be probed,
        # the 10.1029 row must not be touched.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [
                _row("osti", "10.2172/abc"),
                _row("agu", "10.1029/xyz"),
            ])
            calls: list[str] = []
            base_router = make_router({
                "https://doi.org/10.2172/abc": FakeResponse(
                    200, {"content-type": "text/html"},
                    b"<html><body>No PDF here</body></html>",
                    "https://doi.org/10.2172/abc",
                ),
            })

            def recording(url, **kwargs):
                calls.append(url)
                return base_router(url, **kwargs)

            paf._http_get = recording

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
                doi_prefixes={"10.2172"},
            )

            self.assertEqual(summary["selected"], 1)
            self.assertTrue(
                all("10.1029" not in u for u in calls),
                f"non-matching prefix should not be probed; calls={calls}",
            )
            # Surfaced in the summary options for run reproducibility.
            self.assertEqual(
                sorted(summary["options"].get("doi_prefixes") or []),
                ["10.2172"],
            )


class TestCliDoiPrefixFlag(unittest.TestCase):
    """The CLI exposes --doi-prefix; repeatable and comma-separated allowed."""

    def _run_and_capture(self, argv):
        captured: dict = {}

        def fake_run_probe(**kwargs):
            captured.update(kwargs)
            return {"selected": 0, "by_status": {}, "attempts": [], "run_id": "x",
                    "schema_version": paf.SCHEMA_VERSION, "options": {}}

        orig = paf.run_probe
        paf.run_probe = fake_run_probe
        try:
            paf.main(argv)
        finally:
            paf.run_probe = orig
        return captured

    def test_repeatable_flag_collects_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [])
            captured = self._run_and_capture([
                "--store", str(store),
                "--doi-prefix", "10.2172",
                "--doi-prefix", "10.1029",
            ])
            self.assertEqual(captured.get("doi_prefixes"), {"10.2172", "10.1029"})

    def test_comma_separated_value_is_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [])
            captured = self._run_and_capture([
                "--store", str(store),
                "--doi-prefix", "10.2172,10.1029",
            ])
            self.assertEqual(captured.get("doi_prefixes"), {"10.2172", "10.1029"})

    def test_default_is_no_prefix_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [])
            captured = self._run_and_capture(["--store", str(store)])
            self.assertIn("doi_prefixes", captured)
            self.assertIsNone(captured["doi_prefixes"])

    def test_prefix_with_retry_flag_combines_safely(self):
        # The two CLI flags must be combinable: --doi-prefix narrows what
        # --retry-previous-attempts reselects. The captured kwargs should
        # carry both, not silently drop one.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [])
            captured = self._run_and_capture([
                "--store", str(store),
                "--retry-previous-attempts",
                "--doi-prefix", "10.2172",
            ])
            self.assertTrue(captured.get("retry_previous_attempts"))
            self.assertEqual(captured.get("doi_prefixes"), {"10.2172"})

    def test_whitespace_around_comma_is_tolerated(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [])
            captured = self._run_and_capture([
                "--store", str(store),
                "--doi-prefix", " 10.2172 , 10.1029 ",
            ])
            self.assertEqual(captured.get("doi_prefixes"), {"10.2172", "10.1029"})


class TestNormalizeProbeDoi(unittest.TestCase):
    """The probe strips the parasitic ``/pdf`` suffix that some discovery-time
    URL-to-DOI extractors glue onto A&A rows (observed on ~17 queue rows)."""

    def test_strips_trailing_pdf(self):
        self.assertEqual(
            paf._normalize_probe_doi("10.1051/0004-6361/202039407/pdf"),
            "10.1051/0004-6361/202039407",
        )

    def test_case_insensitive_strip(self):
        self.assertEqual(
            paf._normalize_probe_doi("10.1051/0004-6361/202039407/PDF"),
            "10.1051/0004-6361/202039407",
        )

    def test_leaves_clean_doi_alone(self):
        clean = "10.1051/0004-6361/202039407"
        self.assertEqual(paf._normalize_probe_doi(clean), clean)

    def test_empty_input_passes_through(self):
        self.assertEqual(paf._normalize_probe_doi(""), "")

    def test_strip_is_idempotent(self):
        # Defensive: even pathological double-suffixes should be normalised.
        self.assertEqual(
            paf._normalize_probe_doi("10.1051/0004-6361/202039407/pdf/pdf"),
            "10.1051/0004-6361/202039407",
        )

    def test_probe_uses_normalised_doi(self):
        # End-to-end: a queue row with /pdf suffix should be probed at the
        # canonical doi.org URL, not the 404-prone /pdf form.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1051/0004-6361/202039407/pdf")])

            calls: list[str] = []
            table = {
                "https://doi.org/10.1051/0004-6361/202039407": FakeResponse(
                    200,
                    {"content-type": "text/html"},
                    b'<html><head><meta name="citation_pdf_url" '
                    b'content="https://www.aanda.org/articles/aa/pdf/2021/06/aa39407-20.pdf" />'
                    b'</head></html>',
                    "https://www.aanda.org/articles/aa/full_html/2021/06/aa39407-20/aa39407-20.html",
                ),
            }
            base = make_router(table)

            def recording(url, **kwargs):
                calls.append(url)
                return base(url, **kwargs)

            paf._http_get = recording

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            # The probe must call the normalised URL, never the /pdf form.
            self.assertIn(
                "https://doi.org/10.1051/0004-6361/202039407", calls
            )
            self.assertNotIn(
                "https://doi.org/10.1051/0004-6361/202039407/pdf", calls
            )

            # Attempt record exposes the normalisation for auditability.
            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(
                attempt["preferred_identifier"],
                "10.1051/0004-6361/202039407/pdf",
            )
            self.assertEqual(
                attempt["doi_normalized"], "10.1051/0004-6361/202039407"
            )


class TestPublisherLandingOverride(unittest.TestCase):
    """AGU (10.1029) and Wiley (10.1002) get a publisher-direct landing URL
    because doi.org returned 403 to the probe's User-Agent in the live run.
    Other registrants must continue to use the doi.org proxy unchanged.
    """

    def test_agu_routes_to_agupubs(self):
        self.assertEqual(
            paf._publisher_landing_override("10.1029/2023ja031603"),
            "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023ja031603",
        )

    def test_wiley_routes_to_onlinelibrary(self):
        self.assertEqual(
            paf._publisher_landing_override("10.1002/2017ja024077"),
            "https://onlinelibrary.wiley.com/doi/10.1002/2017ja024077",
        )

    def test_non_overridden_registrant_returns_none(self):
        # IOPscience (10.1088), Springer (10.1007), Elsevier (10.1016),
        # A&A (10.1051), OSTI (10.2172), Copernicus (10.5194), AAS legacy
        # (10.1086) all stay on the proxy path -- their landing pages
        # already work or have a different failure mode.
        for prefix in (
            "10.1088", "10.1007", "10.1016", "10.1051",
            "10.2172", "10.5194", "10.1086", "10.3847", "10.1063",
        ):
            with self.subTest(prefix=prefix):
                self.assertIsNone(
                    paf._publisher_landing_override(f"{prefix}/example")
                )

    def test_empty_doi_returns_none(self):
        self.assertIsNone(paf._publisher_landing_override(""))

    def test_probe_uses_override_for_agu(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1029/2023ja031603")])

            calls: list[str] = []
            table = {
                "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023ja031603": FakeResponse(
                    200,
                    {"content-type": "text/html"},
                    b'<html><head><meta name="citation_pdf_url" '
                    b'content="https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/2023ja031603" />'
                    b'</head></html>',
                    "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023ja031603",
                ),
            }
            base = make_router(table)

            def recording(url, **kwargs):
                calls.append(url)
                return base(url, **kwargs)

            paf._http_get = recording

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            # Probe went directly to the AGU publisher landing, bypassing
            # the 403-prone doi.org proxy.
            self.assertIn(
                "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023ja031603",
                calls,
            )
            self.assertNotIn(
                "https://doi.org/10.1029/2023ja031603", calls
            )

            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["landing_route"], "publisher_direct")

    def test_probe_uses_proxy_for_non_overridden_registrant(self):
        # Sanity check: registrants without an override (here Springer)
        # still go through the doi.org proxy as before.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1007/s11207-023-02144-3")])

            calls: list[str] = []
            table = {
                "https://doi.org/10.1007/s11207-023-02144-3": FakeResponse(
                    200, {"content-type": "text/html"},
                    b'<html><head></head></html>',
                    "https://link.springer.com/article/10.1007/s11207-023-02144-3",
                ),
            }
            base = make_router(table)

            def recording(url, **kwargs):
                calls.append(url)
                return base(url, **kwargs)

            paf._http_get = recording

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertIn(
                "https://doi.org/10.1007/s11207-023-02144-3", calls
            )
            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["landing_route"], "doi_proxy")


class TestIsNonArticleDoi(unittest.TestCase):
    """EGU meeting-abstract DOIs (10.5194/egusphere-egu*) are conference
    abstracts hosted on meetingorganizer.copernicus.org, not full papers.
    They must short-circuit before any network call."""

    def test_egu_abstract_doi_is_non_article(self):
        for doi in (
            "10.5194/egusphere-egu23-3939",
            "10.5194/egusphere-egu24-7959",
            "10.5194/egusphere-egu25-14351",
        ):
            with self.subTest(doi=doi):
                self.assertTrue(paf._is_non_article_doi(doi))

    def test_real_copernicus_journal_doi_is_article(self):
        # ACP, ANGEO, etc. on Copernicus are real papers -- must NOT match.
        for doi in (
            "10.5194/acp-22-1-2022",
            "10.5194/angeo-39-1085-2021",
            "10.5194/wes-2023-62",
        ):
            with self.subTest(doi=doi):
                self.assertFalse(paf._is_non_article_doi(doi))

    def test_other_registrant_doi_is_article(self):
        for doi in (
            "10.1029/2023ja031603",
            "10.1051/0004-6361/202039407",
            "10.1088/0004-637x/718/1/251",
            "10.3847/1538-4357/aa603f",
        ):
            with self.subTest(doi=doi):
                self.assertFalse(paf._is_non_article_doi(doi))

    def test_probe_short_circuits_on_egu_abstract(self):
        # End-to-end: an EGU-abstract row must not make any HTTP call.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.5194/egusphere-egu23-3939")])

            calls: list[str] = []

            def recording(url, **kwargs):
                calls.append(url)
                return FakeResponse(
                    500, {"content-type": "text/plain"},
                    b"should-not-be-called", url,
                )

            paf._http_get = recording

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            # No HTTP calls were made.
            self.assertEqual(calls, [])
            # Attempt record uses the new terminal status.
            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["last_result"], paf.STATUS_NON_ARTICLE)
            self.assertEqual(summary["by_status"].get(paf.STATUS_NON_ARTICLE), 1)
            # Queue row stays fetch_failed (we never promote a non-article).
            rows = paf.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "fetch_failed")

    def test_non_article_terminal_status_skips_reprobe(self):
        # Repeated runs must not reprobe an EGU abstract: STATUS_NON_ARTICLE
        # is in the terminal-failure set, so select_failed should drop it.
        self.assertIn(paf.STATUS_NON_ARTICLE, paf.TERMINAL_FAILURE_RESULTS)
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            store.mkdir(parents=True)
            rows = [
                _row("egu", "10.5194/egusphere-egu23-3939"),
                _row("fresh", "10.5194/acp-22-1-2022"),
            ]
            _write_attempt_file(store, "egu", paf.STATUS_NON_ARTICLE)
            picked = paf.select_failed(rows, limit=10, store=store)
            self.assertEqual([r["candidate_id"] for r in picked], ["fresh"])


class TestCopernicusPreprintLanding(unittest.TestCase):
    """Copernicus ``<journal>d-<volume>-<page>-<year>`` discussion-paper DOIs
    have a fully deterministic landing URL that we can construct without any
    DOI-proxy negotiation. Only the ``d``-suffixed preprint shape should match;
    final published articles and meeting abstracts must fall through to the
    standard doi.org path (and EGU abstracts already short-circuit via
    ``_is_non_article_doi``).
    """

    def test_acpd_landing_url(self):
        # Parent task's canonical example, verified to serve application/pdf
        # at the constructed .pdf sibling URL.
        self.assertEqual(
            paf._copernicus_preprint_landing("10.5194/acpd-11-14003-2011"),
            "https://acp.copernicus.org/preprints/11/14003/2011/"
            "acpd-11-14003-2011.html",
        )

    def test_other_journal_d_shapes(self):
        # The pattern generalises across Copernicus journals that operate a
        # discussion server (acp/acpd, gmd/gmdd, angeo/angeod, npg/npgd, ...).
        cases = [
            (
                "10.5194/gmdd-7-3953-2014",
                "https://gmd.copernicus.org/preprints/7/3953/2014/"
                "gmdd-7-3953-2014.html",
            ),
            (
                "10.5194/angeod-30-1689-2012",
                "https://angeo.copernicus.org/preprints/30/1689/2012/"
                "angeod-30-1689-2012.html",
            ),
        ]
        for doi, expected in cases:
            with self.subTest(doi=doi):
                self.assertEqual(paf._copernicus_preprint_landing(doi), expected)

    def test_final_article_shape_does_not_match(self):
        # Final published articles (no trailing ``d`` on the journal slug)
        # already work via the standard Unpaywall path; helper must not
        # construct a guessed URL for them.
        for doi in (
            "10.5194/acp-22-1-2022",
            "10.5194/angeo-39-1085-2021",
            "10.5194/npg-3-247-1996",
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(paf._copernicus_preprint_landing(doi))
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))

    def test_egusphere_abstracts_do_not_match(self):
        # Meeting abstracts and modern egusphere preprints use entirely
        # different URL schemes; we explicitly leave them to other paths.
        for doi in (
            "10.5194/egusphere-egu23-3939",
            "10.5194/egusphere-egu2020-11425",
            "10.5194/egusphere-2025-523",
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(paf._copernicus_preprint_landing(doi))
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))

    def test_review_thread_shape_does_not_match(self):
        # ``acp-2015-891`` is a review-thread anchor, not the preprint
        # ``acpd-VOL-PAGE-YEAR`` shape. Helper must leave it alone.
        self.assertIsNone(paf._copernicus_preprint_landing("10.5194/acp-2015-891"))
        self.assertIsNone(paf._copernicus_preprint_pdf("10.5194/acp-2015-891"))

    def test_non_copernicus_doi_does_not_match(self):
        for doi in (
            "10.1029/2023ja031603",
            "10.1051/0004-6361/202039407",
            "10.1088/0004-637x/718/1/251",
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(paf._copernicus_preprint_landing(doi))
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))

    def test_empty_input(self):
        self.assertIsNone(paf._copernicus_preprint_landing(""))
        self.assertIsNone(paf._copernicus_preprint_landing(None))
        self.assertIsNone(paf._copernicus_preprint_pdf(""))
        self.assertIsNone(paf._copernicus_preprint_pdf(None))

    def test_publisher_override_dispatches_to_copernicus(self):
        # ``_publisher_landing_override`` is the integration seam used by the
        # per-row probe -- it must dispatch the preprint shape to the
        # Copernicus helper in preference to any prefix-only override.
        self.assertEqual(
            paf._publisher_landing_override("10.5194/acpd-11-14003-2011"),
            "https://acp.copernicus.org/preprints/11/14003/2011/"
            "acpd-11-14003-2011.html",
        )

    def test_probe_uses_copernicus_override_end_to_end(self):
        # End-to-end: probe constructs the preprint URL, fetches it, finds
        # the citation_pdf_url, and (in download mode) writes the PDF -- all
        # without ever calling doi.org.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.5194/acpd-11-14003-2011")])

            landing_url = (
                "https://acp.copernicus.org/preprints/11/14003/2011/"
                "acpd-11-14003-2011.html"
            )
            pdf_url = (
                "https://acp.copernicus.org/preprints/11/14003/2011/"
                "acpd-11-14003-2011.pdf"
            )
            pdf_bytes = b"%PDF-1.4 fake bytes\n%%EOF"
            table = {
                landing_url: FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    f'<html><head><meta name="citation_pdf_url" content="{pdf_url}" />'
                    f'</head></html>'.encode(),
                    landing_url,
                ),
                pdf_url: FakeResponse(
                    200, {"content-type": "application/pdf"}, pdf_bytes, pdf_url,
                ),
            }
            calls: list[str] = []
            base = make_router(table)

            def recording(url, **kwargs):
                calls.append(url)
                return base(url, **kwargs)

            paf._http_get = recording

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            # Probe bypassed doi.org entirely.
            self.assertNotIn(
                "https://doi.org/10.5194/acpd-11-14003-2011", calls
            )
            self.assertIn(landing_url, calls)
            self.assertIn(pdf_url, calls)

            # PDF was written and queue promoted.
            written = list((store / "papers").glob("*/paper.pdf"))
            self.assertEqual(len(written), 1)
            self.assertEqual(written[0].read_bytes(), pdf_bytes)
            self.assertEqual(summary["by_status"].get("fetched"), 1)

            attempt = json.loads((store / "authorized_attempts" / "a.json").read_text())
            self.assertEqual(attempt["landing_route"], "publisher_direct")
            self.assertEqual(attempt["last_result"], "fetched")


class TestCopernicusPreprintPdf(unittest.TestCase):
    """Companion to ``_copernicus_preprint_landing``: returns the deterministic
    same-host PDF URL for the ``<journal>d-<volume>-<page>-<year>`` discussion
    preprint shape. This exists because in the live observation the constructed
    HTML landing page is a minimal stub without ``citation_pdf_url`` while the
    sibling ``.pdf`` URL on the same host returns ``application/pdf``. The
    helper lets the probe fall back to that deterministic candidate without any
    network I/O of its own; downstream same-host / content-type / %PDF-magic
    validation in ``_probe_one`` is unchanged.
    """

    def test_acpd_pdf_url(self):
        self.assertEqual(
            paf._copernicus_preprint_pdf("10.5194/acpd-11-14003-2011"),
            "https://acp.copernicus.org/preprints/11/14003/2011/"
            "acpd-11-14003-2011.pdf",
        )

    def test_other_journal_d_shapes(self):
        cases = [
            (
                "10.5194/gmdd-7-3953-2014",
                "https://gmd.copernicus.org/preprints/7/3953/2014/"
                "gmdd-7-3953-2014.pdf",
            ),
            (
                "10.5194/angeod-30-1689-2012",
                "https://angeo.copernicus.org/preprints/30/1689/2012/"
                "angeod-30-1689-2012.pdf",
            ),
        ]
        for doi, expected in cases:
            with self.subTest(doi=doi):
                self.assertEqual(paf._copernicus_preprint_pdf(doi), expected)

    def test_pdf_and_landing_share_host_and_stem(self):
        # By construction the deterministic PDF must live on the same host
        # as the landing URL and share its filename stem. This is what makes
        # the downstream same-host validation pass without any extra logic.
        from urllib.parse import urlparse
        doi = "10.5194/acpd-11-14003-2011"
        landing = paf._copernicus_preprint_landing(doi)
        pdf = paf._copernicus_preprint_pdf(doi)
        self.assertIsNotNone(landing)
        self.assertIsNotNone(pdf)
        self.assertEqual(urlparse(landing).hostname, urlparse(pdf).hostname)
        self.assertTrue(landing.endswith(".html"))
        self.assertTrue(pdf.endswith(".pdf"))
        self.assertEqual(landing[: -len(".html")], pdf[: -len(".pdf")])

    def test_final_article_shape_does_not_match(self):
        for doi in (
            "10.5194/acp-22-1-2022",
            "10.5194/angeo-39-1085-2021",
            "10.5194/npg-3-247-1996",
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))

    def test_egusphere_does_not_match(self):
        for doi in (
            "10.5194/egusphere-egu23-3939",
            "10.5194/egusphere-2025-523",
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))

    def test_non_copernicus_does_not_match(self):
        for doi in (
            "10.1029/2023ja031603",
            "10.1051/0004-6361/202039407",
            "10.1088/0004-637x/718/1/251",
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(paf._copernicus_preprint_pdf(doi))

    def test_empty_and_none_input(self):
        self.assertIsNone(paf._copernicus_preprint_pdf(""))
        self.assertIsNone(paf._copernicus_preprint_pdf(None))


class TestCopernicusPreprintFallback(unittest.TestCase):
    """End-to-end: for ``<journal>d-<volume>-<page>-<year>`` Copernicus DOIs,
    when the constructed landing page is a stub without ``citation_pdf_url``
    (the live-observed shape for acpd-11-14003-2011), the probe must fall back
    to the deterministic same-host ``.pdf`` URL rather than recording
    ``no_official_pdf_link``. Same-host / content-type / %PDF-magic / final-url
    validation must still gate the download."""

    LANDING_URL = (
        "https://acp.copernicus.org/preprints/11/14003/2011/"
        "acpd-11-14003-2011.html"
    )
    PDF_URL = (
        "https://acp.copernicus.org/preprints/11/14003/2011/"
        "acpd-11-14003-2011.pdf"
    )

    def _stub_landing_html(self) -> bytes:
        # A minimal HTML stub without citation_pdf_url and without any
        # same-host PDF anchor -- the live-observed shape that makes
        # extract_pdf_link return None.
        return (
            b"<html><head><title>acpd-11-14003-2011</title></head>"
            b"<body><p>Preprint metadata page.</p></body></html>"
        )

    def test_probe_only_uses_deterministic_pdf_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.5194/acpd-11-14003-2011")])

            table = {
                self.LANDING_URL: FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    self._stub_landing_html(),
                    self.LANDING_URL,
                ),
                # No HTTP call to the .pdf URL in dry-run mode; it must
                # only appear as the discovered candidate.
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(summary["selected"], 1)
            self.assertEqual(summary["by_status"].get("probe_only"), 1)

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "probe_only")
            # The discovered candidate is the deterministic same-host PDF URL,
            # not None (which would have produced no_official_pdf_link).
            self.assertEqual(attempt["pdf_url"], self.PDF_URL)
            # Audit field exposes that this was a deterministic fallback,
            # not a citation_pdf_url discovered on the landing page.
            self.assertEqual(
                attempt.get("pdf_url_source"),
                "copernicus_preprint_deterministic",
            )

    def test_probe_download_uses_deterministic_pdf_fallback(self):
        pdf_bytes = b"%PDF-1.4 fake bytes\n%%EOF"
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.5194/acpd-11-14003-2011")])

            table = {
                self.LANDING_URL: FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    self._stub_landing_html(),
                    self.LANDING_URL,
                ),
                self.PDF_URL: FakeResponse(
                    200, {"content-type": "application/pdf"},
                    pdf_bytes, self.PDF_URL,
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(summary["by_status"].get("fetched"), 1)
            written = list((store / "papers").glob("*/paper.pdf"))
            self.assertEqual(len(written), 1)
            self.assertEqual(written[0].read_bytes(), pdf_bytes)

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "fetched")
            self.assertEqual(attempt["pdf_url"], self.PDF_URL)
            self.assertEqual(
                attempt.get("pdf_url_source"),
                "copernicus_preprint_deterministic",
            )

    def test_landing_citation_pdf_url_still_wins_when_present(self):
        # Defensive: if a future Copernicus landing page DOES expose a
        # citation_pdf_url, we should keep using that path. The deterministic
        # fallback only fires when extract_pdf_link returns None.
        landing_pdf = (
            "https://acp.copernicus.org/preprints/11/14003/2011/"
            "different-name.pdf"
        )
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.5194/acpd-11-14003-2011")])

            table = {
                self.LANDING_URL: FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    (
                        b'<html><head><meta name="citation_pdf_url" content="'
                        + landing_pdf.encode()
                        + b'" /></head></html>'
                    ),
                    self.LANDING_URL,
                ),
            }
            paf._http_get = make_router(table)

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["pdf_url"], landing_pdf)
            # When the link came from the landing HTML itself, the audit field
            # must NOT mark it as a deterministic fallback.
            self.assertNotEqual(
                attempt.get("pdf_url_source"),
                "copernicus_preprint_deterministic",
            )

    def test_non_copernicus_no_fallback_still_records_no_link(self):
        # Sanity: the deterministic fallback is Copernicus-specific. A
        # non-matching DOI whose landing page yields no PDF link must still
        # record no_official_pdf_link, not silently pick up some other URL.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1051/0004-6361/202039407")])

            table = {
                "https://doi.org/10.1051/0004-6361/202039407": FakeResponse(
                    200, {"content-type": "text/html"},
                    b"<html><body>No PDF link here</body></html>",
                    "https://www.aanda.org/articles/aa/full_html/2021/06/foo/foo.html",
                ),
            }
            paf._http_get = make_router(table)

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "no_official_pdf_link")
            self.assertIsNone(attempt.get("pdf_url"))

    def test_off_host_redirect_on_pdf_still_rejected(self):
        # The deterministic candidate is same-host by construction, but if a
        # 3xx chain redirects the actual PDF response off-host, the existing
        # final-URL same-host check must still reject it. This is the safety
        # rail the task asked us to preserve.
        off_host_pdf = "https://other-host.example/something.pdf"
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.5194/acpd-11-14003-2011")])

            table = {
                self.LANDING_URL: FakeResponse(
                    200,
                    {"content-type": "text/html; charset=utf-8"},
                    self._stub_landing_html(),
                    self.LANDING_URL,
                ),
                self.PDF_URL: FakeResponse(
                    302,
                    {"location": off_host_pdf, "content-type": "text/html"},
                    b"", self.PDF_URL,
                ),
                off_host_pdf: FakeResponse(
                    200, {"content-type": "application/pdf"},
                    b"%PDF-1.4 off-host", off_host_pdf,
                ),
            }
            paf._http_get = make_router(table)

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(list((store / "papers").glob("*/paper.pdf")), [])
            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "rejected_not_pdf")
            self.assertEqual(
                attempt.get("error"), "pdf_final_url_off_publisher_host",
            )


class TestIsOffTopicDoi(unittest.TestCase):
    """R6: off-topic / non-article queue-side predicate.

    Per the audit (Section 6), seven DOI prefixes plus a set of lexical
    boilerplate title shapes account for ~240 rows that should be classified
    out of the active retry pool rather than reprobed. This predicate is the
    classifier; it must not mutate any queue, and must not download anything
    by itself — the dry-run preview CLI consumes it.

    Confidence tiers (audit Section 6):
      - definitively off-topic: 10.3406 (Persée), 10.21273 (ASHS),
        10.5962 (BHL), 10.5040 (Bloomsbury)
      - off-topic review threads: 10.7287 (PeerJ Preprints reviews)
      - mixed/conservative (must require lexical boilerplate match): 10.2307
        (JSTOR), 10.21236 (DTIC)
      - lexical boilerplate (any prefix): Corrigendum, Erratum, Editorial
        Board, Acknowledgments, Table of Contents, etc.
    """

    OFF_TOPIC_PREFIXES = (
        "10.3406",   # Persée
        "10.21273",  # ASHS horticulture
        "10.5962",   # BHL
        "10.5040",   # Bloomsbury
        "10.7287",   # PeerJ preprints (review threads)
    )

    MIXED_PREFIXES = ("10.2307", "10.21236")

    BOILERPLATE_TITLES = (
        "Corrigendum",
        "Corrigendum to: Some Paper",
        "Erratum",
        "Erratum: Title Here",
        "Editorial Board",
        "Acknowledgments",
        "Acknowledgements",  # British spelling
        "Table of Contents",
        "Front Matter",
        "Back Matter",
        "Index",
        "List of Contributors",
        "Author Index",
        "Subject Index",
        "Issue Information",
    )

    HELIOPHYSICS_TITLES = (
        "Magnetic reconnection in the solar corona",
        "Solar wind turbulence at 1 AU",
        "Switchbacks observed by Parker Solar Probe",
        "Three-dimensional MHD simulation of CMEs",
    )

    def test_definitively_off_topic_prefixes(self):
        for prefix in self.OFF_TOPIC_PREFIXES:
            with self.subTest(prefix=prefix):
                self.assertTrue(
                    paf._is_off_topic_doi(f"{prefix}/foo", "Some Title")
                )

    def test_mixed_prefix_without_boilerplate_is_not_classified(self):
        # Conservative: 10.2307 (JSTOR) and 10.21236 (DTIC) cover real
        # heliophysics-relevant content too. Without an obvious boilerplate
        # title we must not classify them.
        for prefix in self.MIXED_PREFIXES:
            with self.subTest(prefix=prefix):
                self.assertFalse(
                    paf._is_off_topic_doi(
                        f"{prefix}/foo",
                        "Plasma observations of the heliosphere",
                    )
                )

    def test_mixed_prefix_with_boilerplate_is_classified(self):
        for prefix in self.MIXED_PREFIXES:
            with self.subTest(prefix=prefix):
                self.assertTrue(
                    paf._is_off_topic_doi(
                        f"{prefix}/foo", "Editorial Board"
                    )
                )

    def test_lexical_boilerplate_any_prefix(self):
        for title in self.BOILERPLATE_TITLES:
            with self.subTest(title=title):
                self.assertTrue(
                    paf._is_off_topic_doi("10.1029/2023ja031603", title)
                )

    def test_boilerplate_case_insensitive(self):
        self.assertTrue(
            paf._is_off_topic_doi("10.1029/foo", "CORRIGENDUM")
        )
        self.assertTrue(
            paf._is_off_topic_doi("10.1029/foo", "corrigendum to: paper")
        )

    def test_heliophysics_titles_on_normal_prefix_not_classified(self):
        for title in self.HELIOPHYSICS_TITLES:
            with self.subTest(title=title):
                self.assertFalse(
                    paf._is_off_topic_doi("10.1029/2023ja031603", title)
                )

    def test_empty_doi_returns_false(self):
        # Defensive: no DOI means we cannot classify by prefix; if title is
        # also empty/unremarkable, return False (do not classify).
        self.assertFalse(paf._is_off_topic_doi("", ""))
        self.assertFalse(paf._is_off_topic_doi(None, None))

    def test_empty_title_with_off_topic_prefix_still_classified(self):
        # An off-topic prefix alone is enough — title may be missing.
        self.assertTrue(paf._is_off_topic_doi("10.3406/foo", ""))
        self.assertTrue(paf._is_off_topic_doi("10.3406/foo", None))

    def test_boilerplate_word_not_classified_in_substring(self):
        # We match boilerplate as the dominant title shape, not as a substring
        # of a longer real title. "Index of refraction" should NOT match.
        # We accept a leading boilerplate keyword (e.g. "Erratum: ...") as a
        # match because that is how journals title corrections.
        self.assertFalse(
            paf._is_off_topic_doi(
                "10.1029/foo",
                "Index of refraction of the interplanetary plasma",
            )
        )

    def test_returns_classification_reason(self):
        # _classify_off_topic returns (matched: bool, reason: str|None) so the
        # preview CLI can surface why each row was flagged.
        matched, reason = paf._classify_off_topic(
            "10.3406/abcd", "Some Title"
        )
        self.assertTrue(matched)
        self.assertIn("10.3406", reason)

        matched, reason = paf._classify_off_topic(
            "10.1029/foo", "Erratum: Solar Wind Paper"
        )
        self.assertTrue(matched)
        self.assertIn("Erratum".lower(), reason.lower())

        matched, reason = paf._classify_off_topic(
            "10.1029/foo", "Solar wind turbulence at 1 AU"
        )
        self.assertFalse(matched)
        self.assertIsNone(reason)


class TestClassifyOffTopicPreviewCli(unittest.TestCase):
    """The --classify-off-topic-preview CLI mode must be read-only:
    - it must scan the queue and print candidate rows;
    - it MUST NOT rewrite queue.jsonl or queue.csv;
    - it MUST NOT make any HTTP call.
    Output format: TSV by default; JSONL when --format jsonl is passed.
    """

    def _make_queue(self, store: Path) -> None:
        rows = [
            # Off-topic by prefix.
            {**_row("a", "10.3406/persee-fr-article"), "title": "L'histoire de France"},
            # Off-topic by lexical boilerplate.
            {**_row("b", "10.1029/2023ja031603"), "title": "Corrigendum to: prior paper"},
            # Normal heliophysics row — must NOT be in preview.
            {**_row("c", "10.1029/2023ja031604"), "title": "Solar wind at 1 AU"},
            # Mixed-prefix without boilerplate — must NOT be classified.
            {**_row("d", "10.2307/abcd"), "title": "Plasma waves in the heliosphere"},
            # Mixed prefix WITH boilerplate — should be classified.
            {**_row("e", "10.2307/efgh"), "title": "Editorial Board"},
            # ASHS horticulture — off-topic prefix.
            {**_row("f", "10.21273/HORTSCI"), "title": "Strawberry cultivars"},
        ]
        # Add a fetched row (already done) and a no_supported_identifier row;
        # they must be ignored by the preview (only fetch_failed is in scope).
        rows.append({**_row("g", "10.3406/already_fetched", status="fetched"),
                     "title": "off-topic but already fetched"})
        _seed_queue(store, rows)

    def test_preview_prints_only_flagged_candidates_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            self._make_queue(store)

            # Capture stdout.
            import io as _io
            import contextlib

            buf = _io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = paf.main(
                    ["--store", str(store), "--classify-off-topic-preview"]
                )
            self.assertEqual(rc, 0)
            out = buf.getvalue()

            # TSV format: header + flagged rows.
            lines = [ln for ln in out.splitlines() if ln.strip()]
            # Header line.
            self.assertTrue(lines[0].startswith("candidate_id\t"))
            # Flagged candidate_ids appear; non-flagged do not.
            flagged_ids = []
            for line in lines[1:]:
                cols = line.split("\t")
                flagged_ids.append(cols[0])
            self.assertIn("a", flagged_ids)  # 10.3406 prefix
            self.assertIn("b", flagged_ids)  # Corrigendum
            self.assertIn("e", flagged_ids)  # 10.2307 + Editorial Board
            self.assertIn("f", flagged_ids)  # 10.21273 ASHS
            # Non-flagged must not appear.
            self.assertNotIn("c", flagged_ids)  # normal helio row
            self.assertNotIn("d", flagged_ids)  # 10.2307 w/o boilerplate
            self.assertNotIn("g", flagged_ids)  # status != fetch_failed

    def test_preview_does_not_mutate_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            self._make_queue(store)

            queue_path = store / "queue.jsonl"
            before_mtime = queue_path.stat().st_mtime_ns
            before_bytes = queue_path.read_bytes()

            import io as _io
            import contextlib

            with contextlib.redirect_stdout(_io.StringIO()):
                rc = paf.main(
                    ["--store", str(store), "--classify-off-topic-preview"]
                )
            self.assertEqual(rc, 0)

            # File untouched.
            after_bytes = queue_path.read_bytes()
            self.assertEqual(before_bytes, after_bytes)

            # The rows in the queue still all have their original status.
            rows = paf.read_queue(queue_path)
            statuses = {r["candidate_id"]: r["status"] for r in rows}
            self.assertEqual(statuses["a"], "fetch_failed")
            self.assertEqual(statuses["b"], "fetch_failed")
            self.assertEqual(statuses["g"], "fetched")

    def test_preview_does_not_call_http_get(self):
        # Preview must NOT make any HTTP call. We sabotage _http_get to
        # raise if called.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            self._make_queue(store)

            def explode(url, **kw):
                raise AssertionError(
                    f"preview must not call _http_get; got {url}"
                )

            paf._http_get = explode

            import io as _io
            import contextlib

            with contextlib.redirect_stdout(_io.StringIO()):
                rc = paf.main(
                    ["--store", str(store), "--classify-off-topic-preview"]
                )
            self.assertEqual(rc, 0)

    def test_preview_jsonl_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            self._make_queue(store)

            import io as _io
            import contextlib

            buf = _io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = paf.main(
                    ["--store", str(store),
                     "--classify-off-topic-preview",
                     "--format", "jsonl"]
                )
            self.assertEqual(rc, 0)
            out = buf.getvalue()

            records = [json.loads(ln) for ln in out.splitlines() if ln.strip()]
            ids = [r["candidate_id"] for r in records]
            self.assertIn("a", ids)
            self.assertNotIn("c", ids)
            self.assertNotIn("g", ids)
            # Each JSONL record carries the documented fields.
            for r in records:
                self.assertIn("candidate_id", r)
                self.assertIn("doi", r)
                self.assertIn("prefix", r)
                self.assertIn("year", r)
                self.assertIn("title", r)
                self.assertIn("reason", r)

    def test_preview_does_not_classify_arxiv_only_rows(self):
        # Preview is scoped to DOI-bearing rows in fetch_failed (the active
        # retry surface). An arxiv-only row should not appear even if its
        # title is "Corrigendum" (defensive: avoids over-broad flagging).
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            rows = [
                {**_row("ax", "arxiv:2301.00001", kind="arxiv"),
                 "title": "Corrigendum",
                 "doi": None},
                {**_row("dx", "10.1029/foo"), "title": "Corrigendum"},
            ]
            _seed_queue(store, rows)

            import io as _io
            import contextlib

            buf = _io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = paf.main(
                    ["--store", str(store),
                     "--classify-off-topic-preview"]
                )
            self.assertEqual(rc, 0)
            out = buf.getvalue()
            self.assertNotIn("ax", out)
            self.assertIn("dx", out)


class TestIsOstiDoi(unittest.TestCase):
    """The OSTI tier only fires for DOIs registered under ``10.2172``."""

    def test_canonical_osti_doi(self):
        self.assertTrue(paf._is_osti_doi("10.2172/1234567"))

    def test_case_insensitive(self):
        self.assertTrue(paf._is_osti_doi("10.2172/AbCdEf"))

    def test_with_leading_whitespace(self):
        self.assertTrue(paf._is_osti_doi("  10.2172/abc  "))

    def test_non_osti_doi(self):
        for doi in (
            "10.1029/2023ja031603",
            "10.1051/0004-6361/202039407",
            "10.5194/acpd-11-14003-2011",
            "10.21726/bar",  # prefix that *contains* "2172" as substring
        ):
            with self.subTest(doi=doi):
                self.assertFalse(paf._is_osti_doi(doi))

    def test_empty_or_none(self):
        self.assertFalse(paf._is_osti_doi(""))
        self.assertFalse(paf._is_osti_doi(None))


class TestExtractOstiPdfUrl(unittest.TestCase):
    """JSON-payload-only tests for the OSTI fulltext-link extractor.

    No HTTP. The extractor is robust to schema variants: array vs single
    record, ``links[]`` with ``rel=fulltext``, ``media[]`` with format=pdf,
    plain top-level ``.pdf`` URL fields. Bare landing-page URLs (no .pdf
    suffix) must not be returned, since downstream content-type validation
    would simply reject an HTML response.
    """

    def test_links_rel_fulltext_wins(self):
        payload = [
            {
                "osti_id": 12345,
                "title": "DOE technical report",
                "links": [
                    {"rel": "citation", "href": "https://www.osti.gov/biblio/12345"},
                    {"rel": "fulltext", "href": "https://www.osti.gov/servlets/purl/12345"},
                ],
            }
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/servlets/purl/12345",
        )

    def test_links_rel_fulltext_case_insensitive(self):
        payload = [
            {
                "links": [
                    {"rel": "Fulltext", "href": "https://www.osti.gov/x"},
                ]
            }
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/x",
        )

    def test_links_pdf_suffix_when_no_fulltext_rel(self):
        payload = [
            {
                "links": [
                    {"rel": "citation", "href": "https://www.osti.gov/biblio/9"},
                    {"rel": "other", "href": "https://www.osti.gov/servlets/purl/9.pdf"},
                ]
            }
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/servlets/purl/9.pdf",
        )

    def test_single_record_object_not_array(self):
        payload = {
            "osti_id": 1,
            "links": [{"rel": "fulltext", "href": "https://www.osti.gov/x"}],
        }
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/x",
        )

    def test_records_wrapper_object(self):
        payload = {
            "records": [
                {"links": [{"rel": "fulltext", "href": "https://www.osti.gov/y"}]}
            ]
        }
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/y",
        )

    def test_media_array_pdf_format(self):
        payload = [
            {
                "media": [
                    {"url": "https://www.osti.gov/servlets/purl/42", "mediaFileFormat": "PDF"},
                ]
            }
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/servlets/purl/42",
        )

    def test_media_array_url_with_pdf_suffix(self):
        payload = [
            {
                "media": [
                    {"url": "https://www.osti.gov/foo/42.pdf"},
                ]
            }
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/foo/42.pdf",
        )

    def test_top_level_pdf_url_field(self):
        payload = [
            {
                "media_url": "https://www.osti.gov/foo/9.pdf",
            }
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/foo/9.pdf",
        )

    def test_top_level_product_url_without_pdf_is_ignored(self):
        # A bare landing page is what we already get via doi.org -- so the
        # extractor must NOT return it as a "PDF" candidate.
        payload = [
            {
                "product_url": "https://www.osti.gov/biblio/12345",
            }
        ]
        self.assertIsNone(paf._extract_osti_pdf_url(payload))

    def test_no_links_no_media_returns_none(self):
        payload = [{"osti_id": 1, "title": "no fulltext exposed"}]
        self.assertIsNone(paf._extract_osti_pdf_url(payload))

    def test_empty_list_returns_none(self):
        self.assertIsNone(paf._extract_osti_pdf_url([]))

    def test_none_payload_returns_none(self):
        self.assertIsNone(paf._extract_osti_pdf_url(None))

    def test_malformed_record_ignored(self):
        # Mixed garbage: a string, a None, then a real record.
        payload = [
            "not a record",
            None,
            {"links": [{"rel": "fulltext", "href": "https://www.osti.gov/z"}]},
        ]
        self.assertEqual(
            paf._extract_osti_pdf_url(payload),
            "https://www.osti.gov/z",
        )

    def test_links_with_unexpected_types(self):
        # ``links`` is the right key but its entries are malformed -- the
        # extractor must not crash; it returns None.
        payload = [
            {"links": ["string entry", None, {"rel": None, "href": None}]}
        ]
        self.assertIsNone(paf._extract_osti_pdf_url(payload))


class TestOstiApiPdfUrl(unittest.TestCase):
    """The HTTP-facing helper. Monkeypatch ``_http_get`` to return canned JSON.
    Live network is forbidden in tests.
    """

    def test_non_osti_doi_short_circuits(self):
        # Sentinel: any _http_get call would fail the test.
        def explode(url, **kw):
            raise AssertionError(f"non-OSTI DOI must not call API; got {url}")
        paf._http_get = explode
        for doi in (
            "10.1029/2023ja031603",
            "10.5194/acpd-11-14003-2011",
            "",
            None,
        ):
            with self.subTest(doi=doi):
                self.assertIsNone(
                    paf._osti_api_pdf_url(doi, timeout=5.0, user_agent="UA")
                )

    def test_successful_api_returns_pdf_url(self):
        body = json.dumps([
            {
                "osti_id": 12345,
                "links": [
                    {"rel": "fulltext",
                     "href": "https://www.osti.gov/servlets/purl/12345"},
                ],
            }
        ]).encode("utf-8")
        api_url = (
            "https://www.osti.gov/api/v1/records?identifier=12345"
        )
        table = {
            api_url: FakeResponse(
                200, {"content-type": "application/json"}, body, api_url,
            ),
        }
        calls: list[str] = []
        base = make_router(table)

        def recording(url, **kw):
            calls.append(url)
            return base(url, **kw)

        paf._http_get = recording

        result = paf._osti_api_pdf_url(
            "10.2172/12345", timeout=5.0, user_agent="UA",
        )
        self.assertEqual(result, "https://www.osti.gov/servlets/purl/12345")
        self.assertEqual(calls, [api_url])

    def test_api_http_error_returns_none(self):
        api_url = "https://www.osti.gov/api/v1/records?identifier=99"
        table = {
            api_url: FakeResponse(
                500, {"content-type": "text/plain"}, b"server error", api_url,
            ),
        }
        paf._http_get = make_router(table)
        self.assertIsNone(
            paf._osti_api_pdf_url("10.2172/99", timeout=5.0, user_agent="UA")
        )

    def test_api_404_returns_none(self):
        # Unknown identifier -> the router's default 404 with empty body.
        paf._http_get = make_router({})
        self.assertIsNone(
            paf._osti_api_pdf_url("10.2172/missing", timeout=5.0, user_agent="UA")
        )

    def test_api_malformed_json_returns_none(self):
        api_url = "https://www.osti.gov/api/v1/records?identifier=bad"
        table = {
            api_url: FakeResponse(
                200, {"content-type": "application/json"},
                b"{not json", api_url,
            ),
        }
        paf._http_get = make_router(table)
        self.assertIsNone(
            paf._osti_api_pdf_url("10.2172/bad", timeout=5.0, user_agent="UA")
        )

    def test_api_no_link_returns_none(self):
        api_url = "https://www.osti.gov/api/v1/records?identifier=barerec"
        body = json.dumps([{"osti_id": 1, "title": "no fulltext"}]).encode("utf-8")
        table = {
            api_url: FakeResponse(
                200, {"content-type": "application/json"}, body, api_url,
            ),
        }
        paf._http_get = make_router(table)
        self.assertIsNone(
            paf._osti_api_pdf_url(
                "10.2172/barerec", timeout=5.0, user_agent="UA"
            )
        )

    def test_api_raises_exception_is_swallowed(self):
        def boom(url, **kw):
            raise RuntimeError("network down")
        paf._http_get = boom
        # Helper must never raise; it falls back to the standard path.
        self.assertIsNone(
            paf._osti_api_pdf_url("10.2172/x", timeout=5.0, user_agent="UA")
        )


class TestOstiWiringEndToEnd(unittest.TestCase):
    """End-to-end: a 10.2172 row queries the OSTI API, then uses the returned
    URL as the PDF candidate; downstream content-type / %PDF-magic / same-host
    validation still gates the actual download.
    """

    LANDING = "https://www.osti.gov/biblio/12345"
    PDF_URL = "https://www.osti.gov/servlets/purl/12345"
    API_URL = "https://www.osti.gov/api/v1/records?identifier=12345"

    def _api_body(self) -> bytes:
        return json.dumps([
            {
                "osti_id": 12345,
                "links": [
                    {"rel": "fulltext", "href": self.PDF_URL},
                ],
            }
        ]).encode("utf-8")

    def test_probe_only_uses_osti_api_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.2172/12345")])

            table = {
                self.API_URL: FakeResponse(
                    200, {"content-type": "application/json"},
                    self._api_body(), self.API_URL,
                ),
                "https://doi.org/10.2172/12345": FakeResponse(
                    302,
                    {"location": self.LANDING, "content-type": "text/html"},
                    b"", "https://doi.org/10.2172/12345",
                ),
                self.LANDING: FakeResponse(
                    200, {"content-type": "text/html; charset=utf-8"},
                    # OSTI landing pages do not expose citation_pdf_url and
                    # the PDF link is JS-rendered; the extractor must rely on
                    # the API.
                    b"<html><body>JS-rendered landing</body></html>",
                    self.LANDING,
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(summary["selected"], 1)
            self.assertEqual(summary["by_status"].get("probe_only"), 1)

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "probe_only")
            self.assertEqual(attempt["pdf_url"], self.PDF_URL)
            self.assertEqual(attempt.get("pdf_url_source"), "osti_api")

    def test_download_uses_osti_api_candidate(self):
        pdf_bytes = b"%PDF-1.4 fake osti bytes\n%%EOF"
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.2172/12345")])

            table = {
                self.API_URL: FakeResponse(
                    200, {"content-type": "application/json"},
                    self._api_body(), self.API_URL,
                ),
                "https://doi.org/10.2172/12345": FakeResponse(
                    302,
                    {"location": self.LANDING, "content-type": "text/html"},
                    b"", "https://doi.org/10.2172/12345",
                ),
                self.LANDING: FakeResponse(
                    200, {"content-type": "text/html; charset=utf-8"},
                    b"<html><body>JS-rendered</body></html>",
                    self.LANDING,
                ),
                self.PDF_URL: FakeResponse(
                    200, {"content-type": "application/pdf"},
                    pdf_bytes, self.PDF_URL,
                ),
            }
            paf._http_get = make_router(table)

            summary = paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(summary["by_status"].get("fetched"), 1)
            written = list((store / "papers").glob("*/paper.pdf"))
            self.assertEqual(len(written), 1)
            self.assertEqual(written[0].read_bytes(), pdf_bytes)

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "fetched")
            self.assertEqual(attempt["pdf_url"], self.PDF_URL)
            self.assertEqual(attempt.get("pdf_url_source"), "osti_api")

    def test_api_returns_no_link_falls_back_to_no_link(self):
        # API returns 200 with a record but no fulltext link; landing page
        # also exposes no PDF -> ``no_official_pdf_link``.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.2172/77")])

            empty_body = json.dumps([{"osti_id": 77, "title": "no fulltext"}]).encode("utf-8")
            table = {
                "https://www.osti.gov/api/v1/records?identifier=77": FakeResponse(
                    200, {"content-type": "application/json"},
                    empty_body,
                    "https://www.osti.gov/api/v1/records?identifier=77",
                ),
                "https://doi.org/10.2172/77": FakeResponse(
                    200, {"content-type": "text/html"},
                    b"<html><body>JS-rendered</body></html>",
                    "https://www.osti.gov/biblio/77",
                ),
            }
            paf._http_get = make_router(table)

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "no_official_pdf_link")

    def test_api_error_falls_back_to_landing_page(self):
        # If the API errors out, the probe still tries the landing-page
        # extractor. Seed a landing page that exposes citation_pdf_url so
        # the fallback succeeds and the attempt is recorded with
        # ``pdf_url_source='landing_page_link'``.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.2172/88")])

            html = (
                b'<html><head>'
                b'<meta name="citation_pdf_url" '
                b'content="https://www.osti.gov/biblio/88.pdf" />'
                b'</head></html>'
            )
            table = {
                "https://www.osti.gov/api/v1/records?identifier=88": FakeResponse(
                    500, {"content-type": "text/plain"}, b"oops",
                    "https://www.osti.gov/api/v1/records?identifier=88",
                ),
                "https://doi.org/10.2172/88": FakeResponse(
                    302,
                    {"location": "https://www.osti.gov/biblio/88",
                     "content-type": "text/html"},
                    b"", "https://doi.org/10.2172/88",
                ),
                "https://www.osti.gov/biblio/88": FakeResponse(
                    200, {"content-type": "text/html"}, html,
                    "https://www.osti.gov/biblio/88",
                ),
            }
            paf._http_get = make_router(table)

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "probe_only")
            self.assertEqual(
                attempt["pdf_url"], "https://www.osti.gov/biblio/88.pdf",
            )
            self.assertEqual(
                attempt.get("pdf_url_source"), "landing_page_link",
            )

    def test_non_osti_doi_does_not_query_api(self):
        # An AGU row must never produce a request to www.osti.gov.
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.1029/2023ja031603")])

            calls: list[str] = []
            table = {
                "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023ja031603": FakeResponse(
                    200, {"content-type": "text/html"},
                    b"<html></html>",
                    "https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023ja031603",
                ),
            }
            base = make_router(table)

            def recording(url, **kw):
                calls.append(url)
                return base(url, **kw)

            paf._http_get = recording

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=False,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertFalse(
                any("osti.gov" in u for u in calls),
                f"non-OSTI DOI must not hit osti.gov; got {calls}",
            )

    def test_off_host_pdf_redirect_still_rejected(self):
        # The OSTI API points us at a same-host PDF, but a redirect chain
        # takes the final response off osti.gov -- the existing safety rail
        # must still reject the download.
        off_host_pdf = "https://other-host.example/file.pdf"
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_row("a", "10.2172/12345")])

            table = {
                self.API_URL: FakeResponse(
                    200, {"content-type": "application/json"},
                    self._api_body(), self.API_URL,
                ),
                "https://doi.org/10.2172/12345": FakeResponse(
                    302,
                    {"location": self.LANDING, "content-type": "text/html"},
                    b"", "https://doi.org/10.2172/12345",
                ),
                self.LANDING: FakeResponse(
                    200, {"content-type": "text/html; charset=utf-8"},
                    b"<html></html>",
                    self.LANDING,
                ),
                self.PDF_URL: FakeResponse(
                    302,
                    {"location": off_host_pdf, "content-type": "text/html"},
                    b"", self.PDF_URL,
                ),
                off_host_pdf: FakeResponse(
                    200, {"content-type": "application/pdf"},
                    b"%PDF-1.4 off-host", off_host_pdf,
                ),
            }
            paf._http_get = make_router(table)

            paf.run_probe(
                store=store, limit=10, email="r@example.edu",
                year_min=None, year_max=None, download=True,
                per_request_pause=0.0, http_timeout=5.0,
            )

            self.assertEqual(list((store / "papers").glob("*/paper.pdf")), [])
            attempt = json.loads(
                (store / "authorized_attempts" / "a.json").read_text()
            )
            self.assertEqual(attempt["last_result"], "rejected_not_pdf")
            self.assertEqual(
                attempt.get("error"), "pdf_final_url_off_publisher_host",
            )


if __name__ == "__main__":
    unittest.main()
