---
name: paper-sunkit-magex-magnetic-field-extrapolation
description: >-
  Use when an agent needs a maintained Python implementation of coronal
  magnetic-field extrapolation (PFSS + Schatten current sheet + future
  NLFFF) for new work — central claim is that sunkit-magex is the successor
  to pfsspy with an extensible extrapolation API (sunpy-affiliated software
  package, ~2023+).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "sunkit-magex: SunPy-affiliated magnetic-field extrapolation package"
  first_author: "sunkit-magex contributors"
  authors_verified: false
  year: 2023
  venue: "sunpy-affiliated software package (no standalone publication in local inventory)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: pfss_source_mapping
  secondary_themes: ["magnetic_field"]
  missions: ["SDO", "STEREO", "Solar Orbiter", "n/a"]
  regime: ["corona"]
trigger_keywords:
  - "sunkit-magex"
  - "magnetic field extrapolation"
  - "PFSS Python successor"
  - "Schatten current sheet"
  - "SCS"
  - "pfsspy migration"
  - "sunpy affiliated package"
  - "coronal field"
data_products:
  - instrument: "SDO/HMI synoptic radial magnetogram"
    level: "L1.5"
    cadence: "1 Carrington rotation"
    interval: null
    archive: "JSOC"
  - instrument: "GONG synoptic radial magnetogram"
    level: "synoptic"
    cadence: "1 Carrington rotation"
    interval: null
    archive: "NSO/GONG"
algorithms:
  - name: "PFSS spherical-harmonic solver (sunkit-magex.pfss)"
    equation_refs: ["∇²Φ = 0 with source-surface BC"]
    external_implementations:
      - "https://github.com/sunpy/sunkit-magex"
  - name: "Schatten Current Sheet (SCS) extension"
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunkit-magex"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/sunpy/sunkit-magex"
  data_repo: null
claim_boundary:
  scope: >-
    sunkit-magex is a SunPy-affiliated Python package providing potential-field
    (PFSS) and Schatten current sheet (SCS) extrapolations from synoptic
    radial magnetograms, designed as a maintenance-mode successor to pfsspy
    with an API for additional extrapolation methods.
  out_of_scope:
    - "Do not assume sunkit-magex provides NLFFF extrapolation today; current API focuses on PFSS + SCS."
    - "Do not migrate scientific results blindly from pfsspy to sunkit-magex without re-validating against the same test problems; numerical solvers differ in detail."
    - "Do not treat sunkit-magex as a science citation; it is infrastructure."
failure_modes:
  - "API differences from pfsspy break direct drop-in replacement; field accessors and tracer entry points have moved."
  - "SCS extension requires choosing a current-sheet radius R_cs > R_ss; default may not match a given paper's choice — always document."
  - "Same magnetogram-resolution / nr-convergence considerations as pfsspy apply."
  - "Affiliated-package status depends on the SunPy ecosystem contract; verify sunpy compatibility per release."
  - "If pfsspy and sunkit-magex give different numbers on the same input, the discrepancy is the news — record and reconcile, do not silently pick one."
depends_on:
  - paper-stansby-2020-pfsspy-python-pfss
  - paper-sunpy-2023-interoperable-ecosystem
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: ".library/custom/heliophysics-skills/sub-skills/pfss-modeling.md (sunkit_magex example) and .library/custom/heliophysics-skills/sub-skills/github-repos.md"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "pfss", "infrastructure"]
source_type: software-package
---

# sunkit-magex — paper-skill

