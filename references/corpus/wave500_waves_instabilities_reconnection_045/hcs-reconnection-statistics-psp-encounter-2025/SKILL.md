---
name: hcs-reconnection-statistics-psp-encounter-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# hcs-reconnection-statistics-psp-encounter-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:TODO_verify_with_full_text).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Statistically catalog reconnection-exhaust events in HCS crossings by PSP.
- Quantify exhaust occurrence vs r and reconnection-exhaust thickness.

### When NOT to use it

- Switchback-boundary reconnection — see [[phan-2022-switchback-boundary-reconnection-psp]] (existing).
- Energetic-particle acceleration at HCS — see [[paper-desai-2024-hcs-reconnection-400kev-protons]] (existing).

### Claim boundary

Encounter-aggregated catalog using Walén test + topological diagnostics on HCS crossings.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

HCS-reconnection events catalogued across PSP encounters show characteristic exhaust thickness, occurrence rate vs r, and tied energetic-particle signatures.

### 2.2 Equations / method

- Walén relation ΔV ≈ ±ΔV_A across HCS jump.
- Exhaust-thickness estimate via timing.

### 2.3 Data assumptions

- PSP FIELDS MAG + SWEAP across multiple encounters.
- HCS crossing list.

### 2.4 Failure modes (skill memory)

- **HCS-crossing identification ambiguity**.
- **Walén tolerance** choice changes count.

### 2.5 Figure / numerical targets

- Exhaust-event count per encounter (TODO verify).
- Occurrence-rate vs r curve.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HCS-CROSSING-CATALOG**.
- **C-WALEN**: as in [[phan-2022-switchback-boundary-reconnection-psp]].
- **C-EXHAUST-THICKNESS**.

### 3.2 Procedure

1. C-HCS-CROSSING-CATALOG.
2. C-WALEN at each crossing.
3. C-EXHAUST-THICKNESS for confirmed events.

### 3.3 Minimum reproduction artifacts

- HCS reconnection-event table.
- Occurrence-rate vs r.

---

## 4. Adapter / runtime notes (optional examples)

- PySPEDAS + Walén harness from [[phan-2022-switchback-boundary-reconnection-psp]] suffices.

---

## 5. Research-generation affordance

- **Composability with [[paper-desai-2024-hcs-reconnection-400kev-protons]]**: link energetic-particle signatures to reconnection inventory.
- **Composability with [[paper-murtas-2024-compression-acceleration-hcs]]**: distinguish reconnection vs compression acceleration channels.
- **Open hypothesis**: Does HCS-reconnection occurrence vs r follow PFSS-predicted HCS topology gradients?

---

## Links

- arXiv: https://arxiv.org/abs/TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/arxiv_id=TODO_verify`

## Skill graph

- [[phan-2022-switchback-boundary-reconnection-psp]]
- [[paper-desai-2024-hcs-reconnection-400kev-protons]]
- [[paper-murtas-2024-compression-acceleration-hcs]]

