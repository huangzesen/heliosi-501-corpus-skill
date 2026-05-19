---
name: oblique-drift-instability-solar-wind-heating-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# oblique-drift-instability-solar-wind-heating-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2512.18485).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict heating contribution of oblique-drift-instability modes in the solar wind.
- Diagnose whether observed VDF features are constrained by oblique-drift marginality.

### When NOT to use it

- Parallel drift modes only — see [[proton-alpha-aic-driven-instabilities-2023]].

### Claim boundary

Hybrid simulations and linear-Vlasov scans of oblique-drift-instability families.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Oblique drift modes provide a heating channel not captured by parallel-only models; their action pins specific VDF features at marginal stability.

### 2.2 Equations / method

- Oblique drift-mode dispersion in (k_∥, k_⊥) plane.
- Q heating rate from oblique branch.

### 2.3 Data assumptions

- Hybrid simulation or linear-Vlasov with oblique-k coverage.

### 2.4 Failure modes (skill memory)

- **Reduced dimensionality** loses oblique branches.
- **Drift orientation relative to B** controls γ_max.

### 2.5 Figure / numerical targets

- Q-oblique vs Q-parallel ratio (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-LIN-VLASOV-OBLIQUE**.
- **C-HYBRID-OBLIQUE-DRIFT**.

### 3.2 Procedure

1. Define drift VDF.
2. C-LIN-VLASOV-OBLIQUE: scan oblique k.
3. C-HYBRID-OBLIQUE-DRIFT: validate Q.

### 3.3 Minimum reproduction artifacts

- Q vs (k_⊥/k_∥) curve.

---

## 4. Adapter / runtime notes (optional examples)

- ALPS, PLUME oblique scans are example Layer-3.

---

## 5. Research-generation affordance

- **Composability with [[proton-alpha-aic-driven-instabilities-2023]]**: complements parallel-only attribution.
- **Open hypothesis**: Are observed VDF features previously misattributed to AIC actually oblique-drift signatures?

---

## Links

- arXiv: https://arxiv.org/abs/2512.18485
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.18485`

## Skill graph

- [[proton-alpha-aic-driven-instabilities-2023]]
- [[ion-driven-instabilities-classification-2023]]

