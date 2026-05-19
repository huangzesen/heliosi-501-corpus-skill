---
name: bale-2021-solar-source-switchbacks-magnetic-funnels
description: Per-entry paper-skill in batch_psp_switchbacks_magnetic (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# bale-2021-solar-source-switchbacks-magnetic-funnels

A paper-skill compiled from Bale, Horbury, Velli, Desai, Halekas, et
al. 2021 (ApJ; arXiv:2109.01069).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Apply the canonical *solar-surface-origin* hypothesis for Alfvénic
  switchback patches.
- Map a PSP switchback-patch catalog back to photospheric longitude
  via PFSS and ballistic propagation.

### When NOT to use it

- As a *unique* explanation: competing hypotheses exist
  ([[shoda-2021-turbulence-switchback-generation-alfvenic]]).
- Below the patch scale; the supergranulation-match argument is about
  patch *spacing*, not individual switchback structure.

### Claim boundary

Switchback-patch *spacing*, when mapped to the photosphere via PFSS,
matches the supergranulation scale. The claim is patch-level and bounded
to the analysed encounters; it does not assert a 1-to-1 mapping of
individual switchbacks to funnels.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

The longitudinal spacing of switchback patches observed by PSP,
mapped via PFSS to the photosphere, matches the supergranulation
scale (~ 30 Mm), supporting interpretation of patches as in-situ
remnants of magnetic funnels at supergranulation boundaries.

### 2.2 Equations / method

- Patch detection via quiescent-gap clustering of switchback events.
- Footpoint mapping: PFSS from a synoptic magnetogram + ballistic
  propagation with locally measured `v_sw` to the source surface.
- Inter-patch photospheric longitude spacing Δλ.
- Conversion of Δλ to physical distance at `R_sun`.

### 2.3 Data assumptions

- A switchback event catalog at PSP with documented threshold.
- Bulk velocity for ballistic propagation.
- A synoptic photospheric magnetogram covering the conjunction epoch.
- A PFSS implementation with documented source-surface radius.

### 2.4 Failure modes (skill memory)

- **Patch definition.** Requires a clustering rule (gap threshold);
  the scale-comparison conclusion depends on it.
- **PFSS source-surface radius.** 2.5 R_sun is conventional but not
  unique; sweep.
- **Ballistic propagation.** `v_sw` evolution causes footpoint drift;
  document the propagation scheme.
- **Magnetogram epoch.** Synoptic vs. snapshot differ; cite epoch.
- **Confounding scales.** Granulation, mesogranulation, and active-
  region scales are nearby; statistical-significance check required.

### 2.5 Figure / numerical targets

- Median inter-patch photospheric spacing within a factor of 2 of the
  supergranulation scale (~ 30 Mm).
- Patch-detection recall ≈ paper ±20% on a named encounter (TODO
  verify encounter list).
- Heavy-tail-at-small-spacings distribution shape qualitatively
  matches the paper.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG / C-FETCH-BULK**: PSP `B` and `v_sw`.
- **C-CATALOG-PATCHES**: cluster switchback events into patches by a
  documented quiescent-gap rule.
- **C-FETCH-MAGNETOGRAM**: photospheric synoptic map at the encounter
  epoch.
- **C-PFSS**: PFSS extrapolation to a documented source-surface radius.
- **C-BALLISTIC**: ballistic back-trace from PSP to the source surface
  using locally measured `v_sw`.
- **C-PHOTO-SPACING**: convert per-patch source-surface longitudes to
  inter-patch photospheric spacing.

### 3.2 Procedure

1. C-FETCH-MAG + C-FETCH-BULK over the analysis window.
2. C-CATALOG-PATCHES with explicit gap threshold.
3. C-FETCH-MAGNETOGRAM at the matching epoch.
4. C-PFSS + C-BALLISTIC for each patch to obtain photospheric
   footpoints.
5. C-PHOTO-SPACING: compute inter-patch distances at `R_sun`.
6. Compare distribution to the supergranulation scale; run
   statistical-significance check against random spacing.

### 3.3 Minimum reproduction artifacts

- Patch-spacing histogram PNG with gap threshold and source-surface
  radius recorded.
- Footpoint-mapping CSV.
- Scale-comparison JSON (mean, median, KS statistic vs. random).

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with PSP CDF I/O + a PFSS implementation (`pfsspy` or
  equivalent) + synoptic-map ingestion can satisfy the contracts.
- LingTai HelioSI may bind C-PFSS to an internal `pfss-footpoint-mapper`
  skill — one binding option, not a requirement.

---

## 5. Research-generation affordance

- **Direct tension with [[shoda-2021-turbulence-switchback-generation-alfvenic]]**:
  two distinct mechanisms predict different *joint* distributions of
  patch spacing and per-event spherical-polarisation. A discriminating
  experiment computes both quantities on the same PSP interval and
  fits a mixture model.
- **Composability with [[agapitov-2023-structure-origin-switchbacks-psp]]**:
  conditioning supergranulation-match analysis on the RD-classified
  subset of patches tests whether the boundary-geometry subset
  preferentially aligns with funnel boundaries.
- **Open hypothesis**: does the supergranulation match persist beyond
  the early encounters analysed in the paper? A multi-encounter rerun
  using the same protocol is the experiment.
- **Methodological gap**: sensitivity to source-surface radius is not
  systematically reported; a sweep over `R_ss ∈ {1.5, 2.0, 2.5, 3.0}`
  R_sun would quantify the dependence.

---

## Links

- arXiv: https://arxiv.org/abs/2109.01069
- DOI: TODO verify with full text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.11

## Skill graph

- [[shoda-2021-turbulence-switchback-generation-alfvenic]] — competing
  generation hypothesis.
- [[agapitov-2023-structure-origin-switchbacks-psp]] — RD-subset
  conditioning.
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — boundary
  statistics for patch interior.
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]] — PFSS
  / source-surface companion formalism.
