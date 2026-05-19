# paper-mdi-hmi-cross-calibration-synoptic-flux

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when stitching **MDI and HMI synoptic
magnetograms** across the SOHO–SDO era boundary, where instrument
sensitivities differ enough to affect total unsigned flux.

## Layer 1 — Scientific invariant

- **Paper identity:** MDI–HMI Synoptic Cross-Calibration (representative:
  Liu+ 2012; Riley+ 2014).
- **Year:** TODO verify.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

HMI LOS magnetic flux is systematically `~1.2–1.4×` larger than MDI
in strong-field regions; a linear-saturating mapping with two
parameters reduces residuals to `< 5%` on the overlap interval
(~2010–2011).

### Method assumptions

- Common spatial grid resampling (e.g. CEA-projection synoptic).
- Overlap interval long enough to span at least one Carrington
  rotation.
- Limb correction is applied prior to mapping.

### Failure modes (skill memory)

- **Plate-scale and resolution** differences must be matched before
  flux comparison.
- **Filling-factor assumptions** differ between instruments.
- **Cycle phase** affects the calibration constants.

### Claim boundary

**In scope.** Synoptic Br flux stitching for MDI ↔ HMI within the
overlap interval and within `~3` solar cycles either side.

**Out of scope.** Do NOT extrapolate calibration constants to
pre-Cycle-23 epochs.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `magnetogram.fetch_synoptic_mdi()`      | MDI synoptic             |
| `magnetogram.fetch_synoptic_hmi()`      | HMI synoptic             |
| `magnetogram.resample_grid()`           | common CEA grid          |
| `calibration.fit_linear_saturating()`   | two-parameter mapping    |
| `metrics.flux_residual()`               | unsigned-flux residual   |

### Procedure

1. Resample both synoptic series to a common grid.
2. Fit the calibration mapping on the overlap.
3. Apply to MDI maps for downstream merge.

### Validation target

TODO verify — residual unsigned flux `< 5%` on overlap interval.

## Layer 3 — Adapter / runtime notes (optional examples)

- Python `drms` + `sunpy` for fetches; `scipy.optimize.curve_fit`
  for the saturating mapping.

## Layer 4 — Research-generation affordances

- **Gap:** the open-flux problem's apparent persistence is sensitive
  to cross-calibration choice — pair with
  `[[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]`.
- **Hypothesis:** GONG–HMI cross-calibration noise dominates the
  small-cycle differences in long-baseline PFSS reconstructions.

## Skill graph → depends_on

- `[[paper-gong-network-synoptic-magnetogram-product]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
