---
name: bloch-2024-uncertainty-nn-solar-wind-types
description: >-
  Use when applying neural-network classifiers with calibrated per-prediction uncertainty
  to assign 1-au solar-wind intervals to four physical types (coronal hole, streamer belt,
  sector reversal, solar transients) — central paper claim is that NN classifiers with
  uncertainty estimation produce per-interval class probabilities + confidence bounds for
  the standard 4-class 1-au labelling scheme (arXiv:2409.09230; full author list and venue
  TODO verify).
version: 0.1.0
tags: [machine-learning, neural-network, solar-wind-classification, uncertainty-quantification, four-class, 1au]
quality_level: pilot
executable_status: scaffold
paper:
  authors_verified: false
---

# Bloch-style 2024 — Uncertainty-Aware NN Classification of 1-au Solar-Wind Types

> Compiled from arXiv:2409.09230 (*Classifying different types of solar wind plasma with uncertainty estimations using machine learning*; full author list, lead author surname, and venue TODO verify — inventory lists the arXiv abstract only).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. NN architecture, the uncertainty method (Monte-Carlo dropout / deep ensembles / Bayesian last-layer / evidential), per-class precision-recall, and the calibration metric require the full text.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Producing **per-interval class probabilities with calibrated uncertainty** for the 4-class 1-au solar-wind labelling scheme (coronal hole, streamer belt, sector reversal, solar transients).
- Needing to **abstain on low-confidence intervals** rather than force a label — KNN-style classifiers (cf. [[paper-camporeale-2017-knn-solar-wind-categorization]]) do not natively expose calibrated uncertainty.
- Coupling solar-wind class probabilities downstream to a **risk-aware space-weather product** that needs uncertainty as input.

Do NOT use this skill when:

