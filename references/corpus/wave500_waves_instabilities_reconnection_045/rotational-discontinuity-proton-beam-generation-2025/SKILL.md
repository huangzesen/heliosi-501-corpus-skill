---
name: rotational-discontinuity-proton-beam-generation-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2512.10406"
  venue: "arXiv preprint (Dec 2025; 7 figures)"
---

# rotational-discontinuity-proton-beam-generation-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the hybrid-
> PIC RD initialisation, the beam-extraction recipe, or the RD-vs-
> reconnection discriminator end-to-end. Treat Layer 2 as `pending`;
> do not present this skill as workflow-ready or use it as the basis
> for an experiment without first reading Lin, Bacchini, He, Pezzini
> & Peng (2025), arXiv:2512.10406.


A paper-skill compiled from Lin, Bacchini, He, Pezzini & Peng
(2025), arXiv:2512.10406 (preprint; 7 figures).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the generation of proton beams at switchback-boundary-
  like rotational discontinuities (RDs) in the solar wind.
- Decide whether proton beams observed downstream of an RD in
  PSP / SolO data are consistent with the RD-generation
  mechanism.
- Provide an RD-vs-reconnection-exhaust discriminator for
  switchback-boundary events.

### When NOT to use it

- Reconnection at switchback boundaries — that is the regime of
  [[phan-2022-switchback-boundary-reconnection-psp]]; the two
  papers analyse overlapping event classes but interpret them
  differently, and the discriminator is what separates them.
- AW-driven proton-beam evolution in the switchback interior
  — that is [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]].
- Beam evolution at large heliocentric distances where the RD
  signature has decayed.

### Claim boundary

Hybrid-PIC simulations of an isolated RD with switchback-boundary-
like jumps in a solar-wind-like background, combined with PSP
RD-event candidates. The claim is bounded to (a) the
configuration of the RD (Δθ_B, normal-B continuity, density
continuity), (b) the hybrid resolution achievable, and (c) the
PSP event sample considered.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

RDs with switchback-boundary-like properties produce proton
beams via wave-particle interaction at the discontinuity; the
predicted beam drift v_b matches observed beam drifts downstream
of PSP RDs in matched (Δθ_B, β) bins.

### 2.2 Equations / method

- RD jump conditions: normal-B and density continuous; tangential-
  B rotates by Δθ_B with |B| approximately preserved.
- Reconnection-exhaust jump conditions (alternative
  interpretation): normal-B reversal allowed, density and B-
  magnitude jumps possible.
- Wave-particle resonance condition at the RD that the paper
  identifies as the beam-generation mechanism (paper §4 TODO_
  verify_with_full_text for the exact resonance form).
- v_b(Δθ_B, β, M_A) extracted from the hybrid run.

### 2.3 Data assumptions

- Hybrid-PIC code capable of evolving an RD with a solar-wind-
  like upstream background, sufficient resolution to capture
  ion-scale physics at the discontinuity.
- PSP MAG + SPAN-i RD event catalogue.
- A density continuity diagnostic at PSP cadence (the load-
  bearing discriminator).

### 2.4 Failure modes (skill memory)

- **RD-vs-reconnection-exhaust ambiguity**: events with marginal
  normal-B continuity straddle the discriminator and can be
  mis-classified in either direction.
- **Cadence vs RD thickness**: PSP cadence may be too coarse to
  resolve thin RDs; the apparent jumps then mix into the
  ambient turbulence.
- **Hybrid-resolution dependence**: ion-scale physics at the
  RD requires fine resolution; under-resolved runs miss the
  resonance.
- **Background-turbulence amplitude** dominates the beam
  evolution at long times; the v_b prediction is for the
  immediate downstream.

### 2.5 Figure / numerical targets

- Hybrid simulation produces a downstream proton beam with
  v_b in the paper-reported band (TODO_verify_with_full_text
  exact band).
