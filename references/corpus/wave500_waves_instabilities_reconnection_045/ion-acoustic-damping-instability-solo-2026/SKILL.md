---
name: ion-acoustic-damping-instability-solo-2026
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2604.14311"
  venue: "ApJ accepted (Apr 2026)"
---

# ion-acoustic-damping-instability-solo-2026

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the
> linear-Vlasov solver, T_e estimation pipeline, or event
> classification end-to-end. Treat Layer 2 as `pending`; do not present
> this skill as workflow-ready or use it as the basis for an experiment
> without first reading Ran, Verscharen, Coburn et al. (2026),
> arXiv:2604.14311. The authors note that their code is released under
> MIT — see the paper for the repository URL.


A paper-skill compiled from Ran, Verscharen, Coburn, Nicolaou,
Ioannou, Wu, Liu, Klein & Owen (2026), ApJ accepted
(arXiv:2604.14311).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Decide whether observed Solar Orbiter ion-acoustic-wave (IAW)
  intervals are linearly damped or unstable.
- Quantify (T_e/T_i)-dependent damping / growth rates for IA
  modes from in-situ moments.
- Provide a linear-theory label for ML-detected modulated-IAW
  intervals so that ML training data carry a physical class.

### When NOT to use it

- ML-only detection of modulated IAWs — that is the job of
  [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]];
  this skill provides the *label*, not the *detector*.
- Energy-transfer-direction analysis from VDF signatures — see
  [[ion-acoustic-velocity-space-signatures-2026]].
- Coronal regimes where T_e and T_i cannot be reliably
  separated.

### Claim boundary

Event-level analysis of SolO RPW-identified IAW intervals,
classified into damped (γ < 0) vs unstable (γ > 0) via the
linear-Vlasov dispersion using SWA-PAS + SWA-EAS-derived
(T_e, T_i, drift). The claim is bounded to (a) the SolO event
sample considered, (b) the linear regime, and (c) the moment
quality afforded by SWA-PAS / SWA-EAS during the analysed
intervals.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Ion-acoustic-wave intervals observed by Solar Orbiter separate
into damped vs unstable subpopulations with a paper-specified
(T_e/T_i) threshold; the linear-Vlasov dispersion with measured
(T_e, T_i, drift) reproduces the population boundary.

### 2.2 Equations / method

- IA dispersion ω^2 = k^2 c_s^2 / (1 + k^2 λ_D^2), with
  c_s = √((T_e + 3T_i)/m_i).
- Landau damping rate γ ∝ −exp(−ω^2 / (2 k^2 v_{th,e}^2))
  modified by T_e/T_i; instability requires sufficient
  electron drift v_drift > v_{th,i}.
- Full linear-Vlasov solver with finite k λ_D for the IA
  branch.
- Population classification: per-interval sign of γ.

### 2.3 Data assumptions

- SolO RPW Level-2 spectral products to identify the IAW
  intervals.
- SolO SWA-PAS proton moments and SWA-EAS electron moments
  with adequate cadence.
- Linear-Vlasov solver capable of finite k λ_D.

### 2.4 Failure modes (skill memory)

- **T_e estimation** systematics dominate γ — SWA-EAS
  calibration / spacecraft potential corrections shift the
  classification.
- **Drift estimation** noise: γ depends on v_drift / v_{th,i};
  small noise at small drifts changes the sign.
- **k λ_D** is interval-dependent; assuming k λ_D « 1 is not
  always valid and changes the dispersion.
- **VDF non-thermality**: the simple bi-Maxwellian closure may
  mis-predict γ when the electron or ion VDF carries beams.

### 2.5 Figure / numerical targets

- Damped / unstable population split at the paper-stated
  (T_e/T_i) threshold (TODO_verify_with_full_text for exact
  value).
- A γ(T_e/T_i, drift) heat-map reproducing the paper's
  reference figure.
