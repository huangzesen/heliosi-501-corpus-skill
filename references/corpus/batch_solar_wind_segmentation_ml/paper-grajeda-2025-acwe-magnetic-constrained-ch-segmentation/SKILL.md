---
name: grajeda-2025-acwe-magnetic-constrained-ch-segmentation
description: >-
  Use when segmenting coronal holes in EUV imagery with a magnetic-constrained Active
  Contours Without Edges (ACWE) algorithm that uses photospheric magnetograms to pre-filter
  non-CH dark regions and constrain ACWE evolution — central claim is that the magnetic
  constraint reduces filament false positives and recovers low-intensity CH regions
  otherwise missed (Grajeda et al. 2025, arXiv:2501.13211; venue TODO verify).
version: 0.1.0
tags: [machine-learning, segmentation, coronal-hole, acwe, magnetic-constraint, euv, solar-wind-source, image-processing]
quality_level: pilot
executable_status: scaffold
---

# Grajeda 2025 — Magnetic-Constrained ACWE Coronal-Hole Segmentation

> Compiled from Grajeda, J. A., Boucheron, L. E., Kirk, M. S., Leisner, A., Arge, C. N., Landeros, J. A. (2025), *Incorporating Magnetic Field Characteristics into EUV-Based Automated Segmentation of Coronal Holes*, arXiv:2501.13211 (v2, updated 2025-09-15; venue TODO verify).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. ACWE energy-functional weights, magnetic skewness threshold, and quantitative gain vs unconstrained ACWE require the full text.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Producing **coronal-hole segmentations** on SDO/AIA 193 Å (or 211 Å) EUV imagery for use as solar-wind-source proxies in PFSS / WSA pipelines.
- Replacing or augmenting a **classical EUV-threshold** CH segmentation with a **magnetic-constrained** variant to reduce filament confusion and stray-light bias.
- Building a CH catalog whose boundaries depend explicitly on photospheric magnetic-field unipolarity.
- Producing **CH boundaries with explicit magnetic-skew filtering** rather than EUV-only criteria.

Do NOT use this skill when:

- The downstream product is a **chromospheric** CH delineation — use [[paper-landeros-2024-stride-ch-chromospheric-ensemble]]-style chromospheric ensemble (companion in the inventory but not in this batch).
- Segmenting **filaments** or **active regions** — the model is CH-targeted.
- A **deep-learning** CH detector is required — see the POP-CORN neural-network detector ([[paper-pop-corn-2026-cnn-ch-detection]], not in this batch).

## 2. Paper claim → verifiable task

**Claim (narrow form).** Incorporating photospheric magnetogram-derived magnetic-field characteristics into the classical Active Contours Without Edges (ACWE) EUV-CH segmentation — both as a pre-filter that removes non-CH dark regions and as an evolution-time constraint on the boundary — (a) reduces filament false positives and (b) recovers low-intensity CH regions otherwise missed by intensity-only ACWE.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reproduces the ACWE baseline (no magnetic constraint) on the paper's image set.
2. Adds the magnetic pre-filter and constraint with the paper's parameters (TODO verify magnetic-skew threshold, weight in the ACWE energy functional).
3. Reports the filament-false-positive reduction and the recovered-CH-area gain reported (TODO verify exact numbers).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — EUV ingestion + pre-processing

- Procedure:
  1. Pull SDO/AIA 193 Å (or 211 Å — TODO verify which) full-disk images at the paper's cadence (TODO verify).
  2. Limb-darkening correction; spike removal; exposure normalisation.
  3. Optionally register to a common Carrington grid.

### Algorithm 3.2 — Magnetogram pre-filter

- Procedure:
  1. Pull SDO/HMI line-of-sight magnetograms at the matched timestamps.
  2. Compute a per-region magnetic-flux skewness (unipolarity proxy). The skewness threshold the paper uses is TODO verify (Grajeda 2023 ACWE follow-up uses skewness ≳ ±1; the 2025 paper may calibrate differently).
  3. Use the skewness map to **exclude** regions that are dark in EUV but bipolar (filaments).

### Algorithm 3.3 — ACWE energy functional with magnetic constraint

- ACWE without edges (Chan–Vese variant): evolve a level-set φ minimising an energy
  E(φ) = μ·length + ν·area + λ_in·∫(I − c_in)² H(φ) + λ_out·∫(I − c_out)² (1−H(φ)).
- Grajeda 2025 extends this by adding a magnetic-constraint term that **pulls the boundary toward unipolar regions** and **away from bipolar regions**:
  E_total = E_ACWE + λ_B · E_magnetic.