- (Δθ_B, β)-dependence of v_b matches the paper's reference
  figure.
- RD-vs-reconnection discriminator classifies the paper's
  labelled events with ≲ 10 % error.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-RD-INIT**: initialise a hybrid simulation with an RD
  configuration (Δθ_B, |B|, n, β, M_A) consistent with
  switchback-boundary-like jumps.
- **C-HYBRID-RD**: evolve the RD; extract downstream proton
  VDF moments and identify the beam component.
- **C-RD-EVENT-MATCH**: given a PSP RD event with its jumps,
  identify the matching simulation case and emit
  (v_b_sim, v_b_obs, residual).
- **C-RD-RX-DISCRIMINATOR**: emit a binary RD-vs-reconnection
  flag from (normal-B continuity, density continuity,
  tangential-B jump) on each event.

### 3.2 Procedure

1. C-RD-INIT: pick an (Δθ_B, β, M_A) point that brackets a
   PSP candidate event.
2. C-HYBRID-RD: run, extract downstream beam.
3. C-RD-EVENT-MATCH: pair the run with one or more PSP
   events.
4. C-RD-RX-DISCRIMINATOR on each PSP event in the sample;
   tag as RD or reconnection.
5. Persist (event_id, sim_id, RD_flag, v_b_sim, v_b_obs,
   residual) for downstream consumers.

### 3.3 Minimum reproduction artifacts

- A v_b(Δθ_B, β) figure from the hybrid runs reproducing the
  paper's reference plot shape.
- A per-event table with the discriminator flag and
  (v_b_sim, v_b_obs).
- A confusion-matrix summary on the paper's labelled event
  set.

### Validation target

A reproduction of this skill is considered honest when:

- v_b from the hybrid runs falls within the paper-reported
  band on the labelled events (TODO_verify_with_full_text for
  the exact tolerance).
- The (Δθ_B, β)-dependence figure reproduces the paper's
  reference-figure shape.
- The RD-vs-reconnection-exhaust discriminator classifies the
  paper's labelled events with ≲ 10 % count discrepancy.

---

## 4. Adapter / runtime notes (optional examples)

- dHybridR, CAMELIA are example Layer-3 bindings for C-HYBRID-
  RD; none are shipped here.
- pyspedas-PSP / hampy are example Layer-3 bindings for the
  MAG / SPAN-i RD-event detection upstream of C-RD-EVENT-MATCH.
- The discriminator is a one-line diagnostic on (n, B_n, B_t)
  time series, expressible in any analysis harness.

---

## 5. Research-generation affordance

- **Composability with [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]**:
  proton beams have two sources — AW-driven (switchback
  interior) and RD-driven (boundary). The joint catalogue is a
  composable artifact neither paper produces alone.
- **Tension with [[phan-2022-switchback-boundary-reconnection-psp]]**:
  the same boundary class is interpreted as RD (this paper)
  vs reconnection exhaust (Phan 2022). The discriminator
  (continuity of normal-B and density) is the load-bearing
  test, and any reanalysis should report the discriminator
  state explicitly.
- **Open hypothesis**: PSP beam-event statistics are dominated
  by RD-driven (rather than AW-driven) beams in regions where
  switchback-boundary density continuity holds; testable on
  the existing PSP encounter archive.
- **Gap**: PSP cadence may be inadequate to resolve some thin
  RDs; SolO RPW high-cadence cross-check is the natural next
  composable step.
- **Composability with [[surface-waves-switchback-boundaries-psp-2025]]**:
  surface-wave activity at switchback boundaries may modulate
  the beam-generation efficiency; a joint analysis is open.

---

## Links

- arXiv: https://arxiv.org/abs/2512.10406
- DOI: TODO_verify_with_full_text (preprint as of Dec 2025)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.10406`

## Skill graph

- [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]
- [[phan-2022-switchback-boundary-reconnection-psp]]
- [[surface-waves-switchback-boundaries-psp-2025]]
