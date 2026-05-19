---
name: zhao-2022-3d-anisotropy-kinetic-scales-psp
description: Use when characterising sub-ion-range 3D anisotropy of magnetic-field fluctuations on PSP FIELDS data in the local mean-field frame — central paper claim is that PSP-resolved kinetic-scale turbulence exhibits direction-dependent (3D) anisotropy with distinct spectral indices along the parallel, perpendicular, and displacement axes (Zhao et al. 2022, ApJL 924, L21).
version: 0.1.0
tags: [psp, turbulence, kinetic-scales, 3d-anisotropy, structure-functions, fields, mean-field-frame]
quality_level: pilot
executable_status: scaffold
---

# Zhao 2022 — 3D Anisotropy and Scaling at Kinetic Scales (PSP)

## When to use this paper-skill

Load this skill when you need to:

- decompose PSP FIELDS magnetic-field fluctuations at sub-ion (kinetic) scales into 3D anisotropic components in a **local mean-field** frame,
- separate parallel (∥), perpendicular (⊥), and displacement-direction spectra or second-order structure functions in the inner heliosphere,
- benchmark a new local-frame anisotropy estimator against an independent published 3D decomposition near the ion break.

Skip this skill if your interest is the MHD inertial range (use [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] or the imbalanced 3D follow-up [[sioulas-2024-higher-order-3d-anisotropy]] from `pilot_turbulence/`), the 1/f outer range ([[huang-2023-psp-one-over-f-spectrum]]), or proton/electron heating partition (use the Bowen / Pecora skills in this batch).

## Paper identity and claim boundary

- **Citation**: Zhao, L.-L., Zank, G. P., Adhikari, L., et al. (2022). *Three-Dimensional Anisotropy and Scaling Properties of Solar Wind Turbulence at Kinetic Scales in the Inner Heliosphere: Parker Solar Probe Observations.* **ApJL 924, L21**.
- **DOI**: 10.3847/2041-8213/ac4415
- **ADS bibcode**: 2022ApJ...924L..21Z
- **arXiv**: TODO verify (no ID in inventory).
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.3.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> Using local-frame 3D second-order structure functions on PSP FIELDS data, sub-ion (kinetic-scale) turbulence shows direction-dependent anisotropy and spectral-index decomposition along axes defined by the local mean magnetic field.

Specific numerical exponents per axis, encounter list, distance bins, and exact ion-scale break frequencies are **TODO verify in full paper**. Do not extend the result beyond the kinetic range or beyond PSP encounters actually sampled by the paper.

## Scientific claim to reproduce or operationalize

The kinetic-range (~k ρ_i ≳ 1) magnetic-field fluctuations measured by PSP FIELDS are not isotropic in a local mean-field frame: a 3D decomposition along the local B₀, the displacement, and the perpendicular complement reveals distinct power levels and spectral slopes per axis. This skill operationalises that claim as a reproducible 3D structure-function pipeline returning slope estimates per axis and per heliocentric-distance bin.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, |B| | L2, RTN, ≥1 vec/s (Burst-mode preferred for kinetic scales) | CDAWeb / PSP SOC (`psp_fld_l2_mag_rtn_*.cdf`, `*_4_per_cycle_*.cdf`) |
| PSP FIELDS DFB AC | search-coil-derived B at higher cadence (optional) | L2 | PSP SOC |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN (for ρ_i, V_A) | L3 | CDAWeb / PSP SOC |

Time range: PSP encounter(s) covered by the paper — TODO verify exact list against full text. The MAG cadence must resolve well above the ion break to expose kinetic-range scaling.

## Algorithm/workflow steps

