---
name: bowen-2023-landau-damping-proton-electron-heating
description: Use when partitioning solar-wind turbulent dissipation between protons and electrons via a quasilinear Landau-damping cascade model constrained by measured PSP magnetic spectra — central paper claim is that a linear Vlasov + cascade model fed with PSP FIELDS spectra yields proton vs electron heating rates consistent with PSP first-two-perihelia observations (Bowen et al. 2023, arXiv:2301.09713; venue TODO verify).
version: 0.1.0
tags: [psp, turbulence, heating, landau-damping, vlasov, proton-electron-partition, fields]
quality_level: pilot
executable_status: scaffold
---

# Bowen 2023 — Landau-Damping Proton/Electron Heating Partition (PSP)

## When to use this paper-skill

Load this skill when you need to:

- estimate the **proton vs electron heating rate partition** from a measured turbulence spectrum using a quasilinear Landau-damping cascade model,
- combine a **linear Vlasov solver** (returning γ(k) for damped modes) with a forward-cascade transport equation constrained by PSP FIELDS spectra,
- compare model-predicted Q_p / Q_e ratios to PSP-derived empirical heating rates during the first two perihelia.

Skip this skill if your task is cyclotron-resonant ion heating (use [[bowen-2024-extended-cyclotron-resonant-heating]] / [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]), coherent-structure heating ([[pecora-2022-coherent-structures-proton-electron-heating]]), or reflection-driven AW heating ([[martinovic-2024-slow-wind-imbalanced-alfven-wave-heating]]).

## Paper identity and claim boundary

