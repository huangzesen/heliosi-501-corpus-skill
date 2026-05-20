---
name: roy-2025-surya-heliophysics-foundation-model
description: >-
  Use when leveraging Surya, a 366 M-parameter spatiotemporal-transformer
  foundation model pretrained on SDO AIA + HMI (8 AIA channels + 5 HMI products,
  ~2010–2019, native 4096×4096), for zero-shot or LoRA fine-tuned downstream
  solar tasks (active-region segmentation, AR-emergence forecasting, coronal-field
  extrapolation, flare forecasting, EUV spectra, solar-wind-speed forecasting at
  L1). Central claim: high-resolution time-advancement pretraining followed by
  autoregressive rollout tuning yields a single backbone whose LoRA adapters
  beat task-specific baselines across multiple downstream heliophysics tasks
  (Roy et al. 2025, arXiv:2508.14112; weights released as nasa-ibm-ai4science/Surya-1.0
  on Hugging Face, Apache-2.0).
version: 0.1.0
tags: [machine-learning, foundation-model, sdo, aia, hmi, transformer, lora, fine-tuning, solar-wind-forecast, segmentation, flare-forecast]
quality_level: paper-grounded-pending-full-text
executable_status: scaffold
paper:
  authors_verified: true
---

# Surya 2025 — Foundation Model for Heliophysics on SDO

> Compiled from Roy et al. (2025), *Surya: Foundation Model for Heliophysics*,
> arXiv:2508.14112 (v2 dated 2025-08-21). Authors and abstract were cross-checked
> against the arXiv abs page and the Hugging Face model card
> `nasa-ibm-ai4science/Surya-1.0` on 2026-05-19. Per-task numerical scores,
> the exact eight AIA channels, the exact five HMI products, LoRA rank /
> injected layers, and the autoregressive rollout horizon still require the
> full PDF body (the abs-page abstract and the model-card README do not enumerate
> them).
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic anchors
> and headline architecture verified; downstream per-task scores are not.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Fine-tuning a **single backbone** for multiple heliophysics tasks (solar-wind-speed forecasting at L1, AR segmentation, flare forecasting, EUV-spectra prediction, coronal-field extrapolation, AR-emergence forecasting) without retraining from scratch each time.
- Producing **zero-shot forecasts** of solar dynamics from AIA + HMI inputs without any task-specific fine-tuning.
- Using **LoRA** for parameter-efficient adaptation on a domain-specific downstream task — LoRA is explicitly the adaptation mechanism the model card and abstract advertise.
- Comparing against task-specific baselines — Surya's claim is that one backbone matches or beats per-task specialists across multiple tasks (the exact per-task margins are pending full text).

Do NOT use this skill when:

- The downstream task is in-situ-only (PSP / Solar Orbiter heliospheric time series); Surya's pretraining is image-only on SDO.
- A pure physics model (e.g., MHD simulation) is required — Surya is data-driven and predictive, not a simulator.
- Operational real-time forecasting at sub-minute latency is required without dedicated inference engineering — the model is 366 M parameters and the native input is 4096×4096.
- Cross-mission EUV transfer (STEREO EUVI, GOES SUVI, EUI/Solar Orbiter) is required without re-pretraining.

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the v2 abstract).** Surya is a **366 M-parameter
spatiotemporal-transformer foundation model** with **spectral gating** and
**long–short range attention**, pretrained on multi-instrument SDO observations
— **8 AIA channels + 5 HMI products** — using **high-resolution solar-image
forecasting as the pretext task** and **autoregressive rollout tuning** as a
second stage. Zero-shot evaluations forecast solar dynamics and flare events.
**LoRA** fine-tuning then enables strong downstream performance on solar-wind-speed
forecasting at L1, active-region segmentation, solar-flare forecasting, EUV
spectra, AR-emergence forecasting, and coronal-field extrapolation. Pretraining
input resolution is the SDO native 4096×4096 grid; the training data spans
roughly 2010–2019 (~9 years, ≈218 TB per the Hugging Face model card).

