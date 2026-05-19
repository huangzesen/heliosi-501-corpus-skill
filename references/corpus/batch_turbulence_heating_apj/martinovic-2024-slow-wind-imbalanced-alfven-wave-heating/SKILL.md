---
name: martinovic-2024-slow-wind-imbalanced-alfven-wave-heating
description: Use when fitting a reflection-driven imbalanced Alfvén-wave cascade heating model to combined PSP + Solar Orbiter slow-wind intervals between 0.06 au and 1 au — central paper claim is that the model heating rate matches empirical heating from radial temperature gradients across this range (Martinović et al. 2024, arXiv:2403.17352; venue TODO verify).
version: 0.1.0
tags: [psp, solar-orbiter, slow-wind, alfven-wave-cascade, imbalanced-turbulence, reflection-driven, heating]
quality_level: pilot
executable_status: scaffold
---

# Martinović 2024 — Slow-Wind Imbalanced AW Heating (PSP + SO)

## When to use this paper-skill

Load this skill when you need to:

- fit a **reflection-driven imbalanced Alfvén-wave** cascade heating model to PSP + Solar Orbiter slow-wind intervals between 0.06 and 1 au,
- compare model-predicted heating rates to **empirical** heating derived from radial temperature gradients,
- assess whether AW-cascade heating can sustain slow-wind proton temperatures over this range.

Skip this skill if your interest is fast-wind cyclotron heating ([[bowen-2024-extended-cyclotron-resonant-heating]]), Landau-channel partition ([[bowen-2023-landau-damping-proton-electron-heating]]), or coherent-structure heating ([[pecora-2022-coherent-structures-proton-electron-heating]]).

## Paper identity and claim boundary