- **Citation**: Bowen, T. A., Bale, S. D., Kasper, J. C., Pulupa, M., et al. (2023). *Estimation of Turbulent Proton and Electron Heating Rates via Landau Damping Constrained by Parker Solar Probe Observations.* arXiv:2301.09713; **venue (ApJ / submission status) TODO verify**.
- **DOI**: TODO verify.
- **arXiv**: [2301.09713](https://arxiv.org/abs/2301.09713)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.6.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> A linear Vlasov solver applied to PSP-measured magnetic-field spectra, combined with a quasilinear Landau-damping cascade model, partitions turbulent heating between protons and electrons during the first two PSP perihelia.

Out-of-scope generalisations to refuse: extending the partition to solar-minimum 1-au streams, to non-Landau (e.g. cyclotron) channels — which are explicitly the domain of sibling Bowen 2024 skills — or to electron temperature anisotropy.

## Scientific claim to reproduce or operationalize

Turbulent cascade energy reaching kinetic scales is dissipated via Landau-resonant damping of compressible / kinetic-Alfvén branches; the wavevector-dependent damping rate γ(k) computed from a linear Vlasov solver on the locally measured plasma parameters, combined with the measured magnetic-spectrum amplitude, allows the cascade flux to be split into Q_p (proton heating) and Q_e (electron heating) channels. The paper claims this partition matches PSP-observed empirical Q_p, Q_e at the first two perihelia.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, trace PSD | L2, ~1 vec/s and Burst-mode | CDAWeb / PSP SOC |
| PSP SWEAP/SPC, SPAN-I, SPAN-e | n_p, V_RTN, T_p, T_e, β_p, β_e | L3 | CDAWeb / PSP SOC |
| Linear Vlasov solver | γ(k), real-frequency ω(k) per mode | external code (e.g. PLUME, NHDS, LEOPARD) | TODO verify which solver the paper uses |

Time range: PSP Encounters 1 and 2 (perihelia 2018-11 and 2019-04, ~0.17 au). Restrict to intervals with simultaneously valid n_p, T_p, T_e and clean MAG PSDs.

## Algorithm/workflow steps

1. **Interval selection** — Quasi-stationary PSP E1 / E2 intervals with valid SPC / SPAN-e moments.
2. **Plasma parameters** — Extract n, T_p, T_e, β_p, β_e, V_A per interval.
3. **Measured magnetic PSD** — Compute the trace magnetic PSD on FIELDS data, with the inertial → kinetic transition (ion break) resolved.
4. **Linear Vlasov spectrum** — Run a linear Vlasov solver (e.g. PLUME-class) over the relevant k range and propagation angles θ_kB; extract γ(k, θ) for the relevant damped branches (KAW + ion-acoustic / slow-mode).
5. **Cascade transport** — Apply a quasilinear cascade equation: ∂ε(k)/∂t + ∇_k · F(k) = −2 γ(k) ε(k); solve for the dissipation profile per branch.
6. **Partition** — Integrate γ_e(k) ε(k) over k → Q_e; integrate γ_p(k) ε(k) → Q_p (per branch contribution attributed to species by the linear damping coefficient).
7. **Empirical comparison** — Compute empirical Q_p, Q_e from radial temperature gradients and PSP velocity profiles; compare to model partition.
8. **Acceptance** — Model Q_p / Q_e and absolute heating rate match empirical values within stated tolerance (TODO verify exact tolerance from the paper).

## Minimal executable benchmark or validation target

**Target**: model-predicted Q_p / Q_e in PSP E1–E2 intervals is consistent with empirical Q_p / Q_e from PSP gradients (TODO verify exact numerical ratio).

Recommended check artifacts:

- `bowen2023_landau_heating.csv` — one row per interval: (t_start, t_end, r_au, β_p, β_e, Q_p_model, Q_e_model, Q_p_empirical, Q_e_empirical, ratio_model, ratio_empirical).
- Linear-Vlasov γ(k) spectrum panel per representative interval.
- Single scalar QC: median ratio of model-to-empirical Q_p.

## Known pitfalls / failure modes

- **Linear-theory limit**: the Vlasov solver assumes small-amplitude, locally homogeneous plasma; the cascade itself is nonlinear and amplitudes near the break can violate this — quote δB/B explicitly.
- **Propagation-angle assumption**: γ(k) depends strongly on θ_kB; assuming a single dominant angle (e.g. perpendicular KAW) over-/underestimates Q_e.
- **β sensitivity**: damping rates are exponentially sensitive to β_p, β_e — moment uncertainties propagate strongly.
- **Empirical Q_p estimation**: radial temperature gradients require a clean per-interval Lagrangian mapping; mis-mapping inflates the empirical Q_p and breaks the comparison.
- **SPAN-e electron moments**: T_e from PSP can be biased by photoelectron contamination in some intervals; flag and exclude.
- **Cascade-rate normalisation**: the cascade flux must be calibrated to the inertial-range ε (e.g. PP / vK) before the partition; use [[bandyopadhyay-2020-energy-transfer-psp]] as the upstream input.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "Landau-damping partition matches empirical Q_p, Q_e at PSP E1–E2" becomes the per-interval CSV + ratio scalar.
- **Methods / equations → executable workflows**: linear-Vlasov γ(k) + quasilinear cascade transport + integration over k are workflow steps 4–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP SPC / SPAN-I / SPAN-e L3 time series at the required cadence, plus a linear-Vlasov dispersion-solver capability (PLUME / NHDS / LEOPARD-class); runtimes bind concrete adapters (see Layer 3 for example bindings — the Vlasov-solver surface in particular is a proposed interface, not an existing runtime adapter).
- **Caveats → skill memory**: β sensitivity, angle assumption, SPAN-e photoelectron bias, and the cascade-rate normalisation requirement are skill memory.
- **Figures / results → benchmark artifacts**: per-interval Q_p / Q_e CSV + γ(k) panel form the exported reproducibility set.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `coronal_heating` / `waves_instabilities` cross-bundle (compressible-cascade dissipation branch).
- **Sibling paper-skills**: [[bandyopadhyay-2020-energy-transfer-psp]] (upstream ε), [[bowen-2024-extended-cyclotron-resonant-heating]] (cyclotron channel), [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (mediating role of cyclotron resonance), [[pecora-2022-coherent-structures-proton-electron-heating]] (alternative coherent-structure partition).
- **MCPs (proposed contracts, not assumed runtime)**: `psp-data-mcp`, `vlasov-solver-mcp` (PLUME / NHDS / LEOPARD-class), `cdflib`.
- **Harness contract**: this skill exports {Q_p_model, Q_e_model, Q_p_empirical, Q_e_empirical} per interval; HelioSI roll-up consumes it as the Landau-channel row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.6.
- arXiv: https://arxiv.org/abs/2301.09713
- Howes et al. (2008) — kinetic cascade model (foundational, not from inventory).
- Klein & Howes — PLUME solver (foundational, not from inventory).
