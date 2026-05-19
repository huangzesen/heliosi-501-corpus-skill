---
name: paper-luhmann-2026-stereo-het-sep-protons-first-orbit
description: >-
  Use when stereo het or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: A 2006–2023 SEP proton catalog from STEREO-A HET (and Earth observers) covering STEREO-A's first complete solar orbit serves as a stable observational baseline for longitudinal coverage and event statistics. (arXiv:2601.09630, 2026).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true

layers:
  scientific_invariant: true
  executable_protocol: true
  adapter_binding_examples: false
  research_generation_affordance: true

paper:
  title: "Solar Energetic Proton Events Observed by the High Energy Telescopes on the STEREO Spacecraft or at the Earth During the First Solar Orbit of STEREO A (2006 to 2023)"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2601.09630"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [STEREO-A, GOES, ACE/Wind]
  regime: [inner-heliosphere]

trigger_keywords:
  - "STEREO HET"
  - "proton SEP catalog"
  - "first solar orbit 2006–2023"
  - "Earth-equivalent observers"
  - "longitudinal coverage"

data_products:
  - instrument: "STEREO-A IMPACT/HET"
    level: "L2"
    cadence: "instrument-native"
    interval: "2006–2023"
    archive: "STEREO archive / NASA CDAWeb"
  - instrument: "GOES SEISS/EPS proton"
    level: "L2"
    cadence: "5-min"
    interval: "2006–2023"
    archive: "NOAA SWPC"

algorithms:
  - name: "Event detection threshold (TODO_verify)"
    equation_refs: []
    external_implementations: []
  - name: "Peak-intensity + spectral fit per event"
    equation_refs: []
    external_implementations: []
  - name: "Longitudinal coverage map (STEREO-A heliographic longitude vs Earth)"
    equation_refs: []
    external_implementations: []
  - name: "Association class (CME / type II / source AR)"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2601.09630"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    2006–2023; STEREO-A HET protons (and Earth observers); event list with peak intensity, spectral fit, association class.
  out_of_scope:
    - "Do not generalize to non-HET energy ranges."
    - "Do not draw cycle-25 conclusions from a sample that ends in 2023."

failure_modes:
  - "HET response evolves over orbit lifetime — calibration needed"
  - "Geometric longitude coverage non-uniform during STEREO-B loss period"
  - "Spectral-index uncertainty at small N events"

depends_on:
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No joint catalog merging STEREO-A HET with Solar Orbiter EPD HET to extend longitudinal coverage past 2020."
    related_skills: []
  - type: "hypothesis"
    statement: "Longitudinal occurrence-rate map is asymmetric east–west of source AR by a measurable fraction."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Cross-match the STEREO-A HET catalog with the Solar Orbiter EPD HET catalog for 2020–2023."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2601.09630"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Solar Energetic Proton Events Observed by the High Energy Telescopes on the STEREO Spacecraft or at the Earth During the First Solar Orbit of STEREO A (2006 to 2023) — paper-skill

> Compiled from arXiv:2601.09630 (2026), TODO verify et al.
> **Quality tier**: `stub`. All numeric specifics not present in the
> arXiv-inventory abstract are marked `TODO_verify_with_full_text`.

---

## Layer map (harness-agnostic)

This SKILL.md is structured to be loadable by *any* general-purpose agent
runtime (Claude Code, LingTai, Codex, Cursor, OpenAI Assistants, …).
Named runtimes / MCPs / repos appear only as *adapter examples*; the
contract itself is runtime-neutral. Sections map onto four layers:

1. **Scientific invariant layer** — §1 trigger, §2 narrow claim, §6
   failure modes, §7 claim boundary. Mission- / instrument- / physics-
   level statements; runtime-neutral.
2. **Executable protocol layer (abstract capability contracts)** — §3
   procedures and §4 tool contracts describe what *capabilities* are
   needed (e.g., "load IS☉IS energetic-particle spectra", "compute
   power-law fit") without binding to any particular API, MCP, or
   harness tool. Any runtime that fulfils the named capability satisfies
   the contract.
3. **Adapter / runtime notes (optional examples)** — wherever a named
   tool, MCP, repo, or library would appear, it is exactly one *example
   adapter* satisfying the abstract contract above; substitutable.
4. **Research-generation affordances** — §9 lists gaps, tensions, new
   hypotheses, and follow-up experiments enabled when this skill is
   composed with prior skills in the corpus.

A consuming agent MUST honour Layers 1 and 2; Layer 3 mentions (if any)
are substitutable; Layer 4 entries are seeds for new work, not claims.

---

## 1. Trigger  *(Layer 1)*

A future agent should reach for this skill when:

- STEREO HET
- proton SEP catalog
- first solar orbit 2006–2023

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A 2006–2023 SEP proton catalog from STEREO-A HET (and Earth observers) covering STEREO-A's first complete solar orbit serves as a stable observational baseline for longitudinal coverage and event statistics.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Total event count; cumulative distribution of peak intensity; spectral-index histogram (TODO_verify numbers). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Event detection threshold (TODO_verify)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Event detection threshold (TODO_verify) as a callable on the data products in §4.

### Peak-intensity + spectral fit per event

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Peak-intensity + spectral fit per event as a callable on the data products in §4.

### Longitudinal coverage map (STEREO-A heliographic longitude vs Earth)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Longitudinal coverage map (STEREO-A heliographic longitude vs Earth) as a callable on the data products in §4.

### Association class (CME / type II / source AR)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Association class (CME / type II / source AR) as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| STEREO-A IMPACT/HET | L2 | instrument-native | 2006–2023 | STEREO archive / NASA CDAWeb | abstract: load + decode + subset |
| GOES SEISS/EPS proton | L2 | 5-min | 2006–2023 | NOAA SWPC | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Total event count; cumulative distribution of peak intensity; spectral-index histogram (TODO_verify numbers).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- HET response evolves over orbit lifetime — calibration needed
- Geometric longitude coverage non-uniform during STEREO-B loss period
- Spectral-index uncertainty at small N events

## 7. Claim boundary  *(Layer 1)*

**In scope.** 2006–2023; STEREO-A HET protons (and Earth observers); event list with peak intensity, spectral fit, association class.

**Out of scope — do NOT generalize beyond:**

- Do not generalize to non-HET energy ranges.
- Do not draw cycle-25 conclusions from a sample that ends in 2023.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2601.09630
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No joint catalog merging STEREO-A HET with Solar Orbiter EPD HET to extend longitudinal coverage past 2020.
- **Hypothesis** — Longitudinal occurrence-rate map is asymmetric east–west of source AR by a measurable fraction.
- **Minimal_experiment** — Cross-match the STEREO-A HET catalog with the Solar Orbiter EPD HET catalog for 2020–2023.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
