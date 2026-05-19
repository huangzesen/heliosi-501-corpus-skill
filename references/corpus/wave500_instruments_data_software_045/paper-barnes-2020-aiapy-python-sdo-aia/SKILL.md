---
name: paper-barnes-2020-aiapy-python-sdo-aia
description: >-
  Use when calibrating and registering SDO/AIA images in Python (replacing
  SolarSoft aia_prep) — central claim is that aiapy ports AIA L1 → L1.5 prep,
  point-spread function deconvolution, and degradation correction into the
  Python heliophysics stack on top of sunpy (Barnes et al. 2020, JOSS).
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
  title: "aiapy: A Python Package for Analyzing Solar EUV Image Data from AIA"
  first_author: "Barnes, W. T."
  year: 2020
  venue: Journal of Open Source Software
  doi: 10.21105/joss.02801
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
  - aiapy
  - Barnes 2020
  - AIA prep Python
  - aia_prep replacement
  - AIA degradation
  - AIA PSF deconvolution
data_products:
  - instrument: SDO/AIA
    level: L1 → L1.5 via aiapy
    cadence: 12 s
    interval: 2010-04..present
    archive: JSOC (via drms)
algorithms:
  - name: "aiapy.calibrate.register (rotate, scale, recenter to standard pixel grid)"
    equation_refs: []
    external_implementations:
      - "https://github.com/LM-SAL/aiapy"
  - name: aiapy.calibrate.correct_degradation (channel time-dep response)
    equation_refs: []
    external_implementations: []
  - name: aiapy.psf.deconvolve (Richardson-Lucy)
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.21105/joss.02801"
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/LM-SAL/aiapy"
  data_repo: null
claim_boundary:
  scope: >-
    aiapy: SunPy-affiliated package for SDO/AIA image-prep operations: register,
    correct_degradation, psf_deconvolve, normalize_exposure. Consumes
    sunpy.map.Map objects.
  out_of_scope:
    - Do not use aiapy on HMI or any non-AIA imager.
    - Do not skip degradation correction for absolute photometric work.
    - Do not assume PSF deconvolution is required for all use cases — it is expensive.
failure_modes:
  - Degradation correction uses an internal CalibrationVersion file; outdated cache leads to wrong response.
  - PSF deconvolution amplifies noise; limit iterations.
  - Register output pixel scale fixed; do not chain with another resampler.
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
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# aiapy: A Python Package for Analyzing Solar EUV Image Data from AIA — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when calibrating and registering SDO/AIA images in Python (replacing SolarSoft aia_prep) — central claim is that aiapy ports AIA L1 → L1.5 prep, point-spread function deconvolution, and degradation correction into the Python heliophysics stack on top of sunpy (Barnes et al. 2020, JOSS).

Do NOT use this skill when:

- Do not use aiapy on HMI or any non-AIA imager.
- Do not skip degradation correction for absolute photometric work.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** aiapy: SunPy-affiliated package for SDO/AIA image-prep operations: register, correct_degradation, psf_deconvolve, normalize_exposure. Consumes sunpy.map.Map objects.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### aiapy.calibrate.register (rotate, scale, recenter to standard pixel grid)

- External implementation(s): https://github.com/LM-SAL/aiapy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### aiapy.calibrate.correct_degradation (channel time-dep response)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### aiapy.psf.deconvolve (Richardson-Lucy)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SDO/AIA | L1 → L1.5 via aiapy | 12 s | 2010-04..present | JSOC (via drms) |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Degradation correction uses an internal CalibrationVersion file; outdated cache leads to wrong response.
- PSF deconvolution amplifies noise; limit iterations.
- Register output pixel scale fixed; do not chain with another resampler.

## 7. Claim boundary  *(Layer 1)*

**In scope.** aiapy: SunPy-affiliated package for SDO/AIA image-prep operations: register, correct_degradation, psf_deconvolve, normalize_exposure. Consumes sunpy.map.Map objects.

**Out of scope — do NOT generalize beyond:**

- Do not use aiapy on HMI or any non-AIA imager.
- Do not skip degradation correction for absolute photometric work.
- Do not assume PSF deconvolution is required for all use cases — it is expensive.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.21105/joss.02801
- arXiv: n/a
- Code: https://github.com/LM-SAL/aiapy
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`
- `[[paper-astropy-2022-collaboration-community-package]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
