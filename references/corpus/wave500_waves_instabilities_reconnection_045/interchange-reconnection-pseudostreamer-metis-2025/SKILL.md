---
name: interchange-reconnection-pseudostreamer-metis-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: true
  arxiv: "2502.08015"
  venue: "arXiv preprint (Feb 2025)"
---

# interchange-reconnection-pseudostreamer-metis-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the Metis image pipeline or the
> PFSS pseudostreamer detector end-to-end. Treat Layer 2 as `pending`;
> do not present this skill as workflow-ready or use it as the basis
> for an experiment without first reading Romano, Wyper, Andretta et
> al. (2025), arXiv:2502.08015.


A paper-skill compiled from Romano, Wyper, Andretta, Antiochos,
Russano, Spadaro et al. (2025), arXiv:2502.08015 (36 co-authors;
SolO/Metis observation paper).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify Alfvénic outflows driven by interchange reconnection
  at pseudostreamer footpoints in Metis coronagraph data.
- Quantify outflow speed and tie it to in-situ slow-Alfvénic
  streams via PFSS / coronal-model footpoint mapping.
- Provide a coronal-side "source" measurement for downstream
  in-situ classifiers that label streams as slow-Alfvénic.

### When NOT to use it

- Streamer-belt origin without a pseudostreamer topology — that
  is the job of streamer-belt / heliospheric-current-sheet
  source skills.
- Active-region jets without an outflow into the open
  pseudostreamer leg — separate event class.
- General-purpose CME / flare imaging — out of scope.

### Claim boundary

Single-event analysis combining Metis VL + UV imagery with
PFSS-derived topology of a pseudostreamer; the outflow is
identified by its brightness signature and its speed is
compared with the local Alfvén speed inferred from a coronal
model. The claim is bounded to the specific event analysed;
a statistical generalisation is *not* claimed by this paper.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Metis observes Alfvénic outflows whose timing, location, and
speed are consistent with interchange reconnection at the
footpoints of a specific pseudostreamer; the outflows tie the
corona to a slow-Alfvénic stream in the heliosphere.

### 2.2 Equations / method

- Outflow speed v_⊥(t, r) extracted from Metis brightness time
  series via standard time-distance / running-difference image
  processing.
- Local Alfvén speed v_A = B / √(4π ρ) from a coronal model
  (PFSS extension + density model).
- Pseudostreamer topology classification (closed-closed-open
  null-line configuration) from a PFSS extrapolation.
- Optional: SolO EUI / SPICE coronal-hole / AR boundary cross-
  check at the footpoint.

### 2.3 Data assumptions

- Metis VL and UV imagery covering the candidate event.
- A PFSS or analogous topology model for the parent AR / CH
  pair (synoptic Br input).
- Coronal density model adequate for v_A inference at the
  outflow region.

### 2.4 Failure modes (skill memory)

- **Projection effects** on outflow speed: Metis sees plane-of-
  sky speed; deprojection requires 3D reconstruction or a
  geometric model.
- **Topology-model sensitivity**: the pseudostreamer
  classification is PFSS-dependent; different source-surface
  radii / different magnetograms may classify the same event
  differently.
- **Density-model choice** dominates v_A inference; the
  outflow-vs-v_A claim is sensitive to this.
- **Brightness contamination** from foreground / background
  structures along the line of sight.

### 2.5 Figure / numerical targets

- A time-distance diagram in Metis brightness showing the
  outflow trace.
- Outflow speed lies within a paper-stated band around v_A
  (exact band TODO_verify_with_full_text).
- PFSS topology at the candidate footpoint is pseudostreamer.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-METIS-IMAGE-LOAD**: load Metis VL and UV image stacks
  for a specified time window.
- **C-OUTFLOW-TRACK**: extract v_⊥(t, r) along a user-specified
  slit through the brightness time series.
- **C-PFSS-PSEUDOSTREAMER**: given a synoptic Br input, return
  the null-line / topology map and flag pseudostreamer
  candidates.
- **C-CORONAL-VA**: return v_A(r) at the outflow region from
  the coronal model.
- **C-EUI-SPICE-CROSSCHECK** (optional): footpoint identification
  in SolO EUI / SPICE.

### 3.2 Procedure

1. C-PFSS-PSEUDOSTREAMER on the relevant CR; identify
   candidate pseudostreamer null-lines.
2. C-METIS-IMAGE-LOAD over the candidate event window.
3. C-OUTFLOW-TRACK: extract v_⊥(t, r).
4. C-CORONAL-VA at the outflow region.
5. Report (v_⊥ / v_A, topology_flag, event_window).
6. (Optional) C-EUI-SPICE-CROSSCHECK at the inferred footpoint.

### 3.3 Minimum reproduction artifacts

- Event card with (event_id, topology_flag, v_⊥, v_A, ratio).
- Time-distance figure reproducing the outflow trace from
  Metis brightness.
- PFSS topology figure showing the pseudostreamer at the
  identified Carrington longitude.

### Validation target

A reproduction of this skill is considered honest when:

- The same Metis event is recovered (time window within
  ≲ 30 min of the paper's identification).
- v_⊥ / v_A lies within the paper-stated band (TODO_verify_with_full_text
  for the exact tolerance).
- The PFSS topology at the candidate footpoint is classified
  as a pseudostreamer under the paper's source-surface radius
  choice (or, if a different R_ss is used, the topology change
  is reported explicitly).

---

## 4. Adapter / runtime notes (optional examples)

- Metis Level-2 VL + UV pipelines (SolO MetisDap, SunPy-Metis
  community packages) are example Layer-3 bindings for
  C-METIS-IMAGE-LOAD; none are shipped here.
- pfsspy is an example Layer-3 binding for C-PFSS-PSEUDOSTREAMER.
- aiapy + euipy are example Layer-3 bindings for the optional
  EUI / SPICE crosscheck.

---

## 5. Research-generation affordance

- **Composability with [[ervin-2024-slow-alfvenic-source-regions-pfss-psp]]**:
  slow-Alfvénic streams identified in PSP can be back-projected
  to candidate pseudostreamer footpoints, and Metis-imaged
  outflows at those footpoints provide the corona-side
  evidence.
- **Composability with [[hcs-reconnection-statistics-psp-encounter-2025]]**:
  interchange reconnection at pseudostreamers and steady
  reconnection at the HCS are two distinct contributors to
  slow-wind composition; a joint event-and-statistics study
  can apportion the contributions.
- **Open hypothesis**: Slow-Alfvénic streams in PSP at given
  Carrington longitudes are traceable to specific interchange-
  reconnection events imaged by Metis earlier in the rotation.
- **Gap**: A statistical Metis-pseudostreamer survey is the
  natural next agenda; the paper is single-event and does not
  bound the occurrence rate.
- **Tension with steady-source slow-wind interpretations**:
  steady streamer-belt sources and bursty pseudostreamer
  reconnection both deliver slow wind; the discriminator
  (bursty timing in Metis vs steady-state composition in PSP)
  is the load-bearing measurement.

---

## Links

- arXiv: https://arxiv.org/abs/2502.08015
- DOI: TODO_verify_with_full_text (preprint as of Feb 2025)
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2502.08015`

## Skill graph

- [[ervin-2024-slow-alfvenic-source-regions-pfss-psp]]
- [[hcs-reconnection-statistics-psp-encounter-2025]]
