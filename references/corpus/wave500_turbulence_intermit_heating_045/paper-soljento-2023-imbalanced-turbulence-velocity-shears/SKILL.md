---
name: paper-soljento-2023-imbalanced-turbulence-velocity-shears
description: >-
  Use when working with the central claim of Juska E. Soljento et al. 2023 — Large-scale
  velocity shears in the solar wind modify the imbalanced-turbulence cascade by
  redistributing z+ and z- power, observable as shear-dependent cross-helicity drift.
  (arXiv:2303.04006; venue TODO verify).
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
  title: "Imbalanced Turbulence Modified by Large-scale Velocity Shears in the Solar Wind"
  first_author: "Juska E. Soljento"
  authors:
    - "Juska E. Soljento"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2303.04006"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [imbalanced, velocity-shear, large-scale]
  missions: [other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "velocity shear imbalance"
  - "large-scale shear cascade modification"
  - "z+ z- redistribution"
  - "Soljento 2023 shear"
  - "cross-helicity drift"
data_products:
  - {instrument: "In-situ MAG (mission TODO verify)", level: "L2", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
  - {instrument: "Corresponding plasma", level: "L2/L3", cadence: "TODO verify", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Large-scale velocity-shear estimator"
    equation_refs: ["TODO verify"]
  - name: "Cross-helicity per shear-binned subsample"
    equation_refs: ["TODO verify"]
  - name: "Drift-trend regression vs shear strength"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2303.04006"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    On the analysed dataset, imbalanced-cascade signatures shift systematically with large-
    scale velocity-shear strength.
  out_of_scope:
    - "Do not attribute the trend solely to shear without ruling out stream-mixing."
    - "Do not extend the shear-strength range outside what the sample covers."
    - "Do not assume the trend persists at near-Sun PSP distances without re-running."
failure_modes:
  - "Shear estimator window choice biases magnitude."
  - "Stream-mixed intervals confound shear vs Alfvenicity attribution."
  - "Cross-helicity sign convention requires consistent outward direction."
  - "Sample size at extreme shear is limited."
depends_on:
  - paper-chandran-2025-intermittent-reflection-imbalanced-mhd
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If shear modifies the imbalanced cascade, PSP near-Sun stream-interaction regions should show enhanced cross-helicity drift."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2303.04006v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Juska E. Soljento et al. 2023 — Imbalanced Turbulence Modified by Large-scale Velocity Shear... — paper-skill

> Compiled from arXiv:2303.04006. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Large-scale velocity shears in the solar wind modify the imbalanced-turbulence cascade by redistributing z+ and z- power, observable as shear-dependent cross-helicity drift.
- Reproducing or extending the analysis around In-situ MAG (mission TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- near-Sun extrapolation without re-run
- stream-mixing-uncorrected attribution

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Large-scale velocity shears in the solar wind modify the imbalanced-turbulence cascade by redistributing z+ and z- power, observable as shear-dependent cross-helicity drift.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Large-scale velocity-shear estimator
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Cross-helicity per shear-binned subsample
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Drift-trend regression vs shear strength
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ MAG (mission TODO verify) | L2 | TODO verify | TODO verify | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| Corresponding plasma | L2/L3 | TODO verify | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Shear estimator window choice biases magnitude.
- Stream-mixed intervals confound shear vs Alfvenicity attribution.
- Cross-helicity sign convention requires consistent outward direction.
- Sample size at extreme shear is limited.

## 7. Claim boundary  *(Layer 1)*

**In scope.** On the analysed dataset, imbalanced-cascade signatures shift systematically with large-scale velocity-shear strength.

**Out of scope — do NOT generalize beyond:**

- Do not attribute the trend solely to shear without ruling out stream-mixing.
- Do not extend the shear-strength range outside what the sample covers.
- Do not assume the trend persists at near-Sun PSP distances without re-running.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2303.04006
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-chandran-2025-intermittent-reflection-imbalanced-mhd]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If shear modifies the imbalanced cascade, PSP near-Sun stream-interaction regions should show enhanced cross-helicity drift.
