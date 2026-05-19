---
name: paper-sunraster-sunpy-affiliated-raster-spectra
description: >-
  Use when working with solar slit-spectrograph or raster IFU data (Hinode/EIS,
  IRIS, Solar Orbiter/SPICE) — central claim is that sunraster provides
  n-dimensional Raster / RasterSequence classes (built on ndcube) for (slit-
  position, slit-y, wavelength, time) spectral cubes (SunPy affiliated; no
  standalone paper in local inventory).
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
  title: sunraster — Spectral raster handling for solar IFU/raster instruments
  first_author: sunraster developers
  year: 2024
  venue: software package (SunPy affiliated; no dedicated paper in local inventory)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - other
    - Solar Orbiter
  regime:
    - corona
trigger_keywords:
  - sunraster
  - EIS Python
  - IRIS raster
  - SPICE solar orbiter raster
  - ndcube spectral
data_products:
  - instrument: Hinode/EIS rasters
    level: L1
    cadence: raster-dependent
    interval: 2006-present
    archive: MSSL EIS archive
  - instrument: IRIS spectral rasters
    level: L2
    cadence: raster-dependent
    interval: 2013-present
    archive: LMSAL IRIS archive
  - instrument: Solar Orbiter/SPICE rasters
    level: L2
    cadence: campaign-dependent
    interval: null
    archive: SOAR
algorithms:
  - name: Raster N-D slicing with WCS preservation
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunraster"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/sunpy/sunraster"
  data_repo: null
claim_boundary:
  scope: >-
    sunraster: SunPy-affiliated; data structures (Raster, RasterSequence) with
    WCS-aware slicing. Used by EISpac and IRIS-aware tooling.
  out_of_scope:
    - Do not use sunraster for imaging-only data (no spectral axis).
    - Do not bypass calibration upstream; sunraster does not radiometrically calibrate.
failure_modes:
  - WCS axis-order conventions can flip between mission FITS files — check axis labels before slicing.
  - ndcube version mismatch can break slicing operators.
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
  - paper-astropy-2022-collaboration-community-package
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# sunraster — Spectral raster handling for solar IFU/raster instruments — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when working with solar slit-spectrograph or raster IFU data (Hinode/EIS, IRIS, Solar Orbiter/SPICE) — central claim is that sunraster provides n-dimensional Raster / RasterSequence classes (built on ndcube) for (slit-position, slit-y, wavelength, time) spectral cubes (SunPy affiliated; no standalone paper in local inventory).

Do NOT use this skill when:

- Do not use sunraster for imaging-only data (no spectral axis).
- Do not bypass calibration upstream; sunraster does not radiometrically calibrate.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** sunraster: SunPy-affiliated; data structures (Raster, RasterSequence) with WCS-aware slicing. Used by EISpac and IRIS-aware tooling.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Raster N-D slicing with WCS preservation

- External implementation(s): https://github.com/sunpy/sunraster
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Hinode/EIS rasters | L1 | raster-dependent | 2006-present | MSSL EIS archive |
| IRIS spectral rasters | L2 | raster-dependent | 2013-present | LMSAL IRIS archive |
| Solar Orbiter/SPICE rasters | L2 | campaign-dependent | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- WCS axis-order conventions can flip between mission FITS files — check axis labels before slicing.
- ndcube version mismatch can break slicing operators.

## 7. Claim boundary  *(Layer 1)*

**In scope.** sunraster: SunPy-affiliated; data structures (Raster, RasterSequence) with WCS-aware slicing. Used by EISpac and IRIS-aware tooling.

**Out of scope — do NOT generalize beyond:**

- Do not use sunraster for imaging-only data (no spectral axis).
- Do not bypass calibration upstream; sunraster does not radiometrically calibrate.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://github.com/sunpy/sunraster
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`
- `[[paper-astropy-2022-collaboration-community-package]]`

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- No standalone publication located; citation TODO
