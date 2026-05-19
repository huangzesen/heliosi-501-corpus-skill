---
name: paper-cdaweb-heliophysics-archive
description: >-
  Use when an agent needs to discover, query, or fetch heliophysics in-situ
  data from NASA's primary archive — central claim is that CDAWeb /
  SPDF provides authoritative access to PSP, Wind, ACE, STEREO, SOHO, SDO,
  THEMIS, and MMS data products via Web API, IDL, and Python clients
  (NASA SPDF infrastructure; data archive — no software publication).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "CDAWeb (Coordinated Data Analysis Web) / SPDF — NASA heliophysics data archive"
  first_author: "NASA SPDF team"
  year: 1996
  venue: "NASA data archive (no software publication; cite as a service)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["data_access_infrastructure", "psp_data", "solar_orbiter"]
  missions: ["PSP", "Solar Orbiter", "Wind", "ACE", "STEREO", "SOHO", "SDO", "THEMIS", "MAVEN", "MESSENGER", "Voyager", "Ulysses", "other"]
  regime: ["1au", "inner-heliosphere", "outer-heliosphere"]
trigger_keywords:
  - "CDAWeb"
  - "SPDF"
  - "NASA heliophysics archive"
  - "cdas API"
  - "ws/cdas/AvailableData"
  - "data discovery"
  - "L2 in-situ data"
  - "PSP archive"
  - "Wind archive"
  - "ACE archive"
  - "OMNI"
  - "HAPI server"
data_products:
  - instrument: "PSP/FIELDS MAG"
    level: "L2"
    cadence: "4 Sa/cyc to 293 Hz"
    interval: "PSP mission to date"
    archive: "CDAWeb / SPDF (also PSP SOC)"
  - instrument: "Wind/MFI, Wind/SWE"
    level: "L2"
    cadence: "varies"
    interval: "1994-present"
    archive: "CDAWeb / SPDF"
  - instrument: "ACE/MAG, ACE/SWEPAM, ACE/SWICS"
    level: "L2"
    cadence: "varies"
    interval: "1997-present"
    archive: "CDAWeb / SPDF"
  - instrument: "OMNI (1-min / 1-hour solar wind merged)"
    level: "derived"
    cadence: "1 min / 1 hr"
    interval: "1963-present"
    archive: "OMNIWeb / SPDF"
algorithms:
  - name: "CDAWeb Web Services (cdas API)"
    equation_refs: []
    external_implementations:
      - "https://cdaweb.gsfc.nasa.gov/WS/cdas"
  - name: "HAPI server query"
    equation_refs: []
    external_implementations:
      - "https://hapi-server.org/"
      - "https://github.com/hapi-server/client-python"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov"
claim_boundary:
  scope: >-
    CDAWeb is NASA SPDF's primary heliophysics data archive, providing
    discovery, query, and CDF download for L2 in-situ data from PSP,
    Wind, ACE, STEREO, SOHO, SDO, THEMIS, MMS, MAVEN, MESSENGER, Voyager,
    Ulysses, and others. Access surfaces: Web UI, HTTP cdas API, HAPI
    server, IDL/Python clients (sunpy.net.cdaweb, pyspedas, cdasws).
  out_of_scope:
    - "Do not assume CDAWeb hosts every level of every product; mission SOCs (PSP SOC, SOAR for Solar Orbiter) may carry products CDAWeb does not."
    - "Do not treat CDAWeb as a calibration authority; calibration is mission-team responsibility."
    - "Do not assume CDAWeb URLs are stable across decades; periodically verify (the cdaweb.gsfc.nasa.gov domain has been stable for years but underlying paths change)."
failure_modes:
  - "Large queries (months of high-cadence data) get rate-limited or chunked; respect quotas."
  - "Mirror / load-balancer DNS issues can produce intermittent 5xx; retry with backoff."
  - "Dataset-ID naming convention differs subtly across mission (e.g., `PSP_FLD_L2_MAG_RTN` vs `PSP_FLD_L2_MAG_RTN_4_SA_PER_CYC`); use AvailableData endpoint to enumerate."
  - "Variable names within a dataset can change across versions; pin a version or check `cdf_info()`."
  - "CDAWeb returns CDFs; an agent without cdflib/PyCDF cannot read them."
  - "Solar Orbiter products on CDAWeb may lag behind SOAR; prefer SOAR for SO."
depends_on:
  - paper-cdflib-cdf-reader
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: ".library/custom/heliophysics-skills/reference/databases.md (CDAWeb / SPDF / OMNI / COHOWeb / PSP SOC entries)"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "data-archive", "infrastructure"]
source_type: software-package
---

# CDAWeb / SPDF data archive — paper-skill

> Compiled from `.library/custom/heliophysics-skills/reference/databases.md`
> (CDAWeb / SPDF / OMNI / PSP SOC entries) and
> `.library/custom/heliophysics-skills/SKILL.md` (databases table).
> **Quality tier**: `method-ready` — workflow specified; promotion to
> `executable` requires running a parameterized cdas query and
> verifying the returned CDF.

This skill treats CDAWeb / SPDF as **infrastructure** (a data archive),
not as a paper. It is the *root data-access* skill: most other in-situ
paper-skills resolve through it.

---

## 1. Trigger

Reach for this skill when:

- An agent needs to **discover** what dataset / variable is available for
  a chosen mission / interval.
- A workflow needs to **download** PSP / Wind / ACE / STEREO / OMNI data.
- A reasoning agent is choosing between CDAWeb (multi-mission, generic)
  and a mission-specific SOC (PSP SOC, SOAR).
