---
name: paper-cohen-2026-coronal-flux-tube-shock-spot-newyearseve-2023
description: >-
  Use when 2023-12-31 eruption or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: The 2023-12-31 eruption produced a localized 'shock spot' that illuminated a coronal flux tube, identified through coordinated remote-sensing and in-situ + radio diagnostics. (arXiv:2512.24749, 2025).
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
  title: "Coronal flux tube illuminated by strong shock spot: New Year's Eve solar eruption of 2023-Dec-31"
  first_author: null
  authors: []
  authors_verified: false
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2512.24749"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [SDO, STEREO-A, Solar Orbiter, PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "2023-12-31 eruption"
  - "coronal flux tube"
  - "shock spot illumination"
  - "type II structure"
  - "near-Sun shock geometry"

data_products:
  - instrument: "SDO/AIA + STEREO-A SECCHI + Solar Orbiter EUI"
    level: "L1.5"
    cadence: "event"
    interval: "2023-12-31"
    archive: "JSOC / STEREO / SOAR"
  - instrument: "Wind/WAVES + PSP/FIELDS LFR radio"
    level: "L2"
    cadence: "minute"
    interval: "2023-12-31"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Localized shock-spot identification from EUV/coronagraph"
    equation_refs: []
    external_implementations: []
  - name: "Type II band-pair fit (fundamental + harmonic)"
    equation_refs: []
    external_implementations: []
  - name: "Flux-tube geometry mapping"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2512.24749"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single eruption 2023-12-31; multi-vantage SECCHI/AIA/EUI + radio diagnostics; localized shock-spot identification with no event statistics.
  out_of_scope:
    - "Do not generalize the shock-spot mechanism without a multi-event statistical study."

failure_modes:
  - "Shock-spot localization sensitive to viewpoint geometry"
  - "Type II band-pair confusion under multi-component sources"

depends_on:
  - "paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks"
  - "paper-liu-2026-3d-coronal-shock-longitudinal-sep"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No catalog of shock-spot–illuminated flux tubes across the SO+PSP era."
    related_skills: []
  - type: "hypothesis"
    statement: "Shock-spot illumination correlates with locally enhanced θ_Bn perpendicular to the flux tube."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Identify three additional events with similar EUV+radio coincidence and test the θ_Bn correlation."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2512.24749"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Coronal flux tube illuminated by strong shock spot: New Year's Eve solar eruption of 2023-Dec-31 — paper-skill

> Compiled from arXiv:2512.24749 (2025), unverified author et al.
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

- 2023-12-31 eruption
- coronal flux tube
- shock spot illumination

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** The 2023-12-31 eruption produced a localized 'shock spot' that illuminated a coronal flux tube, identified through coordinated remote-sensing and in-situ + radio diagnostics.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Identified flux-tube illumination via simultaneous EUV + type II signature (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Localized shock-spot identification from EUV/coronagraph

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Localized shock-spot identification from EUV/coronagraph as a callable on the data products in §4.

### Type II band-pair fit (fundamental + harmonic)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Type II band-pair fit (fundamental + harmonic) as a callable on the data products in §4.

### Flux-tube geometry mapping

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Flux-tube geometry mapping as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| SDO/AIA + STEREO-A SECCHI + Solar Orbiter EUI | L1.5 | event | 2023-12-31 | JSOC / STEREO / SOAR | abstract: load + decode + subset |
| Wind/WAVES + PSP/FIELDS LFR radio | L2 | minute | 2023-12-31 | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Identified flux-tube illumination via simultaneous EUV + type II signature (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Shock-spot localization sensitive to viewpoint geometry
- Type II band-pair confusion under multi-component sources

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single eruption 2023-12-31; multi-vantage SECCHI/AIA/EUI + radio diagnostics; localized shock-spot identification with no event statistics.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the shock-spot mechanism without a multi-event statistical study.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2512.24749
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks]]` — assumed for context (see linked skill).
- `[[paper-liu-2026-3d-coronal-shock-longitudinal-sep]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No catalog of shock-spot–illuminated flux tubes across the SO+PSP era.
- **Hypothesis** — Shock-spot illumination correlates with locally enhanced θ_Bn perpendicular to the flux tube.
- **Minimal_experiment** — Identify three additional events with similar EUV+radio coincidence and test the θ_Bn correlation.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
