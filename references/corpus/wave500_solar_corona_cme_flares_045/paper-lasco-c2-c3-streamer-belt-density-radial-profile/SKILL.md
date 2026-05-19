---
name: paper-lasco-c2-c3-streamer-belt-density-radial-profile
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-lasco-c2-c3-streamer-belt-density-radial-profile

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when **LASCO C2/C3 brightness** must be inverted
to electron density along the streamer belt for source-region or
heliospheric density-modeling.

## Layer 1 — Scientific invariant

- **Paper identity:** LASCO Streamer-Belt Radial Density Profile
  (representative: Sittler & Guhathakurta 1999; Spadaro+ 2017).
- **Year:** TODO verify.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

LASCO C2/C3 azimuthally-averaged streamer-belt brightness fits a
two-power-law radial density profile with break point near `~5
R_sun`; the resulting `n_e(r)` is reproducible across solar cycles
when normalized at 1 au.

### Method assumptions

- Long-time-averaged brightness suppresses transients.
- van de Hulst inversion with a chosen geometry.
- F-corona separation is applied.

### Failure modes (skill memory)

- **F-corona / K-corona separation** dominates large-r systematics.
- **Streamer-belt definition** is cycle-phase-dependent.
- **Polarization-not-available** in LASCO post-2010 reduces accuracy.

### Claim boundary

**In scope.** Equatorial streamer-belt density profile, 2.2–30 R_sun.

**Out of scope.** Do NOT extrapolate to polar regions without
re-derivation.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_lasco()`                 | C2/C3 frames             |
| `image.azimuthal_average()`             | radial profile           |
| `radiation.fcorona_separate()`          | F removal                |
| `radiation.van_de_hulst_invert()`       | brightness → n_e         |
| `scaling.fit_two_power_law()`           | radial profile fit       |

### Procedure

1. Fetch long-time-averaged LASCO frames in the target window.
2. Azimuthally average around the streamer belt.
3. Separate F-corona; invert to n_e(r).
4. Fit two-power-law.

### Validation target

TODO verify — break-point near 5 R_sun and 1-au normalization within
factor ~2.

## Layer 3 — Adapter / runtime notes (optional examples)

- IDL SolarSoft `lasco_prep` / Python `sunpy`.

## Layer 4 — Research-generation affordances

- **Gap:** density profiles from LASCO, Metis, and WISPR have not
  been combined into a single radial profile across the encounter
  envelope.
- **Hypothesis:** the two-power-law break point shifts with cycle
  phase — testable with the
  `[[paper-mdi-hmi-cross-calibration-synoptic-flux]]` long baseline.

## Skill graph → depends_on

- `[[paper-metis-coronal-polarized-brightness-electron-density]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
