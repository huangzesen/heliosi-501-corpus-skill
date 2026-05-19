---
name: paper-mondal-2024-two-inertial-subranges
description: >-
  Use when working with the central claim of Shiladittya Mondal et al. 2024 — Eight fast-
  wind intervals between 0.3 and 3.16 au across solar-minimum and -maximum exhibit two
  distinct inertial sub-ranges, f^(-3/2) and f^(-5/3), with an intermittency-scaling test
  confirming the break. (arXiv:2409.03090; venue TODO verify).
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
  title: "Emergence of two inertial sub-ranges in solar wind turbulence: dependence on heliospheric distance and solar activity"
  first_author: "Shiladittya Mondal"
  authors:
    - "Shiladittya Mondal"
    - "Supratik Banerjee"
    - "Luca Sorriso-Valvo"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2409.03090"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [spectral-index, radial-evolution, intermittency]
  missions: [PSP, Helios, Wind, other]
  regime: [inner-heliosphere, 1au, MHD-scale]
trigger_keywords:
  - "two inertial sub-ranges"
  - "-3/2 vs -5/3"
  - "fast wind 0.3-3.16 au"
  - "intermittency-scaling test"
  - "solar-cycle dependence"
  - "Mondal Banerjee Sorriso-Valvo 2024"
data_products:
  - {instrument: "Multi-mission in-situ MAG (PSP/Helios/Wind/etc.)", level: "L2", cadence: "TODO verify", interval: "0.3-3.16 au, eight fast-wind windows", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Trace magnetic PSD with two-range power-law fit"
    equation_refs: ["TODO verify"]
  - name: "4th-order moment (kurtosis) per sub-range"
    equation_refs: ["TODO verify"]
  - name: "Break-frequency identification"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2409.03090"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Two power-law sub-ranges (~-3/2 and ~-5/3) coexist within the inertial range on the
    analysed eight fast-wind intervals between 0.3 and 3.16 au, verified by the kurtosis
    behaviour across the break.
  out_of_scope:
    - "Do not assert universal two-range structure across slow non-Alfvenic streams without re-fitting."
    - "Do not extrapolate the location of the break to sub-0.3 au PSP data without re-derivation."
    - "Do not equate the break with a single physical mechanism absent additional discriminators."
failure_modes:
  - "Two-range fit is fragile when frequency overlap is small; report Δlog(f)."
  - "Kurtosis estimation needs sample-size bounds; report N per band."
  - "Solar-cycle binning is coarse on eight intervals."
  - "Mission-cadence differences shift the high-f end of the fit window."
depends_on:
  - huang-2023-psp-one-over-f-spectrum
  - chen-2022-magnetic-field-spectral-evolution-inner-heliosphere
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill systematically scans PSP E1-E13 perihelia for the same two-range structure."
  - type: hypothesis
    statement: "If the break is intrinsic, the f^(-3/2) range should extend to lower frequencies as r decreases toward perihelion."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2024 item 12"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Shiladittya Mondal et al. 2024 — Emergence of two inertial sub-ranges in solar wind turbulenc... — paper-skill

> Compiled from arXiv:2409.03090. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Eight fast-wind intervals between 0.3 and 3.16 au across solar-minimum and -maximum exhibit two distinct inertial sub-ranges, f^(-3/2) and f^(-5/3), with an intermittency-scaling test confirming the break.
- Reproducing or extending the analysis around Multi-mission in-situ MAG (PSP/Helios/Wind/etc.).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- slow-wind extrapolation without re-fit
- sub-0.3 au break extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Eight fast-wind intervals between 0.3 and 3.16 au across solar-minimum and -maximum exhibit two distinct inertial sub-ranges, f^(-3/2) and f^(-5/3), with an intermittency-scaling test confirming the break.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Trace magnetic PSD with two-range power-law fit
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### 4th-order moment (kurtosis) per sub-range
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Break-frequency identification
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Multi-mission in-situ MAG (PSP/Helios/Wind/etc.) | L2 | TODO verify | 0.3-3.16 au, eight fast-wind windows | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Two-range fit is fragile when frequency overlap is small; report Δlog(f).
- Kurtosis estimation needs sample-size bounds; report N per band.
- Solar-cycle binning is coarse on eight intervals.
- Mission-cadence differences shift the high-f end of the fit window.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Two power-law sub-ranges (~-3/2 and ~-5/3) coexist within the inertial range on the analysed eight fast-wind intervals between 0.3 and 3.16 au, verified by the kurtosis behaviour across the break.

**Out of scope — do NOT generalize beyond:**

- Do not assert universal two-range structure across slow non-Alfvenic streams without re-fitting.
- Do not extrapolate the location of the break to sub-0.3 au PSP data without re-derivation.
- Do not equate the break with a single physical mechanism absent additional discriminators.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2409.03090
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[huang-2023-psp-one-over-f-spectrum]] — sibling/upstream context for the same physics domain.
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill systematically scans PSP E1-E13 perihelia for the same two-range structure.
- **Hypothesis** — If the break is intrinsic, the f^(-3/2) range should extend to lower frequencies as r decreases toward perihelion.
