---
name: paper-mcintyre-2024-helicity-barrier-transition-range
description: >-
  Use when working with the central claim of J. R. McIntyre et al. 2024 — Statistical
  analysis of the ion-scale transition-range magnetic spectrum at 1 au shows a steepening
  behaviour consistent with the helicity-barrier prediction for strongly imbalanced
  turbulence. (arXiv:2407.10815; venue TODO verify).
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
  title: "Evidence for the helicity barrier from measurements of the turbulence transition range"
  first_author: "J. R. McIntyre"
  authors:
    - "J. R. McIntyre"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2407.10815"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [helicity-barrier, ion-scale, spectral-break]
  missions: [other]
  regime: [1au, ion-scale]
trigger_keywords:
  - "helicity barrier observational"
  - "transition-range steepening"
  - "ion-scale spectrum"
  - "imbalanced cross helicity"
  - "McIntyre 2024 helicity barrier"
data_products:
  - {instrument: "In-situ MAG (Wind/Ulysses/etc. TODO verify)", level: "L2", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Ion-scale transition-range power-spectrum fit"
    equation_refs: ["TODO verify"]
  - name: "Imbalance-conditioned subsample selection"
    equation_refs: ["TODO verify"]
  - name: "Comparison to helicity-barrier prediction"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2407.10815"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Observational evidence for helicity-barrier-driven spectral steepening in the ion-scale
    transition range of the analysed 1-au dataset, conditioned on imbalance.
  out_of_scope:
    - "Do not assert helicity barrier is unique cause without a competing-model discriminator."
    - "Do not extrapolate the result to balanced turbulence."
    - "Do not equate transition-range slope with a specific dissipation channel."
failure_modes:
  - "Transition-range fit window depends on β."
  - "Imbalance-conditioning threshold sensitivity."
  - "Local-mean-field choice shifts the spectrum."
  - "Spectral leakage from inertial range affects transition-range slope."
depends_on:
  - paper-sasmal-2026-helicity-barrier-flr-mhd-heating
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If helicity barrier holds at near-Sun, PSP highly imbalanced intervals should show the same transition-range steepening."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2407.10815v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# J. R. McIntyre et al. 2024 — Evidence for the helicity barrier from measurements of the t... — paper-skill

> Compiled from arXiv:2407.10815. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Statistical analysis of the ion-scale transition-range magnetic spectrum at 1 au shows a steepening behaviour consistent with the helicity-barrier prediction for strongly imbalanced turbulence.
- Reproducing or extending the analysis around In-situ MAG (Wind/Ulysses/etc. TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- balanced-turbulence intervals
- dissipation-channel attribution

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Statistical analysis of the ion-scale transition-range magnetic spectrum at 1 au shows a steepening behaviour consistent with the helicity-barrier prediction for strongly imbalanced turbulence.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Ion-scale transition-range power-spectrum fit
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Imbalance-conditioned subsample selection
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Comparison to helicity-barrier prediction
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ MAG (Wind/Ulysses/etc. TODO verify) | L2 | TODO verify | TODO verify | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Transition-range fit window depends on β.
- Imbalance-conditioning threshold sensitivity.
- Local-mean-field choice shifts the spectrum.
- Spectral leakage from inertial range affects transition-range slope.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Observational evidence for helicity-barrier-driven spectral steepening in the ion-scale transition range of the analysed 1-au dataset, conditioned on imbalance.

**Out of scope — do NOT generalize beyond:**

- Do not assert helicity barrier is unique cause without a competing-model discriminator.
- Do not extrapolate the result to balanced turbulence.
- Do not equate transition-range slope with a specific dissipation channel.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2407.10815
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-sasmal-2026-helicity-barrier-flr-mhd-heating]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If helicity barrier holds at near-Sun, PSP highly imbalanced intervals should show the same transition-range steepening.
