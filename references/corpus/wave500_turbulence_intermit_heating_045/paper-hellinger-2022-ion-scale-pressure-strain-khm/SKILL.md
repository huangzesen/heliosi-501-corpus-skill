---
name: paper-hellinger-2022-ion-scale-pressure-strain-khm
description: >-
  Use when working with the central claim of Petr Hellinger et al. 2022 — 2D hybrid
  simulations analysed with a compressible Hall-MHD Karman-Howarth-Monin equation (extended
  to a tensor pressure) show the ion-scale spectral break is set by a combination of Hall
  physics and effective dissipation through the pressure-strain energy-exchange channel and
  resistivity. (arXiv:2203.12322; venue TODO verify).
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
  title: "Ion-scale transition of plasma turbulence: Pressure-strain effect"
  first_author: "Petr Hellinger"
  authors:
    - "Petr Hellinger"
    - "Victor Montagud-Camps"
    - "Luca Franci"
    - "Lorenzo Matteini"
    - "Emanuele Papini"
    - "Andrea Verdini"
    - "Simone Landi"
  year: 2022
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2203.12322"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [ion-scale, pressure-strain, KHM-equation, hybrid-simulation]
  missions: [n/a]
  regime: [ion-scale, MHD-scale, kinetic]
trigger_keywords:
  - "Karman-Howarth-Monin equation"
  - "Hall MHD"
  - "pressure-strain channel"
  - "ion-scale break"
  - "hybrid PIC simulation"
  - "Hellinger Montagud-Camps Franci Matteini Papini Verdini Landi 2022"
data_products:
  - {instrument: "2D hybrid simulation output", level: "derived", cadence: "TODO verify dt", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "Compressible Hall-MHD KHM equation with tensor pressure"
    equation_refs: ["TODO verify Eq."]
  - name: "Pressure-strain energy-exchange diagnostic"
    equation_refs: ["TODO verify"]
  - name: "Hybrid (fluid e, kinetic i) simulation analysis"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2203.12322"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the simulated 2D hybrid parameter regime, the KHM-budget decomposition identifies
    the combined Hall+pressure-strain+resistivity contribution as setting the ion-scale break.
  out_of_scope:
    - "Do not export the 2D result to 3D in-situ data without a 3D KHM extension."
    - "Do not equate simulation resistivity with physical resistivity."
    - "Do not assume tensor-pressure inclusion is unique to ion-scale physics."
failure_modes:
  - "2D restriction breaks isotropic averaging assumption."
  - "Numerical resistivity dominates real dissipation at limited resolution."
  - "Tensor-pressure measurement requires sufficient time sampling."
  - "KHM source-term residual must be reported, not absorbed."
depends_on:
  - paper-sharma-2026-subion-current-sheets-kaw-pic
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If pressure-strain is the dominant ion-scale channel, observational pressure-strain estimates from PSP burst data should track simulation diagnostics."
  - type: minimal_experiment
    statement: "Compute observational pressure-strain proxy from PSP SPAN-I VDF + MAG burst data and overlay simulation KHM term."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2203.12322v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Petr Hellinger et al. 2022 — Ion-scale transition of plasma turbulence: Pressure-strain e... — paper-skill

> Compiled from arXiv:2203.12322. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- 2D hybrid simulations analysed with a compressible Hall-MHD Karman-Howarth-Monin equation (extended to a tensor pressure) show the ion-scale spectral break is set by a combination of Hall physics and effective dissipation through the pressure-strain energy-exchange channel and resistivity.
- Reproducing or extending the analysis around 2D hybrid simulation output.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- 3D conclusions from 2D simulation
- physical-resistivity quantification

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** 2D hybrid simulations analysed with a compressible Hall-MHD Karman-Howarth-Monin equation (extended to a tensor pressure) show the ion-scale spectral break is set by a combination of Hall physics and effective dissipation through the pressure-strain energy-exchange channel and resistivity.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Compressible Hall-MHD KHM equation with tensor pressure
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Pressure-strain energy-exchange diagnostic
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Hybrid (fluid e, kinetic i) simulation analysis
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| 2D hybrid simulation output | derived | TODO verify dt | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- 2D restriction breaks isotropic averaging assumption.
- Numerical resistivity dominates real dissipation at limited resolution.
- Tensor-pressure measurement requires sufficient time sampling.
- KHM source-term residual must be reported, not absorbed.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the simulated 2D hybrid parameter regime, the KHM-budget decomposition identifies the combined Hall+pressure-strain+resistivity contribution as setting the ion-scale break.

**Out of scope — do NOT generalize beyond:**

- Do not export the 2D result to 3D in-situ data without a 3D KHM extension.
- Do not equate simulation resistivity with physical resistivity.
- Do not assume tensor-pressure inclusion is unique to ion-scale physics.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2203.12322
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-sharma-2026-subion-current-sheets-kaw-pic]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If pressure-strain is the dominant ion-scale channel, observational pressure-strain estimates from PSP burst data should track simulation diagnostics.
- **Minimal_experiment** — Compute observational pressure-strain proxy from PSP SPAN-I VDF + MAG burst data and overlay simulation KHM term.
