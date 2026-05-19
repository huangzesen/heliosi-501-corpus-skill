---
name: paper-jebaraj-2025-electron-beam-radio-five-spacecraft-2021
description: >-
  Use when type iii radio burst or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Multilateration with five spacecraft (PSP, STEREO-A, Wind, Solar Orbiter, Mars Express) for the 2021-12-04 event traces type III radio sources along a Parker spiral (~493 km/s) and quantitatively reconciles 'higher than expected' electron d… (arXiv:2502.15067, 2025).
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
  title: "Electron Beam Propagation and Radio-Wave Scattering in the Inner Heliosphere using Five Spacecraft"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2502.15067"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP, STEREO-A, Wind, Solar Orbiter, Mars Express, ACE]
  regime: [inner-heliosphere]

trigger_keywords:
  - "type III radio burst"
  - "five-spacecraft multilateration"
  - "BELLA Bayesian"
  - "radio-wave scattering"
  - "Parker spiral 493 km/s"
  - "2021-12-04 event"

data_products:
  - instrument: "PSP/FIELDS LFR/HFR"
    level: "L2"
    cadence: "high cadence"
    interval: "2021-12-04 ± 1 d"
    archive: "PSP SOC"
  - instrument: "STEREO-A WAVES + Wind WAVES + Solar Orbiter RPW + Mars Express MARSIS"
    level: "L2"
    cadence: "minute"
    interval: "2021-12-04"
    archive: "agency archives"
  - instrument: "Nançay Radioheliograph 150 MHz"
    level: "L1"
    cadence: "imaging"
    interval: "2021-12-04"
    archive: "ground archive"
  - instrument: "ACE in-situ density"
    level: "L2"
    cadence: "1-min"
    interval: "2021-12-04"
    archive: "NASA CDAWeb"

algorithms:
  - name: "BELLA Bayesian multilateration of radio sources"
    equation_refs: []
    external_implementations: []
  - name: "Parker-spiral fit to the apparent path"
    equation_refs: []
    external_implementations: []
  - name: "Radio-wave scattering forward model"
    equation_refs: []
    external_implementations: []
  - name: "Cross-check against Nançay imaging + ACE in-situ"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2502.15067"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event 2021-12-04; five-observer radio multilateration; scattering interpretation; quantitative density profile via BELLA + ACE in-situ check.
  out_of_scope:
    - "Do not interpret apparent path as the true particle trajectory."
    - "Do not generalize the scattering parameters to other events without re-fit."

failure_modes:
  - "Multilateration degeneracy with few observers near the same plane"
  - "Scattering model assumptions affect inferred density profile"
  - "Cross-mission radio-band calibration"

depends_on:
  - "paper-duan-2026-sep-type-ii-radio-source-regions"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No standard five-spacecraft multilateration pipeline for PSP-era type III events."
    related_skills: []
  - type: "hypothesis"
    statement: "Scattering parameters fit per event correlate with ambient turbulence amplitude."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Apply BELLA + scattering fit to three additional five-observer type III events; compare scattering coefficients."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2502.15067"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Electron Beam Propagation and Radio-Wave Scattering in the Inner Heliosphere using Five Spacecraft — paper-skill

> Compiled from arXiv:2502.15067 (2025), TODO verify et al.
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

- type III radio burst
- five-spacecraft multilateration
- BELLA Bayesian

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Multilateration with five spacecraft (PSP, STEREO-A, Wind, Solar Orbiter, Mars Express) for the 2021-12-04 event traces type III radio sources along a Parker spiral (~493 km/s) and quantitatively reconciles 'higher than expected' electron densities with radio-wave scattering.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Inferred Parker spiral wind speed ~493 km/s consistent with ACE; scattering model reconciles inferred densities (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### BELLA Bayesian multilateration of radio sources

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - BELLA Bayesian multilateration of radio sources as a callable on the data products in §4.

### Parker-spiral fit to the apparent path

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Parker-spiral fit to the apparent path as a callable on the data products in §4.

### Radio-wave scattering forward model

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Radio-wave scattering forward model as a callable on the data products in §4.

### Cross-check against Nançay imaging + ACE in-situ

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-check against Nançay imaging + ACE in-situ as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/FIELDS LFR/HFR | L2 | high cadence | 2021-12-04 ± 1 d | PSP SOC | abstract: load + decode + subset |
| STEREO-A WAVES + Wind WAVES + Solar Orbiter RPW + Mars Express MARSIS | L2 | minute | 2021-12-04 | agency archives | abstract: load + decode + subset |
| Nançay Radioheliograph 150 MHz | L1 | imaging | 2021-12-04 | ground archive | abstract: load + decode + subset |
| ACE in-situ density | L2 | 1-min | 2021-12-04 | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Inferred Parker spiral wind speed ~493 km/s consistent with ACE; scattering model reconciles inferred densities (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Multilateration degeneracy with few observers near the same plane
- Scattering model assumptions affect inferred density profile
- Cross-mission radio-band calibration

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event 2021-12-04; five-observer radio multilateration; scattering interpretation; quantitative density profile via BELLA + ACE in-situ check.

**Out of scope — do NOT generalize beyond:**

- Do not interpret apparent path as the true particle trajectory.
- Do not generalize the scattering parameters to other events without re-fit.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2502.15067
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-duan-2026-sep-type-ii-radio-source-regions]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No standard five-spacecraft multilateration pipeline for PSP-era type III events.
- **Hypothesis** — Scattering parameters fit per event correlate with ambient turbulence amplitude.
- **Minimal_experiment** — Apply BELLA + scattering fit to three additional five-observer type III events; compare scattering coefficients.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
