---
name: agapitov-2020-localized-magnetic-structures-boundaries
description: Per-entry paper-skill in batch_psp_switchbacks_magnetic (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# agapitov-2020-localized-magnetic-structures-boundaries

A paper-skill compiled from Agapitov, Dudok de Wit, Mozer, et al. 2020
(ApJS; arXiv:2003.05409).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Catalog small-scale localized magnetic kinks / switchbacks (including
  full `B_R` reversals) in near-Sun PSP data, and characterise their
  boundaries.
- Provide a boundary-statistics foundation for downstream classifier
  skills.

### When NOT to use it

- *Origin* questions; this paper-skill is structural, not generative.
- Scales above MHD; the analysis is at near-native FIELDS cadence.

### Claim boundary

Statistical characterisation of small-scale magnetic kinks (some with
full `B_R` reversal) and their boundaries in early-PSP near-Sun
intervals via variance analysis on FIELDS waveforms. Bounded to the
analysed intervals and to the chosen detection criteria.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

In near-Sun PSP intervals, localized magnetic structures with sudden
deflections — including full `B_R` reversals — are present, and their
boundary widths, deflection amplitudes, and inter-event spacings form
measurable distributions that vary with heliocentric distance.

### 2.2 Equations / method

- Running statistics on `B_R / |B|` over a documented window.
- Event detection: deflection of `|B_R| / |B|` past a threshold (full
  reversal: sign change of `B_R / |B|`).
- Boundary localisation by sharp gradients in `B_R / |B|` and `|B|`.
- Per-event features: amplitude, duration, boundary-width, local
  `|B|` variation.

### 2.3 Data assumptions

- High-cadence vector `B` (native FIELDS waveform where available).
- Spacecraft ephemeris (for heliocentric-distance binning).

### 2.4 Failure modes (skill memory)

- **Threshold dependence.** Event counts depend strongly on the
  threshold.
- **Cadence sensitivity.** Boundary-width measurement requires high
  cadence; subsampling biases widths upward.
- **`|B|` plateau requirement** for "true" switchback definition;
  cite which subset satisfies it.
- **Window selection.** Short windows miss extended events; long
  windows blend events.
- **Hand-curation gap.** Paper samples may be hand-curated; reproduce
  with explicit automated thresholds.

### 2.5 Figure / numerical targets

- Detect a population of full-reversal structures in a paper-named
  interval (TODO verify interval list).
- Boundary-width distribution shape (sharp tail at small widths)
  consistent with paper figure.
- Sign of inter-event-spacing trend with heliocentric distance
  matches paper (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG**: high-cadence vector `B`.
- **C-FETCH-EPHEM**: heliocentric distance per sample.
- **C-DETECT-DEFLECTION**: threshold-based event detector on
  `B_R / |B|` with explicit window and threshold.
- **C-BOUNDARY**: locate entry/exit boundary via gradient peaks.
- **C-FEATURES**: per-event amplitude, duration, boundary width,
  local `|B|` variation.
- **C-BIN-R**: heliocentric-distance binning of population
  statistics.

### 3.2 Procedure

1. C-FETCH-MAG + C-FETCH-EPHEM over the analysis window.
2. C-DETECT-DEFLECTION with documented threshold + window.
3. C-BOUNDARY per detected event.
4. C-FEATURES per event.
5. C-BIN-R to compute population distributions.
6. Compare to paper figures.

### 3.3 Minimum reproduction artifacts

- Event-list CSV with threshold + window recorded.
- Distribution PNGs (amplitude, duration, boundary width).
- `r`-binned statistics JSON.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with CDF I/O + edge-detection math satisfies the
  contracts.
- LingTai HelioSI may bind C-DETECT-DEFLECTION to a `switchback-
  boundary-finder` skill; one binding among many.

---

## 5. Research-generation affordance

- **Foundational composability**: this skill provides the boundary
  catalog consumed by [[agapitov-2023-structure-origin-switchbacks-psp]]
  (geometric classification),
  [[phan-2022-switchback-boundary-reconnection-psp]] (exhaust
  diagnostic), and
  [[phan-2023-switchback-boundaries-closed]] (topology).
- **Open hypothesis**: full-reversal structures and partial-deflection
  structures may obey different inter-event spacing laws; the paper
  does not separate them in detail (TODO verify).
- **Bridge to generation hypotheses**: matched-detector outputs from
  this skill applied to a turbulence-origin simulation
  ([[shoda-2021-turbulence-switchback-generation-alfvenic]]) and a
  solar-origin reconstruction
  ([[bale-2021-solar-source-switchbacks-magnetic-funnels]]) give a
  direct head-to-head test against the same boundary-width
  distribution.
- **Methodological experiment**: vary the deflection threshold over
  ranges spanning {30°, 60°, 90°, 120°, 160°} and quantify how the
  population distributions scale — the systematic is unreported in
  the inventory.

---

## Links

- arXiv: https://arxiv.org/abs/2003.05409
- DOI: TODO verify with full text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §2.13;
  `extended_search.md` §3.2

## Skill graph

- [[agapitov-2023-structure-origin-switchbacks-psp]] — classification
  on top of this boundary catalog.
- [[phan-2022-switchback-boundary-reconnection-psp]] — exhaust
  diagnostic.
- [[phan-2023-switchback-boundaries-closed]] — topology follow-up.
- [[bale-2021-solar-source-switchbacks-magnetic-funnels]] — solar-
  origin hypothesis depending on this catalog.
- [[shoda-2021-turbulence-switchback-generation-alfvenic]] — turbulence-
  origin hypothesis to be tested against this catalog.
