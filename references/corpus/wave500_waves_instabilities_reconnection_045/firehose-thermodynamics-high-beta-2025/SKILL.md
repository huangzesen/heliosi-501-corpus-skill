---
name: firehose-thermodynamics-high-beta-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# firehose-thermodynamics-high-beta-2025

A paper-skill compiled from the primary source (author list pending verification), 2025 (TODO_verify_journal; arXiv:2501.13663).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the marginal-stability state of high-β plasmas with respect to firehose instability.
- Diagnose whether observed (β_∥, T_⊥/T_∥) distributions sit on the firehose boundary.

### When NOT to use it

- Mirror instability — see anisotropy-instabilities skills.
- Cyclotron resonance — see [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]].

### Claim boundary

Kinetic theory / hybrid simulation of firehose-susceptible high-β plasmas with explicit treatment of effective collisionality. The mapping between thermodynamic forcing and marginal-stability stationarity is the main result.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Firehose-susceptible regions of (β_∥, T_⊥/T_∥) space exhibit anomalous effective collisionality that pins the plasma to the marginal-stability curve under continuous thermodynamic forcing.

### 2.2 Equations / method

- Firehose threshold T_⊥/T_∥ < 1 − 2/β_∥.
- Effective collision rate ν_eff inferred from pitch-angle scattering.
- Quasi-stationary marginal-stability ansatz.

### 2.3 Data assumptions

- Hybrid simulation or analytic kinetic closure.
- Continuous driving of (β_∥, ξ) toward firehose region.
- VDF diagnostics to extract anisotropy and ν_eff.

### 2.4 Failure modes (skill memory)

- **Driving rate** competes with ν_eff; choice matters.
- **Initial VDF shape** biases firehose-fluctuation amplitudes.
- **Reduced dimensionality** misses oblique firehose branches.

### 2.5 Figure / numerical targets

- ν_eff scaling with distance from threshold (TODO verify).
- Marginal-stability locus reproduced.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HYBRID-SIM**: hybrid kinetic plasma simulation with prescribed driving.
- **C-FIREHOSE-LIN**: linear firehose dispersion solver.
- **C-NU-EFF**: effective-collision-rate extractor from VDF.

### 3.2 Procedure

1. Initialize near firehose threshold.
2. Apply chosen anisotropy driving.
3. Run to quasi-steady state.
4. C-NU-EFF: extract ν_eff vs distance from threshold.
5. Compare against C-FIREHOSE-LIN prediction.

### 3.3 Minimum reproduction artifacts

- ν_eff vs distance-from-threshold curve.
- Marginal-stability locus plot.

---

## 4. Adapter / runtime notes (optional examples)

- Any hybrid PIC code satisfies the contracts.

---

## 5. Research-generation affordance

- **Composability with [[ion-driven-instabilities-classification-2023]]**: feed observed (β_∥, ξ) into the classifier to flag firehose-susceptible intervals.
- **Composability with PSP solar-wind data**: encounter-scan whether (β_∥, ξ) clusters near the firehose threshold predicted here.
- **Open hypothesis**: Is the observed solar-wind avoidance of T_⊥/T_∥ < 1 − 2/β_∥ a kinetic-feedback (ν_eff) phenomenon or a thermodynamic one?

---

## Links

- arXiv: https://arxiv.org/abs/2501.13663
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2501.13663`

## Skill graph

- [[ion-driven-instabilities-classification-2023]]
- [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]