**Verifiable task.** A reproduction succeeds when an agent:

1. Loads the released pretrained weights (`surya.366m.v1.pt` from the Hugging Face hub) into the published spatiotemporal-transformer architecture.
2. Reconstructs the pretraining input stack of 8 AIA channels + 5 HMI products at native resolution (the exact 8 AIA wavelengths and 5 HMI products are not enumerated on the abs page or model card README — TODO verify against the full PDF or the GitHub config).
3. Reproduces at least one zero-shot solar-dynamics forecast (frame-to-frame) and one LoRA-fine-tuned downstream task using the companion paper-skill [[paper-roy-2025-suryabench-ml-benchmark-dataset]] as the dataset source.
4. Confirms the LoRA-adapted task score matches or improves on the paper-stated task-specific baseline within the tolerance the paper reports (numerical targets and tolerances TODO verify against the full PDF).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Pretraining input + objective

- Inputs: **8 AIA channels + 5 HMI products** (abstract verified; specific
  wavelengths and product names TODO verify — typical SDO AIA EUV channels are
  94, 131, 171, 193, 211, 304, 335 Å plus a UV channel, but the precise eight
  Surya uses are not enumerated in the abstract or model card README).
- Pretext: predict frame at time `t+Δt` from a context window of past frames
  (frame-to-frame **time-advancement / image forecasting**). Native input
  resolution is **4096×4096** (the SDO native grid; the Hugging Face card
  states explicitly that pretraining runs at this resolution).
- Two-stage training: (a) image-forecasting pretext, (b) autoregressive rollout
  tuning to stabilise multi-step forecasts. Rollout horizon (number of
  autoregressive steps) is TODO verify.
- Training corpus: ~9 years of SDO data, roughly 2010–2019 per the model card,
  with the Surya-bench downstream slices extending to 2024 (cf.
  [[paper-roy-2025-suryabench-ml-benchmark-dataset]]).

### Algorithm 3.2 — Architecture: spatiotemporal transformer

- Total parameters: **366 M** (abstract + model-card verified).
- Two distinctive components named in the abstract:
  - **Spectral gating** — a frequency-domain mixing operator within the
    transformer block. Whether this is FNO-style (Fourier Neural Operator
    weight gating in the spectral domain) or a learned band-attention
    variant is TODO verify against the methods section.
  - **Long–short range attention** — a windowed/global hybrid attention
    pattern. Specific window sizes and the long-range routing strategy
    are TODO verify.
- File format of released checkpoint: PyTorch `.pt` (`surya.366m.v1.pt`),
  Apache-2.0 license.

### Algorithm 3.3 — LoRA fine-tuning for downstream tasks

- Procedure:
  1. Load `surya.366m.v1.pt` as the backbone (frozen base).
  2. Attach LoRA adapters at the transformer layers specified by the paper
     (which layers and what rank `r` are TODO verify).
  3. Fine-tune on the task-specific dataset with the task loss
     (regression for solar-wind speed, per-pixel cross-entropy for AR
     segmentation, classification for flare prediction, MSE for EUV spectra).
  4. Evaluate against the task-specific baseline.

Code skeleton (pseudocode at scaffold tier; runnable once LoRA rank and
injected layers are pinned):

