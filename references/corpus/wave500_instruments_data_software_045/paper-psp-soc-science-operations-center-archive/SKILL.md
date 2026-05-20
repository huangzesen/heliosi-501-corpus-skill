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
  research_generation_affordance: true
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
algorithms:
  - name: "per-instrument archive discovery (FIELDS @ Berkeley / SWEAP @ SAO / ISʘIS @ Princeton)"
  - name: "signed-off calibration-version resolution"
  - name: "direct team-archive fetch"
  - name: "CDAWeb mirror cross-check"
validation_target: >-
  For a chosen PSP encounter the per-instrument SOC archives (FIELDS,
  SWEAP, ISʘIS) expose the products listed in §4; for an encounter
  fully released to CDAWeb, the SOC fetch and CDAWeb mirror agree
  bit-identically on arrays and calibration version, and any persistent
  diff is recorded as a verification flag rather than silently absorbed.
  ISʘIS L3 'rates' files MUST be consumed with explicit pitch-angle
  reconstruction; consuming them without it is a calibration-layer error.
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
research_generation_affordances:
  - type: gap
    statement: "No single canonical 'PSP archive paper'; the skill aggregates per-instrument archive URLs (FIELDS @ Berkeley, SWEAP @ SAO, ISʘIS @ Princeton, WISPR @ NRL) anchored by mission-overview + per-instrument hardware papers."
    related_skills: ["bale-2016-fields-instrument-suite-psp", "kasper-2016-sweap-investigation-psp", "mccomas-2016-isois-energetic-particle-investigation-psp"]
    proposed_action: "Cite the per-instrument hardware papers and the Fox 2016 mission overview together; never silently bundle them into a fabricated 'archive paper'."
  - type: tension
    statement: "CDAWeb mirrors PSP data but lags SOC for recent encounters. Defaulting to CDAWeb for current encounters silently retrieves stale or empty data; defaulting to SOC means handling per-instrument URL drift."
    related_skills: ["paper-cdaweb-heliophysics-archive"]
    proposed_action: "Add a corpus-level routing rule: current-encounter PSP work → SOC; post-release encounters → CDAWeb. Record in adapter_notes of downstream PSP paper-skills."
  - type: minimal_experiment
    statement: "For a fully-released encounter, fetch the same FIELDS MAG L2 product from SOC and from CDAWeb and diff arrays + calibration version; any persistent diff is a mirroring-lag or calibration-version finding."
    related_skills: ["paper-cdaweb-heliophysics-archive", "paper-cdflib-cdf-reader"]
    proposed_action: "Commit the SOC vs CDAWeb diff harness; persistent divergence blocks promotion of downstream PSP loaders past method-ready."
  - type: open_question
    statement: "ISʘIS L3 'rates' files require explicit pitch-angle reconstruction. The corpus has no reusable pitch-angle reconstruction sub-skill — every ISʘIS-consuming entry rebuilds it."
    related_skills: ["mccomas-2016-isois-energetic-particle-investigation-psp"]
    proposed_action: "Add a shared pitch-angle reconstruction sub-skill at SEP/shocks promotion; surface absence as a verification flag on every ISʘIS-consuming entry until it lands."
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

**Concrete benchmark targets** (`method-ready` tier):

1. **Per-instrument archive availability.** For a chosen PSP encounter
   (e.g. E10 perihelion), the FIELDS archive at
   `https://fields.ssl.berkeley.edu/` exposes at least one signed-off
   L2 MAG product; the SWEAP archive at `http://sweap.cfa.harvard.edu/`
   exposes SPC + SPAN-I L3 moments; the ISʘIS archive at
   `https://spp-isois.princeton.edu/` exposes EPI-Lo / EPI-Hi L2 rates.
   A missing product on a *released* encounter is a regression.
2. **SOC vs CDAWeb mirror parity.** For an encounter that has been
   fully released to CDAWeb, fetching the same product from SOC and
   from CDAWeb returns arrays whose calibration version *matches*; any
   persistent diff is recorded as a verification flag on this skill,
   not silently absorbed into either path.
3. **ISʘIS pitch-angle reconstruction guard.** A reproduction that
   consumes an ISʘIS L3 "rates" file *without* pitch-angle
   reconstruction must raise an error (not a warning), because the
   resulting science is not faithful. This is a calibration-layer
   gate, not a soft check.

`executable` promotion requires running these three checks on at
least one fully-released encounter.

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

- **Gap.** No single canonical "PSP archive paper" exists. The skill
  aggregates per-instrument archive URLs (FIELDS @ Berkeley, SWEAP @
  SAO, ISʘIS @ Princeton, WISPR @ NRL) and is anchored by mission-
  overview + per-instrument hardware papers. Treat the missing single
  citation as an *immutable* verification flag — cite the per-
  instrument hardware papers and the Fox 2016 mission overview
  together, never silently bundle them into a fabricated "archive
  paper".
- **Tension.** CDAWeb mirrors PSP data but typically *lags* the SOC
  archives for recent encounters. A skill that defaults silently to
  CDAWeb for current-encounter PSP work will retrieve stale or empty
  data. Conversely, defaulting to SOC means handling authentication
  and per-instrument URL drift. The corpus-level resolution is a
  routing rule: current-encounter PSP work routes through SOC;
  older (post-release) encounters route through CDAWeb. The rule
  must be recorded in `adapter_notes` of downstream PSP paper-skills,
  not left implicit.
- **Minimal experiment.** For a single PSP encounter that is fully
  released to CDAWeb, fetch the same FIELDS MAG L2 product from SOC
  (Berkeley) and from CDAWeb and diff the arrays + calibration
  version. Expected: bit-identity once mirroring is complete. Any
  persistent diff is a calibration-version or mirroring-lag finding
  and a blocker for promoting downstream PSP loaders past
  `method-ready`. This is the composable experiment shared with
  `[[paper-cdaweb-heliophysics-archive]]` and
  `[[paper-cdflib-cdf-reader]]`.
- **Open question.** ISʘIS L3 "rates" files require explicit pitch-
  angle reconstruction (a load-bearing failure mode in §6). The
  corpus does not currently expose a *reusable* pitch-angle
  reconstruction sub-skill — every ISʘIS-consuming entry must rebuild
  it from L3 metadata. A future hardening step is a shared pitch-
  angle reconstruction sub-skill, gated at SEP/shocks promotion;
  until it lands, surface its absence as a verification flag on
  every ISʘIS-consuming paper-skill.
- **Composable experiment.** Compose this skill with
  `[[paper-cdaweb-heliophysics-archive]]` to build a corpus-level
  PSP routing table: per encounter, record whether CDAWeb and SOC
  agree (and on what calibration version). Any encounter where
  they diverge silently is a discoverable inconsistency, not a user
  error.

## Weak entries / citation TODOs

- No single canonical 'archive paper' — cite mission overview + per-instrument papers
