---
name: paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution
description: >-
  Use when comparing Alfvénic vs non-Alfvénic turbulence in the inner
  heliosphere using PSP first-five-orbit (E1–E5) data and tracking how
  fluctuation properties (magnetic / velocity spectra, outward-wave
  dominance, magnetic excess) evolve with radial distance, stream speed,
  and large-scale context — Shi, Velli, Panasenco, Tenerani, Réville et al.
  2021 (A&A 650, A21).
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
  title: "Alfvénic versus non-Alfvénic turbulence in the inner heliosphere as observed by Parker Solar Probe"
  first_author: "Shi, C."
  authors:
    - "Chen Shi"
    - "Marco Velli"
    - "Olga Panasenco"
    - "Anna Tenerani"
    - "Victor Réville"
    - "Stuart D. Bale"
    - "Justin Kasper"
    - "Kelly Korreck"
    - "J. W. Bonnell"
    - "Thierry Dudok de Wit"
    - "David M. Malaspina"
    - "Keith Goetz"
    - "Peter R. Harvey"
    - "Robert J. MacDowall"
    - "Marc Pulupa"
    - "Anthony W. Case"
    - "Davin Larson"
    - "J. L. Verniero"
    - "Roberto Livi"
    - "Michael Stevens"
    - "Phyllis Whittlesey"
    - "Milan Maksimovic"
    - "Michel Moncuquet"
  year: 2021
  venue: "Astronomy & Astrophysics 650, A21"
  doi: "10.1051/0004-6361/202039818"
  arxiv_id: "2101.00830"
  ads_bibcode: "2021A&A...650A..21S"
domain:
  primary_theme: turbulence
  secondary_themes: [alfvenic, classification, radial-evolution, stream-origin, current-sheets, velocity-shears]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "Alfvenicity classification"
  - "normalised cross helicity sigma_c"
  - "residual energy sigma_R"
  - "PSP E1-E5 statistics"
  - "spectral index radial evolution"
  - "expansion-driven turbulence"
  - "turbulence age"
  - "outward wave dominance"
  - "magnetic excess"
  - "stream origin coronal hole vs active region"
  - "heliospheric current sheet velocity shear"
  - "Shi Velli Panasenco Tenerani 2021"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s (resampled)", interval: "PSP E1–E5 (first five orbits, ~2018-10 to 2020-09)", archive: "CDAWeb / PSP SOC"}
  - {instrument: "PSP/SWEAP SPC", level: "L3", cadence: "~1 Hz", interval: "E1–E5", archive: "CDAWeb / PSP SOC"}
algorithms:
  - name: "Alfvenicity diagnostics: normalised cross helicity σ_c, residual energy σ_R"
    equation_refs: ["paper §2 Alfvenicity definitions"]
  - name: "Trace magnetic / velocity power spectra and inertial-range slopes"
    equation_refs: ["paper §3 spectra and slopes"]
  - name: "Turbulence age T_age proxy ~ r / V_SW (or related Elsasser-amplitude-evolution proxy)"
    equation_refs: ["paper §3 turbulence-age framing"]
  - name: "Radial-distance binning and stream-class stratification"
    equation_refs: ["paper §3 radial binning"]
  - name: "Stream-origin annotation (coronal hole vs active region / pseudostreamer)"
    equation_refs: ["paper §4 stream-origin context"]
  - name: "Large-scale structure annotation (HCS crossings, velocity shears)"
    equation_refs: ["paper §5 structure-driven modulation"]
