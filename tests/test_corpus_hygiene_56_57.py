"""Audit tests for issues #56 and #57.

Issue #56 — HelioSI leakage in design-pattern descriptions.
    The ``wave500_agent_runtime_eval_design_045`` batch contains 45
    harness-agnostic design-pattern paper-skills. Their per-entry
    ``description:`` (in SKILL.md frontmatter) and the ``required_data``
    list (in metadata.yaml) must not name the consuming harness
    ("HelioSI"); they should refer to the consuming agent/manuscript in
    harness-agnostic terms.

Issue #57 — slug year must match ``paper.year`` / metadata ``year``.
    When a slug follows the convention ``paper-<author>-<year>-...``,
    the leading year must equal the entry's ``paper.year`` (in SKILL.md
    frontmatter) and ``year`` (in metadata.yaml). The fix that closed
    #57 renamed ``paper-cohen-2026-coronal-flux-tube-shock-spot-newyearseve-2023``
    to ``paper-cohen-2025-...``; this test guards against future
    regressions.

Both checks are stdlib + PyYAML. They SKIP cleanly when PyYAML is
unavailable, following the convention of ``test_title_unicode.py``.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"
DESIGN_BATCH = CORPUS / "wave500_agent_runtime_eval_design_045"


def _have_pyyaml():
    try:
        import yaml  # noqa: F401
    except ImportError:
        return False
    return True


@unittest.skipUnless(_have_pyyaml(),
                     "PyYAML not installed; harness-leakage audit skipped")
class TestDesignPatternHarnessAgnostic(unittest.TestCase):
    """Issue #56 -- no HelioSI in per-entry description / required_data."""

    @classmethod
    def setUpClass(cls):
        cls.entry_dirs = sorted(
            d for d in DESIGN_BATCH.iterdir()
            if d.is_dir() and d.name.startswith("paper-")
        )

    def test_batch_exists(self):
        self.assertTrue(
            DESIGN_BATCH.is_dir(),
            f"missing design-pattern batch: {DESIGN_BATCH}",
        )
        self.assertGreaterEqual(
            len(self.entry_dirs), 1,
            f"design-pattern batch has no paper-* entries: {DESIGN_BATCH}",
        )

    def test_skill_md_description_is_harness_agnostic(self):
        import yaml
        leaks = []
        for d in self.entry_dirs:
            skill = d / "SKILL.md"
            if not skill.is_file():
                continue
            text = skill.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                continue
            try:
                end = text.index("\n---", 4)
            except ValueError:
                continue
            try:
                fm = yaml.safe_load(text[4:end])
            except Exception:
                continue
            if not isinstance(fm, dict):
                continue
            desc = fm.get("description")
            if isinstance(desc, str) and "HelioSI" in desc:
                leaks.append(str(skill.relative_to(BUNDLE)))
        self.assertEqual(
            leaks, [],
            f"{len(leaks)} design-pattern SKILL.md description fields still "
            f"name 'HelioSI' (should reference the consuming "
            f"agent/manuscript): {leaks[:5]}",
        )

    def test_metadata_required_data_is_harness_agnostic(self):
        import yaml
        leaks = []
        for d in self.entry_dirs:
            meta = d / "metadata.yaml"
            if not meta.is_file():
                continue
            try:
                with open(meta) as f:
                    data = yaml.safe_load(f)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            req = data.get("required_data")
            if not isinstance(req, list):
                continue
            for i, item in enumerate(req):
                if isinstance(item, str) and "HelioSI" in item:
                    leaks.append(f"{meta.relative_to(BUNDLE)}:required_data[{i}]={item!r}")
        self.assertEqual(
            leaks, [],
            f"{len(leaks)} design-pattern metadata.yaml required_data items "
            f"still name 'HelioSI' (should reference the consuming "
            f"agent/manuscript): {leaks[:5]}",
        )


