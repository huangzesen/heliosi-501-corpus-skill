---
name: paper-pyspedas-multimission-data-access
description: >-
  Use when a workflow needs a unified Python downloader for multi-mission
  in-situ heliophysics data (PSP, Solar Orbiter, MMS, THEMIS, Wind, ACE, etc.)
  with built-in tplot variables and plotting — central claim is that pySPEDAS
  ports SPEDAS-IDL conventions to Python with mission-specific loaders
  (software package; no standalone publication located in local inventory).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "pySPEDAS: Python port of SPEDAS for multi-mission space-physics data"
  first_author: "pySPEDAS contributors"
  authors_verified: false
  year: 2022
  venue: "software package (Python port of SPEDAS-IDL); no dedicated paper located in local inventory"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["psp_data", "solar_orbiter", "data_access_infrastructure"]
  missions: ["PSP", "Solar Orbiter", "Wind", "ACE", "THEMIS", "MAVEN", "MESSENGER", "STEREO", "other"]
  regime: ["1au", "inner-heliosphere"]
trigger_keywords:
  - "pyspedas"
  - "SPEDAS"
  - "tplot"
  - "PSP loader"
  - "MMS loader"
  - "THEMIS loader"
  - "Solar Orbiter loader"
  - "multi-mission data"
  - "in-situ time series"
  - "CDAWeb python"
  - "SPDF"
data_products:
  - instrument: "PSP/FIELDS MAG (RTN, L2)"
    level: "L2"
    cadence: "4 Sa/cyc, 293 Hz survey"
    interval: null
    archive: "SPDF / PSP SOC"
  - instrument: "PSP/SWEAP SPAN-I"
    level: "L2"
    cadence: "0.2 Hz"
    interval: null
    archive: "SPDF"
  - instrument: "Solar Orbiter MAG"
    level: "L2"
    cadence: "8 Hz (normal mode)"
    interval: null
    archive: "SOAR / SPDF"
  - instrument: "MMS FGM / FPI"
    level: "L2"
    cadence: "burst / fast"
    interval: null
    archive: "SDC / SPDF"
algorithms:
  - name: "Mission-specific loader (pyspedas.psp.fields, pyspedas.solo.mag, ...)"
    equation_refs: []
    external_implementations:
      - "https://github.com/spedas/pyspedas"
  - name: "tplot variable model"
    equation_refs: []
    external_implementations:
      - "https://github.com/MAVENSDC/PyTplot"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/spedas/pyspedas"
  data_repo: null
claim_boundary:
  scope: >-
    pySPEDAS provides Python loaders for in-situ heliophysics data from
    multiple missions (PSP, Solar Orbiter, MMS, THEMIS, Wind, ACE, MAVEN,
    MESSENGER, STEREO, etc.) following SPEDAS-IDL conventions. It is
    primarily a *downloader + tplot variable producer*; it does not by
    itself perform mission-specific calibration beyond what's encoded in
    the source CDFs.
  out_of_scope:
    - "Do not assume pySPEDAS loaders include all instrument modes for every mission; some modes still require manual CDF fetching."
    - "Do not treat tplot variables as a publication-grade product; they are convenience structures."
    - "Do not use pySPEDAS as the only authority for instrument calibration; defer to mission documentation."
    - "Do not assume the local inventory contains a dedicated pySPEDAS publication; local extended_search.md explicitly notes none was found (§ summary)."
failure_modes:
  - "Loaders silently return empty arrays if the requested interval has no data; check return length before continuing."
  - "Variable names differ subtly across missions (`PSP_psp_fld_l2_mag_RTN_4_Sa_per_Cyc` vs `psp_fld_l2_mag_RTN_4_Sa_per_Cyc`); print returned variable names rather than hard-coding."
  - "pySPEDAS keeps a local cache directory; clearing it resets quota issues but loses already-downloaded data."
  - "Burst-mode data (MMS, PSP) is large; a one-day query can download many GB without warning."
  - "tplot's time axis uses Unix timestamps; mixing with numpy `datetime64` requires explicit conversion."
  - "SPEDAS-IDL behavioral quirks (e.g., default trange tracking) sometimes leak into the Python port; check `pyspedas.tplot_options('trange', ...)`."
depends_on:
  - paper-cdflib-cdf-reader
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/extended_search.md §7 summary (notes PySPEDAS has no dedicated paper); sioulas-reproduction/results/github_repos/consolidated_repos.json (pyspedas entry); .library/custom/heliophysics-skills/sub-skills/github-repos.md (pyspedas entry)"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "data-access", "infrastructure"]
source_type: software-package
---

# pySPEDAS — paper-skill

