---
name: paper-psp-soc-science-operations-center-archive
description: >-
  Use when accessing pre-public-release PSP/FIELDS, PSP/SWEAP, PSP/ISʘIS, or
  PSP/WISPR data products direct from the mission-team archives at JHU/APL,
  Berkeley, Princeton — central claim is that the PSP SOC + per-instrument team
  archives are the canonical source for PSP data ahead of CDAWeb mirror release;
  CDAWeb mirrors lag for newer encounters.
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
  title: Parker Solar Probe Science Operations Center / FIELDS archive
  first_author: PSP Science Operations Center / FIELDS team
  year: 2020
  venue: "(PSP project documentation; companion overview Fox et al. 2016 Space Sci. Rev. — mission, and Bale et al. 2016 — FIELDS archive)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: psp_data
  secondary_themes: []
  missions:
    - PSP
  regime:
    - inner-heliosphere
    - corona
trigger_keywords:
  - PSP SOC
  - FIELDS archive Berkeley
  - SWEAP archive
  - ISOIS archive Princeton
  - PSP data team archive
data_products:
  - instrument: PSP/FIELDS
    level: L2 / L3
    cadence: various
    interval: null
    archive: "https://fields.ssl.berkeley.edu/"
  - instrument: PSP/SWEAP
    level: L2 / L3
    cadence: various
    interval: null
    archive: "http://sweap.cfa.harvard.edu/"
  - instrument: PSP/ISʘIS
    level: L2 / L3
    cadence: various
    interval: null
    archive: "https://spp-isois.princeton.edu/"
algorithms: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://fields.ssl.berkeley.edu/"
claim_boundary:
  scope: >-
    PSP archives: SOC at JHU/APL (mission ephemeris + housekeeping); FIELDS at
    Berkeley (https://fields.ssl.berkeley.edu/); SWEAP at SAO (Harvard); ISʘIS
    at Princeton; WISPR at NRL. CDAWeb mirrors after release.
  out_of_scope:
    - Do not assume CDAWeb is complete for the current encounter — use mission-team archive.
    - "Do not bypass team-published version: per-instrument READMEs flag deprecated products."
    - Do not use unprocessed L1 for science without consulting team release notes.
failure_modes:
  - "Encounter-specific FIELDS calibration tables: a single archive directory may carry multiple versions; use the latest signed-off."
  - "ISʘIS L3 'rates' files require explicit pitch-angle reconstruction."
depends_on:
  - bale-2016-fields-instrument-suite-psp
  - kasper-2016-sweap-investigation-psp
  - mccomas-2016-isois-energetic-particle-investigation-psp
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
# Parker Solar Probe Science Operations Center / FIELDS archive — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when accessing pre-public-release PSP/FIELDS, PSP/SWEAP, PSP/ISʘIS, or PSP/WISPR data products direct from the mission-team archives at JHU/APL, Berkeley, Princeton — central claim is that the PSP SOC + per-instrument team archives are the canonical source for PSP data ahead of CDAWeb mirror release; CDAWeb mirrors lag for newer encounters.

Do NOT use this skill when:

- Do not assume CDAWeb is complete for the current encounter — use mission-team archive.
- Do not bypass team-published version: per-instrument READMEs flag deprecated products.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PSP archives: SOC at JHU/APL (mission ephemeris + housekeeping); FIELDS at Berkeley (https://fields.ssl.berkeley.edu/); SWEAP at SAO (Harvard); ISʘIS at Princeton; WISPR at NRL. CDAWeb mirrors after release.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

This skill is primarily a *contract* (instrument / data product / archive); see §4 for the abstract tool contract. No standalone algorithm is teach-able from this skill alone.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS | L2 / L3 | various | — | https://fields.ssl.berkeley.edu/ |
| PSP/SWEAP | L2 / L3 | various | — | http://sweap.cfa.harvard.edu/ |
| PSP/ISʘIS | L2 / L3 | various | — | https://spp-isois.princeton.edu/ |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Encounter-specific FIELDS calibration tables: a single archive directory may carry multiple versions; use the latest signed-off.
- ISʘIS L3 'rates' files require explicit pitch-angle reconstruction.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PSP archives: SOC at JHU/APL (mission ephemeris + housekeeping); FIELDS at Berkeley (https://fields.ssl.berkeley.edu/); SWEAP at SAO (Harvard); ISʘIS at Princeton; WISPR at NRL. CDAWeb mirrors after release.

**Out of scope — do NOT generalize beyond:**

- Do not assume CDAWeb is complete for the current encounter — use mission-team archive.
- Do not bypass team-published version: per-instrument READMEs flag deprecated products.
- Do not use unprocessed L1 for science without consulting team release notes.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://fields.ssl.berkeley.edu/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[bale-2016-fields-instrument-suite-psp]]`
- `[[kasper-2016-sweap-investigation-psp]]`
- `[[mccomas-2016-isois-energetic-particle-investigation-psp]]`

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- No single canonical 'archive paper' — cite mission overview + per-instrument papers