# Author = letters and hyphens only (no digits). Year is the first
# 4-digit token. Slugs that don't fit ``paper-<author>-<year>-...``
# (e.g. infrastructure entries like ``paper-cdaweb-heliophysics-archive``)
# are excluded from this rule; their author prefix is not a person name
# and their slug never carried a publication year in the first place.
SLUG_YEAR_RE = re.compile(r"^paper-(?:[a-z][a-z-]*[a-z]|[a-z])-(\d{4})-")

# Slugs with a documented pre-existing slug-year vs paper.year mismatch
# that is OUT OF SCOPE for issue #57 (which addressed only paper-cohen).
# The audit pins these so a future curator either (a) renames them and
# removes the entry here, or (b) consciously re-confirms the entry by
# editing this list. Adding a new entry here without an open issue is
# discouraged.
KNOWN_SLUG_YEAR_MISMATCHES = {
    "paper-camporeale-2017-knn-solar-wind-categorization",
    "paper-jebaraj-2025-localized-particle-global-coronal-shock",
    "paper-li-2026-3he-rich-bidirectional-sep-solar-orbiter",
    "paper-niemiec-2025-numerical-superdiffusive-particle-acceleration",
    "paper-stoffel-2025-rerunaway-Forbush-cross-correlation",
    # ARCANE (Rüdisser et al.): slug encodes year 2024 (factory-generated
    # successor-lineage stub) but the verified primary source is
    # arXiv:2505.09365 (May 2025 preprint, Space Weather 2026,
    # doi:10.1029/2025SW004537). The bibliographic block is authoritative;
    # the slug name is preserved for stable cross-references. Internalized
    # 2026-05-19 in feat/internalize-wave500-ml-batch1.
    "paper-rudisser-2024-icme-unet-realtime-deployment",
    # Andrés et al.: slug encodes 2021 (arXiv submission Dec 2021) but the
    # paper appeared in A&A 661, A116 in 2022. Slug preserved for stable
    # cross-skill [[wikilinks]]; bibliographic block carries the publication
    # year. Internalized 2026-05-19 in feat/internalize-wave500-turbulence-batch1.
    "paper-andres-2021-incompressible-cascade-anisotropic-pp",
    # McIntyre et al.: slug encodes 2024 (arXiv submission Jul 2024) but the
    # paper appeared in Phys. Rev. X 15, 031008 in 2025. Slug preserved for
    # stable cross-skill [[wikilinks]]; bibliographic block carries the
    # publication year. Internalized 2026-05-19 in
    # feat/internalize-wave500-turbulence-batch1.
    "paper-mcintyre-2024-helicity-barrier-transition-range",
}


@unittest.skipUnless(_have_pyyaml(),
                     "PyYAML not installed; slug-year audit skipped")
