---
name: paper-king-2005-omni-1min-5min-solar-wind-dataset
description: >-
  Use when working with the OMNI 1-min / 5-min / hourly multi-spacecraft merged
  solar-wind dataset (Wind, ACE, IMP-8, etc.) time-shifted to the bow shock nose
  — central claim is that the OMNI pipeline (King & Papitashvili 2005) provides
  a continuous bow-shock-shifted L1 solar-wind + IMF time series suitable as a
  magnetospheric driver dataset.
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
  title: Solar wind spatial scales in and comparisons of hourly Wind and ACE plasma and magnetic field data
  first_author: "King, J. H."
  year: 2005
  venue: Journal of Geophysical Research
  doi: 10.1029/2004JA010649
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - Wind
    - ACE
  regime:
    - 1au
trigger_keywords:
  - OMNI dataset
  - King Papitashvili 2005
  - OMNIWeb
  - bow shock nose shift
  - merged solar wind 1 min
  - L1 monitor merged
  - 1-min OMNI
  - high resolution OMNI
data_products:
  - instrument: OMNI 1-min
    level: L2 derived
    cadence: 1 min
    interval: 1995-01..present
    archive: SPDF / OMNIWeb
  - instrument: OMNI hourly
    level: L2 derived
    cadence: 1 hour
    interval: 1963-01..present
    archive: SPDF / OMNIWeb
  - instrument: OMNI 5-min
    level: L2 derived
    cadence: 5 min
    interval: 1995-01..present
    archive: SPDF
algorithms:
  - name: Multi-spacecraft phase-front propagation time-shift
    equation_refs:
      - "§3 King & Papitashvili 2005"
    external_implementations: []
  - name: Spacecraft selection priority logic
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1029/2004JA010649"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://omniweb.gsfc.nasa.gov/"
claim_boundary:
  scope: >-
    OMNI = NASA SPDF time-shifted, cross-calibrated, multi-source IMF + solar-
    wind plasma + activity-index data file, available at 1 min, 5 min, and 1
    hour resolution. Source spacecraft selection is automated to prefer Wind,
    then ACE, then IMP-8.
  out_of_scope:
    - "Do not assume OMNI replaces source spacecraft data — for instrument-level analysis go back to Wind/SWE, ACE/MAG, etc."
    - Do not use OMNI 1-min data prior to 1995 (pre-Wind era).
    - Do not treat the time-shift as instantaneous propagation — it is a planar approximation.
failure_modes:
  - Time-shift fails when phase-front is highly tilted; quality flag IMF_PTS / Plasma_PTS indicates fit count.
  - Gaps may be filled by lower-priority spacecraft — source ID changes mid-file.
  - Hourly OMNI before 1995 has different cadence and instrument heritage.
depends_on:
  - paper-lepping-1995-wind-mfi-magnetometer
  - paper-ogilvie-1995-wind-swe-faraday-cup
  - paper-smith-1998-ace-mag-vector-helium-magnetometer
  - paper-mccomas-1998-ace-swepam-solar-wind-electron-proton-alpha
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: OMNI does not propagate to magnetopause subsolar; users must add an additional delay layer for magnetopause coupling studies.
    related_skills: []
    proposed_action: "document a magnetopause-propagation paper-skill (e.g., Cane 2000)"
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# Solar wind spatial scales in and comparisons of hourly Wind and ACE plasma and magnetic field data — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when working with the OMNI 1-min / 5-min / hourly multi-spacecraft merged solar-wind dataset (Wind, ACE, IMP-8, etc.) time-shifted to the bow shock nose — central claim is that the OMNI pipeline (King & Papitashvili 2005) provides a continuous bow-shock-shifted L1 solar-wind + IMF time series suitable as a magnetospheric driver dataset.

Do NOT use this skill when:

- Do not assume OMNI replaces source spacecraft data — for instrument-level analysis go back to Wind/SWE, ACE/MAG, etc.
- Do not use OMNI 1-min data prior to 1995 (pre-Wind era).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** OMNI = NASA SPDF time-shifted, cross-calibrated, multi-source IMF + solar-wind plasma + activity-index data file, available at 1 min, 5 min, and 1 hour resolution. Source spacecraft selection is automated to prefer Wind, then ACE, then IMP-8.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Multi-spacecraft phase-front propagation time-shift

- Paper reference: §3 King & Papitashvili 2005
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Spacecraft selection priority logic

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| OMNI 1-min | L2 derived | 1 min | 1995-01..present | SPDF / OMNIWeb |
| OMNI hourly | L2 derived | 1 hour | 1963-01..present | SPDF / OMNIWeb |
| OMNI 5-min | L2 derived | 5 min | 1995-01..present | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Time-shift fails when phase-front is highly tilted; quality flag IMF_PTS / Plasma_PTS indicates fit count.
- Gaps may be filled by lower-priority spacecraft — source ID changes mid-file.
- Hourly OMNI before 1995 has different cadence and instrument heritage.

## 7. Claim boundary  *(Layer 1)*

**In scope.** OMNI = NASA SPDF time-shifted, cross-calibrated, multi-source IMF + solar-wind plasma + activity-index data file, available at 1 min, 5 min, and 1 hour resolution. Source spacecraft selection is automated to prefer Wind, then ACE, then IMP-8.

**Out of scope — do NOT generalize beyond:**

- Do not assume OMNI replaces source spacecraft data — for instrument-level analysis go back to Wind/SWE, ACE/MAG, etc.
- Do not use OMNI 1-min data prior to 1995 (pre-Wind era).
- Do not treat the time-shift as instantaneous propagation — it is a planar approximation.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1029/2004JA010649
- arXiv: n/a
- Code: n/a
- Data / archive: https://omniweb.gsfc.nasa.gov/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-lepping-1995-wind-mfi-magnetometer]]`
- `[[paper-ogilvie-1995-wind-swe-faraday-cup]]`
- `[[paper-smith-1998-ace-mag-vector-helium-magnetometer]]`
- `[[paper-mccomas-1998-ace-swepam-solar-wind-electron-proton-alpha]]`

**Research-generation affordances.**

- **Gap** — OMNI does not propagate to magnetopause subsolar; users must add an additional delay layer for magnetopause coupling studies. Proposed: document a magnetopause-propagation paper-skill (e.g., Cane 2000).
