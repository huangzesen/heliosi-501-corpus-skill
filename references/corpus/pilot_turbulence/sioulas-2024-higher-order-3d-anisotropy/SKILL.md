---
name: sioulas-2024-higher-order-3d-anisotropy
description: Decompose higher-order structure functions of imbalanced Alfvénic turbulence into parallel, perpendicular, and fluctuation-direction axes and test Critical Balance vs Scale-Dependent Dynamic Alignment (arXiv 2404.04055).
version: 0.1.0
tags: [psp, turbulence, 3d-anisotropy, higher-order-structure-functions, critical-balance, scale-dependent-dynamic-alignment, imbalanced-alfvenic]
quality_level: pilot
executable_status: scaffold
---

# Sioulas 2024 — Higher-Order 3D Anisotropy in Imbalanced Alfvénic Turbulence

## When to use this paper-skill

Load this skill when you need to:

- compute **3D structure functions** of z± Elsässer fields decomposed along **parallel**, **perpendicular**, and **fluctuation-direction** axes,
- test predictions of **Critical Balance (CB)** vs **Scale-Dependent Dynamic Alignment (SDDA)** in imbalanced Alfvénic turbulence,
- characterize how high-order exponents ζ_n depend on σ_c, and identify the two sub-inertial segments and the "anomalous coherence" regime reported by this paper.

