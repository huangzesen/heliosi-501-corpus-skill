---
name: wave-particle-equilibria-heavy-ions-2026
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2603.22613"
  venue: "ApJ accepted (Mar 2026)"
---

# wave-particle-equilibria-heavy-ions-2026

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the equilibrium derivation or the
> hybrid-PIC verification end-to-end. Treat Layer 2 as `pending`;
> do not present this skill as workflow-ready or use it as the basis
> for an experiment without first reading Villarroel-Sepúlveda et al.
> (2026), arXiv:2603.22613.


A paper-skill compiled from Villarroel-Sepúlveda, Verscharen, Moya,
López & Klein (2026), ApJ accepted (arXiv:2603.22613).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict equilibrium VDFs of heavy ions under wave-particle
  interaction in weakly collisional space plasmas.
- Decide whether observed heavy-ion T_⊥/T_∥ (or higher-order
  moments) is consistent with the wave-particle equilibrium
  prediction for the inferred local wave spectrum.
- Provide the null hypothesis for "extreme-heating" diagnostics:
  a heavy-ion VDF that *departs* from F_eq is by definition out
  of equilibrium with the wave spectrum and requires another
  driver.

### When NOT to use it

- Single-instability action without an equilibrium framework
  (use the dedicated dispersion skills).
- Collisional or transition-collisional regimes where the
  weak-collision assumption fails.
- Coronal regions where wave-spectrum input is not
  observationally constrained.

### Claim boundary

Wave-particle-equilibrium theory for heavy ions in weakly
collisional plasmas, with hybrid-PIC verification for a
representative set of (wave spectrum, heavy-ion species, β)
combinations. The claim is bounded to (a) the species set
considered (typically He^2+, O^{6+}, Fe), (b) the wave-spectrum
shapes scanned by the paper, and (c) the weak-collision regime.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Heavy-ion VDFs in weakly collisional space plasmas settle into
wave-particle equilibria F_eq(v) specified by the local wave
spectrum and species charge / mass. Observed solar-wind heavy
ions in Alfvénic streams sit on this F_eq locus within the
paper's stated bars; intervals that depart from F_eq are
diagnostic of either non-Alfvénic compositional input or of an
additional driver.

### 2.2 Equations / method

- Quasi-linear flux closure on the heavy-ion VDF in pitch-angle
  / energy space.
- F_eq(v) defined as the steady solution of the quasi-linear
  diffusion equation under the prescribed wave spectrum.
- T_⊥/T_∥ and higher-order moments computed from F_eq for
  comparison with in-situ VDFs.
- Hybrid-PIC verification: initialise the heavy-ion species away
  from F_eq and integrate forward; the system should relax to
  F_eq within a paper-stated number of cyclotron times.

### 2.3 Data assumptions

- A prescribed wave spectrum at the resonant frequency band of
  the species under consideration (from observed δB(f) if
  possible).
- Heavy-ion VDF measurement at adequate energy / angular
  resolution.
- Hybrid-PIC code with heavy-ion species support for the
  verification step.

### 2.4 Failure modes (skill memory)

- **Wave-spectrum prescription** dominates F_eq; small changes
  in the spectrum shape produce large changes in the equilibrium
  T_⊥/T_∥.
- **Collisionality residual** breaks the weak-collision
  assumption; transition-collisional plasmas may sit between
  F_eq and a Maxwellian.
- **Species charge / mass mis-specification** mis-locates the
  resonance and therefore mis-locates F_eq in velocity space.
- **VDF measurement resolution** can smear the F_eq signature
  past detectability.

### 2.5 Figure / numerical targets

- F_eq(v) curves per heavy-ion species under the paper's
  reference wave spectrum.
- T_⊥/T_∥ for each species recovered to within stated bars
  (TODO_verify_with_full_text for exact tolerance).
- Hybrid run relaxes to F_eq within a paper-stated number of
  Ω_p^{-1}.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-WAVE-SPECTRUM**: prescribe a wave spectrum P_w(f, k) at
  the resonant band for the species of interest.
