---
name: camporeale-2017-knn-solar-wind-categorization
description: >-
  Use when applying a supervised KNN-style classifier to assign 1-au solar-wind intervals to
  one of four physical types (coronal-hole / streamer-belt / sector-reversal / ejecta) using a
  hand-engineered feature vector — central paper claim is that out of ten supervised models
  benchmarked, KNN reaches ~92.8% accuracy on a Xu & Borovsky-style 4-class scheme at 1 au
  (arXiv:1811.02323; the canonical companion to the Xu-Borovsky labelling tradition; venue / DOI TODO verify).
version: 0.1.0
tags: [machine-learning, supervised, knn, solar-wind-classification, 1au, ace, wind, four-class, xu-borovsky]
quality_level: pilot
executable_status: scaffold
paper:
  authors_verified: false
---

# Camporeale-style 2017/2018 — Supervised 4-Class Solar-Wind Categorization at 1 au (KNN)

> Compiled from the supervised-ML solar-wind categorisation literature catalogued at arXiv:1811.02323 (Camporeale, Carè, Borovsky et al., *Machine Learning Approach for Solar Wind Categorization*; venue / DOI TODO verify, likely JGR Space Physics).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. The exact feature list, the labelling rule (Xu–Borovsky), and per-model accuracy table require the full text.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Labelling 1-au in-situ solar-wind intervals (ACE / Wind) with a **4-class supervised** scheme: coronal-hole, streamer-belt-origin, sector-reversal, ejecta.
- Choosing among **standard supervised classifiers** (KNN, SVM, decision tree, MLP, …) for a heliophysics tabular dataset — this paper benchmarks ten and identifies KNN as the headline.
- Acting as a **baseline** against which more recent unsupervised (e.g., [[paper-regan-2026-mars-solar-wind-ml-classification]]) or uncertainty-aware (e.g., [[paper-bloch-2024-uncertainty-nn-solar-wind-types]]) pipelines are compared.

Do NOT use this skill when:

- The target is **near-Sun PSP** intervals — the 1-au labelling scheme does not transfer.
- The dataset has no ground-truth labels — go unsupervised ([[paper-regan-2026-mars-solar-wind-ml-classification]], [[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]).
- Per-event boundary detection is required (this is window classification, not segmentation; see [[paper-rudisser-2022-icme-unet-automatic-detection]]).

## 2. Paper claim → verifiable task

**Claim (narrow form).** A supervised K-Nearest-Neighbours classifier trained on a hand-engineered 1-au solar-wind feature vector and labelled per the Xu–Borovsky 4-class scheme achieves approximately **92.8% accuracy** on a held-out test set, outperforming nine other standard supervised models in the same benchmark.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reconstructs the same 4-class labelled dataset (TODO verify the exact source — ACE OMNI-based feature vectors are typical).
2. Trains KNN with the paper's K and distance metric (TODO verify).
3. Reproduces the headline accuracy within tolerance (TODO verify the paper's tolerance).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Xu–Borovsky 4-class labelling

- Procedure:
  1. Pull ACE (or OMNI / Wind) 1-au in-situ moments + magnetic field at the cadence the paper uses (TODO verify; OMNI 1-hour averages are standard).
  2. Apply the Xu–Borovsky labelling rule (Xu & Borovsky 2015) — typically thresholds on |B|/√n_p, T_p/T_exp, V_sw, etc. to assign one of {coronal-hole, streamer-belt-origin, sector-reversal, ejecta}.
  3. The paper inherits this labelling rather than relearning it; the exact thresholds are inherited from Xu–Borovsky and the paper's specific cutoffs are TODO verify.

### Algorithm 3.2 — Feature vector

- Standard features (exact list TODO verify):
  - V_sw, n_p, T_p, |B|.
  - Derived: T_p/T_exp, |B|/√n_p, plasma β, V_A, sound speed, magnetic-field rotation rate.
  - Optional: alpha-to-proton ratio N_α/N_p, charge-state composition (if SWICS is used).

### Algorithm 3.3 — Multi-model benchmark + KNN tuning

- Procedure:
  1. Split (TODO verify split fractions; standard 70/15/15 or chronological is plausible).
  2. Benchmark the ten models: KNN, SVM (linear + RBF), decision tree, random forest, gradient boosting, logistic regression, MLP, naive Bayes, LDA, QDA. The exact list is TODO verify.
  3. Tune KNN (K, distance metric) via cross-validation on the training set.
  4. Evaluate per-class precision / recall / F1 on the test set.

### Algorithm 3.4 — Confusion matrix interpretation

- The Xu–Borovsky classes are not symmetric: streamer-belt vs sector-reversal often confuse because they share intermediate-velocity / intermediate-density signatures. A reproduction must report the full confusion matrix, not only the headline accuracy.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once feature list, K, and split are pinned.
def camporeale2017_knn(features_df, labels):
    X, y = features_df.to_numpy(), labels.to_numpy()
    X_train, X_test, y_train, y_test = chrono_split(X, y)         # TODO verify
    knn = KNeighborsClassifier(n_neighbors=K_paper, metric="paper_metric")
    knn.fit(X_train, y_train)
    return classification_report(y_test, knn.predict(X_test)), confusion_matrix(...)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| ACE SWEPAM | n_p, V_sw, T_p | L2 | ~1998 – present | CDAWeb / SPDF | `cdflib` |
| ACE MAG | B (GSE) | L2 | Same | CDAWeb / SPDF | `cdflib` |
| ACE SWICS | charge-state composition (optional) | L2 | Same | CDAWeb / SPDF | `cdflib` |
| OMNI | 1-h merged 1-au feature set | L2 derived | Same | OMNIWeb | `cdflib` |
| Xu–Borovsky labels | 4-class labelled intervals | derived | Same | Xu & Borovsky 2015 supplementary / regenerated | TODO verify the label source |

## 5. Validation target → benchmark artifact

- **Claim**: KNN achieves ~92.8% overall accuracy across the 4-class Xu–Borovsky scheme on a 1-au benchmark.
- **Metric**: top-1 accuracy on a held-out test set.
- **Tolerance**: TODO verify (no tolerance stated in the inventory abstract).
- **Reference figure**: TODO verify — likely a comparison bar chart + confusion matrix.

Recommended check artifacts:

- `camporeale2017_predictions.csv` — per-window (t, feature_vector, label_truth, label_predicted, model).
- A full confusion matrix per model.
- A bar chart of all-model accuracies for direct comparison with the paper's table.

## 6. Failure modes → skill memory

- **Label rule inheritance.** Xu–Borovsky thresholds were tuned on solar-cycle-23 data; applying them unmodified to cycle-25 intervals can drift class boundaries. The paper's training window matters.
- **Class imbalance.** Ejecta are a tiny minority class; raw accuracy hides poor ejecta recall. Always report macro-F1 alongside accuracy.
- **Feature normalisation.** KNN is distance-based; un-normalised features will be dominated by V_sw and |B|.
- **Distance-metric choice.** Euclidean vs cosine vs Mahalanobis change KNN behaviour substantially; the paper's choice is TODO verify.
- **K selection.** The headline accuracy depends on K; the paper's K is TODO verify.
- **OMNI vs raw ACE.** OMNI is propagation-corrected and resampled; the paper's exact source matters.
- **Cross-cycle generalisation.** Models trained on a single solar cycle often fail across cycles; a benchmarked promotion should report cross-cycle accuracy.

## 7. Claim boundary

**In scope.** Supervised 4-class solar-wind categorisation at 1 au using the Xu–Borovsky labelling scheme on ACE / OMNI features; KNN as the top-1 model among ten benchmarked.

**Out of scope — do NOT generalise beyond:**

- Distances other than ~1 au.
- Labelling schemes other than Xu–Borovsky 4-class (e.g., the 7-class Stansby scheme; or unsupervised regimes from [[paper-regan-2026-mars-solar-wind-ml-classification]]).
- Per-event boundary detection — this is window classification.
- Causal physical attribution — KNN is a similarity classifier, not a physical model.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/1811.02323
- ADS: TODO verify.
- Code: TODO verify.
- Data: ACE / OMNI L2 (public).

## 9. Skill graph → depends_on

- `[[paper-bloch-2024-uncertainty-nn-solar-wind-types]]` — successor with uncertainty estimation, same labelling tradition.
- `[[paper-regan-2026-mars-solar-wind-ml-classification]]` — unsupervised contrast.
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — symbolic-clustering alternative.
- `[[paper-koikkalainen-2025-complexity-solar-wind-streams]]` — information-theory features for the same problem.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — per-sample segmentation for one of the four classes (ejecta).

## Notes

- The Xu–Borovsky labelling rule (Xu & Borovsky 2015) is the load-bearing prerequisite for this skill; if a future agent intends to retrain at non-1-au distances, the labelling rule must be relearned, not merely transferred.
- The "ten models benchmarked" claim implies a table that should be reproduced verbatim before any benchmarked-tier promotion.
