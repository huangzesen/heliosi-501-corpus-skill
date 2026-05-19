---
name: paper-sharma-2026-subion-current-sheets-kaw-pic
description: >-
  Use when working with the central claim of Johan Sharma et al. 2026 — PIC simulations of
  KAW-driven turbulence resolving electron scales show formation of sub-ion current sheets
  and intermittent coherent structures that mediate dissipation at sub-ion scales.
  (arXiv:2601.18131; venue TODO verify).
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
  title: "Sub-ion scale current sheets in kinetic Alfvén wave turbulence"
  first_author: "Johan Sharma"
  authors:
    - "Johan Sharma"
    - "Ch Akshath Kumar"
    - "Kirit D. Makwana"
  year: 2026
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2601.18131"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [kinetic-scale, current-sheets, PIC-simulation, KAW]
  missions: [n/a]
  regime: [kinetic, electron-scale]
trigger_keywords:
  - "KAW turbulence PIC"
  - "sub-ion current sheets"
  - "electron-scale resolution"
  - "coherent structures"
  - "Sharma Kumar Makwana 2026"
  - "intermittent dissipation"
data_products:
  - {instrument: "PIC simulation outputs (3D EM fields, particles)", level: "derived", cadence: "TODO verify dt", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "PIC simulation of KAW-driven turbulence with electron-scale resolution"
    equation_refs: ["TODO verify"]
  - name: "Current-sheet identification and statistics in the simulation domain"
    equation_refs: ["TODO verify"]
  - name: "Sub-ion power-spectrum analysis"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2601.18131"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Sub-ion current-sheet statistics in fully kinetic PIC simulations of KAW-driven turbulence
    with electron-scale resolution.
  out_of_scope:
    - "Do not directly map simulation parameters (β, mass ratio, box size) to solar-wind plasma without scaling discussion."
    - "Do not equate simulation sub-ion sheets with observed PSP current sheets without an observational matched analysis."
    - "Do not extend results to MHD inertial range."
failure_modes:
  - "Reduced ion/electron mass ratio biases scale separation."
  - "Box-size limits restrict outer-scale energy."
  - "Numerical heating contaminates dissipation diagnostics."
  - "Initial conditions can pre-imprint coherent structures."
depends_on: []
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If sub-ion current sheets dominate dissipation, observed PVI distributions at sub-ion lags should match simulated PVI within tolerance."
  - type: minimal_experiment
    statement: "Compute PVI(τ) at sub-ion lags on PSP burst-mode MAG and overlay simulated distribution."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 item 3"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Johan Sharma et al. 2026 — Sub-ion scale current sheets in kinetic Alfvén wave turbulen... — paper-skill

> Compiled from arXiv:2601.18131. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- PIC simulations of KAW-driven turbulence resolving electron scales show formation of sub-ion current sheets and intermittent coherent structures that mediate dissipation at sub-ion scales.
- Reproducing or extending the analysis around PIC simulation outputs (3D EM fields, particles).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- direct dimensional comparison without scaling
- MHD inertial-range extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PIC simulations of KAW-driven turbulence resolving electron scales show formation of sub-ion current sheets and intermittent coherent structures that mediate dissipation at sub-ion scales.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### PIC simulation of KAW-driven turbulence with electron-scale resolution
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Current-sheet identification and statistics in the simulation domain
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Sub-ion power-spectrum analysis
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PIC simulation outputs (3D EM fields, particles) | derived | TODO verify dt | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Reduced ion/electron mass ratio biases scale separation.
- Box-size limits restrict outer-scale energy.
- Numerical heating contaminates dissipation diagnostics.
- Initial conditions can pre-imprint coherent structures.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Sub-ion current-sheet statistics in fully kinetic PIC simulations of KAW-driven turbulence with electron-scale resolution.

**Out of scope — do NOT generalize beyond:**

- Do not directly map simulation parameters (β, mass ratio, box size) to solar-wind plasma without scaling discussion.
- Do not equate simulation sub-ion sheets with observed PSP current sheets without an observational matched analysis.
- Do not extend results to MHD inertial range.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2601.18131
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

No paper-skill dependencies (self-contained).

**Affordances.**

- **Hypothesis** — If sub-ion current sheets dominate dissipation, observed PVI distributions at sub-ion lags should match simulated PVI within tolerance.
- **Minimal_experiment** — Compute PVI(τ) at sub-ion lags on PSP burst-mode MAG and overlay simulated distribution.
