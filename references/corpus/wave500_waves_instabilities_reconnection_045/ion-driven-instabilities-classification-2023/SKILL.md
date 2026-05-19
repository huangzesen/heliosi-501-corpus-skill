---
name: ion-driven-instabilities-classification-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# ion-driven-instabilities-classification-2023

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2023 (TODO_verify_journal; arXiv:2306.06060).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Classify a given in-situ VDF against parallel/oblique ion-driven instability families.
- Decide which instability family dominates the local plasma state in the inner heliosphere.

### When NOT to use it

- Electron-driven instabilities — see [[electron-driven-instabilities-solar-wind-2022]].
- Heating-rate inference — separate skill.

### Claim boundary

Linear-Vlasov classification framework using multi-dimensional stability scan over species drift, temperature anisotropy, and β. Applied to inner-heliosphere VDFs.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Multi-dimensional linear classification of ion-driven instabilities partitions inner-heliosphere VDFs into stable / cyclotron / firehose / mirror / drift-driven classes with quantified margins.

### 2.2 Equations / method

- Multi-species linear-Vlasov dispersion D(ω, k, params).
- Margin = γ_max(local VDF) / max_growth-class boundary.
- Class membership by largest γ_max within tolerance.

### 2.3 Data assumptions

- In-situ proton (and α) VDF or its moment proxy.
- Linear-Vlasov dispersion solver with multi-species support.

### 2.4 Failure modes (skill memory)

- **Moment-only inputs** miss non-Maxwellian instabilities.
- **k-grid coverage** crucial for oblique modes.
- **Solver-tolerance** at low γ_max yields class flip-flop.

### 2.5 Figure / numerical targets

- Classification reproduced on paper's labeled test events (TODO verify).
- Class fractions in inner-heliosphere intervals.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-LIN-VLASOV**: multi-species linear-Vlasov dispersion solver.
- **C-VDF-LOAD**: in-situ VDF loader.
- **C-INSTAB-CLASSIFIER**: γ_max-based classification.

### 3.2 Procedure

1. C-VDF-LOAD for the candidate interval.
2. C-LIN-VLASOV: scan k-grid.
3. C-INSTAB-CLASSIFIER: assign class.

### 3.3 Minimum reproduction artifacts

- Per-interval classification JSON.
- γ_max-vs-k diagnostic plot.

---

## 4. Adapter / runtime notes (optional examples)

- Any linear-Vlasov dispersion solver suffices (NHDS, PLUME, ALPS).

---

## 5. Research-generation affordance

- **Composability with [[firehose-thermodynamics-high-beta-2025]]**: validate ν_eff hypothesis by class-conditioning.
- **Composability with [[expansion-instability-young-solar-wind-thermo-2026]]**: trace instability-class transitions vs r.
- **Open hypothesis**: Does class membership cluster by stream type (fast vs slow vs CIR)?

---

## Links

- arXiv: https://arxiv.org/abs/2306.06060
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2306.06060`

## Skill graph

- [[firehose-thermodynamics-high-beta-2025]]
- [[expansion-instability-young-solar-wind-thermo-2026]]
- [[klein-2018-multispecies-stability-anisotropy]]

