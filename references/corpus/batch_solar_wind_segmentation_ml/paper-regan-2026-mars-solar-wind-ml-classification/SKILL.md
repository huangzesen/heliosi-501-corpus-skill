---
name: regan-2026-mars-solar-wind-ml-classification
description: >-
  Use when classifying upstream MAVEN solar-wind intervals at Mars into recurrent regimes
  via unsupervised PCA + K-Means (K=4) and tracking how regime occurrence is modulated by
  solar activity across Cycles 24-25 — central claim is that the pipeline recovers slow /
  fast / intermediate / compressed regimes whose occurrence is strongly modulated by solar
  activity (Regan et al. 2026, arXiv:2604.08710; venue TODO verify).
version: 0.1.0
tags: [machine-learning, unsupervised, pca, kmeans, solar-wind-classification, mars, maven, solar-cycle, segmentation]
quality_level: pilot
executable_status: scaffold
---

# Regan 2026 — Solar Wind Classification at Mars via PCA + K-Means (MAVEN)

> Compiled from Regan, C. E. et al. (2026), *Solar Wind Classifications at Mars using Machine Learning Techniques*, arXiv:2604.08710 (Heliophysics Summer School ML Special Collection; venue TODO verify).
> **Quality tier**: `pilot scaffold` — claims are anchored to the arXiv abstract in the source inventory. Numerical thresholds, the exact feature list, and per-cluster occurrence fractions require the full PDF before promotion.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Building an **unsupervised classifier** for solar-wind regimes upstream of Mars using **MAVEN** plasma + magnetic-field moments over Solar Cycles 24–25.
- Re-using a **PCA → K-Means** template on any single-spacecraft multi-feature solar-wind dataset where labels are not available.
- Quantifying how **regime occurrence depends on solar activity** at non-1-au heliocentric distances (Mars at ~1.38–1.67 au).
- Choosing between **supervised vs. unsupervised** solar-wind classification: this paper is the canonical unsupervised reference at Mars.

Do NOT use this skill when:

- Classifying **PSP near-Sun encounter** data (different parameter regime; see [[paper-camporeale-2017-knn-solar-wind-categorization]] for supervised 1-au).
- The required outcome is **physical-source labelling** (coronal hole / streamer belt / sector reversal / ejecta) rather than data-driven clustering — supervised labels require source-region heuristics.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Applied to a normalised multi-dimensional MAVEN upstream-solar-wind dataset spanning Solar Cycles 24–25, an unsupervised pipeline of Principal Component Analysis followed by K-Means clustering recovers **four** physically interpretable regimes — slow, fast, intermediate, and compressed solar wind — whose relative occurrence and temporal organisation are strongly modulated by solar activity.

**Verifiable task.** A reproduction succeeds when an agent:

