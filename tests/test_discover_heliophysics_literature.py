"""Tests for scripts/discover_heliophysics_literature.py.

Stdlib-only unittest module. No network calls: every test exercises the
script's pure functions (query-URL builders, backend parsers, normaliser,
dedupe, classifier) or runs the CLI in --dry-run mode against the fixture
files under ``tests/fixtures/discovery/``.

The script ships as an open-ended literature discovery frontier; this test
module pins its dedupe/classification/query-building contracts so future
edits to backends or taxonomy cannot silently regress the seed pipeline.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
import urllib.parse
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "discover_heliophysics_literature.py"
FIXTURE_DIR = BUNDLE / "tests" / "fixtures" / "discovery"
JSONL_FIXTURE = FIXTURE_DIR / "sample_records.jsonl"
ARXIV_FIXTURE = FIXTURE_DIR / "arxiv_sample.xml"
OPENALEX_FIXTURE = FIXTURE_DIR / "openalex_sample.json"


def _load_module():
    """Import the script as a module so we can call its functions directly."""
    spec = importlib.util.spec_from_file_location(
        "discover_heliophysics_literature", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


discover = _load_module()


def _run_cli(*args, env_extra=None):
    cmd = [sys.executable, str(SCRIPT), *args]
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        cmd,
        cwd=str(BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestQueryUrlBuilders(unittest.TestCase):
    """Query-URL construction is a pure function. Pin its surface."""

    def test_arxiv_url_encodes_query_and_caps_max_results(self):
        url = discover.build_arxiv_url("solar wind", max_results=5)
        self.assertTrue(url.startswith("https://export.arxiv.org/api/query?"))
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["search_query"], "all:solar wind")
        self.assertEqual(parsed["max_results"], "5")
        self.assertEqual(parsed["sortBy"], "submittedDate")
        self.assertEqual(parsed["sortOrder"], "descending")

    def test_openalex_url_caps_per_page_at_200(self):
        url = discover.build_openalex_url("alfvenic turbulence", max_results=10_000)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["search"], "alfvenic turbulence")
        self.assertEqual(parsed["per-page"], "200")
        self.assertEqual(parsed["page"], "1")

    def test_crossref_url_uses_rows_param(self):
        url = discover.build_crossref_url("CME reconnection", max_results=50)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["query"], "CME reconnection")
        self.assertEqual(parsed["rows"], "50")
        self.assertEqual(parsed["offset"], "0")

    def test_ads_url_includes_fl_for_required_fields(self):
        url = discover.build_ads_url("Parker Solar Probe", max_results=25)
        self.assertIn("api.adsabs.harvard.edu/v1/search/query", url)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["q"], "Parker Solar Probe")
        self.assertEqual(parsed["rows"], "25")
        # The script must always request enough fields to populate the
        # normalised schema (bibcode + DOI + author + abstract + identifier).
        for needle in ("bibcode", "doi", "abstract", "identifier"):
            self.assertIn(needle, parsed["fl"])


class TestNormaliseHelpers(unittest.TestCase):
    def test_normalize_doi_strips_resolver_and_lowercases(self):
        self.assertEqual(
            discover.normalize_doi("https://doi.org/10.1234/ABCD"),
            "10.1234/abcd",
        )
        self.assertEqual(discover.normalize_doi("doi:10.5678/efgh"), "10.5678/efgh")
        self.assertIsNone(discover.normalize_doi(None))
        self.assertIsNone(discover.normalize_doi(""))

    def test_normalize_arxiv_id_handles_v_suffix_and_prefix(self):
        self.assertEqual(
            discover.normalize_arxiv_id("arXiv:2401.00001v3"),
            "2401.00001",
        )
        self.assertEqual(
            discover.normalize_arxiv_id("https://arxiv.org/abs/2403.04567"),
            "2403.04567",
        )
        self.assertEqual(
            discover.normalize_arxiv_id("astro-ph/0701234v2"),
            "astro-ph/0701234",
        )
        self.assertIsNone(discover.normalize_arxiv_id("not-an-arxiv-id"))
        self.assertIsNone(discover.normalize_arxiv_id(None))

    def test_normalize_title_is_case_punct_accent_insensitive(self):
        a = discover.normalize_title("Alfvén Waves, Switchbacks!")
        b = discover.normalize_title("alfven waves switchbacks")
        self.assertEqual(a, b)


class TestClassification(unittest.TestCase):
    def test_classifier_returns_sorted_unique_tags(self):
        tags = discover.classify_topics(
            title="Parker Solar Probe switchbacks and turbulence",
            abstract="We use PSP and Solar Orbiter to study Alfvénic turbulence.",
        )
        self.assertEqual(tags, sorted(set(tags)))
        for needle in ("parker-solar-probe", "solar-orbiter", "switchbacks", "turbulence", "alfven-waves"):
            self.assertIn(needle, tags)

    def test_classifier_empty_for_off_topic_text(self):
        self.assertEqual(
            discover.classify_topics("A study of lattice quantum chromodynamics", "QCD lattice."),
            [],
        )

    def test_classifier_is_robust_to_none_inputs(self):
        self.assertEqual(discover.classify_topics(None, None), [])


class TestDedupeKey(unittest.TestCase):
    def test_doi_wins_over_arxiv(self):
        rec = {"doi": "10.1234/X", "arxiv_id": "2401.00001", "title": "T", "year": 2024}
        self.assertEqual(discover.dedupe_key(rec), "doi:10.1234/x")

    def test_arxiv_used_when_no_doi(self):
        rec = {"doi": None, "arxiv_id": "arXiv:2403.04567v2", "title": "T", "year": 2024}
        self.assertEqual(discover.dedupe_key(rec), "arxiv:2403.04567")

    def test_bibcode_used_when_no_doi_or_arxiv(self):
        rec = {"doi": None, "arxiv_id": None, "bibcode": "2023ApJ...999..123X", "title": "T", "year": 2023}
        self.assertEqual(discover.dedupe_key(rec), "bibcode:2023apj...999..123x")

    def test_title_year_fallback_collides_on_normalised_titles(self):
        a = discover.dedupe_key({"title": "Alfvén Waves!", "year": 2024})
        b = discover.dedupe_key({"title": "alfven waves", "year": 2024})
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("title:"))


class TestParsers(unittest.TestCase):
    def test_parse_arxiv_atom_round_trips_doi_and_arxiv_id(self):
        records = discover.parse_arxiv_atom(ARXIV_FIXTURE.read_bytes())
        self.assertEqual(len(records), 2)
        first = records[0]
        self.assertEqual(first["source"], "arxiv")
        self.assertEqual(first["arxiv_id"], "2401.00001")
        self.assertEqual(first["doi"], "10.1234/psp.switchback.2024")
        self.assertEqual(first["year"], 2024)
        self.assertIn("A. Author", first["authors"])
        self.assertTrue(first["title"].startswith("Parker Solar Probe"))

    def test_parse_openalex_json_handles_inverted_abstract(self):
        payload = json.loads(OPENALEX_FIXTURE.read_text())
        records = discover.parse_openalex_json(payload)
        self.assertEqual(len(records), 2)
        psp = records[0]
        self.assertEqual(psp["source"], "openalex")
        # OpenAlex DOIs include the resolver prefix; normaliser should strip it.
        self.assertEqual(psp["doi"], "10.1234/psp.switchback.2024")
        self.assertEqual(psp["year"], 2024)
        # Inverted abstract must be reconstructed in word-position order.
        self.assertEqual(psp["abstract"], "Parker Solar Probe switchbacks")


class TestDedupeIntegration(unittest.TestCase):
    """End-to-end dedupe via run_discovery in dry-run mode."""

    def test_fixture_dedupes_9_raw_to_7(self):
        candidates, summary = discover.run_discovery(
            queries=discover.DEFAULT_QUERIES,
            backends=["arxiv", "openalex"],
            max_results=10,
            live=False,
            fixture_path=JSONL_FIXTURE,
            timeout=5.0,
            page_pause_seconds=0,
            ads_token=None,
            now_iso="2026-05-19T00:00:00Z",
        )
        self.assertEqual(summary["raw_candidate_count"], 9)
        self.assertEqual(summary["deduped_candidate_count"], 7)
        self.assertEqual(len(candidates), 7)
        # All dedupe keys must be unique.
        keys = [c["id"] for c in candidates]
        self.assertEqual(len(set(keys)), 7)
        # The two backends with duplicates (DOI + arXiv + bibcode collisions)
        # collapse to one record each; surviving keys should include exactly
        # the deterministic strings below.
        self.assertIn("doi:10.1234/psp.switchback.2024", keys)
        self.assertIn("arxiv:2403.04567", keys)
        self.assertIn("bibcode:2023apj...999..123x", keys)

    def test_dry_run_reports_honest_framing(self):
        _, summary = discover.run_discovery(
            queries=discover.DEFAULT_QUERIES,
            backends=["arxiv", "openalex"],
            max_results=10,
            live=False,
            fixture_path=JSONL_FIXTURE,
            timeout=5.0,
            page_pause_seconds=0,
            ads_token=None,
        )
        self.assertEqual(summary["mode"], "dry-run")
        self.assertIn("frontier", summary["framing"])
        self.assertIn("not a complete survey", summary["framing"])


class TestHttpRetry(unittest.TestCase):
    """Exercise the polite-retry seam in ``_http_get`` without touching network.

    The script accepts ``sleep`` and ``urlopen`` keyword shims so transient
    HTTP failures can be simulated deterministically.
    """

    def test_retries_on_429_and_eventually_succeeds(self):
        import urllib.error
        import io

        sleeps = []

        def fake_sleep(sec):
            sleeps.append(sec)

        calls = {"n": 0}

        class _FakeResp:
            def __init__(self, body):
                self._body = body

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return self._body

        def fake_urlopen(req, timeout=None):
            calls["n"] += 1
            if calls["n"] < 3:
                raise urllib.error.HTTPError(
                    req.full_url, 429, "Too Many Requests", hdrs=None, fp=io.BytesIO(b"")
                )
            return _FakeResp(b"OK")

        body = discover._http_get(
            "https://example.invalid/x",
            timeout=1.0,
            max_retries=3,
            retry_base_seconds=0.25,
            sleep=fake_sleep,
            urlopen=fake_urlopen,
        )
        self.assertEqual(body, b"OK")
        self.assertEqual(calls["n"], 3)
        # Backoff: sleep before attempts 1 and 2 (not before attempt 0).
        self.assertEqual(sleeps, [0.25, 0.5])

    def test_retry_gives_up_and_raises_http_retry_error(self):
        import urllib.error
        import io

        def fake_sleep(_):
            pass

        def fake_urlopen(req, timeout=None):
            raise urllib.error.HTTPError(
                req.full_url, 503, "Service Unavailable", hdrs=None, fp=io.BytesIO(b"")
            )

        with self.assertRaises(discover._HTTPRetryError):
            discover._http_get(
                "https://example.invalid/x",
                timeout=1.0,
                max_retries=2,
                retry_base_seconds=0.01,
                sleep=fake_sleep,
                urlopen=fake_urlopen,
            )

    def test_non_transient_status_is_not_retried(self):
        import urllib.error
        import io

        calls = {"n": 0}

        def fake_urlopen(req, timeout=None):
            calls["n"] += 1
            raise urllib.error.HTTPError(
                req.full_url, 404, "Not Found", hdrs=None, fp=io.BytesIO(b"")
            )

        with self.assertRaises(discover._HTTPRetryError):
            discover._http_get(
                "https://example.invalid/x",
                timeout=1.0,
                max_retries=5,
                retry_base_seconds=0.01,
                sleep=lambda _: None,
                urlopen=fake_urlopen,
            )
        # 404 is not in the transient set -> exactly one call, no backoff.
        self.assertEqual(calls["n"], 1)


class TestCliBehavior(unittest.TestCase):
    def test_help_advertises_dry_run_default(self):
        rc, out, err = _run_cli("--help")
        self.assertEqual(rc, 0)
        self.assertIn("--dry-run", out)
        self.assertIn("--live", out)
        self.assertIn("NO network", out)

    def test_version_flag(self):
        rc, out, _ = _run_cli("--version")
        self.assertEqual(rc, 0)
        self.assertIn("discover_heliophysics_literature", out)

    def test_queries_only_lists_default_slate(self):
        rc, out, _ = _run_cli("--queries-only")
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["mode"], "dry-run")
        qs = [item["q"] for item in payload["queries"]]
        self.assertIn("PFSS open flux", qs)
        self.assertIn("Parker Solar Probe switchbacks", qs)

    def test_dry_run_emits_jsonl_to_stdout_with_summary_on_stderr(self):
        rc, out, err = _run_cli("--dry-run", "--output", "-")
        self.assertEqual(rc, 0, msg=err)
        lines = [ln for ln in out.splitlines() if ln.strip()]
        self.assertEqual(len(lines), 7)  # deduped from fixture
        first = json.loads(lines[0])
        for required in ("id", "source", "title", "topic_tags", "discovered_at_utc"):
            self.assertIn(required, first)
        # Summary is always written to stderr as JSON.
        summary_line = err.strip().splitlines()[-1]
        summary = json.loads(summary_line)
        self.assertEqual(summary["mode"], "dry-run")
        self.assertEqual(summary["deduped_candidate_count"], 7)

    def test_extra_query_is_appended(self):
        rc, out, _ = _run_cli("--queries-only", "--extra-query", "magnetotail substorm")
        self.assertEqual(rc, 0)
        qs = [item["q"] for item in json.loads(out)["queries"]]
        self.assertEqual(qs[-1], "magnetotail substorm")

    def test_no_arxiv_drops_backend(self):
        rc, out, _ = _run_cli("--queries-only", "--no-arxiv")
        self.assertEqual(rc, 0)
        backends = json.loads(out)["backends"]
        self.assertNotIn("arxiv", backends)
        self.assertIn("openalex", backends)

    def test_enable_ads_in_live_mode_without_token_aborts(self):
        # Strip every ADS-token env var so the script must refuse to run.
        env_extra = {"ADS_API_TOKEN": "", "NASA_ADS_TOKEN": "", "ADS_TOKEN": ""}
        rc, _, err = _run_cli(
            "--live",
            "--enable-ads",
            "--no-arxiv",
            "--no-openalex",
            env_extra=env_extra,
        )
        self.assertEqual(rc, 2)
        self.assertIn("ADS", err)

    def test_enable_ads_dry_run_does_not_require_token(self):
        # Even with --enable-ads, --dry-run must succeed without a token
        # because no network call is issued.
        env_extra = {"ADS_API_TOKEN": "", "NASA_ADS_TOKEN": "", "ADS_TOKEN": ""}
        rc, _, _ = _run_cli("--dry-run", "--enable-ads", env_extra=env_extra)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