> Compiled from the sunkit-magex software package
> (https://github.com/sunpy/sunkit-magex) and local references
> in `.library/custom/heliophysics-skills/sub-skills/pfss-modeling.md`.
> **Quality tier**: `method-ready` — workflow specified; promotion to
> `executable` needs an end-to-end SCS run on a cached magnetogram.

This skill exists because the **infrastructure successor** to pfsspy must
be a first-class node in the skill graph; PFSS work begun in 2024+ should
default here, with pfsspy retained for reproducibility of older results.

---

## 1. Trigger

Reach for this skill when:

- A new (post-2024) workflow needs to compute PFSS or SCS extrapolation
  and the agent must choose between pfsspy and sunkit-magex.
- A migration is required: an existing pfsspy pipeline must be moved to
  the maintained successor.
- A workflow needs the **SCS extension** (Schatten current sheet) beyond
  pure PFSS — pfsspy's coverage of SCS is partial; sunkit-magex centralizes
  it.

Do NOT use this skill when:

- Reproducing a *published* pfsspy result — use `[[paper-stansby-2020-pfsspy-python-pfss]]`
  to preserve numerical traceability.
- Doing NLFFF or full MHD; not in scope.

## 2. Paper claim → verifiable task

**Claim (narrow form).** sunkit-magex provides PFSS + SCS extrapolation
in Python on synoptic radial magnetograms, with an extensible extrapolation
API and active maintenance under the SunPy affiliated-package contract.

**Verifiable task.** A reproduction succeeds when an agent can:

1. Install sunkit-magex.
2. Run PFSS on a known synoptic map and confirm `B_r(R_sun)` matches input.
3. Run SCS extension with chosen `R_cs > R_ss` and confirm the field
   inside `[R_ss, R_cs]` matches the Schatten construction.

## 3. Methods / equations → executable workflow

### PFSS via sunkit-magex

- Reference: sunkit-magex docs.
- Procedure (analogous to pfsspy but with new API entry points):

```python
import sunkit_magex.pfss as pfss
import sunpy.map
mag = sunpy.map.Map("hmi.synoptic_mr_720s.NNNN.fits")
inp = pfss.Input(mag, nr=60, rss=2.5)
out = pfss.pfss(inp)
```

### Schatten Current Sheet extension

- Reference: Schatten 1971; sunkit-magex SCS module.
- Procedure:
  1. Compute PFSS solution to `R_ss`.
  2. Extend with Schatten construction to `R_cs` (e.g., 3.25 R_sun).
  3. Use combined field for footpoint mapping beyond the source surface.

```python
# Conceptual; verify exact API in the installed version
scs = sunkit_magex.scs(mag, nr=60, rss=2.5, css=3.25)
```

## 4. Data / instruments → tool contracts

Same as `[[paper-stansby-2020-pfsspy-python-pfss]]`. Inputs:

| Instrument | Level | Cadence | Archive | Fetch hint |
|---|---|---|---|---|
| SDO/HMI synoptic | L1.5 | 1 CR | JSOC | `sunpy.net.Fido` |
| GONG synoptic | synoptic | 1 CR | NSO/GONG | `Fido` |

## 5. Validation target → benchmark artifact

> Not benchmarked yet — `method-ready` tier. Promotion to `executable`
> requires:
> - Running PFSS + SCS on a chosen CR.
> - Producing a side-by-side comparison with pfsspy on the same CR.
> - Emitting `metrics.json` with `{max_dB_per_pixel, mean_dB_per_pixel}`
>   between pfsspy and sunkit-magex.

## 6. Failure modes → skill memory

- **API drift from pfsspy** — entry points have moved; do not assume a
  drop-in import rename works.
- **R_cs convention** — papers differ on Schatten current-sheet radius;
  document explicitly per run.
- **Same magnetogram-systematics** as pfsspy: polar uncertainty,
  resolution convergence, R_ss sweep.
- **Side-by-side pfsspy/sunkit-magex differences** — if the two disagree,
  the difference is itself a science observation. Record, do not silently
  pick.
- **Affiliated-package version skew** — sunkit-magex pins specific sunpy
  versions; lock environments.

## 7. Claim boundary

**In scope.** PFSS + SCS on synoptic radial magnetograms in Python,
maintained successor to pfsspy.

**Out of scope — do NOT generalize beyond:**

- No NLFFF claims.
- No assertion that sunkit-magex results are numerically identical to
  pfsspy on the same input; record any discrepancy.
- No claim about open-flux problem resolution.

## 8. Links

- DOI: n/a (no standalone publication in local inventory)
- arXiv: n/a
- ADS: n/a
- Code: https://github.com/sunpy/sunkit-magex
- Data: n/a

## 9. Skill graph → depends_on

- `[[paper-stansby-2020-pfsspy-python-pfss]]` — predecessor; carries the
  test-problem validation history.
- `[[paper-sunpy-2023-interoperable-ecosystem]]` — sunkit-magex is an
  affiliated package and inherits the SunPy interop contract.

## Notes

- This skill is intentionally `method-ready`, not `executable`: a runnable
  benchmark requires a cached synoptic magnetogram, which is downloaded
  on demand, not committed.
- No companion publication for sunkit-magex was found in the local
  inventory (extended_search.md, github_repos/). Flag as a TODO: locate
  a JOSS or methods paper before promoting beyond `method-ready`.
