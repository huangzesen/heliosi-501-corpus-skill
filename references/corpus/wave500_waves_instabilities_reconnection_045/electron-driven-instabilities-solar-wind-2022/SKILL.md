# electron-driven-instabilities-solar-wind-2022

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2022 (TODO_verify_journal; arXiv:2206.10403).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict electron-driven instability families (whistler heat-flux, electron firehose) in given solar-wind VDFs.
- Decide whether observed whistler waves are produced by local electron-VDF free energy.

### When NOT to use it

- Ion-driven instabilities — see [[ion-driven-instabilities-classification-2023]].
- Direct whistler-wave detection — see [[whistler-young-solar-wind-statistics-2024]].

### Claim boundary

Linear-Vlasov classification across electron-instability families using observed VDFs and the PLUME / NHDS / ALPS solver family. Coverage limited to the radii and stream types analysed.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Electron-driven instabilities (whistler heat-flux, electron firehose) populate distinct regions of (β_e, T_⊥,e/T_∥,e, q_e/q_max) parameter space; predicted γ_max-driven occurrences correlate with observed wave activity.

### 2.2 Equations / method

- Electron-heat-flux threshold q_e / q_max.
- Whistler heat-flux instability dispersion.
- Electron firehose threshold.

### 2.3 Data assumptions

- Electron VDF or its moment estimate.
- Electron-side multi-species solver support.

### 2.4 Failure modes (skill memory)

- **Heat-flux normalization** choice changes onset point.
- **Electron VDF tail** (strahl) requires kappa or split-population closure.
- **Cadence vs collisional relaxation** matters for class assignment.

### 2.5 Figure / numerical targets

- Heat-flux-instability boundary in (β_e, q_e/q_max) reproduced (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-VDF-ELECTRON**: electron VDF loader.
- **C-LIN-VLASOV-ELECTRON**: electron-species dispersion.
- **C-HEAT-FLUX-NORM**: q_e / q_max diagnostic.

### 3.2 Procedure

1. C-VDF-ELECTRON load.
2. Compute heat-flux and anisotropy moments.
3. C-LIN-VLASOV-ELECTRON: solve dispersion.
4. Classify against thresholds.

### 3.3 Minimum reproduction artifacts

- Per-interval electron-instability classification.
- Threshold-margin diagnostic.

---

## 4. Adapter / runtime notes (optional examples)

- PLUME, NHDS, ALPS support electron species; example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[whistler-young-solar-wind-statistics-2024]]**: validate local-instability hypothesis by overlaying predicted γ_max>0 intervals on whistler-wave detection catalog.
- **Composability with [[suprathermal-electron-whistler-scattering-2024]]**: closes the loop — predicted instability vs observed strahl-broadening.
- **Open hypothesis**: Are observed whistler-wave intervals predominantly local-instability driven or convected remnants?

---

## Links

- arXiv: https://arxiv.org/abs/2206.10403
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2206.10403`

## Skill graph

- [[whistler-young-solar-wind-statistics-2024]]
- [[suprathermal-electron-whistler-scattering-2024]]
- [[klein-2018-multispecies-stability-anisotropy]]

