---
name: telloni-2021-psp-solo-radial-alignment-turbulence
description: Track the radial evolution of cross-helicity, residual energy, and cascade rate from 0.1 to 1 au during the first PSP-Solar Orbiter radial alignment (Telloni et al. 2021, ApJL 912, L21).
version: 0.1.0
tags: [psp, solar-orbiter, radial-alignment, cross-helicity, residual-energy, cascade-rate]
quality_level: pilot
executable_status: scaffold
---

# Telloni 2021 — PSP–Solar Orbiter First Radial Alignment

## When to use this paper-skill

Load this skill when you need to:

- exploit a **radial-alignment conjunction** between PSP and Solar Orbiter to measure radial evolution of MHD turbulence in (approximately) the same plasma parcel,
- compute **normalised cross-helicity σ_c**, **residual energy σ_R**, and **cascade rate ε** at two heliocentric distances and compare them,
- benchmark conjunction-based methodology before generalising to later alignments (e.g. the 2022-Dec follow-up by the same team).

## Paper identity and claim boundary

- **Citation**: Telloni, D., Sorriso-Valvo, L., Woodham, L. D., Panasenco, O., Velli, M., Carbone, F., et al. (2021). *Evolution of Solar Wind Turbulence from 0.1 to 1 au during the First Parker Solar Probe–Solar Orbiter Radial Alignment*. **ApJL 912, L21**.
- **DOI**: 10.3847/2041-8213/abf7d1
- **Source inventory**: `apj_aa_heliophysics_papers.md` §1.11.

**Claim boundary** — supported by inventory:

> PSP + SO radial conjunction; cross-helicity, residual energy, and cascade-rate evolution from 0.1 to 1 au.

Exact σ_c, σ_R, and ε numbers at each spacecraft, and the exact conjunction date / duration, are **TODO verify in full paper**.

## Scientific claim to reproduce or operationalize

During the first PSP–SO radial-alignment conjunction, the normalised cross-helicity σ_c, residual energy σ_R, and energy cascade rate ε can be measured at ~0.1 au (PSP) and ~1 au (SO) under conditions approximating the same plasma parcel. The radial trends of these three quantities provide a single-event-but-direct test of theoretical predictions for MHD turbulence radial evolution.

## Required data/instruments and likely files/archives

| Mission/Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | V_RTN, n_p | L3 | PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR |
| Solar Orbiter SWA/PAS | V_RTN, n_p | L2/L3 | SOAR |

Time range: first PSP–SO radial-alignment conjunction (TODO verify exact date in full paper — typically reported as a specific multi-hour interval).

## Algorithm/workflow steps

1. **Conjunction selection** — From orbit ephemerides, identify the alignment interval; window each spacecraft's data to the comparable plasma-parcel arrival times (use ballistic and/or Parker-spiral mapping).
2. **Elsässer fields** — Compute z± = V ± B/√(μ₀ρ).
3. **Cross-helicity / residual energy** — Per spacecraft, compute:
   - σ_c(ℓ or τ) = (⟨|z⁺|²⟩ − ⟨|z⁻|²⟩) / (⟨|z⁺|²⟩ + ⟨|z⁻|²⟩),
   - σ_R(ℓ or τ) = (⟨|δV|²⟩ − ⟨|δB|²⟩) / (⟨|δV|²⟩ + ⟨|δB|²⟩).
4. **Cascade rate** — Compute ε via the Politano–Pouquet third-order law (same convention as [[bandyopadhyay-2020-energy-transfer-psp]]).
5. **Radial comparison** — Tabulate σ_c, σ_R, ε at the two distances; plot vs r.
6. **Acceptance** — The reported direction of radial evolution of σ_c, σ_R, and ε matches the published figure (TODO verify direction and magnitudes).

## Minimal executable benchmark or validation target

**Target**: σ_c, σ_R, and ε computed at PSP (~0.1 au) and SO (~1 au) for the first-alignment interval; the *direction* of evolution (toward more or less Alfvénic, toward larger or smaller ε, etc.) is consistent with the paper's reported trend (TODO verify direction in full paper).

Artifacts:

- `telloni2021_conjunction.csv` — rows: spacecraft, t_start, t_end, r_au, sigma_c, sigma_R, epsilon.
- a side-by-side figure: PSP vs SO spectra of |z⁺|² and |z⁻|².

## Known pitfalls / failure modes

- **Parcel-mapping uncertainty**: ballistic vs Parker-spiral mapping can shift the SO window by hours; the matched intervals are inherently approximate.
- **Stream context**: the conjunction may sample different stream types at the two spacecraft (the same source region can produce different in-situ signatures after radial evolution and stream interactions); attribute trends carefully.
- **Spectral estimator consistency**: σ_c, σ_R, and ε must be computed with the same windowing / cadence / inertial-range definition at both spacecraft.
- **Plasma density gaps**: ρ-normalisation drives z± amplitudes; SPC / PAS gaps must be handled consistently.
- **Single-event statistics**: results are one realisation, not a statistical ensemble — qualitative agreement with theory is the right target.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "σ_c, σ_R, and ε evolve radially between PSP (~0.1 au) and SO (~1 au) during the first alignment" becomes the validation target — direction-of-evolution agreement with the published figure.
- **Methods / equations → executable workflows**: Elsässer construction, σ_c / σ_R definitions, and Politano–Pouquet ε become workflow steps 2–4, each a callable unit and intentionally shared with [[bandyopadhyay-2020-energy-transfer-psp]].
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS + SWEAP and Solar Orbiter MAG + SWA/PAS time series in the RTN frame on a shared common cadence, plus a spacecraft-ephemeris capability for radial-conjunction selection; the runtime supplies concrete adapters bound to those capabilities (see Layer 3 for example bindings).
- **Caveats / failure modes → skill memory**: parcel-mapping uncertainty, stream-context mismatch, estimator-consistency across spacecraft, density-gap handling, and single-event statistics are persistent memory consulted before quoting a radial trend.
- **Figures / results → benchmark artifacts**: the conjunction CSV (`telloni2021_conjunction.csv`) and the PSP-vs-SO Elsässer-spectrum side-by-side figure are the benchmark artifacts; both are designed to be re-consumed by the 2025 follow-up paper-skill.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[bandyopadhyay-2020-energy-transfer-psp]] (cascade-rate method), [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (statistical-ensemble radial mapping that complements this single-conjunction view), [[damicis-2021-alfvenic-nonalfvenic-psp]] (σ_c-based stream classification).
- **Follow-up paper**: Telloni et al. 2025 (ApJS) on the 2022-Dec radial alignment is a natural next paper-skill; this skill should expose a clean cross-conjunction API for that follow-up.
- **MCPs used**:
  - `psp-data-mcp` and `solar-orbiter-data-mcp`.
  - Orbit-ephemeris MCP / `SSCWeb`-style endpoint for conjunction identification.
- **Harness contract**: exports a conjunction table (CSV) and spectral comparison figure; downstream harness can chain to ε and σ_c radial-evolution tables from other paper-skills.

## References

- Inventory: `apj_aa_heliophysics_papers.md` §1.11.
- DOI: 10.3847/2041-8213/abf7d1
- ResearchGate (cited in inventory sources): https://www.researchgate.net/publication/351386965_Evolution_of_Solar_Wind_Turbulence_from_01_to_1_au_during_the_First_Parker_Solar_Probe-Solar_Orbiter_Radial_Alignment
