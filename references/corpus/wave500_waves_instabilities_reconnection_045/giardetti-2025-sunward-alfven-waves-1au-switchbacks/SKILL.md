---
name: giardetti-2025-sunward-alfven-waves-1au-switchbacks
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# giardetti-2025-sunward-alfven-waves-1au-switchbacks

A paper-skill compiled from N. Giardetti, S. Bourouaine, J. C. Perez et al. 2025 (TODO_verify_journal; arXiv:2512.18806).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify sunward-propagating Alfvén-wave (SAW) intervals in Wind data near 1 au and quantify their occurrence rate.
- Test whether SAW intervals are spatially co-located with large-scale magnetic switchbacks (SBs).

### When NOT to use it

- Near-Sun SAW dynamics — see [[verniero-2020-proton-beams-ion-scale-waves]] / kasper-2021.
- Switchback boundary reconnection — see [[phan-2022-switchback-boundary-reconnection-psp]].

### Claim boundary

>20 years of Wind data near 1 au. SAW classification uses normalized cross helicity, incompressibility, and HMF polarity to fix propagation sign. Association is reported for 1-hour scale; results vary with timescale and stream type.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

SAW occurrence rate near 1 au ranges ~1%–14% depending on timescale and stream type; among 1636 1-hour SAW intervals, 17.5% are associated with switchbacks at scales >1 h.

### 2.2 Equations / method

- Elsässer increments z^± = δV ∓ δB/√(μ_0 ρ); σ_c = (|z^+|^2 − |z^-|^2)/(|z^+|^2 + |z^-|^2).
- Propagation sign fixed by HMF polarity + sign of σ_c.
- Plasma + magnetic compressibility thresholds for AW classification.
- Strahl pitch-angle distribution to identify inverted magnetic topology.

### 2.3 Data assumptions

- Wind MAG + 3DP / SWE bulk plasma + strahl-electron data over >20 years.
- Stable HMF polarity baseline (e.g., 24-hour averaging).
- Stream-type catalog (fast/slow/transient).

### 2.4 Failure modes (skill memory)

- **Polarity-ambiguity intervals** (HCS crossings) corrupt sign of propagation — must mask.
- **Compressibility thresholds** alter SAW count; sweep and report.
- **Stream-type labeling** is heuristic; choice (e.g., Xu–Borovsky vs |V|-threshold) changes 1%–14% range.
- **Strahl-coverage gaps** bias inverted-topology fraction.
- **Timescale dependence**: rate varies strongly with windowing.

### 2.5 Figure / numerical targets

- SAW occurrence rate range 1–14% across timescales and streams (TODO verify exact bins).
- 17.5% of 1-hour SAW intervals associated with >1 h SBs (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-WIND-MAG-PLASMA**: Wind vector B, V, n.
- **C-FETCH-STRAHL**: pitch-angle distribution of suprathermal electrons.
- **C-AW-CLASSIFY**: σ_c-, polarity-, compressibility-based SAW classifier.
- **C-SB-CATALOG**: large-scale switchback list using strahl-PAD inversion.
- **C-OVERLAP-STATS**: temporal-overlap statistics between SAW and SB intervals.

### 3.2 Procedure

1. C-FETCH-WIND-MAG-PLASMA + C-FETCH-STRAHL over the >20 yr archive.
2. Compute σ_c, compressibility on the chosen timescale.
3. C-AW-CLASSIFY: SAW vs outward-AW vs non-AW.
4. C-SB-CATALOG: PAD-based SB boundaries.
5. C-OVERLAP-STATS: report SAW-rate and SAW∩SB fraction by stream.

### 3.3 Minimum reproduction artifacts

- Per-interval SAW classification JSON.
- Stream-type-binned occurrence-rate table.
- SAW∩SB overlap CSV with documented timescale.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with CDF I/O and Elsässer increment computation satisfies the contracts.
- PySPEDAS + sw-scanner are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[shoda-2021-turbulence-switchback-generation-alfvenic]]**: if SBs locally invert the radial field, expected sunward-AW fraction inside SBs is fully predictable — test the joint statistic.
- **Composability with [[bale-2021-solar-source-switchbacks-magnetic-funnels]]**: encounter-scan whether SAW intervals at 1 au map back to funnel-rooted streams via PFSS.
- **Open hypothesis**: Are sunward-AW intervals signatures of *inverted* outward propagation inside SBs (kinematic illusion), or genuine inward-driven AW from interior dynamics? Cross-validate with Walén sign on adjacent boundaries.
- **Methodological experiment**: vary the timescale window and report SAW-rate curves — the 1%–14% spread is a known systematic that has not been published as a one-figure curve.

---

## Links

- arXiv: https://arxiv.org/abs/2512.18806
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.18806`

## Skill graph

- [[shoda-2021-turbulence-switchback-generation-alfvenic]]
- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
- [[phan-2022-switchback-boundary-reconnection-psp]]

