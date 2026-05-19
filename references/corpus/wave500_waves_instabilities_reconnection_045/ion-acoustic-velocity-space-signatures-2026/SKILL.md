---
name: ion-acoustic-velocity-space-signatures-2026
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# ion-acoustic-velocity-space-signatures-2026

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2026 (TODO_verify_journal; arXiv:2601.08329).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Detect the velocity-space signature (FPC) of ion-acoustic instabilities in in-situ VDF data.
- Quantify direction and magnitude of energy transfer in IA-unstable plasmas.

### When NOT to use it

- Linear-only IA classification — see [[ion-acoustic-damping-instability-solo-2026]].

### Claim boundary

Field-particle-correlation (FPC) framework applied to in-situ VDF + E-field data. Coverage limited to intervals with sufficient cadence.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Velocity-space FPC signature of IA instability has a characteristic dipolar structure in (v_∥, time); presence/absence diagnoses energy transfer direction.

### 2.2 Equations / method

- C(v,t) = ⟨q v_∥ E_∥ ∂f/∂v_∥⟩ correlator.
- Energy-transfer integral over velocity space.

### 2.3 Data assumptions

- High-cadence VDF + E_∥ at the IA frequency.
- Adequate FPC averaging window.

### 2.4 Failure modes (skill memory)

- **Cadence aliasing** smears the dipolar feature.
- **E_∥ noise floor** sets sensitivity.

### 2.5 Figure / numerical targets

- FPC dipolar pattern recovered on labeled events (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FPC**: field-particle correlator.
- **C-VDF-LOAD-HIGH-CADENCE**.

### 3.2 Procedure

1. C-VDF-LOAD-HIGH-CADENCE + E_∥.
2. C-FPC: compute correlator vs time.
3. Integrate over v-space.

### 3.3 Minimum reproduction artifacts

- FPC plots per event.
- Energy-transfer rate per event.

---

## 4. Adapter / runtime notes (optional examples)

- Klein-Howes FPC routines are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[ion-acoustic-damping-instability-solo-2026]]**: completes linear→nonlinear loop.
- **Open hypothesis**: Are damped-IA intervals signed differently in FPC than unstable ones?

---

## Links

- arXiv: https://arxiv.org/abs/2601.08329
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2601.08329`

## Skill graph

- [[ion-acoustic-damping-instability-solo-2026]]

