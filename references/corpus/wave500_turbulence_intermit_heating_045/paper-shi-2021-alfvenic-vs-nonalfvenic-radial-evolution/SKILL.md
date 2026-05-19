---
name: paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution
description: >-
  Use when classifying PSP E1-E5 streams by Alfvenicity (σ_c, σ_R) and tracking
  spectral-index radial evolution per class — Shi et al. 2021 statistically
  partition Alfvenic vs non-Alfvenic intervals and test expansion-driven
  spectral evolution (arXiv 2101.00830; venue TODO verify).
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
  title: "Alfvénic versus non-Alfvénic turbulence in the inner heliosphere as observed by Parker Solar Probe"
  first_author: "Shi, C."
  authors:
    - "Chen Shi"
    - "Marco Velli"
    - "Olga Panasenco"
    - "Anna Tenerani"
  year: 2021
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2101.00830"
domain:
  primary_theme: turbulence
  secondary_themes: [alfvenic, classification, radial-evolution]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "Alfvenicity classification"
  - "normalised cross helicity sigma_c"
  - "residual energy sigma_R"
  - "PSP E1-E5 statistics"
  - "spectral index radial evolution"
  - "expansion-driven turbulence"
  - "Shi Velli Panasenco Tenerani 2021"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "PSP E1-E5", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Alfvenicity classification by (σ_c, σ_R)"
    equation_refs: ["TODO verify"]
  - name: "Per-class trace PSD and spectral index fit"
    equation_refs: ["TODO verify"]
  - name: "Radial-distance binning and expansion-trend regression"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2101.00830"
claim_boundary:
  scope: >-
    Across PSP encounters 1-5, intervals partitioned by Alfvenicity exhibit
    measurably distinct inertial-range spectral indices and distinct
    radial-evolution trends.
  out_of_scope:
    - "Do not generalise the classification cuts to ML-style segmentation without re-validation."
    - "Do not export inertial-range indices into kinetic-scale ranges."
    - "Do not extend the radial-evolution trend beyond the encounter-1-5 distance range without re-fitting."
failure_modes:
  - "σ_c / σ_R depend on integration window; report window length."
  - "Stream-overlap intervals (mixed Alfvenicity) inflate within-class variance."
  - "Heliospheric current-sheet crossings flip σ_c sign."
  - "Compressive sub-intervals violate pure-Alfvenic interpretation."
depends_on:
  - damicis-2021-alfvenic-nonalfvenic-psp
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Distance range bound to E1-E5; sibling skill needed for E14+ in the sub-Alfvenic regime."
    related_skills: [paper-adhikari-2025-trans-alfvenic-turbulence]
  - type: hypothesis
    statement: "If expansion-driven spectral steepening holds, the spectral-index drift slope vs r should be reproducible within tolerance in later encounters."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2021 item 4"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence, alfvenic]
---

# Shi et al. 2021 — Alfvenic vs non-Alfvenic radial evolution — paper-skill

> Compiled from arXiv 2101.00830. `stub` tier.

## 1. Trigger
Use when partitioning PSP E1-E5 intervals by Alfvenicity to compare spectral
slopes, or when looking for expansion-driven slope drift in fast vs slow
streams.

Do NOT use for kinetic-scale anisotropy or for direct comparison with the
sw-scanner ML segmentation ([[paper-sioulas-sw-scanner-js-segmentation]])
without re-validation of class boundaries.

## 2. Paper claim → verifiable task
**Claim.** Alfvenic and non-Alfvenic PSP intervals (E1-E5) have distinct
inertial-range spectral indices and distinct radial-evolution trends.

**Verifiable task.** Reproduction succeeds when an agent recovers the
qualitative slope ordering and the trend sign vs r reported by the paper.
Tolerances TODO verify.

## 3. Methods → executable protocol
- Compute σ_c, σ_R per interval using a defined window.
- Classify Alfvenic/non-Alfvenic by thresholds on |σ_c|, σ_R.
- Per-class PSD + spectral-index fit; bin by r.

Capabilities: time-series fetch, sliding-window Elsasser statistics,
distance metadata, weighted regression.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | E1-E5 | CDAWeb | fetch CDF |
| PSP/SWEAP SPC | L3 | ~1 Hz | Same | CDAWeb | fetch CDF |

## 5. Validation target
Not benchmarked yet — per-class spectral indices and radial-trend slopes
TODO verify.

## 6. Failure modes
- σ_c / σ_R window dependence.
- Mixed-Alfvenicity stream overlap.
- HCS sign flips.
- Compressive contamination.

## 7. Claim boundary
**In scope.** PSP E1-E5 Alfvenic/non-Alfvenic classification + per-class
spectral indices and radial trend.
**Out of scope.** ML-style cluster boundaries, kinetic scales, sub-Alfvenic
regime without re-fitting.

## 8. Links and adapter binding examples
- arXiv: https://arxiv.org/abs/2101.00830
- DOI/ADS: TODO verify

## 9. Skill graph + affordances
Depends on [[damicis-2021-alfvenic-nonalfvenic-psp]].

- **Gap** — E14+ sub-Alfvenic sibling missing → [[paper-adhikari-2025-trans-alfvenic-turbulence]] is the closest.
- **Hypothesis** — Expansion-driven slope drift should reproduce in later encounters.
