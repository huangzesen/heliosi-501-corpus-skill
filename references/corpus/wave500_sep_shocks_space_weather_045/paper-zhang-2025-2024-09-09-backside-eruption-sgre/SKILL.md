---
name: paper-zhang-2025-2024-09-09-backside-eruption-sgre
description: >-
  Use when 2024-09-09 backside eruption or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: The 2024-09-09 backside eruption produced a sustained gamma-ray emission event whose source-region observers are limb-occluded for Earth-side instruments; multispacecraft data trace the eruption + shock evolution. (arXiv:2503.23852, 2025).
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
  title: "Multispacecraft Observations of the 2024 September 9 Backside Solar Eruption that Resulted in a Sustained Gamma Ray Emission Event"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2503.23852"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Fermi-LAT, STEREO-A, Solar Orbiter, PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "2024-09-09 backside eruption"
  - "sustained gamma-ray emission"
  - "Fermi LAT"
  - "behind-the-limb proton source"
  - "multispacecraft conjunction"

data_products:
  - instrument: "Fermi/LAT gamma-ray"
    level: "L1"
    cadence: "1-min"
    interval: "2024-09-09 ± 1 d"
    archive: "Fermi SSC"
  - instrument: "STEREO-A SECCHI + Solar Orbiter EUI/Metis"
    level: "L1.5"
    cadence: "event"
    interval: "2024-09-09"
    archive: "STEREO / SOAR"
  - instrument: "PSP/IS☉IS EPI-Hi"
    level: "L2"
    cadence: "instrument-native"
    interval: "2024-09-09 ± 1 d"
    archive: "PSP SOC"

algorithms:
  - name: "Sustained gamma-ray light-curve segmentation"
    equation_refs: []
    external_implementations: []
  - name: "Backside source identification via heliographic coordinates"
    equation_refs: []
    external_implementations: []
  - name: "Shock kinematics + connectivity to Fermi-LOS"
    equation_refs: []
    external_implementations: []
  - name: "Cross-mission timeline alignment"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2503.23852"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event 2024-09-09; behind-the-limb relative to Earth; Fermi-LAT + STEREO-A/SECCHI + Solar Orbiter / PSP context.
  out_of_scope:
    - "Do not generalize the SGRE / backside association to a class without a multi-event statistical study."

failure_modes:
  - "Behind-the-limb source identification depends on STEREO-A geometry"
  - "Sustained gamma-ray decomposition into multiple components"
  - "Connectivity to LAT line-of-sight not directly observed"

depends_on:
  - "paper-share-2026-sol2012-06-03-late-phase-gamma-shock"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No combined Fermi-LAT + IS☉IS / EPD energetic-particle catalog filtered by behind-limb sources."
    related_skills: []
  - type: "hypothesis"
    statement: "Behind-limb SGRE events trace shock-acceleration on field lines connected to the dawnside."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Compile all SGRE events from 2020–2025 with multi-observer source-region position; test connectivity."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2503.23852"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Multispacecraft Observations of the 2024 September 9 Backside Solar Eruption that Resulted in a Sustained Gamma Ray Emission Event — paper-skill

> Compiled from arXiv:2503.23852 (2025), TODO verify et al.
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

- 2024-09-09 backside eruption
- sustained gamma-ray emission
- Fermi LAT

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** The 2024-09-09 backside eruption produced a sustained gamma-ray emission event whose source-region observers are limb-occluded for Earth-side instruments; multispacecraft data trace the eruption + shock evolution.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Gamma-ray flux profile, time-integrated fluence; behind-limb source confirmation (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Sustained gamma-ray light-curve segmentation

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Sustained gamma-ray light-curve segmentation as a callable on the data products in §4.

### Backside source identification via heliographic coordinates

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Backside source identification via heliographic coordinates as a callable on the data products in §4.

### Shock kinematics + connectivity to Fermi-LOS

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Shock kinematics + connectivity to Fermi-LOS as a callable on the data products in §4.

### Cross-mission timeline alignment

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-mission timeline alignment as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Fermi/LAT gamma-ray | L1 | 1-min | 2024-09-09 ± 1 d | Fermi SSC | abstract: load + decode + subset |
| STEREO-A SECCHI + Solar Orbiter EUI/Metis | L1.5 | event | 2024-09-09 | STEREO / SOAR | abstract: load + decode + subset |
| PSP/IS☉IS EPI-Hi | L2 | instrument-native | 2024-09-09 ± 1 d | PSP SOC | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Gamma-ray flux profile, time-integrated fluence; behind-limb source confirmation (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Behind-the-limb source identification depends on STEREO-A geometry
- Sustained gamma-ray decomposition into multiple components
- Connectivity to LAT line-of-sight not directly observed

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event 2024-09-09; behind-the-limb relative to Earth; Fermi-LAT + STEREO-A/SECCHI + Solar Orbiter / PSP context.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the SGRE / backside association to a class without a multi-event statistical study.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2503.23852
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-share-2026-sol2012-06-03-late-phase-gamma-shock]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No combined Fermi-LAT + IS☉IS / EPD energetic-particle catalog filtered by behind-limb sources.
- **Hypothesis** — Behind-limb SGRE events trace shock-acceleration on field lines connected to the dawnside.
- **Minimal_experiment** — Compile all SGRE events from 2020–2025 with multi-observer source-region position; test connectivity.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
