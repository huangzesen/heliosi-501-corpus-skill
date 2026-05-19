"""Per-entry authorship-field hygiene tests (issue #8).

Mirrors ``scripts/validate.sh`` section S4d: asserts that the per-entry
``metadata.yaml`` and ``SKILL.md`` frontmatter blocks do not ship literal
``TODO`` / ``TBD`` author placeholders to consumers. Allowed authorship
states are ``null`` (scalar), ``[]`` / ``null`` (list), or a list of real
non-placeholder strings. Mixed lists like
``["Zhiheng Xi", "TODO_verify_with_full_text"]`` are forbidden -- the
placeholder element must be removed and the entry should set a sibling
``authors_complete: false`` (or equivalent) to preserve honesty about list
completeness; that sibling flag is a *recommendation* on the canonicalizer
side, not an invariant enforced here, because the invariant we care about
is the *absence* of TODO strings on the wire.

This check is skipped when PyYAML is not installed, mirroring the existing
``test_corpus_integrity.TestPerEntryMetadataYaml.test_every_metadata_yaml_parses``
behaviour.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

STARTS_TODO = re.compile(r"^\s*(?:TODO|TBD)", re.IGNORECASE)
PAREN_TODO = re.compile(r"\((?:[^)]*\b)?(?:TODO|TBD)\b[^)]*\)", re.IGNORECASE)


def is_todo_placeholder(s):
    if not isinstance(s, str):
        return False
    return bool(STARTS_TODO.search(s) or PAREN_TODO.search(s))


class _AuthorshipHygieneBase(unittest.TestCase):
    """Shared PyYAML import and violation collector."""

    @classmethod
    def setUpClass(cls):
        try:
            import yaml  # PyYAML
        except ImportError:
            raise unittest.SkipTest(
                "PyYAML not installed -- authorship hygiene check skipped. "
                "Install with `pip install pyyaml` to enable it."
            )
        cls.yaml = yaml

    def _violations_for(self, label, value, path):
        if value is None:
            return []
        if isinstance(value, list):
            out = []
            for i, elem in enumerate(value):
                if is_todo_placeholder(elem):
                    out.append(
                        f"{path.relative_to(BUNDLE)}: {label}[{i}] is a "
                        f"TODO/TBD placeholder: {elem!r}"
                    )
            return out
        if is_todo_placeholder(value):
            return [
                f"{path.relative_to(BUNDLE)}: {label} is a TODO/TBD "
                f"placeholder: {value!r}"
            ]
        return []


class TestMetadataAuthorshipHygiene(_AuthorshipHygieneBase):
    """No TODO/TBD placeholders in metadata.yaml first_author/authors."""

    def test_metadata_first_author_and_authors_have_no_placeholders(self):
        violations = []
        for p in sorted(CORPUS.glob("*/*/metadata.yaml")):
            with open(p) as f:
                data = self.yaml.safe_load(f)
            if not isinstance(data, dict):
                continue
            if "first_author" in data:
                violations.extend(
                    self._violations_for("first_author", data["first_author"], p)
                )
            if "authors" in data:
                violations.extend(
                    self._violations_for("authors", data["authors"], p)
                )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} metadata.yaml authorship-hygiene violations "
                f"(first 5: {violations[:5]})"
            ),
        )


class TestSkillFrontmatterAuthorshipHygiene(_AuthorshipHygieneBase):
    """No TODO/TBD placeholders in SKILL.md paper.first_author/paper.authors."""

    def test_skill_paper_first_author_and_authors_have_no_placeholders(self):
        violations = []
        for p in sorted(CORPUS.glob("*/*/SKILL.md")):
            text = p.read_text()
            if not text.startswith("---\n"):
                continue
            try:
                end = text.index("\n---", 4)
            except ValueError:
                continue
            fm = text[4:end]
            data = self.yaml.safe_load(fm)
            if not isinstance(data, dict):
                continue
            paper = data.get("paper") or {}
            if not isinstance(paper, dict):
                continue
            if "first_author" in paper:
                violations.extend(
                    self._violations_for(
                        "paper.first_author", paper["first_author"], p
                    )
                )
            if "authors" in paper:
                violations.extend(
                    self._violations_for("paper.authors", paper["authors"], p)
                )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} SKILL.md authorship-hygiene violations "
                f"(first 5: {violations[:5]})"
            ),
        )


class TestPlaceholderDetector(unittest.TestCase):
    """Unit tests for the placeholder detector itself."""

    def test_starts_todo_family(self):
        for s in [
            "TODO verify",
            "TODO_verify",
            "TODO_verify_with_full_text",
            "  TODO verify",
            "tbd",
            "TBD",
        ]:
            with self.subTest(s=s):
                self.assertTrue(is_todo_placeholder(s))

    def test_parenthetical_todo_family(self):
        for s in [
            "Mason, G. M. (TODO verify)",
            "+ co-authors (TODO verify full list)",
            "PlasmaPy contributors (TODO enumerate from repo)",
        ]:
            with self.subTest(s=s):
                self.assertTrue(is_todo_placeholder(s))

    def test_real_authors_are_not_placeholders(self):
        for s in [
            "Bobra, M. G.",
            "Zhiheng Xi",
            "NASA SPDF team (data archive; no software publication)",
            "C. Cuddy",
        ]:
            with self.subTest(s=s):
                self.assertFalse(is_todo_placeholder(s))

    def test_non_strings_are_not_placeholders(self):
        for v in [None, [], 0, 2026, {}, True]:
            with self.subTest(v=v):
                self.assertFalse(is_todo_placeholder(v))


if __name__ == "__main__":
    unittest.main()
