---
name: katsavrias-2025-low-db-streams-source-variability
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# katsavrias-2025-low-db-streams-source-variability

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when characterizing low-δB solar-wind streams via PFSS source-region attribution and quantifying the source–in-situ variability link.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** On the Relation Between Source Region and In-Situ Variability of Low-δB Solar Wind Streams
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2511.21971 (posted 2025-11-26)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Low-δB solar-wind streams map via PFSS to compact, low-expansion-factor source regions, with in-situ variability metrics scaling predictably with source-region size.

### Method assumptions

- Low-δB classification is independent of PFSS.
- Source-region size is measurable in PFSS footpoint maps.

### Data assumptions

- In-situ B with high-cadence δB statistics.
- Synoptic Br for PFSS.

### Failure modes (skill memory)

- Low-δB definition depends on cadence.
- Source-region size depends on footpoint-tracing seed density.

### Figure / numerical targets

- Stream classification map.
- δB variability vs source-region size scatter.

### Claim boundary

**In scope.** The studied interval.

**Out of scope — do NOT generalize:**

- Do NOT extend the scaling outside the studied δB range.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `in_situ.fetch_b_high_cadence()` | B at high cadence |  |
| `sw.classify_low_db()` | low-δB classifier |  |
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `source.measure_region_size()` | source-region size |  |

### Procedure

1. Classify low-δB streams.
2. Back-map via PFSS.
3. Measure source-region size and expansion factor.
4. Test δB-vs-size scaling.

### Validation target

Reproduce δB-vs-size scaling.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; pyspedas for in-situ.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-stansby-2025-open-closed-flux-boundary-slow-wind]] — low-δB streams as OCB-proximate slow wind.
- Generative hypothesis: low-δB sources should overlap with AR-edge upflow patches ([[paper-brooks-2025-active-region-upflows-coronal-coupling]]).

---

## Skill graph → depends_on

- [[paper-stansby-2025-open-closed-flux-boundary-slow-wind]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2511.21971
- arXiv HTML: https://arxiv.org/html/2511.21971
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- low-δB threshold
- source-region metric
