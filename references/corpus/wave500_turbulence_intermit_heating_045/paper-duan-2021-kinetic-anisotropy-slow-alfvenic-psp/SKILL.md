---
name: paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp
description: >-
  Use when characterising sub-ion (kinetic-Alfven-wave) anisotropy in
  slow-Alfvenic PSP intervals via wavelet trace/component spectra and the
  magnetic compressibility test — Duan et al. 2021 (ApJL 915, L8) recover
  KAW-consistent perpendicular cascade scaling at first PSP perihelion
  (~0.17 au, 2018 November 5–7).
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
  title: "Anisotropy of Solar-Wind Turbulence in the Inner Heliosphere at Kinetic Scales: PSP Observations"
  first_author: "Duan, D."
  authors:
    - "Die Duan"
    - "Jiansen He"
    - "Trevor A. Bowen"
    - "Lloyd D. Woodham"
    - "Tieyan Wang"
    - "Christopher H. K. Chen"
    - "Alfred Mallet"
    - "Stuart D. Bale"
  year: 2021
  venue: "Astrophysical Journal Letters 915, L8"
  doi: "10.3847/2041-8213/ac07ac"
  arxiv_id: "2102.13294"
  ads_bibcode: "2021ApJ...915L...8D"
domain:
  primary_theme: turbulence
  secondary_themes: [anisotropy, kinetic-scale, KAW, waves_instabilities]
  missions: [PSP]
  regime: [inner-heliosphere, ion-scale, kinetic, sub-ion]
trigger_keywords:
  - "kinetic-scale anisotropy"
  - "kinetic Alfven wave KAW"
  - "magnetic compressibility"
  - "wavelet spectrum PSP"
  - "slow Alfvenic wind"
  - "angle-binned spectrum"
  - "sub-ion cascade"
  - "transition range"
  - "Duan He Bowen Woodham 2021"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "burst (high-rate, sub-ion resolved)", interval: "PSP E1 first perihelion, 2018 November 5–7 statistical window; detail 2018-11-06 14:30–15:30 UT", archive: "CDAWeb / PSP SOC"}
algorithms:
  - name: "Wavelet trace and component (parallel/perpendicular) PSD"
    equation_refs: ["paper §2 wavelet method"]
  - name: "Magnetic compressibility C|| = δB||² / δB_tot²"
    equation_refs: ["paper §3 KAW diagnostic"]
  - name: "Local mean-field projection (scale-dependent) for theta_kB binning"
    equation_refs: ["paper §2"]
  - name: "Per-angle-bin power-law fit on transition and kinetic ranges"
    equation_refs: ["paper §3, Table 1 / Fig. spectral-index summary"]
validation_targets:
  - "Transition-range spectral indices: alpha_t_parallel = -5.7 ± 1.0, alpha_t_perp = -3.7 ± 0.3."
  - "Kinetic-range spectral indices: alpha_k_parallel = -3.12 ± 0.22, alpha_k_perp = -2.57 ± 0.09."
  - "Wavevector anisotropy scaling: k_parallel ~ k_perp^{0.71 ± 0.17} (transition), k_parallel ~ k_perp^{0.38 ± 0.09} (kinetic)."
  - "Power anisotropy P_perp/P_parallel > 10 in the kinetic range, exceeding the transition-range value and exceeding 1 au comparators."
  - "Magnetic compressibility C|| follows the linear-Vlasov KAW prediction below the ion break (qualitative match)."
links:
  doi_url: "https://doi.org/10.3847/2041-8213/ac07ac"
  arxiv_url: "https://arxiv.org/abs/2102.13294"
  ads_url: "https://ui.adsabs.harvard.edu/abs/2021ApJ...915L...8D"
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/ (PSP FIELDS L2)"
claim_boundary:
  scope: >-
    In the slow (V_SW < 400 km/s) but highly Alfvénic PSP E1 perihelion
    interval (~0.17 au, 2018 November 5–7), sub-ion magnetic-field
    fluctuations exhibit (i) perpendicular-to-mean-field power
    anisotropy with P_perp/P_parallel > 10 in the kinetic range,
    (ii) a distinct steepened "transition range" between inertial and
    kinetic ranges in all theta_kB bins, and (iii) magnetic
    compressibility consistent with kinetic-Alfven-wave (KAW)
    turbulence below the ion break.
  out_of_scope:
    - "Do not extrapolate to fast (>400 km/s) or non-Alfvenic streams without re-running the angle binning — the claim is conditioned on slow-Alfvenic wind."
    - "Do not extend the KAW interpretation past the electron break or to scales where instrument noise dominates."
    - "Do not equate magnetic compressibility level with branch identification (KAW vs whistler) without an explicit linear-Vlasov comparison; the paper offers a consistency check, not a uniqueness proof."
    - "Encounters E2+ are NOT covered; do not generalize the kinetic-range exponents to later encounters without re-fitting."
