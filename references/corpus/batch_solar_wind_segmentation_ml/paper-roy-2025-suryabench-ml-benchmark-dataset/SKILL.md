---
name: roy-2025-suryabench-ml-benchmark-dataset
description: >-
  Use when consuming SuryaBench, a high-resolution ML-ready SDO dataset covering
  May 2010 – July 2024 (~ one full solar cycle) with preprocessed AIA + HMI imagery
  and six application sub-datasets (active-region segmentation, AR-emergence
  forecasting, coronal-field extrapolation, solar-flare prediction, EUV-spectra
  prediction, solar-wind-speed estimation). Central claim: unified preprocessing
  (roll-angle correction, orbital adjustment, exposure normalisation, instrument
  degradation compensation) plus standardised per-task labels enable reproducible
  benchmarking and pretraining for foundation models such as Surya
  (Roy et al. 2025, arXiv:2508.14107; sub-datasets released under
  `nasa-ibm-ai4science/` on Hugging Face).
version: 0.1.0
tags: [machine-learning, benchmark, dataset, sdo, aia, hmi, reproducibility, multi-task]
quality_level: paper-grounded-pending-full-text
executable_status: scaffold
paper:
  authors_verified: true
---

# SuryaBench 2025 — Benchmark Dataset for ML in Heliophysics

> Compiled from Roy et al. (2025), *SuryaBench: Benchmark Dataset for
> Advancing Machine Learning in Heliophysics and Space Weather Prediction*,
> arXiv:2508.14107 (submission 2025-08-18). Authors, abstract, application
> list, and the May 2010 – July 2024 time window were cross-checked against
> the arXiv abs page and the public Hugging Face dataset card
> `nasa-ibm-ai4science/Surya-bench-solarwind` on 2026-05-19; the
> solar-wind sub-dataset card pins concrete split definitions and a CC-BY-4.0
> licence. Per-task baseline scores, the exact AIA-channel / HMI-product list,
> degradation-compensation coefficients, and AR-label provenance still require
> the full PDF and per-task dataset cards.
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic anchors,
> applications, time window, and at least one sub-dataset's split definition
> verified; per-task baselines and label-provenance remain pending.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Benchmarking any heliophysics ML model on a **standardised SDO-derived dataset** rather than rolling a one-off dataset.
- Running **comparable evaluations** across active-region segmentation, AR-emergence forecasting, coronal-field extrapolation, flare prediction, EUV-spectra prediction, and solar-wind-speed estimation.
- Pretraining or fine-tuning a foundation model on the same corpus the [[paper-roy-2025-surya-heliophysics-foundation-model]] uses.
- Documenting **data lineage** (roll correction, orbital adjustments, exposure normalisation, degradation compensation) for reviewer-grade reproducibility.

Do NOT use this skill when:

- The downstream task requires in-situ-only inputs (PSP / Solar Orbiter heliospheric in-situ data) without an SDO imagery channel.
- The downstream task requires raw, unprocessed L1 data — SuryaBench is delivered preprocessed.
- The required cycle / window is outside **2010-05 – 2024-07**.

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the abstract).** SuryaBench is a high-resolution,
ML-ready dataset derived from NASA's Solar Dynamics Observatory covering
**May 2010 – July 2024** (~ one full solar cycle) and including processed
AIA + HMI imagery plus six auxiliary application benchmark datasets for:
**active-region segmentation, active-region emergence forecasting,
coronal-field extrapolation, solar-flare prediction, solar EUV-spectra
prediction, and solar-wind-speed estimation**. Preprocessing includes
**spacecraft roll-angle correction, orbital adjustments, exposure normalisation,
and instrument degradation compensation**. The dataset is positioned as the
canonical pretraining + fine-tuning source for foundation models such as
Surya (cf. [[paper-roy-2025-surya-heliophysics-foundation-model]]).

**Verifiable task.** A reproduction succeeds when an agent:

1. Pulls the SuryaBench preprocessed imagery (e.g., from `nasa-ibm-ai4science/core-sdo` on Hugging Face) for the requested channel set and window subset.
2. For the solar-wind-speed application: loads `nasa-ibm-ai4science/Surya-bench-solarwind` and reproduces the **train (Feb 15 – Dec 31 each year 2010–2019; ≈70 000 rows) / validation (Jan 15–31 each year 2010–2019; ≈3 430 rows) / test (all instances 2020–2024; ≈40 000 rows) / leaky-validation (Jan 1–14 and Feb 1–14 each year 2010–2019; ≈5 860 rows)** split exactly as defined by the dataset card. Total ≈119 225 hourly L1 timesteps.
3. Confirms a published task-baseline score on the dataset (per-task baseline scores TODO verify against the full SuryaBench PDF and the remaining per-task dataset cards).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — SDO image ingestion + preprocessing

