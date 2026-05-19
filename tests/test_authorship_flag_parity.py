"""Per-entry `authors_verified` parity tests (issue #62).

Mirrors ``scripts/validate.sh`` section S4f: asserts that the
``authors_verified: false`` disclosure is consistent between
``metadata.yaml`` and the per-entry ``SKILL.md`` YAML frontmatter.

Concretely, for each of the 501 entries:

1. If ``metadata.yaml`` has top-level ``authors_verified: false``, the
   corresponding ``SKILL.md`` frontmatter MUST have
   ``paper.authors_verified: false`` (forward direction).
2. If ``SKILL.md`` frontmatter has ``paper.authors_verified: false``,
   ``metadata.yaml`` MUST also have top-level
   ``authors_verified: false`` (reverse direction). The reverse
   direction guards against a SKILL.md being honest about unverified
   authorship while the corresponding metadata.yaml silently advertises
   the inverse.

The invariant is exact bidirectional parity, not "at least one side
flagged". After issue #62 fixup the expected count is 173 / 173.

This check is skipped when PyYAML is not installed, mirroring the
existing ``test_authorship_hygiene`` and ``test_corpus_integrity``
modules. The CI workflow installs PyYAML so it always runs there.
"""

from __future__ import annotations

import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"


class _ParityBase(unittest.TestCase):
    """Shared PyYAML import + per-entry scan."""

    @classmethod
    def setUpClass(cls):
        try:
            import yaml  # PyYAML
        except ImportError:
            raise unittest.SkipTest(
                "PyYAML not installed -- authors_verified parity check "
                "skipped. Install with `pip install pyyaml` to enable it."
            )
        cls.yaml = yaml
        cls.meta_false = set()
        cls.skill_false = set()
        for meta in sorted(CORPUS.glob("*/*/metadata.yaml")):
            entry = str(meta.parent.relative_to(CORPUS))
            try:
                with open(meta) as f:
                    data = yaml.safe_load(f)
            except Exception:
                # YAML parseability is enforced by test_corpus_integrity;
                # parity check just skips unparseable entries.
                continue
            if isinstance(data, dict) and data.get("authors_verified") is False:
                cls.meta_false.add(entry)
        for skill in sorted(CORPUS.glob("*/*/SKILL.md")):
            entry = str(skill.parent.relative_to(CORPUS))
            text = skill.read_text()
            if not text.startswith("---\n"):
                continue
            try:
                end = text.index("\n---", 4)
            except ValueError:
                continue
            try:
                data = yaml.safe_load(text[4:end])
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            paper = data.get("paper")
            if not isinstance(paper, dict):
                continue
            if paper.get("authors_verified") is False:
                cls.skill_false.add(entry)


class TestMetadataImpliesSkillFlag(_ParityBase):
    """metadata.yaml authors_verified:false ==> SKILL paper.authors_verified:false."""

    def test_every_metadata_false_has_skill_false(self):
        missing = sorted(self.meta_false - self.skill_false)
        self.assertEqual(
            missing, [],
            msg=(
                f"{len(missing)} entries have metadata.yaml "
                f"authors_verified: false but SKILL.md frontmatter does NOT "
                f"have paper.authors_verified: false "
                f"(first 5: {missing[:5]})"
            ),
        )


class TestSkillFlagImpliesMetadata(_ParityBase):
    """SKILL paper.authors_verified:false ==> metadata.yaml authors_verified:false."""

    def test_every_skill_false_has_metadata_false(self):
        missing = sorted(self.skill_false - self.meta_false)
        self.assertEqual(
            missing, [],
            msg=(
                f"{len(missing)} entries have SKILL.md "
                f"paper.authors_verified: false but metadata.yaml does NOT "
                f"have top-level authors_verified: false "
                f"(first 5: {missing[:5]})"
            ),
        )


class TestParityCountsMatch(_ParityBase):
    """The two sets have identical size (redundant guard, but documents intent)."""

    def test_counts_match(self):
        self.assertEqual(
            len(self.meta_false), len(self.skill_false),
            msg=(
                f"authors_verified: false count mismatch: "
                f"metadata.yaml = {len(self.meta_false)}, "
                f"SKILL.md paper block = {len(self.skill_false)}; "
                f"see TestMetadataImpliesSkillFlag / "
                f"TestSkillFlagImpliesMetadata for offending entries."
            ),
        )


if __name__ == "__main__":
    unittest.main()