validation_targets:
  - "PSP E1–E5 are the supported coverage; conclusions are restricted to ~0.17–0.7 au coverage of these orbits."
  - "Magnetic-field power spectrum steepens with outward transport; velocity spectrum shape remains essentially unchanged (abstract-level verified)."
  - "Spectral steepening rate is controlled by turbulence 'age' (a combined function of wind speed and radial distance), not by radial distance alone (abstract-level verified)."
  - "Faster solar wind statistically exhibits higher Alfvenicity (more outward-wave dominance, more balanced magnetic/kinetic energy) (abstract-level)."
  - "Outward-wave dominance weakens with increasing radial distance; magnetic-energy excess grows toward the Sun (abstract-level)."
  - "Stream-to-stream variability is significant even at similar bulk speeds — origin matters (abstract-level)."
  - "Slow wind originating near polar coronal holes has lower Alfvenicity than slow wind originating from active regions / pseudostreamers (abstract-level)."
  - "HCS crossings and velocity shears measurably modify turbulence properties (abstract-level)."
links:
  doi_url: "https://doi.org/10.1051/0004-6361/202039818"
  arxiv_url: "https://arxiv.org/abs/2101.00830"
  ads_url: "https://ui.adsabs.harvard.edu/abs/2021A%26A...650A..21S"
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/ (PSP FIELDS + SWEAP)"
claim_boundary:
  scope: >-
    Across PSP encounters 1–5, MHD-scale turbulence properties depend
    measurably on (i) Alfvenicity (σ_c, σ_R), (ii) heliocentric distance
    via a turbulence-age control parameter that combines r and V_SW,
    (iii) stream origin (polar coronal-hole vs active-region /
    pseudostreamer), and (iv) co-located large-scale structures (HCS,
    velocity shears). The magnetic spectrum steepens outward while the
    velocity spectrum shape is roughly preserved.
  out_of_scope:
    - "Do not generalise the (σ_c, σ_R) classification cuts to ML-style segmentation without re-validating class boundaries (the paper uses analytic thresholds, not a learned classifier)."
    - "Do not export the inertial-range slope conclusions into kinetic scales — the analysis is MHD-scale."
    - "Do not extend the radial-evolution trend to encounters E6+ (closer perihelia, sub-Alfvenic excursions) without re-fitting."
    - "Do not interpret 'turbulence age' as a calibrated radiative-transfer-style parameter; it is a phenomenological combination of (r, V_SW) used to collapse the radial trend."
failure_modes:
  - "σ_c / σ_R values depend on the integration window τ_int chosen — different τ_int yields different class assignments; document and report sensitivity."
  - "Stream-overlap intervals (mixed Alfvenicity, e.g. CIRs, fast/slow boundaries) inflate within-class variance; isolate and flag them rather than averaging across the boundary."
  - "Heliospheric current-sheet crossings flip σ_c sign; treat them as separate sub-intervals."
  - "Compressive sub-intervals (large δn/n) violate the pure-Alfvenic interpretation; pre-filter or report compressibility."
  - "Velocity-shear crossings can both inject and modify Alfvenicity locally; co-locate ML-style segmentation outputs with the (σ_c, σ_R) thresholds before drawing causal arrows."
  - "Stream-origin labels (coronal hole vs active region vs pseudostreamer) carry observational uncertainty (back-mapping margin); inherit that uncertainty into the per-class statistics."
  - "Velocity-spectrum estimates from SPC are noisier than magnetic-spectrum estimates from FIELDS; the 'velocity spectrum shape unchanged' claim is conditioned on SPC's noise floor."
