---
name: roy-2025-surya-heliophysics-foundation-model
description: >-
  Use when leveraging Surya, a 366M-parameter spatiotemporal-transformer foundation model
  pretrained on SDO AIA + HMI, for zero-shot or LoRA-fine-tuned downstream solar tasks
  (solar-wind-speed forecasting, AR segmentation, flare forecasting, EUV spectra) —
  central claim is that Surya is the first heliophysics foundation model using time
  advancement as a pretext on full-resolution SDO data (Roy et al. 2025, arXiv:2508.14112;
  venue TODO verify).
version: 0.1.0
tags: [machine-learning, foundation-model, sdo, aia, hmi, transformer, lora, fine-tuning, solar-wind-forecast, segmentation, flare-forecast]
quality_level: pilot
executable_status: scaffold
---

# Surya 2025 — Foundation Model for Heliophysics on SDO

> Compiled from Roy, S. et al. (2025), *Surya: Foundation Model for Heliophysics*, arXiv:2508.14112 (venue TODO verify).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. Tokeniser details, exact LoRA hyperparameters, and per-task fine-tuning splits require the full paper.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Fine-tuning a **single backbone** for multiple heliophysics tasks (solar-wind-speed forecasting, AR segmentation, flare forecasting, EUV-spectra prediction) without retraining from scratch each time.
- Producing **zero-shot forecasts** of solar dynamics from AIA + HMI inputs.
- Using **LoRA** for parameter-efficient adaptation on a domain-specific downstream task.
- Comparing against task-specific baselines — Surya's claim is that one backbone beats per-task specialists across multiple tasks.

Do NOT use this skill when:

- The downstream task is in-situ-only (PSP / SO time series); Surya's pretraining is image-only.
- A pure physics model (e.g., MHD simulation) is required — Surya is data-driven.
- Operational real-time forecasting at sub-minute latency is required without inference-engineering work.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Surya is a 366 M-parameter spatiotemporal-transformer foundation model with spectral gating + long–short range attention, pretrained on multi-instrument SDO observations — **8 AIA channels + 5 HMI products** — using **high-resolution solar-image forecasting as the pretext task** and **autoregressive rollout tuning** as a second stage. Zero-shot evaluations forecast solar dynamics + flare events. LoRA fine-tuning enables strong downstream performance on solar-wind-speed forecasting, active-region segmentation, solar-flare forecasting, and EUV spectra. Surya is the first heliophysics foundation model using time advancement as the pretext task on full-resolution SDO data.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reconstructs the pretraining input stack (8 AIA + 5 HMI channels) and the pretraining objective.
2. Reproduces zero-shot forecasting metrics within tolerance (TODO verify which forecasting metric and tolerance).
3. Runs LoRA fine-tuning on at least one downstream task (e.g., solar-wind-speed forecasting) and reaches the paper's reported score within tolerance (TODO verify).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Pretraining input + objective