This is the **3D follow-up** to [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (2D parallel/perpendicular only).

## Paper identity and claim boundary

- **Citation**: Sioulas, N., Zikopoulos, T., Shi, C., Velli, M. (2024). *Higher-Order Analysis of Three-Dimensional Anisotropy in Imbalanced Alfvénic Turbulence*.
- **arXiv**: [2404.04055](https://arxiv.org/abs/2404.04055)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md` entry #11 (2024). Also referenced in `apj_aa_heliophysics_papers.md` §1.2 as the "companion 2404.04055 for 3D anisotropy follow-up" to Sioulas 2023.

**Claim boundary** — supported by inventory:

> 3D structure-function analysis (n up to high order) decomposed into parallel/perpendicular/fluctuation-direction axes; tests of Critical Balance vs Scale-Dependent Dynamic Alignment for z± modes; exponents ζ_n binned by σ_c; identification of two sub-inertial segments and an "anomalous coherence" regime.

The specific functional forms of CB / SDDA predictions, the exact ζ_n numbers, and the boundary scales of the two sub-inertial segments are **TODO verify in full paper**.

## Scientific claim to reproduce or operationalize

In **imbalanced Alfvénic** (|σ_c| close to 1) solar wind turbulence, a 3D structure-function decomposition along (parallel, perpendicular, fluctuation-direction) axes resolves higher-order exponents ζ_n whose behaviour **discriminates between Critical Balance and Scale-Dependent Dynamic Alignment** for z± modes. Two distinct sub-inertial-range segments are detected, plus an "anomalous coherence" regime — features absent from a 2D parallel/perpendicular treatment.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 RTN | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | V_RTN, n_p | L3 | PSP SOC |
| (optional) Solar Orbiter MAG + SWA | B_RTN, V_RTN, n_p | L2/L3 | SOAR (for radial coverage) |

Time range: PSP encounters with high-quality MAG + SPC/SPAN-I coverage on intervals selected for large |σ_c| (imbalanced Alfvénic streams).

## Algorithm/workflow steps

1. **Imbalanced-Alfvénic interval selection** — Filter intervals with |σ_c| above an imbalance threshold (e.g. > 0.7 — TODO verify); ensure inertial-range coverage and quasi-stationarity.
2. **Elsässer fields** — Compute z± = V ± B/√(μ₀ρ).
3. **Local mean-field frame** — For each lag ℓ, build a scale-dependent local mean field B₀(t, ℓ) and the fluctuation direction (from δz± components in the perpendicular plane).
4. **3D axis decomposition** — For each pair separated by ℓ, classify the displacement along (∥, ⊥, fluctuation-direction) bins.
5. **Higher-order structure functions** — Compute S_n^a(ℓ) = ⟨|δz±·ê_a|^n⟩ for a ∈ {∥, ⊥, fluct} and n up to a high order (e.g. n=2..8 — TODO verify the maximum reported).
6. **Scaling exponents** — Fit S_n^a ∝ ℓ^{ζ_n^a} in the inertial range per axis.
7. **CB vs SDDA test** — Compare measured ζ_n^a against the CB and SDDA prediction templates for z± modes.
8. **Sub-inertial segmentation** — Identify the two reported sub-inertial segments (TODO verify boundary scales).
9. **σ_c binning** — Stratify all results by σ_c.

## Minimal executable benchmark or validation target

**Target**: a per-σ_c-bin set of ζ_n^∥, ζ_n^⊥, ζ_n^fluct profiles in the inertial range that (qualitatively) selects between CB and SDDA in the direction reported by the paper (TODO verify direction in full paper).

Artifacts:

- `sioulas2024_zeta_n.csv` — columns: sigma_c_bin, axis (par/perp/fluct), n, zeta_n, fit_uncertainty.
- a multi-panel ζ_n^a vs n figure overlaid with CB / SDDA reference curves.

## Known pitfalls / failure modes

- **High-n moment convergence**: ζ_n at large n is statistically unstable on finite PSP intervals; restrict to orders that converge.
- **Local-mean-field-frame definition**: the fluctuation direction is sensitive to how the perpendicular plane and δz± are projected; document the convention.
- **Imbalanced filter threshold**: a too-strict |σ_c| cut shrinks the sample drastically; a too-loose cut admits balanced intervals and washes out the test.
- **Cross-bin contamination**: pairs near axis boundaries can leak between (∥, ⊥, fluct) bins; the bin widths matter.
- **CB / SDDA prediction templates**: small differences in how the templates are parameterised can move the apparent CB-vs-SDDA verdict; freeze the template definitions early.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "ζ_n^a discriminates CB from SDDA in imbalanced Alfvénic turbulence, with two sub-inertial segments and an anomalous-coherence regime" becomes the validation target — ζ_n^a curves and a side-by-side CB / SDDA template overlay.
- **Methods / equations → executable workflows**: imbalanced-Alfvénic filter, local-mean-field-frame construction, 3D axis decomposition, higher-order S_n^a computation, and CB / SDDA template comparison become workflow steps 1–7, each a callable unit.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS MAG and SWEAP/SPAN-I (optionally augmented by Solar Orbiter) are surfaced via `psp-data-mcp` and `solar-orbiter-data-mcp` contracts; the imbalanced filter shares its σ_c implementation with [[damicis-2021-alfvenic-nonalfvenic-psp]].
- **Caveats / failure modes → skill memory**: high-n moment convergence, local-frame definition, imbalance threshold, axis-bin contamination, and template parameterisation are persistent memory consulted before declaring a CB-vs-SDDA verdict.
- **Figures / results → benchmark artifacts**: the ζ_n CSV (`sioulas2024_zeta_n.csv`) and the multi-panel ζ_n vs n figure with CB / SDDA overlays are the exported benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (2D anisotropy predecessor — same group, same local-mean-field framework), [[sioulas-2022-magnetic-field-intermittency-psp-solo]] (higher-order moments without 3D decomposition), [[damicis-2021-alfvenic-nonalfvenic-psp]] (σ_c stratification used here as a covariate), [[huang-2023-psp-one-over-f-spectrum]] (low-frequency outer-scale context).
- **MCPs used**:
  - `psp-data-mcp` for PSP MAG + SWEAP retrieval.
  - `solar-orbiter-data-mcp` (optional, for radial coverage).
  - `sw-scanner` (or equivalent) for Alfvénicity-based segmentation.
- **Harness contract**: this skill exports a high-dimensional ζ_n table (CSV) and a CB / SDDA overlay figure. The harness can roll up multiple paper-skill outputs into a turbulence-theory-test table — this paper-skill's ζ_n outputs are the canonical "3D higher-order anisotropy" column.

## References

- Inventory: `solar_wind_turbulence_2020_2026.md` entry #11 (2024).
- Inventory cross-reference: `apj_aa_heliophysics_papers.md` §1.2 ("companion 2404.04055").
- arXiv: https://arxiv.org/abs/2404.04055
