---
name: anti-equilibrium-alfven-ion-cyclotron-effects-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# anti-equilibrium-alfven-ion-cyclotron-effects-2023

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from the primary source (author list pending verification), 2023 (TODO_verify_journal; arXiv:2308.14944).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict how non-equilibrium (non-Maxwellian) VDFs shift Alfvén ion-cyclotron (AIC) wave growth rates.
- Decide whether observed AIC-wave occurrence intervals require non-Maxwellian VDFs to explain growth.

### When NOT to use it

- Pure bi-Maxwellian AIC growth — see [[ion-driven-instabilities-classification-2023]].

### Claim boundary

Linear-Vlasov analysis using observed (non-Maxwellian) VDFs. Growth-rate shifts quantified relative to bi-Maxwellian baseline.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Non-equilibrium VDF features (beams, shoulders) shift AIC γ_max by paper-quantified factors; some observed AIC intervals are only explainable with non-Maxwellian closure.

### 2.2 Equations / method

- Linear-Vlasov dispersion with observed VDF inputs.
- γ_max(observed VDF) / γ_max(bi-Maxwellian fit).

### 2.3 Data assumptions

- In-situ VDF in distribution-function form.
- Linear-Vlasov solver with arbitrary-VDF input.

### 2.4 Failure modes (skill memory)

- **Fit choice** for bi-Maxwellian baseline matters.
- **Noise floor in VDF** smears non-Maxwellian features.

### 2.5 Figure / numerical targets

- γ_max ratio reproduced on labeled events (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-LIN-VLASOV-FREEFORM-VDF**.
- **C-VDF-LOAD**.

### 3.2 Procedure

1. C-VDF-LOAD.
2. C-LIN-VLASOV-FREEFORM-VDF: solve dispersion.
3. Compare to bi-Maxwellian fit.

### 3.3 Minimum reproduction artifacts

- γ_max ratio table per event.

---

## 4. Adapter / runtime notes (optional examples)

- ALPS supports free-form VDF — example Layer-3 binding.

---

## 5. Research-generation affordance

- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**: provides non-Maxwellian-VDF closure for AIC-wave occurrence prediction.
- **Open hypothesis**: How often does bi-Maxwellian closure miscall AIC stability?

---

## Links

- arXiv: https://arxiv.org/abs/2308.14944
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2308.14944`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[klein-2018-multispecies-stability-anisotropy]]

