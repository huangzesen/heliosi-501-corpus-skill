---
name: paper-astropy-2022-collaboration-community-package
description: >-
  Use when a workflow needs core astronomy primitives (units, FITS I/O,
  coordinates, time scales, tables) that the rest of the Python heliophysics
  stack (sunpy, pfsspy, sunkit-magex, pyspedas via pytplot) builds on — central
  claim is that Astropy v5.0 (Astropy Collaboration 2022, ApJ) is the community-
  governed substrate for astronomical Python.
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
  title: "The Astropy Project: Sustaining and Growing a Community-oriented Open-source Project and the Latest Major Release (v5.0)"
  first_author: Astropy Collaboration
  year: 2022
  venue: The Astrophysical Journal
  doi: 10.3847/1538-4357/ac7c74
  arxiv_id: 2206.14220
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - n/a
trigger_keywords:
  - Astropy
  - astropy.units
  - astropy.coordinates
  - astropy.time
  - Astropy 5.0
  - Astropy collaboration 2022
  - FITS Python
  - scientific Python astronomy core
data_products: []
algorithms:
  - name: astropy.units quantity arithmetic with unit safety
    equation_refs: []
    external_implementations:
      - "https://github.com/astropy/astropy"
  - name: astropy.coordinates SkyCoord/Frame transforms
    equation_refs: []
    external_implementations: []
  - name: astropy.time multi-scale time
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.3847/1538-4357/ac7c74"
  arxiv_url: "https://arxiv.org/abs/2206.14220"
  ads_url: null
  code_repo: "https://github.com/astropy/astropy"
  data_repo: null
claim_boundary:
  scope: >-
    Astropy core: astropy.units, astropy.time, astropy.coordinates,
    astropy.io.fits, astropy.table, astropy.constants, astropy.wcs. Affiliated
    packages include sunpy, pyspedas (via dependencies), specutils, ccdproc.
  out_of_scope:
    - Do not use Astropy as a numerical solver; it is a primitives library.
    - Do not assume astropy.coordinates contains every heliophysics frame — sunpy.coordinates extends it.
    - Do not assume Astropy time scales auto-correct for leap seconds without IERS update.
failure_modes:
  - Forgetting to call quantity.to(unit) silently propagates wrong units in arithmetic that mixes scalars.
  - IERS table update lag introduces tens of ms time errors for tasks that need UT1.
  - Cross-frame coordinate transforms require explicit obstime — easy to omit.
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
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# The Astropy Project: Sustaining and Growing a Community-oriented Open-source Project and the Latest Major Release (v5.0) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when a workflow needs core astronomy primitives (units, FITS I/O, coordinates, time scales, tables) that the rest of the Python heliophysics stack (sunpy, pfsspy, sunkit-magex, pyspedas via pytplot) builds on — central claim is that Astropy v5.0 (Astropy Collaboration 2022, ApJ) is the community-governed substrate for astronomical Python.

Do NOT use this skill when:

- Do not use Astropy as a numerical solver; it is a primitives library.
- Do not assume astropy.coordinates contains every heliophysics frame — sunpy.coordinates extends it.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Astropy core: astropy.units, astropy.time, astropy.coordinates, astropy.io.fits, astropy.table, astropy.constants, astropy.wcs. Affiliated packages include sunpy, pyspedas (via dependencies), specutils, ccdproc.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### astropy.units quantity arithmetic with unit safety

- External implementation(s): https://github.com/astropy/astropy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### astropy.coordinates SkyCoord/Frame transforms

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### astropy.time multi-scale time

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote-sensing data dependencies (this skill is purely software / infrastructure or coordinate-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Forgetting to call quantity.to(unit) silently propagates wrong units in arithmetic that mixes scalars.
- IERS table update lag introduces tens of ms time errors for tasks that need UT1.
- Cross-frame coordinate transforms require explicit obstime — easy to omit.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Astropy core: astropy.units, astropy.time, astropy.coordinates, astropy.io.fits, astropy.table, astropy.constants, astropy.wcs. Affiliated packages include sunpy, pyspedas (via dependencies), specutils, ccdproc.

**Out of scope — do NOT generalize beyond:**

- Do not use Astropy as a numerical solver; it is a primitives library.
- Do not assume astropy.coordinates contains every heliophysics frame — sunpy.coordinates extends it.
- Do not assume Astropy time scales auto-correct for leap seconds without IERS update.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.3847/1538-4357/ac7c74
- arXiv: https://arxiv.org/abs/2206.14220
- Code: https://github.com/astropy/astropy
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.
