---
name: paper-sunkit-image-sunpy-affiliated
description: >-
  Use when a workflow needs SunPy-compatible solar image processing — feature
  tracking, enhancement, time-distance maps, radial filters, active-region
  detection — central claim is that sunkit-image is the official SunPy-
  affiliated image-processing toolbox (no standalone publication located in
  local inventory; cite repository + JOSS where present).
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
  title: sunkit-image — Solar image processing for the SunPy ecosystem
  first_author: sunkit-image developers
  year: 2024
  venue: software package (SunPy affiliated; no dedicated paper in local inventory)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
    - STEREO
    - other
  regime:
    - corona
trigger_keywords:
  - sunkit-image
  - solar image processing Python
  - OCCULT loop tracing
  - radial filter coronagraph
  - SunPy affiliated image
data_products: []
algorithms:
  - name: Radial filtering (Newkirk / Nash style)
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunkit-image"
  - name: Loop tracing (Aschwanden 2008 OCCULT)
    equation_refs: []
    external_implementations: []
  - name: time_distance map (slit along feature)
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/sunpy/sunkit-image"
  data_repo: null
claim_boundary:
  scope: >-
    sunkit-image: SunPy-affiliated package providing radial filtering
    (rsanchez_2015 unsharp mask), trace_loops_2008 (Aschwanden), time_distance,
    multi-Gaussian normalization, peek_at_jet. Consumes sunpy.map.Map.
  out_of_scope:
    - Do not use sunkit-image for non-solar imagery.
    - Do not assume identical algorithms across versions — feature detectors evolve.
failure_modes:
  - Loop tracing parameters need per-image tuning; defaults underperform on noisy data.
  - Radial filter parameters strongly affect quantitative photometry.
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
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
# sunkit-image — Solar image processing for the SunPy ecosystem — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when a workflow needs SunPy-compatible solar image processing — feature tracking, enhancement, time-distance maps, radial filters, active-region detection — central claim is that sunkit-image is the official SunPy-affiliated image-processing toolbox (no standalone publication located in local inventory; cite repository + JOSS where present).

Do NOT use this skill when:

- Do not use sunkit-image for non-solar imagery.
- Do not assume identical algorithms across versions — feature detectors evolve.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** sunkit-image: SunPy-affiliated package providing radial filtering (rsanchez_2015 unsharp mask), trace_loops_2008 (Aschwanden), time_distance, multi-Gaussian normalization, peek_at_jet. Consumes sunpy.map.Map.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Radial filtering (Newkirk / Nash style)

- External implementation(s): https://github.com/sunpy/sunkit-image
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Loop tracing (Aschwanden 2008 OCCULT)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### time_distance map (slit along feature)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote-sensing data dependencies (this skill is purely software / infrastructure or coordinate-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Loop tracing parameters need per-image tuning; defaults underperform on noisy data.
- Radial filter parameters strongly affect quantitative photometry.

## 7. Claim boundary  *(Layer 1)*

**In scope.** sunkit-image: SunPy-affiliated package providing radial filtering (rsanchez_2015 unsharp mask), trace_loops_2008 (Aschwanden), time_distance, multi-Gaussian normalization, peek_at_jet. Consumes sunpy.map.Map.

**Out of scope — do NOT generalize beyond:**

- Do not use sunkit-image for non-solar imagery.
- Do not assume identical algorithms across versions — feature detectors evolve.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://github.com/sunpy/sunkit-image
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- No standalone JOSS/ApJ paper found in local inventory; citation TODO
