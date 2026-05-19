---
name: paper-feng-2025-shock-sep-modeling-2022-09-05
description: >-
  Use when 2022-09-05 labor day event or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: The 2022-09-05 SEP event is modeled by coupling a shock-propagation simulation with a SEP transport solver and the resulting intensity profile reproduces the observed PSP near-Sun + 1 au profiles within tolerance. (arXiv:2501.03066, 2025).
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
  title: "Shock and SEP Modeling Study for the 5 September 2022 SEP Event"
  first_author: null
  authors: []
  authors_verified: false
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2501.03066"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP, Solar Orbiter, STEREO-A, Wind, ACE]
  regime: [inner-heliosphere]

trigger_keywords:
  - "2022-09-05 Labor Day event"
  - "shock modeling"
  - "iPATH / EPREM (TODO_verify)"
  - "SEP intensity profile"
  - "Time-dependent DSA"

data_products:
  - instrument: "PSP/IS☉IS EPI-Hi + EPI-Lo"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "2022-09-05 ± 2 d"
    archive: "PSP SOC"
  - instrument: "Multi-mission energetic-particle observers"
    level: "L2"
    cadence: "instrument-native"
    interval: "2022-09-05 ± 2 d"
    archive: "agency archives"

algorithms:
  - name: "MHD shock-propagation simulation (TODO_verify code)"
    equation_refs: []
    external_implementations: []
  - name: "Transport-equation SEP solver (TODO_verify code)"
    equation_refs: []
    external_implementations: []
  - name: "Per-observer intensity-profile prediction"
    equation_refs: []
    external_implementations: []
  - name: "Tolerance check against in-situ time series"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2501.03066"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event 2022-09-05; coupled shock + SEP transport model; PSP near-perihelion + 1 au observers; tolerance on peak intensity / time-of-peak / spectral index.
  out_of_scope:
    - "Do not generalize fitted injection function to other events without re-fit."
    - "Do not use as evidence for a single mechanism over alternatives without ablation."

failure_modes:
  - "Source-region injection function is a strong assumption"
  - "MHD shock geometry sensitive to background-wind initialization"
  - "Cross-mission inter-calibration impacts agreement"

depends_on:
  - "paper-xu-2026-psp-iva-sep-events"
  - "paper-bian-2026-30march2022-sep-data-assimilation"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No standard injection-function library calibrated across IVA-event catalog."
    related_skills: []
  - type: "hypothesis"
    statement: "A single injection-function class can fit multiple Labor-Day-like events with shock-strength scaling."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Refit the same coupled model to 2022-04-17 and 2024-05-11 PSP-near-perihelion events."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2501.03066"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Shock and SEP Modeling Study for the 5 September 2022 SEP Event — paper-skill

> Compiled from arXiv:2501.03066 (2025), unverified author et al.
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

- 2022-09-05 Labor Day event
- shock modeling
- iPATH / EPREM (TODO_verify)

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** The 2022-09-05 SEP event is modeled by coupling a shock-propagation simulation with a SEP transport solver and the resulting intensity profile reproduces the observed PSP near-Sun + 1 au profiles within tolerance.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Per-observer peak intensity / time-of-peak / spectral-index within tolerance (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### MHD shock-propagation simulation (TODO_verify code)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - MHD shock-propagation simulation (TODO_verify code) as a callable on the data products in §4.

### Transport-equation SEP solver (TODO_verify code)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Transport-equation SEP solver (TODO_verify code) as a callable on the data products in §4.

### Per-observer intensity-profile prediction

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-observer intensity-profile prediction as a callable on the data products in §4.

### Tolerance check against in-situ time series

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Tolerance check against in-situ time series as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/IS☉IS EPI-Hi + EPI-Lo | L2/L3 | instrument-native | 2022-09-05 ± 2 d | PSP SOC | abstract: load + decode + subset |
| Multi-mission energetic-particle observers | L2 | instrument-native | 2022-09-05 ± 2 d | agency archives | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Per-observer peak intensity / time-of-peak / spectral-index within tolerance (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Source-region injection function is a strong assumption
- MHD shock geometry sensitive to background-wind initialization
- Cross-mission inter-calibration impacts agreement

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event 2022-09-05; coupled shock + SEP transport model; PSP near-perihelion + 1 au observers; tolerance on peak intensity / time-of-peak / spectral index.

**Out of scope — do NOT generalize beyond:**

- Do not generalize fitted injection function to other events without re-fit.
- Do not use as evidence for a single mechanism over alternatives without ablation.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2501.03066
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-xu-2026-psp-iva-sep-events]]` — assumed for context (see linked skill).
- `[[paper-bian-2026-30march2022-sep-data-assimilation]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No standard injection-function library calibrated across IVA-event catalog.
- **Hypothesis** — A single injection-function class can fit multiple Labor-Day-like events with shock-strength scaling.
- **Minimal_experiment** — Refit the same coupled model to 2022-04-17 and 2024-05-11 PSP-near-perihelion events.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
