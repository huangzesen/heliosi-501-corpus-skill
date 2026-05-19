# kontar-2025-ion-scale-turbulence-cascade-rate-corona

A paper-skill compiled from E. P. Kontar, A. G. Emslie, + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2509.17861).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Estimate the ion-scale turbulent energy-cascade rate ε in the corona and inner heliosphere from a combination of remote-sensing and in-situ inputs.
- Decide whether the inferred ε matches independently-measured heating rates.

### When NOT to use it

- Sub-electron-scale dissipation — see [[sharma-2026-kaw-subion-current-sheets-pic]].
- Pure DNS-derived cascade scalings without observational anchor.

### Claim boundary

Combined remote-sensing density-spectrum and in-situ ion-scale wave data; ε estimated via a third-order / spectral-flux closure adapted to the corona. Coverage limited to the regions where both data sources exist.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Inferred ion-scale ε(r) is consistent with the observed thermal heating rate over the corona and inner heliosphere, supporting the picture that ion-scale turbulence carries most of the dissipated energy.

### 2.2 Equations / method

- Spectral-flux estimator at ion scales.
- Density-spectrum to velocity-spectrum mapping via plasma compressibility.
- Heating-rate inference from temperature profiles.

### 2.3 Data assumptions

- Remote-sensing density spectrum (radio scintillation or analogue).
- In-situ ion-scale magnetic spectrum (PSP / SolO FIELDS).
- Independent T(r) measurement for heating-rate comparison.

### 2.4 Failure modes (skill memory)

- **Density-to-velocity mapping** depends on compressibility assumption.
- **Coverage gaps** between remote and in-situ regimes — flag continuity assumption.
- **Heating-rate proxy** depends on whether T_⊥ vs T_∥ is used.
- **Cascade-closure choice** (third-order vs spectral flux) yields factor-of-few differences.

### 2.5 Figure / numerical targets

- ε(r) agreement with thermal heating rate within stated bars (TODO verify magnitude).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-DENS-SPECTRUM-REMOTE**: load remote-sensing density spectrum.
- **C-MAG-SPECTRUM-INSITU**: in-situ ion-scale magnetic spectrum.
- **C-CASCADE-FLUX-ION**: ion-scale ε estimator.
- **C-HEATING-RATE-FROM-T**: heating-rate inference from T(r).

### 3.2 Procedure

1. Load remote + in-situ inputs in matched r.
2. C-CASCADE-FLUX-ION: estimate ε(r).
3. C-HEATING-RATE-FROM-T: compute Q(r).
4. Compare ε vs Q.

### 3.3 Minimum reproduction artifacts

- ε(r) and Q(r) curves.
- Closure-method-sensitivity table.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness providing both remote-sensing scintillation and PSP/SolO MAG access satisfies the contracts.

---

## 5. Research-generation affordance

- **Composability with [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]**: partition ε between cyclotron-resonant and Landau channels at the same r.
- **Tension with [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]**: PS-RDT predicts increased heating fraction — quantify whether observed ε(r) follows the PS-RDT scaling.
- **Open hypothesis**: Does the ion-scale ε near the Alfvén surface match the predicted Q from Alfvén-wave deposition in 1D wind models?

---

## Links

- arXiv: https://arxiv.org/abs/2509.17861
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2509.17861`

## Skill graph

- [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]
- [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]
- [[kasper-2021-psp-enters-magnetically-dominated-corona]]

