---
name: klein-2018-multispecies-stability-anisotropy
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# klein-2018-multispecies-stability-anisotropy

A paper-skill compiled from K. G. Klein, + co-authors (TODO verify) et al. 2018 (TODO_verify_journal; arXiv:TODO_verify_with_full_text).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Run a multi-species linear-Vlasov stability scan on a given in-situ VDF.
- Supply the dispersion-solver backbone for instability classification skills.

### When NOT to use it

- Specific event-classification logic — see [[ion-driven-instabilities-classification-2023]].
- Test-particle dynamics — see [[peng-2025-chaotic-ion-motion-finite-amplitude-alfven]].

### Claim boundary

Linear stability solver with multi-species support, anisotropy, and drift. Outputs γ(k), ω(k), polarization for each branch over chosen k-grid.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Multi-species linear-Vlasov dispersion can be solved on observed VDF moment sets to recover γ(k) and polarization with documented numerical-tolerance behavior.

### 2.2 Equations / method

- Multi-species linear-Vlasov dispersion relation.
- Polarization expansions in (E, B, n, V) components.
- Bi-Maxwellian moment closure (extensible).

### 2.3 Data assumptions

- Per-species moments (n, V, T_⊥, T_∥) provided.
- B, ρ background.
- k-grid resolution sufficient to capture oblique modes.

### 2.4 Failure modes (skill memory)

- **Bi-Maxwellian closure** misses non-Maxwellian instabilities.
- **Numerical contour** in complex ω plane needs care.
- **k-grid limits** clip oblique-mode growth.

### 2.5 Figure / numerical targets

- Recovers Gary–Wang multi-species stability map within stated tolerance (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-LIN-VLASOV-MULTI**: multi-species linear-Vlasov solver.
- **C-K-SCAN**: k-grid scan harness.
- **C-POLARIZATION-DIAG**: polarization extractor.

### 3.2 Procedure

1. Provide per-species moments.
2. Define k-grid (parallel and oblique).
3. C-LIN-VLASOV-MULTI: solve dispersion.
4. C-POLARIZATION-DIAG: tag branches.

### 3.3 Minimum reproduction artifacts

- γ(k), ω(k) tables.
- Polarization-tagged branch list.

---

## 4. Adapter / runtime notes (optional examples)

- PLUME, NHDS, ALPS are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with all kinetic-instability skills in this batch**: this is the foundational solver layer.
- **Methodological experiment**: extend to non-Maxwellian closure and quantify γ_max shifts.

---

## Links

- arXiv: https://arxiv.org/abs/TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md (TODO verify section)`

## Skill graph

- [[ion-driven-instabilities-classification-2023]]
- [[firehose-thermodynamics-high-beta-2025]]

