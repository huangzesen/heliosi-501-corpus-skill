---
name: skalidis-2025-residual-energy-weakly-compressible-mhd
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# skalidis-2025-residual-energy-weakly-compressible-mhd

A paper-skill compiled from R. Skalidis, A. Tritsis, J. R. Beattie et al. 2025 (TODO_verify_journal; arXiv:2512.11973).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the sign and spectral slope of residual energy E_r = E_kin − E_mag in weakly compressible MHD with a strong guide field.
- Diagnose whether observed E_r-slope vs β trend in the solar wind is consistent with kinetic- vs magnetic-driving phenomenology.

### When NOT to use it

- Highly compressible MHD turbulence (M_s ≳ 1) — see compressible-cascade skills.
- Single-fluid kinetic scales — see [[zhao-2022-3d-anisotropy-kinetic-scales-psp]].

### Claim boundary

Direct numerical simulations with PENCIL at M_s ≈ 0.1 and varying β (or M_A). Driving via velocity or magnetic forcing at large scales. Claim is about *spectral slopes* and *sign* of E_r in the inertial range of these simulations.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

E_r > 0 in weakly compressible MHD. Magnetically-driven runs follow α ≈ −3/2 (dynamic alignment); kinetically-driven runs follow α ≈ −1 (reflection-driven). β-dependent slope α(β): −2 ≲ α ≲ −5/3 at β=4; −5/3 ≲ α ≲ −3/2 at β=1; α ≈ −1 at β=0.3.

### 2.2 Equations / method

- E_r(k) = E_kin(k) − E_mag(k).
- Sonic Mach number M_s and Alfvén Mach number M_A.
- Plasma β = 2 M_A^2 / M_s^2.
- Spectral fitting in inertial range.

### 2.3 Data assumptions

- PENCIL DNS at M_s ≈ 0.1.
- Forcing scheme (velocity vs magnetic) declared.
- Inertial-range extent fits a power law over ≥ 1 decade.

### 2.4 Failure modes (skill memory)

- **Forcing-scale leakage** corrupts inertial-range slope estimate.
- **Numerical dissipation** at high-k flattens slopes — pick fit window away from dissipation.
- **Finite box size** sets minimum k accessible.
- **Compressibility threshold**: weakly compressible regime breaks down approaching M_s ~ 1.

### 2.5 Figure / numerical targets

- Magnetically-driven α ≈ −3/2.
- Kinetically-driven α ≈ −1.
- β-trend recovered within reported error bars (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-MHD-DNS**: weakly compressible MHD with mean guide field.
- **C-FORCING**: switchable velocity vs magnetic large-scale forcing.
- **C-SPECTRAL-FIT**: inertial-range fit of E_kin, E_mag, E_r.

### 3.2 Procedure

1. Choose β ∈ {0.3, 1.0, 4.0}.
2. Run pair of simulations with velocity and magnetic forcing.
3. Evolve to a quasi-steady state.
4. C-SPECTRAL-FIT for E_kin, E_mag, E_r over inertial range.
5. Report slope α and sign of E_r.

### 3.3 Minimum reproduction artifacts

- Power-spectrum CSV for E_kin, E_mag, E_r per run.
- Fitted slopes vs (β, forcing) table.

---

## 4. Adapter / runtime notes (optional examples)

- Any MHD DNS code with a large-scale forcing module satisfies the contracts.
- PENCIL, Athena, MURaM are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Tension with solar-wind observations**: in-situ E_r is typically negative; the simulation's E_r > 0 raises a tension that may resolve via dynamic alignment vs compressibility — test which mechanism dominates locally.
- **Composability with [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]**: the α ≈ −1 reflection-driven signature gives a direct discriminator between forcing modes; check whether PSP spectra in young solar wind show this slope.
- **Open hypothesis**: Does the β-dependence of α(β) (Skalidis et al.) survive when expanding-box geometry is added?
- **Methodological experiment**: hybridize velocity + magnetic forcing in a single run and trace the slope as a continuous function of the forcing ratio.

---

## Links

- arXiv: https://arxiv.org/abs/2512.11973
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.11973`

## Skill graph

- [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]
- [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]