- The exact form of E_magnetic and the weight λ_B is TODO verify.

### Algorithm 3.4 — Convergence + boundary export

- Procedure:
  1. Initialise φ from a seed (e.g., low-intensity threshold).
  2. Iterate until convergence (max iterations + tolerance — TODO verify).
  3. Export per-pixel CH mask, per-CH skewness, area, and centroid.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once magnetic-constraint weight and skewness threshold are pinned.
def grajeda2025_acwe_magnetic(euv, magnetogram, params):
    pre = preprocess_euv(euv)
    skew = magnetic_skewness(magnetogram)
    seed = init_phi_from_intensity(pre)
    phi = evolve_acwe_with_magnetic_constraint(pre, skew, seed, lambda_B=params.lambda_B, ...)
    return mask_from_phi(phi)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SDO AIA | 193 Å (or 211 Å) full-disk EUV image | L1 → preprocessed | 2010-05 – 2024 (TODO verify exact window) | JSOC | `sunpy` |
| SDO HMI | Line-of-sight magnetogram | L1.5 | Matched timestamps | JSOC | `sunpy` |
| (Optional) PFSS open-field mask | Boundary cross-check | derived | Same | `pfsspy` / [[paper-stansby-2020-pfsspy-python-pfss]] | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: magnetic-constrained ACWE reduces filament FPs and recovers low-intensity CH area vs intensity-only ACWE.
- **Metric**: per-image (a) IoU vs hand-labelled ground truth, (b) filament-FP count, (c) recovered low-intensity-CH area.
- **Tolerance**: TODO verify.
- **Reference figure**: TODO verify — likely a side-by-side baseline/improved segmentation panel.

Recommended check artifacts:

- `grajeda2025_segmentations.npz` — per-image (image_id, mask_baseline, mask_magnetic).
- `grajeda2025_metrics.csv` — per-image IoU, FP count, recovered area.

## 6. Failure modes → skill memory

- **Magnetogram noise floor.** HMI weak-field noise can break skewness-based unipolarity tests near disk centre; weak-field thresholding matters.
- **Limb darkening + projection.** Near-limb CH detection is biased; high-latitude CHs are especially affected.
- **Filament vs CH ambiguity.** Filaments appear dark in 193 Å like CHs; the magnetic constraint resolves this only if the filament's underlying field is bipolar — quiescent filaments often satisfy this, eruptive ones may not.
- **EUV calibration drift.** AIA degradation drifts CH-intensity thresholds across years; degradation correction must be applied.
- **ACWE initialisation sensitivity.** Different φ seeds converge to different local minima; report the seeding rule.
- **Convergence stopping rule.** Fixed iteration count vs energy-based stopping change results; pin the rule.
- **PFSS comparison is downstream, not validation.** Cross-checking against PFSS open-field maps is a useful sanity check but not a ground truth — PFSS itself has known footpoint mis-mapping issues.

## 7. Claim boundary

**In scope.** Magnetic-constrained ACWE segmentation of coronal holes on SDO/AIA 193 Å (or 211 Å) full-disk EUV imagery, using HMI line-of-sight magnetograms as the magnetic constraint.

**Out of scope — do NOT generalise beyond:**

- Chromospheric CH segmentation — use a chromospheric pipeline.
- Non-SDO EUV instruments without recalibrating thresholds.
- Filament / AR / sunspot segmentation.
- 3D coronal-volume CH attribution — the segmentation is per-image 2D.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2501.13211 (v2, updated 2025-09-15).
- ADS: TODO verify.
- Code: TODO verify (the Grajeda group typically releases reference ACWE pipelines).
- Data: SDO via JSOC (public); cf. companion [[paper-roy-2025-suryabench-ml-benchmark-dataset]] for ML-ready SDO data.

## 9. Skill graph → depends_on

- `[[paper-roy-2025-suryabench-ml-benchmark-dataset]]` — supplies preprocessed AIA + HMI inputs.
- `[[paper-roy-2025-surya-heliophysics-foundation-model]]` — alternative deep-learning CH segmentation baseline; LoRA-fine-tunable on the same data.
- `[[paper-stansby-2020-pfsspy-python-pfss]]` — PFSS for the open-field cross-check (infrastructure, in `batch_heliophysics_software_infrastructure/`).
- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — downstream consumer (CH-origin classification at 1 au).

## Notes

- The 2025-09-15 v2 update suggests the paper underwent revisions; the abstract referenced here is from the v2 page and is the most current version in the inventory.
- The "skewness" threshold the paper uses is the most reproducibility-critical parameter; without it, the magnetic constraint reduces to a soft regulariser.
