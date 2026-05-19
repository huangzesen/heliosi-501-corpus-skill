---
name: paper-sunpy-2023-interoperable-ecosystem
description: >-
  Use when a heliophysics workflow needs the canonical Python entry point for
  loading solar maps, querying VSO/JSOC/HEK, doing coordinate transforms, or
  reading FITS-based solar data — central paper claim is that SunPy is an
  interoperable ecosystem of Python packages providing a stable core (sunpy
  core) plus affiliated packages for solar data analysis (The SunPy Project,
  arXiv:2304.09794, 2023).
version: 0.1.0
kind: paper-skill
quality: stub
paper:
  title: "The SunPy Project: An Interoperable Ecosystem for Solar Data Analysis"
  first_author: "The SunPy Community"
  year: 2023
  venue: "arXiv preprint (software/ecosystem paper)"
  doi: null
  arxiv_id: "2304.09794"
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["solar_imaging", "data_access_infrastructure", "open_source_ecosystem"]
  missions: ["SDO", "STEREO", "Solar Orbiter", "PSP", "other"]
  regime: ["corona", "1au", "inner-heliosphere"]
trigger_keywords:
  - "sunpy"
  - "sunpy.map"
  - "Fido"
  - "VSO"
  - "HEK"
  - "JSOC client"
  - "solar coordinate transforms"
  - "Helioprojective"
  - "Heliographic Stonyhurst"
  - "FITS solar data"
  - "AIA"
  - "HMI"
  - "EUI"
  - "affiliated packages"
data_products: []
algorithms:
  - name: "Fido unified data search"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunpy (sunpy.net.Fido)"
  - name: "sunpy.map.Map FITS map model"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunpy (sunpy.map)"
  - name: "Astropy-based solar coordinate frames"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunpy (sunpy.coordinates)"
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2304.09794"
  ads_url: null
  code_repo: "https://github.com/sunpy/sunpy"
  data_repo: null
claim_boundary:
  scope: >-
    The paper describes the SunPy Project — `sunpy` core plus affiliated
    packages (e.g., `aiapy`, `sunkit-image`, `sunkit-instruments`, `pfsspy`,
    `solar-mach`) — as an interoperable Python ecosystem for solar physics
    that supports data search (Fido), solar coordinate handling, FITS map
    objects, and common image-processing primitives. Claims are scoped to
    the ecosystem's design and interoperability surface as of the 2023
    paper, not to any specific numerical result.
  out_of_scope:
    - "Do not treat this skill as authoritative for any heliophysics scientific claim — it provides infrastructure, not findings."
    - "Do not assume any specific affiliated package is installed by default; only `sunpy` core is guaranteed by `pip install sunpy`."
    - "Do not assume API stability across major sunpy versions; check installed `sunpy.__version__` before relying on behavior."
failure_modes:
  - "Mixing astropy coordinate frames with sunpy frames without an explicit `obstime` raises silent transform errors at runtime."
  - "Fido attribute combinations that are not supported by a given client (e.g., asking JSOC for non-HMI/AIA data) return empty results without warning."
  - "`sunpy.map.Map` mis-detects instrument when FITS headers are non-standard (custom pipelines); set `instrument=` explicitly."
  - "Affiliated packages have independent release cycles and may pin incompatible sunpy versions; lock environments per project."
depends_on: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/extended_search.md §7.6"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-paper", "infrastructure"]
source_type: software-paper
---

# SunPy 2023 Project ecosystem — paper-skill

> Compiled from The SunPy Community (2023), "The SunPy Project: An Interoperable
> Ecosystem for Solar Data Analysis", arXiv:2304.09794.
> **Quality tier**: `stub` — promotion to `method-ready` requires a runnable
> Fido + Map round-trip workflow.

This file is the *agent-native compiled form* of the SunPy 2023 ecosystem
paper, not a summary. SunPy is treated here as **infrastructure**: an agent
should load this skill when it needs to *fetch and represent* solar data, not
when it needs to *interpret* it.

---

## 1. Trigger

A future agent should reach for this skill when:

- It needs to fetch SDO/AIA, SDO/HMI, STEREO/SECCHI, or Solar Orbiter/EUI
  data and does not yet have a download path.
- It needs to load a FITS file and treat it as a solar map with WCS-aware
  coordinates.
- It needs to convert between solar coordinate frames (Helioprojective,
  Heliographic Stonyhurst, Heliographic Carrington, Heliocentric, HCRS).
- It is deciding between SunPy and a domain-specific reader (e.g., `aiapy`
  for AIA-specific calibration); this skill defines the boundary.
- It needs to identify which affiliated package owns a given functionality
  (PFSS → `pfsspy`/`sunkit-magex`; image processing → `sunkit-image`).

Do NOT use this skill when:

- The task is in-situ time-series analysis (use `paper-pyspedas-multimission-data-access`
  or `paper-cdflib-cdf-reader` instead).
- The task is plasma kinetic-dispersion analysis (use ALPS/PLUME skills).

## 2. Paper claim → verifiable task

**Claim (narrow form).** SunPy provides (i) a stable core package
(`sunpy`) implementing solar coordinates, FITS map objects, and a unified
data-search interface (`Fido`), and (ii) a constellation of affiliated
packages with a documented interoperability contract. The 2023 paper claims
this ecosystem is *the* community-adopted Python entry point for solar
data analysis.

**Verifiable task.** A reproduction succeeds when an agent can:

1. Call `Fido.search(...)` for a named AIA wavelength + interval and
   retrieve at least one file.
2. Load that file with `sunpy.map.Map` and confirm the resulting object
   has a valid `wcs` and `observer_coordinate`.
