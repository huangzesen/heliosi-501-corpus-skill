---
name: alfven-surface-wind-braking-torque-psp-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# alfven-surface-wind-braking-torque-psp-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2509.07088).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Reconstruct the global Alfvén surface from PSP sub-Alfvénic crossings.
- Estimate the wind angular-momentum braking torque from PSP-derived surface and stress-tensor balance.

### When NOT to use it

- Local sub-Alfvénic interval identification — see [[kasper-2021-psp-enters-magnetically-dominated-corona]].
- Coronal-base AW-injection budget — see [[mcmurdo-2025-uniturbulence-kink-wave-heating-amrvac]].

### Claim boundary

Uses PSP-recorded crossings of the M_A=1 surface across multiple encounters, plus a global PFSS or analogous coronal model. Torque estimate is bounded by the model and the encounter coverage.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Multiple PSP sub-Alfvénic intervals constrain the Alfvén-surface heliographic shape; the inferred wind braking torque is consistent with the long-term solar spin-down rate within stated bars.

### 2.2 Equations / method

- Sub-Alfvénic condition M_A = V/V_A < 1.
- Angular-momentum stress tensor: ρ V_r (V_φ r − B_r B_φ r / (4π ρ V_r)).
- Surface fitting from M_A=1 boundary points.

### 2.3 Data assumptions

- PSP MAG + plasma data with reliable density estimate (QTN preferred).
- Multi-encounter coverage of sub-Alfvénic crossings.
- Coronal magnetic model (PFSS / WSA) for global surface extrapolation.

### 2.4 Failure modes (skill memory)

- **Density proxy** (QTN vs SPC vs SPAN-i) shifts V_A.
- **Encounter sampling** biases the inferred surface shape.
- **Coronal-model choice** affects extrapolation — sweep.
- **φ V_φ uncertainty** dominates torque error bars.

### 2.5 Figure / numerical targets

- Surface heliocentric distance distribution consistent with PSP encounter-by-encounter (TODO verify).
- Braking torque within order-of-magnitude of long-term spin-down (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP-MAG-PLASMA-QTN**: in-situ inputs.
- **C-MA-MASK**: M_A<1 interval mask with density-proxy choice recorded.
- **C-CORONAL-MODEL**: PFSS / WSA global field.
- **C-SURFACE-FIT**: fit Alfvén surface to mask + model.
- **C-TORQUE**: integrate stress tensor over the surface.

### 3.2 Procedure

1. C-FETCH-PSP-MAG-PLASMA-QTN over relevant encounters.
2. C-MA-MASK: identify sub-Alfvénic intervals.
3. C-CORONAL-MODEL: pull PFSS field.
4. C-SURFACE-FIT: extrapolate surface globally.
5. C-TORQUE: integrate stress tensor.

### 3.3 Minimum reproduction artifacts

- Alfvén-surface mesh.
- Torque-budget JSON with sensitivity sweep.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with PSP CDF I/O + PFSS solver suffices.
- pfsspy / sunkit-magex are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[kasper-2021-psp-enters-magnetically-dominated-corona]]**: anchor at the original sub-Alfvénic interval and extend to the multi-encounter ensemble.
- **Tension with [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]**: solar-max sub-Alfvénic statistics may shift surface shape vs solar-min — joint solar-cycle dependence.
- **Open hypothesis**: Does the inferred braking torque match independent Sun-as-a-star spin-down estimates within factor 2?

---

## Links

- arXiv: https://arxiv.org/abs/2509.07088
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2509.07088`

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]
- [[wu-2026-nonspherical-coronal-magnetic-field-open-flux]]

