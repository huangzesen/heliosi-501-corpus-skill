---
name: paper-freeland-1998-solarsoft-ssw-idl-ecosystem
description: >-
  Use when an analysis still depends on IDL-based SolarSoft (SSW) routines (many
  SOHO/STEREO/SDO instrument preps remain SSW-canonical) or when porting a SSW
  workflow to Python — central claim is that SolarSoft is the umbrella IDL/UNIX
  shell ecosystem unifying mission instrument analysis libraries (Freeland &
  Handy 1998, Sol. Phys.).
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
  title: Data analysis with the SolarSoft system
  first_author: "Freeland, S. L."
  year: 1998
  venue: Solar Physics
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - corona
    - 1au
trigger_keywords:
  - SolarSoft
  - SSW
  - Freeland 1998
  - IDL heliophysics
  - aia_prep
  - eit_prep
  - secchi_prep
  - ssw_upgrade
data_products: []
algorithms:
  - name: ssw_upgrade / rsync mirror
    equation_refs: []
    external_implementations:
      - "https://www.lmsal.com/solarsoft/"
  - name: "Per-instrument prep dispatch (aia_prep, eit_prep, secchi_prep)"
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://www.lmsal.com/solarsoft/"
  data_repo: null
claim_boundary:
  scope: >-
    SolarSoft (SSW): GSFC-hosted SVN/Rsync tree of IDL routines per
    mission/instrument; provides `ssw_upgrade`, `setssw`, per-instrument prep
    routines (e.g., aia_prep, eit_prep, secchi_prep, lasco prep). Active but
    progressively superseded by Python ecosystem.
  out_of_scope:
    - Do not assume SSW updates are instantaneous; sync explicitly.
    - "Do not assume SSW prep matches Python-port output bit-for-bit — small differences exist (e.g., aiapy vs aia_prep)."
    - Do not require IDL license for casual users — Python ports cover most modern needs.
failure_modes:
  - Mixed mission paths in $SSW_INSTR can cause hidden dependencies — set narrowly.
  - "IDL version compatibility: SSW assumes IDL >= 8.x for some packages."
  - Some prep routines hard-code calibration files — sync regularly.
depends_on:
  []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: Python ports (sunpy/aiapy/sunkit) cover only a subset of SSW capabilities; many EIS/IRIS/RHESSI workflows still require IDL.
    related_skills:
      - paper-barnes-2020-aiapy-python-sdo-aia
    proposed_action: compile an EIS Python migration paper-skill when one is available
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# Data analysis with the SolarSoft system — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when an analysis still depends on IDL-based SolarSoft (SSW) routines (many SOHO/STEREO/SDO instrument preps remain SSW-canonical) or when porting a SSW workflow to Python — central claim is that SolarSoft is the umbrella IDL/UNIX shell ecosystem unifying mission instrument analysis libraries (Freeland & Handy 1998, Sol. Phys.).

Do NOT use this skill when:

- Do not assume SSW updates are instantaneous; sync explicitly.
- Do not assume SSW prep matches Python-port output bit-for-bit — small differences exist (e.g., aiapy vs aia_prep).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SolarSoft (SSW): GSFC-hosted SVN/Rsync tree of IDL routines per mission/instrument; provides `ssw_upgrade`, `setssw`, per-instrument prep routines (e.g., aia_prep, eit_prep, secchi_prep, lasco prep). Active but progressively superseded by Python ecosystem.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### ssw_upgrade / rsync mirror

- External implementation(s): https://www.lmsal.com/solarsoft/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Per-instrument prep dispatch (aia_prep, eit_prep, secchi_prep)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote-sensing data dependencies (this skill is purely software / infrastructure or coordinate-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Mixed mission paths in $SSW_INSTR can cause hidden dependencies — set narrowly.
- IDL version compatibility: SSW assumes IDL >= 8.x for some packages.
- Some prep routines hard-code calibration files — sync regularly.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SolarSoft (SSW): GSFC-hosted SVN/Rsync tree of IDL routines per mission/instrument; provides `ssw_upgrade`, `setssw`, per-instrument prep routines (e.g., aia_prep, eit_prep, secchi_prep, lasco prep). Active but progressively superseded by Python ecosystem.

**Out of scope — do NOT generalize beyond:**

- Do not assume SSW updates are instantaneous; sync explicitly.
- Do not assume SSW prep matches Python-port output bit-for-bit — small differences exist (e.g., aiapy vs aia_prep).
- Do not require IDL license for casual users — Python ports cover most modern needs.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://www.lmsal.com/solarsoft/
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

- **Gap** — Python ports (sunpy/aiapy/sunkit) cover only a subset of SSW capabilities; many EIS/IRIS/RHESSI workflows still require IDL. Proposed: compile an EIS Python migration paper-skill when one is available.

## Weak entries / citation TODOs

- Sol. Phys. 182, 497 (1998); DOI not in local inventory
