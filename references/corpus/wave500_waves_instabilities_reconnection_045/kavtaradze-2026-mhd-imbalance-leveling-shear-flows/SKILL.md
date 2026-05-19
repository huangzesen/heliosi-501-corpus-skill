---
name: kavtaradze-2026-mhd-imbalance-leveling-shear-flows
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# kavtaradze-2026-mhd-imbalance-leveling-shear-flows

A paper-skill compiled from M. Kavtaradze, G. Mamatsashvili, G. Chagelishvili et al. 2026 (TODO_verify_journal; arXiv:2602.13528).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Assess whether a sheared background flow drives imbalanced Alfvénic turbulence toward σ_c → 0.
- Diagnose linear non-modal (transient growth + over-reflection) contributions to MHD energy partition.

### When NOT to use it

- Reflection-driven balancing in radial expansion — see [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]].
- Strictly nonlinear cascade phenomenology in the absence of mean shear.

### Claim boundary

Super-Alfvénic plane shear flows with streamwise mean field. The leveling mechanism is *linear* (non-modal): transient growth and over-reflection of counter-propagating Alfvén waves equalize their energies.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Initially perfectly imbalanced Alfvénic turbulence in a streamwise-field plane shear flow relaxes toward σ_c ≈ 0 via shear-induced linear non-modal dynamics, independent of the nonlinear cascade.

### 2.2 Equations / method

- Linearized incompressible MHD with mean shear U_x = S y; streamwise B_0.
- Shearing-wave Fourier substitution k_y(t) = k_y(0) − S k_x t.
- Energy budgets E^± of co/counter-propagating Alfvén waves as functions of k(t).

### 2.3 Data assumptions

- Super-Alfvénic mean shear: |S| L > V_A (in non-dim units).
- Streamwise mean field; uniform density.
- Initial spectral support away from k_y(t)=0 caustic.

### 2.4 Failure modes (skill memory)

- **Sub-Alfvénic regime** — leveling weakens; mechanism not guaranteed.
- **Cross-field component of B_0** — breaks the streamwise-field assumption and removes pure shearing-wave reduction.
- **Initial spectrum** concentrated near k_x=0 (Alfvénic null) yields atypical evolution.
- **Compressibility / density gradients** modify over-reflection coefficients.

### 2.5 Figure / numerical targets

- σ_c → 0 in shearing-wave ensemble averages for super-Alfvénic shear (TODO verify exact decay rate).
- Over-reflection coefficient agrees with analytic linear theory at chosen (k_x, k_z, S/V_A).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-SHEAR-LINMHD**: linearized incompressible MHD in shearing-wave coordinates.
- **C-ENERGY-PARTITION**: compute σ_c(t) for E^± Elsässer modes.
- **C-NON-MODAL**: extract transient-growth + over-reflection amplitudes per (k_x,k_z).

### 3.2 Procedure

1. Initialize purely outward Elsässer ensemble at t=0.
2. C-SHEAR-LINMHD: integrate each shearing wave across the caustic.
3. C-ENERGY-PARTITION: bin σ_c(t) over the ensemble.
4. C-NON-MODAL: tabulate over-reflection coefficient vs (k_x/k_z, S/V_A).
5. Repeat with reduced shear and document leveling weakening.

### 3.3 Minimum reproduction artifacts

- σ_c(t) curves for super- and sub-Alfvénic shear.
- Over-reflection coefficient table.
- Shearing-wave amplitude trajectories.

---

## 4. Adapter / runtime notes (optional examples)

- Any spectral linearized-MHD solver with a shearing-box substitution suffices.
- Pencil / Athena++ shear-box are example Layer-3 adapters.

---

## 5. Research-generation affordance

- **Tension with imbalanced-turbulence observations**: most PSP encounters report σ_c ≈ 1; the solar wind is *not* a plane shear, but if Parker-spiral azimuthal shear were locally super-Alfvénic, expect leveling — joint test against [[telloni-2021-psp-solo-radial-alignment-turbulence]] absent.
- **Composability with [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]**: separate linear-shear leveling from reflection-driven balancing in expanding-box runs.
- **Open hypothesis**: Are intervals where shear is super-Alfvénic (e.g., across CIRs) the ones where σ_c falls in PSP data?

---

## Links

- arXiv: https://arxiv.org/abs/2602.13528
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2602.13528`

## Skill graph

- [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]
- [[telloni-2021-psp-solo-radial-alignment-turbulence]]