1. **Interval selection** — Choose quasi-stationary intervals with continuous FIELDS MAG coverage at a cadence resolving sub-ion scales; require valid SPC/SPAN-I plasma moments for ρ_i and V_A.
2. **Local mean field** — At each scale ℓ, compute a scale-dependent mean field B₀(t, ℓ) via a moving average of width ℓ (or equivalent local-frame estimator).
3. **3D local frame** — Define three orthogonal axes at each (t, ℓ): ê_∥ = B̂₀; ê_disp along the spacecraft-relative displacement projected ⊥ B₀; ê_⊥ = ê_∥ × ê_disp.
4. **Second-order structure functions** — Compute S₂^(i)(ℓ) = ⟨|δB(t, ℓ) · ê_i|²⟩ for i ∈ {∥, disp, ⊥}.
5. **Slope fitting** — Fit S₂^(i)(ℓ) ∝ ℓ^{α_i} in the sub-ion range; convert to equivalent spectral indices (β_i = α_i + 1 under Taylor's hypothesis where valid).
6. **Distance binning** — Repeat per heliocentric-distance bin; report (α_∥, α_disp, α_⊥) vs r.
7. **Acceptance** — Recover a direction-dependent (α_∥ ≠ α_⊥ ≠ α_disp) decomposition at kinetic scales consistent with the paper's qualitative ordering (TODO verify per-axis numerical values).

## Minimal executable benchmark or validation target

**Target**: per-axis sub-ion-range slopes (α_∥, α_disp, α_⊥) recovered from PSP FIELDS data are direction-dependent, with the qualitative ordering reported in the paper (TODO verify specific numerical ordering from Fig. / Table in the paper).

Recommended check artifacts:

- `zhao2022_kinetic_anisotropy.csv` — one row per interval × distance bin: (t_start, t_end, r_au, α_∥, α_disp, α_⊥, k_break, β_i).
- Log-log structure-function panel split by axis with fitted slopes.
- A single scalar QC: ratio α_⊥ / α_∥ vs heliocentric distance.

## Known pitfalls / failure modes

- **Scale-dependent vs static mean field**: using a single global B₀ rather than a scale-dependent one collapses the 3D decomposition; the moving-average width must equal ℓ.
- **Taylor hypothesis at sub-ion scales**: V_sw / V_A is finite; the Taylor mapping ω = k · V_sw breaks down for fluctuations co-moving with the plasma (kinetic-Alfvén / cyclotron waves).
- **Cadence / Nyquist**: FIELDS survey-mode cadence may not reach far enough above the ion break — Burst-mode segments are needed.
- **Spin-tone / instrument artefacts**: residual spin lines in MAG inflate parallel-axis power; despun product or notch filters are required.
- **Local-frame sampling bias**: spacecraft trajectory rarely samples all 3D angles equally; report angular coverage explicitly.
- **Ion-scale break position**: scales the fitting window; estimate the break independently per interval rather than assuming a fixed k ρ_i.

## Paper-as-Skill compilation

This paper is compiled into an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "kinetic-scale 3D anisotropy on PSP" becomes the per-axis slope CSV and the α_⊥ / α_∥ scalar.
- **Methods / equations → executable workflows**: scale-dependent local mean field + three-axis decomposition + second-order structure functions become workflow steps 2–5.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS MAG L2 (survey and Burst-mode) + SWEAP plasma moments appear as `psp-data-mcp` contracts; named MCPs remain proposed surfaces — the harness uses Read/Bash/WebFetch + cdflib as the guaranteed substrate.
- **Caveats → skill memory**: Taylor breakdown, scale-dependent B₀ requirement, and the cadence/Nyquist constraint are persistent skill memory.
- **Figures / results → benchmark artifacts**: per-axis slopes per distance bin form the exported reproducibility scalar set.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**, and this paper-skill is a leaf within that graph.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph (kinetic-range branch).
- **Sibling paper-skills**: [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (MHD-range counterpart), [[sioulas-2024-higher-order-3d-anisotropy]] (higher-order, imbalanced-Alfvénic regime), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (radial spectral steepening across MHD-kinetic), [[bowen-2024-extended-cyclotron-resonant-heating]] (ion-cyclotron waves at the spectral break — same scale regime).
- **MCPs (proposed contracts, not assumed runtime)**: `psp-data-mcp` for FIELDS / SWEAP retrieval; `cdflib` / `pyspedas` for I/O.
- **Harness contract**: this skill exports a tuple {α_∥(r), α_disp(r), α_⊥(r)} per heliocentric-distance bin; HelioSI roll-up consumes it as the per-axis kinetic-range anisotropy row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.3.
- IOPscience: https://iopscience.iop.org/article/10.3847/2041-8213/ac4415
- ADS: https://ui.adsabs.harvard.edu/abs/2022ApJ...924L..21Z
- Cho & Lazarian (2004) — anisotropy framework (foundational, not from inventory).
