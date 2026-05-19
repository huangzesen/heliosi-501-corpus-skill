# expansion-instability-young-solar-wind-thermo-2026

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2026 (TODO_verify_journal; arXiv:2603.25443).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict combined effect of expansion + kinetic instabilities on T_⊥/T_∥(r) in the young solar wind.
- Decide whether observed PSP near-Sun anisotropy is regulated by instabilities, expansion, or both.

### When NOT to use it

- Single-instability-only models — see [[firehose-thermodynamics-high-beta-2025]].
- Pure adiabatic CGL with no instability.

### Claim boundary

Hybrid expanding-box simulations covering near-Sun radii. Anisotropy thresholds from cyclotron, mirror, and firehose instabilities applied. Comparison against PSP encounters is qualitative.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Joint expansion + kinetic-instability regulation explains the observed bounded (β_∥, T_⊥/T_∥) distribution in the young solar wind; neither mechanism alone suffices.

### 2.2 Equations / method

- CGL adiabatic invariants in expanding-box geometry.
- Linear thresholds: cyclotron (T_⊥/T_∥ > 1 + a/β_∥^b), mirror, firehose (T_⊥/T_∥ < 1 − 2/β_∥).
- Marginal-stability hugging.

### 2.3 Data assumptions

- 1D hybrid expanding-box code.
- Initial VDF at near-Sun radius.
- PSP encounter data for comparison.

### 2.4 Failure modes (skill memory)

- **1D geometry** misses oblique-mirror branches.
- **Initial VDF** sets which instability is hit first.
- **Expansion rate** mis-calibration shifts predicted (β_∥, ξ) trajectories.

### 2.5 Figure / numerical targets

- (β_∥, T_⊥/T_∥) trajectories vs r match PSP envelope (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HEB-HYBRID**: hybrid expanding-box code.
- **C-INSTAB-THRESH**: cyclotron / mirror / firehose threshold checker.
- **C-PSP-COMPARE**: PSP (β_∥, ξ) envelope loader.

### 3.2 Procedure

1. C-HEB-HYBRID: integrate from near-Sun to chosen r_max.
2. C-INSTAB-THRESH at each snapshot.
3. C-PSP-COMPARE: overlay trajectories onto PSP envelope.

### 3.3 Minimum reproduction artifacts

- (β_∥, ξ)(r) trajectories.
- Threshold-hit log per instability.

---

## 4. Adapter / runtime notes (optional examples)

- Any hybrid expanding-box code suffices.

---

## 5. Research-generation affordance

- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**: where simulation hits cyclotron threshold, predict in-situ wave occurrence.
- **Composability with [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]**: combine beam regulation with anisotropy regulation.
- **Open hypothesis**: Are PSP intervals far from the marginal-stability envelope intervals where expansion timescale beats ν_eff?

---

## Links

- arXiv: https://arxiv.org/abs/2603.25443
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2603.25443`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]
- [[firehose-thermodynamics-high-beta-2025]]

