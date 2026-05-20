---
name: sasli-2026-ember-modulated-ion-acoustic-wave-ml
description: >-
  Use when running EMBER (Electron heating from Modulated Burst-mode Event
  Recognition) on PSP FIELDS Digital Burst Memory (DBM) voltage waveforms to
  detect modulated ion-acoustic waves (mIAWs — including triggered IAWs and
  frequency-dispersed IAWs) and correlate them with anomalous core-electron
  heating. Central paper claim: an ensemble of 16 background-only anomaly
  detectors (physics-motivated + classical outlier + deep-learning), run on
  log-scaled Fourier spectrograms of DBM bursts from PSP Encounters 6–9 and 15,
  recovers ≈ 93 % of labelled mIAW events at an estimated 1 % FAR on a
  curated catalog of 42 anomalous + 496 background spectrograms; flagged
  intervals show core perpendicular T_e above adiabatic cooling and elevated
  T_e/T_i ratios, reproducing previously reported heating phenomenology
  without using temperatures in the detection step. Sasli et al. 2026,
  arXiv:2605.00162, submitted to Earth and Space Science.
version: 0.1.0
tags: [machine-learning, event-detection, anomaly-detection, ion-acoustic-waves, electron-heating, psp, fields, dbm, burst-mode, ensemble-detector, automated-pipeline]
quality_level: paper-grounded-pending-full-text
executable_status: scaffold
paper:
  authors_verified: true
---

# Sasli 2026 — EMBER: Anomaly-Ensemble ML for Modulated Ion-Acoustic Waves on PSP

> Compiled from Sasli, Seebaluck, Colpitts, Coughlin (2026), *EMBER:
> Machine-Learning Detection of Modulated Ion Acoustic Waves and
> Associated Core-Electron Heating in the Solar Wind with Parker Solar
> Probe*, arXiv:2605.00162 v1 (submitted to *Earth and Space Science*;
> arXiv submission 2026-04-30). Authors (University of Minnesota), Key
> Points block, abstract, data source (PSP FIELDS DBM bursts on
> Encounters 6–9 and 15), representation (log-scaled Fourier
> spectrograms, ~524 288 samples per burst), method (ensemble of 16
> background-only anomaly detectors combining physics-motivated,
> classical outlier, and deep-learning detectors), curated catalog size
> (**42 anomalous + 496 background DBM spectrograms**), and headline
> metric (**~93 % recall at ~1 % FAR ≈ 1 false positive per 100 held-out
> backgrounds**, explicitly flagged as approximate because background
> statistics are limited) were cross-checked against the arXiv abs page
> and the full PDF on 2026-05-19. Electron-moment side: SWEAP/SPAN-e
> shows core perpendicular T_e above adiabatic cooling and elevated
> T_e/T_i in flagged intervals.
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic
> anchors, ensemble size, representation, encounter list, catalog
> counts, and headline metric verified; per-detector weights, exact
> network architectures inside the ensemble, and the per-encounter
> distribution of positives can be read off later sections of the PDF.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Detecting **modulated ion-acoustic waves** (mIAW — including TIAWs and FDIAWs) in PSP FIELDS DBM voltage waveforms at scale, replacing expert visual inspection.
- Building automated population statistics of **small-scale plasma processes** that drive nonlinear electron heating but are missed by survey-mode pipelines.
- Coupling an ML event detector to **anomalous core-electron heating diagnostics** (SWEAP/SPAN-e) to test the statistical link between mIAW occurrence and T_e enhancement without circular use of T_e as a detector feature.
- Generating **per-burst latent embeddings** that can be combined with global coronal-context features from foundation models like [[paper-roy-2025-surya-heliophysics-foundation-model]] (the EMBER paper explicitly motivates this composition).

Do NOT use this skill when:

