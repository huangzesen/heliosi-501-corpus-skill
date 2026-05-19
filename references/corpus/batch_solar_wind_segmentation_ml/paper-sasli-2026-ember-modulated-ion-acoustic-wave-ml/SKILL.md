---
name: sasli-2026-ember-modulated-ion-acoustic-wave-ml
description: >-
  Use when running an ML pipeline (EMBER) on PSP FIELDS burst-mode electric-field waveforms to
  detect modulated ion-acoustic waves and correlate them with anomalous core-electron heating —
  central paper claim is that EMBER recovers ~93% of modulated ion-acoustic-wave events linked
  to anomalous core-electron heating, enabling large-scale statistics of small-scale plasma
  processes near the Sun (Sasli et al. 2026, arXiv:2605.00162; venue TODO verify).
version: 0.1.0
tags: [machine-learning, event-detection, ion-acoustic-waves, electron-heating, psp, fields, burst-mode, automated-pipeline]
quality_level: pilot
executable_status: scaffold
---

# Sasli 2026 — EMBER: ML Detection of Modulated Ion-Acoustic Waves on PSP

> Compiled from Sasli, A., Seebaluck, K., Colpitts, C. (2026), *EMBER: Machine-Learning Detection of Modulated Ion Acoustic Waves and Associated Core-Electron Heating in the Solar Wind with Parker Solar Probe*, arXiv:2605.00162 (venue TODO verify).
> **Quality tier**: `pilot scaffold` — claims grounded in the inventory abstract. Specific architecture, training-set definition, and the 93% recall number need full-text confirmation.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Detecting **modulated ion-acoustic waves** (mIAW) in PSP FIELDS burst-mode electric-field waveforms at scale.
- Building automated population statistics of **small-scale plasma processes** (a class of bursty, often missed, electron-heating events).
- Coupling an ML event detector to **anomalous core-electron heating** diagnostics to test causal connections between mIAW occurrence and electron Q_e.
- Choosing between hand-labelled burst-mode event lists and a learnable detector: EMBER is the canonical learnable alternative.

Do NOT use this skill when:

