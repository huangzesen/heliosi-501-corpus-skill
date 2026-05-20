---
name: oblique-drift-instability-solar-wind-heating-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2512.18485"
  venue: "arXiv preprint (Dec 2025; revised Feb 2026)"
---

# oblique-drift-instability-solar-wind-heating-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the
> linear-Vlasov solver, k-grid, or hybrid-verification end-to-end.
> Treat Layer 2 as `pending`; do not present this skill as workflow-
> ready or use it as the basis for an experiment without first reading
> Martinovic, Klein, Ofman et al. (2025), arXiv:2512.18485.


A paper-skill compiled from Martinovic, Klein, Ofman, Yogesh,
Verniero, Yoon, Howes, Verscharen & Alterman (2025), arXiv:2512.18485.

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the heating contribution of *oblique* drift-instability
  modes (i.e. k_⊥ ≠ 0) in the solar wind for a given drift VDF.
- Diagnose whether observed VDF features (β_∥, Δv_pα, anisotropy)
  are constrained by oblique-branch marginal stability rather
  than by the parallel branches alone.
- Provide a marginal-stability locus in the (β_∥, Δv_pα/v_A)
  plane that supersedes parallel-only loci where the oblique
  branch dominates.

### When NOT to use it

- Parallel drift modes only — see
  [[proton-alpha-aic-driven-instabilities-2023]] and
  [[ion-driven-instabilities-classification-2023]].
- Pure stochastic / cyclotron heating channels (no drift) — see
  [[chandran-2010-stochastic-heating-perp-alfven]] and the
  Bowen-2024 cyclotron skills.
- Nonlinear saturation amplitudes at large drift — the paper's
  marginal-stability claim is linear; nonlinear evolution is
  bounded only by limited hybrid runs.

### Claim boundary

Linear-Vlasov scan in the (k_∥, k_⊥) plane of drift-mode families
for representative solar-wind VDFs (with optional hybrid
verification of the heating partition). The claim is bounded to
(a) the linear regime, (b) the (β_∥, Δv) range scanned in the
paper, and (c) the species pair (typically proton + α) considered.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Oblique drift modes (γ_max at k_⊥ ≠ 0) provide a heating channel
not captured by parallel-only models; their action pins specific
VDF features at a marginal-stability locus that is *shifted* in
the (β_∥, Δv_pα/v_A) plane relative to parallel-only loci. The
observed VDF population sits more tightly against the oblique
locus than against the parallel-only locus.

### 2.2 Equations / method

- Linear-Vlasov dispersion D(ω, k_∥, k_⊥; VDF) = 0 over a 2-D
  k-grid.
- γ_max(k_∥, k_⊥) maximised over the oblique branch (k_⊥ > k_⊥*
  for some cutoff k_⊥* fixed by the analysis).
- Q_oblique computed from γ_max times the energy in the unstable
  modes (quasi-linear estimate).
- Marginal-stability contour: locus of (β_∥, Δv_pα/v_A) on which
  γ_max(oblique) = γ_threshold (paper choice; typically
  10^{-4} Ω_p or similar).

### 2.3 Data assumptions

- In-situ VDF measurements (proton + α, or proton + electron)
  with enough resolution to constrain (Δv, T_∥, T_⊥, β_∥).
- Linear-Vlasov solver with full (k_∥, k_⊥) coverage and
  arbitrary-VDF capability.
- Optional: hybrid-PIC code for nonlinear verification.

### 2.4 Failure modes (skill memory)

- **Reduced dimensionality** of the k-grid loses oblique branches:
  any parallel-only solver mis-classifies the boundary.
- **Drift orientation relative to B** controls γ_max — VDF
  pre-processing must preserve the (∥, ⊥) decomposition.
- **VDF fitting choice** (bi-Maxwellian vs free-form) shifts the
  marginal-stability locus by amounts comparable to the paper's
  claimed shift.
- **k-grid resolution** at small k_⊥ can spuriously suppress the
  oblique branch — convergence in k_⊥ must be demonstrated.

### 2.5 Figure / numerical targets

- Q-oblique / Q-parallel ratio recovered to within stated bars
  (paper Fig. TODO_verify_with_full_text).
- Marginal-stability locus in the (β_∥, Δv_pα/v_A) plane shifted
  relative to parallel-only models by a paper-specified factor.
