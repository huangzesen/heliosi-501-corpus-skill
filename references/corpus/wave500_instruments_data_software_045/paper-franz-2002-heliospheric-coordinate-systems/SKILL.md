---
name: paper-franz-2002-heliospheric-coordinate-systems
description: >-
  Use when transforming heliophysics vectors among GSE, GSM, HEE, HEEQ, HCI,
  RTN, and Carrington frames — central claim is that Fränz & Harper (2002)
  provide closed-form algorithms and definitions for the major heliospheric
  coordinate systems (with errata) that anchor every multi-mission analysis.
version: 0.1.0
kind: paper-skill
quality: method-ready
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: Heliospheric Coordinate Systems
  first_author: "Fränz, M."
  year: 2002
  venue: Planetary and Space Science
  doi: 10.1016/S0032-0633(01)00119-2
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - 1au
    - inner-heliosphere
    - corona
trigger_keywords:
  - heliospheric coordinates
  - Fränz Harper 2002
  - GSE GSM HEEQ
  - Carrington longitude
  - RTN frame
  - coordinate transformation
  - HCI HEEQ HEE
  - Stonyhurst heliographic
data_products: []
algorithms:
  - name: GSE↔GSM via dipole tilt angle
    equation_refs:
      - "Fränz & Harper 2002 §3"
    external_implementations:
      - github.com/spacepy/spacepy (CoordTransform)
  - name: HEEQ↔HCI via Carrington solar rotation
    equation_refs:
      - §4
    external_implementations:
      - sunpy.coordinates
validation_target: null
links:
  doi_url: "https://doi.org/10.1016/S0032-0633(01)00119-2"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Fränz & Harper (2002) define and inter-relate: GEI, GEO, GSE, GSM, SM, MAG,
    HEE, HAE, HEEQ, HCI, HCD, HGRTN. Includes Carrington longitude / latitude.
    An erratum (2007) corrects sign / rotation issues.
  out_of_scope:
    - Do not skip the 2007 erratum — several rotation matrices are corrected.
    - Do not assume RTN/HGRTN are spacecraft-centric without specifying which spacecraft.
    - Do not confuse HEEQ (Stonyhurst) with HCI (inertial heliocentric).
failure_modes:
  - Sign errors propagate silently — verify a known test vector after any transform chain.
  - Carrington longitude conventions differ (synodic vs. sidereal) across packages.
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
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# Heliospheric Coordinate Systems — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when transforming heliophysics vectors among GSE, GSM, HEE, HEEQ, HCI, RTN, and Carrington frames — central claim is that Fränz & Harper (2002) provide closed-form algorithms and definitions for the major heliospheric coordinate systems (with errata) that anchor every multi-mission analysis.

Do NOT use this skill when:

- Do not skip the 2007 erratum — several rotation matrices are corrected.
- Do not assume RTN/HGRTN are spacecraft-centric without specifying which spacecraft.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Fränz & Harper (2002) define and inter-relate: GEI, GEO, GSE, GSM, SM, MAG, HEE, HAE, HEEQ, HCI, HCD, HGRTN. Includes Carrington longitude / latitude. An erratum (2007) corrects sign / rotation issues.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### GSE↔GSM via dipole tilt angle

- Paper reference: Fränz & Harper 2002 §3
- External implementation(s): github.com/spacepy/spacepy (CoordTransform)
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### HEEQ↔HCI via Carrington solar rotation

- Paper reference: §4
- External implementation(s): sunpy.coordinates
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote-sensing data dependencies (this skill is purely software / infrastructure or coordinate-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Sign errors propagate silently — verify a known test vector after any transform chain.
- Carrington longitude conventions differ (synodic vs. sidereal) across packages.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Fränz & Harper (2002) define and inter-relate: GEI, GEO, GSE, GSM, SM, MAG, HEE, HAE, HEEQ, HCI, HCD, HGRTN. Includes Carrington longitude / latitude. An erratum (2007) corrects sign / rotation issues.

**Out of scope — do NOT generalize beyond:**

- Do not skip the 2007 erratum — several rotation matrices are corrected.
- Do not assume RTN/HGRTN are spacecraft-centric without specifying which spacecraft.
- Do not confuse HEEQ (Stonyhurst) with HCI (inertial heliocentric).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1016/S0032-0633(01)00119-2
- arXiv: n/a
- Code: n/a
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- 2007 erratum not always tracked in citing software
