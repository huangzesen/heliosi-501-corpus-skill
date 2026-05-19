---
name: paper-kilpua-2025-shock-effect-turbulence-parameters
description: >-
  Use when working with the central claim of Emilia Kilpua et al. 2025 — Interplanetary-
  shock crossings systematically modify post-shock turbulence parameters (correlation
  length, spectral slope, PVI distribution) relative to pre-shock ambient values.
  (arXiv:2505.04450; venue TODO verify).
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
  title: "Effect of interplanetary shock waves on turbulence parameters"
  first_author: "Emilia Kilpua"
  authors:
    - "Emilia Kilpua"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2505.04450"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [shocks, correlation-length, intermittency]
  missions: [other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "IP shock turbulence modification"
  - "post-shock correlation length"
  - "spectral slope across shock"
  - "Kilpua 2025 IP shock"
  - "PVI distribution shock"
data_products:
  - {instrument: "Multi-mission MAG + plasma at IP shocks", level: "L2/L3", cadence: "TODO verify", interval: "Catalogued IP shocks", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Shock-crossing catalogue join"
    equation_refs: ["TODO verify"]
  - name: "Pre/post-shock correlation length and spectral slope"
    equation_refs: ["TODO verify"]
  - name: "PVI distribution change across shock"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2505.04450"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Pre/post-shock turbulence-parameter contrast on the analysed IP-shock sample.
  out_of_scope:
    - "Do not attribute the contrast to a single shock-process without ruling out upstream/downstream stream differences."
    - "Do not generalise across Mach-number bins outside the sample."
    - "Do not equate post-shock parameters with sheath-only or driver-only sub-windows without re-conditioning."
failure_modes:
  - "Pre/post window length choice biases parameter estimates."
  - "Shock-normal direction uncertainty."
  - "Sample size per Mach bin is limited."
  - "Driver vs sheath mixing in post-shock window."
depends_on:
  - paper-good-2025-residual-energy-mhd-shocks
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill provides the same contrast specifically for collisionless quasi-perpendicular shocks."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2505.04450v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Emilia Kilpua et al. 2025 — Effect of interplanetary shock waves on turbulence parameter... — paper-skill

> Compiled from arXiv:2505.04450. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Interplanetary-shock crossings systematically modify post-shock turbulence parameters (correlation length, spectral slope, PVI distribution) relative to pre-shock ambient values.
- Reproducing or extending the analysis around Multi-mission MAG + plasma at IP shocks.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- unconditioned driver/sheath mixing
- single-Mach-bin extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Interplanetary-shock crossings systematically modify post-shock turbulence parameters (correlation length, spectral slope, PVI distribution) relative to pre-shock ambient values.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Shock-crossing catalogue join
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Pre/post-shock correlation length and spectral slope
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### PVI distribution change across shock
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Multi-mission MAG + plasma at IP shocks | L2/L3 | TODO verify | Catalogued IP shocks | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Pre/post window length choice biases parameter estimates.
- Shock-normal direction uncertainty.
- Sample size per Mach bin is limited.
- Driver vs sheath mixing in post-shock window.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Pre/post-shock turbulence-parameter contrast on the analysed IP-shock sample.

**Out of scope — do NOT generalize beyond:**

- Do not attribute the contrast to a single shock-process without ruling out upstream/downstream stream differences.
- Do not generalise across Mach-number bins outside the sample.
- Do not equate post-shock parameters with sheath-only or driver-only sub-windows without re-conditioning.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2505.04450
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-good-2025-residual-energy-mhd-shocks]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill provides the same contrast specifically for collisionless quasi-perpendicular shocks.
