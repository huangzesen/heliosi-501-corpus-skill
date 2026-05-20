---
name: hu-2022-deep-swim-cnn-discontinuities
description: >-
  Use when running Deep-SWIM, a semi-supervised CNN pipeline that classifies
  5-minute Wind/MFI magnetic-field windows (3s-resampled, B_x/B_y/B_z stacked
  as channels) as discontinuity vs ambient solar wind. Central paper claim: a
  four-layer 1D-CNN trained with contrastive learning + pseudo-labeling +
  Online Hard Example Mining (OHEM) reaches AUC ≈ 0.90 on the held-out
  validation set and precision 0.52 / recall 0.73 / AUC 0.82 on a one-day
  expert-hand-labelled test set (2018-11-18), under heavy class imbalance
  (~15 % discontinuity-positive windows). NeurIPS 2021 Machine Learning and
  the Physical Sciences workshop (Lamdouar et al. 2022, arXiv:2203.01184).
  Note: the slug retains a legacy first-author placeholder; the verified lead
  author is Hala Lamdouar (University of Oxford), not Hu.
version: 0.1.0
tags: [machine-learning, cnn, contrastive-learning, pseudo-labeling, ohem, solar-wind, discontinuity, current-sheet, wind-mfi, classification]
quality_level: paper-grounded-pending-full-text
executable_status: scaffold
paper:
  authors_verified: true
---

# Deep-SWIM (Lamdouar et al.) 2022 — Semi-Supervised CNN for Wind-Spacecraft B-Field Discontinuities

> Compiled from Lamdouar et al. (2022), *Deep-SWIM: A few-shot learning
> approach to classify Solar WInd Magnetic field structures*,
> arXiv:2203.01184, **NeurIPS 2021 Fourth Workshop on Machine Learning and
> the Physical Sciences**. Authors, abstract, data source (Wind MFI,
> 11 Hz → resampled to 3 s, 5-min windows), label provenance (one day of
> expert hand-labels for 2018-11-18 + a heuristic rotation-angle catalog
> covering 2006–2021 provided by co-authors Szabo and Narock), pipeline
> components (contrastive learning, pseudo-labeling with epoch-scheduled
> weight `α(t)` with `α_f = 3`, `T_1 = 5`, `T_2 = 100`; OHEM with
> `ω = 0.8`), and headline metrics (AUC 0.90 on validation, AUC 0.82 with
> precision 0.52 / recall 0.73 on the hand-labelled day) were verified
> against the arXiv abs page and the full PDF on 2026-05-19. The legacy
> slug "hu-2022" is preserved for cross-batch link stability.
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic
> anchors, data + labels, pipeline structure, and headline numbers verified.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Building a **per-window binary classifier** (discontinuity vs ambient turbulence) on **5-minute Wind/MFI** B-field windows (`B_x, B_y, B_z` stacked as 3 channels).
- Working with a **very small expert-labelled set** (a single day) plus a noisy heuristic catalog — Deep-SWIM is explicitly a semi-supervised pipeline that combines pseudo-labeling and contrastive learning to compensate.
- Pre-processing for downstream **coherent-structure / current-sheet** statistics (compare with PVI from [[pecora-2022-coherent-structures-proton-electron-heating]] in the turbulence batch).
- Needing a CNN baseline to compare against unsupervised approaches ([[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]).

Do NOT use this skill when:

- Detecting **large-scale** structures (ICMEs, multi-hour shocks) — Deep-SWIM windows are 5 min and miss multi-hour events.
- Producing **per-sample** segmentation — Deep-SWIM is window-level binary classification.
- Needing physical sub-labels (rotational discontinuity vs tangential vs ED) — Deep-SWIM is binary discontinuity-vs-ambient.
- Working on PSP near-Sun encounters — the model is Wind-trained and is not validated for the inner-heliosphere distribution.

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the workshop paper).** A four-layer
**1D-CNN** consuming 5-minute Wind/MFI windows with the three components
`(B_x, B_y, B_z)` stacked as input channels, **trained semi-supervised
with contrastive learning + pseudo-labeling + Online Hard Example Mining
(OHEM)**, classifies windows as discontinuity-positive vs ambient with
**AUC ≈ 0.90 on the held-out validation set**. On the single day of
expert-hand-labelled data (**2018-11-18**, 286 segments), the best model
reaches **precision 0.52, recall 0.73, AUC 0.82**. SVM baselines
(linear-kernel, with ORB features for images) and a 2D-CNN ResNet-18 on
Gramian-Angular-Field transforms are dominated by the 1D-CNN under
pseudo-labeling; for image inputs pseudo-labeling causes divergence.

