---
name: paper-andres-2021-incompressible-cascade-anisotropic-pp
description: >-
  Use when applying the Politano-Pouquet exact third-order relation on PSP
  MAG+SWEAP data and decomposing the incompressible MHD cascade rate into
  parallel and perpendicular components relative to the local mean field —
  Andrés, Sahraoui, Huang, Hadid & Galtier 2022 survey >2 yr of PSP data
  spanning 0.2–0.8 au and report perpendicular-cascade dominance approaching
  the Sun and 2D-cascade dominance over slab in slow wind.
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
  title: "The incompressible energy cascade rate in anisotropic solar wind turbulence"
  first_author: "Andrés, N."
  authors:
    - "N. Andrés"
    - "F. Sahraoui"
    - "S. Huang"
    - "L. Z. Hadid"
    - "S. Galtier"
  year: 2022
  venue: "Astronomy & Astrophysics 661, A116"
  doi: "10.1051/0004-6361/202142994"
  arxiv_id: "2112.13748"
  ads_bibcode: "2022A&A...661A.116A"
  identity_uncertainty: >-
    Slug name 'andres-2021-...' inherits the arXiv-submission year (Dec 2021)
    but the paper was published in A&A in 2022. The 'paper.year' field is the
    publication year (2022); the slug is preserved unchanged to avoid breaking
    cross-skill [[wikilinks]]. The fifth author (S. Galtier) was missing from
    the original factory metadata and is restored here from the publisher
    landing page.
domain:
  primary_theme: turbulence
  secondary_themes: [cascade-rate, anisotropy, exact-relation, MHD, geometry-2D-vs-slab]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "Politano-Pouquet third-order law"
  - "incompressible MHD cascade rate"
  - "anisotropic cascade decomposition"
  - "parallel perpendicular epsilon"
  - "2D vs slab cascade"
  - "PSP statistical survey 0.2-0.8 au"
  - "Andres Sahraoui Huang Hadid Galtier 2022"
  - "Elsasser increment flux"
  - "variance anisotropy ratio"
  - "temperature cascade correlation"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s (resampled)", interval: ">2 yr of PSP observations spanning 0.2–0.8 au (encounter list pending full-text verification)", archive: "CDAWeb / PSP SOC"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same as MAG", archive: "CDAWeb / PSP SOC"}
algorithms:
  - name: "Politano-Pouquet (PP) third-order exact relation for incompressible MHD"
    equation_refs: ["paper §2 PP exact relation"]
    external_implementations: []
  - name: "Isotropic ε estimate (volume integral form)"
    equation_refs: ["paper §3 isotropic form"]
  - name: "Anisotropic ε decomposition: parallel and perpendicular to local mean field"
    equation_refs: ["paper §3 anisotropic decomposition"]
  - name: "2D vs slab geometric decomposition"
    equation_refs: ["paper §4 2D/slab geometry"]
  - name: "Variance anisotropy ratio, cross-helicity, residual energy diagnostics"
    equation_refs: ["paper §3 ancillary diagnostics"]
validation_targets:
  - "Variance anisotropy ratio shows no measurable heliocentric-distance dependence over 0.2–0.8 au (abstract-level verified)."
  - "Perpendicular cascade rate dominates over parallel cascade as PSP approaches the Sun (qualitative, abstract-level)."
  - "2D cascade geometry dominates over the slab component in slow solar wind at the largest MHD scales (abstract-level verified)."
  - "Strong correlation between isotropic and anisotropic ε and proton temperature (qualitative, abstract-level)."
  - "Per-direction ε magnitudes and the precise (parallel, perpendicular, 2D, slab) split values: pending full-text verification."
links:
  doi_url: "https://doi.org/10.1051/0004-6361/202142994"
  arxiv_url: "https://arxiv.org/abs/2112.13748"
  ads_url: "https://ui.adsabs.harvard.edu/abs/2022A%26A...661A.116A"
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/ (PSP FIELDS + SWEAP)"
claim_boundary:
  scope: >-
    Over >2 yr of PSP data covering 0.2–0.8 au, the incompressible
    Politano-Pouquet cascade rate decomposed parallel and perpendicular to
    the local mean field shows perpendicular-cascade dominance approaching
    the Sun and a 2D-cascade dominance over the slab component in slow
    solar wind at the largest MHD scales. Variance anisotropy is
    statistically distance-independent over the analysed range.
  out_of_scope:
    - "Do not apply the incompressible PP law to intervals with measurable density compressibility without explicitly quoting δn/n and falling back to a compressible cascade relation."
    - "Do not equate per-direction ε with a single scalar dissipation rate; the PP exact relation constrains the cascade flux, not local dissipation."
    - "Do not extrapolate the parallel/perpendicular ratio or the 2D/slab split below 0.2 au or beyond 0.8 au without re-fitting on the new bins."
    - "Do not import the 2D-dominance conclusion to fast streams without separate re-binning — the abstract conditions 2D dominance on slow solar wind."
