---
name: roy-2025-suryabench-ml-benchmark-dataset
description: >-
  Use when consuming SuryaBench, a standardised ML-ready SDO dataset, for benchmarking
  models across six heliophysics tasks (AR segmentation, AR-emergence forecasting,
  coronal-field extrapolation, flare prediction, EUV spectra, solar-wind-speed) — central
  claim is a unified, reproducible benchmark over preprocessed AIA + HMI data spanning
  2010-05 to 2024-07 (Roy et al. 2025, arXiv:2508.14107; venue TODO verify).
version: 0.1.0
tags: [machine-learning, benchmark, dataset, sdo, aia, hmi, reproducibility, multi-task]
quality_level: pilot
executable_status: scaffold
---

# SuryaBench 2025 — Benchmark Dataset for ML in Heliophysics

> Compiled from Roy, S. et al. (2025), *SuryaBench: Benchmark Dataset for Advancing Machine Learning in Heliophysics and Space Weather Prediction*, arXiv:2508.14107 (venue TODO verify).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. Per-task label provenance, train/val/test split rules, and exact preprocessing pipelines require the full paper.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Benchmarking any heliophysics ML model on a **standardised SDO-derived dataset** rather than rolling a one-off dataset.
- Running **comparable evaluations** across active-region segmentation, AR-emergence forecasting, coronal-field extrapolation, flare prediction, EUV-spectra prediction, and solar-wind-speed estimation.
- Pretraining a foundation model on the same corpus the [[paper-roy-2025-surya-heliophysics-foundation-model]] uses.
- Documenting **data lineage** (roll correction, orbital adjustments, exposure normalisation, degradation compensation) for reviewer-grade reproducibility.

Do NOT use this skill when:

- The downstream task requires in-situ-only inputs (PSP / Solar Orbiter heliospheric data).
- The downstream task requires raw, unprocessed L1 data (SuryaBench is preprocessed).
- The required cycle / window is outside 2010-05 — 2024-07.

## 2. Paper claim → verifiable task

**Claim (narrow form).** SuryaBench is a high-resolution, ML-ready dataset derived from SDO covering **2010-05 to 2024-07** (~one full solar cycle) and including processed AIA + HMI imagery plus auxiliary benchmark application datasets for: active-region segmentation, AR-emergence forecasting, coronal-field extrapolation, solar-flare prediction, EUV-spectra prediction, and solar-wind-speed estimation. Preprocessing includes spacecraft roll-angle correction, orbital adjustments, exposure normalisation, and degradation compensation.

**Verifiable task.** A reproduction succeeds when an agent:

1. Re-fetches the raw inputs and reproduces the SuryaBench preprocessing pipeline (the exact algorithm for each step is TODO verify).
2. Re-creates the per-task labels from the paper's stated sources (TODO verify the source per task).
3. Validates a published task-baseline score on the dataset (TODO verify which baselines the paper supplies).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — SDO data ingestion

- Procedure:
  1. Pull SDO AIA L1 for the chosen channels and SDO HMI L1.5/L2 for the chosen products.
  2. Apply: roll correction → orbital geometry adjustment → exposure normalisation → instrument degradation compensation. Each step's exact implementation is TODO verify.
  3. Tile / pad to a fixed resolution if downstream tasks require uniform input size.

### Algorithm 3.2 — Per-task label assembly

- For each application:
  - **Active-region segmentation** — labels from (HEK / SHARP-based / hand-labelled) — TODO verify.
  - **AR emergence forecasting** — emergence-event catalog — TODO verify.
  - **Coronal-field extrapolation** — PFSS / NLFFF target field — TODO verify.
  - **Solar-flare prediction** — GOES X-ray flare catalog labels.
  - **EUV-spectra prediction** — EVE reference spectra.
  - **Solar-wind-speed estimation** — L1 / ACE / DSCOVR V_sw at the propagation-aligned timestamp.

### Algorithm 3.3 — Train/val/test split rules

