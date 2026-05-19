# kasper-2021-psp-enters-magnetically-dominated-corona

A paper-skill compiled from Kasper, Klein, Lichko, Huang, et al. 2021
(PRL 127, 255101; doi:10.1103/PhysRevLett.127.255101).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify and characterise the first sub-Alfvénic PSP intervals
  (Encounter 8).
- Estimate a trajectory-projected Alfvén radius from PSP plasma +
  field data.

### When NOT to use it

- Population-level Alfvén-transition statistics — see
  [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]].
- Extending Encounter-8 findings to other encounters without rerunning
  the protocol.

### Claim boundary

First PSP sub-Alfvénic intervals during Encounter 8, with Alfvén-surface
diagnostics from SWEAP + FIELDS. Bounded to those E8 intervals; not a
global Alfvén-surface map.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

During PSP Encounter 8, the spacecraft crossed intervals with
`M_A = v_sw / V_A < 1` and `β_total < 1`, identifying the first in-situ
entries into the magnetically dominated solar corona.

### 2.2 Equations / method

- `V_A = |B| / √(μ_0 ρ)` with documented density proxy.
- `M_A = v_sw / V_A` in the solar inertial frame.
- `β_total = (P_p + P_e) / P_B`, with `P_B = |B|² / (2 μ_0)`.
- Hysteretic detection of `M_A < 1` intervals.
- Trajectory-projected Alfvén-radius extraction at `M_A = 1` crossings.

### 2.3 Data assumptions

- High-cadence vector `B` during E8.
- Bulk + density at matching cadence (with explicit choice: proton
  moments, QTN-derived `n_e`, or both).
- Spacecraft ephemeris in the solar inertial frame.

### 2.4 Failure modes (skill memory)

- **Density-proxy choice** shifts `V_A` and the count of sub-Alfvénic
  intervals.
- **Hysteresis filter** parameters control short-dropout suppression.
- **Temperature anisotropy.** Scalar `T` underestimates `P_p` when the
  pressure tensor is anisotropic.
- **Frame.** `v_sw` must be in the solar inertial frame.
- **Trajectory-projected Alfvén radius.** PSP's `M_A = 1` crossings
  define a one-dimensional projection, not the global surface.

### 2.5 Figure / numerical targets

- Recover at least one E8 sub-Alfvénic interval within ~1 min of the
  paper's published boundaries (TODO verify boundaries).
- `β_total < 1` during the interval.
- Trajectory-projected Alfvén-radius estimate matches the paper at the
  corresponding heliocentric distance.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG**: high-cadence vector `B` at PSP.
- **C-FETCH-BULK**: bulk velocity + proton moments.
- **C-FETCH-NE** *(optional)*: QTN-derived electron density.
- **C-FETCH-EPHEM**: PSP position in the solar inertial frame.
- **C-DETECT-SUBA**: hysteretic `M_A < 1` detection.
- **C-BETA**: `β_total` computation from the same data.

### 3.2 Procedure

1. Restrict to the E8 perihelion window.
2. C-FETCH-MAG + C-FETCH-BULK (+ C-FETCH-NE if available).
3. Compute `V_A`, `M_A`, `β_total`.
4. C-DETECT-SUBA with documented hysteresis parameters.
5. Intersect with C-FETCH-EPHEM to locate `M_A = 1` crossings; record
   the projected Alfvén radius.
6. Compare to paper boundaries.

### 3.3 Minimum reproduction artifacts

- `e8_subAlfvenic_intervals.json` with hysteresis parameters recorded.
- β-time-series PNG.
- Derived-Alfvén-radius CSV with the density proxy explicit.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness that can read PSP CDF files (or fetch them over HTTP) and
  do basic vector arithmetic satisfies the contracts.
- LingTai HelioSI may bind C-FETCH-NE to an internal QTN-density skill;
  the contract is satisfied either way.

---

## 5. Research-generation affordance

- **Composability with [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]**:
  apply identical density-proxy and hysteresis parameters to E8 and to
  solar-max encounters; differences in `M_A` PDF or sub-Alfvénic
  occurrence become physically interpretable (cycle effect) rather
  than methodological.
- **Open hypothesis**: do sub-Alfvénic excursions correlate with
  pressure-balance-domain crossings ([[mozer-2021-magnetic-pressure-
  balance-domains-psp]])? A simple intersection of catalogs answers
  this and is unreported in the inventory.
- **Open hypothesis**: are switchbacks systematically absent inside
  the E8 sub-Alfvénic intervals (consistency with later mission
  findings)? Composing with switchback catalogs from this batch
  quantifies the suppression.

---

## Links

- DOI: https://doi.org/10.1103/PhysRevLett.127.255101
- arXiv: TODO verify
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.9

## Skill graph

- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]] —
  solar-maximum statistical follow-up.
- [[mozer-2021-magnetic-pressure-balance-domains-psp]] — pressure-
  balance cross-test.
- [[agapitov-2023-structure-origin-switchbacks-psp]] — switchback-
  suppression check inside the sub-Alfvénic intervals.