failure_modes:
  - "Third-order moments have heavy statistical noise; small-sample bias in the tails can flip the sign of ε at large lag if the interval set is short."
  - "Local-mean-field estimator (scale-dependent vs window-mean) changes the parallel/perpendicular split nontrivially."
  - "Proton density source (SPC vs SPAN-I derived) propagates into ε via Elsasser variables — quote the source and document any cross-instrument calibration."
  - "Compressibility violates the incompressible-MHD derivation; pre-filter intervals on δn/n threshold or fall back to compressible PP relation."
  - "Selecting the inertial-range fit window is sensitive — too short biases ε downward, too long crosses into the energy-containing range."
  - "Encounter coverage of 0.2 au depends on PSP perihelion sampling distribution; selection effects in the close-perihelion bins can mimic radial trends."
depends_on:
  - paper-bandyopadhyay-2020-energy-transfer-psp
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Anisotropic-ε statistics are bound to PSP 0.2–0.8 au. No sibling skill yet provides a Solar Orbiter or Helios reanalysis with the same PP-anisotropic pipeline."
    proposed_action: "Replicate the PP-anisotropic pipeline on Solar Orbiter MAG+SWA over the Helios-overlap distance band and overlay ε⊥/ε∥(r)."
  - type: hypothesis
    statement: "If the perpendicular-cascade-dominance is set by the 2D-cascade geometry rather than by kinetic dissipation, then ε⊥/ε∥ at the inertial range should correlate with the 2D/slab variance ratio across PSP intervals."
    proposed_action: "Stratify PSP intervals by 2D/slab variance ratio (computed from the Bieber-decomposition style two-point statistics) and test for a per-bin correlation with ε⊥/ε∥."
  - type: tension
    statement: "Per-direction PP cascade rate should be cross-checked against compressible-cascade flux estimates — the incompressible relation may under- or over-estimate ε if mean δn/n exceeds the threshold implicit in the derivation."
    related_skills: [paper-cuesta-2023-compressible-turbulence-eight-perihelia]
    proposed_action: "Run incompressible PP and compressible PP on the same PSP intervals; quantify the ε gap as a function of δn/n."
  - type: composable_experiment
    statement: "Couple ε⊥/ε∥(r) to a sub-ion anisotropy skill (e.g. [[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]]) — testing whether the upstream MHD-scale 2D-cascade geometry sets the kinetic-scale KAW signature, or whether the two regimes are decoupled."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2021 item 6"
  verified_by: "internalization-batch 2026-05-19 (arXiv 2112.13748 + A&A landing 661 A116)"
  verified_at: "2026-05-19T00:00:00Z"
  verification_notes:
    - "field=doi value=10.1051/0004-6361/202142994 source=A-and-A-landing-661-A116 verified_at=2026-05-19"
    - "field=venue value=A-and-A-661-A116-2022 source=A-and-A-landing verified_at=2026-05-19"
    - "field=arxiv_id value=2112.13748 source=arXiv-abs-page verified_at=2026-05-19"
    - "field=fifth_author value=S-Galtier-added-was-missing-from-factory-metadata source=A-and-A-landing verified_at=2026-05-19"
    - "field=publication_year value=2022-preserving-andres-2021-slug-for-wikilink-stability source=A-and-A-landing verified_at=2026-05-19"
tags: [heliophysics, paper-skill, turbulence, cascade, anisotropy, MHD, exact-relation]
---

# Andrés et al. 2022 — incompressible anisotropic cascade rate (PSP, 0.2–0.8 au) — paper-skill

> Compiled from arXiv:2112.13748 = A&A 661, A116 (DOI 10.1051/0004-6361/202142994).
> `paper-grounded-pending-full-text` tier — bibliographic anchors, the 0.2–0.8 au
> radial range, the perpendicular-cascade-dominance and 2D-over-slab claims,
> the variance-anisotropy-vs-distance flatness, and the temperature
> correlation are verified at abstract level. Precise numerical (parallel,
> perpendicular, 2D, slab) ε values and the encounter-by-encounter interval
> list remain pending full-text verification.
>
> **Identity note (preserve uncertainty).** The slug is `andres-2021-...`
> inheriting the arXiv submission year (Dec 2021); the paper was published in
> A&A in 2022. Slug name is preserved to keep cross-skill `[[wikilinks]]`
> stable; `paper.year` is the publication year. The fifth author
> S. Galtier was missing from the original factory metadata and has been
> restored.

## 1. Trigger  *(Layer 1)*

