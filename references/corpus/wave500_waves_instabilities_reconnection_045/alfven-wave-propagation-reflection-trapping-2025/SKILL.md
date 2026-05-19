# alfven-wave-propagation-reflection-trapping-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2507.13809).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify reflection layers and trapping regions for low-frequency Alfvén waves in a prescribed V_A(r) profile.
- Predict the fraction of injected wave energy that escapes vs reflects vs is trapped.

### When NOT to use it

- Sub-ion kinetic dissipation — kinetic skills downstream.
- Reflection-driven turbulence energy partition — see [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]].

### Claim boundary

Wave-equation analysis with prescribed V_A(r); reflection and trapping regions identified analytically and via 1D wave-equation simulation. Claim limited to the AW dispersion relation used.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

AW reflection occurs at gradients in V_A; trapping occurs between adjacent reflection layers; transmitted-energy fraction is a calculable function of V_A profile and wave frequency.

### 2.2 Equations / method

- 1D AW equation in spherically expanding atmosphere.
- WKB reflection coefficient ∝ |∂_r ln V_A|.
- Trapping-layer condition between adjacent reflection nodes.

### 2.3 Data assumptions

- V_A(r) profile prescribed (observational fit or model).
- AW frequency band of interest.

### 2.4 Failure modes (skill memory)

- **WKB breakdown** in steep V_A gradients.
- **Frequency-dependent reflection** must be computed across band.
- **Profile choice** dominates results — sweep.

### 2.5 Figure / numerical targets

- Reflection coefficient curves vs frequency (TODO verify analytic).
- Trapping-region locations vs V_A profile.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-VA-PROFILE**: V_A(r) loader.
- **C-AW-EQ-1D**: 1D AW equation solver.
- **C-REFLECT-TRAP-ANALYZER**: identify reflection/trapping regions.

### 3.2 Procedure

1. C-VA-PROFILE: choose V_A(r).
2. C-AW-EQ-1D: integrate wave equation over band.
3. C-REFLECT-TRAP-ANALYZER: extract reflection + trapping.

### 3.3 Minimum reproduction artifacts

- Reflection-coefficient table.
- Trapping-region map.

---

## 4. Adapter / runtime notes (optional examples)

- Any 1D wave-equation solver suffices.

---

## 5. Research-generation affordance

- **Composability with [[alfven-surface-wind-braking-torque-psp-2025]]**: the Alfvén-surface itself is a reflection layer — quantify trapping near M_A=1.
- **Composability with [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]**: feed the analytic reflection coefficient into the RDT model.
- **Open hypothesis**: Are observed AW spectra near 0.1 AU dominated by reflected/trapped components rather than fresh injection?

---

## Links

- arXiv: https://arxiv.org/abs/2507.13809
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2507.13809`

## Skill graph

- [[alfven-surface-wind-braking-torque-psp-2025]]
- [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]

