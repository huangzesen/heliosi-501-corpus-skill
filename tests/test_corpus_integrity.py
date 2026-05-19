"""Per-entry corpus integrity tests (issues #2 and #7).

Asserts two structural invariants across all 501 per-entry directories
under ``references/corpus/<batch>/<slug>/``:

1. Every ``SKILL.md`` carries a YAML frontmatter block delimited by ``---``
   on its own line, with a non-empty ``name:`` field (issue #2).
2. Every ``metadata.yaml`` parses as valid YAML (issue #7). This test is
   skipped if PyYAML is not installed -- PyYAML is not a runtime dependency
   of the bundle, but the CI workflow installs it so this check fires
   there.

Stdlib only at import time -- ``yaml`` is imported lazily inside the test
that uses it so an environment without PyYAML can still discover and run
the rest of the suite.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

EXPECTED_ENTRY_COUNT = 501


class TestPerEntrySkillFrontmatter(unittest.TestCase):
    """Issue #2 -- every per-entry SKILL.md must have a YAML frontmatter."""

    @classmethod
    def setUpClass(cls):
        cls.skill_files = sorted(CORPUS.glob("*/*/SKILL.md"))

    def test_exactly_501_per_entry_skill_files(self):
        self.assertEqual(
            len(self.skill_files), EXPECTED_ENTRY_COUNT,
            f"expected {EXPECTED_ENTRY_COUNT} per-entry SKILL.md files, "
            f"got {len(self.skill_files)}",
        )

    def test_every_skill_md_has_frontmatter_block(self):
        missing = []
        for p in self.skill_files:
            text = p.read_text()
            if not text.startswith("---\n"):
                missing.append(str(p.relative_to(BUNDLE)))
                continue
            try:
                text.index("\n---", 4)
            except ValueError:
                missing.append(str(p.relative_to(BUNDLE)))
        self.assertEqual(
            missing, [],
            f"{len(missing)} per-entry SKILL.md files lack a YAML frontmatter "
            f"block (first 5: {missing[:5]})",
        )

    def test_every_skill_md_frontmatter_has_nonempty_name(self):
        bad = []
        for p in self.skill_files:
            text = p.read_text()
            if not text.startswith("---\n"):
                # Caught by the previous test -- skip here to keep the
                # failure surface focused.
                continue
            try:
                end = text.index("\n---", 4)
            except ValueError:
                continue
            fm = text[4:end]
            name_lines = [
                ln for ln in fm.splitlines() if re.match(r"^name\s*:", ln)
            ]
            if not name_lines:
                bad.append(str(p.relative_to(BUNDLE)))
                continue
            val = name_lines[0].split(":", 1)[1].strip().strip('"').strip("'")
            if not val:
                bad.append(str(p.relative_to(BUNDLE)))
        self.assertEqual(
            bad, [],
            f"{len(bad)} per-entry SKILL.md frontmatter blocks are missing a "
            f"non-empty name: field (first 5: {bad[:5]})",
        )


class TestPerEntryMetadataYaml(unittest.TestCase):
    """Issue #7 -- every per-entry metadata.yaml must parse as valid YAML."""

    @classmethod
    def setUpClass(cls):
        cls.meta_files = sorted(CORPUS.glob("*/*/metadata.yaml"))

    def test_exactly_501_per_entry_metadata_files(self):
        self.assertEqual(
            len(self.meta_files), EXPECTED_ENTRY_COUNT,
            f"expected {EXPECTED_ENTRY_COUNT} per-entry metadata.yaml files, "
            f"got {len(self.meta_files)}",
        )

    def test_every_metadata_yaml_parses(self):
        try:
            import yaml  # PyYAML
        except ImportError:
            self.skipTest(
                "PyYAML not installed -- strict metadata.yaml parse check "
                "skipped. Install with `pip install pyyaml` to enable it."
            )
        bad = []
        for p in self.meta_files:
            try:
                with open(p) as f:
                    yaml.safe_load(f)
            except Exception as e:  # noqa: BLE001 -- want any parse failure
                bad.append((str(p.relative_to(BUNDLE)), str(e)[:160]))
        self.assertEqual(
            bad, [],
            f"{len(bad)} per-entry metadata.yaml files failed to parse "
            f"(first 5: {bad[:5]})",
        )


if __name__ == "__main__":
    unittest.main()
