---
name: wang-2020-magnetic-holes-psp-solar-wind
description: Per-entry paper-skill in batch_psp_switchbacks_magnetic (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# wang-2020-magnetic-holes-psp-solar-wind

A paper-skill compiled from Wang et al. 2020 (ApJ; arXiv:2010.14008).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Catalog magnetic holes (sharp `|B|` drops with approximate total-
  pressure balance) in PSP intervals.
- Report scale-size, depth, and inter-event spacing statistics, in
  solar-cycle context.

### When NOT to use it

- Kinetic-scale mirror modes — distinct β-anisotropy conditioning is
  required, which this skill does not enforce.

### Claim boundary

Automated detection of magnetic holes on PSP FIELDS data with scale-
size and depth statistics, placed in solar-cycle context. Bounded to
the detector's threshold definition and to the analysed encounters.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Localized intervals where `|B|` drops by more than a threshold below
the local mean for at least a minimum duration are detectable in PSP
FIELDS data; their depth, scale-size, and inter-event spacing form
measurable distributions consistent with the early-mission solar-cycle
context.

### 2.2 Equations / method

- Sliding-window mean `⟨|B|⟩_τ`.
- Candidate hole: contiguous interval with `|B| / ⟨|B|⟩_τ < 1 − Δ_threshold`
  for ≥ minimum duration.
- Shape check: symmetric dip + recovery to baseline.
- Per-hole metrics: depth, time duration, scale-size `L = v_sw · Δt`
  via Taylor hypothesis, asymmetry.

### 2.3 Data assumptions

- High-cadence vector `B` from PSP FIELDS.
- Bulk velocity for Taylor-hypothesis scale conversion.

### 2.4 Failure modes (skill memory)

- **Threshold definition.** Communities use 50% / 75% / 90% — fix and
  document.
- **Sliding-window length.** Too short cancels real holes; too long
  over-counts.
- **Taylor breakdown.** At sub-Alfvénic conditions Taylor needs
  correction.
- **Confusion with current sheets.** Cross-check `B`-rotation.
- **Calibration epoch.** Use up-to-date L2 products.

### 2.5 Figure / numerical targets

- Magnetic-hole count for a paper-named encounter window within ±25%
  of the published value (TODO verify).
- Depth distribution peak consistent with paper (TODO verify peak
  value).
- Heavy-tail scale-size distribution qualitatively consistent with
  paper.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG**: high-cadence vector `B`.
- **C-FETCH-BULK**: `v_sw` for Taylor conversion.
- **C-DETREND-B**: sliding-window mean of `|B|` over documented `τ`.
- **C-DETECT-HOLE**: contiguous-interval detector with depth threshold
  + minimum duration.
- **C-SHAPE-CHECK**: reject false positives by symmetry + recovery
  test.
- **C-FEATURES**: per-hole depth, duration, scale-size, asymmetry.

### 3.2 Procedure

1. C-FETCH-MAG + C-FETCH-BULK over the analysis window.
2. C-DETREND-B with documented `τ`.
3. C-DETECT-HOLE → candidate list.
4. C-SHAPE-CHECK → confirmed holes.
5. C-FEATURES per hole; record `M_A` regime for Taylor validity.
6. Aggregate; tag with activity index for solar-cycle context.

### 3.3 Minimum reproduction artifacts

- Hole-catalog CSV with depth threshold, `τ`, and Taylor regime
  recorded.
- Depth and scale-size histogram PNGs.
- Summary JSON with encounter coverage + activity index.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with PSP CDF I/O + standard signal processing satisfies
  the contracts.
- LingTai HelioSI may bind C-DETECT-HOLE to an internal hole-finder
  skill — one binding option.

---

## 5. Research-generation affordance

- **Composability with [[mozer-2021-magnetic-pressure-balance-domains-psp]]**:
  magnetic holes are extreme PBDs. Intersecting the catalogs answers
  whether all holes sit inside PBDs (expected) and whether PBDs
  dominate the wind near holes (open).
- **Composability with [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]**
  and [[kasper-2021-psp-enters-magnetically-dominated-corona]]:
  conditioning hole occurrence on `M_A` regime tests whether the
  Taylor-hypothesis bias is large enough to distort the reported
  scale-size distribution.
- **Open hypothesis**: dependence of hole occurrence rate on
  heliocentric distance and on wind type. Reanalyse with this protocol
  across all encounters with consistent parameters.
- **Methodological experiment**: sensitivity to depth threshold ∈
  {30%, 50%, 75%}; the inventory does not characterise this.

---

## Links

- arXiv: https://arxiv.org/abs/2010.14008
- DOI: TODO verify with full text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §3.1

## Skill graph

- [[mozer-2021-magnetic-pressure-balance-domains-psp]] — PBD super-set.
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — sibling
  small-scale-structure catalog.
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]] —
  `M_A` regime conditioning.
