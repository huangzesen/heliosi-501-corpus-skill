---
name: paper-mcintyre-2024-helicity-barrier-transition-range
description: >-
  Use when looking for observational evidence of the helicity-barrier-driven
  spectral steepening in the ion-scale transition range of solar-wind
  turbulence — McIntyre, Chen, Squire, Meyrand & Simon 2024 (PRX 15, 031008,
  2025) measure the PSP magnetic-spectrum shape near the ion gyroradius and
  show it varies with solar-wind parameters consistently with the
  helicity-barrier prediction, becoming prominent at low ion plasma beta
  (β_p ≲ 0.5) and high imbalance (|σ_c| ≳ 0.4).
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
  title: "Evidence for the helicity barrier from measurements of the turbulence transition range in the solar wind"
  first_author: "McIntyre, J. R."
  authors:
    - "J. R. McIntyre"
    - "C. H. K. Chen"
    - "J. Squire"
    - "R. Meyrand"
    - "P. A. Simon"
  year: 2025
  venue: "Physical Review X 15, 031008"
  doi: "10.1103/PhysRevX.15.031008"
  arxiv_id: "2407.10815"
  ads_bibcode: null
  identity_uncertainty: >-
    Slug 'mcintyre-2024-...' inherits the arXiv-submission year (Jul 2024)
    but the paper was published in PRX in 2025. The 'paper.year' field is
    the publication year (2025); slug is preserved unchanged to keep
    cross-skill [[wikilinks]] stable. ADS bibcode is not asserted (ADS UI
    is JS-rendered).
domain:
  primary_theme: turbulence
  secondary_themes: [helicity-barrier, ion-scale, transition-range, imbalance, ion-cyclotron]
  missions: [PSP]
  regime: [inner-heliosphere, ion-scale, transition-range]
trigger_keywords:
  - "helicity barrier observational"
  - "transition-range spectral steepening"
  - "ion gyroradius spectrum shape"
  - "imbalanced turbulence cross helicity"
  - "ion plasma beta low"
  - "ion-cyclotron heating"
  - "PSP ion-scale spectrum"
  - "McIntyre Chen Squire Meyrand Simon 2024"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "high-cadence sufficient to resolve scales near the ion gyroradius / ion break", interval: "selected PSP intervals (encounter set covering low-β_p high-|σ_c| conditions; exact list pending full-text verification)", archive: "CDAWeb / PSP SOC"}
  - {instrument: "PSP/SWEAP (SPC and/or SPAN-I)", level: "L3", cadence: "as available", interval: "matched to MAG selection (n_p, T_p, B for β_p)", archive: "CDAWeb / PSP SOC"}
algorithms:
  - name: "Magnetic-spectrum shape near the ion gyroradius (transition range)"
    equation_refs: ["paper §II spectrum-shape diagnostic"]
  - name: "Imbalance-conditioned subsample selection (|σ_c| threshold ~ 0.4)"
    equation_refs: ["paper §III imbalance conditioning"]
  - name: "β_p-conditioned subsample selection (low-β_p subsample, β_p ≲ 0.5)"
    equation_refs: ["paper §III β-conditioning"]
  - name: "Comparison to helicity-barrier theoretical prediction"
    equation_refs: ["paper §IV theory comparison"]
validation_targets:
  - "PSP data used (not Wind/Ulysses, despite factory metadata's hedge) — verified at abstract level."
  - "Helicity-barrier signature becomes prominent for ion plasma beta β_p ≲ 0.5 (abstract-level)."
  - "Helicity-barrier signature becomes prominent for normalised cross helicity |σ_c| ≳ 0.4 (abstract-level)."
  - "Magnetic-energy spectrum shape near the ion gyroradius varies systematically with solar-wind parameters in the direction predicted by the helicity-barrier model."
  - "These conditions (low β_p, high |σ_c|) frequently occur in the solar wind and particularly close to the Sun."
links:
  doi_url: "https://doi.org/10.1103/PhysRevX.15.031008"
  arxiv_url: "https://arxiv.org/abs/2407.10815"
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/ (PSP FIELDS + SWEAP)"
claim_boundary:
  scope: >-
    The ion-scale transition-range magnetic-spectrum shape in PSP solar-wind
    intervals depends on (β_p, |σ_c|) in the direction predicted by the
    helicity-barrier model — the barrier signature becomes prominent at
    β_p ≲ 0.5 and |σ_c| ≳ 0.4. The claim is statistical (over the
    selected PSP interval set), conditional on those plasma parameters, and
    operates near the ion gyroradius scale.
  out_of_scope:
    - "Do not assert helicity barrier is the *unique* cause of transition-range steepening without an independent discriminator against ion-cyclotron-damping, Hall-MHD, or kinetic-Alfvén-wave alternatives."
    - "Do not extrapolate the result to balanced turbulence (|σ_c| ≲ 0.4) — the abstract conditions evidence on the high-imbalance subsample."
    - "Do not equate transition-range slope with a specific dissipation channel; the paper supports a barrier-shaped spectrum, not a localised heating rate."
    - "Do not extend the conclusion to high-β_p plasma (β_p ≳ 0.5) without a separately stratified analysis."
    - "Do not transfer the result from PSP to 1 au without re-running — the (β_p, |σ_c|) joint distribution shifts radially."
