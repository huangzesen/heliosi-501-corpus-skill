---
name: paper-brueckner-1995-soho-lasco-coronagraph-suite
description: >-
  Use when retrieving SOHO/LASCO C2/C3 white-light coronagraph images (since
  1996) for CME morphology, kinematics, and catalog construction — central claim
  is that LASCO's three nested coronagraphs (C1 1.1–3 R☉ — failed 1998; C2 2–6
  R☉; C3 3.7–30 R☉) provide multi-decade white-light corona movies with
  ~minute–hour cadence (Brueckner et al. 1995, Sol. Phys.).
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
  title: The Large Angle Spectroscopic Coronagraph (LASCO)
  first_author: "Brueckner, G. E."
  year: 1995
  venue: Solar Physics
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - other
  regime:
    - corona
trigger_keywords:
  - SOHO LASCO
  - Brueckner 1995
  - white-light corona
  - CDAW CME catalog
  - coronagraph
  - CME kinematics
  - C2 C3 imagery
  - SOHO coronal mass ejection
data_products:
  - instrument: SOHO/LASCO C2
    level: L0.5/L1
    cadence: ~12 min
    interval: 1996-present
    archive: LASCO/NRL / VSO / SPDF
  - instrument: SOHO/LASCO C3
    level: L0.5/L1
    cadence: ~12-60 min
    interval: 1996-present
    archive: LASCO/NRL
  - instrument: LASCO CDAW CME catalog
    level: catalog
    cadence: event-based
    interval: 1996-present
    archive: cdaw.gsfc.nasa.gov/CME_list/
algorithms:
  - name: "LASCO reduce (vignette, mask, F-corona subtraction)"
    equation_refs:
      - §4 Brueckner 1995
    external_implementations:
      - SolarSoft reduce_level_05.pro / reduce_level_1.pro
  - name: CDAW CME catalog manual measurement workflow
    equation_refs: []
    external_implementations:
      - "https://cdaw.gsfc.nasa.gov/CME_list/"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://lasco-www.nrl.navy.mil/"
claim_boundary:
  scope: >-
    SOHO/LASCO: externally occulted (C2, C3) and internally occulted (C1) white-
    light polarized-brightness coronagraphs. C1 lost in 1998 SOHO mishap; C2 +
    C3 routinely operational. CDAW LASCO CME catalog is the canonical multi-
    decade CME database.
  out_of_scope:
    - Do not use LASCO C1 for any epoch after 1998-06-24.
    - Do not treat the CDAW CME catalog as automatic — it is manually curated and biased.
    - Do not assume photometric flat field is stable across the mission; LASCO calibration evolves.
failure_modes:
  - Cosmic-ray hits leave streaks; despike before differencing.
  - Pylon (occulter support) leaves a fixed-azimuth blank — mask in radial profiles.
  - "Pre-2003 spacecraft roll campaigns mean N is not always 'up'; check ROLL keyword."
depends_on:
  []
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
# The Large Angle Spectroscopic Coronagraph (LASCO) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving SOHO/LASCO C2/C3 white-light coronagraph images (since 1996) for CME morphology, kinematics, and catalog construction — central claim is that LASCO's three nested coronagraphs (C1 1.1–3 R☉ — failed 1998; C2 2–6 R☉; C3 3.7–30 R☉) provide multi-decade white-light corona movies with ~minute–hour cadence (Brueckner et al. 1995, Sol. Phys.).

Do NOT use this skill when:

- Do not use LASCO C1 for any epoch after 1998-06-24.
- Do not treat the CDAW CME catalog as automatic — it is manually curated and biased.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SOHO/LASCO: externally occulted (C2, C3) and internally occulted (C1) white-light polarized-brightness coronagraphs. C1 lost in 1998 SOHO mishap; C2 + C3 routinely operational. CDAW LASCO CME catalog is the canonical multi-decade CME database.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### LASCO reduce (vignette, mask, F-corona subtraction)

- Paper reference: §4 Brueckner 1995
- External implementation(s): SolarSoft reduce_level_05.pro / reduce_level_1.pro
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### CDAW CME catalog manual measurement workflow

- External implementation(s): https://cdaw.gsfc.nasa.gov/CME_list/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SOHO/LASCO C2 | L0.5/L1 | ~12 min | 1996-present | LASCO/NRL / VSO / SPDF |
| SOHO/LASCO C3 | L0.5/L1 | ~12-60 min | 1996-present | LASCO/NRL |
| LASCO CDAW CME catalog | catalog | event-based | 1996-present | cdaw.gsfc.nasa.gov/CME_list/ |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Cosmic-ray hits leave streaks; despike before differencing.
- Pylon (occulter support) leaves a fixed-azimuth blank — mask in radial profiles.
- Pre-2003 spacecraft roll campaigns mean N is not always 'up'; check ROLL keyword.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SOHO/LASCO: externally occulted (C2, C3) and internally occulted (C1) white-light polarized-brightness coronagraphs. C1 lost in 1998 SOHO mishap; C2 + C3 routinely operational. CDAW LASCO CME catalog is the canonical multi-decade CME database.

**Out of scope — do NOT generalize beyond:**

- Do not use LASCO C1 for any epoch after 1998-06-24.
- Do not treat the CDAW CME catalog as automatic — it is manually curated and biased.
- Do not assume photometric flat field is stable across the mission; LASCO calibration evolves.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://lasco-www.nrl.navy.mil/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Sol. Phys. 162, 357 (1995)
