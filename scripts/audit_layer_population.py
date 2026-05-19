#!/usr/bin/env python3
"""Audit explicit ``layers:`` boolean blocks across the 501 entries (issue #58).

Issue #58: the aggregator headline reads "the corpus follows a four-layer
authoring model", which sounds like a structural invariant ("every entry
populates all four layers"). In practice some entries carry an explicit
``layers:`` block where one or more of
``{scientific_invariant, executable_protocol, adapter_binding_examples,
research_generation_affordance}`` is ``false``. Examples cited in the
issue: ``paper-orbiter-fno-autoregressive-spherical``,
``paper-astropy-2022-collaboration-community-package``,
``paper-opie-2024-temperature-anisotropy-velocity-shears``.

The fix is two-sided:

  * Reword the docs to say "up to four layers, populated as the entry
    matures" rather than implying every entry populates all four.
  * Publish the actual fully-populated vs partially-populated counts in
    ``references/corpus_qa_report_v2.md`` (and the manifest
    ``four_layer_model.layer_population_across_501`` block) so the
    aggregator headline cannot drift from reality silently.

This helper computes those counts deterministically from the corpus on
disk and exposes them as both a human-readable table and JSON (consumed
by ``tests/test_layer_population.py``).

Definitions:

* "explicit layers block (SKILL.md)" — the YAML frontmatter at the top
  of ``references/corpus/<batch>/<slug>/SKILL.md`` parses to a mapping
  whose ``layers`` key is itself a mapping containing all four expected
  boolean keys.
* "explicit layers block (metadata.yaml)" — same shape, in
  ``metadata.yaml`` instead of the SKILL.md frontmatter.
* "fully populated" — all four boolean keys are truthy.
* "partially populated" — at least one key is falsy.

Entries that do not carry an explicit ``layers:`` block at all express
their layer coverage prose-side (numbered ``## 1. ... ## 9.`` sections,
``## Layer 1 — Scientific invariant`` headers, etc., audited by
``scripts/audit_layer_schemas.py`` / ``tests/test_layer_schemas.py``).
They are NOT counted as ``no_block`` failures — the corpus deliberately
ships heterogeneous rendering families (issue #13). The booleans are an
*additional* machine-readable signal where present, not a requirement.

Stdlib + PyYAML. When PyYAML is missing, the script prints a SKIP banner
and exits 0 in non-strict mode (matching ``scripts/validate.sh``'s S4c/
S4d conventions).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

LAYER_KEYS = (
    "scientific_invariant",
    "executable_protocol",
    "adapter_binding_examples",
    "research_generation_affordance",
)


def _load_yaml():
    try:
        import yaml  # PyYAML
    except ImportError:
        return None
    return yaml


def _parse_metadata(path: Path, yaml_mod):
    try:
        with open(path) as f:
            return yaml_mod.safe_load(f)
    except Exception:
        return None


def _parse_skill_frontmatter(path: Path, yaml_mod):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---\n"):
        return None
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return None
    try:
        return yaml_mod.safe_load(text[4:end])
    except Exception:
        return None


def _layers_block(data):
    if not isinstance(data, dict):
        return None
    layers = data.get("layers")
    if not isinstance(layers, dict):
        return None
    if not all(k in layers for k in LAYER_KEYS):
        return None
    return {k: bool(layers.get(k)) for k in LAYER_KEYS}


def _summarize_surface(records):
    """records: list[(batch, slug, layers_dict_or_None)]."""
    with_block = [(b, s, L) for b, s, L in records if L is not None]
    fully = sum(1 for _, _, L in with_block if all(L.values()))
    partial = sum(1 for _, _, L in with_block if not all(L.values()))
    distribution = Counter(sum(L.values()) for _, _, L in with_block)
    per_key = Counter()
    for _, _, L in with_block:
        for k, v in L.items():
            if v:
                per_key[k] += 1
    by_batch = defaultdict(lambda: {
        "with_block": 0, "fully": 0, "partial": 0,
        "by_n_true": Counter(),
    })
    for b, _, L in with_block:
        bb = by_batch[b]
        bb["with_block"] += 1
        n = sum(L.values())
        bb["by_n_true"][n] += 1
        if n == 4:
            bb["fully"] += 1
        else:
            bb["partial"] += 1
    return {
        "entries_with_block": len(with_block),
        "entries_without_block": len(records) - len(with_block),
        "fully_populated": fully,
        "partially_populated": partial,
        "distribution_by_n_true": dict(sorted(distribution.items())),
        "per_layer_true": {k: per_key.get(k, 0) for k in LAYER_KEYS},
        "by_batch": {
            b: {
                "with_block": v["with_block"],
                "fully": v["fully"],
                "partial": v["partial"],
                "by_n_true": dict(sorted(v["by_n_true"].items())),
            }
            for b, v in sorted(by_batch.items())
        },
    }


def compute(yaml_mod):
    """Return a dict shaped like ``{metadata: {...}, skill: {...}, totals: {...}}``."""
    if not CORPUS.is_dir():
        raise SystemExit(f"audit_layer_population.py: corpus dir not found: {CORPUS}")

    meta_records = []
    skill_records = []
    parity_mismatches = []

    for meta_path in sorted(CORPUS.glob("*/*/metadata.yaml")):
        entry_dir = meta_path.parent
        batch = entry_dir.parent.name
        slug = entry_dir.name

        meta = _parse_metadata(meta_path, yaml_mod)
        skill = _parse_skill_frontmatter(entry_dir / "SKILL.md", yaml_mod)

        m_layers = _layers_block(meta)
        s_layers = _layers_block(skill)

        meta_records.append((batch, slug, m_layers))
        skill_records.append((batch, slug, s_layers))

        if m_layers is not None and s_layers is not None and m_layers != s_layers:
            parity_mismatches.append(f"{batch}/{slug}")

    return {
        "total_entries": len(meta_records),
        "metadata_yaml": _summarize_surface(meta_records),
        "skill_md_frontmatter": _summarize_surface(skill_records),
        "parity_mismatches_meta_vs_skill": parity_mismatches,
    }


def _render_human(summary):
    out = []
    t = summary["total_entries"]
    out.append(f"layer-population audit (issue #58) — {t} entries scanned")
    out.append("=" * 72)
    for label, key in (
        ("SKILL.md frontmatter `layers:` block", "skill_md_frontmatter"),
        ("metadata.yaml top-level `layers:` block", "metadata_yaml"),
    ):
        s = summary[key]
        out.append("")
        out.append(label)
        out.append("-" * 72)
        out.append(
            f"  entries with explicit block : {s['entries_with_block']}/{t}"
        )
        out.append(
            f"  fully populated (4/4)       : {s['fully_populated']}"
        )
        out.append(
            f"  partially populated (<4/4)  : {s['partially_populated']}"
        )
        if s["distribution_by_n_true"]:
            out.append(f"  distribution by # layers true:")
            for n, c in s["distribution_by_n_true"].items():
                out.append(f"    {n}/4 layers true: {c} entries")
        out.append(f"  per-layer true counts:")
        for k in LAYER_KEYS:
            out.append(f"    {k:<32s} {s['per_layer_true'][k]}")
        if s["by_batch"]:
            out.append(f"  per-batch (only batches with the block):")
            for batch, bv in s["by_batch"].items():
                dist = ", ".join(
                    f"{n}/4×{c}" for n, c in bv["by_n_true"].items()
                )
                out.append(
                    f"    {batch:<48s} with_block={bv['with_block']:>3d} "
                    f"fully={bv['fully']:>3d} partial={bv['partial']:>3d} "
                    f"({dist})"
                )
    pm = summary["parity_mismatches_meta_vs_skill"]
    out.append("")
    out.append(f"metadata.yaml ↔ SKILL.md `layers:` parity mismatches: "
               f"{len(pm)}")
    if pm:
        for slug in pm[:10]:
            out.append(f"  - {slug}")
        if len(pm) > 10:
            out.append(f"  ... and {len(pm) - 10} more")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="audit_layer_population.py",
        description=(
            "Audit explicit `layers:` boolean blocks across all 501 "
            "per-entry SKILL.md / metadata.yaml files (issue #58). "
            "Reports fully-populated vs partially-populated counts on "
            "both surfaces. Stdlib + PyYAML."
        ),
    )
    p.add_argument("--json", action="store_true",
                   help="emit machine-readable JSON")
    p.add_argument(
        "--strict", action="store_true",
        help=(
            "exit non-zero on metadata.yaml ↔ SKILL.md parity mismatch. "
            "Used by tests/test_layer_population.py to keep both surfaces "
            "in sync as the corpus evolves."
        ),
    )
    args = p.parse_args(argv)

    yaml_mod = _load_yaml()
    if yaml_mod is None:
        print(
            "SKIP: PyYAML not installed -- layer-population audit skipped. "
            "Install with `pip install pyyaml`.",
            file=sys.stderr,
        )
        return 0

    summary = compute(yaml_mod)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=False))
    else:
        print(_render_human(summary))

    if args.strict and summary["parity_mismatches_meta_vs_skill"]:
        print(
            f"audit_layer_population.py: FAIL — "
            f"{len(summary['parity_mismatches_meta_vs_skill'])} parity "
            f"mismatch(es) between metadata.yaml and SKILL.md `layers:` "
            f"blocks (strict mode).",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
