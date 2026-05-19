---
name: paper-marsh-2024-parasol-sep-forecasting
description: >-
  Use when parasol or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: The PARASOL SEP-forecast model couples solar-eruption inputs with a transport solver to deliver event-time forecasts of SEP intensity and spectrum, with verification on a hold-out set. (arXiv:2412.11852, 2024).
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
  title: "Towards advanced forecasting of solar energetic particle events with the PARASOL model"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2024
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2412.11852"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [GOES, STEREO, ACE, Wind]
  regime: [inner-heliosphere]

trigger_keywords:
  - "PARASOL"
  - "SEP forecast"
  - "operational model"
  - "ensemble forecasting"

data_products:
  - instrument: "GOES SEM/SEISS proton"
    level: "L2"
    cadence: "5-min"
    interval: "Verification set"
    archive: "NOAA"
  - instrument: "Multi-mission SEP context"
    level: "L2"
    cadence: "minute"
    interval: "Verification set"
    archive: "agency archives"

algorithms:
  - name: "Eruption-input ingestion (CME kinematics / flare class)"
    equation_refs: []
    external_implementations: []
  - name: "Coupled transport solver"
    equation_refs: []
    external_implementations: []
  - name: "Per-event ensemble forecast"
    equation_refs: []
    external_implementations: []
  - name: "Verification (TSS / Brier / RMSE)"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2412.11852"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Forecast model description + retrospective verification (TODO_verify catalog); SEP intensity / spectrum prediction.
  out_of_scope:
    - "Do not deploy operationally without an explicit uncertainty quantification."

failure_modes:
  - "Eruption inputs are uncertain at forecast time"
  - "Ensemble spread may underestimate tail risk"

depends_on:
  - "paper-meng-2025-sepnet-multi-task-ml"
  - "paper-feng-2025-shock-sep-modeling-2022-09-05"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No head-to-head benchmark of PARASOL vs SEPNET on a common verification set."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Run both on a shared 2018–2024 event list; compare TSS / RMSE."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2412.11852"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Towards advanced forecasting of solar energetic particle events with the PARASOL model — paper-skill

> Compiled from arXiv:2412.11852 (2024), TODO verify et al.
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

- PARASOL
- SEP forecast
- operational model

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** The PARASOL SEP-forecast model couples solar-eruption inputs with a transport solver to deliver event-time forecasts of SEP intensity and spectrum, with verification on a hold-out set.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Verification scores on hold-out catalog (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Eruption-input ingestion (CME kinematics / flare class)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Eruption-input ingestion (CME kinematics / flare class) as a callable on the data products in §4.

### Coupled transport solver

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Coupled transport solver as a callable on the data products in §4.

### Per-event ensemble forecast

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-event ensemble forecast as a callable on the data products in §4.

### Verification (TSS / Brier / RMSE)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Verification (TSS / Brier / RMSE) as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| GOES SEM/SEISS proton | L2 | 5-min | Verification set | NOAA | abstract: load + decode + subset |
| Multi-mission SEP context | L2 | minute | Verification set | agency archives | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Verification scores on hold-out catalog (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Eruption inputs are uncertain at forecast time
- Ensemble spread may underestimate tail risk

## 7. Claim boundary  *(Layer 1)*

**In scope.** Forecast model description + retrospective verification (TODO_verify catalog); SEP intensity / spectrum prediction.

**Out of scope — do NOT generalize beyond:**

- Do not deploy operationally without an explicit uncertainty quantification.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2412.11852
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-meng-2025-sepnet-multi-task-ml]]` — assumed for context (see linked skill).
- `[[paper-feng-2025-shock-sep-modeling-2022-09-05]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No head-to-head benchmark of PARASOL vs SEPNET on a common verification set.
- **Minimal_experiment** — Run both on a shared 2018–2024 event list; compare TSS / RMSE.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
