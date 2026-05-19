---
name: paper-sasmal-2026-helicity-barrier-flr-mhd-heating
description: >-
  Use when working with the central claim of Ramesh Sasmal et al. 2026 — Exact cascade laws
  derived for finite-Larmor-radius MHD with an imbalance-induced helicity barrier
  characterise ion-heating channels relevant to coronal and solar-wind turbulence.
  (arXiv:2604.28165; venue TODO verify).
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
  title: "Determination of turbulent heating rate and relaxed states in finite Larmor radius MHD turbulence with helicity barrier"
  first_author: "Ramesh Sasmal"
  authors:
    - "Ramesh Sasmal"
    - "Supratik Banerjee"
  year: 2026
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2604.28165"
  ads_bibcode: null
domain:
  primary_theme: coronal_heating
  secondary_themes: [turbulence, helicity-barrier, FLR-MHD, exact-relation]
  missions: [n/a]
  regime: [MHD-scale, ion-scale, fluid]
trigger_keywords:
  - "helicity barrier"
  - "FLR MHD"
  - "imbalanced turbulence heating"
  - "ion heating channel"
  - "exact cascade law"
  - "Sasmal Banerjee 2026"
data_products: []
algorithms:
  - name: "FLR-MHD exact cascade-law derivation"
    equation_refs: ["TODO verify Eq."]
  - name: "Helicity-barrier identification and quantification"
    equation_refs: ["TODO verify"]
  - name: "Ion-heating-rate partition under FLR-MHD"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.28165"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Closed-form exact cascade laws (derived for FLR-MHD with helicity barrier) and the
    corresponding ion-heating-rate partition under the stated theoretical assumptions.
  out_of_scope:
    - "Do not export FLR-MHD heating partition to fully kinetic regimes without validation."
    - "Do not equate the analytical barrier with observed spectral breaks without a discriminator."
    - "Do not use the relaxed-state form outside the imbalance range tested."
failure_modes:
  - "Closure assumptions (FLR ordering) constrain applicability."
  - "Helicity-barrier sharpness depends on cross-helicity asymmetry assumption."
  - "Heating-rate partition is theoretical; needs observational anchor."
depends_on:
  - martinovic-2024-slow-wind-imbalanced-alfven-wave-heating
  - paper-mcintyre-2024-helicity-barrier-transition-range
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the FLR-MHD heating partition is correct, the predicted Q_i should match empirical ion-heating rates in imbalanced PSP intervals within tolerance."
  - type: minimal_experiment
    statement: "Compute Q_i prediction from FLR-MHD inputs on Martinović 2024 PSP intervals and overlay."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 item 8"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, coronal_heating]
---

# Ramesh Sasmal et al. 2026 — Determination of turbulent heating rate and relaxed states i... — paper-skill

> Compiled from arXiv:2604.28165. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Exact cascade laws derived for finite-Larmor-radius MHD with an imbalance-induced helicity barrier characterise ion-heating channels relevant to coronal and solar-wind turbulence.
- Deciding whether coronal_heating-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- fully kinetic regime
- balanced-turbulence limit

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Exact cascade laws derived for finite-Larmor-radius MHD with an imbalance-induced helicity barrier characterise ion-heating channels relevant to coronal and solar-wind turbulence.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### FLR-MHD exact cascade-law derivation
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Helicity-barrier identification and quantification
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Ion-heating-rate partition under FLR-MHD
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Closure assumptions (FLR ordering) constrain applicability.
- Helicity-barrier sharpness depends on cross-helicity asymmetry assumption.
- Heating-rate partition is theoretical; needs observational anchor.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Closed-form exact cascade laws (derived for FLR-MHD with helicity barrier) and the corresponding ion-heating-rate partition under the stated theoretical assumptions.

**Out of scope — do NOT generalize beyond:**

- Do not export FLR-MHD heating partition to fully kinetic regimes without validation.
- Do not equate the analytical barrier with observed spectral breaks without a discriminator.
- Do not use the relaxed-state form outside the imbalance range tested.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2604.28165
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[martinovic-2024-slow-wind-imbalanced-alfven-wave-heating]] — sibling/upstream context for the same physics domain.
- [[paper-mcintyre-2024-helicity-barrier-transition-range]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If the FLR-MHD heating partition is correct, the predicted Q_i should match empirical ion-heating rates in imbalanced PSP intervals within tolerance.
- **Minimal_experiment** — Compute Q_i prediction from FLR-MHD inputs on Martinović 2024 PSP intervals and overlay.
