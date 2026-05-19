# abbas-squire-2026-parker-spiral-reflection-driven-turbulence

A paper-skill compiled from K. Abbas, J. Squire et al. 2026 (TODO_verify_journal; arXiv:2512.07446).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict how the Parker-spiral geometry modifies the outer-scale eddy structure and heating efficiency of reflection-driven turbulence.
- Decide whether observed perpendicular outer-scale and cross-helicity radial profile are consistent with PS RDT vs radial-field RDT.

### When NOT to use it

- Sub-ion kinetic dissipation — see [[bowen-2023-landau-damping-proton-electron-heating]].
- Near-Sun streamer-belt turbulence at small R — see [[chen-2021-near-sun-streamer-belt-turbulence]].

### Claim boundary

3D expanding-box MHD simulations with Parker-spiral background mean field. Comparison made against radial-field baseline. Heating is inferred from cascade-flux closure rather than direct kinetic dissipation.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

With a Parker spiral, the growing azimuthal field cuts across pancake-like eddies, reducing the perpendicular outer scale, lengthening eddy turnover only weakly with r, dissipating a larger fraction of fluctuation energy as heat, and keeping σ_c high to larger r.

### 2.2 Equations / method

- Expanding-box MHD with mean B_0(r) = B_r(r) e_r + B_φ(r) e_φ.
- Reflection coefficient set by ∂_r V_A.
- Outer-scale L_⊥(r) measured perpendicular to local B.
- Cascade-flux heating rate ε(r).

### 2.3 Data assumptions

- Expanding-box MHD solver with arbitrary background mean field.
- Specified Alfvén-speed profile V_A(r).
- Long enough integration to reach quasi-steady cascade.

### 2.4 Failure modes (skill memory)

- **Box-size truncation** of L_⊥ at large r.
- **Mean-field rotation rate** prescription influences PS angle as r grows.
- **Numerical dissipation** at sub-grid replaces real kinetic dissipation; ε(r) is a *cascade* rate, not a thermal heating rate.
- **Initial spectrum** controls when the cascade saturates.

### 2.5 Figure / numerical targets

- L_⊥(r) smaller in PS than radial-field baseline (TODO verify magnitude).
- σ_c(r) higher in PS run at large r.
- Heating-fraction increase quantified vs radial-field reference.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-MHD-EXPBOX**: expanding-box MHD with arbitrary mean B_0(r).
- **C-OUTER-SCALE**: estimate L_⊥ perpendicular to local B.
- **C-CASCADE-FLUX**: third-order Politano–Pouquet (or analogue) heating estimate.

### 3.2 Procedure

1. Configure PS mean field with chosen V_A(r).
2. C-MHD-EXPBOX: evolve to quasi-steady cascade.
3. C-OUTER-SCALE: report L_⊥(r) vs radial-field baseline.
4. C-CASCADE-FLUX: estimate ε(r), σ_c(r).
5. Compute fluctuation-energy fraction dissipated.

### 3.3 Minimum reproduction artifacts

- L_⊥(r) curves for PS vs radial cases.
- Heating-fraction table.
- σ_c(r) profile.

---

## 4. Adapter / runtime notes (optional examples)

- Any expanding-box MHD code with PS background satisfies the contracts.
- Snoopy, Pencil-expbox are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Tension with [[telloni-2021-psp-solo-radial-alignment-turbulence]]**: PSP-SolO radial-alignment estimates of σ_c(r) and L_⊥(r) provide a direct test of PS-RDT predictions; joint analysis sparsely published.
- **Composability with [[shoda-2021-turbulence-switchback-generation-alfvenic]]**: PS-RDT predicts switchbacks as part of the spectrum; compare switchback occurrence vs r between models.
- **Open hypothesis**: Does the PS-RDT prediction of high σ_c at large r explain why HCS-distant streams remain Alfvénic at 1 au?
- **Methodological experiment**: vary the PS pitch angle independently of V_A(r) and isolate which controls L_⊥.

---

## Links

- arXiv: https://arxiv.org/abs/2512.07446
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.07446`

## Skill graph

- [[telloni-2021-psp-solo-radial-alignment-turbulence]]
- [[shoda-2021-turbulence-switchback-generation-alfvenic]]
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]

