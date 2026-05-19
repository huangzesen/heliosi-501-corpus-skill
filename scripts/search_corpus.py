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
    rows = []
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
        print(json.dumps({
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
        }, ensure_ascii=False))
        return 0

    print(f"batches: {len(batches)}")
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
    print(f"total skills: {total}")
    return 0


def cmd_maturity(args, manifest):
    tax = manifest.get("maturity_taxonomy", {})
    counts = tax.get("counts", {})
    order = [
        "T1_locally_reproduced",
        "T2_method_ready_executable_pilot",
        "T3_paper_grounded_pending_full_text",
        "T4_stub_or_scaffold_paper_grounded",
        "T5_agent_runtime_or_design_precedent",
        "T6_link_only_or_routing",
        "T7_weak_attribution_or_citation_todo",
    ]
    rows = []
    for k in order:
        rows.append((k, _safe_int(counts.get(k, 0), label=f"tier={k!r}")))
    for k in counts.keys():
        if k in order:
            continue
        rows.append((k, _safe_int(counts.get(k, 0), label=f"tier={k!r}")))
    total = sum(v for _, v in rows)

    if getattr(args, "json", False):
        print(json.dumps({
            "command": "maturity",
            "counts": {k: v for k, v in rows},
            "total": total,
        }, ensure_ascii=False))
        return 0

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
    g = p.add_mutually_exclusive_group(required=True)
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
        "--json",
        action="store_true",
        help=(
            "emit machine-readable JSON to stdout instead of the human "
            "table format. Applies to --query/--show/--batches/--maturity."
        ),
    )

    args = p.parse_args(argv)

    # Issue #28: --in / --limit only affect --query. If the caller paired
    # them with --batches/--maturity/--show, warn so they don't think the
    # flag silently filtered the output.
    if args.query is None:
        non_query = (
            "--batches" if args.batches
            else "--maturity" if args.maturity
            else "--show"
        )
        ignored = []
        if args.search_in != _DEFAULT_SEARCH_IN:
            ignored.append(f"--in {args.search_in}")
        if args.limit != _DEFAULT_LIMIT:
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
    p.error("no command")


if __name__ == "__main__":
    raise SystemExit(main())
