---
name: whistler-young-solar-wind-statistics-2024
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# whistler-young-solar-wind-statistics-2024

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2024 (TODO_verify_journal; arXiv:2408.00736).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Catalog whistler-wave amplitude and propagation direction in PSP young-solar-wind intervals.
- Decide whether sunward vs anti-sunward whistler populations dominate at given r.

### When NOT to use it

- Electron-driver mechanism — see [[electron-driven-instabilities-solar-wind-2022]].
- Whistler–electron scattering rates — see [[suprathermal-electron-whistler-scattering-2024]].

### Claim boundary

Statistical catalog from PSP FIELDS waveform-snapshot data over a chosen radial range. Polarization analysis with Singular-Value-Decomposition or analogue identifies propagation sign.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Whistler-wave amplitude distribution in PSP young-solar-wind shows paper-quantified statistics; sunward vs anti-sunward fractions vary with r.

### 2.2 Equations / method

- Magnetic spectrogram in the 0.05–0.5 f_ce band.
- SVD polarization analysis for k-direction.
- Amplitude PDF binned by r.

### 2.3 Data assumptions

- PSP FIELDS waveform / spectral burst data.
- Magnetic-field background for f_ce.

### 2.4 Failure modes (skill memory)

- **Burst sampling bias** — burst triggers privilege strong events.
- **SVD ambiguity** at low SNR.
- **f_ce band selection** truncates relevant events.

### 2.5 Figure / numerical targets

- Amplitude PDF reproduced (TODO verify).
- Sunward/anti-sunward ratio vs r reproduced.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP-FIELDS-WAVE**: high-cadence waveform/spectrum.
- **C-POL-SVD**: polarization analysis.
- **C-AMP-PDF**: amplitude PDF estimator binned by r.

### 3.2 Procedure

1. C-FETCH-PSP-FIELDS-WAVE.
2. C-POL-SVD per event.
3. C-AMP-PDF aggregation.

### 3.3 Minimum reproduction artifacts

- Whistler-event catalog with amplitude and k-direction.
- Amplitude PDF per r bin.

---

## 4. Adapter / runtime notes (optional examples)

- PySPEDAS PSP-FIELDS bindings are example Layer-3 adapters.

---

## 5. Research-generation affordance

- **Composability with [[electron-driven-instabilities-solar-wind-2022]]**: where local γ_max>0 predicted, expect anti-sunward whistler at f_ce-fraction band.
- **Composability with [[suprathermal-electron-whistler-scattering-2024]]**: feed amplitude statistics into scattering-rate estimate.
- **Open hypothesis**: Are sunward-propagating whistlers signatures of reflection at V_A gradients or of local generation?

---

## Links

- arXiv: https://arxiv.org/abs/2408.00736
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2408.00736`

## Skill graph

- [[electron-driven-instabilities-solar-wind-2022]]
- [[suprathermal-electron-whistler-scattering-2024]]

