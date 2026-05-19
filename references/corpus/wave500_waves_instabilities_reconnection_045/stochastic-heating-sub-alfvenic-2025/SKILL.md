---
name: stochastic-heating-sub-alfvenic-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# stochastic-heating-sub-alfvenic-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from the primary source (author list pending verification), 2025 (TODO_verify_journal; arXiv:2509.20654).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Quantify stochastic-heating rates in PSP sub-Alfvénic intervals.
- Decide whether stochastic-heating closes the perpendicular heating budget below the Alfvén surface.

### When NOT to use it

- Above-Alfvén-surface intervals — separate.
- Cyclotron-resonant channel — see [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]].

### Claim boundary

Per-interval Q_⊥ estimate from observed δv_⊥ in sub-Alfvénic PSP intervals using Chandran et al. (2010) stochastic-heating prescription or analogue.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Stochastic-heating estimates in PSP sub-Alfvénic intervals account for the majority of inferred perpendicular heating within stated bars.

### 2.2 Equations / method

- Stochastic-heating rate Q_⊥ ~ c_1 (δv_⊥)^3 / ρ_i exp(−c_2/ε).
- ε ≡ δv_⊥/v_⊥.

### 2.3 Data assumptions

- PSP MAG + plasma in sub-Alfvénic intervals.
- Density estimate for ρ_i.

### 2.4 Failure modes (skill memory)

- **c_1, c_2 calibration** is theoretical — paper choice critical.
- **v_⊥ baseline** definition matters.

### 2.5 Figure / numerical targets

- Q_⊥ closure within stated fraction (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP-SUB-ALFVENIC**.
- **C-CHANDRAN-Q-PERP**.

### 3.2 Procedure

1. C-FETCH-PSP-SUB-ALFVENIC.
2. C-CHANDRAN-Q-PERP per interval.

### 3.3 Minimum reproduction artifacts

- Q_⊥(r) curve in sub-Alfvénic regime.

---

## 4. Adapter / runtime notes (optional examples)

- PSP MAG+plasma pipelines.

---

## 5. Research-generation affordance

- **Composability with [[kasper-2021-psp-enters-magnetically-dominated-corona]]**: ties stochastic-heating to the first M_A<1 interval.
- **Tension with [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]**: which channel dominates in sub-Alfvénic regime?
- **Open hypothesis**: Does stochastic heating account for the observed near-Sun T_⊥ enhancement?
- **Composability with [[chandran-2010-stochastic-heating-perp-alfven]]**: provides the analytic foundation.

---

## Links

- arXiv: https://arxiv.org/abs/2509.20654
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2509.20654`

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]
- [[chandran-2010-stochastic-heating-perp-alfven]]

