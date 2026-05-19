# paper-flare-forecasting-sharp-features-deep-learning

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when building a **deep-learning flare forecaster**
on SHARP (Space-weather HMI Active Region Patch) features — i.e.
classifying an AR's 24-hour M/X-flare probability.

## Layer 1 — Scientific invariant

- **Paper identity:** Deep-Learning Flare Forecasting from SHARP
  Features (representative: Bobra & Couvidat 2015; Huang+ 2018;
  Park+ 2020).
- **Year:** TODO verify.
- **Venue:** ApJ / Sol. Phys. — TODO verify.

### Claim (narrow form)

SHARP keyword features (USFLUX, TOTUSJH, MEANGAM, ...) predict 24-hour
M/X-class flare probability with **TSS ~ 0.7–0.8**, comparable to or
exceeding hand-crafted predictors, when trained on a balanced sample.

### Method assumptions

- SHARP keyword time series at 12-min cadence.
- A pre-event window of fixed length is fed to the model.
- Class balance is corrected by oversampling or class weights.

### Failure modes (skill memory)

- **Operational metric drift.** TSS on the test set drops once the
  training-set cycle phase is exited.
- **Feature leak.** Some SHARP keywords are computed *after* the
  event; ensure the window predates the flare.
- **AR vs. full-disk** mismatch: SHARP is AR-scoped, so full-disk
  flares from outside any SHARP cutout are missed.
- **Class imbalance** dominates apparent accuracy.

### Claim boundary

**In scope.** 24-hour M/X-class flare forecasts for AR-scale events
in the HMI era.

**Out of scope.** Do NOT generalize to pre-HMI (MDI) periods without
cross-calibration; do NOT generalize across solar cycles without
retraining.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `vector_mag.fetch_sharp_keywords()`     | SHARP feature series     |
| `dataset.windowed_supervised()`         | training-window builder  |
| `ml.train_classifier()`                 | RF / LSTM / CNN          |
| `metrics.tss_hss_far()`                 | flare-forecast metrics   |
| `evaluation.cycle_holdout()`            | temporal split           |

### Procedure

1. Fetch SHARP keyword history.
2. Build supervised windows ending strictly before flare onset.
3. Train classifier; evaluate via temporal hold-out.
4. Report TSS / HSS / FAR per class.

### Validation target

TODO verify — `TSS ≥ 0.7` on a paper-stated temporal hold-out.

## Layer 3 — Adapter / runtime notes (optional examples)

- Python `drms` for SHARP queries; `scikit-learn` / `pytorch` for
  the model.

## Layer 4 — Research-generation affordances

- **Gap:** topology-derived features
  (`[[paper-flare-qsl-pre-eruption-topology-decay-index]]`) have not
  been combined with SHARP features in a single ML model in a
  fully reproducible way.
- **Tension:** different papers' TSS values are not directly
  comparable due to split conventions.
- **Hypothesis:** including the AR's connectivity to coronal-hole
  boundaries
  (`[[paper-coronal-hole-boundary-detection-suvi-segmentation]]`)
  raises TSS for confined-flare false alarms.

## Skill graph → depends_on

- `[[paper-hmi-vector-magnetogram-disambiguation-acute-angle]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
