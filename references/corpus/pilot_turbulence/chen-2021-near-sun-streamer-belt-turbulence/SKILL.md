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

- **Citation**: Chen, C. H. K., Chandran, B. D. G., Woodham, L. D., Jones, S. I., Perez, J. C., Bourouaine, S., Bowen, T. A., Klein, K. G., Moncuquet, M., Kasper, J. C., Bale, S. D. (2021). *The Near-Sun Streamer Belt Solar Wind: Turbulence and Solar Wind Acceleration*. **A&A 650, L3**.
- **DOI**: [10.1051/0004-6361/202039872](https://doi.org/10.1051/0004-6361/202039872)
- **arXiv**: [2101.00246](https://arxiv.org/abs/2101.00246)
- **ADS**: [2021A&A...650L...3C](https://ui.adsabs.harvard.edu/abs/2021A%26A...650L...3C)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md` entry #3 (2021).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via arXiv 2101.00246 + A&A 650 L3 page):**

- PSP Encounter 4 reached as low as 27.9 R☉; in-situ MAG + SPC are used to study turbulence in the streamer-belt slow wind near the heliospheric current sheet (HCS).
- Verified, qualitative claim: **turbulence properties differ between inbound and outbound legs**; near the HCS (outbound, streamer-belt) the turbulence shows **lower amplitudes, increased magnetic compressibility, and steeper spectra**.
- The paper links these turbulence properties to solar-wind acceleration mechanisms in the streamer-belt origin scenario (this linkage is an interpretation, not a directly measured causal claim).

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- Exact inertial-range slope values per leg (B and V), per-window σ_c and σ_R numerical values, and exact HCS-crossing times are **TODO_verify** against §3 / figures of A&A 650, L3.
- Whether the leg-to-leg compressibility increase is monotonic in proximity to the HCS or a step at the crossing is TODO_verify.
- The "linked to acceleration" framing is interpretive — the supporting evidence chain (e.g. through what specific acceleration mechanism — Alfvén-wave-driven, reflection, expansion) requires full-text inspection.

> **Assumptions and failure modes** (load-bearing): SPC plasma moments degrade in the high-flux streamer belt — coverage and uncertainty must be checked before quoting σ_c; B_R sign reversals near the HCS can be multiple, so the inbound/outbound split is itself a curation step; mass density gaps in slow streamer-belt wind drive ρ-normalisation noise for the Elsässer construction.

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
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP/SPC L3 CDF time series scoped to the Encounter-4 interval (RTN frame, common cadence); the runtime supplies concrete adapters bound to those capabilities (see Layer 3 for example bindings).
- **Caveats / failure modes → skill memory**: HCS-crossing ambiguity, SPC data quality, leg-length stationarity, acceleration interpretation, and density-gap handling are persistent memory consulted before quoting a leg-to-leg difference.
- **Figures / results → benchmark artifacts**: the per-leg CSV (`chen2021_e4_legs.csv`) and the two-panel PSD figure are the exported benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Layer 4 — Research-generation affordances

- **Gap:** the paper anchors the inbound-vs-outbound distinction at PSP E4 only; whether the *same* streamer-belt-near-HCS signature (lower amplitude, higher compressibility, steeper spectrum) reappears at later HCS crossings (E5+, where SPAN-I replaces SPC and the data quality budget changes) is unresolved. Compose with [[damicis-2021-alfvenic-nonalfvenic-psp]] (Alfvénicity stratification across multiple encounters) to test whether E4 is a representative or atypical streamer-belt sample.
- **Tension:** "lower amplitudes + steeper spectra" near the HCS could be read either as (a) a turbulence *state* (driven by reduced large-scale stirring of streamer-belt slow wind) or (b) a *measurement* effect (the SPC noise floor in low-amplitude regimes acts like a high-frequency filter, steepening the apparent slope). Reproducing the analysis with SPAN-I where overlap exists discriminates between these.
- **Hypothesis:** the compressibility enhancement near the HCS is *quantitatively* tied to the local plasma β rather than to HCS proximity per se; binning E4 intervals by β at fixed |B_R|-polarity-distance from the crossing should collapse the leg-vs-leg compressibility difference onto a single β-curve.
- **Minimal_experiment:** rerun the leg analysis with two independent HCS-crossing detectors (B_R-polarity vs sector-indicator) and report the (slope_B, slope_V, σ_c, σ_R) tuple per detector; if the inbound/outbound distinction survives both detectors, the streamer-belt signature is detector-agnostic; if not, the leg labels are partly an artefact.
- **Composable experiment:** join the per-leg PSD table with the cascade-rate framework from [[bandyopadhyay-2020-energy-transfer-psp]] using the same E1-style methodology — does the streamer-belt slow wind sit on the *same* ε(r) curve as the fast-wind reference, or off it? This is the cleanest "is streamer-belt slow wind a separate population?" test the data support.

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
- DOI: https://doi.org/10.1051/0004-6361/202039872 (A&A 650 L3, 2021)
- arXiv: https://arxiv.org/abs/2101.00246 (preprint title matches journal title; verified 2026-05-19)
- ADS: https://ui.adsabs.harvard.edu/abs/2021A%26A...650L...3C
