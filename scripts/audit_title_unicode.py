#!/usr/bin/env python3
"""Audit non-ASCII code points in entry title fields (issue #59).

Issue #59: an automated pass flagged that 95 / 501 manifest entries carry
non-ASCII characters in their ``title`` field. Examples cited in the issue:
``'SunPy — Python for Solar Physics'`` (U+2014 EM DASH),
``'Alfvénic solar wind …'`` (U+00E9), ``'(ISʘIS)'`` (U+0298). The likely
correct fix is **not** to ASCII-normalize scientific titles — Greek letters,
accented author names, degree signs, and the ISʘIS solar-disk glyph are all
intentional title typography — but to (a) confirm the observed code points
all fall in an expected scientific/typographic allowlist, (b) confirm the
manifest title field for an entry agrees with the per-entry
``metadata.yaml`` title (so the 95-entry count is not an artefact of one
surface drifting from another), and (c) make sure no entry is silently
carrying a Unicode-replacement glyph (U+FFFD), a C0/C1 control, or a
zero-width / bidi control character.

Definitions:

* "title fields scanned" — the manifest ``entries[].title`` and the
  per-entry ``metadata.yaml`` top-level ``title:`` surface. The per-entry
  ``SKILL.md`` frontmatter ``name:`` field is intentionally out of scope
  because it is a kebab-case slug, not a title.
* "non-ASCII" — any code point with ``ord(c) > 127``.
* "suspicious" — the Unicode replacement character (U+FFFD), or any code
  point in Unicode category Cc / Cf / Co / Cs (excluding the ordinary
  ``\\n`` / ``\\t`` whitespace which never appears in titles anyway).
* "expected allowlist" — code points the corpus is known to use
  intentionally. The audit reports any non-ASCII character not on the
  allowlist as ``unexpected_non_ascii`` so a future curation pass can
  decide whether to extend the allowlist or fix the title.

The allowlist is intentionally narrow: it covers the code points that
actually occur in the corpus today (LATIN with accent for author names,
EM/EN DASH, Greek letters used as physics parameter names, ISʘIS's solar
disk glyph, °, ×, Å, …). Any new code point requires a deliberate
allowlist update and is therefore visible in code review.

Stdlib + PyYAML. When PyYAML is missing the script prints a SKIP banner and
exits 0 in non-strict mode, matching ``scripts/validate.sh``'s S4c/S4d
conventions.

Usage::

    python3 scripts/audit_title_unicode.py            # human-readable
    python3 scripts/audit_title_unicode.py --json     # machine-readable
    python3 scripts/audit_title_unicode.py --strict   # non-zero on suspicious /
                                                      # unexpected / NFC drift /
                                                      # manifest <-> metadata
                                                      # mismatch
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
CORPUS = BUNDLE / "references" / "corpus"
MANIFEST = BUNDLE / "references" / "corpus_manifest_v2.json"

# Code points known to occur intentionally in the corpus title surfaces.
# Keep this list narrow: a new code point should land here only after a
# human has looked at the entry and confirmed it is intentional (not a
# copy-paste artefact).
EXPECTED_ALLOWLIST = {
    # Latin letters with diacritics (author names, "Alfvénic", "Ångström", …)
    "Å",  # Å  LATIN CAPITAL LETTER A WITH RING ABOVE
    "ä",  # ä  LATIN SMALL LETTER A WITH DIAERESIS
    "é",  # é  LATIN SMALL LETTER E WITH ACUTE
    # Typographic punctuation
    "–",  # –  EN DASH
    "—",  # —  EM DASH
    # Greek letters used as physics parameter names (β, α, δ, etc.)
    "α",  # α  GREEK SMALL LETTER ALPHA
    "β",  # β  GREEK SMALL LETTER BETA
    "δ",  # δ  GREEK SMALL LETTER DELTA
    # Astronomy / physics symbols
    "°",  # °  DEGREE SIGN
    "×",  # ×  MULTIPLICATION SIGN
    "ʘ",  # ʘ  LATIN LETTER BILABIAL CLICK (ISʘIS instrument glyph)
}


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


def _is_suspicious(c: str) -> bool:
    if c == "�":
        return True
    if c in ("\n", "\t"):
        return False
    cat = unicodedata.category(c)
    return cat in ("Cc", "Cf", "Co", "Cs")


def _char_record(c: str) -> dict:
    try:
        name = unicodedata.name(c)
    except ValueError:
        name = "<no-name>"
    return {
        "char": c,
        "codepoint": f"U+{ord(c):04X}",
        "name": name,
        "expected": c in EXPECTED_ALLOWLIST,
    }


def compute(yaml_mod):
    """Compute the audit summary as a plain dict."""
    if not MANIFEST.is_file():
        raise SystemExit(
            f"audit_title_unicode.py: manifest not found: {MANIFEST}"
        )
    if not CORPUS.is_dir():
        raise SystemExit(
            f"audit_title_unicode.py: corpus dir not found: {CORPUS}"
        )

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("entries", [])

    manifest_by_slug = {e.get("slug"): e for e in entries if e.get("slug")}

    # --- manifest surface -------------------------------------------------
    manifest_non_ascii_entries = []
    manifest_chars = Counter()
    manifest_suspicious = []  # (slug, char-repr)
    manifest_nfc_drift = []   # slugs whose title is not NFC-normalized
    for e in entries:
        title = e.get("title") or ""
        if not isinstance(title, str):
            continue
        non_ascii = [c for c in title if ord(c) > 127]
        if non_ascii:
            manifest_non_ascii_entries.append({
                "slug": e.get("slug"),
                "batch": e.get("batch"),
                "title": title,
                "non_ascii_chars": sorted(set(non_ascii)),
            })
            for c in non_ascii:
                manifest_chars[c] += 1
        for c in title:
            if _is_suspicious(c):
                manifest_suspicious.append({
                    "slug": e.get("slug"),
                    "char": repr(c),
                    "codepoint": f"U+{ord(c):04X}",
                })
        if title and title != unicodedata.normalize("NFC", title):
            manifest_nfc_drift.append(e.get("slug"))

    unexpected = sorted(
        {c for c in manifest_chars if c not in EXPECTED_ALLOWLIST},
        key=lambda c: ord(c),
    )

    # --- metadata.yaml surface -------------------------------------------
    meta_non_ascii_count = 0
    meta_chars = Counter()
    meta_suspicious = []
    meta_nfc_drift = []
    title_mismatches = []  # manifest vs metadata.yaml
    meta_titles_seen = 0
    meta_path_missing = 0
    for meta_path in sorted(CORPUS.glob("*/*/metadata.yaml")):
        slug = meta_path.parent.name
        data = _parse_metadata(meta_path, yaml_mod)
        if not isinstance(data, dict):
            continue
        mt = data.get("title")
        if not isinstance(mt, str):
            continue
        meta_titles_seen += 1
        if any(ord(c) > 127 for c in mt):
            meta_non_ascii_count += 1
        for c in mt:
            if ord(c) > 127:
                meta_chars[c] += 1
            if _is_suspicious(c):
                meta_suspicious.append({
                    "slug": slug,
                    "char": repr(c),
                    "codepoint": f"U+{ord(c):04X}",
                })
        if mt and mt != unicodedata.normalize("NFC", mt):
            meta_nfc_drift.append(slug)

        man = manifest_by_slug.get(slug)
        if man is None:
            meta_path_missing += 1
            continue
        man_title = man.get("title") or ""
        # Compare only on the non-ASCII subset to avoid drowning the audit
        # in unrelated content-length differences. We record both surfaces
        # so the human can decide whether the divergence matters for
        # issue #59 (which is strictly about non-ASCII title characters).
        if mt != man_title:
            man_non_ascii = [c for c in man_title if ord(c) > 127]
            meta_non_ascii_ch = [c for c in mt if ord(c) > 127]
            unicode_diff = sorted(set(man_non_ascii)) != sorted(
                set(meta_non_ascii_ch)
            )
            title_mismatches.append({
                "slug": slug,
                "manifest_title": man_title,
                "metadata_title": mt,
                "unicode_set_differs": unicode_diff,
            })

    # Suspicious / unexpected / NFC drift across BOTH surfaces drive the
    # strict-mode exit code. Replacement / control chars are the only
    # real "audit failure" the issue actually cares about; the rest is
    # honest reporting.
    strict_violations = []
    if manifest_suspicious:
        strict_violations.append(
            f"{len(manifest_suspicious)} suspicious char(s) in "
            f"manifest titles (replacement / control / format)"
        )
    if meta_suspicious:
        strict_violations.append(
            f"{len(meta_suspicious)} suspicious char(s) in "
            f"metadata.yaml titles (replacement / control / format)"
        )
    if unexpected:
        strict_violations.append(
            f"{len(unexpected)} non-ASCII code point(s) outside the "
            f"expected allowlist in manifest titles: "
            f"{[f'U+{ord(c):04X}' for c in unexpected]}"
        )
    # Unicode-set divergence between manifest and metadata.yaml means the
    # 95-entry headline isn't honest; non-unicode-only divergence (e.g.
    # one surface is a subtitle-truncated version of the other) is real
    # but out of scope for issue #59 — we report it but don't fail strict
    # on it.
    unicode_mismatches = [m for m in title_mismatches
                          if m["unicode_set_differs"]]
    if unicode_mismatches:
        strict_violations.append(
            f"{len(unicode_mismatches)} entries where manifest vs "
            f"metadata.yaml title disagree on the set of non-ASCII "
            f"code points"
        )
    if manifest_nfc_drift or meta_nfc_drift:
        strict_violations.append(
            f"{len(manifest_nfc_drift)} manifest title(s) and "
            f"{len(meta_nfc_drift)} metadata.yaml title(s) are not "
            f"NFC-normalized"
        )

    summary = {
        "total_entries": len(entries),
        "manifest": {
            "entries_with_non_ascii_title": len(manifest_non_ascii_entries),
            "unique_non_ascii_chars": len(manifest_chars),
            "char_counts": [
                {**_char_record(c), "count": n}
                for c, n in sorted(manifest_chars.items(),
                                   key=lambda kv: (-kv[1], ord(kv[0])))
            ],
            "suspicious_chars": manifest_suspicious,
            "nfc_drift_slugs": sorted(s for s in manifest_nfc_drift if s),
            "entries": sorted(
                manifest_non_ascii_entries,
                key=lambda e: (e["batch"] or "", e["slug"] or ""),
            ),
        },
        "metadata_yaml": {
            "titles_seen": meta_titles_seen,
            "entries_with_non_ascii_title": meta_non_ascii_count,
            "unique_non_ascii_chars": len(meta_chars),
            "char_counts": [
                {**_char_record(c), "count": n}
                for c, n in sorted(meta_chars.items(),
                                   key=lambda kv: (-kv[1], ord(kv[0])))
            ],
            "suspicious_chars": meta_suspicious,
            "nfc_drift_slugs": sorted(s for s in meta_nfc_drift if s),
            "manifest_slug_misses": meta_path_missing,
        },
        "expected_allowlist": sorted(
            (_char_record(c) for c in EXPECTED_ALLOWLIST),
            key=lambda r: r["codepoint"],
        ),
        "unexpected_non_ascii": [
            _char_record(c) for c in unexpected
        ],
        "title_mismatches_manifest_vs_metadata": title_mismatches,
        "strict_violations": strict_violations,
    }
    return summary


def _render_human(summary):
    out = []
    t = summary["total_entries"]
    m = summary["manifest"]
    md = summary["metadata_yaml"]
    out.append(
        f"title-unicode audit (issue #59) — {t} entries scanned"
    )
    out.append("=" * 72)
    out.append("")
    out.append("manifest entries[].title")
    out.append("-" * 72)
    out.append(
        f"  entries with non-ASCII title : "
        f"{m['entries_with_non_ascii_title']}/{t}"
    )
    out.append(
        f"  unique non-ASCII code points : "
        f"{m['unique_non_ascii_chars']}"
    )
    for row in m["char_counts"]:
        marker = " " if row["expected"] else "!"
        out.append(
            f"   {marker} {row['codepoint']} {row['char']!r:>6} "
            f"{row['count']:>5}  {row['name']}"
        )
    out.append(
        f"  suspicious chars (U+FFFD / Cc / Cf / Co / Cs) : "
        f"{len(m['suspicious_chars'])}"
    )
    out.append(
        f"  NFC-drifted titles : {len(m['nfc_drift_slugs'])}"
    )
    out.append("")
    out.append("metadata.yaml top-level title:")
    out.append("-" * 72)
    out.append(
        f"  titles seen : {md['titles_seen']}/{t}"
    )
    out.append(
        f"  entries with non-ASCII title : "
        f"{md['entries_with_non_ascii_title']}"
    )
    out.append(
        f"  unique non-ASCII code points : "
        f"{md['unique_non_ascii_chars']}"
    )
    out.append(
        f"  suspicious chars : {len(md['suspicious_chars'])}"
    )
    out.append(
        f"  NFC-drifted titles : {len(md['nfc_drift_slugs'])}"
    )
    out.append("")
    out.append("expected non-ASCII allowlist:")
    out.append("-" * 72)
    for row in summary["expected_allowlist"]:
        out.append(
            f"    {row['codepoint']} {row['char']!r:>6}  {row['name']}"
        )
    if summary["unexpected_non_ascii"]:
        out.append("")
        out.append("UNEXPECTED non-ASCII code points (not on allowlist):")
        out.append("-" * 72)
        for row in summary["unexpected_non_ascii"]:
            out.append(
                f"  ! {row['codepoint']} {row['char']!r:>6}  {row['name']}"
            )
    out.append("")
    out.append(
        f"manifest <-> metadata.yaml title divergences : "
        f"{len(summary['title_mismatches_manifest_vs_metadata'])}"
    )
    unicode_only = [m for m in summary["title_mismatches_manifest_vs_metadata"]
                    if m["unicode_set_differs"]]
    out.append(
        f"  ... of which differ on the non-ASCII code-point set : "
        f"{len(unicode_only)}"
    )
    for m_ in summary["title_mismatches_manifest_vs_metadata"][:5]:
        out.append(
            f"  - {m_['slug']} "
            f"{'[unicode-set-differs]' if m_['unicode_set_differs'] else '[content-length-only]'}"
        )
    if len(summary["title_mismatches_manifest_vs_metadata"]) > 5:
        out.append(
            f"  ... and "
            f"{len(summary['title_mismatches_manifest_vs_metadata']) - 5} "
            f"more"
        )
    out.append("")
    if summary["strict_violations"]:
        out.append("STRICT-mode violations:")
        for v in summary["strict_violations"]:
            out.append(f"  - {v}")
    else:
        out.append("STRICT-mode violations: none")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="audit_title_unicode.py",
        description=(
            "Audit non-ASCII code points in manifest / metadata.yaml "
            "title fields across all 501 entries (issue #59). Reports "
            "the per-character counts, classifies them against an "
            "expected scientific/typographic allowlist, and flags any "
            "Unicode-replacement / control / format / NFC-drift / "
            "manifest-vs-metadata-divergence issues. Stdlib + PyYAML."
        ),
    )
    p.add_argument(
        "--json", action="store_true",
        help="emit machine-readable JSON",
    )
    p.add_argument(
        "--strict", action="store_true",
        help=(
            "exit non-zero on any of: suspicious chars, unexpected "
            "non-ASCII code points outside the allowlist, manifest <-> "
            "metadata.yaml unicode-set divergence, or NFC drift. "
            "Used by tests/test_title_unicode.py."
        ),
    )
    args = p.parse_args(argv)

    yaml_mod = _load_yaml()
    if yaml_mod is None:
        print(
            "SKIP: PyYAML not installed -- title-unicode audit skipped. "
            "Install with `pip install pyyaml`.",
            file=sys.stderr,
        )
        return 0

    summary = compute(yaml_mod)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2,
                         sort_keys=False))
    else:
        print(_render_human(summary))

    if args.strict and summary["strict_violations"]:
        print(
            f"audit_title_unicode.py: FAIL — "
            f"{len(summary['strict_violations'])} strict-mode "
            f"violation(s); see above.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
