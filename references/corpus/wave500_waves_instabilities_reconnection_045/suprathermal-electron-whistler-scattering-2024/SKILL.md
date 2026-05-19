---
name: suprathermal-electron-whistler-scattering-2024
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# suprathermal-electron-whistler-scattering-2024

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2024 (TODO_verify_journal; arXiv:2402.06016).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Quantify pitch-angle diffusion of suprathermal (strahl) electrons by whistler waves between 0.2 and 1 AU.
- Decide whether observed strahl-width broadening with r is consistent with whistler scattering.

### When NOT to use it

- Whistler generation mechanism — see [[electron-driven-instabilities-solar-wind-2022]].
- Heat-flux closure — separate skill.

### Claim boundary

Diffusion-coefficient inference from observed whistler-wave amplitudes (PSP/SolO/Wind) coupled with quasi-linear theory. Coverage from 0.2 to 1 AU.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Whistler-driven quasi-linear pitch-angle diffusion accounts for the observed strahl-width broadening between 0.2 and 1 AU within stated bars.

### 2.2 Equations / method

- Quasi-linear D_αα from observed wave power.
- Strahl-PAD width evolution as a diffusion process.

### 2.3 Data assumptions

- Multi-mission whistler-amplitude data 0.2–1 AU.
- Strahl-PAD measurements for comparison.

### 2.4 Failure modes (skill memory)

- **Wave-power normalization** uncertainty.
- **Cyclotron-resonance condition** breakdown for non-Maxwellian strahl tail.

### 2.5 Figure / numerical targets

- Strahl-width evolution within ±20% of observations (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-WHISTLER-AMP-MULTI**: whistler-amplitude data 0.2–1 AU.
- **C-QL-DIFFUSION**: quasi-linear diffusion coefficient.
- **C-STRAHL-WIDTH**: strahl-PAD width evolution.

### 3.2 Procedure

1. C-WHISTLER-AMP-MULTI.
2. C-QL-DIFFUSION: compute D_αα.
3. C-STRAHL-WIDTH: compare observed broadening to predicted.

### 3.3 Minimum reproduction artifacts

- D_αα(r) curves.
- Strahl-width vs r comparison.

---

## 4. Adapter / runtime notes (optional examples)

- Any multi-mission CDF I/O suffices.

---

## 5. Research-generation affordance

- **Composability with [[whistler-young-solar-wind-statistics-2024]]**: pulls amplitude statistics directly.
- **Composability with [[electron-driven-instabilities-solar-wind-2022]]**: closes scattering loop with local generation.
- **Open hypothesis**: Do non-broadened strahl intervals correspond to whistler-quiet plasma per joint catalog?

---

## Links

- arXiv: https://arxiv.org/abs/2402.06016
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2402.06016`

## Skill graph

- [[whistler-young-solar-wind-statistics-2024]]
- [[electron-driven-instabilities-solar-wind-2022]]

