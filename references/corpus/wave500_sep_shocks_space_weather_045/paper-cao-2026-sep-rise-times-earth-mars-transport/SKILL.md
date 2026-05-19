---
name: paper-cao-2026-sep-rise-times-earth-mars-transport
description: >-
  Use when sep rise time or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Statistical relationship between SEP rise time at different energies follows a power-law in energy; flatter exponent at Mars implies weaker energy dependence and turbulence-scattering approaching a rigidity-independent regime farther from t… (arXiv:2605.01437, 2026).
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
  title: "Statistical analysis of solar energetic particle rise times using Earth and Mars observations and constraints on particle transport parameters"
  first_author: "Cao, Y."
  authors:
    - "Cao, Y."
    - "Guo, J."
    - "Wang, Y."
    - "Zou, Z."
    - "Zhang, Y."
    - "Li, C."
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2605.01437"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [SOHO, Tianwen-1]
  regime: [inner-heliosphere]

trigger_keywords:
  - "SEP rise time"
  - "Tianwen-1 MEPA"
  - "SOHO ERNE"
  - "parallel mean free path"
  - "rigidity dependence"
  - "diffusion at Mars"
  - "turbulence scattering"
  - "75 events Earth"
  - "58 events Mars"
  - "Nov 2020 to Mar 2025"

data_products:
  - instrument: "SOHO/ERNE"
    level: "L2"
    cadence: "instrument-native"
    interval: "Nov 2020–Mar 2025"
    archive: "ESA / NASA archives"
  - instrument: "Tianwen-1/MEPA"
    level: "L2"
    cadence: "instrument-native"
    interval: "Nov 2020–Mar 2025"
    archive: "Tianwen mission archive (TODO_verify)"

algorithms:
  - name: "Onset-time linear fit (per energy channel)"
    equation_refs: []
    external_implementations: []
  - name: "Peak-time sliding median + Savitzky–Golay smoothing"
    equation_refs: []
    external_implementations: []
  - name: "Rise-time = peak − onset extraction"
    equation_refs: []
    external_implementations: []
  - name: "Power-law fit of rise time vs energy"
    equation_refs: []
    external_implementations: []
  - name: "Rigidity-dependence inversion under parallel-diffusion model"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2605.01437"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    SOHO/ERNE at 1 au and Tianwen-1/MEPA near Mars; Nov 2020–Mar 2025; 75 SEP events at 1 au, 58 near Mars; onset by linear fit, peak by sliding median + Savitzky–Golay; only the rise-time/energy power-law and parallel-diffusion rigidity dependence are claimed.
  out_of_scope:
    - "Do not generalize the Mars rigidity-independence to outer heliosphere distances."
    - "Do not interpret event-averaged rise-time as a per-event acceleration timescale."
    - "Do not use without solar-wind / turbulence context for each event."

failure_modes:
  - "Event-selection ambiguity blurs the rise-time power-law slope; report selection criteria"
  - "Pure-diffusion baseline neglects shock/acceleration evolution"
  - "MEPA cadence and energy-channel calibration are mission-specific"
  - "Cross-mission energy-channel matching needed to compare exponents"

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-laitinen-2026-vda-turbulent-heliosphere"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No SEP rise-time atlas combines PSP near-Sun, 1 au, and Mars at the same energy bins."
    related_skills: ["paper-walker-2026-icme-radial-particle-acceleration-statistics"]
  - type: "hypothesis"
    statement: "If rise-time exponent monotonically flattens with heliocentric distance, the parallel mean-free-path is set by an outer-scale-driven turbulence cascade."
    related_skills: ["paper-laitinen-2026-vda-turbulent-heliosphere"]
  - type: "minimal_experiment"
    statement: "Refit rise-time vs energy on PSP/IS☉IS for the same 2020–2025 events; compare exponent against the Cao+ 2026 Earth/Mars baseline."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2605.01437"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Statistical analysis of solar energetic particle rise times using Earth and Mars observations and constraints on particle transport parameters — paper-skill

> Compiled from arXiv:2605.01437 (2026), Cao, Y. et al.
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

- SEP rise time
- Tianwen-1 MEPA
- SOHO ERNE

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Statistical relationship between SEP rise time at different energies follows a power-law in energy; flatter exponent at Mars implies weaker energy dependence and turbulence-scattering approaching a rigidity-independent regime farther from the Sun.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Power-law exponent of rise time vs energy at Earth and Mars; flatter exponent at Mars; rigidity-independence trend at Mars (signs/order of magnitude per abstract; numeric TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Onset-time linear fit (per energy channel)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Onset-time linear fit (per energy channel) as a callable on the data products in §4.

### Peak-time sliding median + Savitzky–Golay smoothing

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Peak-time sliding median + Savitzky–Golay smoothing as a callable on the data products in §4.

### Rise-time = peak − onset extraction

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Rise-time = peak − onset extraction as a callable on the data products in §4.

### Power-law fit of rise time vs energy

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Power-law fit of rise time vs energy as a callable on the data products in §4.

### Rigidity-dependence inversion under parallel-diffusion model

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Rigidity-dependence inversion under parallel-diffusion model as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| SOHO/ERNE | L2 | instrument-native | Nov 2020–Mar 2025 | ESA / NASA archives | abstract: load + decode + subset |
| Tianwen-1/MEPA | L2 | instrument-native | Nov 2020–Mar 2025 | Tianwen mission archive (TODO_verify) | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Power-law exponent of rise time vs energy at Earth and Mars; flatter exponent at Mars; rigidity-independence trend at Mars (signs/order of magnitude per abstract; numeric TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Event-selection ambiguity blurs the rise-time power-law slope; report selection criteria
- Pure-diffusion baseline neglects shock/acceleration evolution
- MEPA cadence and energy-channel calibration are mission-specific
- Cross-mission energy-channel matching needed to compare exponents

## 7. Claim boundary  *(Layer 1)*

**In scope.** SOHO/ERNE at 1 au and Tianwen-1/MEPA near Mars; Nov 2020–Mar 2025; 75 SEP events at 1 au, 58 near Mars; onset by linear fit, peak by sliding median + Savitzky–Golay; only the rise-time/energy power-law and parallel-diffusion rigidity dependence are claimed.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the Mars rigidity-independence to outer heliosphere distances.
- Do not interpret event-averaged rise-time as a per-event acceleration timescale.
- Do not use without solar-wind / turbulence context for each event.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2605.01437
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-reames-2026-physics-of-seps]]` — assumed for context (see linked skill).
- `[[paper-laitinen-2026-vda-turbulent-heliosphere]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No SEP rise-time atlas combines PSP near-Sun, 1 au, and Mars at the same energy bins. Related: `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]`.
- **Hypothesis** — If rise-time exponent monotonically flattens with heliocentric distance, the parallel mean-free-path is set by an outer-scale-driven turbulence cascade. Related: `[[paper-laitinen-2026-vda-turbulent-heliosphere]]`.
- **Minimal_experiment** — Refit rise-time vs energy on PSP/IS☉IS for the same 2020–2025 events; compare exponent against the Cao+ 2026 Earth/Mars baseline.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
