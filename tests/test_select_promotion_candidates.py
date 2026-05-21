"""Tests for scripts/select_promotion_candidates.py.

The script is read-only over an external acquisition store and emits
report files. These tests build a synthetic store under a tempdir; they
never touch the real ``heliosi_acquisition`` directory and never make
network calls.

Store layout exercised:

    <store>/queue.jsonl
    <store>/attempts/<cand_id>.json            (run-acquisition tier fetch)
    <store>/authorized_attempts/<cand_id>.json (official-PDF probe)
    <store>/papers/<cand_id>/paper.pdf         (authorized-route PDF)
    <store>/papers/<manifest_slug>/paper.pdf   (tier-fetch route PDF)

The fixtures intentionally cover every interesting code path so that
the scoring rules, route inference, and report shapes are pinned.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "select_promotion_candidates.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("select_promotion_candidates", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


spc = _load_module()


# ──────────────────────────────────────────────────────────
#  Fixture builders
# ──────────────────────────────────────────────────────────

def _queue_row(
    cid: str,
    *,
    title: str = "A study of solar wind turbulence",
    year: int = 2024,
    doi: str | None = "10.1234/example",
    arxiv_id: str | None = None,
    bibcode: str | None = None,
    status: str = "fetched",
    source: str = "openalex",
    corpus_status: str = "new_candidate",
    cell: str = "P-test",
    identifier_kind: str = "doi",
    preferred_identifier: str | None = None,
    notes: str = "run:20260521T000000Z-aaaaaa",
) -> dict:
    return {
        "candidate_id": cid,
        "cell": cell,
        "source": source,
        "title": title,
        "year": year,
        "doi": doi,
        "arxiv_id": arxiv_id,
        "bibcode": bibcode,
        "corpus_status": corpus_status,
        "preferred_identifier": preferred_identifier or doi or arxiv_id or bibcode,
        "identifier_kind": identifier_kind,
        "priority": 10,
        "status": status,
        "notes": notes,
        "queued_at_utc": "2026-05-21T00:00:00Z",
    }


def _attempt(
    cid: str,
    *,
    last_result: str = "fetched",
    manifest_status: str | None = "ok",
    manifest_slug: str | None = None,
) -> dict:
    return {
        "schema_version": "heliosi-acquisition-run/1.0",
        "candidate_id": cid,
        "last_result": last_result,
        "fetch_summary": {
            "returncode": 0 if last_result == "fetched" else 1,
            "manifest_status": manifest_status,
            "manifest_slug": manifest_slug,
        },
    }


def _authorized(
    cid: str,
    *,
    last_result: str = "fetched",
    source: str = "official_pdf",
    pdf_url: str = "https://arxiv.org/pdf/2410.02530",
    pdf_bytes: int = 500_000,
) -> dict:
    return {
        "schema_version": "heliosi-authorized-probe/1.0",
        "candidate_id": cid,
        "last_result": last_result,
        "source": source,
        "pdf_url": pdf_url,
        "pdf_bytes": pdf_bytes,
        "landing_url": pdf_url.rsplit("/", 1)[0],
    }


def _build_store(tmp: Path, rows: list[dict], attempts: dict | None = None,
                 authorized: dict | None = None, pdfs: dict | None = None) -> Path:
    """Lay out a synthetic acquisition store under ``tmp``.

    ``attempts`` / ``authorized`` map ``cid -> dict``. ``pdfs`` maps
    ``relative path -> bytes`` so we can place files at either
    ``papers/<cid>/paper.pdf`` (authorized route) or
    ``papers/<manifest_slug>/paper.pdf`` (tier route).
    """
    store = tmp / "store"
    store.mkdir(parents=True, exist_ok=True)
    (store / "attempts").mkdir(exist_ok=True)
    (store / "authorized_attempts").mkdir(exist_ok=True)
    (store / "papers").mkdir(exist_ok=True)

    with (store / "queue.jsonl").open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")

    for cid, payload in (attempts or {}).items():
        (store / "attempts" / f"{cid}.json").write_text(json.dumps(payload))

    for cid, payload in (authorized or {}).items():
        (store / "authorized_attempts" / f"{cid}.json").write_text(json.dumps(payload))

    for rel, content in (pdfs or {}).items():
        p = store / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)

    return store


# ──────────────────────────────────────────────────────────
#  Slug + small unit pieces
# ──────────────────────────────────────────────────────────

class TestSuggestedSkillSlug(unittest.TestCase):
    def test_slug_is_deterministic_and_year_prefixed(self):
        slug_a = spc.suggested_skill_slug(
            "cand_abc123def456", year=2024, title="Solar Wind Turbulence Intermittency",
        )
        slug_b = spc.suggested_skill_slug(
            "cand_abc123def456", year=2024, title="Solar Wind Turbulence Intermittency",
        )
        self.assertEqual(slug_a, slug_b)
        self.assertTrue(slug_a.startswith("paper-2024-"))
        # Disambiguator from candidate_id (first 6 hex chars after the
        # ``cand_`` prefix) is appended deterministically.
        self.assertTrue(slug_a.endswith("-abc123"))

    def test_slug_does_not_embed_unverified_surname(self):
        # The queue row carries no verified author. The slug must not
        # invent one, even when the title starts with a word that looks
        # like a name.
        slug = spc.suggested_skill_slug(
            "cand_deadbeefcafefeed", year=2023, title="Parker Solar Probe magnetic switchbacks",
        )
        self.assertNotIn("parker-2023", slug)
        # The token "parker" may appear as a regular title token but
        # never as the surname slot directly after ``paper-``.
        self.assertFalse(slug.startswith("paper-parker"))

    def test_slug_truncates_long_titles_and_is_ascii_kebab(self):
        long_title = "A " * 50 + "very long title with non-ascii: αβγ — and dashes"
        slug = spc.suggested_skill_slug("cand_0123456789abcdef", year=2020, title=long_title)
        self.assertLess(len(slug), 120)
        self.assertEqual(slug, slug.lower())
        for ch in slug:
            self.assertTrue(ch.isalnum() or ch == "-", f"unexpected char {ch!r} in slug {slug!r}")

    def test_slug_falls_back_when_year_missing(self):
        slug = spc.suggested_skill_slug("cand_feedfacefeedface", year=None, title="x")
        self.assertTrue(slug.startswith("paper-unknownyear-"))


class TestRouteInference(unittest.TestCase):
    def test_official_pdf_route(self):
        route, host = spc.infer_route_and_host(
            authorized={"source": "official_pdf", "pdf_url": "https://arxiv.org/pdf/2410.02530"},
            attempt=None,
        )
        self.assertEqual(route, "official_pdf")
        self.assertEqual(host, "arxiv.org")

    def test_tiered_fetch_route_when_only_attempt_present(self):
        route, host = spc.infer_route_and_host(
            authorized=None,
            attempt={
                "last_result": "fetched",
                "fetch_summary": {"manifest_status": "ok", "manifest_slug": "chen-2010-anisotropy"},
            },
        )
        self.assertEqual(route, "tiered_fetch")
        # Tiered fetch leaves host unknown — we don't invent one.
        self.assertIsNone(host)

    def test_unknown_route_when_authorized_lacks_official_source(self):
        route, _host = spc.infer_route_and_host(
            authorized={"source": None, "pdf_url": None, "last_result": "no_official_pdf_link"},
            attempt=None,
        )
        self.assertEqual(route, "unknown")


# ──────────────────────────────────────────────────────────
#  Scoring
# ──────────────────────────────────────────────────────────

class TestScoring(unittest.TestCase):
    def test_high_signal_candidate_scores_above_low_signal(self):
        # High: recent arXiv+DOI, official_pdf route, sizeable PDF, keyword hit.
        high = {
            "year": 2025,
            "doi": "10.1234/x",
            "arxiv_id": "2501.00001",
            "corpus_status": "new_candidate",
            "title": "Solar wind switchback structure observed by Parker",
            "pdf_exists": True,
            "pdf_bytes": 800_000,
            "acquisition_route": "official_pdf",
            "manifest_status": "ok",
        }
        # Low: old, DOI only, no PDF on disk.
        low = {
            "year": 1968,
            "doi": "10.9/old",
            "arxiv_id": None,
            "corpus_status": "new_candidate",
            "title": "An unrelated topic",
            "pdf_exists": False,
            "pdf_bytes": 0,
            "acquisition_route": "unknown",
            "manifest_status": None,
        }
        score_high, reasons_high = spc.score_candidate(high, current_year=2026)
        score_low, reasons_low = spc.score_candidate(low, current_year=2026)
        self.assertGreater(score_high, score_low)
        # Reasons are transparent: each entry carries (component, points, why).
        for r in reasons_high + reasons_low:
            self.assertIn("component", r)
            self.assertIn("points", r)
            self.assertIn("why", r)

    def test_manifest_status_failure_subtracts_points(self):
        base = {
            "year": 2024, "doi": "10.1/x", "arxiv_id": None,
            "corpus_status": "new_candidate", "title": "irrelevant",
            "pdf_exists": True, "pdf_bytes": 200_000,
            "acquisition_route": "tiered_fetch",
            "manifest_status": "ok",
        }
        bad = dict(base, manifest_status="fail")
        s_base, _ = spc.score_candidate(base, current_year=2026)
        s_bad, _ = spc.score_candidate(bad, current_year=2026)
        self.assertGreater(s_base, s_bad)

    def test_keyword_bonus_fires_for_heliophysics_terms(self):
        base = {
            "year": 2024, "doi": "10.1/x", "arxiv_id": None,
            "corpus_status": "new_candidate", "title": "On the nature of bread",
            "pdf_exists": True, "pdf_bytes": 200_000,
            "acquisition_route": "tiered_fetch", "manifest_status": "ok",
        }
        helio = dict(base, title="On reconnection in the solar corona")
        s_base, reasons_base = spc.score_candidate(base, current_year=2026)
        s_helio, reasons_helio = spc.score_candidate(helio, current_year=2026)
        self.assertGreater(s_helio, s_base)
        components_helio = {r["component"] for r in reasons_helio}
        components_base = {r["component"] for r in reasons_base}
        self.assertIn("title_keyword", components_helio)
        self.assertNotIn("title_keyword", components_base)


# ──────────────────────────────────────────────────────────
#  End-to-end: build_report on a synthetic store
# ──────────────────────────────────────────────────────────

class TestBuildReport(unittest.TestCase):
    def _build_realistic_store(self, tmp: Path) -> Path:
        rows = [
            # High-signal: fetched via official PDF, recent, arXiv + DOI.
            _queue_row(
                "cand_aaaaaaaaaaaaaaaa",
                title="Switchback turbulence near the Sun",
                year=2025,
                doi="10.48550/arxiv.2501.00001",
                arxiv_id="2501.00001",
                status="fetched",
                notes="run:1; authorized-probe:1",
            ),
            # Mid-signal: fetched via tier path, slug-style PDF.
            _queue_row(
                "cand_bbbbbbbbbbbbbbbb",
                title="Anisotropy of solar wind fluctuations",
                year=2010,
                doi="10.1/anisotropy",
                arxiv_id=None,
                status="fetched",
                notes="run:1",
            ),
            # Fetched but PDF missing on disk — should still rank but
            # without the on-disk size bonus.
            _queue_row(
                "cand_cccccccccccccccc",
                title="Spectral break in heliospheric plasma",
                year=2022,
                doi="10.1/spectral",
                status="fetched",
                notes="run:1",
            ),
            # Pending — excluded from ranking table.
            _queue_row(
                "cand_dddddddddddddddd",
                title="An unfetched candidate",
                year=2024,
                doi="10.1/pending",
                status="pending",
                notes="",
            ),
            # Fetch-failed — excluded from ranking table.
            _queue_row(
                "cand_eeeeeeeeeeeeeeee",
                title="A failed fetch attempt",
                year=2023,
                doi="10.1/failed",
                status="fetch_failed",
                notes="",
            ),
            # No supported identifier — excluded from ranking table.
            _queue_row(
                "cand_ffffffffffffffff",
                title="Bibcode-only old paper",
                year=1962,
                doi=None,
                arxiv_id=None,
                bibcode="1962ApJ...135..474P",
                status="no_supported_identifier",
                identifier_kind="bibcode_only",
                preferred_identifier=None,
                notes="",
            ),
        ]
        attempts = {
            "cand_aaaaaaaaaaaaaaaa": _attempt("cand_aaaaaaaaaaaaaaaa"),
            "cand_bbbbbbbbbbbbbbbb": _attempt(
                "cand_bbbbbbbbbbbbbbbb", manifest_slug="anisotropy-2010-slug",
            ),
            "cand_cccccccccccccccc": _attempt("cand_cccccccccccccccc"),
        }
        authorized = {
            "cand_aaaaaaaaaaaaaaaa": _authorized("cand_aaaaaaaaaaaaaaaa"),
        }
        pdfs = {
            "papers/cand_aaaaaaaaaaaaaaaa/paper.pdf": b"%PDF-1.5\n" + b"x" * 500_000,
            "papers/anisotropy-2010-slug/paper.pdf": b"%PDF-1.5\n" + b"y" * 200_000,
            # cand_cccccccccccccccc: NO pdf on disk — covers the
            # "queue says fetched but file missing" path honestly.
        }
        return _build_store(tmp, rows, attempts=attempts, authorized=authorized, pdfs=pdfs)

    def test_build_report_shape_and_ranking(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = self._build_realistic_store(tmp)
            report = spc.build_report(store, top=10, current_year=2026)

            self.assertEqual(report["schema_version"], "heliosi-promotion-candidates/1.0")
            # Summary counts mirror the queue honestly.
            summary = report["summary"]
            self.assertEqual(summary["queue_total"], 6)
            self.assertEqual(summary["by_status"]["fetched"], 3)
            self.assertEqual(summary["by_status"]["pending"], 1)
            self.assertEqual(summary["by_status"]["fetch_failed"], 1)
            self.assertEqual(summary["by_status"]["no_supported_identifier"], 1)

            # Only fetched rows enter the ranked list.
            ranked_ids = [c["candidate_id"] for c in report["candidates"]]
            self.assertEqual(set(ranked_ids), {
                "cand_aaaaaaaaaaaaaaaa",
                "cand_bbbbbbbbbbbbbbbb",
                "cand_cccccccccccccccc",
            })
            # High-signal candidate ranks first.
            self.assertEqual(ranked_ids[0], "cand_aaaaaaaaaaaaaaaa")
            # Candidate with missing PDF ranks below the one with a tier PDF
            # (other signals equal-ish).
            ranked_ids_set_order = ranked_ids
            self.assertLess(
                ranked_ids_set_order.index("cand_bbbbbbbbbbbbbbbb"),
                ranked_ids_set_order.index("cand_cccccccccccccccc"),
            )

            # Per-candidate provenance fields are present and honest.
            top_a = report["candidates"][0]
            self.assertEqual(top_a["acquisition_route"], "official_pdf")
            self.assertEqual(top_a["acquisition_host"], "arxiv.org")
            self.assertTrue(top_a["pdf_exists"])
            self.assertGreater(top_a["pdf_bytes"], 100_000)
            self.assertEqual(top_a["queue_status"], "fetched")
            self.assertEqual(top_a["latest_attempt_result"], "fetched")
            self.assertTrue(top_a["suggested_skill_slug"].startswith("paper-2025-"))
            self.assertIsInstance(top_a["score_reasons"], list)

            mid_b = next(c for c in report["candidates"] if c["candidate_id"] == "cand_bbbbbbbbbbbbbbbb")
            # Slug-style PDF still counted via manifest_slug lookup.
            self.assertTrue(mid_b["pdf_exists"])
            self.assertEqual(mid_b["acquisition_route"], "tiered_fetch")
            self.assertIsNone(mid_b["acquisition_host"])

            missing_c = next(c for c in report["candidates"] if c["candidate_id"] == "cand_cccccccccccccccc")
            self.assertFalse(missing_c["pdf_exists"])
            self.assertEqual(missing_c["pdf_bytes"], 0)

            # Route counts reflect the provenance trail honestly.
            # Candidate c has an attempts/<cid>.json that claims
            # ``last_result == "fetched"``; the route is therefore
            # ``tiered_fetch`` even though no PDF was found on disk.
            # The missing PDF is surfaced separately via pdf_exists.
            self.assertEqual(summary["by_route"]["official_pdf"], 1)
            self.assertEqual(summary["by_route"]["tiered_fetch"], 2)
            self.assertNotIn("unknown", summary["by_route"])

            # Host counts include arxiv.org (the only official-PDF host).
            self.assertEqual(summary["by_host"].get("arxiv.org"), 1)

    def test_top_n_truncates_candidates_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = self._build_realistic_store(tmp)
            report = spc.build_report(store, top=1, current_year=2026)
            self.assertEqual(len(report["candidates"]), 1)
            # ...but summary counts still reflect the full queue.
            self.assertEqual(report["summary"]["queue_total"], 6)

    def test_handles_empty_store_without_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = _build_store(tmp, rows=[])
            report = spc.build_report(store, top=10, current_year=2026)
            self.assertEqual(report["summary"]["queue_total"], 0)
            self.assertEqual(report["candidates"], [])

    def test_missing_store_raises_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                spc.build_report(Path(tmp) / "does-not-exist", top=10, current_year=2026)


# ──────────────────────────────────────────────────────────
#  Output rendering
# ──────────────────────────────────────────────────────────

class TestRenderMarkdown(unittest.TestCase):
    def test_markdown_has_banner_summary_top_table_and_checklist(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = TestBuildReport()._build_realistic_store(tmp)
            report = spc.build_report(store, top=10, current_year=2026)
            md = spc.render_markdown(report, store_path_display="<acquisition-store>")

            # Honest banner — fetched PDF is not a verified paper-skill.
            self.assertIn("Fetched PDF", md)
            self.assertIn("not", md.lower())
            # Summary counts table.
            self.assertIn("Queue total", md)
            self.assertIn("6", md)  # queue total
            # Top-N candidates table includes the high-signal row.
            self.assertIn("cand_aaaaaaaaaaaaaaaa", md)
            self.assertIn("Switchback turbulence near the Sun", md)
            # Route + host counts.
            self.assertIn("official_pdf", md)
            self.assertIn("arxiv.org", md)
            # Manual / agentic next-step checklist heading present.
            self.assertIn("Next step", md)
            # No absolute fixture-private path leaks into the report
            # text — the caller-supplied display path is used.
            self.assertNotIn(str(store), md)
            self.assertIn("<acquisition-store>", md)


# ──────────────────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────────────────

class TestCLI(unittest.TestCase):
    def test_cli_writes_md_and_json_only_when_asked(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = TestBuildReport()._build_realistic_store(tmp)
            md_out = tmp / "report.md"
            json_out = tmp / "report.json"
            rc = spc.main([
                "--store", str(store),
                "--output-md", str(md_out),
                "--output-json", str(json_out),
                "--top", "2",
            ])
            self.assertEqual(rc, 0)
            self.assertTrue(md_out.exists())
            self.assertTrue(json_out.exists())

            payload = json.loads(json_out.read_text())
            self.assertEqual(payload["schema_version"], "heliosi-promotion-candidates/1.0")
            self.assertEqual(len(payload["candidates"]), 2)

            md_text = md_out.read_text()
            self.assertIn("cand_aaaaaaaaaaaaaaaa", md_text)

    def test_cli_without_outputs_is_a_noop_dry_run(self):
        # No --output-md / --output-json => script must not write files
        # under the store or anywhere. Useful for "just tell me the
        # counts" invocations from CI.
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            store = TestBuildReport()._build_realistic_store(tmp)
            before = sorted(p.relative_to(store).as_posix() for p in store.rglob("*"))
            rc = spc.main(["--store", str(store)])
            self.assertEqual(rc, 0)
            after = sorted(p.relative_to(store).as_posix() for p in store.rglob("*"))
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