- **Citation**: Martinović, M. M. and collaborators (2024). *Heating of the Slow Solar Wind by Imbalanced Alfvén-Wave Turbulence from 0.06 au to 1 au: PSP and SO Observations.* arXiv:2403.17352. **Venue TODO verify.**
- **DOI**: TODO verify.
- **arXiv**: [2403.17352](https://arxiv.org/abs/2403.17352)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.16.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> A reflection-driven imbalanced Alfvén-wave cascade model fitted to combined PSP + Solar Orbiter **slow-wind** intervals between 0.06 and 1 au produces a heating rate comparable to the empirical heating rate inferred from radial temperature gradients.

Out-of-scope: extending the conclusion to fast-wind streams; collapsing across stream classes when the paper conditions on slow wind; conflating model heating with cyclotron- or Landau-channel rates without explicit cross-paper analysis.

## Scientific claim to reproduce or operationalize

Slow-wind proton heating from 0.06 to 1 au can be sustained by an imbalanced Alfvén-wave cascade driven by Alfvén-wave reflection at the inhomogeneous background. Fitting the reflection-driven cascade model to combined PSP + SO slow-wind data yields a heating rate compatible with the empirical Q_p from radial T_p gradients.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN, T_p | L3 | CDAWeb / PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR / CDAWeb |
| Solar Orbiter SWA/PAS | n_p, V_RTN, T_p | L2 | SOAR |
| Reflection-driven AW cascade model | empirical / closed-form heating Q_AW(r, z+, z-, L) | external code | TODO verify which model (Chandran-Hollweg-class, van Ballegooijen-class) |

Time range: combined PSP + SO slow-wind intervals spanning 0.06 au to ~1 au — exact selection **TODO verify**.

## Algorithm/workflow steps

1. **Slow-wind selection** — Identify slow-wind intervals per spacecraft (V_sw threshold and / or Alfvénicity / ionic-composition criteria — TODO verify the paper's exact rule).
2. **Elsässer amplitudes** — Compute z± per interval; report (z+², z-², imbalance ratio z+² / z-²).
3. **Outer scale L** — Estimate the correlation length L per interval from the autocorrelation of B or z±.
4. **Reflection-driven AW model** — Evaluate Q_AW = f(z+², z-², L, V_A, dV_A/dr) per the chosen model (TODO verify formula); the imbalanced cascade rate is the input.
5. **Empirical Q_p** — Compute empirical Q_p from radial T_p gradient and adiabatic-expansion baseline.
6. **Comparison** — Compare Q_AW to empirical Q_p per heliocentric-distance bin from 0.06 to 1 au.
7. **Acceptance** — Q_AW ≈ Q_p (within paper-stated tolerance) across the range (TODO verify the exact tolerance and per-bin ratios).

## Minimal executable benchmark or validation target

**Target**: model Q_AW from the reflection-driven imbalanced AW cascade matches empirical Q_p in PSP + SO slow-wind bins between 0.06 and 1 au, to within the paper's stated tolerance (TODO verify exact ratio and tolerance).

Recommended check artifacts:

- `martinovic2024_slow_wind_aw_heating.csv` — one row per interval: (mission, t_start, t_end, r_au, V_sw, z+², z-², imbalance, L, Q_AW, Q_p_empirical, ratio).
- Q_AW vs Q_p scatter with 1:1 reference line.
- Single scalar QC: median Q_AW / Q_p across the slow-wind interval set.

## Known pitfalls / failure modes

- **Slow-wind definition**: a pure V_sw threshold mixes Alfvénic and non-Alfvénic slow streams; consider conditioning on Alfvénicity (cf. [[damicis-2021-alfvenic-nonalfvenic-psp]]).
- **Correlation-length convention**: Q_AW is strongly sensitive to L; the integration limit on the autocorrelation drives the result — document convention.
- **Adiabatic baseline for Q_p**: the empirical heating rate depends on the assumed adiabatic-expansion baseline; spherical vs non-spherical expansion changes the answer.
- **Imbalance amplification near the Sun**: reflection-driven imbalance grows toward the Sun — z+²/z-² evolves with r and must be measured per interval, not assumed.
- **PSP / SO cadence and frame matching**: as for [[telloni-2025-psp-solo-radial-alignment-2022-december]].
- **Mapping ambiguity**: combining PSP and SO statistically (not Lagrangianly) means the heating-rate comparison is a statistical, not parcel-level, statement.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "Q_AW ≈ Q_p in slow wind from 0.06 to 1 au" becomes the per-interval CSV + median Q_AW / Q_p scalar.
- **Methods / equations → executable workflows**: Elsässer amplitudes + correlation length + reflection-driven AW model evaluation + empirical Q_p from T_p gradient are steps 2–5.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS / SWEAP + SO MAG / SWA-PAS as `psp-data-mcp` + `solar-orbiter-data-mcp`; the AW cascade model is an external code — `aw-cascade-mcp` is a proposed interface, not an existing runtime MCP.
- **Caveats → skill memory**: slow-wind class mixing, correlation-length convention, adiabatic baseline.
- **Figures / results → benchmark artifacts**: Q_AW vs Q_p scatter + per-interval CSV.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `coronal_heating` (AW-cascade branch) + `solar_orbiter` (slow-wind PSP-SO pooled).
- **Sibling paper-skills**: [[damicis-2021-alfvenic-nonalfvenic-psp]] (Alfvénic vs non-Alfvénic classification — relevant to slow-wind selection), [[bandyopadhyay-2020-energy-transfer-psp]] (upstream cascade-rate input), [[telloni-2021-psp-solo-radial-alignment-turbulence]] / [[telloni-2025-psp-solo-radial-alignment-2022-december]] (Lagrangian-conjunction context), [[bowen-2023-landau-damping-proton-electron-heating]] (alternative dissipation channel for cross-check), [[bowen-2024-extended-cyclotron-resonant-heating]] (fast-wind cyclotron complement).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `solar-orbiter-data-mcp`, `aw-cascade-mcp` (external model evaluator), `cdflib`.
- **Harness contract**: exports {z+², z-², L, Q_AW, Q_p_empirical} per slow-wind interval; HelioSI roll-up consumes it as the slow-wind AW-heating row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.16.
- arXiv: https://arxiv.org/abs/2403.17352
- Chandran & Hollweg / van Ballegooijen — reflection-driven AW cascade theory (foundational, not from inventory).
