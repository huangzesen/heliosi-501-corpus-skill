---
name: hu-2022-deep-swim-cnn-discontinuities
description: >-
  Use when applying a few-shot CNN ("Deep-SWIM") to classify short magnetic-field windows
  in solar-wind in-situ data into discontinuity vs. non-discontinuity classes — central
  paper claim is that 5-minute windows of stacked magnetic-field components fed into a CNN
  yield a binary discontinuity classifier trainable with limited labelled data (arXiv:2203.01184,
  Deep-SWIM; full author list and venue TODO verify).
version: 0.1.0
tags: [machine-learning, cnn, few-shot, solar-wind, discontinuity, current-sheet, classification]
quality_level: pilot
executable_status: scaffold
paper:
  authors_verified: false
---

# Deep-SWIM (Hu et al.) 2022 — Few-Shot CNN for Solar-Wind B-Field Discontinuities

> Compiled from arXiv:2203.01184, *Deep-SWIM: A few-shot learning approach to classify Solar WInd Magnetic field structures* (full author list, lead author surname, and venue TODO verify — inventory lists the ar5iv mirror only).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. CNN depth, training set size, episode design (few-shot), and per-class accuracy require the full text.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Building a **per-window binary classifier** (discontinuity vs ambient turbulence) on 5-minute solar-wind B-field windows.
- Working with a **small labelled set** — Deep-SWIM is explicitly a few-shot pipeline.
- Pre-processing for downstream **coherent-structure / current-sheet** statistics (compare with PVI from [[paper-pecora-2022-coherent-structures-proton-electron-heating]] in the turbulence batch).
- Needing a CNN baseline to compare against unsupervised approaches ([[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]).

Do NOT use this skill when:

- Detecting **large-scale** structures (ICMEs, switchbacks at sec–min scales) — Deep-SWIM windows are 5 min and miss multi-hour events.
- Producing **per-sample** segmentation — Deep-SWIM is window-level binary classification.
- Needing physical labels (current-sheet vs rotational-discontinuity vs tangential-discontinuity) — Deep-SWIM is binary discontinuity-vs-ambient unless extended.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Splitting solar-wind magnetic-field time series into **5-minute windows**, stacking the three magnetic-field components into a multi-channel CNN input, and training with few-shot episodes yields a **binary discontinuity classifier** that recovers labelled discontinuities with reasonable accuracy under limited supervision. Exact accuracy / F1 numbers are TODO verify from the inventory.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reproduces the same windowing (5-min, components stacked) on the same instrument/window pair (TODO verify which mission — likely Wind / ACE / Cluster).
2. Trains a few-shot CNN with the same episode structure (TODO verify N-way K-shot).
3. Recovers the per-class accuracy within tolerance (TODO verify).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Windowing + label assignment

- Procedure:
  1. Pull L2 magnetic-field data at the cadence the paper uses (TODO verify; for 5-min windows the native cadence must be ≥ 0.1 Hz).
  2. Slide a 5-min window with stride (TODO verify; non-overlapping or 50%-overlap are typical).
  3. Label each window by intersecting with a discontinuity catalog (TODO verify catalog — Tsurutani–Smith, Vasquez, or hand-labelled).

### Algorithm 3.2 — Multi-channel input tensor

- Stack {B_x, B_y, B_z} or {B_R, B_T, B_N} as separate channels. The component frame (GSE vs RTN) is TODO verify.
- Optionally include |B| as a fourth channel (TODO verify).

### Algorithm 3.3 — Few-shot CNN architecture + training

- Procedure:
  1. Build the CNN (depth, kernel sizes TODO verify).
  2. Train via few-shot episodes: N-way K-shot meta-learning OR transfer-learn from a base classifier with very small fine-tuning set. The exact paradigm (prototypical networks, MAML, Reptile, plain transfer) is TODO verify.
  3. Evaluate on a disjoint test set.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once architecture, episode design, and labels are pinned.
def deep_swim(timeseries, label_catalog):
    windows = slide_5min_windows(timeseries)             # 3.1
    X = stack_components(windows)                         # 3.2
    y = label_by_catalog(windows, label_catalog)
    model = build_few_shot_cnn()                          # 3.3 — arch TODO verify
    return train_few_shot(model, X_train, y_train), evaluate(model, X_test, y_test)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| (Likely) Wind MFI | B (GSE) | L2 ≥ 0.1 Hz | Window TODO verify | CDAWeb / SPDF | `cdflib` |
| (Or) ACE MAG | B (GSE) | L2 | Same | CDAWeb / SPDF | `cdflib` |
| Discontinuity catalog | t_event per discontinuity | derived | Same | Tsurutani–Smith / Vasquez / hand-labelled — TODO verify | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: Few-shot CNN classifier recovers solar-wind B-field discontinuities from 5-min windows with limited labels (numerical accuracy / F1 TODO verify).
- **Metric**: per-window binary accuracy / F1 on held-out test set.
- **Tolerance**: TODO verify.
- **Reference figure**: TODO verify — likely a confusion matrix + accuracy-vs-shots-K curve.

Recommended check artifacts:

- `deepswim_predictions.csv` — per-window (t_center, p_disc, label_truth).
- An accuracy-vs-K (shots) curve.
- A confusion matrix at the paper's chosen threshold.

## 6. Failure modes → skill memory

- **Catalog identity.** Tsurutani–Smith vs Vasquez catalogs differ in discontinuity definitions (TD vs RD vs ED); a "discontinuity" label is catalog-conditioned.
- **Window stride.** Overlapping windows leak labels into adjacent windows.
- **Frame choice (GSE vs RTN).** Rotation-invariant features survive frame changes; raw component values do not. Document the frame.
- **Class imbalance.** Discontinuities occupy a small fraction of time; few-shot learning helps but the imbalance still inflates raw accuracy.
- **Few-shot episode design.** N-way K-shot, prototypical-networks, MAML, and plain transfer give different sample efficiencies and stability; the paper's choice is TODO verify and load-bearing.
- **Distance / regime sensitivity.** Discontinuity statistics differ between 1 au and inner-heliosphere; a Wind-trained model is not a PSP-near-Sun classifier.

## 7. Claim boundary

**In scope.** Few-shot CNN per-window binary classification (discontinuity vs ambient) on 5-min solar-wind B-field windows, with limited labelled data.

**Out of scope — do NOT generalise beyond:**

- Per-sample segmentation — Deep-SWIM is window-level.
- Multi-class discontinuity type (RD vs TD vs ED) — binary unless explicitly retrained.
- Other in-situ structures (ICMEs, switchbacks).
- Other distance regimes (PSP near-Sun) without retraining.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2203.01184
- ADS: TODO verify.
- Code: TODO verify.
- Data: Wind / ACE L2 (public).

## 9. Skill graph → depends_on

- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling ML approach on larger structures (ICMEs); shares the windowed-input lesson.
- `[[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]` — sibling ML event detector on PSP burst-mode waveforms.
- `[[paper-pecora-2022-coherent-structures-proton-electron-heating]]` — physical coherent-structure detection via PVI (non-ML baseline).
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — unsupervised time-series-mining alternative.

## Notes

- "Deep-SWIM" is the system name; the methods section should expose the exact few-shot recipe (prototypical / MAML / transfer) before any benchmarked-tier promotion.
