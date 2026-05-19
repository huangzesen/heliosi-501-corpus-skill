#!/usr/bin/env python3
"""Audit unflagged numeric tolerances / factors in per-entry SKILL.md bodies (issue #39).

Issue #39 (Unflagged numeric tolerances in 'Verifiable task' bodies): a
per-entry ``SKILL.md`` body can carry a numeric tolerance or multiplicative
factor in prose (e.g. ``within ±15 min of paper times``,
``factor 1.5--2x more open flux``, ``ratio ~1.5-2.0 in minimum``) that
looks like a sourced quantitative claim but is in fact unverified --
neither cited to a paper line nor flagged ``TODO_verify`` / ``TODO verify``
/ ``TBD`` / ``provisional``. A downstream agent reading the body will
treat the number as authoritative and reproduce the fabrication risk.

The audit scans every per-entry SKILL.md body (i.e. the markdown that
follows the YAML frontmatter) for a small, deliberately narrow set of
**numeric-claim patterns**:

  * ``+/- N unit``  (plus-minus tolerance, e.g. ``+-15 min``, ``+-20%``)
  * ``within N unit`` for a small list of physics units (``min``, ``s``,
    ``hr``, ``day``, ``km``, ``km/s``, ``au``, ``sigma``, ``%``, ...)
  * ``factor [of] N[-M] x``  (multiplicative factor claims)
  * ``ratio ~?N[.NN]-M[.MM]`` (numeric ratio targets)

For each match the script classifies the section it appears in:

  * **caveat zone** -- ``claim boundary``, ``failure modes``,
    ``out of scope``, ``research-generation affordances``, ``links``,
    ``skill graph``, ``notes``, ``trigger keywords``. Numeric claims in
    these sections are caveats / out-of-scope statements, not load-bearing
    quantitative claims, and are NOT flagged.

  * **tool-contract zone** -- ``data / instruments``, ``tool contract``,
    ``data products``. Numeric tokens here (e.g. ``2023-03-13 +- 2 d``)
    describe data-fetch windows, not paper tolerances; not flagged.

  * **validation zone** -- ``validation target`` (with or without
    section-number prefix). Numeric claims are *expected* here, but they
    MUST be accompanied by ``TODO_verify`` / ``TODO verify`` / ``TBD`` /
    ``provisional`` / ``unverified`` **on the same line**, otherwise
    they appear validated when they are not. Same-line (not proximity)
    matching is deliberate -- see ``has_todo_marker``.

  * **body zone** -- everything else (``trigger``, ``claim narrow form``,
    ``paper claim verifiable task``, ``methods / equations``,
    ``executable workflow``, etc.). This is the dangerous zone the issue
    is named after. Same rule as validation zone: requires a same-line
    TODO-marker.

A ``tables`` heuristic also exempts matches that appear on a markdown
table row (lines starting with ``|`` or aligned with a ``|...|`` row),
since instrument-table entries like ``2023-03-13 +- 2 d`` are not paper
tolerances.

An **expected-flags** allowlist (``references/numeric_claims_expected.json``,
created by this issue) pins the current set of known unflagged numeric
claims as "documented curation debt" so this audit can land without
forcing a 40-file content edit in the same PR. Going forward the test
fails when a NEW unflagged match appears: a curator drains the debt by
adding ``TODO_verify`` to the line (which makes the match disappear from
the audit) and removing the corresponding row from the expected-flags
file.

Stdlib only. Designed to mirror the audit/test conventions of
``scripts/audit_title_unicode.py`` / ``tests/test_title_unicode.py`` and
the ``scripts/validate.sh`` S4* sections.

Usage::

    python3 scripts/audit_numeric_claims.py            # human-readable
    python3 scripts/audit_numeric_claims.py --json     # machine-readable
    python3 scripts/audit_numeric_claims.py --strict   # non-zero on
                                                       # any flag not on
                                                       # the expected list
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
EXPECTED_PATH = BUNDLE / "references" / "numeric_claims_expected.json"


# Narrow, high-signal numeric-claim patterns. We deliberately do NOT scan
# for "any number" -- that would drown the audit in years, section
# numbers, identifiers, and instrument levels (L1 / L2 / L3). Each pattern
# captures a *tolerance* or *factor* shape that authoritatively asserts
# a paper-side quantity.
PATTERNS = (
    (
        "plus-minus",
        re.compile(
            r"±\s*\d+(?:\.\d+)?(?:\s*[a-zA-Zµ°%/]+)?"
        ),
    ),
    (
        "within-N-unit",
        re.compile(
            r"\bwithin\s+(?:±\s*)?\d+(?:\.\d+)?\s*"
            r"(?:min|minutes|s|sec|seconds|hr|hour|hours|day|days|"
            r"km|m/s|km/s|au|AU|R[_ ]?sun|R⊙|sigma|σ|%|nT|G|"
            r"deg|°|MK|K|eV|keV|MeV|GeV)\b"
        ),
    ),
    (
        "factor-N-x",
        re.compile(
            r"\bfactor\s+(?:of\s+)?\d+(?:\.\d+)?"
            r"(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*[×x]"
        ),
    ),
    (
        "ratio-N-M",
        re.compile(
            r"\bratio\s+[`'\"]?\s*[~≈]?\s*\d+(?:\.\d+)?"
            r"\s*[-–]\s*\d+(?:\.\d+)?"
        ),
    ),
)


# Section-title substrings that mark a "caveat" zone -- numeric claims in
# these zones are explicit out-of-scope / failure-mode prose and do NOT
# need a TODO_verify marker. Matched case-insensitively against the most
# recent markdown header.
CAVEAT_ZONE_TOKENS = (
    "claim boundary",
    "claim_boundary",
    "failure modes",
    "failure_modes",
    "out of scope",
    "out_of_scope",
    "research-generation affordances",
    "research generation affordances",
    "skill graph",
    "depends_on",
    "links",
    "notes",
    "trigger keywords",
    "in scope",  # "**In scope.** ..." prose under claim boundary
)

# Section titles for tool-contract / data zones. These tables carry
# numeric tokens like "2023-03-13 +- 2 d" that are data-window
# descriptors, not paper tolerances. We exempt them by zone.
TOOL_CONTRACT_TOKENS = (
    "data / instruments",
    "data/instruments",
    "data products",
    "tool contract",
    "instruments",
)

# Validation-target zone tokens. Numeric claims are expected here, but
# MUST carry a TODO_verify / TBD / provisional marker nearby.
VALIDATION_ZONE_TOKENS = (
    "validation target",
)


# A token that satisfies the "this claim is flagged as not-yet-verified"
# requirement. Matched case-insensitively in the nearby line window.
TODO_PAT = re.compile(
    r"TODO[_ ]verify|TODO\b|TBD\b|provisional|tentative|unverified",
    re.IGNORECASE,
)


# Markdown section header (level 1-4). We use it to slice the body into
# zones; the *most recent* header before a match defines the zone.
SECTION_RE = re.compile(r"^(#{1,4})\s+(.*?)\s*$", re.MULTILINE)


def split_frontmatter(text: str) -> str:
    """Return the body of a SKILL.md, dropping YAML frontmatter if present."""
    if text.startswith("---\n"):
        try:
            end = text.index("\n---", 4)
        except ValueError:
            return text
        # Skip past the trailing '---' marker line.
        rest = text[end + 4:]
        if rest.startswith("\n"):
            rest = rest[1:]
        return rest
    return text


def section_index(body: str):
    """Yield (offset, header_text_lowercase) for each markdown header."""
    return [
        (m.start(), m.group(2).strip().lower())
        for m in SECTION_RE.finditer(body)
    ]


def zone_at(offset: int, sections):
    """Return the lowercase header text of the most recent header before offset."""
    title = ""
    for off, t in sections:
        if off <= offset:
            title = t
        else:
            break
    return title


def in_zone(title: str, tokens) -> bool:
    return any(tok in title for tok in tokens)


def is_in_table(body: str, offset: int) -> bool:
    """True iff the line containing offset is a markdown table row (starts with '|')."""
    # Find the start of the line containing offset.
    line_start = body.rfind("\n", 0, offset) + 1
    line_end = body.find("\n", offset)
    if line_end == -1:
        line_end = len(body)
    line = body[line_start:line_end].lstrip()
    return line.startswith("|")


_TODO_TOKEN = (
    r"TODO[_ ]verify|TODO\b|TBD\b|provisional|tentative|unverified"
)
_ATTACHED_AFTER_RE = re.compile(
    r"\s*[\[\(\`\"'*\-—–]?\s*(?:" + _TODO_TOKEN + r")",
    re.IGNORECASE,
)
# Leading marker: a TODO token, then optional separators / "—" / spaces,
# then the numeric claim immediately. The marker is consumed against the
# tail of the preceding 60-char window.
_ATTACHED_BEFORE_RE = re.compile(
    r"(?:" + _TODO_TOKEN + r")"
    r"(?:\s*[\)\]\`\"'*\-—–:]?\s*)*\Z",
    re.IGNORECASE,
)


def has_todo_marker(body: str, match_start: int, match_end: int) -> bool:
    """True iff a TODO/TBD/provisional marker is *directly attached* to the
    numeric match -- immediately before OR immediately after it.

    "Directly attached" means: starting at the numeric match's boundary,
    skipping optional whitespace and a single grouping/punctuation token
    (``(`` / ``[`` / backtick / ``-`` / em-dash / colon), we find a
    TODO / TBD / provisional / unverified token.

    Loose proximity is intentionally rejected: in the Dresing-2025
    example the same sentence carries ``within +-15 min of paper times,
    (b) runs both MHD scenarios (TODO verify code), ...`` -- the
    ``TODO verify`` qualifies the *MHD code identity*, not the
    ``+-15 min`` tolerance, and any rule that scans further than the
    immediately-attached tail would silently absolve the tolerance.

    The natural author phrasings the audit asks for:

      * ``+-15 min (TODO_verify ...)``                  (after)
      * ``factor 1.5-2x (TODO_verify) more flux``       (after)
      * ``TODO verify -- ratio ~1.5-2.0 in minimum.``   (before)
      * ``TODO_verify: +-5% pass band``                 (before)
    """
    tail = body[match_end:match_end + 80]
    if _ATTACHED_AFTER_RE.match(tail):
        return True
    head = body[max(0, match_start - 60):match_start]
    if _ATTACHED_BEFORE_RE.search(head):
        return True
    return False


def classify_match(body: str, sections, offset: int):
    """Return one of: 'caveat', 'tool_contract', 'table', 'validation', 'body'."""
    if is_in_table(body, offset):
        return "table"
    title = zone_at(offset, sections)
    if in_zone(title, CAVEAT_ZONE_TOKENS):
        return "caveat"
    if in_zone(title, TOOL_CONTRACT_TOKENS):
        return "tool_contract"
    if in_zone(title, VALIDATION_ZONE_TOKENS):
        return "validation"
    return "body"


def collect_flags(corpus_dir: Path):
    """Return (flags, by_zone_counts).

    Each flag is a dict with: slug, batch, path, pattern, match, zone,
    section_title, line_number, has_todo_nearby.
    Only matches in 'body' or 'validation' zones with no TODO marker
    nearby are returned.
    """
    flags = []
    by_zone = {
        "caveat": 0,
        "tool_contract": 0,
        "table": 0,
        "validation_with_todo": 0,
        "validation_without_todo": 0,
        "body_with_todo": 0,
        "body_without_todo": 0,
    }
    for skill_path in sorted(corpus_dir.glob("*/*/SKILL.md")):
        rel = skill_path.relative_to(corpus_dir)
        batch = rel.parts[0]
        slug = rel.parts[1]
        text = skill_path.read_text(encoding="utf-8")
        body = split_frontmatter(text)
        sections = section_index(body)

        for pat_name, pat in PATTERNS:
            for m in pat.finditer(body):
                offset = m.start()
                zone = classify_match(body, sections, offset)
                has_todo = has_todo_marker(body, offset, m.end())
                if zone in ("caveat", "tool_contract", "table"):
                    by_zone[zone] += 1
                    continue
                if zone == "validation":
                    if has_todo:
                        by_zone["validation_with_todo"] += 1
                        continue
                    by_zone["validation_without_todo"] += 1
                else:  # body
                    if has_todo:
                        by_zone["body_with_todo"] += 1
                        continue
                    by_zone["body_without_todo"] += 1

                # Compute 1-based line number for the match.
                line_no = body.count("\n", 0, offset) + 1
                flags.append({
                    "batch": batch,
                    "slug": slug,
                    "path": str(rel),
                    "pattern": pat_name,
                    "match": m.group(0),
                    "zone": zone,
                    "section_title": zone_at(offset, sections),
                    "body_line": line_no,
                    "has_todo_nearby": has_todo,
                })
    return flags, by_zone


def load_expected(expected_path: Path):
    """Return the expected-flags allowlist as a list, or [] if missing."""
    if not expected_path.is_file():
        return []
    try:
        data = json.loads(expected_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, dict):
        return data.get("expected", [])
    if isinstance(data, list):
        return data
    return []


def flag_signature(flag) -> tuple:
    """A stable identity for a flag, used to compare against the allowlist.

    The body-line number is part of the signature so that two distinct
    occurrences of the same match string in the same file (e.g. one
    paragraph using ``+-1`` twice) are tracked as two separate
    curation-debt rows. Without the line number a fixed second-instance
    edit could silently exempt the first instance via signature collapse.
    """
    return (
        flag["path"],
        flag["pattern"],
        flag["match"].strip(),
        flag.get("body_line"),
    )


def _expected_sig(item):
    """Convert an allowlist entry (list or dict) to the canonical tuple key."""
    if isinstance(item, list):
        # Pad to length 4 in case an older allowlist omitted body_line.
        return tuple(list(item) + [None] * (4 - len(item)))[:4]
    return (
        item.get("path"),
        item.get("pattern"),
        (item.get("match") or "").strip(),
        item.get("body_line"),
    )


def compute(corpus_dir: Path, expected_path: Path):
    flags, by_zone = collect_flags(corpus_dir)
    expected = load_expected(expected_path)
    expected_sigs = {_expected_sig(item) for item in expected}

    live_sigs = {flag_signature(f) for f in flags}
    new_flags = [f for f in flags if flag_signature(f) not in expected_sigs]
    obsolete_expected = sorted(
        sig for sig in expected_sigs if sig not in live_sigs
    )

    return {
        "total_entries_scanned": len(list(corpus_dir.glob("*/*/SKILL.md"))),
        "flag_count": len(flags),
        "expected_count": len(expected_sigs),
        "new_flag_count": len(new_flags),
        "obsolete_expected_count": len(obsolete_expected),
        "by_zone_counts": by_zone,
        "flags": flags,
        "new_flags": new_flags,
        "obsolete_expected": [
            {
                "path": s[0],
                "pattern": s[1],
                "match": s[2],
                "body_line": s[3],
            }
            for s in obsolete_expected
        ],
    }


def _render_human(summary):
    out = []
    out.append(
        f"numeric-claims audit (issue #39) -- "
        f"{summary['total_entries_scanned']} entries scanned"
    )
    out.append("=" * 72)
    bz = summary["by_zone_counts"]
    out.append("")
    out.append("zone breakdown (numeric tokens matched by pattern):")
    out.append(f"  caveat zone (exempt)          : {bz['caveat']}")
    out.append(f"  tool-contract zone (exempt)   : {bz['tool_contract']}")
    out.append(f"  markdown table (exempt)       : {bz['table']}")
    out.append(
        f"  validation zone, TODO nearby  : {bz['validation_with_todo']}"
    )
    out.append(
        f"  validation zone, NO todo (FLAG): {bz['validation_without_todo']}"
    )
    out.append(f"  body zone, TODO nearby        : {bz['body_with_todo']}")
    out.append(f"  body zone, NO todo (FLAG)     : {bz['body_without_todo']}")
    out.append("")
    out.append(
        f"total flags                   : {summary['flag_count']}"
    )
    out.append(
        f"expected (curation-debt)      : {summary['expected_count']}"
    )
    out.append(
        f"NEW flags (not on allowlist)  : {summary['new_flag_count']}"
    )
    out.append(
        f"obsolete entries on allowlist : {summary['obsolete_expected_count']}"
    )
    if summary["new_flags"]:
        out.append("")
        out.append("NEW flags (these break strict mode):")
        out.append("-" * 72)
        for f in summary["new_flags"]:
            out.append(
                f"  ! {f['path']}:{f['body_line']}  "
                f"[{f['pattern']}] {f['match']!r}  zone={f['zone']!r}  "
                f"section={f['section_title']!r}"
            )
    if summary["obsolete_expected"]:
        out.append("")
        out.append(
            "Obsolete allowlist entries (no longer match anything -- "
            "remove from numeric_claims_expected.json):"
        )
        for s in summary["obsolete_expected"]:
            out.append(
                f"  - {s['path']}:{s.get('body_line')}  "
                f"[{s['pattern']}] {s['match']!r}"
            )
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="audit_numeric_claims.py",
        description=(
            "Audit unflagged numeric tolerances / factors in per-entry "
            "SKILL.md bodies (issue #39). Reports any numeric tolerance "
            "or multiplicative-factor token in the prose that is not "
            "accompanied by a TODO_verify / TBD / provisional marker "
            "within +/- 2 lines, classified by section zone. Stdlib only."
        ),
    )
    p.add_argument("--json", action="store_true",
                   help="emit machine-readable JSON")
    p.add_argument("--strict", action="store_true",
                   help=(
                       "exit non-zero if any NEW flag (not on the "
                       "expected-flags allowlist) exists, or any "
                       "expected entry no longer matches anything"
                   ))
    p.add_argument(
        "--update-expected", action="store_true",
        help=(
            "overwrite references/numeric_claims_expected.json with the "
            "live audit's flag set. Use sparingly -- the steady-state "
            "answer is to drain debt by adding TODO_verify to bodies, "
            "not by silencing the audit."
        ),
    )
    args = p.parse_args(argv)

    if not CORPUS.is_dir():
        raise SystemExit(
            f"audit_numeric_claims.py: corpus dir not found: {CORPUS}"
        )

    summary = compute(CORPUS, EXPECTED_PATH)

    if args.update_expected:
        payload = {
            "_comment": (
                "Curation-debt allowlist for scripts/audit_numeric_claims.py "
                "(issue #39). Each entry is a (path, pattern, match) tuple "
                "that the audit currently reports but is documented as "
                "known. Drain this list by adding 'TODO_verify' near each "
                "match in the source SKILL.md (not by silencing the audit)."
            ),
            "expected": [
                {
                    "path": f["path"],
                    "pattern": f["pattern"],
                    "match": f["match"].strip(),
                    "body_line": f["body_line"],
                }
                for f in summary["flags"]
            ],
        }
        EXPECTED_PATH.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            f"audit_numeric_claims.py: wrote "
            f"{len(payload['expected'])} expected-flag entries to "
            f"{EXPECTED_PATH.relative_to(BUNDLE)}",
            file=sys.stderr,
        )

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(_render_human(summary))

    if args.strict:
        if summary["new_flag_count"] > 0 or summary["obsolete_expected_count"] > 0:
            print(
                f"audit_numeric_claims.py: FAIL -- "
                f"{summary['new_flag_count']} new unflagged numeric "
                f"claim(s); {summary['obsolete_expected_count']} obsolete "
                f"allowlist entries.",
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
