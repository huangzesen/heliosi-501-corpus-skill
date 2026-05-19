---
name: paper-duan-2026-sep-type-ii-radio-source-regions
description: >-
  Use when halo cme or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Of 43 SEP halo-CMEs vs 131 non-SEP halo-CMEs 2010–2024, almost all SEP and ~2/3 non-SEP events have type II bursts; SEP-associated type IIs have longer duration and lower ending frequency; starting frequency depends on source region (single… (arXiv:2604.20237, 2026).
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
  title: "Solar Energetic Particle Events and Associated Type II Radio Bursts from Different Source Regions"
  first_author: "Duan, X."
  authors:
    - "Duan, X."
    - "Li, T."
    - "Cui, Y."
    - "Hou, Y."
    - "Li, C."
    - "Wijsen, N."
    - "Jiang, Z."
    - "Yan, Y."
    - "Ma, S."
    - "Sun, Z."
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2604.20237"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [GOES, SOHO/LASCO, ground-based radio (TODO_verify, e.g. Wind/WAVES, e-CALLISTO)]
  regime: [inner-heliosphere]

trigger_keywords:
  - "halo CME"
  - "type II radio burst"
  - "starting frequency"
  - "single AR multi AR outside AR"
  - "Fe O abundance"
  - "proton electron spectral index"
  - "SEP vs non-SEP halo"
  - "43 SEP 131 non-SEP"
  - "2010–2024"

data_products:
  - instrument: "Wind/WAVES type II"
    level: "L2"
    cadence: "event"
    interval: "2010–2024"
    archive: "NASA CDAWeb"
  - instrument: "GOES SEM/EPS proton intensity"
    level: "L2"
    cadence: "5-min"
    interval: "2010–2024"
    archive: "NOAA SWPC"
  - instrument: "SOHO/LASCO halo CME catalog"
    level: "L3"
    cadence: "event"
    interval: "2010–2024"
    archive: "CDAW catalog"
  - instrument: "SDO/AIA + HMI source-region context"
    level: "L1.5"
    cadence: "event"
    interval: "2010–2024"
    archive: "JSOC"

algorithms:
  - name: "Halo-CME / type II joint catalog assembly"
    equation_refs: []
    external_implementations: []
  - name: "Source-region classifier (single AR / multi AR / outside AR)"
    equation_refs: []
    external_implementations: []
  - name: "Proton & electron spectral-index fit per event"
    equation_refs: []
    external_implementations: []
  - name: "Type II start/end frequency and duration measurement"
    equation_refs: []
    external_implementations: []
  - name: "Anti-correlation test: proton index vs type II starting frequency"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.20237"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Halo-CME statistical sample 2010–2024; type II properties (start/end frequency, duration); SEP proton/electron spectral indices; source-region taxonomy (single AR / multi AR / outside AR).
  out_of_scope:
    - "Do not interpret 'outside AR' events as a single physical class."
    - "Do not use these statistics to predict event-specific energy spectra."
    - "Do not generalize to non-halo or limb CMEs from this sample alone."

failure_modes:
  - "Halo selection bias toward strong / Earth-directed events"
  - "Type II identification at low frequencies is sensitive to background-cleaning"
  - "Outside-AR classification subjective; specify magnetogram thresholds"
  - "Particle-flux ground-truth differs by mission (GOES vs SEPMOD vs IS☉IS) for cross-mission comparison"

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-jebaraj-2024-type-ii-multi-vantage-catalog"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No multi-vantage-point version of this statistic combining ground radio + Wind/WAVES + STEREO/WAVES + PSP/FIELDS."
    related_skills: ["paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks"]
  - type: "hypothesis"
    statement: "The type II starting-frequency / proton-index anti-correlation is mediated by ambient density and shock-formation height."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Add Solar Orbiter and PSP-conjunction events (2020–2025) to test whether source-region taxonomy generalizes off the Sun–Earth line."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2604.20237"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Solar Energetic Particle Events and Associated Type II Radio Bursts from Different Source Regions — paper-skill

> Compiled from arXiv:2604.20237 (2026), Duan, X. et al.
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

- halo CME
- type II radio burst
- starting frequency

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Of 43 SEP halo-CMEs vs 131 non-SEP halo-CMEs 2010–2024, almost all SEP and ~2/3 non-SEP events have type II bursts; SEP-associated type IIs have longer duration and lower ending frequency; starting frequency depends on source region (single AR > multi AR > outside AR); proton spectral index anti-correlates with type II starting frequency.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces 43 SEP + 131 non-SEP event counts; near-100% SEP / ~67% non-SEP type II association rates; AR-class starting-frequency ordering; proton-index ↔ type II starting frequency anti-correlation sign. within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Halo-CME / type II joint catalog assembly

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Halo-CME / type II joint catalog assembly as a callable on the data products in §4.

### Source-region classifier (single AR / multi AR / outside AR)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Source-region classifier (single AR / multi AR / outside AR) as a callable on the data products in §4.

### Proton & electron spectral-index fit per event

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Proton & electron spectral-index fit per event as a callable on the data products in §4.

### Type II start/end frequency and duration measurement

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Type II start/end frequency and duration measurement as a callable on the data products in §4.

### Anti-correlation test: proton index vs type II starting frequency

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Anti-correlation test: proton index vs type II starting frequency as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Wind/WAVES type II | L2 | event | 2010–2024 | NASA CDAWeb | abstract: load + decode + subset |
| GOES SEM/EPS proton intensity | L2 | 5-min | 2010–2024 | NOAA SWPC | abstract: load + decode + subset |
| SOHO/LASCO halo CME catalog | L3 | event | 2010–2024 | CDAW catalog | abstract: load + decode + subset |
| SDO/AIA + HMI source-region context | L1.5 | event | 2010–2024 | JSOC | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: 43 SEP + 131 non-SEP event counts; near-100% SEP / ~67% non-SEP type II association rates; AR-class starting-frequency ordering; proton-index ↔ type II starting frequency anti-correlation sign.

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Halo selection bias toward strong / Earth-directed events
- Type II identification at low frequencies is sensitive to background-cleaning
- Outside-AR classification subjective; specify magnetogram thresholds
- Particle-flux ground-truth differs by mission (GOES vs SEPMOD vs IS☉IS) for cross-mission comparison

## 7. Claim boundary  *(Layer 1)*

**In scope.** Halo-CME statistical sample 2010–2024; type II properties (start/end frequency, duration); SEP proton/electron spectral indices; source-region taxonomy (single AR / multi AR / outside AR).

**Out of scope — do NOT generalize beyond:**

- Do not interpret 'outside AR' events as a single physical class.
- Do not use these statistics to predict event-specific energy spectra.
- Do not generalize to non-halo or limb CMEs from this sample alone.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2604.20237
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).
- `[[paper-jebaraj-2024-type-ii-multi-vantage-catalog]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No multi-vantage-point version of this statistic combining ground radio + Wind/WAVES + STEREO/WAVES + PSP/FIELDS. Related: `[[paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks]]`.
- **Hypothesis** — The type II starting-frequency / proton-index anti-correlation is mediated by ambient density and shock-formation height.
- **Minimal_experiment** — Add Solar Orbiter and PSP-conjunction events (2020–2025) to test whether source-region taxonomy generalizes off the Sun–Earth line.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
