---
name: paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp
description: >-
  Use when characterising sub-ion (kinetic-Alfven-wave) anisotropy in
  slow-Alfvenic PSP intervals via wavelet spectra and the magnetic
  compressibility test — Duan et al. 2021 angle-bin sub-ion spectra and
  identify KAW-consistent perpendicular cascade (arXiv 2102.13294; venue TODO verify).
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
  title: "Anisotropy of Solar-Wind Turbulence in the Inner Heliosphere at Kinetic Scales: PSP Observations"
  first_author: "Duan, D."
  authors:
    - "Die Duan"
    - "Jiansen He"
    - "Trevor A. Bowen"
    - "Lloyd D. Woodham"
  year: 2021
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2102.13294"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [anisotropy, kinetic-scale, KAW, waves_instabilities]
  missions: [PSP]
  regime: [inner-heliosphere, ion-scale, kinetic]
trigger_keywords:
  - "kinetic-scale anisotropy"
  - "kinetic Alfven wave KAW"
  - "magnetic compressibility"
  - "wavelet spectrum PSP"
  - "slow Alfvenic wind"
  - "angle-binned spectrum"
  - "sub-ion cascade"
  - "Duan He Bowen Woodham 2021"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "burst-mode for sub-ion", interval: "TODO verify which PSP encounters", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Wavelet trace and component spectra"
    equation_refs: ["TODO verify"]
  - name: "Magnetic compressibility C|| = P_B||/P_B,tot"
    equation_refs: ["TODO verify"]
  - name: "Angle-binned sub-ion-range spectral index extraction"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2102.13294"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    In slow-Alfvenic PSP intervals (encounter range TODO verify), sub-ion
    magnetic-field fluctuations exhibit perpendicular-to-mean-field anisotropy
    with magnetic compressibility consistent with kinetic-Alfven-wave (KAW)
    turbulence.
  out_of_scope:
    - "Do not assume identical anisotropy in fast non-Alfvenic streams without re-binning."
    - "Do not extend KAW interpretation to scales beyond the resolved sub-ion-to-electron range."
    - "Do not equate magnetic compressibility level with branch identification absent the linear-Vlasov prediction."
failure_modes:
  - "Spacecraft spin-tone in MAG can mimic perpendicular power if not despun."
  - "Local-mean-field direction estimator (scale-dependent vs window-mean) shifts θ_kB binning."
  - "Sample-size collapses at large θ_kB bins, inflating slope error bars."
  - "Burst-mode duty cycle creates window-selection bias."
depends_on:
  - zhao-2022-3d-anisotropy-kinetic-scales-psp
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Claim is bound to slow-Alfvenic wind; sibling skill needed for fast-stream sub-ion anisotropy in the same encounter set."
  - type: hypothesis
    statement: "If KAW interpretation holds, magnetic-compressibility ratio at the ion break should match the linear-Vlasov KAW prediction within a defined tolerance."
    proposed_action: "Define a minimal experiment that computes C|| vs the linear-Vlasov prediction over PSP burst windows."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2021 item 5"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence, kinetic, KAW]
---

# Duan et al. 2021 — kinetic anisotropy in slow Alfvenic PSP wind — paper-skill

> Compiled from arXiv 2102.13294. `stub` tier — encounter selection, exact
> spectral indices, and compressibility tolerances are TODO verify.

## 1. Trigger
Use when measuring sub-ion magnetic-field anisotropy in slow-Alfvenic PSP
intervals, or distinguishing KAW vs whistler interpretations via magnetic
compressibility.

Do NOT use for fast non-Alfvenic streams without re-binning, or for
electron-scale physics beyond the resolved range.

## 2. Paper claim → verifiable task
**Claim.** Sub-ion magnetic-field fluctuations in slow-Alfvenic PSP intervals
show perpendicular anisotropy and magnetic compressibility consistent with
KAW turbulence.

**Verifiable task.** Reproduction succeeds when an agent recovers (i) the
qualitative steepening of perpendicular sub-ion spectra and (ii) the
compressibility level reported, within tolerance TODO verify.

## 3. Methods → executable protocol (abstract)
- Wavelet trace + component spectra on PSP MAG burst.
- Magnetic compressibility C|| computed in a local mean-field frame.
- Angle-binned spectral-index fit over the sub-ion range.

Capabilities: high-cadence MAG read, wavelet/PSD computation, local-frame
projection, per-bin power-law fit.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst (high-rate) | TODO verify encounters | CDAWeb / SPDF | fetch+decode CDF |

## 5. Validation target
Not benchmarked yet. Requires the paper's numerical spectral-index and
compressibility values.

## 6. Failure modes
- Spin-tone contamination if MAG is not despun.
- Local-mean-field direction estimator dependency.
- Sample collapse at extreme θ_kB.
- Burst-mode duty-cycle bias.

## 7. Claim boundary
**In scope.** Sub-ion anisotropy in slow-Alfvenic PSP wind.
**Out of scope.** Fast non-Alfvenic streams, electron-scale dynamics,
branch-identification without Vlasov support.

## 8. Links and adapter binding examples
- arXiv: https://arxiv.org/abs/2102.13294
- DOI: TODO verify
- ADS: TODO verify

## 9. Skill graph + affordances
Depends on [[zhao-2022-3d-anisotropy-kinetic-scales-psp]].

- **Gap** — Fast-stream counterpart at the same encounters.
- **Hypothesis** — KAW interpretation testable via Vlasov C|| match.
