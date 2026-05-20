---
name: paper-cuesta-2022-intermittency-psp-helios-voyager
description: >-
  Use when tracking radial evolution of solar-wind magnetic-field intermittency
  from 0.16 au to ~10 au using PSP, Helios 1 and Voyager 1 MAG data via
  auto-correlation, structure functions and scale-dependent kurtosis (SDK) —
  Cuesta et al. 2022 (ApJS 259, 23) build SDK(τ) families across distance bins
  and link SDK at fixed physical scale to the effective Reynolds number.
version: 0.2.0
kind: paper-skill
quality: paper-grounded-pending-full-text
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: true
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
  venue: "Astrophysical Journal Supplement Series 259, 23"
  doi: "10.3847/1538-4365/ac45fa"
  arxiv_id: "2202.01874"
  ads_bibcode: "2022ApJS..259...23C"
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, radial-evolution, multi-spacecraft, kurtosis, Reynolds-number]
  missions: [PSP, Helios, Voyager]
  regime: [inner-heliosphere, 1au, outer-heliosphere]
trigger_keywords:
  - "scale-dependent kurtosis SDK"
  - "magnetic field intermittency radial"
  - "structure function order n"
  - "correlation length lambda_C"
  - "ion inertial length d_i normalisation"
  - "effective Reynolds number"
  - "PSP Helios Voyager joint analysis"
  - "Kolmogorov refined similarity hypothesis"
  - "Cuesta Parashar Chhiber Matthaeus 2022"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s (resampled)", interval: "PSP perihelion intervals near 0.16 au", archive: "CDAWeb / PSP SOC"}
  - {instrument: "Helios 1 MAG", level: "L2 (Helios-1 archive)", cadence: "~6 s native (resampled to common cadence)", interval: "0.3–1 au selected intervals", archive: "CDAWeb / NSSDC Helios archive"}
  - {instrument: "Voyager 1 MAG", level: "L2 (Voyager MAG)", cadence: "~48 s native (resampled)", interval: "1–10 au cruise selected intervals", archive: "CDAWeb / PDS PPI"}
algorithms:
  - name: "Auto-correlation R(τ) and correlation length λ_C (e-folding or integral)"
    equation_refs: ["paper §2 correlation analysis"]
  - name: "Structure functions S_n(τ) of magnetic-field-vector increments"
    equation_refs: ["paper §2 structure functions"]
  - name: "Scale-dependent kurtosis SDK(τ) = S_4(τ) / S_2(τ)^2"
    equation_refs: ["paper §3 SDK"]
  - name: "Effective Reynolds number Re_eff via λ_C / d_i (or related ratio)"
    equation_refs: ["paper §3 Re_eff definition"]
  - name: "Distance-binned aggregation and trend extraction"
    equation_refs: ["paper §4 distance-binned trends"]
validation_targets:
  - "PSP (~0.16 au), Helios 1 (0.3–1 au), Voyager 1 (1–10 au) are the only three distance bands the paper supports — radial trend conclusions are restricted to these bins."
  - "Intervals (or distance bins) with lower effective Reynolds number Re_eff at a fixed physical scale show lower kurtosis (less intermittency) on average — this is the headline causal-style claim verified at abstract level."
  - "Auto-correlation, structure-function S_n and SDK families are reproducible with a single uniform pipeline across the three missions; per-mission systematic differences should not exceed the inter-bin Re_eff effect."
links:
  doi_url: "https://doi.org/10.3847/1538-4365/ac45fa"
  arxiv_url: "https://arxiv.org/abs/2202.01874"
  ads_url: "https://ui.adsabs.harvard.edu/abs/2022ApJS..259...23C"
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/ (PSP, Helios 1, Voyager 1 MAG)"
claim_boundary:
  scope: >-
    Magnetic-field intermittency measured by SDK(τ), kurtosis at a fixed
    physical scale, structure-function family S_n(τ), and correlation
    length λ_C is characterised across three heliocentric bands —
    PSP ~0.16 au, Helios 1 0.3–1 au, and Voyager 1 1–10 au — using a
    single uniform pipeline. The claim that "regions with lower Re_eff at
    a fixed physical scale have on average lower kurtosis" is supported
    by the abstract at this verification depth.
  out_of_scope:
    - "Do not equate the three-band trend with a continuous expansion law without modeling the per-mission systematic-error budget (cadence, calibration epoch, sampling direction)."
    - "Do not export the SDK lag dependence to kinetic scales unresolved at Voyager (Voyager 1 cadence cannot resolve d_i in the outer heliosphere)."
    - "Do not extend the radial trend below 0.16 au or beyond 10 au from this sample alone."
    - "Do not interpret SDK(τ) as a single-cause intermittency measure — Re_eff covariation is a *correlation*, not a controlled-experiment causal statement."
