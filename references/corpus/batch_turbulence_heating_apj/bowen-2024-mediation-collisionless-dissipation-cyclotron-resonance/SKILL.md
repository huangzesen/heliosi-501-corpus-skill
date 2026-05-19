---
name: bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance
description: Use when arguing that cyclotron resonance — not Landau / KAW damping alone — mediates collisionless turbulent dissipation in the inner heliosphere — central paper claim is that PSP FIELDS ion-scale magnetic spectra exhibit circular-polarisation signatures and resonant-heating diagnostics consistent with cyclotron resonance acting as the mediating dissipation mechanism (Bowen et al. 2024, Nature Astronomy; PMID 38659611).
version: 0.1.0
tags: [psp, cyclotron-resonance, collisionless-dissipation, ion-scale, polarisation, nature-astronomy, fields]
quality_level: pilot
executable_status: scaffold
---

# Bowen 2024 — Mediation of Collisionless Dissipation by Cyclotron Resonance (PSP)

## When to use this paper-skill

Load this skill when you need to:

- test whether the **collisionless dissipation** of solar-wind turbulence is mediated by **cyclotron resonance** rather than by KAW / Landau damping alone,
- inspect ion-scale magnetic spectra for **circular-polarisation signatures** that constrain the dissipation mechanism,
- combine PSP FIELDS spectra with resonant-heating diagnostics to argue for a specific dissipation pathway.

Skip this skill if your question is the observational detection of ICW peaks in fast streams (use [[bowen-2024-extended-cyclotron-resonant-heating]]) or the Landau-channel proton/electron partition (use [[bowen-2023-landau-damping-proton-electron-heating]]).

## Paper identity and claim boundary

- **Citation**: Bowen, T. A., Bale, S. D., Chandran, B. D. G., et al. (2024). *Mediation of Collisionless Turbulent Dissipation Through Cyclotron Resonance.* **Nature Astronomy** (PMID 38659611).
- **DOI**: TODO verify (Nature Astronomy DOI).
- **arXiv**: TODO verify.
- **PubMed**: 38659611.
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.9.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> PSP FIELDS magnetic spectra at ion scales, combined with circular-polarisation analysis and resonant-heating diagnostics, are consistent with cyclotron resonance mediating collisionless dissipation in solar-wind turbulence.

Out-of-scope: claiming cyclotron resonance is the unique dissipation channel everywhere; collapsing this statement onto a single perihelion or encounter; extending to electron-scale dissipation without separate evidence.

## Scientific claim to reproduce or operationalize

At ion scales, PSP FIELDS magnetic spectra exhibit polarisation signatures (handedness, ellipticity, helicity) characteristic of cyclotron resonance with the proton population; combined with resonant-heating diagnostics, these features place the dissipation channel in the cyclotron-resonant regime rather than purely in Landau / KAW damping.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, full-vector PSD, magnetic helicity σ_m | L2, ≥1 vec/s; Burst-mode for ion-scale resolution | CDAWeb / PSP SOC |
| PSP SWEAP/SPC, SPAN-I | n_p, V_RTN, T_p⊥, T_p∥ | L3 | CDAWeb / PSP SOC |

Time range: representative PSP intervals covering a range of stream classes and heliocentric distances (TODO verify exact encounter list from full paper).

## Algorithm/workflow steps

1. **Interval selection** — Quasi-stationary PSP intervals with FIELDS Burst-mode or high-cadence MAG and valid SPC/SPAN-I moments.
2. **Mean-field-aligned frame** — Compute scale-dependent local B₀ and rotate B into a (∥, ⊥1, ⊥2) frame.
3. **Polarisation diagnostics** — Compute reduced normalised magnetic helicity σ_m(f), ellipticity ε(f), polarisation angle relative to B₀.
4. **Cyclotron signature** — Identify frequencies / wavenumbers where σ_m is strongly LH (negative under PSP convention — TODO verify convention) and ellipticity → 1 (circular).
5. **Resonance overlap** — Combine the local proton distribution function with the cyclotron resonance condition ω − k_∥ v_∥ = ±Ω_p; compute the fraction of proton phase space resonant with the wave band.
6. **Heating-rate diagnostic** — Estimate Q_p from quasilinear theory using the measured wave amplitude and resonance overlap; compare to alternative channels (Landau / KAW).
7. **Acceptance** — Circular-polarisation signature + resonance overlap together imply a cyclotron-mediated dissipation channel; Q_p,cyc is comparable to or dominates Q_p,Landau (TODO verify exact ratio in full paper).

