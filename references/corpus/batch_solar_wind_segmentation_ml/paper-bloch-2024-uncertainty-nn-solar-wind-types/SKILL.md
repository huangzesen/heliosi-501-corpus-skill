---
name: bloch-2024-uncertainty-nn-solar-wind-types
description: >-
  Use when applying probabilistic neural networks with Shannon-entropy
  uncertainty estimates to assign 1-minute Wind-spacecraft 1-au solar-wind
  intervals to four physical types (coronal hole, streamer-belt, sector-reversal,
  magnetic obstacle / solar transient), optionally extended to five classes by
  adding sheath. Central paper claim is that an 8-parameter probabilistic neural
  network ("8PNN") reaches ~96 % accuracy and macro-F1 ≈ 0.96 on the four-class
  scheme, with per-prediction Shannon-entropy uncertainty enabling threshold-based
  abstention (Narock et al. 2024, arXiv:2409.09230, Solar Physics in press).
  Note: the slug retains a legacy first-author placeholder; the verified lead
  author is Tom Narock (Goucher College), not Bloch.
version: 0.1.0
tags: [machine-learning, probabilistic-neural-network, solar-wind-classification, uncertainty-quantification, four-class, five-class, sheath, wind-mfi-swe, 1au]
quality_level: paper-grounded-pending-full-text
executable_status: scaffold
paper:
  authors_verified: true
---

# Narock 2024 — Probabilistic-NN Classification of 1-au Solar-Wind Types with Uncertainty

> Compiled from Narock, Pal, Arsham, Narock, Nieves-Chinchilla (2024),
> *Classifying different types of solar wind plasma with uncertainty
> estimations using machine learning*, arXiv:2409.09230 (submission
> 2024-09-13). Authors, abstract, methods (Wind MFI + SWE 1-minute data;
> probabilistic NN with Shannon entropy as the aleatoric uncertainty
> proxy), and headline accuracy figures (3-parameter PNN macro-F1 0.8764,
> accuracy 87.79 %; 8-parameter PNN macro-F1 0.9628, accuracy 96.32 %)
> were cross-checked against the arXiv abs page and the full PDF on
> 2026-05-19. The submission is listed as *Solar Physics* in the PDF header
> (placeholder DOI `10.1007/...`), pending the journal-issued DOI.
> The legacy slug "bloch-2024" is preserved for cross-batch link stability;
> the verified lead author is Tom Narock (Goucher College).
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic anchors,
> data source, architecture family, headline accuracy numbers, and uncertainty
> method verified; per-class confusion-matrix values and feature-importance
> ranking can be read from the full PDF if needed.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Producing **per-time-step class probabilities with calibrated uncertainty** for the 4-class (or 5-class with sheath) 1-au solar-wind labelling scheme on Wind data.
- Needing to **abstain on low-confidence intervals** via a user-specified Shannon-entropy threshold rather than force a label — KNN-style classifiers (cf. [[paper-camporeale-2017-knn-solar-wind-categorization]]) do not natively expose calibrated per-prediction uncertainty.
- Coupling solar-wind class probabilities downstream to a **risk-aware space-weather product** that needs uncertainty as input (the paper specifically motivates real-time forecasting).
- Replacing a window-based classifier (Nguyen 2019 / Rüdisser 2022) with a **point-by-point** classifier — the abstract emphasises per-timestep prediction over windowed approaches.

Do NOT use this skill when:

- The downstream product is a binary or event-level decision (use [[paper-rudisser-2022-icme-unet-automatic-detection]] for ICME segmentation).
- No labelled training set exists — go unsupervised ([[paper-regan-2026-mars-solar-wind-ml-classification]], [[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]).
- Working at near-Sun PSP distances — the 1-au labelling scheme and the 1-min Wind feature engineering do not transfer.

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the abstract and §4 Results).** A
probabilistic neural network trained on 1-minute Wind spacecraft features
(MFI magnetic field + SWE plasma) and labelled by an extension of the
Xu–Borovsky 4-class scheme that generalises "ejecta" to **magnetic obstacle
(MO)**, classifies each 1-min time-step into one of four types — **coronal
hole (CH), streamer-belt (SB), sector-reversal (SR), magnetic obstacle
(MO)** — and outputs per-step class probabilities plus a **Shannon-entropy
uncertainty score** drawn from the same softmax output. The **3-parameter
PNN ("3PNN")** using Xu–Borovsky's `(V_a, T_ratio, Entropy)` reaches
macro-F1 ≈ 0.8764 and 87.79 % accuracy. The **8-parameter PNN ("8PNN")**
adding cross helicity `σ_c`, residual energy `σ_r`, plasma β, B_rms, and
total pressure `P_tot` reaches **macro-F1 ≈ 0.9628 and ≈ 96.3 % accuracy**.
A 5-class extension adding **sheath (SH)** is reported but the model
"regularly misclassifies SHs as MOs and vice versa", confirming SH is not
yet cleanly distinguishable as a single class.

