---
name: paper-johnston-2024-unified-ion-heating-low-beta
description: >-
  Use when working with the central claim of Zade Johnston et al. 2024 — Test-particle
  simulations in synthetic turbulent fields yield a unified low-β ion-heating phenomenology
  bridging stochastic and cyclotron-resonant regimes through a single threshold parameter.
  (arXiv:2409.07015; venue TODO verify).
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
  title: "A Unified Phenomenology of Ion Heating in Low-β Plasmas: Test-Particle Simulations"
  first_author: "Zade Johnston"
  authors:
    - "Zade Johnston"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2409.07015"
  ads_bibcode: null
domain:
  primary_theme: coronal_heating
  secondary_themes: [ion-heating, stochastic-heating, cyclotron-resonance, low-beta]
  missions: [n/a]
  regime: [MHD-scale, ion-scale]
trigger_keywords:
  - "unified ion heating"
  - "low-beta plasma"
  - "test-particle simulation"
  - "stochastic to cyclotron transition"
  - "Johnston 2024 unified"
  - "threshold parameter"
data_products: []
algorithms:
  - name: "Test-particle integration in synthetic Alfvenic turbulence"
    equation_refs: ["TODO verify"]
  - name: "Threshold-parameter scan for heating regime"
    equation_refs: ["TODO verify"]
  - name: "Unified Q_perp / Q_par prediction"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2409.07015"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within low-β test-particle simulations, the predicted ion-heating phenomenology unifies
    stochastic and cyclotron-resonant heating via a single threshold parameter.
  out_of_scope:
    - "Do not extend to high-β regimes without re-validating the synthetic field assumptions."
    - "Do not equate test-particle heating with self-consistent kinetic dissipation."
    - "Do not apply the threshold to observational PSP data without proper rescaling."
failure_modes:
  - "Synthetic Alfven-wave amplitude statistics may not match observations."
  - "Limited simulation duration restricts low-rate channels."
  - "Single-particle treatment ignores collective effects."
  - "Threshold-parameter definition shifts numerical match."
depends_on:
  - paper-bourouaine-2019-stochastic-heating-near-sun
  - paper-klein-2017-stochastic-heating-beta-amplitude
  - paper-chandran-2013-stochastic-heating-alpha-proton
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the unified picture is correct, observed Q_perp / Q_par fractions should follow the predicted threshold curve in PSP low-β intervals."
  - type: minimal_experiment
    statement: "Overlay predicted threshold curve against PSP low-β heating-rate inferences from radial gradients."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2409.07015v5)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, coronal_heating]
---

# Zade Johnston et al. 2024 — A Unified Phenomenology of Ion Heating in Low-β Plasmas: Tes... — paper-skill

> Compiled from arXiv:2409.07015. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Test-particle simulations in synthetic turbulent fields yield a unified low-β ion-heating phenomenology bridging stochastic and cyclotron-resonant regimes through a single threshold parameter.
- Deciding whether coronal_heating-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- high-β regime
- self-consistent dissipation quantification

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Test-particle simulations in synthetic turbulent fields yield a unified low-β ion-heating phenomenology bridging stochastic and cyclotron-resonant regimes through a single threshold parameter.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Test-particle integration in synthetic Alfvenic turbulence
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Threshold-parameter scan for heating regime
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Unified Q_perp / Q_par prediction
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Synthetic Alfven-wave amplitude statistics may not match observations.
- Limited simulation duration restricts low-rate channels.
- Single-particle treatment ignores collective effects.
- Threshold-parameter definition shifts numerical match.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within low-β test-particle simulations, the predicted ion-heating phenomenology unifies stochastic and cyclotron-resonant heating via a single threshold parameter.

**Out of scope — do NOT generalize beyond:**

- Do not extend to high-β regimes without re-validating the synthetic field assumptions.
- Do not equate test-particle heating with self-consistent kinetic dissipation.
- Do not apply the threshold to observational PSP data without proper rescaling.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2409.07015
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-bourouaine-2019-stochastic-heating-near-sun]] — sibling/upstream context for the same physics domain.
- [[paper-klein-2017-stochastic-heating-beta-amplitude]] — sibling/upstream context for the same physics domain.
- [[paper-chandran-2013-stochastic-heating-alpha-proton]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If the unified picture is correct, observed Q_perp / Q_par fractions should follow the predicted threshold curve in PSP low-β intervals.
- **Minimal_experiment** — Overlay predicted threshold curve against PSP low-β heating-rate inferences from radial gradients.