## Minimal executable benchmark or validation target

**Target**: ion-scale PSP magnetic spectra show LH-circular-polarised signatures with resonance overlap to the proton distribution; the implied Q_p,cyc is consistent with the paper's conclusion that cyclotron resonance mediates the dissipation (TODO verify magnitudes / Fig. in full paper).

Recommended check artifacts:

- `bowen2024_mediation_cyclotron.csv` — one row per interval: (t_start, t_end, r_au, σ_m_band, ε_band, resonance_overlap, Q_p,cyc, Q_p,Landau, ratio).
- σ_m(f) / ellipticity diagnostic panel per representative interval.
- Single scalar QC: Q_p,cyc / Q_p,Landau median across the interval set.

## Known pitfalls / failure modes

- **Frame and handedness convention**: same caveat as [[bowen-2024-extended-cyclotron-resonant-heating]] — the LH/RH sign depends on the chosen +B₀ direction; an inverted convention reverses the conclusion.
- **Reduced vs full helicity**: spacecraft give reduced helicity (1D measurement along V_sw); inferring 3D polarisation from this requires assumptions about k orientation.
- **Resonance-overlap estimate**: the overlap integral depends sensitively on the assumed parallel-velocity distribution, which is only well measured for protons (SPC field-of-view limitations).
- **Wave-vs-structure ambiguity**: not all narrow-band features at ion scales are waves; some may be coherent structures (cf. [[pecora-2022-coherent-structures-proton-electron-heating]]) — control with structure metrics.
- **Cadence requirement**: ion-scale polarisation needs Burst-mode cadence; survey-mode aliases the signal.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "cyclotron resonance mediates collisionless dissipation" becomes the per-interval CSV + Q_p,cyc / Q_p,Landau scalar.
- **Methods / equations → executable workflows**: mean-field frame + reduced helicity + ellipticity + resonance overlap + quasilinear Q_p,cyc are steps 2–6.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS MAG L2 Burst + SWEAP moments as `psp-data-mcp`; named MCPs remain proposed surfaces.
- **Caveats → skill memory**: convention sensitivity, reduced-vs-full helicity caveat, wave-vs-structure ambiguity.
- **Figures / results → benchmark artifacts**: σ_m / ellipticity diagnostic panel + per-interval CSV.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `waves_instabilities` + `coronal_heating` bundles (collisionless-dissipation mechanism branch).
- **Sibling paper-skills**: [[bowen-2024-extended-cyclotron-resonant-heating]] (observational fast-stream identification), [[bowen-2023-landau-damping-proton-electron-heating]] (Landau channel — the explicit alternative this paper contrasts with), [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] (independent ICW evidence from Solar Orbiter density), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (spectral-break radial evolution context), [[zhao-2022-3d-anisotropy-kinetic-scales-psp]] (kinetic-scale anisotropy context).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `cdflib`, optional `wavelet-polarisation-mcp` (shared synthesis candidate with the extended-cyclotron skill).
- **Harness contract**: exports {σ_m_band, ε_band, Q_p,cyc, Q_p,Landau, ratio} per interval; HelioSI roll-up consumes it as the cyclotron-mediation row complementary to the Landau-partition row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.9.
- Nature Astronomy: PMID 38659611 (DOI TODO verify).
- Howes (2008) and Klein & Howes — kinetic-cascade theory (foundational, not from inventory).
