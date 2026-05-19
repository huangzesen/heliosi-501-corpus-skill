---
name: ion-acoustic-damping-instability-solo-2026
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# ion-acoustic-damping-instability-solo-2026

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from the primary source (author list pending verification), 2026 (TODO_verify_journal; arXiv:2604.14311).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Decide whether observed Solar Orbiter ion-acoustic-wave intervals are damped or unstable.
- Quantify (T_e/T_i)-dependent damping rates for IA modes.

### When NOT to use it

- Modulated-IAW machine-learning detection — see [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]] (existing).

### Claim boundary

Solar Orbiter event-level analysis of ion-acoustic-wave intervals; growth/damping classified via linear-Vlasov with measured (T_e, T_i, drift) inputs.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Ion-acoustic-wave intervals separate into damped vs unstable subpopulations with paper-specified (T_e/T_i) thresholds.

### 2.2 Equations / method

- IA dispersion ω^2 = k^2 c_s^2 / (1 + k^2 λ_D^2).
- Landau damping rate γ(T_e/T_i).

### 2.3 Data assumptions

- SolO RPW + SWA inputs.
- Linear-Vlasov solver.

### 2.4 Failure modes (skill memory)

- **T_e estimation** systematics dominate γ.
- **Drift estimation** noise.

### 2.5 Figure / numerical targets

- Damped/unstable split at observed (T_e/T_i) threshold (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-SOLO-RPW-SWA**.
- **C-LIN-VLASOV-IA**.

### 3.2 Procedure

1. C-FETCH-SOLO-RPW-SWA.
2. C-LIN-VLASOV-IA: damping/growth rate per interval.
3. Aggregate classification.

### 3.3 Minimum reproduction artifacts

- Damped vs unstable event tables.

---

## 4. Adapter / runtime notes (optional examples)

- SolO RPW pipelines example Layer-3.

---

## 5. Research-generation affordance

- **Composability with [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]**: ML-detected events labeled with linear-theory classification.
- **Composability with [[ion-acoustic-velocity-space-signatures-2026]]**: cross-validate energy-transfer direction.
- **Open hypothesis**: Does the damped/unstable fraction vary with stream type?

---

## Links

- arXiv: https://arxiv.org/abs/2604.14311
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2604.14311`

## Skill graph

- [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]
- [[ion-acoustic-velocity-space-signatures-2026]]

