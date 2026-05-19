---
name: kinetic-turbulence-collisionless-high-beta-2022
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# kinetic-turbulence-collisionless-high-beta-2022

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2022 (TODO_verify_journal; arXiv:2207.05189).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the cascade phenomenology in collisionless high-β plasmas where pressure anisotropy dominates over magnetic tension.
- Decide whether observed high-β solar-wind intervals exhibit the predicted anisotropy-mediated cascade signatures.

### When NOT to use it

- Low-β / coronal regime — separate skill.
- Single-instability dynamics without turbulent cascade.

### Claim boundary

Hybrid-kinetic simulations in the collisionless high-β regime; cascade phenomenology derived analytically and validated numerically. Claim restricted to the simulated β range.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Collisionless high-β kinetic turbulence is mediated by pressure-anisotropy-driven micro-instabilities; the resulting cascade has a paper-specified spectral index and anisotropy that differ from low-β KAW phenomenology.

### 2.2 Equations / method

- Anisotropy-driven micro-instability thresholds.
- Effective viscosity ν_eff from micro-instability scattering.
- Cascade spectrum modified by ν_eff.

### 2.3 Data assumptions

- Hybrid-kinetic simulation in high-β regime.
- Adequate resolution at ion scales.

### 2.4 Failure modes (skill memory)

- **β regime selection** — extrapolation to other β invalid.
- **Initial-anisotropy** drives which instability dominates.
- **Reduced dimensionality** restricts instability families.

### 2.5 Figure / numerical targets

- Inertial-range slope shift vs low-β reference (TODO verify magnitude).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HYBRID-HIGHBETA**: hybrid-kinetic simulation in high-β.
- **C-ANISOTROPY-DIAG**: pressure-anisotropy moment tracker.
- **C-SPECTRAL-FIT**: inertial-range slope fit.

### 3.2 Procedure

1. Initialize at chosen high-β.
2. Run hybrid-kinetic simulation to saturated state.
3. C-ANISOTROPY-DIAG: confirm β-instability regime.
4. C-SPECTRAL-FIT: extract slope.

### 3.3 Minimum reproduction artifacts

- Spectrum CSV.
- Anisotropy-evolution time series.

---

## 4. Adapter / runtime notes (optional examples)

- Pegasus, Hybrid-VPIC are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[firehose-thermodynamics-high-beta-2025]]**: turbulence-induced ν_eff feeds into firehose marginal-stability state.
- **Composability with PSP HCS/streamer-belt high-β intervals**: test slope shift directly.
- **Open hypothesis**: Do observed slope-anomaly intervals at high β in PSP exhibit the predicted anisotropy mediation?

---

## Links

- arXiv: https://arxiv.org/abs/2207.05189
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2207.05189`

## Skill graph

- [[firehose-thermodynamics-high-beta-2025]]
- [[ion-driven-instabilities-classification-2023]]