failure_modes:
  - "Cadence differences between PSP (~1 vec/s after resample), Helios 1 (~6 s native), and Voyager 1 (~48 s native) bias the inertial-range lag window — resampling must be done before structure-function aggregation, not after."
  - "Sampling-direction differences (PSP swing-by vs Helios in-ecliptic vs Voyager outbound) shift the effective Taylor projection; do not assume isotropy without per-mission sanity checks."
  - "S_n at n ≥ 4 requires large sample sizes; report bin count per lag, especially for short Helios intervals."
  - "Mixed-stream contamination at Helios 1 (CIRs, fast/slow stream mixing) inflates SDK; the paper's per-band aggregation can hide outlier-stream effects."
  - "Voyager MAG calibration epoch and quiet-time gaps in the outer heliosphere reduce effective sample at large τ; mask explicitly."
  - "Lag-to-distance mapping via Taylor frozen-in hypothesis is more reliable at Voyager (large V_SW/V_A) than at PSP perihelion (where V_A approaches V_SW)."
depends_on:
  - sioulas-2022-magnetic-field-intermittency-psp-solo
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill yet uses Solar Orbiter to fill 0.3–1 au alongside PSP+Helios+Voyager for a four-mission consistency check."
    proposed_action: "Replicate the Cuesta SDK(r/d_i) pipeline on Solar Orbiter MAG (Helios-overlap distance band) and overlay on the published three-mission trend."
  - type: hypothesis
    statement: "If Re_eff is the dominant driver of the radial kurtosis trend (paper's framing), then SDK at fixed physical scale should collapse when plotted vs Re_eff *within* a single mission's distance bins, not just across missions."
    proposed_action: "Stratify PSP perihelion intervals by Re_eff (using λ_C / d_i) and test for an intra-mission SDK collapse before invoking the inter-mission trend."
  - type: tension
    statement: "[[sioulas-2022-magnetic-field-intermittency-psp-solo]] reports a *scale-conditional* radial monotonicity (only small scales, ~20–100 d_i, show monotonicity); Cuesta 2022 frames the trend through Re_eff, which is a single-scale aggregate. The two framings are not contradictory but answer different questions — explicitly map between (scale-band) and (Re_eff aggregate)."
    proposed_action: "Run the Cuesta SDK pipeline on the Sioulas PSP+SolO interval set and report SDK both per-scale-band and per-Re_eff-bin."
  - type: composable_experiment
    statement: "Couple the per-bin Re_eff and SDK table from this paper to a cascade-rate table (e.g. [[paper-andres-2021-incompressible-cascade-anisotropic-pp]]) to test whether ε(r) and SDK(r) co-vary — i.e. whether intermittency tracks the cascade rate or the integral-scale geometry."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2022 item 7"
  verified_by: "internalization-batch 2026-05-19 (arXiv 2202.01874 + IOPscience DOI landing)"
  verified_at: "2026-05-19T00:00:00Z"
  verification_notes:
    - "field=doi value=10.3847/1538-4365/ac45fa source=IOPscience-landing verified_at=2026-05-19"
    - "field=venue value=ApJS-259-23-2022 source=IOPscience-landing verified_at=2026-05-19"
    - "field=arxiv_id value=2202.01874 source=arXiv-abs-page verified_at=2026-05-19"
tags: [heliophysics, paper-skill, turbulence, intermittency, multi-mission, kurtosis]
---

# Cuesta et al. 2022 — multi-mission intermittency radial evolution — paper-skill

> Compiled from arXiv:2202.01874 = ApJS 259, 23 (DOI 10.3847/1538-4365/ac45fa).
> `paper-grounded-pending-full-text` tier — bibliographic anchors, the three
> distance bands, and the qualitative Re_eff–kurtosis claim are verified from
> the abstract and IOPscience landing. Per-band numerical values for SDK at
> fixed scale, the precise Re_eff definition, and exact interval lists remain
> pending full-text verification.

## 1. Trigger  *(Layer 1)*

Use when:

- characterising radial evolution of magnetic-field intermittency across the
  full 0.16–10 au span using one consistent pipeline;
- relating intermittency (SDK, kurtosis at fixed scale) to an aggregate
  Reynolds-number-like control parameter (λ_C / d_i);
