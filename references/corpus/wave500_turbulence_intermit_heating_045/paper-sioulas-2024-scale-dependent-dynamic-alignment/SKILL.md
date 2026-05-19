---
name: paper-sioulas-2024-scale-dependent-dynamic-alignment
description: >-
  Use when working with the central claim of Nikos Sioulas et al. 2024 — Scale-dependent
  dynamic alignment (SDDA) inferred from PSP+SO magnetic-velocity increments correlates with
  intermittency growth and compressibility level, supporting an SDDA-mediated cascade.
  (arXiv:2407.03649; venue TODO verify).
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
  title: "Scale-Dependent Dynamic Alignment in MHD Turbulence: Insights into Intermittency, Compressibility"
  first_author: "Nikos Sioulas"
  authors:
    - "Nikos Sioulas"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2407.03649"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [dynamic-alignment, intermittency, compressibility]
  missions: [PSP, Solar Orbiter]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "scale-dependent dynamic alignment"
  - "SDDA angle distribution"
  - "intermittency growth"
  - "Sioulas 2024 SDDA"
  - "compressibility correlation"
  - "velocity-magnetic alignment"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "Inner heliosphere PSP intervals", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
  - {instrument: "Solar Orbiter MAG", level: "L2", cadence: "~1 vec/s", interval: "Inner heliosphere SO intervals", archive: "SOAR"}
algorithms:
  - name: "Scale-dependent alignment-angle distribution"
    equation_refs: ["TODO verify Eq."]
  - name: "SDDA-vs-intermittency joint statistics"
    equation_refs: ["TODO verify"]
  - name: "Compressibility-conditioned subsampling"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2407.03649"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Joint SDDA + intermittency + compressibility statistics on the PSP+SO sample analysed,
    within the MHD inertial range.
  out_of_scope:
    - "Do not export SDDA-vs-intermittency link to kinetic-scale ranges."
    - "Do not assume the correlation is causal absent additional discriminators."
    - "Do not equate compressibility level with magnetosonic-mode fraction without eigenmode decomposition."
failure_modes:
  - "Alignment-angle estimator is sensitive to detrending."
  - "Local-mean-field definition shifts the angle distribution."
  - "Compressibility binning is coarse with limited statistics."
  - "Intermittency metric (SDK vs PVI) consistency required."
depends_on:
  - sioulas-2024-higher-order-3d-anisotropy
  - paper-shi-2023-residual-energy-intermittency-expanding-box
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If SDDA mediates intermittency growth, intervals at higher compressibility should also exhibit weaker SDDA at the same scale."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2407.03649v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Nikos Sioulas et al. 2024 — Scale-Dependent Dynamic Alignment in MHD Turbulence: Insight... — paper-skill

> Compiled from arXiv:2407.03649. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Scale-dependent dynamic alignment (SDDA) inferred from PSP+SO magnetic-velocity increments correlates with intermittency growth and compressibility level, supporting an SDDA-mediated cascade.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- kinetic-scale alignment without re-derivation
- causal-link claim without discriminator

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Scale-dependent dynamic alignment (SDDA) inferred from PSP+SO magnetic-velocity increments correlates with intermittency growth and compressibility level, supporting an SDDA-mediated cascade.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Scale-dependent alignment-angle distribution
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### SDDA-vs-intermittency joint statistics
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Compressibility-conditioned subsampling
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | Inner heliosphere PSP intervals | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| Solar Orbiter MAG | L2 | ~1 vec/s | Inner heliosphere SO intervals | SOAR | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Alignment-angle estimator is sensitive to detrending.
- Local-mean-field definition shifts the angle distribution.
- Compressibility binning is coarse with limited statistics.
- Intermittency metric (SDK vs PVI) consistency required.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Joint SDDA + intermittency + compressibility statistics on the PSP+SO sample analysed, within the MHD inertial range.

**Out of scope — do NOT generalize beyond:**

- Do not export SDDA-vs-intermittency link to kinetic-scale ranges.
- Do not assume the correlation is causal absent additional discriminators.
- Do not equate compressibility level with magnetosonic-mode fraction without eigenmode decomposition.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2407.03649
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[sioulas-2024-higher-order-3d-anisotropy]] — sibling/upstream context for the same physics domain.
- [[paper-shi-2023-residual-energy-intermittency-expanding-box]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If SDDA mediates intermittency growth, intervals at higher compressibility should also exhibit weaker SDDA at the same scale.