failure_modes:
  - "Spacecraft spin-tone in MAG can mimic perpendicular power if not despun (PSP rolls/quasi-sun-pointing must be subtracted)."
  - "Local-mean-field direction estimator (scale-dependent vs window-mean) shifts theta_kB binning and changes the recovered exponents — use the same estimator the paper uses (scale-dependent local mean)."
  - "Sample-size collapse at large theta_kB (>~75 deg) inflates slope error bars; report bin occupancy."
  - "Burst-mode duty cycle creates window-selection bias; report fraction of perihelion covered by burst windows."
  - "Taylor-hypothesis breakdown at sub-ion scales when V_A approaches V_SW near perihelion can bias k-mapping; sanity-check k_di vs f conversion."
  - "Magnetic compressibility is a necessary but not sufficient KAW signature; whistler turbulence at very oblique propagation can mimic part of the C|| signal."
depends_on:
  - zhao-2022-3d-anisotropy-kinetic-scales-psp
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Claim is bound to the slow-Alfvenic E1 sample. No sibling skill yet covers fast streams or later encounters where the local-mean-field excursions are stronger."
    proposed_action: "Re-run the angle-binned exponent fit on E1 fast-wind windows and on E2–E5 perihelia using the same scale-dependent local-mean-field estimator."
  - type: hypothesis
    statement: "If KAW interpretation holds, magnetic-compressibility C|| at the ion break should match the linear-Vlasov KAW prediction at the locally-measured beta_p and theta_kB within a defined tolerance — disagreement would indicate a non-negligible whistler or Hall-MHD contribution."
    proposed_action: "Compute C|| over PSP E1 burst windows and overplot the linear-Vlasov KAW dispersion solution evaluated at the measured (beta_p, theta_kB); deviation > 20 % flags the failure case."
  - type: tension
    statement: "Kinetic-range P_perp/P_parallel > 10 at 0.17 au exceeds 1 au observations — but radial evolution of the anisotropy ratio is undersampled. The radial trend between 0.17 and 1 au is an open question."
    proposed_action: "Run the same Duan-pipeline on Helios + WIND legacy intervals (sub-ion-resolved bursts) to construct a P_perp/P_parallel vs r curve."
  - type: composable_experiment
    statement: "Couple the per-angle-bin exponent table to a cascade-rate skill (e.g. [[paper-andres-2021-incompressible-cascade-anisotropic-pp]]) — testing whether the 2D-dominated MHD-scale geometry and the KAW-consistent sub-ion anisotropy share a common radial trend isolates whether 'KAW-ness' is set by the upstream cascade or by local kinetic physics."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2021 item 5"
  verified_by: "internalization-batch 2026-05-19 (arXiv 2102.13294 abstract + IOPscience DOI page)"
  verified_at: "2026-05-19T00:00:00Z"
  verification_notes:
    - "field=doi value=10.3847/2041-8213/ac07ac source=IOPscience-landing verified_at=2026-05-19"
    - "field=venue value=ApJL-915-L8 source=IOPscience-landing verified_at=2026-05-19"
    - "field=arxiv_id value=2102.13294 source=arXiv-abs-page verified_at=2026-05-19"
tags: [heliophysics, paper-skill, turbulence, kinetic, KAW, sub-ion, transition-range]
---

# Duan et al. 2021 — kinetic-scale anisotropy in slow-Alfvenic PSP wind — paper-skill

> Compiled from arXiv:2102.13294 = ApJL 915, L8 (DOI 10.3847/2041-8213/ac07ac).
> `paper-grounded-pending-full-text` tier — bibliographic anchors, the headline
> spectral-index numbers, and the anisotropy-scaling exponents are verified
> from the abstract and the IOPscience landing page. Sub-fit details (e.g.
> exact k-range used for each per-angle-bin fit, table of per-bin slope vs
> theta_kB) remain pending full-text verification.

## 1. Trigger  *(Layer 1)*

Use when:

- measuring sub-ion (k d_i > 1) magnetic-field anisotropy in slow-Alfvenic PSP
  intervals;
- distinguishing the KAW vs whistler branch via magnetic compressibility C||;
- characterising the **transition range** between MHD and kinetic ranges in
  PSP perihelion data — this paper explicitly resolves a steepened
  transition-range slope in all theta_kB directions, separate from the kinetic
  range proper.

Do NOT use for fast non-Alfvenic streams, for electron-scale physics beyond
the resolved range, or to claim a definitive branch identification without a
companion linear-Vlasov check (this paper is a consistency test, not a
uniqueness proof).