3. Transform a Helioprojective coordinate to Heliographic Stonyhurst
   without losing the `obstime`.

This is an *interoperability* check, not a science claim.

## 3. Methods / equations → executable workflow

### Fido unified data search

- Reference: SunPy Project 2023 §"Data search and download".
- Implementation: `sunpy.net.Fido` in https://github.com/sunpy/sunpy.
- Procedure:
  1. Compose attribute query: `a.Time(t0, t1) & a.Instrument.aia & a.Wavelength(171*u.angstrom)`.
  2. Call `Fido.search(query)`; inspect returned `UnifiedResponse`.
  3. `Fido.fetch(result, path="...")` to download.
  4. Verify file paths and report missing intervals.

```python
import astropy.units as u
from sunpy.net import Fido, attrs as a

q = a.Time("2022-03-28", "2022-03-28T00:10") & a.Instrument.aia & a.Wavelength(171*u.angstrom)
res = Fido.search(q)
files = Fido.fetch(res, path="./data/{instrument}/{file}")
```

### sunpy.map.Map FITS map model

- Reference: SunPy Project 2023 §"Map".
- Procedure:
  1. `m = sunpy.map.Map(path)`.
  2. Inspect `m.observer_coordinate`, `m.coordinate_frame`, `m.wcs`.
  3. Re-project to another observer with `m.reproject_to(out_wcs)` (uses
     `reproject` affiliated package).

### Astropy-based solar coordinate frames

- Reference: SunPy Project 2023 §"Coordinates".
- Frames: `Helioprojective`, `HeliographicStonyhurst`, `HeliographicCarrington`,
  `Heliocentric`, `HCRS`.
- Procedure:
  1. Always set `obstime` explicitly when constructing a `SkyCoord`.
  2. Use `.transform_to(frame)` for conversions; verify `obstime` is
     preserved after the transform.

## 4. Data / instruments → tool contracts

| Capability | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| AIA EUV images | L1 | 12 s / 24 s | any | JSOC | `Fido` → JSOC client (login optional for public series) |
| HMI magnetograms | L1/L1.5 | 720 s / 45 s | any | JSOC | `Fido` → JSOC client; large series should use `drms` directly |
| STEREO/SECCHI | L0.5 | variable | any | VSO / SSC | `Fido` → VSO client |
| Solar Orbiter EUI | L2 | variable | mission | SOAR | `Fido` → SOAR client (affiliated package: `sunpy-soar`) |
| HEK event lists | n/a | n/a | any | HEK | `Fido` → HEK client |

The general-purpose harness (Read, Bash, WebFetch + `pip install sunpy`) is
the only guaranteed surface. A named `mcp:sunpy` does **not** exist by
contract; if a future runtime exposes one, this skill binds to it.

## 5. Validation target → benchmark artifact

> Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
> requires running the §3 Fido search + Map load + coordinate transform on
> a cached AIA interval and emitting `metrics.json` with
> `{n_files_fetched, map_obstime, transform_ok: bool}`.

## 6. Failure modes → skill memory

- **Missing obstime in `SkyCoord`** — transforms silently produce wrong
  output when `obstime` is None. Always pass `obstime=...`.
- **Empty Fido response** — client-attribute mismatches return zero rows
  with no exception. Always assert `len(res)` before fetch.
- **JSOC export quotas** — large AIA series queries get throttled; chunk
  by ≤ 1-hour windows or use `drms` directly.
- **Affiliated-package version skew** — `pfsspy`/`sunkit-magex`/`aiapy`
  pin different sunpy ranges. Pin per project in `pyproject.toml`.
- **FITS header non-compliance** — custom pipelines often miss
  `T_OBS`/`DATE-OBS`; `Map` then defaults to UTC now or fails. Pass
  `instrument=` and explicit metadata.

## 7. Claim boundary

**In scope.** Infrastructure: data search, FITS map representation,
coordinate frames, the affiliated-package ecosystem contract.

**Out of scope — do NOT generalize beyond:**

- Numerical results from sunpy code paths are *not* validated by this
  skill; defer to instrument-specific calibration skills.
- Do not treat sunpy as a substitute for `pyspedas` / `cdflib` for in-situ
  data: it has limited CDF support and is image-centric.
- Do not infer that a given affiliated package is up-to-date; check its
  own SKILL.md or release notes.

If a downstream task asks for "what cascade rate did SunPy compute?"
refuse it — SunPy does not produce science claims; it is plumbing.

## 8. Links

- DOI: n/a (preprint-only ecosystem paper)
- arXiv: https://arxiv.org/abs/2304.09794
- ADS: n/a (not separately verified in local inventory)
- Code: https://github.com/sunpy/sunpy
- Data: n/a (SunPy is a client; archives are external)

## 9. Skill graph → depends_on

- `[[paper-sunpy-2015-python-solar-physics]]` — historical anchor; the
  2023 paper extends the 2015 ecosystem description.
- `[[paper-stansby-2020-pfsspy-python-pfss]]` — affiliated package; the
  SunPy ecosystem entry point for PFSS computations.
- `[[paper-sunkit-magex-magnetic-field-extrapolation]]` — affiliated
  package; PFSS / extrapolation successor.
- `[[paper-gieseler-2022-solar-mach-magnetic-connection]]` — affiliated
  package; magnetic-connection analysis.

## Notes

- The 2023 paper formalizes the "affiliated package" contract; before this
  paper, the boundary was implicit. Use this contract to decide which
  package owns a given capability before writing a new skill.
- This skill is the *common dependency* for many solar-imaging paper-skills;
  budget for it when bundling.
