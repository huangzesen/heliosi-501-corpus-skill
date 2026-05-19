---
name: paper-metis-coronal-polarized-brightness-electron-density
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-metis-coronal-polarized-brightness-electron-density

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when inverting **Solar Orbiter / Metis polarized
brightness** to electron density profiles in the 1.7–9 R_sun range.

## Layer 1 — Scientific invariant

- **Paper identity:** Metis Polarized Brightness Electron-Density
  Inversion (representative: Antonucci+ 2020; Romoli+ 2021;
  Russano+ 2022).
- **Year:** 2020–2022.
- **Venue:** A&A — TODO verify.

### Claim (narrow form)

Metis pB images, after vignetting + stray-light correction, yield
electron density profiles `n_e(r)` between 1.7 and 9 R_sun via van
de Hulst inversion, with stated agreement to LASCO C2/C3 and
Mauna-Loa K-Cor in the overlap region.

### Method assumptions

- pB camera calibration is up to date.
- van de Hulst inversion is appropriate (single-shell or sectoral).
- Streamer-region geometry is parameterized.

### Failure modes (skill memory)

- **Stray light** at small heliocentric distance.
- **F-corona contamination** at large distance.
- **Sectoral geometry** assumptions may be invalid in CME events.

### Claim boundary

**In scope.** Quiet streamer-belt and equatorial-CH density profiles.

**Out of scope.** Do NOT use for transient CME density inversion
without rederivation; use
`[[paper-cme-true-mass-stereo-cor2-density-inversion]]`.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_metis_pb()`              | Metis L2 pB              |
| `image.straylight_subtract()`           | calibration              |
| `radiation.van_de_hulst_invert()`       | pB → n_e                 |
| `metrics.compare_lasco_kcor()`          | overlap cross-check      |

### Procedure

1. Fetch Metis L2 pB.
2. Subtract stray light + F-corona.
3. Invert via van de Hulst (single-shell or sectoral).
4. Compare to LASCO / K-Cor where overlap exists.

### Validation target

TODO verify — `n_e(r)` agreement within ~30% in overlap regions.

## Layer 3 — Adapter / runtime notes (optional examples)

- ESA Solar Orbiter Archive for L2.

## Layer 4 — Research-generation affordances

- **Gap:** Metis + WISPR pB conjunctions have not been combined for
  joint density inversion — pair with
  `[[paper-wispr-tb-imaging-large-scale-coronal-structure]]`.
- **Hypothesis:** density profiles disagree between L0 quiet-streamer
  fits and AWSoM solar wind models
  (`[[paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure]]`).

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
