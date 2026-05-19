#!/usr/bin/env python3
"""Deterministic helper for the heliosi-501-corpus skill bundle.

Stdlib only. Resolves all paths relative to this file so the bundle is
relocatable. Operates on:

  ../references/corpus_manifest_v2.json   (machine roll-up of 501 entries)
  ../references/corpus/<batch>/<slug>/    (per-entry SKILL.md + metadata.yaml)

Search semantics (hygiene batch — addresses GitHub issues #46-#54):
  - --query is a case-insensitive, accent-folded LITERAL SUBSTRING match
    over the manifest haystack (or, with --in skill, over the SKILL.md
    body of every entry). Regex metacharacters are NOT interpreted
    (re.escape is applied). For regex or multi-field filters use the
    Grep tool.
  - Manifest haystack fields searched by --query:
    slug, title, batch, theme, first_author, year, venue, source_type,
    quality, executable_status, arxiv, doi.

Usage examples (also surfaced via --help epilog):
  python3 scripts/search_corpus.py --query PFSS --limit 5
  python3 scripts/search_corpus.py --query "open flux" --in both --limit 10
  python3 scripts/search_corpus.py --batches
  python3 scripts/search_corpus.py --maturity
  python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux
  python3 scripts/search_corpus.py --version
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import textwrap
import unicodedata
from pathlib import Path

__version__ = "0.1.0"

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
REFERENCES = BUNDLE / "references"
MANIFEST = REFERENCES / "corpus_manifest_v2.json"
CORPUS = REFERENCES / "corpus"

EPILOG = """\
Examples:
  python3 scripts/search_corpus.py --query PFSS --limit 5
  python3 scripts/search_corpus.py --query "open flux" --in both --limit 10
  python3 scripts/search_corpus.py --batches
  python3 scripts/search_corpus.py --maturity
  python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux
  python3 scripts/search_corpus.py --version