- Looking for **whistler / ion-cyclotron waves** (different polarisation and frequency band; see [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] for cyclotron context).
- Working with PSP **survey-mode** (non-burst) FIELDS data — EMBER is trained on burst-mode DBM windows.
- Asserting causal direction (mIAW → heating) — the paper's association is statistical (cross-validation against SWEAP without using T_e in the detector).

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the Key Points block and §4–§5).**
EMBER converts each PSP FIELDS **Digital Burst Memory (DBM)** voltage
burst (~524 288 samples per capture) into a **log-scaled Fourier
spectrogram** and applies a suite of **16 background-only anomaly
detectors** combining physics-motivated detectors, classical outlier
detectors, and deep-learning detectors. On a curated catalog of **42
anomalous + 496 background DBM spectrograms drawn from PSP Encounters
6, 7, 8, 9, and 15**, the ensemble recovers **~93 % of labelled
anomalous events at an estimated ~1 % FAR** (i.e., ≈ 1 false positive
per 100 held-out backgrounds — the paper itself notes this number is
approximate because background statistics are limited). Intervals
flagged by EMBER, when cross-referenced with coincident SWEAP/SPAN
diagnostics that were *not* used during detection, show **core
perpendicular electron temperatures above the adiabatic-cooling
expectation and elevated T_e/T_i**, reproducing previously reported
preferential-heating phenomenology.

**Verifiable task.** A reproduction succeeds when an agent:

1. Pulls PSP FIELDS DBM burst captures for Encounters 6–9 and 15 and reproduces the curated catalog (42 positives, 496 backgrounds) from the paper's labelling rule.
2. Computes log-scaled Fourier spectrograms (~524 288 samples per burst) per the paper's STFT configuration.
3. Trains the ensemble of 16 background-only anomaly detectors on the background sub-corpus (no anomaly labels used at training time — they are held out as test positives).
4. Evaluates the ensemble at the paper's threshold and recovers **recall ≈ 93 % at FAR ≈ 1 %** on the held-out positives within the paper's stated approximation envelope.
5. Cross-references detections with PSP SWEAP/SPAN-e core perpendicular T_e and T_e/T_i and reproduces the heating-association signal (core T_perp above adiabatic, elevated T_e/T_i) without those quantities entering the detector.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — DBM burst extraction + labelling

- Procedure:
  1. Pull PSP FIELDS DBM L2 voltage waveforms for **PSP Encounters 6, 7, 8, 9, and 15** from the PSP SOC / SPDF.
  2. Each DBM burst contains ~524 288 samples; the 6-hour DBM block contains dozens of such windows.
  3. Label each burst as anomalous (positive) or background using the paper's catalog (42 anomalous + 496 background spectrograms). The exact thresholding for the modulation envelope criterion is TODO verify from §3 of the paper.

### Algorithm 3.2 — Spectrogram representation

- Convert each DBM voltage burst to a **log-scaled Fourier spectrogram** (the paper calls out "log-scaled Fourier spectrograms" in the abstract).
- STFT window length and overlap are TODO verify from §3 — these strongly shape whether the modulation envelope is preserved.
- The representation is fixed for **all** 16 detectors in the ensemble; only the downstream detector identity changes.

### Algorithm 3.3 — Ensemble of 16 background-only anomaly detectors

- Three detector families combined into one ensemble:
  - **Physics-motivated detectors** — e.g., narrowband peak-detection at f_pi, modulation-depth thresholds.
  - **Classical outlier detectors** — e.g., isolation forest, one-class SVM, robust covariance.
  - **Deep-learning detectors** — e.g., autoencoder reconstruction-error, variational autoencoder log-likelihood.
- **Background-only training:** detectors fit *only* on the background sub-corpus; anomalies are held out and are scored at inference. This is a one-class anomaly-detection setup, not a supervised binary classifier — it sidesteps the class-imbalance problem because labels are only used at evaluation.
- Detector ensemble combination weighting + per-detector architectures are TODO verify from §3.

### Algorithm 3.4 — Heating-association cross-check (SWEAP/SPAN-e)

- Procedure:
  1. For each DBM burst flagged by the ensemble, identify the temporally co-located PSP SWEAP/SPAN-e core-electron moments (core perpendicular T_e, core parallel T_e, T_e/T_i).
  2. Compare the distribution of these moments inside flagged windows vs **matched background-only windows**.
  3. Confirm the published signature: core T_perp above adiabatic-cooling expectation and elevated T_e/T_i. The detector did not use these quantities, so the test is not circular.

Code skeleton (scaffold tier; concrete on encounter list and catalog sizes):

