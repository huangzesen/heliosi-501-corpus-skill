---
name: paper-mcintyre-2023-spectral-index-variation-inner-heliosphere
description: >-
  Use when working with the central claim of J. R. McIntyre et al. 2023 — Variation of the
  magnetic-field inertial-range spectral index in the inner solar wind correlates with
  measurable stream properties (e.g. Alfvenicity, beta, σ_c), beyond pure radial dependence.
  (arXiv:2307.04682; venue TODO verify).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: true
paper:
  title: "Properties underlying the variation of the magnetic field spectral index in the inner solar wind"
  first_author: "J. R. McIntyre"
  authors:
    - "J. R. McIntyre"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2307.04682"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [spectral-index, inner-heliosphere, stream-properties]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "spectral index variation"
  - "stream-property correlation"
  - "Alfvenicity beta"
  - "inner solar wind"
  - "McIntyre 2023 spectral-index"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "Inner-heliosphere encounters", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Per-interval inertial-range spectral-index fit"
    equation_refs: ["TODO verify"]
  - name: "Joint regression vs stream properties"
    equation_refs: ["TODO verify"]
  - name: "Residual analysis after radial-distance subtraction"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2307.04682"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the inner-heliosphere PSP sample analysed, spectral-index variation is partially
    attributable to stream properties beyond radial distance.
  out_of_scope:
    - "Do not impute causation from regression."
    - "Do not extrapolate the predictor set to non-PSP missions without re-fitting."
    - "Do not equate spectral-index variation with a single physical mechanism."
failure_modes:
  - "Predictor collinearity (beta and Alfvenicity correlated)."
  - "Spectral-index fit window choice."
  - "Stream-mixed intervals inflate residual variance."
  - "Limited dynamic range in some predictors."
depends_on:
  - chen-2022-magnetic-field-spectral-evolution-inner-heliosphere
  - paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill provides the same regression-controlled spectral-index decomposition for Solar Orbiter intervals."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2307.04682v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# J. R. McIntyre et al. 2023 — Properties underlying the variation of the magnetic field sp... — paper-skill

> Compiled from arXiv:2307.04682. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Variation of the magnetic-field inertial-range spectral index in the inner solar wind correlates with measurable stream properties (e.g. Alfvenicity, beta, σ_c), beyond pure radial dependence.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- non-PSP extrapolation
- causal-mechanism inference

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Variation of the magnetic-field inertial-range spectral index in the inner solar wind correlates with measurable stream properties (e.g. Alfvenicity, beta, σ_c), beyond pure radial dependence.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Per-interval inertial-range spectral-index fit
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Joint regression vs stream properties
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Residual analysis after radial-distance subtraction
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | Inner-heliosphere encounters | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Predictor collinearity (beta and Alfvenicity correlated).
- Spectral-index fit window choice.
- Stream-mixed intervals inflate residual variance.
- Limited dynamic range in some predictors.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the inner-heliosphere PSP sample analysed, spectral-index variation is partially attributable to stream properties beyond radial distance.

**Out of scope — do NOT generalize beyond:**

- Do not impute causation from regression.
- Do not extrapolate the predictor set to non-PSP missions without re-fitting.
- Do not equate spectral-index variation with a single physical mechanism.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2307.04682
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] — sibling/upstream context for the same physics domain.
- [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill provides the same regression-controlled spectral-index decomposition for Solar Orbiter intervals.
