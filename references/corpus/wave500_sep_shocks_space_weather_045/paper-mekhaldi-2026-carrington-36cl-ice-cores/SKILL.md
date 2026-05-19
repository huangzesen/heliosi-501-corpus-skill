---
name: paper-mekhaldi-2026-carrington-36cl-ice-cores
description: >-
  Use when carrington 1859 or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Two 36Cl records and 10Be data show no significant 1859 enhancement, ruling out an extreme >30 MeV SEP event for the Carrington storm; either the SEP fluence was soft (up to ~3× the largest Space Age event) or there was no Earth-bound SEP. (arXiv:2604.26608, 2026).
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
  title: "36Cl Concentrations from Polar Ice Cores Set New Constraints on the Carrington Event"
  first_author: "Mekhaldi, F."
  authors:
    - "Mekhaldi, F."
    - "Paleari, C. I."
    - "Smith, A. M."
    - "Aldahan, A."
    - "Beer, J."
    - "Christl, M."
    - "Vockenhuber, C."
    - "Hayakawa, H."
    - "Curran, M."
    - "Erhardt, T."
    - "Plummer, C."
    - "Simon, K."
    - "Wilcken, K."
    - "Zheng, M."
    - "Muscheler, R."
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2604.26608"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Ice-core archive (EGRIP, NGRIP, Law Dome)]
  regime: [inner-heliosphere]

trigger_keywords:
  - "Carrington 1859"
  - "36Cl ice core"
  - "10Be EGRIP NGRIP Dome Summit Law Dome"
  - "SEP fluence >30 MeV"
  - "worst-case scenario constraint"
  - "soft SEP event"
  - "no Earth-bound SEP"

data_products:
  - instrument: "EGRIP 36Cl + 10Be"
    level: "ice-core layer-counted"
    cadence: "2–4 yr / semi-annual"
    interval: "1850–1870 CE"
    archive: "ice-core archive (TODO_verify DOI)"
  - instrument: "NGRIP 36Cl"
    level: "ice-core layer-counted"
    cadence: "2–4 yr"
    interval: "1850–1870 CE"
    archive: "ice-core archive"
  - instrument: "Law Dome 36Cl + 10Be"
    level: "ice-core annual"
    cadence: "annual"
    interval: "1850–1870 CE"
    archive: "ice-core archive"

algorithms:
  - name: "Layer-counted chronology of 36Cl / 10Be enhancements"
    equation_refs: []
    external_implementations: []
  - name: "Atmospheric-transport-corrected fluence inversion (>30 MeV)"
    equation_refs: []
    external_implementations: []
  - name: "Comparison against Space Age fluence reference distribution"
    equation_refs: []
    external_implementations: []
  - name: "Two-scenario fit: soft SEP up to 3× SA-max vs no Earth-bound SEP"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.26608"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Greenland (EGRIP, NGRIP) and Antarctic (Law Dome) ice cores; 36Cl 2–4 yr resolution; semi-annual + annual 10Be; 1859 CE Carrington epoch; >30 MeV fluence constraint.
  out_of_scope:
    - "Do not generalize the Carrington upper bound to other historical events (e.g. 774 CE) without separate analysis."
    - "Do not infer event spectral shape from a single cosmogenic isotope."
    - "Do not use as evidence for absence of geomagnetic activity at 1859."

failure_modes:
  - "Atmospheric transport of cosmogenic isotopes biases hemispheric attribution"
  - "Sample-resolution averaging dilutes short-duration spikes"
  - "10Be production yields differ between solar protons and GCRs"
  - "Carrington in-situ instrumentation is absent — model dependence"

depends_on:
  - "paper-dalla-2026-radiation-doses-extreme-seps"
  - "paper-mishev-2026-first-four-gles-1940s"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No joint forward-modeling of 36Cl + 14C + 10Be for 1859 that publishes a posterior on event spectral shape."
    related_skills: []
  - type: "hypothesis"
    statement: "The Carrington SEP spectrum, if extant, is sufficiently soft to explain non-detection in 36Cl while still depositing >30 MeV protons under specific geomagnetic conditions."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Run a CRAC/Geant4 forward model assuming SA-max spectrum × 3 and check predicted 36Cl spike against detection limits."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2604.26608"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# 36Cl Concentrations from Polar Ice Cores Set New Constraints on the Carrington Event — paper-skill

> Compiled from arXiv:2604.26608 (2026), Mekhaldi, F. et al.
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

- Carrington 1859
- 36Cl ice core
- 10Be EGRIP NGRIP Dome Summit Law Dome

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Two 36Cl records and 10Be data show no significant 1859 enhancement, ruling out an extreme >30 MeV SEP event for the Carrington storm; either the SEP fluence was soft (up to ~3× the largest Space Age event) or there was no Earth-bound SEP.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces No significant 36Cl enhancement at 1859 within instrument detection limits; >30 MeV fluence upper bound (specific value TODO_verify); two compatible scenarios as stated in claim. within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Layer-counted chronology of 36Cl / 10Be enhancements

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Layer-counted chronology of 36Cl / 10Be enhancements as a callable on the data products in §4.

### Atmospheric-transport-corrected fluence inversion (>30 MeV)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Atmospheric-transport-corrected fluence inversion (>30 MeV) as a callable on the data products in §4.

### Comparison against Space Age fluence reference distribution

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Comparison against Space Age fluence reference distribution as a callable on the data products in §4.

### Two-scenario fit: soft SEP up to 3× SA-max vs no Earth-bound SEP

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Two-scenario fit: soft SEP up to 3× SA-max vs no Earth-bound SEP as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| EGRIP 36Cl + 10Be | ice-core layer-counted | 2–4 yr / semi-annual | 1850–1870 CE | ice-core archive (TODO_verify DOI) | abstract: load + decode + subset |
| NGRIP 36Cl | ice-core layer-counted | 2–4 yr | 1850–1870 CE | ice-core archive | abstract: load + decode + subset |
| Law Dome 36Cl + 10Be | ice-core annual | annual | 1850–1870 CE | ice-core archive | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: No significant 36Cl enhancement at 1859 within instrument detection limits; >30 MeV fluence upper bound (specific value TODO_verify); two compatible scenarios as stated in claim.

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Atmospheric transport of cosmogenic isotopes biases hemispheric attribution
- Sample-resolution averaging dilutes short-duration spikes
- 10Be production yields differ between solar protons and GCRs
- Carrington in-situ instrumentation is absent — model dependence

## 7. Claim boundary  *(Layer 1)*

**In scope.** Greenland (EGRIP, NGRIP) and Antarctic (Law Dome) ice cores; 36Cl 2–4 yr resolution; semi-annual + annual 10Be; 1859 CE Carrington epoch; >30 MeV fluence constraint.

**Out of scope — do NOT generalize beyond:**

- Do not generalize the Carrington upper bound to other historical events (e.g. 774 CE) without separate analysis.
- Do not infer event spectral shape from a single cosmogenic isotope.
- Do not use as evidence for absence of geomagnetic activity at 1859.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2604.26608
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-dalla-2026-radiation-doses-extreme-seps]]` — assumed for context (see linked skill).
- `[[paper-mishev-2026-first-four-gles-1940s]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No joint forward-modeling of 36Cl + 14C + 10Be for 1859 that publishes a posterior on event spectral shape.
- **Hypothesis** — The Carrington SEP spectrum, if extant, is sufficiently soft to explain non-detection in 36Cl while still depositing >30 MeV protons under specific geomagnetic conditions.
- **Minimal_experiment** — Run a CRAC/Geant4 forward model assuming SA-max spectrum × 3 and check predicted 36Cl spike against detection limits.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
