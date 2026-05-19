---
name: paper-coronal-hole-jet-population-statistics-aia
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-coronal-hole-jet-population-statistics-aia

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when compiling **AIA-era coronal-hole jet
catalogs** and deriving their statistical properties (height, width,
lifetime, recurrence) for solar-wind / SEP source studies.

## Layer 1 — Scientific invariant

- **Paper identity:** AIA Coronal-Hole Jet Population Statistics
  (representative: Savcheva+ 2007; Pucci+ 2013; Mulay+ 2016).
- **Year:** TODO verify.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

The CH jet population observed by AIA has heights `~10^4–10^5 km`,
widths `~10^3–10^4 km`, lifetimes `~5–30 min`, with a recurrence rate
of order one per hour at any latitude in a polar CH. The narrow claim
is the **log-normal nature of the size distributions and the recurrence
correlation with photospheric mixed-polarity flux**.

### Method assumptions

- High-cadence AIA 193 Å and 211 Å imagery.
- Automated or semi-automated detection.
- Boundary against quiet-CH base flow.

### Failure modes (skill memory)

- **Detection threshold** sets the small-end of the size
  distribution.
- **Line-of-sight projection** affects width estimates.
- **Polar coverage** is geometrically degenerate from SDO ecliptic
  view.

### Claim boundary

**In scope.** AIA-era statistics of CH jets within the SDO viewing
geometry.

**Out of scope.** Do NOT generalize to non-polar CH jets without a
separate analysis.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_aia()`                   | AIA cadence              |
| `detection.coronal_jet_pipeline()`      | event detection          |
| `morphology.measure_jet_size()`         | height/width/lifetime    |
| `statistics.fit_lognormal()`            | size distribution        |
| `magnetogram.cospatial_polarity()`      | photospheric polarity    |

### Procedure

1. Fetch high-cadence AIA imagery over the CH region.
2. Detect jets; measure geometry.
3. Fit log-normal distributions; report parameters.
4. Cross-reference photospheric polarity.

### Validation target

TODO verify — log-normal fit parameters match published values
within stated tolerance.

## Layer 3 — Adapter / runtime notes (optional examples)

- Python: `aiapy` + `scikit-image` for detection; `scipy.stats` for
  log-normal fitting.

## Layer 4 — Research-generation affordances

- **Gap:** EUI HRI / EUI FSI jet catalogs at high cadence are not
  yet at the AIA-era statistical scale — pair with
  `[[paper-eui-fsi-hri-coronal-bright-points-statistics]]`.
- **Hypothesis:** CH jet recurrence correlates with PSP-observed
  switchback occurrence
  (`[[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]`).

## Skill graph → depends_on

- `[[paper-coronal-hole-boundary-detection-suvi-segmentation]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
