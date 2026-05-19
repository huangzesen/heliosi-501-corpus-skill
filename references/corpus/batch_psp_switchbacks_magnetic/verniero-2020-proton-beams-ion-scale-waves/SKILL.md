# verniero-2020-proton-beams-ion-scale-waves

A paper-skill compiled from Verniero, Larson, Livi, Rahmati, et al.
2020 (ApJS 248, 5; doi:10.3847/1538-4365/ab86af).

Paper-skills are **harness-agnostic**: they describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (Claude Code, LingTai, Codex, a researcher) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Link ion-scale wave activity in PSP to a proton-beam free-energy
  source.
- Validate a `beam-driven` flag upstream of turbulence-dissipation or
  wave-spectrum skills.
- Identify candidate kinetic-instability events for further VDF /
  dispersion analysis.

### When NOT to use it

- *Electron*-scale instabilities or non-resonant wave growth.
- Wave events without simultaneous 3D VDF coverage.

### Claim boundary

Using PSP SPAN-I 3D VDFs and FIELDS waveforms in selected intervals,
the paper identifies coincident proton-beam populations and ion-scale
wave power, and uses linear-Vlasov stability analysis to attribute
ion-cyclotron / magnetosonic instability as the consistent driver.
Bounded to the analysed intervals; not a population-level claim that
all ion-scale waves are beam-driven.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

In PSP intervals with elevated ion-scale wave power, 3D SPAN-I proton
VDFs exhibit core-plus-beam structure with free energy sufficient to
drive ion-cyclotron / magnetosonic modes per linear-Vlasov analysis,
consistent with observed wave polarisation and frequency content.

### 2.2 Equations / method

- Bi-Maxwellian (or non-Maxwellian) core + beam VDF fit.
- Linear-Vlasov dispersion relation evaluated at local plasma
  parameters (`β`, `θ_kB`, species ratios).
- Match between predicted unstable mode (frequency, polarisation,
  growth rate) and observed wave spectrum / polarisation.

### 2.3 Data assumptions

- 3D proton VDF at cadence sufficient to resolve beam-core separation.
- High-cadence vector `B` + AC/DC wave spectra covering the proton-
  cyclotron band.
- Local plasma parameters (`β`, `n`, `θ_kB`) at matching cadence.

### 2.4 Failure modes (skill memory)

- **SPAN-I FOV coverage.** Beam may be outside the FOV at certain
  attitudes — beam absence can be geometric, not physical.
- **Fit method bias.** Partial-moment fits bias the beam drift.
- **`θ_kB` uncertainty** is large when `δB/B` is small (single-
  spacecraft estimator).
- **Solver choice** (PLUME, NHDS, etc.) changes finite-Larmor-radius
  and relativistic handling — cite solver + version.
- **Mode misidentification.** Oblique whistlers can leak into the
  ion-cyclotron band; cross-check handedness.

### 2.5 Figure / numerical targets

- Reproduce one named beam-plus-wave interval (TODO verify list).
- Positive linear growth rate at the observed frequency band.
- Predicted polarisation handedness matches observed.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-VDF**: 3D proton VDF over a chosen interval.
- **C-FETCH-WAVE**: AC/DC magnetic-field spectra covering the proton-
  cyclotron band.
- **C-FETCH-MAG / C-FETCH-BULK**: vector `B` and bulk + density
  moments at matching cadence.
- **C-FIT-VDF**: fit a parametric core + beam VDF to a 3D distribution.
- **C-VLASOV**: evaluate the linear-Vlasov dispersion relation given
  species parameters and `θ_kB`.
- **C-VERDICT**: classify an interval as {driven, ambiguous, not
  driven} from the agreement of predicted vs. observed mode
  properties.

### 3.2 Procedure

1. Identify candidate intervals via C-FETCH-WAVE; threshold on band-
   integrated wave power.
2. C-FETCH-VDF + C-FETCH-MAG + C-FETCH-BULK over the same window.
3. C-FIT-VDF for core + beam parameters; record FOV diagnostic.
4. C-VLASOV at the local plasma state; record growth rate +
   polarisation per mode.
5. Compare predicted vs. observed mode characteristics; apply
   C-VERDICT.
6. Aggregate over the analysed intervals.

### 3.3 Minimum reproduction artifacts

- Per-interval `vdf_fit.json` with FOV diagnostic.
- Dispersion-curve overlay against observed spectrum.
- Verdict CSV with explicit solver, fit method, and `θ_kB` estimator
  recorded.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with VDF I/O + a linear-Vlasov solver (`PLUME`, `NHDS`,
  `LEOPARD`) can satisfy the contracts.
- LingTai HelioSI may bind C-VLASOV to an internal solver-wrapper
  skill — this is one possible binding, not a requirement.

---

## 5. Research-generation affordance

- **Composability** with [[shankarappa-2025-free-energy-sources-ion-scale-waves]]
  *(future skill, not yet in corpus)*: extend the per-interval verdict
  to a mission-wide statistic of beam-driven vs. anisotropy-driven
  vs. unattributed ion-scale wave events.
- **Open hypothesis**: the fraction of beam-driven events vs.
  heliocentric distance is sparsely characterised; a systematic scan
  across encounters using this protocol is a natural next paper.
- **Cross-tension with turbulence-dissipation skills**: ion-scale wave
  power is also a candidate dissipation channel; combining this
  paper-skill's verdict with cascade-rate or PSD-break diagnostics
  tests whether beam-driven events systematically alter inferred
  dissipation rates.
- **Methodological experiment**: rerun C-VLASOV with non-Maxwellian
  VDF distributions (κ-distribution beams) and quantify how the
  verdict changes — the paper uses a bi-Maxwellian fit and the
  sensitivity is unreported.

---

## Links

- DOI: https://doi.org/10.3847/1538-4365/ab86af
- arXiv: TODO verify
- Code: TODO verify (PLUME / NHDS public solvers exist)
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.7

## Skill graph

- [[verniero-2023-proton-alpha-instabilities-ion-cyclotron]] *(future
  / sibling)* — proton + alpha driven instabilities, extension of
  this protocol.
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]] —
  Alfvén-Mach-number context affects relevant β regime.
- [[bowen-2024-cyclotron-resonance]] *(turbulence-heating batch)* —
  cyclotron-band wave dissipation downstream.
