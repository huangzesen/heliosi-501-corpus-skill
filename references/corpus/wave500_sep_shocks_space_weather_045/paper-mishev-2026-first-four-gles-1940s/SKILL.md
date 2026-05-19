---
name: paper-mishev-2026-first-four-gles-1940s
description: >-
  Use when gle 1942 or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Digitisation and re-analysis of the first four GLEs in the 1940s yields revised GLE intensities and provides forgotten constraints on extreme-event spectra. (arXiv:2602.24250, 2026).
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
  title: "The First Four Ground-Level Enhancements in the 1940s: Investigation, Digitisation, and Analysis of Forgotten Data"
  first_author: "Mishev, A. (TODO verify)"
  authors:
    - "TODO verify author list"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2602.24250"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Historical ground-based ionization / muon archive]
  regime: [inner-heliosphere]

trigger_keywords:
  - "GLE 1942"
  - "GLE 1946"
  - "ionization chamber"
  - "muon detector"
  - "digitisation archival data"
  - "GLE spectral fit"
  - "GLE catalog"

data_products:
  - instrument: "Historical ionization-chamber records"
    level: "archival"
    cadence: "hourly"
    interval: "1942–1946"
    archive: "national archives (TODO_verify)"

algorithms:
  - name: "Archival data digitisation pipeline"
    equation_refs: []
    external_implementations: []
  - name: "Detector-response unfolding to count rate"
    equation_refs: []
    external_implementations: []
  - name: "GLE spectral-index fit under standard cutoff-rigidity framework"
    equation_refs: []
    external_implementations: []
  - name: "Cross-station consistency check"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.24250"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Four GLEs (1942-Feb-28, 1942-Mar-07, 1946-Jul-25, 1946-Nov-19 — TODO_verify); pre-NM-era ionization chambers / muon detectors; archival digitisation; spectral / intensity reconstruction only.
  out_of_scope:
    - "Do not compare directly with NM-era GLEs without rigidity-response calibration."
    - "Do not infer geomagnetic conditions purely from GLE counts."

failure_modes:
  - "Pre-NM detectors have poorly characterized rigidity response"
  - "Time-resolution coarser than modern NMs — peak intensity underestimated"
  - "Geomagnetic cutoff time variation across the 1940s"
  - "Archival metadata quality is mixed"

depends_on:
  - "paper-mekhaldi-2026-carrington-36cl-ice-cores"
  - "paper-dalla-2026-radiation-doses-extreme-seps"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "Modern GLE catalogs typically start at GLE5 (1956); these earlier events remain under-used in extreme-event statistics."
    related_skills: []
  - type: "hypothesis"
    statement: "Including the four 1940s GLEs shifts the GLE fluence distribution tail by an order-unity factor."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Refit Mishev+ digitised time series with a modern unfolding code and compare with NM-era GLE spectra."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2602.24250"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# The First Four Ground-Level Enhancements in the 1940s: Investigation, Digitisation, and Analysis of Forgotten Data — paper-skill

> Compiled from arXiv:2602.24250 (2026), Mishev, A. (TODO verify) et al.
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

- GLE 1942
- GLE 1946
- ionization chamber

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Digitisation and re-analysis of the first four GLEs in the 1940s yields revised GLE intensities and provides forgotten constraints on extreme-event spectra.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Digitised time series for each of four GLEs; spectral indices and peak intensities (TODO_verify numbers). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Archival data digitisation pipeline

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Archival data digitisation pipeline as a callable on the data products in §4.

### Detector-response unfolding to count rate

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Detector-response unfolding to count rate as a callable on the data products in §4.

### GLE spectral-index fit under standard cutoff-rigidity framework

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - GLE spectral-index fit under standard cutoff-rigidity framework as a callable on the data products in §4.

### Cross-station consistency check

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Cross-station consistency check as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| Historical ionization-chamber records | archival | hourly | 1942–1946 | national archives (TODO_verify) | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Digitised time series for each of four GLEs; spectral indices and peak intensities (TODO_verify numbers).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Pre-NM detectors have poorly characterized rigidity response
- Time-resolution coarser than modern NMs — peak intensity underestimated
- Geomagnetic cutoff time variation across the 1940s
- Archival metadata quality is mixed

## 7. Claim boundary  *(Layer 1)*

**In scope.** Four GLEs (1942-Feb-28, 1942-Mar-07, 1946-Jul-25, 1946-Nov-19 — TODO_verify); pre-NM-era ionization chambers / muon detectors; archival digitisation; spectral / intensity reconstruction only.

**Out of scope — do NOT generalize beyond:**

- Do not compare directly with NM-era GLEs without rigidity-response calibration.
- Do not infer geomagnetic conditions purely from GLE counts.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2602.24250
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-mekhaldi-2026-carrington-36cl-ice-cores]]` — assumed for context (see linked skill).
- `[[paper-dalla-2026-radiation-doses-extreme-seps]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — Modern GLE catalogs typically start at GLE5 (1956); these earlier events remain under-used in extreme-event statistics.
- **Hypothesis** — Including the four 1940s GLEs shifts the GLE fluence distribution tail by an order-unity factor.
- **Minimal_experiment** — Refit Mishev+ digitised time series with a modern unfolding code and compare with NM-era GLE spectra.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