- producing a *baseline* radial trend that more focused studies (e.g.
  PSP+SolO scale-conditional intermittency) can be compared against.

Do NOT use this skill for kinetic-scale intermittency at Voyager (cadence
cannot resolve), for sub-0.16-au perihelia (out of sample), or for
single-stream / single-encounter detailed analysis.

## 2. Paper claim → narrow verifiable task

**Verified claim (abstract + IOPscience landing, 2026-05-19).** Using
magnetic-field auto-correlation, structure functions S_n, and scale-dependent
kurtosis SDK on PSP (~0.16 au), Helios 1 (0.3–1 au) and Voyager 1 (1–10 au)
data, the paper shows that intermittency evolves with heliocentric distance
and that, at a fixed physical scale, regions with lower effective Reynolds
number Re_eff have on average lower kurtosis.

**Narrow verifiable task.** Reproduction succeeds when an agent, given the
three-mission interval set, recovers:

1. correlation length λ_C estimates per distance band, computed by the same
   (e-folding or integral) definition across all three missions;
2. structure-function families S_n(τ) up to a stated maximum n that converges
   on each mission's interval lengths;
3. SDK(τ) per distance band with sample-size reporting per lag;
4. the qualitative monotonic ordering between Re_eff and kurtosis at a fixed
   physical scale.

## 3. Executable protocol (Layer 2 — abstract capabilities)

The skill requires the following abstract capabilities:

1. **Multi-mission MAG reader** — returns B(t) for PSP/FIELDS, Helios 1, and
   Voyager 1 in a common frame; must handle each mission's native cadence and
   calibration epoch.
2. **Cadence-harmonising resampler** — projects each mission's series onto a
   common time grid with documented anti-aliasing.
3. **Auto-correlation + λ_C estimator** — computes R(τ) and λ_C via the same
   definition (e-folding or integral) across all three missions.
4. **Structure-function family** — computes S_n(τ) for n up to the
   convergence limit of the shortest interval in the set; returns per-lag
   sample counts.
5. **Scale-dependent kurtosis** — SDK(τ) = S_4(τ) / S_2(τ)^2; reports SDK
   with explicit sample-size masking.
6. **Re_eff calculator** — computes Re_eff per interval from λ_C, d_i
   (requiring proton density n_p), and any additional inputs the paper
   defines; documents the precise functional form.
7. **Distance-binned aggregator** — bins per-interval results by
   heliocentric distance and produces the SDK(τ; r) and SDK(fixed scale; Re_eff)
   tables that are the paper's central artefacts.

Abstract procedure:

1. Select PSP perihelion, Helios 1, and Voyager 1 intervals covering the
   three distance bands.
2. Resample each mission's MAG to a common cadence; document the cadence
   choice (the paper's choice is pending full-text verification).
3. Compute R(τ), λ_C, S_n(τ), SDK(τ), and Re_eff per interval.
4. Aggregate by distance band; report SDK at one or more fixed physical
   scales.
5. Plot SDK(fixed scale) vs Re_eff across all bins; the headline result is
   the monotonic ordering.
6. Acceptance: reproduce the qualitative ordering (lower Re_eff → lower
   kurtosis) and the band-resolved SDK(τ) shapes.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability required |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s (after resample) | PSP perihelion ~0.16 au | CDAWeb / PSP SOC | high-cadence vector MAG reader with despin |
| Helios 1 MAG | L2 / Helios-1 archive | ~6 s native (resampled) | selected intervals 0.3–1 au | CDAWeb / NSSDC Helios archive | legacy CDF reader, calibration-epoch aware |
| Voyager 1 MAG | L2 | ~48 s native (resampled) | selected cruise intervals 1–10 au | CDAWeb / PDS PPI | legacy CDF reader, gap-aware aggregator |
| Proton density n_p (per mission, for d_i) | L2/L3 | as available | matching | mission-specific archives | n_p reader for d_i computation |

## 5. Validation target

**Primary targets (verified at abstract level).**

- Three distance bands are PSP ~0.16 au, Helios 1 0.3–1 au, Voyager 1
  1–10 au; conclusions are restricted to this radial coverage.
- At fixed physical scale, intervals with lower Re_eff show on average lower
  kurtosis — qualitative monotonic ordering.
- A single uniform pipeline (R(τ), λ_C, S_n, SDK, Re_eff) produces consistent
  artefacts across all three missions.

**Tolerance budget.** Per-band SDK(τ) shape and per-band Re_eff–SDK ordering
should reproduce within the paper's stated uncertainty bars (numerical values
**pending full-text verification**). Quantitative disagreement at fixed lag
that exceeds ±0.3 in SDK is a likely pipeline-disagreement flag (resampling,
λ_C definition, or d_i normalisation).