- Procedure:
  1. Pull SDO AIA L1 for the chosen channels and SDO HMI L1.5/L2 for the chosen products (exact channels/products are part of the SuryaBench specification — TODO verify against the full PDF; the companion [[paper-roy-2025-surya-heliophysics-foundation-model]] entry advertises 8 AIA + 5 HMI).
  2. Apply, in order: **roll-angle correction → orbital geometry adjustment → exposure normalisation → instrument degradation compensation**. The abstract lists these four steps explicitly; each step's exact implementation (e.g., the AIA degradation reference table version) is TODO verify.
  3. Tile / resample to a fixed resolution if downstream tasks require uniform input size. The Surya backbone consumes 4096×4096 native; downstream task models may consume downsampled tiles.

### Algorithm 3.2 — Per-task label assembly

- For each of the six applications named in the abstract:
  - **Active-region segmentation** — pixel-level AR masks. Catalog provenance TODO verify (HEK / SHARP-derived / curated).
  - **Active-region emergence forecasting** — AR-emergence event timestamps. Catalog provenance TODO verify.
  - **Coronal-field extrapolation** — PFSS or NLFFF target fields aligned to HMI magnetograms. Method TODO verify.
  - **Solar-flare prediction** — GOES X-ray flare catalog labels.
  - **EUV-spectra prediction** — EVE reference spectra as regression target.
  - **Solar-wind-speed estimation** — L1 hourly V_sw at the propagation-aligned timestamp, sourced from OMNI per the `Surya-bench-solarwind` dataset card.

### Algorithm 3.3 — Train / val / test split rules

- **Solar-wind-speed split (verified from `Surya-bench-solarwind` dataset card):**
  - `train.csv`: Feb 15 – Dec 31 each year, 2010–2019 (≈70 000 rows)
  - `validation.csv`: Jan 15–31 each year, 2010–2019 (≈3 430 rows)
  - `test.csv`: all instances 2020–2024 (≈40 000 rows)
  - `leaky_validation.csv`: Jan 1–14 and Feb 1–14 each year, 2010–2019 (≈5 860 rows; flagged as deliberately leaky so consumers can quantify temporal-leakage bias)
  - Cadence: 1 hour; features per row: `V` (target, km/s), `Bx_gse`, `By_gsm`, `Bz_gsm`, `N`; source: OMNI (May 2010 – Dec 2024); licence: CC-BY-4.0; total ≈119 225 rows.
- Splits for the other five applications follow the same chronological convention but the exact day ranges are TODO verify per task. Chronological splits are essential for forecasting tasks; random per-image splits would leak future labels.

Code skeleton (scaffold tier; concrete for the solar-wind sub-dataset, pseudocode for the rest):

