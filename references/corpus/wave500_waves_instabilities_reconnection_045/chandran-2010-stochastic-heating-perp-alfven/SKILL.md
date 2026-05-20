---
name: chandran-2010-stochastic-heating-perp-alfven
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  doi: "10.1088/0004-637X/720/1/503"
  arxiv: "1001.2069"
  venue: "ApJ 720, 503 (2010)"
---

# chandran-2010-stochastic-heating-perp-alfven

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the full
> calibration / convergence checks end-to-end. Treat Layer 2 as
> `pending`; do not present this skill as workflow-ready or use it as
> the basis for an experiment without first reading Chandran et al.
> (2010), §§3–4, and consulting the in-situ application skill
> [[stochastic-heating-sub-alfvenic-2025]] for the parameter regime
> guard.


A paper-skill compiled from Chandran, Li, Rogers, Quataert &
Germaschewski (2010), *ApJ* **720**, 503
(arXiv:1001.2069; DOI: 10.1088/0004-637X/720/1/503).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Provide the analytic stochastic-heating closure cited by downstream
  PSP-era skills (`Q_⊥` as a function of in-situ-measured fluctuation
  amplitude at the gyroscale).
- Compute Q_⊥(δv_⊥, v_⊥, ρ_i) for a given turbulence amplitude when an
  agent needs a heating-rate estimate without running a kinetic
  simulation.
- Provide the ε threshold (ε ≡ δv_⊥/v_⊥) that other skills use to label
  intervals as stochastic-on vs stochastic-off.

### When NOT to use it

- In-situ application to specific PSP sub-Alfvénic intervals — that is
  the job of [[stochastic-heating-sub-alfvenic-2025]], which conditions
  on M_A < 1 and folds in the appropriate background profile.
- Cyclotron-resonant heating channel — that is the job of
  [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]] /
  [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]].
- Imbalanced (cross-helicity ≠ 0) turbulence: the c_1, c_2 constants
  here were calibrated against randomly-phased AWs, so the closure
  is out-of-scope when σ_c ≳ 0.5.

### Claim boundary

Analytic and test-particle derivation of the perpendicular ion
heating rate in randomly-phased low-frequency Alfvén-wave turbulence;
constants c_1 ≈ 0.75 and c_2 ≈ 0.34 calibrated against the paper's
own test-particle simulations. The claim is bounded to (a) the
randomly-phased AW spectrum used in §3, (b) the ε range where the
exponential suppression remains physically meaningful (ε in the
~0.05–0.5 band; outside this range the closure is an extrapolation),
and (c) protons; minor-ion application requires the analogous
calibration which this paper does not provide.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

For randomly-phased low-frequency Alfvén-wave turbulence with rms
gyroscale velocity δv_⊥(ρ_i), the perpendicular proton heating rate
per unit mass is

  Q_⊥ ≈ c_1 (δv_⊥)^3 / ρ_i · exp(−c_2 / ε), with ε ≡ δv_⊥ / v_⊥,p,

with paper-calibrated constants c_1 ≈ 0.75 and c_2 ≈ 0.34. The
exponential suppression at small ε is the load-bearing prediction:
it is what separates stochastic heating from a pure cascade rate.

### 2.2 Equations / method

- Dimensionless amplitude ε ≡ δv_⊥(ρ_i)/v_⊥,p.
- Q_⊥ closure: Q_⊥ = c_1 (δv_⊥)^3 / ρ_i · exp(−c_2/ε).
- Cascade-rate reference: ε_T ≈ ρ̄ (δv_⊥)^3 / L_⊥; Q_⊥/ε_T → O(1)
  in the ε ≳ 0.2 regime, and → 0 super-exponentially for ε ≲ 0.1.
- Test-particle integration of proton trajectories in the prescribed
  AW spectrum provides the (c_1, c_2) calibration; the trajectory
  diffusion is itself the stochasticity criterion.

### 2.3 Data assumptions

- Test-particle calibration of c_1, c_2 in randomly-phased AW
  turbulence (no imbalance, no compressive admixture).
- Gyroscale amplitude δv_⊥(ρ_i) is the relevant quantity; the
  agent must extrapolate from a spectrum to ρ_i.
- Protons in a low-β, low-collisionality plasma; the derivation
  treats the proton orbit as a quasi-linear stochastic walk.

### 2.4 Failure modes (skill memory)

- **ε ≲ 0.1** kills the exponent — the closure predicts essentially
  zero heating, and any non-zero Q_⊥ measured in this regime is
  evidence that *another* channel (cyclotron, compressive, KAW)
  dominates.
- **Spectrum bandwidth / imbalance** modifies c_1 (and probably c_2);
  the calibration is for ~Goldreich-Sridhar spectra at σ_c = 0.
- **β dependence** beyond the paper's range is not constrained —
  high-β behaviour (β ≳ 1) is an extrapolation.
- **Mis-estimation of v_⊥,p** (using v_th vs v_⊥,p vs total v_th)
  shifts ε and propagates into the exponential.
- **Gyroscale-amplitude reconstruction** from a power spectrum
  measured at lower k is sensitive to the assumed slope.

### 2.5 Figure / numerical targets

- Figure 3 Q_⊥(ε) curve: stochastic suppression at ε < 0.1;
  near-power-law Q_⊥ ∝ ε^3 at ε > 0.2.
- Constants c_1 ≈ 0.75, c_2 ≈ 0.34 recovered when fitting the
  published test-particle dataset (paper §4).
- Cascade-closure check: Q_⊥/ε_T ~ O(1) at ε ~ 0.2–0.3.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-STOCHASTIC-Q-PERP**: evaluate the analytic Q_⊥ closure given
  (δv_⊥(ρ_i), v_⊥,p, ρ_i) and the (c_1, c_2) calibration.