- A pipeline needs **HAPI-server access** for streaming time-series data.

Do NOT use this skill when:

- The data is solar imaging — use VSO / JSOC via
  `[[paper-sunpy-2023-interoperable-ecosystem]]`.
- The data is Solar Orbiter L2 — prefer SOAR (faster, more complete).

## 2. Paper claim → verifiable task

**Claim (narrow form).** CDAWeb / SPDF hosts authoritative L2
in-situ heliophysics data with Web API, HAPI server, and Python/IDL
clients.

**Verifiable task.** A reproduction succeeds when an agent:

1. Queries `AvailableData` for a chosen dataset ID and interval.
2. Downloads a CDF.
3. Opens the CDF with cdflib and confirms variable names match the
   AvailableData metadata.

## 3. Methods / equations → executable workflow

### CDAWeb Web Services (cdas API)

- Reference: https://cdaweb.gsfc.nasa.gov/WS/cdas
- Procedure:

```python
import requests
url = "https://cdaweb.gsfc.nasa.gov/WS/cdas/1/dataviews/sp_phys/datasets"
r = requests.get(url, params={"observatory": "PSP"})
datasets = r.json()
```

For data download:

```python
# Use sunpy.net.cdaweb, pyspedas, or direct HTTP from
# https://cdaweb.gsfc.nasa.gov/sp_phys/data/<mission>/<instrument>/...
```

### HAPI server query

- Reference: https://hapi-server.org/, https://github.com/hapi-server/client-python.
- Procedure:

```python
from hapiclient import hapi
server = "https://cdaweb.gsfc.nasa.gov/hapi"
data, meta = hapi(server, "PSP_FLD_L2_MAG_RTN", "psp_fld_l2_mag_RTN",
                  "2021-04-29T00:00:00", "2021-04-29T06:00:00")
```

### Choosing between clients

| Client | When to use |
|---|---|
| Web UI | exploratory discovery |
| cdas API (HTTP/JSON) | scripted listing |
| HAPI | streaming long intervals |
| `sunpy.net.cdaweb` | inside Fido pipeline |
| `pyspedas` | multi-mission convenience + tplot |
| `cdasws` (python) | low-level scripted downloads |

## 4. Data / instruments → tool contracts

| Mission | Examples of L2 datasets | Notes |
|---|---|---|
| PSP | `PSP_FLD_L2_MAG_RTN`, `PSP_SWP_SPI_SF00_L3_MOM`, `PSP_ISOIS-EPILO_L2-PE` | High-cadence MAG variants exist |
| Wind | `WI_H0_MFI`, `WI_K0_SWE`, `WI_PM_3DP` | 1994-present continuous |
| ACE | `AC_H0_MFI`, `AC_H1_SWE`, `AC_H6_SWI` | 1997-present continuous |
| STEREO | `STA_L1_MAG_RTN`, `STA_L2_PLA_1DMAX` | Two-spacecraft set |
| SOHO | `SOHO_CELIAS-SEM`, `SOHO_COSTEP-EPHIN_L2-1MIN` | EPHIN energetic particles |
| OMNI | `OMNI_HRO_1MIN`, `OMNI2_H0_MRG1HR` | merged 1-min / 1-hr at 1 au |

The general-purpose harness (Bash + Python + cdflib + WebFetch) is the
guaranteed surface. A `mcp:cdaweb` is **not** assumed.

## 5. Validation target → benchmark artifact

> Not benchmarked yet — `method-ready`. Promotion to `executable`
> requires:
> - Parameterized `AvailableData` query producing the expected dataset
>   list.
> - Round-trip download + cdflib open + variable enumeration matching
>   the metadata.

## 6. Failure modes → skill memory

- **Rate limits** — large queries get throttled; chunk by day or use
  HAPI for long intervals.
- **Dataset ID typos** — silent empty response. Use AvailableData
  endpoint to verify ID first.
- **Variable name drift across versions** — same dataset ID may carry
  different variables across instrument revisions; pin or inspect.
- **Mirror flakiness** — retry with exponential backoff.
- **CDF-vs-IDL-vs-Python conventions** — IDL SPEDAS expects certain
  attribute conventions; Python may not enforce them.
- **Solar Orbiter lag on CDAWeb** — prefer SOAR for the latest SO data.

## 7. Claim boundary

**In scope.** Data discovery, query, download for in-situ heliophysics
missions via CDAWeb / SPDF endpoints.

**Out of scope — do NOT generalize beyond:**

- Not a solar-imaging archive (VSO/JSOC are separate).
- Not a calibration authority.
- Not a science result.

## 8. Links

- DOI: n/a (data archive)
- arXiv: n/a
- ADS: n/a
- Code: n/a (multiple clients listed above)
- Data: https://cdaweb.gsfc.nasa.gov

## 9. Skill graph → depends_on

- `[[paper-cdflib-cdf-reader]]` — needed to open any downloaded CDF.
- `[[paper-pyspedas-multimission-data-access]]` — high-level Python
  client; resolves through CDAWeb under the hood.

## Notes

- This is an **infrastructure-only** skill; the source is the
  `.library/custom/heliophysics-skills/reference/databases.md` table,
  not a publication. The skill exists so that every in-situ paper-skill
  has a canonical root to point to for data access.
- HAPI is the modern streaming alternative; promote when an agent needs
  to scan long intervals without local CDF storage.
