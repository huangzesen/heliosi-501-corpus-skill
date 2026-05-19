---
name: bowen-2024-cyclotron-heating-rates-ion-scale-waves
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# bowen-2024-cyclotron-heating-rates-ion-scale-waves

A paper-skill compiled from T. A. Bowen, et al., 2024 (full author list pending verification) (TODO_verify_journal; arXiv:2407.02708).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Estimate proton heating rates from cyclotron damping using PSP-observed ion-scale wave amplitudes.
- Decide whether cyclotron-resonant damping is sufficient to close the perpendicular heating budget.

### When NOT to use it

- Stochastic-heating channel — see [[chandran-2010-stochastic-heating-perp-alfven]].
- Landau-resonance parallel heating — see [[bowen-2023-landau-damping-proton-electron-heating]].

### Claim boundary

Per-interval estimate of cyclotron-damping heating rate from PSP wave-power spectra and linear-damping rates. Closure claim limited to intervals analysed.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Cyclotron-damping heating rates from observed PSP ion-scale waves cover a major fraction of the perpendicular heating budget in chosen encounters.

### 2.2 Equations / method

- Q_⊥ = ∫ γ_cyc(k) E_wave(k) dk.
- γ_cyc from linear-Vlasov on local VDF.

### 2.3 Data assumptions

- PSP MAG ion-scale spectrum + SWEAP VDF.
- Linear-Vlasov solver for γ_cyc.

### 2.4 Failure modes (skill memory)

- **Spectrum normalization** at sub-cyclotron k_∥ uncertain.
- **VDF moments** ignore non-Maxwellian tails that affect γ_cyc.
- **k_∥ vs k_⊥ partition** dominates Q_⊥ estimate.

### 2.5 Figure / numerical targets

- Q_⊥ within stated fraction of independent heating estimates (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP-WAVE-SPECTRUM**.
- **C-LIN-VLASOV-CYCLOTRON**: γ_cyc(k).
- **C-Q-PERP-INTEGRATOR**.

### 3.2 Procedure

1. C-FETCH-PSP-WAVE-SPECTRUM.
2. C-LIN-VLASOV-CYCLOTRON.
3. C-Q-PERP-INTEGRATOR.

### 3.3 Minimum reproduction artifacts

- Q_⊥(r) curve per encounter.
- γ_cyc(k) per interval.

---

## 4. Adapter / runtime notes (optional examples)

- PLUME γ_cyc and PSP MAG-spectrum pipelines are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[bowen-2024-extended-cyclotron-resonant-heating]] (existing)**: extend the resonance band beyond the cyclotron line.
- **Composability with [[kontar-2025-ion-scale-turbulence-cascade-rate-corona]]**: cross-validate Q_⊥ vs cascade rate ε.
- **Open hypothesis**: Are non-closure intervals (Q_⊥ < observed heating) intervals where stochastic heating dominates?

---

## Links

- arXiv: https://arxiv.org/abs/2407.02708
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2407.02708`

## Skill graph

- [[bowen-2024-extended-cyclotron-resonant-heating]]
- [[kontar-2025-ion-scale-turbulence-cascade-rate-corona]]
- [[chandran-2010-stochastic-heating-perp-alfven]]