class TestSlugYearMatchesPaperYear(unittest.TestCase):
    """Issue #57 -- when a slug is ``paper-<author>-<year>-...`` the
    leading year must equal ``paper.year`` (SKILL.md frontmatter) and
    ``year`` (metadata.yaml). Pre-existing mismatches are pinned in
    ``KNOWN_SLUG_YEAR_MISMATCHES`` so this audit guards against
    regressions for entries that the curator has already aligned (most
    importantly ``paper-cohen-2025-coronal-flux-tube-shock-spot-newyearseve-2023``
    after #57's rename)."""

    @classmethod
    def setUpClass(cls):
        cls.entry_dirs = sorted(CORPUS.glob("*/paper-*"))

    def test_any_paper_dirs_found(self):
        self.assertGreater(
            len(self.entry_dirs), 0,
            f"no paper-* entries found under {CORPUS}",
        )

    def test_known_mismatch_allowlist_is_minimal(self):
        """Allowlist entries must still exist on disk; otherwise they
        are stale and should be removed from the list."""
        existing = {d.name for d in self.entry_dirs if d.is_dir()}
        stale = sorted(KNOWN_SLUG_YEAR_MISMATCHES - existing)
        self.assertEqual(
            stale, [],
            "KNOWN_SLUG_YEAR_MISMATCHES contains slugs that no longer "
            f"exist; remove them: {stale}",
        )

    def test_cohen_2025_slug_is_present_and_correct(self):
        """Regression guard for #57: the rename from
        paper-cohen-2026-... to paper-cohen-2025-... must stick, the
        old slug must NOT exist on disk, and the new slug's year fields
        must agree."""
        import yaml
        new_dir = CORPUS / "wave500_sep_shocks_space_weather_045" / (
            "paper-cohen-2025-coronal-flux-tube-shock-spot-newyearseve-2023"
        )
        old_dir = CORPUS / "wave500_sep_shocks_space_weather_045" / (
            "paper-cohen-2026-coronal-flux-tube-shock-spot-newyearseve-2023"
        )
        self.assertTrue(new_dir.is_dir(),
                        f"renamed entry missing: {new_dir}")
        self.assertFalse(old_dir.exists(),
                         f"stale pre-rename entry still on disk: {old_dir}")
        meta = new_dir / "metadata.yaml"
        with open(meta) as f:
            data = yaml.safe_load(f)
        self.assertEqual(data.get("year"), 2025,
                         "paper-cohen-2025 metadata.year must be 2025")
        self.assertEqual(data.get("slug"),
                         "paper-cohen-2025-coronal-flux-tube-shock-spot-newyearseve-2023",
                         "metadata.slug must match the renamed folder")

        skill = new_dir / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        end = text.index("\n---", 4)
        fm = yaml.safe_load(text[4:end])
        self.assertEqual(fm.get("name"),
                         "paper-cohen-2025-coronal-flux-tube-shock-spot-newyearseve-2023",
                         "SKILL.md frontmatter `name:` must match the renamed folder")
        self.assertEqual(fm.get("paper", {}).get("year"), 2025,
                         "SKILL.md paper.year must be 2025")

    def test_slug_year_matches_metadata_and_skill_year(self):
        import yaml
        mismatches = []
        for d in self.entry_dirs:
            if not d.is_dir():
                continue
            m = SLUG_YEAR_RE.match(d.name)
            if not m:
                continue
            if d.name in KNOWN_SLUG_YEAR_MISMATCHES:
                continue
            slug_year = int(m.group(1))

            meta = d / "metadata.yaml"
            if meta.is_file():
                try:
                    with open(meta) as f:
                        data = yaml.safe_load(f)
                except Exception:
                    data = None
                if isinstance(data, dict):
                    yr = data.get("year")
                    if isinstance(yr, int) and yr != slug_year:
                        mismatches.append(
                            f"{meta.relative_to(BUNDLE)}: slug year "
                            f"{slug_year} != metadata year {yr}"
                        )

            skill = d / "SKILL.md"
            if skill.is_file():
                text = skill.read_text(encoding="utf-8")
                if text.startswith("---\n"):
                    try:
                        end = text.index("\n---", 4)
                    except ValueError:
                        end = None
                    if end is not None:
                        try:
                            fm = yaml.safe_load(text[4:end])
                        except Exception:
                            fm = None
                        if isinstance(fm, dict):
                            paper = fm.get("paper")
                            if isinstance(paper, dict):
                                pyr = paper.get("year")
                                if isinstance(pyr, int) and pyr != slug_year:
                                    mismatches.append(
                                        f"{skill.relative_to(BUNDLE)}: slug "
                                        f"year {slug_year} != paper.year {pyr}"
                                    )
        self.assertEqual(
            mismatches, [],
            f"{len(mismatches)} entries have slug-year != paper.year / "
            f"metadata.year (slug-as-citation must not misattribute the "
            f"year). Either fix the entry or, if intentional, add the "
            f"slug to KNOWN_SLUG_YEAR_MISMATCHES with a justification: "
            f"{mismatches[:5]}",
        )


if __name__ == "__main__":
    unittest.main()
