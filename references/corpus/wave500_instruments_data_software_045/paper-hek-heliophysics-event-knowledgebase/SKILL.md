---
name: paper-hek-heliophysics-event-knowledgebase
description: >-
  Use when querying machine-readable catalogs of solar events (flares, CMEs,
  filament eruptions, active regions, coronal holes) — central claim is that the
  HEK at LMSAL is a programmable Heliophysics Event Knowledgebase exposing FRMs
  (Feature Recognition Methods) and HER (Heliophysics Event Reports) via REST +
  sunpy (Hurlburt et al. 2012, Sol. Phys.).
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
  title: The Heliophysics Event Knowledgebase (HEK)
  first_author: "Hurlburt, N."
  year: 2012
  venue: Solar Physics
  doi: 10.1007/s11207-010-9624-2
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
  regime:
    - corona
trigger_keywords:
  - HEK
  - Hurlburt 2012
  - heliophysics event knowledgebase
  - Feature Recognition Method FRM
  - flare catalog HEK
  - active region catalog
data_products:
  - instrument: HEK FL (flare) events
    level: catalog
    cadence: event-based
    interval: null
    archive: HEK
  - instrument: HEK AR (active region) events
    level: catalog
    cadence: event-based
    interval: null
    archive: HEK
  - instrument: HEK CH (coronal hole) events
    level: catalog
    cadence: event-based
    interval: null
    archive: HEK
algorithms:
  - name: HEK REST query → HER record
    equation_refs: []
    external_implementations:
      - sunpy.net.hek
validation_target: null
links:
  doi_url: "https://doi.org/10.1007/s11207-010-9624-2"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://www.lmsal.com/hek/"
claim_boundary:
  scope: >-
    HEK: hosts events from many FRMs (SSW Latest Events, ASSA, SolarSoft,
    manual). Sunpy Fido provider: `Fido.search(a.hek.*)`. Returns event tables
    with start/peak/end times, coordinates, magnitudes.
  out_of_scope:
    - Do not treat HEK as authoritative event truth — FRMs disagree.
    - Do not assume coverage prior to ~2010 is uniform.
failure_modes:
  - "Multi-FRM duplicates: one physical flare can produce several HER rows."
  - "FRM coverage drift: an FRM may shut off without explicit deprecation."
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
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# The Heliophysics Event Knowledgebase (HEK) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when querying machine-readable catalogs of solar events (flares, CMEs, filament eruptions, active regions, coronal holes) — central claim is that the HEK at LMSAL is a programmable Heliophysics Event Knowledgebase exposing FRMs (Feature Recognition Methods) and HER (Heliophysics Event Reports) via REST + sunpy (Hurlburt et al. 2012, Sol. Phys.).

Do NOT use this skill when:

- Do not treat HEK as authoritative event truth — FRMs disagree.
- Do not assume coverage prior to ~2010 is uniform.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** HEK: hosts events from many FRMs (SSW Latest Events, ASSA, SolarSoft, manual). Sunpy Fido provider: `Fido.search(a.hek.*)`. Returns event tables with start/peak/end times, coordinates, magnitudes.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### HEK REST query → HER record

- External implementation(s): sunpy.net.hek
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| HEK FL (flare) events | catalog | event-based | — | HEK |
| HEK AR (active region) events | catalog | event-based | — | HEK |
| HEK CH (coronal hole) events | catalog | event-based | — | HEK |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Multi-FRM duplicates: one physical flare can produce several HER rows.
- FRM coverage drift: an FRM may shut off without explicit deprecation.

## 7. Claim boundary  *(Layer 1)*

**In scope.** HEK: hosts events from many FRMs (SSW Latest Events, ASSA, SolarSoft, manual). Sunpy Fido provider: `Fido.search(a.hek.*)`. Returns event tables with start/peak/end times, coordinates, magnitudes.

**Out of scope — do NOT generalize beyond:**

- Do not treat HEK as authoritative event truth — FRMs disagree.
- Do not assume coverage prior to ~2010 is uniform.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1007/s11207-010-9624-2
- arXiv: n/a
- Code: n/a
- Data / archive: https://www.lmsal.com/hek/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
