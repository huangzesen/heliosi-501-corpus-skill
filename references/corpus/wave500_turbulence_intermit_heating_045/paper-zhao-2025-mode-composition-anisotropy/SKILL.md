---
name: paper-zhao-2025-mode-composition-anisotropy
description: >-
  Use when working with the central claim of Siqi Zhao et al. 2025 — Decomposing in-situ
  solar-wind fluctuations into Alfvén, slow, and fast MHD eigenmodes shows compressible
  modes concentrate quasi-parallel to the mean field while Alfvenic modes spread broadly,
  explaining the observed angular anisotropy. (arXiv:2510.25636; venue TODO verify).
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
  title: "Mode Composition Shapes Magnetic Anisotropy in Solar Wind Turbulence"
  first_author: "Siqi Zhao"
  authors:
    - "Siqi Zhao"
    - "Huirong Yan"
    - "Terry Z. Liu"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2510.25636"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [mhd-eigenmodes, anisotropy, compressible]
  missions: [other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "MHD eigenmode decomposition"
  - "Alfven slow fast modes"
  - "angle-resolved power partition"
  - "anisotropy origin"
  - "Zhao Yan Liu 2025"
  - "compressible mode"
data_products:
  - {instrument: "In-situ MAG + plasma (mission TODO verify)", level: "L2", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "MHD eigenmode projection (Alfven, slow, fast)"
    equation_refs: ["TODO verify"]
  - name: "Angle-resolved per-mode power spectrum"
    equation_refs: ["TODO verify"]
  - name: "Anisotropy decomposition by mode"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2510.25636"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Per-mode angular power partition extracted by linear MHD eigen-decomposition reproduces
    the observed anisotropy pattern in the analysed dataset.
  out_of_scope:
    - "Do not claim eigenmode decomposition is unique outside the linear-MHD regime."
    - "Do not export the partition to kinetic scales beyond the MHD branches."
    - "Do not extrapolate to fast/slow streams not represented in the original sample."
failure_modes:
  - "Eigen-projection requires plasma-beta-dependent transformation; β uncertainty propagates."
  - "Mode mixing inflates per-mode power at intermediate β."
  - "Single-spacecraft Taylor assumption affects the angle estimate."
  - "Plasma-frame vs spacecraft-frame projection can flip propagation direction."
depends_on:
  - cuesta-2022-compressible-turbulence-psp-themis-maven
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill performs the same MHD eigenmode partition on PSP near-Sun intervals."
  - type: hypothesis
    statement: "If mode mixing dominates anisotropy, the per-mode partition should reproduce angular spectra of PSP perihelion data within tolerance."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2025 item 14"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Siqi Zhao et al. 2025 — Mode Composition Shapes Magnetic Anisotropy in Solar Wind Tu... — paper-skill

> Compiled from arXiv:2510.25636. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Decomposing in-situ solar-wind fluctuations into Alfvén, slow, and fast MHD eigenmodes shows compressible modes concentrate quasi-parallel to the mean field while Alfvenic modes spread broadly, explaining the observed angular anisotropy.
- Reproducing or extending the analysis around In-situ MAG + plasma (mission TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- kinetic-scale branch identification
- fast/slow stream extrapolation without re-fit

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Decomposing in-situ solar-wind fluctuations into Alfvén, slow, and fast MHD eigenmodes shows compressible modes concentrate quasi-parallel to the mean field while Alfvenic modes spread broadly, explaining the observed angular anisotropy.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### MHD eigenmode projection (Alfven, slow, fast)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Angle-resolved per-mode power spectrum
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Anisotropy decomposition by mode
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ MAG + plasma (mission TODO verify) | L2 | TODO verify | TODO verify | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Eigen-projection requires plasma-beta-dependent transformation; β uncertainty propagates.
- Mode mixing inflates per-mode power at intermediate β.
- Single-spacecraft Taylor assumption affects the angle estimate.
- Plasma-frame vs spacecraft-frame projection can flip propagation direction.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Per-mode angular power partition extracted by linear MHD eigen-decomposition reproduces the observed anisotropy pattern in the analysed dataset.

**Out of scope — do NOT generalize beyond:**

- Do not claim eigenmode decomposition is unique outside the linear-MHD regime.
- Do not export the partition to kinetic scales beyond the MHD branches.
- Do not extrapolate to fast/slow streams not represented in the original sample.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2510.25636
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[cuesta-2022-compressible-turbulence-psp-themis-maven]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill performs the same MHD eigenmode partition on PSP near-Sun intervals.
- **Hypothesis** — If mode mixing dominates anisotropy, the per-mode partition should reproduce angular spectra of PSP perihelion data within tolerance.
