---
name: whistler-counter-propagating-encounter1-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# whistler-counter-propagating-encounter1-2023

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2023 (TODO_verify_journal; arXiv:2304.01185).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify counter-propagating whistler populations in PSP Encounter-1 data.
- Distinguish locally generated vs convected whistler events using k-direction.

### When NOT to use it

- Generic whistler-statistics catalog — see [[whistler-young-solar-wind-statistics-2024]].

### Claim boundary

Encounter-1-specific event analysis. k-direction extracted from SVD or analogue.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Counter-propagating whistler events in PSP Encounter-1 separate into anti-sunward (local-instability driven) and sunward (reflection/remote-source) populations.

### 2.2 Equations / method

- SVD polarization to identify k.
- Reflection-coefficient diagnostic at V_A gradients.

### 2.3 Data assumptions

- PSP Encounter-1 burst-data coverage.

### 2.4 Failure modes (skill memory)

- **Single-encounter coverage** limits generality.
- **Reflection-candidate identification** requires V_A profile.

### 2.5 Figure / numerical targets

- Counter-propagating event count reproduced (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP-ENCOUNTER1**.
- **C-POL-SVD**.
- **C-VA-GRADIENT-CANDIDATE**.

### 3.2 Procedure

1. C-FETCH-PSP-ENCOUNTER1.
2. C-POL-SVD per event.
3. C-VA-GRADIENT-CANDIDATE: identify reflection candidates.

### 3.3 Minimum reproduction artifacts

- Encounter-1 whistler event catalog with k-sign.

---

## 4. Adapter / runtime notes (optional examples)

- PySPEDAS PSP bindings.

---

## 5. Research-generation affordance

- **Composability with [[alfven-wave-propagation-reflection-trapping-2025]]**: directly tests the reflection-driven prediction.
- **Open hypothesis**: Are reflection-candidate whistlers associated with specific V_A-gradient amplitudes?

---

## Links

- arXiv: https://arxiv.org/abs/2304.01185
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2304.01185`

## Skill graph

- [[whistler-young-solar-wind-statistics-2024]]
- [[alfven-wave-propagation-reflection-trapping-2025]]

