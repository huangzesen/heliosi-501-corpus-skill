---
name: paper-mason-2025-icme-may16-2023-composition-variation
description: >-
  Use when 2023-05-16 sep event or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: PSP and SOLO at similar radial distance (~0.7 au) but ~60° apart in longitude observe the 2023-05-16 SEP event: PSP sees Fe-rich (Fe/O ≈ 0.48), SOLO Fe-poor (Fe/O ≈ 0.08); He/H also differs by ~2×; spectra fit Band function; differences per… (arXiv:2410.19672, 2025).
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
  title: "Composition variation of the May 16 2023 Solar Energetic Particle Event observed by Solar Orbiter and Parker Solar Probe"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2410.19672"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP, Solar Orbiter]
  regime: [inner-heliosphere]

trigger_keywords:
  - "2023-05-16 SEP event"
  - "PSP SOLO conjunction 0.7 au"
  - "Fe/O ratio"
  - "He/H ratio"
  - "Band-function spectral fit"
  - "flare contribution"

data_products:
  - instrument: "PSP/IS☉IS EPI-Hi + EPI-Lo composition"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "2023-05-16 ± 2 d"
    archive: "PSP SOC"
  - instrument: "Solar Orbiter EPD/SIS + HET"
    level: "L2"
    cadence: "instrument-native"
    interval: "2023-05-16 ± 2 d"
    archive: "ESA SOAR"

algorithms:
  - name: "Band-function spectral fit per species per observer"
    equation_refs: []
    external_implementations: []
  - name: "Fe/O and He/H ratio time series"
    equation_refs: []
    external_implementations: []
  - name: "Sunward / anti-Sunward sectoring"
    equation_refs: []
    external_implementations: []
  - name: "Direct-flare-contribution diagnostic"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2410.19672"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event 2023-05-16; PSP and SOLO at ~0.7 au; longitude separation ~60°; H, He, O, Fe spectra 0.1–10 MeV/nuc; Sunward + anti-Sunward directions.
  out_of_scope:
    - "Do not generalize the longitudinal Fe/O contrast to all SEP events."

failure_modes:
  - "Cross-instrument composition calibration"
  - "Time-of-flight alignment for joint spectra"
  - "Direct-flare-contribution attribution is event-specific"

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-clark-2025-may2024-superstorm-sep-feo"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No longitudinal Fe/O atlas at matched radial distance for PSP-era events."
    related_skills: []
  - type: "hypothesis"
    statement: "Fe-rich vs Fe-poor across longitude tracks footpoint-to-flare distance more strongly than to-shock distance."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Repeat the analysis for two additional PSP–SOLO ~0.7 au quasi-aligned events."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2410.19672"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Composition variation of the May 16 2023 Solar Energetic Particle Event observed by Solar Orbiter and Parker Solar Probe — paper-skill

> Compiled from arXiv:2410.19672 (2025), TODO verify et al.
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

- 2023-05-16 SEP event
- PSP SOLO conjunction 0.7 au
- Fe/O ratio

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PSP and SOLO at similar radial distance (~0.7 au) but ~60° apart in longitude observe the 2023-05-16 SEP event: PSP sees Fe-rich (Fe/O ≈ 0.48), SOLO Fe-poor (Fe/O ≈ 0.08); He/H also differs by ~2×; spectra fit Band function; differences persist throughout event suggesting direct flare contribution at PSP.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Fe/O ≈ 0.48 at PSP, ≈ 0.08 at SOLO over 0.1–10 MeV/nuc; He/H factor-of-2 higher at PSP; persistent differences throughout event. within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Band-function spectral fit per species per observer

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Band-function spectral fit per species per observer as a callable on the data products in §4.

### Fe/O and He/H ratio time series

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Fe/O and He/H ratio time series as a callable on the data products in §4.

### Sunward / anti-Sunward sectoring

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Sunward / anti-Sunward sectoring as a callable on the data products in §4.

### Direct-flare-contribution diagnostic

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Direct-flare-contribution diagnostic as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/IS☉IS EPI-Hi + EPI-Lo composition | L2/L3 | instrument-native | 2023-05-16 ± 2 d | PSP SOC | abstract: load + decode + subset |
| Solar Orbiter EPD/SIS + HET | L2 | instrument-native | 2023-05-16 ± 2 d | ESA SOAR | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Fe/O ≈ 0.48 at PSP, ≈ 0.08 at SOLO over 0.1–10 MeV/nuc; He/H factor-of-2 higher at PSP; persistent differences throughout event.

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Cross-instrument composition calibration
- Time-of-flight alignment for joint spectra
- Direct-flare-contribution attribution is event-specific

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event 2023-05-16; PSP and SOLO at ~0.7 au; longitude separation ~60°; H, He, O, Fe spectra 0.1–10 MeV/nuc; Sunward + anti-Sunward directions.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the longitudinal Fe/O contrast to all SEP events.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2410.19672
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).
- `[[paper-clark-2025-may2024-superstorm-sep-feo]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No longitudinal Fe/O atlas at matched radial distance for PSP-era events.
- **Hypothesis** — Fe-rich vs Fe-poor across longitude tracks footpoint-to-flare distance more strongly than to-shock distance.
- **Minimal_experiment** — Repeat the analysis for two additional PSP–SOLO ~0.7 au quasi-aligned events.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
