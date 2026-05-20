#!/usr/bin/env python3
"""Narrow, mechanical repair of ``paper-`` prefix drift in wikilinks.

Companion to ``scripts/audit_wikilinks.py``. The audit surfaces 95
unresolved wikilink targets in the live 501-entry corpus, dominated by
one drift class: a wikilink writes ``[[paper-foo]]`` but the canonical
manifest slug is the bare ``foo``. This script repairs exactly that
class, mechanically, and leaves everything else alone.

Safe-repair rule (this pass only)
---------------------------------

A target ``T`` is repaired to ``S`` only when ALL of these hold:

  1. ``T`` is unresolved (not a manifest slug).
  2. ``T`` starts with ``paper-``.
  3. The audit reports exactly ONE suggestion for ``T``.
  4. That single suggestion equals ``T`` with the ``paper-`` prefix
     stripped, i.e. the canonical paper-prefix repair (``paper-foo`` →
     ``foo``).
  5. The stripped target ``S`` is a canonical manifest slug.

Targets with no suggestion, multiple suggestions, normalised-slug
suggestions, or a single suggestion that is *paper-prefix-add* rather
than *paper-prefix-strip* are reported but never modified. The repair
never invents a slug -- every replacement points at a slug that already
exists in ``references/corpus_manifest_v2.json``.

Per-occurrence rules
--------------------

* A wikilink whose audit ``in_inline_code`` flag is True is NEVER
  rewritten. Inline-code wikilinks are documentation samples
  (``Unresolved links remain as `[[slug]]` until they exist``) and
  treating them as edges would silently turn placeholder text into a
  real cross-reference.
* When a target appears in BOTH prose and inline-code on different
  lines, only the prose occurrences are rewritten; the inline-code
  occurrences are preserved verbatim.
* Display labels are preserved: ``[[paper-foo|Foo (2025)]]`` becomes
  ``[[foo|Foo (2025)]]``.

Defaults and modes
------------------

* Default mode is **dry-run**: report the planned replacement set,
  affected file count, and skip reasons. No file is mutated.
* ``--apply`` is required to mutate files. The script computes the
  exact (path, line, column, original, replacement) plan first and only
  then rewrites; if anything changes between audit and apply the rule
  would still gate on (1)-(5) per occurrence.
* ``--json`` emits a machine-readable payload (default: human report).
* ``--output PATH`` writes to a file instead of stdout.

The script is stdlib-only -- no PyYAML, no third-party deps -- and
makes no network calls. It is deterministic on the same corpus +
manifest input.

Usage::

    python3 scripts/repair_wikilinks.py                    # dry-run, human
    python3 scripts/repair_wikilinks.py --json             # dry-run, JSON
    python3 scripts/repair_wikilinks.py --apply            # apply changes
    python3 scripts/repair_wikilinks.py --apply --json \\
        --output reports/wikilink_repair.json
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

PAPER_PREFIX = "paper-"


def _import_audit():
    """Re-use ``audit_wikilinks.compute_audit`` so the repair plan is
    derived from the same canonical analysis the audit reports. We
    import lazily so the script is still importable as a module from
    tests even if the audit module changes path-resolution rules."""
    sys.path.insert(0, str(HERE))
    try:
        import audit_wikilinks  # noqa: WPS433 -- intentional in-script import
    finally:
        # Do not pollute sys.path beyond the import.
        try:
            sys.path.remove(str(HERE))
        except ValueError:
            pass
    return audit_wikilinks


def _is_safe_paper_prefix_repair(record: dict, slug_set: set) -> tuple:
    """Return ``(eligible, reason, replacement_slug)`` for an unresolved
    audit record.

    ``eligible`` is True only when ALL of the safe-repair rules (1-5 in
    the module docstring) hold. ``reason`` is one of:

    * ``"ok"``                       -- eligible
    * ``"target-not-paper-prefix"``  -- the target itself does not start
                                        with ``paper-`` (e.g. separator
                                        drift like ``Paper_Foo_Bar``)
    * ``"no-suggestion"``            -- the audit had no suggestion
    * ``"multiple-suggestions"``     -- more than one suggestion
    * ``"not-paper-prefix-strip"``   -- single suggestion exists but it
                                        is not the bare ``paper-`` strip
    * ``"suggestion-not-on-manifest"`` -- defensive; should not happen
                                        because the audit validates
                                        suggestions against the manifest
    """
    target = record["target"]
    suggestions = record["suggestions"]

    # Classify by suggestion shape first so reviewers see why each
    # target was refused even when several rules apply at once.
    if not suggestions:
        return False, "no-suggestion", None
    if len(suggestions) > 1:
        return False, "multiple-suggestions", None
    if not target.startswith(PAPER_PREFIX):
        # Single suggestion exists but the target itself is not a
        # paper-prefix form -- e.g. separator drift (``Paper_Foo_Bar``)
        # caught by the normalised-slug heuristic. This pass refuses
        # any non-paper-prefix rewrite.
        return False, "not-paper-prefix-strip", None
    stripped = target[len(PAPER_PREFIX):]
    if suggestions[0] != stripped:
        # Target starts with ``paper-`` and has exactly one suggestion,
        # but that suggestion is not the bare ``paper-`` strip. For
        # example, a paper-prefix-ADD result (manifest has
        # ``paper-paper-foo`` and target was ``paper-foo``). Different
        # repair class -- this pass refuses it.
        return False, "not-paper-prefix-strip", None
    if stripped not in slug_set:
        return False, "suggestion-not-on-manifest", None
    return True, "ok", stripped


def _replace_in_text(text: str, target: str, replacement: str,
                     inline_code_lines: set) -> tuple:
    """Replace every ``[[target]]`` and ``[[target|label]]`` occurrence
    in ``text`` with ``[[replacement]]`` / ``[[replacement|label]]``,
    UNLESS the wikilink span sits inside a single-line backtick code
    span. Returns ``(new_text, n_replaced, n_skipped_inline)``.

    ``inline_code_lines`` is computed once per file from
    ``audit_wikilinks.INLINE_CODE_RE`` and is the set of ``(start, end)``
    character spans for each inline-code run.
    """
    pattern = re.compile(
        r"\[\[" + re.escape(target) + r"(\|[^\]\n]*)?\]\]"
    )
    n_replaced = 0
    n_skipped_inline = 0

    def _repl(m: re.Match) -> str:
        nonlocal n_replaced, n_skipped_inline
        start, end = m.span()
        in_code = any(cs <= start and end <= ce
                      for cs, ce in inline_code_lines)
        if in_code:
            n_skipped_inline += 1
            return m.group(0)
        label = m.group(1) or ""
        n_replaced += 1
        return f"[[{replacement}{label}]]"

    new_text = pattern.sub(_repl, text)
    return new_text, n_replaced, n_skipped_inline


def _build_repair_plan(audit_summary: dict, slug_set: set) -> tuple:
    """Classify every unresolved audit record into ``eligible_targets``
    (a list of ``{target, replacement, occurrences, prose_occurrences,
    inline_occurrences, referrers}``) and ``skipped_targets`` (a list of
    ``{target, occurrences, reason}``). Targets that are eligible by the
    rule but have zero prose occurrences (i.e. they are entirely inside
    inline-code spans) are demoted to ``skipped`` with reason
    ``all-inline-code``, since the per-occurrence rule would skip every
    occurrence anyway.
    """
    eligible_targets = []
    skipped_targets = []

    for rec in audit_summary["unresolved"]:
        ok, reason, replacement = _is_safe_paper_prefix_repair(rec, slug_set)
        if not ok:
            skipped_targets.append({
                "target": rec["target"],
                "occurrences": rec["occurrences"],
                "occurrences_in_inline_code":
                    rec["occurrences_in_inline_code"],
                "reason": reason,
                "suggestions": rec["suggestions"],
            })
            continue
        prose_occs = rec["occurrences"] - rec["occurrences_in_inline_code"]
        if prose_occs == 0:
            # Eligible by name but every reference is inside a backtick
            # span. The per-occurrence rule would skip them all; record
            # the skip honestly so the report shows them.
            skipped_targets.append({
                "target": rec["target"],
                "occurrences": rec["occurrences"],
                "occurrences_in_inline_code":
                    rec["occurrences_in_inline_code"],
                "reason": "all-inline-code",
                "suggestions": rec["suggestions"],
            })
            continue
        eligible_targets.append({
            "target": rec["target"],
            "replacement": replacement,
            "occurrences": rec["occurrences"],
            "prose_occurrences": prose_occs,
            "inline_occurrences": rec["occurrences_in_inline_code"],
            "referrers": rec["referrers"],
        })

    # Stable order: most-occurring eligible first, then alphabetical.
    eligible_targets.sort(
        key=lambda r: (-r["prose_occurrences"], r["target"])
    )
    skipped_targets.sort(key=lambda r: (-r["occurrences"], r["target"]))
    return eligible_targets, skipped_targets


def _files_to_touch(eligible_targets: list) -> dict:
    """Group eligible-target occurrences by the file that needs to be
    edited. Returns ``{rel_path: [(target, replacement), ...]}`` where
    each ``(target, replacement)`` appears once per file regardless of
    how many times the target occurs in that file (the regex sub on the
    file body handles all occurrences in one shot).
    """
    by_file: dict = {}
    for entry in eligible_targets:
        for ref in entry["referrers"]:
            if ref["in_inline_code"]:
                continue
            by_file.setdefault(ref["path"], [])
            tup = (entry["target"], entry["replacement"])
            if tup not in by_file[ref["path"]]:
                by_file[ref["path"]].append(tup)
    return by_file


def _execute_repairs(
    corpus_root: Path,
    by_file: dict,
    audit_module,
    apply_changes: bool,
) -> tuple:
    """Walk ``by_file`` and either compute (dry-run) or apply the file
    rewrites. Returns ``(planned, applied, files_affected, file_reports)``
    where ``file_reports`` is a per-file ``{path, target, replacement,
    occurrences_rewritten}`` list useful for the human report.
    """
    INLINE_CODE_RE = audit_module.INLINE_CODE_RE
    planned = 0
    applied = 0
    files_affected = 0
    file_reports: list = []

    for rel, edits in sorted(by_file.items()):
        abs_path = corpus_root / rel
        try:
            text = abs_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = abs_path.read_text(encoding="latin-1")

        code_spans = [(m.start(), m.end())
                      for m in INLINE_CODE_RE.finditer(text)]

        new_text = text
        per_file_count = 0
        for target, replacement in edits:
            new_text, n_replaced, _ = _replace_in_text(
                new_text, target, replacement, set(code_spans),
            )
            if n_replaced:
                per_file_count += n_replaced
                file_reports.append({
                    "path": rel,
                    "target": target,
                    "replacement": replacement,
                    "occurrences_rewritten": n_replaced,
                })
            # Recompute code spans against the NEW text so a subsequent
            # target in the same file does not pick up shifted offsets.
            code_spans = [(m.start(), m.end())
                          for m in INLINE_CODE_RE.finditer(new_text)]

        planned += per_file_count
        if per_file_count > 0:
            files_affected += 1
            if apply_changes and new_text != text:
                abs_path.write_text(new_text, encoding="utf-8")
                applied += per_file_count

    return planned, applied, files_affected, file_reports


def _render_human(payload: dict, eligible_targets: list,
                  skipped_targets: list,
                  file_reports: list) -> str:
    lines = []
    lines.append("wikilink repair (paper-prefix canonical pass)")
    lines.append("=" * 72)
    lines.append(f"  mode                 : {payload['mode']}")
    lines.append(f"  corpus root          : {payload['corpus_root']}")
    lines.append(f"  manifest             : {payload['manifest_path']}")
    lines.append(f"  unresolved before    : {payload['unresolved_before']}")
    lines.append(f"  unresolved after     : {payload['unresolved_after']}")
    lines.append(f"  eligible targets     : {len(eligible_targets)}")
    lines.append(f"  skipped targets      : {len(skipped_targets)}")
    lines.append(f"  planned replacements : {payload['planned_replacements']}")
    lines.append(f"  applied replacements : {payload['applied_replacements']}")
    lines.append(f"  files affected       : {payload['files_affected']}")
    lines.append("")

    if eligible_targets:
        lines.append(f"eligible targets ({len(eligible_targets)}):")
        lines.append("-" * 72)
        for r in eligible_targets:
            note = ""
            if r["inline_occurrences"]:
                note = (f" ({r['inline_occurrences']} inline-code "
                        f"occurrence(s) preserved)")
            lines.append(
                f"  * [[{r['target']}]] -> [[{r['replacement']}]]"
                f"  -- {r['prose_occurrences']} prose occurrence"
                f"{'s' if r['prose_occurrences'] != 1 else ''}{note}"
            )
        lines.append("")

    if skipped_targets:
        lines.append(f"skipped targets ({len(skipped_targets)}):")
        lines.append("-" * 72)
        by_reason: dict = {}
        for r in skipped_targets:
            by_reason.setdefault(r["reason"], []).append(r)
        for reason in sorted(by_reason):
            group = by_reason[reason]
            lines.append(f"  reason={reason} ({len(group)} target(s)):")
            for r in group[:10]:
                sugg = (f"  suggestions={r['suggestions']!r}"
                        if r["suggestions"] else "")
                lines.append(
                    f"      - [[{r['target']}]] "
                    f"({r['occurrences']} occurrence"
                    f"{'s' if r['occurrences'] != 1 else ''})"
                    f"{sugg}"
                )
            if len(group) > 10:
                lines.append(f"      ... and {len(group) - 10} more")
        lines.append("")

    if file_reports:
        lines.append(f"per-file plan ({len(file_reports)} edit(s)):")
        lines.append("-" * 72)
        for fr in file_reports[:20]:
            lines.append(
                f"  {fr['path']}: [[{fr['target']}]] -> "
                f"[[{fr['replacement']}]] x{fr['occurrences_rewritten']}"
            )
        if len(file_reports) > 20:
            lines.append(f"  ... and {len(file_reports) - 20} more")
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="repair_wikilinks.py",
        description=(
            "Mechanical, narrowly-scoped repair of ``paper-`` prefix "
            "drift in per-entry SKILL.md wikilinks. Default mode is "
            "dry-run; --apply is required to mutate files. Stdlib only."
        ),
    )
    p.add_argument(
        "--corpus",
        type=Path,
        default=DEFAULT_CORPUS,
        help=(
            "Path to the corpus root (default: references/corpus "
            "relative to the bundle)."
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
        "--apply",
        action="store_true",
        help=(
            "Apply the repair plan. Without this flag the script is a "
            "dry-run that only reports what would change."
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
            "controlled by --json. Parent directories are created."
        ),
    )
    args = p.parse_args(argv)

    audit_module = _import_audit()

    corpus_root = args.corpus.resolve()
    manifest_path = args.manifest.resolve()

    audit_summary = audit_module.compute_audit(
        corpus_root=corpus_root,
        manifest_path=manifest_path,
    )
    slug_set = audit_module._load_manifest_slugs(manifest_path)

    eligible_targets, skipped_targets = _build_repair_plan(
        audit_summary, slug_set,
    )
    by_file = _files_to_touch(eligible_targets)
    planned, applied, files_affected, file_reports = _execute_repairs(
        corpus_root=corpus_root,
        by_file=by_file,
        audit_module=audit_module,
        apply_changes=args.apply,
    )

    unresolved_before = audit_summary["totals"]["unresolved_targets"]
    # After we apply, the number of unresolved targets drops by exactly
    # the number of eligible target slugs (each one resolves to its
    # canonical slug). In dry-run mode we report the same hypothetical
    # delta -- the README/audit will show the same number after --apply.
    fully_repaired_targets = sum(
        1 for e in eligible_targets
        # A target is "fully repaired" if all of its prose occurrences
        # are rewritten and there are no other unrepaired occurrences.
        # Because the audit treats target identity as the string itself,
        # rewriting every prose occurrence of ``paper-X`` collapses the
        # unresolved entry (any remaining inline-code occurrences are
        # not edges; they remain reported as inline-code samples).
        if e["prose_occurrences"] > 0 and e["inline_occurrences"] == 0
    )
    # Targets that have BOTH prose and inline-code occurrences will
    # still appear as an unresolved entry after the prose rewrite,
    # because the inline-code placeholder still spells the old target.
    # The audit's `in_inline_code` accounting flags this honestly. We
    # therefore subtract only the targets whose every occurrence is
    # prose.
    unresolved_after = unresolved_before - fully_repaired_targets

    payload = {
        "schema_version": "wikilink-repair-1",
        "mode": "apply" if args.apply else "dry-run",
        "corpus_root": audit_summary["corpus_root"],
        "manifest_path": audit_summary["manifest_path"],
        "unresolved_before": unresolved_before,
        "unresolved_after": unresolved_after,
        "planned_replacements": planned,
        "applied_replacements": applied,
        "files_affected": files_affected,
        "eligible_targets": eligible_targets,
        "skipped_targets": skipped_targets,
        "file_edits": file_reports,
    }

    if args.json:
        out = json.dumps(payload, ensure_ascii=False, indent=2,
                         sort_keys=False)
    else:
        out = _render_human(payload, eligible_targets,
                            skipped_targets, file_reports)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            out + ("\n" if not out.endswith("\n") else ""),
            encoding="utf-8",
        )
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
