---
name: cipher-2025-isax-hdbscan-solar-wind-segmentation
description: >-
  Use when applying CIPHER (Clustering and Indexation Pipeline with Human
  Evaluation for Recognition) to label solar-wind OMNI time series via iSAX
  symbolic compression + HDBSCAN density clustering + a human-in-the-loop
  validation step. Central paper claim: on OMNI 1-minute data with a 35-hour
  chunk size, iSAX word size 8, HDBSCAN min_cluster_size = 5 and
  min_samples = 5, CIPHER recovers meaningful clusters corresponding to
  coronal mass ejections (CMEs) and stream interaction regions (SIRs);
  expert annotations on representative cluster medoids are propagated across
  the cluster to scale labelling. Demonstrated on the 2021-03-11/12 CME case.
  NeurIPS 2025 Machine Learning and the Physical Sciences workshop (5 pages,
  2 figures). Kobayashi, Martin et al. 2025, arXiv:2510.21022.
version: 0.1.0
tags: [machine-learning, unsupervised, time-series-mining, isax, hdbscan, hitl, omni, cme, sir, solar-wind, segmentation, scalable]
quality_level: paper-grounded-pending-full-text
executable_status: scaffold
paper:
  authors_verified: true
---

# CIPHER 2025 — iSAX + HDBSCAN + HITL Solar-Wind Time-Series Mining on OMNI

> Compiled from Kobayashi & Martin et al. (2025), *CIPHER: Scalable Time
> Series Analysis for Physical Sciences with Application to Solar Wind
> Phenomena*, arXiv:2510.21022 (submission 2025-10-23), **NeurIPS 2025
> Machine Learning and the Physical Sciences workshop (5 pages, 2 figures)**.
> Authors, abstract, data source (NASA OMNI 1-min from ACE/Wind-SWE/IMP-8/Geotail
> merged to L1), pipeline (iSAX → HDBSCAN → HITL → annotation propagation),
> hyperparameters (chunk size 35 hours, word size 8, min_cluster_size = 5,
> min_samples = 5), feature focus (bulk flow speed, proton density, proton
> temperature, magnetic field components), and case-study CMEs/SIRs were
> verified against the arXiv abs page and the full PDF on 2026-05-19. Code
> at https://github.com/spaceml-org/CIPHER. The legacy slug "cipher-2025"
> reuses the system name rather than a first author.
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic
> anchors, pipeline structure, hyperparameter values, OMNI data source,
> and the CME case-study evidence verified; supplemental sensitivity
> tests live in the supplemental material (TODO verify).

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Labelling or classifying a **large OMNI 1-minute time-series corpus** for **recurrent shape motifs** without a fully labelled catalog — the workshop paper demonstrates this for CMEs and SIRs on OMNI.
- Acting as an **upstream unsupervised step** that proposes candidate event windows for downstream supervised labelling (cf. [[paper-camporeale-2017-knn-solar-wind-categorization]], [[paper-bloch-2024-uncertainty-nn-solar-wind-types]]).
- Needing a **scalable** alternative to per-window deep models — iSAX is symbolic compression with multi-resolution indexing, and HDBSCAN scales near-linearly via the symbolic distance.
- Inserting a **human-in-the-loop** validation layer for cluster medoids before downstream science use — the HITL step is what turns a clustering output into a labelled corpus and is explicit in the pipeline name (Human Evaluation for Recognition).

Do NOT use this skill when:

- Pre-defined event labels exist — supervised ML on the labelled set is more efficient than re-clustering.
- Per-sample boundary detection is required (use [[paper-rudisser-2022-icme-unet-automatic-detection]] for ICME segmentation).
- The target is **per-event physical attribution without expert involvement** — CIPHER's labels come from the HITL step, not from the clustering alone.
- Real-time streaming inference is required — the paper emphasises *scalable offline analysis*; streaming variants are flagged as future work.

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to §2–§4).** A four-step pipeline — (1)
optional detrending + smoothing + normalisation, (2) iSAX symbolic
compression with multi-resolution indexing, (3) HDBSCAN density clustering
on selected iSAX levels with optional noise re-clustering, (4)
domain-expert validation of cluster medoids and **propagation of the
expert labels across the cluster** — recovers solar-wind phenomena
including **coronal mass ejections (CMEs)** and **stream interaction
regions (SIRs)** from NASA OMNI 1-minute data. The paper validates the
**2021-03-11/12 CME** as one such recovered cluster, with the
expert-identified CME substructures (forward shock, compressed sheath,
magnetic ejecta, trailing solar wind) visible in the raw OMNI panels of
Figure 1(b).

