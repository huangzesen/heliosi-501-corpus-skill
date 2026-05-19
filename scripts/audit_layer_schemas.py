#!/usr/bin/env python3
"""Classify per-entry SKILL.md files by layer-rendering family (issue #13).

The corpus was authored in several waves under slightly different
"layer rendering" conventions. Six families are present:

  1. ``numbered_v0_2_layer_tagged``
     ``## 1. Trigger  *(Layer 1)*`` ... ``## 9. Skill graph +
     research-generation affordances  *(Layer 4)*``
  2. ``numbered_abbreviated_v0_2``
     Same nine-section layout but with the ``*(Layer N)*`` tags
     stripped (``## 1. Trigger`` / ``## 9. Skill graph + affordances``).
  3. ``numbered_executable_workflow``
     ``## 1. Trigger`` ... ``## 9. Skill graph -> depends_on``
     (executable-workflow framing rather than four-layer framing).
  4. ``five_layer_scientific_invariant``
     ``## 1. Trigger and claim boundary`` /
     ``## 2. Scientific invariant layer`` /
     ``## 3. Executable protocol layer`` /
     ``## 4. Adapter / runtime notes`` /
     ``## 5. Research-generation affordance``
  5. ``prose_engineering_paper_skill``
     ``## When to use this paper-skill`` /
     ``## Paper identity and claim boundary`` (instrument/software-paper
     prose convention; no numbered sections).
  6. ``prose_runtime_neutral_layered``
     ``> Runtime-neutral paper-skill`` blockquote + ``## Trigger`` +
     ``## Layer 1 -- Scientific invariant`` (a numbered-Layer-N rather
     than numbered-section convention).

Issue #13 was the inconsistency itself; we intentionally do NOT
regenerate or rewrite 501 bodies. Instead, this helper documents which
rendering each batch ships, so consumers know which section header to
expect when grepping. ``--json`` emits a machine-readable schema that
the QA report (``references/corpus_qa_report_v2.md`` §9) cross-checks.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"


# Six rendering families distinguishable by stable section anchors. Names
# match those documented in ``references/corpus_qa_report_v2.md`` §8.
FAMILIES = [
    (
        # ## 1. Trigger  *(Layer 1)*  ...  ## 9. Skill graph + research-
        # generation affordances  *(Layer 4)*. Used by the v0.2 factory
        # wave500 batches that explicitly tag every section with its layer.
        "numbered_layer_v0_2_explicit",
        [
            re.compile(r"^##\s+1\.\s+Trigger\s+\*\(Layer 1\)\*", re.MULTILINE),
        ],
    ),
    (
        # Same nine-section spine as numbered_layer_v0_2_explicit but the
        # ``*(Layer N)*`` tag is stripped. Shows up in 4 entries of
        # wave500_turbulence_intermit_heating_045.
        "numbered_layer_v0_2_abbreviated",
        [
            re.compile(r"^##\s+1\.\s+Trigger\s*$", re.MULTILINE),
            re.compile(r"^##\s+9\.\s+Skill graph \+ affordances\s*$", re.MULTILINE),
        ],
    ),
    (
        # ## 1. Trigger  ...  ## 9. Skill graph -> depends_on (older
        # 96-baseline executable-workflow rendering; no inline Layer-N tag).
        "numbered_executable_workflow_v1",
        [
            re.compile(r"^##\s+1\.\s+Trigger\s*$", re.MULTILINE),
            re.compile(r"^##\s+2\.\s+Paper claim", re.MULTILINE),
            re.compile(r"^##\s+9\.\s+Skill graph → depends_on", re.MULTILINE),
        ],
    ),
    (
        # ## 1. Trigger and claim boundary / ## 2. Scientific invariant
        # layer / ## 3. Executable protocol layer / ## 4. Adapter notes /
        # ## 5. Research-generation affordance. Compact five-section form
        # used by psp_solo (with issue-#14 Layer-2 placeholders), waves,
        # and batch_psp_switchbacks_magnetic.
        "five_layer_scientific_invariant",
        [
            re.compile(r"^##\s+1\.\s+Trigger and claim boundary", re.MULTILINE),
            re.compile(r"^##\s+2\.\s+Scientific invariant layer", re.MULTILINE),
            re.compile(r"^##\s+3\.\s+Executable protocol layer", re.MULTILINE),
        ],
    ),
    (
        # ## When to use this paper-skill / ## Paper identity and claim
        # boundary (prose H2s; no numbered sections). Used for instrument
        # and software-paper batches where the numbered Layer-2 framing is
        # a poor fit.
        "prose_engineering_instrument",
        [
            re.compile(r"^##\s+When to use this paper-skill", re.MULTILINE),
            re.compile(r"^##\s+Paper identity and claim boundary", re.MULTILINE),
        ],
    ),
    (
        # > Runtime-neutral paper-skill blockquote + ## Trigger + ## Layer 1
        # -- Scientific invariant (numbered-Layer-N rather than numbered-
        # section). Used by PFSS / CME-flares batches.
        "prose_pfss_layered",
        [
            re.compile(r"Runtime-neutral paper-skill", re.MULTILINE),
            re.compile(r"^##\s+Trigger\s*$", re.MULTILINE),
            re.compile(r"^##\s+Layer 1 — Scientific invariant", re.MULTILINE),
        ],
    ),
]


def classify(text: str) -> str | None:
    """Return the rendering-family name, or None when no family matches."""
    for name, patterns in FAMILIES:
        if all(p.search(text) for p in patterns):
            return name
    return None


def walk_corpus():
    """Yield (batch, slug, skill_md_path) for every per-entry SKILL.md."""
    if not CORPUS.is_dir():
        return
    for batch_dir in sorted(p for p in CORPUS.iterdir() if p.is_dir()):
        for entry_dir in sorted(p for p in batch_dir.iterdir() if p.is_dir()):
            skill = entry_dir / "SKILL.md"
            if skill.is_file():
                yield batch_dir.name, entry_dir.name, skill


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="classify_layer_schemas.py",
        description=(
            "Audit per-entry SKILL.md rendering families (issue #13). "
            "Reports which of six known families each batch uses."
        ),
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help=(
            "exit non-zero if any entry is unclassified — used by tests "
            "to keep the rendering-family list reproducible as the corpus "
            "evolves."
        ),
    )
    p.add_argument(
        "--show-unclassified",
        action="store_true",
        help="print the slug of every unclassified entry to stderr",
    )
    args = p.parse_args(argv)

    by_batch: dict = defaultdict(Counter)
    unclassified = []
    total = 0
    for batch, slug, skill_p in walk_corpus():
        total += 1
        try:
            text = skill_p.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error reading {skill_p}: {exc}", file=sys.stderr)
            continue
        fam = classify(text)
        if fam is None:
            unclassified.append((batch, slug))
            by_batch[batch]["UNCLASSIFIED"] += 1
        else:
            by_batch[batch][fam] += 1

    if args.json:
        out = {
            "total_entries": total,
            "families": [name for name, _ in FAMILIES],
            "batches": {
                batch: dict(counter) for batch, counter in sorted(by_batch.items())
            },
            "unclassified_count": len(unclassified),
            "unclassified": [
                f"{b}/{s}" for b, s in unclassified
            ] if args.show_unclassified else None,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"per-batch SKILL.md rendering families "
              f"({total} entries scanned, "
              f"{len(unclassified)} unclassified)")
        print("-" * 80)
        name_w = max((len(b) for b in by_batch), default=24)
        for batch in sorted(by_batch):
            cell_parts = [
                f"{fam}={count}"
                for fam, count in by_batch[batch].most_common()
            ]
            print(f"{batch:<{name_w}}  {' '.join(cell_parts)}")
        if args.show_unclassified and unclassified:
            print("-" * 80)
            print("unclassified entries:", file=sys.stderr)
            for b, s in unclassified:
                print(f"  {b}/{s}", file=sys.stderr)

    if args.strict and unclassified:
        print(
            f"classify_layer_schemas.py: FAIL — {len(unclassified)} "
            f"unclassified entries (strict mode).",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