- The downstream product is a binary or event-level decision (use [[paper-rudisser-2022-icme-unet-automatic-detection]] for ICME segmentation).
- No labelled training set exists — go unsupervised ([[paper-regan-2026-mars-solar-wind-ml-classification]], [[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]).
- Working at near-Sun PSP distances — the 1-au labelling does not transfer.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Neural-network classifiers trained on a 1-au solar-wind feature vector and labelled with the 4-class scheme (coronal hole, streamer belt, sector reversal, solar transients) produce per-interval class probabilities together with **calibrated uncertainty estimates**, enabling abstention or downstream uncertainty propagation. The specific uncertainty method and calibration metric are TODO verify.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reconstructs the 4-class labelled set (TODO verify whether Xu–Borovsky 2015 or Stansby labels are used).
2. Trains the same NN architecture (TODO verify) with the paper's uncertainty method (TODO verify).
3. Recovers per-class accuracy within tolerance (TODO verify) **and** the reported calibration metric (e.g., Expected Calibration Error, Brier score — TODO verify which).
4. Demonstrates the abstention curve (accuracy vs coverage) reported by the paper.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Labelled-data assembly (1-au, 4-class)

- Procedure:
  1. Pull ACE / OMNI / Wind 1-au moments + B at the cadence the paper uses (TODO verify).
  2. Apply the labelling rule (TODO verify whether Xu–Borovsky 4-class or Stansby / Owens). The label classes named in the abstract ("coronal hole, streamer belt, sector reversal, solar transients") are the Xu–Borovsky tradition.
  3. Hold out a chronologically blocked test set for unbiased calibration evaluation.

### Algorithm 3.2 — Feature engineering

- Same per-interval features as [[paper-camporeale-2017-knn-solar-wind-categorization]] (V_sw, n_p, T_p, |B|, derived ratios). The paper's exact list is TODO verify.

### Algorithm 3.3 — NN architecture + uncertainty method

- Procedure:
  1. Build the NN classifier (architecture TODO verify — likely MLP, possibly with class-balanced loss).
  2. Apply the chosen uncertainty method (TODO verify — common options: MC-Dropout (predictive entropy from T forward passes); Deep Ensembles (5–10 NNs); Bayesian last-layer; evidential / Dirichlet-prior output).
  3. Output per-interval (p_coronal_hole, p_streamer_belt, p_sector_reversal, p_transient, uncertainty_score).

### Algorithm 3.4 — Calibration evaluation + abstention curve

- Procedure:
  1. Compute reliability diagram on the test set; report Expected Calibration Error (ECE) and Brier score (TODO verify which the paper uses).
  2. Sweep an uncertainty threshold; plot accuracy vs coverage (the "abstention curve"). Report the operating point the paper highlights.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once architecture + uncertainty method are pinned.
def bloch2024_nn_with_uncertainty(features, labels, method="mc_dropout"):
    nn = build_classifier_with_uncertainty(method)
    nn.fit(X_train, y_train)
    p_class, u = nn.predict_with_uncertainty(X_test)  # u = predictive entropy or ensemble var
    return compute_ece(p_class, y_test), abstention_curve(p_class, u, y_test)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| ACE SWEPAM | n_p, V_sw, T_p | L2 | window TODO verify | CDAWeb / SPDF | `cdflib` |
| ACE MAG | B (GSE) | L2 | Same | CDAWeb / SPDF | `cdflib` |
| OMNI (optional) | 1-h merged 1-au features | L2 derived | Same | OMNIWeb | `cdflib` |
| Xu–Borovsky / Stansby labels | 4-class labels | derived | Same | Catalog source TODO verify | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: NN classifier provides per-interval 4-class probabilities + calibrated uncertainty (calibration metric value TODO verify).
- **Metric**: ECE / Brier (TODO verify which); accuracy at full coverage; accuracy-vs-coverage curve under abstention.
- **Tolerance**: TODO verify.
- **Reference figure**: TODO verify — likely a reliability diagram + abstention curve.

Recommended check artifacts:

- `bloch2024_predictions.csv` — per-interval (t, feature_vector, p_class[4], uncertainty, label_truth).
- A reliability diagram (predicted-probability vs empirical accuracy).
- An abstention curve panel.

## 6. Failure modes → skill memory

- **Over-confidence under distribution shift.** NN softmax is poorly calibrated by default; a "calibrated" model on the training cycle may still over-confidently mis-label cross-cycle intervals.
- **MC-Dropout is not a free Bayesian posterior.** If MC-Dropout is the chosen method, the dropout rate matters and the predictive entropy is only a proxy.
- **Class imbalance.** Transients are rare; un-weighted training collapses to majority classes and inflates accuracy.
- **Calibration ≠ accuracy.** A model can be well-calibrated and still inaccurate; report both.
- **Test-set leakage.** Chronological blocking is essential; random splits inflate calibration scores.
- **Label noise.** Xu–Borovsky / Stansby labels have ~5–10% disagreement near class boundaries; this is an irreducible noise floor.

## 7. Claim boundary

**In scope.** Per-interval 4-class supervised classification of 1-au solar-wind intervals with calibrated uncertainty estimates.

**Out of scope — do NOT generalise beyond:**

- Distances other than 1 au.
- Labelling schemes other than the 4-class Xu–Borovsky / Stansby tradition.
- Out-of-distribution detection without re-validation — calibration is *in-distribution* by default.
- Per-event boundary detection.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2409.09230
- ADS: TODO verify.
- Code: TODO verify.
- Data: ACE / OMNI L2 (public).

## 9. Skill graph → depends_on

- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — predecessor (no uncertainty); shares feature engineering.
- `[[paper-regan-2026-mars-solar-wind-ml-classification]]` — unsupervised alternative at Mars.
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — symbolic-clustering alternative; provides a different uncertainty proxy via cluster-assignment entropy.
- `[[paper-koikkalainen-2025-complexity-solar-wind-streams]]` — feature-side enhancement (information-theory complexity).

## Notes

- The "uncertainty method" identity is the single highest-impact reproducibility detail — MC-Dropout, ensembles, evidential, and Bayesian last-layer differ in calibration behaviour and computational cost.
- The class "solar transients" subsumes ICMEs but is broader; do not treat the transient class as a drop-in replacement for [[paper-rudisser-2022-icme-unet-automatic-detection]] segmentation output.
