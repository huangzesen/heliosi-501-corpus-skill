---
name: paper-spacepy-2022-twelve-years
description: >-
  Use when a workflow needs a Python toolkit for space-physics data production
  (radiation belt, geomagnetic, in-situ time series) or coordinate transforms
  via standard space-physics models (IGRF, T89/T96 magnetic-field models) —
  central claim is that SpacePy is a 12-year-old open-source ecosystem of
  reusable Python tools for heliophysics data production and analysis
  (Morley et al. 2022, arXiv:2208.10447).
version: 0.1.0
kind: paper-skill
quality: stub
paper:
  title: "The SpacePy space science package at 12 years"
  first_author: "Morley, S. K."
  year: 2022
  venue: "arXiv preprint (Frontiers in Astronomy and Space Sciences companion; software paper)"
  doi: null
  arxiv_id: "2208.10447"
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["data_access_infrastructure", "radiation_belt", "geomagnetic"]
  missions: ["other", "n/a"]
  regime: ["1au", "inner-heliosphere", "n/a"]
trigger_keywords:
  - "spacepy"
  - "space physics python"
  - "radiation belt analysis"
  - "IRBEM"
  - "Tsyganenko field model"
  - "T89"
  - "T96"
  - "coordinate transforms space physics"
  - "geomagnetic indices"
  - "MEO/GEO orbit analysis"
data_products: []
algorithms:
  - name: "Time + Coords containers (spacepy.time / spacepy.coordinates)"
    equation_refs: []
    external_implementations:
      - "https://github.com/spacepy/spacepy"
  - name: "IRBEM-based magnetic-field model interface (spacepy.irbempy)"
    equation_refs: []
    external_implementations:
      - "https://github.com/spacepy/spacepy"
      - "https://github.com/PRBEM/IRBEM"
  - name: "Empirical model registry (spacepy.empiricals)"
    equation_refs: []
    external_implementations:
      - "https://github.com/spacepy/spacepy"
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2208.10447"
  ads_url: null
  code_repo: "https://github.com/spacepy/spacepy"
  data_repo: null
claim_boundary:
  scope: >-
    The Morley et al. 2022 paper describes SpacePy's 12-year evolution as an
    open-source toolkit for heliophysics-data production with modules for
    time/coordinate handling, magnetic-field models via IRBEM, plotting,
    and PyCDF (CDF reader). Claims are scoped to the package's design and
    feature surface as of 2022.
  out_of_scope:
    - "Do not treat SpacePy as an in-situ science result — it is infrastructure."
    - "Do not assume SpacePy's CDF reader (PyCDF) is the default for new PSP work; cdflib is the lighter-weight alternative (see paper-cdflib-cdf-reader)."
    - "Do not use SpacePy's older Python 2 era recipes; the package now requires Python 3."
failure_modes:
  - "IRBEM Fortran library must be built locally; install can fail on platforms without a compatible Fortran toolchain (Windows especially)."
  - "PyCDF depends on NASA's CDF C library being installed system-wide; pure-Python alternatives (cdflib) avoid this."
  - "Coordinate transforms have implicit time-system assumptions (TT vs UT vs GPS); explicit Ticktock objects are required."
  - "Tsyganenko T89/T96/T01 models require external coefficient files and Kp/Dst inputs; check that your interval has valid solar-wind drivers."
  - "SpacePy's plotting tools wrap older matplotlib idioms; styles may not match modern projects."
depends_on: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/extended_search.md §7.8 and §7.10"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-paper", "infrastructure"]
source_type: software-paper
---

# SpacePy 12-years paper — paper-skill

> Compiled from Morley et al. (2022), "The SpacePy space science package at
> 12 years", arXiv:2208.10447. **Quality tier**: `stub` — promotion requires
> a runnable IRBEM-based field-line trace and a SpacePy → cdflib comparison.

---

## 1. Trigger

Reach for this skill when:

- A workflow needs **IRBEM-based magnetic-field models** (T89, T96, T01,
  T05) in Python.
- An agent must do **coordinate transforms** between geocentric systems
  (GSM, GSE, SM, GEO, MAG, GEI) with explicit time handling.
- A workflow needs radiation-belt phase-space-density (PSD) analysis,
  invariant coordinates (L*, K, μ).
- A user asks "should I use SpacePy or sunpy?" — SpacePy is for
  geocentric / in-situ / radiation-belt work; SunPy is for solar imaging
  and source modeling.

Do NOT use this skill when:

- The task is solar imaging (use `[[paper-sunpy-2023-interoperable-ecosystem]]`).
- The task is a pure CDF read with no model-coordinate work (use
  `[[paper-cdflib-cdf-reader]]`).

