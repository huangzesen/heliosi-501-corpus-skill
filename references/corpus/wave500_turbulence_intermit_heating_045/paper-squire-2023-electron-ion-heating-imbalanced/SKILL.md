---
name: paper-squire-2023-electron-ion-heating-imbalanced
description: >-
  Use when working with the central claim of Jonathan Squire et al. 2023 — In strongly
  imbalanced solar-wind turbulence the electron/ion heating partition is controlled by the
  helicity barrier, predicting a higher ion fraction than in balanced turbulence within a
  stated parameter range. (arXiv:2308.13048; venue TODO verify).
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
  title: "Electron-ion heating partition in imbalanced solar-wind turbulence"
  first_author: "Jonathan Squire"
  authors:
    - "Jonathan Squire"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2308.13048"
  ads_bibcode: null
domain:
  primary_theme: coronal_heating
  secondary_themes: [electron-heating, ion-heating, imbalanced, helicity-barrier]
  missions: [n/a]
  regime: [MHD-scale, ion-scale]
trigger_keywords:
  - "electron-ion heating partition"
  - "helicity barrier heating"
  - "imbalanced turbulence Q_i/Q_e"
  - "Squire 2023 partition"
  - "theoretical heating channel"
data_products: []
algorithms:
  - name: "Imbalanced-turbulence heating-partition model"
    equation_refs: ["TODO verify Eq."]
  - name: "Helicity-barrier closure and ion-channel weight"
    equation_refs: ["TODO verify"]
  - name: "Predicted Q_i / Q_e as a function of imbalance"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2308.13048"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Predicted Q_i / Q_e behaviour vs imbalance within the helicity-barrier model assumptions;
    no in-situ data tested here.
  out_of_scope:
    - "Do not apply the predicted ratio outside the parameter envelope of the model."
    - "Do not equate the predicted Q_i with a single dissipation mechanism absent linear-Vlasov support."
    - "Do not assume the helicity-barrier closure operates identically at all beta."
failure_modes:
  - "Closure assumptions limit applicability."
  - "Imbalance metric definition shifts the predicted ratio."
  - "Partition prediction sensitive to inner-scale dissipation choice."
  - "No direct observational anchor in this paper."
depends_on:
  - paper-mcintyre-2024-helicity-barrier-transition-range
  - martinovic-2024-slow-wind-imbalanced-alfven-wave-heating
  - paper-sasmal-2026-helicity-barrier-flr-mhd-heating
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the helicity-barrier partition is correct, PSP imbalanced intervals should show Q_i / Q_e above the balanced-turbulence baseline within tolerance."
  - type: minimal_experiment
    statement: "Match the predicted Q_i / Q_e against empirical heating rates on Martinović 2024 PSP intervals."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2308.13048v4)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, coronal_heating]
---

# Jonathan Squire et al. 2023 — Electron-ion heating partition in imbalanced solar-wind turb... — paper-skill

> Compiled from arXiv:2308.13048. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- In strongly imbalanced solar-wind turbulence the electron/ion heating partition is controlled by the helicity barrier, predicting a higher ion fraction than in balanced turbulence within a stated parameter range.
- Deciding whether coronal_heating-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- balanced-turbulence regime
- direct in-situ Q_i / Q_e measurement (this paper is theoretical)

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** In strongly imbalanced solar-wind turbulence the electron/ion heating partition is controlled by the helicity barrier, predicting a higher ion fraction than in balanced turbulence within a stated parameter range.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Imbalanced-turbulence heating-partition model
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Helicity-barrier closure and ion-channel weight
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Predicted Q_i / Q_e as a function of imbalance
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Closure assumptions limit applicability.
- Imbalance metric definition shifts the predicted ratio.
- Partition prediction sensitive to inner-scale dissipation choice.
- No direct observational anchor in this paper.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Predicted Q_i / Q_e behaviour vs imbalance within the helicity-barrier model assumptions; no in-situ data tested here.

**Out of scope — do NOT generalize beyond:**

- Do not apply the predicted ratio outside the parameter envelope of the model.
- Do not equate the predicted Q_i with a single dissipation mechanism absent linear-Vlasov support.
- Do not assume the helicity-barrier closure operates identically at all beta.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2308.13048
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-mcintyre-2024-helicity-barrier-transition-range]] — sibling/upstream context for the same physics domain.
- [[martinovic-2024-slow-wind-imbalanced-alfven-wave-heating]] — sibling/upstream context for the same physics domain.
- [[paper-sasmal-2026-helicity-barrier-flr-mhd-heating]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If the helicity-barrier partition is correct, PSP imbalanced intervals should show Q_i / Q_e above the balanced-turbulence baseline within tolerance.
- **Minimal_experiment** — Match the predicted Q_i / Q_e against empirical heating rates on Martinović 2024 PSP intervals.
