---
name: wang-2023-solar-wind-source-cycle-coronal-rotation
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# wang-2023-solar-wind-source-cycle-coronal-rotation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when relating coronal-rotation rate to solar-wind source-region migration over the cycle, via PFSS topological tracking.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Evolution of Solar Wind Sources and Coronal Rotation Driven by the Cyclic Variation of the Sun's Large-Scale Magnetic Field
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2023
- **arXiv:** 2309.10850 (posted 2023-09-19)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Solar-wind source regions migrate latitudinally and rotate non-rigidly over the cycle, with coronal-rotation rate tracking the dominant PFSS multipole content.

### Method assumptions

- Source-region tracking through PFSS-traced footpoints is reliable across the cycle.
- Coronal rotation can be inferred from source-region drift.

### Data assumptions

- Synoptic Br across the cycle.
- In-situ vsw catalog with timestamps.

### Failure modes (skill memory)

- Source-region identity ambiguous near CH boundaries.
- Multipole power-attribution sensitive to truncation.

### Figure / numerical targets

- Source-region latitude vs cycle phase.
- Coronal-rotation rate vs multipole power.

### Claim boundary

**In scope.** The paper's cycle window.

**Out of scope — do NOT generalize:**

- Do NOT generalize to non-PFSS topology models.
- Do NOT cite the coronal-rotation result outside the studied latitude band.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `source.track_region()` | source-region tracking |  |
| `rotation.coronal_rate()` | rotation rate |  |
| `sph_harm.decompose()` | multipole content |  |

### Procedure

1. Solve PFSS cycle-long.
2. Track source regions through PFSS footpoints.
3. Compute coronal-rotation rate from source drift.
4. Correlate with multipole power.

### Validation target

Recover cycle-phase rotation-rate variation.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; SH decomposition via pyshtools.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-hore-2026-dominant-spatial-scales-coronal-field]] — multipole power vs coronal rotation as a unified framework.
- Generative hypothesis: source-region drift rate should drop during nested-AR phases ([[paper-jiang-2024-nested-active-regions-hcs-reversal]]).

---

## Skill graph → depends_on

- [[paper-hore-2026-dominant-spatial-scales-coronal-field]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2309.10850
- arXiv HTML: https://arxiv.org/html/2309.10850
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- tracking algorithm
- multipole truncation
