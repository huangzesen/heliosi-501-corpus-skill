---
name: sioulas-2022-magnetic-field-intermittency-psp-solo
description: Measure magnetic-field intermittency (PVI, higher-order moments, kurtosis scaling) using PSP + Solar Orbiter MAG data between 0.1 and 1 au (Sioulas et al. 2022, ApJ 934, 143).
version: 0.1.0
tags: [psp, solar-orbiter, intermittency, pvi, kurtosis, higher-order-moments]
quality_level: pilot
executable_status: scaffold
---

# Sioulas 2022 — Magnetic-Field Intermittency in PSP + Solar Orbiter

## When to use this paper-skill

Load this skill when you need to:

- compute the **Partial Variance of Increments (PVI)** time series of PSP / Solar Orbiter magnetic-field data,
- measure higher-order moments of magnetic-field increments and **kurtosis-scaling exponents** in the inertial range,
- compare intermittency between PSP and SO across the heliocentric-distance range ~0.1–1 au.

Use [[huang-2023-psp-one-over-f-spectrum]] when you instead want the 2nd-order spectrum, and [[sioulas-2024-higher-order-3d-anisotropy]] when you need the 3D structure-function refinement.

## Paper identity and claim boundary

- **Citation**: Sioulas, N., Huang, Z., Velli, M., Chhiber, R., Cuesta, M. E., Shi, C., Matthaeus, W. H., Bandyopadhyay, R., Vlahos, L., Bowen, T. A., et al. (2022). *Magnetic Field Intermittency in the Solar Wind: Parker Solar Probe and SolO Observations Ranging from the Alfvén Region up to 1 AU*. **ApJ 934, 143**.
- **DOI**: [10.3847/1538-4357/ac7aa2](https://doi.org/10.3847/1538-4357/ac7aa2)
- **arXiv**: [2206.00871](https://arxiv.org/abs/2206.00871)
- **ADS**: [2022ApJ...934..143S](https://ui.adsabs.harvard.edu/abs/2022ApJ...934..143S)
- **Source inventories**:
  - `apj_aa_heliophysics_papers.md` §1.5.
  - `.library/custom/heliophysics-skills/SKILL.md` (Solar Wind Turbulence and Heating #5).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via IOPscience DOI + arXiv 2206.00871 abs):**

- The paper uses PSP and Solar Orbiter (SolO) data spanning the Alfvén surface region out to 1 au.
- Diagnostics: Partial Variance of Increments (PVI), higher-order moments of magnetic-field vector increments, scale-dependent kurtosis.
- Verified claim (abstract): **small-scale intermittency at separations ~20–100 d_i strengthens with decreasing heliocentric distance when methods relying on higher-order moments are considered; no clear radial trend is observed at larger scales.**

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact kurtosis-scaling exponent κ values per radial bin and the exact moment orders reported (up to which n) are **TODO_verify** against §3 / Figure-set.
- Whether the "intermittency increases toward the Sun" framing inherited from the inventory is a scale-blind statement (it is not — the verified claim is scale-conditional) is now resolved: **scale-conditional**, i.e. only the small-scale band is radially monotonic.
- Treatment of PVI averaging window τ (whether per-interval-stationary or fixed) is TODO_verify in full text.

> **Assumptions and failure modes** (load-bearing): higher-order moments require record lengths long enough to converge S_n at the chosen n; resampling PSP and SolO to a shared cadence is *prerequisite*, not a diagnostic choice; mixing Alfvénic and non-Alfvénic streams within a radial bin can mask the small-scale monotonic trend.

## Scientific claim to reproduce or operationalize

Magnetic-field intermittency, quantified by both the PVI distribution and the scaling of higher-order moments / kurtosis of B-increments, **increases with decreasing heliocentric distance** between 1 au (Solar Orbiter aphelion-side intervals) and ~0.1 au (PSP perihelion intervals). The two spacecraft are used to span the radial range with a uniform increment-statistics pipeline.

## Required data/instruments and likely files/archives

| Mission/Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 RTN | CDAWeb / PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR |
| (optional) PSP / SO ion moments | n_p, V_RTN | L3 | for ρ-normalisation and Alfvénicity stratification |

Time coverage: PSP encounters with near-Sun dwell (perihelia of E1–E12+) plus Solar Orbiter operational years covering 0.3–1 au.

## Algorithm/workflow steps

1. **Interval cataloging** — Build PSP and SO interval lists binned by heliocentric distance, with comparable durations.
2. **MAG resampling** — Resample both PSP and SO MAG to a common cadence (e.g. 1 s) to remove cadence-driven bias in increment statistics.
3. **Increments** — For each lag ℓ, compute the magnetic-field-vector increments ΔB(t, ℓ).
4. **PVI** — PVI(t, ℓ) = |ΔB(t, ℓ)| / √⟨|ΔB|²⟩_τ where the average is over a window τ ≫ ℓ. Save the PVI time series and its PDF.
5. **Higher-order moments / kurtosis** — Compute S_n(ℓ) = ⟨|ΔB|^n⟩ for n = 2, 4, 6, ... ; from them, the scale-dependent kurtosis K(ℓ) = S_4 / S_2².
6. **Kurtosis-scaling exponent** — Fit K(ℓ) ∝ ℓ^(−κ) in the inertial range; report κ per radial bin.
7. **Radial comparison** — Plot K(ℓ) and κ vs heliocentric distance across PSP and SO bins.
8. **Acceptance** — κ (intermittency strength) is larger at smaller r — i.e. intermittency increases toward the Sun.

## Minimal executable benchmark or validation target

**Primary target** (verified at abstract level): at small separations (~20–100 d_i), higher-order-moment-based intermittency strengthens monotonically with decreasing heliocentric distance across PSP + SolO radial bins, when produced by one uniform pipeline. At larger separations no clear radial trend is required to appear (matching the paper's stated scope).

Artifacts:

- `sioulas2022_intermittency.csv` — columns: spacecraft, t_start, t_end, r_au, S2, S4, S6, kurtosis_at_lref, kappa.
- a PVI PDF panel: PSP perihelion vs SO at ~0.8 au.

## Known pitfalls / failure modes

- **Cadence mismatch**: PSP and SO have different native MAG cadences; without resampling, kurtosis scaling differs even on stationary turbulence.
- **PVI averaging window τ**: a too-short τ biases PVI normalisation; a too-long τ smears stream interfaces into the stationary window. Document τ explicitly.
- **Convergence of high-order moments**: S_6, S_8 require very long records; on short PSP intervals, statistical noise can swamp the trend. Limit reported moment orders to those that converge on the chosen interval lengths.
- **Wind-type bias**: Alfvénic vs non-Alfvénic streams have different intermittency; mixing them in radial bins can mask the radial trend.
- **Outlier handling**: a single large discontinuity (e.g. an HCS crossing) dominates ⟨|ΔB|^n⟩ at high n. Define and document an outlier policy.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "intermittency increases with decreasing heliocentric distance" becomes the validation target — κ vs r monotonic, PVI PDF tails fatter near the Sun.
- **Methods / equations → executable workflows**: increment computation, PVI definition, higher-order moments, and kurtosis-scaling fits are workflow steps 3–7, each a callable unit.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG and Solar Orbiter MAG L2 RTN time series (with optional ion moments) and to resample them onto a shared common-cadence grid; the runtime is responsible for binding these abstract capabilities to whatever concrete adapters it ships (see Layer 3 for example bindings).
- **Caveats / failure modes → skill memory**: cadence harmonisation, PVI window τ, moment-order convergence on finite intervals, wind-type stratification, and outlier policy are persistent memory the harness consults before trusting κ.
- **Figures / results → benchmark artifacts**: the intermittency CSV (`sioulas2022_intermittency.csv`) and the PVI PDF comparison panel are the benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Layer 4 — Research-generation affordances

- **Gap:** the verified claim is *scale-conditional* (small-scale, ~20–100 d_i) but the inventory paraphrase had collapsed it to a scale-blind "intermittency increases with decreasing r" statement. The clean composable question is: *at what scale does the radial monotonicity actually break?* Compose with [[sioulas-2024-higher-order-3d-anisotropy]] (3D anisotropy) to ask whether the small-scale-only radial trend is itself a projection effect of the sampling angle distribution at small separations.
- **Tension:** the abstract claims no clear radial trend at larger scales, but [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] reports systematic radial steepening of the inertial-range spectrum. Steepening (a 2nd-order statement) and absence of higher-order-moment trend (a ≥4th-order statement) are not contradictory but are often conflated — re-running both pipelines on the same intervals isolates which moment order carries the radial signal.
- **Hypothesis:** the small-scale radial monotonicity in κ is driven primarily by the Alfvénic sub-population; stratifying intervals by σ_c using [[damicis-2021-alfvenic-nonalfvenic-psp]] before binning by r should reveal that the non-Alfvénic sub-population shows weaker or absent radial monotonicity even at small scales.
- **Minimal_experiment:** rerun the PVI + higher-order-moment pipeline on the PSP+SolO radial bins with two PVI averaging windows τ (one short, one long relative to the local correlation length) and report κ vs r for each τ; if κ(r) shape is τ-invariant in the small-scale band, the inventory paraphrase is recovered; if it is τ-sensitive, the radial monotonicity is partly an artefact of normalisation.
- **Composable experiment:** feed the per-interval κ table into [[bandyopadhyay-2020-energy-transfer-psp]]'s cascade-rate table — testing whether ε(r) and κ(r) co-vary at small scales would identify intermittency as either an upstream symptom of cascade-rate change or an independent radial driver.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[bandyopadhyay-2020-energy-transfer-psp]] (cascade rate), [[huang-2023-psp-one-over-f-spectrum]] (2nd-order spectrum on same MAG data), [[sioulas-2024-higher-order-3d-anisotropy]] (3D extension of structure functions), [[damicis-2021-alfvenic-nonalfvenic-psp]] (Alfvénic stratification used here as a covariate).
- **MCPs used**:
  - `psp-data-mcp`, `solar-orbiter-data-mcp` (or pyspedas + SOAR client).
  - Python numerics for increment / moment computation (`numpy`).
  - PVI implementation (consistent definition across the two spacecraft).
- **Harness contract**: exports an "intermittency table" + PVI PDF figure; downstream consumers can join with the cascade-rate table from `bandyopadhyay-2020-energy-transfer-psp` to study cascade rate vs intermittency.

## References

- Inventory: `apj_aa_heliophysics_papers.md` §1.5.
- DOI: https://doi.org/10.3847/1538-4357/ac7aa2 (IOPscience; resolves to ApJ 934, 143, 2022)
- arXiv: https://arxiv.org/abs/2206.00871 (preprint title matches journal title; verified 2026-05-19)
- ADS: https://ui.adsabs.harvard.edu/abs/2022ApJ...934..143S
- NTRS PDF (linked from inventory): https://ntrs.nasa.gov/api/citations/20230001291/downloads/Sioulas_2022_ApJ_934_143.pdf
