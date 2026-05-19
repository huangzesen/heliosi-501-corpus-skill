---
name: extreme-minor-ion-heating-imbalanced-turbulence-2024
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# extreme-minor-ion-heating-imbalanced-turbulence-2024

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2024 (TODO_verify_journal; arXiv:2408.04703).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict perpendicular heating rates of minor ions (α, O^{5+}, Fe) in highly imbalanced Alfvénic turbulence.
- Decide whether observed minor-ion T_⊥ enhancements in fast wind are produced by the helicity-barrier channel.

### When NOT to use it

- Proton-core-only heating — see [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]].
- Wave-particle equilibria with heavy ions — see [[wave-particle-equilibria-heavy-ions-2026]].

### Claim boundary

Hybrid simulations of imbalanced Alfvénic turbulence with passive minor-ion populations. Heating-rate scaling derived in the simulated regime.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Minor ions receive extreme perpendicular heating in highly imbalanced turbulence — disproportionate to their mass — consistent with helicity-barrier channelling toward gyroresonance.

### 2.2 Equations / method

- Per-species Q_⊥ vs (q_s, m_s, σ_c).
- Helicity-barrier-induced spectral pile-up at ion gyroscales.

### 2.3 Data assumptions

- Hybrid simulation with minor-ion test populations.
- Imbalanced driving with prescribed σ_c.

### 2.4 Failure modes (skill memory)

- **Passive vs back-reacting ions** changes Q_⊥ magnitude.
- **σ_c prescription** dominates result.
- **Box size** clips relevant gyroscales.

### 2.5 Figure / numerical targets

- Q_⊥(m_s/m_p) scaling reproduced (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HYBRID-MINOR-ION**: hybrid simulation with minor-ion populations.
- **C-SIGMA-C-DRIVE**: imbalanced driving control.
- **C-Q-PERP-SPECIES**: per-species heating-rate extractor.

### 3.2 Procedure

1. Initialize with imbalanced σ_c.
2. C-HYBRID-MINOR-ION: evolve to saturated state.
3. C-Q-PERP-SPECIES: extract per-species Q_⊥.

### 3.3 Minimum reproduction artifacts

- Q_⊥/Q_p vs (m_s/m_p) curve.

---

## 4. Adapter / runtime notes (optional examples)

- Pegasus, Hybrid-VPIC are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[helicity-barrier-evidence-transition-range-2024]]**: predicts that minor-ion heating tracks the helicity-barrier transition-range signature.
- **Composability with [[wave-particle-equilibria-heavy-ions-2026]]**: marginal-stability vs out-of-equilibrium populations.
- **Open hypothesis**: Are observed α and heavy-ion T_⊥/T_p enhancements in fast wind closer to the helicity-barrier-predicted scaling than to mass-proportional heating?

---

## Links

- arXiv: https://arxiv.org/abs/2408.04703
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2408.04703`

## Skill graph

- [[helicity-barrier-evidence-transition-range-2024]]
- [[wave-particle-equilibria-heavy-ions-2026]]
- [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]

