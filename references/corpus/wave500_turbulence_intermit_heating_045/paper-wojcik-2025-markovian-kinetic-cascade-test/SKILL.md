---
name: paper-wojcik-2025-markovian-kinetic-cascade-test
description: >-
  Use when working with the central claim of Dariusz Wójcik et al. 2025 — Conditional-
  probability statistics on solar-wind magnetic-field increments at kinetic scales support a
  Markovian cascade structure within a stated range of scales. (arXiv:2503.07255; venue TODO
  verify).
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
  title: "Testing for Markovian character of transfer of fluctuations in solar wind turbulence on kinetic scales"
  first_author: "Dariusz Wójcik"
  authors:
    - "Dariusz Wójcik"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2503.07255"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [kinetic-scale, Markov-process, statistical-test]
  missions: [other]
  regime: [1au, ion-scale, kinetic]
trigger_keywords:
  - "Markov cascade kinetic"
  - "conditional probability increments"
  - "scale-to-scale transfer"
  - "Wojcik 2025 Markov"
  - "kinetic-range statistics"
data_products:
  - {instrument: "In-situ MAG (mission TODO verify)", level: "L2", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Conditional-probability P(δB_l | δB_{l+Δ}) estimator"
    equation_refs: ["TODO verify Eq."]
  - name: "Chapman-Kolmogorov consistency test"
    equation_refs: ["TODO verify"]
  - name: "Kinetic-scale range definition"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2503.07255"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the kinetic-scale range tested on the analysed dataset, the increment-process
    passes Chapman-Kolmogorov-style Markov consistency tests.
  out_of_scope:
    - "Do not export the Markov claim to the MHD inertial range without re-testing."
    - "Do not equate Markovian behaviour with a particular physical cascade closure."
    - "Do not assume continuity-equation Markov implies a unique drift/diffusion form."
failure_modes:
  - "Conditional-PDF estimation is sample-hungry."
  - "Kinetic-scale range definition is dataset-dependent."
  - "Spectral leakage from larger scales biases conditional moments."
  - "Markov test sensitivity depends on chosen Δ step."
depends_on: []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill applies the same Markov test to PSP near-Sun kinetic scales."
  - type: minimal_experiment
    statement: "Repeat the conditional-PDF Markov test on PSP burst-mode kinetic-range data and report pass/fail."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2503.07255v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Dariusz Wójcik et al. 2025 — Testing for Markovian character of transfer of fluctuations ... — paper-skill

> Compiled from arXiv:2503.07255. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Conditional-probability statistics on solar-wind magnetic-field increments at kinetic scales support a Markovian cascade structure within a stated range of scales.
- Reproducing or extending the analysis around In-situ MAG (mission TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- MHD inertial-range Markov claim
- specific cascade closure inference

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Conditional-probability statistics on solar-wind magnetic-field increments at kinetic scales support a Markovian cascade structure within a stated range of scales.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Conditional-probability P(δB_l | δB_{l+Δ}) estimator
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Chapman-Kolmogorov consistency test
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Kinetic-scale range definition
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ MAG (mission TODO verify) | L2 | TODO verify | TODO verify | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Conditional-PDF estimation is sample-hungry.
- Kinetic-scale range definition is dataset-dependent.
- Spectral leakage from larger scales biases conditional moments.
- Markov test sensitivity depends on chosen Δ step.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the kinetic-scale range tested on the analysed dataset, the increment-process passes Chapman-Kolmogorov-style Markov consistency tests.

**Out of scope — do NOT generalize beyond:**

- Do not export the Markov claim to the MHD inertial range without re-testing.
- Do not equate Markovian behaviour with a particular physical cascade closure.
- Do not assume continuity-equation Markov implies a unique drift/diffusion form.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2503.07255
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

No paper-skill dependencies (self-contained).

**Affordances.**

- **Gap** — No sibling skill applies the same Markov test to PSP near-Sun kinetic scales.
- **Minimal_experiment** — Repeat the conditional-PDF Markov test on PSP burst-mode kinetic-range data and report pass/fail.
