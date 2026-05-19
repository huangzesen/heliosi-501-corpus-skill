---
name: paper-romanelli-2024-incompressible-cascade-upstream-mars
description: >-
  Use when working with the central claim of Norberto Romanelli et al. 2024 — The
  incompressible Politano-Pouquet cascade rate evaluated upstream of Mars (MAVEN data)
  yields a quantifiable ε with dependence on solar-wind conditions distinct from 1-au
  reference values. (arXiv:2406.18349; venue TODO verify).
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
  title: "The Incompressible Magnetohydrodynamic Energy Cascade Rate Upstream of Mars"
  first_author: "Norberto Romanelli"
  authors:
    - "Norberto Romanelli"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2406.18349"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [cascade-rate, Mars, MAVEN, exact-relation]
  missions: [MAVEN]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "MAVEN solar wind cascade"
  - "upstream of Mars"
  - "Politano-Pouquet at Mars"
  - "Romanelli 2024 cascade rate"
  - "incompressible MHD cascade"
data_products:
  - {instrument: "MAVEN MAG", level: "L2", cadence: "TODO verify cadence", interval: "MAVEN solar-wind intervals upstream of Mars", archive: "SPDF / MAVEN SOC"}
  - {instrument: "MAVEN SWIA", level: "L2", cadence: "TODO verify", interval: "Same", archive: "SPDF / MAVEN SOC"}
algorithms:
  - name: "PP exact relation on MAVEN MAG upstream of Mars"
    equation_refs: ["TODO verify"]
  - name: "Upstream interval selection (clear of bow-shock)"
    equation_refs: ["TODO verify"]
  - name: "Comparison vs 1-au reference cascade rate"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2406.18349"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    PP cascade rate ε upstream of Mars on the MAVEN sample analysed, vs a 1-au reference set.
  out_of_scope:
    - "Do not use intervals contaminated by the Martian bow-shock foreshock."
    - "Do not extrapolate the Mars-orbit ε to other heliocentric distances without re-fitting."
    - "Do not equate the ε value with absolute dissipation in the Martian magnetosphere."
failure_modes:
  - "Foreshock contamination biases cascade rate."
  - "SWIA moments uncertainty propagates."
  - "Local-mean-field choice at limited cadence affects projection."
  - "Sample-size limitations during specific seasons."
depends_on:
  - paper-andres-2021-incompressible-cascade-anisotropic-pp
  - paper-bandyopadhyay-2020-energy-transfer-psp
adapter_notes: []
research_generation_affordances:
  - type: minimal_experiment
    statement: "Recompute ε with stricter foreshock-exclusion and quantify shift."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2406.18349v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Norberto Romanelli et al. 2024 — The Incompressible Magnetohydrodynamic Energy Cascade Rate U... — paper-skill

> Compiled from arXiv:2406.18349. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- The incompressible Politano-Pouquet cascade rate evaluated upstream of Mars (MAVEN data) yields a quantifiable ε with dependence on solar-wind conditions distinct from 1-au reference values.
- Reproducing or extending the analysis around MAVEN MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- foreshock-contaminated intervals
- Martian magnetosphere dissipation inference

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** The incompressible Politano-Pouquet cascade rate evaluated upstream of Mars (MAVEN data) yields a quantifiable ε with dependence on solar-wind conditions distinct from 1-au reference values.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### PP exact relation on MAVEN MAG upstream of Mars
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Upstream interval selection (clear of bow-shock)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Comparison vs 1-au reference cascade rate
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| MAVEN MAG | L2 | TODO verify cadence | MAVEN solar-wind intervals upstream of Mars | SPDF / MAVEN SOC | fetch+decode CDF; subset by time |
| MAVEN SWIA | L2 | TODO verify | Same | SPDF / MAVEN SOC | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Foreshock contamination biases cascade rate.
- SWIA moments uncertainty propagates.
- Local-mean-field choice at limited cadence affects projection.
- Sample-size limitations during specific seasons.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PP cascade rate ε upstream of Mars on the MAVEN sample analysed, vs a 1-au reference set.

**Out of scope — do NOT generalize beyond:**

- Do not use intervals contaminated by the Martian bow-shock foreshock.
- Do not extrapolate the Mars-orbit ε to other heliocentric distances without re-fitting.
- Do not equate the ε value with absolute dissipation in the Martian magnetosphere.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2406.18349
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-andres-2021-incompressible-cascade-anisotropic-pp]] — sibling/upstream context for the same physics domain.
- [[paper-bandyopadhyay-2020-energy-transfer-psp]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Minimal_experiment** — Recompute ε with stricter foreshock-exclusion and quantify shift.