depends_on:
  - damicis-2021-alfvenic-nonalfvenic-psp
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Distance/orbital coverage is bound to E1–E5 (~0.17–0.7 au); no sibling skill yet covers later encounters where PSP enters the sub-Alfvenic regime (E14+)."
    related_skills: [paper-adhikari-2025-trans-alfvenic-turbulence]
    proposed_action: "Replicate the (σ_c, σ_R)-stratified spectral-slope vs turbulence-age pipeline on PSP E10–E18 and overlay on the E1–E5 trend."
  - type: hypothesis
    statement: "If 'turbulence age' is the correct collapsing variable, plotting magnetic-spectrum slope vs T_age = r / V_SW (or the paper's exact functional form) should yield a one-parameter family that absorbs the radial trend across stream classes — including the active-region-originated slow streams."
    proposed_action: "Compute T_age for every E1–E5 interval, plot slope vs T_age, and test for a single-curve collapse vs a class-separated family."
  - type: tension
    statement: "[[damicis-2021-alfvenic-nonalfvenic-psp]] uses thresholds derived from earlier PSP encounters; Shi 2021 statistically partitions over a broader range. If both pipelines agree on the binary class assignments, the (σ_c, σ_R) thresholds are stable; if they disagree, the binary boundary itself is fragile and may need a 3-class or continuous-axis representation."
    proposed_action: "Cross-run both Alfvenicity classifiers on a common interval set and report the confusion matrix."
  - type: composable_experiment
    statement: "Couple the (σ_c, σ_R, T_age, stream-origin) stratification produced by this paper to (i) the cascade-rate decomposition in [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] and (ii) the sub-ion-scale anisotropy in [[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]] — testing whether the radial spectral steepening tracks the upstream cascade rate or the kinetic-scale dissipation."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2021 item 4"
  verified_by: "internalization-batch 2026-05-19 (arXiv 2101.00830 + A&A landing 650 A21)"
  verified_at: "2026-05-19T00:00:00Z"
  verification_notes:
    - "field=doi value=10.1051/0004-6361/202039818 source=A-and-A-landing-650-A21 verified_at=2026-05-19"
    - "field=venue value=A-and-A-650-A21-2021 source=A-and-A-landing verified_at=2026-05-19"
    - "field=arxiv_id value=2101.00830 source=arXiv-abs-page verified_at=2026-05-19"
    - "field=author_list value=full-23-author-list-restored source=arXiv-abs-page verified_at=2026-05-19"
tags: [heliophysics, paper-skill, turbulence, alfvenic, radial-evolution, stream-origin]
---

# Shi et al. 2021 — Alfvénic vs non-Alfvénic radial evolution in PSP E1–E5 — paper-skill

> Compiled from arXiv:2101.00830 = A&A 650, A21 (DOI 10.1051/0004-6361/202039818).
> `paper-grounded-pending-full-text` tier — bibliographic anchors, the E1–E5
> coverage, and the seven qualitative claims listed in `validation_targets`
> are verified at abstract level from the publisher landing and the arXiv
> abstract. Specific (σ_c, σ_R) threshold values, the exact T_age functional
> form, and per-stream-class spectral-slope numbers are pending full-text
> verification.

## 1. Trigger  *(Layer 1)*

Use when:

- partitioning PSP E1–E5 intervals by Alfvenicity (σ_c, σ_R);
- testing whether the inertial-range *magnetic* spectrum steepens with radial
  distance while the *velocity* spectrum shape is preserved;
- collapsing the radial trend onto a turbulence-age control parameter
  combining r and V_SW;
- annotating turbulence properties by *stream origin* (polar coronal hole vs
  active region / pseudostreamer);
- attributing localised turbulence modifications to large-scale structures
  (HCS, velocity shears) rather than to bulk radial expansion alone.

Do NOT use this skill to (a) draw kinetic-scale conclusions (it is MHD-scale),
(b) treat the (σ_c, σ_R) cuts as ML-cluster boundaries, (c) extrapolate to
PSP encounters beyond E5 without re-fitting, or (d) interpret 'turbulence
age' as a calibrated radiative-transfer-style parameter.

## 2. Paper claim → narrow verifiable task

**Verified claim (abstract + A&A landing, 2026-05-19).** Across PSP encounters
1–5 (first five orbits), magnetic-field power spectra steepen with outward
transport while velocity-spectrum shapes remain essentially unchanged. The
steepening rate is controlled by a 'turbulence age' that combines V_SW and
r, not r alone. Faster wind is statistically more Alfvénic; outward-wave
dominance weakens with r; magnetic-energy excess grows toward the Sun.
Stream origin (coronal hole vs active region / pseudostreamer) modifies
Alfvenicity *at similar bulk speeds*. HCS crossings and velocity shears
measurably modify turbulence properties.

**Narrow verifiable task.** Reproduction succeeds when an agent, on a PSP
E1–E5 interval set:

