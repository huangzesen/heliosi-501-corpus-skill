---
name: paper-bourouaine-2020-switchback-nonswitchback-turbulence
description: >-
  Use when comparing turbulent power, cross-helicity, and residual-energy
  diagnostics between switchback (SB) and non-switchback (NSB) sub-intervals
  during PSP Encounter 1 — Bourouaine et al. 2020 separate SB/NSB populations
  near perihelion (35.7–41.7 R☉) via conditioned correlation functions and
  Elsasser z± spectra (arXiv 2010.00936; venue TODO verify).
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
  title: "Turbulence characteristics of switchbacks and non-switchbacks intervals observed by Parker Solar Probe"
  first_author: "Bourouaine, S."
  authors:
    - "Sofiane Bourouaine"
    - "Jean C. Perez"
    - "Kristopher G. Klein"
    - "Christopher H. K. Chen"
  year: 2020
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2010.00936"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [switchbacks, alfvenic, intermittency]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "switchback turbulence conditioning"
  - "PSP Encounter 1 turbulence"
  - "Elsasser z+ z- spectra"
  - "cross helicity sigma_c switchback"
  - "residual energy sigma_R"
  - "non-switchback NSB interval"
  - "conditioned correlation function"
  - "Alfvenic deflection patch"
  - "1/f range fast wind"
  - "Bourouaine 2020"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s and burst", interval: "PSP E1 (2018-11 perihelion, 35.7-41.7 R_sun)", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC", level: "L3", cadence: "~1 Hz", interval: "Same as MAG window", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Switchback vs non-switchback conditioning"
    equation_refs: ["TODO verify section/equation in arXiv 2010.00936"]
  - name: "Elsasser variable spectra and structure functions"
    equation_refs: ["TODO verify"]
  - name: "Conditioned two-point correlation function"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2010.00936"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    SB and NSB sub-intervals of PSP Encounter 1 (heliocentric range 35.7-41.7
    R_sun) exhibit distinct inertial-range scaling and z+/z- power ratios under
    a defined switchback-identification rule; the comparison is shown for a
    single perihelion only.
  out_of_scope:
    - "Do not extrapolate SB-vs-NSB spectral contrast to later PSP encounters or sub-Alfvenic intervals without re-running the same conditioning rule."
    - "Do not generalise to slow non-Alfvenic streams; the paper conditions on Alfvenic fast/young-wind segments."
    - "Do not equate this paper's SB-identification rule with deflection-angle thresholds used by other PSP switchback catalogues without explicit cross-calibration."
failure_modes:
  - "Switchback-identification rule (deflection-angle threshold, duration cut) directly biases the SB vs NSB partition; report it explicitly."
  - "Trace power vs Elsasser power conventions differ across papers — quote whether |B|^2 or sum of components is used."
  - "Cross-helicity sign depends on outward direction convention (radial vs Parker spiral)."
  - "Mode mixing: deflection patches contain compressive structure that contaminates pure-Alfvenic z+ assumption."
depends_on:
  - paper-bandyopadhyay-2020-energy-transfer-psp
  - paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Paper bounds its SB-vs-NSB partition to Encounter 1; no sibling skill systematically reruns the same rule across E2-E20."
    related_skills: [paper-adhikari-2025-trans-alfvenic-turbulence]
    proposed_action: "Compile a stub skill that applies the same conditioning rule to later PSP encounters and reports σc/σR drift."
  - type: tension
    statement: "If SB and NSB spectra are statistically indistinguishable at higher orders, this weakens the in-situ-generation switchback scenario implied by paper-shoda-2021-turbulence-switchback-generation-alfvenic."
    related_skills: [paper-shoda-2021-turbulence-switchback-generation-alfvenic]
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2020-1"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence, switchback]
---

# Bourouaine 2020 — SB vs NSB turbulence conditioning (PSP E1) — paper-skill

> Compiled from arXiv 2010.00936 (Bourouaine, Perez, Klein, Chen). Quality
> tier `stub` — Layer 2 protocol is sketched abstractly; promotion to
> `method-ready` requires reading the full text for the exact SB-identification
> rule and Elsasser convention.

## 1. Trigger  *(Layer 1)*

Use this skill when:

- Conditioning solar-wind turbulence diagnostics on **switchback vs
  non-switchback** sub-intervals from PSP MAG+SWEAP data.
- Comparing Elsasser z± spectra between deflected and undeflected patches
  during PSP Encounter 1.
