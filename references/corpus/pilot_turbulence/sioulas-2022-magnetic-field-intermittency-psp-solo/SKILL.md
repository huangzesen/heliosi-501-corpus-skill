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

- **Citation**: Sioulas, N., Huang, Z., Velli, M., Chhiber, R., Cuesta, M. M., Shi, C., Matthaeus, W. H., Bandyopadhyay, R., et al. (2022). *Magnetic Field Intermittency in the Solar Wind: Parker Solar Probe and Solar Orbiter*. **ApJ 934, 143**.
- **DOI**: 10.3847/1538-4357/ac7aa2
- **Source inventories**:
  - `apj_aa_heliophysics_papers.md` §1.5.
  - `.library/custom/heliophysics-skills/SKILL.md` (Solar Wind Turbulence and Heating #5).

**Claim boundary** — supported by inventories:

> Partial Variance of Increments (PVI); higher-order moments of magnetic-field increments; kurtosis scaling; cross-spacecraft (PSP + SO) comparison of intermittency between 0.1 and 1 au. **Intermittency increases with decreasing heliocentric distance.**

Exact intermittency exponents, exact moment orders reported, and exact bin boundaries are **TODO verify in full paper**.

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

**Target**: a monotonic-trending κ (or equivalent moment-order intermittency exponent) vs heliocentric distance, with PSP near-perihelion bins showing more pronounced intermittency than 1-au SO bins, reproduced from one uniform pipeline.

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
- **Data / instruments → MCP / tool contracts**: PSP FIELDS MAG and Solar Orbiter MAG (with optional ion moments) are surfaced via `psp-data-mcp` and `solar-orbiter-data-mcp` contracts with a common-cadence interface.
- **Caveats / failure modes → skill memory**: cadence harmonisation, PVI window τ, moment-order convergence on finite intervals, wind-type stratification, and outlier policy are persistent memory the harness consults before trusting κ.
- **Figures / results → benchmark artifacts**: the intermittency CSV (`sioulas2022_intermittency.csv`) and the PVI PDF comparison panel are the benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

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
- DOI: 10.3847/1538-4357/ac7aa2
- NTRS PDF (linked from inventory): https://ntrs.nasa.gov/api/citations/20230001291/downloads/Sioulas_2022_ApJ_934_143.pdf
