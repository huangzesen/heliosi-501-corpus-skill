#!/usr/bin/env python3
"""Audit wiki-style ``[[target]]`` links across per-entry SKILL.md bodies.

Scope. Most ``HelioSI`` corpus cross-references live in prose as
``[[paper-foo-2025-bar]]`` (or occasionally ``[[paper-foo-2025-bar|label]]``)
inside the ``Layer 4`` and ``Skill graph → depends_on`` sections. These
links are not validated by any existing audit, so a typo or a slug that
was renamed during curation will look like a real edge in the skill graph
even when no such target exists in the manifest. This script resolves
every ``[[target]]`` against the canonical slug list in
``references/corpus_manifest_v2.json`` and reports:

  * total corpus entries / scanned files,
  * total wikilinks and unique targets,
  * resolved target count,
  * unresolved target count,
  * per-unresolved-target referring files (with 1-based line numbers and
    occurrence counts),
  * mechanical suggestions for unresolved targets (paper-prefix
    add/strip, and lowercase/non-alphanumeric-stripped slug normalization),
  * coverage of the prose-level ``Skill graph → depends_on`` section
    across the corpus (entries that carry such a section vs not).

The audit is read-only by default and exits 0 even when unresolved links
exist, so it can be wired into ``scripts/validate.sh`` as an informational
section without blocking CI on legacy curation debt. ``--strict`` flips
the exit code to 1 when there is at least one unresolved target.

Stdlib only -- no PyYAML, no third-party deps. Designed to mirror the
audit conventions of ``scripts/audit_numeric_claims.py`` /
``scripts/audit_title_unicode.py``.

Usage::

    python3 scripts/audit_wikilinks.py                 # human-readable
    python3 scripts/audit_wikilinks.py --json          # JSON to stdout
    python3 scripts/audit_wikilinks.py --output reports/wikilink_audit.json --json
    python3 scripts/audit_wikilinks.py --strict        # exit 1 on unresolved
    python3 scripts/audit_wikilinks.py \\
        --manifest references/corpus_manifest_v2.json \\
        --corpus references/corpus
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
DEFAULT_CORPUS = BUNDLE / "references" / "corpus"
DEFAULT_MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"

# Wiki-style link: [[target]] or [[target|display]]. The target is
# everything up to the first '|' or ']'. We deliberately do NOT allow
# nested brackets or newlines inside the target.
WIKILINK_RE = re.compile(r"\[\[([^\]\|\n]+?)(?:\|[^\]\n]*)?\]\]")

# Inline code span: a backtick-delimited run on a single line. Wikilinks
# that sit inside such a span are usually "example" or "placeholder"
# tokens being shown to the reader as literal text (e.g.
# ``Unresolved links remain as `[[slug]]` until they exist``) rather than
# real cross-references. We do NOT silently drop them — every occurrence
# is still recorded — but we tag each occurrence with ``in_inline_code``
# so a downstream consumer can decide whether to treat them as
# documentation samples.
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

# Header that introduces the prose ``Skill graph → depends_on`` section.
# Some entries use the unicode arrow, others use ``->`` or ``-``; allow
# both. We only care that the heading exists; the list under it is parsed
# as ordinary wikilinks.
DEPENDS_HEADER_RE = re.compile(
    r"^##\s*Skill\s*graph\s*(?:→|->|-)\s*depends_on\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def _normalize_slug(s: str) -> str:
    """Aggressive slug normalization used only for suggestion matching.

    Lowercases and strips every non-alphanumeric character. This lets us
    suggest ``paper-foo-bar`` as a match for a wikilink that wrote
    ``paper_foo_bar`` or ``Paper-Foo-Bar``. It is intentionally NOT used
    for canonical resolution -- a true resolved target must match a
    manifest slug exactly.
    """
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _load_manifest_slugs(manifest_path: Path) -> set[str]:
    if not manifest_path.is_file():
        raise SystemExit(
            f"audit_wikilinks.py: manifest not found: {manifest_path}"
        )
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)
    entries = data.get("entries", [])
    return {e["slug"] for e in entries if isinstance(e.get("slug"), str)}


def _iter_skill_files(corpus_root: Path):
    """Yield (relative_posix_path, absolute_path) for every per-entry
    ``SKILL.md`` under ``corpus_root``. The aggregator ``SKILL.md`` at the
    bundle root is *not* under ``corpus_root`` and is therefore excluded
    automatically."""
    if not corpus_root.is_dir():
        raise SystemExit(
            f"audit_wikilinks.py: corpus dir not found: {corpus_root}"
        )
    for p in sorted(corpus_root.glob("*/*/SKILL.md")):
        rel = p.relative_to(corpus_root).as_posix()
        yield rel, p


def _find_wikilinks(text: str):
    """Yield ``(target, line_number, in_inline_code)`` for every
    ``[[...]]`` in ``text``.

    ``line_number`` is 1-based and counts only lines (not bytes).
    ``in_inline_code`` is True when the wikilink's full ``[[...]]`` span
    is wholly contained inside a single-line backtick code span, e.g.
    ``Unresolved links remain as `[[slug]]` until they exist``. Whitespace
    inside the target is stripped.
    """
    code_spans = [(m.start(), m.end())
                  for m in INLINE_CODE_RE.finditer(text)]
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).strip()
        if not target:
            continue
        start, end = m.span()
        in_code = any(cs <= start and end <= ce
                      for cs, ce in code_spans)
        line_no = text.count("\n", 0, start) + 1
        yield target, line_no, in_code


def _suggest(unresolved_target: str, slug_set: set[str],
             normalized_index: dict) -> list[str]:
    """Return a deduplicated, ordered list of plausible canonical slugs
    for an unresolved wikilink target.

    Strategy (ordered by confidence):

      1. ``paper-`` prefix strip -- ``paper-foo`` -> ``foo``.
      2. ``paper-`` prefix add   -- ``foo`` -> ``paper-foo``.
      3. Normalized-slug lookup  -- same alphanumeric letters in the
         same order match a canonical slug.

    All suggestions are validated against ``slug_set`` before being
    returned. The function never invents a slug that does not already
    exist in the manifest.
    """
    suggestions: list[str] = []

    if unresolved_target.startswith("paper-"):
        stripped = unresolved_target[len("paper-"):]
        if stripped in slug_set and stripped not in suggestions:
            suggestions.append(stripped)
    else:
        added = "paper-" + unresolved_target
        if added in slug_set and added not in suggestions:
            suggestions.append(added)

    norm = _normalize_slug(unresolved_target)
    if norm:
        for cand in normalized_index.get(norm, ()):
            if cand not in suggestions:
                suggestions.append(cand)

    return suggestions


def compute_audit(
    corpus_root: Path,
    manifest_path: Path,
) -> dict:
    """Compute the wikilink audit summary as a plain dict.

    Returned schema (stable; consumers may rely on the top-level keys):

    .. code-block:: json

        {
          "schema_version": "wikilink-audit-1",
          "corpus_root": "references/corpus",
          "manifest_path": "references/corpus_manifest_v2.json",
          "totals": {
            "corpus_entries_in_manifest": 501,
            "skill_md_files_scanned": 501,
            "files_with_wikilinks": 442,
            "wikilink_occurrences": 1752,
            "wikilink_occurrences_in_inline_code": 648,
            "unique_targets": 336,
            "resolved_targets": 241,
            "unresolved_targets": 95,
            "depends_on_section_entries": 105
          },
          "unresolved": [
            {
              "target": "paper-foo",
              "occurrences": 3,
              "occurrences_in_inline_code": 0,
              "referrers": [
                {"path": "batch_x/slug/SKILL.md",
                 "line": 102, "in_inline_code": false},
                ...
              ],
              "suggestions": ["foo"]
            },
            ...
          ],
          "depends_on_coverage": {
            "with_section": ["batch_x/slug", ...],
            "without_section_count": 396
          }
        }
    """
    slug_set = _load_manifest_slugs(manifest_path)

    # Build a normalized-slug index once so the suggestion path is O(1)
    # per unresolved target rather than O(N) per target.
    normalized_index: dict[str, list[str]] = {}
    for s in slug_set:
        normalized_index.setdefault(_normalize_slug(s), []).append(s)
    for k in normalized_index:
        normalized_index[k].sort()

    # Map target -> list of {path, line, in_inline_code}. occurrences
    # inferred from len.
    occurrences: dict[str, list[dict]] = {}
    total_occurrences = 0
    in_code_occurrences = 0
    files_with_wikilinks = 0
    files_scanned = 0
    entries_with_depends_section: list[str] = []

    for rel, abs_path in _iter_skill_files(corpus_root):
        files_scanned += 1
        try:
            text = abs_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Falling back to latin-1 so a single bad byte does not stop
            # the audit. We intentionally don't report this as a problem
            # because it is out of scope for the wikilink graph.
            text = abs_path.read_text(encoding="latin-1")

        had_any = False
        for target, line_no, in_code in _find_wikilinks(text):
            occurrences.setdefault(target, []).append(
                {"path": rel, "line": line_no, "in_inline_code": in_code}
            )
            total_occurrences += 1
            if in_code:
                in_code_occurrences += 1
            had_any = True
        if had_any:
            files_with_wikilinks += 1

        if DEPENDS_HEADER_RE.search(text):
            # Strip the trailing /SKILL.md to record the entry id.
            entry_id = rel[:-len("/SKILL.md")] if rel.endswith(
                "/SKILL.md") else rel
            entries_with_depends_section.append(entry_id)

    unique_targets = sorted(occurrences.keys())
    resolved = [t for t in unique_targets if t in slug_set]
    unresolved = [t for t in unique_targets if t not in slug_set]

    unresolved_records = []
    for target in unresolved:
        refs = occurrences[target]
        in_code = sum(1 for r in refs if r["in_inline_code"])
        unresolved_records.append({
            "target": target,
            "occurrences": len(refs),
            "occurrences_in_inline_code": in_code,
            "referrers": refs,
            "suggestions": _suggest(target, slug_set, normalized_index),
        })
    # Stable order: most-occurring unresolved first, then alphabetical
    # for ties so the JSON output is deterministic.
    unresolved_records.sort(key=lambda r: (-r["occurrences"], r["target"]))

    summary = {
        "schema_version": "wikilink-audit-1",
        "corpus_root": str(corpus_root.relative_to(BUNDLE))
        if corpus_root.is_relative_to(BUNDLE) else str(corpus_root),
        "manifest_path": str(manifest_path.relative_to(BUNDLE))
        if manifest_path.is_relative_to(BUNDLE) else str(manifest_path),
        "totals": {
            "corpus_entries_in_manifest": len(slug_set),
            "skill_md_files_scanned": files_scanned,
            "files_with_wikilinks": files_with_wikilinks,
            "wikilink_occurrences": total_occurrences,
            "wikilink_occurrences_in_inline_code": in_code_occurrences,
            "unique_targets": len(unique_targets),
            "resolved_targets": len(resolved),
            "unresolved_targets": len(unresolved),
            "depends_on_section_entries": len(entries_with_depends_section),
        },
        "unresolved": unresolved_records,
        "depends_on_coverage": {
            "with_section": sorted(entries_with_depends_section),
            "without_section_count": files_scanned - len(
                entries_with_depends_section
            ),
        },
    }
    return summary


def _render_human(summary: dict) -> str:
    t = summary["totals"]
    lines = []
    lines.append("wikilink audit — heliosi-501-corpus")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"  corpus root        : {summary['corpus_root']}")
    lines.append(f"  manifest           : {summary['manifest_path']}")
    lines.append(f"  manifest entries   : {t['corpus_entries_in_manifest']}")
    lines.append(f"  SKILL.md scanned   : {t['skill_md_files_scanned']}")
    lines.append(
        f"  files w/ wikilinks : {t['files_with_wikilinks']}"
    )
    lines.append(
        f"  total wikilinks    : {t['wikilink_occurrences']}"
        f"  ({t['wikilink_occurrences_in_inline_code']} inside"
        f" inline `code` spans — likely doc/placeholder samples)"
    )
    lines.append(
        f"  unique targets     : {t['unique_targets']}"
    )
    lines.append(
        f"  resolved           : {t['resolved_targets']}"
    )
    lines.append(
        f"  unresolved         : {t['unresolved_targets']}"
    )
    lines.append(
        f"  depends_on section : {t['depends_on_section_entries']}"
        f" / {t['skill_md_files_scanned']} entries carry a"
        f" '## Skill graph → depends_on' section"
    )
    lines.append("")

    unresolved = summary["unresolved"]
    if not unresolved:
        lines.append("unresolved targets: none")
        return "\n".join(lines)

    lines.append(f"unresolved targets ({len(unresolved)}):")
    lines.append("-" * 72)
    for rec in unresolved:
        suff = (
            f"  ⟶ suggest: {', '.join(rec['suggestions'])}"
            if rec["suggestions"] else ""
        )
        code_note = (
            f" [{rec['occurrences_in_inline_code']} inline-code]"
            if rec["occurrences_in_inline_code"] else ""
        )
        lines.append(
            f"  ! [[{rec['target']}]] "
            f"({rec['occurrences']} occurrence"
            f"{'s' if rec['occurrences'] != 1 else ''}){code_note}"
            f"{suff}"
        )
        for ref in rec["referrers"][:5]:
            tag = " (in code)" if ref["in_inline_code"] else ""
            lines.append(
                f"      - {ref['path']}:{ref['line']}{tag}"
            )
        if len(rec["referrers"]) > 5:
            lines.append(
                f"      ... and {len(rec['referrers']) - 5} more"
            )
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="audit_wikilinks.py",
        description=(
            "Audit wiki-style [[target]] links in per-entry SKILL.md "
            "bodies against the canonical slugs in "
            "references/corpus_manifest_v2.json. Read-only and "
            "exit-0 by default; --strict makes unresolved targets a "
            "non-zero exit. Stdlib only."
        ),
    )
    p.add_argument(
        "--corpus",
        type=Path,
        default=DEFAULT_CORPUS,
        help=(
            "Path to the corpus root (default: "
            "references/corpus relative to the bundle). Must contain "
            "<batch>/<slug>/SKILL.md files."
        ),
    )
    p.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=(
            "Path to the corpus manifest JSON (default: "
            "references/corpus_manifest_v2.json)."
        ),
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a human report.",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Write the report to this file instead of stdout. Format is "
            "controlled by --json (JSON when set, otherwise plain text). "
            "Parent directories are created if missing."
        ),
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Exit 1 when there is at least one unresolved wikilink "
            "target. Default behaviour is exit 0 so this audit can be "
            "wired into validate.sh informationally."
        ),
    )
    args = p.parse_args(argv)

    summary = compute_audit(
        corpus_root=args.corpus.resolve(),
        manifest_path=args.manifest.resolve(),
    )

    if args.json:
        payload = json.dumps(summary, ensure_ascii=False, indent=2,
                             sort_keys=False)
    else:
        payload = _render_human(summary)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + ("\n" if not payload.endswith("\n")
                                          else ""),
                               encoding="utf-8")
    else:
        print(payload)

    if args.strict and summary["totals"]["unresolved_targets"] > 0:
        print(
            f"audit_wikilinks.py: FAIL — "
            f"{summary['totals']['unresolved_targets']} unresolved "
            f"wikilink target(s); see report above.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
