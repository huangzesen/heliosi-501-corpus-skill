"""Tests for scripts/draft_paper_skill_from_candidates.py.

Stdlib-only unittest module. No network calls: every test exercises the
script's pure functions or runs the CLI against the on-disk fixtures under
``tests/fixtures/drafts/``.

The scaffold turns discovery candidates into *quarantined draft* paper-skills
that live outside ``references/corpus/``. The tests below pin the
quarantine contract: defaults must skip ``already_curated`` rows, draft
artifacts must carry unmistakable DRAFT / UNVERIFIED / NOT-PROMOTED markers,
slug generation must be collision-safe, and the manifest + report must
record selected/skipped counts honestly.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
SCRIPT = BUNDLE / "scripts" / "draft_paper_skill_from_candidates.py"
FIXTURE_DIR = BUNDLE / "tests" / "fixtures" / "drafts"
CAND_FIXTURE = FIXTURE_DIR / "candidates_mixed.jsonl"
RUN_BUNDLE_FIXTURE = FIXTURE_DIR / "sample_run_bundle"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "draft_paper_skill_from_candidates", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_cli(*args, cwd=None):
    cmd = [sys.executable, str(SCRIPT), *args]
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or BUNDLE),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=60,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _first_record():
    for line in CAND_FIXTURE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return json.loads(line)
    raise RuntimeError("fixture has no records")


class TestModuleLoads(unittest.TestCase):
    """The script must be importable as a stdlib-only module."""

    def test_module_imports(self):
        mod = _load_module()
        for name in (
            "load_candidates",
            "select_candidates",
            "generate_slug",
            "render_skill_md",
            "render_metadata_yaml",
            "write_drafts",
            "build_manifest",
            "render_report",
            "DEFAULT_SELECTED_STATUSES",
            "DRAFT_FRONTMATTER_KIND",
        ):
            self.assertTrue(
                hasattr(mod, name), f"missing required attr: {name}"
            )


class TestSlugGeneration(unittest.TestCase):
    """Slugs are deterministic, filesystem-safe, and carry the DRAFT prefix."""

    def setUp(self):
        self.mod = _load_module()

    def test_slug_starts_with_draft_prefix(self):
        rec = {
            "id": "doi:10.1234/x.y",
            "title": "A new Parker Solar Probe diagnostic",
            "year": 2025,
            "authors": ["Q. Newauthor", "R. Junior"],
        }
        slug = self.mod.generate_slug(rec)
        self.assertTrue(
            slug.startswith("draft__"),
            f"slug must begin with quarantine prefix 'draft__'; got {slug!r}",
        )

    def test_slug_is_filesystem_safe(self):
        rec = {
            "id": "title:abcd1234",
            "title": "A study of  Alfvén waves & switchbacks / SEPs!",
            "year": 2024,
            "authors": ["É. Author-Name"],
        }
        slug = self.mod.generate_slug(rec)
        bad = [c for c in slug if not (c.isalnum() or c in "_-")]
        self.assertEqual(bad, [], f"slug has unsafe characters {bad!r}: {slug!r}")
        self.assertTrue(slug.startswith("draft__"))

    def test_slug_is_deterministic(self):
        rec = {
            "id": "arxiv:2503.22222",
            "title": "Open-flux estimates",
            "year": 2025,
            "authors": ["S. Stranger"],
        }
        self.assertEqual(
            self.mod.generate_slug(rec), self.mod.generate_slug(rec)
        )

    def test_slugs_differ_for_same_author_year(self):
        r1 = {
            "id": "arxiv:2503.22222",
            "title": "Open-flux estimates from non-spherical PFSS variants",
            "year": 2025,
            "authors": ["S. Stranger"],
        }
        r2 = {
            "id": "arxiv:2504.33333",
            "title": "Another PFSS extension applied to high-latitude open flux",
            "year": 2025,
            "authors": ["S. Stranger", "T. Otheruser"],
        }
        self.assertNotEqual(
            self.mod.generate_slug(r1), self.mod.generate_slug(r2)
        )

    def test_slug_handles_missing_author(self):
        rec = {
            "id": "title:abcd1234abcd1234",
            "title": "Mystery study",
            "year": 2024,
            "authors": [],
        }
        slug = self.mod.generate_slug(rec)
        self.assertTrue(slug.startswith("draft__"))
        # Must end with the hash suffix so collisions are avoided.
        self.assertRegex(slug, r"[0-9a-f]{6}$")


class TestSelectCandidates(unittest.TestCase):
    """Status-based selection has hard defaults and explicit overrides."""

    def setUp(self):
        self.mod = _load_module()
        self.records = self.mod.load_candidates(CAND_FIXTURE)
        # 5 total: 3 new_candidate + 1 unjoined + 1 already_curated.
        self.assertEqual(len(self.records), 5)

    def test_default_only_new_candidate(self):
        sel, skip = self.mod.select_candidates(self.records)
        self.assertEqual(sorted({r["corpus_status"] for r in sel}), ["new_candidate"])
        self.assertEqual(len(sel), 3)
        self.assertEqual(
            sorted({r["corpus_status"] for r in skip}),
            ["already_curated", "unjoined"],
        )

    def test_include_unjoined_adds_unjoined(self):
        sel, skip = self.mod.select_candidates(
            self.records, include_unjoined=True
        )
        self.assertEqual(
            sorted({r["corpus_status"] for r in sel}),
            ["new_candidate", "unjoined"],
        )
        self.assertEqual(len(sel), 4)
        self.assertEqual([r["corpus_status"] for r in skip], ["already_curated"])

    def test_include_all_statuses_includes_already_curated(self):
        sel, skip = self.mod.select_candidates(
            self.records, include_all_statuses=True
        )
        self.assertEqual(len(sel), 5)
        self.assertEqual(skip, [])

    def test_default_skips_already_curated_even_if_unjoined_included(self):
        sel, _ = self.mod.select_candidates(
            self.records, include_unjoined=True
        )
        self.assertNotIn(
            "already_curated", {r["corpus_status"] for r in sel}
        )


class TestRenderSkillMd(unittest.TestCase):
    """The rendered SKILL.md body must read as unmistakably quarantined."""

    def setUp(self):
        self.mod = _load_module()
        self.rec = _first_record()
        self.slug = self.mod.generate_slug(self.rec)
        self.body = self.mod.render_skill_md(self.rec, slug=self.slug)

    def test_skill_md_has_yaml_frontmatter(self):
        self.assertTrue(self.body.startswith("---\n"))
        self.assertGreater(self.body.find("\n---\n", 4), 0)

    def test_frontmatter_carries_quarantine_fields(self):
        end = self.body.find("\n---\n", 4)
        fm = self.body[4:end]
        for needle in (
            f"name: {self.slug}",
            "kind: discovery-draft",
            "promotion_status: unreviewed",
            "verified: false",
            "maturity: candidate",
            "quality_level: unverified-candidate",
            "executable_status: unverified-draft",
            "authors_verified: false",
        ):
            self.assertIn(needle, fm, f"missing quarantine field: {needle!r}")

    def test_body_contains_draft_warning_banner(self):
        for needle in ("DRAFT", "UNVERIFIED", "NOT A CORPUS ENTRY"):
            self.assertIn(needle, self.body)
        self.assertIn("must not be promoted", self.body.lower())

    def test_body_contains_four_layer_sections(self):
        for header in (
            "## Layer 1",
            "## Layer 2",
            "## Layer 3",
            "## Layer 4",
        ):
            self.assertIn(header, self.body)

    def test_body_records_candidate_provenance(self):
        self.assertIn(self.rec["title"], self.body)
        self.assertIn(str(self.rec["year"]), self.body)
        self.assertIn(self.rec["doi"], self.body)
        self.assertIn(self.rec["arxiv_id"], self.body)
        self.assertIn(self.rec["url"], self.body)
        self.assertIn(self.rec["authors"][0], self.body)

    def test_body_lists_validation_todos(self):
        for needle in (
            "verify doi",
            "verify arxiv",
            "verify title",
            "verify authors",
            "fetch full text",
            "extract claim",
            "data/tool contracts",
            "validation target",
            "failure modes",
            "maturity tier",
        ):
            self.assertIn(needle, self.body.lower())

    def test_body_states_no_fabricated_claims(self):
        self.assertIn("non-authoritative", self.body.lower())
        body_lower = self.body.lower()
        self.assertTrue(
            "must not claim" in body_lower
            or "do not claim" in body_lower
            or "do not assert" in body_lower
        )

    def test_body_preserves_source_query_and_backend(self):
        self.assertIn(self.rec["query"], self.body)
        self.assertIn(self.rec["source"], self.body)


class TestRenderMetadataYaml(unittest.TestCase):
    """metadata.yaml must mirror the quarantine state, not corpus state."""

    def setUp(self):
        self.mod = _load_module()
        self.rec = _first_record()
        self.slug = self.mod.generate_slug(self.rec)
        self.text = self.mod.render_metadata_yaml(self.rec, slug=self.slug)

    def test_metadata_yaml_carries_quarantine_fields(self):
        for needle in (
            f"slug: {self.slug}",
            "kind: discovery-draft",
            "promotion_status: unreviewed",
            "verified: false",
            "maturity: candidate",
            "quality_level: unverified-candidate",
            "executable_status: unverified-draft",
            "authors_verified: false",
        ):
            self.assertIn(needle, self.text, f"missing quarantine field: {needle!r}")

    def test_metadata_yaml_preserves_provenance(self):
        self.assertIn(self.rec["doi"], self.text)
        self.assertIn(self.rec["arxiv_id"], self.text)
        self.assertIn(self.rec["url"], self.text)
        self.assertIn(self.rec["query"], self.text)
        self.assertIn(self.rec["source"], self.text)
        self.assertIn(self.rec["discovered_at_utc"], self.text)
        self.assertIn(self.rec["id"], self.text)

    def test_metadata_yaml_includes_promotion_gate_checklist(self):
        for needle in (
            "promotion_gate:",
            "bibliographic_identity_verified",
            "provenance_checked",
            "title_authors_year_conflicts_resolved",
            "abstract_or_full_text_inspected",
            "claims_evidence_extracted",
            "data_tool_contracts_defined",
            "validation_target_recorded",
            "failure_modes_recorded",
            "maturity_tier_assigned",
        ):
            self.assertIn(needle, self.text, f"missing gate item: {needle!r}")


class TestCliEndToEnd(unittest.TestCase):
    """Drive the CLI end-to-end against the on-disk fixtures."""

    def test_default_drafts_only_new_candidate_rows(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_default"
            rc, _, err = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertEqual(rc, 0, f"CLI failed: stderr={err}")
            manifest_path = drafts_dir / "draft_manifest.json"
            report_path = drafts_dir / "draft_report.md"
            self.assertTrue(manifest_path.is_file())
            self.assertTrue(report_path.is_file())
            manifest = json.loads(manifest_path.read_text())
            self.assertEqual(manifest["selected_count"], 3)
            self.assertEqual(manifest["skipped_count"], 2)
            self.assertEqual(
                manifest["selected_counts_by_corpus_status"],
                {"new_candidate": 3},
            )
            self.assertEqual(
                manifest["skipped_counts_by_corpus_status"],
                {"already_curated": 1, "unjoined": 1},
            )
            draft_dirs = sorted(
                p for p in drafts_dir.iterdir()
                if p.is_dir() and p.name.startswith("draft__")
            )
            self.assertEqual(len(draft_dirs), 3)
            for d in draft_dirs:
                self.assertTrue((d / "SKILL.md").is_file())
                self.assertTrue((d / "metadata.yaml").is_file())

    def test_include_unjoined_flag(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_unjoined"
            rc, _, err = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
                "--include-unjoined",
            )
            self.assertEqual(rc, 0, err)
            manifest = json.loads((drafts_dir / "draft_manifest.json").read_text())
            self.assertEqual(manifest["selected_count"], 4)
            self.assertEqual(
                manifest["selected_counts_by_corpus_status"],
                {"new_candidate": 3, "unjoined": 1},
            )

    def test_include_all_statuses_flag(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_all"
            rc, _, err = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
                "--include-all-statuses",
            )
            self.assertEqual(rc, 0, err)
            manifest = json.loads((drafts_dir / "draft_manifest.json").read_text())
            self.assertEqual(manifest["selected_count"], 5)
            self.assertEqual(
                manifest["selected_counts_by_corpus_status"],
                {"already_curated": 1, "new_candidate": 3, "unjoined": 1},
            )

    def test_collision_refused_without_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_collide"
            rc1, _, err1 = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertEqual(rc1, 0, err1)
            rc2, _, err2 = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertNotEqual(rc2, 0)
            self.assertIn("draft", err2.lower())

    def test_overwrite_allows_re_run(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_overwrite"
            rc1, _, err1 = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertEqual(rc1, 0, err1)
            rc2, _, err2 = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
                "--overwrite",
            )
            self.assertEqual(rc2, 0, err2)

    def test_from_run_dir_reads_candidates_jsonl(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_from_bundle"
            rc, _, err = _run_cli(
                "--from-run-dir", str(RUN_BUNDLE_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertEqual(rc, 0, err)
            manifest = json.loads((drafts_dir / "draft_manifest.json").read_text())
            self.assertEqual(manifest["selected_count"], 3)
            self.assertEqual(manifest["input_kind"], "run-bundle")
            self.assertIn("sample_run_bundle", manifest["input_path"])

    def test_from_candidates_and_from_run_dir_are_mutually_exclusive(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_mutex"
            rc, _, _ = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--from-run-dir", str(RUN_BUNDLE_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertNotEqual(rc, 0)

    def test_report_carries_quarantine_disclosure(self):
        with tempfile.TemporaryDirectory() as td:
            drafts_dir = Path(td) / "drafts_report"
            rc, _, err = _run_cli(
                "--from-candidates", str(CAND_FIXTURE),
                "--drafts-dir", str(drafts_dir),
            )
            self.assertEqual(rc, 0, err)
            report = (drafts_dir / "draft_report.md").read_text()
            for needle in (
                "DRAFT",
                "UNVERIFIED",
                "NOT PROMOTED",
                "non-authoritative",
                "Selected counts",
                "Skipped counts",
            ):
                self.assertIn(needle, report, f"report missing: {needle!r}")
            self.assertIn("candidates_mixed.jsonl", report)


class TestQuarantineInvariant(unittest.TestCase):
    """No draft artifact may end up inside references/corpus/."""

    def test_drafts_dir_inside_references_corpus_is_refused(self):
        forbidden = BUNDLE / "references" / "corpus" / "would_be_drafts"
        rc, _, err = _run_cli(
            "--from-candidates", str(CAND_FIXTURE),
            "--drafts-dir", str(forbidden),
        )
        self.assertNotEqual(rc, 0)
        self.assertIn("references/corpus", err)
        self.assertFalse(forbidden.exists())


if __name__ == "__main__":
    unittest.main()
