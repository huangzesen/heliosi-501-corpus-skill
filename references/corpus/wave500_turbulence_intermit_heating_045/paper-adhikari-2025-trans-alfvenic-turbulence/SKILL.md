---
name: paper-adhikari-2025-trans-alfvenic-turbulence
description: >-
  Use when working with the central claim of Subash Adhikari et al. 2025 — Across PSP
  encounters 8-19, sub-Alfvenic intervals show smaller normalised magnetic-fluctuation
  amplitude and stronger anisotropy than super-Alfvenic intervals, with no polarity-
  reversing (>90 deg) switchbacks in the sub-Alfvenic sample. (arXiv:2510.07472; venue TODO
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
  title: "Characterization of the Trans-Alfvénic Region Using Observations from Parker Solar Probe"
  first_author: "Subash Adhikari"
  authors:
    - "Subash Adhikari"
    - "Riddhi Bandyopadhyay"
    - "Joshua Goodwill"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2510.07472"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [sub-alfvenic, anisotropy, switchbacks]
  missions: [PSP]
  regime: [sub-Alfvenic, super-Alfvenic, inner-heliosphere, MHD-scale]
trigger_keywords:
  - "trans-Alfvenic region"
  - "sub-Alfvenic PSP"
  - "normalised fluctuation amplitude"
  - "anisotropy contrast"
  - ">90 degree switchback absence"
  - "Adhikari Bandyopadhyay Goodwill 2025"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "PSP E8-E19", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Sub-/super-Alfvenic interval selection by Mach number"
    equation_refs: ["TODO verify"]
  - name: "Normalised magnetic-fluctuation amplitude statistics"
    equation_refs: ["TODO verify"]
  - name: "Anisotropy diagnostics (per-direction structure function or spectrum)"
    equation_refs: ["TODO verify"]
  - name: "Switchback deflection-angle catalogue cross-match"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2510.07472"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    PSP E8-E19 sub-Alfvenic vs super-Alfvenic statistical contrast in normalised fluctuation
    amplitude, anisotropy, and presence of >90 deg deflections.
  out_of_scope:
    - "Do not generalise to encounters outside E8-E19 without re-selection."
    - "Do not infer absence of small-deflection switchbacks from absence of >90 deg ones."
    - "Do not extend to slow-Alfvenic streams under different selection criteria."
failure_modes:
  - "Mach-number estimation depends on density source (SPC vs derived)."
  - "Sub-Alfvenic intervals are statistically small; report N."
  - "Sampling-angle bias differs between sub-/super-Alfvenic populations."
  - "Switchback catalogue threshold dependence."
depends_on:
  - adhikari-2026-alfven-transition-young-solar-wind-solar-max
  - kasper-2021-psp-enters-magnetically-dominated-corona
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill quantifies trans-Alfvenic turbulence in slow-Alfvenic streams specifically."
  - type: hypothesis
    statement: "If anisotropy enhancement persists in sub-Alfvenic regime, anisotropic ε should also be larger in sub-Alfvenic bins."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 item 6"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Subash Adhikari et al. 2025 — Characterization of the Trans-Alfvénic Region Using Observat... — paper-skill

> Compiled from arXiv:2510.07472. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Across PSP encounters 8-19, sub-Alfvenic intervals show smaller normalised magnetic-fluctuation amplitude and stronger anisotropy than super-Alfvenic intervals, with no polarity-reversing (>90 deg) switchbacks in the sub-Alfvenic sample.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- encounter range outside E8-E19
- slow-Alfvenic-specific conclusions without re-selection

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Across PSP encounters 8-19, sub-Alfvenic intervals show smaller normalised magnetic-fluctuation amplitude and stronger anisotropy than super-Alfvenic intervals, with no polarity-reversing (>90 deg) switchbacks in the sub-Alfvenic sample.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Sub-/super-Alfvenic interval selection by Mach number
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Normalised magnetic-fluctuation amplitude statistics
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Anisotropy diagnostics (per-direction structure function or spectrum)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Switchback deflection-angle catalogue cross-match
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | PSP E8-E19 | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Mach-number estimation depends on density source (SPC vs derived).
- Sub-Alfvenic intervals are statistically small; report N.
- Sampling-angle bias differs between sub-/super-Alfvenic populations.
- Switchback catalogue threshold dependence.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PSP E8-E19 sub-Alfvenic vs super-Alfvenic statistical contrast in normalised fluctuation amplitude, anisotropy, and presence of >90 deg deflections.

**Out of scope — do NOT generalize beyond:**

- Do not generalise to encounters outside E8-E19 without re-selection.
- Do not infer absence of small-deflection switchbacks from absence of >90 deg ones.
- Do not extend to slow-Alfvenic streams under different selection criteria.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2510.07472
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]] — sibling/upstream context for the same physics domain.
- [[kasper-2021-psp-enters-magnetically-dominated-corona]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill quantifies trans-Alfvenic turbulence in slow-Alfvenic streams specifically.
- **Hypothesis** — If anisotropy enhancement persists in sub-Alfvenic regime, anisotropic ε should also be larger in sub-Alfvenic bins.
