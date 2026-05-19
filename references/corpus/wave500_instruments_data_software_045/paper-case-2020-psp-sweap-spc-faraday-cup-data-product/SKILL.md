---
name: paper-case-2020-psp-sweap-spc-faraday-cup-data-product
description: >-
  Use when retrieving PSP SWEAP/SPC Faraday-cup ion bulk moments (proton +
  alpha) at high cadence (≥1 Hz at perihelion) — central claim is that SPC is a
  sun-pointed Faraday cup giving Np, Vp, Tp via I(V) sweeps every 0.2–1 s with
  calibrated moments (Case et al. 2020, ApJS).
version: 0.1.0
kind: paper-skill
quality: method-ready
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: The Solar Probe Cup on the Parker Solar Probe
  first_author: "Case, A. W."
  year: 2020
  venue: The Astrophysical Journal Supplement Series
  doi: 10.3847/1538-4365/ab5a7b
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: psp_data
  secondary_themes: []
  missions:
    - PSP
  regime:
    - inner-heliosphere
    - MHD-scale
trigger_keywords:
  - PSP SPC
  - Case 2020
  - solar probe cup
  - Faraday cup PSP
  - PSP proton bulk moments
  - SWEAP SPC alpha
  - PSP near-sun ions
data_products:
  - instrument: PSP/SWEAP SPC
    level: L3 moments
    cadence: 0.2-1 s
    interval: null
    archive: SPDF / PSP SOC
  - instrument: PSP/SWEAP SPC I-V curves
    level: L2
    cadence: 0.2-1 s
    interval: null
    archive: SPDF
algorithms:
  - name: Bimaxwellian Faraday-cup fit to I(V) sweep
    equation_refs:
      - §3 Case 2020
    external_implementations: []
  - name: SPC quality-flag interpretation
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.3847/1538-4365/ab5a7b"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/"
claim_boundary:
  scope: >-
    PSP/SWEAP SPC: nine-channel Faraday cup, modulated voltage sweeps; produces
    calibrated proton bulk moments at 0.2-1 s cadence; alpha moments at slower
    cadence. Operational on all encounters.
  out_of_scope:
    - Do not use SPC outside the sun-pointed ±30° field of view; SPAN-I covers wider angles.
    - Do not assume SPC alpha moments are reliable in cold streams where He²⁺ peak overlaps proton.
    - Do not assume moments are correct without checking the SPC quality flag.
failure_modes:
  - "Alpha peak misidentification at high Tp — use bi-maxwellian fit, not moment integration."
  - "When PSP yaws away from sun (off-pointing), SPC FOV moves off bulk — flag drops."
  - Cup contamination during Venus flybys produces transient artifacts.
depends_on:
  - kasper-2016-sweap-investigation-psp
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
# The Solar Probe Cup on the Parker Solar Probe — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving PSP SWEAP/SPC Faraday-cup ion bulk moments (proton + alpha) at high cadence (≥1 Hz at perihelion) — central claim is that SPC is a sun-pointed Faraday cup giving Np, Vp, Tp via I(V) sweeps every 0.2–1 s with calibrated moments (Case et al. 2020, ApJS).

Do NOT use this skill when:

- Do not use SPC outside the sun-pointed ±30° field of view; SPAN-I covers wider angles.
- Do not assume SPC alpha moments are reliable in cold streams where He²⁺ peak overlaps proton.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PSP/SWEAP SPC: nine-channel Faraday cup, modulated voltage sweeps; produces calibrated proton bulk moments at 0.2-1 s cadence; alpha moments at slower cadence. Operational on all encounters.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Bimaxwellian Faraday-cup fit to I(V) sweep

- Paper reference: §3 Case 2020
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### SPC quality-flag interpretation

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/SWEAP SPC | L3 moments | 0.2-1 s | — | SPDF / PSP SOC |
| PSP/SWEAP SPC I-V curves | L2 | 0.2-1 s | — | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Alpha peak misidentification at high Tp — use bi-maxwellian fit, not moment integration.
- When PSP yaws away from sun (off-pointing), SPC FOV moves off bulk — flag drops.
- Cup contamination during Venus flybys produces transient artifacts.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PSP/SWEAP SPC: nine-channel Faraday cup, modulated voltage sweeps; produces calibrated proton bulk moments at 0.2-1 s cadence; alpha moments at slower cadence. Operational on all encounters.

**Out of scope — do NOT generalize beyond:**

- Do not use SPC outside the sun-pointed ±30° field of view; SPAN-I covers wider angles.
- Do not assume SPC alpha moments are reliable in cold streams where He²⁺ peak overlaps proton.
- Do not assume moments are correct without checking the SPC quality flag.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.3847/1538-4365/ab5a7b
- arXiv: n/a
- Code: n/a
- Data / archive: https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[kasper-2016-sweap-investigation-psp]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
