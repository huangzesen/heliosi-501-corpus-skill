---
name: regulation-proton-alpha-flow-compressive-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# regulation-proton-alpha-flow-compressive-2023

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from + co-authors (TODO verify full list) et al. 2023 (TODO_verify_journal; arXiv:2308.02036).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the radial evolution of proton-α differential flow under combined compressive-fluctuation and instability regulation.
- Decide whether observed |v_α − v_p| decay vs r is consistent with the proposed regulation channel.

### When NOT to use it

- Pure expansion-driven flow decay without fluctuations.
- Multi-fluid coronal acceleration mechanism.

### Claim boundary

Hybrid simulations with prescribed compressive-fluctuation amplitude; observed flow-decay statistics compared.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Combined compressive-fluctuation pitch-angle scattering and ion-scale-instability action regulate proton-α drift toward marginal stability; the observed |Δv_pα|(r) is reproducible.

### 2.2 Equations / method

- Drift-instability threshold for proton-α systems.
- Compressive-fluctuation effective scattering rate.

### 2.3 Data assumptions

- Hybrid simulation with α population.
- Prescribed compressive-fluctuation amplitude.

### 2.4 Failure modes (skill memory)

- **Fluctuation-amplitude prescription** drives magnitude of regulation.
- **Initial Δv_pα** sets onset of instability.

### 2.5 Figure / numerical targets

- Δv_pα(r) profile within in-situ envelope (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HYBRID-PROTON-ALPHA**.
- **C-COMPRESSIVE-AMP**.
- **C-DRIFT-INSTAB**.

### 3.2 Procedure

1. Initialize with Δv_pα.
2. Apply compressive-fluctuation field.
3. Run hybrid simulation.
4. Track Δv_pα(t).

### 3.3 Minimum reproduction artifacts

- Δv_pα(r) profile.

---

## 4. Adapter / runtime notes (optional examples)

- Hybrid PIC with α support satisfies contracts.

---

## 5. Research-generation affordance

- **Composability with [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]**: extend AW-driven beam regulation to multi-species drift.
- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**: connect ion-scale wave occurrence to drift regulation.
- **Open hypothesis**: Do CIR-adjacent intervals where compressive fluctuations are enhanced show faster Δv_pα decay?

---

## Links

- arXiv: https://arxiv.org/abs/2308.02036
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2308.02036`

## Skill graph

- [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]
- [[verniero-2020-proton-beams-ion-scale-waves]]

