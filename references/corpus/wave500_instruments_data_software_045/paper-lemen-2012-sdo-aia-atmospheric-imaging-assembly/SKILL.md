---
name: paper-lemen-2012-sdo-aia-atmospheric-imaging-assembly
description: >-
  Use when retrieving SDO/AIA full-disk EUV/UV imagery (94, 131, 171, 193, 211,
  304, 335, 1600, 1700 Å, plus 4500 Å) at 12 s cadence from 2010 onward —
  central claim is that AIA delivers 0.6"-pixel multi-wavelength imagery
  spanning chromosphere through flaring corona with stable photometric response
  (Lemen et al. 2012, Sol. Phys.).
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
  title: The Atmospheric Imaging Assembly (AIA) on the Solar Dynamics Observatory (SDO)
  first_author: "Lemen, J. R."
  year: 2012
  venue: Solar Physics
  doi: 10.1007/s11207-011-9776-8
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
  regime:
    - corona
trigger_keywords:
  - SDO AIA
  - Lemen 2012
  - atmospheric imaging assembly
  - EUV corona
  - AIA 171
  - AIA 193
  - AIA 304
  - solar dynamics observatory imager
data_products:
  - instrument: SDO/AIA EUV
    level: L1.5 (lev1 + pointing)
    cadence: 12 s
    interval: 2010-04..present
    archive: JSOC / SDAC
  - instrument: SDO/AIA UV (1600/1700)
    level: L1.5
    cadence: 24 s
    interval: 2010-04..present
    archive: JSOC
algorithms:
  - name: "aia_prep (point spread function, registration, flat-field)"
    equation_refs:
      - §6 Lemen 2012
    external_implementations:
      - SolarSoft aia_prep.pro
      - github.com/sunpy/aiapy
  - name: AIA differential emission measure (DEM) inversion
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1007/s11207-011-9776-8"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "http://jsoc.stanford.edu/"
claim_boundary:
  scope: >-
    SDO/AIA: four telescopes, ten wavelength channels (seven EUV, two UV, one
    visible continuum); 4096×4096 CCD, 0.6"/pix, 12 s cadence (EUV) / 24 s (UV).
    Mission 2010-04-30 to present.
  out_of_scope:
    - Do not use 1700 Å as a coronal diagnostic — it is photospheric continuum.
    - Do not skip aiapy / SolarSoft pointing correction when stacking across orbits.
    - Do not treat single-channel intensities as DEM-resolved — multi-channel inversion is needed.
failure_modes:
  - Saturation during X-class flares — use saturation-mitigated AEC images or DESAT pipeline.
  - PSF wings cause leakage between channels; deconvolve before quantitative EM.
  - Calibration evolves; refer to V9/V10 aia_response files.
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
# The Atmospheric Imaging Assembly (AIA) on the Solar Dynamics Observatory (SDO) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving SDO/AIA full-disk EUV/UV imagery (94, 131, 171, 193, 211, 304, 335, 1600, 1700 Å, plus 4500 Å) at 12 s cadence from 2010 onward — central claim is that AIA delivers 0.6"-pixel multi-wavelength imagery spanning chromosphere through flaring corona with stable photometric response (Lemen et al. 2012, Sol. Phys.).

Do NOT use this skill when:

- Do not use 1700 Å as a coronal diagnostic — it is photospheric continuum.
- Do not skip aiapy / SolarSoft pointing correction when stacking across orbits.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SDO/AIA: four telescopes, ten wavelength channels (seven EUV, two UV, one visible continuum); 4096×4096 CCD, 0.6"/pix, 12 s cadence (EUV) / 24 s (UV). Mission 2010-04-30 to present.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### aia_prep (point spread function, registration, flat-field)

- Paper reference: §6 Lemen 2012
- External implementation(s): SolarSoft aia_prep.pro, github.com/sunpy/aiapy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### AIA differential emission measure (DEM) inversion

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SDO/AIA EUV | L1.5 (lev1 + pointing) | 12 s | 2010-04..present | JSOC / SDAC |
| SDO/AIA UV (1600/1700) | L1.5 | 24 s | 2010-04..present | JSOC |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Saturation during X-class flares — use saturation-mitigated AEC images or DESAT pipeline.
- PSF wings cause leakage between channels; deconvolve before quantitative EM.
- Calibration evolves; refer to V9/V10 aia_response files.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SDO/AIA: four telescopes, ten wavelength channels (seven EUV, two UV, one visible continuum); 4096×4096 CCD, 0.6"/pix, 12 s cadence (EUV) / 24 s (UV). Mission 2010-04-30 to present.

**Out of scope — do NOT generalize beyond:**

- Do not use 1700 Å as a coronal diagnostic — it is photospheric continuum.
- Do not skip aiapy / SolarSoft pointing correction when stacking across orbits.
- Do not treat single-channel intensities as DEM-resolved — multi-channel inversion is needed.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1007/s11207-011-9776-8
- arXiv: n/a
- Code: n/a
- Data / archive: http://jsoc.stanford.edu/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.