> Compiled from the pySPEDAS software package
> (https://github.com/spedas/pyspedas) and local references. **Quality
> tier**: `method-ready` — workflow documented, runnable. No
> standalone publication located locally; local source explicitly notes
> the gap.

---

## 1. Trigger

Reach for this skill when:

- A workflow needs PSP/FIELDS, PSP/SWEAP, Solar Orbiter MAG, MMS FGM/FPI,
  THEMIS, Wind, ACE, etc. **time-series in-situ data** in Python.
- An agent needs to **multi-mission overplot** quickly (tplot variables).
- A user wants the "SPEDAS-IDL but in Python" experience.
- A workflow is choosing between pySPEDAS and `cdflib` directly —
  pySPEDAS adds mission-loader conventions and tplot; cdflib is lower
  level.

Do NOT use this skill when:

- The task is purely about reading a single CDF file with no mission
  context (use `[[paper-cdflib-cdf-reader]]`).
- The task is solar imaging (use `[[paper-sunpy-2023-interoperable-ecosystem]]`).

## 2. Paper claim → verifiable task

**Claim (narrow form).** pySPEDAS provides per-mission Python loaders
that download CDF files from SPDF / SOC / SDC archives and convert them
into `tplot` variables compatible with the SPEDAS-IDL ecosystem.

**Verifiable task.** A reproduction succeeds when an agent:

1. Imports `pyspedas`.
2. Calls a known loader (`pyspedas.psp.fields(trange=..., level="l2")`).
3. Receives a non-empty list of tplot variable names.
4. Loads the corresponding variable via `pytplot.get_data(name)` and
   verifies non-zero length.

## 3. Methods / equations → executable workflow

### Mission-specific loader

- Reference: pySPEDAS docs, per-mission submodule.
- Procedure:

```python
import pyspedas
import pytplot
trange = ["2021-04-29/00:00", "2021-04-29/06:00"]
vars_psp = pyspedas.psp.fields(trange=trange, level="l2", datatype="mag_rtn_4_sa_per_cyc")
t, b = pytplot.get_data(vars_psp[0])
```

### tplot variable model

- Reference: PyTplot.
- Procedure:
  1. Variables are named, time-tagged arrays with metadata.
  2. Use `pytplot.tplot(["var1", "var2"])` for quick stacks.
  3. Convert to plain arrays for downstream science.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Archive | Loader call (pyspedas) |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 4 Sa/cyc | SPDF | `pyspedas.psp.fields(datatype="mag_rtn_4_sa_per_cyc")` |
| PSP/SWEAP SPAN-I | L2 | 0.2 Hz | SPDF | `pyspedas.psp.spi(datatype="sf00_l2_8dx32ex8a")` |
| Solar Orbiter MAG | L2 | 8 Hz | SOAR/SPDF | `pyspedas.solo.mag(...)` |
| MMS FGM | L2 | burst | SDC/SPDF | `pyspedas.mms.fgm(...)` |
| Wind 3DP | L2 | varies | SPDF | `pyspedas.wind.threedp(...)` |

The general-purpose harness's Bash+pip is sufficient; no `mcp:pyspedas`
is asserted.

## 5. Validation target → benchmark artifact

> Not benchmarked yet — `method-ready`. Promotion to `executable`
> requires a smoke test:
> - For each of {PSP, Solar Orbiter, MMS}, load a known interval.
> - Confirm the returned tplot variables contain expected names.
> - Emit `metrics.json` with `{n_vars_loaded, length_samples,
>   first_timestamp, last_timestamp}`.

## 6. Failure modes → skill memory

- **Empty returns** — silent. Always check returned variable list length.
- **Variable naming drift** — across pySPEDAS releases the variable name
  template can change. Print returned names; do not hard-code.
- **Cache directory growth** — `~/.pyspedas/` can balloon to many GB;
  monitor and prune.
- **Burst-mode data volume** — MMS burst, PSP MAG full cadence: a day can
  exceed 50 GB.
- **trange string parsing** — accepts ISO 8601 and `YYYY-MM-DD/HH:MM`;
  ambiguity around timezone can shift queries by hours.
- **Threading/multiprocessing** — pySPEDAS is single-process; parallel
  downloads via `concurrent.futures` can corrupt cache files.

## 7. Claim boundary

**In scope.** Multi-mission Python data loaders + tplot variables.

**Out of scope — do NOT generalize beyond:**

- pySPEDAS does NOT calibrate beyond the source CDF; do not claim
  publication-grade calibration without verifying.
- pySPEDAS is NOT a coordinate-transform library at the depth of SpacePy;
  use SpacePy or astropy for that.
- pySPEDAS is NOT a science-analysis package; downstream science needs
  its own paper-skills.

## 8. Links

- DOI: n/a (no dedicated publication in local inventory)
- arXiv: n/a (local source explicitly notes none was found)
- ADS: n/a
- Code: https://github.com/spedas/pyspedas
- Data: n/a (consumes SPDF/SOC/SDC archives)

## 9. Skill graph → depends_on

- `[[paper-cdflib-cdf-reader]]` — underlies pySPEDAS for CDF reading.
- `[[paper-spacepy-2022-twelve-years]]` — adjacent space-physics toolkit;
  the two are complementary, not redundant.

## Notes

- Local source `extended_search.md` summary notes explicitly:
  *"PySPEDAS: No dedicated PySPEDAS paper surfaced; query 7 was dominated
  by SunPy and SpacePy results."* This skill is therefore tagged
  `software-package` with no `paper` field doi/arxiv.
- A future verifier should locate a JOSS or Frontiers paper on pySPEDAS if
  one exists; promotion to `executable` does not require it, but
  `benchmarked` should cite a primary description.