**Verifiable task.** A reproduction succeeds when an agent:

1. Pulls Wind MFI + SWE 1-minute L2 data and derives the 8 input features (`V_a`, `T_ratio`, `Entropy`, `σ_c`, `σ_r`, `B_rms`, plasma β, `P_tot`) using the formulae in §2 of the paper.
2. Assembles labels by extending Xu–Borovsky (2015) with the Nieves-Chinchilla (2018) magnetic-obstacle definition.
3. Trains the 8PNN with a softmax output and uses Shannon entropy `H = -Σ p_i ln p_i` as the per-prediction aleatoric uncertainty proxy.
4. Recovers macro-F1 ≈ 0.96 and accuracy ≈ 96 % on the 4-class test set within a tolerance the paper reports (per-class confusion-matrix entries TODO verify against the full PDF).
5. Sweeps the uncertainty threshold and demonstrates that lower thresholds give fewer-but-more-confident predictions (the paper's abstention behaviour is qualitative; the exact operating point is TODO verify).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Labelled-data assembly (1-au, 4-class, Wind 1-min)

- Procedure:
  1. Pull Wind/MFI B (GSE) and Wind/SWE plasma moments (`n_p`, `V_sw`, `T_p`) at **1-minute** cadence from CDAWeb / SPDF.
  2. Compute per-minute features from §2 of the paper:
     - `V_a = B / sqrt(μ_0 m_p N_p)`
     - `T_ratio = T_expected / T_p` (Xu–Borovsky convention)
     - `Entropy = T_p / N_p^(2/3)`
     - `σ_c = (E_+ − E_−)/(E_+ + E_−)` from Elsasser-variable trace spectral densities (cross helicity)
     - `σ_r = (E_v − E_b)/(E_v + E_b)` (residual energy)
     - `B_rms` over 10-minute windows (per Salman et al. 2021 definition)
     - plasma β, `P_tot`
  3. Apply the Xu–Borovsky (2015) classification rule, replacing the "ejecta" category with the Nieves-Chinchilla (2018) magnetic-obstacle (MO) definition. Use a chronologically blocked test set; do not random-split.

### Algorithm 3.2 — PNN architecture + Shannon-entropy uncertainty

- Procedure:
  1. Build a probabilistic neural network classifier with a softmax output layer over K=4 (or K=5 if including sheath) classes. Architecture is implemented in Keras / TensorFlow per the paper.
  2. The paper treats the softmax distribution as a proxy for aleatoric uncertainty (i.e., the irreducible noise component, not epistemic). Per the paper, "techniques for quantifying both aleatoric and epistemic uncertainty do exist" but the 8PNN as published quantifies aleatoric only.
  3. Quantify per-prediction uncertainty as Shannon entropy: `H = -Σ p_i ln p_i`, ranging in (0, -ln(1/K)].
  4. Output per-step `(p_CH, p_SB, p_SR, p_MO, H)`; or for the 5-class variant `(p_CH, p_SB, p_SR, p_MO, p_SH, H)`.

### Algorithm 3.3 — Calibration + abstention curve

- Procedure:
  1. Hold a chronologically blocked test set with the ICME / MO catalog overlay used by the paper.
  2. Generate the macro-averaged precision, recall, F1, and accuracy on the test set (the paper reports 3PNN macro-F1 0.8764 / accuracy 87.79 % and 8PNN macro-F1 0.9628 / accuracy 96.32 %).
  3. Sweep a user-specified Shannon-entropy threshold `H_max`: predictions with `H ≥ H_max` are returned as "unclassified" rather than forced to a class.
  4. Identify a risk-averse operating point (low `H_max` → fewer but higher-confidence predictions) consistent with the paper's discussion. The specific operating-point value the paper recommends is TODO verify.

Code skeleton (scaffold tier; runnable once feature derivation is wired):

```python
# Pseudocode aligned to the paper's PNN + Shannon-entropy formulation.
import numpy as np

def shannon_entropy(probs):
    eps = 1e-12
    return -np.sum(probs * np.log(probs + eps), axis=-1)

def narock2024_8pnn(features, labels, threshold_H):
    model = build_pnn_softmax(n_in=8, n_out=4)   # Keras MLP per the paper
    model.fit(features.train, labels.train)
    probs = model.predict(features.test)
    H = shannon_entropy(probs)
    y_hat = probs.argmax(axis=-1)
    abstain = H >= threshold_H
    return y_hat, probs, H, abstain
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Wind/MFI | B (GSE) | L2 1-minute | Wind mission window (1994 onwards; exact interval TODO verify) | CDAWeb / SPDF | `cdflib` |
| Wind/SWE | n_p, V_sw, T_p | L2 1-minute | Same | CDAWeb / SPDF | `cdflib` |
| ICME / MO catalog | event boundaries for MO labels | derived | Same | Nieves-Chinchilla MO catalog (TODO verify catalog URL) | n/a |
| Xu–Borovsky labels | 3-parameter classification rule | derived | Same | Xu & Borovsky 2015 (computed on-the-fly from MFI+SWE features) | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: 8PNN reaches **macro-F1 ≈ 0.9628 and accuracy ≈ 96.32 %** on the 4-class scheme (3PNN reaches macro-F1 ≈ 0.8764 and accuracy ≈ 87.79 %); Shannon-entropy per-prediction uncertainty enables threshold-based abstention.
- **Metric**: macro-averaged precision, recall, F1, and accuracy on a chronologically blocked test set; per-class confusion-matrix entries available in Figure 1 of the paper (per-class numbers TODO verify by reading off the published figure).
- **Tolerance**: TODO verify (the paper does not quote an explicit tolerance; ≤ 1 percentage point on accuracy is a reasonable target given the headline-number precision).
- **Reference figure**: Figure 1 (confusion matrices for 3PNN and 8PNN); Figure 2 (8PNN feature importance via Integrated Gradients) — referenced in §4 of the paper.

Recommended check artifacts:

- `narock2024_predictions.csv` — one row per 1-min step: `(t, V_a, T_ratio, Entropy, σ_c, σ_r, B_rms, β, P_tot, p_CH, p_SB, p_SR, p_MO, H, label_truth)`.
- A confusion-matrix panel for both 3PNN and 8PNN at the paper's reported operating point.
- An abstention curve (accuracy vs coverage as `H_max` is swept).

## 6. Failure modes → skill memory

- **Shock contamination biases the 3-parameter scheme.** §4.1 of the paper notes that shocks (which precede sheaths) disrupt the Xu–Borovsky `(V_a, T_ratio, Entropy)` relationships and produce mislabelling in the period just before sheath arrival. The 8PNN partially mitigates this.
- **Sheath identification fails as a single class.** The 5-class extension (`+SH`) "regularly misclassifies SHs as MOs and vice versa" per §4.3; SH classification needs sub-typing the paper explicitly defers to future work.
- **Epistemic uncertainty is not captured.** The Shannon entropy on a softmax output is an *aleatoric* uncertainty proxy only; ensemble or Bayesian methods would be needed to capture epistemic uncertainty (model-parameter uncertainty), and the paper flags this as future work.
- **Class imbalance.** Transients (MO) are rare relative to CH/SB/SR; macro-averaged metrics intentionally give equal weight to each class — micro-averaged numbers would be dominated by CH/SB and inflate accuracy.
- **Chronological vs random splits.** Required for honest evaluation; random splits leak future labels and inflate the 96 % accuracy.
- **Label noise floor.** Xu–Borovsky / MO labels carry inherent boundary disagreement (typically several percent near class transitions); an irreducible-noise floor.
- **Wind-only training.** The model is trained on Wind 1-min data; transferring to ACE or DSCOVR would require feature-level recalibration and a cross-instrument validation step the paper does not perform.
- **End-of-MO inaccuracy.** §4.2 reports that incorrect predictions concentrate in the *trailing third* of MO intervals (5 % vs 2 % in the leading third), consistent with the physical erosion of MO outer layers via reconnection. Downstream consumers should weight late-MO predictions accordingly.

## 7. Claim boundary

**In scope.** Per-1-min supervised 4-class (or 5-class) classification of 1-au Wind solar-wind intervals with **aleatoric** uncertainty estimates (Shannon entropy on PNN softmax outputs), trained on Xu–Borovsky-extended labels with magnetic obstacles.

**Out of scope — do NOT generalise beyond:**

- Distances other than 1 au.
- Labelling schemes other than the Xu–Borovsky 4-class extension with MO (and optionally SH).
- **Epistemic** uncertainty quantification — the published method captures aleatoric only.
- Out-of-distribution detection without re-validation — calibration is *in-distribution* by default.
- Per-event boundary detection — the model is per-timestep classification, not segmentation.
- Real-time forecasting on missions other than Wind without re-training.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: https://doi.org/10.48550/arXiv.2409.09230 (arXiv-issued; the *Solar Physics* DOI placeholder `10.1007/...` is printed in the PDF header — TODO verify the final journal DOI once issued).
- arXiv: https://arxiv.org/abs/2409.09230 (submission 2024-09-13).
- ADS: TODO verify (no bibcode posted at verification time).
- Code: TODO verify — the paper does not publish a repo URL on the abs page.
- Data: Wind/MFI + Wind/SWE L2 1-min via CDAWeb / SPDF (public).

## 9. Skill graph → depends_on

- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — predecessor (Gaussian-process undecided-class scheme); the paper explicitly cites Camporeale, Carè & Borovsky 2017 as a prior uncertainty-aware classifier.
- `[[paper-regan-2026-mars-solar-wind-ml-classification]]` — unsupervised alternative at Mars.
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — symbolic-clustering alternative; provides a different uncertainty proxy via cluster-assignment entropy.
- `[[paper-koikkalainen-2025-complexity-solar-wind-streams]]` — feature-side enhancement (information-theory complexity).
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — window-based ICME segmenter the paper contrasts with its point-by-point approach.

## 10. Research-generation affordances

- **Sheath sub-typing.** §4.3 explicitly defers sheath sub-types (preceded by shock vs CH vs MO) to future work. A natural follow-up is to train a hierarchical classifier — first detect SH vs not-SH, then sub-type SHs by the preceding solar-wind class — and measure whether macro-F1 on the 5-class scheme recovers above 0.90.
- **Epistemic-uncertainty ablation.** Replacing the softmax-entropy proxy with a Deep-Ensemble or MC-Dropout variant and measuring whether out-of-distribution intervals (e.g., near-perihelion PSP-style regimes if features were homogenised) produce systematically higher epistemic entropy is a high-information research direction.
- **Feature-importance generalisability.** Figure 2's IG ranking flags `P_tot` and plasma β as load-bearing; cross-checking this ranking under a SHAP method and on independent Wind windows would test feature-importance robustness.
- **Cross-mission transfer.** Re-training on ACE/SWEPAM at 1 min and reporting the macro-F1 delta vs the Wind-trained model directly quantifies how mission-specific the 8PNN's calibration is — a prerequisite for any operational deployment downstream.

## Notes

- The "uncertainty method" identity is the single highest-impact reproducibility detail — softmax + Shannon entropy (aleatoric only) is qualitatively different from MC-Dropout or Deep Ensembles (which would capture epistemic uncertainty). Downstream skills must not assume the published model is fully Bayesian.
- The slug `bloch-2024-uncertainty-nn-solar-wind-types` is a legacy artefact from an earlier inventory phase. The actual lead author is **Tom Narock (Goucher College)** with Sanchita Pal (NASA GSFC), Aryana Arsham (Goucher), Ayris Narock (ADNET/NASA GSFC), and Teresa Nieves-Chinchilla (NASA GSFC). The slug is preserved here only for cross-batch link stability; consumer-facing prose and the metadata `authors[]` list reflect the verified citation.
