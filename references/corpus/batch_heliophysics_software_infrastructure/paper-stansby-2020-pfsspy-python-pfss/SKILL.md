---
name: paper-stansby-2020-pfsspy-python-pfss
description: >-
  Use when an agent needs to compute a Potential Field Source Surface (PFSS)
  extrapolation in Python from a synoptic magnetogram, classify field lines as
  open/closed, or map solar-wind source footpoints — central claim is that
  pfsspy provides an open-source Python PFSS solver with sunpy interoperability
  (pfsspy software package; companion test-problem paper Stansby et al. 2022,
  arXiv:2201.07783).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "pfsspy: A Python package for Potential Field Source Surface extrapolations (with test-problem companion: Stansby et al. 2022)"
  first_author: "Stansby, D."
  year: 2020
  venue: "JOSS / software package (companion test-problem paper: arXiv:2201.07783, 2022)"
  doi: null
  arxiv_id: "2201.07783"
  ads_bibcode: null
domain:
  primary_theme: pfss_source_mapping
  secondary_themes: ["magnetic_field", "coronal_heating"]
  missions: ["SDO", "STEREO", "Solar Orbiter", "n/a"]
  regime: ["corona"]
trigger_keywords:
  - "pfsspy"
  - "PFSS"
  - "potential field source surface"
  - "coronal field extrapolation"
  - "open/closed field line"
  - "source surface"
  - "Schatten current sheet"
  - "magnetogram"
  - "HMI synoptic"
  - "GONG synoptic"
  - "footpoint mapping"
  - "field-line tracer"
data_products:
  - instrument: "SDO/HMI synoptic magnetograms"
    level: "L1.5"
    cadence: "1 Carrington rotation"
    interval: null
    archive: "JSOC"
  - instrument: "GONG synoptic magnetograms"
    level: "synoptic"
    cadence: "1 Carrington rotation"
    interval: null
    archive: "NSO/GONG"
algorithms:
  - name: "PFSS spherical-harmonic solver"
    equation_refs: ["∇²Φ = 0 with B_r prescribed at r=R_sun and B_θ=B_φ=0 at r=R_ss"]
    external_implementations:
      - "https://github.com/sunpy/pfsspy"
  - name: "Field-line tracer (Python + Fortran backend)"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/pfsspy (pfsspy.tracing)"
  - name: "Open/closed field classification"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/pfsspy"
validation_target:
  claim: "pfsspy reproduces analytic PFSS test problems (dipole, multipole) within numerical tolerance"
  metric: "L2 norm of B_r at r=R_sun between numerical and analytic solution"
  tolerance: "convergent with nr (radial grid); paper-stated tolerance from Stansby 2022 companion (TODO verify exact value)"
  reference_figure: "Stansby et al. 2022 Fig 2 / Fig 3 (TODO verify in full text)"
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2201.07783"
  ads_url: null
  code_repo: "https://github.com/sunpy/pfsspy"
  data_repo: null
claim_boundary:
  scope: >-
    pfsspy implements a Python PFSS solver that takes a synoptic radial
    magnetogram and a chosen source-surface radius R_ss (default 2.5 R_sun)
    and returns 3D potential B-fields, supports field-line tracing, and
    interoperates with sunpy.map. The companion test-problem paper
    (arXiv:2201.07783) demonstrates the solver against analytic test cases.
  out_of_scope:
    - "Do not use pfsspy for non-potential (NLFFF/MHD) extrapolations; those need different codes."
    - "Do not assume the default R_ss=2.5 R_sun is correct for any specific event; it is a community convention."
    - "Do not extrapolate pfsspy results to predict in-situ solar-wind speed without coupling to a separate empirical model (e.g., WSA)."
    - "pfsspy is now in maintenance mode; new development happens in sunkit-magex (see paper-sunkit-magex-magnetic-field-extrapolation)."
