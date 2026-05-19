---
name: brennan-2024-tracing-reconnecting-expanding-field-lines
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# brennan-2024-tracing-reconnecting-expanding-field-lines

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when distinguishing reconnecting from expanding field lines in time-dependent extrapolations.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Tracing Field Lines That Are Reconnecting or Expanding or Both
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2409.04573 (posted 2024-09-06)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A field-line classification scheme distinguishes reconnecting vs purely expanding field lines in time-dependent extrapolations by comparing footpoint-mapping derivatives to expansion-rate derivatives, with the difference recoverable from PFSS+trajectory snapshots.

### Method assumptions

- Footpoint mapping derivatives are computable to required precision.
- Expansion-rate is bounded over the time interval.

### Data assumptions

- Time-dependent extrapolation outputs.
- PFSS snapshots for validation.

### Failure modes (skill memory)

- Numerical noise dominates derivatives for short intervals.
- Mapping-derivative singularities at QSLs need regularization.

### Figure / numerical targets

- Classification map of reconnecting vs expanding lines.
- QSL alignment panel.

### Claim boundary

**In scope.** The time-dependent runs studied.

**Out of scope — do NOT generalize:**

- Do NOT apply the classifier in steady PFSS without redefining time-derivatives.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `coronal.time_dependent_solve()` | time-dependent field |  |
| `topology.footpoint_mapping_derivative()` | derivatives |  |
| `topology.expansion_rate()` | expansion rate |  |
| `classifier.reconnect_vs_expand()` | classifier |  |
| `pfss.solve()` | validation snapshot |  |

### Procedure

1. Run time-dependent extrapolation.
2. Compute footpoint-mapping and expansion derivatives.
3. Classify field lines.
4. Validate against PFSS snapshots.

### Validation target

Classifier vs PFSS agreement.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Time-dependent code paper-specific; sunkit-magex.pfss for validation.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-mackay-2026-tracking-magnetic-topology-change-corona]] — classifier feeds topology-change tracker.
- Generative hypothesis: reconnecting-line density correlates with magnetic-separator reconnection flux ([[paper-nadol-2026-magnetic-separator-reconnection-flare-ribbons]]).

---

## Skill graph → depends_on

- [[paper-mackay-2026-tracking-magnetic-topology-change-corona]]

## Links

- arXiv: https://arxiv.org/abs/2409.04573
- arXiv HTML: https://arxiv.org/html/2409.04573
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- classifier definition
- regularization
