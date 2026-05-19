---
name: paper-magyar-2024-plasma-frame-synthetic-modeling
description: >-
  Use when working with the central claim of Norbert Magyar et al. 2024 — A toolkit that
  overlays synthetic MHD/turbulence models on PSP time series translates single-spacecraft
  temporal variations into plasma-frame variations more accurately than Taylor-hypothesis
  alone, especially at low solar-wind speeds. (arXiv:2405.12547; venue TODO verify).
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
  title: "Solar wind data analysis aided by synthetic modeling: a better understanding of plasma-frame variations from temporal data"
  first_author: "Norbert Magyar"
  authors:
    - "Norbert Magyar"
    - "Jaye Verniero"
    - "Adam Szabo"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2405.12547"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [plasma-frame, synthetic-modeling, Taylor-hypothesis]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "plasma frame variation"
  - "Taylor hypothesis correction"
  - "synthetic MHD model"
  - "PSP time-series translation"
  - "slow-wind near-Sun"
  - "Magyar Verniero Szabo 2024"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "TODO verify", interval: "TODO verify intervals", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "TODO verify", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Synthetic-model overlay on single-spacecraft time series"
    equation_refs: ["TODO verify"]
  - name: "Plasma-frame variation reconstruction"
    equation_refs: ["TODO verify"]
  - name: "Taylor-hypothesis comparison baseline"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2405.12547"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Plasma-frame variation reconstruction from PSP single-spacecraft data assisted by an
    overlaid synthetic MHD/turbulence model, within the parameter regime tested.
  out_of_scope:
    - "Do not export the correction to non-Alfvenic streams without re-validating the model assumptions."
    - "Do not assume the reconstruction is unique — multiple synthetic models can fit a single time series."
    - "Do not equate plasma-frame variations with 3D wavevector spectra."
failure_modes:
  - "Model-overlay choice is non-unique."
  - "Slow-flow regime amplifies Taylor-hypothesis error but also synthetic-model error."
  - "Plasma moments uncertainty propagates into the frame translation."
  - "Compressive contamination violates incompressible model overlays."
depends_on:
  - paper-stevens-2022-mhd-theory-psp-reconcile
adapter_notes: []
research_generation_affordances:
  - type: minimal_experiment
    statement: "Apply the toolkit to PSP slow-Alfvenic intervals and compare plasma-frame slopes vs Taylor-hypothesis only."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2405.12547v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Norbert Magyar et al. 2024 — Solar wind data analysis aided by synthetic modeling: a bett... — paper-skill

> Compiled from arXiv:2405.12547. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- A toolkit that overlays synthetic MHD/turbulence models on PSP time series translates single-spacecraft temporal variations into plasma-frame variations more accurately than Taylor-hypothesis alone, especially at low solar-wind speeds.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- non-Alfvenic streams without re-validation
- 3D wavevector recovery

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A toolkit that overlays synthetic MHD/turbulence models on PSP time series translates single-spacecraft temporal variations into plasma-frame variations more accurately than Taylor-hypothesis alone, especially at low solar-wind speeds.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Synthetic-model overlay on single-spacecraft time series
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Plasma-frame variation reconstruction
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Taylor-hypothesis comparison baseline
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | TODO verify | TODO verify intervals | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC/SPAN-I | L3 | TODO verify | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Model-overlay choice is non-unique.
- Slow-flow regime amplifies Taylor-hypothesis error but also synthetic-model error.
- Plasma moments uncertainty propagates into the frame translation.
- Compressive contamination violates incompressible model overlays.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Plasma-frame variation reconstruction from PSP single-spacecraft data assisted by an overlaid synthetic MHD/turbulence model, within the parameter regime tested.

**Out of scope — do NOT generalize beyond:**

- Do not export the correction to non-Alfvenic streams without re-validating the model assumptions.
- Do not assume the reconstruction is unique — multiple synthetic models can fit a single time series.
- Do not equate plasma-frame variations with 3D wavevector spectra.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2405.12547
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-stevens-2022-mhd-theory-psp-reconcile]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Minimal_experiment** — Apply the toolkit to PSP slow-Alfvenic intervals and compare plasma-frame slopes vs Taylor-hypothesis only.
