#!/usr/bin/env python3
"""Deterministic helper for the heliosi-501-corpus skill bundle.

Stdlib only. Resolves all paths relative to this file so the bundle is
relocatable. Operates on:

  ../references/corpus_manifest_v2.json   (machine roll-up of 501 entries)
  ../references/corpus/<batch>/<slug>/    (per-entry SKILL.md + metadata.yaml)

Usage examples:
  python3 scripts/search_corpus.py --query PFSS --limit 5
  python3 scripts/search_corpus.py --query "open flux" --in both --limit 10
  python3 scripts/search_corpus.py --batches
  python3 scripts/search_corpus.py --maturity
  python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
REFERENCES = BUNDLE / "references"
MANIFEST = REFERENCES / "corpus_manifest_v2.json"
CORPUS = REFERENCES / "corpus"


def _load_manifest():
    if not MANIFEST.is_file():
        sys.exit(f"manifest not found: {MANIFEST}")
    with MANIFEST.open("r", encoding="utf-8") as f:
        return json.load(f)


def _entry_haystack(entry: dict) -> str:
    """Concatenate searchable fields from a manifest entry."""
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
    return " ".join(p for p in parts if p).lower()


def _skill_md_path(entry: dict) -> Path:
    rel = entry.get("path", "")
    return CORPUS / rel / "SKILL.md"


def _metadata_yaml_path(entry: dict) -> Path:
    rel = entry.get("path", "")
    return CORPUS / rel / "metadata.yaml"


def _grep_skill_bodies(query_lower: str, entries: list) -> set:
    """Return slugs whose SKILL.md body contains query_lower."""
    hits = set()
    pat = re.compile(re.escape(query_lower), re.IGNORECASE)
    for e in entries:
        p = _skill_md_path(e)
        if not p.is_file():
            continue
        try:
            with p.open("r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        if pat.search(text):
            hits.add(e.get("slug"))
    return hits


def cmd_query(args, manifest):
    entries = manifest.get("entries", [])
    q = args.query.strip()
    if not q:
        sys.exit("--query is empty")
    q_lower = q.lower()

    matched = []
    if args.search_in in ("manifest", "both"):
        for e in entries:
            if q_lower in _entry_haystack(e):
                matched.append(e)

    if args.search_in in ("skill", "both"):
        body_hits = _grep_skill_bodies(q_lower, entries)
        if args.search_in == "skill":
            matched = [e for e in entries if e.get("slug") in body_hits]
        else:
            existing = {e.get("slug") for e in matched}
            for e in entries:
                if e.get("slug") in body_hits and e.get("slug") not in existing:
                    matched.append(e)

    if not matched:
        print(f"no matches for: {q!r} (searched in: {args.search_in})")
        return 0

    total = len(matched)
    if args.limit and total > args.limit:
        matched = matched[: args.limit]

    print(f"matches: {total} (showing {len(matched)})  query={q!r}  in={args.search_in}")
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
        print(f"{slug}")
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
    slug = args.show.strip()
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
    for e in matches:
        skill_p = _skill_md_path(e)
        meta_p = _metadata_yaml_path(e)
        print(f"slug:     {e.get('slug')}")
        print(f"batch:    {e.get('batch')}")
        print(f"title:    {e.get('title')}")
        print(f"year:     {e.get('year')}")
        print(f"quality:  {e.get('quality')}")
        print(f"status:   {e.get('executable_status')}")
        print(f"arxiv:    {e.get('arxiv')}")
        print(f"doi:      {e.get('doi')}")
        print(f"skill:    {skill_p}  (exists={skill_p.is_file()})")
        print(f"metadata: {meta_p}   (exists={meta_p.is_file()})")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="search_corpus.py",
        description="Deterministic helper for heliosi-501-corpus skill bundle.",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--query", "-q", type=str, help="substring search over manifest fields")
    g.add_argument("--batches", action="store_true", help="list batches with counts")
    g.add_argument("--maturity", action="store_true", help="print T1–T7 tier counts")
    g.add_argument("--show", type=str, help="print paths for a given slug")
    p.add_argument(
        "--in",
        dest="search_in",
        choices=("manifest", "skill", "both"),
        default="manifest",
        help="where to search when using --query (default: manifest)",
    )
    p.add_argument("--limit", "-n", type=int, default=20, help="cap result count (default 20)")

    args = p.parse_args(argv)
    manifest = _load_manifest()

    if args.batches:
        return cmd_batches(manifest)
    if args.maturity:
        return cmd_maturity(manifest)
    if args.show:
        return cmd_show(args, manifest)
    if args.query is not None:
        return cmd_query(args, manifest)
    p.error("no command")


if __name__ == "__main__":
    raise SystemExit(main())
