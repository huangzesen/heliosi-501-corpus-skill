---
name: paper-pereira-2026-connection-angle-gle-anisotropy
description: >-
  Use when gle proton anisotropy or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Proton anisotropy in GLE events correlates with magnetic-connection angle between the observer and the source region. (arXiv:2603.19953, 2026).
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
  title: "Connection-angle dependence of proton anisotropy in ground-level enhancement events"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2603.19953"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Neutron monitor network, GOES]
  regime: [inner-heliosphere]

trigger_keywords:
  - "GLE proton anisotropy"
  - "connection-angle dependence"
  - "neutron monitor network"
  - "GLE-event catalog"

data_products:
  - instrument: "NMDB neutron monitor"
    level: "L1"
    cadence: "1-min"
    interval: "GLE catalog"
    archive: "NMDB"
  - instrument: "GOES SEM proton"
    level: "L2"
    cadence: "5-min"
    interval: "GLE catalog"
    archive: "NOAA"

algorithms:
  - name: "Per-event connection-angle determination"
    equation_refs: []
    external_implementations: []
  - name: "Anisotropy fit from multi-station NM differences"
    equation_refs: []
    external_implementations: []
  - name: "Connection-angle vs anisotropy regression"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2603.19953"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Statistical GLE-event catalog (TODO_verify); proton anisotropy vs connection angle.
  out_of_scope:
    - "Do not generalize the relation to non-GLE SEP events without separate analysis."

failure_modes:
  - "Connection-angle determination depends on PFSS"
  - "Single-station NM anisotropy is weak"

depends_on:
  - "paper-mason-2026-unusual-2024-june-8-gle"
  - "paper-mishev-2026-first-four-gles-1940s"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No combined NM + multi-observer in-situ analysis of GLE proton anisotropy."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Cross-match GOES + STEREO-A relativistic-channel anisotropy with NM-derived anisotropy for the same GLEs."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2603.19953"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Connection-angle dependence of proton anisotropy in ground-level enhancement events — paper-skill

> Compiled from arXiv:2603.19953 (2026), TODO verify et al.
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

- GLE proton anisotropy
- connection-angle dependence
- neutron monitor network

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Proton anisotropy in GLE events correlates with magnetic-connection angle between the observer and the source region.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Connection-angle vs anisotropy correlation (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Per-event connection-angle determination

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-event connection-angle determination as a callable on the data products in §4.

### Anisotropy fit from multi-station NM differences

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Anisotropy fit from multi-station NM differences as a callable on the data products in §4.

### Connection-angle vs anisotropy regression

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Connection-angle vs anisotropy regression as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| NMDB neutron monitor | L1 | 1-min | GLE catalog | NMDB | abstract: load + decode + subset |
| GOES SEM proton | L2 | 5-min | GLE catalog | NOAA | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Connection-angle vs anisotropy correlation (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Connection-angle determination depends on PFSS
- Single-station NM anisotropy is weak

## 7. Claim boundary  *(Layer 1)*

**In scope.** Statistical GLE-event catalog (TODO_verify); proton anisotropy vs connection angle.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the relation to non-GLE SEP events without separate analysis.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2603.19953
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-mason-2026-unusual-2024-june-8-gle]]` — assumed for context (see linked skill).
- `[[paper-mishev-2026-first-four-gles-1940s]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No combined NM + multi-observer in-situ analysis of GLE proton anisotropy.
- **Minimal_experiment** — Cross-match GOES + STEREO-A relativistic-channel anisotropy with NM-derived anisotropy for the same GLEs.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
