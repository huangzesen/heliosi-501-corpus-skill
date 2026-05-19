---
name: huang-2023-psp-one-over-f-spectrum
description: Detect and characterize the low-frequency 1/f range of solar wind magnetic-field turbulence in PSP Encounters 1–13 (Huang et al. 2023, ApJL).
version: 0.1.0
tags: [psp, turbulence, one-over-f-spectrum, magnetic-incompressibility, double-power-law, alfven-point]
quality_level: pilot
executable_status: scaffold
---

# Huang 2023 — PSP 1/f Turbulence Spectrum

## When to use this paper-skill

Load this skill when you need to:

- detect the **low-frequency 1/f range** in PSP magnetic-field spectra,
- characterize how the 1/f outer scale and inertial-range slope evolve with heliocentric distance,
- pre-screen PSP intervals for **magnetic incompressibility** (δ|B|/|B| ≪ 1) before spectral analysis.

Use [[chen-2021-near-sun-streamer-belt-turbulence]] for streamer-belt-specific spectra at E4, and [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] for anisotropic structure-function radial mapping.

## Paper identity and claim boundary

- **Citation**: Huang, Z., Sioulas, N., Shi, C., Velli, M., Bowen, T., Davis, N., et al. (2023). *New Observations of Solar Wind 1/f Turbulence Spectrum from Parker Solar Probe*. **ApJL**.
- **DOI**: 10.3847/2041-8213/acd7f2
- **arXiv**: [2303.00843](https://arxiv.org/abs/2303.00843)
- **Source inventories**:
  - `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.4.
  - `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md` entry #9 (2023).

**Claim boundary** — supported by inventories:

> 109 magnetically incompressible PSP intervals (δ|B|/|B| ≪ 1) from Encounters 1–13 are analyzed; double-power-law fits to the trace magnetic spectra characterize the low-frequency 1/f spectral index and its radial evolution from the Alfvén point out to ~0.3 au. The inertial-range slope close to the Sun is reported as ~−3/2, and the 1/f range extends to larger scales closer to the Sun.

Exact break-frequency values, exact slope distributions, and per-encounter statistics are **TODO verify in full paper**.

## Scientific claim to reproduce or operationalize

Magnetic-field spectra in **magnetically incompressible** PSP intervals (δ|B|/|B| ≪ 1) between the Alfvén surface and ~0.3 au exhibit a clear two-segment shape: a **low-frequency ~1/f range** at outer scales and an **inertial range with slope close to −3/2** at smaller scales. The 1/f outer scale extends further toward larger spatial scales as the spacecraft gets closer to the Sun.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, |B| | L2 RTN, native cadence | CDAWeb / PSP SOC (`psp_fld_l2_mag_rtn_*.cdf`) |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN (for context, Alfvén-point determination, normalisation) | L3 | PSP SOC |

Time range: PSP Encounters 1–13 — i.e. roughly 2018-11 through ~2022, including post-Alfvén-surface intervals.

## Algorithm/workflow steps

1. **Interval selection** — Scan PSP MAG L2 for candidate intervals long enough to resolve outer scales (e.g. >> correlation length).
2. **Magnetic-incompressibility filter** — Compute δ|B|/|B|; keep only intervals where this is ≪ 1 (paper uses 109 such intervals; threshold value **TODO verify**).
3. **Trace spectrum** — Compute trace PSD = (PSD_R + PSD_T + PSD_N) on each interval using a windowed Welch / multitaper estimator.
4. **Double-power-law fit** — Fit log(PSD) = piecewise linear in log f with a break frequency f_break; parameters {slope_lowf, slope_highf, f_break, amplitude}.
5. **1/f test** — Check whether slope_lowf ≈ −1 within fit uncertainty (paper's defining criterion); record slope_highf for the inertial range.
6. **Radial trend** — Bin intervals by heliocentric distance and plot slope_lowf, slope_highf, and f_break vs r/R_sun.
7. **Acceptance** — slope_highf near the Sun ~ −3/2; slope_lowf ~ −1 with f_break shifting to lower f as r decreases.

## Minimal executable benchmark or validation target

**Target**: on a subset of PSP MAG L2 in Encounters 1–13 with δ|B|/|B| ≪ 1, the median inertial-range slope close to the Sun is consistent with −3/2, the low-frequency slope is consistent with −1, and the break frequency shifts to lower values at smaller heliocentric distance.

Artifacts:

- `huang2023_intervals.csv` — one row per interval: t_start, t_end, r_au, slope_lowf, slope_highf, f_break, fit_chi2, mean_delta_modB_over_modB.
- a panel plot: f·PSD vs f (compensated) for several intervals at increasing r.

## Known pitfalls / failure modes

- **Magnetic-incompressibility threshold**: too loose a δ|B|/|B| cut admits compressible streams (slow wind, stream interfaces) and broadens the slope distribution toward −5/3 in the inertial range, polluting the −3/2 detection.
- **Window length vs outer-scale resolution**: short windows cannot resolve the 1/f range; long windows include non-stationary features (CIRs, shocks).
- **Spectral estimator**: a single FFT with no windowing biases high-frequency power; Welch / multitaper is necessary for unbiased slope fitting.
- **Break-frequency identification**: the break is best identified jointly with the two slopes; a naive break-detection that fits slopes independently is unstable.
- **Encounter mix**: weighting toward later encounters with longer near-Sun dwell biases the radial trend; report per-encounter counts.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "1/f at outer scales, inertial slope ~−3/2 near the Sun, break shifts with r" becomes the validation target on a magnetically-incompressible interval set.
- **Methods / equations → executable workflows**: the magnetic-incompressibility filter, Welch/multitaper trace-PSD, and double-power-law-with-break fitter become workflow steps 2–5, each a callable unit.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP L3 CDF time series (RTN frame, common cadence) and a Welch / multitaper spectral-estimator capability; the runtime supplies concrete adapters bound to those capabilities (see Layer 3 for example bindings).
- **Caveats / failure modes → skill memory**: incompressibility-threshold choice, window-length vs outer-scale resolution, spectral-estimator bias, joint break detection, and encounter-mix weighting are persistent memory consulted before accepting a 1/f detection.
- **Figures / results → benchmark artifacts**: the intervals CSV (`huang2023_intervals.csv`) and the compensated-spectrum panel are the benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[chen-2021-near-sun-streamer-belt-turbulence]] (Encounter-4 streamer-belt spectra), [[sioulas-2024-higher-order-3d-anisotropy]] (3D structure-function follow-up), [[sioulas-2022-magnetic-field-intermittency-psp-solo]] (PVI / kurtosis statistics on the same MAG L2 substrate).
- **MCPs used**:
  - `psp-data-mcp` for MAG L2 + SWEAP L3 retrieval.
  - PSD/Welch utilities in `scipy.signal`.
  - `sw-scanner` for Alfvénicity-based pre-segmentation if needed.
- **Harness contract**: this skill exports an "intervals table" (one row per accepted interval) and a small set of validation plots. The acceptance check is the median inertial-range slope near the Sun being close to −3/2 on the filtered subset.

## References

- Inventory: `apj_aa_heliophysics_papers.md` §1.4.
- Inventory: `solar_wind_turbulence_2020_2026.md` #9 (2023).
- DOI: 10.3847/2041-8213/acd7f2
- arXiv: https://arxiv.org/abs/2303.00843