- Procedure:
  1. Pull SDO AIA L1 (the 8 channels the paper uses; typically 94, 131, 171, 193, 211, 304, 335 Å + 1600 Å OR 1700 Å — TODO verify the exact 8).
  2. Pull HMI L1.5 / L2 (the 5 HMI products — magnetograms, Dopplergrams, continuum, line-of-sight + vector products — TODO verify the exact 5).
  3. Pretext: predict frame t+Δt from frames {t−kΔt, …, t}. Predict at full SDO resolution (4096×4096 in principle; the paper's training resolution is TODO verify).
  4. Two-stage training: (a) image-forecasting pretext, (b) autoregressive rollout tuning. The exact rollout horizon is TODO verify.

### Algorithm 3.2 — Architecture: spatiotemporal transformer with spectral gating + long–short range attention

- Spectral gating: TODO verify whether this is FNO-style frequency-domain gating or local Fourier-band attention.
- Long–short range attention: TODO verify the windowed-attention pattern.
- Total parameters: 366 M.

### Algorithm 3.3 — LoRA fine-tuning for downstream tasks

- Procedure:
  1. Choose a downstream task (e.g., solar-wind-speed prediction at L1).
  2. Attach LoRA adapters at the layers the paper specifies (TODO verify which layers + rank r).
  3. Fine-tune on the task-specific dataset with the loss the paper specifies (regression / segmentation / classification).
  4. Evaluate against the task-specific baseline.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once architecture and LoRA hyperparameters are pinned.
def surya_finetune(task, data):
    backbone = load_surya_pretrained()
    adapter = lora_adapter(backbone, layers=PAPER_LAYERS, rank=PAPER_RANK)
    fit(adapter, data)
    return evaluate(adapter, data.test, baseline=task.baseline)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SDO AIA | 8 EUV channels | L1, native 12 s | 2010-05 – 2024-07 (per SuryaBench window) | JSOC / SDO archive | `sunpy` / direct JSOC fetch |
| SDO HMI | 5 products (magnetograms, Dopplergrams, continuum, …) | L1.5 / L2 | Same | JSOC | `sunpy` / JSOC |
| Solar-wind-speed labels | V_sw at L1 / ACE / DSCOVR | L2 | Same | CDAWeb / OMNIWeb | `cdflib` |
| Active-region masks | Per-pixel labels for AR segmentation downstream | derived | Same | SuryaBench supplementary / HEK | TODO verify |
| Flare catalog | GOES X-ray peak class | L2 | Same | NOAA SWPC | WebFetch |
| EUV spectra | Reference EVE / Surya-EUV target | L2 | Same | LASP EVE archive | WebFetch |

This skill leans on the companion [[paper-roy-2025-suryabench-ml-benchmark-dataset]] for the standardised ML-ready data.

## 5. Validation target → benchmark artifact

- **Claim**: Surya improves over task-specific baselines on solar-wind-speed forecasting, AR segmentation, flare forecasting, and EUV-spectra prediction via LoRA fine-tuning, and produces zero-shot solar-dynamics + flare forecasts.
- **Metric**: per-task — solar-wind RMSE / correlation; AR-segmentation IoU; flare-forecasting TSS or Brier; EUV-spectra MSE. The specific numerical targets are TODO verify.
- **Tolerance**: TODO verify per task.
- **Reference figure**: TODO verify — likely a multi-panel summary of per-task scores vs baselines.

Recommended check artifacts:

- `surya_zeroshot_forecasts.npz` — frame-by-frame zero-shot solar-dynamics outputs.
- `surya_finetune_<task>.csv` — per-task fine-tuning results vs baseline.
- A LoRA-rank-vs-score curve for at least one downstream task.

## 6. Failure modes → skill memory

- **Pretraining provenance.** Foundation-model behaviour reflects the training set; using Surya on out-of-distribution data (different cycle, different instrument calibration) without retraining risks silent degradation.
- **LoRA rank choice.** Too-low rank under-fits; too-high erases the foundation-model prior. The paper's rank is TODO verify.
- **Channel availability mismatch.** Surya expects 8 AIA + 5 HMI channels; downstream pipelines with missing channels need explicit handling (zero-fill vs masked attention).
- **Autoregressive rollout drift.** Forecast quality degrades non-linearly with horizon; report metrics at multiple horizons.
- **Solar-cycle leakage.** Chronological splits across the 2010–2024 corpus must avoid leaking near-future data into training.
- **Compute budget.** Pretraining cost is substantial; only fine-tuning is realistic without dedicated infrastructure.
- **"First" claims age.** The "first heliophysics foundation model" wording is dated to 2025; downstream skills should not assert future-tense uniqueness.

## 7. Claim boundary

**In scope.** A 366 M-parameter spatiotemporal-transformer foundation model trained on full-resolution SDO AIA + HMI data using time-advancement as the pretext, with LoRA fine-tuning enabling multiple downstream solar tasks.

**Out of scope — do NOT generalise beyond:**

- In-situ-only tasks (PSP / Solar Orbiter heliospheric data) without re-pretraining.
- Generative simulation of solar dynamics (Surya is predictive, not a physics simulator).
- Operational real-time forecasting at sub-minute latency without inference-engineering.
- Cross-mission EUV transfer (STEREO EUVI, GOES SUVI, EUI/Solar Orbiter) without re-pretraining.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2508.14112
- ADS: TODO verify.
- Code: TODO verify — IBM / NASA partnership models often release weights via Hugging Face; the inventory does not list a URL.
- Data: SDO via JSOC + companion [[paper-roy-2025-suryabench-ml-benchmark-dataset]].

## 9. Skill graph → depends_on

- `[[paper-roy-2025-suryabench-ml-benchmark-dataset]]` — companion ML-ready dataset; the natural pretraining + fine-tuning source.
- `[[paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation]]` — task-specific baseline for coronal-hole / open-flux segmentation; a Surya LoRA on CH segmentation should be compared against this.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling segmentation pipeline (in-situ vs imagery).
- `[[paper-pyspedas-multimission-data-access]]` — in-situ data ingestion for solar-wind-speed downstream task.

## Notes

- Surya is an ML-architecture skill, not a physics skill — its scientific claims are about transfer learning and downstream-task performance, not about solar physics directly. Downstream science papers using Surya carry their own claim boundaries.
