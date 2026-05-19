---
name: paper-good-2025-residual-energy-mhd-shocks
description: >-
  Use when working with the central claim of S. W. Good et al. 2025 — MHD-shock theory
  predicts a specific residual-energy (magnetic-minus-kinetic) signature across the shock
  front, validated against an interplanetary-shock observational set. (arXiv:2509.20096;
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
  title: "Residual energy of magnetohydrodynamic shocks"
  first_author: "S. W. Good"
  authors:
    - "S. W. Good"
    - "K. J. Palmunen"
    - "C. H. K. Chen"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2509.20096"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [residual-energy, shocks, interplanetary]
  missions: [other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "residual energy shock"
  - "MHD shock magnetic-kinetic"
  - "interplanetary shock observation"
  - "Good Palmunen Chen 2025"
  - "Rankine-Hugoniot residual"
data_products:
  - {instrument: "Multi-mission MAG + plasma at IP shocks (TODO verify)", level: "L2/L3", cadence: "TODO verify", interval: "Catalogued IP shocks", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "MHD-shock Rankine-Hugoniot expansion to derive residual-energy signature"
    equation_refs: ["TODO verify Eq."]
  - name: "Interplanetary-shock catalogue cross-match"
    equation_refs: ["TODO verify"]
  - name: "Observed vs predicted Δ(magnetic-kinetic) comparison"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2509.20096"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Derived residual-energy signature across MHD shocks and its agreement with the observed
    IP-shock sample over the studied parameter range.
  out_of_scope:
    - "Do not extrapolate the residual-energy prediction to collisionless quasi-perpendicular shocks without re-derivation."
    - "Do not generalise to internal-shock structures inside ICMEs without re-selection."
    - "Do not assume validity outside the Mach-number / beta range tested."
failure_modes:
  - "Shock identification (timing, normal direction) propagates into Δ(magnetic-kinetic)."
  - "Plasma-moment uncertainty dominates kinetic energy."
  - "Compressibility deviations from the closed-form derivation."
  - "Sample size per Mach bin is limited."
depends_on: []
adapter_notes: []
research_generation_affordances:
  - type: minimal_experiment
    statement: "Apply the predicted Δ(magnetic-kinetic) law to a PSP IP-shock catalogue and verify across multiple Mach bins."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 item 7 / theme_turbulence.json"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# S. W. Good et al. 2025 — Residual energy of magnetohydrodynamic shocks — paper-skill

> Compiled from arXiv:2509.20096. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- MHD-shock theory predicts a specific residual-energy (magnetic-minus-kinetic) signature across the shock front, validated against an interplanetary-shock observational set.
- Reproducing or extending the analysis around Multi-mission MAG + plasma at IP shocks (TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- intra-ICME structures
- collisionless quasi-perp shocks without re-derivation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** MHD-shock theory predicts a specific residual-energy (magnetic-minus-kinetic) signature across the shock front, validated against an interplanetary-shock observational set.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### MHD-shock Rankine-Hugoniot expansion to derive residual-energy signature
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Interplanetary-shock catalogue cross-match
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Observed vs predicted Δ(magnetic-kinetic) comparison
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Multi-mission MAG + plasma at IP shocks (TODO verify) | L2/L3 | TODO verify | Catalogued IP shocks | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Shock identification (timing, normal direction) propagates into Δ(magnetic-kinetic).
- Plasma-moment uncertainty dominates kinetic energy.
- Compressibility deviations from the closed-form derivation.
- Sample size per Mach bin is limited.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Derived residual-energy signature across MHD shocks and its agreement with the observed IP-shock sample over the studied parameter range.

**Out of scope — do NOT generalize beyond:**

- Do not extrapolate the residual-energy prediction to collisionless quasi-perpendicular shocks without re-derivation.
- Do not generalise to internal-shock structures inside ICMEs without re-selection.
- Do not assume validity outside the Mach-number / beta range tested.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2509.20096
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

No paper-skill dependencies (self-contained).

**Affordances.**

- **Minimal_experiment** — Apply the predicted Δ(magnetic-kinetic) law to a PSP IP-shock catalogue and verify across multiple Mach bins.
