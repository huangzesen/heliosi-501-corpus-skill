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
import shutil
import subprocess
import sys
import tempfile
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
MANIFEST_FIXTURE = FIXTURE_DIR / "sample_manifest.json"


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


class TestYearRangeUrlBuilders(unittest.TestCase):
    """Pin the per-backend integration of ``--year-from`` / ``--year-until``.

    Each URL builder must accept optional ``year_from`` / ``year_until``
    kwargs and translate them into the backend's native year-filter syntax
    without breaking the existing query string. arXiv has no first-class
    year filter, so its URL is unchanged; the year filter is applied
    post-fetch (covered by ``TestArxivYearPostFilter`` below).
    """

    def test_ads_url_appends_year_clause(self):
        url = discover.build_ads_url(
            "solar wind", max_results=10, year_from=1958, year_until=1969
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        # Year clause is appended (not replacing) the user query.
        self.assertIn("solar wind", parsed["q"])
        self.assertIn("year:1958-1969", parsed["q"])

    def test_ads_url_appends_open_ended_year_range(self):
        url = discover.build_ads_url(
            "solar wind", max_results=10, year_from=1990, year_until=None
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertIn("year:1990-", parsed["q"])

        url = discover.build_ads_url(
            "solar wind", max_results=10, year_from=None, year_until=1989
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertIn("year:-1989", parsed["q"])

    def test_ads_url_without_year_kwargs_is_unchanged(self):
        # Backwards compatibility: existing callers pass no year kwargs.
        url = discover.build_ads_url("solar wind", max_results=10)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["q"], "solar wind")
        self.assertNotIn("year:", parsed["q"])

    def test_openalex_url_adds_publication_year_filter(self):
        url = discover.build_openalex_url(
            "alfvenic turbulence",
            max_results=10,
            year_from=2000,
            year_until=2024,
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["search"], "alfvenic turbulence")
        # OpenAlex range syntax: publication_year:YYYY-YYYY.
        self.assertEqual(parsed["filter"], "publication_year:2000-2024")

    def test_openalex_url_open_ended_year_range(self):
        url = discover.build_openalex_url(
            "alfvenic turbulence",
            max_results=10,
            year_from=2010,
            year_until=None,
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["filter"], "publication_year:2010-")

        url = discover.build_openalex_url(
            "alfvenic turbulence",
            max_results=10,
            year_from=None,
            year_until=1989,
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["filter"], "publication_year:-1989")

    def test_openalex_url_without_year_kwargs_omits_filter(self):
        url = discover.build_openalex_url("alfvenic turbulence", max_results=10)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertNotIn("filter", parsed)

    def test_crossref_url_adds_pub_date_filter(self):
        url = discover.build_crossref_url(
            "CME reconnection",
            max_results=10,
            year_from=1970,
            year_until=1989,
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["query"], "CME reconnection")
        self.assertEqual(
            parsed["filter"],
            "from-pub-date:1970-01-01,until-pub-date:1989-12-31",
        )

    def test_crossref_url_open_ended_year_range(self):
        url = discover.build_crossref_url(
            "CME reconnection",
            max_results=10,
            year_from=2010,
            year_until=None,
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["filter"], "from-pub-date:2010-01-01")

        url = discover.build_crossref_url(
            "CME reconnection",
            max_results=10,
            year_from=None,
            year_until=1989,
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["filter"], "until-pub-date:1989-12-31")

    def test_crossref_url_without_year_kwargs_omits_filter(self):
        url = discover.build_crossref_url("CME reconnection", max_results=10)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertNotIn("filter", parsed)

    def test_arxiv_url_is_unchanged_by_year_kwargs(self):
        """arXiv's Atom API has no first-class year filter; the URL builder
        accepts the kwargs for uniformity but produces an identical URL."""
        base = discover.build_arxiv_url("solar wind", max_results=5)
        with_years = discover.build_arxiv_url(
            "solar wind", max_results=5, year_from=2000, year_until=2024
        )
        # Both URLs must agree on every query parameter -- the year filter
        # is applied post-fetch by filter_records_by_year.
        self.assertEqual(
            dict(urllib.parse.parse_qsl(urllib.parse.urlparse(base).query)),
            dict(urllib.parse.parse_qsl(urllib.parse.urlparse(with_years).query)),
        )


class TestYearRangePostFilter(unittest.TestCase):
    """The arXiv backend (and any future backend that lacks a year filter)
    must be filtered post-fetch via ``filter_records_by_year``."""

    def _recs(self):
        return [
            {"title": "old", "year": 1985},
            {"title": "edge-low", "year": 2000},
            {"title": "mid", "year": 2010},
            {"title": "edge-high", "year": 2024},
            {"title": "future", "year": 2026},
            {"title": "no-year", "year": None},
        ]

    def test_filter_keeps_inclusive_range(self):
        out = discover.filter_records_by_year(
            self._recs(), year_from=2000, year_until=2024
        )
        kept_years = sorted(r["year"] for r in out)
        self.assertEqual(kept_years, [2000, 2010, 2024])

    def test_filter_open_ended_year_from_only(self):
        out = discover.filter_records_by_year(
            self._recs(), year_from=2010, year_until=None
        )
        kept_years = sorted(r["year"] for r in out)
        self.assertEqual(kept_years, [2010, 2024, 2026])

    def test_filter_open_ended_year_until_only(self):
        out = discover.filter_records_by_year(
            self._recs(), year_from=None, year_until=1999
        )
        kept_years = sorted(r["year"] for r in out)
        self.assertEqual(kept_years, [1985])

    def test_filter_drops_records_with_unknown_year_when_any_bound_set(self):
        """A record whose year is None cannot be proven to satisfy the bound.
        We DROP it rather than silently keep it; the alternative would be a
        quiet honesty violation when the user asked for a date-bounded
        sample."""
        out = discover.filter_records_by_year(
            self._recs(), year_from=2000, year_until=2024
        )
        self.assertFalse(any(r["year"] is None for r in out))

    def test_filter_passes_through_when_no_bounds(self):
        out = discover.filter_records_by_year(
            self._recs(), year_from=None, year_until=None
        )
        self.assertEqual(out, self._recs())


class TestYearRangeCliValidation(unittest.TestCase):
    """CLI must validate ``--year-from`` / ``--year-until`` integers and
    refuse inverted ranges (from > until)."""

    def test_cli_accepts_year_range_and_passes_through(self):
        rc, out, err = _run_cli(
            "--queries-only", "--year-from", "1958", "--year-until", "1969"
        )
        self.assertEqual(rc, 0, msg=err)
        payload = json.loads(out)
        self.assertEqual(payload["year_from"], 1958)
        self.assertEqual(payload["year_until"], 1969)

    def test_cli_accepts_only_year_from(self):
        rc, out, _ = _run_cli("--queries-only", "--year-from", "2010")
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(payload["year_from"], 2010)
        self.assertIsNone(payload["year_until"])

    def test_cli_rejects_inverted_year_range(self):
        rc, _, err = _run_cli(
            "--queries-only", "--year-from", "2020", "--year-until", "2010"
        )
        self.assertNotEqual(rc, 0)
        self.assertIn("year-from", err.lower())

    def test_cli_rejects_non_integer_year(self):
        rc, _, err = _run_cli("--queries-only", "--year-from", "not-a-year")
        self.assertNotEqual(rc, 0)
        # argparse handles the integer parse; the error message must mention
        # the offending flag.
        self.assertIn("year-from", err.lower())

    def test_cli_records_year_range_in_run_metadata(self):
        tmp = Path(tempfile.mkdtemp(prefix="hsi-year-meta-"))
        try:
            run_dir = tmp / "run-y"
            rc, _, err = _run_cli(
                "--dry-run",
                "--run-dir", str(run_dir),
                "--no-corpus-manifest",
                "--year-from", "1958",
                "--year-until", "1989",
            )
            self.assertEqual(rc, 0, msg=err)
            meta = json.loads((run_dir / "run_metadata.json").read_text())
            self.assertEqual(meta["cli_args"]["year_from"], 1958)
            self.assertEqual(meta["cli_args"]["year_until"], 1989)
            # The human report must surface the range too so an auditor can
            # recover the decade slice from the bundle alone.
            report = (run_dir / "run_report.md").read_text()
            self.assertIn("1958", report)
            self.assertIn("1989", report)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestMailtoPolitePool(unittest.TestCase):
    """Pin the OpenAlex ``mailto=`` query parameter and the Crossref
    User-Agent ``(mailto:<email>)`` suffix used to join the polite pool.

    The knob's default is ``$LINGTAI_RESEARCH_EMAIL`` so secrets / personal
    addresses stay in environment, not in code.
    """

    def test_openalex_url_adds_mailto_when_provided(self):
        url = discover.build_openalex_url(
            "alfvenic turbulence",
            max_results=10,
            mailto="research@example.org",
        )
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertEqual(parsed["mailto"], "research@example.org")

    def test_openalex_url_omits_mailto_when_absent(self):
        url = discover.build_openalex_url("alfvenic turbulence", max_results=10)
        parsed = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        self.assertNotIn("mailto", parsed)

    def test_user_agent_with_mailto_appends_polite_pool_suffix(self):
        ua = discover._user_agent(mailto="research@example.org")
        self.assertIn("(mailto:research@example.org)", ua)
        # The base USER_AGENT identity is preserved.
        self.assertIn("heliosi-discover", ua)

    def test_user_agent_without_mailto_is_base_string(self):
        ua = discover._user_agent(mailto=None)
        self.assertEqual(ua, discover.USER_AGENT)

    def test_cli_accepts_mailto_and_records_in_cli_args(self):
        tmp = Path(tempfile.mkdtemp(prefix="hsi-mailto-meta-"))
        try:
            run_dir = tmp / "run-m"
            rc, _, err = _run_cli(
                "--dry-run",
                "--run-dir", str(run_dir),
                "--no-corpus-manifest",
                "--mailto", "research@example.org",
            )
            self.assertEqual(rc, 0, msg=err)
            meta = json.loads((run_dir / "run_metadata.json").read_text())
            self.assertEqual(meta["cli_args"]["mailto"], "research@example.org")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_cli_defaults_to_env_lingtai_research_email(self):
        """When ``--mailto`` is not passed, the script must default to
        ``$LINGTAI_RESEARCH_EMAIL`` so the polite-pool address stays in env."""
        tmp = Path(tempfile.mkdtemp(prefix="hsi-mailto-env-"))
        try:
            run_dir = tmp / "run-me"
            rc, _, err = _run_cli(
                "--dry-run",
                "--run-dir", str(run_dir),
                "--no-corpus-manifest",
                env_extra={"LINGTAI_RESEARCH_EMAIL": "env-default@example.org"},
            )
            self.assertEqual(rc, 0, msg=err)
            meta = json.loads((run_dir / "run_metadata.json").read_text())
            self.assertEqual(
                meta["cli_args"]["mailto"], "env-default@example.org"
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_cli_no_mailto_when_neither_flag_nor_env_set(self):
        tmp = Path(tempfile.mkdtemp(prefix="hsi-mailto-none-"))
        try:
            run_dir = tmp / "run-mn"
            # Explicitly blank the env var so the default lookup returns None.
            rc, _, err = _run_cli(
                "--dry-run",
                "--run-dir", str(run_dir),
                "--no-corpus-manifest",
                env_extra={"LINGTAI_RESEARCH_EMAIL": ""},
            )
            self.assertEqual(rc, 0, msg=err)
            meta = json.loads((run_dir / "run_metadata.json").read_text())
            self.assertIsNone(meta["cli_args"]["mailto"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


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

    def test_fixture_dedupes_15_raw_to_13(self):
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
        self.assertEqual(summary["raw_candidate_count"], 15)
        self.assertEqual(summary["deduped_candidate_count"], 13)
        self.assertEqual(len(candidates), 13)
        # All dedupe keys must be unique.
        keys = [c["id"] for c in candidates]
        self.assertEqual(len(set(keys)), 13)
        # The two backends with duplicates (DOI + arXiv + bibcode collisions)
        # collapse to one record each; surviving keys should include exactly
        # the deterministic strings below.
        self.assertIn("doi:10.1234/psp.switchback.2024", keys)
        self.assertIn("arxiv:2403.04567", keys)
        self.assertIn("bibcode:2023apj...999..123x", keys)
        # Pre-1990 synthetic fixture rows survive dedupe via their ADS
        # bibcodes (no DOI, no arXiv); the one row with no bibcode (IMP-8,
        # 1979) survives via the title+year fallback.
        self.assertIn("bibcode:1958apj...999..001p", keys)
        self.assertIn("bibcode:1962sci...999..002n", keys)
        self.assertTrue(
            any(k.startswith("title:") for k in keys),
            "expected the IMP-8 pre-DOI pre-bibcode row to survive via "
            "title+year fallback",
        )

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


class TestPre1990FixtureBehavior(unittest.TestCase):
    """Pin dedupe + corpus_status + classification for the pre-1990 synthetic
    rows added to ``sample_records.jsonl``.

    These rows characterise the 1950-present discovery envelope: no DOI, no
    arXiv ID, ADS bibcode present where applicable, and the title+year
    fallback for the one row with no bibcode either. The intent is to lock
    in the script's behavior on the pre-DOI / pre-arXiv path so the
    1950-present sweep can rely on stable join semantics.
    """

    @classmethod
    def setUpClass(cls):
        cls.candidates, cls.summary = discover.run_discovery(
            queries=discover.DEFAULT_QUERIES,
            backends=["arxiv", "openalex"],
            max_results=10,
            live=False,
            fixture_path=JSONL_FIXTURE,
            timeout=5.0,
            page_pause_seconds=0,
            ads_token=None,
            now_iso="2026-05-19T00:00:00Z",
            corpus_manifest_path=MANIFEST_FIXTURE,
        )
        cls.by_id = {c["id"]: c for c in cls.candidates}

    def _get(self, dedupe_id):
        rec = self.by_id.get(dedupe_id)
        self.assertIsNotNone(
            rec, f"expected dedupe id {dedupe_id!r} in candidate set"
        )
        return rec

    def test_parker_1958_record_has_no_doi_no_arxiv_bibcode_only(self):
        rec = self._get("bibcode:1958apj...999..001p")
        self.assertIsNone(rec["doi"])
        self.assertIsNone(rec["arxiv_id"])
        self.assertEqual(rec["bibcode"], "1958ApJ...999..001P")
        self.assertEqual(rec["year"], 1958)
        # Pre-1990 fixture rows are NOT in the fixture manifest, so they
        # must classify as new_candidate even though the join is enabled.
        self.assertEqual(rec["corpus_status"], "new_candidate")
        self.assertIsNone(rec["corpus_match_via"])
        # The taxonomy must still tag the row on title/abstract content.
        self.assertIn("solar-wind", rec["topic_tags"])
        self.assertIn("heliosphere", rec["topic_tags"])

    def test_mariner_1962_record_is_pre_arxiv_pre_doi(self):
        rec = self._get("bibcode:1962sci...999..002n")
        self.assertIsNone(rec["doi"])
        self.assertIsNone(rec["arxiv_id"])
        self.assertEqual(rec["year"], 1962)
        self.assertEqual(rec["corpus_status"], "new_candidate")
        self.assertIn("solar-wind", rec["topic_tags"])

    def test_voyager_1984_record_is_outer_heliosphere(self):
        rec = self._get("bibcode:1984jgr....999..005b")
        self.assertIsNone(rec["doi"])
        self.assertIsNone(rec["arxiv_id"])
        self.assertEqual(rec["year"], 1984)
        self.assertEqual(rec["corpus_status"], "new_candidate")
        # Heliosphere keyword must fire on this Voyager record.
        self.assertIn("heliosphere", rec["topic_tags"])

    def test_imp8_1979_record_falls_back_to_title_year_key(self):
        # IMP-8 row has no DOI, no arXiv ID, and no bibcode. Its dedupe id
        # must therefore live on the title+year SHA1 fallback branch.
        imp8_keys = [
            k
            for k, c in self.by_id.items()
            if c.get("year") == 1979
            and c.get("doi") is None
            and c.get("arxiv_id") is None
            and not c.get("bibcode")
        ]
        self.assertEqual(len(imp8_keys), 1)
        self.assertTrue(imp8_keys[0].startswith("title:"))
        rec = self.by_id[imp8_keys[0]]
        self.assertEqual(rec["year"], 1979)
        self.assertEqual(rec["corpus_status"], "new_candidate")
        # Classification still works on the title/abstract content.
        self.assertTrue(
            "sep" in rec["topic_tags"] or "shock" in rec["topic_tags"],
            f"expected SEP/shock tag on IMP-8 row, got {rec['topic_tags']}",
        )

    def test_all_pre_1990_rows_classify_as_new_candidate(self):
        """The fixture manifest has no pre-1990 entries, so every pre-1990
        candidate (5 by bibcode + 1 by title+year fallback) must be marked
        new_candidate when the novelty join is enabled."""
        pre_1990 = [
            c for c in self.candidates
            if c.get("year") is not None and c["year"] < 1990
        ]
        self.assertEqual(len(pre_1990), 6)
        for c in pre_1990:
            self.assertEqual(
                c["corpus_status"],
                "new_candidate",
                f"pre-1990 row {c['id']} not labelled new_candidate: {c}",
            )
            self.assertIsNone(c["corpus_match_via"])
            # The pre-1990 rows must not silently acquire fake DOI/arXiv
            # values during normalisation.
            self.assertIsNone(c["doi"])
            self.assertIsNone(c["arxiv_id"])

    def test_pre_1990_bibcode_dedupe_keys_are_lowercased(self):
        """Bibcode-based dedupe keys must be lowercased so case differences
        between ADS and other sources collapse correctly."""
        for c in self.candidates:
            if c.get("year") is not None and c["year"] < 1990 and c.get("bibcode"):
                self.assertEqual(
                    c["id"],
                    f"bibcode:{c['bibcode'].lower()}",
                    f"pre-1990 row {c['id']} has non-lowercased bibcode id",
                )

    def test_year_bounded_dry_run_filters_fixture_rows(self):
        """A dry-run against the multi-decade fixture must honor year bounds.

        The 1950-present pilot workflow is intentionally dry-run-first; if
        fixture records ignore ``year_from`` / ``year_until`` then the pilot
        cannot rehearse a date-bounded ADS-era slice before touching live APIs.
        """
        candidates, summary = discover.run_discovery(
            queries=discover.DEFAULT_QUERIES,
            backends=["arxiv", "openalex", "ads"],
            max_results=10,
            live=False,
            fixture_path=JSONL_FIXTURE,
            timeout=5.0,
            page_pause_seconds=0,
            ads_token=None,
            now_iso="2026-05-19T00:00:00Z",
            year_from=1958,
            year_until=1989,
        )
        self.assertEqual(summary["mode"], "dry-run")
        self.assertEqual(summary["year_from"], 1958)
        self.assertEqual(summary["year_until"], 1989)
        self.assertEqual(summary["raw_candidate_count"], 6)
        self.assertEqual(summary["deduped_candidate_count"], 6)
        self.assertEqual(summary["per_backend_counts"], {"arxiv": 0, "openalex": 0, "ads": 6})
        self.assertEqual(len(candidates), 6)
        years = sorted(c["year"] for c in candidates)
        self.assertEqual(years, [1958, 1962, 1976, 1979, 1981, 1984])
        self.assertTrue(all(1958 <= y <= 1989 for y in years))


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
        self.assertEqual(len(lines), 13)  # deduped from fixture
        first = json.loads(lines[0])
        for required in ("id", "source", "title", "topic_tags", "discovered_at_utc"):
            self.assertIn(required, first)
        # Summary is always written to stderr as JSON.
        summary_line = err.strip().splitlines()[-1]
        summary = json.loads(summary_line)
        self.assertEqual(summary["mode"], "dry-run")
        self.assertEqual(summary["deduped_candidate_count"], 13)

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


class TestCorpusManifestIndex(unittest.TestCase):
    """The manifest index drives the novelty join. Test it in isolation."""

    def test_build_index_extracts_canonical_keys(self):
        idx = discover.build_corpus_manifest_index(MANIFEST_FIXTURE)
        # DOI map is keyed by normalised DOI (lowercased, no resolver prefix).
        self.assertIn("10.1234/psp.switchback.2024", idx["by_doi"])
        psp = idx["by_doi"]["10.1234/psp.switchback.2024"]
        self.assertEqual(psp["slug"], "paper-psp-switchback-2024")

        # arXiv map is keyed by normalised arXiv ID. The "not-in-local-inventory"
        # sentinel and the "TODO_verify" placeholder MUST be filtered out --
        # those values are not valid IDs and must not match a candidate that
        # happens to have the literal "not-in-local-inventory" string.
        self.assertIn("2401.00001", idx["by_arxiv"])
        self.assertIn("2403.04567", idx["by_arxiv"])
        self.assertNotIn("not-in-local-inventory", idx["by_arxiv"])
        self.assertNotIn("todo_verify", idx["by_arxiv"])
        self.assertNotIn("TODO_verify", idx["by_arxiv"])

        # Title+year fallback is keyed by sha1(normalised_title|year) so it
        # collides with the script's own fallback dedupe key.
        self.assertTrue(any(k.startswith("title:") for k in idx["by_title_year"]))

    def test_index_total_entries_count_is_reported(self):
        idx = discover.build_corpus_manifest_index(MANIFEST_FIXTURE)
        # 5 entries in the fixture manifest. Sentinel / TODO arXiv values
        # are filtered out of by_arxiv but the entries themselves are still
        # indexed via DOI / title+year if available.
        self.assertEqual(idx["entry_count"], 5)
        self.assertEqual(idx["source_path"], str(MANIFEST_FIXTURE))


class TestNoveltyAnnotation(unittest.TestCase):
    """Test the per-candidate annotation that compares against the manifest."""

    def setUp(self):
        self.idx = discover.build_corpus_manifest_index(MANIFEST_FIXTURE)

    def _annotate(self, rec):
        return discover.annotate_candidate_with_corpus_status(rec, self.idx)

    def test_doi_match_marks_already_curated(self):
        rec = {
            "id": "doi:10.1234/psp.switchback.2024",
            "doi": "10.1234/psp.switchback.2024",
            "title": "anything",
            "year": 2024,
        }
        out = self._annotate(rec)
        self.assertEqual(out["corpus_status"], "already_curated")
        self.assertEqual(out["corpus_match_via"], "doi")
        self.assertIn("paper-psp-switchback-2024", out["corpus_match_slugs"])

    def test_arxiv_match_marks_already_curated_when_no_doi(self):
        rec = {
            "id": "arxiv:2403.04567",
            "doi": None,
            "arxiv_id": "arXiv:2403.04567v2",
            "title": "anything",
            "year": 2024,
        }
        out = self._annotate(rec)
        self.assertEqual(out["corpus_status"], "already_curated")
        self.assertEqual(out["corpus_match_via"], "arxiv")
        self.assertIn("paper-solo-cme-2024", out["corpus_match_slugs"])

    def test_title_year_fallback_match(self):
        rec = {
            "id": "title:does-not-matter",
            "doi": None,
            "arxiv_id": None,
            "title": "Machine Learning Classification of Solar Wind Types from Wind Spacecraft Data",
            "year": 2022,
        }
        out = self._annotate(rec)
        self.assertEqual(out["corpus_status"], "already_curated")
        self.assertEqual(out["corpus_match_via"], "title_year")
        self.assertIn("paper-wind-ml-classification-2022", out["corpus_match_slugs"])

    def test_non_match_marks_new_candidate(self):
        rec = {
            "id": "doi:10.0000/unknown.1",
            "doi": "10.0000/unknown.1",
            "arxiv_id": "2999.99999",
            "title": "Some completely new heliophysics paper not in the curated bundle",
            "year": 2026,
        }
        out = self._annotate(rec)
        self.assertEqual(out["corpus_status"], "new_candidate")
        self.assertEqual(out["corpus_match_via"], None)
        self.assertEqual(out["corpus_match_slugs"], [])

    def test_sentinel_arxiv_does_not_collide(self):
        """A candidate whose arXiv ID is literally the sentinel string must
        not match the manifest entry that uses the sentinel."""
        rec = {
            "id": "title:whatever",
            "doi": None,
            "arxiv_id": "not-in-local-inventory",
            "title": "A different paper that happens to lack a real arXiv ID",
            "year": 2025,
        }
        out = self._annotate(rec)
        # Neither the candidate nor the manifest entry should have produced
        # a valid arXiv key, so this must NOT match the sentinel manifest row.
        self.assertEqual(out["corpus_status"], "new_candidate")
        self.assertEqual(out["corpus_match_via"], None)

    def test_doi_match_wins_over_arxiv_when_both_present(self):
        """If a candidate has both DOI and arXiv ID, the join must report the
        DOI match (canonical priority), not the arXiv one."""
        rec = {
            "id": "doi:10.1234/psp.switchback.2024",
            "doi": "10.1234/psp.switchback.2024",
            "arxiv_id": "2401.00001",
            "title": "anything",
            "year": 2024,
        }
        out = self._annotate(rec)
        self.assertEqual(out["corpus_match_via"], "doi")


class TestNoveltyJoinIntegration(unittest.TestCase):
    """End-to-end: run_discovery with corpus_manifest_path emits per-record
    novelty annotations and a top-level summary count."""

    def test_run_discovery_annotates_candidates_and_summary(self):
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
            corpus_manifest_path=MANIFEST_FIXTURE,
        )

        # Every candidate must carry the novelty fields.
        for c in candidates:
            self.assertIn("corpus_status", c)
            self.assertIn("corpus_match_via", c)
            self.assertIn("corpus_match_slugs", c)
            self.assertIn("corpus_match_titles", c)
            self.assertIn(c["corpus_status"], {"already_curated", "new_candidate"})

        # The 15-row fixture dedupes to 13 candidates. Three are present in
        # the fixture manifest (PSP switchback DOI, SolO CME arXiv ID, Wind
        # ML title+year). The other ten -- including the six pre-1990
        # synthetic rows -- are new.
        statuses = [c["corpus_status"] for c in candidates]
        self.assertEqual(sum(s == "already_curated" for s in statuses), 3)
        self.assertEqual(sum(s == "new_candidate" for s in statuses), 10)

        # The summary must surface the count and the manifest source path.
        self.assertIn("novelty_join", summary)
        nj = summary["novelty_join"]
        self.assertEqual(nj["enabled"], True)
        self.assertEqual(nj["already_curated_count"], 3)
        self.assertEqual(nj["new_candidate_count"], 10)
        self.assertEqual(nj["unjoined_count"], 0)
        self.assertEqual(nj["manifest_path"], str(MANIFEST_FIXTURE))
        # The honesty disclosure must call out fallback limits explicitly.
        self.assertIn("title", nj["limits"].lower())

    def test_run_discovery_without_manifest_omits_novelty_annotation(self):
        """When no manifest is supplied (and the default does not exist),
        candidates carry corpus_status='unjoined' and the summary records
        that the join was disabled."""
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
            corpus_manifest_path=None,
        )
        for c in candidates:
            self.assertEqual(c["corpus_status"], "unjoined")
            self.assertEqual(c["corpus_match_via"], None)
            self.assertEqual(c["corpus_match_slugs"], [])
        self.assertEqual(summary["novelty_join"]["enabled"], False)
        self.assertEqual(summary["novelty_join"]["already_curated_count"], 0)
        # When disabled, the script makes no novelty claim either way: every
        # row is unjoined, not a new_candidate.
        self.assertEqual(summary["novelty_join"]["new_candidate_count"], 0)
        self.assertEqual(
            summary["novelty_join"]["unjoined_count"],
            summary["deduped_candidate_count"],
        )


class TestCliCorpusManifestFlag(unittest.TestCase):
    def test_cli_accepts_corpus_manifest_and_reports_counts(self):
        rc, out, err = _run_cli(
            "--dry-run",
            "--output", "-",
            "--corpus-manifest", str(MANIFEST_FIXTURE),
        )
        self.assertEqual(rc, 0, msg=err)
        lines = [ln for ln in out.splitlines() if ln.strip()]
        # Same 13 deduped candidates as the no-manifest run.
        self.assertEqual(len(lines), 13)
        # Each candidate JSONL row must carry the novelty fields.
        for ln in lines:
            rec = json.loads(ln)
            self.assertIn("corpus_status", rec)
            self.assertIn(rec["corpus_status"], {"already_curated", "new_candidate"})
        summary = json.loads(err.strip().splitlines()[-1])
        self.assertEqual(summary["novelty_join"]["enabled"], True)
        self.assertEqual(summary["novelty_join"]["already_curated_count"], 3)
        self.assertEqual(summary["novelty_join"]["new_candidate_count"], 10)
        self.assertEqual(summary["novelty_join"]["unjoined_count"], 0)

    def test_cli_no_corpus_manifest_flag_reports_disabled(self):
        # Force the script to skip the manifest by pointing at a path that
        # does not exist. The CLI must report novelty_join.enabled = False
        # rather than crashing.
        rc, out, err = _run_cli(
            "--dry-run",
            "--output", "-",
            "--corpus-manifest", "/nonexistent/path/to/manifest.json",
        )
        self.assertEqual(rc, 0, msg=err)
        summary = json.loads(err.strip().splitlines()[-1])
        self.assertEqual(summary["novelty_join"]["enabled"], False)


class TestRunBundlePythonAPI(unittest.TestCase):
    """The orchestrator + bundle writers are pure Python; test them directly."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="hsi-run-bundle-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, *, manifest_path=None, prior_index=None):
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
            corpus_manifest_path=manifest_path,
        )
        if prior_index is not None:
            candidates = discover.annotate_with_prior_runs(candidates, prior_index)
        return candidates, summary

    def test_write_run_bundle_emits_three_artifacts(self):
        candidates, summary = self._run(manifest_path=MANIFEST_FIXTURE)
        prior_index = discover.scan_prior_runs(None)
        run_dir = self.tmp / "run-a"
        discover._prepare_run_dir(run_dir, overwrite=False)
        metadata = discover.build_run_metadata(
            summary=summary,
            candidates=candidates,
            cli_args={"mode": "dry-run"},
            prior_index=prior_index,
            run_dir=run_dir,
            git_commit=None,
        )
        report_text = discover.render_run_report(metadata)
        paths = discover.write_run_bundle(
            run_dir,
            candidates=candidates,
            metadata=metadata,
            report_text=report_text,
        )

        self.assertTrue(paths["candidates_jsonl"].is_file())
        self.assertTrue(paths["run_metadata_json"].is_file())
        self.assertTrue(paths["run_report_md"].is_file())

        # candidates.jsonl: one JSON object per line, novelty-annotated.
        lines = paths["candidates_jsonl"].read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 13)
        for ln in lines:
            rec = json.loads(ln)
            self.assertIn("corpus_status", rec)
            # Prior-run scan was disabled, so those fields must NOT appear.
            self.assertNotIn("seen_in_prior_run", rec)
            self.assertNotIn("prior_run_ids", rec)

        # run_metadata.json: pin schema_version + dedupe + novelty + limits.
        meta = json.loads(paths["run_metadata_json"].read_text(encoding="utf-8"))
        self.assertEqual(meta["schema_version"], discover.RUN_BUNDLE_SCHEMA_VERSION)
        self.assertEqual(meta["script_version"], discover.__version__)
        self.assertEqual(meta["mode"], "dry-run")
        self.assertEqual(meta["query_count"], len(discover.DEFAULT_QUERIES))
        self.assertEqual(meta["dedupe_summary"]["raw_candidate_count"], 15)
        self.assertEqual(meta["dedupe_summary"]["deduped_candidate_count"], 13)
        self.assertEqual(meta["novelty_join"]["enabled"], True)
        self.assertEqual(meta["candidate_counts_by_corpus_status"]["already_curated"], 3)
        self.assertEqual(meta["candidate_counts_by_corpus_status"]["new_candidate"], 10)
        self.assertEqual(meta["candidate_counts_by_corpus_status"]["unjoined"], 0)
        self.assertEqual(meta["prior_runs"]["enabled"], False)
        self.assertIn("frontier sample", meta["limits"])
        self.assertIn("not verified absence", meta["limits"])
        self.assertNotIn("candidate_counts_by_prior_run", meta)

        # output_paths must point inside the bundle directory.
        for k in ("candidates_jsonl", "run_metadata_json", "run_report_md"):
            self.assertTrue(meta["output_paths"][k].startswith(str(run_dir)))

        # run_report.md: human-readable, references the canonical counts.
        report = paths["run_report_md"].read_text(encoding="utf-8")
        self.assertIn("# Discovery run report", report)
        self.assertIn("Raw candidates fetched: **15**", report)
        self.assertIn("Deduped candidates emitted: **13**", report)
        self.assertIn("Already curated (manifest hit): **3**", report)
        self.assertIn("New candidates (no manifest hit): **10**", report)
        self.assertIn("Limits (honest framing)", report)
        self.assertIn("Next actions", report)
        # When prior-run scan is disabled the report should NOT advertise
        # seen-in-prior-run counts (those are only emitted when enabled).
        self.assertNotIn("Seen in a prior run:", report)

    def test_disabled_manifest_join_keeps_unjoined_in_bundle(self):
        """When the manifest is disabled, candidates must stay 'unjoined',
        never silently become 'new_candidate'."""
        candidates, summary = self._run(manifest_path=None)
        prior_index = discover.scan_prior_runs(None)
        run_dir = self.tmp / "run-noj"
        discover._prepare_run_dir(run_dir, overwrite=False)
        metadata = discover.build_run_metadata(
            summary=summary,
            candidates=candidates,
            cli_args={"mode": "dry-run", "no_corpus_manifest": True},
            prior_index=prior_index,
            run_dir=run_dir,
            git_commit=None,
        )
        report_text = discover.render_run_report(metadata)
        paths = discover.write_run_bundle(
            run_dir,
            candidates=candidates,
            metadata=metadata,
            report_text=report_text,
        )
        meta = json.loads(paths["run_metadata_json"].read_text(encoding="utf-8"))
        # All 13 candidates must be 'unjoined', not 'new_candidate'.
        by = meta["candidate_counts_by_corpus_status"]
        self.assertEqual(by["unjoined"], 13)
        self.assertEqual(by["already_curated"], 0)
        self.assertEqual(by["new_candidate"], 0)
        self.assertEqual(meta["novelty_join"]["enabled"], False)
        # The candidate JSONL itself must agree.
        rows = [
            json.loads(ln)
            for ln in paths["candidates_jsonl"]
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        for r in rows:
            self.assertEqual(r["corpus_status"], "unjoined")

    def test_prior_runs_scan_disabled_when_root_missing(self):
        idx = discover.scan_prior_runs(self.tmp / "does" / "not" / "exist")
        self.assertEqual(idx["enabled"], False)
        self.assertEqual(idx["total_prior_keys"], 0)
        self.assertEqual(idx["runs_scanned"], [])

    def test_prior_runs_scan_indexes_sibling_runs(self):
        # Create a prior run-dir with a hand-written candidates.jsonl that
        # carries an explicit `id` field; the scan must reuse that id.
        prior = self.tmp / "queue" / "older-run"
        prior.mkdir(parents=True)
        with (prior / discover.RUN_BUNDLE_CANDIDATES_NAME).open(
            "w", encoding="utf-8"
        ) as f:
            f.write(
                json.dumps(
                    {
                        "id": "doi:10.1234/psp.switchback.2024",
                        "doi": "10.1234/psp.switchback.2024",
                        "title": "PSP switchbacks",
                        "year": 2024,
                    }
                )
                + "\n"
            )
            f.write(
                json.dumps(
                    {
                        "id": "arxiv:2403.04567",
                        "arxiv_id": "2403.04567",
                        "title": "SolO CME reconnection",
                        "year": 2024,
                    }
                )
                + "\n"
            )
        idx = discover.scan_prior_runs(self.tmp / "queue")
        self.assertEqual(idx["enabled"], True)
        self.assertEqual(idx["total_prior_keys"], 2)
        names = [r["name"] for r in idx["runs_scanned"]]
        self.assertIn("older-run", names)
        self.assertIn("doi:10.1234/psp.switchback.2024", idx["key_to_runs"])
        self.assertIn(
            "older-run", idx["key_to_runs"]["doi:10.1234/psp.switchback.2024"]
        )

    def test_annotate_with_prior_runs_marks_seen_and_unseen(self):
        candidates, _ = self._run(manifest_path=MANIFEST_FIXTURE)
        # Seed a prior-run dir whose JSONL has only the PSP DOI key. After
        # annotation, exactly one candidate must report seen_in_prior_run.
        prior = self.tmp / "queue" / "older-run"
        prior.mkdir(parents=True)
        with (prior / discover.RUN_BUNDLE_CANDIDATES_NAME).open(
            "w", encoding="utf-8"
        ) as f:
            f.write(
                json.dumps(
                    {
                        "id": "doi:10.1234/psp.switchback.2024",
                        "doi": "10.1234/psp.switchback.2024",
                        "title": "PSP switchbacks",
                        "year": 2024,
                    }
                )
                + "\n"
            )
        idx = discover.scan_prior_runs(self.tmp / "queue")
        annotated = discover.annotate_with_prior_runs(candidates, idx)
        seen = [c for c in annotated if c.get("seen_in_prior_run") is True]
        unseen = [c for c in annotated if c.get("seen_in_prior_run") is False]
        self.assertEqual(len(seen), 1)
        self.assertEqual(len(unseen), 12)
        self.assertIn("older-run", seen[0]["prior_run_ids"])

    def test_annotate_with_prior_runs_when_disabled_emits_no_fields(self):
        candidates, _ = self._run(manifest_path=MANIFEST_FIXTURE)
        idx = discover.scan_prior_runs(None)
        annotated = discover.annotate_with_prior_runs(candidates, idx)
        # Disabled scan: the annotation function must NOT invent fields.
        for c in annotated:
            self.assertNotIn("seen_in_prior_run", c)
            self.assertNotIn("prior_run_ids", c)

    def test_prepare_run_dir_refuses_non_empty_without_overwrite(self):
        run_dir = self.tmp / "run-existing"
        run_dir.mkdir()
        (run_dir / "leftover.txt").write_text("preserve me")
        with self.assertRaises(SystemExit):
            discover._prepare_run_dir(run_dir, overwrite=False)
        # leftover must survive the failed attempt.
        self.assertTrue((run_dir / "leftover.txt").is_file())
        # With --run-dir-overwrite the call must succeed and not delete the
        # leftover (writers will simply create new files alongside).
        discover._prepare_run_dir(run_dir, overwrite=True)
        self.assertTrue((run_dir / "leftover.txt").is_file())

    def test_iter_prior_run_dirs_excludes_current_run_dir(self):
        queue = self.tmp / "queue"
        queue.mkdir()
        # "current" run looks like a prior run (it has a candidates.jsonl)
        # but should be filtered out by ``exclude=``.
        current = queue / "current-run"
        current.mkdir()
        (current / discover.RUN_BUNDLE_CANDIDATES_NAME).write_text("")
        # "older" must show up.
        older = queue / "older-run"
        older.mkdir()
        (older / discover.RUN_BUNDLE_CANDIDATES_NAME).write_text("")
        dirs = discover._iter_prior_run_dirs(queue, exclude=current)
        names = [d.name for d in dirs]
        self.assertIn("older-run", names)
        self.assertNotIn("current-run", names)

    def test_render_run_report_mentions_prior_runs_when_enabled(self):
        candidates, summary = self._run(manifest_path=MANIFEST_FIXTURE)
        prior = self.tmp / "queue" / "older-run"
        prior.mkdir(parents=True)
        (prior / discover.RUN_BUNDLE_CANDIDATES_NAME).write_text(
            json.dumps(
                {
                    "id": "doi:10.1234/psp.switchback.2024",
                    "doi": "10.1234/psp.switchback.2024",
                    "title": "PSP switchbacks",
                    "year": 2024,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        idx = discover.scan_prior_runs(self.tmp / "queue")
        candidates = discover.annotate_with_prior_runs(candidates, idx)
        run_dir = self.tmp / "run-with-prior"
        discover._prepare_run_dir(run_dir, overwrite=False)
        metadata = discover.build_run_metadata(
            summary=summary,
            candidates=candidates,
            cli_args={"mode": "dry-run"},
            prior_index=idx,
            run_dir=run_dir,
            git_commit=None,
        )
        report = discover.render_run_report(metadata)
        self.assertIn("Seen in a prior run: **1**", report)
        self.assertIn("Unseen in prior runs: **12**", report)
        self.assertIn("`older-run`", report)
        self.assertIn("Prior-run dedupe (when enabled) is scoped", report)


class TestRunBundleCli(unittest.TestCase):
    """End-to-end CLI invocation: --run-dir + --prior-runs-root."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="hsi-run-bundle-cli-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_cli_run_dir_writes_bundle(self):
        run_dir = self.tmp / "run-a"
        rc, _, err = _run_cli(
            "--dry-run",
            "--output", str(self.tmp / "ignored.jsonl"),
            "--run-dir", str(run_dir),
            "--corpus-manifest", str(MANIFEST_FIXTURE),
        )
        self.assertEqual(rc, 0, msg=err)
        for name in (
            "candidates.jsonl",
            "run_metadata.json",
            "run_report.md",
        ):
            self.assertTrue(
                (run_dir / name).is_file(),
                f"missing run-bundle artifact: {name}",
            )
        meta = json.loads((run_dir / "run_metadata.json").read_text())
        self.assertEqual(meta["schema_version"], discover.RUN_BUNDLE_SCHEMA_VERSION)
        self.assertEqual(meta["mode"], "dry-run")
        self.assertEqual(meta["novelty_join"]["enabled"], True)
        self.assertEqual(meta["candidate_counts_by_corpus_status"]["already_curated"], 3)
        self.assertEqual(meta["candidate_counts_by_corpus_status"]["new_candidate"], 10)
        self.assertEqual(meta["prior_runs"]["enabled"], False)
        rows = (run_dir / "candidates.jsonl").read_text().splitlines()
        self.assertEqual(len(rows), 13)
        for ln in rows:
            self.assertIn("corpus_status", json.loads(ln))

    def test_cli_refuses_non_empty_run_dir_without_overwrite(self):
        run_dir = self.tmp / "run-existing"
        run_dir.mkdir()
        (run_dir / "leftover.txt").write_text("preserve me")
        rc, _, err = _run_cli(
            "--dry-run",
            "--run-dir", str(run_dir),
        )
        self.assertNotEqual(rc, 0)
        self.assertIn("non-empty", err)
        # The leftover file must still be present; we never silently wipe it.
        self.assertTrue((run_dir / "leftover.txt").is_file())

    def test_cli_run_dir_overwrite_allows_reuse(self):
        run_dir = self.tmp / "run-existing"
        run_dir.mkdir()
        (run_dir / "leftover.txt").write_text("preserve me")
        rc, _, err = _run_cli(
            "--dry-run",
            "--run-dir", str(run_dir),
            "--run-dir-overwrite",
            "--no-corpus-manifest",
        )
        self.assertEqual(rc, 0, msg=err)
        self.assertTrue((run_dir / "candidates.jsonl").is_file())

    def test_cli_prior_runs_root_marks_seen_candidates(self):
        queue = self.tmp / "queue"
        run_a = queue / "run-a"
        run_b = queue / "run-b"

        rc, _, err = _run_cli(
            "--dry-run",
            "--run-dir", str(run_a),
            "--no-corpus-manifest",
        )
        self.assertEqual(rc, 0, msg=err)

        rc, _, err = _run_cli(
            "--dry-run",
            "--run-dir", str(run_b),
            "--no-corpus-manifest",
            "--prior-runs-root", str(queue),
        )
        self.assertEqual(rc, 0, msg=err)

        meta = json.loads((run_b / "run_metadata.json").read_text())
        self.assertEqual(meta["prior_runs"]["enabled"], True)
        self.assertEqual(
            meta["prior_runs"]["root"], str(queue)
        )
        scanned = meta["prior_runs"]["runs_scanned"]
        names = [r["name"] for r in scanned]
        self.assertIn("run-a", names)
        # The CURRENT run-dir (run-b) must NEVER appear in its own prior list.
        self.assertNotIn("run-b", names)

        self.assertEqual(
            meta["candidate_counts_by_prior_run"]["seen_in_prior_run"], 13
        )
        self.assertEqual(
            meta["candidate_counts_by_prior_run"]["unseen_in_prior_runs"], 0
        )

        # Every candidate row must carry the prior-run dedupe fields.
        rows = [
            json.loads(ln)
            for ln in (run_b / "candidates.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        for r in rows:
            self.assertTrue(r["seen_in_prior_run"])
            self.assertIn("run-a", r["prior_run_ids"])

        # Report must surface the cross-run counts honestly.
        report = (run_b / "run_report.md").read_text()
        self.assertIn("Seen in a prior run: **13**", report)
        self.assertIn("Unseen in prior runs: **0**", report)
        self.assertIn("`run-a`", report)

    def test_cli_disabled_manifest_keeps_unjoined_in_bundle(self):
        """The --no-corpus-manifest flag must NOT cause candidates to be
        labelled 'new_candidate' in the run bundle."""
        run_dir = self.tmp / "run-noj"
        rc, _, err = _run_cli(
            "--dry-run",
            "--run-dir", str(run_dir),
            "--no-corpus-manifest",
        )
        self.assertEqual(rc, 0, msg=err)
        meta = json.loads((run_dir / "run_metadata.json").read_text())
        by = meta["candidate_counts_by_corpus_status"]
        self.assertEqual(by["unjoined"], 13)
        self.assertEqual(by["already_curated"], 0)
        self.assertEqual(by["new_candidate"], 0)
        rows = (run_dir / "candidates.jsonl").read_text().splitlines()
        for ln in rows:
            self.assertEqual(json.loads(ln)["corpus_status"], "unjoined")


if __name__ == "__main__":
    unittest.main()
