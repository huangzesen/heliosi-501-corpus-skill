---
name: carbone-2021-electron-density-turbulence-ion-cyclotron-waves
description: Use when characterising electron-density turbulence and ion-cyclotron-wave statistics at ~0.5 au from Solar Orbiter RPW spacecraft-potential-derived density — central paper claim is that RPW-derived n_e at ~0.5 au shows definite spectral / intermittency properties and that ion-cyclotron waves can be statistically identified via wavelet analysis (Carbone et al. 2021, A&A 656, A16; arXiv 2105.07790).
version: 0.1.0
tags: [solar-orbiter, rpw, electron-density, ion-cyclotron-waves, intermittency, wavelet, aanda]
quality_level: pilot
executable_status: scaffold
---

# Carbone 2021 — Electron-Density Turbulence + ICWs (Solar Orbiter)

## When to use this paper-skill

Load this skill when you need to:

- compute **electron-density turbulence spectra and intermittency** at ~0.5 au using Solar Orbiter RPW spacecraft-potential-derived n_e,
- statistically identify **ion-cyclotron waves** via wavelet analysis in the inner heliosphere,
- complement PSP-based ICW detection (cf. [[bowen-2024-extended-cyclotron-resonant-heating]]) with a Solar Orbiter density-channel measurement.

Skip this skill if your interest is magnetic-field-only turbulence ([[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]) or PSP-specific cyclotron heating ([[bowen-2024-extended-cyclotron-resonant-heating]]).

## Paper identity and claim boundary

- **Citation**: Carbone, F., Telloni, D., Sorriso-Valvo, L., et al. (2021). *Statistical Study of Electron Density Turbulence and Ion-Cyclotron Waves in the Inner Heliosphere: Solar Orbiter Observations.* **A&A 656, A16**.
- **DOI**: 10.1051/0004-6361/202140931
- **arXiv**: [2105.07790](https://arxiv.org/abs/2105.07790)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.14.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> RPW spacecraft-potential-derived electron density at ~0.5 au yields well-defined spectra and intermittency statistics for density fluctuations, and wavelet analysis statistically identifies ion-cyclotron waves in the same intervals.

Out-of-scope: extending the result to PSP-distance regimes without independent analysis; collapsing the ICW identification across all SO encounters when the paper conditions on specific cruise-phase windows (TODO verify which encounters).

## Scientific claim to reproduce or operationalize

Electron-density fluctuations measured by Solar Orbiter RPW (via the spacecraft potential) at ~0.5 au exhibit power spectra and intermittency consistent with solar-wind density turbulence; concurrent wavelet analysis on MAG data statistically identifies ion-cyclotron wave events. The skill operationalises this as a joint density-turbulence + ICW-catalog pipeline.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| SO RPW (Radio and Plasma Waves) | spacecraft potential V_sc → n_e | L2/L3 | SOAR / CDAWeb |
| SO MAG | B_RTN | L2 | SOAR / CDAWeb |
| SO SWA/PAS | n_p, V_RTN, T_p (cross-check) | L2 | SOAR |

Time range: SO cruise-phase intervals at ~0.5 au — TODO verify exact selection.

## Algorithm/workflow steps

1. **Interval selection** — Identify clean solar-wind intervals at ~0.5 au with simultaneous RPW, MAG, and SWA-PAS coverage.
2. **n_e from V_sc** — Convert RPW spacecraft potential to electron density via the empirical calibration (TODO verify exact calibration / panel used by the paper).
3. **Density PSD** — Compute n_e PSD via Welch / wavelet; fit an inertial-range slope.
4. **Intermittency on n_e** — Compute structure functions S_n(τ) on n_e; report scale-dependent kurtosis or PDF tails.
5. **Wavelet analysis on B** — Wavelet transform B_RTN; compute reduced magnetic helicity σ_m(f, t).
6. **ICW detection** — Identify wavelet events with LH-circular polarisation near the proton-cyclotron frequency band; build an event catalog.
7. **Joint statistics** — Aggregate over intervals; report density-spectral slope, kurtosis exponent, and ICW occurrence rate at ~0.5 au.
8. **Acceptance** — Recover the qualitative density-turbulence statistics and ICW occurrence rate of the paper (TODO verify exact slopes and rates).

## Minimal executable benchmark or validation target

**Target**: at ~0.5 au, RPW-derived n_e PSD slope and intermittency, plus wavelet-identified ICW occurrence rate, match the Carbone 2021 statistics (TODO verify exact numerical values).

Recommended check artifacts:

- `carbone2021_ne_icw.csv` — one row per interval: (t_start, t_end, r_au, slope_n_e_PSD, kurtosis_exponent, ICW_count, ICW_rate).
- Wavelet σ_m(f, t) panel with ICW events marked.
- Single scalar QC: median ICW occurrence rate (events / hour) across the interval set.

## Known pitfalls / failure modes

- **V_sc → n_e calibration**: the spacecraft-potential-to-density calibration is mission-, panel-, and bias-dependent; use the published SO RPW calibration and document its version.
- **Calibration outliers**: low spacecraft-potential intervals (e.g. shadow, photoemission shifts) yield biased n_e — flag and exclude.
- **Wavelet boundary effects**: ICW detection at the start/end of intervals suffers cone-of-influence edge effects; mask boundaries.
- **MAG cadence vs proton cyclotron frequency**: ensure MAG cadence resolves f_cp at 0.5 au (~few Hz) — survey-mode may be insufficient.
- **Doppler shift**: spacecraft-frame frequencies are Doppler-shifted (cf. [[bowen-2024-extended-cyclotron-resonant-heating]]).
- **Solar Orbiter cruise-phase coverage**: 2021-era cruise intervals are limited; statistical claims at 0.5 au have small N — quote N explicitly.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "RPW n_e turbulence + ICW at ~0.5 au" becomes the per-interval CSV + ICW occurrence-rate scalar.
- **Methods / equations → executable workflows**: V_sc → n_e calibration + density PSD/intermittency + wavelet ICW detection are steps 2–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve Solar Orbiter RPW, MAG, and SWA-PAS time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces).
- **Caveats → skill memory**: V_sc calibration version dependency, wavelet edge effects, Doppler shift, cadence requirement.
- **Figures / results → benchmark artifacts**: wavelet σ_m panel + per-interval CSV.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar_orbiter` + `waves_instabilities` bundles (ICW + density-turbulence branch).
- **Sibling paper-skills**: [[bowen-2024-extended-cyclotron-resonant-heating]] (PSP-side ICW detection — independent instrument), [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (cyclotron-resonance mediation argument), [[cuesta-2022-compressible-turbulence-psp-themis-maven]] (density-fluctuation multi-spacecraft context), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (magnetic spectral context at similar distance).
- **MCPs (proposed contracts)**: `solar-orbiter-data-mcp`, `cdflib`, optional `wavelet-polarisation-mcp` synthesis candidate.
- **Harness contract**: exports {slope_n_e, kurtosis_exponent, ICW_rate} per interval at ~0.5 au; HelioSI roll-up consumes it as the SO density-channel ICW row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.14.
- DOI: https://doi.org/10.1051/0004-6361/202140931
- arXiv: https://arxiv.org/abs/2105.07790
- Pedersen et al. — RPW V_sc → n_e calibration (foundational, not from inventory).
