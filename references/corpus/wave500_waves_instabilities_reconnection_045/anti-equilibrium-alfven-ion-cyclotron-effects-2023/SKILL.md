---
name: anti-equilibrium-alfven-ion-cyclotron-effects-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2308.14944"
  venue: "ApJ accepted (Aug 2023)"
---

# anti-equilibrium-alfven-ion-cyclotron-effects-2023

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the
> free-form-VDF gridding, the bi-Maxwellian fit recipe, or the
> per-event aggregation end-to-end. Treat Layer 2 as `pending`; do
> not present this skill as workflow-ready or use it as the basis
> for an experiment without first reading Walters, Klein, Lichko,
> Stevens, Verscharen & Chandran (2023), arXiv:2308.14944.


A paper-skill compiled from Walters, Klein, Lichko, Stevens,
Verscharen & Chandran (2023), ApJ accepted (arXiv:2308.14944;
11 pages, 4 figures, 1 table per arXiv comments).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict how non-equilibrium (non-Maxwellian) VDFs shift Alfvén
  ion-cyclotron (AIC) wave growth rates relative to the
  bi-Maxwellian baseline.
- Decide whether observed AIC-wave occurrence intervals require
  non-Maxwellian VDFs to explain their growth (i.e. flag
  bi-Maxwellian mis-classifications).
- Provide a "free-form-VDF" closure that downstream skills
  ([[verniero-2020-proton-beams-ion-scale-waves]],
  [[klein-2018-multispecies-stability-anisotropy]]) can use as a
  drop-in replacement for the bi-Maxwellian closure.

### When NOT to use it

- Pure bi-Maxwellian AIC growth — see
  [[ion-driven-instabilities-classification-2023]] and
  [[klein-2018-multispecies-stability-anisotropy]].
- Cyclotron-family branches other than AIC (oblique AIC,
  mirror): the bi-Maxwellian-bias quantification is restricted
  to AIC in this paper.
- Nonlinear AIC saturation: this is a linear-growth-rate skill.

### Claim boundary

Linear-Vlasov dispersion analysis using observed (non-Maxwellian)
VDFs as the dielectric input; growth-rate shifts γ_max
quantified relative to a bi-Maxwellian fit baseline of the same
VDFs. The claim is bounded to (a) the linear regime, (b) the
PSP / Wind events sampled in the paper, and (c) the AIC branch
specifically.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Non-equilibrium VDF features (beams, shoulders, plateaus) shift
the AIC γ_max by paper-quantified factors relative to a
bi-Maxwellian fit of the same VDFs; some observed AIC intervals
are only explainable when the dispersion uses the free-form VDF.

### 2.2 Equations / method

- Linear-Vlasov dispersion D(ω, k; F(v)) = 0 using the observed
  F(v) directly, not a fit.
- Bi-Maxwellian baseline: fit F(v) → F_bi-Max(v) with parameters
  (n, v_drift, T_∥, T_⊥); solve dispersion with F_bi-Max.
- Define the bias ratio R_γ = γ_max(F_obs) / γ_max(F_bi-Max).
- Population statistics on R_γ over the paper's labelled event
  set.

### 2.3 Data assumptions

- In-situ VDF in *distribution-function* form (not just
  moments) — PSP SPAN-i, Wind/SWE/3DP, or analogous.
- A linear-Vlasov solver with arbitrary-VDF input (ALPS,
  LEOPARD, or analogous).
- A bi-Maxwellian fit recipe consistent across the sample.

### 2.4 Failure modes (skill memory)

- **Fit choice** for the bi-Maxwellian baseline matters: a
  beam-aware fit (two-component bi-Max) versus a single
  bi-Maxwellian changes the bias.
- **Noise floor in VDF** smears non-Maxwellian features; the
  effective bias is then under-estimated.
- **Velocity-grid resolution** in the dispersion solver must
  be fine enough to resolve the beam / shoulder.
- **Cross-helicity / wave-direction selection**: AIC is a
  parallel-propagating branch; selection of k orientation
  matters for γ_max.

### 2.5 Figure / numerical targets

- γ_max ratio R_γ per labelled event reproduced within stated
  bars (TODO_verify_with_full_text for exact tolerance from
  paper §IV).
- Sign of the bi-Maxwellian bias reproduced (under-estimate
  when the observed VDF carries beams).
- The set of intervals reclassified overlaps the paper's set
  within ≲ 10 % count discrepancy.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-VDF-LOAD**: load the in-situ VDF for an interval in
  distribution-function form.
- **C-BI-MAX-FIT**: fit (n, v_drift, T_∥, T_⊥) to F(v).
- **C-LIN-VLASOV-FREEFORM-VDF**: solve dispersion using F(v)
  directly.
- **C-LIN-VLASOV-BI-MAX**: solve dispersion using F_bi-Max.
- **C-BIAS-AGGREGATE**: emit (R_γ, classification_change)
  per interval and aggregate the bias statistics.

### 3.2 Procedure

1. C-VDF-LOAD: pull F(v) for the interval.
2. C-BI-MAX-FIT → F_bi-Max(v).
3. C-LIN-VLASOV-FREEFORM-VDF on F(v) → γ_max(F_obs).
4. C-LIN-VLASOV-BI-MAX on F_bi-Max → γ_max(F_bi-Max).
5. Emit R_γ and the classification change flag.
6. C-BIAS-AGGREGATE over the event set; produce the
   reclassification fraction.

### 3.3 Minimum reproduction artifacts

- A γ_max-ratio table per event in the paper's labelled set.
- A histogram of R_γ across the sample.
- A short list of intervals reclassified from "stable" to
  "unstable" by the free-form closure.

### Validation target

A reproduction of this skill is considered honest when:

- R_γ on the paper's labelled events reproduces the paper's
  reported values to within stated bars (TODO_verify_with_full_text
  for the exact tolerance from §IV).
- The sign pattern of the bi-Maxwellian bias is recovered.
- The reclassification fraction matches the paper to within
  ≲ 10 % count discrepancy.

---

## 4. Adapter / runtime notes (optional examples)

- ALPS supports free-form VDF input — example Layer-3 binding.
- LEOPARD with kappa / multi-component closure is an example
  Layer-3 binding that requires a parametric VDF
  representation.
- pyspedas / PSP-SPAN-i Level-3 loaders are example Layer-3
  bindings for C-VDF-LOAD; none are shipped here.

---

## 5. Research-generation affordance

- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**:
  provide the free-form-VDF closure for AIC-wave occurrence
  prediction; the Verniero PSP-encounter beam catalogue is a
  natural input.
- **Composability with [[klein-2018-multispecies-stability-anisotropy]]**:
  the multispecies stability constraints there are bi-Maxwellian-
  based; the bias quantified here propagates into them, and
  re-running with free-form VDFs is a composable agenda item.
- **Tension with bi-Maxwellian survey papers**: any AIC-
  occurrence statistic in the Wind / Helios archives that
  used bi-Maxwellian fits inherits the bias and may need
  revision.
- **Open hypothesis**: A non-trivial fraction of historical
  AIC-stability calls are mis-classifications because the
  underlying VDFs carried beams that the bi-Maxwellian fit
  smoothed away.
- **Gap**: The bias quantification is restricted to AIC;
  analogous quantification for oblique AIC and mirror branches
  is an open agenda.

---

## Links

- arXiv: https://arxiv.org/abs/2308.14944
- DOI: TODO_verify_with_full_text (ApJ-accepted preprint)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2308.14944`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[klein-2018-multispecies-stability-anisotropy]]
- [[ion-driven-instabilities-classification-2023]]