- Deciding whether observed inertial-range slope changes near perihelion are
  driven by switchbacks or by the ambient stream.

Do NOT use when:

- The target is sub-Alfvenic wind (use [[paper-adhikari-2025-trans-alfvenic-turbulence]]).
- The target is slow non-Alfvenic wind ([[damicis-2021-alfvenic-nonalfvenic-psp]]).
- A switchback-formation mechanism is in question rather than turbulence
  conditioning ([[paper-shoda-2021-turbulence-switchback-generation-alfvenic]],
  [[tenerani-2026-spherically-polarized-magnetic-fields]]).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** During PSP Encounter 1 (35.7–41.7 R☉), magnetic-field
intervals partitioned into switchback (SB) and non-switchback (NSB)
populations by the paper's deflection-based rule exhibit measurably distinct
Elsasser z+ and z− power, normalised cross helicity σc, and residual energy
σR; the partition is reproducible by re-running the same rule on the same MAG
data.

**Verifiable task.** A reproduction succeeds when an agent recovers the
qualitative SB-vs-NSB ordering of inertial-range Elsasser power and σc
reported by the paper for PSP E1, with the SB/NSB rule explicitly named. The
exact tolerance is TODO verify against the published figures.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Switchback vs non-switchback conditioning
- Paper reference: Sec. 2 (TODO verify exact section).
- Abstract procedure:
  1. Read PSP/FIELDS MAG B_RTN over the PSP E1 perihelion window.
  2. Define a switchback indicator (e.g. radial-field deflection angle exceeds
     a threshold for at least a minimum duration); the threshold/duration
     pair is the **conditioning rule** and must be reported.
  3. Split the time series into SB and NSB sub-windows.
- Capability requirements:
  - Time-series read of MAG L2 over an arbitrary interval.
  - Local mean-field estimator for the deflection-angle measure.
  - Boolean masking of a continuous time series.

### Elsasser variable spectra
- Paper reference: Sec. 3 (TODO verify).
- Abstract procedure:
  1. Combine MAG B and SWEAP V to construct z± = V ± B/√(μ0 ρ) on a common
     cadence.
  2. Compute trace power spectra of z+ and z− over SB and NSB masks
     separately.
  3. Report z+/z− power ratio, σc, σR as functions of frequency.

### Conditioned two-point correlation function
- Paper reference: TODO verify section.
- Abstract procedure: compute lag-domain correlation of B (and V if used)
  separately inside SB and NSB masks; interpret outer-scale and inertial-range
  cross-overs.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s + burst | E1 perihelion 2018-11 | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC | L3 | ~1 Hz | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires fixing the SB-identification rule, the Elsasser convention, and the
target z+/z− ratio numbers from the paper figures (TODO verify exact values).

## 6. Failure modes → skill memory  *(Layer 1)*

- SB-identification threshold tightly controls the partition; never report
  results without the threshold.
- Trace vs component power conventions can shift slopes by visual ~0.1 — be
  explicit.
- Cross-helicity sign depends on outward-flow convention; flip when crossing
  HCS.
- Compressive contamination inside deflection patches breaks the pure-Alfvenic
  z± picture; include δ|B|/|B| as a sanity diagnostic.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PSP E1 (35.7–41.7 R☉) SB-vs-NSB Elsasser-power contrast, under
the paper's deflection-based rule, on Alfvenic fast/young wind.

**Out of scope — do NOT generalize to:**

- Later PSP encounters without re-running the rule.
- Sub-Alfvenic intervals or slow non-Alfvenic wind.
- Other catalogues' switchback definitions without cross-calibration.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a (preprint as of inventory; venue TODO verify)
- arXiv: https://arxiv.org/abs/2010.00936
- ADS: n/a
- Code: n/a
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph.**
- [[paper-bandyopadhyay-2020-energy-transfer-psp]] — upstream cascade-rate
  context for the same E1 window.
- [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]] — sibling
  Alfvenicity-conditioned analysis across E1–E5.

**Affordances.**

- **Gap** — The SB/NSB conditioning rule is bound to E1; whether the partition
  carries the same spectral contrast across PSP E2–E20 is unresolved.
  Proposed: stub a sibling skill that applies the same rule to E14–E19.
- **Tension** — If SB and NSB inertial-range spectra are statistically
  indistinguishable at higher orders, the in-situ switchback-generation
  hypothesis weakens. Related: [[paper-shoda-2021-turbulence-switchback-generation-alfvenic]].
