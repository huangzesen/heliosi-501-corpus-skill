#!/usr/bin/env python3
"""Emit a machine-readable corpus skill graph.

Reads the canonical manifest at
``references/corpus_manifest_v2.json`` and the wikilink-audit
computation in ``scripts/audit_wikilinks.py`` (imported directly --
not duplicated) and writes a single JSON artifact at
``references/corpus_skill_graph.json`` that joins manifest *nodes*
with the *resolved* ``[[target]]`` edges discovered in per-entry
``SKILL.md`` bodies. Unresolved references are NOT silently dropped:
they are preserved verbatim alongside the audit's suggestions and
sorted into conservative classification buckets so a downstream
consumer can tell honest curation debt apart from doc placeholders.

Honesty boundary. The audit cannot tell -- and neither can this
builder -- whether a ``paper-foo`` wikilink that does not resolve is a
typo, a slug that was renamed during curation, or a future paper that
was never internalized. The graph therefore exposes:

  * ``edges``: only wikilinks whose target is a canonical manifest slug
    AND whose ``[[...]]`` is NOT wholly contained inside an inline-code
    span (the audit's ``in_inline_code`` flag);
  * ``unresolved_references``: every unresolved wikilink target the
    audit reports, with its occurrences / referrers / suggestions
    forwarded verbatim plus a non-authoritative ``classification``
    label;
  * ``external_reference_candidates``: a roll-up of unresolved targets
    that look like runtime / tool names (no ``paper-`` prefix and no
    audit suggestion) -- useful as a pointer to off-corpus
    infrastructure, but explicitly flagged as non-authoritative.

The artifact is deliberately a *current snapshot*, not a proof of
corpus completeness. See ``GRAPH_POLICY.md`` for the curation policy
that governs how the graph is allowed to grow.

Stdlib only -- no PyYAML, no third-party deps. Designed to be wired
into ``scripts/validate.sh`` as a smoke check, not a hard gate.

Usage::

    python3 scripts/build_corpus_skill_graph.py
    python3 scripts/build_corpus_skill_graph.py \\
        --output references/corpus_skill_graph.json
    python3 scripts/build_corpus_skill_graph.py --no-timestamp
    python3 scripts/build_corpus_skill_graph.py --stdout
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
DEFAULT_CORPUS = BUNDLE / "references" / "corpus"
DEFAULT_MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"
# Default output is ``corpus_skill_graph.json`` next to the manifest --
# computed from --manifest at runtime so the default is consistent
# whether the script is run from the bundle or from a tempdir test
# fixture.

# Reuse audit_wikilinks.compute_audit so we never reimplement the
# wikilink regex / inline-code detection / suggestion heuristic. This
# also pins the audit + graph schemas together: if the audit grows a
# new field, the graph builder picks it up automatically.
sys.path.insert(0, str(HERE))
from audit_wikilinks import (  # noqa: E402  (deliberate post-sys.path import)
    compute_audit,
    DEPENDS_HEADER_RE,
)


SCHEMA_VERSION = "corpus-skill-graph-1"

# Fields we forward verbatim from manifest entries onto nodes. Fields
# absent from a particular entry are written as ``null`` rather than
# guessed.
NODE_MANIFEST_FIELDS = (
    "slug",
    "batch",
    "path",
    "title",
    "first_author",
    "year",
    "venue",
    "doi",
    "arxiv",
    "theme",
    "source_type",
    "quality",
    "executable_status",
    "harness_agnostic",
    "layers",
    "research_generation_affordances_present",
    "research_generation_affordances_count",
    "weak_flag_count",
)

LIMITATIONS = [
    "edges: only wikilinks whose target resolves to a canonical manifest slug "
    "and whose [[...]] is NOT wholly inside an inline-code span are emitted. "
    "Inline-code placeholders are intentionally excluded (counted under "
    "totals.edges_inline_code_excluded).",
    "unresolved_references is a verbatim forwarding of the wikilink-audit "
    "unresolved set with a conservative classification label. The "
    "classification is non-authoritative; closing each entry is a content "
    "decision, not a mechanical one.",
    "external_reference_candidates is a roll-up of unresolved targets that "
    "look like off-corpus runtime / tool / loader names (no paper- prefix "
    "and no audit suggestion). The roll-up is informational only and MUST "
    "NOT be treated as a list of node identifiers.",
    "edge.provenance[].context distinguishes 'depends_on_section' (the "
    "wikilink sits under a '## Skill graph -> depends_on' header) from "
    "'wikilink_prose' (every other resolved wikilink). The depends_on "
    "section is the current convention for declaring intra-corpus edges; "
    "prose links are real edges too, just less explicitly typed.",
    "this artifact is a CURRENT SNAPSHOT, not a proof of corpus "
    "completeness. See GRAPH_POLICY.md for the curation policy.",
]


def _classify_unresolved(rec: dict) -> str:
    """Return a conservative classification label for an unresolved
    wikilink-audit record.

    The labels are deliberately conservative -- they describe what we
    can tell *from the audit alone*, not what the wikilink was meant to
    point at. Buckets:

    * ``inline_code_literal`` -- every occurrence sits inside a
      code-sample context (a single-line backtick span OR a multi-line
      ``` fenced block) AND the audit has no suggestion. Almost always
      a placeholder example (``Unresolved links remain as `[[slug]]`
      ...``) or an in-snippet token (e.g. a pandas-style column index
      that happens to parse as a wikilink). The bucket name is
      retained for backwards compatibility with consumers of the
      ``corpus-skill-graph-1`` schema; the predicate is broadened to
      cover both inline-code spans and fenced blocks.
    * ``inline_code_canonical_suggestion`` -- every occurrence sits
      inside a code-sample context AND the audit has at least one
      suggestion. Typically a doc snippet showing the legacy form of a
      slug that now exists under a canonical name; the snippet is not
      really an edge.
    * ``paper_reference_needs_curation`` -- target starts with
      ``paper-``, has at least one prose (non-code-sample) occurrence,
      and the audit has no mechanical suggestion. This is honest
      curation debt: the wikilink looks like a paper-skill reference
      that does not exist in the manifest under any prefix variation.
    * ``external_reference_candidate`` -- target does NOT start with
      ``paper-``, has at least one prose occurrence, and the audit has
      no mechanical suggestion. Usually a runtime / tool / loader
      name (``pfss-tracing``, ``nspf-fem``, ``psp-sweap-bulk-loader``)
      that the corpus refers to as off-bundle infrastructure rather
      than as a peer paper-skill.
    * ``unresolved_no_suggestion`` -- a fallback so the classification
      function is total. Should rarely fire on the live corpus.
    """
    in_code = rec["occurrences_in_inline_code"]
    # ``occurrences_in_fenced_code_block`` was added alongside the
    # audit's fenced-block detection; older audit payloads may omit
    # it, so default to 0 for backwards compatibility.
    in_fenced = rec.get("occurrences_in_fenced_code_block", 0)
    total = rec["occurrences"]
    target = rec["target"]
    has_sug = bool(rec["suggestions"])

    # An occurrence is a "code sample" iff it sits inside inline code
    # OR a fenced block. On the live corpus these are disjoint sets,
    # but the schema allows both flags to be True on the same
    # referrer; we sum and cap at total so a hypothetical overlap
    # never pushes the count above 100 %.
    in_code_sample = min(total, in_code + in_fenced)

    if total > 0 and in_code_sample == total:
        return (
            "inline_code_canonical_suggestion" if has_sug
            else "inline_code_literal"
        )
    # At least one prose occurrence. If the audit found a mechanical
    # suggestion, the prose ref is genuinely ambiguous and we leave it
    # in a clearly-named fallback bucket so a future PR can curate it.
    if has_sug:
        return "unresolved_no_suggestion"
    if target.startswith("paper-"):
        return "paper_reference_needs_curation"
    return "external_reference_candidate"


def _depends_on_line_ranges(text: str) -> list[tuple[int, int]]:
    """Return a list of ``(start_line, end_line)`` 1-based inclusive
    ranges of every ``## Skill graph -> depends_on`` section in
    ``text``. ``end_line`` is the line of the next ``## ...`` header
    OR the last line of the file.

    The header pattern matches the same regex the audit already uses
    (``DEPENDS_HEADER_RE``) so the graph and the audit agree on which
    sections count.
    """
    lines = text.splitlines()
    headers = []  # (line_no_1based, is_depends_on)
    for i, ln in enumerate(lines, start=1):
        # Match any '## ...' header. We test depends_on with the audit
        # regex on a single-line basis to stay in sync.
        if ln.startswith("## "):
            is_depends = bool(DEPENDS_HEADER_RE.match(ln))
            headers.append((i, is_depends))

    if not headers:
        return []

    ranges = []
    total_lines = len(lines)
    for idx, (line_no, is_depends) in enumerate(headers):
        if not is_depends:
            continue
        next_line = (
            headers[idx + 1][0] - 1 if idx + 1 < len(headers)
            else total_lines
        )
        ranges.append((line_no, next_line))
    return ranges


def _line_in_ranges(line: int, ranges: list[tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= line <= end:
            return True
    return False


def _build_depends_on_index(corpus_root: Path) -> dict[str, list[tuple[int, int]]]:
    """Map ``<batch>/<slug>/SKILL.md`` -> list of depends_on line
    ranges. Used to tag each resolved-edge provenance record."""
    index: dict[str, list[tuple[int, int]]] = {}
    for p in sorted(corpus_root.glob("*/*/SKILL.md")):
        rel = p.relative_to(corpus_root).as_posix()
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = p.read_text(encoding="latin-1")
        ranges = _depends_on_line_ranges(text)
        if ranges:
            index[rel] = ranges
    return index


def _source_slug_for_rel(rel_skill_md_path: str,
                        path_to_slug: dict[str, str]) -> str | None:
    """Map an audit-relative ``<batch>/<slug>/SKILL.md`` path to the
    manifest slug whose ``path`` matches ``<batch>/<slug>``.

    The audit's ``referrers[].path`` records use the corpus-root-
    relative POSIX path of the SKILL.md. The manifest's ``entries[].path``
    records use the same ``<batch>/<slug>`` form but WITHOUT the
    trailing ``/SKILL.md``. We strip the suffix and look the entry up
    in ``path_to_slug``; if the SKILL.md lives outside any manifest
    entry's directory, return None and the edge is dropped (the audit
    only scans SKILL.md files under the corpus root, so this is rare).
    """
    if rel_skill_md_path.endswith("/SKILL.md"):
        entry_path = rel_skill_md_path[: -len("/SKILL.md")]
    else:
        entry_path = rel_skill_md_path
    return path_to_slug.get(entry_path)


def _load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.is_file():
        raise SystemExit(
            f"build_corpus_skill_graph.py: manifest not found: "
            f"{manifest_path}"
        )
    with open(manifest_path, encoding="utf-8") as f:
        return json.load(f)


def _build_nodes(manifest: dict, depends_on_index: dict) -> list[dict]:
    nodes = []
    for entry in manifest.get("entries", []):
        if not isinstance(entry, dict) or "slug" not in entry:
            continue
        node = {}
        for k in NODE_MANIFEST_FIELDS:
            # Use the field if present, else explicit null. We never
            # invent values.
            node[k] = entry.get(k) if k in entry else None
        rel_skill_md = (
            f"{entry['path']}/SKILL.md" if isinstance(entry.get("path"), str)
            else None
        )
        node["depends_on_section_present"] = bool(
            rel_skill_md and rel_skill_md in depends_on_index
        )
        nodes.append(node)
    # Stable order matches the manifest's own entry order so a diff of
    # the graph mirrors a diff of the manifest.
    return nodes


def _build_edges(
    audit: dict,
    slug_set: set[str],
    path_to_slug: dict[str, str],
    depends_on_index: dict,
) -> tuple[list[dict], int]:
    """Return ``(edges, inline_code_excluded_count)``.

    Edges are deduplicated by ``(source, target)``. Multiple
    occurrences in the same source file become multiple ``provenance``
    records on a single edge. Edges with ``link_type='wikilink'`` only;
    future link types can be added in a backwards-compatible way.

    A resolved wikilink whose occurrence sits wholly inside an inline
    code span is NOT emitted as an edge -- it is a doc sample. Those
    are counted in the returned ``inline_code_excluded_count`` so the
    summary stays honest.
    """
    # The audit already returns resolved targets via
    # ``totals.resolved_targets``, but the per-occurrence record is in
    # ``occurrences`` (which we don't have here) -- so we recover the
    # resolved-occurrence list by re-walking the audit's structure.
    # Specifically, the audit's ``unresolved`` list contains UNresolved
    # targets only; everything else is implicitly resolved. To recover
    # resolved occurrences we rerun a tiny scan against the corpus.
    # That keeps the regex / inline-code logic in ONE place
    # (audit_wikilinks) instead of duplicating it here.
    #
    # We rely on the audit's existing inline-code detection to know
    # which resolved occurrences to skip. Re-scanning is cheap (501
    # SKILL.md files, no I/O outside the bundle).
    from audit_wikilinks import _iter_skill_files, _find_wikilinks  # noqa: E402

    corpus_root = Path(audit["_corpus_root_abs"])
    edges_by_key: dict[tuple[str, str], dict] = {}
    inline_code_excluded = 0

    for rel, abs_path in _iter_skill_files(corpus_root):
        try:
            text = abs_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = abs_path.read_text(encoding="latin-1")

        source_slug = _source_slug_for_rel(rel, path_to_slug)
        if source_slug is None:
            continue

        ranges = depends_on_index.get(rel, [])

        for target, line_no, in_code, in_fenced in _find_wikilinks(text):
            if target not in slug_set:
                continue  # unresolved -- handled separately
            if in_code or in_fenced:
                # Both inline-code spans and fenced ``` blocks are
                # documentation samples, not real cross-references.
                # Excluded counts roll into edges_inline_code_excluded
                # for backwards-compatible reporting; fenced occurrences
                # are surfaced separately via the audit's
                # ``wikilink_occurrences_in_fenced_code_block`` total.
                inline_code_excluded += 1
                continue
            context = (
                "depends_on_section" if _line_in_ranges(line_no, ranges)
                else "wikilink_prose"
            )
            key = (source_slug, target)
            edge = edges_by_key.get(key)
            if edge is None:
                edge = {
                    "source": source_slug,
                    "target": target,
                    "link_type": "wikilink",
                    "occurrences": 0,
                    "provenance": [],
                }
                edges_by_key[key] = edge
            edge["occurrences"] += 1
            edge["provenance"].append({
                "path": rel,
                "line": line_no,
                "context": context,
            })

    # Sort edges deterministically: source slug, then target slug.
    edges = sorted(
        edges_by_key.values(),
        key=lambda e: (e["source"], e["target"]),
    )
    # Sort provenance within each edge by (path, line) for determinism.
    for e in edges:
        e["provenance"].sort(key=lambda r: (r["path"], r["line"]))
    return edges, inline_code_excluded


def _build_unresolved(audit: dict) -> tuple[list[dict], list[dict]]:
    """Return ``(unresolved_records, external_reference_candidates)``.

    Unresolved records mirror the audit's schema verbatim but add a
    ``classification`` field. The external-candidates roll-up is a
    subset of the unresolved records.
    """
    unresolved = []
    externals = []
    for rec in audit["unresolved"]:
        cls = _classify_unresolved(rec)
        out = {
            "target": rec["target"],
            "occurrences": rec["occurrences"],
            "occurrences_in_inline_code":
                rec["occurrences_in_inline_code"],
            "occurrences_in_fenced_code_block":
                rec.get("occurrences_in_fenced_code_block", 0),
            "classification": cls,
            "referrers": rec["referrers"],
            "suggestions": rec["suggestions"],
        }
        unresolved.append(out)
        if cls == "external_reference_candidate":
            externals.append({
                "target": rec["target"],
                "occurrences": rec["occurrences"],
                "referrers": rec["referrers"],
            })
    # Audit already orders unresolved by (-occurrences, target); keep
    # that ordering by re-sorting our copies on the same key.
    unresolved.sort(key=lambda r: (-r["occurrences"], r["target"]))
    externals.sort(key=lambda r: (-r["occurrences"], r["target"]))
    return unresolved, externals


def build_graph(
    corpus_root: Path,
    manifest_path: Path,
    generated_at: str | None,
) -> dict:
    """Compute the full graph payload as a plain dict.

    ``generated_at`` is taken verbatim from the caller so the CLI can
    choose between a deterministic ``None`` (``--no-timestamp``) and a
    real UTC ISO-8601 timestamp.
    """
    manifest = _load_manifest(manifest_path)
    audit = compute_audit(
        corpus_root=corpus_root,
        manifest_path=manifest_path,
    )
    # Stash the absolute corpus root so _build_edges can re-walk
    # without taking another CLI dependency.
    audit["_corpus_root_abs"] = str(corpus_root)

    entries = manifest.get("entries", [])
    slug_set: set[str] = {
        e["slug"] for e in entries
        if isinstance(e, dict) and isinstance(e.get("slug"), str)
    }
    path_to_slug: dict[str, str] = {
        e["path"]: e["slug"] for e in entries
        if isinstance(e, dict) and isinstance(e.get("slug"), str)
        and isinstance(e.get("path"), str)
    }

    depends_on_index = _build_depends_on_index(corpus_root)
    nodes = _build_nodes(manifest, depends_on_index)
    edges, inline_code_excluded = _build_edges(
        audit, slug_set, path_to_slug, depends_on_index,
    )
    unresolved, externals = _build_unresolved(audit)

    edges_in_depends_on = sum(
        1 for e in edges for p in e["provenance"]
        if p["context"] == "depends_on_section"
    )

    # Audit payload trimmed to the parts a downstream consumer cares
    # about; the full ``unresolved`` list is already in the graph's
    # ``unresolved_references`` field.
    audit_for_payload = {
        "schema_version": audit["schema_version"],
        "corpus_root": audit["corpus_root"],
        "manifest_path": audit["manifest_path"],
        "totals": audit["totals"],
        "depends_on_coverage": audit["depends_on_coverage"],
    }

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "source_manifest": str(
            manifest_path.relative_to(BUNDLE)
            if manifest_path.is_relative_to(BUNDLE) else manifest_path
        ),
        "source_audit": audit_for_payload,
        "limitations": LIMITATIONS,
        "totals": {
            "nodes": len(nodes),
            "edges": len(edges),
            "edges_resolved_wikilinks": len(edges),
            "edges_in_depends_on_section": edges_in_depends_on,
            "edges_inline_code_excluded": inline_code_excluded,
            "unresolved_targets": audit["totals"]["unresolved_targets"],
            "external_reference_candidates": len(externals),
            "depends_on_section_entries":
                audit["totals"]["depends_on_section_entries"],
        },
        "nodes": nodes,
        "edges": edges,
        "unresolved_references": unresolved,
        "external_reference_candidates": externals,
        "depends_on_coverage": audit["depends_on_coverage"],
    }
    return payload


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="build_corpus_skill_graph.py",
        description=(
            "Emit a machine-readable corpus skill graph at "
            "references/corpus_skill_graph.json. Joins manifest nodes "
            "with the resolved wikilink edges discovered by "
            "scripts/audit_wikilinks.py and preserves unresolved "
            "references with a conservative classification. Stdlib only."
        ),
    )
    p.add_argument(
        "--corpus",
        type=Path,
        default=DEFAULT_CORPUS,
        help=(
            "Path to the corpus root (default: references/corpus "
            "relative to the bundle). Must contain "
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
        "--output",
        type=Path,
        default=None,
        help=(
            "Path to the graph JSON output (default: "
            "corpus_skill_graph.json next to --manifest, i.e. "
            "references/corpus_skill_graph.json on the live bundle)."
        ),
    )
    p.add_argument(
        "--stdout",
        action="store_true",
        help=(
            "Print the graph JSON to stdout in addition to (or instead "
            "of) writing --output. When set with --output, both happen."
        ),
    )
    p.add_argument(
        "--no-timestamp",
        action="store_true",
        help=(
            "Set generated_at to null in the payload so two invocations "
            "produce byte-identical output. Use this in tests or when "
            "checking the artifact into version control."
        ),
    )
    args = p.parse_args(argv)

    if args.no_timestamp:
        generated_at = None
    else:
        generated_at = (
            _dt.datetime.now(_dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
        )

    manifest_path = args.manifest.resolve()
    output_path = (
        args.output.resolve() if args.output is not None
        else manifest_path.parent / "corpus_skill_graph.json"
    )

    payload = build_graph(
        corpus_root=args.corpus.resolve(),
        manifest_path=manifest_path,
        generated_at=generated_at,
    )

    serialized = json.dumps(payload, ensure_ascii=False, indent=2,
                            sort_keys=False) + "\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(serialized, encoding="utf-8")

    if args.stdout:
        sys.stdout.write(serialized)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
