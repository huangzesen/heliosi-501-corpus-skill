---
name: paper-ruohotie-2025-intermittency-icme-psp-solo
description: >-
  Use when working with the central claim of Julia Ruohotie et al. 2025 — Intermittency
  diagnostics (PVI, scale-dependent kurtosis, structure-function exponents) inside ICMEs
  observed by PSP and Solar Orbiter show systematic differences vs ambient solar-wind
  intermittency statistics. (arXiv:2505.22283; venue TODO verify).
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
  title: "Intermittency in Interplanetary Coronal Mass Ejections Observed by Parker Solar Probe and Solar Orbiter"
  first_author: "Julia Ruohotie"
  authors:
    - "Julia Ruohotie"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2505.22283"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, ICME, multi-spacecraft]
  missions: [PSP, Solar Orbiter]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "ICME intermittency"
  - "PVI inside ICME"
  - "PSP Solar Orbiter ICME"
  - "scale-dependent kurtosis ICME"
  - "Ruohotie 2025 ICME"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "ICME intervals", archive: "CDAWeb / SPDF"}
  - {instrument: "Solar Orbiter MAG", level: "L2", cadence: "~1 vec/s", interval: "ICME intervals", archive: "SOAR"}
algorithms:
  - name: "ICME interval selection (catalogue join)"
    equation_refs: ["TODO verify"]
  - name: "PVI per scale inside ICME"
    equation_refs: ["TODO verify"]
  - name: "Scale-dependent kurtosis comparison vs ambient"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2505.22283"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Intermittency diagnostics inside ICMEs from the PSP+SO sample studied, vs paired ambient-
    wind sub-intervals.
  out_of_scope:
    - "Do not equate intermittency contrast with a single physical mechanism (e.g. flux-rope topology vs sheath turbulence)."
    - "Do not generalise to outer-heliosphere ICMEs."
    - "Do not apply the same diagnostics without consistent flux-rope detrending."
failure_modes:
  - "Catalogue choice introduces selection bias."
  - "Flux-rope contribution biases PVI if not detrended."
  - "Sample sizes per ICME phase (sheath vs flux rope) are small."
  - "Cadence harmonisation between PSP and SO."
depends_on:
  - paper-good-2026-correlation-length-magnetic-clouds
  - sioulas-2022-magnetic-field-intermittency-psp-solo
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill conditions intermittency separately on sheath vs flux-rope phases."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2505.22283v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Julia Ruohotie et al. 2025 — Intermittency in Interplanetary Coronal Mass Ejections Obser... — paper-skill

> Compiled from arXiv:2505.22283. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Intermittency diagnostics (PVI, scale-dependent kurtosis, structure-function exponents) inside ICMEs observed by PSP and Solar Orbiter show systematic differences vs ambient solar-wind intermittency statistics.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- outer-heliosphere ICME
- mechanism identification from contrast alone

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Intermittency diagnostics (PVI, scale-dependent kurtosis, structure-function exponents) inside ICMEs observed by PSP and Solar Orbiter show systematic differences vs ambient solar-wind intermittency statistics.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### ICME interval selection (catalogue join)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### PVI per scale inside ICME
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Scale-dependent kurtosis comparison vs ambient
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | ICME intervals | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| Solar Orbiter MAG | L2 | ~1 vec/s | ICME intervals | SOAR | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Catalogue choice introduces selection bias.
- Flux-rope contribution biases PVI if not detrended.
- Sample sizes per ICME phase (sheath vs flux rope) are small.
- Cadence harmonisation between PSP and SO.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Intermittency diagnostics inside ICMEs from the PSP+SO sample studied, vs paired ambient-wind sub-intervals.

**Out of scope — do NOT generalize beyond:**

- Do not equate intermittency contrast with a single physical mechanism (e.g. flux-rope topology vs sheath turbulence).
- Do not generalise to outer-heliosphere ICMEs.
- Do not apply the same diagnostics without consistent flux-rope detrending.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2505.22283
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-good-2026-correlation-length-magnetic-clouds]] — sibling/upstream context for the same physics domain.
- [[sioulas-2022-magnetic-field-intermittency-psp-solo]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill conditions intermittency separately on sheath vs flux-rope phases.
