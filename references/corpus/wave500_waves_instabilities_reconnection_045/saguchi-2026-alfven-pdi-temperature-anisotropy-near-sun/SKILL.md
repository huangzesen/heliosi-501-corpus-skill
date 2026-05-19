---
name: saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun

A paper-skill compiled from H. Saguchi, Y. Kawazura, M. Shoda et al. 2026 (ApJ (TODO verify venue); arXiv:2604.22489).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict where Alfvén-wave parametric decay instability (PDI) is expected to grow in the near-Sun solar wind.
- Decide whether observed temperature anisotropy increases or suppresses local PDI growth rate.

### When NOT to use it

- Direct in-situ event identification of decay products — see ion-scale-wave detection skills.
- Full nonlinear saturation of PDI; this skill is a *linear growth-rate* contract.

### Claim boundary

Linear maximum growth rates γ_max/ω_0 of Alfvén-wave PDI under CGL closure for three expanding background profiles between R_0 ≈ 1.02 R_⊙ and 30 R_0. Claim is bounded to the linear regime and to the three profiles considered.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

For β_∥ ≲ 0.1, T_⊥0/T_∥0 > 1 increases γ_max/ω_0 by factors ~1.5 over R≈1–10 R_0 relative to MHD; T_∥0 > T_⊥0 decreases γ_max/ω_0 at larger R.

### 2.2 Equations / method

- CGL linear dispersion relation for parent Alfvén wave + sideband decay products.
- β_∥ = 8π p_∥0 / B_0^2; ξ = T_⊥0/T_∥0.
- Compare against isotropic MHD growth rate at matched (β, k‖ a_0).

### 2.3 Data assumptions

- Background expansion profile (B_0(R), n_0(R), T_∥0(R), T_⊥0(R)) over 1.02–30 R_⊙.
- Parent-wave amplitude a_0 = δB_⊥/B_0 specified.
- PSP-constrained (β_∥, ξ) profile or analogue available.

### 2.4 Failure modes (skill memory)

- **CGL closure breakdown** when ion FLR effects become important — narrows validity window.
- **Parent-wave amplitude** chosen too large; weak-amplitude expansion of dispersion no longer holds.
- **Profile choice** (adiabatic vs PSP-constrained) drives factor-of-few changes in γ_max — always sweep.
- **Heliospheric-distance interpretation** depends on chosen expansion model; report which.

### 2.5 Figure / numerical targets

- γ_max/ω_0 enhancement ≈ 1.5 for T_⊥0 > T_∥0 at β ≲ 0.1 over R≈1–10 R_0 (TODO verify exact).
- Sign reversal of anisotropy effect at high β.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-PROFILE-EXPANSION**: provide R-dependent (B_0,n_0,T_∥,T_⊥).
- **C-DISPERSION-CGL**: solve linear CGL dispersion for parent + sideband.
- **C-DISPERSION-MHD**: solve isotropic MHD reference dispersion.
- **C-GROWTH-SCAN**: scan k‖ a_0 and report γ_max/ω_0 vs R.

### 3.2 Procedure

1. C-PROFILE-EXPANSION: load one of the three expansion cases.
2. C-DISPERSION-CGL at each R: find γ_max over k‖ a_0 grid.
3. C-DISPERSION-MHD at matched β: record reference γ_max.
4. Compute enhancement ratio γ_CGL/γ_MHD vs R.
5. Repeat for ξ > 1 and ξ < 1 to recover sign of anisotropy effect.

### 3.3 Minimum reproduction artifacts

- γ_max(R) curves per profile and per ξ regime.
- Enhancement-ratio JSON keyed by (β_∥, ξ, R).
- Sensitivity sweep over parent-wave amplitude a_0.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness providing a CGL linear-dispersion solver and an expansion-profile loader can satisfy the contracts.
- PlasmaPy / Vlasiator dispersion modules are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**: condition observed ion-scale-wave occurrence on locally inferred (β_∥, ξ); test whether PDI-favourable conditions correlate with detected wave intervals.
- **Open hypothesis**: PSP encounter-scan whether observed PDI signatures (compressible sidebands, density-Δv anticorrelation) cluster in low-β, T_⊥>T_∥ intervals.
- **Tension with [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]**: cyclotron-resonant dissipation and PDI compete for parent-wave energy — partition between channels is unconstrained jointly.
- **Composability with [[shoda-2021-turbulence-switchback-generation-alfvenic]]**: PDI may seed compressible fluctuations that mediate switchback generation; joint runs not done.

---

## Links

- arXiv: https://arxiv.org/abs/2604.22489
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2604.22489`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]
- [[shoda-2021-turbulence-switchback-generation-alfvenic]]

