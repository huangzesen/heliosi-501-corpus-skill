# Pilot Batch 1 — PSP / Solar Wind Turbulence Paper-Skills

- **Generated**: 2026-05-18
- **Theme**: solar-wind-turbulence (PSP / Solar Orbiter inner-heliosphere observations)
- **Status**: pilot scaffold — claims grounded in the curated inventories below; numerical specifics flagged `TODO verify in full paper` per skill.
- **Source inventories**:
  - `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  - `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md`
  - `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md`
- **Parent skill**: `.library/custom/heliophysics-skills/SKILL.md` (theme: turbulence).

## Skills

| # | Slug | Year | Lead | DOI / arXiv | Core claim (one line) | Quality | Status |
|---|------|------|------|-------------|------------------------|---------|--------|
| 1 | `bandyopadhyay-2020-energy-transfer-psp` | 2020 | R. Bandyopadhyay | DOI 10.3847/1538-4365/ab5dae · arXiv 1912.02959 | Cascade rate near the Sun is ~100× the 1-au value, by Politano–Pouquet and von Kármán methods on PSP E1. | pilot | scaffold |
| 2 | `sioulas-2023-anisotropic-scaling-inner-heliosphere` | 2023 | N. Sioulas | DOI 10.3847/1538-4357/acd053 · arXiv 2303.10810 | Wavevector-anisotropic structure-function scaling evolves with heliocentric distance between PSP and Solar Orbiter (0.1–1 au). | pilot | scaffold |
| 3 | `huang-2023-psp-one-over-f-spectrum` | 2023 | Z. Huang | DOI 10.3847/2041-8213/acd7f2 · arXiv 2303.00843 | Magnetically incompressible PSP intervals (E1–E13) show a 1/f outer range and an inertial slope ~−3/2 near the Sun, with the 1/f range extending to larger scales closer to the Sun. | pilot | scaffold |
| 4 | `sioulas-2022-magnetic-field-intermittency-psp-solo` | 2022 | N. Sioulas | DOI 10.3847/1538-4357/ac7aa2 | Magnetic-field intermittency (PVI, higher-order moments, kurtosis scaling) increases with decreasing heliocentric distance between SO (~1 au) and PSP (~0.1 au). | pilot | scaffold |
| 5 | `telloni-2021-psp-solo-radial-alignment-turbulence` | 2021 | D. Telloni | DOI 10.3847/2041-8213/abf7d1 | First PSP–SO radial alignment: σ_c, σ_R, ε evolve from 0.1 au to 1 au in approximately the same plasma parcel. | pilot | scaffold |
| 6 | `damicis-2021-alfvenic-nonalfvenic-psp` | 2021 | (see attribution note) | arXiv 2101.00830 | PSP E1–E5 intervals stratify into Alfvénic vs non-Alfvénic streams with distinct spectral indices and radial dependences. | pilot (weak attribution) | scaffold |
| 7 | `chen-2021-near-sun-streamer-belt-turbulence` | 2021 | C. H. K. Chen | arXiv 2101.00246 | PSP E4 (down to ~27.9 R☉) streamer-belt wind shows distinguishable inbound/outbound trace PSDs and σ_c, σ_R linked to solar-wind acceleration. | pilot | scaffold |
| 8 | `sioulas-2024-higher-order-3d-anisotropy` | 2024 | N. Sioulas | arXiv 2404.04055 | A 3D structure-function decomposition (∥, ⊥, fluctuation-direction) of imbalanced Alfvénic z± turbulence discriminates Critical Balance from Scale-Dependent Dynamic Alignment, with two sub-inertial segments and an "anomalous coherence" regime. | pilot | scaffold |

## Cross-cutting infrastructure

These eight skills share — and intentionally re-use — the following implementation building blocks (suitable for promotion to dedicated sub-skills in a later pass):

- **PSP / SO data MCP contract**: PSP FIELDS MAG L2, PSP SWEAP (SPC + SPAN-I) L3, Solar Orbiter MAG L2, SOAR SWA/PAS L2/L3.
- **Elsässer-field computation**: z± = V ± B/√(μ₀ρ).
- **Cross-helicity / residual energy**: σ_c, σ_R definitions and stratification logic.
- **Cascade-rate estimators**: Politano–Pouquet third-order law + von Kármán decay law.
- **Higher-order structure functions and PVI**: shared increment + moment pipeline.
- **Local mean-field decomposition**: scale-dependent moving average for ∥/⊥ classification.
- **Spectral estimators**: Welch / multitaper trace PSDs with documented windowing.

## Weak entries flagged for full-text verification

| Slug | Issue | Recommended action |
|------|-------|--------------------|
| `damicis-2021-alfvenic-nonalfvenic-psp` | arXiv 2101.00830 is **dual-attributed** across the two inventories: `apj_aa` §1.13 assigns it to "D'Amicis et al. 2021, A&A"; `solar_wind_turbulence_2020_2026.md` #4 assigns it to "Shi, Velli, Panasenco, Tenerani 2021". | Pull the arXiv 2101.00830 abstract page, resolve the attribution, and either rename the slug or split into two paper-skills. |
| `sioulas-2023-anisotropic-scaling-inner-heliosphere` | arXiv 2303.10810 appears twice in `apj_aa`: once at §1.2 (Sioulas et al. 2023, ApJ) and once at §3.5 (Cuesta et al. 2023, "Scaling Anisotropy with Stationary Background Field"). | Verify which paper the arXiv ID corresponds to before manuscript citation; the DOI 10.3847/1538-4357/acd053 should disambiguate. |
| `chen-2021-near-sun-streamer-belt-turbulence` | No DOI in inventory; year and venue need confirmation. | Cross-check arXiv 2101.00246 against ADS. |
| `sioulas-2024-higher-order-3d-anisotropy` | No DOI in inventory; CB / SDDA template parameterisations referenced from inventory text but not numerically specified. | Confirm publication venue + freeze CB / SDDA template definitions on a full-text read. |
| All pilots | Specific numerical exponents, threshold values, and per-interval / per-bin counts are **TODO verify in full paper** in every skill. | Full-text pass before promoting any pilot to `production` quality_level. |

## Roll-up reproducibility targets

A HelioSI harness consuming this pilot batch should be able to roll the eight skill outputs up into:

- A **single radial-evolution table** of σ_c, σ_R, slope_B, slope_V, ε, kurtosis-exponent across PSP encounters and Solar Orbiter,
- A **two-population (Alfvénic / non-Alfvénic) covariate column** for every interval in the radial-evolution table,
- One **streamer-belt-specific** reference case (Chen 2021 / PSP E4),
- One **conjunction case** (Telloni 2021 / first PSP–SO radial alignment),
- A **CB-vs-SDDA verdict** column on imbalanced Alfvénic subsets (Sioulas 2024).
