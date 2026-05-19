---
name: proton-alpha-aic-driven-instabilities-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# proton-alpha-aic-driven-instabilities-2023

A paper-skill compiled from the primary source (author list pending verification), 2023 (TODO_verify_journal; arXiv:2310.14136).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Diagnose whether a specific ion-cyclotron-wave event is driven by proton-only, alpha-only, or joint instability.
- Validate the multi-species instability driver against observed wave polarization.

### When NOT to use it

- Statistical AIC occurrence — separate skill.

### Claim boundary

Event-level linear-Vlasov dispersion analysis on a specific PSP ion-cyclotron-wave interval.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

The cited AIC event is driven by joint proton + α free energy; neither species alone reproduces the observed γ_max and polarization.

### 2.2 Equations / method

- Multi-species linear-Vlasov dispersion.
- Polarization comparison to observed wave packet.

### 2.3 Data assumptions

- Event-level high-cadence VDF for p and α.
- Wave-spectrum and polarization measurement.

### 2.4 Failure modes (skill memory)

- **Cadence limits** may smear VDF at relevant scale.
- **Single event** doesn't generalize.

### 2.5 Figure / numerical targets

- γ_max from p+α dispersion matches observed wave growth (TODO verify).
- Polarization reproduces left-handed AIC signature.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-VDF-EVENT-LOAD**.
- **C-LIN-VLASOV-PA**.
- **C-POL-COMPARE**.

### 3.2 Procedure

1. C-VDF-EVENT-LOAD for chosen event.
2. C-LIN-VLASOV-PA: solve dispersion.
3. C-POL-COMPARE against wave-packet observation.

### 3.3 Minimum reproduction artifacts

- Event report JSON.
- Polarization-comparison PNG.

---

## 4. Adapter / runtime notes (optional examples)

- PLUME/NHDS support multi-species; example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[anti-equilibrium-alfven-ion-cyclotron-effects-2023]]**: combine multi-species and non-Maxwellian effects in one closure.
- **Open hypothesis**: What fraction of AIC events in PSP catalog are joint-driven rather than single-species?

---

## Links

- arXiv: https://arxiv.org/abs/2310.14136
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2310.14136`

## Skill graph

- [[anti-equilibrium-alfven-ion-cyclotron-effects-2023]]
- [[verniero-2020-proton-beams-ion-scale-waves]]