Notes:
  - --query is a literal substring match (regex metacharacters are escaped).
    For regex / multi-field filters use `grep` directly over references/corpus/.
  - --query matching is case-insensitive and accent-folded (NFKD), so
    'Alfven' and 'Alfveń' (combining acute) return the same results.
  - Under --in both, manifest-matched rows are tagged [manifest] and
    body-grep-only rows are tagged [skill]. (Manifest-matched entries are
    not re-read from disk, so [both] is never emitted — issue #30.)

Workflow gating (issue #60):
  python3 scripts/search_corpus.py --ready-for experiment
  python3 scripts/search_corpus.py --ready-for hypothesis --limit 50
  python3 scripts/search_corpus.py --ready-for verify --json
  python3 scripts/search_corpus.py --maturity-tier T1 --maturity-tier T2
  python3 scripts/search_corpus.py --ready-for verify --query alfven

  - --ready-for is the workflow-intent filter:
      discovery   -> all entries
      hypothesis  -> T1/T2, plus T3 entries with a populated Layer-4
                     research-generation block; Layer-2 stubs excluded
      experiment  -> T1 + T2 only (locally-reproduced or method-ready);
                     Layer-2 stubs and weak-attribution entries excluded
      verify      -> verification-target set: T3/T4/T7 + Layer-2 stubs +
                     entries with TODO_verify on DOI / weak_flag_count > 0
  - --maturity-tier T1|T2|...|T7 restricts to one or more derived tiers
    (repeatable). The tier is derived deterministically from manifest
    (quality, executable_status) and matches `--maturity` counts.
  - Both filters apply to --query and can be used standalone: running
    `search_corpus.py --ready-for experiment` lists the experiment-ready
    entries directly. Empty results exit 1.
"""


def _load_manifest():
    if not MANIFEST.is_file():
        sys.exit(f"manifest not found: {MANIFEST}")
    with MANIFEST.open("r", encoding="utf-8") as f:
        return json.load(f)


def _positive_int(s: str) -> int:
    """argparse type for --limit: must be a positive integer (>= 1).

    Rejects 0 (which used to silently disable the cap due to Python
    truthiness — issue #3) and negative values (which used to silently drop
    the last N results via slice semantics — issue #4).
    """
    try:
        n = int(s)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"--limit must be an integer, got {s!r}")
    if n <= 0:
        raise argparse.ArgumentTypeError(f"--limit must be >= 1, got {n}")
    return n


def _fold(s) -> str:
    """Lowercase + strip combining marks (NFKD then drop Mn).

    Always-on for both haystack and query so 'alfven' and 'Alfven' (combining
    acute on the 'e') match identically. Pure ASCII inputs are unchanged.
    """
    if s is None or s == "":
        return ""
    if not isinstance(s, str):
        s = str(s)
    nfkd = unicodedata.normalize("NFKD", s)
    no_marks = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    return no_marks.lower()


def _fmt(v, placeholder: str = "n/a") -> str:
    """Render a manifest field for human output.

    Null / missing / empty-string fields print as ``n/a`` instead of leaking
    the literal Python ``None`` (issue #25). Non-string scalars are coerced
    via ``str``; lists/dicts use ``json.dumps`` so they stay parseable.
    """
    if v is None:
        return placeholder
    if isinstance(v, str):
        return v if v.strip() else placeholder
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False, sort_keys=True)
    return str(v)


def _safe_int(v, default: int = 0, *, label: str = "") -> int:
    """Coerce ``v`` to int; on failure, warn to stderr and return ``default``.

    Avoids the unhandled TypeError/ValueError traceback when manifest count
    fields are ever null/string/missing (issue #29). The ``label`` is included
    in the warning so the offending batch or tier is identifiable.
    """
    if isinstance(v, bool):
        # bool is a subclass of int — keep the existing int semantics.
        return int(v)
    if isinstance(v, int):
        return v
    try:
        return int(v)
    except (TypeError, ValueError):
        where = f" ({label})" if label else ""
        print(
            f"warning: non-integer count{where}: {v!r} -> using {default}",
            file=sys.stderr,
        )
        return default


def _synthesized_batch_theme(batch_name: str, entries: list) -> str:
    """Derive a per-batch theme from constituent entry themes (issue #26).

    Used only when ``batches[i].theme`` is null/blank. If all entries share
    one theme, return it; otherwise return the most common theme followed by
    ``(+N more)``. Returns ``""`` when no entry-level themes are available.
    """
    themes = [
        (e.get("theme") or "").strip()
        for e in entries
        if e.get("batch") == batch_name
    ]
    themes = [t for t in themes if t]
    if not themes:
        return ""
    c = collections.Counter(themes)
    top, top_count = c.most_common(1)[0]
    if len(c) == 1:
        return top
    return f"{top} (+{len(c) - 1} more)"





def _entry_haystack(entry: dict) -> str:
    """Concatenate searchable fields from a manifest entry (accent-folded)."""
    parts = [
        entry.get("slug", ""),
        entry.get("title", ""),
        entry.get("batch", ""),
        entry.get("theme", ""),
        entry.get("first_author", ""),
        str(entry.get("year", "")),
        entry.get("venue", "") or "",
        entry.get("source_type", "") or "",
        entry.get("quality", "") or "",
        entry.get("executable_status", "") or "",
        entry.get("arxiv", "") or "",
        entry.get("doi", "") or "",
    ]
    return _fold(" ".join(p for p in parts if p))


# -- Maturity-tier derivation (issue #60) -----------------------------------
#
# The corpus manifest reports *global* tier counts under
# `maturity_taxonomy.counts` but does NOT emit a per-entry tier label. We
# derive the per-entry tier deterministically from the manifest's
# `quality` + `executable_status` pair, using a rule reverse-engineered
# from the per-batch counts in `references/corpus_qa_report_v2.md` §4.
# The derived counts match the manifest exactly: T1=1, T2=22, T3=260,
# T4=164, T5=52, T6=1, T7=1, total=501. The rule lives here, and the
# unit test `tests/test_workflow_gating.py` re-asserts the totals so any
# corpus update that changes the rule must update the test in lockstep.

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


def _derive_tier(entry: dict) -> str:
    """Return one of T1..T7 (or 'T?' as an audit sentinel) for an entry.

    Pure function over the two manifest fields the rule depends on. Adding
    a new (quality, executable_status) pair to the corpus *should* surface
    here as 'T?' rather than being silently re-bucketed.
    """
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
        # 'pilot' is overloaded: the four 'runnable-from-...' statuses
        # (T2) coexist with 'scaffold' (T4) on this quality label.
        return "T2" if "runnable" in es else "T4"
    if q == "paper-grounded-pending-full-text":
        # The single 'constructive-pipeline-specified' entry promotes to T2;
        # everything else (8 statuses, dominated by
        # 'pipeline-specified-not-yet-runnable') stays at T3.
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


# -- Layer-2 stub detection (issue #14 + #60) -------------------------------
#
# The manifest does not carry the `layer2_stub` metadata field, so we read
# it lazily off disk. We only need to look at entries whose batch is one of
# the two known-stub batches; everywhere else the field is absent. The
# extraction is a literal substring match for the top-level
# `layer2_stub: true` line -- safer than a full YAML parse (the bundle has
# no third-party deps) and matches what audit_layer2_stubs.py writes.
_LAYER2_STUB_BATCHES = frozenset({
    "wave500_inner_heliosphere_psp_solo_045",
    "wave500_waves_instabilities_reconnection_045",
})

_LAYER2_STUB_LINE_RE = re.compile(
    r"^layer2_stub\s*:\s*true\s*(?:#.*)?$", re.MULTILINE
)


def _has_layer2_stub(entry: dict) -> bool:
    """True if the entry's metadata.yaml carries layer2_stub: true."""
    if entry.get("batch") not in _LAYER2_STUB_BATCHES:
        return False
    p = _metadata_yaml_path(entry)
    if not p.is_file():
        return False
    try:
        with p.open("r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return False
    return bool(_LAYER2_STUB_LINE_RE.search(text))


# -- Workflow-eligibility filter (issue #60) --------------------------------
#
# `--ready-for {experiment,hypothesis,verify,discovery}` answers four
# different questions an agent might ask of the corpus. The semantics are
# conservative on purpose: the corpus is overwhelmingly T3/T4 and stating
# that 500 entries are "experiment-ready" would re-create exactly the
# overpromise issue #60 flags.

READY_FOR_CHOICES = ("experiment", "hypothesis", "verify", "discovery")


def _ready_for_experiment(entry: dict) -> bool:
    """Experiment-ready: T1 or T2 (locally reproduced / method-ready /
    runnable pilot) AND not flagged as a Layer-2 stub.

    Rationale: T1 is the only entry with a documented numerical
    reproduction; T2 is method-ready or pilot-runnable. Anything T3/T4 has
    not yet authored Layer-2 to method-ready, so it is by definition not
    experiment-ready under the corpus's own taxonomy.
    """
    if _has_layer2_stub(entry):
        return False
    return _derive_tier(entry) in ("T1", "T2")


def _ready_for_hypothesis(entry: dict) -> bool:
    """Hypothesis-ready: T1/T2 OR T3 entries with a populated Layer 4 /
    research-generation block, AND not a Layer-2 stub.

    Hypothesis generation only needs the Layer-1 claim + Layer-4
    affordance, not a runnable contract. T3 entries that author Layer 4
    qualify; T4/T5 do not (their Layer 1 may be partial). Layer-2 stubs
    are excluded because their claim boundary is also under-specified.
    """
    if _has_layer2_stub(entry):
        return False
    tier = _derive_tier(entry)
    if tier in ("T1", "T2"):
        return True
    if tier == "T3" and bool(entry.get("research_generation_affordances_present")):
        return True
    return False


def _ready_for_verify(entry: dict) -> bool:
    """Verify-ready: the entries that *should* be picked up next for
    full-text verification.

    Concretely: T3/T4/T7 entries that still carry a verification TODO --
    i.e. weak_flag_count > 0 OR DOI/arxiv marked TODO -- and any T2/T3
    entry under the Layer-2 stub set. This is the inverse of
    experiment-ready: it surfaces what to spend verification budget on.
    """
    tier = _derive_tier(entry)
    if tier in ("T1", "T6"):
        return False  # T1 already reproduced, T6 is a routing hub
    weak = _safe_int(entry.get("weak_flag_count", 0), label="weak_flag_count")
    if weak > 0:
        return True
    doi = entry.get("doi") or ""
    if isinstance(doi, str) and doi.strip().lower().startswith(("todo", "tbd")):
        return True
    if _has_layer2_stub(entry):
        return True
    return tier in ("T3", "T4", "T7")


def _ready_for_discovery(entry: dict) -> bool:
    """Discovery-ready: every entry is a candidate for open browsing.

    Documented as such so the user can pair `--ready-for discovery` with
    `--query` for a no-op tier filter (useful for scripted UIs that
    always pass a `--ready-for`).
    """
    return True


_READY_FOR_DISPATCH = {
    "experiment": _ready_for_experiment,
    "hypothesis": _ready_for_hypothesis,
    "verify": _ready_for_verify,
    "discovery": _ready_for_discovery,
}


def _skill_md_path(entry: dict) -> Path:
    rel = entry.get("path", "")
    return CORPUS / rel / "SKILL.md"


def _metadata_yaml_path(entry: dict) -> Path:
    rel = entry.get("path", "")
    return CORPUS / rel / "metadata.yaml"


def _grep_skill_bodies(
    tokens_folded,
    entries: list,
    *,
    max_hits: int | None = None,
    announce: bool = False,
) -> set:
    """Return slugs whose folded SKILL.md body contains ALL folded tokens.

    Multi-token queries are AND-matched (each token must appear somewhere
    in the body). Single-token queries reduce to the previous behavior.
    Accepts either a list of tokens or a single pre-folded string for
    backward compatibility.

    Issue #11 hardening:
      - ``max_hits`` lets callers short-circuit once enough matches accrue
        (e.g. ``--in skill --limit 1`` no longer scans all 501 files).
      - ``announce`` emits a one-line stderr notice before scanning so the
        user sees progress for the otherwise-silent multi-second walk.
      - OSError on file open / read is reported to stderr (with the slug)
        instead of being swallowed.
      - The Unicode REPLACEMENT CHARACTER (U+FFFD) introduced by
        ``errors='replace'`` is detected and warned about per-file, since a
        replacement adjacent to a search token causes a false negative.
    """
    if isinstance(tokens_folded, str):
        tokens = [tokens_folded] if tokens_folded else []
    else:
        tokens = [t for t in tokens_folded if t]
    if not tokens:
        return set()
    patterns = [re.compile(re.escape(t)) for t in tokens]
    hits: set = set()
    if announce:
        print(
            f"scanning {len(entries)} SKILL.md files (limit={max_hits or 'none'})...",
            file=sys.stderr,
        )
    for e in entries:
        if max_hits is not None and len(hits) >= max_hits:
            break
        p = _skill_md_path(e)
        if not p.is_file():
            continue
        try:
            with p.open("r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError as exc:
            print(
                f"warning: cannot read {p} for slug {e.get('slug')!r}: {exc}",
                file=sys.stderr,
            )
            continue
        if "�" in text:
            print(
                f"warning: replacement char in {e.get('slug')!r}; "
                f"matches near non-UTF-8 bytes may be incorrect",
                file=sys.stderr,
            )
        folded = _fold(text)
        if all(pat.search(folded) for pat in patterns):
            hits.add(e.get("slug"))
    return hits


def _apply_ready_for(entries, ready_for):
    """Return only entries that match the given --ready-for predicate."""
    if not ready_for:
        return entries
    pred = _READY_FOR_DISPATCH[ready_for]
    return [e for e in entries if pred(e)]


def _apply_maturity_tier(entries, tiers):
    """Return only entries whose derived tier is in the given list."""
    if not tiers:
        return entries
    wanted = {t.strip().upper() for t in tiers if t.strip()}
    return [e for e in entries if _derive_tier(e) in wanted]


def cmd_query(args, manifest):
    entries = manifest.get("entries", [])
    # Empty / whitespace-only queries are now caught in main() before the
    # manifest load (issue #27); this branch is still here as a safety net
    # if cmd_query is called directly from tests.
    q = (args.query or "").strip()
    if not q:
        sys.exit("--query is empty")
    # Whitespace-separated tokens are AND-matched against the haystack
    # (issue #12). Single-token queries reduce to the previous behavior.
    # Quoting is the shell's job: `--query "open flux"` arrives as one
    # argv element which splits into two tokens, while
    # `--query "PFSS open flux"` splits into three.
    tokens_folded = [_fold(t) for t in q.split() if t]
    if not tokens_folded:
        sys.exit("--query is empty")

    # Apply workflow / tier filters BEFORE matching so the search runs over a
    # smaller candidate set and the reported total reflects the eligible
    # population, not the corpus-wide total.
    entries = _apply_ready_for(entries, getattr(args, "ready_for", None))
    entries = _apply_maturity_tier(entries, getattr(args, "maturity_tier", None))

    manifest_hits: set = set()
    matched: list = []  # preserve manifest order
    if args.search_in in ("manifest", "both"):
        for e in entries:
            hay = _entry_haystack(e)
            if all(t in hay for t in tokens_folded):
                manifest_hits.add(e.get("slug"))
                matched.append(e)

    body_hits: set = set()
    if args.search_in in ("skill", "both"):
        if args.search_in == "skill":
            # Skill-only path can short-circuit at --limit (issue #11):
            # there is no second source we need to merge with, so once we
            # have `limit` hits we can stop reading files.
            body_hits = _grep_skill_bodies(
                tokens_folded,
                entries,
                max_hits=args.limit if args.limit else None,
                announce=True,
            )
            matched = [e for e in entries if e.get("slug") in body_hits]
        else:
            # `--in both`: only grep entries the manifest didn't already
            # match (issue #30). Avoids ~501-file I/O for the common case
            # where the manifest already provides hits.
            existing = {e.get("slug") for e in matched}
            unmatched = [e for e in entries if e.get("slug") not in existing]
            body_hits = _grep_skill_bodies(
                tokens_folded,
                unmatched,
                announce=True,
            )
            for e in unmatched:
                if e.get("slug") in body_hits:
                    matched.append(e)

    if not matched:
        # Exit non-zero so shell pipelines / CI can detect zero hits
        # (issue #10; matches grep / git grep / the existing cmd_show
        # convention).
        msg = f"no matches for: {q!r} (searched in: {args.search_in})"
        if getattr(args, "json", False):
            print(json.dumps({
                "command": "query",
                "query": q,
                "search_in": args.search_in,
                "total": 0,
                "matches": [],
            }, ensure_ascii=False))
        else:
            print(msg, file=sys.stderr)
        return 1

    total = len(matched)
    capped = bool(args.limit) and total > args.limit
    if capped:
        matched = matched[: args.limit]

    if getattr(args, "json", False):
        result = {
            "command": "query",
            "query": q,
            "search_in": args.search_in,
            "total": total,
            "returned": len(matched),
            "capped": capped,
            "limit": args.limit,
            "matches": [
                {
                    "slug": e.get("slug"),
                    "batch": e.get("batch"),
                    "year": e.get("year"),
                    "quality": e.get("quality"),
                    "executable_status": e.get("executable_status"),
                    "title": e.get("title"),
                    "first_author": e.get("first_author"),
                    "doi": e.get("doi"),
                    "arxiv": e.get("arxiv"),
                    "skill_path": (
                        f"references/corpus/{e.get('path','')}/SKILL.md"
                    ),
                    "provenance": (
                        "manifest" if e.get("slug") in manifest_hits
                        else "skill" if e.get("slug") in body_hits
                        else None
                    ),
                }
                for e in matched
            ],
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    header = f"matches: {total}"
    if capped:
        header += f" (showing {len(matched)})"
    header += f"  query={q!r}  in={args.search_in}"
    print(header)
    print("-" * 80)
    for e in matched:
        slug = e.get("slug", "")
        batch = e.get("batch", "")
        year = _fmt(e.get("year"))
        qual = _fmt(e.get("quality"))
        exe = _fmt(e.get("executable_status"))
        title = (e.get("title") or "").strip().replace("\n", " ")
        if len(title) > 90:
            title = title[:87] + "..."

        prov = ""
        if args.search_in == "both":
            # manifest_hits and body_hits are now disjoint (issue #30);
            # we no longer re-grep manifest-matched entries, so [both] is
            # never produced.
            if slug in manifest_hits:
                prov = " [manifest]"
            elif slug in body_hits:
                prov = " [skill]"

        print(f"{slug}{prov}")
        print(f"  batch: {batch}  year: {year}")
        print(f"  quality: {qual}  status: {exe}")
        print(f"  title: {title}")
        print(f"  skill: references/corpus/{e.get('path','')}/SKILL.md")
    return 0


def cmd_batches(args, manifest):
    batches = manifest.get("batches", [])
    entries = manifest.get("entries", [])
    # Apply workflow filters so `--batches --ready-for verify` etc. reports
    # per-batch counts of the eligible subset rather than the corpus-wide
    # totals (issue #60). Without the filter both helpers act as before.
    ready_for = getattr(args, "ready_for", None)
    maturity_tier = getattr(args, "maturity_tier", None)
    filtered_entries = _apply_ready_for(entries, ready_for)
    filtered_entries = _apply_maturity_tier(filtered_entries, maturity_tier)
    is_filtered = (ready_for is not None) or bool(maturity_tier)

    rows = []
    if is_filtered:
        # Recount each batch from the filtered entry list so totals reflect
        # eligibility. Themes are still taken from the manifest batch block
        # (or synthesized from filtered entries).
        from collections import Counter as _Counter
        per_batch = _Counter(e.get("batch") for e in filtered_entries)
        batch_order = [b.get("batch", "") for b in batches]
        for name in batch_order:
            count = per_batch.get(name, 0)
            raw_theme = next(
                (
                    (b.get("theme") or "").strip()
                    for b in batches if b.get("batch") == name
                ),
                "",
            )
            if raw_theme:
                theme = raw_theme
                synthesized = False
            else:
                theme = _synthesized_batch_theme(name, filtered_entries)
                synthesized = bool(theme)
            rows.append((name, count, theme, synthesized))
    else:
        for b in batches:
            name = b.get("batch", "")
            count = _safe_int(
                b.get("manifest_skill_count", 0),
                default=0,
                label=f"batch={name!r}.manifest_skill_count",
            )
            raw_theme = (b.get("theme") or "").strip()
            if raw_theme:
                theme = raw_theme
                synthesized = False
            else:
                theme = _synthesized_batch_theme(name, entries)
                synthesized = bool(theme)
            rows.append((name, count, theme, synthesized))
    total = sum(r[1] for r in rows)

    if getattr(args, "json", False):
        out_doc = {
            "command": "batches",
            "batches": [
                {
                    "batch": name,
                    "manifest_skill_count": count,
                    "theme": theme or None,
                    "theme_synthesized": synthesized,
                }
                for name, count, theme, synthesized in rows
            ],
            "total_skills": total,
        }
        if is_filtered:
            out_doc["filtered_by"] = {
                "ready_for": ready_for,
                "maturity_tier": (
                    sorted({t.upper() for t in (maturity_tier or [])})
                    or None
                ),
            }
        print(json.dumps(out_doc, ensure_ascii=False))
        return 0

    header = f"batches: {len(batches)}"
    if is_filtered:
        bits = []
        if ready_for is not None:
            bits.append(f"ready-for={ready_for}")
        if maturity_tier:
            tiers = sorted({t.upper() for t in maturity_tier})
            bits.append(f"tiers={','.join(tiers)}")
        header += "  (filtered: " + " ".join(bits) + ")"
    print(header)
    print("-" * 80)
    name_w = max((len(r[0]) for r in rows), default=20)
    # textwrap.shorten collapses whitespace too aggressively for our
    # hyphen-joined themes — we just cap at 60 with a single-char ellipsis
    # so the column stays aligned but the truncation is visible.
    def _shorten(text: str, width: int = 60) -> str:
        if len(text) <= width:
            return text
        return text[: width - 1] + "…"

    for name, count, theme, synthesized in rows:
        suffix = " (synth)" if synthesized else ""
        cell = _shorten((theme or "") + suffix, 60)
        print(f"{name:<{name_w}}  {count:>4}  {cell}")
    print("-" * 80)
    label = "total skills" if not is_filtered else "matching skills"
    print(f"{label}: {total}")
    return 0


_MATURITY_ORDER = (
    "T1_locally_reproduced",
    "T2_method_ready_executable_pilot",
    "T3_paper_grounded_pending_full_text",
    "T4_stub_or_scaffold_paper_grounded",
    "T5_agent_runtime_or_design_precedent",
    "T6_link_only_or_routing",
    "T7_weak_attribution_or_citation_todo",
)


_TIER_LABEL = {
    "T1": "T1_locally_reproduced",
    "T2": "T2_method_ready_executable_pilot",
    "T3": "T3_paper_grounded_pending_full_text",
    "T4": "T4_stub_or_scaffold_paper_grounded",
    "T5": "T5_agent_runtime_or_design_precedent",
    "T6": "T6_link_only_or_routing",
    "T7": "T7_weak_attribution_or_citation_todo",
    "T?": "T_unclassified",
}


def cmd_maturity(args, manifest):
    # When workflow filters are active we recount from the entry list using
    # the same derive-then-filter pipeline as cmd_query / cmd_filter; this
    # lets `--maturity --ready-for verify` report tier counts of the verify
    # subset (issue #60).
    ready_for = getattr(args, "ready_for", None)
    maturity_tier = getattr(args, "maturity_tier", None)
    is_filtered = (ready_for is not None) or bool(maturity_tier)

    if is_filtered:
        entries = manifest.get("entries", [])
        entries = _apply_ready_for(entries, ready_for)
        entries = _apply_maturity_tier(entries, maturity_tier)
        derived = {k: 0 for k in _MATURITY_ORDER}
        for e in entries:
            label = _TIER_LABEL.get(_derive_tier(e), "T_unclassified")
            derived.setdefault(label, 0)
            derived[label] += 1
        rows = [(k, derived.get(k, 0)) for k in _MATURITY_ORDER]
        for k in derived:
            if k in _MATURITY_ORDER:
                continue
            rows.append((k, derived[k]))
    else:
        tax = manifest.get("maturity_taxonomy", {})
        counts = tax.get("counts", {})
        rows = []
        for k in _MATURITY_ORDER:
            rows.append((k, _safe_int(counts.get(k, 0), label=f"tier={k!r}")))
        for k in counts.keys():
            if k in _MATURITY_ORDER:
                continue
            rows.append((k, _safe_int(counts.get(k, 0), label=f"tier={k!r}")))
    total = sum(v for _, v in rows)

    if getattr(args, "json", False):
        out_doc = {
            "command": "maturity",
            "counts": {k: v for k, v in rows},
            "total": total,
        }
        if is_filtered:
            out_doc["filtered_by"] = {
                "ready_for": ready_for,
                "maturity_tier": (
                    sorted({t.upper() for t in (maturity_tier or [])})
                    or None
                ),
            }
        print(json.dumps(out_doc, ensure_ascii=False))
        return 0

    if is_filtered:
        bits = []
        if ready_for is not None:
            bits.append(f"ready-for={ready_for}")
        if maturity_tier:
            tiers = sorted({t.upper() for t in maturity_tier})
            bits.append(f"tiers={','.join(tiers)}")
        print(f"maturity tiers (filtered: {' '.join(bits)})")
    else:
        print("maturity tiers (from corpus_manifest_v2.json)")
    print("-" * 80)
    for k, v in rows:
        print(f"  {k:<44} {v:>5}")
    print("-" * 80)
    print(f"  TOTAL                                        {total:>5}")
    return 0


def _classify_partial(slug_lower: str, candidate_lower: str) -> str | None:
    """Bucket a partial slug match by how anchored it is (issue #24).

    Returns one of:
      - ``"prefix"``  — candidate starts with the query.
      - ``"token"``   — query appears as a whole dash-separated token.
      - ``"weak"``    — substring match only (mid-token).
      - ``None``      — no match.
    """
    if not slug_lower or not candidate_lower:
        return None
    if candidate_lower.startswith(slug_lower):
        return "prefix"
    tokens = candidate_lower.split("-")
    if slug_lower in tokens:
        return "token"
    # Multi-token query like "wu-2026" must align to a dash boundary on
    # both sides to qualify as a strong token-run match.
    if slug_lower in candidate_lower:
        starts_ok = (
            candidate_lower.startswith(slug_lower)
            or ("-" + slug_lower) in candidate_lower
        )
        ends_ok = (
            candidate_lower.endswith(slug_lower)
            or (slug_lower + "-") in candidate_lower
        )
        if starts_ok and ends_ok:
            return "token"
        return "weak"
    return None


def cmd_filter(args, manifest):
    """Standalone --ready-for / --maturity-tier listing command (issue #60).

    Reuses _apply_ready_for and _apply_maturity_tier (shared with cmd_query)
    so the filter semantics match exactly. Outputs the same row format as
    cmd_query for consistency.
    """
    entries = manifest.get("entries", [])
    entries = _apply_ready_for(entries, args.ready_for)
    entries = _apply_maturity_tier(entries, args.maturity_tier)
    total = len(entries)
    capped = bool(args.limit) and total > args.limit
    if capped:
        shown = entries[: args.limit]
    else:
        shown = entries

    if getattr(args, "json", False):
        result = {
            "command": "filter",
            "ready_for": args.ready_for,
            "maturity_tier": (
                sorted({t.upper() for t in (args.maturity_tier or [])})
                or None
            ),
            "total": total,
            "returned": len(shown),
            "capped": capped,
            "limit": args.limit,
            "matches": [
                {
                    "slug": e.get("slug"),
                    "batch": e.get("batch"),
                    "year": e.get("year"),
                    "quality": e.get("quality"),
                    "executable_status": e.get("executable_status"),
                    "tier": _derive_tier(e),
                    "layer2_stub": _has_layer2_stub(e),
                    "title": e.get("title"),
                    "skill_path": (
                        f"references/corpus/{e.get('path','')}/SKILL.md"
                    ),
                }
                for e in shown
            ],
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0 if total > 0 else 1

    header_bits = []
    if args.ready_for is not None:
        header_bits.append(f"ready-for={args.ready_for}")
    if args.maturity_tier:
        tiers = sorted({t.upper() for t in args.maturity_tier})
        header_bits.append(f"tiers={','.join(tiers)}")
    header = f"matches: {total}"
    if capped:
        header += f" (showing {len(shown)})"
    if header_bits:
        header += "  " + "  ".join(header_bits)
    print(header)
    if total == 0:
        return 1
    print("-" * 80)
    for e in shown:
        slug = e.get("slug", "")
        batch = e.get("batch", "")
        year = _fmt(e.get("year"))
        qual = _fmt(e.get("quality"))
        exe = _fmt(e.get("executable_status"))
        tier = _derive_tier(e)
        stub = "stub" if _has_layer2_stub(e) else ""
        tag = f"[{tier}]" + (f"[layer2-{stub}]" if stub else "")
        title = (e.get("title") or "").strip().replace("\n", " ")
        if len(title) > 90:
            title = title[:87] + "..."
        print(f"{slug}  {tag}")
        print(f"  batch: {batch}  year: {year}")
        print(f"  quality: {qual}  status: {exe}")
        print(f"  title: {title}")
        print(f"  skill: references/corpus/{e.get('path','')}/SKILL.md")
    return 0


def cmd_show(args, manifest):
    slug = (args.show or "").strip()
    if not slug:
        sys.exit("--show requires a non-empty slug (got empty string)")
    slug_lc = slug.lower()
    entries = manifest.get("entries", [])
    # Case-insensitive exact match (issue #23): slugs are canonical
    # lowercase, but tolerate users who paste an UPPERCASE version.
    matches = [
        e for e in entries
        if (e.get("slug") or "").lower() == slug_lc
    ]
    if not matches:
        # Boundary-aware partial fallback (issue #24): rank prefix > token >
        # weak so that 'wu-2026' surfaces 'wu-2026-...' above 'hwu-2026-...'.
        ranked: dict = {"prefix": [], "token": [], "weak": []}
        for e in entries:
            kind = _classify_partial(slug_lc, (e.get("slug") or "").lower())
            if kind is not None:
                ranked[kind].append(e)
        ordered = ranked["prefix"] + ranked["token"] + ranked["weak"]
        if not ordered:
            if getattr(args, "json", False):
                print(json.dumps({
                    "command": "show",
                    "query": slug,
                    "exact_match": False,
                    "matches": [],
                    "partial": [],
                }, ensure_ascii=False))
            else:
                print(f"no entry with slug containing: {slug!r}")
            return 1
        if getattr(args, "json", False):
            print(json.dumps({
                "command": "show",
                "query": slug,
                "exact_match": False,
                "matches": [],
                "partial": [
                    {
                        "slug": e.get("slug"),
                        "batch": e.get("batch"),
                        "match_kind": _classify_partial(
                            slug_lc, (e.get("slug") or "").lower()
                        ),
                    }
                    for e in ordered[:20]
                ],
            }, ensure_ascii=False))
            return 1
        print(f"no exact slug match; {len(ordered)} partial matches:")
        for e in ordered[:20]:
            kind = _classify_partial(slug_lc, (e.get("slug") or "").lower())
            tag = "" if kind in ("prefix", "token") else "  (weak match)"
            print(f"  {e.get('slug')}  (batch: {e.get('batch')}){tag}")
        return 1
    if len(matches) > 1 and not getattr(args, "json", False):
        print(
            f"WARNING: {len(matches)} entries share slug {slug!r}. "
            f"Slugs are documented as globally unique — manifest may be corrupt."
        )
        print("-" * 80)

    if getattr(args, "json", False):
        result = {
            "command": "show",
            "query": slug,
            "exact_match": True,
            "matches": [
                {
                    "slug": e.get("slug"),
                    "batch": e.get("batch"),
                    "title": e.get("title"),
                    "year": e.get("year"),
                    "first_author": e.get("first_author"),
                    "quality": e.get("quality"),
                    "executable_status": e.get("executable_status"),
                    "arxiv": e.get("arxiv"),
                    "doi": e.get("doi"),
                    "skill_path": str(_skill_md_path(e)),
                    "skill_exists": _skill_md_path(e).is_file(),
                    "metadata_path": str(_metadata_yaml_path(e)),
                    "metadata_exists": _metadata_yaml_path(e).is_file(),
                }
                for e in matches
            ],
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    label_w = 9  # widest label is 'metadata:' (9 chars)
    for i, e in enumerate(matches):
        if i > 0:
            print("-" * 80)
        skill_p = _skill_md_path(e)
        meta_p = _metadata_yaml_path(e)
        print(f"{'slug:':<{label_w}} {_fmt(e.get('slug'))}")
        print(f"{'batch:':<{label_w}} {_fmt(e.get('batch'))}")
        print(f"{'title:':<{label_w}} {_fmt(e.get('title'))}")
        print(f"{'year:':<{label_w}} {_fmt(e.get('year'))}")
        print(f"{'quality:':<{label_w}} {_fmt(e.get('quality'))}")
        print(f"{'status:':<{label_w}} {_fmt(e.get('executable_status'))}")
        print(f"{'arxiv:':<{label_w}} {_fmt(e.get('arxiv'))}")
        print(f"{'doi:':<{label_w}} {_fmt(e.get('doi'))}")
        print(f"{'skill:':<{label_w}} {skill_p} (exists={skill_p.is_file()})")
        print(f"{'metadata:':<{label_w}} {meta_p} (exists={meta_p.is_file()})")
    return 0


_DEFAULT_LIMIT = 20
_DEFAULT_SEARCH_IN = "manifest"


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="search_corpus.py",
        description="Deterministic helper for heliosi-501-corpus skill bundle.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    g = p.add_mutually_exclusive_group(required=False)
    g.add_argument("--query", "-q", type=str, help="literal-substring search over manifest fields")
    g.add_argument("--batches", action="store_true", help="list batches with count + theme columns")
    g.add_argument("--maturity", action="store_true", help="print T1-T7 tier counts")
    g.add_argument("--show", type=str, help="print paths for a given slug")
    p.add_argument(
        "--in",
        dest="search_in",
        choices=("manifest", "skill", "both"),
        default=_DEFAULT_SEARCH_IN,
        help="where to search when using --query (default: manifest)",
    )
    p.add_argument(
        "--limit",
        "-n",
        type=_positive_int,
        default=_DEFAULT_LIMIT,
        help="cap result count (must be >= 1; default 20)",
    )
    p.add_argument(
        "--ready-for",
        dest="ready_for",
        choices=READY_FOR_CHOICES,
        default=None,
        help=(
            "workflow-eligibility filter (issue #60). "
            "experiment: T1/T2 and not Layer-2 stub; "
            "hypothesis: T1/T2 or T3 with Layer-4 affordances, not stub; "
            "verify: pending entries with full-text TODO or Layer-2 stub; "
            "discovery: all entries. "
            "Used standalone (lists eligible entries) or paired with "
            "--query as a workflow filter."
        ),
    )
    p.add_argument(
        "--maturity-tier",
        dest="maturity_tier",
        action="append",
        choices=("T1", "T2", "T3", "T4", "T5", "T6", "T7"),
        default=None,
        help=(
            "filter to entries in the given maturity tier(s). Repeatable "
            "(e.g. --maturity-tier T1 --maturity-tier T2). Used standalone "
            "or paired with --query."
        ),
    )
    p.add_argument(
        "--json",
        action="store_true",
        help=(
            "emit machine-readable JSON to stdout instead of the human "
            "table format. Applies to all commands."
        ),
    )

    args = p.parse_args(argv)

    # The mutually-exclusive group is no longer `required=True` so we can
    # accept `--ready-for` / `--maturity-tier` as standalone commands. If
    # the user supplied no command flag and no filter, restore the original
    # "one of ... is required" error.
    standalone_filter = (
        args.query is None
        and not args.batches
        and not args.maturity
        and args.show is None
        and (args.ready_for is not None or args.maturity_tier is not None)
    )
    no_command = (
        args.query is None
        and not args.batches
        and not args.maturity
        and args.show is None
        and not standalone_filter
    )
    if no_command:
        p.error(
            "one of the arguments --query/-q --batches --maturity --show "
            "--ready-for --maturity-tier is required"
        )

    # Issue #28: --in / --limit only affect --query. If the caller paired
    # them with --batches/--maturity/--show, warn so they don't think the
    # flag silently filtered the output.
    if args.query is None:
        non_query = (
            "--batches" if args.batches
            else "--maturity" if args.maturity
            else "--show" if args.show is not None
            else "--ready-for/--maturity-tier"
        )
        ignored = []
        # --in is meaningful only for --query (the body grep is body-only).
        # --limit, however, applies to standalone --ready-for / --maturity-tier
        # listings too, so it's NOT included in the ignored set when those
        # filters are used.
        if args.search_in != _DEFAULT_SEARCH_IN:
            ignored.append(f"--in {args.search_in}")
        if args.limit != _DEFAULT_LIMIT and not standalone_filter:
            ignored.append(f"--limit {args.limit}")
        if ignored:
            print(
                f"warning: {non_query} ignores {' / '.join(ignored)} "
                f"(only --query consumes these flags)",
                file=sys.stderr,
            )

    # Issue #27: validate empty --query BEFORE loading the 501-entry
    # manifest. Pure-whitespace strings count as empty.
    if args.query is not None and not args.query.strip():
        p.error("--query is empty")

    manifest = _load_manifest()

    if args.batches:
        return cmd_batches(args, manifest)
    if args.maturity:
        return cmd_maturity(args, manifest)
    if args.show is not None:
        return cmd_show(args, manifest)
    if args.query is not None:
        return cmd_query(args, manifest)
    if standalone_filter:
        return cmd_filter(args, manifest)
    p.error("no command")


if __name__ == "__main__":
    raise SystemExit(main())