failure_modes:
  - "Transition-range fit window depends on β_p — at higher β_p the ion gyroradius and ion inertial length separate, shifting which scales are 'transition-range'."
  - "Imbalance-conditioning threshold (|σ_c| ≳ 0.4) is set by the paper; lowering the threshold dilutes the signal, raising it collapses sample size."
  - "Local-mean-field choice (window-mean vs scale-dependent) shifts the spectral-shape diagnostic; the paper's claim is conditioned on the estimator it uses."
  - "Spectral leakage from the inertial range can mimic the transition-range steepening if the fit window crosses the ion break."
  - "PSP burst-mode duty cycle controls how many low-β_p high-|σ_c| intervals reach the sub-ion range; burst availability biases the subsample."
  - "Cross-helicity sign convention requires a consistent outward-direction reference; sign flips at HCS crossings inflate |σ_c| dispersion."
  - "Ion-cyclotron damping and helicity-barrier predictions can produce overlapping spectral signatures — the paper's argument is parameter-trend consistency, not a uniqueness theorem."
depends_on:
  - paper-sasmal-2026-helicity-barrier-flr-mhd-heating
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the helicity barrier holds robustly, PSP perihelia intervals with very low β_p (β_p ≲ 0.2) and very high |σ_c| (|σ_c| ≳ 0.8) should show an even sharper transition-range steepening than the published abstract-level signal."
    proposed_action: "Stratify PSP perihelion intervals into a 2D (β_p, |σ_c|) grid and test for monotonic strengthening of the barrier signature toward the lower-β_p, higher-|σ_c| corner."
  - type: gap
    statement: "PSP-only coverage. No sibling skill yet runs the same transition-range-shape pipeline on Solar Orbiter or Wind to test whether the barrier signature persists at higher heliocentric distance when the same (β_p, |σ_c|) cuts are imposed."
    proposed_action: "Replicate on SolO MAG+SWA at 0.3–1 au and on Wind at 1 au, using identical β_p, |σ_c| thresholds; expect lower sample size but check whether the (β_p, |σ_c|)-conditioned signature remains."
  - type: tension
    statement: "Transition-range steepening is also predicted by ion-cyclotron-resonant absorption (e.g. [[bowen-2024-extended-cyclotron-resonant-heating]]) and by kinetic-Alfvén-wave physics ([[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]]). Same PSP intervals should be analysed through all three lenses to distinguish which predictions co-vary uniquely with (β_p, |σ_c|)."
    related_skills: [bowen-2024-extended-cyclotron-resonant-heating, paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp, paper-sasmal-2026-helicity-barrier-flr-mhd-heating]
    proposed_action: "Run helicity-barrier, ion-cyclotron-resonance, and KAW diagnostics on a shared PSP interval set; report which diagnostic best collapses with the (β_p, |σ_c|) axis."
  - type: composable_experiment
    statement: "Couple the (β_p, |σ_c|, transition-range-shape) catalogue to [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]]'s stream-origin annotation — testing whether the barrier signature concentrates in active-region-originated, highly-Alfvénic streams or whether it is uniform across stream classes once (β_p, |σ_c|) are matched."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2407.10815v1)"
  verified_by: "internalization-batch 2026-05-19 (arXiv 2407.10815 + PRX landing)"
  verified_at: "2026-05-19T00:00:00Z"
  verification_notes:
    - "field=doi value=10.1103/PhysRevX.15.031008 source=PRX-landing verified_at=2026-05-19"
    - "field=venue value=PRX-15-031008-2025 source=PRX-landing verified_at=2026-05-19"
    - "field=arxiv_id value=2407.10815 source=arXiv-abs-page verified_at=2026-05-19"
    - "field=author_list value=five-authors-restored source=arXiv-abs-page verified_at=2026-05-19"
    - "field=mission value=PSP-corrected-from-Wind-Ulysses-hedge source=arXiv-abstract verified_at=2026-05-19"
    - "field=publication_year value=2025-preserving-mcintyre-2024-slug-for-wikilink-stability source=PRX-landing verified_at=2026-05-19"
tags: [heliophysics, paper-skill, turbulence, helicity-barrier, ion-scale, transition-range, PSP, imbalance]
---

# McIntyre et al. 2024/2025 — Helicity-barrier evidence in PSP transition-range spectra — paper-skill