**Verifiable task.** A reproduction succeeds when an agent:

1. Pulls Wind/MFI 11 Hz B (CDAWeb), removes 3 s instrument-rotation artefacts by smoothing + resampling to 3 s, and slides **5-minute windows** with `B_x, B_y, B_z` stacked as 3 channels.
2. Uses the May–July 2018 stratified sample described in §2 (20 % train ≈ 5 428 5 s segments supervised, 70 % unlabelled ≈ 18 492 segments for the semi-supervised stage, 10 % validation ≈ 2 576 segments) with the heuristic rotation-angle catalog as the noisy weak label and the **2018-11-18** expert-hand-labelled day (286 segments) as the held-out test set.
3. Trains a four-layer 1D-CNN with contrastive learning + pseudo-labeling + OHEM and recovers **AUC ≈ 0.90 on validation** and **(precision 0.52, recall 0.73, AUC 0.82) on 2018-11-18** within a small tolerance (the paper reports MAD across random seeds: MAD_precision ≈ 0.014, MAD_recall ≈ 0.000, MAD_AUC ≈ 0.003).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Windowing + label assembly

- Procedure:
  1. Pull Wind/MFI L2 B (GSE) at native 11 Hz from CDAWeb.
  2. Smooth and **resample to 3 s** to remove the 3 s rotation-period artefacts of the fluxgate magnetometer.
  3. Slide 5-minute windows (overlap policy TODO verify; the §2 reference to "5 s segments" of count 5 428 / 18 492 / 2 576 / 286 indicates the dataset is segmented at 5 s sub-units within the 5-min window).
  4. Assign binary labels from (a) **expert hand-labelling for one day, 2018-11-18** (286 segments with 39 discontinuities identified by hand, 24 shared with the heuristic catalog), and (b) **a non-ML heuristic rotation-angle catalog covering 2006–2021** provided by co-authors Adam Szabo and Ayris Narock (NASA Goddard).
  5. Class prior: only ≈ 15 % of 5-minute windows contain a discontinuity (heavy imbalance).
  6. Three-month sample (May–July 2018) used for the ablation study: 20 % supervised train, 70 % unlabelled for semi-supervised, 10 % validation; 2018-11-18 is the held-out final test set.

### Algorithm 3.2 — Channel-stacked input + the two compared modalities

- **Modality A (image / 2D-CNN baseline).** Convert each window to a Gramian Angular Field image and feed it to a ResNet-18 backbone. The paper finds this modality fails to converge once pseudo-labeling is added.
- **Modality B (time-series / 1D-CNN, the load-bearing pipeline).** Stack `(B_x, B_y, B_z)` as 3 channels into a four-layer 1D-CNN. This is the path that yields the headline AUC 0.90.

### Algorithm 3.3 — Semi-supervised pipeline (contrastive + pseudo + OHEM)

- **Contrastive learning.** Three simultaneous inputs to the model — anchor, positive, negative. The classification head is replaced with a fully-connected embedding head; a downstream classifier head is appended for fine-tuning.
- **Pseudo-labeling.** Predicted labels for unlabelled data are refreshed every epoch. Total loss `L_total = L_labelled + α(t) · L_unlabelled`, with `α(t)` piecewise linear:
  - `α(t) = 0` for `t < T_1 = 5`,
  - `α(t) = α_f · (t − T_1) / (T_2 − T_1)` for `T_1 < t < T_2 = 100`,
  - `α(t) = α_f = 3` for `t > T_2`.
- **OHEM.** `L_total = ω · L_OHEM + (1 − ω) · L_raw` with `ω = 0.8`, where `L_OHEM` is the loss on the top 70 % hardest examples.
- **Training details.** Adam optimiser, learning rate `1e-3`, batch size 16, single NVIDIA A100, ImageNet weights as init for the 2D-CNN.
- **SVM baseline.** Linear kernel, `γ = 1.0`, `c = 0.1` (chosen by AUC grid search); time-series SVM applied directly to the windowed data, image SVM uses ORB features.

