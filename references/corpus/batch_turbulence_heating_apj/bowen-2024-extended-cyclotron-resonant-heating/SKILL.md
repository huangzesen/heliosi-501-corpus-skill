---
name: bowen-2024-extended-cyclotron-resonant-heating
description: Use when diagnosing ion-cyclotron resonant heating at the magnetic-spectral break in PSP fast streams — central paper claim is that left-hand circularly polarised ion-cyclotron waves at the break frequency mediate an extended cyclotron-resonant heating channel in fast solar wind between ~15–55 R☉ (Bowen et al. 2024, arXiv:2406.10446; venue ApJ TODO verify).
version: 0.1.0
tags: [psp, fast-wind, ion-cyclotron-waves, cyclotron-resonance, heating, spectral-break, fields, polarisation]
quality_level: pilot
executable_status: scaffold
---

# Bowen 2024 — Extended Cyclotron-Resonant Heating (PSP Fast Wind)

## When to use this paper-skill

Load this skill when you need to:

- identify **left-hand circularly polarised ion-cyclotron waves (ICWs)** at the magnetic-spectral break in PSP FIELDS data,
- estimate the cyclotron-resonant heating rate associated with those waves in PSP **fast-stream** intervals between ~15–55 R☉,
- argue for an **extended** cyclotron-heating channel (i.e. extending over a wide near-Sun radial range), as opposed to a single-distance result.

Skip this skill if you need the more theoretical mediation argument (use [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]) or Landau-channel partitioning (use [[bowen-2023-landau-damping-proton-electron-heating]]).

## Paper identity and claim boundary