1. Builds the normalised feature vector from MAVEN upstream intervals (TODO verify the exact feature list; the abstract lists "multi-dimensional" but does not enumerate).
2. Runs PCA, retains the principal components stated in the paper (TODO verify number of components and explained-variance threshold).
3. Runs K-Means with K=4 (per the paper's central claim) and obtains four clusters that map to slow / fast / intermediate / compressed.
4. Reproduces the **occurrence-vs-solar-activity** modulation reported (TODO verify exact occurrence fractions and the solar-activity proxy used — F10.7 / SSN / heliospheric current sheet tilt).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Upstream-solar-wind interval extraction at Mars (MAVEN)

- Paper reference: methods section — TODO verify section number and the upstream-flag definition.
- Procedure:
  1. Pull MAVEN SWIA on-board moments (n_p, V_sw, T_p) and MAG L2 (B_RTN) over the mission window covering Solar Cycles 24–25.
  2. Apply an upstream filter that excludes magnetosheath / induced magnetosphere / wake intervals. Standard MAVEN approaches use a model bow-shock + spacecraft-position cut; the paper's exact filter and bow-shock model are TODO verify.
  3. Down-sample / window-average to the cadence used by the paper (TODO verify, often 4-min or 1-hour upstream averages).

### Algorithm 3.2 — Feature normalisation + PCA

- Procedure:
  1. Build the per-interval feature vector. Candidate features (from heliophysics ML practice; exact list TODO verify): n_p, V_sw, T_p, |B|, V_A, sound speed, plasma β, T_p/T_exp, |B|/√n_p, etc.
  2. Normalise each feature (z-score or min-max — TODO verify).
  3. Fit PCA on the normalised matrix; retain top components capturing the variance threshold stated in the paper.

### Algorithm 3.3 — K-Means clustering with physical post-labelling

- Procedure:
  1. Run K-Means with K=4 on the PCA-reduced features. Use deterministic seeding (e.g., `random_state` fixed) for reproducibility.
  2. Inspect per-cluster centroids in the original feature space; assign physical labels (slow / fast / intermediate / compressed) by manual mapping — the paper does *not* claim K is learned, it is set to 4.
  3. (Stability check, recommended even if absent from the paper.) Repeat with multiple seeds and report cluster-assignment consistency (e.g., Rand index across seeds).

### Algorithm 3.4 — Solar-activity-modulated occurrence statistics

- Procedure:
  1. Bin time by a solar-activity proxy (TODO verify — F10.7, sunspot number, or solar-cycle phase).
  2. Compute the relative occurrence of each cluster per bin.
  3. Report the modulation pattern (e.g., increased "compressed" fraction near solar maximum is a typical finding; verify against the paper).

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once feature list + filter are pinned.
def regan2026_classify_maven(features_df, k=4):
    X = standardise(features_df)            # 3.2 step 2
    pcs = PCA(n_components="paper_value").fit_transform(X)  # TODO verify n_components
    labels = KMeans(n_clusters=k, random_state=0).fit_predict(pcs)
    return labels  # post-map to {slow, fast, intermediate, compressed}
```

## 4. Data / instruments → tool contracts

Each row below is rendered as a tool contract. Named MCPs are NOT assumed to exist; the general-purpose harness (Read, Bash, WebFetch + cdflib / pytplot / pyspedas) is the guaranteed surface.

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| MAVEN SWIA | n_p, V_RTN, T_p (on-board moments) | L2, ~4 s native | Mission start (2014-09) – present, Solar Cycles 24–25 | NASA PDS / SPDF | `cdflib` via SPDF/CDAWeb; cf. [[paper-pyspedas-multimission-data-access]] |
| MAVEN MAG | B_RTN | L2, 32 Hz native (decimated for upstream) | Same window | NASA PDS / SPDF | Same |
| Upstream-flag derived | bow-shock-excluded times | derived | Same window | n/a (compute) | Bow-shock model + position cut; **exact model TODO verify** |
| Solar-activity proxy | F10.7 / SSN / cycle phase | daily | Same window | LISIRD / SILSO | WebFetch |

Theory-only? No — this is a pure data-driven pipeline; no in-situ data ⇒ no skill.

## 5. Validation target → benchmark artifact

- **Claim**: An unsupervised PCA + K-Means (K=4) pipeline recovers slow / fast / intermediate / compressed regimes whose occurrence varies systematically with solar activity.
- **Metric**: (a) Per-cluster centroid (V_sw, n_p, T_p, |B|) consistent with each regime's canonical signatures; (b) Pearson / rank correlation between per-cluster occurrence fraction and the solar-activity proxy.
- **Tolerance**: TODO verify in the full paper. At minimum, the four-cluster solution must qualitatively recover the slow/fast/intermediate/compressed centroids; quantitative thresholds need full-text confirmation.
- **Reference figure**: TODO verify — the abstract mentions "distinct" regimes; the figure(s) showing the four-cluster centroids + occurrence-vs-time must be identified.

Recommended check artifacts:

- `regan2026_maven_clusters.csv` — one row per upstream interval: (t_start, t_end, n_p, V_sw, T_p, |B|, PC1, PC2, cluster_id, physical_label).
- `regan2026_occurrence_by_cycle.csv` — per-month occurrence fractions of each cluster + F10.7 (or chosen proxy).
- One scalar QC: silhouette score for K=4; one stability QC: Rand index across multiple seeds.

## 6. Failure modes → skill memory

- **Magnetosheath contamination.** Upstream-flag mis-classification (bow-shock crossings, induced-magnetosphere intervals) leaks plasma states into the "compressed" cluster. The exact upstream-filter the paper uses is TODO verify; reviewers must pin the bow-shock model.
- **K must be chosen, not learned.** K-Means assumes K; the paper sets K=4 by hand. An agent must not silently substitute K=3 or K=5 without re-validating cluster physicality.
- **Feature normalisation matters.** PCA is variance-driven; failing to standardise will overweight |B| or T_p depending on units.
- **PCA component count.** Retaining too few PCs collapses the intermediate cluster; retaining too many resurrects measurement noise. The paper's chosen component count is load-bearing and TODO verify.
- **K-Means initialisation sensitivity.** Single-seed runs may rotate labels. Always run multiple seeds and report consistency.
- **Solar-cycle coverage.** MAVEN started in late Cycle 24; cycle-phase comparisons are sensitive to the start-of-cycle definition. Document the cycle-boundary convention used.
- **Mars vs. 1-au regimes are different.** Compressed regimes at Mars are amplified by stream interactions over the additional ~0.5 au of propagation; agents must not transplant the same cluster definitions back to 1 au — see [[paper-camporeale-2017-knn-solar-wind-categorization]] for the 1-au supervised analogue.

## 7. Claim boundary

**In scope.** Unsupervised PCA + K-Means (K=4) classification of MAVEN upstream solar-wind intervals over Solar Cycles 24–25 at Mars (~1.38–1.67 au), with per-cluster occurrence modulated by solar activity.

**Out of scope — do NOT generalise beyond:**

- 1-au or near-Sun solar wind (PSP / Wind / ACE / Solar Orbiter at different distances).
- Supervised classification with physical-source labels — Regan 2026 is explicitly unsupervised.
- K ≠ 4 cluster solutions without re-establishing physical correspondence.
- ICME / CIR event-level segmentation (cluster regimes are statistical, not per-event boundaries) — see [[paper-rudisser-2022-icme-unet-automatic-detection]] for event detection.

If a downstream task asks for a generalisation listed above, refuse it and route to the sibling paper-skill that covers it (or report none).

## 8. Links

- DOI: TODO verify (preprint via Heliophysics Summer School ML Special Collection).
- arXiv: https://arxiv.org/abs/2604.08710
- ADS: TODO verify.
- Code: n/a — no public repo cited in the inventory.
- Data: MAVEN SWIA + MAG L2 via NASA PDS / SPDF (public).

## 9. Skill graph → depends_on

- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — supervised 4-class 1-au counterpart; the *physical* slow / fast / sector-reversal / ejecta labelling tradition starts there. Regan 2026 differs by being unsupervised and at Mars.
- `[[paper-bloch-2024-uncertainty-nn-solar-wind-types]]` — uncertainty-quantified NN classification at 1 au; sibling pipeline-design contrast.
- `[[paper-pyspedas-multimission-data-access]]` — MAVEN data ingestion contract (infrastructure, in `batch_heliophysics_software_infrastructure/`).
- `[[paper-koikkalainen-2025-complexity-solar-wind-streams]]` — complementary information-theory-based stream classification (different feature space).

## Notes

- The paper is part of the *Heliophysics Summer School Machine Learning Special Collection*; if the special collection's editorial DOI block becomes available, promote venue and DOI together rather than separately.
- The bow-shock exclusion logic is the highest-impact reproducibility detail and must be verified against the paper's methods section before any benchmarked claim.