## 2. Paper claim → narrow verifiable task

**Verified claim (abstract + IOPscience landing, 2026-05-19).** In the slow
(V_SW < 400 km/s) but highly Alfvénic PSP first-perihelion interval
(~0.17 au, statistical window 2018 November 5–7; example detail window
2018-11-06 14:30–15:30 UT), magnetic-field fluctuations in the transition and
kinetic ranges are strongly anisotropic with P_perp/P_parallel > 10 in the
kinetic range, the spectral indices in each range scale-bin and direction-bin
take the verified values listed in the validation targets, and magnetic
compressibility below the ion break is consistent with kinetic-Alfven-wave
turbulence.

**Narrow verifiable task.** Reproduction succeeds when an agent, given the
above PSP E1 burst-mode interval, recovers:

1. transition-range slopes alpha_t_parallel ≈ -5.7 ± 1.0 and alpha_t_perp ≈
   -3.7 ± 0.3 within the paper's stated uncertainty;
2. kinetic-range slopes alpha_k_parallel ≈ -3.12 ± 0.22 and alpha_k_perp ≈
   -2.57 ± 0.09;
3. wavevector-anisotropy scaling exponents 0.71 ± 0.17 (transition) and
   0.38 ± 0.09 (kinetic);
4. P_perp/P_parallel > 10 in the kinetic range and stronger than published
   1 au comparators;
5. C||(k d_i) qualitatively matching the linear-Vlasov KAW prediction below
   the ion break.

## 3. Executable protocol (Layer 2 — abstract capabilities)

The skill requires the following abstract capabilities (Layer-2 contracts —
no bound adapter names):

1. **High-cadence MAG reader.** Returns despun B(t) in RTN (or instrument
   frame) at burst-mode cadence covering sub-ion frequencies; must support
   bad-block masking.
2. **Wavelet PSD with directional decomposition.** Produces trace power and
   parallel/perpendicular component power as a function of frequency, with a
   scale-dependent **local mean-field** estimator B_0(t, scale).
3. **theta_kB binning.** Bins each (t, scale) point into angle bins relative
   to B_0(t, scale); returns per-bin PSD curves with explicit occupancy.
4. **Per-bin power-law fitter.** Fits PSD(f) ∝ f^alpha over a frequency
   window using a scale-bounded least-squares (or robust) fit, with error
   estimation from the per-bin sample count.
5. **Magnetic compressibility C||.** Computes C||(f) = P_||(f) / P_tot(f) in
   the local mean-field frame, sub-sampled to the kinetic range.
6. **Linear-Vlasov KAW reference (optional comparator).** Solves the linear
   dispersion at the locally measured (beta_p, theta_kB) and returns the
   predicted C||(k d_i) curve for the KAW branch.

Abstract procedure:

1. Identify the slow-Alfvenic E1 interval (V_SW < 400 km/s, sigma_c > a
   chosen threshold — paper uses E1 perihelion).
2. Read PSP FIELDS MAG burst windows covering the interval.
3. Compute scale-dependent local mean field B_0(t, scale) and wavelet trace +
   component spectra.
4. Bin (t, scale) by theta_kB; require minimum bin occupancy before fitting.
5. Fit alpha_t and alpha_k in the transition and kinetic ranges respectively,
   in each theta_kB bin.
6. Compute k_parallel(k_perp) scaling from the per-bin spectra.
7. Compute C||(k d_i); overlay linear-Vlasov KAW prediction.
8. Acceptance: match the five verified target items above within stated
   tolerances.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability required |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst (sub-ion resolved) | PSP E1, ~2018-11-05 to 2018-11-07 (statistical); detail 2018-11-06 14:30–15:30 UT | CDAWeb / PSP SOC | high-cadence vector MAG reader with despin |
| PSP/SWEAP ion moments (optional) | L3 | as available | same interval | CDAWeb | proton n_p, V_SW, T_p, beta_p for Alfvenicity gating and Vlasov input |

## 5. Validation target

**Primary numeric targets (verified at abstract level).**

- Transition range: alpha_t_parallel = -5.7 ± 1.0; alpha_t_perp = -3.7 ± 0.3.
- Kinetic range: alpha_k_parallel = -3.12 ± 0.22; alpha_k_perp = -2.57 ± 0.09.
- Wavevector anisotropy: k_parallel ~ k_perp^{0.71 ± 0.17} (transition);
  k_parallel ~ k_perp^{0.38 ± 0.09} (kinetic).
- Power anisotropy: P_perp / P_parallel > 10 in the kinetic range, exceeding
  transition-range and 1 au values.
- C|| qualitatively consistent with linear-Vlasov KAW below the ion break.

