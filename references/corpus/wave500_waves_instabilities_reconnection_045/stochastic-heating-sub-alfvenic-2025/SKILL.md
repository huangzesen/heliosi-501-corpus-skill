---
name: stochastic-heating-sub-alfvenic-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2509.20654"
  venue: "arXiv preprint (Sep 2025)"
---

# stochastic-heating-sub-alfvenic-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the gyroscale-
> amplitude extrapolation, the (c_1, c_2) regime guards, or the
> heating-budget comparison end-to-end. Treat Layer 2 as `pending`;
> do not present this skill as workflow-ready or use it as the basis
> for an experiment without first reading Bowen, Ervin, Mallet,
> Chandran et al. (2025), arXiv:2509.20654, *and* consulting the
> upstream analytic closure [[chandran-2010-stochastic-heating-perp-alfven]].


A paper-skill compiled from Bowen, Ervin, Mallet, Chandran,
Sioulas, Isenberg, Bale, Squire, Klein & Pezzi (2025),
arXiv:2509.20654.

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Quantify stochastic-heating rates in PSP sub-Alfvénic
  intervals.
- Decide whether stochastic heating closes the perpendicular
  heating budget below the Alfvén surface.
- Provide a Q_⊥(r) profile that downstream cycle / cascade
  budget skills can subtract from to isolate other heating
  channels.

### When NOT to use it

- Above-Alfvén-surface intervals — the closure was derived for
  randomly-phased AW turbulence with σ_c ~ 0, and at large
  heliocentric distances σ_c drops and the regime shifts.
- Cyclotron-resonant channel — see
  [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]] and
  [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]].
- Intervals where ε falls outside the Chandran-2010 calibration
  band [0.05, 0.5]; the closure is then an extrapolation.

### Claim boundary

Per-interval Q_⊥ estimate from observed δv_⊥(ρ_i) in sub-Alfvénic
PSP intervals using the Chandran-2010 stochastic-heating
prescription. The claim is bounded to (a) the M_A < 1 intervals
identified in the paper, (b) the Chandran-2010 (c_1, c_2)
calibration, and (c) the ε ∈ [0.05, 0.5] band.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Stochastic-heating estimates in PSP sub-Alfvénic intervals
account for a paper-stated fraction of the inferred perpendicular
heating budget within stated bars; the closure-budget agreement
is what makes stochastic heating the leading-candidate
perpendicular-heating channel in the M_A < 1 regime.

### 2.2 Equations / method

- M_A diagnostic: M_A = v_sw / v_A < 1.
- ε = δv_⊥(ρ_i) / v_⊥,p (where v_⊥,p ≈ v_th,p in the
  inertial regime).
- Q_⊥ closure (Chandran 2010): Q_⊥ ≈ c_1 (δv_⊥)^3 / ρ_i
  · exp(−c_2/ε), with (c_1, c_2) = (0.75, 0.34) from the
  Chandran-2010 calibration.
- Heating budget: independent estimate of inferred Q_⊥(r)
  from observed T_⊥(r) evolution along the encounter, or
  from the cascade rate ε_T ≈ ρ̄ (δv_⊥)^3 / L_⊥.
- Closure fraction f_closure = Q_⊥ / Q_⊥_inferred per interval.

### 2.3 Data assumptions

- PSP MAG + plasma at adequate cadence to resolve the gyroscale
  spectrum in sub-Alfvénic intervals.
- Density estimate (from SPC, QTN, or SPAN-i) for ρ_i.
- A defensible gyroscale-amplitude extrapolation from the
  available spectrum.

### 2.4 Failure modes (skill memory)

- **(c_1, c_2) calibration** is for balanced AW turbulence;
  sub-Alfvénic intervals often have σ_c that is non-zero, so
  the closure is out-of-calibration in those regions.
- **v_⊥ baseline definition** matters: using v_th,p vs v_⊥,p vs
  total v_th shifts ε.
- **Gyroscale-amplitude reconstruction**: extrapolating from
  the inertial-range spectrum to ρ_i requires choosing a
  slope, and this is a load-bearing systematic.
- **Density estimate**: SPC saturation in some sub-Alfvénic
  intervals can mis-estimate ρ_i.

