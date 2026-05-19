# mozer-2021-magnetic-pressure-balance-domains-psp

A paper-skill compiled from Mozer et al. 2021 (ApJ; arXiv:2110.08506).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Detect contiguous intervals of approximate total-pressure stationarity
  ("pressure-balance domains", PBDs) in PSP solar-wind data.
- Pre-segment intervals before turbulence-statistic skills that assume
  stationarity.

### When NOT to use it

- Kinetic-scale compressive modes (Bernstein etc.).
- Plasma where reliable proton + electron temperatures are unavailable
  — the balance test loses leverage.

### Claim boundary

Total-pressure analysis (`P_B + P_th`) on near-Sun PSP intervals reveals
extended domains over which the sum is approximately constant despite
individually large, anti-correlated `δP_B` and `δP_th`. The claim is
bounded to the analysed PSP near-Sun intervals; it is not asserted to
hold globally.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

In near-Sun PSP intervals, contiguous domains exist where
`|δ(P_B + P_th)| / ⟨P_total⟩` stays below a threshold for a documented
minimum duration, even when `δP_B` and `δP_th` individually are large
and anti-correlated.

### 2.2 Equations / method

- `P_B = |B|² / (2 μ_0)`, `P_th = n k_B (T_p + T_e)` (or
  proton-only).
- `P_total = P_B + P_th`; sliding-window mean `⟨P_total⟩_τ`.
- Normalised residual `r(t) = (P_total − ⟨P_total⟩_τ) /
  ⟨P_total⟩_τ`.
- PBD = contiguous interval with `|r(t)| < threshold` for ≥ minimum
  duration.
- Anti-correlation diagnostic `corr(δP_B, δP_th) < −0.5` per PBD.

### 2.3 Data assumptions

- High-cadence `B`, `n`, and at least proton `T` at common time base.
- Electron temperature optional (with explicit proxy if missing).

### 2.4 Failure modes (skill memory)

- **`T_e` missing or uncalibrated** near perihelion; document the
  proxy and its effect on `P_th`.
- **Detrending window length** trades signal vs. boundary smearing.
- **Residual threshold** controls PBD detection sensitivity.
- **Cadence mismatch** between `B` and SWEAP introduces aliasing if
  resampled improperly.
- **Pressure anisotropy.** Scalar `T_p` underestimates `P_th` when the
  proton pressure tensor is anisotropic.

### 2.5 Figure / numerical targets

- Identify at least one PBD in a paper-named interval (TODO verify).
- Per-PBD anti-correlation `corr(δP_B, δP_th) < −0.5`.
- PBD duration distribution shape consistent with paper figure.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG / C-FETCH-MOMENTS**: vector `B`, density, proton
  temperature.
- **C-FETCH-TE** *(optional)*: electron temperature product.
- **C-DETREND**: sliding-window mean over a documented `τ`.
- **C-PBD**: contiguous-interval detector with explicit residual
  threshold and minimum duration.
- **C-ANTICORR**: correlation between `δP_B` and `δP_th` per PBD.

### 3.2 Procedure

1. C-FETCH-MAG + C-FETCH-MOMENTS (+ C-FETCH-TE if available).
2. Co-register to a common cadence.
3. Compute `P_B`, `P_th`, `P_total`.
4. C-DETREND with documented `τ`.
5. C-PBD with documented threshold + minimum duration.
6. C-ANTICORR per PBD; flag non-trivial balance.
7. Aggregate PBD statistics over the window.

### 3.3 Minimum reproduction artifacts

- PBD list JSON with `τ`, threshold, minimum duration, and `T_e` proxy
  recorded.
- Anti-correlation CSV.
- Time-series PNG of `P_B`, `P_th`, `P_total` overlaid.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with CDF I/O + sliding-window math satisfies the
  contracts.
- LingTai HelioSI may bind C-FETCH-TE to an internal `psp-electron-
  loader` skill — one binding option.

---

## 5. Research-generation affordance

- **Composability with turbulence-statistic skills**: PBDs are natural
  stationarity windows for PSD slope and structure-function analyses.
  A turbulence-statistics paper-skill (e.g.
  [[shoda-2021-turbulence-switchback-generation-alfvenic]] for sim-vs-
  obs comparison; or future
  [[bowen-2023-landau-damping-proton-electron-heating]]) gains
  cleaner statistics by gating on PBDs.
- **Composability with switchback skills**: do switchback patches sit
  preferentially inside or outside PBDs? Intersecting the catalogs
  ([[bale-2021-solar-source-switchbacks-magnetic-funnels]] for
  patches) gives a free statistic the field has not reported.
- **Open hypothesis**: PBD occurrence vs. heliocentric distance and
  vs. wind type (slow vs. fast Alfvénic) is sparsely characterised; a
  systematic survey using this protocol is a natural follow-up.

---

## Links

- arXiv: https://arxiv.org/abs/2110.08506
- DOI: TODO verify with full text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §2.12;
  `extended_search.md` §3.7

## Skill graph

- [[wang-2020-magnetic-holes-psp-solar-wind]] — sibling small-scale
  structure (a magnetic hole is a special PBD with extreme `|B|`
  dip).
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — boundary
  diagnostic on the same time series.
- [[kasper-2021-psp-enters-magnetically-dominated-corona]] — `β` /
  Alfvén-Mach context.
