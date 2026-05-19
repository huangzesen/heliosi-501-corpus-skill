"""Authorship-field hygiene tests (issues #8 and #65).

Mirrors ``scripts/validate.sh`` sections S4d and S4i: asserts that
per-entry ``metadata.yaml`` / ``SKILL.md`` frontmatter blocks **and**
per-batch ``manifest.json`` files do not ship literal ``TODO`` / ``TBD``
/ ``+ co-authors`` author placeholders to consumers. Allowed authorship
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
behaviour. The manifest.json check is stdlib-only.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

STARTS_TODO = re.compile(r"^\s*(?:TODO|TBD)", re.IGNORECASE)
PAREN_TODO = re.compile(r"\((?:[^)]*\b)?(?:TODO|TBD)\b[^)]*\)", re.IGNORECASE)
# "+ co-authors", "+ co-authors per inventory", "+ FIELDS team co-authors" --
# template-only stand-ins for an unverified author tail. These are not real
# names and must never appear on the wire even without a TODO marker.
CO_AUTHORS = re.compile(r"\+\s*[^()]*\bco-?authors\b", re.IGNORECASE)


def is_todo_placeholder(s):
    if not isinstance(s, str):
        return False
    return bool(
        STARTS_TODO.search(s)
        or PAREN_TODO.search(s)
        or CO_AUTHORS.search(s)
    )


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


class TestManifestAuthorshipHygiene(unittest.TestCase):
    """No TODO/TBD/+ co-authors placeholders in per-batch manifest.json
    author-related fields (issue #65). This is the machine-readable
    corpus-integrity invariant for downstream consumers that ingest the
    per-batch manifests.

    We walk every value in every per-batch manifest.json and flag a
    violation whenever any ancestor key in its dotted path contains the
    substring ``author`` (case-insensitive) -- this covers ``first_author``,
    ``lead_author``, ``authors[]``, and any future ``*author*`` field
    without enumerating them. Stdlib-only.
    """

    AUTHOR_KEY = re.compile(r"author", re.IGNORECASE)

    def _walk(self, node, key_path, hits):
        if isinstance(node, dict):
            for k, v in node.items():
                self._walk(v, key_path + [str(k)], hits)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                self._walk(v, key_path + [f"[{i}]"], hits)
        else:
            if not any(self.AUTHOR_KEY.search(p) for p in key_path):
                return
            if is_todo_placeholder(node):
                hits.append((".".join(key_path), node))

    def test_manifest_author_fields_have_no_placeholders(self):
        manifests = sorted(CORPUS.glob("*/manifest.json"))
        self.assertGreater(
            len(manifests), 0,
            msg="no per-batch manifest.json files found under references/corpus/",
        )
        violations = []
        for mf in manifests:
            with open(mf) as f:
                data = json.load(f)
            hits = []
            self._walk(data, [], hits)
            for path, val in hits:
                violations.append(
                    f"{mf.relative_to(BUNDLE)}: {path} is an authorship "
                    f"placeholder: {val!r}"
                )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} manifest.json authorship-hygiene "
                f"violations (first 10: {violations[:10]})"
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
            "Stoffel, T. (TODO verify list)",
            "W. Sun (et al., TODO verify)",
            "TODO_verify (canonical: Antonucci 2020)",
            "TODO_verify_with_full_text",
        ]:
            with self.subTest(s=s):
                self.assertTrue(is_todo_placeholder(s))

    def test_co_authors_template_family(self):
        for s in [
            "+ co-authors",
            "+ co-authors per inventory",
            "+ co-authors (TODO verify)",
            "+ FIELDS team co-authors (TODO verify)",
            "+ SpacePy contributors (TODO verify full list)",
            "+coauthors",
        ]:
            with self.subTest(s=s):
                self.assertTrue(is_todo_placeholder(s))

    def test_real_authors_are_not_placeholders(self):
        for s in [
            "Bobra, M. G.",
            "Zhiheng Xi",
            "NASA SPDF team (data archive; no software publication)",
            "C. Cuddy",
            "et al.",
            "Stoffel, T.",
            "W. Sun",
        ]:
            with self.subTest(s=s):
                self.assertFalse(is_todo_placeholder(s))

    def test_non_strings_are_not_placeholders(self):
        for v in [None, [], 0, 2026, {}, True]:
            with self.subTest(v=v):
                self.assertFalse(is_todo_placeholder(v))


if __name__ == "__main__":
    unittest.main()