```python
# Pseudocode — runnable when the LoRA configuration is read from the
# released paper/repo. Abstract identifies LoRA as the adaptation method
# but does not pin the rank or layer set.
def surya_finetune(task, data):
    backbone = load_surya_pretrained("nasa-ibm-ai4science/Surya-1.0")
    adapter = lora_adapter(backbone, layers=PAPER_LAYERS, rank=PAPER_RANK)
    fit(adapter, data, loss=task.loss)
    return evaluate(adapter, data.test, baseline=task.baseline)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SDO AIA | 8 EUV/UV channels (specific list TODO verify) | L1, native 12 s | ≈ 2010-05 – 2019 for pretraining; 2010-05 – 2024-07 for SuryaBench downstream | JSOC / SDO archive | `sunpy` / direct JSOC fetch; cf. [[paper-roy-2025-suryabench-ml-benchmark-dataset]] |
| SDO HMI | 5 products (specific list TODO verify; line-of-sight magnetogram, vector magnetogram, Dopplergram, continuum, and one other) | L1.5 / L2 | Same | JSOC | `sunpy` / JSOC |
| Solar-wind-speed labels | V_sw at L1 (OMNI hourly, May 2010 – Dec 2024 per the Surya-bench-solarwind dataset card) | L2 derived | 2010-05-13 – 2024-12-31 | OMNIWeb | `cdflib` |
| Active-region masks | Per-pixel labels for AR segmentation downstream | derived | Same | SuryaBench supplementary; provenance TODO verify in detail | n/a |
| Flare catalog | GOES X-ray peak class | L2 | Same | NOAA SWPC | WebFetch |
| EUV spectra | Reference EVE / Surya-EUV target | L2 | Same | LASP EVE archive | WebFetch |
| Released backbone | `surya.366m.v1.pt`, Apache-2.0 | weights | n/a | Hugging Face: `nasa-ibm-ai4science/Surya-1.0` | `huggingface_hub` |

This skill leans on the companion [[paper-roy-2025-suryabench-ml-benchmark-dataset]] for the standardised ML-ready data and on the per-task benchmark sub-datasets (`nasa-ibm-ai4science/Surya-bench-solarwind`, `surya-bench-flare-forecasting`, `surya-bench-coronal-extrapolation`, etc.).

## 5. Validation target → benchmark artifact

- **Claim**: Surya improves over task-specific baselines on solar-wind-speed forecasting, AR segmentation, flare forecasting, EUV-spectra prediction, AR-emergence forecasting, and coronal-field extrapolation via LoRA fine-tuning, and produces zero-shot solar-dynamics + flare forecasts.
- **Metric**: per-task — solar-wind RMSE / correlation against L1 OMNI V_sw; AR-segmentation IoU; flare-forecasting TSS or HSS; EUV-spectra MSE / spectral correlation. The specific numerical targets are TODO verify against the full PDF.
- **Tolerance**: TODO verify per task.
- **Reference figure**: TODO verify — likely a multi-panel summary of per-task scores vs baselines.

Recommended check artifacts:

- `surya_zeroshot_forecasts.npz` — frame-by-frame zero-shot solar-dynamics outputs at a chosen rollout horizon.
- `surya_finetune_<task>.csv` — per-task LoRA-fine-tuned predictions vs baseline and vs SuryaBench ground truth.
- A LoRA-rank-vs-score curve for at least one downstream task to characterise sensitivity to the adapter rank.

## 6. Failure modes → skill memory

- **Pretraining provenance window.** The released backbone is trained on ~2010–2019 SDO data; LoRA fine-tunes on 2020–2024 SuryaBench slices implicitly assume the pretraining distribution still covers the late-cycle regime. Cross-cycle distribution shift may degrade silently.
- **Channel availability mismatch.** Surya expects the specific 8 AIA + 5 HMI channel set used in pretraining (exact list TODO verify); downstream pipelines with missing channels need explicit handling (zero-fill vs masked attention) and the choice will bias results.
- **LoRA rank choice.** Too-low rank under-fits the downstream task; too-high erases the foundation-model prior. The paper's rank is TODO verify and is the dominant hyperparameter for downstream performance.
- **Autoregressive rollout drift.** Forecast quality degrades non-linearly with rollout horizon; always report metrics at multiple horizons rather than a single number.
- **Solar-cycle leakage.** Chronological splits across the 2010–2024 corpus must avoid leaking future data into training; the SuryaBench split (cf. companion skill) enforces 2020–2024 as test and 2010–2019 as train/val.
- **Compute budget.** Pretraining cost is substantial (≈218 TB input corpus, 4096² inputs, 366 M parameters); only fine-tuning is realistic without dedicated infrastructure. The Apache-2.0 weights release makes fine-tuning the practical path.
- **"First" claims age.** The abstract's "first heliophysics foundation model on full-resolution SDO data" wording is timestamped to 2025; downstream skills should not assert future-tense uniqueness.

## 7. Claim boundary

**In scope.** A 366 M-parameter spatiotemporal-transformer foundation model trained on full-resolution SDO AIA + HMI data using time-advancement as the pretext task, released as Apache-2.0 weights, with LoRA fine-tuning enabling multiple SDO-based downstream solar tasks.

**Out of scope — do NOT generalise beyond:**

- In-situ-only tasks (PSP / Solar Orbiter heliospheric in-situ data) without re-pretraining on an in-situ-aware encoder.
- Generative simulation of solar dynamics (Surya is predictive, not a physics simulator).
- Operational real-time forecasting at sub-minute latency without dedicated inference engineering.
- Cross-mission EUV transfer (STEREO EUVI, GOES SUVI, EUI/Solar Orbiter) without re-pretraining.
- Sub-pixel localisation claims — pretraining and downstream tasks operate at SDO grid resolution.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: https://doi.org/10.48550/arXiv.2508.14112 (arXiv-issued; journal DOI not yet assigned).
- arXiv: https://arxiv.org/abs/2508.14112 (v2, 2025-08-21).
- ADS: TODO verify (no bibcode posted at the time of verification on 2026-05-19).
- Code / weights: Hugging Face `nasa-ibm-ai4science/Surya-1.0` (Apache-2.0; `surya.366m.v1.pt`); reference repo `https://github.com/NASA-IMPACT/Surya` per the model card.
- Data: SDO via JSOC + companion [[paper-roy-2025-suryabench-ml-benchmark-dataset]] benchmark suite.

