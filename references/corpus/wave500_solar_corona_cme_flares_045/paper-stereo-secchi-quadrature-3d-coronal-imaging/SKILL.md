---
name: paper-stereo-secchi-quadrature-3d-coronal-imaging
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-stereo-secchi-quadrature-3d-coronal-imaging

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when STEREO A/B (quadrature era) observations
are used to **stereo-pair-reconstruct 3-D coronal loops, streamers,
or filaments** from EUVI + coronagraph imagery.

## Layer 1 — Scientific invariant

- **Paper identity:** STEREO / SECCHI Quadrature 3-D Coronal Imaging
  (representative: Aschwanden+ 2008; Inhester 2006; Howard+ 2008).
- **Year:** 2008.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

Stereo-pair tie-pointing of identifiable features in EUVI + COR1/COR2
yields 3-D structure with **angular precision `< 2°` at quadrature**;
loss of stereoscopy off-quadrature degrades the precision smoothly.

### Method assumptions

- Both spacecraft viewing the same feature.
- Common feature identification across viewpoints.

### Failure modes (skill memory)

- **Feature identification** is the dominant systematic.
- **Optical depth** changes between viewpoints in EUV.
- **STEREO-B loss** (2014) ends quadrature observations.

### Claim boundary

**In scope.** Quadrature-era stereoscopic reconstruction of coronal
structures.

**Out of scope.** Do NOT extend the precision claim to the
single-viewpoint STEREO-A-only era.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_stereo_euvi()`           | EUVI on each viewpoint   |
| `imagery.fetch_stereo_cor1_cor2()`      | coronagraph              |
| `geometry.tie_point_3d()`               | per-feature 3-D reco     |
| `metrics.angular_precision()`           | residual error           |

### Procedure

1. Fetch EUVI + COR pair.
2. Identify shared features across both viewpoints.
3. Tie-point reconstruct 3-D positions.
4. Report angular precision.

### Validation target

TODO verify — angular precision `< 2°` at quadrature.

## Layer 3 — Adapter / runtime notes (optional examples)

- IDL SolarSoft `secchi_prep`; Aschwanden `aia/scc_measure`.

## Layer 4 — Research-generation affordances

- **Gap:** the Aschwanden + EUVI loop-reconstruction sample is
  reusable for NLFFF validation but rarely re-used today.
- **Hypothesis:** revisiting these data with NLFFF in
  `[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`
  resolves the historical loop-extrapolation mismatch.

## Skill graph → depends_on

- `[[paper-mierla-2010-3d-cme-reconstruction-stereo-secchi]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