**Tolerance budget.** Any of the listed exponents disagreeing by more than the
stated 1σ on the paper's own interval flags a likely pipeline disagreement
(wrong mean-field estimator, wrong frequency window, insufficient bin
occupancy). Exact per-bin slope values and the precise frequency windows used
for each fit are **pending full-text verification**.

## 6. Failure modes (load-bearing)

- **Spin-tone contamination.** PSP FIELDS spin tones can leak into
  perpendicular power if despin is incomplete; verify the residual spin-tone
  line is below the kinetic-range fit window.
- **Local-mean-field estimator drift.** Using a window-mean B_0 instead of the
  scale-dependent estimator can compress theta_kB toward the median angle
  and bias alpha_perp upward; the paper's claim is conditioned on
  *scale-dependent* B_0.
- **Bin-occupancy collapse.** Extreme theta_kB bins (>~75 deg) can collapse
  in sample size during a short burst, inflating slope error bars beyond the
  reported ±0.1 magnitude.
- **Burst-mode duty cycle bias.** Burst windows are not uniformly distributed
  in the stream; report the fraction of perihelion covered and check for
  selection effects on V_SW and sigma_c.
- **Taylor-hypothesis breakdown.** Near perihelion, V_A can approach V_SW,
  invalidating the simple f → k_perp V_SW / 2π mapping; the paper's
  k_parallel(k_perp) recovery depends on this — sanity-check by recomputing
  with V_eff = sqrt(V_SW^2 + V_A^2).
- **Branch ambiguity.** C|| consistency is necessary but not sufficient for
  KAW identification; the paper does not exclude oblique whistler or
  KAW/whistler hybrid contributions.

## 7. Claim boundary

**In scope.** Sub-ion magnetic-field anisotropy in slow (<400 km/s) but
highly Alfvénic PSP E1 perihelion wind (~0.17 au), with explicit resolution
of a transition range separate from the kinetic range.

**Out of scope.** Fast (>400 km/s) or non-Alfvenic streams (no re-binning
performed); encounters E2 and beyond; electron-scale dynamics; definitive
branch identification (KAW vs whistler) without independent Vlasov support.

## 8. Links and identifiers

- DOI: <https://doi.org/10.3847/2041-8213/ac07ac> (ApJL 915, L8 — IOPscience
  landing verified 2026-05-19).
- arXiv: <https://arxiv.org/abs/2102.13294> (preprint title matches journal
  title; verified 2026-05-19).
- ADS: <https://ui.adsabs.harvard.edu/abs/2021ApJ...915L...8D> (bibcode
  follows ApJL 915 L8 D pattern; not independently verified via ADS UI which
  is JS-rendered).
- Data: PSP/FIELDS L2 burst-mode MAG via CDAWeb.

## 9. Skill graph + Layer-4 affordances

Depends on [[zhao-2022-3d-anisotropy-kinetic-scales-psp]] (3D extension of the
angle-binned method used here in 1D-of-angle).

- **Gap.** The verified claim is bound to slow-Alfvenic E1. No sibling skill
  yet covers fast streams or later encounters where the local-mean-field
  excursions are larger and the burst duty cycle is different.
- **Hypothesis (testable).** If the KAW interpretation is correct, the
  measured C||(k d_i) should fall within tolerance of the linear-Vlasov KAW
  prediction evaluated at the measured (beta_p, theta_kB). A deviation > 20 %
  at scales 1 < k d_i < 10 would flag a whistler/Hall-MHD contribution.
- **Tension.** Kinetic-range P_perp/P_parallel > 10 at 0.17 au is stronger
  than 1 au comparators, but radial coverage between 0.17 and 1 au is
  undersampled by this paper.
- **Composable experiment.** Couple the per-angle-bin exponent table to a
  cascade-rate skill — e.g.
  [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] — testing
  whether the 2D-dominated MHD-scale geometry and the KAW-consistent sub-ion
  anisotropy share a common radial trend isolates whether "KAW-ness" at
  sub-ion scales is set by the upstream cascade or by local kinetic physics.

## 10. Relation to HelioSI corpus

- Parent sub-graph: `wave500_turbulence_intermit_heating_045` (kinetic-scale
  cascade and dissipation).
- Sibling paper-skills: [[zhao-2022-3d-anisotropy-kinetic-scales-psp]] (3D
  generalisation), [[paper-andres-2021-incompressible-cascade-anisotropic-pp]]
  (cascade-rate anisotropy on overlapping PSP intervals),
  [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]] (provides the
  Alfvenicity stratification this paper conditions on).
- Required capabilities (not bound here): high-cadence MAG reader,
  scale-dependent local-mean-field estimator, wavelet PSD with directional
  decomposition, per-angle-bin power-law fitter, linear-Vlasov solver
  (optional).