- Observed VDFs cluster against the oblique locus with smaller
  residuals than against the parallel-only locus.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-VDF-LOAD**: provide the in-situ VDF (or a parametric drift
  VDF) for the interval / population of interest.
- **C-LIN-VLASOV-OBLIQUE**: solve the linear dispersion over a
  full (k_∥, k_⊥) grid; emit γ_max and (k_∥*, k_⊥*) of the
  maximally growing mode.
- **C-LIN-VLASOV-PARALLEL**: reference parallel-only solver for
  the same VDF.
- **C-MARGINAL-LOCUS**: scan (β_∥, Δv_pα/v_A) and emit the
  contour where γ_max = γ_threshold.
- **C-HYBRID-OBLIQUE-DRIFT** (optional): hybrid-PIC verification
  of the nonlinear Q partition.

### 3.2 Procedure

1. C-VDF-LOAD: define the drift VDF (parametric or from in-situ
   data).
2. C-LIN-VLASOV-OBLIQUE: scan the (k_∥, k_⊥) plane, emit
   γ_max(oblique).
3. C-LIN-VLASOV-PARALLEL: emit γ_max(parallel) on the same VDF.
4. C-MARGINAL-LOCUS: scan (β_∥, Δv_pα/v_A); emit the oblique
   and parallel marginal contours.
5. (Optional) C-HYBRID-OBLIQUE-DRIFT: initialise a hybrid run at
   one (β_∥, Δv) point on each contour and report Q in each
   branch.
6. Persist (γ_max_oblique, γ_max_parallel, locus_shift,
   Q_partition_if_run) on the analysed sample.

### 3.3 Minimum reproduction artifacts

- A Q_oblique / Q_parallel curve over the paper's (β_∥, Δv)
  scan range.
- Marginal-stability locus plot with oblique vs parallel
  contours overplotted.
- VDF-cluster figure: observed (β_∥, Δv) points overlaid on
  both loci.

### Validation target

A reproduction of this skill is considered honest when:

- The Q_oblique / Q_parallel ratio recovered on the paper's
  scan sits within the paper's stated bars (TODO_verify_with_full_text
  for the exact tolerance band).
- The marginal-stability locus shift in the (β_∥, Δv_pα/v_A)
  plane has the same sign and order of magnitude as the paper
  reports.
- A hybrid run at one locus point produces Q in the same branch
  as the linear theory predicts (qualitative check).

---

## 4. Adapter / runtime notes (optional examples)

- ALPS, PLUME, NHDS, LEOPARD are example Layer-3 bindings for
  C-LIN-VLASOV-OBLIQUE (ALPS supports arbitrary VDFs); none are
  shipped here.
- dHybridR, CAMELIA are example Layer-3 bindings for
  C-HYBRID-OBLIQUE-DRIFT.

---

## 5. Research-generation affordance

- **Composability with [[proton-alpha-aic-driven-instabilities-2023]]**:
  some intervals previously attributed to AIC may be oblique-drift
  signatures. Re-running the AIC sample through the oblique
  contract yields a reclassification fraction that is a
  quantitative measure of the parallel-only bias.
- **Composability with [[klein-2018-multispecies-stability-anisotropy]]**:
  multispecies stability constraints from parallel-only models
  can be revised by the oblique contour.
- **Tension with parallel-only attribution**: in regimes where
  the oblique branch dominates, the parallel-only literature has
  under-bounded the marginal-stability locus, and the size of
  the under-bound is what this paper quantifies.
- **Open hypothesis**: VDFs previously attributed to AIC are
  actually oblique-drift signatures in some fraction of the PSP /
  SolO archive; the fraction is the load-bearing follow-up
  number.
- **Gap**: Nonlinear saturation of the oblique branch at large
  drift is bounded only by limited hybrid runs; extending hybrid
  coverage is an open agenda item.

---

## Links

- arXiv: https://arxiv.org/abs/2512.18485
- DOI: TODO_verify_with_full_text (preprint as of submission)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.18485`

## Skill graph

- [[proton-alpha-aic-driven-instabilities-2023]]
- [[ion-driven-instabilities-classification-2023]]
- [[klein-2018-multispecies-stability-anisotropy]]
