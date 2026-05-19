---
name: paper-share-2026-sol2012-06-03-late-phase-gamma-shock
description: >-
  Use when sol2012-06-03 or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Late-phase gamma-ray emission from SOL2012-06-03 is produced by >300 MeV protons accelerated by the CME-driven shock, drawing on suprathermal flare-accelerated ions as a seed population. (arXiv:2602.10284, 2026).
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
  title: "Evidence that SOL2012-06-03 Late Phase gamma-Rays are Produced by >300 MeV Protons from CME-Shock Acceleration of Suprathermals from the Flare"
  first_author: "Share, G. H. (TODO verify)"
  authors:
    - "TODO verify"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2602.10284"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Fermi-LAT, GOES, ACE/Wind]
  regime: [inner-heliosphere]

trigger_keywords:
  - "SOL2012-06-03"
  - "late-phase gamma rays"
  - ">300 MeV protons"
  - "CME-shock reacceleration of suprathermals"
  - "flare seed population"
  - "Fermi LAT"
  - "RHESSI"
  - "long-duration gamma-ray emission"

data_products:
  - instrument: "Fermi/LAT gamma-ray"
    level: "L1"
    cadence: "1-min binning"
    interval: "SOL2012-06-03 ± 1 d"
    archive: "Fermi SSC"
  - instrument: "GOES SEM proton"
    level: "L2"
    cadence: "5-min"
    interval: "SOL2012-06-03 ± 1 d"
    archive: "NOAA"
  - instrument: "ACE/EPAM + Wind/3DP suprathermals"
    level: "L2"
    cadence: "instrument-native"
    interval: "SOL2012-06-03 ± 1 d"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Gamma-ray light-curve + spectrum fit"
    equation_refs: []
    external_implementations: []
  - name: "Proton-energy threshold inversion (≥300 MeV) from gamma-ray pion-decay component"
    equation_refs: []
    external_implementations: []
  - name: "Seed-population test: suprathermal flare ions vs ambient solar wind"
    equation_refs: []
    external_implementations: []
  - name: "Shock kinematics from coronagraph height-time"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.10284"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event SOL2012-06-03; Fermi-LAT (TODO_verify) + supporting in-situ; gamma-ray fluence as a tracer for >300 MeV proton population at the Sun.
  out_of_scope:
    - "Do not generalize to all long-duration gamma-ray events."
    - "Do not infer CME-shock parameters from gamma-rays alone."

failure_modes:
  - "Pion-decay vs bremsstrahlung decomposition relies on instrument response"
  - "Single-event interpretation does not constrain mechanism universally"
  - "Shock-suprathermal coupling assumed; not directly measured"

depends_on:
  - "paper-mason-2026-unusual-2024-june-8-gle"
  - "paper-reames-2026-physics-of-seps"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No multi-event catalog testing shock-acceleration-of-suprathermal-seeds against late-phase gamma-ray emission."
    related_skills: []
  - type: "hypothesis"
    statement: "Long-duration gamma-ray events correlate with high-Mach CME shocks above ~5 R_sun."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Compile a Fermi-LAT long-duration list and cross-match with SOHO/LASCO height-time tables."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2602.10284"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Evidence that SOL2012-06-03 Late Phase gamma-Rays are Produced by >300 MeV Protons from CME-Shock Acceleration of Suprathermals from the Flare — paper-skill

> Compiled from arXiv:2602.10284 (2026), Share, G. H. (TODO verify) et al.
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

- SOL2012-06-03
- late-phase gamma rays
- >300 MeV protons

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Late-phase gamma-ray emission from SOL2012-06-03 is produced by >300 MeV protons accelerated by the CME-driven shock, drawing on suprathermal flare-accelerated ions as a seed population.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Late-phase gamma-ray flux consistent with >300 MeV proton population accelerated at the CME shock with flare suprathermals as the seed (specific numerics TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Gamma-ray light-curve + spectrum fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Gamma-ray light-curve + spectrum fit as a callable on the data products in §4.

### Proton-energy threshold inversion (≥300 MeV) from gamma-ray pion-decay component

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Proton-energy threshold inversion (≥300 MeV) from gamma-ray pion-decay component as a callable on the data products in §4.

### Seed-population test: suprathermal flare ions vs ambient solar wind

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Seed-population test: suprathermal flare ions vs ambient solar wind as a callable on the data products in §4.

### Shock kinematics from coronagraph height-time

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Shock kinematics from coronagraph height-time as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Fermi/LAT gamma-ray | L1 | 1-min binning | SOL2012-06-03 ± 1 d | Fermi SSC | abstract: load + decode + subset |
| GOES SEM proton | L2 | 5-min | SOL2012-06-03 ± 1 d | NOAA | abstract: load + decode + subset |
| ACE/EPAM + Wind/3DP suprathermals | L2 | instrument-native | SOL2012-06-03 ± 1 d | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Late-phase gamma-ray flux consistent with >300 MeV proton population accelerated at the CME shock with flare suprathermals as the seed (specific numerics TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Pion-decay vs bremsstrahlung decomposition relies on instrument response
- Single-event interpretation does not constrain mechanism universally
- Shock-suprathermal coupling assumed; not directly measured

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event SOL2012-06-03; Fermi-LAT (TODO_verify) + supporting in-situ; gamma-ray fluence as a tracer for >300 MeV proton population at the Sun.

**Out of scope — do NOT generalize beyond:**

- Do not generalize to all long-duration gamma-ray events.
- Do not infer CME-shock parameters from gamma-rays alone.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2602.10284
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-mason-2026-unusual-2024-june-8-gle]]` — assumed for context (see linked skill).
- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No multi-event catalog testing shock-acceleration-of-suprathermal-seeds against late-phase gamma-ray emission.
- **Hypothesis** — Long-duration gamma-ray events correlate with high-Mach CME shocks above ~5 R_sun.
- **Minimal_experiment** — Compile a Fermi-LAT long-duration list and cross-match with SOHO/LASCO height-time tables.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
