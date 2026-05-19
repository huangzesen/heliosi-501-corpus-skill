---
name: cipher-2025-isax-hdbscan-solar-wind-segmentation
description: >-
  Use when mining solar-wind time series for recurrent structures using a CIPHER-style
  pipeline that chains iSAX symbolic compression, HDBSCAN density clustering, and a
  human-in-the-loop validation step — central paper claim is that CIPHER is a scalable
  unsupervised time-series analysis pipeline applied to solar-wind phenomena, with iSAX
  + HDBSCAN + HITL as the load-bearing combination (arXiv:2510.21022, 2025; full author
  list and venue TODO verify).
version: 0.1.0
tags: [machine-learning, unsupervised, time-series-mining, isax, hdbscan, hitl, solar-wind, segmentation, scalable]
quality_level: pilot
executable_status: scaffold
---

# CIPHER 2025 — iSAX + HDBSCAN + HITL Solar-Wind Time-Series Mining

> Compiled from arXiv:2510.21022 (*CIPHER: Scalable Time Series Analysis for Physical Sciences with Application to Solar Wind Phenomena*, 2025; full author list and venue TODO verify).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. iSAX cardinality / word length, HDBSCAN min-cluster-size, and the human-validation rubric require the full text.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Mining a **large solar-wind time-series corpus** (multi-year, multi-mission) for **recurrent shape motifs** without a labelled catalog.
- Acting as an **upstream unsupervised step** that proposes candidate structures for downstream supervised labelling (cf. [[paper-camporeale-2017-knn-solar-wind-categorization]], [[paper-bloch-2024-uncertainty-nn-solar-wind-types]]).
- Needing a **scalable** alternative to per-window deep models — iSAX is symbolic compression and HDBSCAN scales near-linearly.
- Inserting a **human-in-the-loop** validation layer for the cluster set before downstream science use.

Do NOT use this skill when:

- Pre-defined event labels exist — supervised ML is more efficient.
- Per-sample boundary detection is required ([[paper-rudisser-2022-icme-unet-automatic-detection]]).
- The target is **per-event physical attribution** — CIPHER produces clusters of shapes, not physical class labels.

## 2. Paper claim → verifiable task

**Claim (narrow form).** A pipeline combining iSAX symbolic compression, HDBSCAN density clustering, and a human-in-the-loop validation step is a scalable, unsupervised time-series analysis approach demonstrated on solar-wind phenomena. The headline scaling and the specific solar-wind phenomena identified are TODO verify.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reproduces the iSAX representation with the paper's word length and cardinality (TODO verify).
2. Runs HDBSCAN with the same min-cluster-size and min-samples (TODO verify); reproduces the cluster count within tolerance.
3. Replays the human-validation pass on the same intervals and reaches the same cluster acceptance rate (TODO verify).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — iSAX symbolic compression

- iSAX (indexable Symbolic Aggregate approXimation) collapses a real-valued window into a discrete word.
- Procedure:
  1. Choose word length w and cardinality c (TODO verify the paper's values).
  2. Standardise each window (z-score).
  3. PAA-reduce to w segments; quantile-bin each segment to one of c symbols.
- Output: per-window symbolic string.

### Algorithm 3.2 — HDBSCAN density clustering on iSAX words

- Procedure:
  1. Define a distance metric between iSAX words (MINDIST is standard; the paper's choice is TODO verify).
  2. Run HDBSCAN with min_cluster_size and min_samples (TODO verify).
  3. Output: per-window cluster id (or noise label −1).

### Algorithm 3.3 — Human-in-the-loop validation

- Procedure:
  1. Present cluster exemplars (medoids) to a human reviewer.
  2. Accept / reject / merge clusters based on physical plausibility.
  3. Re-label retained clusters with physical names if applicable.
- The paper's HITL protocol (UI, acceptance criteria, inter-reviewer agreement) is TODO verify.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once iSAX (w, c) and HDBSCAN params are pinned.
def cipher_pipeline(timeseries, window_len, w, c, min_cluster_size):
    windows = slide_windows(timeseries, window_len)
    isax_words = [isax(zscore(w), word_len=w, cardinality=c) for w in windows]
    cluster_ids = hdbscan(isax_words, min_cluster_size=min_cluster_size).labels_
    return cluster_ids, exemplars_per_cluster(windows, cluster_ids)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Solar-wind in-situ feature(s) | Vector or scalar per-window (V_sw, |B|, n_p, …) | L2 / derived | Mission window TODO verify | CDAWeb / SPDF / PSP SOC | `cdflib`; cf. [[paper-pyspedas-multimission-data-access]] |
| Optional ICME / CIR catalog | Event labels for HITL anchoring | derived | Same | Richardson–Cane / Möstl | n/a |

CIPHER is mission-agnostic in principle; the paper's specific mission (Wind / PSP / Solar Orbiter / OMNI) is TODO verify.

## 5. Validation target → benchmark artifact

- **Claim**: CIPHER is scalable + recovers identifiable solar-wind phenomena via unsupervised clustering with human validation.
- **Metric**: cluster count, cluster purity vs ground-truth catalog (when available), human-acceptance rate, wall-clock scaling.
- **Tolerance**: TODO verify.
- **Reference figure**: TODO verify — typical CIPHER-style figures show cluster medoids, dendrograms, and a confusion table against a labelled subset.

Recommended check artifacts:

- `cipher_clusters.csv` — per-window (t_start, t_end, isax_word, cluster_id, distance_to_medoid).
- A per-cluster medoid waveform panel.
- A scalability curve (wall-clock vs N windows).

## 6. Failure modes → skill memory

- **iSAX parameter sensitivity.** Word length w and cardinality c reshape the symbolic distance landscape; small changes can collapse / split clusters.
- **HDBSCAN noise label.** A large fraction of −1 (noise) often means the window length is wrong, not that the data are noise-dominated.
- **Z-score per window.** Removes amplitude information; physically distinct streams with the same *shape* will collapse into the same cluster. Decide whether amplitude matters.
- **Distance metric.** Euclidean on iSAX words, MINDIST, and DTW give different results; the paper's choice is load-bearing.
- **HITL bias.** Human acceptance reflects reviewer priors; require multi-reviewer agreement and report inter-rater κ.
- **Scalability vs interpretability.** iSAX is fast but lossy; high cardinality recovers detail at the cost of cluster count.
- **Mission-specificity.** Patterns learned on one mission do not transfer without re-clustering.

## 7. Claim boundary

**In scope.** Unsupervised iSAX + HDBSCAN clustering with HITL validation of solar-wind time-series windows.

**Out of scope — do NOT generalise beyond:**

- Per-sample segmentation (CIPHER is per-window).
- Physical attribution of clusters without an explicit human validation step.
- Cross-mission transfer of cluster labels without re-clustering.
- Real-time streaming inference — the inventory abstract emphasises *scalable* offline analysis.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2510.21022
- ADS: TODO verify.
- Code: TODO verify — CIPHER-class pipelines typically have public reference implementations.
- Data: depends on the mission used by the paper (TODO verify).

## 9. Skill graph → depends_on

- `[[paper-koikkalainen-2025-complexity-solar-wind-streams]]` — complementary unsupervised approach using information-theory complexity features.
- `[[paper-regan-2026-mars-solar-wind-ml-classification]]` — unsupervised PCA + K-Means alternative at Mars.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — supervised event-detector contrast for ICMEs.
- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — supervised label feed for HITL anchoring.

## Notes

- The HITL component is what makes CIPHER more than another unsupervised pipeline; benchmarking without HITL changes the claim entirely.
