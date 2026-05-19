---
name: chen-2021-near-sun-streamer-belt-turbulence
description: Characterize near-Sun streamer-belt solar wind turbulence and its link to wind acceleration using PSP Encounter 4 in-situ data (arXiv 2101.00246).
version: 0.1.0
tags: [psp, encounter-4, streamer-belt, turbulence, cross-helicity, residual-energy, hcs]
quality_level: pilot
executable_status: scaffold
---

# Chen 2021 — Near-Sun Streamer-Belt Solar Wind Turbulence (PSP E4)

## When to use this paper-skill

Load this skill when you need to:

- characterize **streamer-belt solar wind** (near the heliospheric current sheet, HCS) turbulence using PSP Encounter 4 data (down to ~27.9 R☉),
- compute **trace magnetic and velocity power spectra** with an inbound/outbound split across the HCS,
- compute **cross-helicity σ_c and residual energy σ_R** in the same configuration to connect turbulence properties with the solar-wind acceleration scenario in the streamer belt.

Use [[damicis-2021-alfvenic-nonalfvenic-psp]] for general Alfvénicity stratification across Encounters 1–5; this skill is the streamer-belt-specific cousin focused on E4.

## Paper identity and claim boundary

- **Citation**: Chen, C. H. K., Chandran, B. D. G., Woodham, L. D., Jones-Mecholsky, S. I., et al. (2021). *The Near-Sun Streamer Belt Solar Wind: Turbulence and Solar Wind Acceleration*.
- **arXiv**: [2101.00246](https://arxiv.org/abs/2101.00246)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md` entry #3 (2021).

**Claim boundary** — supported by inventory:

> PSP Encounter 4 (down to 27.9 R☉) in-situ MAG + SPC analysis split inbound/outbound; trace power spectra of magnetic and velocity fluctuations near the heliospheric current sheet; cross-helicity and residual-energy diagnostics linked to solar-wind acceleration mechanisms.

Numerical slopes, σ_c values, and exact HCS-crossing times are **TODO verify in full paper**.

## Scientific claim to reproduce or operationalize

In the streamer-belt solar wind sampled by PSP Encounter 4 (perihelion ~27.9 R☉), inbound and outbound legs across the HCS exhibit **distinct turbulence signatures** (trace B and V power spectra, σ_c, σ_R) that can be linked to mechanisms of solar-wind acceleration in this slow / streamer-belt origin regime.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 RTN | CDAWeb / PSP SOC (`psp_fld_l2_mag_rtn_*.cdf`) |
| PSP SWEAP/SPC | V_RTN, n_p, T_p | L3 | CDAWeb / PSP SOC (`psp_swp_spc_l3i_*.cdf`) |

Time range: **PSP Encounter 4** (perihelion 2020-01-29; ~27.9 R☉ closest approach). Split into inbound and outbound legs around the HCS crossing.

## Algorithm/workflow steps

1. **HCS identification** — Use B_R sign changes (and SPC sector indicators where available) to mark the HCS crossing(s) during E4.
2. **Inbound / outbound split** — Define inbound and outbound legs of comparable duration around perihelion / the HCS.
3. **Spectral estimation** — Compute trace PSDs of B_RTN and V_RTN per leg using a windowed estimator (Welch / multitaper).
4. **Inertial-range slopes** — Fit slopes of B and V PSDs in the inertial range.
5. **Elsässer fields and σ_c / σ_R** — Compute z± = V ± B/√(μ₀ρ); compute σ_c and σ_R per leg.
6. **Acceleration linkage** — Discuss the leg-to-leg differences in σ_c / σ_R / slopes in relation to acceleration mechanisms (e.g. Alfvén-wave-driven heating, expansion).
7. **Acceptance** — Inbound and outbound legs show distinguishable trace spectra and σ_c, consistent with the published characterisation (TODO verify direction in full paper).

## Minimal executable benchmark or validation target

**Target**: per-leg PSD figures and a small table of (slope_B, slope_V, σ_c, σ_R) for inbound and outbound legs of PSP E4 around the HCS, showing measurably different values consistent with the streamer-belt origin scenario.

Artifacts:

- `chen2021_e4_legs.csv` — columns: leg, t_start, t_end, slope_B, slope_V, sigma_c, sigma_R.
- a two-panel PSD figure: inbound vs outbound.

## Known pitfalls / failure modes

- **HCS-crossing ambiguity**: B_R polarity reversals near the HCS can be multiple and noisy; over-aggressive crossing labelling fragments the legs.
- **SPC data quality near streamer belt**: SPC plasma moments can degrade in the high-flux streamer-belt regime; check coverage and uncertainty estimates.
- **Leg-length stationarity**: inbound and outbound legs may sample different stream contexts even within the streamer belt; report stationarity diagnostics.
- **Acceleration interpretation**: the link to acceleration is an interpretation overlaid on the measurements; do not over-claim causality from σ_c alone.
- **Mass density gaps**: ρ-normalisation for z± depends on continuous SPC density; interpolation choices matter, especially in slow streamer-belt wind.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "inbound vs outbound legs of PSP E4 streamer-belt wind show distinct turbulence signatures linked to acceleration" becomes the validation target — distinguishable per-leg PSDs and σ_c / σ_R.
- **Methods / equations → executable workflows**: HCS-crossing identification, leg splitting, trace PSD estimation, inertial-range slope fitting, Elsässer construction, and σ_c / σ_R computation become workflow steps 1–5, each a callable unit.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS MAG L2 and SWEAP/SPC L3 are surfaced via the `psp-data-mcp` contract specialised to Encounter 4.
- **Caveats / failure modes → skill memory**: HCS-crossing ambiguity, SPC data quality, leg-length stationarity, acceleration interpretation, and density-gap handling are persistent memory consulted before quoting a leg-to-leg difference.
- **Figures / results → benchmark artifacts**: the per-leg CSV (`chen2021_e4_legs.csv`) and the two-panel PSD figure are the exported benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[bandyopadhyay-2020-energy-transfer-psp]] (cascade-rate method), [[damicis-2021-alfvenic-nonalfvenic-psp]] (broader Alfvénicity stratification), [[telloni-2021-psp-solo-radial-alignment-turbulence]] (radial-conjunction view), [[huang-2023-psp-one-over-f-spectrum]] (spectral methodology shared at small scales).
- **MCPs used**:
  - `psp-data-mcp` for E4 MAG + SPC retrieval.
  - HCS-crossing list MCP (or B_R polarity heuristic).
  - `sw-scanner` if Alfvénicity-based segmentation is desired in addition to the leg split.
- **Harness contract**: this skill exports a "leg table" + a PSD comparison figure for PSP E4 streamer-belt wind; downstream skills can use it as a streamer-belt reference set.

## References

- Inventory: `solar_wind_turbulence_2020_2026.md` entry #3 (2021).
- arXiv: https://arxiv.org/abs/2101.00246
