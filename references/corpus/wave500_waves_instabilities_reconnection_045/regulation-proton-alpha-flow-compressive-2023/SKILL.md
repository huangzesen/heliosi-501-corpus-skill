---
name: regulation-proton-alpha-flow-compressive-2023
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2308.02036"
  venue: "ApJ accepted (Aug 2023; 13 pages, 9 figures)"
---

# regulation-proton-alpha-flow-compressive-2023

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the hybrid-
> PIC initial-condition design, the prescribed-compressive-driver
> spectrum, or the (compressive, instability) decomposition recipe
> end-to-end. Treat Layer 2 as `pending`; do not present this skill
> as workflow-ready or use it as the basis for an experiment without
> first reading Zhu, Verscharen, He, Maruca & Owen (2023),
> arXiv:2308.02036.


A paper-skill compiled from Zhu, Verscharen, He, Maruca & Owen
(2023), ApJ accepted (arXiv:2308.02036; 13 pages, 9 figures).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the radial evolution of proton-α differential flow
  Δv_pα(r) under combined compressive-fluctuation and ion-scale
  instability regulation.
- Decide whether an observed |v_α − v_p|(r) decay is consistent
  with the proposed regulation channel.
- Compose with multi-species stability skills to bound the
  marginal-stability locus along an encounter.

### When NOT to use it

- Pure expansion-driven flow decay without fluctuations (a
  simpler scaling law applies).
- Multi-fluid coronal acceleration mechanisms — out of scope
  for this in-situ-regime paper.
- Heavy-ion (Fe, O) drift regulation: only proton + α are
  covered by the simulations and diagnostics here.

### Claim boundary

Hybrid-PIC simulations of proton + α populations with a
*prescribed* compressive-fluctuation amplitude δn/n, compared
to observed Δv_pα(r) statistics in Wind / Helios / PSP. The
claim is bounded to (a) the prescribed compressive spectrum,
(b) the (β_p, β_α, Δv_pα) range scanned, and (c) the proton +
α-only configuration.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

The combination of compressive-fluctuation pitch-angle
scattering and ion-scale-instability action regulates the
proton-α differential flow toward marginal stability; the
observed |Δv_pα|(r) decay envelope is reproducible by the
hybrid simulations within the paper's stated bars.

### 2.2 Equations / method

- Drift-instability threshold for proton-α systems on the
  parallel and oblique branches; γ_max(Δv_pα, β).
- Compressive-fluctuation effective pitch-angle scattering
  rate ν_eff(δn/n, k_∥) acting on the relative drift.
- Hybrid run with prescribed compressive driver in addition
  to the proton-α drift; Δv_pα(t) extracted from the
  population moments.
- Decomposition into (compressive, instability) contributions
  via a comparison run with the driver turned off.

### 2.3 Data assumptions

- Hybrid-PIC code with proton + α support and a compressive-
  forcing module (e.g. P3D, dHybridR, CAMELIA with the
  appropriate setup).
- In-situ Δv_pα(r) statistics; PSP SPAN-i α moments,
  Wind/SWE α channel, or Helios α data.
- Prescribed compressive spectrum δn/n at the relevant scale.

### 2.4 Failure modes (skill memory)

- **Fluctuation-amplitude prescription** drives the magnitude
  of regulation; the prescribed δn/n is the load-bearing
  input.
- **Initial Δv_pα,0** sets the onset of instability; runs
  initialised far above threshold relax differently than
  those near marginal.
- **β regime**: at low β the AIC drift branch dominates; at
  higher β the magnetosonic / fast-mode branch contributes.
  The (compressive, instability) decomposition is regime-
  dependent.
- **PSP α-channel calibration** can mis-estimate Δv_pα,obs;
  the comparison envelope is sensitive to this.

### 2.5 Figure / numerical targets

- Δv_pα(r) hybrid-output profile inside the in-situ envelope
  from the paper's reference dataset (TODO_verify_with_full_text
  for the exact band).