Use when:

- applying the Politano–Pouquet (PP) exact third-order relation to PSP MAG +
  SWEAP data;
- decomposing the inertial-range incompressible cascade rate ε into
  components parallel and perpendicular to the *local* mean field;
- separating 2D vs slab geometric contributions to the cascade in slow solar
  wind at MHD scales;
- producing a baseline ε(r) and ε⊥/ε∥(r) for cross-comparison with kinetic
  anisotropy and intermittency diagnostics.

Do NOT use this skill for compressible-cascade flux estimates (use
[[paper-cuesta-2023-compressible-turbulence-eight-perihelia]] or a
compressible PP relation), for von-Kármán decay estimates, or to claim a
single-scalar dissipation rate — the exact relation constrains the cascade
flux, not local dissipation.

## 2. Paper claim → narrow verifiable task

**Verified claim (abstract + A&A landing, 2026-05-19).** Over more than two
years of PSP observations covering heliocentric distances 0.2–0.8 au, the
incompressible MHD energy cascade rate decomposed into parallel and
perpendicular components shows (i) variance anisotropy independent of
heliocentric distance in the analysed range, (ii) perpendicular-cascade
dominance approaching the Sun, (iii) 2D-cascade dominance over the slab
component in slow solar wind at the largest MHD scales, and (iv) strong
correlation between both the isotropic and anisotropic ε and the proton
temperature.

**Narrow verifiable task.** Reproduction succeeds when an agent, on a PSP
interval set spanning 0.2–0.8 au:

1. computes ε via the PP isotropic form and the anisotropic (parallel /
   perpendicular to local mean field) decomposition;
2. recovers ε⊥ > ε∥ on average as the spacecraft approaches the Sun
   (qualitative monotonic ordering);
3. recovers a flat (within stated uncertainty) variance-anisotropy ratio
   vs heliocentric distance over 0.2–0.8 au;
4. recovers ε_2D > ε_slab in slow-wind intervals at the largest MHD scales;
5. recovers a positive ε–T_p correlation across the interval set.

## 3. Executable protocol (Layer 2 — abstract capabilities)

The skill requires the following abstract capabilities:

1. **PSP MAG + ion-moment reader** — returns B(t), V(t), n_p(t), T_p(t) at a
   common cadence; must support the SPC↔SPAN-I cross-instrument hand-off
   over the 2-year span.
2. **Elsasser-variable builder** — z± = V ± B/√(μ₀ ρ); requires consistent
   n_p source documentation.
3. **PP third-order computer** — evaluates the PP exact relation on Elsasser
   increments per lag ℓ in the inertial range.
4. **Local-mean-field projector** — for each (t, ℓ), projects increments
   into bins parallel and perpendicular to the *scale-dependent* local mean
   field B_0(t, ℓ).
5. **Anisotropic ε aggregator** — per-direction ε computed from the
   projected PP cascade flux.
6. **2D/slab geometric decomposer** — Bieber-style or equivalent two-point
   correlation decomposition into 2D and slab variance / flux.
7. **Distance-binned aggregator** — bins the interval set by heliocentric
   distance and produces ε(r), ε⊥(r), ε∥(r), and ε_2D/ε_slab(r) tables.
8. **Diagnostic compositor** — variance-anisotropy ratio, cross-helicity σ_c,
   residual energy σ_r, and ε vs T_p correlation tables.

Abstract procedure:

1. Select PSP intervals over the >2 yr / 0.2–0.8 au window; per-interval
   stationarity tests; compressibility pre-filter (δn/n threshold for
   incompressible-PP validity).
2. Build z± and compute structure-function-like third-order increments per
   lag.
3. Apply PP isotropic form for ε_iso(ℓ).
4. Project onto local-mean-field-parallel/perpendicular and compute ε∥(ℓ),
   ε⊥(ℓ).
5. Decompose 2D vs slab geometry; compute ε_2D and ε_slab.
6. Bin all quantities by heliocentric distance and compute the four
   acceptance items from §2.
7. Acceptance: match the four qualitative claims; numerical agreement at
   per-bin level requires full-text targets (pending).

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability required |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s (after resample) | >2 yr spanning 0.2–0.8 au | CDAWeb / PSP SOC | high-cadence vector MAG reader with despin |
| PSP/SWEAP SPC | L3 | ~1 Hz | early-mission portion of >2 yr span | CDAWeb / PSP SOC | proton moments reader (n_p, V, T_p) |
| PSP/SWEAP SPAN-I | L3 | ~3.5 s / sweep | later portion of >2 yr span | CDAWeb / PSP SOC | proton moments reader (cross-calibrated with SPC) |

## 5. Validation target

**Primary qualitative targets (verified at abstract level).**

