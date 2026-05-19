# helicity-barrier-evidence-transition-range-2024

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2024 (TODO_verify_journal; arXiv:2407.10815).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Test the helicity-barrier prediction (energy pile-up at ion scales for σ_c ≈ ±1) against in-situ ion-scale spectra.
- Decide whether observed transition-range spectral steepening is a helicity-barrier signature.

### When NOT to use it

- Sub-ion KAW cascade exponents — see [[stationary-power-law-kinetic-alfven-turbulence-2025]].
- MHD-range Iroshnikov–Kraichnan vs Goldreich–Sridhar phenomenology — separate skill.

### Claim boundary

In-situ ion-scale spectra binned by local σ_c; barrier signature defined as energy pile-up at the ion gyroscale for high-σ_c bins. Claim is statistical over the analyzed mission segments.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Solar-wind intervals with |σ_c| → 1 show a transition-range steepening / pile-up consistent with the helicity-barrier prediction; balanced (σ_c ≈ 0) intervals do not.

### 2.2 Equations / method

- σ_c = (|z^+|² − |z^-|²)/(|z^+|² + |z^-|²).
- Magnetic spectrum slope α_B(σ_c) in transition range.
- Pile-up amplitude vs σ_c.

### 2.3 Data assumptions

- High-cadence in-situ magnetic spectra.
- Plasma data for V_A and ρ.
- σ_c binning resolution.

### 2.4 Failure modes (skill memory)

- **σ_c estimator** depends on Elsässer-window choice.
- **Taylor hypothesis** breaks near transition range for slow-stream intervals.
- **Density estimate** for V_A affects z^± normalization.

### 2.5 Figure / numerical targets

- Pile-up amplitude scales monotonically with |σ_c| (TODO verify).
- α_B steepening matches paper-reported values.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG-PLASMA**: in-situ B, V, n.
- **C-SIGMA-C**: σ_c estimator with window choice recorded.
- **C-TRANSITION-FIT**: transition-range spectral analyzer.

### 3.2 Procedure

1. C-FETCH-MAG-PLASMA.
2. C-SIGMA-C binning.
3. C-TRANSITION-FIT per σ_c bin.
4. Aggregate pile-up vs σ_c.

### 3.3 Minimum reproduction artifacts

- Transition-range spectrum per σ_c bin.
- Pile-up amplitude table.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with CDF I/O and spectral-fitter satisfies the contracts.

---

## 5. Research-generation affordance

- **Composability with [[bowen-2024-extended-cyclotron-resonant-heating]]**: helicity barrier may channel energy into cyclotron resonance — joint test.
- **Composability with [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]**: PS-RDT predicts high σ_c at large r — the helicity barrier should be most evident there.
- **Open hypothesis**: Does the helicity barrier weaken inside switchbacks where σ_c locally inverts?

---

## Links

- arXiv: https://arxiv.org/abs/2407.10815
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2407.10815`

## Skill graph

- [[bowen-2024-extended-cyclotron-resonant-heating]]
- [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]

