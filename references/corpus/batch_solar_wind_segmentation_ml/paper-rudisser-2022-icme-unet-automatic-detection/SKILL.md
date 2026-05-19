---
name: rudisser-2022-icme-unet-automatic-detection
description: >-
  Use when automatically detecting ICMEs in 1-au in-situ solar-wind time series via a
  U-Net-style segmentation pipeline transferred from medical imaging — central claim is
  TSS ~0.64 on Wind 1997-2015 (466/640 ICMEs detected, 254 FPs) with ~20x faster training
  than baseline and comparable cross-mission transferability to STEREO-A/B (Rüdisser et
  al. 2022, arXiv:2205.03578; venue TODO verify).
version: 0.1.0
tags: [machine-learning, segmentation, icme, event-detection, wind, stereo, unet, time-series, space-weather]
quality_level: pilot
executable_status: scaffold
---

# Rüdisser 2022 — U-Net Automatic ICME Detection in Solar-Wind Time Series

> Compiled from Rüdisser, H. T., Windisch, A., Amerstorfer, U. V., Möstl, C., Amerstorfer, T., Bailey, R. L., Reiss, M. A. (2022), *Automatic Detection of Interplanetary Coronal Mass Ejections in Solar Wind In Situ Data*, arXiv:2205.03578 (venue TODO verify — likely Space Weather).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. Architecture details, exact training-set partition, and per-spacecraft hyperparameters require the full paper.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Building or replacing an **automated ICME detector** on 1-au in-situ solar-wind data (Wind, ACE, STEREO-A/B, Solar Orbiter at 1 au).
- Treating the ICME-vs-ambient-wind problem as a **time-series segmentation** (per-sample binary label) rather than per-window classification.
- Transferring a **medical-imaging U-Net** pattern to heliophysics 1D time series.
- Producing an ICME *start-time / end-time* catalog with calibrated false-positive rate for use by downstream space-weather pipelines.

Do NOT use this skill when:

- Detecting **interplanetary shocks** (different signature; reuse only the segmentation pattern, not the trained weights).
- Detecting **CIRs / stream interaction regions** — although the abstract mentions extensibility, the trained model is *ICME-only*; see [[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]] for a general structure-mining pipeline.
- Working with PSP near-perihelion data — the distance / amplitude regime differs from Wind / STEREO and re-training is required.

## 2. Paper claim → verifiable task

**Claim (narrow form).** A U-Net-style segmentation network applied to 1997–2015 Wind in-situ solar-wind data achieves a **True Skill Statistic (TSS) of 0.64** on the ICME catalog, detecting **466 of 640** catalogued ICMEs with **254 false positives**. The model trains ~**20× faster** than the existing baseline. Applied to Wind / STEREO-A / STEREO-B datasets with reduced features and smaller training sets, TSS values of **0.56 / 0.57 / 0.53** are reported. Mean absolute error on ICME start time is **~2 h 56 min**, on end time **~3 h 20 min**.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reproduces TSS = 0.64 ± tolerance on the same Wind 1997–2015 catalog split (TODO verify exact tolerance from the paper).
2. Recovers MAE(start) ≈ 2 h 56 min ± tolerance, MAE(end) ≈ 3 h 20 min ± tolerance.
3. Cross-trains on STEREO-A / STEREO-B and reaches TSS within ~0.05 of the paper's reported values.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Catalog assembly and per-sample labelling

- Procedure:
  1. Pull the Wind in-situ time series (plasma + magnetic field) for 1997–2015. The catalog used (Richardson–Cane vs. Möstl vs. union) is TODO verify.
  2. Convert event-level catalog (t_start, t_end per ICME) into a per-sample binary mask (1 = inside ICME, 0 = ambient).
  3. Resample / interpolate to the cadence the paper uses (TODO verify; common choices are 10-min or 1-hour averages).

### Algorithm 3.2 — Feature stack

- The exact feature list is TODO verify; standard ICME diagnostic features include:
  - Magnetic field magnitude |B|, components Bx, By, Bz (GSE).
  - Solar-wind speed V_sw, n_p, T_p.
  - Derived: T_p / T_exp ratio, plasma β, |B|/Bxy ratio.
- Normalise per-channel.

### Algorithm 3.3 — U-Net architecture for 1D time series

- The paper transfers a 2D U-Net (medical image segmentation) to 1D time series. Architecture details (depth, channel count, activation, dropout) are TODO verify.
- Loss: TODO verify (Dice + binary cross-entropy is standard; class-imbalance handling is needed since ICMEs are rare in time).

### Algorithm 3.4 — Training schedule + cross-mission transfer

- Procedure:
  1. Train on Wind 1997–2015 with a chronologically blocked split (TODO verify; random per-sample splitting leaks across events).
  2. Tune hyperparameters on validation block; freeze and evaluate on test block.
  3. Transfer: re-train on STEREO-A / STEREO-B / smaller-feature configurations and report TSS.

### Algorithm 3.5 — Per-event TSS, MAE(start), MAE(end)

- Procedure:
  1. Threshold per-sample probabilities, then group contiguous positive samples into predicted events.
  2. Match predicted to catalog events (e.g., by IoU > τ); compute confusion (TP, FP, FN).
  3. TSS = TPR – FPR = TP/(TP+FN) – FP/(FP+TN).
  4. For matched events compute MAE on start and end timestamps.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once feature list, U-Net depth and split are pinned.