- TODO verify whether splits are chronological, by Carrington rotation, or random per-image. Chronological splits are essential for forecasting tasks.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once preprocessing details and labels are pinned.
def suryabench_load(task, split):
    raw = fetch_sdo(channels=PAPER_CHANNELS, window="2010-05..2024-07")
    pre = preprocess(raw, roll_correct=True, orbit_adjust=True, exposure_norm=True, degradation=True)
    labels = load_task_labels(task)
    return splits_per_paper(pre, labels)[split]
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SDO AIA | 8 channels (TODO verify which) | L1 → preprocessed | 2010-05 – 2024-07 | JSOC | `sunpy` / JSOC export |
| SDO HMI | 5 products (TODO verify which) | L1.5/L2 → preprocessed | Same | JSOC | `sunpy` / JSOC |
| HEK / SHARP | AR + flare event records | derived | Same | HEK / JSOC | `sunpy.net.hek` |
| GOES | X-ray flare catalog | L2 | Same | NOAA SWPC | WebFetch |
| EVE | EUV spectra (downstream label) | L2 | Same | LASP EVE | WebFetch |
| Solar-wind-speed | L1 / ACE / DSCOVR V_sw at L1 | L2 | Same | CDAWeb / SPDF | `cdflib` |

SuryaBench is itself a *derived* dataset — agents should treat it as a single archive once released (TODO verify release path; typical IBM/NASA practice is a Hugging Face hub mirror).

## 5. Validation target → benchmark artifact

- **Claim**: SuryaBench provides a unified ML-ready dataset enabling reproducible benchmarking across six heliophysics applications.
- **Metric**: reproducibility of the published baseline scores on each task using SuryaBench-supplied splits.
- **Tolerance**: TODO verify per task.
- **Reference figure**: TODO verify — likely a per-task baseline table.

Recommended check artifacts:

- A per-task baseline-score reproduction notebook.
- An MD5 / SHA of the preprocessed images to confirm pipeline fidelity.
- A dataset-cards file documenting per-task split definitions.

## 6. Failure modes → skill memory

- **Degradation compensation drift.** AIA instrument degradation factors evolve over time; using an out-of-date degradation table biases late-cycle samples.
- **Roll-angle correction frame.** Different correction conventions (Carrington vs Stonyhurst) yield numerically different pixel grids.
- **Per-task label source.** Different active-region catalogs (HEK vs SHARP-derived vs hand-labelled) disagree at boundaries; the SuryaBench choice is TODO verify.
- **Chronological vs random splits.** Forecasting tasks require chronological splits; random splits leak future labels.
- **Solar-wind-speed propagation lag.** Aligning V_sw at L1 to a corresponding solar-disk image requires ballistic propagation; the lag definition matters.
- **Resolution mismatch.** Downstream models often expect 256² / 512² / 1024²; SuryaBench native is full-resolution and must be downsampled consistently across train/val/test.

## 7. Claim boundary

**In scope.** A standardised, preprocessed, ML-ready SDO-derived dataset covering 2010-05 — 2024-07 with auxiliary task-specific labels for six heliophysics applications.

**Out of scope — do NOT generalise beyond:**

- Non-SDO instruments (STEREO, SOHO, EUI/Solar Orbiter).
- Windows outside 2010-05 — 2024-07.
- In-situ-only tasks where solar imagery is not a natural input.
- Operational real-time benchmarking — the dataset is offline.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2508.14107
- ADS: TODO verify.
- Code: TODO verify (likely a public mirror).
- Data: TODO verify the canonical hosting URL (Hugging Face / Zenodo / NASA-hosted).

## 9. Skill graph → depends_on

- `[[paper-roy-2025-surya-heliophysics-foundation-model]]` — primary consumer; uses SuryaBench for pretraining + fine-tuning.
- `[[paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation]]` — coronal-hole segmentation baseline candidate.
- `[[paper-pyspedas-multimission-data-access]]` — in-situ side for the solar-wind-speed downstream task.
- `[[paper-sunpy-2023-interoperable-ecosystem]]` — natural toolchain for ingesting SDO L1 inputs.

## Notes

- SuryaBench is a *benchmark* skill, not a *physics* skill — its quality bar is data lineage and split fidelity, not heliophysics novelty.
- Any benchmarked-tier promotion of this skill must include MD5 / SHA fingerprints of preprocessing outputs to guarantee bit-level reproducibility.
