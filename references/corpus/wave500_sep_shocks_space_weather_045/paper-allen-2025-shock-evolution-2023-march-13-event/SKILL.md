---
name: paper-allen-2025-shock-evolution-2023-march-13-event
description: >-
  Use when 2023-03-13 widespread event or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: In-situ + remote-sensing data for 2023-03-13 yield a time-resolved evolution of the shock's local θ_Bn, Mach number, and surface geometry, complementing the widespread-event ESP analysis of Dresing+ 2025. (arXiv:2511.03496, 2025).
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
  title: "Evolution of the Shock Properties of the 2023 March 13 Event from In-Situ and Remote-Sensing Data"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2511.03496"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP, Solar Orbiter, STEREO-A, Wind, ACE, BepiColombo, MAVEN]
  regime: [inner-heliosphere]

trigger_keywords:
  - "2023-03-13 widespread event"
  - "shock evolution"
  - "Rankine-Hugoniot"
  - "3D shock surface"
  - "θ_Bn radial evolution"

data_products:
  - instrument: "PSP/FIELDS MAG + SWEAP"
    level: "L2"
    cadence: "high cadence"
    interval: "2023-03-13 ± 2 d"
    archive: "PSP SOC"
  - instrument: "Solar Orbiter MAG + SWA"
    level: "L2"
    cadence: "high cadence"
    interval: "2023-03-13 ± 2 d"
    archive: "ESA SOAR"
  - instrument: "STEREO-A IMPACT/PLASTIC"
    level: "L2"
    cadence: "high cadence"
    interval: "2023-03-13 ± 2 d"
    archive: "STEREO archive"
  - instrument: "Multi-observer coronagraphs + EUV"
    level: "L1.5"
    cadence: "event"
    interval: "2023-03-13"
    archive: "agency archives"

algorithms:
  - name: "Per-observer Rankine-Hugoniot shock fit"
    equation_refs: []
    external_implementations: []
  - name: "θ_Bn radial-evolution series"
    equation_refs: []
    external_implementations: []
  - name: "3D shock surface fit at multiple times"
    equation_refs: []
    external_implementations: []
  - name: "Comparison to widespread-ESP global structure"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2511.03496"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event 2023-03-13; multi-observer (PSP/SO/STEREO-A/near-Earth/MAVEN/BepiColombo — TODO_verify); local Rankine-Hugoniot shock parameters and surface evolution.
  out_of_scope:
    - "Do not extrapolate the local fits to longitudes not covered by observers."
    - "Do not use as evidence for a specific acceleration mechanism without coupling to a transport model."

failure_modes:
  - "Cross-mission magnetometer-frame alignment"
  - "Local-shock-fit ambiguity in turbulent upstream"
  - "Time-of-flight alignment across observers"

depends_on:
  - "paper-dresing-2025-widespread-esp-march-2023"
  - "paper-kouloumvakos-2026-iva-shock-properties"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No combined evolution model that uses the 2023-03-13 shock fit + MHD propagation forward into 1 au observers."
    related_skills: []
  - type: "hypothesis"
    statement: "Local shock θ_Bn evolution explains the circumsolar ESP signature better than a single global Mach number."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Couple the Rankine-Hugoniot time-series to ENLIL/EUHFORIA hindcast and back-test ESP timing."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2511.03496"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Evolution of the Shock Properties of the 2023 March 13 Event from In-Situ and Remote-Sensing Data — paper-skill

> Compiled from arXiv:2511.03496 (2025), TODO verify et al.
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

- 2023-03-13 widespread event
- shock evolution
- Rankine-Hugoniot

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** In-situ + remote-sensing data for 2023-03-13 yield a time-resolved evolution of the shock's local θ_Bn, Mach number, and surface geometry, complementing the widespread-event ESP analysis of Dresing+ 2025.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Time-resolved θ_Bn, Mach number; 3D-surface kinematic parameters; consistency with widespread-ESP front (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Per-observer Rankine-Hugoniot shock fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-observer Rankine-Hugoniot shock fit as a callable on the data products in §4.

### θ_Bn radial-evolution series

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - θ_Bn radial-evolution series as a callable on the data products in §4.

### 3D shock surface fit at multiple times

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - 3D shock surface fit at multiple times as a callable on the data products in §4.

### Comparison to widespread-ESP global structure

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Comparison to widespread-ESP global structure as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/FIELDS MAG + SWEAP | L2 | high cadence | 2023-03-13 ± 2 d | PSP SOC | abstract: load + decode + subset |
| Solar Orbiter MAG + SWA | L2 | high cadence | 2023-03-13 ± 2 d | ESA SOAR | abstract: load + decode + subset |
| STEREO-A IMPACT/PLASTIC | L2 | high cadence | 2023-03-13 ± 2 d | STEREO archive | abstract: load + decode + subset |
| Multi-observer coronagraphs + EUV | L1.5 | event | 2023-03-13 | agency archives | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Time-resolved θ_Bn, Mach number; 3D-surface kinematic parameters; consistency with widespread-ESP front (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Cross-mission magnetometer-frame alignment
- Local-shock-fit ambiguity in turbulent upstream
- Time-of-flight alignment across observers

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event 2023-03-13; multi-observer (PSP/SO/STEREO-A/near-Earth/MAVEN/BepiColombo — TODO_verify); local Rankine-Hugoniot shock parameters and surface evolution.

**Out of scope — do NOT generalize beyond:**

- Do not extrapolate the local fits to longitudes not covered by observers.
- Do not use as evidence for a specific acceleration mechanism without coupling to a transport model.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2511.03496
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-dresing-2025-widespread-esp-march-2023]]` — assumed for context (see linked skill).
- `[[paper-kouloumvakos-2026-iva-shock-properties]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No combined evolution model that uses the 2023-03-13 shock fit + MHD propagation forward into 1 au observers.
- **Hypothesis** — Local shock θ_Bn evolution explains the circumsolar ESP signature better than a single global Mach number.
- **Minimal_experiment** — Couple the Rankine-Hugoniot time-series to ENLIL/EUHFORIA hindcast and back-test ESP timing.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
