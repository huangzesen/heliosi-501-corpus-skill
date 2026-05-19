---
name: paper-pulkkinen-2013-kameleon-ccmc-output-reader
description: >-
  Use when reading or interpolating CCMC simulation outputs (SWMF/BATS-R-US,
  ENLIL, OpenGGCM, MAS) through a uniform API — central claim is that Kameleon
  is the CCMC-supplied reader that exposes diverse simulation grids as common
  interpolation calls (Pulkkinen et al. 2013, Space Weather; Kameleon software
  CCMC).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: "Geospace Environment Modeling 2008–2009 Challenge: Ground Magnetic Field Perturbations and the Kameleon Software"
  first_author: "Pulkkinen, A."
  year: 2013
  venue: Space Weather
  doi: 10.1002/swe.20098
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - MHD-scale
trigger_keywords:
  - Kameleon CCMC
  - Pulkkinen 2013
  - CCMC simulation reader
  - ENLIL output reader
  - SWMF reader
  - iSWA
data_products:
  - instrument: CCMC model outputs (SWMF/ENLIL/OpenGGCM)
    level: simulation L2
    cadence: model-specific
    interval: null
    archive: CCMC runs-on-request
algorithms:
  - name: Unified grid-agnostic interpolation API
    equation_refs: []
    external_implementations:
      - "https://ccmc.gsfc.nasa.gov/Kameleon/"
validation_target: null
links:
  doi_url: "https://doi.org/10.1002/swe.20098"
  arxiv_url: null
  ads_url: null
  code_repo: "https://ccmc.gsfc.nasa.gov/Kameleon/"
  data_repo: "https://ccmc.gsfc.nasa.gov/"
claim_boundary:
  scope: >-
    Kameleon: C++/Python library wrapping CCMC model output formats (.cdf, .dat)
    with a unified interpolation interface (interpolate(x,y,z,var)). Used
    heavily by iSWA and runs-on-request.
  out_of_scope:
    - Do not treat Kameleon as a simulation tool; it is a reader/interpolator.
    - Do not assume Kameleon supports every CCMC model version — check supported-models list.
    - Do not assume the Python wrapper is in active maintenance equal to the C++ core.
failure_modes:
  - Boundary points may return NaN silently when off-grid; check interpolate flag.
  - Mismatched coordinate convention (GSM vs SM) yields wrong field lines.
depends_on:
  []
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# Geospace Environment Modeling 2008–2009 Challenge: Ground Magnetic Field Perturbations and the Kameleon Software — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when reading or interpolating CCMC simulation outputs (SWMF/BATS-R-US, ENLIL, OpenGGCM, MAS) through a uniform API — central claim is that Kameleon is the CCMC-supplied reader that exposes diverse simulation grids as common interpolation calls (Pulkkinen et al. 2013, Space Weather; Kameleon software CCMC).

Do NOT use this skill when:

- Do not treat Kameleon as a simulation tool; it is a reader/interpolator.
- Do not assume Kameleon supports every CCMC model version — check supported-models list.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Kameleon: C++/Python library wrapping CCMC model output formats (.cdf, .dat) with a unified interpolation interface (interpolate(x,y,z,var)). Used heavily by iSWA and runs-on-request.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Unified grid-agnostic interpolation API

- External implementation(s): https://ccmc.gsfc.nasa.gov/Kameleon/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| CCMC model outputs (SWMF/ENLIL/OpenGGCM) | simulation L2 | model-specific | — | CCMC runs-on-request |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Boundary points may return NaN silently when off-grid; check interpolate flag.
- Mismatched coordinate convention (GSM vs SM) yields wrong field lines.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Kameleon: C++/Python library wrapping CCMC model output formats (.cdf, .dat) with a unified interpolation interface (interpolate(x,y,z,var)). Used heavily by iSWA and runs-on-request.

**Out of scope — do NOT generalize beyond:**

- Do not treat Kameleon as a simulation tool; it is a reader/interpolator.
- Do not assume Kameleon supports every CCMC model version — check supported-models list.
- Do not assume the Python wrapper is in active maintenance equal to the C++ core.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1002/swe.20098
- arXiv: n/a
- Code: https://ccmc.gsfc.nasa.gov/Kameleon/
- Data / archive: https://ccmc.gsfc.nasa.gov/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- Pulkkinen 2013 is the GEM-challenge paper that cites Kameleon; no standalone Kameleon paper in local inventory
