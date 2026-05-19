---
name: paper-galtier-2023-fast-magnetoacoustic-turbulence-iroshnikov
description: >-
  Use when working with the central claim of Sebastien Galtier et al. 2023 — Wave-turbulence
  kinetic-equation analysis of fast magnetosonic waves predicts an Iroshnikov-Kraichnan
  k^(-3/2) power spectrum for the fast-mode cascade under the stated theoretical
  assumptions. (arXiv:2303.00643; venue TODO verify).
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
  title: "Fast magneto-acoustic wave turbulence and the Iroshnikov-Kraichnan spectrum"
  first_author: "Sebastien Galtier"
  authors:
    - "Sebastien Galtier"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2303.00643"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [wave-turbulence, fast-mode, Iroshnikov-Kraichnan, theory]
  missions: [n/a]
  regime: [MHD-scale, fluid]
trigger_keywords:
  - "fast magnetoacoustic turbulence"
  - "Iroshnikov-Kraichnan -3/2"
  - "wave kinetic equation"
  - "Galtier 2023 wave turbulence"
  - "fast-mode cascade"
data_products: []
algorithms:
  - name: "Wave kinetic equation for fast magnetosonic modes"
    equation_refs: ["TODO verify Eq."]
  - name: "Steady-state spectrum derivation"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2303.00643"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Theoretical k^(-3/2) prediction for the fast-magnetosonic wave-turbulence cascade under
    the paper's wave-turbulence assumptions.
  out_of_scope:
    - "Do not apply the prediction directly to strong-turbulence regimes."
    - "Do not equate the wave-turbulence spectrum with a strong-MHD cascade slope."
    - "Do not assert universality outside the weak-amplitude regime."
failure_modes:
  - "Weak-turbulence ordering may fail in real solar wind."
  - "Mode-coupling truncation assumptions are restrictive."
  - "No direct in-situ anchor in the paper itself."
depends_on:
  - paper-zhao-2025-mode-composition-anisotropy
  - cuesta-2022-compressible-turbulence-psp-themis-maven
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If a fast-mode dominated band exists in PSP data, its slope should approach -3/2 in the weak-amplitude limit."
  - type: minimal_experiment
    statement: "Eigenmode-project PSP fluctuations into the fast branch and fit the fast-mode-only spectral slope."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2303.00643v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Sebastien Galtier et al. 2023 — Fast magneto-acoustic wave turbulence and the Iroshnikov-Kra... — paper-skill

> Compiled from arXiv:2303.00643. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Wave-turbulence kinetic-equation analysis of fast magnetosonic waves predicts an Iroshnikov-Kraichnan k^(-3/2) power spectrum for the fast-mode cascade under the stated theoretical assumptions.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- strong-turbulence regime
- direct in-situ slope inference without mode projection

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Wave-turbulence kinetic-equation analysis of fast magnetosonic waves predicts an Iroshnikov-Kraichnan k^(-3/2) power spectrum for the fast-mode cascade under the stated theoretical assumptions.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Wave kinetic equation for fast magnetosonic modes
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Steady-state spectrum derivation
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Weak-turbulence ordering may fail in real solar wind.
- Mode-coupling truncation assumptions are restrictive.
- No direct in-situ anchor in the paper itself.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Theoretical k^(-3/2) prediction for the fast-magnetosonic wave-turbulence cascade under the paper's wave-turbulence assumptions.

**Out of scope — do NOT generalize beyond:**

- Do not apply the prediction directly to strong-turbulence regimes.
- Do not equate the wave-turbulence spectrum with a strong-MHD cascade slope.
- Do not assert universality outside the weak-amplitude regime.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2303.00643
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-zhao-2025-mode-composition-anisotropy]] — sibling/upstream context for the same physics domain.
- [[cuesta-2022-compressible-turbulence-psp-themis-maven]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If a fast-mode dominated band exists in PSP data, its slope should approach -3/2 in the weak-amplitude limit.
- **Minimal_experiment** — Eigenmode-project PSP fluctuations into the fast branch and fit the fast-mode-only spectral slope.
