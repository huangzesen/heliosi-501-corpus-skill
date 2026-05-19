---
name: paper-zank-2022-turbulence-sub-alfvenic
description: >-
  Use when working with the central claim of G. P. Zank et al. 2022 — A nearly-
  incompressible (NI) MHD-based theoretical framework characterises sub-Alfvenic solar-wind
  turbulence with distinct anisotropy and cross-helicity behaviour relative to super-
  Alfvenic conditions. (arXiv:2202.02563; venue TODO verify).
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
  title: "Turbulence in the Sub-Alfvénic Solar Wind"
  first_author: "G. P. Zank"
  authors:
    - "G. P. Zank"
  year: 2022
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2202.02563"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [sub-alfvenic, theory, NI-MHD]
  missions: [n/a]
  regime: [sub-Alfvenic, MHD-scale, fluid]
trigger_keywords:
  - "sub-Alfvenic turbulence theory"
  - "NI MHD framework"
  - "Zank 2022 sub-Alfvenic"
  - "cross-helicity anisotropy"
  - "theoretical sub-Alfvenic"
data_products: []
algorithms:
  - name: "NI-MHD framework for sub-Alfvenic turbulence"
    equation_refs: ["TODO verify Eq."]
  - name: "Predicted anisotropy and cross-helicity behaviour"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2202.02563"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Theoretical predictions for sub-Alfvenic turbulence under NI-MHD framework assumptions.
  out_of_scope:
    - "Do not extrapolate the framework predictions to fully kinetic regimes."
    - "Do not export to compressible super-Alfvenic regimes without re-derivation."
    - "Do not anchor framework parameters to a single observational interval without uncertainty propagation."
failure_modes:
  - "NI ordering restricts applicability."
  - "Sub-Alfvenic data are statistically limited."
  - "Predictions are framework-dependent."
depends_on:
  - paper-adhikari-2025-trans-alfvenic-turbulence
  - kasper-2021-psp-enters-magnetically-dominated-corona
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "Predicted cross-helicity and anisotropy should match PSP sub-Alfvenic observations within stated tolerance."
  - type: minimal_experiment
    statement: "Overlay framework prediction against PSP E8-E19 sub-Alfvenic statistics."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2202.02563v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# G. P. Zank et al. 2022 — Turbulence in the Sub-Alfvénic Solar Wind — paper-skill

> Compiled from arXiv:2202.02563. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- A nearly-incompressible (NI) MHD-based theoretical framework characterises sub-Alfvenic solar-wind turbulence with distinct anisotropy and cross-helicity behaviour relative to super-Alfvenic conditions.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- super-Alfvenic compressible regime
- fully kinetic sub-Alfvenic regime

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A nearly-incompressible (NI) MHD-based theoretical framework characterises sub-Alfvenic solar-wind turbulence with distinct anisotropy and cross-helicity behaviour relative to super-Alfvenic conditions.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### NI-MHD framework for sub-Alfvenic turbulence
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Predicted anisotropy and cross-helicity behaviour
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- NI ordering restricts applicability.
- Sub-Alfvenic data are statistically limited.
- Predictions are framework-dependent.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Theoretical predictions for sub-Alfvenic turbulence under NI-MHD framework assumptions.

**Out of scope — do NOT generalize beyond:**

- Do not extrapolate the framework predictions to fully kinetic regimes.
- Do not export to compressible super-Alfvenic regimes without re-derivation.
- Do not anchor framework parameters to a single observational interval without uncertainty propagation.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2202.02563
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-adhikari-2025-trans-alfvenic-turbulence]] — sibling/upstream context for the same physics domain.
- [[kasper-2021-psp-enters-magnetically-dominated-corona]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — Predicted cross-helicity and anisotropy should match PSP sub-Alfvenic observations within stated tolerance.
- **Minimal_experiment** — Overlay framework prediction against PSP E8-E19 sub-Alfvenic statistics.
