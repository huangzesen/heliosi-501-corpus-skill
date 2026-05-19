---
name: paper-chiantipy-dere-1997-chianti-atomic-database-python
description: >-
  Use when computing optically-thin emissivities, contribution functions, and
  DEM-folded synthetic spectra for solar/coronal plasma — central claim is that
  the CHIANTI atomic database + ChiantiPy Python interface provide the standard
  solar EUV/X-ray emissivity model (Dere et al. 1997, A&AS; v11 paper Del Zanna
  et al. 2021 for current release).
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
  title: CHIANTI — An Atomic Database for Emission Lines
  first_author: "Dere, K. P."
  year: 1997
  venue: "Astronomy & Astrophysics Supplement Series"
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
trigger_keywords:
  - CHIANTI atomic database
  - ChiantiPy
  - Dere 1997
  - Del Zanna 2021
  - contribution function
  - DEM AIA
  - EUV emissivity
  - optically thin solar
data_products:
  - instrument: CHIANTI atomic database (v11 latest)
    level: reference data
    cadence: n/a
    interval: static
    archive: "https://www.chiantidatabase.org/"
algorithms:
  - name: Contribution function G(T) computation
    equation_refs:
      - Dere 1997 §3
    external_implementations:
      - "https://github.com/chianti-atomic/ChiantiPy"
  - name: DEM-folded synthetic AIA / EIS spectra
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/chianti-atomic/ChiantiPy"
  data_repo: "https://www.chiantidatabase.org/"
claim_boundary:
  scope: >-
    CHIANTI: atomic database (continually updated; v11 in 2021/2024) of energy
    levels, oscillator strengths, collision rates for ~190 ions. ChiantiPy is
    the Python wrapper computing emissivities, contribution functions, DEM-
    folded synthetic spectra.
  out_of_scope:
    - "Do not assume CHIANTI is photo-ionized — it is for collisionally ionized, optically thin plasma."
    - Do not extrapolate CHIANTI beyond its temperature/density grids without warnings.
    - Do not mix CHIANTI versions in a single analysis pipeline silently.
failure_modes:
  - Different CHIANTI versions yield different G(T); always record version.
  - Density-dependent line ratios mis-handled if ionization equilibrium not from same version.
  - AIA temperature response uses pre-baked CHIANTI grids — replace if updating version.
depends_on:
  []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: No paper-skill yet captures the v11 CHIANTI release (Del Zanna et al. 2021) revisions to recombination rates that change AIA response curves.
    related_skills: []
    proposed_action: compile a Del Zanna 2021 CHIANTI v10/v11 paper-skill
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# CHIANTI — An Atomic Database for Emission Lines — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when computing optically-thin emissivities, contribution functions, and DEM-folded synthetic spectra for solar/coronal plasma — central claim is that the CHIANTI atomic database + ChiantiPy Python interface provide the standard solar EUV/X-ray emissivity model (Dere et al. 1997, A&AS; v11 paper Del Zanna et al. 2021 for current release).

Do NOT use this skill when:

- Do not assume CHIANTI is photo-ionized — it is for collisionally ionized, optically thin plasma.
- Do not extrapolate CHIANTI beyond its temperature/density grids without warnings.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** CHIANTI: atomic database (continually updated; v11 in 2021/2024) of energy levels, oscillator strengths, collision rates for ~190 ions. ChiantiPy is the Python wrapper computing emissivities, contribution functions, DEM-folded synthetic spectra.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Contribution function G(T) computation

- Paper reference: Dere 1997 §3
- External implementation(s): https://github.com/chianti-atomic/ChiantiPy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### DEM-folded synthetic AIA / EIS spectra

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| CHIANTI atomic database (v11 latest) | reference data | n/a | static | https://www.chiantidatabase.org/ |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Different CHIANTI versions yield different G(T); always record version.
- Density-dependent line ratios mis-handled if ionization equilibrium not from same version.
- AIA temperature response uses pre-baked CHIANTI grids — replace if updating version.

## 7. Claim boundary  *(Layer 1)*

**In scope.** CHIANTI: atomic database (continually updated; v11 in 2021/2024) of energy levels, oscillator strengths, collision rates for ~190 ions. ChiantiPy is the Python wrapper computing emissivities, contribution functions, DEM-folded synthetic spectra.

**Out of scope — do NOT generalize beyond:**

- Do not assume CHIANTI is photo-ionized — it is for collisionally ionized, optically thin plasma.
- Do not extrapolate CHIANTI beyond its temperature/density grids without warnings.
- Do not mix CHIANTI versions in a single analysis pipeline silently.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://github.com/chianti-atomic/ChiantiPy
- Data / archive: https://www.chiantidatabase.org/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

- **Gap** — No paper-skill yet captures the v11 CHIANTI release (Del Zanna et al. 2021) revisions to recombination rates that change AIA response curves. Proposed: compile a Del Zanna 2021 CHIANTI v10/v11 paper-skill.

## Weak entries / citation TODOs

- Original 1997 ADS bibcode 1997A&AS..125..149D — verify before citing
