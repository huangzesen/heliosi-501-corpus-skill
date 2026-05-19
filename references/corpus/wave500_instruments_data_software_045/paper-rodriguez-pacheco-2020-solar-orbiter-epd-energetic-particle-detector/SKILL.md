---
name: paper-rodriguez-pacheco-2020-solar-orbiter-epd-energetic-particle-detector
description: >-
  Use when retrieving Solar Orbiter EPD energetic-particle data spanning STEP
  (2–80 keV electrons + suprathermal ions), EPT (electrons 25–475 keV; ions 25
  keV–6.4 MeV/nuc), SIS (3.5 keV/nuc–100 MeV/nuc heavy ions), and HET (10–100
  MeV ions, 0.3–18 MeV electrons) — central claim is that EPD delivers
  integrated SEP coverage from suprathermal to relativistic from 0.28 au outward
  (Rodríguez-Pacheco et al. 2020, A&A).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: The Energetic Particle Detector — Energetic particle instrument suite for the Solar Orbiter mission
  first_author: "Rodríguez-Pacheco, J."
  year: 2020
  venue: "Astronomy & Astrophysics"
  doi: 10.1051/0004-6361/201935287
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: energetic_particles
  secondary_themes: []
  missions:
    - Solar Orbiter
  regime:
    - inner-heliosphere
trigger_keywords:
  - Solar Orbiter EPD
  - Rodríguez-Pacheco 2020
  - EPT STEP HET SIS
  - energetic particle Solar Orbiter
  - SEP composition Solar Orbiter
data_products:
  - instrument: SO/EPD STEP
    level: L2
    cadence: 1 s - 1 min
    interval: null
    archive: SOAR
  - instrument: SO/EPD EPT
    level: L2
    cadence: 1 s - 1 min
    interval: null
    archive: SOAR
  - instrument: SO/EPD HET
    level: L2
    cadence: ~minutes
    interval: null
    archive: SOAR
  - instrument: SO/EPD SIS
    level: L2
    cadence: ~minutes
    interval: null
    archive: SOAR
algorithms:
  - name: EPT four-telescope pitch-angle reconstruction
    equation_refs:
      - §5 Rodríguez-Pacheco 2020
    external_implementations: []
  - name: SIS ToF + energy heavy-ion identification
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1051/0004-6361/201935287"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://soar.esac.esa.int/"
claim_boundary:
  scope: >-
    Solar Orbiter / EPD: STEP, EPT (4 telescopes), HET (2 telescopes), SIS
    (composition spectrometer). Different cadences and FOVs.
  out_of_scope:
    - Do not treat EPD electrons below 25 keV without using STEP — EPT begins at 25 keV.
    - Do not assume HET ion identification below 10 MeV/nuc; use SIS for that.
    - Do not compare EPD raw count rates across telescopes without geometry correction.
failure_modes:
  - Electron channels contaminated by ions during impulsive proton-rich events; check ion-flag.
  - Pitch angles biased if MAG B-direction is not converted to the relevant EPT telescope frame.
  - SIS gain table updates require reprocessing — confirm L2 version.
depends_on:
  - muller-2020-solar-orbiter-mission-overview
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# The Energetic Particle Detector — Energetic particle instrument suite for the Solar Orbiter mission — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving Solar Orbiter EPD energetic-particle data spanning STEP (2–80 keV electrons + suprathermal ions), EPT (electrons 25–475 keV; ions 25 keV–6.4 MeV/nuc), SIS (3.5 keV/nuc–100 MeV/nuc heavy ions), and HET (10–100 MeV ions, 0.3–18 MeV electrons) — central claim is that EPD delivers integrated SEP coverage from suprathermal to relativistic from 0.28 au outward (Rodríguez-Pacheco et al. 2020, A&A).

Do NOT use this skill when:

- Do not treat EPD electrons below 25 keV without using STEP — EPT begins at 25 keV.
- Do not assume HET ion identification below 10 MeV/nuc; use SIS for that.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Solar Orbiter / EPD: STEP, EPT (4 telescopes), HET (2 telescopes), SIS (composition spectrometer). Different cadences and FOVs.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### EPT four-telescope pitch-angle reconstruction

- Paper reference: §5 Rodríguez-Pacheco 2020
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### SIS ToF + energy heavy-ion identification

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SO/EPD STEP | L2 | 1 s - 1 min | — | SOAR |
| SO/EPD EPT | L2 | 1 s - 1 min | — | SOAR |
| SO/EPD HET | L2 | ~minutes | — | SOAR |
| SO/EPD SIS | L2 | ~minutes | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Electron channels contaminated by ions during impulsive proton-rich events; check ion-flag.
- Pitch angles biased if MAG B-direction is not converted to the relevant EPT telescope frame.
- SIS gain table updates require reprocessing — confirm L2 version.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Solar Orbiter / EPD: STEP, EPT (4 telescopes), HET (2 telescopes), SIS (composition spectrometer). Different cadences and FOVs.

**Out of scope — do NOT generalize beyond:**

- Do not treat EPD electrons below 25 keV without using STEP — EPT begins at 25 keV.
- Do not assume HET ion identification below 10 MeV/nuc; use SIS for that.
- Do not compare EPD raw count rates across telescopes without geometry correction.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1051/0004-6361/201935287
- arXiv: n/a
- Code: n/a
- Data / archive: https://soar.esac.esa.int/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[muller-2020-solar-orbiter-mission-overview]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