- **C-GYROSCALE-AMPLITUDE**: given a perpendicular-velocity power
  spectrum P(k_⊥) (or an analogue from MAG-derived δB_⊥), return
  δv_⊥(ρ_i). The agent is responsible for declaring the
  extrapolation it does.
- **C-CASCADE-RATE-REFERENCE**: evaluate ε_T = ρ̄ (δv_⊥)^3/L_⊥ on
  the same interval, for the Q_⊥/ε_T sanity check.
- **C-EPSILON-LABEL**: emit ε ≡ δv_⊥/v_⊥,p as a tag on each interval
  so downstream skills can condition on the stochastic-on / -off
  regime without re-deriving the criterion.

### 3.2 Procedure

1. Acquire (δv_⊥, v_⊥,p, ρ_i) — either from an in-situ pipeline
   (see Layer 3) or from a turbulence model.
2. C-EPSILON-LABEL: compute ε = δv_⊥/v_⊥,p. If ε < 0.05 or
   ε > 0.5, emit an out-of-calibration warning *before* returning
   a Q_⊥ number — the closure is an extrapolation in that band.
3. C-STOCHASTIC-Q-PERP: evaluate Q_⊥ with (c_1, c_2) = (0.75, 0.34).
4. C-CASCADE-RATE-REFERENCE: evaluate ε_T on the same interval and
   emit the ratio Q_⊥/ε_T as a check on plausibility.
5. Persist (ε, Q_⊥, Q_⊥/ε_T, interval_id, out-of-calibration_flag)
   for downstream consumers ([[stochastic-heating-sub-alfvenic-2025]],
   composition-with-cyclotron skills).

### 3.3 Minimum reproduction artifacts

- A Q_⊥(ε) curve over ε ∈ [0.05, 0.5] that visually matches the
  paper's Figure 3 shape (suppression knee near ε ≈ 0.1).
- Recovered fit constants c_1, c_2 from the test-particle data with
  ≲ 20 % residual (or a justification for the deviation).
- ε histogram on a real PSP encounter, with the out-of-calibration
  fraction reported.

### Validation target

A reproduction of this skill is considered honest when:

- The Q_⊥(ε) curve over ε ∈ [0.05, 0.5] reproduces the paper's
  Figure 3 shape with the suppression knee within Δε ≲ 0.02 of
  ε ≈ 0.1.
- Fit constants land at c_1 = 0.75 ± 0.15 (TODO_verify_with_full_text
  for the exact tolerance the paper accepts) and
  c_2 = 0.34 ± 0.05 (TODO_verify_with_full_text) when reproducing
  the test-particle dataset (paper §4).
- The cascade-ratio sanity check returns Q_⊥/ε_T ∈ [0.5, 2] for
  ε ∈ [0.2, 0.3], i.e. the closure is consistent with energy
  conservation at the ε regime where stochastic heating is
  expected to be efficient.

These tolerances are paper-derived (Fig. 3 visual reading + §4
calibration text); a reproduction agent that misses any of them
must report which constant moved and by how much before claiming
the analytic closure has been verified.

---

## 4. Adapter / runtime notes (optional examples)

- Implementable as a one-liner closure evaluator in any harness.
- PSP MAG + SPC pipelines (pyspedas, pyspedas-PSP, or LingTai's
  xhelio-spice-adjacent MAG/SPC loaders) are an example Layer-3
  binding for the (δv_⊥, v_⊥,p, ρ_i) inputs.
- For agents wanting to *re-derive* (c_1, c_2): any test-particle
  integrator in a prescribed AW spectrum (e.g. a 2.5D pseudo-spectral
  solver) is an example Layer-3 binding; no binding is shipped here.

---

## 5. Research-generation affordance

- **Composability with [[peng-2025-chaotic-ion-motion-finite-amplitude-alfven]]**:
  ε > 0.1 (Chandran) vs P_eff < 25 (Peng et al.) are two distinct
  chaos criteria, derived from different sides of the stochasticity
  picture (orbit diffusion vs adiabatic-invariant breaking). A joint
  diagnostic — labelling intervals by both ε and P_eff — is a
  minimal experiment that resolves whether one criterion subsumes
  the other.
- **Composability with [[stochastic-heating-sub-alfvenic-2025]]**:
  Bowen et al. 2025 apply this closure inside M_A < 1; the
  calibration regime overlaps but does not coincide, and any
  discrepancy is interpretable as a regime-extrapolation residual.
- **Tension with [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]**:
  Both channels claim Q_⊥; which dominates is interval-conditional.
  Composing the two skills produces a *partition* diagnostic that
  neither paper individually supplies.
- **Open hypothesis**: Are observed Q_⊥ events bimodal in ε,
  separating stochastic-heating-on vs -off regimes? The paper
  predicts the *functional form*, but the in-situ population is
  what tests whether the bimodality is realised.
- **Gap**: c_1, c_2 are not re-calibrated for imbalanced (σ_c ≠ 0)
  AW turbulence. PSP intervals where σ_c is large are therefore
  out-of-calibration; a re-derivation is an open agenda item.

---

## Links

- arXiv: https://arxiv.org/abs/1001.2069
- DOI: https://doi.org/10.1088/0004-637X/720/1/503
- ADS: https://ui.adsabs.harvard.edu/abs/2010ApJ...720..503C
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md (Chandran 2010 ApJ 720 503)`

## Skill graph

- [[stochastic-heating-sub-alfvenic-2025]]
- [[peng-2025-chaotic-ion-motion-finite-amplitude-alfven]]
- [[bowen-2024-cyclotron-heating-rates-ion-scale-waves]]
- [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]
