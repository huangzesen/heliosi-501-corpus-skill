---
name: paper-coronal-hole-boundary-detection-suvi-segmentation
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-coronal-hole-boundary-detection-suvi-segmentation

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when **coronal-hole (CH) boundaries** must be
extracted from EUV imagery (SUVI/AIA/EUI) for source-mapping or
solar-wind connectivity studies.

## Layer 1 — Scientific invariant

- **Paper identity:** Coronal-Hole Boundary Detection from EUV Imagery
  (representative: SPoCA / CHIMERA / Reiss+ 2015).
- **Year:** TODO verify.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

Multi-threshold or watershed-segmentation pipelines extract CH
boundaries from 193/195 Å EUV imagery with **boundary-pixel agreement
~80%** between independent pipelines on disk-center holes; agreement
drops near the limb.

### Method assumptions

- Multi-channel EUV imagery; 193/195 Å dominant.
- Boundary defined by an intensity threshold + morphology.
- Limb-darkening corrections are applied.

### Failure modes (skill memory)

- **Filament dimming** can be falsely segmented as CH.
- **Limb-near holes** suffer from line-of-sight contamination.
- **Cycle phase** changes the optimal threshold.
- **Boundary jitter** between frames demands temporal smoothing.

### Claim boundary

**In scope.** Disk-center, on-disk CH boundary extraction from
SUVI/AIA 193/195 Å.

**Out of scope.** Do NOT use these boundaries as ground-truth open-
closed magnetic boundaries; they are an EUV proxy.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_aia()` / `fetch_suvi()`  | EUV imagery              |
| `image.limb_darken_correct()`           | µ-correction             |
| `segmentation.threshold_watershed()`    | CH mask                  |
| `morphology.smooth_boundary()`          | temporal smoothing       |
| `metrics.iou_vs_reference()`            | inter-pipeline agreement |

### Procedure

1. Fetch and prep EUV imagery.
2. Apply limb-darkening correction.
3. Threshold + watershed segmentation.
4. Smooth boundaries in time.
5. Compare against a published catalog.

### Validation target

TODO verify — IoU ≥ 0.6 against a reference catalog.

## Layer 3 — Adapter / runtime notes (optional examples)

- The CHIMERA, SPoCA, ACWE pipelines are reference adapters.

## Layer 4 — Research-generation affordances

- **Gap:** ML-based CH segmentation
  (`[[paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation]]`)
  uses a magnetogram constraint; pair with this skill to quantify
  the EUV-only systematic.
- **Hypothesis:** CH boundaries are systematically retracted near
  pseudo-streamers
  (`[[paper-coronal-hole-pseudostreamer-boundary-classification]]`).

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
