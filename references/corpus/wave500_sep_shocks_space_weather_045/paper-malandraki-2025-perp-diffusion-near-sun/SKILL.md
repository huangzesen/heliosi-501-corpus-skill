---
name: paper-malandraki-2025-perp-diffusion-near-sun
description: >-
  Use when parallel diffusion or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: PSP in-situ energetic-particle observations constrain parallel and perpendicular diffusion coefficients in the near-Sun solar wind, providing the κ_perp/κ_par ratio at heliocentric distances closer than previously sampled. (arXiv:2509.10648, 2025).
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
  title: "Parallel and perpendicular diffusion of energetic particles in the near-Sun solar wind observed by Parker Solar Probe"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2509.10648"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "parallel diffusion"
  - "perpendicular diffusion"
  - "PSP IS☉IS energetic-particle"
  - "near-Sun heliosphere"
  - "diffusion-coefficient ratio κ_perp / κ_par"

data_products:
  - instrument: "PSP/IS☉IS EPI-Hi + EPI-Lo"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "Near-perihelion events (TODO_verify)"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/FIELDS MAG"
    level: "L2"
    cadence: "high cadence"
    interval: "Same intervals"
    archive: "PSP SOC"

algorithms:
  - name: "Onset-vs-energy and decay-vs-time joint fit"
    equation_refs: []
    external_implementations: []
  - name: "Pitch-angle decay-rate inference for κ_par"
    equation_refs: []
    external_implementations: []
  - name: "Cross-field-spread inference for κ_perp"
    equation_refs: []
    external_implementations: []
  - name: "κ_perp / κ_par ratio extraction"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2509.10648"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    PSP IS☉IS events at ≤0.3 au (TODO_verify); event-based κ_par and κ_perp inferred from intensity / anisotropy / pitch-angle decay; near-Sun only.
  out_of_scope:
    - "Do not extrapolate beyond the measured energy range or distance bin."
    - "Do not use as a turbulence-cascade test without an independent turbulence diagnostic."

failure_modes:
  - "Single-spacecraft cross-field-spread inference is weak; report priors"
  - "Anisotropy saturation in EPI-Lo at high intensity"
  - "Local turbulence-spectrum estimate enters the diffusion derivation"

depends_on:
  - "paper-laitinen-2026-vda-turbulent-heliosphere"
  - "paper-bian-2026-30march2022-sep-data-assimilation"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No paired Solar Orbiter EPD perpendicular-diffusion measurement at matched encounter times."
    related_skills: []
  - type: "hypothesis"
    statement: "κ_perp / κ_par decreases monotonically with heliocentric distance closer than 0.3 au."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Apply the same diffusion fit on a Solar Orbiter HET event during a PSP–SOLO radial alignment."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2509.10648"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Parallel and perpendicular diffusion of energetic particles in the near-Sun solar wind observed by Parker Solar Probe — paper-skill

> Compiled from arXiv:2509.10648 (2025), TODO verify et al.
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

- parallel diffusion
- perpendicular diffusion
- PSP IS☉IS energetic-particle

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PSP in-situ energetic-particle observations constrain parallel and perpendicular diffusion coefficients in the near-Sun solar wind, providing the κ_perp/κ_par ratio at heliocentric distances closer than previously sampled.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces κ_par(E), κ_perp(E), and κ_perp/κ_par at near-Sun distances (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Onset-vs-energy and decay-vs-time joint fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Onset-vs-energy and decay-vs-time joint fit as a callable on the data products in §4.

### Pitch-angle decay-rate inference for κ_par

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Pitch-angle decay-rate inference for κ_par as a callable on the data products in §4.

### Cross-field-spread inference for κ_perp

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-field-spread inference for κ_perp as a callable on the data products in §4.

### κ_perp / κ_par ratio extraction

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - κ_perp / κ_par ratio extraction as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/IS☉IS EPI-Hi + EPI-Lo | L2/L3 | instrument-native | Near-perihelion events (TODO_verify) | NASA CDAWeb / PSP SOC | abstract: load + decode + subset |
| PSP/FIELDS MAG | L2 | high cadence | Same intervals | PSP SOC | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: κ_par(E), κ_perp(E), and κ_perp/κ_par at near-Sun distances (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Single-spacecraft cross-field-spread inference is weak; report priors
- Anisotropy saturation in EPI-Lo at high intensity
- Local turbulence-spectrum estimate enters the diffusion derivation

## 7. Claim boundary  *(Layer 1)*

**In scope.** PSP IS☉IS events at ≤0.3 au (TODO_verify); event-based κ_par and κ_perp inferred from intensity / anisotropy / pitch-angle decay; near-Sun only.

**Out of scope — do NOT generalize beyond:**

- Do not extrapolate beyond the measured energy range or distance bin.
- Do not use as a turbulence-cascade test without an independent turbulence diagnostic.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2509.10648
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-laitinen-2026-vda-turbulent-heliosphere]]` — assumed for context (see linked skill).
- `[[paper-bian-2026-30march2022-sep-data-assimilation]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No paired Solar Orbiter EPD perpendicular-diffusion measurement at matched encounter times.
- **Hypothesis** — κ_perp / κ_par decreases monotonically with heliocentric distance closer than 0.3 au.
- **Minimal_experiment** — Apply the same diffusion fit on a Solar Orbiter HET event during a PSP–SOLO radial alignment.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
