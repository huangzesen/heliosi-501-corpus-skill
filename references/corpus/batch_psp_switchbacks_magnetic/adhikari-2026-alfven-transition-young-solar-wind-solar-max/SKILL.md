---
name: adhikari-2026-alfven-transition-young-solar-wind-solar-max
description: Per-entry paper-skill in batch_psp_switchbacks_magnetic (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# adhikari-2026-alfven-transition-young-solar-wind-solar-max

A paper-skill compiled from Adhikari et al. 2026 (ApJ 997, 2;
doi:10.3847/1538-4357/ae2c78).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (Claude Code, LingTai, Codex, a researcher) may satisfy those
contracts.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Label PSP intervals as sub- vs. super-Alfvénic with a documented
  Alfvén-Mach-number statistic.
- Compare PSP-sampled Alfvén-transition positions to solar-maximum
  source-surface predictions.
- Provide statistical labelling upstream of turbulence / reconnection
  / wind-classification skills.

### When NOT to use it

- *Causal* decomposition of sub-Alfvénic excursions (low density vs.
  low velocity vs. enhanced `|B|`) — that needs conditioning by sibling
  skills.
- Mapping the full 3D Alfvén surface — the paper bounds itself to PSP-
  sampled regions.

### Claim boundary

Statistical analysis of `M_A` and sub-Alfvénic interval occurrence in
PSP encounters approaching solar maximum, with comparison to solar-
maximum source-surface predictions in the regions PSP traversed. Not a
global Alfvén-surface map.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Across PSP encounters approaching solar maximum, the statistics of
`M_A = v_sw / V_A` and the occurrence of sub-Alfvénic intervals are
consistent with an Alfvén-surface geometry predicted by solar-maximum
source-surface models in the regions PSP traversed.

### 2.2 Equations / method

- `V_A = |B| / √(μ_0 ρ)` with an explicit density proxy.
- `M_A = v_sw / V_A` per sample, in the solar inertial frame.
- Hysteretic detection of sub-Alfvénic intervals (`M_A < 1`) with a
  minimum dwell time.
- Source-surface prediction (PFSS from ADAPT / HMI / GONG) projected
  to PSP's trajectory.

### 2.3 Data assumptions

- High-cadence vector magnetic field and bulk velocity at PSP.
- A density proxy with a known systematic (proton vs. electron, with
  or without QTN correction).
- A synoptic photospheric magnetogram for the PFSS prediction.
- Spacecraft ephemeris in the solar inertial frame.

### 2.4 Failure modes (skill memory)

- **Density proxy** directly shifts `V_A` and `M_A`.
- **Hysteresis filter** thresholds control sub-Alfvénic interval count.
- **Source-surface model selection** (ADAPT vs. HMI vs. GONG; source-
  surface radius) is non-unique — pick one and document.
- **Activity-index choice** required to bind "approaching solar maximum"
  to an explicit time window.
- **Frame.** `v_sw` must be in the solar inertial frame, not the
  spacecraft frame.

### 2.5 Figure / numerical targets

- Recover at least one named sub-Alfvénic interval (TODO verify).
- Sign of sub-Alfvénic occurrence trend across encounters matches paper
  (TODO verify sign).
- `M_A` PDF shape matches paper figure (peak + tail).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG**: high-cadence vector `B`.
- **C-FETCH-BULK**: `v_sw`, proton density.
- **C-FETCH-NE** *(optional)*: QTN-derived electron density.
- **C-FETCH-EPHEM**: spacecraft position in solar inertial frame.
- **C-PFSS**: extrapolate a synoptic magnetogram to a source surface
  and project to a given trajectory.
- **C-DETECT-SUBA**: hysteretic detection of `M_A < 1` intervals with
  configurable dwell time.

### 3.2 Procedure

1. C-FETCH-MAG, C-FETCH-BULK, C-FETCH-EPHEM over the analysis window.
2. Choose density proxy (proton; or electron via C-FETCH-NE).
3. Compute `V_A` and `M_A` per sample.
4. Apply C-DETECT-SUBA.
5. C-PFSS prediction for the matching epoch; project to PSP
   trajectory.
6. Per encounter: sub-Alfvénic fraction, `M_A` PDF, comparison panel
   against the projected Alfvén-surface.
7. Aggregate across the encounter set.

### 3.3 Minimum reproduction artifacts

- Per-encounter `M_A_stats.json` and sub-Alfvénic interval list.
- `M_A` PDF figure with density-proxy and hysteresis parameters
  recorded.
- Source-surface comparison panel with the model + epoch explicit.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with `WebFetch` + a CDF reader + a PFSS implementation
  (e.g. `pfsspy`) can satisfy the contracts.
- LingTai HelioSI may bind C-FETCH-* to a `cdaweb`-style adapter and
  C-PFSS to an internal `pfss-source-surface-mapper` skill; this is
  one of many possible bindings and is *not* required.

---

## 5. Research-generation affordance

- **Bridge to [[kasper-2021-psp-enters-magnetically-dominated-corona]]**:
  apply the *same* detector + density proxy to E8 and to solar-max
  encounters; quantify whether the apparent "Alfvén-surface motion"
  is a physical solar-cycle signal or an artefact of changing density
  proxies / activity indices.
- **Open hypothesis**: does the sub-Alfvénic occurrence rate scale with
  active-region area or with coronal-hole boundary length? The paper
  reports occurrence vs. activity index (TODO verify); a finer driver
  attribution is unreported.
- **Composability with switchback skills**: switchback occurrence is
  known to suppress in sub-Alfvénic intervals; cross-tabulate this
  paper-skill's sub-Alfvénic catalog with
  [[agapitov-2023-structure-origin-switchbacks-psp]] to test the
  suppression quantitatively across encounters.
- **Open methodological gap**: a comparison to **non-PFSS** Alfvén-
  surface models (MHD coronal simulations) is absent in the inventory;
  rerunning with an MHD-derived Alfvén surface would test the PFSS
  assumption.

---

## Links

- DOI: https://doi.org/10.3847/1538-4357/ae2c78
- arXiv: TODO verify with full text
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.6

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]] — solar-
  minimum first-crossing baseline.
- [[agapitov-2023-structure-origin-switchbacks-psp]] — switchback
  suppression cross-test.
- [[bale-2021-solar-source-switchbacks-magnetic-funnels]] — PFSS
  footpoint-mapping companion (same source-surface formalism).
