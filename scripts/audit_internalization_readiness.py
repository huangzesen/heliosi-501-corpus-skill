#!/usr/bin/env python3
"""Audit internalization / agent-native readiness across the 501 paper-skills.

Jason's invariant for a "shipped" paper-skill is two-sided:

  (a) **bibliographic anchor** — a stable handle a downstream agent (or a
      reviewer reading the corpus blind) can use to locate the source
      paper (DOI, arXiv ID, ADS bibcode, code repo, or verified URL);
  (b) **agent-native content** — Layer-1 narrow-form claim, Layer-2
      executable protocol against abstract capabilities, validation
      target, and (when present) Layer-4 research affordances must be
      authored beyond the factory's TODO scaffolds.

Many entries currently satisfy (a) but ship Layer-2 / Layer-4 sections
that are the factory's boilerplate ("documented in the paper; runtime
supplies the named capability", "abstract procedure: the runtime that
wants to borrow this pattern...", "Not benchmarked yet — promotion
requires…"). Those are TODO-equivalent: they declare the *shape* of
content without the content. This audit quantifies that gap so other
daemons can prioritize the worst debt.

The script is **non-blocking by default** — it prints a per-entry score
and ranking and exits 0 even when many entries fall below the readiness
bar. ``--strict-active`` raises a non-zero exit code only when *active*
entries (quality_level in {method-ready, paper-grounded-locally-
reproduced, pilot, pilot_weak_attribution}) fall below the
``--min-active-score`` threshold. This keeps the audit safe to wire into
``scripts/validate.sh`` without making the existing 85 % T3+T4 debt
block CI.

Stdlib + PyYAML (matches scripts/audit_layer_population.py). When PyYAML
is missing the script prints a SKIP banner to stderr and exits 0, in
parallel with validate.sh's S4c/S4d convention.

Usage examples::

    python3 scripts/audit_internalization_readiness.py --top 30
    python3 scripts/audit_internalization_readiness.py --json
    python3 scripts/audit_internalization_readiness.py --top 50 \\
        --output /tmp/readiness.txt
    python3 scripts/audit_internalization_readiness.py --strict-active \\
        --min-active-score 70
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


# --- Score weights (sum to 100; penalties are subtractive on top) ----------

WEIGHT_BIB_ANCHOR = 25
WEIGHT_IDENTITY = 10
WEIGHT_LAYER1 = 25
WEIGHT_LAYER2 = 20
WEIGHT_VALIDATION = 10
WEIGHT_LAYER4 = 10
# Maximum TODO-density penalty (subtracted from the raw score after
# everything else; protects against gaming the audit by stripping TODOs
# *without* writing real content — see VALIDATION.md "Do not lower
# scores by deleting TODOs.").
MAX_TODO_PENALTY = 15

ACTIVE_QUALITIES = {
    "method-ready",
    "paper-grounded-locally-reproduced",
    "pilot",
    "pilot_weak_attribution",
}

# Factory-boilerplate phrases that mark a section as TODO-equivalent
# even though it doesn't carry a literal ``TODO_verify`` marker. Each
# string here was confirmed by grep across the live corpus on
# 2026-05-19; counts are documented inline so a future curator can spot
# drift.
# Matched case-insensitively (the design-pattern template ships with
# "Abstract procedure:" capitalized while the psp-solo placeholder is
# lower-case).
LAYER2_BOILERPLATE = (
    # 45 entries in wave500_inner_heliosphere_psp_solo_045 (issue #14
    # class A) ship Layer-2 algorithm rows that just say "documented in
    # the paper; runtime supplies the named capability".
    "documented in the paper; runtime supplies the named capability",
    # 45 entries in wave500_agent_runtime_eval_design_045 ship the
    # factory's design-pattern-extractor template, whose Method N
    # blocks say "abstract procedure: the runtime that wants to borrow
    # this pattern must be able to..." — declarative without content.
    "abstract procedure: the runtime that wants to borrow this pattern",
)

VALIDATION_BOILERPLATE = (
    # ~254 entries (mostly wave500) carry the factory's default
    # "Not benchmarked yet — promotion requires…" Layer-2 §5 stub.
    "Not benchmarked yet",
    "Not benchmarked yet -- this is a",
)

LAYER4_BOILERPLATE = (
    "Adapter notes intentionally empty",
)

# Markers that flag a TODO/placeholder string in metadata.yaml /
# SKILL.md. We deliberately treat the full family (TODO_verify_*,
# TBD, TODO verify, unverified, provisional) as one bucket — these
# are the factory's triage tokens (see SKILL.md "Verification status
# (read first)").
TODO_RE = re.compile(
    r"\b(?:TODO[_ ]?verify(?:_with_full_text)?|TBD|TODO\b|unverified|provisional)",
    re.IGNORECASE,
)


def _load_yaml():
    try:
        import yaml  # PyYAML
    except ImportError:
        return None
    return yaml


def _parse_metadata(path, yaml_mod):
    try:
        with open(path) as f:
            return yaml_mod.safe_load(f)
    except Exception:
        return None


def _parse_skill_frontmatter(path, yaml_mod):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None, ""
    body = text
    fm = None
    if text.startswith("---\n"):
        try:
            end = text.index("\n---", 4)
            try:
                fm = yaml_mod.safe_load(text[4:end])
            except Exception:
                fm = None
            body = text[end + 4 :]
        except ValueError:
            fm = None
            body = text
    return fm, body


# --- Field probes ----------------------------------------------------------


def _is_meaningful_string(value):
    """A string field counts as 'meaningful' if it is non-empty, not a
    bare placeholder, and does not start with TODO/TBD/null-equivalent
    text. The check is intentionally lenient on internal TODO tokens
    inside an otherwise authored field — we don't want a single inline
    TODO to mask a 200-word claim section."""
    if value is None:
        return False
    if not isinstance(value, str):
        return False
    s = value.strip()
    if not s:
        return False
    low = s.lower()
    if low in {"null", "none", "n/a", "tbd", "todo"}:
        return False
    if low.startswith("todo_verify") or low.startswith("todo verify"):
        return False
    if low.startswith("todo:") or low.startswith("tbd:"):
        return False
    return True


def _is_meaningful_list(value):
    if not isinstance(value, list):
        return False
    cleaned = [v for v in value if v not in (None, "", [])]
    if not cleaned:
        return False
    # If every entry is itself a TODO placeholder, treat as empty.
    real = 0
    for v in cleaned:
        if isinstance(v, str):
            if _is_meaningful_string(v):
                real += 1
        else:
            real += 1
    return real > 0


def _bib_anchor_signal(meta, skill_fm):
    """Compute the bibliographic-anchor sub-score 0..WEIGHT_BIB_ANCHOR.

    Six tiers, each contributing up to ~4-5 pts, with verified arXiv /
    DOI weighted heaviest because those are the things Jason's review
    actually cared about.
    """
    bits = {
        "arxiv": False,
        "doi": False,
        "ads": False,
        "url_or_code": False,
        "id_verifications": False,
        "external_links": False,
    }
    if isinstance(meta, dict):
        if _is_meaningful_string(meta.get("arxiv")) or _is_meaningful_string(
            meta.get("arxiv_id")
        ):
            bits["arxiv"] = True
        if _is_meaningful_string(meta.get("doi")):
            bits["doi"] = True
        if _is_meaningful_string(meta.get("ads_bibcode")) or _is_meaningful_string(
            meta.get("ads")
        ):
            bits["ads"] = True
        prov = meta.get("provenance") or {}
        if isinstance(prov, dict):
            idv = prov.get("id_verifications")
            if isinstance(idv, list) and any(isinstance(r, dict) for r in idv):
                bits["id_verifications"] = True
        ext = meta.get("external_links") or meta.get("links")
        if _is_meaningful_list(ext) or (
            isinstance(ext, dict)
            and any(_is_meaningful_string(v) for v in ext.values())
        ):
            bits["external_links"] = True
    if isinstance(skill_fm, dict):
        paper = skill_fm.get("paper") or {}
        if isinstance(paper, dict):
            if _is_meaningful_string(paper.get("arxiv_id")) or _is_meaningful_string(
                paper.get("arxiv")
            ):
                bits["arxiv"] = True
            if _is_meaningful_string(paper.get("doi")):
                bits["doi"] = True
            if _is_meaningful_string(paper.get("ads_bibcode")) or _is_meaningful_string(
                paper.get("ads")
            ):
                bits["ads"] = True
        links = skill_fm.get("links")
        if isinstance(links, dict) and any(
            _is_meaningful_string(v) for v in links.values()
        ):
            bits["external_links"] = True
            code = links.get("code_repo") or links.get("code")
            if _is_meaningful_string(code):
                bits["url_or_code"] = True
    if not bits["url_or_code"] and bits["external_links"]:
        # external_links covers it
        bits["url_or_code"] = True

    weights = {
        "arxiv": 6,
        "doi": 6,
        "ads": 3,
        "url_or_code": 3,
        "id_verifications": 4,
        "external_links": 3,
    }
    score = sum(weights[k] for k, v in bits.items() if v)
    return min(score, WEIGHT_BIB_ANCHOR), bits


def _identity_signal(meta, skill_fm):
    title_ok = False
    year_ok = False
    venue_ok = False
    if isinstance(meta, dict):
        if _is_meaningful_string(meta.get("title")):
            title_ok = True
        if isinstance(meta.get("year"), int):
            year_ok = True
        elif _is_meaningful_string(meta.get("year")):
            year_ok = True
        if _is_meaningful_string(meta.get("journal")) or _is_meaningful_string(
            meta.get("venue")
        ):
            venue_ok = True
    if isinstance(skill_fm, dict):
        paper = skill_fm.get("paper") or {}
        if isinstance(paper, dict):
            if _is_meaningful_string(paper.get("title")):
                title_ok = True
            if isinstance(paper.get("year"), int):
                year_ok = True
            elif _is_meaningful_string(paper.get("year")):
                year_ok = True
            if _is_meaningful_string(paper.get("venue")) or _is_meaningful_string(
                paper.get("journal")
            ):
                venue_ok = True
    pts = (4 if title_ok else 0) + (3 if year_ok else 0) + (3 if venue_ok else 0)
    return pts, {"title": title_ok, "year": year_ok, "venue": venue_ok}


# --- Body section extractor ------------------------------------------------


# Three rendering families coexist in the corpus (see
# references/corpus_qa_report_v2.md §13). Detect each layer's section by
# header pattern; pick the longest match if multiple families fire.
LAYER1_HEADERS = [
    r"^##\s+Layer\s*1\b",
    r"^##\s+\d+\.?\s+Scientific\b",
    r"^##\s+\d+\.?\s+Paper\s+claim\b",
    r"^##\s+Scientific\s+claim\b",
    r"^##\s+Paper\s+identity\b",
]
LAYER2_HEADERS = [
    r"^##\s+Layer\s*2\b",
    r"^##\s+\d+\.?\s+Executable\b",
    r"^##\s+\d+\.?\s+Methods?\s*/?\s*equations\b",
    r"^##\s+Algorithm",
]
VALIDATION_HEADERS = [
    r"^###?\s+Validation\s+target\b",
    r"^##\s+\d+\.?\s+Validation\b",
    r"^##\s+Minimal\s+executable\s+benchmark\b",
]
LAYER4_HEADERS = [
    r"^##\s+Layer\s*4\b",
    r"^##\s+\d+\.?\s+Skill\s+graph\b",
    r"^##\s+\d+\.?\s+Research[- ]generation\b",
    r"^##\s+Research[- ]generation\b",
]


def _extract_section(body, header_patterns, next_header_pattern=r"^##\s"):
    """Return the longest section under any matching H2 header. We pick
    the longest because the wave500 design-pattern family uses very
    short sections, while baseline batches author long ones — under-
    counting would be the *honest* failure mode (we want to flag short
    sections as debt, not over-credit them)."""
    best = ""
    lines = body.splitlines()
    n = len(lines)
    for i, line in enumerate(lines):
        if any(re.match(p, line) for p in header_patterns):
            # Find next H2 after this header.
            j = i + 1
            while j < n and not re.match(next_header_pattern, lines[j]):
                j += 1
            section = "\n".join(lines[i:j])
            if len(section) > len(best):
                best = section
    return best


def _layer1_signal(body, meta):
    sec = _extract_section(body, LAYER1_HEADERS)
    has_section = bool(sec.strip())
    long_enough = len(sec) >= 600  # ~10 lines minimum
    has_claim = False
    has_failure = False
    has_targets = False
    if has_section:
        low = sec.lower()
        if "claim" in low and ("narrow" in low or "boundary" in low or "verifiable" in low):
            has_claim = True
        if "failure mode" in low or "pitfall" in low or "skill memory" in low:
            has_failure = True
        if (
            "figure" in low
            or "numerical target" in low
            or "validation target" in low
            or re.search(r"\d", sec) is not None and "target" in low
        ):
            has_targets = True
    # Pure TODO check: if the section is mostly TODO placeholders, dock.
    todo_in_section = len(TODO_RE.findall(sec)) if has_section else 0
    todo_dense = (
        has_section
        and todo_in_section > 0
        and todo_in_section * 80 > max(len(sec), 1)
    )
    # Validation targets present in metadata.yaml count too.
    vt_meta = (
        _is_meaningful_list(meta.get("validation_targets"))
        if isinstance(meta, dict)
        else False
    )
    pts = 0
    if has_section:
        pts += 8
    if long_enough:
        pts += 5
    if has_claim:
        pts += 5
    if has_failure:
        pts += 4
    if has_targets or vt_meta:
        pts += 3
    if todo_dense:
        pts = max(0, pts - 5)
    return min(pts, WEIGHT_LAYER1), {
        "has_section": has_section,
        "long_enough": long_enough,
        "has_claim": has_claim,
        "has_failure_modes": has_failure,
        "has_targets": has_targets,
        "todo_dense": todo_dense,
    }


def _layer2_signal(body, meta):
    sec = _extract_section(body, LAYER2_HEADERS)
    has_section = bool(sec.strip())
    long_enough = len(sec) >= 500
    has_capabilities = False
    has_procedure = False
    boilerplate = False
    layer2_stub_flag = False
    if has_section:
        low = sec.lower()
        if (
            "capabilit" in low
            or "abstract capabilit" in low
            or re.search(r"\b[Cc]-[A-Z][A-Z0-9_-]+\b", sec)
            or re.search(r"`[a-z_]+\.[a-z_]+\(", sec)
        ):
            has_capabilities = True
        if (
            "procedure" in low
            or "algorithm" in low
            or "steps" in low
            or re.search(r"^\s*\d+\.\s", sec, re.M)
        ):
            has_procedure = True
        sec_low = sec.lower()
        for needle in LAYER2_BOILERPLATE:
            if needle.lower() in sec_low:
                boilerplate = True
                break
    if isinstance(meta, dict) and meta.get("layer2_stub") is True:
        layer2_stub_flag = True
    pts = 0
    if has_section:
        pts += 6
    if long_enough:
        pts += 5
    if has_capabilities:
        pts += 5
    if has_procedure:
        pts += 4
    if boilerplate or layer2_stub_flag:
        pts = max(0, pts - 12)
    return min(pts, WEIGHT_LAYER2), {
        "has_section": has_section,
        "long_enough": long_enough,
        "has_capabilities": has_capabilities,
        "has_procedure": has_procedure,
        "boilerplate": boilerplate,
        "layer2_stub_flag": layer2_stub_flag,
    }


def _validation_signal(body, meta):
    has_meta = (
        isinstance(meta, dict)
        and _is_meaningful_list(meta.get("validation_targets"))
    )
    sec = _extract_section(body, VALIDATION_HEADERS)
    has_section = bool(sec.strip())
    has_numeric = bool(re.search(r"\d", sec)) if has_section else False
    boilerplate = False
    if has_section:
        sec_low = sec.lower()
        for needle in VALIDATION_BOILERPLATE:
            if needle.lower() in sec_low:
                boilerplate = True
                break
    # Detect "validation_target: null" at frontmatter level.
    if isinstance(meta, dict):
        vt_meta_list = meta.get("validation_targets") or []
        if isinstance(vt_meta_list, list):
            # If every entry contains a TODO marker, dock.
            if vt_meta_list and all(
                TODO_RE.search(str(v) or "") for v in vt_meta_list
            ):
                has_meta = False
    pts = 0
    if has_meta:
        pts += 5
    if has_section:
        pts += 3
    if has_numeric:
        pts += 3
    if boilerplate:
        pts = max(0, pts - 5)
    return min(pts, WEIGHT_VALIDATION), {
        "has_meta_validation_targets": has_meta,
        "has_section": has_section,
        "has_numeric_reference": has_numeric,
        "boilerplate": boilerplate,
    }


def _layer4_signal(body, meta, skill_fm):
    sec = _extract_section(body, LAYER4_HEADERS)
    has_section = bool(sec.strip())
    long_enough = len(sec) >= 400
    has_meta_affordances = False
    has_skill_fm_affordances = False
    if isinstance(meta, dict):
        if _is_meaningful_list(meta.get("research_generation_affordances")):
            has_meta_affordances = True
        # The 213-entry SKILL.md-frontmatter family puts these on the
        # frontmatter only and flags them via the
        # ``research_generation_affordances_present`` boolean.
        if meta.get("research_generation_affordances_present") is True:
            has_meta_affordances = True
    if isinstance(skill_fm, dict):
        if _is_meaningful_list(skill_fm.get("research_generation_affordances")):
            has_skill_fm_affordances = True
    boilerplate = False
    if has_section:
        sec_low = sec.lower()
        for needle in LAYER4_BOILERPLATE:
            if needle.lower() in sec_low:
                boilerplate = True
                break
    pts = 0
    if has_section:
        pts += 3
    if long_enough:
        pts += 2
    if has_meta_affordances or has_skill_fm_affordances:
        pts += 5
    if boilerplate:
        pts = max(0, pts - 3)
    return min(pts, WEIGHT_LAYER4), {
        "has_section": has_section,
        "long_enough": long_enough,
        "has_meta_affordances": has_meta_affordances,
        "has_skill_fm_affordances": has_skill_fm_affordances,
        "boilerplate": boilerplate,
    }


def _todo_penalty(body, meta_text):
    """Penalty proportional to TODO density across SKILL.md body and
    metadata.yaml raw text. Capped at ``MAX_TODO_PENALTY`` so a single
    busy entry does not dominate the ranking. Importantly this is a
    *penalty*, not the primary metric — deleting TODOs without
    authoring content lowers TODOs but does not raise Layer-1/2/4
    component scores. See VALIDATION.md "Do not lower scores by
    deleting TODOs."
    """
    n_todo = len(TODO_RE.findall(body)) + len(TODO_RE.findall(meta_text or ""))
    total_chars = max(len(body) + len(meta_text or ""), 1)
    # Heuristic: 1 TODO per 1000 chars maps to ~5 pts; 5+/1000 maxes out.
    density_per_1k = n_todo * 1000.0 / total_chars
    penalty = min(MAX_TODO_PENALTY, density_per_1k * 3.0)
    # Also penalize raw TODO count above 10 to catch large entries.
    if n_todo >= 10:
        penalty = max(penalty, min(MAX_TODO_PENALTY, 5.0 + 0.3 * (n_todo - 10)))
    return round(penalty, 2), n_todo


# --- Top-level evaluator ---------------------------------------------------


def score_entry(meta_path, skill_path, yaml_mod):
    meta = _parse_metadata(meta_path, yaml_mod)
    skill_fm, body = _parse_skill_frontmatter(skill_path, yaml_mod)
    meta_text = ""
    try:
        meta_text = meta_path.read_text(encoding="utf-8")
    except OSError:
        pass

    bib_pts, bib_bits = _bib_anchor_signal(meta, skill_fm)
    id_pts, id_bits = _identity_signal(meta, skill_fm)
    l1_pts, l1_bits = _layer1_signal(body, meta)
    l2_pts, l2_bits = _layer2_signal(body, meta)
    val_pts, val_bits = _validation_signal(body, meta)
    l4_pts, l4_bits = _layer4_signal(body, meta, skill_fm)
    todo_pen, n_todo = _todo_penalty(body, meta_text)

    raw = bib_pts + id_pts + l1_pts + l2_pts + val_pts + l4_pts
    score = max(0.0, raw - todo_pen)

    quality = None
    pending = None
    active = None
    tier_class = None
    layer2_stub = None
    if isinstance(meta, dict):
        quality = meta.get("quality_level") or meta.get("quality")
        pending = meta.get("pending")
        active = meta.get("active")
        tier_class = meta.get("tier_class")
        layer2_stub = meta.get("layer2_stub")
    if isinstance(skill_fm, dict):
        if quality is None:
            quality = skill_fm.get("quality")
    is_active = (quality in ACTIVE_QUALITIES) or (tier_class == "active") or (
        active is True
    )

    return {
        "batch": meta_path.parent.parent.name,
        "slug": meta_path.parent.name,
        "quality_level": quality,
        "is_active": is_active,
        "pending": pending,
        "tier_class": tier_class,
        "layer2_stub": layer2_stub,
        "n_todo": n_todo,
        "score": round(score, 2),
        "raw_score": round(raw, 2),
        "todo_penalty": todo_pen,
        "components": {
            "bibliographic_anchor": {
                "score": bib_pts,
                "max": WEIGHT_BIB_ANCHOR,
                "bits": bib_bits,
            },
            "identity": {
                "score": id_pts,
                "max": WEIGHT_IDENTITY,
                "bits": id_bits,
            },
            "layer1_claim": {
                "score": l1_pts,
                "max": WEIGHT_LAYER1,
                "bits": l1_bits,
            },
            "layer2_protocol": {
                "score": l2_pts,
                "max": WEIGHT_LAYER2,
                "bits": l2_bits,
            },
            "validation_target": {
                "score": val_pts,
                "max": WEIGHT_VALIDATION,
                "bits": val_bits,
            },
            "layer4_affordance": {
                "score": l4_pts,
                "max": WEIGHT_LAYER4,
                "bits": l4_bits,
            },
        },
    }


def collect(corpus_root, yaml_mod):
    if not corpus_root.is_dir():
        raise SystemExit(
            f"audit_internalization_readiness.py: corpus dir not found: "
            f"{corpus_root}"
        )
    rows = []
    for meta_path in sorted(corpus_root.glob("*/*/metadata.yaml")):
        skill_path = meta_path.parent / "SKILL.md"
        if not skill_path.is_file():
            continue
        rows.append(score_entry(meta_path, skill_path, yaml_mod))
    return rows


def _summarize(rows):
    n = len(rows)
    if not n:
        return {"total_entries": 0}
    scores = [r["score"] for r in rows]
    by_batch = defaultdict(list)
    by_quality = defaultdict(list)
    active_rows = [r for r in rows if r["is_active"]]
    for r in rows:
        by_batch[r["batch"]].append(r["score"])
        by_quality[r["quality_level"] or "<unknown>"].append(r["score"])
    return {
        "total_entries": n,
        "active_entries": len(active_rows),
        "mean_score": round(sum(scores) / n, 2),
        "median_score": round(sorted(scores)[n // 2], 2),
        "min_score": round(min(scores), 2),
        "max_score": round(max(scores), 2),
        "histogram": _histogram(scores),
        "by_batch_mean": {
            b: round(sum(v) / len(v), 2)
            for b, v in sorted(by_batch.items(), key=lambda kv: sum(kv[1]) / len(kv[1]))
        },
        "by_quality_mean": {
            q: round(sum(v) / len(v), 2)
            for q, v in sorted(
                by_quality.items(), key=lambda kv: sum(kv[1]) / len(kv[1])
            )
        },
        "active_score_min": round(min(r["score"] for r in active_rows), 2)
        if active_rows
        else None,
        "active_score_mean": round(
            sum(r["score"] for r in active_rows) / len(active_rows), 2
        )
        if active_rows
        else None,
    }


def _histogram(scores):
    buckets = [(0, 25), (25, 50), (50, 70), (70, 85), (85, 101)]
    out = {}
    for lo, hi in buckets:
        n = sum(1 for s in scores if lo <= s < hi)
        out[f"{lo}-{hi - 1 if hi != 101 else 100}"] = n
    return out


def _render_human(rows, summary, top_n):
    out = []
    out.append(
        f"internalization-readiness audit — {summary['total_entries']} entries "
        f"scanned ({summary['active_entries']} active)"
    )
    out.append("=" * 72)
    out.append(
        f"  mean score   : {summary['mean_score']}/100   "
        f"median: {summary['median_score']}   "
        f"min: {summary['min_score']}   max: {summary['max_score']}"
    )
    out.append(
        f"  active mean  : {summary['active_score_mean']}   "
        f"active min: {summary['active_score_min']}"
    )
    out.append("")
    out.append("  score histogram (lower = more internalization debt):")
    for bucket, n in summary["histogram"].items():
        bar = "#" * min(60, n // 4 + (1 if n else 0))
        out.append(f"    {bucket:<7s} {n:>4d}  {bar}")
    out.append("")
    out.append("  per-batch mean (ascending — worst-debt batch first):")
    for b, m in summary["by_batch_mean"].items():
        out.append(f"    {b:<52s} {m}")
    out.append("")
    out.append("  per-quality_level mean (ascending):")
    for q, m in summary["by_quality_mean"].items():
        out.append(f"    {q:<48s} {m}")

    out.append("")
    out.append(f"  worst-debt entries (lowest score first, top {top_n}):")
    out.append(
        "    score  L1  L2  Val L4  Bib Id  TODOs  active  batch/slug"
    )
    for r in sorted(rows, key=lambda r: (r["score"], r["slug"]))[:top_n]:
        c = r["components"]
        marker = "*" if r["is_active"] else " "
        out.append(
            f"    {r['score']:>5}  "
            f"{c['layer1_claim']['score']:>2}  "
            f"{c['layer2_protocol']['score']:>2}  "
            f"{c['validation_target']['score']:>2}  "
            f"{c['layer4_affordance']['score']:>2}  "
            f"{c['bibliographic_anchor']['score']:>2}  "
            f"{c['identity']['score']:>2}  "
            f"{r['n_todo']:>4}   {marker}      "
            f"{r['batch']}/{r['slug']}"
        )
    out.append("")
    out.append("  legend: L1=Layer-1 claim, L2=Layer-2 protocol, Val=validation,")
    out.append("          L4=Layer-4 affordance, Bib=bibliographic anchor,")
    out.append("          Id=identity, *=active quality_level (debt blocks promotion)")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="audit_internalization_readiness.py",
        description=(
            "Score each of the 501 paper-skills on internalization / "
            "agent-native readiness (bibliographic anchor + Layer-1 "
            "claim + Layer-2 protocol + validation + Layer-4 "
            "affordance, with a TODO-density penalty). Non-blocking by "
            "default; --strict-active makes the audit fail CI only "
            "when entries flagged as active drop below "
            "--min-active-score."
        ),
    )
    p.add_argument(
        "--top",
        type=int,
        default=30,
        help="rows to print in the worst-debt ranking (human mode)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of the human summary",
    )
    p.add_argument(
        "--output",
        type=str,
        default=None,
        help="write report to this path instead of stdout",
    )
    p.add_argument(
        "--strict-active",
        action="store_true",
        help=(
            "exit non-zero when any active-quality entry "
            "(quality_level in {method-ready, paper-grounded-locally-"
            "reproduced, pilot, pilot_weak_attribution}) scores below "
            "--min-active-score. Safe for CI: 51/501 entries are active."
        ),
    )
    p.add_argument(
        "--min-active-score",
        type=float,
        default=55.0,
        help="threshold used by --strict-active (default 55/100)",
    )
    p.add_argument(
        "--corpus",
        type=str,
        default=str(CORPUS),
        help="override corpus root (defaults to references/corpus/)",
    )
    args = p.parse_args(argv)

    yaml_mod = _load_yaml()
    if yaml_mod is None:
        print(
            "SKIP: PyYAML not installed -- internalization-readiness audit "
            "skipped. Install with `pip install pyyaml`.",
            file=sys.stderr,
        )
        return 0

    rows = collect(Path(args.corpus), yaml_mod)
    summary = _summarize(rows)
    payload = {
        "schema_version": "internalization-readiness-1.0",
        "summary": summary,
        "weights": {
            "bibliographic_anchor": WEIGHT_BIB_ANCHOR,
            "identity": WEIGHT_IDENTITY,
            "layer1_claim": WEIGHT_LAYER1,
            "layer2_protocol": WEIGHT_LAYER2,
            "validation_target": WEIGHT_VALIDATION,
            "layer4_affordance": WEIGHT_LAYER4,
            "max_todo_penalty": MAX_TODO_PENALTY,
        },
        "min_active_score": args.min_active_score,
        "rows": rows,
    }

    if args.json:
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        text = _render_human(rows, summary, args.top)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)

    if args.strict_active:
        failing = [
            r
            for r in rows
            if r["is_active"] and r["score"] < args.min_active_score
        ]
        if failing:
            print(
                f"audit_internalization_readiness.py: FAIL — "
                f"{len(failing)} active entries below "
                f"--min-active-score={args.min_active_score}:",
                file=sys.stderr,
            )
            for r in sorted(failing, key=lambda r: r["score"])[:20]:
                print(
                    f"  - {r['score']:>5}  {r['batch']}/{r['slug']} "
                    f"(quality={r['quality_level']})",
                    file=sys.stderr,
                )
            if len(failing) > 20:
                print(f"  ... and {len(failing) - 20} more", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
