---
name: suprathermal-anisotropy-instabilities-stimulated-2024
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# suprathermal-anisotropy-instabilities-stimulated-2024

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2024 (TODO_verify_journal; arXiv:2409.09180).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict how a suprathermal proton population modifies temperature-anisotropy instability thresholds.
- Decide whether observed PSP suprathermal-tail intervals shift the firehose/mirror/cyclotron boundaries.

### When NOT to use it

- Pure bi-Maxwellian instability thresholds — see [[ion-driven-instabilities-classification-2023]].

### Claim boundary

Hybrid simulations with explicit suprathermal proton component. Threshold shifts measured against bi-Maxwellian baseline.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Suprathermal proton populations stimulate anisotropy instabilities at lower core anisotropy than a bi-Maxwellian closure predicts; magnitude of the shift quantified.

### 2.2 Equations / method

- κ-distribution suprathermal proton population.
- Modified instability dispersion with two-population VDF.

### 2.3 Data assumptions

- Hybrid simulation with two-population proton VDF.
- κ-index for suprathermal tail specified.

### 2.4 Failure modes (skill memory)

- **κ choice** dominates magnitude of shift.
- **Density ratio** of suprathermal to core matters.

### 2.5 Figure / numerical targets

- Threshold shift vs (κ, n_sup/n_core) (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HYBRID-TWO-POP**: hybrid simulation with two-population proton VDF.
- **C-INSTAB-THRESH-TWO-POP**.

### 3.2 Procedure

1. Initialize two-population VDF.
2. Run hybrid simulation.
3. Extract threshold shift.

### 3.3 Minimum reproduction artifacts

- Threshold-shift table vs (κ, n_sup/n_core).

---

## 4. Adapter / runtime notes (optional examples)

- Any hybrid code with κ-distribution support satisfies the contracts.

---

## 5. Research-generation affordance

- **Composability with [[paper-cuesta-2024-kappa-distributions-energetic-protons]] (existing)**: link suprathermal-tail observations to threshold shifts predicted here.
- **Composability with [[ion-driven-instabilities-classification-2023]]**: classifier should incorporate the κ-modified thresholds.
- **Open hypothesis**: Are PSP intervals labeled bi-Maxwellian-stable but observed unstable instances of suprathermal stimulation?

---

## Links

- arXiv: https://arxiv.org/abs/2409.09180
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2409.09180`

## Skill graph

- [[paper-cuesta-2024-kappa-distributions-energetic-protons]]
- [[ion-driven-instabilities-classification-2023]]