- Variance-anisotropy ratio flat over 0.2–0.8 au within stated uncertainty.
- ε⊥ > ε∥ ordering on average as PSP approaches the Sun.
- ε_2D > ε_slab in slow-wind intervals at the largest MHD scales.
- Positive ε ↔ T_p correlation across the interval set.

**Tolerance budget.** Per-direction ε magnitudes, per-bin error bars, and the
exact ε_2D / ε_slab split values are **pending full-text verification**.
Discrepancy in the *sign* of any of the four ordering claims at the
per-bin level is a pipeline-disagreement flag.

## 6. Failure modes (load-bearing)

- **Heavy-tailed third-order statistics.** PP third-order moments are
  dominated by rare large-amplitude increments; finite-sample bias can flip
  the sign of ε at large ℓ if the interval set is too short.
- **Local-mean-field estimator drift.** Window-mean B_0 vs scale-dependent
  B_0 changes the parallel/perpendicular split — the paper's claim is
  conditioned on the scale-dependent estimator.
- **Proton density source.** SPC and SPAN-I have different epochs and
  calibration; mixing them without documented cross-calibration biases the
  Elsasser variables → biases ε.
- **Compressibility violation.** When δn/n exceeds the incompressible-PP
  validity threshold, the recovered ε is not the true cascade flux; flag and
  fall back to a compressible PP form.
- **Inertial-range fit-window sensitivity.** Too narrow biases ε downward;
  too wide crosses into the energy-containing range. Report the chosen lag
  window per bin.
- **Perihelion-bin selection effect.** PSP sampling at 0.2 au is sparser and
  more biased toward specific stream types than at 0.8 au; the radial trend
  in ε⊥/ε∥ can absorb a hidden stream-type-selection effect.

## 7. Claim boundary

**In scope.** Incompressible PP cascade rate, decomposed parallel /
perpendicular to the local mean field and into 2D / slab geometric
components, over >2 yr of PSP data spanning 0.2–0.8 au.

**Out of scope.** Compressible cascade, single-scalar dissipation
interpretation, fast-stream-specific 2D dominance (the abstract conditions
2D dominance on slow wind), radial extrapolation outside 0.2–0.8 au, and
kinetic-scale interpretation (the analysis is MHD-scale).

## 8. Links and identifiers

- DOI: <https://doi.org/10.1051/0004-6361/202142994> (A&A 661, A116 —
  verified 2026-05-19 from A&A landing).
- arXiv: <https://arxiv.org/abs/2112.13748> (verified 2026-05-19).
- ADS: <https://ui.adsabs.harvard.edu/abs/2022A%26A...661A.116A> (bibcode
  follows A&A 661 A116 pattern; not independently verified via ADS UI).

## 9. Skill graph + Layer-4 affordances

Depends on [[bandyopadhyay-2020-energy-transfer-psp]] (single-PSP-
encounter PP cascade-rate baseline this paper extends to a multi-year survey
and to anisotropic decomposition).

- **Gap.** No Solar Orbiter or Helios sibling skill yet runs the same
  PP-anisotropic + 2D/slab pipeline. Add one to extend ε⊥/ε∥(r) into the
  Helios distance band and produce a cross-mission consistency check.
- **Hypothesis (testable).** If perpendicular-cascade dominance is set by
  the 2D-cascade geometry rather than by kinetic dissipation, then ε⊥/ε∥
  should correlate with the 2D/slab variance ratio across PSP intervals at
  fixed heliocentric distance.
- **Tension.** Incompressible PP ε can diverge from a compressible PP ε on
  the same interval — compare against
  [[paper-cuesta-2023-compressible-turbulence-eight-perihelia]] and report
  ε_gap(δn/n).
- **Composable experiment.** Couple ε⊥/ε∥(r) from this paper to the
  sub-ion-scale KAW signature in
  [[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]] — testing whether
  the upstream MHD-scale 2D dominance sets the kinetic-scale anisotropy or
  whether the two regimes are decoupled.

## 10. Relation to HelioSI corpus

- Parent sub-graph: `wave500_turbulence_intermit_heating_045` (cascade,
  anisotropy, exact relations).
- Sibling paper-skills:
  [[bandyopadhyay-2020-energy-transfer-psp]] (single-encounter
  baseline), [[paper-cuesta-2023-compressible-turbulence-eight-perihelia]]
  (compressible cascade comparator),
  [[paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp]] (sub-ion-scale
  composable experiment).
- Required capabilities (not bound here): PSP MAG+ion-moments reader,
  Elsasser-variable builder, PP third-order computer, scale-dependent
  local-mean-field projector, anisotropic ε aggregator, 2D/slab geometric
  decomposer, distance-binned aggregator.