```python
# Concrete for the solar-wind sub-dataset (split rules read from the
# dataset card on 2026-05-19); the other sub-datasets are referenced by
# name and require their own dataset-card lookup.
def suryabench_solarwind_load(split):
    from huggingface_hub import hf_hub_download
    import pandas as pd
    path = hf_hub_download(
        repo_id="nasa-ibm-ai4science/Surya-bench-solarwind",
        repo_type="dataset",
        filename=f"{split}.csv",
    )
    return pd.read_csv(path)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SDO AIA | EUV/UV channels (specific list TODO verify; advertised as 8 channels in the Surya companion) | L1 → preprocessed | 2010-05 – 2024-07 | JSOC | `sunpy` / JSOC export; cf. `nasa-ibm-ai4science/core-sdo` on Hugging Face |
| SDO HMI | 5 products (specific list TODO verify) | L1.5/L2 → preprocessed | Same | JSOC | `sunpy` / JSOC |
| HEK / SHARP | AR + flare event records (label provenance TODO verify per sub-dataset) | derived | Same | HEK / JSOC | `sunpy.net.hek` |
| GOES | X-ray flare catalog | L2 | Same | NOAA SWPC | WebFetch |
| EVE | EUV spectra (downstream label) | L2 | Same | LASP EVE | WebFetch |
| OMNI L1 V_sw + B + N | Hourly L1 features (`V`, `Bx_gse`, `By_gsm`, `Bz_gsm`, `N`) | L2 hourly | 2010-05-13 – 2024-12-31 | OMNIWeb / SPDF; mirrored in Hugging Face `nasa-ibm-ai4science/Surya-bench-solarwind` | `cdflib` or `huggingface_hub` |
| Hugging Face SuryaBench sub-datasets | per-application benchmark files | dataset CSV / NumPy | Same | `nasa-ibm-ai4science/Surya-bench-*` | `huggingface_hub` |

SuryaBench is a *derived* dataset — agents should pull from the released Hugging Face mirrors rather than re-running the preprocessing pipeline, unless the goal is to validate the preprocessing itself.

## 5. Validation target → benchmark artifact

- **Claim**: SuryaBench provides a unified ML-ready dataset enabling reproducible benchmarking across six heliophysics applications.
- **Metric**: reproducibility of the published baseline scores on each task using SuryaBench-supplied splits. The solar-wind dataset card explicitly notes baseline numbers are not embedded in the card (TODO verify per the full PDF or per-task readmes).
- **Tolerance**: TODO verify per task.
- **Reference figure**: TODO verify — likely a per-task baseline table in the PDF.

Recommended check artifacts:

- A per-task baseline-score reproduction notebook (one notebook per application).
- MD5 / SHA fingerprints of the preprocessed images to confirm pipeline fidelity vs the Hugging Face mirror.
- A dataset-card file documenting per-task split definitions (the solar-wind card is the template).

## 6. Failure modes → skill memory

- **Degradation compensation drift.** AIA instrument degradation factors evolve over time; using an out-of-date degradation table biases late-cycle samples. SuryaBench's compensation reference version is TODO verify.
- **Roll-angle correction frame.** Different correction conventions (Carrington vs Stonyhurst, or the SDO native frame) yield numerically different pixel grids; downstream models that crop or rotate must respect the SuryaBench convention.
- **Per-task label source.** Different active-region catalogs (HEK vs SHARP-derived vs hand-labelled) disagree at boundaries; the SuryaBench choice per application is TODO verify.
- **Chronological vs random splits.** Forecasting tasks require chronological splits; random splits leak future labels. The solar-wind sub-dataset provides a deliberately leaky `leaky_validation.csv` to make this risk measurable rather than hidden.
- **Solar-wind-speed propagation lag.** Aligning V_sw at L1 to a corresponding solar-disk image requires ballistic (or kinematic) propagation; the lag definition affects every solar-wind-speed downstream score. The SuryaBench convention is TODO verify.
- **Resolution mismatch.** Downstream models often expect 256² / 512² / 1024²; SuryaBench native is full-resolution and must be downsampled consistently across train/val/test.

## 7. Claim boundary

**In scope.** A standardised, preprocessed, ML-ready SDO-derived dataset covering 2010-05 — 2024-07 with auxiliary task-specific labels for six heliophysics applications, released as Hugging Face sub-datasets.

**Out of scope — do NOT generalise beyond:**

- Non-SDO instruments (STEREO, SOHO, EUI/Solar Orbiter).
- Windows outside 2010-05 — 2024-07.
- In-situ-only tasks where solar imagery is not a natural input.
- Operational real-time benchmarking — the dataset is offline.
- Per-event physical attribution — SuryaBench provides supervised labels; physical-cause inference requires additional analysis.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: https://doi.org/10.48550/arXiv.2508.14107 (arXiv-issued; journal DOI not yet assigned).
- arXiv: https://arxiv.org/abs/2508.14107 (submission 2025-08-18).
- ADS: TODO verify (no bibcode posted at verification time).
- Code / data: Hugging Face — `nasa-ibm-ai4science/core-sdo`, `nasa-ibm-ai4science/Surya-bench-solarwind` (DOI 10.57967/hf/7276), `nasa-ibm-ai4science/surya-bench-coronal-extrapolation`, `nasa-ibm-ai4science/surya-bench-flare-forecasting` and additional per-application sub-datasets; CC-BY-4.0.

## 9. Skill graph → depends_on

- `[[paper-roy-2025-surya-heliophysics-foundation-model]]` — primary consumer; uses SuryaBench for pretraining + fine-tuning.
- `[[paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation]]` — coronal-hole segmentation baseline candidate.
- `[[paper-pyspedas-multimission-data-access]]` — in-situ side for the solar-wind-speed downstream task.
- `[[paper-sunpy-2023-interoperable-ecosystem]]` — natural toolchain for ingesting SDO L1 inputs and for replicating the preprocessing pipeline.

## 10. Research-generation affordances

- **Preprocessing-fidelity audit.** A self-contained study would re-derive SuryaBench preprocessing from raw JSOC L1 and compare MD5 / SHA against the Hugging Face mirror; surface drift cases reveal which preprocessing step (roll / orbit / exposure / degradation) is fragile to upstream changes.
- **Cross-mission negative result.** Applying SuryaBench-trained downstream models to STEREO EUVI or EUI imagery without re-preprocessing is an expected-failure experiment; its diagnostic value is in characterising the size of the SDO-specific calibration prior.
- **Composable experiment with Surya:** the deliberately leaky `leaky_validation.csv` in the solar-wind sub-dataset enables a quantitative measurement of how much temporal leakage inflates Surya's reported solar-wind-speed score. This is a high-value, low-cost test that does not require re-pretraining.
- **Label-source ablation.** The active-region segmentation sub-dataset's label provenance is unspecified in the abstract. Cross-comparing the SuryaBench AR labels with an independently sourced catalog (HEK or SHARP-derived) would quantify catalog noise and establish an irreducible-error floor for AR-segmentation downstream tasks.

## Notes

- SuryaBench is a *benchmark* skill, not a *physics* skill — its quality bar is data lineage and split fidelity, not heliophysics novelty.
- Any benchmarked-tier promotion of this skill must include MD5 / SHA fingerprints of preprocessing outputs to guarantee bit-level reproducibility, and per-task baseline numbers read from the full PDF.
- The solar-wind sub-dataset card explicitly publishes a `leaky_validation.csv` alongside `validation.csv`; this is an unusual and useful design choice — it makes the temporal-leakage failure mode measurable instead of latent.