failure_modes:
  - "Synoptic magnetogram polarity-flip near poles is poorly observed; pfsspy results in polar regions inherit that uncertainty."
  - "Low nr (radial grid) gives unphysical field-line curvature near the source surface; verify convergence with nr."
  - "Field-line tracer step size: too large misses small loops; too small explodes runtime. Default OK for diagnostic maps, not for footpoint statistics."
  - "Choice of R_ss is a hyperparameter; papers comparing models must sweep it (Asvestari et al., Badman et al., etc.)."
  - "GONG vs HMI synoptic maps differ in flux normalization; document which input was used per run."
  - "pfsspy uses a spherical-harmonic decomposition: very high-resolution magnetograms must be downsampled to avoid memory blow-up."
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: ".library/custom/heliophysics-skills/sub-skills/pfss-modeling.md and sioulas-reproduction/results/arxiv_papers/extended_search.md §2.1"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "pfss", "infrastructure"]
source_type: software-package
---

# pfsspy — paper-skill

> Compiled from the pfsspy software package (https://github.com/sunpy/pfsspy)
> and Stansby et al. (2022), "Test Problems for Potential Field Source Surface
> Extrapolations of Solar and Stellar Magnetic Fields", arXiv:2201.07783.
> **Quality tier**: `method-ready` — full workflow procedure documented;
> promotion to `executable` requires running the end-to-end §3 pipeline on a
> cached HMI synoptic map.

---

## 1. Trigger

Reach for this skill when:

- A workflow needs to **extrapolate a coronal magnetic field** from a
  synoptic photospheric magnetogram to a source surface.
- An agent needs to **classify open vs. closed field lines** for solar-wind
  source mapping.
- A switchback / streamer / coronal-hole analysis needs **footpoint
  mapping** from 1 au (or PSP/SO) back to the photosphere.
- A reasoning agent must choose between `pfsspy` and `sunkit-magex` — this
  skill describes pfsspy and points to the maintenance successor.

Do NOT use this skill when:

- The required model is NLFFF (non-linear force-free) — pfsspy is
  *potential-field only*.
- The task is a full MHD simulation of the corona (use AWSoM/MAS/etc., not
  pfsspy).

## 2. Paper claim → verifiable task

**Claim (narrow form).** pfsspy implements a spherical-harmonic PFSS solver
with field-line tracing and open/closed classification in Python, and the
companion 2022 test-problem paper demonstrates it converges to analytic
solutions (dipole, low-order multipoles) under controlled inputs.

**Verifiable task.** A reproduction succeeds when an agent:

1. Loads a known HMI / GONG synoptic radial magnetogram.
2. Runs `pfsspy.pfss` with `nr=60`, `R_ss=2.5 R_sun`.
3. Confirms `B_r` at `r=R_sun` matches the input within numerical
   tolerance.
4. Traces ≥10 field lines and classifies each as open/closed.

## 3. Methods / equations → executable workflow

### PFSS spherical-harmonic solver

- Reference: Stansby 2022 §2; pfsspy docs.
- Equation: `∇²Φ = 0` with `B = -∇Φ`; boundary conditions `B_r(R_sun) =
  observed`, `B_θ(R_ss) = B_φ(R_ss) = 0`.
- Procedure:
  1. Load synoptic magnetogram as `sunpy.map.Map`.
  2. `pfsspy.Input(map, nr=nr, rss=R_ss)`.
  3. `output = pfsspy.pfss(input)`.
  4. Inspect `output.bg` (3D B-field on grid).

```python
import pfsspy
import sunpy.map
mag = sunpy.map.Map("hmi.synoptic_mr_720s.NNNN.fits")
inp = pfsspy.Input(mag, nr=60, rss=2.5)
out = pfsspy.pfss(inp)
br = out.bg[..., 0]
```

### Field-line tracer

- Reference: pfsspy `pfsspy.tracing` module.
- Procedure:
  1. Choose seed points on a 2D `SkyCoord` grid at `r=R_sun` (or `r=R_ss`
     for backwards tracing).
  2. `tracer = pfsspy.tracing.FortranTracer()`.
  3. `flines = tracer.trace(seeds, out)`.
  4. Classify with `flines.connectivities` or by checking `ss_distance`.

### Open/closed classification

- A field line is **open** if it terminates on the source surface;
  **closed** if both ends are on the photosphere.
- Cache per-pixel classification as a polarity map for downstream
  source-mapping workflows.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| SDO/HMI synoptic radial magnetogram | L1.5 | 1 Carrington rotation | any CR | JSOC | `sunpy.net.Fido` → JSOC, series `hmi.synoptic_mr_720s` (general-purpose: WebFetch + `drms`) |
| GONG synoptic radial magnetogram | synoptic | 1 CR | any CR | NSO/GONG | `Fido` → GONG client; or direct HTTP from `nso.edu/data/nisp-synoptic-data/` |
| ADAPT ensemble synoptic maps | derived | 1 CR | any CR | NSO/GONG | not in default sunpy clients; fetch via HTTP listing |

The named `mcp:jsoc` or `mcp:gong` are *not assumed*; baseline is
`Fido` + Bash/WebFetch.

## 5. Validation target → benchmark artifact

- **Claim**: pfsspy reproduces analytic dipole/multipole PFSS solutions
  within tolerance.
- **Metric**: L2 norm of `B_r(R_sun)` between numerical and analytic
  fields; or mean angular error between analytic and computed open-field
  footpoint locations.
- **Tolerance**: TODO verify numeric tolerance from Stansby 2022 full
  text (local inventory carries only the abstract snippet).
- **Reference figure**: Stansby et al. 2022 Fig 2 / Fig 3 (TODO verify
  with full text).

## 6. Failure modes → skill memory

- **Polar magnetogram uncertainty** — HMI poles are observed at extreme
  viewing angle. Polar field strength is *inferred*, not measured. PFSS
  open-flux estimates inherit this systematic.
- **R_ss is a free parameter** — community default 2.5 R_sun is convention,
  not physics. Sweep R_ss for any open-flux argument.
- **Convergence with nr** — too coarse a radial grid distorts the
  source-surface field. Always test `nr ∈ {30, 60, 120}` for robustness.
- **High-l harmonics blow up** — full-resolution HMI synoptic (3600×1440)
  must be downsampled to ~360×180 for tractable solves.
- **Tracer step size** — Python tracer is slow; FortranTracer is faster;
  step size affects loop-length statistics.
- **pfsspy is maintenance-mode** — new features live in
  `sunkit-magex`. Use pfsspy for reproducibility; sunkit-magex for new
  work.
- **Open-flux problem** — even when pfsspy converges, total open flux is
  systematically smaller than in-situ measurements (the "open flux
  problem"). Do not use pfsspy alone to predict heliospheric open flux
  amplitude.

## 7. Claim boundary

**In scope.** Potential-field extrapolation from a synoptic radial
magnetogram with chosen source-surface radius; field-line tracing;
open/closed classification; sunpy.map interoperability.

**Out of scope — do NOT generalize beyond:**

- Do not use pfsspy to claim non-potential coronal structure (filaments,
  active-region twist, free magnetic energy).
- Do not predict total heliospheric open flux from pfsspy alone without
  acknowledging the open-flux problem.
- Do not use the default R_ss=2.5 R_sun without justification for
  individual events.
- Do not use pfsspy for stellar PFSS without verifying the test-problem
  scope covers your stellar regime.

## 8. Links

- DOI: n/a (software package; companion paper DOI not in local
  inventory)
- arXiv: https://arxiv.org/abs/2201.07783 (companion test-problem paper)
- ADS: n/a
- Code: https://github.com/sunpy/pfsspy
- Data: n/a (uses external HMI / GONG magnetograms)

## 9. Skill graph → depends_on

- `[[paper-sunpy-2023-interoperable-ecosystem]]` — pfsspy is an
  affiliated package; SunPy maps are its input contract.
- `[[paper-sunkit-magex-magnetic-field-extrapolation]]` — successor
  package; new work should resolve there first.
- `[[paper-gieseler-2022-solar-mach-magnetic-connection]]` — common
  downstream consumer of pfsspy field-line traces for
  spacecraft-magnetic-connection visualization.

## Notes

- The "open flux problem" is a recurring failure mode worth its own
  paper-skill once a paper-anchor is selected.
- Local source `.library/custom/heliophysics-skills/sub-skills/pfss-modeling.md`
  contains a runnable pfsspy code snippet that should be lifted into a
  `scripts/` artifact at `executable` promotion.