1. computes (σ_c, σ_R) per interval with a documented integration window;
2. computes trace magnetic and velocity power spectra and the inertial-range
   slopes;
3. recovers magnetic-slope steepening with r and unchanged velocity-spectrum
   shape;
4. demonstrates that magnetic slope collapses onto a turbulence-age axis;
5. recovers higher Alfvenicity in faster wind statistically;
6. recovers stream-origin dependence at similar bulk speeds;
7. flags HCS / velocity-shear sub-intervals as separate sub-populations and
   shows that within-class statistics shift when they are isolated.

## 3. Executable protocol (Layer 2 — abstract capabilities)

The skill requires the following abstract capabilities:

1. **PSP MAG + ion-moment reader.** Returns B(t), V(t), n_p(t), T_p(t)
   covering E1–E5 in a common cadence; supports despin and bad-block masks.
2. **Alfvenicity diagnostics.** σ_c(τ_int), σ_R(τ_int) per interval, with
   explicit τ_int reporting.
3. **Trace PSD + inertial-range slope fitter.** Per-interval magnetic and
   velocity trace PSDs and a robust inertial-range slope fitter; report fit
   window per interval.
4. **Turbulence-age constructor.** Computes T_age (or the paper's exact
   functional form combining r and V_SW); allows alternative definitions to
   be plugged in.
5. **Stream-origin annotator.** Labels intervals by coronal-hole / active-
   region / pseudostreamer origin; inherits back-mapping uncertainty as a
   per-interval confidence flag.
6. **Large-scale structure annotator.** Flags HCS crossings and velocity-
   shear regions; treats them as separate sub-intervals in downstream
   aggregation.
7. **Radial / class aggregator.** Bins per-interval results by (r, Alfvenicity
   class, stream origin) and produces the slope-vs-r and slope-vs-T_age
   curves.

Abstract procedure:

1. Build the E1–E5 interval list; document the interval-segmentation rule
   (e.g. stationarity over a target window).
2. Compute (σ_c, σ_R) per interval; classify by analytic thresholds.
3. Compute trace magnetic + velocity PSDs and fit slopes.
4. Annotate intervals with stream origin and large-scale structures.
5. Compute T_age per interval.
6. Aggregate slope vs r, slope vs T_age, σ_c vs (V_SW, r), σ_c vs
   stream origin.
7. Acceptance: reproduce the seven qualitative claims in §2.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability required |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s (after resample) | E1–E5 | CDAWeb / PSP SOC | high-cadence vector MAG reader with despin |
| PSP/SWEAP SPC | L3 | ~1 Hz | E1–E5 (SPC was the primary moments source through E5) | CDAWeb / PSP SOC | proton moments reader (n_p, V, T_p) |

## 5. Validation target

**Primary qualitative targets (verified at abstract level).**

- Magnetic-spectrum steepening with radial distance; velocity-spectrum shape
  unchanged.
- Turbulence-age collapse of the magnetic-slope radial trend.
- Faster wind statistically more Alfvénic.
- Outward-wave dominance weakens with r; magnetic-energy excess grows toward
  the Sun.
- Stream-origin dependence at similar bulk speeds (coronal-hole-origin slow
  wind less Alfvénic than active-region-origin slow wind).
- HCS / velocity-shear modulation of turbulence properties.

**Tolerance budget.** Slope-vs-r and slope-vs-T_age numerical values, exact
(σ_c, σ_R) class-threshold values, and per-class slope numbers are **pending
full-text verification**. Sign reversal of any of the qualitative claims at
the per-bin level is a pipeline-disagreement flag.

## 6. Failure modes (load-bearing)

- **σ_c, σ_R window dependence.** Class assignment changes with τ_int; the
  paper's class boundary is conditioned on a specific τ_int that must be
  reproduced.
- **Stream-overlap intervals.** CIRs and fast/slow boundaries inflate
  within-class variance; isolate and flag rather than averaging across.
- **HCS sign flips.** σ_c sign reverses across an HCS crossing; aggregating
  across the crossing without isolating reduces apparent Alfvenicity.