- **Citation**: Bowen, T. A., Mallet, A., Squire, J., Bale, S. D., et al. (2024). *Extended Cyclotron Resonant Heating of the Turbulent Solar Wind.* arXiv:2406.10446. **Venue (ApJ) TODO verify.**
- **DOI**: TODO verify.
- **arXiv**: [2406.10446](https://arxiv.org/abs/2406.10446)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.8.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> Left-hand circularly polarised ICWs are identified at the spectral break in PSP fast streams over ~15–55 R☉, and the associated cyclotron-resonant heating rate is estimated; the channel extends across a wide near-Sun radial range, not just a single perihelion.

Out-of-scope: extending the claim to slow non-Alfvénic wind, to 1 au, or to electron heating; conflating with stochastic-heating diagnostics ([[chandran-2010-stochastic-heating]] in upstream literature) without explicit cross-paper analysis.

## Scientific claim to reproduce or operationalize

A persistent feature near the magnetic-spectral break in PSP fast streams is a left-handed circularly polarised wave population identified with ion-cyclotron waves. Their amplitude and resonance with the ion thermal population imply a cyclotron-resonant heating rate; the paper shows this channel is active over a wide radial range (~15–55 R☉), supporting an extended (rather than localised) cyclotron-heating scenario.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, full-vector PSD at ion-scale frequencies | L2, ≥1 vec/s, Burst-mode preferred | CDAWeb / PSP SOC |
| PSP FIELDS DFB AC | high-cadence B for ICW resolution (optional) | L2 | PSP SOC |
| PSP SWEAP/SPC, SPAN-I | n_p, V_RTN, T_p, T_p⊥ / T_p∥ | L3 | CDAWeb / PSP SOC |

Time range: PSP fast-stream intervals spanning ~15–55 R☉ — multi-encounter coverage. Restrict to intervals with high Alfvénicity and clean MAG.

## Algorithm/workflow steps

1. **Stream selection** — Identify fast-wind intervals between ~15 and 55 R☉ across PSP encounters; require Alfvénic stream criteria (high σ_c).
2. **Spectral break** — Determine the magnetic-spectral break frequency f_b per interval from the trace PSD; use it as the central frequency for ICW search.
3. **Polarisation analysis** — Compute magnetic helicity / signed normalised reduced helicity σ_m(f, t) (e.g. via wavelet or short-time FFT in mean-field-aligned coordinates); identify left-hand circularly polarised peaks near f_b.
4. **ICW band integration** — Define a band around f_b and integrate the LH-polarised power δB_ICW².
5. **Resonance condition** — Estimate the resonant velocity v_res from ω − k_∥ v_res = ±Ω_p (cyclotron condition) using local plasma parameters.
6. **Heating-rate estimate** — Convert δB_ICW² + resonance overlap with the proton distribution to a quasilinear heating rate Q_p,ICW per interval (use a closed-form quasilinear expression — TODO verify exact formula).
7. **Radial aggregation** — Bin Q_p,ICW vs heliocentric distance over 15–55 R☉; show channel persistence.
8. **Acceptance** — LH ICW peak near the break is detected over the majority of fast-stream intervals across the radial range, and Q_p,ICW magnitudes are consistent with paper (TODO verify exact magnitudes).

## Minimal executable benchmark or validation target

**Target**: LH-circular-polarised ICW band identified near the spectral break across PSP fast-stream intervals between ~15–55 R☉, with a Q_p,ICW estimate consistent with the paper's reported values (TODO verify exact range).

Recommended check artifacts:

- `bowen2024_extended_cyclotron.csv` — one row per interval: (t_start, t_end, r_au, f_b, δB_ICW², Q_p,ICW, σ_c, σ_m_band).
- σ_m(f, t) spectrogram per representative interval.
- Single scalar QC: fraction of fast-stream intervals with detectable LH-polarised peak at f_b.

## Known pitfalls / failure modes

- **Polarisation sign / handedness convention**: the LH/RH convention depends on the chosen reference frame (plasma vs spacecraft, +B₀ direction) — be explicit; an inverted sign trivially reverses the conclusion.
- **Doppler shift**: spacecraft-frame frequencies are Doppler-shifted; ICW identification requires either an inertial-frame correction or a careful argument that the shift is small.
- **Spin-tone leakage**: residual MAG spin lines can mimic narrow-band power near the break.
- **Cadence**: low survey-mode cadence aliases the near-break power; Burst-mode is preferred.
- **Stream class**: ICW features are stronger in Alfvénic fast wind; mixing in slow streams dilutes detection statistics.
- **Quasilinear assumption**: Q_p,ICW formula assumes small-amplitude waves — verify δB/B₀ at the band.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "extended cyclotron-resonant heating channel in PSP fast streams over 15–55 R☉" becomes the per-interval CSV + the radial Q_p,ICW(r) curve.
- **Methods / equations → executable workflows**: spectral-break detection + magnetic helicity/polarisation analysis + cyclotron resonance condition + quasilinear heating estimate are steps 2–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 (+ optional DFB AC) and SWEAP plasma-moment time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings).
- **Caveats → skill memory**: handedness convention, Doppler-shift caveat, spin-tone leakage are persistent skill memory.
- **Figures / results → benchmark artifacts**: σ_m(f, t) spectrogram + radial Q_p,ICW curve.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `waves_instabilities` + `coronal_heating` bundles (ion-scale wave-heating branch).
- **Sibling paper-skills**: [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (companion mechanism paper), [[bowen-2023-landau-damping-proton-electron-heating]] (Landau channel — alternative dissipation pathway), [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] (ICW identification on Solar Orbiter density data — same wave class, different instrument), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (spectral break radial evolution context).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `cdflib`, an optional `wavelet-polarisation-mcp` (the wavelet helicity estimator is a candidate synthesis-skill).
- **Harness contract**: exports {f_b, δB_ICW², Q_p,ICW} per (interval, r); HelioSI roll-up consumes it as the cyclotron-channel row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.8.
- arXiv: https://arxiv.org/abs/2406.10446
- Marsch (2006) — solar-wind cyclotron-heating review (foundational, not from inventory).