Code skeleton (scaffold tier; pseudocode that matches the paper's hyperparameters):

```python
# Pseudocode aligned to the paper's reported pipeline (Lamdouar et al. 2022).
def deep_swim(timeseries, hand_catalog, heuristic_catalog):
    windows = slide_5min_windows(resample(timeseries, to_cadence_s=3))
    X = stack_components(windows)  # (N, 3, T) with T derived from 3 s cadence
    y_lab, y_heur = label_supervised_and_heuristic(windows, hand_catalog, heuristic_catalog)
    cnn = build_1d_cnn(layers=4)
    contrastive_pretrain(cnn, X_train_supervised, y_lab)
    train_with_pseudo_labels_and_ohem(
        cnn, X_train_supervised, y_lab, X_unlabelled,
        alpha_schedule={"alpha_f": 3, "T1": 5, "T2": 100},
        ohem_omega=0.8, ohem_top_frac=0.70,
        optimizer="adam", lr=1e-3, batch_size=16,
    )
    return evaluate(cnn, X_test_2018_11_18, hand_labels_2018_11_18)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Wind/MFI | B (GSE) | L2 11 Hz, smoothed to 3 s for Deep-SWIM | Three-month sample May–Jul 2018 (training) + 2018-11-18 (final test); heuristic catalog 2006–2021 | CDAWeb (https://cdaweb.gsfc.nasa.gov/) | `cdflib` |
| Expert hand-labels | discontinuity boundaries on 2018-11-18 (39 events) | derived | 2018-11-18 | Provided by Szabo & Narock per §2 footnote (TODO verify public release URL) | n/a |
| Heuristic rotation-angle catalog | weak labels (noisy positives) | derived | 2006–2021 | Provided by Szabo & Narock per §2 footnote (TODO verify public release URL) | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: Best model (B5: 1D-CNN + contrastive + pseudo-labeling + OHEM) reaches **AUC ≈ 0.90 on validation**; on the 2018-11-18 hand-labelled test set, **precision 0.52, recall 0.73, AUC 0.82**. Seed-variability MAD: MAD_precision ≈ 0.014, MAD_recall ≈ 0.000, MAD_AUC ≈ 0.003.
- **Metric**: per-window binary precision, recall, AUC on the 2018-11-18 hand-labelled test set; AUC on the 10 % validation set.
- **Tolerance**: ≤ 0.02 AUC drift relative to the paper's reported MAD across seeds; per-class precision / recall drift bounded by the paper's MAD figures.
- **Reference figure**: Figure 1 (pipeline schematic) and Figure 2 (true-negative / true-positive / false-positive examples on 2018-11-18); Table 1 (ablation A1–B7 across SVM/ResNet-18/1D-CNN).

Recommended check artifacts:

- `deepswim_predictions.csv` — per-window `(t_center, p_discontinuity, label_truth, source∈{hand,heuristic})`.
- A confusion matrix on the 2018-11-18 held-out day.
- The full ablation table A1–B7 reproduced (so reviewers can spot which component of the pipeline drives which metric delta).

## 6. Failure modes → skill memory

- **Catalog identity.** The heuristic rotation-angle catalog disagrees with the hand-labels on the one day where both exist (24 shared / 39 hand-labelled discontinuities — i.e., the heuristic finds a different subset). Downstream consumers should not treat the heuristic catalog as ground truth.
- **Frame choice (GSE).** The paper uses GSE components; cross-checking with RTN would require rotation and is not covered by the published model.
- **Class imbalance (~ 15 %).** Random per-window splits would dramatically inflate accuracy; the paper uses stratified sampling and reports macro-level metrics, but precision (0.52) remains modest even at recall 0.73.
- **GAF / image pipeline diverges with pseudo-labeling.** The paper specifically reports that 2D-CNN + pseudo-labeling **diverges**; consumers attempting an image-based replacement will hit the same trap.
- **Hand-labelled test set is a single day.** AUC 0.82 on 286 segments is a small-sample estimate; generalisation across cycles is not characterised by this paper alone.
- **PSP / inner-heliosphere transfer.** Discontinuity statistics differ between 1 au and inner-heliosphere; a Wind-trained model is not a PSP-near-Sun classifier.
- **3 s resampling discards sub-3-s structure.** The 3 s smoothing removes the magnetometer rotation artefact but also discards sub-second discontinuities; consumers needing those must change the preprocessing pipeline (and the labelling regime).

## 7. Claim boundary

**In scope.** Per-window binary classification (discontinuity vs ambient) on 5-minute, 3-s-resampled Wind/MFI B-field windows with the four-layer 1D-CNN + contrastive + pseudo-labeling + OHEM pipeline, evaluated against expert hand-labels for 2018-11-18.

**Out of scope — do NOT generalise beyond:**

- Per-sample segmentation — Deep-SWIM is window-level.
- Multi-class discontinuity type (RD vs TD vs ED) — binary unless explicitly retrained.
- Other in-situ structures (ICMEs, switchbacks, shocks at the scale of multiple windows).
- Other distance regimes (PSP near-Sun) without retraining.
- Sub-3-s scales (the 3-s resampling discards faster structure).
- Long-baseline operational use without periodic re-labelling — the paper's test set is one day.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: https://doi.org/10.48550/arXiv.2203.01184 (arXiv-issued; workshop paper has no separate DOI; the workshop archive PDF lives at `https://ml4physicalsciences.github.io/2021/files/NeurIPS_ML4PS_2021_138.pdf`).
- arXiv: https://arxiv.org/abs/2203.01184 (submission 2022-03-02).
- ADS: TODO verify (no bibcode posted at verification time).
- Code: TODO verify — the workshop PDF does not advertise a code repo URL.
- Data: Wind/MFI L2 via CDAWeb (public); heuristic catalog and hand-labels provided by co-authors Szabo & Narock (TODO verify public release URL).

## 9. Skill graph → depends_on

- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling ML approach on larger structures (ICMEs); shares the windowed-input lesson and the class-imbalance challenge.
- `[[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]` — sibling ML event detector on PSP burst-mode waveforms; shares the spectrogram-vs-raw representation choice and the small-labelled-set regime.
- `[[paper-pecora-2022-coherent-structures-proton-electron-heating]]` — physical coherent-structure detection via PVI (non-ML baseline; complementary to ML detection).
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — unsupervised time-series-mining alternative on the same in-situ class of problem.

## 10. Research-generation affordances

- **Catalog-disagreement diagnostic.** The single-day discrepancy (24/39 shared between heuristic and hand-labels) is a quantitative measure of catalog noise; a meta-analysis that re-runs Deep-SWIM with the heuristic catalog *as ground truth* and measures the AUC drop directly quantifies the noise penalty.
- **Multi-day hand-labelling.** Extending the hand-labelled test set from one day (286 segments) to a multi-cycle sample is the highest-information improvement available without changing the pipeline; the precision 0.52 number is the bottleneck the abstract calls out.
- **Cross-instrument transfer.** Re-training on ACE/MAG or Solar Orbiter/MAG and reporting the AUC delta directly tests how Wind-specific the rotation-angle preprocessing is.
- **Multi-class extension.** Sub-typing detected discontinuities into rotational vs tangential vs ED via a hierarchical classifier (Deep-SWIM as the gate, a downstream physical classifier on positives) would close the gap between window-level detection and the physical discontinuity taxonomy.

## Notes

- "Deep-SWIM" is the system name; the methods section pins the four-layer 1D-CNN + contrastive + pseudo-labeling + OHEM recipe with specific hyperparameters (`α_f = 3`, `T_1 = 5`, `T_2 = 100`, `ω = 0.8`, top-70 % OHEM, lr 1e-3, batch 16). These are load-bearing — substituting MAML or Prototypical Networks would change the pipeline class, not just tune hyperparameters.
- The slug `hu-2022-deep-swim-cnn-discontinuities` is a legacy artefact from an earlier inventory phase. The actual lead author is **Hala Lamdouar (University of Oxford)**, with co-authors at Intel Labs, U. Vienna, Colorado School of Mines, UCLA, UTFPR-Paraná, Harvey Mudd, SwRI, and NASA GSFC. The slug is preserved here only for cross-batch link stability; consumer-facing prose and the metadata `authors[]` list reflect the verified citation.
