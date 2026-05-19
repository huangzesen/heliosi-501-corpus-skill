---
name: paper-davis-2023-1f-evolution-single-fast-stream
description: >-
  Use when working with the central claim of Nooshin Davis et al. 2023 — In a single fast-
  wind stream sampled by PSP Encounter 10 between 17.4 and 45.7 R_sun, the low-frequency
  spectral index below f_b decreases from ~-0.61 to ~-0.94 as r increases, indicating
  dynamic in-situ formation rather than a coronal origin of the 1/f range.
  (arXiv:2303.01663; venue TODO verify).
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
  title: "The Evolution of the 1/f Range Within a Single Fast-Solar-Wind Stream Between 17.4 and 45.7 Solar Radii"
  first_author: "Nooshin Davis"
  authors:
    - "Nooshin Davis"
    - "B. D. G. Chandran"
    - "T. A. Bowen"
    - "S. T. Badman"
    - "T. Dudok de Wit"
    - "C. H. K. Chen"
    - "S. D. Bale"
    - "Zesen Huang"
    - "Nikos Sioulas"
    - "Marco Velli"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2303.01663"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [one-over-f, radial-evolution, spectral-index]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "1/f range dynamic origin"
  - "PSP Encounter 10 fast scan"
  - "single-stream radial evolution"
  - "low-frequency spectral index"
  - "f_b break frequency"
  - "Davis Chandran Bowen Badman 2023"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "PSP E10, 17.4-45.7 R_sun", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Single-stream tracking with PSP fast radial scan"
    equation_refs: ["TODO verify"]
  - name: "Below-break low-frequency spectral-index fit"
    equation_refs: ["TODO verify"]
  - name: "Radial trend regression on alpha_LF(r)"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2303.01663"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the single PSP-E10 fast stream between 17.4 and 45.7 R_sun, the low-frequency
    spectral index below the break decreases from ~-0.61 to ~-0.94 with r.
  out_of_scope:
    - "Do not generalise the single-stream radial trend to a population mean without statistical extension."
    - "Do not extrapolate alpha_LF(r) below 17.4 R_sun."
    - "Do not export to slow-wind streams."
failure_modes:
  - "Stream-tracking assumption fragile across stream-stream interfaces."
  - "Break-frequency identification couples to f_b model."
  - "Trace vs component-spectrum convention shifts alpha_LF by ~0.05."
  - "Finite-window edge effects at the lowest frequencies."
depends_on:
  - huang-2023-psp-one-over-f-spectrum
  - paper-brodiano-2025-intermittent-1f-spectrum-pristine
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill provides a slow-wind single-stream radial trend of alpha_LF."
  - type: hypothesis
    statement: "If the dynamic-origin picture holds, alpha_LF should approach -1 with increasing advection time across multiple encounters."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2303.01663v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Nooshin Davis et al. 2023 — The Evolution of the 1/f Range Within a Single Fast-Solar-Wi... — paper-skill

> Compiled from arXiv:2303.01663. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- In a single fast-wind stream sampled by PSP Encounter 10 between 17.4 and 45.7 R_sun, the low-frequency spectral index below f_b decreases from ~-0.61 to ~-0.94 as r increases, indicating dynamic in-situ formation rather than a coronal origin of the 1/f range.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- population-level inference
- slow-wind extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** In a single fast-wind stream sampled by PSP Encounter 10 between 17.4 and 45.7 R_sun, the low-frequency spectral index below f_b decreases from ~-0.61 to ~-0.94 as r increases, indicating dynamic in-situ formation rather than a coronal origin of the 1/f range.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Single-stream tracking with PSP fast radial scan
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Below-break low-frequency spectral-index fit
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Radial trend regression on alpha_LF(r)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | PSP E10, 17.4-45.7 R_sun | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Stream-tracking assumption fragile across stream-stream interfaces.
- Break-frequency identification couples to f_b model.
- Trace vs component-spectrum convention shifts alpha_LF by ~0.05.
- Finite-window edge effects at the lowest frequencies.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the single PSP-E10 fast stream between 17.4 and 45.7 R_sun, the low-frequency spectral index below the break decreases from ~-0.61 to ~-0.94 with r.

**Out of scope — do NOT generalize beyond:**

- Do not generalise the single-stream radial trend to a population mean without statistical extension.
- Do not extrapolate alpha_LF(r) below 17.4 R_sun.
- Do not export to slow-wind streams.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2303.01663
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[huang-2023-psp-one-over-f-spectrum]] — sibling/upstream context for the same physics domain.
- [[paper-brodiano-2025-intermittent-1f-spectrum-pristine]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill provides a slow-wind single-stream radial trend of alpha_LF.
- **Hypothesis** — If the dynamic-origin picture holds, alpha_LF should approach -1 with increasing advection time across multiple encounters.