- **Compressive contamination.** Pure-Alfvenic interpretation requires
  δn/n below some threshold; pre-filter or report compressibility.
- **Velocity-shear injection.** Shears can both inject and modify
  Alfvenicity locally; co-locating ML-segmentation outputs with the
  thresholds avoids attributing local injection to bulk radial trends.
- **Stream-origin back-mapping uncertainty.** Origin labels carry margin;
  inherit it into per-class statistics rather than treating origin as a
  certain label.
- **SPC velocity-spectrum noise floor.** The 'velocity spectrum shape
  unchanged' claim is conditioned on SPC's noise floor; harder to extend to
  intervals where SPC noise dominates the slope window.

## 7. Claim boundary

**In scope.** PSP E1–E5 (~2018-10 to 2020-09 timeframe, distances roughly
0.17–0.7 au) MHD-scale Alfvenicity classification, magnetic-spectrum
steepening, velocity-spectrum-shape preservation, turbulence-age control of
the radial trend, stream-origin dependence, and HCS / velocity-shear
modulation.

**Out of scope.** Encounters E6+, sub-Alfvenic excursions, kinetic-scale
spectra, ML-cluster-style segmentation, single-encounter detail studies, and
treating turbulence age as a calibrated parameter.

## 8. Links and identifiers

- DOI: <https://doi.org/10.1051/0004-6361/202039818> (A&A 650, A21 —
  verified 2026-05-19 from A&A landing).
- arXiv: <https://arxiv.org/abs/2101.00830> (full 23-author list verified
  2026-05-19).
- ADS: <https://ui.adsabs.harvard.edu/abs/2021A%26A...650A..21S> (bibcode
  follows A&A 650 A21 pattern; not independently verified via ADS UI).

## 9. Skill graph + Layer-4 affordances

Depends on [[damicis-2021-alfvenic-nonalfvenic-psp]] (a complementary
Alfvenicity-classification skill on overlapping PSP intervals).

- **Gap.** Distance coverage is bound to E1–E5. Replicating the pipeline on
  E10+ (closer perihelia, sub-Alfvenic excursions) would extend the trend
  through the radial range covered by
  [[paper-adhikari-2025-trans-alfvenic-turbulence]].
- **Hypothesis (testable).** If 'turbulence age' is the correct collapsing
  variable, magnetic-slope vs T_age should yield a single one-parameter
  family that absorbs the radial trend across stream classes, including
  active-region-originated slow streams.
- **Tension.** The (σ_c, σ_R) class assignments produced by this pipeline
  should be compared to [[damicis-2021-alfvenic-nonalfvenic-psp]] on a
  shared interval set — disagreement would indicate that the binary
  boundary is fragile and a continuous-axis representation is needed.
- **Composable experiment.** Stratify cascade-rate
  ([[paper-andres-2021-incompressible-cascade-anisotropic-pp]]) and sub-ion
  anisotropy
  ([[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]]) by the
  (σ_c, σ_R, T_age, stream-origin) tuple from this paper to test whether the
  radial spectral steepening tracks the upstream cascade rate or the
  kinetic-scale dissipation signature.

## 10. Relation to HelioSI corpus

- Parent sub-graph: `wave500_turbulence_intermit_heating_045` (Alfvenicity,
  radial evolution, stream-origin context).
- Sibling paper-skills:
  [[damicis-2021-alfvenic-nonalfvenic-psp]] (overlapping classification),
  [[paper-adhikari-2025-trans-alfvenic-turbulence]] (later-encounter
  trans-Alfvenic regime),
  [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] (cascade-rate
  composable experiment),
  [[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]] (sub-ion-scale
  KAW signature that this skill's Alfvenicity stratification conditions).
- Required capabilities (not bound here): PSP MAG+SWEAP reader, Alfvenicity
  diagnostics, trace PSD + slope fitter, turbulence-age constructor, stream-
  origin annotator, large-scale-structure annotator, class-binned aggregator.
