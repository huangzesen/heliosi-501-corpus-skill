---
name: stationary-power-law-kinetic-alfven-turbulence-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# stationary-power-law-kinetic-alfven-turbulence-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2508.03478).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict stationary spectral exponents of kinetic-Alfvénic turbulence (KAW) from a closed wave-kinetic equation.
- Diagnose whether observed KAW-range exponents match the analytic stationary solution.

### When NOT to use it

- MHD-range exponents — separate skill.
- Driven nonstationary cascades — this skill is the *stationary* analytic answer.

### Claim boundary

Stationary, locally cascading KAW wave-kinetic equation with specified interaction kernel. Solutions are exact within the closure; finite-flux corrections are not derived in full.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Stationary power-law solutions of the KAW wave-kinetic equation yield specific perpendicular and parallel exponents that match published in-situ KAW-range spectra within stated tolerances.

### 2.2 Equations / method

- Wave-kinetic equation for KAW occupation number n(k).
- Stationary flux solution n(k) ∝ k_⊥^(-α_⊥) k_∥^(-α_∥).
- Cascade-flux closure.

### 2.3 Data assumptions

- Locality of interactions in (k_⊥, k_∥).
- Closure kernel specified.
- Stationarity assumption holds over the inertial-KAW window.

### 2.4 Failure modes (skill memory)

- **Locality breakdown** at small k yields non-power-law solutions.
- **Closure kernel choice** changes exponents.
- **Stationarity assumption** breaks if driving is not balanced.

### 2.5 Figure / numerical targets

- Exact analytic α_⊥, α_∥ values reproduced (TODO verify).
- Match to PSP / SolO KAW exponents within stated tolerance.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-WAVE-KIN-KAW**: numerical wave-kinetic-equation solver.
- **C-ANALYTIC-EXPONENTS**: derive stationary α from closure.
- **C-COMPARE-INSITU**: compare against in-situ spectrum fits.

### 3.2 Procedure

1. Set up wave-kinetic equation with chosen closure.
2. Find stationary solution analytically and numerically.
3. Extract α_⊥, α_∥.
4. Compare against PSP / SolO KAW exponents.

### 3.3 Minimum reproduction artifacts

- Analytic + numerical exponent table.
- Spectrum-overlay PNG vs in-situ.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness providing wave-kinetic-equation tools satisfies the contracts.

---

## 5. Research-generation affordance

- **Composability with [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]**: direct test of α_⊥, α_∥ predictions.
- **Composability with [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]**: validate stationarity assumption by checking spectral-slope radial evolution.
- **Open hypothesis**: Are observed KAW-range slope variations driven by departures from stationarity rather than physics?

---

## Links

- arXiv: https://arxiv.org/abs/2508.03478
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2508.03478`

## Skill graph

- [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]

