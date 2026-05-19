---
name: paper-brodiano-2025-intermittent-1f-spectrum-pristine
description: >-
  Use when working with the central claim of Maia Brodiano et al. 2025 — A phenomenological
  intermittent-fluctuation model reproduces the 1/f magnetic spectrum in pristine (young)
  solar wind through scale-dependent occurrence of discrete coherent structures.
  (arXiv:2506.04366; venue TODO verify).
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
  title: "An Intermittent Model for the 1/f Spectrum in the Pristine Solar Wind"
  first_author: "Maia Brodiano"
  authors:
    - "Maia Brodiano"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2506.04366"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [one-over-f, intermittency, theory]
  missions: [n/a]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "1/f intermittent model"
  - "pristine solar wind"
  - "coherent-structure occurrence"
  - "scale-dependent statistics"
  - "Brodiano 2025 phenomenology"
data_products: []
algorithms:
  - name: "Intermittent-event scale-dependent occurrence model"
    equation_refs: ["TODO verify Eq."]
  - name: "Synthesised 1/f spectrum from occurrence model"
    equation_refs: ["TODO verify"]
  - name: "Comparison vs observed PSP near-Sun 1/f range"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2506.04366"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the model's stated assumptions on coherent-event occurrence and amplitude
    statistics, the synthesised spectrum reproduces a 1/f range in the pristine-wind regime.
  out_of_scope:
    - "Do not equate model fit with mechanism identification."
    - "Do not export the model parameters to slow non-Alfvenic wind without re-tuning."
    - "Do not assume the model explains the high-frequency inertial-range simultaneously."
failure_modes:
  - "Model parameter degeneracy with respect to occurrence rate and amplitude distribution."
  - "Lack of explicit MHD constraint."
  - "Validation requires conditioning observations on pristine-wind criterion."
depends_on:
  - huang-2023-psp-one-over-f-spectrum
  - paper-davis-2023-1f-evolution-single-fast-stream
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If intermittent coherent events drive the 1/f range, PVI distributions in pristine PSP intervals should match the model's occurrence statistic."
  - type: minimal_experiment
    statement: "Fit the model occurrence rate to PVI distribution at f<f_b in pristine PSP intervals and compare alpha_LF."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2506.04366v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Maia Brodiano et al. 2025 — An Intermittent Model for the 1/f Spectrum in the Pristine S... — paper-skill

> Compiled from arXiv:2506.04366. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- A phenomenological intermittent-fluctuation model reproduces the 1/f magnetic spectrum in pristine (young) solar wind through scale-dependent occurrence of discrete coherent structures.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- slow non-Alfvenic wind without re-tune
- inertial-range slope joint fitting

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A phenomenological intermittent-fluctuation model reproduces the 1/f magnetic spectrum in pristine (young) solar wind through scale-dependent occurrence of discrete coherent structures.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Intermittent-event scale-dependent occurrence model
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Synthesised 1/f spectrum from occurrence model
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Comparison vs observed PSP near-Sun 1/f range
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Model parameter degeneracy with respect to occurrence rate and amplitude distribution.
- Lack of explicit MHD constraint.
- Validation requires conditioning observations on pristine-wind criterion.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the model's stated assumptions on coherent-event occurrence and amplitude statistics, the synthesised spectrum reproduces a 1/f range in the pristine-wind regime.

**Out of scope — do NOT generalize beyond:**

- Do not equate model fit with mechanism identification.
- Do not export the model parameters to slow non-Alfvenic wind without re-tuning.
- Do not assume the model explains the high-frequency inertial-range simultaneously.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2506.04366
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[huang-2023-psp-one-over-f-spectrum]] — sibling/upstream context for the same physics domain.
- [[paper-davis-2023-1f-evolution-single-fast-stream]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If intermittent coherent events drive the 1/f range, PVI distributions in pristine PSP intervals should match the model's occurrence statistic.
- **Minimal_experiment** — Fit the model occurrence rate to PVI distribution at f<f_b in pristine PSP intervals and compare alpha_LF.
