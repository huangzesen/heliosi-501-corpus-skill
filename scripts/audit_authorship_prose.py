#!/usr/bin/env python3
"""Audit and (optionally) rewrite consumer-facing authorship placeholders.

Issue #55: several per-entry SKILL.md files ship templated phrases in their
visible prose that *look like* author lists but are in fact placeholders
inherited from the paper-to-skill factory. Concretely, two templated
patterns are produced by the factory and surface to the agent in the
rendered SKILL.md body (not the YAML frontmatter):

  Pattern A — "Compiled from TODO verify (... authors) (YYYY)"
      e.g. `> Compiled from TODO verify (CIPHER authors) (2025), "...",`
           `TODO verify, arXiv:2510.21022.`
      Found in ~21 per-entry SKILL.md files under
      ``wave500_sw_classification_ml_foundation_045/``.

  Pattern B — "A paper-skill compiled from [<real names>, ] + co-authors
              (TODO verify full list) et al. YYYY (...)"
      e.g. `A paper-skill compiled from + co-authors (TODO verify full`
           `list) et al. 2024 (TODO_verify_journal; arXiv:2412.07451).`
      Found in ~36 per-entry SKILL.md files under
      ``wave500_waves_instabilities_reconnection_045/`` and in two
      manifest.json ``authors[]`` arrays (batch_heliophysics_software
      _infrastructure / pilot_2026_and_runtime).

Both phrases are *templated* (not author-supplied data); they are honest
about being unverified, but they read as if they were the author list.
Issue #55 specifically calls this out as a UX problem and asks for the
visible authorship placeholders to be removed from consumer-facing prose
while preserving honesty about the unverified state.

This audit:

  1. Locates every occurrence of the two patterns in SKILL.md bodies
     and in any per-batch ``manifest.json`` ``authors[]`` arrays.
  2. In ``--apply`` mode, rewrites them to non-author wording that
     preserves the rest of the sentence (year, arXiv id, journal
     placeholder, real co-author names if any).
  3. Emits a non-zero exit status if any unrewritten occurrences remain
     after the audit, so CI / ``validate.sh`` can use it as a regression
     guard.

Allowed (NOT rewritten by this script):
  - non-authorship TODO_verify markers (e.g. ``TODO_verify_journal``,
    ``TODO verify arXiv ID``, ``DOI: TODO verify``) — those are
    intentional curation debt outside the issue-#55 class.
  - ``authors: []`` / ``authors_verified: false`` in YAML — those are
    *already* honest and the right way to encode the unverified state.

This is stdlib-only; the rewrites are line-based to keep the diff
minimal and review-able.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"


# Pattern A: "Compiled from TODO verify (<anything> authors[ <anything>]) (YYYY)..."
# We anchor on "Compiled from TODO verify (" + a parenthetical that contains
# the literal word "authors". The trailing year + rest of the sentence is
# preserved by capturing it.
PATTERN_A_RE = re.compile(
    r"Compiled from TODO verify \(([^)]*\bauthors?\b[^)]*)\) (\(\d{4}\)[,.])"
)

# Pattern B (bare): "compiled from + co-authors (TODO verify full list) et al. YYYY"
PATTERN_B_BARE_RE = re.compile(
    r"compiled from \+ co-authors \(TODO verify full list\) et al\.\s*(\d{4})"
)
# Pattern B (named-prefix): "compiled from <Name(s)>, + co-authors (TODO verify full list) et al. YYYY"
# We require a comma + space before "+ co-authors" so the captured prefix
# always ends with a real author token.
PATTERN_B_NAMED_RE = re.compile(
    r"compiled from (.+?), \+ co-authors \(TODO verify full list\) et al\.\s*(\d{4})"
)

# Manifest authors[] placeholder string. We match the exact literal so we do
# not accidentally rewrite a real author whose surname happens to include
# substrings of the placeholder.
MANIFEST_PLACEHOLDER = "+ co-authors (TODO verify full list)"


def rewrite_pattern_a(text: str) -> tuple[str, int]:
    """Strip the false-author parenthetical from `Compiled from TODO verify ...`.

    Before:  ``> Compiled from TODO verify (CIPHER authors) (2025), "...",``
    After:   ``> Compiled from the primary source (authorship pending``
             ``verification) (2025), "...",``

    The rewrite keeps the year and the rest of the citation line intact and
    only removes the parenthetical that claimed to name authors.
    """
    def _sub(m: re.Match) -> str:
        year_paren = m.group(2)
        return f"Compiled from the primary source (authorship pending verification) {year_paren}"
    return PATTERN_A_RE.subn(_sub, text)


def rewrite_pattern_b(text: str) -> tuple[str, int]:
    """Strip the `+ co-authors (TODO verify full list)` placeholder.

    Two cases:
      (1) bare: "compiled from + co-authors (TODO verify full list) et al. YYYY"
          → "compiled from the primary source (author list pending verification), YYYY"
      (2) named-prefix: "compiled from N1, N2, + co-authors (TODO verify full list) et al. YYYY"
          → "compiled from N1, N2, et al., YYYY (full author list pending verification)"

    The named-prefix case is rewritten FIRST so we do not double-match the
    bare regex on the same line.
    """
    total = 0

    def _named(m: re.Match) -> str:
        prefix = m.group(1).strip()
        year = m.group(2)
        return f"compiled from {prefix}, et al., {year} (full author list pending verification)"

    text, n1 = PATTERN_B_NAMED_RE.subn(_named, text)
    total += n1

    def _bare(m: re.Match) -> str:
        year = m.group(1)
        return f"compiled from the primary source (author list pending verification), {year}"

    text, n2 = PATTERN_B_BARE_RE.subn(_bare, text)
    total += n2

    return text, total


def rewrite_skill_body(text: str) -> tuple[str, int]:
    """Apply both pattern rewrites to a SKILL.md body."""
    text, na = rewrite_pattern_a(text)
    text, nb = rewrite_pattern_b(text)
    return text, na + nb


def find_skill_violations(text: str) -> list[str]:
    """Return a list of violating snippets from a SKILL.md body."""
    out: list[str] = []
    for m in PATTERN_A_RE.finditer(text):
        out.append(m.group(0))
    for m in PATTERN_B_NAMED_RE.finditer(text):
        out.append(m.group(0))
    # PATTERN_B_BARE_RE can overlap PATTERN_B_NAMED_RE on the same input string
    # (the named pattern consumes the bare one if a name prefix exists), so
    # only report bare matches on text where the named pattern did not match.
    # Easier: compute bare matches on a copy where named matches were stripped.
    stripped, _ = PATTERN_B_NAMED_RE.subn("", text)
    for m in PATTERN_B_BARE_RE.finditer(stripped):
        out.append(m.group(0))
    return out


def find_manifest_violations(data) -> list[str]:
    """Return a list of placeholder snippets from a manifest.json structure."""
    out: list[str] = []
    if isinstance(data, dict):
        entries = data.get("entries") or data.get("skills") or []
    elif isinstance(data, list):
        entries = data
    else:
        return out
    if not isinstance(entries, list):
        return out
    for e in entries:
        if not isinstance(e, dict):
            continue
        authors = e.get("authors")
        if isinstance(authors, list):
            for a in authors:
                if isinstance(a, str) and MANIFEST_PLACEHOLDER in a:
                    slug = e.get("slug", "<no-slug>")
                    out.append(f"{slug}: authors[] contains {a!r}")
    return out


def rewrite_manifest_text(text: str) -> tuple[str, int]:
    """Strip the templated placeholder element from manifest.json text.

    Uses a line/string-level transform instead of a full JSON round-trip
    so the diff stays minimal and reviewable (json.dump otherwise
    reformats every inline ``authors`` array to a multi-line block).

    Two surface forms appear in the corpus:

      (1) Inline:   ``"authors": ["Bobra, M. G.", "+ co-authors (TODO verify full list)"],``
          → ``"authors": ["Bobra, M. G."],``

      (2) Own line: ``        "+ co-authors (TODO verify full list)"``      (last element, no comma)
          or       ``        "+ co-authors (TODO verify full list)",``     (not-last element)
          → entire line removed; if the line above had a dangling comma
            (because the placeholder was the new last element) the comma
            is also stripped.

    Returns (new_text, num_edits).
    """
    edits = 0

    # Pass A: own-line occurrences. Remove the line (with surrounding
    # whitespace and trailing newline). Then strip a dangling comma on
    # the preceding non-blank line if the placeholder was the last array
    # element (heuristic: if the next non-blank line is a closing `]`).
    new_lines: list[str] = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped in (
            f'"{MANIFEST_PLACEHOLDER}"',
            f'"{MANIFEST_PLACEHOLDER}",',
        ):
            # Look ahead: if the next non-blank line starts with `]`, then
            # the placeholder was the last array element and we must drop
            # the trailing comma on the previous emitted line.
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            next_non_blank = lines[j].lstrip() if j < len(lines) else ""
            placeholder_was_last = (
                stripped == f'"{MANIFEST_PLACEHOLDER}"'
                and next_non_blank.startswith("]")
            )
            if placeholder_was_last and new_lines and new_lines[-1].rstrip().endswith(","):
                # Strip trailing comma on previous emitted line.
                prev = new_lines[-1]
                new_lines[-1] = prev.rstrip()[:-1] + prev[len(prev.rstrip()):]
            edits += 1
            i += 1
            continue
        new_lines.append(line)
        i += 1
    text2 = "\n".join(new_lines)

    # Pass B: inline occurrences inside a one-line authors array.
    #   "authors": ["Bobra, M. G.", "+ co-authors (TODO verify full list)"],
    # The regex below removes the placeholder element and a preceding
    # comma+space (or a following comma+space if it was first), inside
    # a square-bracket array on the same physical line.
    inline_pat = re.compile(
        r',\s*"\+ co-authors \(TODO verify full list\)"'  # trailing element
        r'|"\+ co-authors \(TODO verify full list\)"\s*,\s*'  # leading element
    )
    text3, n_inline = inline_pat.subn("", text2)
    edits += n_inline

    return text3, edits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--apply", action="store_true",
        help="Rewrite SKILL.md and manifest.json files in place. Without "
             "this flag, the script only audits and prints a report.",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit non-zero if any violations remain after the audit. "
             "Used by validate.sh / CI as a regression guard.",
    )
    args = parser.parse_args()

    skill_violations: list[tuple[Path, list[str]]] = []
    skill_rewrites = 0
    rewritten_skill_files: list[Path] = []

    for p in sorted(CORPUS.glob("*/*/SKILL.md")):
        text = p.read_text()
        if args.apply:
            new_text, n = rewrite_skill_body(text)
            if n > 0:
                p.write_text(new_text)
                skill_rewrites += n
                rewritten_skill_files.append(p)
                text = new_text
        v = find_skill_violations(text)
        if v:
            skill_violations.append((p, v))

    manifest_violations: list[tuple[Path, list[str]]] = []
    manifest_rewrites = 0
    rewritten_manifests: list[Path] = []

    for p in sorted(CORPUS.glob("*/manifest.json")):
        text = p.read_text()
        if args.apply:
            new_text, n = rewrite_manifest_text(text)
            if n > 0:
                # Sanity: the rewrite must still parse as valid JSON.
                try:
                    json.loads(new_text)
                except Exception as e:
                    print(f"WARN: {p}: post-rewrite JSON parse failure ({e}); "
                          f"reverting", file=sys.stderr)
                else:
                    p.write_text(new_text)
                    manifest_rewrites += n
                    rewritten_manifests.append(p)
                    text = new_text
        if MANIFEST_PLACEHOLDER in text:
            # Re-locate violating slugs by parsing post-edit JSON.
            try:
                data = json.loads(text)
            except Exception as e:
                manifest_violations.append((p, [f"<post-edit JSON parse failure: {e}>"]))
                continue
            v = find_manifest_violations(data)
            if v:
                manifest_violations.append((p, v))

    print(f"== authorship-prose audit ==")
    print(f"SKILL.md scanned: {len(list(CORPUS.glob('*/*/SKILL.md')))}")
    print(f"manifest.json scanned: {len(list(CORPUS.glob('*/manifest.json')))}")
    if args.apply:
        print(f"SKILL.md rewrites applied: {skill_rewrites} edits across "
              f"{len(rewritten_skill_files)} files")
        print(f"manifest.json rewrites applied: {manifest_rewrites} entries "
              f"across {len(rewritten_manifests)} files")
    if skill_violations:
        print(f"\nremaining SKILL.md violations: {len(skill_violations)} files")
        for p, snippets in skill_violations[:10]:
            print(f"  - {p.relative_to(BUNDLE)}")
            for s in snippets[:2]:
                print(f"      {s[:110]}")
        if len(skill_violations) > 10:
            print(f"  ... and {len(skill_violations) - 10} more files")
    if manifest_violations:
        print(f"\nremaining manifest.json violations: {len(manifest_violations)} files")
        for p, snippets in manifest_violations:
            print(f"  - {p.relative_to(BUNDLE)}")
            for s in snippets:
                print(f"      {s}")

    if args.strict and (skill_violations or manifest_violations):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