> Compiled from arXiv:2407.10815 = Phys. Rev. X 15, 031008 (2025)
> (DOI 10.1103/PhysRevX.15.031008).
> `paper-grounded-pending-full-text` tier — bibliographic anchors, PSP as
> the data source, the (β_p ≲ 0.5, |σ_c| ≳ 0.4) parameter regime where the
> barrier signature is prominent, and the spectral-shape-varies-with-
> solar-wind-parameters direction-of-effect are verified at abstract level.
> Per-bin numerical spectral-shape parameters, the exact functional form
> of the helicity-barrier prediction used for comparison, and the precise
> PSP interval list are pending full-text verification.
>
> **Identity note (preserve uncertainty).** Slug name preserves the arXiv-
> submission year (2024); publication year is 2025. ADS bibcode not
> asserted. Factory metadata hedged the mission as "Wind/Ulysses/etc.
> TODO verify" — corrected to PSP.

## 1. Trigger  *(Layer 1)*

Use when:

- looking for observational evidence of the helicity barrier in solar-wind
  turbulence;
- characterising how the magnetic-energy spectrum shape *near the ion
  gyroradius* (transition range) depends on solar-wind plasma parameters
  (β_p, |σ_c|);
- stratifying turbulence intervals by (β_p, |σ_c|) to test the prediction
  that barrier-shaped spectra emerge at low β_p and high imbalance.

Do NOT use this skill to (a) attribute a dissipation channel (the
spectral-shape signature is a barrier *signature*, not a heating-rate
measurement), (b) generalise to balanced or high-β_p subsamples without
re-fitting, or (c) claim uniqueness of the helicity-barrier explanation
over competing models (ion-cyclotron damping, KAW dispersion) without a
direct model-vs-model discriminator.

## 2. Paper claim → narrow verifiable task

**Verified claim (abstract + PRX landing, 2026-05-19).** Using Parker
Solar Probe data, the magnetic-energy spectrum shape near the ion
gyroradius varies with solar-wind parameters in the direction predicted by
the helicity-barrier model. The barrier signature becomes prominent at ion
plasma beta β_p ≲ 0.5 and normalised cross helicity |σ_c| ≳ 0.4;
these conditions frequently occur in the solar wind, particularly
close to the Sun.

**Narrow verifiable task.** Reproduction succeeds when an agent, given a
PSP interval set covering a range of (β_p, |σ_c|):

1. computes the magnetic-energy spectrum shape near the ion gyroradius for
   each interval, using a documented spectral-shape diagnostic;
2. computes β_p and |σ_c| per interval;
3. recovers a monotonic strengthening of the barrier-shape signature with
   decreasing β_p across the sample;
4. recovers a monotonic strengthening with increasing |σ_c|;
5. shows the strongest barrier-shape signature in the (β_p ≲ 0.5,
   |σ_c| ≳ 0.4) corner.

## 3. Executable protocol (Layer 2 — abstract capabilities)

Required abstract capabilities:

1. **PSP MAG + ion-moment reader.** Returns high-cadence B(t) plus n_p,
   T_p, V from SWEAP, sufficient to resolve scales near the ion gyroradius
   and to compute β_p.
2. **Spectrum-shape diagnostic near the ion gyroradius.** Computes the
   magnetic-energy spectrum shape (e.g. local slope, curvature, or
   barrier-specific shape parameter) near the ion gyroradius scale.
3. **β_p calculator.** β_p = 2 μ₀ n_p k_B T_p / B² (or the paper's exact
   form).
4. **σ_c diagnostic.** Normalised cross helicity over a documented
   integration window.
5. **(β_p, |σ_c|)-stratified aggregator.** Bins per-interval spectrum-shape
   parameters by (β_p, |σ_c|) and produces 2D mean / median tables.
6. **Helicity-barrier theory reference.** Returns the model-predicted
   spectrum shape at a given (β_p, |σ_c|) for comparison.

Abstract procedure:

1. Select PSP intervals spanning the (β_p, |σ_c|) plane.
2. Compute spectrum-shape parameter near the ion gyroradius per interval.
3. Compute β_p and |σ_c| per interval; require minimum integration window.
4. Aggregate spectrum-shape vs (β_p, |σ_c|).
5. Compare to the helicity-barrier prediction at matched (β_p, |σ_c|).
6. Acceptance: recover the monotonic strengthening trends and the
   barrier-shape concentration in the (low-β_p, high-|σ_c|) corner.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability required |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | high-cadence (sub-ion resolved) | selected PSP intervals covering the (β_p, |σ_c|) plane | CDAWeb / PSP SOC | high-cadence vector MAG reader with despin |
