---
name: damicis-2021-alfvenic-nonalfvenic-psp
description: Stratify PSP inner-heliosphere intervals by Alfvénicity (cross-helicity, residual energy) and compare spectral / scaling properties of Alfvénic vs non-Alfvénic streams (arXiv 2101.00830).
version: 0.1.0
tags: [psp, alfvenicity, cross-helicity, residual-energy, stream-classification]
quality_level: pilot
executable_status: scaffold
---

# Alfvénic vs Non-Alfvénic Turbulence in the Inner Heliosphere (arXiv 2101.00830)

## When to use this paper-skill

Load this skill when you need to:

- **stratify PSP intervals by Alfvénicity** using the normalised cross-helicity σ_c and residual energy σ_R,
- compare **spectral indices** and other turbulence diagnostics between Alfvénic (|σ_c| → 1) and non-Alfvénic (|σ_c| ~ 0) PSP streams,
- test radial / expansion-driven hypotheses for Alfvénicity evolution between ~0.1 au and ~0.5 au using the inner-heliosphere PSP coverage.

## Paper identity and claim boundary

- **Slug requested by user**: `damicis-2021-alfvenic-nonalfvenic-psp`. **Important attribution caveat**: the user-supplied arXiv ID **2101.00830** appears with two different attributions in the provided inventories:
  - `apj_aa_heliophysics_papers.md` §1.13 lists arXiv 2101.00830 under "D'Amicis, R., Bruno, R., Panasenco, O., Telloni, D., et al. (2021), A&A — *Alfvénic versus Non-Alfvénic Turbulence in the Inner Heliosphere as Observed by Parker Solar Probe*."
  - `solar_wind_turbulence_2020_2026.md` entry #4 (2021) lists the same arXiv 2101.00830 under "Chen Shi, Marco Velli, Olga Panasenco, Anna Tenerani (2021) — *Alfvénic versus non-Alfvénic turbulence in the inner heliosphere as observed by Parker Solar Probe*", with methods "Statistical survey over PSP Encounters 1–5; classification by Alfvénicity (σ_c, σ_R); spectral-index measurements vs heliocentric distance and stream context; tests of expansion-driven evolution."

  These two inventory entries are inconsistent. Without resolving the conflict against the actual arXiv 2101.00830 abstract, the **safer attribution is Shi et al. (2021)** (the more detailed inventory). The user's slug `damicis-2021-...` is retained per the task spec, but the SKILL is grounded in the methodologically detailed Shi et al. (2021) record from `solar_wind_turbulence_2020_2026.md`. **TODO verify the correct attribution of arXiv 2101.00830 against the live abstract before manuscript citation.**

