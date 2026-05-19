---
name: paper-swap-fov-extended-corona-low-temperature
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-swap-fov-extended-corona-low-temperature

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when using **PROBA-2 / SWAP** wide-field
174 Å imagery to study the extended low-temperature corona
between disk and ~2 R_sun.

## Layer 1 — Scientific invariant

- **Paper identity:** PROBA-2 / SWAP Extended-Corona Imaging
  (representative: Seaton+ 2013; Mierla+ 2013).
- **Year:** 2013.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

SWAP's `~55 arcmin` FOV at 174 Å extends EUV observations to
~1.7 R_sun, **bridging the gap between disk EUV imagers and inner
coronagraphs** with sensitivity to cool (~1 MK) coronal structures.

### Method assumptions

- SWAP L1 reduction is applied.
- Coordinate calibration with AIA / STEREO EUVI.

### Failure modes (skill memory)

- **Diffuse PSF wings** in the extended FOV.
- **Low-cadence and limited exposure** restrict transient studies.

### Claim boundary

**In scope.** Quasi-static features in the cool (~1 MK) extended
corona to ~1.7 R_sun.

**Out of scope.** Do NOT use for hot-temperature loops or short-
lived (< 1 min) brightenings.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_swap_l1()`               | SWAP frames              |
| `imagery.stitch_with_aia()`             | extended composite       |
| `morphology.identify_offlimb_loop()`    | extended-corona feature  |

### Procedure

1. Fetch SWAP L1.
2. Co-register with AIA on-disk.
3. Identify off-limb features in the 1.2–1.7 R_sun band.

### Validation target

TODO verify — recover published off-limb feature catalog.

## Layer 3 — Adapter / runtime notes (optional examples)

- ROB / SIDC SWAP archive.

## Layer 4 — Research-generation affordances

- **Gap:** SWAP + EUI FSI joint datasets at high cadence are
  rare — pair with
  `[[paper-eui-fsi-hri-coronal-bright-points-statistics]]`.
- **Hypothesis:** persistent off-limb cool structures
  systematically connect to pseudostreamer footprints
  (`[[paper-coronal-hole-pseudostreamer-boundary-classification]]`).

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