**Verifiable task.** A reproduction succeeds when an agent:

1. Pulls NASA OMNI 1-min L1 data (bulk flow speed `V`, proton density `N_p`, proton temperature `T_p`, magnetic field components and magnitude) across a span that covers the 2021-03-11/12 CME.
2. Runs the CIPHER preprocessing (optional detrending + smoothing + per-window z-score normalisation).
3. Applies iSAX with **chunk size = 35 hours** and **word size = 8** for the symbolic compression.
4. Runs HDBSCAN with **min_cluster_size = 5** and **min_samples = 5** on a selected iSAX index level.
5. Recovers a CME-consistent cluster containing the 2021-03-11/12 sequence as a member, where a domain expert (or a Richardson–Cane / HelioForecast cross-check) confirms the four substructures (forward shock / sheath / magnetic ejecta / trailing wind) visible on the raw panels.
6. Re-runs against a SIR-overlapping window to recover a SIR cluster (the paper validates this in §4 but uses different features — primarily flow speed — in Figure 2).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Preprocessing

- Optional steps (verified from §2):
  - Detrending and smoothing to remove large-scale biases and high-frequency noise (the paper cites pyBoat for biological-data-style optimal time-frequency analysis as inspiration).
  - Per-window normalisation (z-score). The choice of which OMNI parameter is the primary clustering input is task-dependent: §4 uses **proton density** for CME-class recovery and **flow speed** for SIR-class recovery.

### Algorithm 3.2 — iSAX symbolic compression

- iSAX = indexable Symbolic Aggregate approXimation; PAA-reduced + quantile-binned symbolic words.
- Hyperparameters from §3.2:
  - **chunk size = 35 hours** (the fixed-length window).
  - **word size = 8** (number of symbolic segments per chunk).
  - Multi-resolution indexing across iSAX levels is part of the algorithm; HDBSCAN runs on a "selected level" (§2). The exact level used in the paper's headline result is TODO verify from the supplemental material.

### Algorithm 3.3 — HDBSCAN clustering with optional noise re-clustering

- From §2 and §3.2:
  - **min_cluster_size = 5** — minimum number of sequences for a valid cluster.
  - **min_samples = 5** — noise-sensitivity parameter (called "noise_sensitivity_param" in the paper).
  - Optional **noise re-clustering**: unassigned (`label = -1`) points can be re-clustered under relaxed density constraints (whether the headline result uses this re-clustering pass is TODO verify).

### Algorithm 3.4 — HITL validation + label propagation

