---
name: paper-burrell-2018-pyhc-python-heliophysics-community
description: >-
  Use when navigating the Python in Heliophysics Community (PyHC) ecosystem map
  (sunpy, spacepy, pysat, pyspedas, plasmapy, kamodo, etc.) and the PyHC
  core/affiliated tiers — central claim is that PyHC defines package-tiering and
  community standards for interoperable heliophysics Python (Burrell et al.
  2018, JGR-Space; PyHC continues to evolve).
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
  title: Snakes on a Spaceship — An Overview of Python in Heliophysics
  first_author: "Burrell, A. G."
  year: 2018
  venue: "Journal of Geophysical Research: Space Physics"
  doi: 10.1029/2018JA025877
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - n/a
trigger_keywords:
  - PyHC
  - Burrell 2018
  - Python in Heliophysics Community
  - heliophysics Python standards
  - core affiliated packages
  - PyHC summer school
data_products: []
algorithms:
  - name: PyHC standards (testing/docs/licensing tiers)
    equation_refs: []
    external_implementations:
      - "https://heliopython.org/"
validation_target: null
links:
  doi_url: "https://doi.org/10.1029/2018JA025877"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://heliopython.org/"
claim_boundary:
  scope: >-
    PyHC: community body governing Python heliophysics packages. Defines 'core'
    (sunpy, spacepy, plasmapy, pysat, kamodo, pyspedas), maintains annual
    meetings, and publishes the Python Heliophysics Standards (testing, docs,
    licensing) that affiliated packages target.
  out_of_scope:
    - Do not treat PyHC membership as a quality guarantee — affiliated packages vary in maturity.
    - Do not assume the standards are mandatory; they are recommendations.
    - Do not confuse PyHC with NASA SDAC — PyHC is community-run.
failure_modes:
  - Affiliated-package version drift can silently break cross-imports.
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
  - paper-spacepy-2022-twelve-years
  - paper-plasmapy-plasma-physics-python
  - paper-pyspedas-multimission-data-access
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
# Snakes on a Spaceship — An Overview of Python in Heliophysics — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when navigating the Python in Heliophysics Community (PyHC) ecosystem map (sunpy, spacepy, pysat, pyspedas, plasmapy, kamodo, etc.) and the PyHC core/affiliated tiers — central claim is that PyHC defines package-tiering and community standards for interoperable heliophysics Python (Burrell et al. 2018, JGR-Space; PyHC continues to evolve).

Do NOT use this skill when:

- Do not treat PyHC membership as a quality guarantee — affiliated packages vary in maturity.
- Do not assume the standards are mandatory; they are recommendations.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PyHC: community body governing Python heliophysics packages. Defines 'core' (sunpy, spacepy, plasmapy, pysat, kamodo, pyspedas), maintains annual meetings, and publishes the Python Heliophysics Standards (testing, docs, licensing) that affiliated packages target.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### PyHC standards (testing/docs/licensing tiers)

- External implementation(s): https://heliopython.org/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote-sensing data dependencies (this skill is purely software / infrastructure or coordinate-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Affiliated-package version drift can silently break cross-imports.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PyHC: community body governing Python heliophysics packages. Defines 'core' (sunpy, spacepy, plasmapy, pysat, kamodo, pyspedas), maintains annual meetings, and publishes the Python Heliophysics Standards (testing, docs, licensing) that affiliated packages target.

**Out of scope — do NOT generalize beyond:**

- Do not treat PyHC membership as a quality guarantee — affiliated packages vary in maturity.
- Do not assume the standards are mandatory; they are recommendations.
- Do not confuse PyHC with NASA SDAC — PyHC is community-run.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1029/2018JA025877
- arXiv: n/a
- Code: n/a
- Data / archive: https://heliopython.org/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`
- `[[paper-spacepy-2022-twelve-years]]`
- `[[paper-plasmapy-plasma-physics-python]]`
- `[[paper-pyspedas-multimission-data-access]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
