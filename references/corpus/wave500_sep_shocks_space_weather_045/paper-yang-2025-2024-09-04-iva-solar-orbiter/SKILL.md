---
name: paper-yang-2025-2024-09-04-iva-solar-orbiter
description: >-
  Use when solar orbiter iva event or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: A Solar Orbiter SEP event exhibits inverse velocity dispersion that is explained by a time-dependent shock-acceleration model. (arXiv:2507.00954, 2025).
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
  title: "Inverse Velocity Dispersion of Solar Energetic Protons Observed by Solar Orbiter and Its Shock Acceleration Explanation"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2507.00954"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Solar Orbiter]
  regime: [inner-heliosphere]

trigger_keywords:
  - "Solar Orbiter IVA event"
  - "inverse velocity dispersion"
  - "shock-acceleration explanation"

data_products:
  - instrument: "Solar Orbiter/EPD HET"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event window TODO_verify"
    archive: "ESA SOAR"
  - instrument: "Solar Orbiter/MAG"
    level: "L2"
    cadence: "high cadence"
    interval: "Same interval"
    archive: "ESA SOAR"

algorithms:
  - name: "Contour-line-of-intensity IVA detection"
    equation_refs: []
    external_implementations: []
  - name: "Time-dependent shock-acceleration fit"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2507.00954"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event (TODO_verify date); Solar Orbiter EPD; IVA + shock acceleration model.
  out_of_scope:
    - "Do not generalize across many events from one IVA case."

failure_modes:
  - "Single-spacecraft IVA detection"
  - "Time-dependent shock-acceleration model parameter degeneracy"

depends_on:
  - "paper-xu-2026-psp-iva-sep-events"
  - "paper-kouloumvakos-2026-iva-shock-properties"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "Joint Solar Orbiter + PSP IVA catalog still incomplete."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Add Solar Orbiter IVA events to the PSP catalog; refit joint statistics."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2507.00954"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Inverse Velocity Dispersion of Solar Energetic Protons Observed by Solar Orbiter and Its Shock Acceleration Explanation — paper-skill

> Compiled from arXiv:2507.00954 (2025), TODO verify et al.
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

- Solar Orbiter IVA event
- inverse velocity dispersion
- shock-acceleration explanation

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A Solar Orbiter SEP event exhibits inverse velocity dispersion that is explained by a time-dependent shock-acceleration model.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces IVA detection + acceleration-model fit (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Contour-line-of-intensity IVA detection

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Contour-line-of-intensity IVA detection as a callable on the data products in §4.

### Time-dependent shock-acceleration fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Time-dependent shock-acceleration fit as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Solar Orbiter/EPD HET | L2 | instrument-native | Event window TODO_verify | ESA SOAR | abstract: load + decode + subset |
| Solar Orbiter/MAG | L2 | high cadence | Same interval | ESA SOAR | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: IVA detection + acceleration-model fit (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Single-spacecraft IVA detection
- Time-dependent shock-acceleration model parameter degeneracy

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event (TODO_verify date); Solar Orbiter EPD; IVA + shock acceleration model.

**Out of scope — do NOT generalize beyond:**

- Do not generalize across many events from one IVA case.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2507.00954
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-xu-2026-psp-iva-sep-events]]` — assumed for context (see linked skill).
- `[[paper-kouloumvakos-2026-iva-shock-properties]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — Joint Solar Orbiter + PSP IVA catalog still incomplete.
- **Minimal_experiment** — Add Solar Orbiter IVA events to the PSP catalog; refit joint statistics.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