- **C-EQUILIBRIUM-VDF**: solve the quasi-linear closure for
  F_eq(v) under the prescribed spectrum.
- **C-HEAVY-ION-VDF-LOAD**: load the measured heavy-ion VDF
  for an interval (from SolO SWA HIS or PSP SWEAP α-heavy mode).
- **C-MOMENT-COMPARE**: emit T_⊥/T_∥ and selected higher-order
  moments computed from F_eq and from the measured VDF;
  return the residual.
- **C-HYBRID-HEAVY-ION-VERIFY** (optional): initialise the
  hybrid code away from F_eq and verify relaxation.

### 3.2 Procedure

1. C-WAVE-SPECTRUM: prescribe P_w(f, k) at the resonant band.
2. C-EQUILIBRIUM-VDF: solve for F_eq(v) for each species of
   interest.
3. C-HEAVY-ION-VDF-LOAD: load the observed VDF for the same
   interval.
4. C-MOMENT-COMPARE: emit (T_⊥/T_∥)_eq, (T_⊥/T_∥)_obs and the
   residual.
5. Persist (interval_id, species, residual, on_equilibrium_flag)
   for downstream consumers.
6. (Optional) C-HYBRID-HEAVY-ION-VERIFY at one (spectrum,
   species, β) point to confirm relaxation.

### 3.3 Minimum reproduction artifacts

- F_eq(v) curves per heavy-ion species.
- T_⊥/T_∥ comparison table on a labelled SolO SWA HIS subset.
- Hybrid-relaxation figure for one reference case.

### Validation target

A reproduction of this skill is considered honest when:

- The F_eq(v) curves reproduce the paper's reference-case
  figure within ≲ 20 % in the peak amplitude.
- T_⊥/T_∥ recovered on the paper's labelled set sits within the
  paper-stated bars (TODO_verify_with_full_text for exact
  tolerance).
- The hybrid relaxation lands on F_eq within a paper-stated
  number of Ω_p^{-1} (qualitative check if the exact number is
  not yet verified).

---

## 4. Adapter / runtime notes (optional examples)

- ALPS / PLUME / NHDS-style quasi-linear closures are example
  Layer-3 bindings for C-EQUILIBRIUM-VDF; none are shipped here.
- dHybridR / CAMELIA / PEGASUS with heavy-ion species support
  are example Layer-3 bindings for the optional verification.
- SolO SWA HIS / PSP SWEAP α-heavy pipelines are example
  Layer-3 bindings for C-HEAVY-ION-VDF-LOAD.

---

## 5. Research-generation affordance

- **Composability with [[extreme-minor-ion-heating-imbalanced-turbulence-2024]]**:
  heavy ions out of F_eq correspond to the extreme-heating
  regime. Combining the two contracts produces a dichotomy
  diagnostic (in-equilibrium vs extreme-heating) that neither
  paper individually supplies.
- **Composability with [[klein-2018-multispecies-stability-anisotropy]]**:
  the F_eq locus and the multispecies stability locus are
  related but not identical; intervals that fall in the gap are
  scientifically interesting.
- **Open hypothesis**: Heavy-ion VDFs in well-developed
  Alfvénic streams sit on F_eq, while those in compressive /
  shock-adjacent intervals do not — the dichotomy is
  observable in the SWA HIS archive.
- **Gap**: The framework assumes a *prescribed* wave spectrum;
  the self-consistent back-reaction of heavy-ion absorption on
  the spectrum is not closed.
- **Tension with parallel-only quasi-linear closures**:
  parallel-only closures predict a different F_eq for the same
  spectrum; the discriminator is the angular structure of the
  heavy-ion VDF.

---

## Links

- arXiv: https://arxiv.org/abs/2603.22613
- DOI: TODO_verify_with_full_text (ApJ-accepted preprint)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2603.22613`

## Skill graph

- [[extreme-minor-ion-heating-imbalanced-turbulence-2024]]
- [[klein-2018-multispecies-stability-anisotropy]]
