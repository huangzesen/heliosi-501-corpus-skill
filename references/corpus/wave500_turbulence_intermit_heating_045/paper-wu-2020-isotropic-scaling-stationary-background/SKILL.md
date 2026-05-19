---
name: paper-wu-2020-isotropic-scaling-stationary-background
description: >-
  Use when measuring solar-wind turbulence scaling exponents with a strict
  local-stationarity-of-the-background-field criterion — Wu et al. 2020
  argue that under stationary-background sampling the magnetic-field
  structure-function exponents are isotropic (arXiv 2011.10244; venue TODO verify).
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
  title: "Isotropic Scaling Features Measured Locally in the Solar Wind Turbulence with Stationary Background Field"
  first_author: "Wu, H."
  authors:
    - "Honghong Wu"
    - "Chuanyi Tu"
    - "Xin Wang"
    - "Jiansen He"
  year: 2020
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2011.10244"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [anisotropy, structure-function, sampling]
  missions: [Wind, ACE, other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "stationary background field"
  - "local mean field structure function"
  - "isotropy versus anisotropy solar wind"
  - "sampling-angle dependence"
  - "Wu Tu Wang He 2020"
  - "local frame turbulence"
  - "structure function scaling exponents"
  - "Kolmogorov isotropy"
data_products:
  - {instrument: "TODO verify (likely Wind/MFI + 3DP or ACE/MAG+SWEPAM)", level: "L2", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Stationary-background-field windowing"
    equation_refs: ["TODO verify"]
  - name: "Local-mean-field structure functions"
    equation_refs: ["TODO verify"]
  - name: "Sampling-angle-resolved scaling exponents"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2011.10244"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Under a strict stationarity-of-background-field criterion applied to
    fast-wind in-situ data (mission TODO verify), the magnetic-field
    structure-function exponents become approximately isotropic with respect
    to sampling angle θ_VB.
  out_of_scope:
    - "Do not conclude that turbulence is intrinsically isotropic when stationarity is relaxed."
    - "Do not export the isotropy claim to kinetic-scale spectra; the paper addresses inertial-range structure functions."
    - "Do not generalise to slow or non-Alfvenic streams without re-applying the stationarity rule."
failure_modes:
  - "Choice of stationarity window length and threshold tightly controls how many intervals survive — report explicit cuts."
  - "Selection bias: stationary windows preferentially capture quiet intervals which may themselves be more isotropic."
  - "Local-mean-field estimator (scale-dependent vs scale-independent) shifts apparent exponents."
  - "Single-spacecraft Taylor-hypothesis bias persists; stationarity does not remove it."
depends_on: []
adapter_notes: []
research_generation_affordances:
  - type: tension
    statement: "Isotropic-scaling conclusion under stationary background contrasts with anisotropic-exponent results in [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] and [[sioulas-2024-higher-order-3d-anisotropy]] in the inner heliosphere."
    related_skills: [sioulas-2023-anisotropic-scaling-inner-heliosphere, sioulas-2024-higher-order-3d-anisotropy]
    proposed_action: "Define a minimal experiment that applies the same stationarity rule to PSP E1-E13 fast-wind data and reports whether isotropy survives near the Sun."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2020 item 2"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence, anisotropy]
---

# Wu et al. 2020 — isotropic scaling under stationary background field — paper-skill

> Compiled from arXiv 2011.10244. `stub` tier — many details (instrument
> identity, exact stationarity threshold, exponent values) are TODO verify.

## 1. Trigger  *(Layer 1)*

Use when:
- Measuring solar-wind turbulence scaling exponents and you need a
  **stationarity-controlled** estimator to remove non-stationary background
  drift.
- Adjudicating whether observed angular anisotropy of structure-function
  exponents is intrinsic or an artefact of background non-stationarity.

Do NOT use when:
- Working at kinetic scales (use [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]).
- The target is near-Sun PSP data without re-deriving the stationarity cut.

## 2. Paper claim → verifiable task

**Claim (narrow form).** When the analysis is restricted to time windows in
which the background magnetic field passes a strict stationarity test, the
inferred magnetic-field structure-function exponents are approximately
isotropic in the sampling angle θ_VB (mission TODO verify).

**Verifiable task.** A reproduction succeeds when an agent recovers the
qualitative collapse of ζ_n(θ_VB) onto a single curve after applying the
paper's stationarity rule to the same dataset. Exact tolerances TODO verify.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Stationary-background-field windowing
- Procedure: slide a window of length L over the time series, compute a
  stationarity score on the background mean field (e.g. low variance of
  per-window mean angle), and accept only windows above threshold.
- Capability: per-window statistics on a continuous vector time series.

### Local-mean-field structure functions
- Procedure: per accepted window, define a local mean field; compute
  increment vectors at lag τ; project parallel/perpendicular; compute
  S_n(τ, θ) = ⟨|δB|^n⟩.

### Sampling-angle-resolved scaling exponents
- Procedure: fit ζ_n(θ_VB) over the inertial range; compare to the
  unconditioned estimate.

## 4. Data / instruments → abstract tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| TODO verify mission (Wind/ACE/Helios) MAG | L2 | TODO verify | TODO verify | CDAWeb | fetch+decode CDF |
| Corresponding plasma instrument | L2/L3 | TODO verify | TODO verify | CDAWeb | for V to compute θ_VB |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion requires fixing exponent targets vs angle from
the paper's figures.

## 6. Failure modes → skill memory

- Stationarity threshold determines yield and selects quieter intervals.
- Local-mean-field estimator choice shifts exponents.
- Taylor-hypothesis bias persists.
- Inertial-range fitting window must be re-justified per interval.

## 7. Claim boundary

**In scope.** Inertial-range magnetic-field structure-function exponents,
under the paper's stationarity rule, on the dataset it analyses.

**Out of scope.** Kinetic-scale anisotropy, slow/non-Alfvenic wind, PSP
near-Sun data without re-derivation.

## 8. Links and adapter binding examples

- DOI: n/a
- arXiv: https://arxiv.org/abs/2011.10244
- ADS: n/a

## 9. Skill graph + affordances

No `depends_on` yet.

- **Tension** — Conflicts with [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] and
  [[sioulas-2024-higher-order-3d-anisotropy]], which find robust 3D
  anisotropy. Discriminator: apply the stationarity rule of this paper to the
  PSP data of the Sioulas papers and report whether isotropy emerges.
