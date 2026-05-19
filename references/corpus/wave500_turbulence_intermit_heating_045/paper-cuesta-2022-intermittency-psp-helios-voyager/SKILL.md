---
name: paper-cuesta-2022-intermittency-psp-helios-voyager
description: >-
  Use when tracking radial evolution of solar-wind intermittency from 0.16 au
  to ~10 au using multi-spacecraft (PSP, Helios 1, Voyager 1) MAG time series
  via structure functions, scale-dependent kurtosis, and correlation length —
  Cuesta et al. 2022 build the SDK(r) family across distance bins
  (arXiv 2202.01874; venue TODO verify).
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
  title: "Intermittency in the Expanding Solar Wind: Observations from Parker Solar Probe (0.16 au), Helios 1 (0.3–1 au), and Voyager 1 (1–10 au)"
  first_author: "Cuesta, M. E."
  authors:
    - "Manuel Enrique Cuesta"
    - "Tulasi N. Parashar"
    - "Rohit Chhiber"
    - "William H. Matthaeus"
  year: 2022
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2202.01874"
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, radial-evolution, multi-spacecraft]
  missions: [PSP, Helios, Voyager]
  regime: [inner-heliosphere, 1au, outer-heliosphere]
trigger_keywords:
  - "scale-dependent kurtosis SDK"
  - "magnetic field intermittency radial"
  - "structure function order n"
  - "correlation length lambda_C"
  - "ion inertial length d_i normalisation"
  - "PSP Helios Voyager joint analysis"
  - "Cuesta Parashar Chhiber Matthaeus 2022"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "~0.16 au perihelion", archive: "CDAWeb / SPDF"}
  - {instrument: "Helios 1 MAG", level: "L2", cadence: "TODO verify", interval: "0.3-1 au", archive: "CDAWeb / SPDF"}
  - {instrument: "Voyager 1 MAG", level: "L2", cadence: "TODO verify", interval: "1-10 au", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Auto-correlation function and correlation length"
    equation_refs: ["TODO verify"]
  - name: "Structure functions S_n(lag)"
    equation_refs: ["TODO verify"]
  - name: "Scale-dependent kurtosis SDK(lag)"
    equation_refs: ["TODO verify"]
  - name: "Distance-binned trend of λ_C / d_i"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2202.01874"
claim_boundary:
  scope: >-
    Radial trend of magnetic-field correlation length λ_C (and SDK) across
    PSP (~0.16 au), Helios 1 (0.3-1 au) and Voyager 1 (1-10 au) follows a
    quantifiable monotonic dependence when normalised to ion inertial length.
  out_of_scope:
    - "Do not equate the three-mission trend with a uniform expansion law without per-mission systematic-error budget."
    - "Do not export the SDK lag dependence to kinetic scales unresolved at Voyager."
    - "Do not extend the radial trend below 0.16 au or beyond 10 au from this sample alone."
failure_modes:
  - "Cadence differences between PSP/Helios/Voyager bias inertial-range cut-off."
  - "Sampling-direction differences (PSP swing-by vs Voyager outbound) shift effective Taylor projection."
  - "SDK requires sufficient sample size at large lags; report sample count per lag."
  - "Mixed-stream contamination at Helios is a known issue."
depends_on:
  - sioulas-2022-magnetic-field-intermittency-psp-solo
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill uses Solar Orbiter to fill the 0.3-1 au range alongside PSP+Helios for a four-mission consistency check."
  - type: minimal_experiment
    statement: "Replicate SDK(r/d_i) using Solar Orbiter MAG over the same distance window as Helios 1 and overlay."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2022 item 7"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence, intermittency]
---

# Cuesta et al. 2022 — multi-mission intermittency radial evolution — paper-skill

> Compiled from arXiv 2202.01874. `stub` tier.

## 1. Trigger
Use when tracking magnetic-field intermittency (SDK, λ_C/d_i) over a broad
radial span (0.16-10 au) with PSP+Helios+Voyager.

Do NOT use for kinetic-scale intermittency (Voyager cadence cannot resolve)
or for single-mission detailed encounter analysis.

## 2. Paper claim → verifiable task
**Claim.** Magnetic-field correlation length normalised to d_i has a
monotonic trend across PSP, Helios 1, Voyager 1.

**Verifiable task.** Reproduction recovers the qualitative monotonic trend
with bin-averaged values within tolerance TODO verify.

## 3. Methods → executable protocol
- Auto-correlation and λ_C via e-folding (or integral length).
- Structure functions S_n(τ).
- SDK(τ) = S_4 / S_2^2.
- Bin by heliocentric distance; normalise lags by d_i.

Capabilities: multi-mission CDF fetch, cadence harmonisation, per-bin
statistical aggregation.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | perihelion (0.16 au) | CDAWeb | fetch CDF |
| Helios 1 MAG | L2 | TODO verify | 0.3-1 au | CDAWeb | fetch CDF |
| Voyager 1 MAG | L2 | TODO verify | 1-10 au | CDAWeb | fetch CDF |

## 5. Validation target
Not benchmarked yet.

## 6. Failure modes
- Cadence mismatch.
- Effective sampling direction differences.
- SDK sample-size requirement.
- Helios stream contamination.

## 7. Claim boundary
**In scope.** Distance-binned λ_C/d_i and SDK from the three named missions
over 0.16-10 au.
**Out of scope.** Sub-PSP-perihelion distances, kinetic-scale intermittency
at Voyager, single-stream conclusions.

## 8. Links and adapter binding examples
- arXiv: https://arxiv.org/abs/2202.01874
- DOI/ADS: TODO verify

## 9. Skill graph + affordances
Depends on [[sioulas-2022-magnetic-field-intermittency-psp-solo]].

- **Gap** — Solar Orbiter not used to fill 0.3-1 au.
- **Minimal experiment** — Overlay Solar Orbiter SDK(r/d_i).
