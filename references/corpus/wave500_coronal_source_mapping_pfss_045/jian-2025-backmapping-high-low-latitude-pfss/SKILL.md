---
name: jian-2025-backmapping-high-low-latitude-pfss
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# jian-2025-backmapping-high-low-latitude-pfss

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when back-mapping high- and low-latitude solar wind under multiple coronal+heliospheric magnetic-field configurations (PFSS, current-sheet, MHD).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Backmapping of the High- and Low-Latitude Solar Wind Under Multiple Heliospheric and Coronal Magnetic Field Configurations
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2510.21076 (posted 2025-10-24)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Backmapping under PFSS vs PFSS+PFCS vs MHD yields systematically different source-region attributions at high latitude where PFSS alone is insufficient — quantified across Ulysses and Solar Orbiter high-latitude passes.

### Method assumptions

- Multi-configuration backmapping is consistent at the same R_ss.
- High-latitude coverage allows model discrimination.

### Data assumptions

- Ulysses + SolO high-latitude in-situ.
- Synoptic Br across the relevant intervals.
- MHD ambient as available.

### Failure modes (skill memory)

- Ulysses-era magnetogram products differ from modern.
- MHD vs PFSS comparison depends on grid.

### Figure / numerical targets

- Per-latitude source-region attribution under each config.
- Disagreement map.

### Claim boundary

**In scope.** High-latitude pass intervals.

**Out of scope — do NOT generalize:**

- Do NOT generalize to low latitudes without separate testing.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `pfcs.solve()` | current-sheet layer |  |
| `mhd.ambient()` | MHD ambient |  |
| `backmap.compare_configs()` | back-map comparison |  |

### Procedure

1. Identify high-latitude pass intervals.
2. Backmap under each model config.
3. Quantify per-latitude disagreement.

### Validation target

Reproduce disagreement map.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; PFCS / MHD codes paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]] — NSPF as a fourth config to compare against.
- Generative hypothesis: disagreement-map structure correlates with effective-multipole degree at high latitude ([[paper-hore-2026-dominant-spatial-scales-coronal-field]]).

---

## Skill graph → depends_on

- [[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2510.21076
- arXiv HTML: https://arxiv.org/html/2510.21076
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- Ulysses interval
- MHD model identity
