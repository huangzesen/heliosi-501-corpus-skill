---
name: paper-allen-2024-radial-evolution-icme-sep-solo-ace
description: >-
  Use when icme radial evolution or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: ICME-associated particle acceleration measured at Solar Orbiter and ACE during radial conjunctions traces the radial evolution of the driving shock. (arXiv:2410.01885, 2024).
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
  title: "Radial Evolution of ICME-Associated Particle Acceleration Observed by Solar Orbiter and ACE"
  first_author: null
  authors: []
  authors_verified: false
  year: 2024
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2410.01885"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Solar Orbiter, ACE]
  regime: [inner-heliosphere]

trigger_keywords:
  - "ICME radial evolution"
  - "Solar Orbiter ACE conjunction"
  - "ICME-driven shock acceleration"

data_products:
  - instrument: "Solar Orbiter EPD HET/EPT/SIS"
    level: "L2"
    cadence: "instrument-native"
    interval: "Conjunction events"
    archive: "ESA SOAR"
  - instrument: "ACE EPAM + SIS + ULEIS"
    level: "L2"
    cadence: "instrument-native"
    interval: "Conjunction events"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Cross-mission energy-channel matching"
    equation_refs: []
    external_implementations: []
  - name: "Per-conjunction Rankine-Hugoniot fit"
    equation_refs: []
    external_implementations: []
  - name: "Radial evolution metric (intensity / spectral index)"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2410.01885"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Solar Orbiter + ACE radial conjunctions (TODO_verify event list); ICME-shock + SEP cross-correlation.
  out_of_scope:
    - "Do not generalize beyond the conjunction-event sample."

failure_modes:
  - "Cross-mission inter-calibration"
  - "Conjunction quality varies (angular separation tolerance)"

depends_on:
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"
  - "paper-luo-2025-2023-july-17-radial-ion-fluence-psp"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "Joint SO + ACE + PSP radial atlas missing."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Add PSP–SO–ACE triple-conjunction events; refit the radial evolution metric."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2410.01885"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Radial Evolution of ICME-Associated Particle Acceleration Observed by Solar Orbiter and ACE — paper-skill

> Compiled from arXiv:2410.01885 (2024), unverified author et al.
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

- ICME radial evolution
- Solar Orbiter ACE conjunction
- ICME-driven shock acceleration

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** ICME-associated particle acceleration measured at Solar Orbiter and ACE during radial conjunctions traces the radial evolution of the driving shock.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Per-event radial evolution of intensity / spectral index (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Cross-mission energy-channel matching

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-mission energy-channel matching as a callable on the data products in §4.

### Per-conjunction Rankine-Hugoniot fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-conjunction Rankine-Hugoniot fit as a callable on the data products in §4.

### Radial evolution metric (intensity / spectral index)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Radial evolution metric (intensity / spectral index) as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Solar Orbiter EPD HET/EPT/SIS | L2 | instrument-native | Conjunction events | ESA SOAR | abstract: load + decode + subset |
| ACE EPAM + SIS + ULEIS | L2 | instrument-native | Conjunction events | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Per-event radial evolution of intensity / spectral index (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Cross-mission inter-calibration
- Conjunction quality varies (angular separation tolerance)

## 7. Claim boundary  *(Layer 1)*

**In scope.** Solar Orbiter + ACE radial conjunctions (TODO_verify event list); ICME-shock + SEP cross-correlation.

**Out of scope — do NOT generalize beyond:**

- Do not generalize beyond the conjunction-event sample.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2410.01885
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` — assumed for context (see linked skill).
- `[[paper-luo-2025-2023-july-17-radial-ion-fluence-psp]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — Joint SO + ACE + PSP radial atlas missing.
- **Minimal_experiment** — Add PSP–SO–ACE triple-conjunction events; refit the radial evolution metric.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