## 9. Skill graph → depends_on

- `[[paper-roy-2025-suryabench-ml-benchmark-dataset]]` — companion ML-ready dataset; the natural pretraining + fine-tuning source.
- `[[paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation]]` — task-specific baseline for coronal-hole / open-flux segmentation; a Surya LoRA on CH segmentation should be compared against this.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling segmentation pipeline (in-situ vs imagery); shares the labelled-data-scarcity lesson.
- `[[paper-pyspedas-multimission-data-access]]` — in-situ data ingestion for the solar-wind-speed downstream task.

## 10. Research-generation affordances

- **Cross-skill tension.** Surya's "one backbone beats per-task specialists" claim is observational (per-task scores reported); it does not separate gains from the pretraining objective vs gains from the dataset scale. A controlled experiment that fine-tunes from random initialisation on the same SuryaBench splits would isolate the foundation-model contribution.
- **LoRA-rank ablation.** A rank-vs-score curve on the solar-wind-speed task is a high-information, low-cost experiment because the public Hugging Face dataset (`Surya-bench-solarwind`) has fixed splits (train 2010-2019, test 2020-2024).
- **Channel-ablation hypothesis.** Whether the five HMI products are individually necessary (or one of them dominates) is unknown from the abstract. A leave-one-channel-out study at fine-tuning time would surface the load-bearing inputs.
- **Composable experiment with PSP in-situ:** the foundation-model latent embeddings could be used as a global coronal-context feature for an in-situ downstream task (cf. [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]] which explicitly mentions Surya as a downstream-context generator). Specifying this composition requires a deterministic mapping from SDO frames at time `t` to PSP location at time `t`; that mapping is not part of Surya itself.

## Notes

- Surya is an ML-architecture skill, not a physics skill — its scientific claims are about transfer learning and downstream-task performance, not about solar physics directly. Downstream science papers using Surya carry their own claim boundaries.
- The Apache-2.0 weight release (verified on Hugging Face on 2026-05-19) is the most consequential reproducibility artifact: it removes pretraining cost from the reproducer's path and reduces "reproducible" to "load + LoRA-fine-tune + evaluate."
