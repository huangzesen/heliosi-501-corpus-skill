---
name: paper-jiang-2022-forced-anisotropic-third-order-hyperviscosity
description: >-
  Use when working with the central claim of Bin Jiang et al. 2022 — In forced anisotropic
  MHD simulations with hyperviscosity, the third-order law-derived cascade rate matches the
  imposed injection rate within stated tolerance when computed with the appropriate
  anisotropic projection. (arXiv:2212.03617; venue TODO verify).
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
  title: "Energy transfer and third-order law in forced anisotropic MHD turbulence with hyperviscosity"
  first_author: "Bin Jiang"
  authors:
    - "Bin Jiang"
    - "Yan Yang"
    - "Sean Oughton"
  year: 2022
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2212.03617"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [cascade-rate, exact-relation, forced-MHD, simulation]
  missions: [n/a]
  regime: [MHD-scale, fluid]
trigger_keywords:
  - "forced MHD turbulence"
  - "hyperviscosity"
  - "third-order law cascade rate"
  - "anisotropic projection"
  - "injection rate match"
  - "Jiang Yang Oughton 2022"
data_products:
  - {instrument: "Forced MHD simulation output", level: "derived", cadence: "TODO verify dt", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "Forced anisotropic MHD simulation with hyperviscosity"
    equation_refs: ["TODO verify"]
  - name: "Third-order-law cascade-rate estimator (anisotropic projection)"
    equation_refs: ["TODO verify"]
  - name: "Injection-rate vs ε comparison"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2212.03617"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the simulated forcing/hyperviscosity parameter range, the anisotropic third-order
    law recovers the injection rate within the reported tolerance.
  out_of_scope:
    - "Do not export the tolerance to natural-viscosity simulations without re-validation."
    - "Do not equate hyperviscosity dissipation with physical kinetic dissipation."
    - "Do not generalise to compressible MHD without an additional source term."
failure_modes:
  - "Hyperviscosity narrows the inertial range; report the usable range."
  - "Forcing scheme imprint can dominate at large scales."
  - "Statistical convergence requires long time series."
  - "Projection axis choice (global vs local mean field) shifts ε."
depends_on:
  - paper-andres-2021-incompressible-cascade-anisotropic-pp
  - paper-jiang-2025-angular-third-order-law
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the anisotropic-projection estimator is unbiased in forced simulations, spacecraft estimates conditioned on local-mean-field stability should also be unbiased."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2212.03617v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Bin Jiang et al. 2022 — Energy transfer and third-order law in forced anisotropic MH... — paper-skill

> Compiled from arXiv:2212.03617. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- In forced anisotropic MHD simulations with hyperviscosity, the third-order law-derived cascade rate matches the imposed injection rate within stated tolerance when computed with the appropriate anisotropic projection.
- Reproducing or extending the analysis around Forced MHD simulation output.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- compressible cascade
- natural-viscosity quantitative comparison

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** In forced anisotropic MHD simulations with hyperviscosity, the third-order law-derived cascade rate matches the imposed injection rate within stated tolerance when computed with the appropriate anisotropic projection.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Forced anisotropic MHD simulation with hyperviscosity
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Third-order-law cascade-rate estimator (anisotropic projection)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Injection-rate vs ε comparison
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Forced MHD simulation output | derived | TODO verify dt | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Hyperviscosity narrows the inertial range; report the usable range.
- Forcing scheme imprint can dominate at large scales.
- Statistical convergence requires long time series.
- Projection axis choice (global vs local mean field) shifts ε.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the simulated forcing/hyperviscosity parameter range, the anisotropic third-order law recovers the injection rate within the reported tolerance.

**Out of scope — do NOT generalize beyond:**

- Do not export the tolerance to natural-viscosity simulations without re-validation.
- Do not equate hyperviscosity dissipation with physical kinetic dissipation.
- Do not generalise to compressible MHD without an additional source term.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2212.03617
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] — sibling/upstream context for the same physics domain.
- [[paper-jiang-2025-angular-third-order-law]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If the anisotropic-projection estimator is unbiased in forced simulations, spacecraft estimates conditioned on local-mean-field stability should also be unbiased.