### 2.5 Figure / numerical targets

- Q_⊥(r) curve over the sub-Alfvénic interval reproducing the
  paper's reference-figure shape.
- Closure fraction f_closure within the paper-stated band
  (TODO_verify_with_full_text for exact fraction).
- Reported out-of-calibration ε fraction.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP-SUB-ALFVENIC**: load MAG + plasma over the
  sub-Alfvénic intervals identified in the paper.
- **C-SUB-ALFVENIC-FLAG**: emit M_A and the M_A < 1 flag per
  interval.
- **C-GYROSCALE-AMPLITUDE**: extrapolate the spectrum to ρ_i
  and emit δv_⊥(ρ_i) with the assumed slope reported.
- **C-CHANDRAN-Q-PERP**: evaluate the Chandran-2010 closure
  given (δv_⊥, v_⊥,p, ρ_i). (This is the same contract that
  [[chandran-2010-stochastic-heating-perp-alfven]] exposes.)
- **C-HEATING-BUDGET**: emit independent Q_⊥_inferred (cascade
  rate or T_⊥(r)-evolution-based) for the comparison.

### 3.2 Procedure

1. C-FETCH-PSP-SUB-ALFVENIC over the encounter window.
2. C-SUB-ALFVENIC-FLAG: keep only M_A < 1 intervals.
3. C-GYROSCALE-AMPLITUDE per interval.
4. C-CHANDRAN-Q-PERP: emit Q_⊥ and the ε out-of-calibration
   flag.
5. C-HEATING-BUDGET: emit Q_⊥_inferred.
6. Emit f_closure = Q_⊥ / Q_⊥_inferred per interval; aggregate
   over the encounter sub-Alfvénic window.

### 3.3 Minimum reproduction artifacts

- Q_⊥(r) figure reproducing the paper's reference plot in the
  sub-Alfvénic regime.
- Histogram of f_closure on the analysed intervals.
- Reported out-of-calibration ε fraction.

### Validation target

A reproduction of this skill is considered honest when:

- f_closure on the labelled sub-Alfvénic intervals sits within
  the paper-stated band (TODO_verify_with_full_text for the
  exact fraction).
- The Q_⊥(r) reference figure shape is reproduced (decreasing
  Q_⊥ with heliocentric distance in the sub-Alfvénic window).
- The out-of-calibration ε fraction is explicitly reported and
  is not silently absorbed.

---

## 4. Adapter / runtime notes (optional examples)

- PSP MAG + SPAN-i pipelines (pyspedas-PSP, sunpy-PSP plugins,
  or LingTai's xhelio-spice-adjacent MAG/SPC loaders) are
  example Layer-3 bindings for C-FETCH-PSP-SUB-ALFVENIC.
- The Chandran-2010 closure is a one-liner once the inputs are
  assembled.
- The heating-budget capability is realisable from a fit to
  T_⊥(r) or from any cascade-rate estimator on the same
  intervals.

---

## 5. Research-generation affordance

- **Composability with [[chandran-2010-stochastic-heating-perp-alfven]]**:
  provides the analytic foundation; this skill is its sub-
  Alfvénic in-situ application. Discrepancies are interpretable
  as a regime-extrapolation residual rather than a closure
  failure.
- **Composability with [[kasper-2021-psp-enters-magnetically-dominated-corona]]**:
  ties stochastic heating to the first M_A < 1 interval.
- **Tension with [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]**:
  the perpendicular-channel claim of this skill and the
  cyclotron-channel claim of Bowen 2024 jointly partition the
  heating budget; which channel dominates in sub-Alfvénic
  conditions is the load-bearing open question.
- **Open hypothesis**: Stochastic heating accounts for the
  near-Sun T_⊥ enhancement that the cascade-only budget under-
  predicts.
- **Gap**: σ_c-dependent re-calibration of (c_1, c_2) is not
  done; in highly imbalanced sub-Alfvénic intervals the
  closure is uncontrolled.

---

## Links

- arXiv: https://arxiv.org/abs/2509.20654
- DOI: TODO_verify_with_full_text (preprint as of Sep 2025)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2509.20654`

## Skill graph

- [[chandran-2010-stochastic-heating-perp-alfven]]
- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]
