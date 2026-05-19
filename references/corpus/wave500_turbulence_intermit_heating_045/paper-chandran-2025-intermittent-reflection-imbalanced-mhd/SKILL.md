---
name: paper-chandran-2025-intermittent-reflection-imbalanced-mhd
description: >-
  Use when working with the central claim of B. D. G. Chandran et al. 2025 — An analytic
  phenomenology of strong imbalanced reflection-driven MHD turbulence predicts intermittent
  z+ structure with a defined scaling for the high-order moments distinct from balanced
  GS95-style cascades. (arXiv:2502.04585; venue TODO verify).
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
  title: "Intermittent, Reflection-Driven, Strong Imbalanced MHD Turbulence"
  first_author: "B. D. G. Chandran"
  authors:
    - "B. D. G. Chandran"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2502.04585"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, reflection-driven, imbalanced, theory]
  missions: [n/a]
  regime: [MHD-scale, fluid]
trigger_keywords:
  - "reflection-driven turbulence"
  - "imbalanced cascade"
  - "intermittency phenomenology"
  - "z+ structure"
  - "Chandran 2025 imbalanced theory"
  - "strong MHD turbulence"
data_products: []
algorithms:
  - name: "Analytic intermittency phenomenology under imbalance"
    equation_refs: ["TODO verify Eq."]
  - name: "Predicted high-order moment scaling"
    equation_refs: ["TODO verify"]
  - name: "Reflection-driven cascade closure"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2502.04585"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Analytic predictions for strong imbalanced reflection-driven MHD turbulence within the
    stated assumptions on cross-helicity and outer-scale forcing.
  out_of_scope:
    - "Do not export to weak-turbulence regime without re-derivation."
    - "Do not equate the phenomenology with a numerical cascade rate without simulation calibration."
    - "Do not extrapolate to compressible or kinetic regimes."
failure_modes:
  - "Closure assumptions on outer-scale reflection are restrictive."
  - "High-order moments require empirical anchoring."
  - "Single-mode imbalance limit may not match realistic stream profiles."
depends_on:
  - martinovic-2024-slow-wind-imbalanced-alfven-wave-heating
  - paper-shi-2023-residual-energy-intermittency-expanding-box
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the predicted high-order z+ scaling holds, PSP near-Sun strongly imbalanced intervals should match it within tolerance."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2502.04585v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# B. D. G. Chandran et al. 2025 — Intermittent, Reflection-Driven, Strong Imbalanced MHD Turbu... — paper-skill

> Compiled from arXiv:2502.04585. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- An analytic phenomenology of strong imbalanced reflection-driven MHD turbulence predicts intermittent z+ structure with a defined scaling for the high-order moments distinct from balanced GS95-style cascades.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- weak-turbulence regime
- kinetic-scale extension

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** An analytic phenomenology of strong imbalanced reflection-driven MHD turbulence predicts intermittent z+ structure with a defined scaling for the high-order moments distinct from balanced GS95-style cascades.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Analytic intermittency phenomenology under imbalance
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Predicted high-order moment scaling
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Reflection-driven cascade closure
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Closure assumptions on outer-scale reflection are restrictive.
- High-order moments require empirical anchoring.
- Single-mode imbalance limit may not match realistic stream profiles.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Analytic predictions for strong imbalanced reflection-driven MHD turbulence within the stated assumptions on cross-helicity and outer-scale forcing.

**Out of scope — do NOT generalize beyond:**

- Do not export to weak-turbulence regime without re-derivation.
- Do not equate the phenomenology with a numerical cascade rate without simulation calibration.
- Do not extrapolate to compressible or kinetic regimes.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2502.04585
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[martinovic-2024-slow-wind-imbalanced-alfven-wave-heating]] — sibling/upstream context for the same physics domain.
- [[paper-shi-2023-residual-energy-intermittency-expanding-box]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If the predicted high-order z+ scaling holds, PSP near-Sun strongly imbalanced intervals should match it within tolerance.
