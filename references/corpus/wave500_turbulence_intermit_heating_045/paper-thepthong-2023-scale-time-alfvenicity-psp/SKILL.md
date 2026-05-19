---
name: paper-thepthong-2023-scale-time-alfvenicity-psp
description: >-
  Use when working with the central claim of Panisara Thepthong et al. 2023 — Alfvenicity
  diagnostics (σ_c, alignment angle) on PSP data show systematic scale dependence and slow
  time-evolution within single encounters, distinguishing genuine Alfvenic regions from
  mixed states. (arXiv:2312.08707; venue TODO verify).
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
  title: "Scale and Time Dependence of Alfvenicity in the Solar Wind as Observed by Parker Solar Probe"
  first_author: "Panisara Thepthong"
  authors:
    - "Panisara Thepthong"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2312.08707"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [alfvenicity, scale-dependence, PSP]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "Alfvenicity scale dependence"
  - "scale-resolved sigma_c"
  - "time-evolution within encounter"
  - "Thepthong 2023 PSP"
  - "alignment angle scale-dependence"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "PSP encounters (TODO verify range)", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Scale-resolved σ_c(τ)"
    equation_refs: ["TODO verify"]
  - name: "Per-encounter time-dependent Alfvenicity evolution"
    equation_refs: ["TODO verify"]
  - name: "Alignment-angle scale-dependence statistics"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2312.08707"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within PSP encounters analysed, Alfvenicity diagnostics show systematic scale dependence
    and intra-encounter time evolution.
  out_of_scope:
    - "Do not equate scale-dependent σ_c with a single physical mechanism."
    - "Do not generalise the time evolution to inter-encounter trends."
    - "Do not export to slow non-Alfvenic streams without re-selection."
failure_modes:
  - "σ_c(τ) requires Elsasser variable construction at high cadence; cadence mismatch biases."
  - "Time-evolution metric depends on chosen window."
  - "Stream-overlap intervals inflate σ_c variance."
  - "Compressibility contamination."
depends_on:
  - damicis-2021-alfvenic-nonalfvenic-psp
  - paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If scale-dependent σ_c reflects ongoing alignment, the slope of σ_c(τ) should correlate with cascade rate ε within the same intervals."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2312.08707v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Panisara Thepthong et al. 2023 — Scale and Time Dependence of Alfvenicity in the Solar Wind a... — paper-skill

> Compiled from arXiv:2312.08707. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Alfvenicity diagnostics (σ_c, alignment angle) on PSP data show systematic scale dependence and slow time-evolution within single encounters, distinguishing genuine Alfvenic regions from mixed states.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- slow non-Alfvenic without re-select
- inter-encounter trend extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Alfvenicity diagnostics (σ_c, alignment angle) on PSP data show systematic scale dependence and slow time-evolution within single encounters, distinguishing genuine Alfvenic regions from mixed states.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Scale-resolved σ_c(τ)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Per-encounter time-dependent Alfvenicity evolution
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Alignment-angle scale-dependence statistics
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | PSP encounters (TODO verify range) | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- σ_c(τ) requires Elsasser variable construction at high cadence; cadence mismatch biases.
- Time-evolution metric depends on chosen window.
- Stream-overlap intervals inflate σ_c variance.
- Compressibility contamination.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within PSP encounters analysed, Alfvenicity diagnostics show systematic scale dependence and intra-encounter time evolution.

**Out of scope — do NOT generalize beyond:**

- Do not equate scale-dependent σ_c with a single physical mechanism.
- Do not generalise the time evolution to inter-encounter trends.
- Do not export to slow non-Alfvenic streams without re-selection.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2312.08707
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[damicis-2021-alfvenic-nonalfvenic-psp]] — sibling/upstream context for the same physics domain.
- [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If scale-dependent σ_c reflects ongoing alignment, the slope of σ_c(τ) should correlate with cascade rate ε within the same intervals.
