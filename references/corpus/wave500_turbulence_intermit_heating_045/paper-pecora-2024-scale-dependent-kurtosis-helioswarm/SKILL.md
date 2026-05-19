---
name: paper-pecora-2024-scale-dependent-kurtosis-helioswarm
description: >-
  Use when working with the central claim of Francesco Pecora et al. 2024 — A multi-point
  HelioSwarm-style SDK estimator outperforms single-spacecraft SDK in recovering true
  increment kurtosis from a synthetic multi-spacecraft configuration spanning the inertial-
  to-kinetic range. (arXiv:2407.06679; venue TODO verify).
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
  title: "Evaluation of scale-dependent kurtosis with HelioSwarm"
  first_author: "Francesco Pecora"
  authors:
    - "Francesco Pecora"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2407.06679"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, HelioSwarm, scale-dependent-kurtosis, multi-point]
  missions: [other]
  regime: [1au, MHD-scale, ion-scale]
trigger_keywords:
  - "HelioSwarm SDK"
  - "multi-spacecraft kurtosis"
  - "scale-dependent kurtosis estimator"
  - "Pecora 2024 multi-point"
  - "synthetic configuration test"
data_products:
  - {instrument: "Synthetic HelioSwarm trajectory through turbulence model", level: "derived", cadence: "TODO verify dt", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "Multi-point SDK estimator with HelioSwarm geometry"
    equation_refs: ["TODO verify"]
  - name: "Synthetic-trajectory benchmark vs single-spacecraft estimator"
    equation_refs: ["TODO verify"]
  - name: "Bias and variance evaluation"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2407.06679"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the synthetic test cases, the HelioSwarm-style multi-point SDK estimator has lower
    bias and variance than the single-spacecraft estimator at the studied scales.
  out_of_scope:
    - "Do not assume the bias improvement transfers to real HelioSwarm data without on-orbit calibration."
    - "Do not extend the conclusion beyond the spacecraft-spacing range tested."
    - "Do not equate synthetic-test bias floors with absolute bias on real data."
failure_modes:
  - "Spacecraft-spacing distribution biases the estimator if too narrow."
  - "Synthetic turbulence model assumptions may not match real intermittency."
  - "Time-tag synchronisation across spacecraft is critical."
  - "Per-lag sample count depends on configuration geometry."
depends_on:
  - sioulas-2022-magnetic-field-intermittency-psp-solo
  - paper-cuesta-2022-intermittency-psp-helios-voyager
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "Once HelioSwarm flies, the predicted bias improvement should be visible on data with matched configurations."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2407.06679v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Francesco Pecora et al. 2024 — Evaluation of scale-dependent kurtosis with HelioSwarm — paper-skill

> Compiled from arXiv:2407.06679. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- A multi-point HelioSwarm-style SDK estimator outperforms single-spacecraft SDK in recovering true increment kurtosis from a synthetic multi-spacecraft configuration spanning the inertial-to-kinetic range.
- Reproducing or extending the analysis around Synthetic HelioSwarm trajectory through turbulence model.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- on-orbit data conclusions before launch
- spacing ranges outside the tested envelope

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A multi-point HelioSwarm-style SDK estimator outperforms single-spacecraft SDK in recovering true increment kurtosis from a synthetic multi-spacecraft configuration spanning the inertial-to-kinetic range.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Multi-point SDK estimator with HelioSwarm geometry
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Synthetic-trajectory benchmark vs single-spacecraft estimator
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Bias and variance evaluation
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Synthetic HelioSwarm trajectory through turbulence model | derived | TODO verify dt | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Spacecraft-spacing distribution biases the estimator if too narrow.
- Synthetic turbulence model assumptions may not match real intermittency.
- Time-tag synchronisation across spacecraft is critical.
- Per-lag sample count depends on configuration geometry.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the synthetic test cases, the HelioSwarm-style multi-point SDK estimator has lower bias and variance than the single-spacecraft estimator at the studied scales.

**Out of scope — do NOT generalize beyond:**

- Do not assume the bias improvement transfers to real HelioSwarm data without on-orbit calibration.
- Do not extend the conclusion beyond the spacecraft-spacing range tested.
- Do not equate synthetic-test bias floors with absolute bias on real data.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2407.06679
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[sioulas-2022-magnetic-field-intermittency-psp-solo]] — sibling/upstream context for the same physics domain.
- [[paper-cuesta-2022-intermittency-psp-helios-voyager]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — Once HelioSwarm flies, the predicted bias improvement should be visible on data with matched configurations.
