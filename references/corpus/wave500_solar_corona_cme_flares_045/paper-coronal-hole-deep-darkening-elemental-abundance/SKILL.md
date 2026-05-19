# paper-coronal-hole-deep-darkening-elemental-abundance

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when interpreting **deep CH darkening in
EUV/X-ray** in terms of low first-ionization-potential (FIP) bias and
how this connects to in-situ "fast-wind" composition.

## Layer 1 — Scientific invariant

- **Paper identity:** Coronal-Hole Deep Darkening and Elemental
  Abundance (representative: Brooks+ 2015; Laming 2015 review).
- **Year:** TODO verify.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

Deep-darkened regions of CHs in EUV/X-ray show **photospheric-like
abundances (low FIP bias ~1)** consistent with the fast wind,
whereas streamer-belt regions show coronal abundances (FIP bias
~2–4). The narrow claim is that EUV brightness deficit and FIP-bias
deficit are co-spatial within stated boundaries.

### Method assumptions

- DEM inversion of EUV / X-ray imagery.
- FIP bias derived from emission-line ratios (e.g. Si/S, Fe/Si).
- Comparison to in-situ Fe/O or Mg/Ne at 1 au or PSP.

### Failure modes (skill memory)

- **DEM inversion** is ill-posed; results depend on regularization.
- **Line blends** in EUV spectra are non-negligible.
- **In-situ time lag** between coronal source and detector must be
  applied carefully.

### Claim boundary

**In scope.** Spatially-resolved FIP-bias maps in CH interiors and
their correspondence to in-situ FIP at conjunctions.

**Out of scope.** Do NOT use as a real-time identification of fast
wind without in-situ confirmation.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_aia()`                   | DEM input                |
| `imagery.fetch_xrt()`                   | X-ray DEM input          |
| `coronal_dem.invert()`                  | T-dependent emission     |
| `spectro.fip_ratio()`                   | line-ratio FIP bias      |
| `in_situ.fetch_psp_composition()`       | Fe/O or Mg/Ne in-situ    |
| `metrics.fip_corona_vs_insitu()`        | composition link         |

### Procedure

1. Build DEM maps over CH from AIA/XRT.
2. Compute FIP-bias maps from line ratios.
3. Pull in-situ composition at the magnetically connected interval.
4. Compare.

### Validation target

TODO verify — co-spatial FIP-bias deficit and in-situ low-FIP
fraction.

## Layer 3 — Adapter / runtime notes (optional examples)

- `chiantipy` for line emissivities; `aiapy` for AIA prep; `psipy`
  for connectivity from MAS.

## Layer 4 — Research-generation affordances

- **Gap:** no PSP-aligned multi-spacecraft FIP campaign has fully
  exploited Brooks/Laming framework — pair with
  `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]`.
- **Hypothesis:** SASW with low-FIP signatures originates from
  pseudostreamer boundaries
  (`[[paper-coronal-hole-pseudostreamer-boundary-classification]]`).

## Skill graph → depends_on

- `[[paper-suvi-multi-wavelength-temperature-dem-corona]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