- Looking for **whistler / ion-cyclotron waves** (different polarisation and frequency band; see [[paper-bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] for cyclotron context).
- Building a *survey-mode* (non-burst) wave detector — the paper is specifically tuned to burst-mode waveforms.

## 2. Paper claim → verifiable task

**Claim (narrow form).** A machine-learning pipeline trained on PSP FIELDS burst-mode waveform segments labelled for modulated ion-acoustic waves recovers approximately **93%** of mIAW events (TODO verify exact recall / precision split). The detected events are statistically associated with anomalous core-electron heating signatures.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reconstructs the labelled training / validation set (or its public equivalent) of mIAW-containing burst-mode windows.
2. Trains the model class the paper specifies (CNN / transformer / hybrid — **TODO verify**) on this set.
3. Reports a recall metric within tolerance of the paper's claim on a held-out test set.
4. Cross-references detected mIAW events with core-electron moments (T_e_core, anisotropy, heat flux) and recovers the heating-association reported.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Burst-mode waveform extraction + labelling

- Paper reference: methods — TODO verify section.
- Procedure:
  1. Pull PSP FIELDS DFB / TDS burst-mode E-field waveforms over the encounter set used by the paper (TODO verify encounter list; near-perihelion is the natural choice).
  2. Window the burst captures (typical TDS-style 0.5–3.5 s captures; window length and overlap TODO verify).
  3. Label each window for mIAW presence (positive / negative). The paper's label definition (amplitude threshold, modulation envelope criterion) is TODO verify.

### Algorithm 3.2 — Feature representation

- Procedure (the paper's exact representation is TODO verify; standard candidates):
  - Raw waveform tensor, or
  - Spectrogram (STFT / wavelet), or
  - Hand-engineered features (modulation depth, dominant frequency relative to f_pi).

### Algorithm 3.3 — Model training + evaluation

- Procedure:
  1. Split labelled set into train / validation / test (split fractions TODO verify; insist on event-disjoint splits, not random per-window, to avoid leakage).
  2. Train the EMBER model (architecture TODO verify) with class-imbalance handling — mIAW are rare positives.
  3. Evaluate recall, precision, F1 on the test set. The paper's headline metric is ~93% recall (TODO verify whether this is recall, accuracy, or F1).

### Algorithm 3.4 — Anomalous-core-electron-heating association

- Procedure:
  1. For each detected mIAW event, extract the temporally co-located PSP SWEAP/SPAN-e core-electron moments (T_e_core, T_e_perp/T_e_par, heat flux q_e). Calibration version TODO verify.
  2. Compare T_e_core distributions inside mIAW windows vs. matched mIAW-absent windows. Report a non-zero positive shift consistent with anomalous heating.
  3. Identify the statistical significance level the paper uses (p < 0.01 vs bootstrap CI vs other) — TODO verify.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once architecture and labels are pinned.
def ember_pipeline(burst_waveforms, labels):
    X = represent(burst_waveforms)        # 3.2 — spectrogram or raw, TODO verify
    model = build_ember_model()           # 3.3 — architecture TODO verify
    fit(model, X_train, y_train)
    return evaluate(model, X_test, y_test)  # recall + precision + F1
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| PSP FIELDS DFB / TDS burst | E-field waveform (V/m) | L2 burst-mode (per-capture) | Encounter list — TODO verify | PSP SOC / SPDF | `cdflib`, burst-mode catalog filter; cf. [[paper-pyspedas-multimission-data-access]] |
| PSP SWEAP/SPAN-e | T_e_core, T_e_perp/T_e_par, q_e | L3 | Same encounter window | PSP SOC | `cdflib` |
| PSP SWEAP/SPC, SPAN-i | n_p, V_RTN, T_p | L3 | Same | PSP SOC | `cdflib` |
| (Auxiliary) FIELDS MAG | B_RTN for context | L2 1 vec/s | Same | PSP SOC | `cdflib` |

EMBER does **not** require a named ML MCP — the harness's general-purpose Bash + Python environment is sufficient. The training dataset is the load-bearing artifact and likely lives in the paper's supplementary material (TODO verify the release path).

## 5. Validation target → benchmark artifact

- **Claim**: EMBER recovers ~93% of modulated ion-acoustic wave events on a held-out PSP FIELDS burst-mode test set (TODO verify whether this is recall, precision, accuracy, or F1, and the test-set definition).
- **Metric**: recall on a held-out test set drawn from the same paper-defined labelling rule.
- **Tolerance**: ±2 percentage points on the headline metric (TODO verify; the paper's stated tolerance may differ).
- **Reference figure**: TODO verify — likely a confusion matrix or precision-recall curve in the results section.

Recommended check artifacts:

- `ember_detections.csv` — one row per detection: (t_start, t_end, prob, dominant_f_Hz, modulation_depth, encounter).
- `ember_heating_association.csv` — paired (mIAW-window, control-window) electron moments and the per-window T_e_core differential.
- A confusion-matrix panel on the held-out test set.

## 6. Failure modes → skill memory

- **Label leakage across windows.** Burst captures often come in clusters; random per-window splits inflate recall. Always use event-level (or encounter-level) splits.
- **Class imbalance.** mIAW are rare positives; un-weighted training collapses to the majority class. The paper's weighting scheme is TODO verify and must be reproduced.
- **Spectrogram window choice.** STFT window length and overlap strongly shape the spectrogram features; sub-optimal choices erase the modulation envelope.
- **Burst-mode trigger bias.** PSP FIELDS burst captures are not uniformly sampled in time — they are triggered. Population statistics derived from EMBER detections are conditional on the trigger; the "anomalous heating association" must control for the trigger.
- **Core-electron moment calibration.** SPAN-e T_e_core can be biased by photoelectron contamination near perihelion; verify the calibration version (TODO verify which calibration the paper used).
- **mIAW ≠ unmodulated IAW.** The detector targets *modulated* events; unmodulated ion-acoustic waves are a different class and the recall does not apply.
- **"93%" is a single-number summary.** A confusion matrix at the paper's chosen threshold may show high recall but low precision (or vice versa). Always report both.

## 7. Claim boundary

**In scope.** ML detection of modulated ion-acoustic waves on PSP FIELDS burst-mode E-field waveforms during the encounters used by the paper, and the statistical association of those detections with anomalous core-electron heating.

**Out of scope — do NOT generalise beyond:**

- Other wave classes (whistler, ICW, KAW) — they are out of EMBER's training distribution.
- Survey-mode (non-burst) FIELDS data — the model is trained on burst-mode windows.
- Causal claims about mIAW → core-electron heating direction — the paper's association is statistical; causality requires additional case-study evidence.
- Other spacecraft (Wind / Solar Orbiter / MMS) — re-training is required.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill that covers it (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2605.00162
- ADS: TODO verify.
- Code: TODO verify — likely supplementary or GitHub repo; the inventory does not list one.
- Data: PSP FIELDS burst-mode + SWEAP via PSP SOC / SPDF (public).

## 9. Skill graph → depends_on

- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling ML event detector for a different solar-wind structure (ICMEs vs. mIAW); shares the event-split + class-imbalance lessons.
- `[[paper-hu-2022-deep-swim-cnn-discontinuities]]` — sibling few-shot CNN classifier for solar-wind B-field discontinuities; shares the windowed-waveform input pattern.
- `[[paper-pyspedas-multimission-data-access]]` — PSP burst-mode data ingestion (infrastructure).
- `[[paper-bowen-2023-landau-damping-proton-electron-heating]]` — Q_e channel context (Landau-damping cascade view of core-electron heating).

## Notes

- The "93%" number is the single most-quoted result in the abstract; a benchmarked promotion requires (i) the exact metric definition, (ii) the test-set split, (iii) the threshold at which the metric is reported, and (iv) precision alongside recall.
