---
name: telloni-2025-psp-solo-radial-alignment-2022-december
description: Use when analysing the 2022 December PSP–Solar Orbiter radial conjunction for turbulence radial evolution — central paper claim is that structure-function spectral evolution and cross-helicity radial trend in the same approximate plasma parcel are recovered between PSP and SO during the 2022 December alignment (Telloni et al. 2025, ApJS; DOI 10.3847/1538-4365/add011).
version: 0.1.0
tags: [psp, solar-orbiter, radial-alignment, conjunction, turbulence, cross-helicity, structure-functions]
quality_level: pilot
executable_status: scaffold
---

# Telloni 2025 — PSP/SO Radial Alignment 2022 December

## When to use this paper-skill

Load this skill when you need to:

- identify and analyse the **2022 December PSP–Solar Orbiter radial conjunction**,
- compute structure-function spectral evolution and cross-helicity radial trend across a near-Lagrangian PSP→SO mapping,
- compare to the earlier first PSP–SO alignment ([[telloni-2021-psp-solo-radial-alignment-turbulence]]) for cross-event consistency.

Skip this skill if your interest is statistical multi-spacecraft compressibility ([[cuesta-2022-compressible-turbulence-psp-themis-maven]]) or a non-conjunction radial-evolution survey ([[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]).

## Paper identity and claim boundary

- **Citation**: Telloni, D. and collaborators (2025). *Evolution of Solar Wind Turbulence during Radial Alignment of Parker Solar Probe and Solar Orbiter in 2022 December.* **ApJS**.
- **DOI**: 10.3847/1538-4365/add011
- **arXiv**: TODO verify.
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.12.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> During the 2022 December PSP–SO radial alignment, structure-function spectral evolution and cross-helicity radial trend are observed in the approximately co-mapped plasma parcel.

Out-of-scope: collapsing this single-event result into a general statistical statement about all PSP–SO conjunctions, ignoring co-rotation timing uncertainties, or generalising the cross-helicity sign across stream classes that the alignment did not actually sample.

## Scientific claim to reproduce or operationalize

A radial PSP–SO conjunction in 2022 December provides a near-Lagrangian path along which the same approximate plasma parcel is sampled at two heliocentric distances. Structure-function-based spectral evolution and cross-helicity radial trends across this path are reported.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN, T_p | L3 | CDAWeb / PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR / CDAWeb |
| Solar Orbiter SWA/PAS | n_p, V_RTN, T_p | L2 | SOAR / CDAWeb |

Time range: 2022-12 conjunction window (exact start/end **TODO verify** against the paper's selection).

## Algorithm/workflow steps

1. **Conjunction identification** — Find the time window in 2022 December where PSP and SO are within an acceptable angular separation in heliographic longitude (radial alignment).
2. **Plasma-parcel mapping** — Estimate the ballistic mapping τ_map = (r_SO − r_PSP)/V_sw for each PSP sample; pair PSP samples at time t with SO samples at t + τ_map.
3. **Per-spacecraft windows** — Build matched PSP / SO sub-intervals (e.g. 1 h) with continuous MAG + plasma data.
4. **Structure functions** — Compute S₂(τ), S₃(τ) per spacecraft on Elsässer / magnetic increments.
5. **Cross-helicity radial trend** — Compute σ_c per matched window pair; report σ_c(PSP) → σ_c(SO).
6. **Spectral evolution** — Fit inertial-range slopes per window pair; report slope(PSP) → slope(SO).
7. **Acceptance** — Recover the structure-function spectral evolution and cross-helicity radial trend reported in the paper (qualitative sign + magnitude — TODO verify exact numerical values).

## Minimal executable benchmark or validation target

**Target**: matched PSP / SO windows from the 2022-12 alignment yield the structure-function spectral evolution and cross-helicity radial trend reported by Telloni et al. 2025 (TODO verify exact slope and σ_c numerical values).

Recommended check artifacts:

- `telloni2025_alignment_2022dec.csv` — one row per matched window: (t_PSP_start, t_PSP_end, t_SO_start, t_SO_end, r_PSP_au, r_SO_au, slope_B_PSP, slope_B_SO, σ_c_PSP, σ_c_SO).
- PSP vs SO PSD overlay panel.
- Single scalar QC: Δσ_c = σ_c(SO) − σ_c(PSP).

## Known pitfalls / failure modes

- **Mapping ambiguity**: the ballistic mapping ignores stream interaction; mis-mapping breaks the Lagrangian comparison. Use multiple V_sw choices and report sensitivity.
- **Angular-separation tolerance**: the "alignment" criterion (longitudinal separation) drives the selection; different tolerances change the window set.
- **Frame conventions**: PSP and SO use RTN; verify consistent +R / +N orientation before pairing increments.
- **Cadence matching**: SO MAG vs PSP MAG cadences differ — resample to a common bandwidth before structure-function comparison.
- **Non-radial structures**: CIRs / HCS crossings within the conjunction window violate the Lagrangian assumption; exclude such intervals.
- **Single-event statistical caveat**: one alignment cannot bound the population — flag this in any roll-up.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "structure-function and σ_c evolve between PSP and SO during 2022-12 alignment" becomes the matched-window CSV + Δσ_c scalar.
- **Methods / equations → executable workflows**: conjunction identification + ballistic mapping + per-spacecraft structure functions + σ_c comparison are steps 1–5.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS / SWEAP + SO MAG / SWA-PAS as `psp-data-mcp` and `solar-orbiter-data-mcp` (proposed; SOAR retrieval via WebFetch is the guaranteed surface).
- **Caveats → skill memory**: mapping ambiguity, separation tolerance, RTN-frame convention, single-event statistical caveat.
- **Figures / results → benchmark artifacts**: matched-window CSV + PSP/SO PSD overlay.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` + `solar_orbiter` bundles (radial-evolution / conjunction branch).
- **Sibling paper-skills**: [[telloni-2021-psp-solo-radial-alignment-turbulence]] (first alignment — direct methodological predecessor), [[cuesta-2022-compressible-turbulence-psp-themis-maven]] (statistical multi-spacecraft alternative), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (radial spectral steepening context), [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (anisotropy radial evolution).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `solar-orbiter-data-mcp`, `cdflib`. The ballistic-mapping step is a candidate Stage-B synthesis skill.
- **Harness contract**: exports per-window (r_PSP, r_SO, σ_c_PSP, σ_c_SO, slope_B_PSP, slope_B_SO); HelioSI roll-up consumes it as a single-event Lagrangian row complementary to [[telloni-2021-psp-solo-radial-alignment-turbulence]].

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.12.
- DOI: https://doi.org/10.3847/1538-4365/add011
- Telloni et al. 2021 — methodological predecessor (paper-skill [[telloni-2021-psp-solo-radial-alignment-turbulence]]).
