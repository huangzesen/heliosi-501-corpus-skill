---
name: chen-2022-magnetic-field-spectral-evolution-inner-heliosphere
description: Use when characterising the radial evolution of the magnetic-field inertial-range spectral slope across PSP, Helios, and Wind — central paper claim is that the inertial-range slope steepens from ~-3/2 near the Sun to ~-5/3 by ~0.6 au (Chen et al. 2022, arXiv:2209.02451; venue TODO verify).
version: 0.1.0
tags: [psp, helios, wind, magnetic-field, spectral-slope, radial-evolution, turbulence]
quality_level: pilot
executable_status: scaffold
---

# Chen 2022 — Magnetic Field Spectral Evolution (PSP/Helios/Wind)

## When to use this paper-skill

Load this skill when you need to:

- combine **PSP + Helios + Wind** magnetic-field PSDs into a single radial-evolution dataset spanning ~0.1 au to 1 au,
- characterise the **inertial-range slope evolution** from ~-3/2 near the Sun to ~-5/3 by ~0.6 au,
- benchmark a spectral-slope estimator across three instruments / mission eras.

Skip this skill if your interest is the 1/f outer range ([[huang-2023-psp-one-over-f-spectrum]]), compressible / density-channel turbulence ([[cuesta-2022-compressible-turbulence-psp-themis-maven]], [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]]), or kinetic-scale anisotropy ([[zhao-2022-3d-anisotropy-kinetic-scales-psp]]).

## Paper identity and claim boundary

- **Citation**: Chen, C. H. K., et al. (2022). *Magnetic Field Spectral Evolution in the Inner Heliosphere.* arXiv:2209.02451. **Venue TODO verify.**
- **DOI**: TODO verify.
- **arXiv**: [2209.02451](https://arxiv.org/abs/2209.02451)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.15.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> Combined PSP / Helios / Wind magnetic-field PSDs show the inertial-range slope steepening from ~-3/2 near the Sun to ~-5/3 by ~0.6 au.

Out-of-scope: extending the steepening claim beyond ~1 au into the outer heliosphere; conflating the trend with stream-class-specific differences without explicit conditioning (TODO verify whether the paper conditions on Alfvénicity / fast-vs-slow); collapsing the result onto a single encounter.

## Scientific claim to reproduce or operationalize

The inertial-range slope α_B of the magnetic-field trace PSD is not radially constant in the inner heliosphere: near the Sun (~0.1 au, PSP) it is closer to -3/2; by ~0.6 au it has steepened to ~-5/3, with Wind / Helios 1-au measurements consistent with that asymptote.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| Helios MAG | B (RTN / spacecraft frame) | reprocessed L2 | NASA / restored Helios archive |
| Wind MFI | B (GSE) | L2 | CDAWeb |
| (optional) PSP SWEAP, Wind 3DP / SWE | n_p, V_sw (for Taylor mapping) | L3 / L2 | CDAWeb |

Time range: pooled multi-mission samples covering 0.1 to ~1 au — TODO verify exact stream selection.

## Algorithm/workflow steps

1. **Per-mission interval catalog** — Build clean solar-wind intervals per mission (PSP, Helios, Wind), excluding shocks / CMEs.
2. **Trace PSD** — Compute trace magnetic PSD per interval via Welch / multitaper with explicit window length and overlap; report bandwidth.
3. **Inertial-range bounds** — Determine f_low (above the 1/f / outer-scale break — cf. [[huang-2023-psp-one-over-f-spectrum]]) and f_high (below the ion break — cf. [[bowen-2024-extended-cyclotron-resonant-heating]]) per interval.
4. **Slope fit** — Fit α_B in the inertial range; report uncertainty.
5. **Radial binning** — Bin α_B vs heliocentric distance over [0.1, 1] au.
6. **Trend** — Show α_B steepening from ~-3/2 to ~-5/3 over this range.
7. **Acceptance** — Recover the qualitative radial trend reported in the paper; α_B(0.1 au) ≈ -3/2 and α_B(0.6 au) ≈ -5/3 to within paper-stated scatter (TODO verify exact transition distance).

## Minimal executable benchmark or validation target

**Target**: pooled PSP/Helios/Wind α_B vs r curve shows steepening from ~-3/2 to ~-5/3 between 0.1 and 0.6 au, with Wind asymptote consistent with -5/3 (TODO verify exact transition distance and binwise α_B values).

Recommended check artifacts:

- `chen2022_alpha_b_vs_r.csv` — one row per (mission, interval): (mission, t_start, t_end, r_au, alpha_B, alpha_B_err, f_low, f_high).
- Three-panel PSD comparison plot at representative r ∈ {0.15, 0.3, 0.6, 1.0} au.
- Single scalar QC: fitted slope of α_B vs ln(r) (or piecewise model parameters).

## Known pitfalls / failure modes

- **f_low / f_high definition**: the slope is sensitive to the inertial-range bounds; quote them explicitly per interval and avoid global thresholds.
- **Outer-scale contamination**: if f_low encroaches into the 1/f range, α_B flattens artificially (cf. [[huang-2023-psp-one-over-f-spectrum]]).
- **Ion-break contamination**: if f_high enters the kinetic range, α_B steepens artificially.
- **Helios archive caveats**: reprocessed Helios MAG products carry calibration uncertainties — version-pin the dataset.
- **Cadence / Nyquist mismatch**: PSP, Helios, Wind sample at different cadences — match bandwidth before pooling.
- **Stream-class conditioning**: aggregating fast and slow streams can blur the trend if the underlying scaling depends on stream class.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "α_B steepens from ~-3/2 to ~-5/3 between 0.1 and 0.6 au" becomes the multi-mission α_B(r) CSV + the piecewise-fit scalar.
- **Methods / equations → executable workflows**: trace PSD + inertial-range bound determination + slope fit + radial binning are steps 2–5.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG, Helios MAG, and Wind MFI time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces — the Helios reprocessed archive in particular has no guaranteed adapter and falls back to WebFetch + custom readers).
- **Caveats → skill memory**: f_low / f_high sensitivity, outer-scale and ion-break contamination, Helios calibration version pinning.
- **Figures / results → benchmark artifacts**: multi-mission PSD overlay + α_B vs r curve.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` (radial-evolution branch).
- **Sibling paper-skills**: [[huang-2023-psp-one-over-f-spectrum]] (sets f_low context — outer-scale break), [[bowen-2024-extended-cyclotron-resonant-heating]] (sets f_high context — ion-scale break), [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (anisotropy radial evolution complement), [[telloni-2021-psp-solo-radial-alignment-turbulence]] / [[telloni-2025-psp-solo-radial-alignment-2022-december]] (Lagrangian counterparts), [[bandyopadhyay-2020-energy-transfer-psp]] (cascade rate at near-Sun anchor point).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `helios-archive-mcp`, `wind-data-mcp`, `cdflib`. The slope-fit + range-determination pipeline is a candidate Stage-B synthesis skill.
- **Harness contract**: exports α_B(r) curve and per-interval (r, α_B, f_low, f_high); HelioSI roll-up consumes it as the magnetic-spectral-evolution row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.15.
- arXiv: https://arxiv.org/abs/2209.02451
- Bruno & Carbone (2013) review — solar-wind PSD slopes (foundational, not from inventory).
