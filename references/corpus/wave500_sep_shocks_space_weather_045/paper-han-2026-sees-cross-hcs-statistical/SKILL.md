---
name: paper-han-2026-sees-cross-hcs-statistical
description: >-
  Use when solar energetic electrons or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Opposite-side SEE events (source and observer in different magnetic sectors) are rarer and more isotropic; both source and spacecraft tend to lie closer to the HCS than for same-side events — particle transport across the HCS is inefficient… (arXiv:2604.19446, 2026).
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
  title: "Do Solar Energetic Electrons cross the Heliospheric Current Sheet? — A Statistical Study"
  first_author: "Han, C."
  authors:
    - "Han, C."
    - "Wimmer-Schweingruber, R. F."
    - "Kuhl, P."
    - "Berger, L."
    - "Ding, Z."
    - "Kollhoff, A."
    - "Shi, Q."
    - "Xu, Z."
    - "Qin, M."
    - "Wang, M."
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2604.19446"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Solar Orbiter, STEREO, Wind]
  regime: [inner-heliosphere]

trigger_keywords:
  - "solar energetic electrons"
  - "HCS crossing"
  - "same-side opposite-side"
  - "strahl pitch angle"
  - "first-order anisotropy"
  - "PFSS footpoint polarity"
  - "60 same-side 9 opposite-side"
  - "magnetic sector"

data_products:
  - instrument: "Solar Orbiter/EPD (STEP/EPT)"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event windows TODO_verify"
    archive: "ESA SOAR"
  - instrument: "Wind/3DP electron"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "Event windows"
    archive: "NASA CDAWeb"
  - instrument: "PFSS magnetogram"
    level: "synoptic"
    cadence: "27-day"
    interval: "Event windows"
    archive: "GONG / WSA archive"

algorithms:
  - name: "PFSS-based footpoint polarity assignment"
    equation_refs: []
    external_implementations: []
  - name: "Strahl PA-based local sector identification"
    equation_refs: []
    external_implementations: []
  - name: "First-order anisotropy classifier for crossing events"
    equation_refs: []
    external_implementations: []
  - name: "Same-side / opposite-side binary classification"
    equation_refs: []
    external_implementations: []
  - name: "HCS-distance correlation analysis"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.19446"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Statistical classification of solar energetic electron events into same-side vs opposite-side; polarity determined by combined PFSS footpoint + in-situ MAG sector + strahl PA + energetic-electron anisotropy; 60 same-side and 9 opposite-side events.
  out_of_scope:
    - "Do not generalize to protons — anisotropy/transport regimes differ."
    - "Do not infer cross-HCS diffusion coefficients without a transport model."
    - "Do not use the sector classifier inside ICME sheaths or magnetic clouds."

failure_modes:
  - "Strahl identification fails inside ICMEs/sheath — flag and remove"
  - "PFSS source-surface choice modulates footpoint polarity at the few-percent level"
  - "Statistics on opposite-side events are small (N=9)"
  - "Energetic-electron anisotropy can saturate at high intensity"

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No matched-pair proton/electron HCS-crossing statistical study at the same event set."
    related_skills: []
  - type: "tension"
    statement: "Cross-HCS diffusion inferred from electrons may disagree with proton-based cross-field diffusion coefficients."
    related_skills: ["paper-malandraki-2025-perp-diffusion-near-sun"]
  - type: "minimal_experiment"
    statement: "Re-run the same classifier on PSP/IS☉IS electrons for E22–E24 and compare same-side / opposite-side fractions."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2604.19446"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Do Solar Energetic Electrons cross the Heliospheric Current Sheet? — A Statistical Study — paper-skill

> Compiled from arXiv:2604.19446 (2026), Han, C. et al.
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

- solar energetic electrons
- HCS crossing
- same-side opposite-side

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Opposite-side SEE events (source and observer in different magnetic sectors) are rarer and more isotropic; both source and spacecraft tend to lie closer to the HCS than for same-side events — particle transport across the HCS is inefficient unless source or observer sits near the HCS.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Counts of same-side (60) vs opposite-side (9) events; opposite-side anisotropy distribution shifted toward isotropic; HCS distance distributions for both classes (TODO_verify numeric thresholds from full text). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### PFSS-based footpoint polarity assignment

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - PFSS-based footpoint polarity assignment as a callable on the data products in §4.

### Strahl PA-based local sector identification

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Strahl PA-based local sector identification as a callable on the data products in §4.

### First-order anisotropy classifier for crossing events

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - First-order anisotropy classifier for crossing events as a callable on the data products in §4.

### Same-side / opposite-side binary classification

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Same-side / opposite-side binary classification as a callable on the data products in §4.

### HCS-distance correlation analysis

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - HCS-distance correlation analysis as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Solar Orbiter/EPD (STEP/EPT) | L2 | instrument-native | Event windows TODO_verify | ESA SOAR | abstract: load + decode + subset |
| Wind/3DP electron | L2/L3 | instrument-native | Event windows | NASA CDAWeb | abstract: load + decode + subset |
| PFSS magnetogram | synoptic | 27-day | Event windows | GONG / WSA archive | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Counts of same-side (60) vs opposite-side (9) events; opposite-side anisotropy distribution shifted toward isotropic; HCS distance distributions for both classes (TODO_verify numeric thresholds from full text).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Strahl identification fails inside ICMEs/sheath — flag and remove
- PFSS source-surface choice modulates footpoint polarity at the few-percent level
- Statistics on opposite-side events are small (N=9)
- Energetic-electron anisotropy can saturate at high intensity

## 7. Claim boundary  *(Layer 1)*

**In scope.** Statistical classification of solar energetic electron events into same-side vs opposite-side; polarity determined by combined PFSS footpoint + in-situ MAG sector + strahl PA + energetic-electron anisotropy; 60 same-side and 9 opposite-side events.

**Out of scope — do NOT generalize beyond:**

- Do not generalize to protons — anisotropy/transport regimes differ.
- Do not infer cross-HCS diffusion coefficients without a transport model.
- Do not use the sector classifier inside ICME sheaths or magnetic clouds.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2604.19446
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).
- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No matched-pair proton/electron HCS-crossing statistical study at the same event set.
- **Tension** — Cross-HCS diffusion inferred from electrons may disagree with proton-based cross-field diffusion coefficients. Related: `[[paper-malandraki-2025-perp-diffusion-near-sun]]`.
- **Minimal_experiment** — Re-run the same classifier on PSP/IS☉IS electrons for E22–E24 and compare same-side / opposite-side fractions.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
