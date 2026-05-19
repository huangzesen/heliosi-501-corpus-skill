---
name: sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when quantifying how *missing* portions of the photospheric Br (farside, polar) propagate into PFSS-based solar-wind forecasts.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Quantifying Uncertainties in Solar Wind Forecasting Due to Incomplete Solar Magnetic Field Information
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2504.19534 (posted 2025-04-28)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Forecast uncertainty at L1 grows non-linearly with farside / polar magnetogram incompleteness, with the polar gap dominating for cycle minimum and the farside gap dominating for maximum.

### Method assumptions

- Ensemble of magnetogram completions is representative.
- Forecast error is decomposable into PFSS + kernel + ensemble terms.

### Data assumptions

- Multiple synoptic Br products + AI-farside ensembles.
- L1 vsw + |B| ground truth.

### Failure modes (skill memory)

- Ensemble size insufficient to span polar uncertainty.
- AI-farside artifacts mimic real flux.

### Figure / numerical targets

- Forecast error vs polar-gap depth.
- Forecast error vs farside-completion variance.
- Cycle-phase attribution panel.

### Claim boundary

**In scope.** The paper's ensembles + forecast configuration.

**Out of scope — do NOT generalize:**

- Do NOT extend to non-PFSS forecast pipelines unchecked.
- Do NOT cite polar-vs-farside attribution outside the modelled cycle phase.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `magnetogram.ai_farside_ensemble()` | AI-farside completions |  |
| `magnetogram.polar_fill_ensemble()` | polar completions |  |
| `pfss.solve()` | PFSS |  |
| `wsa.predict_speed()` | L1 forecast |  |
| `error.decompose()` | ensemble vs kernel |  |

### Procedure

1. Generate magnetogram ensemble (polar + farside).
2. Solve PFSS for each member.
3. Run forecast kernel; collect L1 predictions.
4. Compute ensemble spread vs ground truth.
5. Attribute error by completion type and cycle phase.

### Validation target

Reproduce the cycle-phase-dependent attribution.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; AI-farside model is paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-ai-farside-synchronic-coronal-field-extrapolation]] — uncertainty quantification of the AI-farside skill itself.
- Tension with [[paper-wsa-l1-errors-2025]] — overlap in topology-error attribution.

---

## Skill graph → depends_on

- [[paper-ai-farside-synchronic-coronal-field-extrapolation]]
- [[paper-wsa-l1-errors-2025]]

## Links

- arXiv: https://arxiv.org/abs/2504.19534
- arXiv HTML: https://arxiv.org/html/2504.19534
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- ensemble size
- AI-farside model
