---
name: paper-mason-2026-sunward-3he-rich-sep-solo-psp
description: >-
  Use when 3he-rich sep or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: PSP and Solar Orbiter observe 3He-rich SEP events near perihelion exhibiting Sunward streaming, indicating reflected / mirrored / backward-streaming behavior beyond canonical impulsive forward-streaming expectations. (arXiv:2601.20624, 2026).
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
  title: "Sunward Streaming 3He-rich SEP Events Observed by Solar Orbiter and Parker Solar Probe during Perihelion Passage"
  first_author: null
  authors: []
  authors_verified: false
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2601.20624"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Solar Orbiter, PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "3He-rich SEP"
  - "Sunward streaming"
  - "impulsive event"
  - "Solar Orbiter EPD/SIS"
  - "PSP IS☉IS EPI-Lo"
  - "perihelion passage"

data_products:
  - instrument: "Solar Orbiter/EPD SIS+STEP+EPT"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event windows"
    archive: "ESA SOAR"
  - instrument: "PSP/IS☉IS EPI-Lo"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event windows"
    archive: "NASA CDAWeb / PSP SOC"

algorithms:
  - name: "3He-rich event identification (3He/4He ratio threshold)"
    equation_refs: []
    external_implementations: []
  - name: "Pitch-angle distribution / first-order anisotropy"
    equation_refs: []
    external_implementations: []
  - name: "Sunward vs anti-Sunward streaming classification"
    equation_refs: []
    external_implementations: []
  - name: "Connectivity check (PFSS + ballistic)"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2601.20624"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Conjunction-event sample (TODO_verify dates); Solar Orbiter EPD/SIS + PSP IS☉IS EPI-Lo; pitch-angle / first-order anisotropy; near-perihelion only.
  out_of_scope:
    - "Do not generalize Sunward 3He-rich behavior to gradual events."
    - "Do not use mirror-point interpretation without an explicit field-line model."

failure_modes:
  - "3He/4He fits sensitive to mass-resolution and background"
  - "Sunward streaming may arise from mirror points beyond observer rather than truly Sunward source"
  - "Single-spacecraft pitch-angle coverage limits anisotropy inference"

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No multi-event 3He-rich anisotropy atlas tied to Heliographic latitude and magnetic-connectivity class."
    related_skills: []
  - type: "hypothesis"
    statement: "Near-perihelion Sunward 3He-rich events trace open-field regions where mirror points lie inside ~1 au."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Tabulate Sunward / anti-Sunward 3He events across all PSP–SOLO conjunctions and check mirror-point distance distribution."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2601.20624"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Sunward Streaming 3He-rich SEP Events Observed by Solar Orbiter and Parker Solar Probe during Perihelion Passage — paper-skill

> Compiled from arXiv:2601.20624 (2026), unverified author et al.
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

- 3He-rich SEP
- Sunward streaming
- impulsive event

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PSP and Solar Orbiter observe 3He-rich SEP events near perihelion exhibiting Sunward streaming, indicating reflected / mirrored / backward-streaming behavior beyond canonical impulsive forward-streaming expectations.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Per-event 3He/4He ratio above impulsive-event threshold; Sunward-streaming anisotropy (numerics TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### 3He-rich event identification (3He/4He ratio threshold)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - 3He-rich event identification (3He/4He ratio threshold) as a callable on the data products in §4.

### Pitch-angle distribution / first-order anisotropy

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Pitch-angle distribution / first-order anisotropy as a callable on the data products in §4.

### Sunward vs anti-Sunward streaming classification

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Sunward vs anti-Sunward streaming classification as a callable on the data products in §4.

### Connectivity check (PFSS + ballistic)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Connectivity check (PFSS + ballistic) as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Solar Orbiter/EPD SIS+STEP+EPT | L2 | instrument-native | Event windows | ESA SOAR | abstract: load + decode + subset |
| PSP/IS☉IS EPI-Lo | L2 | instrument-native | Event windows | NASA CDAWeb / PSP SOC | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Per-event 3He/4He ratio above impulsive-event threshold; Sunward-streaming anisotropy (numerics TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- 3He/4He fits sensitive to mass-resolution and background
- Sunward streaming may arise from mirror points beyond observer rather than truly Sunward source
- Single-spacecraft pitch-angle coverage limits anisotropy inference

## 7. Claim boundary  *(Layer 1)*

**In scope.** Conjunction-event sample (TODO_verify dates); Solar Orbiter EPD/SIS + PSP IS☉IS EPI-Lo; pitch-angle / first-order anisotropy; near-perihelion only.

**Out of scope — do NOT generalize beyond:**

- Do not generalize Sunward 3He-rich behavior to gradual events.
- Do not use mirror-point interpretation without an explicit field-line model.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2601.20624
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).
- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No multi-event 3He-rich anisotropy atlas tied to Heliographic latitude and magnetic-connectivity class.
- **Hypothesis** — Near-perihelion Sunward 3He-rich events trace open-field regions where mirror points lie inside ~1 au.
- **Minimal_experiment** — Tabulate Sunward / anti-Sunward 3He events across all PSP–SOLO conjunctions and check mirror-point distance distribution.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
