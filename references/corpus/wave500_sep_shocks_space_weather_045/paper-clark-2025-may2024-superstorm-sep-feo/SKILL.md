---
name: paper-clark-2025-may2024-superstorm-sep-feo
description: >-
  Use when may 2024 superstorm or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: SEP Fe/O abundance ratios during the May 2024 superstorm show characteristic energy dependence that reflects the compound nature of the driver and shock-acceleration of suprathermal seed populations. (arXiv:2511.03905, 2025).
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
  title: "Energy-dependent SEP Fe/O abundances during the May 2024 superstorm"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2511.03905"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP, Solar Orbiter, ACE, Wind, STEREO-A]
  regime: [inner-heliosphere]

trigger_keywords:
  - "May 2024 superstorm"
  - "Fe/O abundance"
  - "energy dependence"
  - "multi-observer composition"
  - "compound event"

data_products:
  - instrument: "PSP/IS☉IS EPI-Hi + EPI-Lo composition"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "May 2024 storm"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "Solar Orbiter EPD/SIS+HET composition"
    level: "L2"
    cadence: "instrument-native"
    interval: "May 2024 storm"
    archive: "ESA SOAR"
  - instrument: "ACE/SIS + Wind/EPACT + STEREO-A LET/HET"
    level: "L2"
    cadence: "instrument-native"
    interval: "May 2024 storm"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Cross-mission Fe/O energy-spectrum harmonization"
    equation_refs: []
    external_implementations: []
  - name: "Per-event Fe/O vs energy power-law fit"
    equation_refs: []
    external_implementations: []
  - name: "Compound-event decomposition (multiple CMEs / shocks)"
    equation_refs: []
    external_implementations: []
  - name: "Seed-population diagnostic"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2511.03905"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    May 2024 superstorm composite event; multi-observer (TODO_verify); Fe/O vs energy spectrum only.
  out_of_scope:
    - "Do not use Fe/O alone as a flare-vs-shock classifier."
    - "Do not generalize compound-event behavior to single CME events."

failure_modes:
  - "Cross-instrument Fe/O calibration differs by O(1) factors"
  - "Compound-event boundaries are subjective"
  - "Suprathermal seed identification requires independent corroboration"

depends_on:
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"
  - "paper-reames-2026-physics-of-seps"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No multi-event compound-event Fe/O statistical study across cycle 25."
    related_skills: []
  - type: "hypothesis"
    statement: "Compound-event Fe/O energy dependence is steeper than single-CME events at the same shock strength."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Compile cycle-25 compound vs single-CME events and compare Fe/O(E) slopes."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2511.03905"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Energy-dependent SEP Fe/O abundances during the May 2024 superstorm — paper-skill

> Compiled from arXiv:2511.03905 (2025), TODO verify et al.
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

- May 2024 superstorm
- Fe/O abundance
- energy dependence

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SEP Fe/O abundance ratios during the May 2024 superstorm show characteristic energy dependence that reflects the compound nature of the driver and shock-acceleration of suprathermal seed populations.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Fe/O(E) power-law parameters per observer; compound-event substructure (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Cross-mission Fe/O energy-spectrum harmonization

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-mission Fe/O energy-spectrum harmonization as a callable on the data products in §4.

### Per-event Fe/O vs energy power-law fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-event Fe/O vs energy power-law fit as a callable on the data products in §4.

### Compound-event decomposition (multiple CMEs / shocks)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Compound-event decomposition (multiple CMEs / shocks) as a callable on the data products in §4.

### Seed-population diagnostic

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Seed-population diagnostic as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/IS☉IS EPI-Hi + EPI-Lo composition | L2/L3 | instrument-native | May 2024 storm | NASA CDAWeb / PSP SOC | abstract: load + decode + subset |
| Solar Orbiter EPD/SIS+HET composition | L2 | instrument-native | May 2024 storm | ESA SOAR | abstract: load + decode + subset |
| ACE/SIS + Wind/EPACT + STEREO-A LET/HET | L2 | instrument-native | May 2024 storm | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Fe/O(E) power-law parameters per observer; compound-event substructure (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Cross-instrument Fe/O calibration differs by O(1) factors
- Compound-event boundaries are subjective
- Suprathermal seed identification requires independent corroboration

## 7. Claim boundary  *(Layer 1)*

**In scope.** May 2024 superstorm composite event; multi-observer (TODO_verify); Fe/O vs energy spectrum only.

**Out of scope — do NOT generalize beyond:**

- Do not use Fe/O alone as a flare-vs-shock classifier.
- Do not generalize compound-event behavior to single CME events.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2511.03905
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` — assumed for context (see linked skill).
- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No multi-event compound-event Fe/O statistical study across cycle 25.
- **Hypothesis** — Compound-event Fe/O energy dependence is steeper than single-CME events at the same shock strength.
- **Minimal_experiment** — Compile cycle-25 compound vs single-CME events and compare Fe/O(E) slopes.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