## 6. Failure modes (load-bearing)

- **Cadence resampling order.** Resampling must precede increment
  computation; resampling *after* aggregating S_n biases the inertial range.
- **Mission-specific sampling direction.** PSP swing-by vs Helios in-ecliptic
  vs Voyager outbound shift the effective Taylor projection; isotropy must
  be checked, not assumed.
- **High-n convergence.** S_n at n ≥ 4 demands long records — short Helios
  intervals can fail convergence; report sample count per lag.
- **Stream-mixture bias at Helios.** CIRs and fast/slow boundaries during
  Helios in-ecliptic operations can inflate SDK relative to a uniform stream.
- **Voyager calibration / gaps.** Outer-heliosphere MAG calibration epochs
  and large-τ gap structure reduce effective sample at the largest lags.
- **Taylor-hypothesis margin at PSP perihelion.** V_A approaches V_SW near
  0.16 au, so the lag-to-distance mapping margin is narrower than at Helios
  or Voyager — sanity-check with V_eff = sqrt(V_SW^2 + V_A^2).
- **Re_eff definition sensitivity.** SDK collapse vs Re_eff depends on the
  exact Re_eff functional form; document the form explicitly.

## 7. Claim boundary

**In scope.** Per-band SDK, S_n, λ_C and the qualitative Re_eff–kurtosis
monotonic ordering across PSP ~0.16 au, Helios 1 0.3–1 au, Voyager 1 1–10 au.

**Out of scope.** Kinetic-scale intermittency at Voyager, sub-0.16-au or
super-10-au extrapolation, continuous radial expansion-law fits, single-
encounter / single-stream conclusions, and causal claims about Re_eff being
the *sole* driver of the trend (the paper supports correlation, not a
controlled-experiment causal statement).

## 8. Links and identifiers

- DOI: <https://doi.org/10.3847/1538-4365/ac45fa> (ApJS 259, 23 — verified
  2026-05-19 from IOPscience landing).
- arXiv: <https://arxiv.org/abs/2202.01874> (verified 2026-05-19).
- ADS: <https://ui.adsabs.harvard.edu/abs/2022ApJS..259...23C> (bibcode
  follows ApJS 259 23 C pattern; not independently verified via ADS UI).

## 9. Skill graph + Layer-4 affordances

Depends on [[sioulas-2022-magnetic-field-intermittency-psp-solo]] (a PSP+SolO
intermittency-radial pipeline that is the natural inner-heliosphere comparator
to Cuesta's three-mission span).

- **Gap.** Solar Orbiter is not used to fill the 0.3–1 au band alongside
  Helios; running the Cuesta pipeline on SolO MAG would give a four-mission
  consistency check.
- **Hypothesis (testable).** If Re_eff is the dominant control on radial
  kurtosis, SDK(fixed scale) should collapse vs Re_eff *within* a single
  mission's intervals, not just across missions. Test on PSP-only perihelion
  intervals stratified by λ_C / d_i.
- **Tension.** [[sioulas-2022-magnetic-field-intermittency-psp-solo]] reports
  *scale-conditional* radial monotonicity (only at small scales, ~20–100 d_i).
  Cuesta 2022 frames the trend through an aggregate Re_eff — explicitly
  cross-map (scale band) ↔ (Re_eff aggregate) to reconcile.
- **Composable experiment.** Couple the per-bin Re_eff/SDK table to a
  cascade-rate skill (e.g.
  [[paper-andres-2021-incompressible-cascade-anisotropic-pp]]) to test whether
  ε(r) and SDK(r) co-vary, distinguishing intermittency-as-cascade-symptom
  vs intermittency-as-geometry-effect.

## 10. Relation to HelioSI corpus

- Parent sub-graph: `wave500_turbulence_intermit_heating_045` (intermittency,
  scale-dependent kurtosis, radial evolution).
- Sibling paper-skills: [[sioulas-2022-magnetic-field-intermittency-psp-solo]]
  (PSP+SolO scale-conditional intermittency),
  [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] (cascade rate
  on overlapping PSP intervals),
  [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]] (provides the
  stream-type stratification this skill's failure-mode list assumes).
- Required capabilities (not bound here): multi-mission MAG reader,
  cadence-harmonising resampler, structure-function family, SDK, λ_C
  estimator, Re_eff calculator, distance-binned aggregator.
