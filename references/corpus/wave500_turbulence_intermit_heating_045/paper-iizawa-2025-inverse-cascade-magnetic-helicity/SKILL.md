---
name: paper-iizawa-2025-inverse-cascade-magnetic-helicity
description: >-
  Use when working with the central claim of Masatomi Iizawa et al. 2025 — Magnetic helicity
  density spectra computed from PSP data over >500 heliocentric-distance samples show
  persistent sign characteristics consistent with an inverse cascade in the inner
  heliosphere. (arXiv:2507.13213; venue TODO verify).
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
  title: "Evidence for an Inverse Cascade of Magnetic Helicity in the Inner Heliosphere"
  first_author: "Masatomi Iizawa"
  authors:
    - "Masatomi Iizawa"
    - "Yasuhito Narita"
    - "Tommaso Alberti"
    - "Stuart D. Bale"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2507.13213"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [magnetic-helicity, inverse-cascade, radial-evolution]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "magnetic helicity spectrum"
  - "inverse cascade"
  - "sign-change frequency"
  - "PSP statistics"
  - "Iizawa Narita Alberti Bale 2025"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "PSP encounters (TODO verify range)", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Magnetic helicity density spectrum from single-spacecraft B"
    equation_refs: ["TODO verify"]
  - name: "Distance binning across encounters"
    equation_refs: ["TODO verify"]
  - name: "Sign-change frequency tracking"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2507.13213"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Single-spacecraft magnetic-helicity density spectra from PSP MAG show inverse-cascade-
    consistent sign behaviour across >500 heliocentric-distance samples.
  out_of_scope:
    - "Do not infer 3D helicity flux from a 1D spectrum without explicit reduction assumptions."
    - "Do not export the inner-heliosphere trend to outer-heliosphere distances."
    - "Do not equate inverse-cascade signature with the dynamo definition of inverse helicity transfer."
failure_modes:
  - "Single-spacecraft spectrum requires axisymmetry/Taylor assumptions."
  - "Sign-change estimation is noisy at low statistical sample."
  - "Distance binning lumps wind types unless conditioned."
  - "Spin tone contamination if not despun."
depends_on: []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill cross-checks the inverse-cascade signature with multi-spacecraft (e.g. Solar Orbiter conjunction) measurements."
  - type: minimal_experiment
    statement: "Compute the same helicity spectra on a PSP-SO radial alignment window and compare sign behaviour."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2025 item 13"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Masatomi Iizawa et al. 2025 — Evidence for an Inverse Cascade of Magnetic Helicity in the ... — paper-skill

> Compiled from arXiv:2507.13213. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Magnetic helicity density spectra computed from PSP data over >500 heliocentric-distance samples show persistent sign characteristics consistent with an inverse cascade in the inner heliosphere.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- 3D flux interpretation
- outer-heliosphere extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Magnetic helicity density spectra computed from PSP data over >500 heliocentric-distance samples show persistent sign characteristics consistent with an inverse cascade in the inner heliosphere.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Magnetic helicity density spectrum from single-spacecraft B
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Distance binning across encounters
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Sign-change frequency tracking
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | PSP encounters (TODO verify range) | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Single-spacecraft spectrum requires axisymmetry/Taylor assumptions.
- Sign-change estimation is noisy at low statistical sample.
- Distance binning lumps wind types unless conditioned.
- Spin tone contamination if not despun.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single-spacecraft magnetic-helicity density spectra from PSP MAG show inverse-cascade-consistent sign behaviour across >500 heliocentric-distance samples.

**Out of scope — do NOT generalize beyond:**

- Do not infer 3D helicity flux from a 1D spectrum without explicit reduction assumptions.
- Do not export the inner-heliosphere trend to outer-heliosphere distances.
- Do not equate inverse-cascade signature with the dynamo definition of inverse helicity transfer.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2507.13213
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

No paper-skill dependencies (self-contained).

**Affordances.**

- **Gap** — No sibling skill cross-checks the inverse-cascade signature with multi-spacecraft (e.g. Solar Orbiter conjunction) measurements.
- **Minimal_experiment** — Compute the same helicity spectra on a PSP-SO radial alignment window and compare sign behaviour.