- **arXiv**: [2101.00830](https://arxiv.org/abs/2101.00830)
- **Year**: 2021
- **Journal**: A&A (per §1.13 attribution); to verify.

**Claim boundary** — grounded in the more detailed inventory entry:

> Statistical survey over PSP Encounters 1–5; classification by Alfvénicity (σ_c, σ_R); spectral-index measurements vs heliocentric distance and stream context; tests of expansion-driven evolution.

Exact σ_c / σ_R thresholds, exact spectral-index numbers, and exact stream counts are **TODO verify in full paper**.

## Scientific claim to reproduce or operationalize

Inner-heliosphere PSP intervals can be statistically classified into Alfvénic vs non-Alfvénic streams via σ_c and σ_R, and the two populations exhibit **distinct spectral indices** and distinct radial / stream-context dependencies, with the differences interpretable in terms of expansion-driven evolution of MHD turbulence.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | V_RTN, n_p | L3 | PSP SOC |

Time range: PSP Encounters 1–5 (per the inventory entry).

## Algorithm/workflow steps

1. **Interval cataloging** — Build a catalog of quasi-stationary intervals in PSP E1–E5, with comparable interval lengths and inertial-range coverage.
2. **Elsässer fields** — Compute z± = V ± B/√(μ₀ρ).
3. **σ_c and σ_R** — Compute per interval:
   - σ_c = (⟨|z⁺|²⟩ − ⟨|z⁻|²⟩) / (⟨|z⁺|²⟩ + ⟨|z⁻|²⟩),
   - σ_R = (⟨|δV|²⟩ − ⟨|δB|²⟩) / (⟨|δV|²⟩ + ⟨|δB|²⟩).
4. **Stratification** — Classify intervals as "Alfvénic" (|σ_c| above a threshold, e.g. 0.6 — TODO verify) vs "non-Alfvénic" (|σ_c| below a smaller threshold).
5. **Spectral indices** — Compute trace PSDs of B and V per interval; fit inertial-range slope.
6. **Radial and stream-context dependence** — Plot σ_c, σ_R, and slopes vs heliocentric distance, stratified by Alfvénic / non-Alfvénic class.
7. **Acceptance** — Recover the two-population picture: Alfvénic intervals show systematically different inertial-range slope vs non-Alfvénic intervals (TODO verify direction).

## Minimal executable benchmark or validation target

**Target**: a stratified table of (σ_c, σ_R, inertial-range slope) per PSP interval in E1–E5, with the Alfvénic / non-Alfvénic classes occupying distinct regions of the σ_c–slope plane.

Artifacts:

- `damicis2021_stratification.csv` — columns: t_start, t_end, r_au, sigma_c, sigma_R, slope_B, slope_V, class.
- a σ_c–slope scatter plot with class colouring.

## Known pitfalls / failure modes

- **Threshold sensitivity**: results depend on the σ_c cutoff for the Alfvénic class; report dependence on threshold.
- **σ_c estimator window**: σ_c can be defined per scale or per interval. The two conventions are not equivalent — use a single one.
- **Density gaps**: ρ-normalisation issues propagate into z± and σ_c. Document the gap-handling policy.
- **Stream interfaces**: stream-interface crossings can spuriously depress σ_c; exclude or mark them.
- **Encounter mix bias**: heliocentric-distance distribution across E1–E5 is non-uniform; weight per-bin statistics accordingly.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "Alfvénic vs non-Alfvénic PSP streams have distinct spectral indices and distinct radial / stream-context dependencies" becomes the validation target — distinct regions in the σ_c–slope plane.
- **Methods / equations → executable workflows**: Elsässer construction, σ_c / σ_R definitions, thresholding by |σ_c|, and inertial-range slope fitting become workflow steps 2–6, each a callable unit.
- **Data / instruments → MCP / tool contracts**: PSP FIELDS MAG L2 + SWEAP L3 surfaced via `psp-data-mcp`; the Alfvénicity-based segmentation can lean on the `sw-scanner` interface.
- **Caveats / failure modes → skill memory**: threshold sensitivity, σ_c estimator-window convention, density-gap handling, stream-interface contamination, and encounter-mix weighting are persistent memory consulted before reporting a class-stratified slope.
- **Figures / results → benchmark artifacts**: the stratification CSV (`damicis2021_stratification.csv`) and the σ_c–slope scatter are the exported benchmark artifacts; the table is intended to be a canonical covariate for downstream turbulence paper-skills.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[telloni-2021-psp-solo-radial-alignment-turbulence]] (uses σ_c and σ_R in a single conjunction), [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (anisotropy radial map that benefits from Alfvénicity stratification), [[chen-2021-near-sun-streamer-belt-turbulence]] (a complementary E4 streamer-belt stream study).
- **MCPs used**:
  - `psp-data-mcp` for MAG L2 + SWEAP L3.
  - `sw-scanner` for Alfvénicity-based interval segmentation.
- **Harness contract**: this skill exports a "stratification table" of (σ_c, σ_R, slope_B, slope_V) per interval; this table is a canonical covariate for many downstream turbulence paper-skills.

## References

- Inventory (attribution A): `apj_aa_heliophysics_papers.md` §1.13 — D'Amicis et al. (2021), A&A.
- Inventory (attribution B): `solar_wind_turbulence_2020_2026.md` entry #4 — Shi, Velli, Panasenco, Tenerani (2021).
- arXiv: https://arxiv.org/abs/2101.00830
- **Cross-attribution discrepancy: TODO verify which entry the arXiv ID belongs to before citing.**