## 2. Paper claim → verifiable task

**Claim (narrow form).** SpacePy is an open-source Python package
providing space-physics utilities (time/coords/field models via IRBEM,
empirical models, CDF I/O via PyCDF) and has been maintained as a
production toolkit for 12 years (Morley et al. 2022).

**Verifiable task.** A reproduction succeeds when an agent can:

1. Install SpacePy with `irbempy` extension.
2. Construct a `Ticktock` time array + `Coords` position array for a known
   spacecraft interval (e.g., a Wind perihelion segment).
3. Trace a magnetic field line through T96 from a known starting position
   and verify the trace closes near Earth.

## 3. Methods / equations → executable workflow

### Time + coordinate containers

- Reference: SpacePy docs `spacepy.time.Ticktock`, `spacepy.coordinates.Coords`.
- Procedure:
  1. Build `t = Ticktock(["2022-01-01T00:00", ...], "ISO")`.
  2. Build `c = Coords([[r, lat, lon], ...], "GEO", "sph", ticks=t)`.
  3. Convert: `c_gsm = c.convert("GSM", "car")`.

### IRBEM-based field models

- Reference: `spacepy.irbempy` wraps the IRBEM Fortran library.
- Procedure:
  1. Choose field model (`"T89"`, `"T96"`, etc.).
  2. Pass position + time + solar-wind drivers (Kp, Dst, Pdyn).
  3. `traced = spacepy.irbempy.trace_field_line(t, c, extMag="T96")`.

### Empirical model registry

- Reference: `spacepy.empiricals` — wraps community empirical models
  (Tsyganenko coefficients, plasmapause models, etc.).

## 4. Data / instruments → tool contracts

No instrument-specific data contracts. SpacePy reads time series from
external sources (CDF, ASCII). Inputs:

| Driver | Source | Use |
|--------|--------|-----|
| Kp / Dst | OMNI | field-model driver |
| Pdyn (solar-wind dynamic pressure) | OMNI | field-model driver |
| Spacecraft ephemeris | mission archive (CDAWeb) | position input |

## 5. Validation target → benchmark artifact

> Not benchmarked yet — see `claim_boundary.scope`. Promotion to
> `executable` requires:
> - Tracing a known field line with T96 for a chosen interval.
> - Confirming closure within tolerance against an IRBEM Fortran
>   reference run.

## 6. Failure modes → skill memory

- **IRBEM build failure on Windows** — compile from source on Linux/macOS
  or use the IRBEM-Lib wheel where available.
- **CDF C library dependency for PyCDF** — install NASA CDF first, or
  switch to cdflib for read-only.
- **Implicit time system** — `Ticktock` distinguishes UT/TAI/GPS/TT; mixing
  systems silently shifts results by leap-second offsets.
- **Field-model driver freshness** — Kp/Dst arrays must cover the entire
  trace interval; missing drivers → silent extrapolation.
- **Tsyganenko model regime** — models are tuned to specific Kp/Dst ranges;
  using T96 in a Kp=8 storm exceeds its calibration.
- **Coordinate-system "spherical" convention differs from physics use** —
  `spacepy.coordinates` uses (r, lat, lon) with lat ∈ [-90, 90]; assert
  units before passing to external code.

## 7. Claim boundary

**In scope.** Space-physics Python utilities: time/coords, IRBEM field
models, empirical model registry, CDF I/O via PyCDF.

**Out of scope — do NOT generalize beyond:**

- Do not claim SpacePy replaces SunPy for solar imaging.
- Do not assert SpacePy's IRBEM wrapping yields numerically identical
  results to a direct IRBEM Fortran call without verifying.
- Do not use SpacePy's empirical models outside their calibration ranges.

## 8. Links

- DOI: n/a (preprint listing; published version exists in Frontiers in
  Astronomy and Space Sciences but DOI not in local inventory)
- arXiv: https://arxiv.org/abs/2208.10447
- ADS: n/a
- Code: https://github.com/spacepy/spacepy
- Data: n/a (consumer of external archives)

## 9. Skill graph → depends_on

- `[[paper-cdflib-cdf-reader]]` — alternative CDF reader; SpacePy's PyCDF
  and cdflib are sibling tools with different dependency footprints.
- `[[paper-pyspedas-multimission-data-access]]` — pySPEDAS often *uses*
  SpacePy under the hood for coordinate transforms.

## Notes

- The local inventory lists arXiv:2208.10447 as a software paper but does
  not name the full author list — flag at promotion.
- SpacePy / SunPy split is the canonical "in-situ vs. imaging" boundary
  in heliophysics Python — useful when an agent must route a request.
