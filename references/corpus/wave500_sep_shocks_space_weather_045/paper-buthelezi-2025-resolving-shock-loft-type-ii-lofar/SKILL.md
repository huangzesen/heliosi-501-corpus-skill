---
name: paper-buthelezi-2025-resolving-shock-loft-type-ii-lofar
description: >-
  Use when lofar type ii or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: LOFAR resolves type II band splitting and herringbone fine structure that map onto distinct shock locations / acceleration sites at the coronal shock front. (arXiv:2502.16934, 2025).
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
  title: "Resolving spatial and temporal shock structures using LOFAR observations of type II radio bursts"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2502.16934"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [LOFAR (ground)]
  regime: [inner-heliosphere]

trigger_keywords:
  - "LOFAR type II"
  - "shock fine structure"
  - "type II band splitting"
  - "high-resolution radio imaging"

data_products:
  - instrument: "LOFAR LBA/HBA dynamic spectra + imaging"
    level: "L2"
    cadence: "sub-second"
    interval: "Event windows TODO_verify"
    archive: "LOFAR Long-Term Archive"

algorithms:
  - name: "Dynamic-spectrum band-splitting fit"
    equation_refs: []
    external_implementations: []
  - name: "Imaging-localization of bands"
    equation_refs: []
    external_implementations: []
  - name: "Herringbone burst onset detection"
    equation_refs: []
    external_implementations: []
  - name: "Shock-front mapping from band geometry"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2502.16934"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    LOFAR observations of selected type II bursts (TODO_verify); spatial + temporal resolution at the shock; band-splitting + herringbone localization.
  out_of_scope:
    - "Do not generalize shock fine structure across all events from one LOFAR sample."

failure_modes:
  - "Ionospheric scintillation / RFI artifacts at low frequencies"
  - "Band-split-vs-harmonic confusion"

depends_on:
  - "paper-jin-2025-third-harmonic-type-ii-2024-09-14"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No combined LOFAR + PSP/FIELDS type II band-splitting study using interplanetary continuation."
    related_skills: []
  - type: "hypothesis"
    statement: "LOFAR band-split downstream-side maps onto upstream-trapped electron reservoirs."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Identify a LOFAR + Wind/WAVES type II pair; align bands across coronal-to-IP transition."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2502.16934"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Resolving spatial and temporal shock structures using LOFAR observations of type II radio bursts — paper-skill

> Compiled from arXiv:2502.16934 (2025), TODO verify et al.
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

- LOFAR type II
- shock fine structure
- type II band splitting

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** LOFAR resolves type II band splitting and herringbone fine structure that map onto distinct shock locations / acceleration sites at the coronal shock front.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Per-event resolved shock band map; herringbone count (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Dynamic-spectrum band-splitting fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Dynamic-spectrum band-splitting fit as a callable on the data products in §4.

### Imaging-localization of bands

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Imaging-localization of bands as a callable on the data products in §4.

### Herringbone burst onset detection

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Herringbone burst onset detection as a callable on the data products in §4.

### Shock-front mapping from band geometry

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Shock-front mapping from band geometry as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| LOFAR LBA/HBA dynamic spectra + imaging | L2 | sub-second | Event windows TODO_verify | LOFAR Long-Term Archive | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Per-event resolved shock band map; herringbone count (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Ionospheric scintillation / RFI artifacts at low frequencies
- Band-split-vs-harmonic confusion

## 7. Claim boundary  *(Layer 1)*

**In scope.** LOFAR observations of selected type II bursts (TODO_verify); spatial + temporal resolution at the shock; band-splitting + herringbone localization.

**Out of scope — do NOT generalize beyond:**

- Do not generalize shock fine structure across all events from one LOFAR sample.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2502.16934
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-jin-2025-third-harmonic-type-ii-2024-09-14]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No combined LOFAR + PSP/FIELDS type II band-splitting study using interplanetary continuation.
- **Hypothesis** — LOFAR band-split downstream-side maps onto upstream-trapped electron reservoirs.
- **Minimal_experiment** — Identify a LOFAR + Wind/WAVES type II pair; align bands across coronal-to-IP transition.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
