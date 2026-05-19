---
name: paper-kollhoff-2026-acr-helium-solo-het
description: >-
  Use when anomalous cosmic ray helium or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Solar Orbiter/HET measures ACR helium spectra inside 1 au, constraining inner-heliosphere modulation against the historic IBEX/Voyager picture. (arXiv:2602.22418, 2026).
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
  title: "Anomalous cosmic rays within the inner heliosphere: Observations of helium by the High Energy Telescope onboard Solar Orbiter"
  first_author: "Kollhoff, A. (TODO verify)"
  authors:
    - "TODO verify"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2602.22418"
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
  - "anomalous cosmic ray helium"
  - "Solar Orbiter HET"
  - "ACR inner heliosphere"
  - "solar modulation"
  - "termination shock origin"
  - "energy spectrum"

data_products:
  - instrument: "Solar Orbiter/EPD HET He channel"
    level: "L2"
    cadence: "instrument-native"
    interval: "quiet-time intervals 2020–2025 (TODO_verify)"
    archive: "ESA SOAR"

algorithms:
  - name: "Quiet-time selection (excluding SEP/CIR/ICME enhancements)"
    equation_refs: []
    external_implementations: []
  - name: "ACR He energy spectrum fit"
    equation_refs: []
    external_implementations: []
  - name: "Distance binning and modulation-trend extraction"
    equation_refs: []
    external_implementations: []
  - name: "Cross-check against Voyager / IBEX boundary conditions"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.22418"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Solar Orbiter HET ACR He spectrum within ~0.3–1 au; quiet-time intervals (TODO_verify); spectrum and intensity vs heliocentric distance only.
  out_of_scope:
    - "Do not generalize to other ACR species without separate analysis."
    - "Do not infer termination-shock conditions directly from inner-heliosphere data alone."

failure_modes:
  - "Contamination by residual SEP/CIR He at low energies"
  - "HET background calibration uncertainty"
  - "Quiet-time definition affects spectral slope"

depends_on:
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No co-temporal PSP/IS☉IS ACR-He measurement with matched quiet-time selection."
    related_skills: []
  - type: "hypothesis"
    statement: "Inner-heliosphere ACR-He modulation tracks solar-cycle activity index with a measurable lag."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Compute the same ACR-He spectrum on PSP/IS☉IS quiet-time intervals at matched heliocentric distance."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2602.22418"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Anomalous cosmic rays within the inner heliosphere: Observations of helium by the High Energy Telescope onboard Solar Orbiter — paper-skill

> Compiled from arXiv:2602.22418 (2026), Kollhoff, A. (TODO verify) et al.
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

- anomalous cosmic ray helium
- Solar Orbiter HET
- ACR inner heliosphere

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Solar Orbiter/HET measures ACR helium spectra inside 1 au, constraining inner-heliosphere modulation against the historic IBEX/Voyager picture.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces ACR He spectrum measured at Solar Orbiter; modulation trend with heliocentric distance (numerical values TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Quiet-time selection (excluding SEP/CIR/ICME enhancements)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Quiet-time selection (excluding SEP/CIR/ICME enhancements) as a callable on the data products in §4.

### ACR He energy spectrum fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - ACR He energy spectrum fit as a callable on the data products in §4.

### Distance binning and modulation-trend extraction

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Distance binning and modulation-trend extraction as a callable on the data products in §4.

### Cross-check against Voyager / IBEX boundary conditions

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-check against Voyager / IBEX boundary conditions as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Solar Orbiter/EPD HET He channel | L2 | instrument-native | quiet-time intervals 2020–2025 (TODO_verify) | ESA SOAR | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: ACR He spectrum measured at Solar Orbiter; modulation trend with heliocentric distance (numerical values TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Contamination by residual SEP/CIR He at low energies
- HET background calibration uncertainty
- Quiet-time definition affects spectral slope

## 7. Claim boundary  *(Layer 1)*

**In scope.** Solar Orbiter HET ACR He spectrum within ~0.3–1 au; quiet-time intervals (TODO_verify); spectrum and intensity vs heliocentric distance only.

**Out of scope — do NOT generalize beyond:**

- Do not generalize to other ACR species without separate analysis.
- Do not infer termination-shock conditions directly from inner-heliosphere data alone.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2602.22418
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No co-temporal PSP/IS☉IS ACR-He measurement with matched quiet-time selection.
- **Hypothesis** — Inner-heliosphere ACR-He modulation tracks solar-cycle activity index with a measurable lag.
- **Minimal_experiment** — Compute the same ACR-He spectrum on PSP/IS☉IS quiet-time intervals at matched heliocentric distance.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
