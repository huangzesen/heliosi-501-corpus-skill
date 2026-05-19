---
name: peng-2025-chaotic-ion-motion-finite-amplitude-alfven
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# peng-2025-chaotic-ion-motion-finite-amplitude-alfven

A paper-skill compiled from J. Peng, J. He, R. Lin et al. 2025 (TODO_verify_journal; arXiv:2510.07144).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Decide whether ion motion in a prescribed finite-amplitude oblique Alfvén-wave field is chaotic.
- Predict the Chaos Ratio CR over (k_x, k_z, B_w) and identify the global chaos threshold.

### When NOT to use it

- Wave excitation mechanism — this skill treats the wave as a *given* finite-amplitude field.
- Macroscopic heating-rate closure — see [[bowen-2023-landau-damping-proton-electron-heating]].

### Claim boundary

Test-particle integration in a prescribed oblique low-frequency AW. Chaos is diagnosed via maximum Lyapunov exponent λ_m and the chaos ratio CR over an initial-condition ensemble. Threshold CR = 0.01 defines the chaotic region in parameter space.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Wave-driven field-line curvature (WFLC) causes pitch-angle scattering that disrupts adiabatic invariance and produces stochastic ion energization. The chaos boundary is well-approximated by the effective curvature radius criterion P_eff < 25.

### 2.2 Equations / method

- Test-particle Newton–Lorentz equations in prescribed AW field.
- Maximum Lyapunov exponent λ_m from tangent-vector growth.
- Effective relative curvature radius P_eff (paper-defined).
- Magnetic-moment μ time evolution as adiabatic-invariance proxy.

### 2.3 Data assumptions

- Prescribed oblique low-frequency AW with amplitude B_w and wavenumbers (k_x, k_z).
- Test-particle ion ensemble with chosen initial pitch-angle distribution.
- Sufficient integration time for λ_m convergence.

### 2.4 Failure modes (skill memory)

- **Λ_m convergence** requires long integration; report convergence test.
- **Initial-condition coverage** biases CR estimate; quote ensemble size.
- **B_w too large** breaks the prescribed-wave assumption (back-reaction matters).
- **Single-wave assumption** misses spectrum effects.

### 2.5 Figure / numerical targets

- Global chaos threshold CR = 0.01 contour matches P_eff < 25 prediction (TODO verify).
- λ_m positive in the chaotic region; small near the boundary.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-WAVE-FIELD**: analytic finite-amplitude AW field generator.
- **C-TEST-PARTICLE**: ion ensemble integrator with tangent dynamics.
- **C-LYAPUNOV**: λ_m and CR estimator.

### 3.2 Procedure

1. Choose (k_x, k_z, B_w).
2. C-WAVE-FIELD: build AW field.
3. C-TEST-PARTICLE: integrate ensemble.
4. C-LYAPUNOV: estimate λ_m, CR.
5. Scan parameter space and fit chaos boundary.

### 3.3 Minimum reproduction artifacts

- Per-(k_x,k_z,B_w) CR table.
- λ_m maps in parameter space.
- Magnetic-moment μ(t) histograms.

---

## 4. Adapter / runtime notes (optional examples)

- Any test-particle code with tangent-vector capability satisfies the contracts.
- Numba/JAX particle integrators are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[bowen-2023-landau-damping-proton-electron-heating]]**: compare WFLC heating channel with Landau-resonance heating in matched β regimes.
- **Composability with [[chandran-2010-stochastic-heating-perp-alfven]] (stub-link)**: contrast Chen-2010 stochastic-heating criterion (ε ≡ δv_⊥/v_⊥ > 0.1) with the P_eff < 25 criterion.
- **Open hypothesis**: Do PSP intervals with locally chaotic ion VDFs (non-Gaussian pitch-angle distributions) cluster in the WFLC-favourable region of (k_x, k_z, B_w)?
- **Methodological experiment**: superpose a turbulent AW spectrum on the single-wave prescription and quantify CR shift.

---

## Links

- arXiv: https://arxiv.org/abs/2510.07144
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2510.07144`

## Skill graph

- [[bowen-2023-landau-damping-proton-electron-heating]]
- [[chandran-2010-stochastic-heating-perp-alfven]]

