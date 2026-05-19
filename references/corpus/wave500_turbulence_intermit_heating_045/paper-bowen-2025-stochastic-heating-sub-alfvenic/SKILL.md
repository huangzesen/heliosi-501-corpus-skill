---
name: paper-bowen-2025-stochastic-heating-sub-alfvenic
description: >-
  Use when working with the central claim of Trevor A. Bowen et al. 2025 — Stochastic-
  heating diagnostics (delta-B_perp / B threshold criterion) applied to PSP encounter
  intervals that crossed into the sub-Alfvenic regime show stochastic heating remains active
  and consistent with established threshold criteria. (arXiv:2509.20654; venue TODO verify).
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
  title: "Stochastic Heating in the Sub-Alfvénic Solar Wind"
  first_author: "Trevor A. Bowen"
  authors:
    - "Trevor A. Bowen"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2509.20654"
  ads_bibcode: null
domain:
  primary_theme: coronal_heating
  secondary_themes: [stochastic-heating, sub-alfvenic, PSP]
  missions: [PSP]
  regime: [sub-Alfvenic, inner-heliosphere, ion-scale]
trigger_keywords:
  - "stochastic heating sub-Alfvenic"
  - "delta-B_perp threshold"
  - "PSP E14+"
  - "stochastic-heating amplitude"
  - "Bowen 2025 sub-Alfvenic"
  - "ion gyromotion chaos"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "high-rate", interval: "PSP E14+ sub-Alfvenic intervals", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Stochastic-heating threshold criterion delta-B_perp/B"
    equation_refs: ["TODO verify"]
  - name: "Sub-Alfvenic interval selection by Mach number"
    equation_refs: ["TODO verify"]
  - name: "Stochastic-heating rate Q_perp estimate"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2509.20654"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Stochastic-heating threshold diagnostic on PSP sub-Alfvenic intervals (encounter set TODO
    verify) shows continued activity consistent with the Chandran-style criterion.
  out_of_scope:
    - "Do not generalise the result to all PSP sub-Alfvenic intervals without the same window-selection rule."
    - "Do not equate the diagnostic with absolute Q_perp absent a calibrated normalisation."
    - "Do not export to electron heating channels."
failure_modes:
  - "Threshold criterion's normalisation depends on β_p and δB scale."
  - "Sub-Alfvenic samples are statistically small."
  - "Spectrum-amplitude estimator (PSD vs structure function) shifts threshold."
  - "Wave activity inside threshold window can bias δB_perp."
depends_on:
  - paper-bourouaine-2019-stochastic-heating-near-sun
  - paper-klein-2017-stochastic-heating-beta-amplitude
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill quantifies stochastic vs cyclotron-resonant partition specifically in sub-Alfvenic intervals."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2509.20654v1) / apj_aa #1.20"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, coronal_heating]
---

# Trevor A. Bowen et al. 2025 — Stochastic Heating in the Sub-Alfvénic Solar Wind — paper-skill

> Compiled from arXiv:2509.20654. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Stochastic-heating diagnostics (delta-B_perp / B threshold criterion) applied to PSP encounter intervals that crossed into the sub-Alfvenic regime show stochastic heating remains active and consistent with established threshold criteria.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether coronal_heating-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- electron-heating channel
- global Q_perp without normalisation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Stochastic-heating diagnostics (delta-B_perp / B threshold criterion) applied to PSP encounter intervals that crossed into the sub-Alfvenic regime show stochastic heating remains active and consistent with established threshold criteria.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Stochastic-heating threshold criterion delta-B_perp/B
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Sub-Alfvenic interval selection by Mach number
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Stochastic-heating rate Q_perp estimate
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | high-rate | PSP E14+ sub-Alfvenic intervals | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Threshold criterion's normalisation depends on β_p and δB scale.
- Sub-Alfvenic samples are statistically small.
- Spectrum-amplitude estimator (PSD vs structure function) shifts threshold.
- Wave activity inside threshold window can bias δB_perp.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Stochastic-heating threshold diagnostic on PSP sub-Alfvenic intervals (encounter set TODO verify) shows continued activity consistent with the Chandran-style criterion.

**Out of scope — do NOT generalize beyond:**

- Do not generalise the result to all PSP sub-Alfvenic intervals without the same window-selection rule.
- Do not equate the diagnostic with absolute Q_perp absent a calibrated normalisation.
- Do not export to electron heating channels.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2509.20654
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-bourouaine-2019-stochastic-heating-near-sun]] — sibling/upstream context for the same physics domain.
- [[paper-klein-2017-stochastic-heating-beta-amplitude]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill quantifies stochastic vs cyclotron-resonant partition specifically in sub-Alfvenic intervals.
