#!/usr/bin/env python3
"""Audit and (optionally) backfill Layer-2 executable-protocol stubs.

Issue #14: many per-entry SKILL.md files document a Layer-2 "executable
protocol" that is in fact a placeholder. Two known classes:

  (a) 45 entries in ``wave500_inner_heliosphere_psp_solo_045`` whose
      Layer-2 algorithm sub-section contains the literal phrase
      ``"documented in the paper; runtime supplies the named capability"``;
  (b) 10 short entries in ``wave500_waves_instabilities_reconnection_045``
      (enumerated in ``KNOWN_WAVES_STUBS`` below) whose Layer-2 procedure
      is a 1-3 line skeleton (e.g. ``C-VDF-LOAD``, ``solve dispersion``).

Both classes are *not* runnable contracts. This script:

  - audits each entry and tags it with a structured marker
    (``layer2_stub: true`` in ``metadata.yaml``, plus ``layer2_status: stub``)
    so downstream tooling (search_corpus.py --ready-for, validate.sh)
    can refuse to advertise them as executable;
  - inserts a banner near the top of the SKILL.md body warning agents
    that Layer 2 is not populated and the paper itself must be read.

The script is idempotent: re-running it does not duplicate banners or
metadata fields. By default it runs in audit mode (no writes); pass
``--apply`` to perform the mutation.

This is stdlib-only -- the metadata write path is a simple line-based
splice that preserves existing YAML formatting (we never round-trip the
whole document through PyYAML, which would reorder keys).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"

PLACEHOLDER_PHRASE = "documented in the paper; runtime supplies the named capability"

PSP_SOLO_BATCH = "wave500_inner_heliosphere_psp_solo_045"
WAVES_BATCH = "wave500_waves_instabilities_reconnection_045"

KNOWN_WAVES_STUBS = (
    "anti-equilibrium-alfven-ion-cyclotron-effects-2023",
    "chandran-2010-stochastic-heating-perp-alfven",
    "interchange-reconnection-pseudostreamer-metis-2025",
    "ion-acoustic-damping-instability-solo-2026",
    "kelvin-helmholtz-cme-large-scale-2025",
    "oblique-drift-instability-solar-wind-heating-2025",
    "regulation-proton-alpha-flow-compressive-2023",
    "rotational-discontinuity-proton-beam-generation-2025",
    "stochastic-heating-sub-alfvenic-2025",
    "wave-particle-equilibria-heavy-ions-2026",
)

# The banner is inserted at the top of the SKILL.md body, after the
# `# <slug>` H1 line and before the first H2. We key off the marker so
# re-runs are idempotent.
BANNER_MARKER = "<!-- layer2-stub-banner: issue-14 -->"

BANNER_TEXT = (
    f"{BANNER_MARKER}\n"
    "> **Layer 2 not populated — read paper before use.** This entry's\n"
    "> executable-protocol layer is a stub: the algorithm sub-sections name\n"
    "> capabilities but do not specify the procedure end-to-end. Treat\n"
    "> Layer 2 as `pending`; do not present this skill as workflow-ready or\n"
    "> use it as the basis for an experiment without first verifying the\n"
    "> paper's methods section.\n"
)


def detect_psp_solo_stubs():
    """Return sorted list of (batch, slug) tuples that match the psp_solo
    placeholder phrase. Recomputed from disk each run -- this is the
    'class (a)' detector and must not drift from the parent-audit count of 45.
    """
    out = []
    bdir = CORPUS / PSP_SOLO_BATCH
    if not bdir.is_dir():
        return out
    for entry in sorted(bdir.iterdir()):
        if not entry.is_dir():
            continue
        skill = entry / "SKILL.md"
        if not skill.is_file():
            continue
        text = skill.read_text(encoding="utf-8")
        if PLACEHOLDER_PHRASE in text:
            out.append((PSP_SOLO_BATCH, entry.name))
    return out


def detect_waves_stubs():
    """Return sorted list of (batch, slug) tuples from the curated
    KNOWN_WAVES_STUBS list whose directory exists on disk. Class (b).
    """
    out = []
    bdir = CORPUS / WAVES_BATCH
    if not bdir.is_dir():
        return out
    for slug in KNOWN_WAVES_STUBS:
        if (bdir / slug).is_dir():
            out.append((WAVES_BATCH, slug))
    return out


def insert_banner(text: str) -> tuple[str, bool]:
    """Splice BANNER_TEXT into the body after the first H1 and before the
    first H2. Idempotent: returns (text, False) when BANNER_MARKER is
    already present.
    """
    if BANNER_MARKER in text:
        return text, False
    # Find the first '\n# ' (H1) -- skill bodies always start with the H1.
    h1 = re.search(r"^# [^\n]+\n", text, re.MULTILINE)
    if not h1:
        # Fall back to inserting after the closing frontmatter '---'.
        fm_end = text.find("\n---\n", 4)
        if fm_end == -1:
            return text, False
        insert_at = fm_end + len("\n---\n")
    else:
        insert_at = h1.end()
    new = text[:insert_at] + "\n" + BANNER_TEXT + "\n" + text[insert_at:]
    return new, True


# Metadata mutation: we add three keys if absent. Existing values are not
# overwritten (a future curation pass that promotes an entry past stub can
# set layer2_stub: false manually and the script will leave it alone).
METADATA_FIELDS = (
    ("layer2_stub", "true"),
    ("layer2_status", "stub"),
    # YAML-safe: any value containing ':' must be quoted, so we wrap the
    # reason string in double quotes. (PyYAML would otherwise read the
    # colon as a nested mapping delimiter -- caught in initial test.)
    ("layer2_banner_reason", '"issue-14: placeholder executable protocol"'),
)


def splice_metadata(text: str) -> tuple[str, bool]:
    """Append METADATA_FIELDS at the end of the metadata.yaml if they are
    not already present (key match is case-sensitive, top-level only).
    Idempotent.
    """
    changed = False
    lines = text.splitlines(keepends=True)
    # Top-level key set: lines that match '^\S[^:]*:' at column 0.
    existing = set()
    for ln in lines:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:", ln)
        if m:
            existing.add(m.group(1))
    to_append = []
    for key, val in METADATA_FIELDS:
        if key in existing:
            continue
        to_append.append(f"{key}: {val}\n")
        changed = True
    if not to_append:
        return text, False
    # Ensure trailing newline.
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"
    return "".join(lines) + "".join(to_append), changed


def process(entries, *, apply: bool, verbose: bool):
    skill_changed = 0
    meta_changed = 0
    skill_already = 0
    meta_already = 0
    for batch, slug in entries:
        entry_dir = CORPUS / batch / slug
        skill_p = entry_dir / "SKILL.md"
        meta_p = entry_dir / "metadata.yaml"
        if skill_p.is_file():
            text = skill_p.read_text(encoding="utf-8")
            new, did = insert_banner(text)
            if did:
                skill_changed += 1
                if apply:
                    skill_p.write_text(new, encoding="utf-8")
                if verbose:
                    print(f"  banner: {batch}/{slug}")
            else:
                skill_already += 1
        if meta_p.is_file():
            text = meta_p.read_text(encoding="utf-8")
            new, did = splice_metadata(text)
            if did:
                meta_changed += 1
                if apply:
                    meta_p.write_text(new, encoding="utf-8")
                if verbose:
                    print(f"  meta:   {batch}/{slug}")
            else:
                meta_already += 1
    return skill_changed, skill_already, meta_changed, meta_already


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="audit_layer2_stubs.py",
        description=(
            "Audit and optionally backfill Layer-2 stub markers (issue #14)."
        ),
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="actually write banners + metadata fields (default: dry run)",
    )
    p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="print one line per mutated file",
    )
    p.add_argument(
        "--audit-only",
        action="store_true",
        help=(
            "print the detected entries (count + slugs) and exit; do not "
            "splice banners or metadata even if --apply is also set"
        ),
    )
    args = p.parse_args(argv)

    psp = detect_psp_solo_stubs()
    waves = detect_waves_stubs()
    all_entries = psp + waves
    print(f"detected {len(psp)} psp_solo stubs (class a) "
          f"+ {len(waves)} waves stubs (class b) = {len(all_entries)} total")
    if args.audit_only:
        for batch, slug in all_entries:
            print(f"  {batch}/{slug}")
        return 0
    sk_ch, sk_al, mt_ch, mt_al = process(
        all_entries, apply=args.apply, verbose=args.verbose
    )
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        f"[{mode}] SKILL.md banners: changed={sk_ch} already-present={sk_al}; "
        f"metadata.yaml fields: changed={mt_ch} already-present={mt_al}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