- δn/n-dependence of Δv_pα-decay slope reproduces the paper's
  reference figure within stated bars.
- (compressive, instability) contribution decomposition
  matches the paper's Table TODO_verify_with_full_text within
  ≲ 15 % per channel.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-HYBRID-PROTON-ALPHA**: hybrid-PIC run with proton + α
  populations at prescribed (β_p, β_α, Δv_pα,0).
- **C-COMPRESSIVE-AMP**: apply a prescribed compressive-
  fluctuation driver at amplitude δn/n and spectral shape
  matching the paper's reference.
- **C-DRIFT-INSTAB**: evaluate γ_max for the proton-α drift
  configuration on parallel + oblique branches.
- **C-DECOMP-PROFILE**: extract Δv_pα(t) and decompose into
  (compressive, instability) contributions by comparison
  with a driver-off run.

### 3.2 Procedure

1. Initialise hybrid with (β_p, β_α, Δv_pα,0).
2. Apply C-COMPRESSIVE-AMP at the paper's reference δn/n.
3. C-HYBRID-PROTON-ALPHA: run until Δv_pα stabilises.
4. C-DRIFT-INSTAB on the same VDF for cross-check.
5. C-DECOMP-PROFILE: subtract a driver-off run to obtain the
   per-channel contribution.
6. Sweep δn/n and Δv_pα,0; emit the regulation surface.
7. Compare to observed Δv_pα(r) envelope.

### 3.3 Minimum reproduction artifacts

- A Δv_pα(t) figure for one reference run.
- A regulation surface in (Δv_pα,0, δn/n) reproducing the
  paper's reference shape.
- A per-channel decomposition table on one or more reference
  cases.

### Validation target

A reproduction of this skill is considered honest when:

- The Δv_pα(r) hybrid-output profile lies inside the in-situ
  envelope (TODO_verify_with_full_text for the exact band).
- The δn/n-dependence figure reproduces the paper's reference
  slope sign and order of magnitude.
- The per-channel (compressive, instability) decomposition is
  consistent with the paper's Table within ≲ 15 % per channel
  (TODO_verify_with_full_text for the exact table).

---

## 4. Adapter / runtime notes (optional examples)

- Hybrid PIC codes with α support and compressive forcing
  (e.g. P3D, dHybridR, CAMELIA) are example Layer-3 bindings;
  none are shipped here.
- Wind/SWE α-channel L2 loaders and PSP SPAN-i α-mode L3 are
  example Layer-3 bindings for the in-situ Δv_pα(r) envelope.

---

## 5. Research-generation affordance

- **Composability with [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]**:
  Bianco 2025 covers AW-driven proton-beam evolution; this
  skill adds the compressive-fluctuation channel for
  multi-species drift. The combined picture is a more
  complete drift-evolution model than either supplies alone.
- **Composability with [[verniero-2020-proton-beams-ion-scale-waves]]**:
  the ion-scale-wave occurrence statistics of Verniero 2020
  are the observational counterpart of the drift-instability
  regulator quantified here.
- **Open hypothesis**: CIR-adjacent intervals where compressive
  fluctuations are enhanced show measurably faster Δv_pα
  decay than ambient stream intervals at matched heliocentric
  distance.
- **Gap**: The simulations use a *prescribed* compressive
  driver; self-consistent generation of compressive
  fluctuations from the same instabilities is not closed
  here, and is the natural next agenda item.
- **Tension with expansion-only Δv_pα decay models**: pure
  expansion predicts a different functional form for
  Δv_pα(r) than the regulated picture; the discriminator is
  the δn/n-dependence quantified here.

---

## Links

- arXiv: https://arxiv.org/abs/2308.02036
- DOI: TODO_verify_with_full_text (ApJ-accepted preprint)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2308.02036`

## Skill graph

- [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]
- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[klein-2018-multispecies-stability-anisotropy]]
