---
name: paper-suvi-multi-wavelength-temperature-dem-corona
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-suvi-multi-wavelength-temperature-dem-corona

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when computing **multi-wavelength DEM** (differential
emission measure) inversions from GOES/SUVI to characterize coronal
temperature structure, especially as input to PFSS-modeled Alfvén-speed
maps.

## Layer 1 — Scientific invariant

- **Paper identity:** SUVI Multi-Wavelength DEM Inversion of the Corona
  (representative: Vasudevan+ 2021; Tadikonda+ 2019).
- **Year:** 2019–2021.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

SUVI's six EUV channels at GOES cadence support DEM inversions
producing temperature maps with **systematic agreement with AIA-DEM
to ~20%** in the 0.5–3 MK range during overlapping observations.

### Method assumptions

- SUVI L2 calibrated radiances.
- Regularized DEM inversion (Hannah & Kontar 2012 or sparse method).
- Co-temporal AIA cross-check is available.

### Failure modes (skill memory)

- **Hot-plasma sensitivity** is weaker than AIA's 94/131 Å.
- **DEM ill-posedness** dominates at the temperature endpoints.
- **L2 vs L1b** product choice affects calibration uncertainty.

### Claim boundary

**In scope.** Quiet-Sun and active-region DEM in 0.5–3 MK.

**Out of scope.** Do NOT use SUVI alone for hot flare plasma
(> 5 MK).

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_suvi_l2()`               | SUVI six-channel data    |
| `coronal_dem.invert()`                  | DEM inversion            |
| `metrics.compare_aia_dem()`             | cross-check              |
| `field.alfven_map_from_dem_pfss()`      | downstream v_A           |

### Procedure

1. Fetch SUVI L2 multi-channel imagery.
2. Invert DEM with regularization.
3. Compare to AIA-DEM where co-temporal.
4. Build downstream Alfvén-speed map by combining DEM + PFSS.

### Validation target

TODO verify — DEM agreement with AIA within ~20%.

## Layer 3 — Adapter / runtime notes (optional examples)

- `sunkit-dem` Python package; AIA DEM via `aiapy`.

## Layer 4 — Research-generation affordances

- **Gap:** SUVI-derived `v_A` maps have not been used as input to
  EUV-wave classifier
  (`[[paper-eui-euv-wave-fast-mode-mhd-front]]`) in production.

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
