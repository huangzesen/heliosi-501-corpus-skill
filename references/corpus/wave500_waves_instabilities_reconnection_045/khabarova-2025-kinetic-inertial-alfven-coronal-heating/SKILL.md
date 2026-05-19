# khabarova-2025-kinetic-inertial-alfven-coronal-heating

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2505.03267).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict how kinetic vs inertial Alfvén waves (KAW vs IAW) partition energy between heating and particle acceleration in coronal conditions.
- Decide whether observed nonthermal tails at small scales require IAW-driven energization.

### When NOT to use it

- MHD-range dynamics — separate skill.
- In-situ kinetic spectrum at 1 AU — see [[zhao-2022-3d-anisotropy-kinetic-scales-psp]].

### Claim boundary

Theoretical review with quantitative model expressions for KAW/IAW absorption rates and acceleration efficiencies under specified coronal plasma parameters.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Both KAW (high β regions) and IAW (low β regions) contribute to coronal heating, with paper-specified rates; IAW dominate parallel particle acceleration in low-β coronal-hole roots.

### 2.2 Equations / method

- KAW absorption rate in high-β.
- IAW absorption rate in low-β.
- Parallel-acceleration efficiency expressions.

### 2.3 Data assumptions

- Coronal density, temperature, B profiles.
- Specified turbulence amplitude at ion scales.

### 2.4 Failure modes (skill memory)

- **β regime selection** drives whether KAW or IAW dominates.
- **Turbulence-amplitude assumption** is the dominant input uncertainty.

### 2.5 Figure / numerical targets

- Absorption-rate magnitudes vs β (TODO verify exact).
- Acceleration-efficiency expressions reproduced.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-KAW-IAW-DISP**: dispersion + damping for KAW and IAW.
- **C-CORONAL-PROFILE**: coronal background loader.
- **C-PARTICLE-ACCEL-EFF**: parallel-acceleration efficiency estimator.

### 3.2 Procedure

1. Load coronal profile and turbulence amplitude.
2. C-KAW-IAW-DISP: compute damping rates for both modes.
3. C-PARTICLE-ACCEL-EFF: estimate parallel acceleration.
4. Compute heating vs particle-acceleration partition.

### 3.3 Minimum reproduction artifacts

- Heating/acceleration partition table.
- Damping-rate curves for KAW/IAW.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness providing dispersion+damping rate solvers satisfies the contracts.

---

## 5. Research-generation affordance

- **Composability with [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]**: cross-validate cyclotron-resonant heating against KAW/IAW damping.
- **Composability with [[kontar-2025-ion-scale-turbulence-cascade-rate-corona]]**: feed ε(r) into KAW/IAW absorption-rate budget.
- **Open hypothesis**: Are IAW signatures (parallel acceleration in low-β coronal-hole roots) responsible for observed nonthermal tails in PSP encounter-1 data?

---

## Links

- arXiv: https://arxiv.org/abs/2505.03267
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2505.03267`

## Skill graph

- [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]
- [[kontar-2025-ion-scale-turbulence-cascade-rate-corona]]

