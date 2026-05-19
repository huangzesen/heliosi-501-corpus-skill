# chandran-2010-stochastic-heating-perp-alfven

A paper-skill compiled from B. D. G. Chandran, + co-authors (TODO verify full list) et al. 2010 (TODO_verify_journal; arXiv:TODO_verify_with_full_text).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Provide the analytic stochastic-heating closure used by downstream PSP-era skills.
- Compute Q_⊥(δv_⊥, v_⊥, ρ_i) for given turbulence amplitude.

### When NOT to use it

- In-situ application — see [[stochastic-heating-sub-alfvenic-2025]].

### Claim boundary

Analytic derivation; constants c_1, c_2 calibrated against test-particle simulations.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Stochastic perpendicular heating rate has the form Q_⊥ ~ c_1 (δv_⊥)^3 / ρ_i exp(−c_2/ε), with calibrated c_1, c_2.

### 2.2 Equations / method

- ε ≡ δv_⊥/v_⊥.
- Q_⊥ closure expression.

### 2.3 Data assumptions

- Test-particle calibration of c_1, c_2.

### 2.4 Failure modes (skill memory)

- **ε ≲ 0.1** kills the exponent.
- **Spectrum bandwidth** modifies c_1.

### 2.5 Figure / numerical targets

- Reproduces published Q_⊥(ε) curve (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-STOCHASTIC-Q-PERP**: analytic closure evaluator.

### 3.2 Procedure

1. Supply (δv_⊥, v_⊥, ρ_i).
2. Evaluate Q_⊥.

### 3.3 Minimum reproduction artifacts

- Q_⊥ evaluator.

---

## 4. Adapter / runtime notes (optional examples)

- Implementable as a one-liner — any harness suffices.

---

## 5. Research-generation affordance

- **Composability with [[peng-2025-chaotic-ion-motion-finite-amplitude-alfven]]**: ε > 0.1 vs P_eff < 25 — two distinct chaos criteria, joint diagnostic.
- **Open hypothesis**: Are observed Q_⊥ events bimodal in ε, separating stochastic-heating-on vs -off regimes?

---

## Links

- arXiv: https://arxiv.org/abs/TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md (TODO verify section)`

## Skill graph

- [[stochastic-heating-sub-alfvenic-2025]]
- [[peng-2025-chaotic-ion-motion-finite-amplitude-alfven]]