def rudisser2022_icme_unet(time_series, mask, model_cfg):
    X, y = preprocess(time_series, mask)         # 3.1 + 3.2
    model = build_1d_unet(model_cfg)             # 3.3 — depth + channels TODO verify
    fit(model, X_train, y_train)
    preds = predict(model, X_test)
    events = postprocess_threshold_and_group(preds)
    return compute_tss_mae(events, y_test)        # 3.5
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Wind MFI | B (GSE) | L2 | 1997-01 – 2015-12 | CDAWeb / SPDF | `cdflib` |
| Wind SWE | n_p, V_sw, T_p | L2 | Same | CDAWeb / SPDF | `cdflib` |
| STEREO-A IMPACT/MAG | B | L2 | TODO verify | CDAWeb / SPDF | `cdflib` |
| STEREO-A PLASTIC | n_p, V_sw, T_p | L2 | Same | CDAWeb / SPDF | `cdflib` |
| STEREO-B IMPACT/MAG + PLASTIC | Same | L2 | 2007 – 2014 (pre-loss) | CDAWeb / SPDF | `cdflib` |
| ICME catalog | t_start, t_end per event | derived | 1997–2015 | Richardson–Cane catalog (NASA), Möstl catalog, or union | WebFetch — exact catalog TODO verify |

## 5. Validation target → benchmark artifact

- **Claim**: TSS = 0.64 on Wind 1997–2015; MAE(start) ≈ 2 h 56 min; MAE(end) ≈ 3 h 20 min; TSS(STEREO-A / -B) ≈ 0.57 / 0.53; training ~20× faster than baseline (baseline identity TODO verify).
- **Metric**: TSS = TPR – FPR; MAE in hours on event start / end timestamps.
- **Tolerance**: TODO verify in the paper. Pragmatic suggestion: |ΔTSS| ≤ 0.03; |Δ MAE| ≤ 30 min.
- **Reference figure**: TODO verify — likely a confusion-matrix / TSS table and an MAE histogram.

Recommended check artifacts:

- `rudisser2022_predictions.csv` — per-sample (t, p_ICME, label_truth).
- `rudisser2022_events.csv` — per-predicted-event (t_start, t_end, p_max, matched_catalog_id, IoU).
- A TSS + MAE summary table replicating the paper's headline numbers.

## 6. Failure modes → skill memory

- **Catalog identity matters.** Richardson–Cane and Möstl catalogs disagree on ~10–20% of borderline events; the headline TSS is *catalog-conditioned*. Always fix the catalog before claiming a TSS.
- **Random per-sample splits leak events.** Use chronologically blocked splits or event-disjoint folds.
- **Per-sample threshold rotates TSS / MAE.** Lowering the threshold raises recall but degrades MAE; the operating point matters.
- **Class imbalance.** ICMEs occupy a small fraction of time; un-weighted loss collapses to "all ambient". Use Dice / Tversky / weighted BCE.
- **Feature normalisation.** Magnetic-field magnitude and speed live on very different scales; per-channel z-score is essential.
- **STEREO-A vs -B asymmetry.** STEREO-B has fewer events post-2014 (contact loss); TSS comparisons across missions must control for sample size.
- **Cross-mission "reduced features".** Smaller feature sets (e.g., dropping electron pitch-angle) lower performance; the headline 0.56 / 0.57 / 0.53 are conditional on the paper's chosen subsets — TODO verify.
- **MAE is on matched events only.** Falsely-detected and missed events do not contribute; report match rate alongside MAE.

## 7. Claim boundary

**In scope.** U-Net-style 1D segmentation of 1-au in-situ solar-wind time series (Wind 1997–2015, STEREO-A/B subsets) for ICME boundary detection, with TSS and MAE headline performance.

**Out of scope — do NOT generalise beyond:**

- Other in-situ structures (CIRs, shocks, magnetic clouds without sheaths) — the model is ICME-trained.
- Sub-au or super-au distances (PSP near-Sun, Voyager outer heliosphere).
- Forecasting ICME arrival from coronagraph imagery — this is a *post-arrival* detector on in-situ data.
- Per-feature physical attribution — the network is opaque; do not derive physical statements from layer activations.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2205.03578
- ADS: TODO verify.
- Code: TODO verify — the abstract emphasises rapid training; a public code release is plausible but not in the inventory.
- Data: Wind / STEREO L2 via CDAWeb / SPDF (public); ICME catalogs via Richardson–Cane / Möstl (public).

## 9. Skill graph → depends_on

- `[[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]` — sibling ML event detector on different signature (mIAW vs ICME); shares the event-disjoint split lesson.
- `[[paper-hu-2022-deep-swim-cnn-discontinuities]]` — sibling CNN on B-field discontinuities; smaller windows, finer scales.
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — unsupervised alternative; identifies structures without a labelled catalog.
- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — supervised but window-classification (not segmentation) reference.

## Notes

- The 20× training-speed claim is relative to a baseline architecture which the abstract names obliquely; identifying the baseline (likely an LSTM or earlier CNN ICME detector) is part of the verification gate.
- Operationalising the detector for real-time use requires a chosen probability threshold; the paper's "TSS = 0.64" likely corresponds to an optimised threshold — do not transplant the same threshold to a different feature set.
