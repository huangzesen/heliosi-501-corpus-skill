---
name: free-energy-sources-ion-scale-waves-psp-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# free-energy-sources-ion-scale-waves-psp-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2512.11182).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Attribute observed ion-scale-wave events to specific VDF free-energy sources.
- Decide whether anisotropy, drift, or beam is dominant for each event class.

### When NOT to use it

- Wave generation in simulation — separate skill.

### Claim boundary

Per-event linear-Vlasov attribution on PSP ion-scale-wave catalog.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

PSP ion-scale-wave events partition into anisotropy-driven, drift-driven, and beam-driven subpopulations with paper-quantified fractions.

### 2.2 Equations / method

- Per-event γ_max attributed to (anisotropy, drift, beam) parameter free energy.

### 2.3 Data assumptions

- PSP wave catalog with simultaneous VDFs.
- Multi-species linear-Vlasov solver.

### 2.4 Failure modes (skill memory)

- **Coexisting drivers** — attribution requires decomposition.
- **VDF cadence** limits attribution fidelity.

### 2.5 Figure / numerical targets

- Driver-fraction percentages reproduced (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-WAVE-CATALOG-PSP**.
- **C-DRIVER-DECOMPOSE**: attribute γ_max to (anisotropy, drift, beam).

### 3.2 Procedure

1. C-WAVE-CATALOG-PSP.
2. C-DRIVER-DECOMPOSE per event.
3. Aggregate driver fractions.

### 3.3 Minimum reproduction artifacts

- Attribution table per event.

---

## 4. Adapter / runtime notes (optional examples)

- PLUME parameter-scan example Layer-3.

---

## 5. Research-generation affordance

- **Composability with [[ion-driven-instabilities-classification-2023]]**: closes the loop on classification → attribution.
- **Open hypothesis**: Does driver type correlate with stream class or local σ_c?

---

## Links

- arXiv: https://arxiv.org/abs/2512.11182
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.11182`

## Skill graph

- [[ion-driven-instabilities-classification-2023]]
- [[verniero-2020-proton-beams-ion-scale-waves]]

