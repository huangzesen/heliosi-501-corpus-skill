---
name: paper-bian-2026-30march2022-sep-data-assimilation
description: >-
  Use when sep 30 march 2022 or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Data-assimilation of multi-spacecraft SEP intensities for 2022-03-30 yields posterior constraints on parallel + perpendicular diffusion coefficients of the event's transport model. (arXiv:2602.00765, 2026).
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
  title: "A study of solar energetic particle transport on 30 March 2022 using multi-spacecraft data assimilation"
  first_author: "Bian, N. (TODO verify)"
  authors:
    - "TODO verify"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2602.00765"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP, Solar Orbiter, ACE, Wind, STEREO-A]
  regime: [inner-heliosphere]

trigger_keywords:
  - "SEP 30 March 2022"
  - "data assimilation"
  - "multi-spacecraft"
  - "parallel mean free path"
  - "perpendicular diffusion"
  - "Parker transport equation"
  - "Bayesian inversion"

data_products:
  - instrument: "PSP/IS☉IS EPI-Hi+EPI-Lo"
    level: "L2"
    cadence: "instrument-native"
    interval: "2022-03-30 ± 2 d"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "Solar Orbiter EPD (HET/EPT/SIS/STEP)"
    level: "L2"
    cadence: "instrument-native"
    interval: "2022-03-30 ± 2 d"
    archive: "ESA SOAR"
  - instrument: "ACE/EPAM + Wind/3DP + STEREO-A HET/SEPT"
    level: "L2"
    cadence: "instrument-native"
    interval: "2022-03-30 ± 2 d"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Multi-spacecraft intensity time-series alignment"
    equation_refs: []
    external_implementations: []
  - name: "Forward transport solver (parallel + perpendicular diffusion)"
    equation_refs: []
    external_implementations: []
  - name: "Bayesian data assimilation / parameter posterior"
    equation_refs: []
    external_implementations: []
  - name: "Pulse-of-injection vs continuous-injection comparison"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.00765"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event 2022-03-30; observers (PSP, Solar Orbiter, ACE/Wind/STEREO-A — TODO_verify); Parker-transport solver with diffusion-coefficient parameter posterior.
  out_of_scope:
    - "Do not generalize the posterior coefficients to other events without re-fitting."
    - "Do not use the assimilation framework for non-impulsive (gradual-only) events without separate validation."

failure_modes:
  - "Source-injection function is a strong prior assumption"
  - "Cross-spacecraft inter-calibration introduces systematic bias"
  - "Posterior identifiability between κ_perp and κ_par may be weak"
  - "Magnetic connectivity uncertainty propagates into posterior"

depends_on:
  - "paper-laitinen-2026-vda-turbulent-heliosphere"
  - "paper-malandraki-2025-perp-diffusion-near-sun"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No standardized data-assimilation benchmark suite for SEP transport across the SEP IVA / widespread event catalog."
    related_skills: []
  - type: "hypothesis"
    statement: "κ_perp/κ_par increases with heliocentric distance for events crossing the HCS."
    related_skills: ["paper-han-2026-sees-cross-hcs-statistical"]
  - type: "minimal_experiment"
    statement: "Apply the same inversion to the 2022-09-05 Labor Day event; compare posterior diffusion coefficients."
    related_skills: ["paper-xu-2026-psp-iva-sep-events"]

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2602.00765"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# A study of solar energetic particle transport on 30 March 2022 using multi-spacecraft data assimilation — paper-skill

> Compiled from arXiv:2602.00765 (2026), Bian, N. (TODO verify) et al.
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

- SEP 30 March 2022
- data assimilation
- multi-spacecraft

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Data-assimilation of multi-spacecraft SEP intensities for 2022-03-30 yields posterior constraints on parallel + perpendicular diffusion coefficients of the event's transport model.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Posterior on κ_par / κ_perp for the event; per-observer fitted intensity time series within tolerance (TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Multi-spacecraft intensity time-series alignment

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Multi-spacecraft intensity time-series alignment as a callable on the data products in §4.

### Forward transport solver (parallel + perpendicular diffusion)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Forward transport solver (parallel + perpendicular diffusion) as a callable on the data products in §4.

### Bayesian data assimilation / parameter posterior

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Bayesian data assimilation / parameter posterior as a callable on the data products in §4.

### Pulse-of-injection vs continuous-injection comparison

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Pulse-of-injection vs continuous-injection comparison as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/IS☉IS EPI-Hi+EPI-Lo | L2 | instrument-native | 2022-03-30 ± 2 d | NASA CDAWeb / PSP SOC | abstract: load + decode + subset |
| Solar Orbiter EPD (HET/EPT/SIS/STEP) | L2 | instrument-native | 2022-03-30 ± 2 d | ESA SOAR | abstract: load + decode + subset |
| ACE/EPAM + Wind/3DP + STEREO-A HET/SEPT | L2 | instrument-native | 2022-03-30 ± 2 d | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Posterior on κ_par / κ_perp for the event; per-observer fitted intensity time series within tolerance (TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Source-injection function is a strong prior assumption
- Cross-spacecraft inter-calibration introduces systematic bias
- Posterior identifiability between κ_perp and κ_par may be weak
- Magnetic connectivity uncertainty propagates into posterior

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event 2022-03-30; observers (PSP, Solar Orbiter, ACE/Wind/STEREO-A — TODO_verify); Parker-transport solver with diffusion-coefficient parameter posterior.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the posterior coefficients to other events without re-fitting.
- Do not use the assimilation framework for non-impulsive (gradual-only) events without separate validation.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2602.00765
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-laitinen-2026-vda-turbulent-heliosphere]]` — assumed for context (see linked skill).
- `[[paper-malandraki-2025-perp-diffusion-near-sun]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No standardized data-assimilation benchmark suite for SEP transport across the SEP IVA / widespread event catalog.
- **Hypothesis** — κ_perp/κ_par increases with heliocentric distance for events crossing the HCS. Related: `[[paper-han-2026-sees-cross-hcs-statistical]]`.
- **Minimal_experiment** — Apply the same inversion to the 2022-09-05 Labor Day event; compare posterior diffusion coefficients. Related: `[[paper-xu-2026-psp-iva-sep-events]]`.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
