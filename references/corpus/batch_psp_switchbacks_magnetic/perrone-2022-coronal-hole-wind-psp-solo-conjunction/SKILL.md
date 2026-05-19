# perrone-2022-coronal-hole-wind-psp-solo-conjunction

A paper-skill compiled from Perrone, Perri, Bruno, Stansby, D'Amicis,
Jagarlamudi, et al. 2022 (A&A 668, A189; doi:10.1051/0004-6361/202243989).

Paper-skills are **harness-agnostic**: they describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Track a coronal-hole stream radially through the inner heliosphere
  via a PSP + Solar Orbiter conjunction.
- Compare bulk + turbulence diagnostics of the same stream at multiple
  heliocentric distances.

### When NOT to use it

- Transient (CME / SIR) propagation between spacecraft.
- Population-level cross-spacecraft turbulence laws (the paper is a
  single-conjunction case study).

### Claim boundary

A single PSP + SO conjunction sampling a coronal-hole stream at
multiple heliocentric distances; the reported radial evolution of bulk
and turbulence properties applies to that conjunction. Not a
population-level law.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

For a PSP + SO conjunction sampling the same coronal-hole stream at
different heliocentric distances, bulk-property and turbulence
diagnostics (cross-helicity `σ_c`, residual energy `σ_R`, inertial-
range spectral slope, density-fluctuation amplitude) evolve radially
in a way consistent with expansion-driven turbulence relaxation.

### 2.2 Equations / method

- Bulk moments and `|B|` at each spacecraft.
- Elsässer variables `z± = δv ± δB / √(μ_0 ρ)`, then `σ_c =
  (⟨|z+|²⟩ − ⟨|z−|²⟩) / (⟨|z+|²⟩ + ⟨|z−|²⟩)` and `σ_R = (⟨|δv|²⟩ −
  ⟨|δB̂|²⟩) / (⟨|δv|²⟩ + ⟨|δB̂|²⟩)` with `δB̂ = δB / √(μ_0 ρ)`.
- Inertial-range PSD slope on the trace magnetic spectrum over a
  fixed scale window.
- Compressibility: `δn / n` and `δ|B| / |B|`.

### 2.3 Data assumptions

- Co-temporal bulk + magnetic field at PSP and SO during the
  conjunction.
- An EUV synoptic / coronal-hole map at the encounter epoch (for
  origin confirmation).
- Consistent coordinate frame between the two spacecraft (e.g. both
  rotated to RTN).

### 2.4 Failure modes (skill memory)

- **Conjunction selection.** Small HGI-longitude separation required.
- **Stream contamination.** Mixed slow-wind interval inflates
  compressibility — apply wind-type filter.
- **PSD-method dependence.** Welch vs. multitaper vs. wavelet gives
  different slopes; fix the estimator.
- **Frame mixing.** RTN(PSP) vs. SRF(SO) without rotation produces
  spurious differences.
- **Time-lag uncertainty.** Imperfect Parker-spiral propagation
  broadens the matched window — sweep the lag.

### 2.5 Figure / numerical targets

- Sign and magnitude of `σ_c` trend PSP → SO match paper (TODO verify).
- Inertial-range slope at SO consistent with −5/3 or −3/2.
- Density-fluctuation amplitude within ±30% of paper.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-PSP**: bulk + `B` at PSP.
- **C-FETCH-SO**: bulk + `B` at SO.
- **C-FETCH-EUV** *(optional)*: EUV synoptic / coronal-hole map at
  the conjunction epoch.
- **C-ELSASSER**: compute `z±`, `σ_c`, `σ_R` over a documented scale
  band.
- **C-PSD**: compute the trace magnetic PSD with a fixed estimator.
- **C-COMPRESSIBILITY**: compute `δn / n`, `δ|B| / |B|`.
- **C-FRAME-ROTATE**: rotate SO into the PSP frame consistently.

### 3.2 Procedure

1. C-FETCH-PSP, C-FETCH-SO, C-FRAME-ROTATE over the conjunction
   window.
2. *(Optional)* C-FETCH-EUV to confirm coronal-hole footpoint at each
   spacecraft.
3. Per spacecraft: bulk summary `(v_sw, n_p, T_p, |B|)`.
4. C-ELSASSER over a common scale band.
5. C-PSD with a documented method and fixed scale window.
6. C-COMPRESSIBILITY at each spacecraft.
7. Assemble radial-evolution table {PSP, SO} × {bulk, σ_c, σ_R,
   slope, compressibility}; compare to paper figures.

### 3.3 Minimum reproduction artifacts

- Per-spacecraft summary JSON with PSD estimator and scale window
  recorded.
- Radial-evolution table CSV.
- PSD overlay PNG.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with PSP + SO CDF readers + Python signal-processing
  libraries can satisfy the contracts.
- LingTai HelioSI may bind C-FETCH-PSP and C-FETCH-SO to `cdaweb` /
  `soar` adapters; this is one binding among many.

---

## 5. Research-generation affordance

- **Composability with [[dakeyo-2026-source-alignment-psp-solo]]**
  (pilot batch): apply the source-alignment method *first* to obtain
  the matched sub-interval, then this skill *second* to compute the
  radial-evolution diagnostics on the matched pair. The combined
  workflow upgrades a single case study into a reproducible pipeline.
- **Open hypothesis**: whether `σ_c` decays with distance follow a
  universal law across multiple conjunctions; the paper studies one
  conjunction; a meta-study using this skill on additional PSP × SO
  alignments is a natural follow-up.
- **Tension with theoretical turbulence-decay models**: compare the
  observed `σ_c` slope to expanding-box MHD predictions
  ([[shoda-2021-turbulence-switchback-generation-alfvenic]] uses the
  same framework) — quantitative mismatch falsifies the input
  spectrum.

---

## Links

- DOI: https://doi.org/10.1051/0004-6361/202243989
- arXiv: TODO verify
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.8

## Skill graph

- [[dakeyo-2026-source-alignment-psp-solo]] (pilot batch) — alignment
  method that selects the matched sub-interval.
- [[shoda-2021-turbulence-switchback-generation-alfvenic]] — turbulence-
  decay theory companion.
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]] —
  Alfvén-Mach context for both spacecraft.