```python
# Pseudocode aligned to the paper's §3–§5 (Sasli et al. 2026).
def ember_pipeline(dbm_paths, span_paths, threshold):
    bursts = load_dbm(dbm_paths, encounters=[6, 7, 8, 9, 15])  # ~524288 samples each
    spec = log_fourier_spectrogram(bursts)
    detectors = [physics_detector_i(), ...,
                 classical_outlier_j(), ...,
                 deep_anomaly_detector_k(), ...]   # 16 total
    fit_background_only(detectors, spec_background_only=spec[is_background(bursts)])
    scores = ensemble_score(detectors, spec)        # shape (N, 16) → 1 ensemble score
    flagged = scores > threshold
    span_moments = load_span_e_moments(span_paths)
    heating = heating_association_test(
        flagged_windows=flagged, background_windows=~flagged,
        moments=span_moments[["Te_perp", "Te_par", "Te_over_Ti"]],
    )
    return flagged, heating  # recall ≈ 93% at FAR ≈ 1%
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| PSP FIELDS DBM | E-field voltage waveform (~524 288 samples per burst) | L2 burst-mode (per-capture) | PSP Encounters 6, 7, 8, 9, 15 | PSP SOC / SPDF | `cdflib`, burst-mode catalog filter; cf. [[paper-pyspedas-multimission-data-access]] |
| PSP SWEAP/SPAN-e | core T_e perpendicular and parallel; T_e/T_i | L3 | Same encounter windows | PSP SOC | `cdflib` |
| PSP SWEAP/SPC, SPAN-i | n_p, V_RTN, T_p (for T_e/T_i ratio context) | L3 | Same | PSP SOC | `cdflib` |
| Auxiliary FIELDS MAG | B_RTN for context | L2 1 vec/s | Same | PSP SOC | `cdflib` |

EMBER is published as an **open-source Python pipeline** ("Ember … an open-source pipeline" per the Key Points block); the exact GitHub URL is TODO verify (the abs page does not list one at verification time on 2026-05-19, but the Key Points block explicitly advertises it as open source).

## 5. Validation target → benchmark artifact

- **Claim**: EMBER recovers **~93 % of anomalous mIAW events at ~1 % FAR (≈ 1 false positive per 100 held-out backgrounds)** on a curated catalog of **42 anomalous + 496 background DBM spectrograms** drawn from PSP Encounters 6–9 and 15. The paper itself notes this number is approximate due to limited background statistics.
- **Metric**: recall at fixed FAR on a held-out test set drawn from the same curated catalog. Precision is bounded by the catalog imbalance (42 positives / 496 backgrounds ≈ 7.8 % prior).
- **Tolerance**: the paper explicitly flags the 93 % / 1 % numbers as approximate; a reproducer should additionally report a bootstrap CI given the small positive-class size (n = 42). The paper's own stated tolerance in §4 is TODO_verify — provisional: ±2 percentage points on the headline recall.
- **Reference figure**: TODO verify the specific figure number in §4 that visualises the precision–recall (or recall–FAR) curve at the operating point.

Recommended check artifacts:

- `ember_detections.csv` — one row per detection: `(t_start, t_end, prob, dominant_f_Hz, modulation_depth, encounter)`.
- `ember_heating_association.csv` — paired (mIAW-window, control-window) electron moments and the per-window T_e_perp differential.
- A confusion-matrix or PR-curve panel on the held-out test set with bootstrap CIs.

## 6. Failure modes → skill memory

- **Limited background statistics.** The paper's own Key Points block flags the 1 % FAR estimate as approximate because background statistics are limited (496 background spectrograms is not a huge sample for a tail-of-the-distribution FAR estimate). Downstream consumers should report bootstrap CIs, not point estimates.
- **Encounter selection bias.** Encounters 6, 7, 8, 9, 15 are not a uniform sample of the PSP mission; mIAW prevalence depends on heliocentric distance and stream type. Population statistics from EMBER detections are conditional on this encounter set.
- **Burst-mode trigger bias.** PSP FIELDS DBM captures are triggered, not uniformly sampled in time. Statistical statements about mIAW rates "per unit time" must condition on the trigger; the heating-association cross-check inherits this conditioning.
- **STFT window choice.** Window length and overlap shape the spectrogram; sub-optimal choices erase the modulation envelope and would silently drop the recall.
- **Background-only training is one-class anomaly detection.** It is robust to class imbalance but is sensitive to background-distribution shift — a non-stationary background within the curated catalog would inflate the apparent FAR.
- **Core T_e calibration version.** SWEAP/SPAN-e T_e can be biased by photoelectron contamination near perihelion; the calibration version used for the heating-association test is TODO verify from §5.
- **mIAW ≠ unmodulated IAW.** The detector targets *modulated* events (TIAWs and FDIAWs); unmodulated ion-acoustic waves are a different class and the 93 % recall does not apply.
- **Causal direction not established.** The heating-association cross-check is statistical, not causal — both directions (waves drive heating vs heating drives wave generation) remain consistent with the observation.
- **"93 %" is one number with one threshold.** Always report the full recall–FAR curve, not just the operating point.

## 7. Claim boundary

**In scope.** ML detection of modulated ion-acoustic waves on PSP FIELDS DBM burst-mode E-field waveforms from Encounters 6–9 and 15, and the statistical association of those detections with anomalous core-electron heating measured by SWEAP/SPAN-e in the same encounters.

**Out of scope — do NOT generalise beyond:**

- Other wave classes (whistler, ICW, KAW) — they are out of EMBER's training distribution.
- Survey-mode (non-burst) FIELDS data — the model is trained on burst-mode DBM windows.
- Causal claims about mIAW → core-electron heating direction.
- PSP Encounters outside the 6–9 / 15 training set without re-validation.
- Other spacecraft (Wind / Solar Orbiter / MMS) — re-training on different instrument calibrations is required.
- Population-level rate estimates that do not condition on the DBM trigger.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill that covers it (or report none).

## 8. Links

- DOI: https://doi.org/10.48550/arXiv.2605.00162 (arXiv-issued; journal DOI from *Earth and Space Science* TODO verify once issued).
- arXiv: https://arxiv.org/abs/2605.00162 (v1, 2026-04-30).
- ADS: TODO verify (no bibcode posted at verification time).
- Code: open-source Python pipeline (advertised in the Key Points block); exact GitHub URL TODO verify from §3 of the PDF or supplementary.
- Data: PSP FIELDS DBM + SWEAP via PSP SOC / SPDF (public).

## 9. Skill graph → depends_on

- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling ML event detector for a different solar-wind structure (ICMEs vs mIAW); shares the event-split + class-imbalance lessons.
- `[[paper-hu-2022-deep-swim-cnn-discontinuities]]` — sibling ML event classifier on Wind/MFI windows; shares the small-labelled-set regime and the contrast between supervised (Deep-SWIM) and one-class anomaly (EMBER) approaches.
- `[[paper-pyspedas-multimission-data-access]]` — PSP burst-mode data ingestion (infrastructure).
- `[[paper-bowen-2023-landau-damping-proton-electron-heating]]` — Q_e channel context (Landau-damping cascade view of core-electron heating, complementary to mIAW-driven heating).
- `[[paper-roy-2025-surya-heliophysics-foundation-model]]` — explicitly named in §1 as a downstream foundation-model context provider; EMBER detections could be cross-walked to Surya latent embeddings.

## 10. Research-generation affordances

- **Mission-wide population scan.** The published evaluation covers only Encounters 6–9 and 15; running the trained ensemble on all PSP encounters and reporting the per-encounter detection rate (with bootstrap CIs given small background statistics per encounter) is a high-value follow-up.
- **Detector-ablation study.** The 93 % recall comes from a 16-detector ensemble combining three families (physics + classical + deep). A leave-one-detector-out study would surface which family is load-bearing and whether the deep-learning component is necessary.
- **Threshold-uncertainty quantification.** The paper explicitly flags the 1 % FAR as approximate. A bootstrap-CI study on FAR at fixed recall (and recall at fixed FAR) using the 496 backgrounds is a direct mitigation that does not require additional data.
- **Causal-direction test.** Using survey-mode SWEAP/SPAN-e T_e to bin epochs and only then asking whether DBM-burst-triggered mIAW rates differ between high-T_e and low-T_e epochs would test the inverse hypothesis (heating triggers waves), separately from the published direction.
- **Composable experiment with [[paper-roy-2025-surya-heliophysics-foundation-model]]:** the Surya latent embeddings provide a global coronal-context fingerprint at the time of each DBM burst. Adding the Surya latent as a feature to the ensemble would test whether large-scale coronal structure improves mIAW recall — a direct realisation of the foundation-model-context vision the paper's §6 floats.

## Notes

- The "93 % at 1 % FAR" headline is one operating point; the recall–FAR curve and the bootstrap CIs around this point are the load-bearing artifacts for any benchmarked-tier promotion.
- The dataset description matches the paper precisely (PSP Encounters 6–9 and 15, 42 anomalous + 496 background DBM spectrograms, ~524 288 samples per burst), but the per-encounter distribution of positives and the per-detector weights inside the 16-member ensemble are not enumerated in the abstract / Key Points block and require the §3–§4 body.
