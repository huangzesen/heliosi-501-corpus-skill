---
name: paper-andres-2021-incompressible-cascade-anisotropic-pp
description: >-
  Use when evaluating the Politano-Pouquet exact third-order relation on PSP
  data and decomposing the cascade rate into directions parallel and
  perpendicular to the local mean field — Andres et al. 2021 apply this
  decomposition over >2 yr of PSP data (arXiv 2112.13748; venue TODO verify).
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
  title: "The incompressible energy cascade rate in anisotropic solar wind turbulence"
  first_author: "Andres, N."
  authors:
    - "N. Andres"
    - "F. Sahraoui"
    - "S. Huang"
    - "L. Z. Hadid"
  year: 2021
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2112.13748"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [cascade-rate, anisotropy, exact-relation]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "Politano-Pouquet third-order law"
  - "incompressible MHD cascade rate"
  - "anisotropic cascade decomposition"
  - "parallel perpendicular epsilon"
  - "PSP statistical survey"
  - "Andres Sahraoui Huang Hadid 2021"
  - "Elsasser flux divergence"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: ">2 yr of PSP data (TODO verify encounter set)", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Politano-Pouquet third-order exact relation"
    equation_refs: ["TODO verify Eq. numbers"]
    external_implementations: []
  - name: "Anisotropic decomposition: parallel and perpendicular cascade rate"
    equation_refs: ["TODO verify"]
  - name: "Isotropic-vs-anisotropic cascade-rate comparison"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2112.13748"
claim_boundary:
  scope: >-
    Over >2 yr of PSP data (encounter set TODO verify), the incompressible
    Politano-Pouquet cascade rate ε, decomposed parallel and perpendicular to
    the local mean field, is statistically distinct from the isotropic
    estimate.
  out_of_scope:
    - "Do not apply the incompressible PP law to intervals with measurable density compressibility without quoting δn/n."
    - "Do not equate the per-direction ε with a single scalar dissipation rate."
    - "Do not extrapolate the parallel/perpendicular ratio across heliocentric distance without per-bin re-fitting."
failure_modes:
  - "Third-order law is statistically expensive; small-sample bias inflates noise in tails."
  - "Local-mean-field estimator choice changes the parallel/perpendicular split."
  - "Density estimation (SPC vs derived) propagates into ε; quote source."
  - "Compressibility violates the incompressible derivation; pre-filter δn/n."
depends_on:
  - paper-bandyopadhyay-2020-energy-transfer-psp
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Anisotropic-ε statistics are bound to PSP; no sibling skill provides Solar-Orbiter or Helios comparison."
  - type: tension
    statement: "Per-direction cascade-rate ordering should be cross-checked against compressible-cascade estimates in [[cuesta-2022-compressible-turbulence-psp-themis-maven]]."
    related_skills: [cuesta-2022-compressible-turbulence-psp-themis-maven]
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2021 item 6"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence, cascade, anisotropy]
---

# Andres et al. 2021 — incompressible anisotropic cascade rate (PSP) — paper-skill

> Compiled from arXiv 2112.13748. `stub` tier.

## 1. Trigger
Use when applying PP exact relation on PSP MAG+SWEAP and decomposing the
inertial-range cascade rate into ε∥ and ε⊥.

Do NOT use for compressible-cascade flux ([[cuesta-2022-compressible-turbulence-psp-themis-maven]])
or for von-Kármán decay estimates.

## 2. Paper claim → verifiable task
**Claim.** Anisotropic (per-direction) PP cascade rates over >2 yr of PSP data
are statistically distinct from the isotropic estimate.

**Verifiable task.** A reproduction recovers the qualitative ε⊥ vs ε∥
ordering and the deviation from the isotropic estimate. Numerical
values TODO verify.

## 3. Methods → executable protocol
- PP exact relation on Elsasser increments.
- Anisotropic projection into parallel/perpendicular bins relative to local
  mean field.
- Per-bin scalar ε.

Capabilities: per-lag structure-function in three projections; bootstrap
error bars; local-mean-field estimator.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | >2 yr (encounters TODO verify) | CDAWeb | fetch CDF |
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | Same | CDAWeb | fetch CDF |

## 5. Validation target
Not benchmarked yet — per-direction ε values TODO verify.

## 6. Failure modes
- Small-sample bias at high-order moments.
- Local-mean-field choice changes split.
- Density-source choice propagates.
- Compressibility violates derivation.

## 7. Claim boundary
**In scope.** Statistical per-direction PP ε over the analysed PSP interval.
**Out of scope.** Compressible cascade, single-scalar dissipation
interpretation, radial extrapolation without re-binning.

## 8. Links and adapter binding examples
- arXiv: https://arxiv.org/abs/2112.13748
- DOI/ADS: TODO verify

## 9. Skill graph + affordances
Depends on [[paper-bandyopadhyay-2020-energy-transfer-psp]].

- **Gap** — No Solar Orbiter / Helios sibling.
- **Tension** — Compare against [[cuesta-2022-compressible-turbulence-psp-themis-maven]] compressible ε.
