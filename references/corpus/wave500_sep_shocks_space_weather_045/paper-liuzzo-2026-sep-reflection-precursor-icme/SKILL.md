---
name: paper-liuzzo-2026-sep-reflection-precursor-icme
description: >-
  Use when bi-directional electron beam or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Two impulsive SEE events show a primary anti-Sunward beam followed by a Sunward counter-streaming beam; modeled travel path 1–2 au is consistent with reflection off a precursor-ICME shock beyond 1 au; one event also shows inverse velocity d… (arXiv:2604.25019, 2026).
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
  title: "Solar Energetic Particle Reflection by Precursor ICMEs: Multi-spacecraft Observations of Bi-Directional Electron Beams at 1 AU"
  first_author: "Liuzzo, L."
  authors:
    - "Liuzzo, L."
    - "Wei, W."
    - "Poppe, A. R."
    - "Lee, C. O."
    - "Angelopoulos, V."
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2604.25019"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [THEMIS-ARTEMIS, Wind, STEREO-A]
  regime: [inner-heliosphere]

trigger_keywords:
  - "bi-directional electron beam"
  - "BDE"
  - "precursor ICME shock reflection"
  - "THEMIS-ARTEMIS"
  - "Wind 3DP"
  - "STEREO-A"
  - "IVD electrons"
  - "energetic-electron 1–600 keV"
  - "Sunward hazard"

data_products:
  - instrument: "THEMIS-ARTEMIS/SST+ESA"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event windows TODO_verify"
    archive: "NASA CDAWeb"
  - instrument: "Wind/3DP electron"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event windows"
    archive: "NASA CDAWeb"
  - instrument: "STEREO-A/SEPT+HET"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event windows"
    archive: "STEREO archive"
  - instrument: "Wind/MFI MAG"
    level: "L2"
    cadence: "high cadence"
    interval: "Event windows"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Anti-Sunward primary onset identification by PAD"
    equation_refs: []
    external_implementations: []
  - name: "Sunward counter-streaming beam delay-vs-energy fit (path length)"
    equation_refs: []
    external_implementations: []
  - name: "Inverse-velocity-dispersion (IVD) signature detection for electrons"
    equation_refs: []
    external_implementations: []
  - name: "Precursor-ICME identification (sheath/leading-edge MAG+plasma signatures)"
    equation_refs: []
    external_implementations: []
  - name: "1–2 au reflection-path consistency check"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.25019"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Case study of two impulsive SEE events (1–600 keV); observers THEMIS-ARTEMIS, Wind, STEREO-A (one event); precursor ICME identified beyond 1 au; bi-directional beam interpreted as reflection from precursor shock.
  out_of_scope:
    - "Do not extend ICME-reflection mechanism to ions without independent test."
    - "Do not use as a generic event-classification method without conjunction-observer support."

failure_modes:
  - "Counter-streaming beams from local magnetic-mirror points can mimic precursor reflection"
  - "Strahl contamination in low-energy 3DP channels"
  - "Path-length fit sensitive to choice of scattering-free transport baseline"
  - "Single-spacecraft IVD ambiguous without conjunction observers"

depends_on:
  - "paper-han-2026-sees-cross-hcs-statistical"
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No statistical survey of BDE-from-precursor-ICME events across solar-cycle 25."
    related_skills: []
  - type: "hypothesis"
    statement: "Precursor-ICME shock reflectivity for SEEs correlates with shock obliquity and Mach number."
    related_skills: ["paper-trotta-2025-ip-shock-variability-multi-spacecraft"]
  - type: "minimal_experiment"
    statement: "Survey ARTEMIS/Wind/STEREO conjunctions 2018–2025 for BDE+precursor-ICME pairs; tabulate reflection-path lengths."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2604.25019"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Solar Energetic Particle Reflection by Precursor ICMEs: Multi-spacecraft Observations of Bi-Directional Electron Beams at 1 AU — paper-skill

> Compiled from arXiv:2604.25019 (2026), Liuzzo, L. et al.
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

- bi-directional electron beam
- BDE
- precursor ICME shock reflection

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Two impulsive SEE events show a primary anti-Sunward beam followed by a Sunward counter-streaming beam; modeled travel path 1–2 au is consistent with reflection off a precursor-ICME shock beyond 1 au; one event also shows inverse velocity dispersion in electrons, the first such detection at 1 au.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Inferred counter-streaming path length 1–2 au; one event shows electron IVD signature (numeric energies TODO_verify); precursor ICME found beyond 1 au for both events. within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Anti-Sunward primary onset identification by PAD

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Anti-Sunward primary onset identification by PAD as a callable on the data products in §4.

### Sunward counter-streaming beam delay-vs-energy fit (path length)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Sunward counter-streaming beam delay-vs-energy fit (path length) as a callable on the data products in §4.

### Inverse-velocity-dispersion (IVD) signature detection for electrons

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Inverse-velocity-dispersion (IVD) signature detection for electrons as a callable on the data products in §4.

### Precursor-ICME identification (sheath/leading-edge MAG+plasma signatures)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Precursor-ICME identification (sheath/leading-edge MAG+plasma signatures) as a callable on the data products in §4.

### 1–2 au reflection-path consistency check

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - 1–2 au reflection-path consistency check as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| THEMIS-ARTEMIS/SST+ESA | L2 | instrument-native | Event windows TODO_verify | NASA CDAWeb | abstract: load + decode + subset |
| Wind/3DP electron | L2 | instrument-native | Event windows | NASA CDAWeb | abstract: load + decode + subset |
| STEREO-A/SEPT+HET | L2 | instrument-native | Event windows | STEREO archive | abstract: load + decode + subset |
| Wind/MFI MAG | L2 | high cadence | Event windows | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Inferred counter-streaming path length 1–2 au; one event shows electron IVD signature (numeric energies TODO_verify); precursor ICME found beyond 1 au for both events.

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Counter-streaming beams from local magnetic-mirror points can mimic precursor reflection
- Strahl contamination in low-energy 3DP channels
- Path-length fit sensitive to choice of scattering-free transport baseline
- Single-spacecraft IVD ambiguous without conjunction observers

## 7. Claim boundary  *(Layer 1)*

**In scope.** Case study of two impulsive SEE events (1–600 keV); observers THEMIS-ARTEMIS, Wind, STEREO-A (one event); precursor ICME identified beyond 1 au; bi-directional beam interpreted as reflection from precursor shock.

**Out of scope — do NOT generalize beyond:**

- Do not extend ICME-reflection mechanism to ions without independent test.
- Do not use as a generic event-classification method without conjunction-observer support.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2604.25019
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-han-2026-sees-cross-hcs-statistical]]` — assumed for context (see linked skill).
- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No statistical survey of BDE-from-precursor-ICME events across solar-cycle 25.
- **Hypothesis** — Precursor-ICME shock reflectivity for SEEs correlates with shock obliquity and Mach number. Related: `[[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]`.
- **Minimal_experiment** — Survey ARTEMIS/Wind/STEREO conjunctions 2018–2025 for BDE+precursor-ICME pairs; tabulate reflection-path lengths.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
