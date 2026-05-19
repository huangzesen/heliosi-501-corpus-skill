---
name: paper-wrench-2024-debiasing-structure-function-sparse
description: >-
  Use when working with the central claim of Daniel Wrench et al. 2024 — A data-driven de-
  biasing procedure applied to gappy in-situ MAG time series recovers structure-function
  estimates with reduced bias compared to naive gap-skipping or zero-fill, validated against
  synthetic and real solar-wind data. (arXiv:2412.10053; venue TODO verify).
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
  title: "De-Biasing Structure Function Estimates From Sparse Time Series of the Solar Wind: A Data-Driven Approach"
  first_author: "Daniel Wrench"
  authors:
    - "Daniel Wrench"
    - "Tulasi N. Parashar"
    - "Sean Oughton"
    - "Marcus Frean"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2412.10053"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [structure-function, missing-data, correction, ML]
  missions: [other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "sparse time series"
  - "structure-function de-biasing"
  - "missing-data correction"
  - "gap-skipping bias"
  - "solar-wind structure function"
  - "Wrench Parashar Oughton Frean 2024"
data_products:
  - {instrument: "In-situ MAG time series (mission TODO verify)", level: "L2", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Synthetic-gap test on dense time series"
    equation_refs: ["TODO verify"]
  - name: "Naive-vs-de-biased estimator comparison"
    equation_refs: ["TODO verify"]
  - name: "Data-driven correction model (ML or analytic)"
    equation_refs: ["TODO verify exact form"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2412.10053"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    De-biased structure-function estimator validated against synthetic-gap insertions and real
    gappy solar-wind MAG records within the paper's tested gap-statistics regime.
  out_of_scope:
    - "Do not apply the trained correction outside its training-distribution gap-fraction range without re-validation."
    - "Do not equate de-biased S_n with bias-free at very high gap fractions."
    - "Do not extend the method to multi-variate cross-spectral quantities without extension."
failure_modes:
  - "Correction quality depends on gap statistics matching training set."
  - "Long-tail high-order S_n (n>=4) most sensitive to residual bias."
  - "ML-based correction can overfit to training mission cadence."
  - "Reported tolerance is dataset-dependent."
depends_on:
  - sioulas-2022-magnetic-field-intermittency-psp-solo
adapter_notes: []
research_generation_affordances:
  - type: minimal_experiment
    statement: "Apply the correction to PSP burst-mode-with-dropouts MAG and verify recovered S_4 against gap-free intervals."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2412.10053v2)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Daniel Wrench et al. 2024 — De-Biasing Structure Function Estimates From Sparse Time Ser... — paper-skill

> Compiled from arXiv:2412.10053. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- A data-driven de-biasing procedure applied to gappy in-situ MAG time series recovers structure-function estimates with reduced bias compared to naive gap-skipping or zero-fill, validated against synthetic and real solar-wind data.
- Reproducing or extending the analysis around In-situ MAG time series (mission TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- out-of-distribution gap-fraction without re-training
- cross-spectral statistic correction

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A data-driven de-biasing procedure applied to gappy in-situ MAG time series recovers structure-function estimates with reduced bias compared to naive gap-skipping or zero-fill, validated against synthetic and real solar-wind data.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Synthetic-gap test on dense time series
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Naive-vs-de-biased estimator comparison
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Data-driven correction model (ML or analytic)
- Paper reference: TODO verify exact form.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ MAG time series (mission TODO verify) | L2 | TODO verify | TODO verify | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Correction quality depends on gap statistics matching training set.
- Long-tail high-order S_n (n>=4) most sensitive to residual bias.
- ML-based correction can overfit to training mission cadence.
- Reported tolerance is dataset-dependent.

## 7. Claim boundary  *(Layer 1)*

**In scope.** De-biased structure-function estimator validated against synthetic-gap insertions and real gappy solar-wind MAG records within the paper's tested gap-statistics regime.

**Out of scope — do NOT generalize beyond:**

- Do not apply the trained correction outside its training-distribution gap-fraction range without re-validation.
- Do not equate de-biased S_n with bias-free at very high gap fractions.
- Do not extend the method to multi-variate cross-spectral quantities without extension.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2412.10053
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[sioulas-2022-magnetic-field-intermittency-psp-solo]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Minimal_experiment** — Apply the correction to PSP burst-mode-with-dropouts MAG and verify recovered S_4 against gap-free intervals.
