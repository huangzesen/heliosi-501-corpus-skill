---
name: parametric-instability-alfven-wave-packets-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# parametric-instability-alfven-wave-packets-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2507.10038).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the parametric instability of finite-bandwidth Alfvén-wave packets (not single waves).
- Distinguish packet-PDI growth rates from monochromatic-PDI predictions.

### When NOT to use it

- Single-wave PDI growth — see [[saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun]].
- Strong-turbulence cascade.

### Claim boundary

Linear stability of Alfvén-wave *packets* with specified bandwidth; analytic growth rates derived for chosen packet shape; numerical verification in 1D MHD.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Packet bandwidth modifies γ_max relative to the monochromatic case; the modification scales with bandwidth-to-frequency ratio in a paper-specified way.

### 2.2 Equations / method

- Mathieu/wave-packet stability equation for AW + sideband decay.
- Effective γ_max(Δω/ω_0).

### 2.3 Data assumptions

- Packet shape, bandwidth, central frequency, amplitude specified.
- Background β fixed.

### 2.4 Failure modes (skill memory)

- **Packet-shape choice** changes the effective coupling.
- **Amplitude beyond linear regime** invalidates analysis.
- **Bandwidth too large** removes wave-packet identity.

### 2.5 Figure / numerical targets

- γ_max vs Δω/ω_0 curve (TODO verify analytic).
- 1D MHD verification of analytic growth rate.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-PACKET-PDI-LINEAR**: packet linear stability analyzer.
- **C-MHD-1D-VERIFY**: 1D MHD packet evolution.

### 3.2 Procedure

1. Specify packet (shape, Δω, ω_0, amplitude).
2. C-PACKET-PDI-LINEAR: derive γ_max.
3. C-MHD-1D-VERIFY: run 1D MHD to confirm growth.

### 3.3 Minimum reproduction artifacts

- γ_max vs Δω/ω_0 plot.
- 1D MHD energy-growth curves.

---

## 4. Adapter / runtime notes (optional examples)

- Any 1D MHD code + linear-stability harness satisfies the contracts.

---

## 5. Research-generation affordance

- **Tension with monochromatic PDI**: solar-wind AW spectra are *broadband*; predictions for switchback/PDI seeds should use packet-PDI rather than single-wave growth rates.
- **Composability with [[saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun]]**: combine packet structure with anisotropy correction.
- **Open hypothesis**: Does observed compressible-sideband occurrence in PSP correlate with broadband AW activity per packet-PDI prediction?

---

## Links

- arXiv: https://arxiv.org/abs/2507.10038
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2507.10038`

## Skill graph

- [[saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun]]
- [[shoda-2021-turbulence-switchback-generation-alfvenic]]

