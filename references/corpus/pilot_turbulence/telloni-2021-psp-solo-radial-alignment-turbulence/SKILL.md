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
- **DOI**: [10.3847/2041-8213/abf7d1](https://doi.org/10.3847/2041-8213/abf7d1) (IOPscience; resolves to ApJL 912, L21; verified 2026-05-19)
- **Source inventory**: `apj_aa_heliophysics_papers.md` §1.11.

**Evidence boundary — what the article body supports (verified 2026-05-19 via IOPscience DOI):**

- **Conjunction window**: PSP at ~0.1 au on **2020-09-27** is radially aligned with Solar Orbiter at ~1 au on **2020-10-02**. Alignment is identified within **±1.5° heliographic longitude** and ±5 km/s in V_sw — these are the published conjunction tolerances.
- **Spectral evolution**: the magnetic-trace inertial-range spectral exponent shifts from **~ -3/2** at PSP (closer to a Iroshnikov–Kraichnan-like / SDDA-flat slope near the Sun) toward **~ -5/3** (Kolmogorov-like) at SO.
- **Turbulence state evolution**: the plasma evolves from a *highly Alfvénic, less-developed* turbulence state near the Sun — high cross-helicity σ_c and good equipartition between magnetic and kinetic energies (i.e. low |σ_R|) — to *fully developed, intermittent* turbulence at 1 au.

**Out-of-evidence-boundary at this verification depth (still TODO_verify_with_full_text):**

- Exact numerical σ_c, σ_R, and ε per spacecraft (the abstract / article body verified at this depth quotes the qualitative direction and the spectral exponents but not the σ_c / σ_R / ε numerical triples).
- The Politano–Pouquet ε derivation choices on this short conjunction window (third-order moment vs Yaglom-law form) — the article describes "energy dissipation rates show directional change" but the specific formula and uncertainty are not extracted here.
- Whether the Parker-spiral or ballistic mapping is the canonical one in the article; both are workflow options consistent with the ±1.5° / ±5 km/s tolerance.

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

**Primary targets** (article-verified 2026-05-19):

1. **Conjunction reproduction**: independent of the science, the conjunction-selection step must return the 2020-09-27 (PSP) / 2020-10-02 (SO) pair within the published tolerance window of ±1.5° heliographic longitude and ±5 km/s in V_sw. A reproduction that misses this window is failing at the data layer, not the science layer.
2. **Spectral-slope evolution**: the fitted inertial-range exponent α_B is ≈ −3/2 at PSP and ≈ −5/3 at SO on the matched intervals. The qualitative *direction* of evolution (steepening with r) is the science target; the exact transition profile is single-event and not required to match.
3. **Turbulence-state evolution**: σ_c is *higher* at PSP than at SO; |σ_R| is *lower* at PSP than at SO (i.e. better magnetic–kinetic equipartition near the Sun). The sign of both Δσ_c and Δ|σ_R| across the conjunction is the discriminator.

The numerical σ_c, σ_R, and ε triples per spacecraft are *not* a target at this verification depth — the article describes the qualitative direction and the spectral exponents, and the third-order ε formula choice was not extracted from the article body here.

Artifacts:

- `telloni2021_conjunction.csv` — rows: spacecraft, t_start, t_end, r_au, alpha_B, sigma_c, sigma_R, epsilon, alpha_B_err.
- A side-by-side figure: PSP vs SO trace PSDs with the −3/2 and −5/3 reference slopes overlaid.
- A scalar QC: sign(Δσ_c) and sign(Δ|σ_R|) across the conjunction (PSP → SO).

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

## Layer 4 — Research-generation affordances

- **Gap:** the article verifies *direction* of σ_c, σ_R, and α_B evolution across the conjunction but the σ_c, σ_R, ε *numerical* triples at each spacecraft are not extracted at this verification depth. Promotion to method-ready requires reading §3 of the published article and copying the per-spacecraft numbers into the validation_targets list. Until then, downstream consumers should treat σ_c, σ_R, ε targets as **qualitative-direction tests only**.
- **Tension:** the article's qualitative claim is that the plasma reaches "fully developed and intermittent turbulence at 1 au". The statistical-ensemble companion [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] reports radial evolution of anisotropic scaling using *many* PSP intervals — but a single conjunction is *one realisation*, not an ensemble. The two methodologies should *agree in direction* but may disagree in *magnitude*; if the conjunction shows a stronger σ_c drop than the statistical ensemble, the conjunction is biased by stream class or by parcel-mapping error rather than constituting a counter-example.
- **Hypothesis:** the steepening from −3/2 to −5/3 across the conjunction is driven by the development of *non-Alfvénic* turbulence components during transit (i.e. by σ_c → 0); stratifying the same conjunction by σ_c sub-window should show that the windows with the largest σ_c drop also carry the largest spectral-slope steepening. The cleanest test is to compute α_B(t) at PSP in σ_c sub-windows and at SO in σ_c sub-windows that map ballistically to the PSP sub-windows.
- **Minimal_experiment:** rerun the conjunction pipeline with *two* parcel-mapping conventions side-by-side — strict ballistic (V_sw uniform) and Parker-spiral (V_sw with rotation). The published tolerance window already permits both; if the σ_c / α_B trends are robust across the two conventions, the conjunction inference is mapping-insensitive (good). If they flip, the result is mapping-driven and the article-level claim needs to be re-stated.
- **Composable experiment:** join the per-spacecraft (α_B, σ_c, σ_R) row from this conjunction with [[bandyopadhyay-2020-energy-transfer-psp]]'s near-Sun ε estimate and the SO-side ε from a Politano–Pouquet evaluation on the matched interval — the *consistent* Lagrangian ε(r) evolution across one realisation is the quantity downstream cascade-rate skills should ingest.
- **Follow-up:** the 2022-Dec second-alignment paper [[telloni-2025-psp-solo-radial-alignment-2022-december]] (already internalized in batch-1) is a *natural ensemble counterpart* to this single-event paper — comparing the two-conjunction trend direction is itself a research output, not a check.

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
- DOI: https://doi.org/10.3847/2041-8213/abf7d1 (IOPscience; ApJL 912, L21, 2021; verified 2026-05-19; conjunction window 2020-09-27 PSP / 2020-10-02 SO; ±1.5° longitude and ±5 km/s tolerance; spectral exponent ~ −3/2 → ~ −5/3)
- ResearchGate (cited in inventory sources): https://www.researchgate.net/publication/351386965_Evolution_of_Solar_Wind_Turbulence_from_01_to_1_au_during_the_First_Parker_Solar_Probe-Solar_Orbiter_Radial_Alignment
