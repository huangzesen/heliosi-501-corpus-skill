---
name: macneil-2024-adapt-aft-flux-transport-in-situ
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# macneil-2024-adapt-aft-flux-transport-in-situ

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when scoring ADAPT vs AFT flux-transport models against multi-spacecraft polarity / OSF measurements.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Assessing the Performance of the ADAPT and AFT Flux Transport Models Using In-Situ Measurements from Multiple Spacecraft
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2402.10432 (posted 2024-02-16)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

ADAPT and AFT achieve similar global skill but differ in polar-region completeness, with measurable downstream effects on PFSS-based polarity agreement at L1, PSP, and SolO.

### Method assumptions

- Same PFSS solver applied on top of both products.
- In-situ polarity validation is independent of the input model.

### Data assumptions

- ADAPT and AFT synoptic-map streams.
- L1+PSP+SolO polarity.

### Failure modes (skill memory)

- Cycle-phase shifts the relative ranking.
- Polar fill-in policy is product-specific.

### Figure / numerical targets

- Per-product polarity-agreement vs latitude.
- Polar-completeness diagnostic.

### Claim boundary

**In scope.** The studied interval + ADAPT/AFT versions.

**Out of scope — do NOT generalize:**

- Do NOT generalize to other flux-transport models without re-scoring.
- Do NOT cite the ranking outside the validated cycle phase.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_adapt()` | ADAPT |  |
| `magnetogram.fetch_aft()` | AFT |  |
| `pfss.solve()` | PFSS |  |
| `polarity.evaluate_multi_sc()` | polarity |  |
| `metric.polar_completeness()` | polar gap diagnostic |  |

### Procedure

1. Stream ADAPT + AFT maps.
2. Solve PFSS on both.
3. Score polarity at L1/PSP/SolO.
4. Compute polar-completeness diagnostic.

### Validation target

Recover per-product polarity-vs-latitude table.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- ADAPT/AFT via NSO/AFRL streams; sunkit-magex.pfss for PFSS.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field]] to attribute polar-vs-farside uncertainty.
- Generative hypothesis: ADAPT–AFT differential at high latitude predicts which cycle phases need the AI-farside augmentation.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-ai-farside-synchronic-coronal-field-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2402.10432
- arXiv HTML: https://arxiv.org/html/2402.10432
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- ADAPT/AFT versions
- polar completeness metric
