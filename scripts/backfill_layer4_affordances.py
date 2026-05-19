#!/usr/bin/env python3
"""Audit and (optionally) backfill ``research_generation_affordances_present``.

Issue #63: ``--ready-for hypothesis`` silently collapses to
``--ready-for experiment`` because zero per-entry ``metadata.yaml`` files
carry the gating field that ``scripts/search_corpus.py`` checks. The
hypothesis bucket is defined as a strict superset of the experiment
bucket -- T1/T2 plus T3 entries that author a substantive Layer 4
(research-generation affordances) block -- but with the field unwritten
the predicate reduces to ``tier in {T1, T2}`` and the two buckets are
identical.

This script reads each per-entry ``SKILL.md``, looks for a Layer 4 /
research-generation-affordances section, and writes
``research_generation_affordances_present: true`` to the entry's
``metadata.yaml`` when the section is *substantive* by the heuristic
below. The script is **conservative on purpose**: it does not invent
affordance content, it does not flag stub or empty Layer 4 sections as
present, and it does not modify SKILL.md bodies (the source of truth
stays where the author wrote it).

The script also updates the manifest roll-up
(``references/corpus_manifest_v2.json``) so ``scripts/search_corpus.py``
(which reads the field from the manifest, not the per-entry
metadata.yaml) actually picks the change up. Existing
``research_generation_affordances_present: true`` records in the
manifest are preserved -- the script only flips ``false`` to ``true``
when its heuristic detects a substantive section, never the other way.
When applying, the script also mirrors pre-existing manifest ``true``
records into per-entry ``metadata.yaml`` if that field is absent; newly
created manifest/metadata ``true`` records are gated by the same
substantive-content heuristic. This keeps the two surfaces in sync
without deleting historical/curated manifest flags that may have come
from an earlier QA pass.

Heuristic for "substantive Layer 4":

  1. The body contains a header matching
     ``layer 4`` OR ``research-generation affordance(s)`` (case-insensitive),
     extracted as the slice between that header and the next header at
     any depth.
  2. After stripping known empty-section sentinels
     ("No research-generation affordances identified yet" and "TBD"/"TODO"
     stand-alone variants), the section has at least
     ``MIN_NON_HEADING_CHARS`` (=300) characters of non-blank content,
     at least ``MIN_BULLETS`` (=2) markdown bullets, at least
     ``MIN_CLEANED_CHARS`` (=250) characters of content after stripping
     the empty-section sentinels, and contains at least one substantive
     marker token (``Gap:``, ``Hypothesis:``, ``Tension:``,
     ``Minimal_experiment``, ``compose with``, etc., as in
     ``SUBSTANTIVE_TOKENS``).

These thresholds were tuned conservatively against the 260 T3 entries.
A higher threshold over-rejects (e.g. legitimate two-bullet affordance
blocks from the wave500 SEP batch); a lower threshold over-accepts
(empty "## Layer 4 — TBD" sections). If you change them, re-run the
script in audit mode and inspect ``--list-substantive`` output before
applying.

The metadata splice is idempotent at the file level: entries that already
carry the field (or one with a different value) are not overwritten.
Dataset-level expansion is controlled by the tier filter: running
unrestricted ``--apply`` may honestly mark additional non-T3 entries if
those SKILL.md files also contain substantive Layer 4 affordances. For
the issue #63 repair, use ``--tier T3 --apply``; after that scoped pass,
a repeated ``--tier T3 --apply`` is a no-op.

By default the script applies to all entries (any tier). Pair with
``--tier T3`` to limit the write to the tier that the issue #63 fix
actually cares about; T1/T2 entries do not need the field to qualify
for ``--ready-for hypothesis`` (the predicate short-circuits on tier
membership) but writing the field there is still honest documentation
of the SKILL.md content.

Stdlib only -- the metadata write path is a line-based splice that
preserves existing YAML formatting, matching scripts/audit_layer2_stubs.py.
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
MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"


# -- Layer-4 substantive-content heuristic ---------------------------------

LAYER4_HEADER_RE = re.compile(
    r"^#{1,6}\s+.*(?:layer\s*4|research[- ]generation\s+affordance).*$",
    re.IGNORECASE | re.MULTILINE,
)
NEXT_HEADER_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)

# Phrases that mean "section header is present but the content is empty".
# Stripped before counting cleaned-body length so an entry that only says
# 'No research-generation affordances identified yet.' does not pass.
EMPTY_PHRASES = (
    "no research-generation affordances identified yet",
    "no research-generation affordance identified yet",
    "tbd",
    "todo",
)

# At least one of these tokens must appear in the section body for the
# block to count as substantive. They are the conventional markers the
# corpus authors used to enumerate gaps, hypotheses, tensions, and
# minimal experiments (see corpus_index_v2.md §research-generation map).
SUBSTANTIVE_TOKENS = (
    "gap:", "gap —", "gap--", "**gap**",
    "hypothesis:", "hypothesis —", "**hypothesis**",
    "tension:", "tension —", "**tension**",
    "minimal_experiment", "minimal experiment",
    "**minimal_experiment**", "**experiment**",
    "experiment:", "experiment —",
    "generative hypothesis",
    "new hypothesis",
    "compose with",
    "open question",
)

# Thresholds (kept here so a future curation pass can tune them without
# touching the splice logic).
MIN_NON_HEADING_CHARS = 300
MIN_BULLETS = 2
MIN_CLEANED_CHARS = 250


def extract_layer4(text: str) -> str | None:
    """Return the body of the first Layer 4 / research-generation-affordance
    section, or ``None`` if no such header is present. The body is the slice
    between the header and the next header at any depth.
    """
    m = LAYER4_HEADER_RE.search(text)
    if not m:
        return None
    start = m.end()
    rest = text[start:]
    nm = NEXT_HEADER_RE.search(rest)
    end = start + nm.start() if nm else len(text)
    return text[start:end]


def is_substantive(layer4_text: str | None) -> tuple[bool, str]:
    """Return ``(True, reason)`` if Layer 4 is substantive by the heuristic;
    ``(False, reason)`` otherwise. ``reason`` carries the counts so the audit
    listing is debuggable.
    """
    if not layer4_text:
        return False, "no Layer 4 section header"
    body = layer4_text
    low = body.lower()
    cleaned = low
    for ph in EMPTY_PHRASES:
        cleaned = cleaned.replace(ph, "")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    non_heading_chars = sum(len(ln) for ln in lines)
    bullet_lines = [ln for ln in lines if ln.startswith(("-", "*", "+"))]
    n_bullets = len(bullet_lines)
    has_marker = any(tok in low for tok in SUBSTANTIVE_TOKENS)
    cleaned_chars = len(cleaned.strip())
    ok = (
        has_marker
        and non_heading_chars >= MIN_NON_HEADING_CHARS
        and n_bullets >= MIN_BULLETS
        and cleaned_chars >= MIN_CLEANED_CHARS
    )
    return ok, (
        f"chars={non_heading_chars} bullets={n_bullets} "
        f"cleaned={cleaned_chars} marker={has_marker}"
    )


# -- Tier derivation (kept in lockstep with scripts/search_corpus.py) ------

_STUB_T5_STATUSES = frozenset({
    "historical-citation-only",
    "ecosystem-diff-procedure-only",
    "review-routing-not-runnable",
    "design-pattern-extractor",
    "manuscript-checklist-only",
    "architecture-template-only",
    "benchmark-design-template",
    "benchmark-protocol-template",
})
_STUB_T3_STATUSES = frozenset({
    "contract-specified-not-yet-benchmarked",
    "examples-only-not-yet-benchmarked",
    "pipeline-specified-not-yet-runnable",
})


def derive_tier(entry: dict) -> str:
    q = (entry.get("quality") or "").strip()
    es = (entry.get("executable_status") or "").strip()
    if q == "paper-grounded-locally-reproduced":
        return "T1"
    if q == "link-only-cross-batch":
        return "T6"
    if q == "pilot_weak_attribution":
        return "T7"
    if q == "positioning-skill-not-executable-science":
        return "T5"
    if q == "method-ready":
        return "T2"
    if q == "pilot":
        return "T2" if "runnable" in es else "T4"
    if q == "paper-grounded-pending-full-text":
        return "T2" if es == "constructive-pipeline-specified" else "T3"
    if q == "stub":
        if es in _STUB_T5_STATUSES:
            return "T5"
        if es == "pipeline-specified-not-yet-benchmarked":
            return "T2"
        if es in _STUB_T3_STATUSES:
            return "T3"
        return "T4"
    return "T?"


# -- Metadata splice -------------------------------------------------------

FIELD_KEY = "research_generation_affordances_present"
# YAML-safe scalar; lower-case true is canonical YAML 1.1/1.2 boolean.
FIELD_VALUE = "true"
FIELD_LINE = f"{FIELD_KEY}: {FIELD_VALUE}\n"

_TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")


def splice_metadata(text: str) -> tuple[str, bool, str]:
    """Return ``(new_text, changed, reason)``.

    Idempotent: if ``FIELD_KEY`` is already a top-level key (regardless of
    value), we return ``(text, False, 'already present')`` and do not
    overwrite. This protects a hand-curated ``false`` value from being
    flipped by a careless re-run, which matches scripts/audit_layer2_stubs.py.
    """
    lines = text.splitlines(keepends=True)
    existing = set()
    for ln in lines:
        m = _TOP_LEVEL_KEY_RE.match(ln)
        if m:
            existing.add(m.group(1))
    if FIELD_KEY in existing:
        return text, False, "already present"
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"
    return "".join(lines) + FIELD_LINE, True, "appended"


# -- Audit / apply pipeline -----------------------------------------------

def _load_manifest():
    if not MANIFEST.is_file():
        sys.exit(f"manifest not found: {MANIFEST}")
    with MANIFEST.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_candidate_entries(manifest, *, tier_filter: set[str] | None):
    """Yield ``(entry, tier, skill_text)`` for entries whose tier is in
    ``tier_filter`` (or all entries if no filter)."""
    for e in manifest.get("entries", []):
        tier = derive_tier(e)
        if tier_filter is not None and tier not in tier_filter:
            continue
        skill_p = CORPUS / e.get("path", "") / "SKILL.md"
        if not skill_p.is_file():
            yield e, tier, None
            continue
        try:
            text = skill_p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            yield e, tier, None
            continue
        yield e, tier, text


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="backfill_layer4_affordances.py",
        description=(
            "Backfill `research_generation_affordances_present: true` to "
            "per-entry metadata.yaml when Layer 4 is substantive (issue #63)."
        ),
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="actually write the field (default: dry run / audit)",
    )
    p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="print one line per mutated or skipped file",
    )
    p.add_argument(
        "--tier",
        action="append",
        choices=("T1", "T2", "T3", "T4", "T5", "T6", "T7"),
        default=None,
        help=(
            "restrict to entries of the given tier(s). Repeatable. "
            "Default: all tiers."
        ),
    )
    p.add_argument(
        "--list-substantive",
        action="store_true",
        help=(
            "print one line per entry detected as substantive (slug, batch, "
            "tier, body counts) and exit; does not touch metadata.yaml"
        ),
    )
    p.add_argument(
        "--json",
        action="store_true",
        help=(
            "emit a machine-readable JSON summary at the end (in addition to "
            "or instead of the human-readable summary, depending on --verbose)"
        ),
    )
    args = p.parse_args(argv)

    manifest = _load_manifest()
    tier_filter = set(args.tier) if args.tier else None

    audit = []  # list of (entry, tier, substantive, reason, has_skill)
    for entry, tier, text in iter_candidate_entries(
        manifest, tier_filter=tier_filter
    ):
        if text is None:
            audit.append((entry, tier, False, "no SKILL.md", False))
            continue
        layer4 = extract_layer4(text)
        sub, reason = is_substantive(layer4)
        audit.append((entry, tier, sub, reason, True))

    if args.list_substantive:
        n = 0
        for entry, tier, sub, reason, _ in audit:
            if not sub:
                continue
            n += 1
            print(
                f"{entry.get('slug', '<?>')}  "
                f"[{tier}]  {entry.get('batch', '<?>')}  "
                f"({reason})"
            )
        print(f"-- {n} substantive Layer 4 sections detected --", file=sys.stderr)
        return 0

    # Apply pass: per-entry metadata.yaml.
    n_substantive = 0
    n_written = 0
    n_already = 0
    n_manifest_mirrored = 0
    n_no_skill = 0
    n_not_substantive = 0
    substantive_slugs: set[str] = set()
    written = []
    for entry, tier, sub, reason, has_skill in audit:
        if sub:
            n_substantive += 1
            substantive_slugs.add(entry.get("slug") or "")
        elif not has_skill:
            n_no_skill += 1
        else:
            n_not_substantive += 1

        # Write metadata when either (a) this run's heuristic detects a
        # substantive Layer-4 block, or (b) the manifest already carries a
        # curated/historical true flag that should be mirrored into the
        # per-entry metadata surface. The latter is what prevents a
        # tier-filtered issue #63 backfill from leaving manifest-only true
        # records behind.
        mirror_manifest_true = entry.get(FIELD_KEY) is True
        should_write_metadata = sub or mirror_manifest_true
        if not should_write_metadata:
            continue

        meta_p = CORPUS / entry.get("path", "") / "metadata.yaml"
        if not meta_p.is_file():
            if args.verbose:
                print(
                    f"  skip (no metadata.yaml): {entry.get('slug')}",
                    file=sys.stderr,
                )
            continue
        try:
            text = meta_p.read_text(encoding="utf-8")
        except OSError as exc:
            print(
                f"warning: cannot read {meta_p}: {exc}",
                file=sys.stderr,
            )
            continue
        new_text, changed, splice_reason = splice_metadata(text)
        if not changed:
            n_already += 1
            if args.verbose:
                print(
                    f"  already-present: {entry.get('slug')}  ({splice_reason})",
                    file=sys.stderr,
                )
            continue
        n_written += 1
        if mirror_manifest_true and not sub:
            n_manifest_mirrored += 1
        written.append({
            "slug": entry.get("slug"),
            "batch": entry.get("batch"),
            "tier": tier,
            "reason": reason,
            "source": "manifest-mirror" if mirror_manifest_true and not sub else "heuristic",
        })
        if args.apply:
            meta_p.write_text(new_text, encoding="utf-8")
        if args.verbose:
            mode = "WRITE" if args.apply else "DRY"
            source = "manifest-mirror" if mirror_manifest_true and not sub else "heuristic"
            print(
                f"  {mode}: {entry.get('slug')}  [{tier}]  "
                f"{entry.get('batch')}  ({source})",
                file=sys.stderr,
            )

    # Apply pass: manifest roll-up. The manifest entry is what
    # search_corpus.py actually consults for the ``--ready-for hypothesis``
    # gate, so we have to update both surfaces. We only ever flip
    # ``false`` -> ``true`` for entries this heuristic just flagged
    # substantive; an existing ``true`` is preserved (some entries were
    # pre-flagged by an earlier QA pass against full SKILL.md authoring).
    n_manifest_flipped = 0
    n_manifest_already_true = 0
    for e in manifest.get("entries", []):
        slug = e.get("slug") or ""
        if slug not in substantive_slugs:
            continue
        if e.get("research_generation_affordances_present") is True:
            n_manifest_already_true += 1
            continue
        e["research_generation_affordances_present"] = True
        n_manifest_flipped += 1
    if args.apply and n_manifest_flipped > 0:
        # Match the existing on-disk shape: 2-space indent, no trailing
        # newline (the file ships without one; see `tail -c` against
        # corpus_manifest_v2.json). `json.dump(indent=2)` produces the
        # same indentation and key ordering as the original generator.
        with MANIFEST.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    mode = "APPLY" if args.apply else "DRY-RUN"
    summary = {
        "mode": mode,
        "tier_filter": sorted(tier_filter) if tier_filter else None,
        "entries_scanned": len(audit),
        "substantive_layer4": n_substantive,
        "not_substantive_or_missing": n_not_substantive,
        "no_skill_md": n_no_skill,
        "metadata_written": n_written,
        "metadata_already_present": n_already,
        "metadata_manifest_mirrored": n_manifest_mirrored,
        "manifest_flipped": n_manifest_flipped,
        "manifest_already_true": n_manifest_already_true,
    }
    if args.json:
        print(json.dumps(
            {"summary": summary, "written": written},
            ensure_ascii=False,
        ))
    else:
        print(
            f"[{mode}] scanned={len(audit)}  "
            f"substantive={n_substantive}  "
            f"written={n_written}  already-present={n_already}  "
            f"manifest-mirrored={n_manifest_mirrored}  "
            f"not-substantive={n_not_substantive}  no-skill={n_no_skill}  "
            f"manifest_flipped={n_manifest_flipped}  "
            f"manifest_already_true={n_manifest_already_true}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
