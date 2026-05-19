---
name: bianco-2025-alfven-wave-proton-beam-evolution-hebox
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# bianco-2025-alfven-wave-proton-beam-evolution-hebox

A paper-skill compiled from J. S. Bianco, A. Tenerani, C. Gonzalez et al. 2025 (TODO_verify_journal; arXiv:2511.02940).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the radial evolution of proton-beam drift speed and core-to-beam density ratio from 0.3 to 1.5 AU.
- Decide whether observed beam-drift quenching is consistent with kinetic-instability regulation rather than expansion alone.

### When NOT to use it

- Mechanisms producing the initial Alfvén-wave amplitude — see [[saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun]].
- Beam–core thermal-pressure anisotropy without an Alfvén-wave driver.

### Claim boundary

1D hybrid expanding-box simulations covering 0.3–1.5 AU. Initial conditions chosen to represent Helios states at 0.3 AU including an amplitude-modulated Alfvén wave. Comparison against in-situ data is qualitative.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Amplitude-modulated Alfvén waves nonlinearly drive a field-aligned proton beam. Hybrid runs reproduce the observed mean radial evolution of the drift v_d and core-to-beam density ratio, indicating kinetic-instability regulation in addition to expansion.

### 2.2 Equations / method

- 1D hybrid Vlasov–PIC equations with expanding-box terms.
- Beam drift v_d as the first moment of the beam-population VDF.
- Core-to-beam density ratio from VDF segmentation.
- Linear stability thresholds (e.g., ion/ion-cyclotron) as diagnostics.

### 2.3 Data assumptions

- 1D HEB code with amplitude-modulated Alfvén-wave initial condition.
- VDF segmentation algorithm for core/beam separation.
- Helios-like initial state at 0.3 AU.

### 2.4 Failure modes (skill memory)

- **1D geometry** misses oblique instabilities — flag scope.
- **Beam-core segmentation threshold** biases v_d / density.
- **Initial amplitude** of the modulated AW sets the saturated beam strength.
- **Expanding-box assumption** breaks down at very large r.

### 2.5 Figure / numerical targets

- Mean v_d(r) profile within stated error bars (TODO verify exact).
- Core/beam density ratio radial trend.
- Onset of instability-marginal-stability state at the right r.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HEB-1D**: 1D hybrid expanding-box code.
- **C-AW-INIT**: amplitude-modulated Alfvén-wave initial condition.
- **C-VDF-SEGMENT**: core/beam segmentation of the ion VDF.
- **C-STABILITY-LINEAR**: linear-Vlasov ion/ion-instability checker.

### 3.2 Procedure

1. C-AW-INIT at 0.3 AU with chosen amplitude/modulation.
2. C-HEB-1D: integrate to 1.5 AU.
3. C-VDF-SEGMENT at output snapshots.
4. Track v_d(r), density ratio.
5. C-STABILITY-LINEAR: confirm marginal-stability state.

### 3.3 Minimum reproduction artifacts

- v_d(r) and density-ratio time series.
- VDF snapshots at chosen r.
- Marginal-stability diagnostic curves.

---

## 4. Adapter / runtime notes (optional examples)

- Any 1D HEB-capable hybrid code satisfies the contracts.
- CAMELIA, dHybridR are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**: predict in-situ ion-scale-wave occurrence locked to beam-drift trajectories; test against PSP catalog.
- **Composability with [[klein-2018-multispecies-stability-anisotropy]]**: pass instantaneous HEB VDF into the linear-Vlasov stability checker — verify whether the run lives on the marginal-stability surface.
- **Open hypothesis**: Are non-instability-quenched beam states observed in PSP (high v_d > threshold) signatures of inactive AW driver?
- **Methodological experiment**: vary the amplitude-modulation depth and quantify how strongly v_d(r) reorganizes.

---

## Links

- arXiv: https://arxiv.org/abs/2511.02940
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2511.02940`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[klein-2018-multispecies-stability-anisotropy]]
- [[saguchi-2026-alfven-pdi-temperature-anisotropy-near-sun]]

