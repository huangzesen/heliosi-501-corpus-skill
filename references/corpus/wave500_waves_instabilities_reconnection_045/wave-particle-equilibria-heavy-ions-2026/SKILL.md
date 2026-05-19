---
name: wave-particle-equilibria-heavy-ions-2026
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# wave-particle-equilibria-heavy-ions-2026

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from + co-authors (TODO verify full list) et al. 2026 (TODO_verify_journal; arXiv:2603.22613).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict equilibrium VDFs of heavy ions under wave-particle interaction in weakly collisional space plasmas.
- Decide whether observed heavy-ion T_⊥/T_∥ matches wave-particle-equilibrium prediction.

### When NOT to use it

- Single-instability action without equilibrium framework.

### Claim boundary

Wave-particle equilibrium theory with heavy ions; verified by hybrid simulation.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Heavy-ion VDFs in weakly collisional space plasmas settle into wave-particle equilibria specified by the wave spectrum; observed solar-wind heavy ions sit on this locus within stated bars.

### 2.2 Equations / method

- Wave-particle equilibrium VDF F_eq(v).
- Quasi-linear flux closure.

### 2.3 Data assumptions

- Wave spectrum prescription.
- Heavy-ion species composition.

### 2.4 Failure modes (skill memory)

- **Wave-spectrum prescription** dominates F_eq.
- **Collisionality residual** breaks weak-collision assumption.

### 2.5 Figure / numerical targets

- F_eq locus matches in-situ heavy-ion VDFs (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-WAVE-SPECTRUM**.
- **C-EQUILIBRIUM-VDF**.
- **C-HYBRID-HEAVY-ION-VERIFY**.

### 3.2 Procedure

1. C-WAVE-SPECTRUM.
2. C-EQUILIBRIUM-VDF.
3. C-HYBRID-HEAVY-ION-VERIFY.

### 3.3 Minimum reproduction artifacts

- F_eq(v) curves per heavy-ion species.

---

## 4. Adapter / runtime notes (optional examples)

- Hybrid PIC with heavy-ion species suffices.

---

## 5. Research-generation affordance

- **Composability with [[extreme-minor-ion-heating-imbalanced-turbulence-2024]]**: heavy ions out of equilibrium correspond to extreme-heating regime.
- **Open hypothesis**: Are SolO SWA heavy-ion VDFs at given streams more consistent with wave-particle equilibrium or pure adiabatic expansion?

---

## Links

- arXiv: https://arxiv.org/abs/2603.22613
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2603.22613`

## Skill graph

- [[extreme-minor-ion-heating-imbalanced-turbulence-2024]]
- [[klein-2018-multispecies-stability-anisotropy]]

