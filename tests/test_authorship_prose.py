"""Consumer-facing authorship-prose hygiene tests (issue #55).

Sibling to ``tests/test_authorship_hygiene.py`` (issue #8), which guards
the YAML frontmatter / metadata.yaml ``first_author`` / ``authors[]``
fields. This module guards the *rendered prose* of per-entry SKILL.md
bodies and the per-batch ``manifest.json`` ``authors[]`` arrays against
two templated phrases inherited from the paper-to-skill factory:

  Pattern A — ``> Compiled from TODO verify (<...> authors) (YYYY), ...``
  Pattern B — ``A paper-skill compiled from [<real names>, ] + co-authors
              (TODO verify full list) et al. YYYY (...)``

Both phrases look like author lists in the rendered SKILL.md and so
mislead consumers; the existing S4d authorship-hygiene check does not
catch them because they live in the prose body, not the frontmatter.

The detector regexes here mirror those in
``scripts/audit_authorship_prose.py``; the script is the canonical
fixer (``--apply``) and this test is the regression guard. Non-author
TODO_verify markers elsewhere in the body (``TODO_verify_journal``,
``arxiv: TODO verify``, ``DOI: TODO verify``) are *intentional*
curation debt and are NOT flagged here.

This test also enforces the topic-skill `kind` distinction added for
issue #55: the aggregate entry ``paper-open-flux-problem-in-situ-vs-
pfss-discrepancy`` must declare ``kind: topic-skill`` in its
metadata.yaml so downstream tooling can refuse to apply paper-skill
invariants (e.g. requiring a single first author) to it.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"


PATTERN_A_RE = re.compile(
    r"Compiled from TODO verify \(([^)]*\bauthors?\b[^)]*)\) (\(\d{4}\)[,.])"
)
PATTERN_B_BARE_RE = re.compile(
    r"compiled from \+ co-authors \(TODO verify full list\) et al\.\s*(\d{4})"
)
PATTERN_B_NAMED_RE = re.compile(
    r"compiled from (.+?), \+ co-authors \(TODO verify full list\) et al\.\s*(\d{4})"
)
MANIFEST_PLACEHOLDER = "+ co-authors (TODO verify full list)"


def _skill_violations(text: str) -> list[str]:
    out: list[str] = []
    for m in PATTERN_A_RE.finditer(text):
        out.append(m.group(0))
    for m in PATTERN_B_NAMED_RE.finditer(text):
        out.append(m.group(0))
    stripped, _ = PATTERN_B_NAMED_RE.subn("", text)
    for m in PATTERN_B_BARE_RE.finditer(stripped):
        out.append(m.group(0))
    return out


class TestSkillBodyAuthorshipProse(unittest.TestCase):
    """No templated authorship placeholders in per-entry SKILL.md bodies."""

    def test_no_compiled_from_todo_verify_authors(self):
        violations = []
        for p in sorted(CORPUS.glob("*/*/SKILL.md")):
            text = p.read_text()
            for snippet in _skill_violations(text):
                violations.append(f"{p.relative_to(BUNDLE)}: {snippet[:140]}")
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} SKILL.md body authorship-prose "
                f"violations (issue #55) (first 5: {violations[:5]}). "
                f"Run `python3 scripts/audit_authorship_prose.py --apply` "
                f"to rewrite the templated phrases to non-author wording."
            ),
        )


class TestManifestAuthorsPlaceholder(unittest.TestCase):
    """No '+ co-authors (TODO verify full list)' in manifest authors[]."""

    def test_no_co_authors_placeholder_in_manifest_authors(self):
        violations = []
        for p in sorted(CORPUS.glob("*/manifest.json")):
            try:
                data = json.loads(p.read_text())
            except Exception:
                continue
            if isinstance(data, dict):
                entries = data.get("entries") or data.get("skills") or []
            else:
                entries = data
            if not isinstance(entries, list):
                continue
            for e in entries:
                if not isinstance(e, dict):
                    continue
                authors = e.get("authors")
                if not isinstance(authors, list):
                    continue
                for a in authors:
                    if isinstance(a, str) and MANIFEST_PLACEHOLDER in a:
                        violations.append(
                            f"{p.relative_to(BUNDLE)}: "
                            f"{e.get('slug', '<no-slug>')} authors[]: {a!r}"
                        )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} manifest.json authors[] placeholder "
                f"violations (issue #55) (first 5: {violations[:5]}). "
                f"Run `python3 scripts/audit_authorship_prose.py --apply` "
                f"to strip the placeholder strings and set "
                f"authors_complete: false."
            ),
        )


class TestKindDistinction(unittest.TestCase):
    """`kind` enum sanity and topic-skill exemplar (issue #55)."""

    # Known kinds in the corpus today. `paper-skill` is the dominant
    # value; `tool-skill` is used for software-only entries (e.g. helioml,
    # sktime); `topic-skill` was added for issue #55 to mark aggregate
    # entries that span multiple representative papers.
    ALLOWED_KINDS = {"paper-skill", "topic-skill", "tool-skill"}
    # Canonical topic-skill exemplar called out in issue #55. Renaming the
    # slug or removing the entry is allowed, but if it stays it MUST carry
    # `kind: topic-skill` in its metadata.yaml so paper-skill invariants
    # (e.g. requiring a single first_author or a single arXiv ID) do not
    # apply to it.
    TOPIC_SKILL_EXEMPLAR = (
        "wave500_solar_corona_cme_flares_045/"
        "paper-open-flux-problem-in-situ-vs-pfss-discrepancy"
    )

    @classmethod
    def setUpClass(cls):
        try:
            import yaml  # PyYAML
        except ImportError:
            raise unittest.SkipTest(
                "PyYAML not installed -- kind enum check skipped."
            )
        cls.yaml = yaml

    def test_metadata_kind_is_in_allowed_enum(self):
        bad = []
        for p in sorted(CORPUS.glob("*/*/metadata.yaml")):
            with open(p) as f:
                data = self.yaml.safe_load(f)
            if not isinstance(data, dict):
                continue
            kind = data.get("kind")
            if kind is None:
                continue  # legacy entries without a kind field are allowed
            if kind not in self.ALLOWED_KINDS:
                bad.append(f"{p.relative_to(BUNDLE)}: kind={kind!r}")
        self.assertEqual(
            bad, [],
            msg=(
                f"{len(bad)} metadata.yaml `kind:` values outside the "
                f"allowed enum {sorted(self.ALLOWED_KINDS)} "
                f"(first 5: {bad[:5]})"
            ),
        )

    def test_open_flux_aggregate_declares_topic_skill_kind(self):
        meta = CORPUS / self.TOPIC_SKILL_EXEMPLAR / "metadata.yaml"
        if not meta.is_file():
            self.skipTest(f"{self.TOPIC_SKILL_EXEMPLAR} not present")
        with open(meta) as f:
            data = self.yaml.safe_load(f)
        self.assertIsInstance(data, dict)
        self.assertEqual(
            data.get("kind"), "topic-skill",
            msg=(
                f"{meta.relative_to(BUNDLE)}: aggregate entry must declare "
                f"`kind: topic-skill` (issue #55); got {data.get('kind')!r}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
