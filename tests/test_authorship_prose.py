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


# -- Issue #55 follow-up: broader rendered factory-prose detectors ----------
#
# The patterns above (Pattern A with the literal word "authors" inside the
# parenthetical, Pattern B with "+ co-authors (TODO verify full list)") only
# catch a subset of the factory templating. After 4e1a75b the corpus still
# carries a wider family of consumer-visible placeholder prose in the
# rendered SKILL.md blockquote at the top of the body, e.g.
#
#   > Compiled from TODO verify (Xu / Borovsky collaboration) (2020),
#     "...", TODO verify (likely J. Geophys. Res. Space Phys.),
#     TODO verify arXiv ID.
#
# These do NOT contain the literal word "authors" in the parenthetical
# (the placeholder phrasing varies — "collaboration", "lineage",
# "successor", "MHD-emulator lineage", ...), and they all surface in the
# rendered body where an agent reads them as if they were a real citation.
#
# The detectors below run on the SKILL.md BODY only (text after the YAML
# frontmatter). They are intentionally NOT applied to:
#   - the YAML frontmatter (uncertainty markers there are honest:
#     ``authors_verified: false``, ``venue: "TODO verify ..."``, etc.);
#   - non-corpus files (CHANGELOG, README, this test file, fixtures).


def _skill_body(text: str) -> str:
    """Return the body of a SKILL.md (text after the YAML frontmatter).

    If no frontmatter delimiter is present the full text is returned.
    """
    if not text.startswith("---\n"):
        return text
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return text
    rest = text[end + len("\n---"):]
    # Drop the trailing newline after the closing '---' if present.
    return rest.lstrip("\n")


# Literal start of the templated factory citation. Anchored on the
# blockquote prefix so we only flag the rendered citation line, not e.g.
# an inline mention inside §8 Links or §9 affordances.
COMPILED_FROM_TODO_VERIFY_RE = re.compile(
    r"^>\s*Compiled from TODO verify\b", re.MULTILINE
)

# Trailing "TODO verify arXiv ID" placeholder anywhere in the body
# (typically the last token of the same blockquote line).
TODO_VERIFY_ARXIV_ID_RE = re.compile(r"\bTODO verify arXiv ID\b")

# Klein-2018 variant: "compiled from <Name>, + co-authors (TODO verify) et al. YYYY"
# Note the parenthetical is "(TODO verify)" without "full list", so the
# existing PATTERN_B_BARE / PATTERN_B_NAMED above miss it.
COMPILED_FROM_CO_AUTHORS_TODO_VERIFY_RE = re.compile(
    r"compiled from .+?,\s*\+ co-authors \(TODO verify\)\s*et al\.\s*\d{4}",
    re.IGNORECASE,
)


def _broader_body_violations(body: str) -> list[str]:
    """Detect broader factory-prose phrases in a SKILL.md body."""
    out: list[str] = []
    for m in COMPILED_FROM_TODO_VERIFY_RE.finditer(body):
        # Capture the rest of the line for the violation report.
        line_end = body.find("\n", m.end())
        if line_end == -1:
            line_end = len(body)
        out.append(body[m.start():line_end])
    for m in TODO_VERIFY_ARXIV_ID_RE.finditer(body):
        line_start = body.rfind("\n", 0, m.start()) + 1
        line_end = body.find("\n", m.end())
        if line_end == -1:
            line_end = len(body)
        out.append(body[line_start:line_end])
    for m in COMPILED_FROM_CO_AUTHORS_TODO_VERIFY_RE.finditer(body):
        out.append(m.group(0))
    return out


class TestSkillBodyBroaderFactoryProse(unittest.TestCase):
    """Issue #55 follow-up: no broader factory placeholder prose in bodies.

    Scope: only the per-entry SKILL.md body (text after the YAML
    frontmatter). Frontmatter ``venue: "TODO verify ..."`` and
    ``authors_verified: false`` are honest uncertainty markers and remain
    in scope of the existing S4d / S4f checks.
    """

    def test_no_compiled_from_todo_verify_blockquote(self):
        violations = []
        for p in sorted(CORPUS.glob("*/*/SKILL.md")):
            body = _skill_body(p.read_text())
            for m in COMPILED_FROM_TODO_VERIFY_RE.finditer(body):
                line_end = body.find("\n", m.end())
                if line_end == -1:
                    line_end = len(body)
                violations.append(
                    f"{p.relative_to(BUNDLE)}: {body[m.start():line_end][:140]}"
                )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} SKILL.md bodies start a blockquote "
                f"with the templated ``> Compiled from TODO verify ...`` "
                f"factory prose (issue #55 follow-up) "
                f"(first 5: {violations[:5]}). "
                f"Run `python3 scripts/audit_authorship_prose.py --apply` "
                f"to rewrite the citation line to non-placeholder wording."
            ),
        )

    def test_no_todo_verify_arxiv_id_in_body(self):
        violations = []
        for p in sorted(CORPUS.glob("*/*/SKILL.md")):
            body = _skill_body(p.read_text())
            for m in TODO_VERIFY_ARXIV_ID_RE.finditer(body):
                line_start = body.rfind("\n", 0, m.start()) + 1
                line_end = body.find("\n", m.end())
                if line_end == -1:
                    line_end = len(body)
                violations.append(
                    f"{p.relative_to(BUNDLE)}: {body[line_start:line_end][:140]}"
                )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} SKILL.md body lines still carry the "
                f"templated ``TODO verify arXiv ID`` factory placeholder "
                f"(issue #55 follow-up) (first 5: {violations[:5]}). "
                f"Run `python3 scripts/audit_authorship_prose.py --apply`."
            ),
        )

    def test_no_co_authors_todo_verify_bare_paren_in_body(self):
        violations = []
        for p in sorted(CORPUS.glob("*/*/SKILL.md")):
            body = _skill_body(p.read_text())
            for m in COMPILED_FROM_CO_AUTHORS_TODO_VERIFY_RE.finditer(body):
                violations.append(
                    f"{p.relative_to(BUNDLE)}: {m.group(0)[:140]}"
                )
        self.assertEqual(
            violations, [],
            msg=(
                f"{len(violations)} SKILL.md body lines carry the Klein-"
                f"style ``compiled from <name>, + co-authors (TODO verify) "
                f"et al. YYYY`` placeholder (issue #55 follow-up) "
                f"(first 5: {violations[:5]}). "
                f"Run `python3 scripts/audit_authorship_prose.py --apply`."
            ),
        )

    def test_audit_script_strict_exits_zero(self):
        """End-to-end: scripts/audit_authorship_prose.py --strict must pass."""
        import subprocess
        script = BUNDLE / "scripts" / "audit_authorship_prose.py"
        result = subprocess.run(
            ["python3", str(script), "--strict"],
            capture_output=True, text=True, cwd=str(BUNDLE),
        )
        self.assertEqual(
            result.returncode, 0,
            msg=(
                f"audit_authorship_prose.py --strict exited "
                f"{result.returncode}.\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
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
