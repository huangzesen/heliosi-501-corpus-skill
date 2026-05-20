---
name: paper-jiang-2025-angular-third-order-law
description: >-
  Use when working with the central claim of Bin Jiang et al. 2025 — In anisotropic MHD
  simulations the Politano-Pouquet cascade rate inferred along a single sampling direction
  is least biased at a polar angle of ~60 deg relative to the mean field. (arXiv:2512.16610;
  venue TODO verify).
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
  title: "Angular dependence of third-order law in anisotropic MHD turbulence"
  first_author: "Bin Jiang"
  authors:
    - "Bin Jiang"
    - "Zhuoran Gao"
    - "Yan Yang"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2512.16610"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [cascade-rate, exact-relation, anisotropy, simulation]
  missions: [n/a]
  regime: [MHD-scale, fluid]
trigger_keywords:
  - "third-order law angular bias"
  - "anisotropic MHD simulation"
  - "optimal sampling angle 60deg"
  - "single-direction sampling"
  - "Jiang Gao Yang 2025"
  - "cascade rate estimator"
data_products:
  - {instrument: "Anisotropic MHD simulation output", level: "derived", cadence: "TODO verify dt", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "Anisotropic MHD simulation with controlled mean-field angle"
    equation_refs: ["TODO verify"]
  - name: "Single-direction PP cascade-rate estimator at varied sampling angles"
    equation_refs: ["TODO verify"]
  - name: "Bias-vs-angle curve"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2512.16610"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within anisotropic MHD simulations under the studied parameter regime, the bias of single-
    direction PP cascade-rate estimation is minimised near a ~60 deg sampling angle.
  out_of_scope:
    - "Do not export the optimal angle to compressible or sub-Alfvenic regimes without re-simulating."
    - "Do not interpret the bias as removable; some residual bias persists at all angles."
    - "Do not equate the simulation parameter regime with PSP near-Sun conditions."
failure_modes:
  - "Bias-minimisation may be regime-specific (driving, mean-field strength)."
  - "Box-size effects truncate outer-scale flux."
  - "Resolution at small lags affects ε normalisation."
  - "Sampling-angle definition (instantaneous vs window-mean B) shifts the minimum."
depends_on:
  - paper-andres-2021-incompressible-cascade-anisotropic-pp
  - paper-bandyopadhyay-2020-energy-transfer-psp
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "Spacecraft-style ε estimation should be most reliable when conditioning on intervals with effective sampling angle near 60 deg."
  - type: minimal_experiment
    statement: "Condition PSP PP ε estimates on local theta_VB near 60 deg and compare to other-angle bins."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 item 4"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Bin Jiang et al. 2025 — Angular dependence of third-order law in anisotropic MHD tur... — paper-skill

> Compiled from arXiv:2512.16610. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- In anisotropic MHD simulations the Politano-Pouquet cascade rate inferred along a single sampling direction is least biased at a polar angle of ~60 deg relative to the mean field.
- Reproducing or extending the analysis around Anisotropic MHD simulation output.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- compressible cascade
- direct spacecraft ε estimation without regime check

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** In anisotropic MHD simulations the Politano-Pouquet cascade rate inferred along a single sampling direction is least biased at a polar angle of ~60 deg relative to the mean field.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Anisotropic MHD simulation with controlled mean-field angle
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Single-direction PP cascade-rate estimator at varied sampling angles
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Bias-vs-angle curve
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Anisotropic MHD simulation output | derived | TODO verify dt | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Bias-minimisation may be regime-specific (driving, mean-field strength).
- Box-size effects truncate outer-scale flux.
- Resolution at small lags affects ε normalisation.
- Sampling-angle definition (instantaneous vs window-mean B) shifts the minimum.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within anisotropic MHD simulations under the studied parameter regime, the bias of single-direction PP cascade-rate estimation is minimised near a ~60 deg sampling angle.

**Out of scope — do NOT generalize beyond:**

- Do not export the optimal angle to compressible or sub-Alfvenic regimes without re-simulating.
- Do not interpret the bias as removable; some residual bias persists at all angles.
- Do not equate the simulation parameter regime with PSP near-Sun conditions.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2512.16610
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] — sibling/upstream context for the same physics domain.
- [[bandyopadhyay-2020-energy-transfer-psp]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — Spacecraft-style ε estimation should be most reliable when conditioning on intervals with effective sampling angle near 60 deg.
- **Minimal_experiment** — Condition PSP PP ε estimates on local theta_VB near 60 deg and compare to other-angle bins.
