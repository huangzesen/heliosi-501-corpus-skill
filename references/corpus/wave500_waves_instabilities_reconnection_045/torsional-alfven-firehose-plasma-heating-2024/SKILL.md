---
name: torsional-alfven-firehose-plasma-heating-2024
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# torsional-alfven-firehose-plasma-heating-2024

A paper-skill compiled from the primary source (author list pending verification), 2024 (TODO_verify_journal; arXiv:2412.07451).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict perpendicular plasma heating from torsional Alfvén oscillations in firehose-unstable backgrounds.
- Diagnose whether observed firehose-marginal-stability intervals exhibit torsional-AW heating signatures.

### When NOT to use it

- Static firehose marginal-stability — see [[firehose-thermodynamics-high-beta-2025]].
- Mirror-mode heating — separate skill.

### Claim boundary

MHD / hybrid simulations of torsional AW in firehose-susceptible plasma. Heating-rate scaling derived in the simulated regime.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Torsional AW oscillations in firehose-unstable plasma drive a heating channel with specific (β_∥, ξ)-dependent rate distinct from passive firehose regulation.

### 2.2 Equations / method

- Torsional-AW equation in cylindrical / spherical geometry.
- Firehose-modified dispersion.
- Q heating-rate integral.

### 2.3 Data assumptions

- Torsional-AW initial state.
- Firehose-marginal background.

### 2.4 Failure modes (skill memory)

- **Geometry choice** affects torsional-mode polarization.
- **Firehose marginality** depends on driving rate.

### 2.5 Figure / numerical targets

- Q vs (β_∥, ξ) curve reproduced (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-TORSIONAL-AW-INIT**.
- **C-FIREHOSE-BACKGROUND**.
- **C-Q-MHD**: MHD-level heating-rate integrator.

### 3.2 Procedure

1. C-FIREHOSE-BACKGROUND: prepare unstable state.
2. C-TORSIONAL-AW-INIT: seed oscillation.
3. Run to saturated state.
4. C-Q-MHD: integrate heating rate.

### 3.3 Minimum reproduction artifacts

- Q vs (β_∥, ξ) table.

---

## 4. Adapter / runtime notes (optional examples)

- Any MHD or hybrid code with cylindrical geometry suffices.

---

## 5. Research-generation affordance

- **Composability with [[firehose-thermodynamics-high-beta-2025]]**: adds dynamic AW heating to passive marginal-stability state.
- **Composability with [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]**: torsional + amplitude-modulated AW joint effects.
- **Open hypothesis**: Are observed enhanced-heating intervals in PSP at firehose-marginal points associated with torsional-AW polarization?

---

## Links

- arXiv: https://arxiv.org/abs/2412.07451
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2412.07451`

## Skill graph

- [[firehose-thermodynamics-high-beta-2025]]
- [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]

