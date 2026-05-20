---
name: kelvin-helmholtz-cme-large-scale-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2512.19942"
  venue: "ApJL accepted (Dec 2025)"
---

# kelvin-helmholtz-cme-large-scale-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities and one-step procedures but do not specify the
> coronagraph-image-tracking pipeline end-to-end. Treat Layer 2 as
> `pending`; do not present this skill as workflow-ready or use it as
> the basis for an experiment without first reading Ofman et al.
> (2025), arXiv:2512.19942, and binding a coronagraph-image package.


A paper-skill compiled from Ofman, Khabarova, Kwon, Yogesh, Heifetz
& Nykyri (2025), ApJL accepted (arXiv:2512.19942).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify Kelvin–Helmholtz (KH) instability features along the
  flanks of a CME-driven sheath observed in coronagraph imagery.
- Quantify KH-wave amplitudes and wavelengths from imagery and,
  where available, in-situ shear measurements.
- Compose with downstream reconnection / SEP skills when a KH
  classification is required as a precondition.

### When NOT to use it

- KH at switchback boundaries (a kinetic-scale problem) — that is
  a separate skill (no current corpus entry; flagged as a gap).
- General-purpose CME tracking — that is the job of GCS-fit / mass
  estimation skills (separate corpus area).

### Claim boundary

Event-level identification and analysis of a large-scale,
CME-driven KH wave train in coronagraph imagery; comparison of the
measured wavelength with the magnetised-KH linear threshold using
sheath / ambient plasma parameters. The claim is bounded to the
specific CME event analysed in the paper; a statistical
generalisation is *not* claimed. The instability classification
is also linear; nonlinear evolution beyond wave-train formation is
out of scope.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

The CME analysed in the paper drives a large-scale KH wave train
along its flank with wavelength and amplitude consistent with the
linear, magnetised KH threshold given the inferred sheath /
ambient shear and field configuration.

### 2.2 Equations / method

- Magnetised KH stability criterion (single-fluid, incompressible
  with field aligned to flow):
  ρ_1 ρ_2 (v_1 − v_2)^2 / (ρ_1 + ρ_2)^2
    > (B_∥1^2 + B_∥2^2) / (4π (ρ_1 + ρ_2)).
- Wavelength of maximum growth λ_max ∝ shear-layer width L
  (with the proportionality fixed by the velocity / density
  profile assumed).
- Identification of the KH wave train from coronagraph
  difference-image time series.

### 2.3 Data assumptions

- White-light coronagraph imagery (LASCO/COR or Metis) covering
  the CME flank during the candidate KH window.
- Ambient and sheath density / field estimates (from in-situ
  ICME-sheath catalogue or from a coronal model).
- Sheath shear layer width L estimable from image kinematics.

### 2.4 Failure modes (skill memory)

- **Projection ambiguity** in 2D imagery: the observed wavelength
  is a projected quantity unless 3D reconstruction (multi-viewpoint)
  is available.
- **Shear-width estimation** is sensitive to image resolution and
  to the cadence used.
- **Field-orientation assumption** matters: only the field
  component along the flow direction stabilises KH, and that
  component is rarely directly measured at the flank.
- **Density-ratio inference** from white-light brightness depends
  on the Thomson-scattering geometry assumed.

### 2.5 Figure / numerical targets

- A coronagraph difference-image time series showing the KH wave
  train; wavelength λ measured to ≲ 20 % accuracy.
- λ within the linear-theory band λ_max(L) to within a factor of
  ≲ 2 (paper-stated; the exact factor is to be confirmed against
  the full text).
- Magnetised KH criterion satisfied at the identified interface.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-CORONAGRAPH-IMAGE-LOAD**: load a coronagraph movie /
  difference-image stack over a specified time window.
- **C-WAVE-TRAIN-EXTRACT**: identify a periodic boundary
  deformation pattern in the difference-image stack and return
  (λ_obs, amplitude, position-angle range, time window).
- **C-SHEATH-AMBIENT-PARAMETERS**: return (ρ_1, ρ_2, v_1, v_2,
  B_∥1, B_∥2, L) — either from an in-situ ICME-sheath catalogue
  or from a coronal model that the runtime selects.
- **C-KH-LINEAR**: evaluate the magnetised KH criterion above
  and report (a) whether the interface is linearly unstable and
  (b) λ_max(L).

### 3.2 Procedure

1. C-CORONAGRAPH-IMAGE-LOAD over a window enclosing the CME and
   its flank.
2. C-WAVE-TRAIN-EXTRACT: emit (λ_obs, amplitude, time window).
3. C-SHEATH-AMBIENT-PARAMETERS: emit the plasma parameters
   needed for the KH evaluation.
4. C-KH-LINEAR: report (unstable? yes/no) and λ_max.
5. Compose: report (λ_obs / λ_max) and the binary
   instability flag. Out-of-band ratios are evidence that
   either the inferred parameters are wrong or that a different
   instability is acting.

### 3.3 Minimum reproduction artifacts

- An event card with (event_id, CME catalogue ID, λ_obs, λ_max,
  instability flag, plasma parameters used) for the paper's
  event.
- A difference-image figure reproducing the wave-train
  identification.

### Validation target

A reproduction of this skill is considered honest when:

- The same CME event identified in the paper is recovered from
  the LASCO/COR catalogue with the same time window to within
  ≲ 30 minutes.
- The measured λ_obs lies within a factor of ≲ 2 of λ_max(L)
  computed from the sheath / ambient parameters (paper-stated
  tolerance; exact factor TODO_verify_with_full_text).
- The magnetised KH criterion is satisfied at the identified
  interface with the inferred (ρ, v, B_∥) within their stated
  uncertainty bars.

---

## 4. Adapter / runtime notes (optional examples)

- LASCO / COR / Metis pipelines (e.g. SunPy + custom difference-
  image utilities, or aiapy for context EUV) are example Layer-3
  bindings for C-CORONAGRAPH-IMAGE-LOAD; none are shipped here.
- The in-situ ICME-sheath catalogue (e.g. Helio4Cast HELCATS, or
  HelioCloud) is an example Layer-3 binding for
  C-SHEATH-AMBIENT-PARAMETERS.

---

## 5. Research-generation affordance

- **Composability with [[hcs-reconnection-statistics-psp-encounter-2025]]**:
  KH-active CME flanks may seed reconnection downstream. A joint
  event-and-statistics study is a natural follow-up that neither
  paper individually supports.
- **Composability with the (future) switchback-KH skill**:
  KH at large scale (CME flank) and at small scale (switchback
  boundary) are governed by the same magnetised criterion at
  different (β, shear, scale) regimes; a cross-scale comparison
  is a composable experiment.
- **Open hypothesis**: Is KH activity on CME flanks statistically
  associated with enhanced suprathermal-particle generation
  downstream of the event?
- **Gap**: Statistical KH-occurrence rate on CME flanks is not
  constrained by this paper; it is an obvious next agenda item
  (apply the contract to the LASCO CME catalogue).
- **Tension with reconnection-only flank interpretations**: some
  flank brightenings are interpreted as reconnection signatures;
  KH provides an alternative mechanism, and the discriminator
  (periodicity in image space) is the load-bearing measurement.

---

## Links

- arXiv: https://arxiv.org/abs/2512.19942
- DOI: TODO_verify_with_full_text (preprint; ApJL acceptance noted in arXiv comments)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.19942`

## Skill graph

- [[hcs-reconnection-statistics-psp-encounter-2025]]
