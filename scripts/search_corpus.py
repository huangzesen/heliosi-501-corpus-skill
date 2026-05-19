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
import json
import re
import sys
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
  - Under --in both, each row is tagged [manifest], [skill], or [both]
    so callers can tell which source matched.
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


def _grep_skill_bodies(tokens_folded, entries: list) -> set:
    """Return slugs whose folded SKILL.md body contains ALL folded tokens.

    Multi-token queries are AND-matched (each token must appear somewhere
    in the body). Single-token queries reduce to the previous behavior.
    Accepts either a list of tokens or a single pre-folded string for
    backward compatibility.
    """
    if isinstance(tokens_folded, str):
        tokens = [tokens_folded] if tokens_folded else []
    else:
        tokens = [t for t in tokens_folded if t]
    if not tokens:
        return set()
    patterns = [re.compile(re.escape(t)) for t in tokens]
    hits = set()
    for e in entries:
        p = _skill_md_path(e)
        if not p.is_file():
            continue
        try:
            with p.open("r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        folded = _fold(text)
        if all(pat.search(folded) for pat in patterns):
            hits.add(e.get("slug"))
    return hits


def cmd_query(args, manifest):
    entries = manifest.get("entries", [])
    q = args.query.strip()
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

    manifest_hits = set()
    matched = []  # preserve manifest order
    if args.search_in in ("manifest", "both"):
        for e in entries:
            hay = _entry_haystack(e)
            if all(t in hay for t in tokens_folded):
                manifest_hits.add(e.get("slug"))
                matched.append(e)

    body_hits = set()
    if args.search_in in ("skill", "both"):
        body_hits = _grep_skill_bodies(tokens_folded, entries)
        if args.search_in == "skill":
            matched = [e for e in entries if e.get("slug") in body_hits]
        else:
            existing = {e.get("slug") for e in matched}
            for e in entries:
                if e.get("slug") in body_hits and e.get("slug") not in existing:
                    matched.append(e)

    if not matched:
        # Exit non-zero so shell pipelines / CI can detect zero hits
        # (issue #10; matches grep / git grep / the existing cmd_show
        # convention).
        print(
            f"no matches for: {q!r} (searched in: {args.search_in})",
            file=sys.stderr,
        )
        return 1

    total = len(matched)
    capped = bool(args.limit) and total > args.limit
    if capped:
        matched = matched[: args.limit]

    header = f"matches: {total}"
    if capped:
        header += f" (showing {len(matched)})"
    header += f"  query={q!r}  in={args.search_in}"
    print(header)
    print("-" * 80)
    for e in matched:
        slug = e.get("slug", "")
        batch = e.get("batch", "")
        year = e.get("year", "")
        qual = e.get("quality", "")
        exe = e.get("executable_status", "")
        title = (e.get("title") or "").strip().replace("\n", " ")
        if len(title) > 90:
            title = title[:87] + "..."

        prov = ""
        if args.search_in == "both":
            in_m = slug in manifest_hits
            in_b = slug in body_hits
            if in_m and in_b:
                prov = " [both]"
            elif in_m:
                prov = " [manifest]"
            elif in_b:
                prov = " [skill]"

        print(f"{slug}{prov}")
        print(f"  batch: {batch}  year: {year}")
        print(f"  quality: {qual}  status: {exe}")
        print(f"  title: {title}")
        print(f"  skill: references/corpus/{e.get('path','')}/SKILL.md")
    return 0


def cmd_batches(manifest):
    batches = manifest.get("batches", [])
    print(f"batches: {len(batches)}")
    print("-" * 80)
    rows = []
    for b in batches:
        rows.append(
            (
                b.get("batch", ""),
                int(b.get("manifest_skill_count", 0)),
                b.get("theme", "") or "",
            )
        )
    name_w = max((len(r[0]) for r in rows), default=20)
    for name, count, theme in rows:
        theme_short = theme[:60]
        print(f"{name:<{name_w}}  {count:>4}  {theme_short}")
    total = sum(r[1] for r in rows)
    print("-" * 80)
    print(f"total skills: {total}")
    return 0


def cmd_maturity(manifest):
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
    print("maturity tiers (from corpus_manifest_v2.json)")
    print("-" * 80)
    total = 0
    for k in order:
        v = int(counts.get(k, 0))
        total += v
        print(f"  {k:<44} {v:>5}")
    other_keys = [k for k in counts.keys() if k not in order]
    for k in other_keys:
        v = int(counts.get(k, 0))
        total += v
        print(f"  {k:<44} {v:>5}")
    print("-" * 80)
    print(f"  TOTAL                                        {total:>5}")
    return 0


def cmd_show(args, manifest):
    slug = (args.show or "").strip()
    if not slug:
        sys.exit("--show requires a non-empty slug (got empty string)")
    entries = manifest.get("entries", [])
    matches = [e for e in entries if e.get("slug") == slug]
    if not matches:
        sub = [e for e in entries if slug.lower() in (e.get("slug") or "").lower()]
        if not sub:
            print(f"no entry with slug containing: {slug!r}")
            return 1
        print(f"no exact slug match; {len(sub)} partial matches:")
        for e in sub[:20]:
            print(f"  {e.get('slug')}  (batch: {e.get('batch')})")
        return 1
    if len(matches) > 1:
        print(
            f"WARNING: {len(matches)} entries share slug {slug!r}. "
            f"Slugs are documented as globally unique — manifest may be corrupt."
        )
        print("-" * 80)
    label_w = 9  # widest label is 'metadata:' (9 chars)
    for i, e in enumerate(matches):
        if i > 0:
            print("-" * 80)
        skill_p = _skill_md_path(e)
        meta_p = _metadata_yaml_path(e)
        print(f"{'slug:':<{label_w}} {e.get('slug')}")
        print(f"{'batch:':<{label_w}} {e.get('batch')}")
        print(f"{'title:':<{label_w}} {e.get('title')}")
        print(f"{'year:':<{label_w}} {e.get('year')}")
        print(f"{'quality:':<{label_w}} {e.get('quality')}")
        print(f"{'status:':<{label_w}} {e.get('executable_status')}")
        print(f"{'arxiv:':<{label_w}} {e.get('arxiv')}")
        print(f"{'doi:':<{label_w}} {e.get('doi')}")
        print(f"{'skill:':<{label_w}} {skill_p} (exists={skill_p.is_file()})")
        print(f"{'metadata:':<{label_w}} {meta_p} (exists={meta_p.is_file()})")
    return 0


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
        default="manifest",
        help="where to search when using --query (default: manifest)",
    )
    p.add_argument(
        "--limit",
        "-n",
        type=_positive_int,
        default=20,
        help="cap result count (must be >= 1; default 20)",
    )

    args = p.parse_args(argv)
    manifest = _load_manifest()

    if args.batches:
        return cmd_batches(manifest)
    if args.maturity:
        return cmd_maturity(manifest)
    if args.show is not None:
        return cmd_show(args, manifest)
    if args.query is not None:
        return cmd_query(args, manifest)
    p.error("no command")


if __name__ == "__main__":
    raise SystemExit(main())
