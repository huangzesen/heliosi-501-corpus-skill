---
name: paper-gieseler-2022-solar-mach-magnetic-connection
description: >-
  Use when an agent needs a quick spacecraft magnetic-connection plot
  (Parker-spiral ballistic backmapping for multiple spacecraft at a chosen
  time) — central claim is that Solar-MACH provides an open-source Python
  tool / web app that computes and visualizes magnetic connection
  configurations between spacecraft and the Sun (Gieseler et al. 2022,
  arXiv:2210.00819).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "Solar-MACH: An open-source tool to analyze solar magnetic connection configurations"
  first_author: "Gieseler, J."
  year: 2022
  venue: "arXiv preprint / Frontiers in Astronomy and Space Sciences (companion software paper)"
  doi: null
  arxiv_id: "2210.00819"
  ads_bibcode: null
domain:
  primary_theme: pfss_source_mapping
  secondary_themes: ["solar_orbiter", "psp_data", "energetic_particles"]
  missions: ["PSP", "Solar Orbiter", "Wind", "ACE", "STEREO", "MAVEN", "MESSENGER", "other"]
  regime: ["inner-heliosphere", "1au"]
trigger_keywords:
  - "solar-mach"
  - "magnetic connection"
  - "Parker spiral backmapping"
  - "ballistic mapping"
  - "spacecraft footpoint"
  - "multi-spacecraft conjunction"
  - "SEP event analysis"
  - "longitudinal separation"
data_products:
  - instrument: "Spacecraft ephemeris (any)"
    level: "derived"
    cadence: "1 day"
    interval: null
    archive: "SPICE / mission ephemerides"
  - instrument: "In-situ solar-wind speed (optional)"
    level: "L2"
    cadence: "any"
    interval: null
    archive: "CDAWeb / OMNI"
algorithms:
  - name: "Parker-spiral ballistic backmapping"
    equation_refs: ["v_sw φ_spiral = -Ω_sun (r - R_ss)"]
    external_implementations:
      - "https://github.com/sunpy/solar-mach"
      - "https://solar-mach.github.io (web app)"
  - name: "Multi-spacecraft visualization (polar projection)"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/solar-mach"
validation_target:
  claim: "Solar-MACH reproduces the Parker-spiral footpoint longitudes for a chosen multi-spacecraft conjunction at a chosen time"
  metric: "Spacecraft-by-spacecraft footpoint longitude on the source surface (degrees, Carrington)"
  tolerance: "±5 deg vs. an independent Parker-spiral calculation with the same v_sw"
  reference_figure: "Gieseler et al. 2022 Fig 1 / Fig 2 (TODO verify in full text)"
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2210.00819"
  ads_url: null
  code_repo: "https://github.com/sunpy/solar-mach"
  data_repo: null
claim_boundary:
  scope: >-
    Solar-MACH computes Parker-spiral ballistic magnetic-connection
    footpoints for a configurable list of spacecraft at a chosen time,
    using user-supplied or default solar-wind speeds. It is a *ballistic*
    mapping tool — it does not, by itself, compute a PFSS field. Multi-
    spacecraft polar visualization is the primary output.
  out_of_scope:
    - "Do not treat Solar-MACH output as a PFSS/SCS footpoint — it is purely Parker-spiral."
    - "Do not interpret a Solar-MACH footpoint as the *source region* of solar wind without coupling to a PFSS or in-situ source-mapping skill."
    - "Do not assume the default v_sw matches every event — supply mission-measured speeds for accuracy."
failure_modes:
  - "Default v_sw (often 400 km/s) is a convenience, not a physical value; using it for a fast-wind event mismaps longitudes by tens of degrees."
  - "Spacecraft ephemerides for niche missions can drift if SPICE kernels are not up to date; check kernel age."
  - "Web app and Python package can diverge in defaults; record which version produced a figure."
  - "Parker-spiral assumes radial outflow and steady B; CME events break the assumption."
  - "Longitude convention (Carrington vs Stonyhurst) is a frequent off-by-one in cross-paper comparisons."
  - "The ballistic mapping ignores latitude — connection in latitude direction is left to the user."
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/extended_search.md §7.4; sioulas-reproduction/results/github_repos/consolidated_repos.json (Solar-MACH entry)"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-paper", "infrastructure", "connectivity"]
source_type: software-paper
---

# Solar-MACH — paper-skill

> Compiled from Gieseler et al. (2022), arXiv:2210.00819, "An open-source
> tool to analyze solar magnetic connection". **Quality tier**:
> `method-ready` — workflow specified; promotion to `executable`
> requires a regression test of one published conjunction.

---

## 1. Trigger

Reach for this skill when:

- A SEP event analysis needs **footpoint longitudes** of multiple
  spacecraft (PSP, SO, STEREO-A, Wind, etc.) at the same instant.
- An agent is composing a multi-spacecraft figure for a CME-driven SEP
  paper.
- A user asks: "given v_sw = X at PSP, where on the Sun is PSP
  ballistically connected today?"

Do NOT use this skill when:

- A *PFSS* footpoint is required — use `[[paper-stansby-2020-pfsspy-python-pfss]]`
  or `[[paper-sunkit-magex-magnetic-field-extrapolation]]`.
- A *modeled* solar wind connection (WSA, HUX, EUHFORIA) is required.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Solar-MACH implements Parker-spiral ballistic
backmapping for multiple spacecraft at a user-chosen time and visualizes
the magnetic-connection configuration in a polar diagram.

**Verifiable task.** A reproduction succeeds when an agent:

1. Installs `solarmach` (PyPI).
2. Constructs a configuration with `bodies=["PSP", "Solar Orbiter",
   "STEREO-A"]` at `t=...`.
3. Generates the polar plot.
4. Reports per-spacecraft footpoint Carrington longitudes.

## 3. Methods / equations → executable workflow

### Parker-spiral ballistic backmapping

- Reference: standard Parker-spiral geometry; Solar-MACH README.
- Equation: at heliocentric radius `r`, the magnetic field line connecting
  to the spacecraft has source longitude `φ_src = φ_sc + Ω_sun (r - R_ss) /
  v_sw`.
- Procedure:
  1. Choose time `t` and reference source surface `R_ss`.
  2. For each spacecraft, query heliocentric position (sunpy/SPICE).
  3. Apply Parker-spiral mapping with chosen `v_sw`.
  4. Emit polar plot + table of footpoints.

```python
from solarmach import SolarMACH
sm = SolarMACH(
    date="2022-03-28 12:00",
    body_list=["PSP", "Solar Orbiter", "STEREO-A", "Earth"],
    vsw_list=[350, 400, 450, 400],
)
sm.plot()
df = sm.coord_table
```

### Multi-spacecraft visualization

- Polar plot with Sun at center, spacecraft at their heliocentric radii,
  Parker spirals overlaid.
- Output is a publication-ready figure for SEP-event panels.

## 4. Data / instruments → tool contracts

| Capability | Source | Fetch hint |
|---|---|---|
| Spacecraft ephemeris | SPICE kernels via `sunpy-soar` / `astropy` | bundled; refresh kernels with `solarmach.update_kernels()` if exposed |
| Solar-wind speed (optional) | user input or in-situ archive | for accurate mapping, supply mission `v_sw` |

## 5. Validation target → benchmark artifact

- **Claim**: footpoint longitudes match an independent Parker-spiral
  calc for the same `v_sw`.
- **Metric**: per-spacecraft footpoint Carrington longitude (deg).
- **Tolerance**: ±5° vs. independent calculation.
- **Reference figure**: Gieseler et al. 2022 Fig 1 / Fig 2 (TODO
  verify in full text — local source carries only the abstract).

## 6. Failure modes → skill memory

- **Default v_sw** — frequent silent error. Always supply
  mission-measured v_sw per spacecraft.
- **SPICE kernel staleness** — for missions launched recently or
  decommissioned, kernels may be missing/old.
- **Web app vs. Python divergence** — record version.
- **Longitude convention** — Carrington vs Stonyhurst; pick one and
  state it in the figure caption.
- **CME contamination** — Parker spiral assumes steady wind. SEP
  arrival during a CME breaks the mapping.
- **Latitude is ignored** — the ballistic mapping is 2D; latitude
  connection requires PFSS/SCS or external models.

## 7. Claim boundary

**In scope.** Parker-spiral ballistic magnetic connection for arbitrary
spacecraft sets at a chosen time; polar visualization.

**Out of scope — do NOT generalize beyond:**

- Not a coronal-field model.
- Not a transit-time predictor (use HUX / EUHFORIA / ENLIL).
- Does not couple to a source-mapping PFSS skill automatically; user
  must compose.

## 8. Links

- DOI: n/a (companion paper DOI not in local inventory)
- arXiv: https://arxiv.org/abs/2210.00819
- ADS: n/a
- Code: https://github.com/sunpy/solar-mach
- Data: n/a (web app at https://solar-mach.github.io)

## 9. Skill graph → depends_on

- `[[paper-sunpy-2023-interoperable-ecosystem]]` — Solar-MACH is a
  SunPy-affiliated package.
- `[[paper-stansby-2020-pfsspy-python-pfss]]` — for the *coronal*
  footpoint step that Solar-MACH does NOT perform.

## Notes

- A 2022 v_sw default of 400 km/s is convention; the failure mode is
  treating it as physics. Always parameterize.