- Per-event tags on the paper's overlap subset reproduced to
  within ≲ 5 % count discrepancy.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-SOLO-RPW-IAW**: load RPW Level-2 spectral data
  and emit IAW interval candidates.
- **C-FETCH-SOLO-SWA-MOMENTS**: load SWA-PAS proton moments
  and SWA-EAS electron moments aligned to the IAW windows.
- **C-LIN-VLASOV-IA**: solve the IA-branch dispersion and
  return γ(T_e, T_i, v_drift, k λ_D).
- **C-IAW-EVENT-CLASSIFY**: emit (damped | unstable | marginal)
  per interval based on γ sign and a stated marginal band.

### 3.2 Procedure

1. C-FETCH-SOLO-RPW-IAW: identify IAW interval candidates.
2. C-FETCH-SOLO-SWA-MOMENTS: aligned (T_e, T_i, v_drift) per
   interval.
3. C-LIN-VLASOV-IA: emit γ.
4. C-IAW-EVENT-CLASSIFY: emit per-interval class and an
   uncertainty band reflecting T_e / drift estimation noise.
5. Aggregate: report damped / unstable counts vs (T_e/T_i)
   bin and recover the paper's threshold.

### 3.3 Minimum reproduction artifacts

- Per-interval table with (interval_id, T_e/T_i, drift, γ,
  class, uncertainty band).
- (T_e/T_i)-binned damped vs unstable population histogram.
- γ heat-map reproducing the paper's reference figure shape.

### Validation target

A reproduction of this skill is considered honest when:

- The damped vs unstable population split sits at the paper-
  stated (T_e/T_i) threshold (TODO_verify_with_full_text for
  the exact threshold).
- Per-event tags on the paper's overlap subset match within
  ≲ 5 % count discrepancy (a stronger check requires the
  paper's released code, which the authors note is MIT-
  licensed).
- The γ heat-map reproduces the paper figure shape (sign
  pattern in the (T_e/T_i, drift) plane).

---

## 4. Adapter / runtime notes (optional examples)

- The paper's released code (URL TODO_verify_with_full_text;
  MIT-licensed per arXiv comments) is the canonical Layer-3
  binding for C-LIN-VLASOV-IA.
- SolO RPW LFR/TDS pipelines (e.g. solo-rpw via solar-orbiter-
  python, or community SunPy plugins) are example Layer-3
  bindings for C-FETCH-SOLO-RPW-IAW.
- SolO SWA-PAS / EAS Level-2 loaders (e.g. swapy / cdaspy)
  are example Layer-3 bindings for the moment fetch.

---

## 5. Research-generation affordance

- **Composability with [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]**:
  ML-detected events labelled with linear-theory damped /
  unstable classes produce a labelled training set that
  neither paper individually supplies.
- **Composability with [[ion-acoustic-velocity-space-signatures-2026]]**:
  cross-validate the energy-transfer direction inferred from
  VDF signatures against the γ sign from this skill; a clean
  agreement is a strong, multi-method confirmation.
- **Tension with steady-state IAW interpretations**: marginal-γ
  events are a population in their own right and may resolve
  the long-standing question of whether IAWs are predominantly
  damped or unstable in the solar wind.
- **Open hypothesis**: The damped / unstable fraction varies
  with stream type (Alfvénic / non-Alfvénic / CIR-adjacent);
  the test is straightforward against any existing stream
  classifier.
- **Gap**: T_e estimation systematics produce a residual that
  is not closed by this paper; an independent T_e constraint
  (e.g. from RPW quasi-thermal noise) would tighten the
  population boundary.

---

## Links

- arXiv: https://arxiv.org/abs/2604.14311
- DOI: TODO_verify_with_full_text (ApJ-accepted preprint)
- Code: MIT-licensed (URL TODO_verify_with_full_text)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2604.14311`

## Skill graph

- [[paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml]]
- [[ion-acoustic-velocity-space-signatures-2026]]