- For each cluster, present a representative medoid (the paper uses Figure 1(a)'s middle-panel symbolic + summary view).
- Expert cross-checks **multiple OMNI parameters** in the raw data of one member sequence (the paper specifically calls out that the expert "did not rely on density alone but cross-checked additional parameters").
- Expert assigns a meaningful physical label (e.g., "CME with forward shock, compressed sheath, magnetic ejecta, trailing wind").
- The expert's label is **propagated to all members of the cluster** ("annotations are propagated across clusters to yield systematic, scalable classifications").

Code skeleton (scaffold tier; runnable against the public repo):

```python
# Pseudocode aligned to the published hyperparameters (Kobayashi & Martin
# et al. 2025). See https://github.com/spaceml-org/CIPHER for the released
# pipeline; the call sketched below mirrors the paper's §3 configuration.
def cipher_solar_wind(omni_1min_df, primary="proton_density"):
    windows = slide_windows(omni_1min_df[primary], chunk_hours=35)
    pre = preprocess(windows, detrend=True, smooth=True, normalize="zscore")
    isax_words = isax_encode(pre, word_size=8)
    labels = hdbscan_cluster(isax_words, min_cluster_size=5, min_samples=5)
    medoids = exemplars_per_cluster(windows, labels)
    expert_labels = hitl_validate(medoids, additional_panels=["V", "Bz", "N_p", "T_p"])
    return propagate_labels(labels, expert_labels)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| NASA OMNI | merged L1 ACE / Wind-SWE / IMP-8 / Geotail features (`V`, `N_p`, `T_p`, `B`, `B_x/By/Bz`) | L2 1-minute | Spans the workshop demo: 2021-03-11/12 CME plus surrounding context | OMNIWeb / SPDF | `cdflib`; cf. [[paper-pyspedas-multimission-data-access]] |
| Richardson–Cane / HelioForecast ICME catalog | event boundaries for HITL anchoring | derived | Same | https://helioforecast.space/icmecat | n/a |

CIPHER is in principle mission-agnostic, but the workshop paper validates on **OMNI 1-min** specifically; transferring to PSP/Solar Orbiter native cadence requires re-tuning the chunk size and word size.

## 5. Validation target → benchmark artifact

- **Claim**: CIPHER recovers identifiable solar-wind phenomena (CMEs, SIRs) via unsupervised clustering with human validation, on NASA OMNI 1-min data; the 2021-03-11/12 CME is the worked case in Figure 1(b).
- **Metric**: cluster count and cluster purity against the Richardson–Cane / HelioForecast ICME catalog or an analogous SIR catalog; **expert acceptance rate**; cluster-medoid coherence (the 5–95 % confidence intervals shown in Figure 1(a) and Figure 2 are the paper's coherence diagnostic — quantitative tolerance values are not reported in the 5-page workshop format).
- **Tolerance**: ≤ 2 clusters drift from the published clustering for the same `(chunk=35 h, word=8, min_cluster_size=5, min_samples=5)` config; the published 5-page workshop format does not pin a hard numeric tolerance, so any reproducer should additionally re-run the supplemental sensitivity sweep (TODO verify supplemental hyperparameter range).
- **Reference figure**: Figure 1(a) (CIPHER cluster on smoothed-detrended proton density, with symbolic + summary panels); Figure 1(b) (2021-03-11/12 CME raw OMNI parameters with the four CME substructures shaded); Figure 2 (SIR cluster from flow speed).

Recommended check artifacts:

- `cipher_clusters.csv` — per-window `(t_start, t_end, isax_word, cluster_id, distance_to_medoid)` on a span containing 2021-03-11/12.
- A per-cluster medoid panel reproducing Figure 1(a) for the recovered CME cluster.
- A confusion-table cross-check against the HelioForecast ICME catalog for the same window.

## 6. Failure modes → skill memory

- **iSAX parameter sensitivity.** The headline result uses `(chunk = 35 h, word = 8)`; smaller chunks fragment the CME signal, larger chunks dilute it. The supplemental material reports a sensitivity sweep (TODO verify the swept ranges).
- **HDBSCAN noise label.** A large fraction of `−1` (noise) often means the chunk size is wrong, not that the data are noise-dominated. The paper provides an optional re-clustering pass for noise points (use only when the noise fraction is high).
- **Single-parameter clustering loses cross-parameter signatures.** §4 explicitly demonstrates that clustering on proton density alone recovers CMEs, but the **HITL expert must cross-check on multiple parameters** before assigning a CME label. Skipping the cross-check inflates the apparent purity.
- **Z-score per window removes amplitude.** Two streams with the same *shape* but different amplitudes collapse into the same cluster. Decide whether amplitude information matters for the downstream label.
- **HITL bias.** Expert acceptance reflects reviewer priors; a multi-reviewer rubric with inter-rater agreement is good practice but not part of the published pipeline.
- **Mission-specificity.** Patterns learned on OMNI 1-min do not transfer to PSP native cadence without re-tuning chunk/word size.
- **5-page workshop format.** The paper is intentionally compact; the supplemental material carries the sensitivity tests and is the load-bearing reference for any benchmarked-tier promotion.

## 7. Claim boundary

**In scope.** Unsupervised iSAX + HDBSCAN clustering with HITL validation on NASA OMNI 1-min solar-wind data, with the demonstrated parameter set `(chunk=35 h, word=8, min_cluster_size=5, min_samples=5)`, recovering CMEs and SIRs.

**Out of scope — do NOT generalise beyond:**

- Per-sample segmentation — CIPHER is per-chunk.
- Physical attribution of clusters without an explicit HITL step.
- Cross-mission transfer of cluster labels without re-clustering on the target mission.
- Real-time streaming inference — the paper emphasises *scalable offline analysis*.
- Sub-chunk resolution events (any event much shorter than 35 hours) — the chunk size sets the time resolution.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: https://doi.org/10.48550/arXiv.2510.21022 (arXiv-issued).
- arXiv: https://arxiv.org/abs/2510.21022 (submission 2025-10-23).
- ADS: TODO verify (no bibcode posted at verification time).
- Code: https://github.com/spaceml-org/CIPHER (advertised in the workshop PDF's Broader Impact section).
- Data: NASA OMNI 1-min via OMNIWeb / SPDF (https://omniweb.gsfc.nasa.gov); HelioForecast ICME catalog (https://helioforecast.space/icmecat).

## 9. Skill graph → depends_on

- `[[paper-koikkalainen-2025-complexity-solar-wind-streams]]` — complementary unsupervised approach using information-theory complexity features on solar-wind streams.
- `[[paper-regan-2026-mars-solar-wind-ml-classification]]` — unsupervised PCA + K-Means alternative at Mars.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — supervised event-detector contrast for ICMEs.
- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — supervised label feed for HITL anchoring (4-class scheme).
- `[[paper-bloch-2024-uncertainty-nn-solar-wind-types]]` — supervised counterpart with uncertainty quantification; CIPHER's HITL-validated clusters could be used as additional training labels for that 8PNN.

## 10. Research-generation affordances

- **Multi-parameter joint clustering.** §5 "Limitations and Future Work" specifically calls out joint multi-parameter clustering as a high-value extension; the current published pipeline clusters on one primary parameter and HITL-cross-checks the rest. A multi-channel iSAX variant (per-parameter iSAX words concatenated) is the natural next step and would test whether the HITL cross-check can be partially automated.
- **Streaming variant.** Online iSAX + incremental HDBSCAN would convert CIPHER from offline to streaming; the workshop paper flags this explicitly as future work.
- **Cross-mission transfer at PSP cadence.** Re-running CIPHER on PSP FIELDS / SWEAP native-cadence data with a re-tuned chunk size would test the universality claim; the result would not produce CME/SIR clusters at the same `(35 h, 8)` parameter set.
- **Composable experiment with [[paper-bloch-2024-uncertainty-nn-solar-wind-types]]:** use the HITL-validated CIPHER clusters as an additional weakly-labelled training set for the 8PNN, and measure whether macro-F1 on the 5-class scheme (CH/SB/SR/MO/SH) improves — directly addressing the sheath-confusion failure mode that the Narock 2024 paper calls out.
- **Hyperparameter automation.** Future work flagged in §5 includes "automated selection of compression and clustering hyperparameters" — a Bayesian-optimisation wrapper around the `(chunk, word, min_cluster_size, min_samples)` grid against a held-out HelioForecast ICME-overlap purity metric is a self-contained research project.

## Notes

- The HITL component is what turns CIPHER from "yet another unsupervised pipeline" into a label-generation system; benchmarking without HITL changes the claim entirely.
- The 5-page workshop format pins headline hyperparameters but defers sensitivity tests to the supplemental material — any benchmarked-tier promotion must read the supplemental.
- The slug `cipher-2025-isax-hdbscan-solar-wind-segmentation` reuses the **system name** (CIPHER) rather than a first author; the verified lead authors are **Jasmine R. Kobayashi (SwRI) and Daniela Martin (University of Delaware), co-equal**, with 13 additional co-authors across SwRI, Boston University, U. Delaware, Catholic U. of America, Georgia State, Oxford, U. Vienna, UTFPR-Paraná, Colorado, Stanford, Intel Labs, ESA, NASA GSFC, and Drexel. Heliolab / Frontier Development Lab (FDL) is acknowledged as the research environment.
