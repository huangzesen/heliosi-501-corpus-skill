"""Tests for scripts/enrich_acquisition_identifiers.py.

No network. The resolver argument to :func:`run_enrichment` is injected
as a callable, and the lower-level HTTP layer is exercised via
``http_get_json`` and ``urlopen`` seams. The ADS token never appears in
any assertion fixture -- we either use mocks or a dummy token value, and
we verify it does not leak into summaries, attempts, or run logs.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "enrich_acquisition_identifiers.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("enrich_acquisition_identifiers", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


enr = _load_module()


def _no_id_row(cid: str, bibcode: str, **overrides) -> dict:
    row = {
        "candidate_id": cid,
        "cell": "P-test",
        "source": "ads",
        "title": f"title for {cid}",
        "year": 1965,
        "doi": None,
        "arxiv_id": None,
        "bibcode": bibcode,
        "corpus_status": "new_candidate",
        "preferred_identifier": None,
        "identifier_kind": "bibcode_only",
        "priority": 90,
        "status": "no_supported_identifier",
        "notes": "",
        "queued_at_utc": "2026-05-20T12:00:00Z",
    }
    row.update(overrides)
    return row


def _pending_row(cid: str, identifier: str, kind: str = "doi") -> dict:
    return {
        "candidate_id": cid,
        "cell": "P-test",
        "source": "ads",
        "title": f"title for {cid}",
        "year": 1965,
        "doi": identifier if kind == "doi" else None,
        "arxiv_id": identifier if kind == "arxiv" else None,
        "bibcode": None,
        "corpus_status": "new_candidate",
        "preferred_identifier": identifier if kind == "doi" else f"arXiv:{identifier}",
        "identifier_kind": kind,
        "priority": 10 if kind == "doi" else 20,
        "status": "pending",
        "notes": "",
        "queued_at_utc": "2026-05-20T12:00:00Z",
    }


def _seed_queue(store: Path, rows: list[dict]) -> None:
    store.mkdir(parents=True, exist_ok=True)
    with (store / "queue.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------

class TestParseAdsResponse(unittest.TestCase):
    def test_extracts_doi_first(self):
        payload = {
            "response": {
                "docs": [
                    {
                        "bibcode": "1958IAUS....6..284A",
                        "doi": ["10.1017/S0074180900237856"],
                        "identifier": ["arXiv:9901.00001"],
                        "title": ["Interplanetary Magnetic Field"],
                    }
                ]
            }
        }
        out = enr.parse_ads_response(payload)
        self.assertEqual(out["doi"], "10.1017/s0074180900237856")
        # arXiv id is still extracted but the row promoter prefers DOI.
        self.assertEqual(out["arxiv_id"], "9901.00001")
        self.assertIsNotNone(out["raw_doc"])

    def test_extracts_arxiv_when_no_doi(self):
        payload = {
            "response": {
                "docs": [
                    {
                        "bibcode": "2020arXiv200101234X",
                        "doi": [],
                        "identifier": ["arXiv:2001.01234", "2020arXiv200101234X"],
                    }
                ]
            }
        }
        out = enr.parse_ads_response(payload)
        self.assertIsNone(out["doi"])
        self.assertEqual(out["arxiv_id"], "2001.01234")

    def test_no_docs(self):
        out = enr.parse_ads_response({"response": {"docs": []}})
        self.assertIsNone(out["doi"])
        self.assertIsNone(out["arxiv_id"])
        self.assertIsNone(out["raw_doc"])

    def test_empty_payload(self):
        out = enr.parse_ads_response({})
        self.assertEqual(out, {"doi": None, "arxiv_id": None, "raw_doc": None})


class TestNormalizeHelpers(unittest.TestCase):
    def test_normalize_doi_strips_resolver_prefix(self):
        self.assertEqual(
            enr.normalize_doi("https://doi.org/10.1017/S0074180900237856"),
            "10.1017/s0074180900237856",
        )
        self.assertIsNone(enr.normalize_doi("not-a-doi"))

    def test_normalize_arxiv_id_new_and_old(self):
        self.assertEqual(enr.normalize_arxiv_id("arXiv:2301.01234v2"), "2301.01234")
        self.assertEqual(enr.normalize_arxiv_id("astro-ph/0701123"), "astro-ph/0701123")
        self.assertIsNone(enr.normalize_arxiv_id("2020ApJ...123A"))


class TestBuildAdsQueryUrl(unittest.TestCase):
    def test_url_has_expected_pieces(self):
        url = enr.build_ads_query_url("1958IAUS....6..284A")
        self.assertTrue(url.startswith(enr.ADS_SEARCH_URL + "?"))
        self.assertIn("q=bibcode%3A%221958IAUS", url)
        self.assertIn("fl=", url)
        self.assertIn("rows=1", url)


# ---------------------------------------------------------------------------
# Token isolation
# ---------------------------------------------------------------------------

class TestResolveToken(unittest.TestCase):
    def test_token_file_wins_over_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            tf = Path(tmp) / "tok"
            tf.write_text("from-file\n")
            got = enr.resolve_token(tf, env={"ADS_API_TOKEN": "from-env"})
            self.assertEqual(got, "from-file")


    def test_json_token_file_ads_api_token_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            tf = Path(tmp) / "ads.json"
            tf.write_text(json.dumps({"ADS_API_TOKEN": "from-json", "source": "test"}))
            got = enr.resolve_token(tf, env={"ADS_API_TOKEN": "from-env"})
            self.assertEqual(got, "from-json")

    def test_json_token_file_common_token_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            tf = Path(tmp) / "ads.json"
            tf.write_text(json.dumps({"token": "from-common-key"}))
            got = enr.resolve_token(tf, env={})
            self.assertEqual(got, "from-common-key")

    def test_unknown_json_token_file_is_not_used_as_bearer_blob(self):
        with tempfile.TemporaryDirectory() as tmp:
            tf = Path(tmp) / "ads.json"
            tf.write_text(json.dumps({"source": "test", "stored_at": "now"}))
            self.assertIsNone(enr.resolve_token(tf, env={}))

    def test_env_fallback(self):
        got = enr.resolve_token(None, env={"NASA_ADS_TOKEN": "env-token"})
        self.assertEqual(got, "env-token")

    def test_missing_token(self):
        self.assertIsNone(enr.resolve_token(None, env={}))

    def test_token_header_not_logged_in_url(self):
        # The URL builder must NOT embed the token.
        url = enr.build_ads_query_url("1958IAUS....6..284A")
        self.assertNotIn("Bearer", url)
        self.assertNotIn("Authorization", url)


# ---------------------------------------------------------------------------
# Row selection
# ---------------------------------------------------------------------------

class TestSelectEnrichCandidates(unittest.TestCase):
    def test_picks_only_no_id_bibcode_only_rows(self):
        rows = [
            _no_id_row("a", "1958A"),
            _pending_row("b", "10.1/b"),
            _no_id_row("c", "1969C"),
            # bibcode_only but somehow already pending -- skipped
            {**_no_id_row("d", "1971D"), "status": "pending"},
            # no bibcode -- skipped
            {**_no_id_row("e", "1971E"), "bibcode": None},
        ]
        picked = enr.select_enrich_candidates(rows)
        self.assertEqual([r["candidate_id"] for r in picked], ["a", "c"])

    def test_limit_caps_selection(self):
        rows = [_no_id_row(f"r{i}", f"19{60 + i}X") for i in range(5)]
        picked = enr.select_enrich_candidates(rows, limit=2)
        self.assertEqual(len(picked), 2)

    def test_candidate_id_filter(self):
        rows = [_no_id_row(f"r{i}", f"19{60 + i}X") for i in range(5)]
        picked = enr.select_enrich_candidates(rows, only_candidate_ids={"r1", "r3"})
        self.assertEqual([r["candidate_id"] for r in picked], ["r1", "r3"])


# ---------------------------------------------------------------------------
# Row promotion
# ---------------------------------------------------------------------------

class TestPromoteRow(unittest.TestCase):
    def test_doi_promotion(self):
        row = _no_id_row("a", "1958A")
        promoted, note = enr.promote_row(
            row,
            {"doi": "10.1/x", "arxiv_id": "1234.5678", "raw_doc": {}},
            run_id="run-1",
        )
        self.assertTrue(promoted)
        self.assertEqual(row["doi"], "10.1/x")
        self.assertEqual(row["preferred_identifier"], "10.1/x")
        self.assertEqual(row["identifier_kind"], "doi")
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["priority"], enr.PRIORITY_DOI)
        self.assertIn("ads-resolved-doi:run-1", row["notes"])
        self.assertEqual(note, "ads-resolved-doi:run-1")

    def test_arxiv_promotion(self):
        row = _no_id_row("a", "1958A")
        promoted, note = enr.promote_row(
            row,
            {"doi": None, "arxiv_id": "2001.01234", "raw_doc": {}},
            run_id="run-1",
        )
        self.assertTrue(promoted)
        self.assertEqual(row["arxiv_id"], "2001.01234")
        self.assertEqual(row["preferred_identifier"], "arXiv:2001.01234")
        self.assertEqual(row["identifier_kind"], "arxiv")
        self.assertEqual(row["status"], "pending")
        self.assertEqual(row["priority"], enr.PRIORITY_ARXIV)
        self.assertIn("ads-resolved-arxiv:run-1", row["notes"])
        self.assertEqual(note, "ads-resolved-arxiv:run-1")

    def test_no_ads_hit_leaves_row(self):
        row = _no_id_row("a", "1958A")
        promoted, note = enr.promote_row(
            row,
            {"doi": None, "arxiv_id": None, "raw_doc": None},
            run_id="run-1",
        )
        self.assertFalse(promoted)
        self.assertEqual(note, "no_ads_hit")
        self.assertEqual(row["status"], "no_supported_identifier")
        self.assertEqual(row["identifier_kind"], "bibcode_only")

    def test_ads_hit_but_no_ids(self):
        row = _no_id_row("a", "1958A")
        promoted, note = enr.promote_row(
            row,
            {"doi": None, "arxiv_id": None, "raw_doc": {"bibcode": "1958A"}},
            run_id="run-1",
        )
        self.assertFalse(promoted)
        self.assertEqual(note, "no_doi_no_arxiv")
        self.assertEqual(row["status"], "no_supported_identifier")


# ---------------------------------------------------------------------------
# Full driver -- DOI / arXiv / nothing / dry-run / candidate filter
# ---------------------------------------------------------------------------

def _stub_resolver(responses: dict) -> "callable":
    """Build a resolver that returns a fixture-keyed response."""
    def resolve(bibcode: str) -> dict:
        return responses.get(bibcode, {"doi": None, "arxiv_id": None, "raw_doc": None})
    return resolve


class TestRunEnrichment(unittest.TestCase):
    def test_doi_path_promotes_and_rewrites_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [
                _no_id_row("a", "1958A"),
                _no_id_row("b", "1969B"),
                _pending_row("p", "10.1/p"),
            ])
            resolver = _stub_resolver({
                "1958A": {"doi": "10.1/found-a", "arxiv_id": None, "raw_doc": {}},
                "1969B": {"doi": None, "arxiv_id": None, "raw_doc": None},
            })
            summary = enr.run_enrichment(
                store=store,
                resolver=resolver,
                request_pause_seconds=0.0,
                sleep=lambda _s: None,
            )
            self.assertEqual(summary["selected"], 2)
            self.assertEqual(summary["by_outcome"].get("ads-resolved-doi:" + summary["run_id"]), 1)
            self.assertEqual(summary["by_outcome"].get("no_ads_hit"), 1)

            rows = enr.read_queue(store / "queue.jsonl")
            by_id = {r["candidate_id"]: r for r in rows}
            self.assertEqual(by_id["a"]["status"], "pending")
            self.assertEqual(by_id["a"]["doi"], "10.1/found-a")
            self.assertEqual(by_id["a"]["preferred_identifier"], "10.1/found-a")
            self.assertEqual(by_id["a"]["identifier_kind"], "doi")
            # Unchanged rows stay as they were.
            self.assertEqual(by_id["b"]["status"], "no_supported_identifier")
            self.assertEqual(by_id["p"]["status"], "pending")

            attempt = json.loads((store / "enrichment_attempts" / "a.json").read_text())
            self.assertTrue(attempt["promoted"])
            self.assertEqual(attempt["resolved_doi"], "10.1/found-a")
            # Token must never appear anywhere in persisted artefacts.
            blob = json.dumps(attempt).lower()
            self.assertNotIn("bearer", blob)
            self.assertNotIn("authorization", blob)
            run_dir = store / "runs" / summary["run_id"]
            summary_text = (run_dir / "summary.json").read_text().lower()
            log_text = (run_dir / "log.txt").read_text().lower()
            for artefact_text in (summary_text, log_text):
                self.assertNotIn("bearer", artefact_text)
                self.assertNotIn("authorization", artefact_text)
                self.assertNotIn("do-not-log", artefact_text)

            # CSV mirror was written.
            self.assertTrue((store / "queue.csv").exists())

    def test_arxiv_path_promotes(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "2020A")])
            resolver = _stub_resolver({
                "2020A": {"doi": None, "arxiv_id": "2001.01234", "raw_doc": {}},
            })
            summary = enr.run_enrichment(
                store=store, resolver=resolver,
                request_pause_seconds=0.0, sleep=lambda _s: None,
            )
            rows = enr.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "pending")
            self.assertEqual(rows[0]["identifier_kind"], "arxiv")
            self.assertEqual(rows[0]["arxiv_id"], "2001.01234")
            self.assertEqual(rows[0]["preferred_identifier"], "arXiv:2001.01234")
            self.assertTrue(
                any(k.startswith("ads-resolved-arxiv:") for k in summary["by_outcome"])
            )

    def test_no_identifier_leaves_row_and_records_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1969A")])
            resolver = _stub_resolver({
                "1969A": {"doi": None, "arxiv_id": None, "raw_doc": None},
            })
            summary = enr.run_enrichment(
                store=store, resolver=resolver,
                request_pause_seconds=0.0, sleep=lambda _s: None,
            )
            self.assertEqual(summary["by_outcome"].get("no_ads_hit"), 1)
            rows = enr.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "no_supported_identifier")
            attempt = json.loads((store / "enrichment_attempts" / "a.json").read_text())
            self.assertFalse(attempt["promoted"])
            self.assertEqual(attempt["outcome"], "no_ads_hit")

    def test_dry_run_does_not_mutate_queue_or_write_attempts(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1958A")])
            resolver = _stub_resolver({
                "1958A": {"doi": "10.1/x", "arxiv_id": None, "raw_doc": {}},
            })
            summary = enr.run_enrichment(
                store=store, resolver=resolver, dry_run=True,
                request_pause_seconds=0.0, sleep=lambda _s: None,
            )
            self.assertEqual(summary["selected"], 1)
            # Queue unchanged.
            rows = enr.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "no_supported_identifier")
            self.assertIsNone(rows[0]["doi"])
            # No attempt file persisted.
            self.assertFalse((store / "enrichment_attempts" / "a.json").exists())
            # But the run summary is still produced for visibility.
            self.assertEqual(summary["selected"], 1)

    def test_candidate_id_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [
                _no_id_row("a", "1958A"),
                _no_id_row("b", "1969B"),
                _no_id_row("c", "1971C"),
            ])
            resolver = _stub_resolver({
                "1958A": {"doi": "10.1/a", "arxiv_id": None, "raw_doc": {}},
                "1969B": {"doi": "10.1/b", "arxiv_id": None, "raw_doc": {}},
                "1971C": {"doi": "10.1/c", "arxiv_id": None, "raw_doc": {}},
            })
            summary = enr.run_enrichment(
                store=store, resolver=resolver,
                only_candidate_ids={"b"},
                request_pause_seconds=0.0, sleep=lambda _s: None,
            )
            self.assertEqual(summary["selected"], 1)
            rows = enr.read_queue(store / "queue.jsonl")
            by_id = {r["candidate_id"]: r for r in rows}
            self.assertEqual(by_id["b"]["status"], "pending")
            self.assertEqual(by_id["a"]["status"], "no_supported_identifier")
            self.assertEqual(by_id["c"]["status"], "no_supported_identifier")

    def test_http_error_records_attempt_without_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1958A")])

            def boom(_bibcode: str) -> dict:
                raise enr.AdsHTTPError("ADS HTTP 503 after 3/3 attempts")

            summary = enr.run_enrichment(
                store=store, resolver=boom,
                request_pause_seconds=0.0, sleep=lambda _s: None,
            )
            self.assertEqual(summary["by_outcome"].get("http_error"), 1)
            attempt = json.loads((store / "enrichment_attempts" / "a.json").read_text())
            self.assertEqual(attempt["outcome"], "http_error")
            self.assertFalse(attempt["promoted"])
            self.assertIn("503", attempt["http_error"])
            # Row unchanged.
            rows = enr.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "no_supported_identifier")


    def test_recent_attempt_skip_is_applied_in_driver(self):
        import datetime as dt

        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1958A")])
            attempt_dir = store / "enrichment_attempts"
            attempt_dir.mkdir(parents=True)
            (attempt_dir / "a.json").write_text(json.dumps({
                "attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "outcome": "no_doi_no_arxiv",
            }))

            calls = {"n": 0}
            def resolver(_bibcode: str) -> dict:
                calls["n"] += 1
                return {"doi": "10.1/should-not-call", "arxiv_id": None, "raw_doc": {}}

            summary = enr.run_enrichment(
                store=store,
                resolver=resolver,
                retry_after_seconds=3600,
                request_pause_seconds=0.0,
                sleep=lambda _s: None,
            )
            self.assertEqual(calls["n"], 0)
            self.assertEqual(summary["by_outcome"].get("skipped_recent_attempt"), 1)
            rows = enr.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "no_supported_identifier")

    def test_resumability_after_attempt_written_before_queue_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1958A")])
            # Simulate a crash after a promoted=true attempt was written but
            # before queue.jsonl was rewritten; rerun should converge.
            enr.write_attempt(store, "a", {
                "schema_version": enr.SCHEMA_VERSION,
                "candidate_id": "a",
                "bibcode": "1958A",
                "attempted_at_utc": "2026-05-20T00:00:00Z",
                "outcome": "ads-resolved-doi:old-run",
                "promoted": True,
                "resolved_doi": "10.1/old",
            })
            summary = enr.run_enrichment(
                store=store,
                resolver=_stub_resolver({
                    "1958A": {"doi": "10.1/found", "arxiv_id": None, "raw_doc": {}},
                }),
                request_pause_seconds=0.0,
                sleep=lambda _s: None,
            )
            rows = enr.read_queue(store / "queue.jsonl")
            self.assertEqual(rows[0]["status"], "pending")
            self.assertEqual(rows[0]["doi"], "10.1/found")
            attempt = json.loads((store / "enrichment_attempts" / "a.json").read_text())
            self.assertEqual(attempt["run_id"], summary["run_id"])
            self.assertEqual(attempt["resolved_doi"], "10.1/found")

    def test_summary_artefact_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1958A")])
            resolver = _stub_resolver({
                "1958A": {"doi": "10.1/x", "arxiv_id": None, "raw_doc": {}},
            })
            summary = enr.run_enrichment(
                store=store, resolver=resolver,
                request_pause_seconds=0.0, sleep=lambda _s: None,
            )
            run_dir = store / "runs" / summary["run_id"]
            self.assertTrue(run_dir.is_dir())
            self.assertTrue(run_dir.name.endswith("-enrich"))
            written = json.loads((run_dir / "summary.json").read_text())
            self.assertEqual(written["run_id"], summary["run_id"])
            self.assertEqual(written["selected"], 1)


# ---------------------------------------------------------------------------
# HTTP retry seam
# ---------------------------------------------------------------------------

class TestHttpGetJsonRetry(unittest.TestCase):
    def test_retries_on_transient_then_succeeds(self):
        import urllib.error

        calls = {"n": 0}

        class _OkResp:
            def __init__(self, data: bytes):
                self._data = data
            def read(self) -> bytes:
                return self._data
            def __enter__(self):
                return self
            def __exit__(self, *exc):
                return False

        def fake_urlopen(req, timeout):
            calls["n"] += 1
            if calls["n"] == 1:
                raise urllib.error.HTTPError(
                    req.full_url, 503, "service unavailable", hdrs=None, fp=None
                )
            return _OkResp(b'{"response": {"docs": []}}')

        sleeps: list[float] = []
        out = enr._http_get_json(
            "https://example.invalid/q",
            {"Authorization": "Bearer DO-NOT-LOG"},
            timeout=1.0,
            max_retries=2,
            retry_base_seconds=0.5,
            sleep=sleeps.append,
            urlopen=fake_urlopen,
        )
        self.assertEqual(out, {"response": {"docs": []}})
        self.assertEqual(calls["n"], 2)
        self.assertEqual(sleeps, [0.5])


    def test_make_resolver_wires_headers_and_parses_payload(self):
        class _OkResp:
            def read(self) -> bytes:
                return b'{"response": {"docs": [{"doi": ["10.1/ABC"], "identifier": []}]}}'
            def __enter__(self):
                return self
            def __exit__(self, *exc):
                return False

        seen = {}
        def fake_urlopen(req, timeout):
            seen["url"] = req.full_url
            seen["auth"] = req.headers.get("Authorization")
            seen["timeout"] = timeout
            return _OkResp()

        def fake_get_json(url, headers, *, timeout, max_retries, retry_base_seconds):
            return enr._http_get_json(
                url,
                headers,
                timeout=timeout,
                max_retries=max_retries,
                retry_base_seconds=retry_base_seconds,
                sleep=lambda _s: None,
                urlopen=fake_urlopen,
            )

        resolver = enr.make_resolver(
            "DO-NOT-LOG",
            timeout=7.0,
            max_retries=0,
            retry_base_seconds=0.0,
            http_get_json=fake_get_json,
        )
        out = resolver("1958IAUS....6..284A")
        self.assertEqual(out["doi"], "10.1/abc")
        self.assertIn("bibcode", seen["url"])
        self.assertEqual(seen["auth"], "Bearer DO-NOT-LOG")
        self.assertEqual(seen["timeout"], 7.0)

    def test_exhausts_retries_and_raises_without_token_leak(self):
        import urllib.error

        def always_503(req, timeout):
            raise urllib.error.HTTPError(
                req.full_url, 503, "service unavailable", hdrs=None, fp=None
            )

        with self.assertRaises(enr.AdsHTTPError) as ctx:
            enr._http_get_json(
                "https://example.invalid/q",
                {"Authorization": "Bearer DO-NOT-LOG"},
                timeout=1.0,
                max_retries=1,
                retry_base_seconds=0.0,
                sleep=lambda _s: None,
                urlopen=always_503,
            )
        self.assertNotIn("DO-NOT-LOG", str(ctx.exception))
        self.assertIn("503", str(ctx.exception))


# ---------------------------------------------------------------------------
# CLI plumbing
# ---------------------------------------------------------------------------

class TestCliMain(unittest.TestCase):

    def test_main_dry_run_without_token_reports_distinct_offline_outcome(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Path(tmp) / "store"
            _seed_queue(store, [_no_id_row("a", "1958A")])
            rc = enr.main(["--store", str(store), "--dry-run", "--limit", "1", "--request-pause-seconds", "0"])
            self.assertEqual(rc, 0)
            run_dirs = list((store / "runs").glob("*-enrich"))
            self.assertEqual(len(run_dirs), 1)
            summary = json.loads((run_dirs[0] / "summary.json").read_text())
            self.assertEqual(summary["by_outcome"].get("dry_run_no_token"), 1)
            self.assertFalse((store / "enrichment_attempts" / "a.json").exists())


# ---------------------------------------------------------------------------
# Recent-attempt skipping
# ---------------------------------------------------------------------------

class TestRetryAfterSkipping(unittest.TestCase):
    def test_recent_attempt_is_skipped(self):
        import datetime as dt
        prior = {"attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        self.assertTrue(
            enr.should_skip_due_to_recent_attempt(
                prior, retry_after_seconds=3600,
                now_utc=dt.datetime.now(dt.timezone.utc),
            )
        )

    def test_old_attempt_not_skipped(self):
        import datetime as dt
        prior = {"attempted_at_utc": "2020-01-01T00:00:00Z"}
        self.assertFalse(
            enr.should_skip_due_to_recent_attempt(
                prior, retry_after_seconds=3600,
                now_utc=dt.datetime.now(dt.timezone.utc),
            )
        )

    def test_no_retry_after_means_no_skip(self):
        import datetime as dt
        prior = {"attempted_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        self.assertFalse(
            enr.should_skip_due_to_recent_attempt(
                prior, retry_after_seconds=None,
                now_utc=dt.datetime.now(dt.timezone.utc),
            )
        )


if __name__ == "__main__":
    unittest.main()