| PSP/SWEAP SPC | L3 | ~1 Hz | early-mission portion of selection | CDAWeb / PSP SOC | proton moments reader (for β_p) |
| PSP/SWEAP SPAN-I | L3 | as available | later portion of selection | CDAWeb / PSP SOC | proton moments reader (cross-calibrated with SPC) |

## 5. Validation target

**Primary qualitative targets (verified at abstract level).**

- Mission: PSP.
- Barrier signature prominent at β_p ≲ 0.5.
- Barrier signature prominent at |σ_c| ≳ 0.4.
- Spectrum shape near the ion gyroradius varies systematically with
  (β_p, |σ_c|) in the direction predicted by the helicity barrier.

**Tolerance budget.** Exact spectral-shape numerical values per (β_p,
|σ_c|) bin, the precise barrier-prediction functional form used for
comparison, and the encounter-by-encounter interval list are **pending
full-text verification**. Sign reversal of either monotonic trend at the
per-bin level is a pipeline-disagreement flag.

## 6. Failure modes (load-bearing)

- **Transition-range fit window depends on β_p.** At higher β_p the ion
  gyroradius and ion inertial length separate, shifting which scales are
  'transition-range'.
- **Imbalance threshold sensitivity.** |σ_c| ≳ 0.4 is the paper's choice;
  lowering dilutes the signal, raising collapses sample size.
- **Local-mean-field estimator drift.** Window-mean vs scale-dependent
  changes the spectral-shape diagnostic.
- **Inertial-range spectral leakage.** Fit window crossing the ion break
  can mimic transition-range steepening.
- **PSP burst-mode duty-cycle bias.** Sub-ion-resolved windows in the
  low-β_p high-|σ_c| corner depend on burst availability — report the
  fraction of perihelion covered in burst.
- **σ_c sign convention / HCS flips.** Inconsistent outward reference
  inflates |σ_c| dispersion and biases the conditioning cut.
- **Non-uniqueness of barrier signature.** Ion-cyclotron damping and KAW
  physics also produce transition-range steepening — the paper's argument
  is *parameter-trend consistency*, not a uniqueness proof.

## 7. Claim boundary

**In scope.** Statistical PSP analysis of magnetic-energy spectrum shape
near the ion gyroradius, stratified by (β_p, |σ_c|); evidence that the
helicity-barrier prediction is consistent with the observed parameter
trend; barrier signature concentrated at β_p ≲ 0.5 and |σ_c| ≳ 0.4.

**Out of scope.** Balanced (|σ_c| ≲ 0.4) or high-β_p subsamples, 1 au
extrapolation without re-fitting, dissipation-channel attribution, and
claims of uniqueness vs ion-cyclotron or KAW alternatives.

## 8. Links and identifiers

- DOI: <https://doi.org/10.1103/PhysRevX.15.031008> (PRX 15, 031008 (2025)
  — verified 2026-05-19).
- arXiv: <https://arxiv.org/abs/2407.10815> (verified 2026-05-19).
- ADS: not asserted (UI is JS-rendered).

## 9. Skill graph + Layer-4 affordances

Depends on [[paper-sasmal-2026-helicity-barrier-flr-mhd-heating]]
(theoretical sibling on the same barrier physics).

- **Hypothesis (testable).** PSP perihelia intervals with very low β_p
  (β_p ≲ 0.2) and very high |σ_c| (|σ_c| ≳ 0.8) should show an even
  sharper transition-range steepening than the published abstract-level
  signal.
- **Gap.** PSP-only coverage. No sibling skill yet runs the same
  transition-range-shape pipeline on SolO or Wind to test radial
  persistence.
- **Tension.** Transition-range steepening is also predicted by
  ion-cyclotron-resonant absorption ([[bowen-2024-extended-cyclotron-resonant-heating]])
  and by KAW physics ([[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]]).
  Same PSP intervals should be analysed through all three lenses to
  distinguish which prediction co-varies uniquely with (β_p, |σ_c|).
- **Composable experiment.** Couple the (β_p, |σ_c|, transition-range-
  shape) catalogue to
  [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]]'s stream-
  origin annotation — testing whether the barrier signature is uniform
  across stream classes once (β_p, |σ_c|) are matched.

## 10. Relation to HelioSI corpus

- Parent sub-graph: `wave500_turbulence_intermit_heating_045` (ion-scale,
  helicity-barrier, imbalance).
- Sibling paper-skills:
  [[paper-sasmal-2026-helicity-barrier-flr-mhd-heating]],
  [[bowen-2024-extended-cyclotron-resonant-heating]],
  [[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]],
  [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]].
- Required capabilities (not bound here): PSP MAG+SWEAP reader,
  spectrum-shape diagnostic near the ion gyroradius, β_p calculator, σ_c
  diagnostic, (β_p, |σ_c|)-stratified aggregator, helicity-barrier theory
  reference.
