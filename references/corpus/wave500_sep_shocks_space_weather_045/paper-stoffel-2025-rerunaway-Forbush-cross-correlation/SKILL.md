---
name: paper-stoffel-2025-rerunaway-Forbush-cross-correlation
description: >-
  Use when forbush decrease or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Cross-correlation between solar-activity indices (Kp/Dst/sunspot/F10.7/etc.) and GCR flux during Forbush-decrease events reveals lag/structure relationships that constrain how ICME shocks modulate the cosmic-ray flux. (arXiv:2604.06383, 2026).
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
  title: "New insights from cross-correlation studies between solar activity indices and cosmic-ray flux during Forbush decrease events"
  first_author: "Stoffel, T."
  authors:
    - "et al."
  authors_complete: false
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2604.06383"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Neutron monitor network (NMDB), OMNI]
  regime: [inner-heliosphere]

trigger_keywords:
  - "Forbush decrease"
  - "cosmic-ray modulation"
  - "solar activity index"
  - "neutron monitor"
  - "cross-correlation lag"
  - "ICME shock geoeffectiveness"

data_products:
  - instrument: "NMDB neutron monitor"
    level: "L1"
    cadence: "hourly"
    interval: "Event windows TODO_verify"
    archive: "NMDB"
  - instrument: "OMNI solar activity / geomagnetic indices"
    level: "L2"
    cadence: "hourly"
    interval: "Event windows"
    archive: "NASA OMNI"

algorithms:
  - name: "Forbush-decrease event identification (threshold on GCR flux deficit)"
    equation_refs: []
    external_implementations: []
  - name: "Cross-correlation function: CR flux vs each index"
    equation_refs: []
    external_implementations: []
  - name: "Lag-extremum tabulation per event class"
    equation_refs: []
    external_implementations: []
  - name: "ICME-driven vs CIR-driven sub-classification"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.06383"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Statistical Forbush decrease catalog (TODO verify date range); neutron-monitor GCR flux vs solar/geomagnetic indices; lag analysis with cross-correlation function (no claim of causal mechanism beyond linear lag).
  out_of_scope:
    - "Do not interpret correlation lags as causal mechanisms."
    - "Do not extrapolate to high-rigidity GCRs without rigidity-resolved analysis."
    - "Do not use for solar-cycle-averaged modulation statements without explicit cycle context."

failure_modes:
  - "Neutron-monitor rigidity cut-off varies by station — homogenize first"
  - "ICME superposition during recurrent activity blurs single-event lag"
  - "Geomagnetic indices share trends with CR flux at long lags — control"
  - "Magnetograph data quality during cycle-25 ramp may bias activity-index baselines"

depends_on:
  - "paper-dalla-2026-radiation-doses-extreme-seps"
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No joint CIR vs ICME Forbush-decrease decomposition with conjunction observers across radial distance."
    related_skills: []
  - type: "hypothesis"
    statement: "CIR-driven and ICME-driven Forbush decreases obey different lag-amplitude scaling vs solar-wind ram pressure."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Split a Forbush catalog by driver (CIR vs ICME) and re-run the lag analysis; compare lag distributions."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2604.06383"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# New insights from cross-correlation studies between solar activity indices and cosmic-ray flux during Forbush decrease events — paper-skill

> Compiled from arXiv:2604.06383 (2026), Stoffel, T. et al.
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

- Forbush decrease
- cosmic-ray modulation
- solar activity index

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Cross-correlation between solar-activity indices (Kp/Dst/sunspot/F10.7/etc.) and GCR flux during Forbush-decrease events reveals lag/structure relationships that constrain how ICME shocks modulate the cosmic-ray flux.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Per-class lag distributions; statistically significant negative correlation peaks (TODO_verify numerical lag values from full text). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Forbush-decrease event identification (threshold on GCR flux deficit)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Forbush-decrease event identification (threshold on GCR flux deficit) as a callable on the data products in §4.

### Cross-correlation function: CR flux vs each index

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-correlation function: CR flux vs each index as a callable on the data products in §4.

### Lag-extremum tabulation per event class

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Lag-extremum tabulation per event class as a callable on the data products in §4.

### ICME-driven vs CIR-driven sub-classification

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - ICME-driven vs CIR-driven sub-classification as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| NMDB neutron monitor | L1 | hourly | Event windows TODO_verify | NMDB | abstract: load + decode + subset |
| OMNI solar activity / geomagnetic indices | L2 | hourly | Event windows | NASA OMNI | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Per-class lag distributions; statistically significant negative correlation peaks (TODO_verify numerical lag values from full text).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Neutron-monitor rigidity cut-off varies by station — homogenize first
- ICME superposition during recurrent activity blurs single-event lag
- Geomagnetic indices share trends with CR flux at long lags — control
- Magnetograph data quality during cycle-25 ramp may bias activity-index baselines

## 7. Claim boundary  *(Layer 1)*

**In scope.** Statistical Forbush decrease catalog (TODO verify date range); neutron-monitor GCR flux vs solar/geomagnetic indices; lag analysis with cross-correlation function (no claim of causal mechanism beyond linear lag).

**Out of scope — do NOT generalize beyond:**

- Do not interpret correlation lags as causal mechanisms.
- Do not extrapolate to high-rigidity GCRs without rigidity-resolved analysis.
- Do not use for solar-cycle-averaged modulation statements without explicit cycle context.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2604.06383
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-dalla-2026-radiation-doses-extreme-seps]]` — assumed for context (see linked skill).
- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No joint CIR vs ICME Forbush-decrease decomposition with conjunction observers across radial distance.
- **Hypothesis** — CIR-driven and ICME-driven Forbush decreases obey different lag-amplitude scaling vs solar-wind ram pressure.
- **Minimal_experiment** — Split a Forbush catalog by driver (CIR vs ICME) and re-run the lag analysis; compare lag distributions.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
