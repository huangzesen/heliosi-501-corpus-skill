---
name: telloni-2025-psp-solo-radial-alignment-2022-december
description: Use when analysing the 2022 December PSP–Solar Orbiter radial conjunction for turbulence radial evolution — central paper claim is that structure-function spectral evolution and cross-helicity radial trend in the same approximate plasma parcel are recovered between PSP and SO during the 2022 December alignment (Silwal et al. 2025, ApJS 278; DOI 10.3847/1538-4365/add011). Slug retained for backwards compatibility; lead author of the published paper is Silwal, not Telloni (verified 2026-05-19).
version: 0.1.0
tags: [psp, solar-orbiter, radial-alignment, conjunction, turbulence, cross-helicity, structure-functions]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "A. Silwal"
  authors:
    - "A. Silwal"
    - "L. Zhao"
    - "X. Zhu"
    - "L. Sorriso-Valvo"
    - "L. Z. Hadid"
    - "G. P. Zank"
  authors_verified: false
  doi: "10.3847/1538-4365/add011"
  arxiv_id: null
  year: 2025
  venue: "The Astrophysical Journal Supplement Series 278 (2025)"
---

# Silwal 2025 — PSP/SO Radial Alignment 2022 December (slug: telloni-2025-…)

> **Attribution note (verified 2026-05-19).** The IOPscience landing page for DOI 10.3847/1538-4365/add011 lists **A. Silwal** as first author, not D. Telloni. The corpus slug is retained for backwards compatibility but the cited lead author is now A. Silwal. Inventories that name "Telloni 2025" for this DOI are *paraphrases* — use Silwal et al. 2025, ApJS 278 (2025) when citing this entry in a manuscript.

## When to use this paper-skill

Load this skill when you need to:

- identify and analyse the **2022 December PSP–Solar Orbiter radial conjunction**,
- compute structure-function spectral evolution and cross-helicity radial trend across a near-Lagrangian PSP→SO mapping,
- compare to the earlier first PSP–SO alignment ([[telloni-2021-psp-solo-radial-alignment-turbulence]]) for cross-event consistency.

Skip this skill if your interest is statistical multi-spacecraft compressibility ([[cuesta-2022-compressible-turbulence-psp-themis-maven]]) or a non-conjunction radial-evolution survey ([[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]).

## Paper identity and claim boundary

- **Citation**: Silwal, A., Zhao, L., Zhu, X., Sorriso-Valvo, L., Hadid, L. Z., Zank, G. P., et al. (2025). *Evolution of Solar Wind Turbulence during Radial Alignment of Parker Solar Probe and Solar Orbiter in 2022 December.* **ApJS 278** (2025). Full author tail beyond first 6 TODO_verify.
- **DOI**: [10.3847/1538-4365/add011](https://doi.org/10.3847/1538-4365/add011)
- **arXiv**: not located on 2026-05-19 (TODO_verify whether a preprint exists).
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.12 (inventory attributes lead authorship to Telloni — see attribution note above).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via IOPscience DOI page):**

- The paper investigates radial evolution of solar wind turbulence during a PSP–SO radial alignment **on 2022 December 10**, with **PSP at ≈0.11 au and SO at ≈0.88 au** (abstract-verified absolute positions).
- The mapping method is a **ballistic propagation model with time-constant acceleration constrained by in situ solar wind velocity at PSP and SO** (abstract-verified — this is more specific than a constant-V_sw ballistic mapping; the constant-acceleration variant accommodates a non-trivial expansion profile).

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- Per-window inertial-range slopes, σ_c radial trend direction and magnitude, and Δσ_c across the conjunction are **TODO_verify** against §3 / figures of ApJS 278.
- The conjunction window's exact start/end times beyond the central 2022-12-10 anchor are TODO_verify.
- Whether the abstract's "approximately the same plasma parcel" framing relies on the constant-acceleration mapping or also on co-rotation timing checks is TODO_verify.

Out-of-scope (the entry deliberately refuses these): collapsing this single-event result into a general statistical statement about all PSP–SO conjunctions, ignoring co-rotation timing uncertainties, or generalising the cross-helicity sign across stream classes that the alignment did not actually sample.

> **Assumptions and failure modes** (load-bearing): a single radial conjunction provides one Lagrangian sample — population claims require many events; the constant-acceleration mapping is not equivalent to a constant-V_sw mapping and the choice affects which PSP samples pair with which SO samples; RTN-frame +R / +N orientation conventions differ between SOAR / SOC delivered products and must be harmonised before pairing increments.

## Scientific claim to reproduce or operationalize

A radial PSP–SO conjunction in 2022 December provides a near-Lagrangian path along which the same approximate plasma parcel is sampled at two heliocentric distances. Structure-function-based spectral evolution and cross-helicity radial trends across this path are reported.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN, T_p | L3 | CDAWeb / PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR / CDAWeb |
| Solar Orbiter SWA/PAS | n_p, V_RTN, T_p | L2 | SOAR / CDAWeb |

Time range: **2022-12-10** central conjunction anchor with PSP ≈ 0.11 au and SO ≈ 0.88 au (abstract-verified absolute positions); exact full window start/end **TODO_verify** against the paper's §2 selection.

## Algorithm/workflow steps

1. **Conjunction identification** — Find the time window in 2022 December where PSP and SO are within an acceptable angular separation in heliographic longitude (radial alignment).
2. **Plasma-parcel mapping** — Apply a ballistic propagation model with a **time-constant acceleration constrained by in-situ solar-wind velocity at PSP and SO** (the paper's method, abstract-verified). Pair PSP samples at time t with SO samples at the corresponding mapped time. Also report a constant-V_sw variant as a sensitivity check, since constant-V_sw and constant-acceleration mappings can differ noticeably across a ≈0.77-au baseline.
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
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS + SWEAP and Solar Orbiter MAG + SWA-PAS time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces — SOAR retrieval via WebFetch is the guaranteed fallback).
- **Caveats → skill memory**: mapping ambiguity, separation tolerance, RTN-frame convention, single-event statistical caveat.
- **Figures / results → benchmark artifacts**: matched-window CSV + PSP/SO PSD overlay.

## Layer 4 — Research-generation affordances

- **Gap:** the radial alignment is a single Lagrangian event (one date, one mapping); statistical claims about PSP→SO radial turbulence evolution cannot be drawn from this entry alone. Compose with [[telloni-2021-psp-solo-radial-alignment-turbulence]] (first PSP–SO alignment, June 2020) and [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (multi-encounter radial survey) to build an event-stratified population view.
- **Tension:** the abstract reports a *constant-acceleration* ballistic mapping; the literature standard is constant-V_sw. The two mappings can pair PSP samples with different SO samples across a 0.77-au baseline. Re-running the analysis under both mappings, on the same windows, separates "radial evolution of turbulence" from "sensitivity to the parcel-tracking model" — a result that would otherwise be ambiguous in any roll-up.
- **Hypothesis:** the difference Δσ_c = σ_c(SO) − σ_c(PSP) across this single 2022-12-10 conjunction is dominated by *expansion* (radial decoupling of forward and backward Alfvén waves) rather than by *parametric decay* or *interaction with CIR structures*. Testable by stratifying the matched windows by the local expansion factor inferred from V_sw and by HCS-distance during the SO leg.
- **Minimal_experiment:** rerun the matched-window structure functions with two angular-separation tolerances (e.g. ±2° vs ±5° heliographic longitude) and report (slope_B_PSP, slope_B_SO, σ_c_PSP, σ_c_SO) per tolerance; if the trend is tolerance-invariant the alignment is the dominant driver, if not, the "radial evolution" signal is partly a window-selection effect.
- **Composable experiment:** join the matched-window table with [[bandyopadhyay-2020-energy-transfer-psp]] for ε(PSP-leg) and a 1-au cascade-rate reference for ε(SO-leg) — testing whether ε co-decays Lagrangianly with σ_c across this single radial path provides the first single-event test of whether cascade-rate decay tracks Alfvénicity decay (vs being radially decoupled).

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` + `solar_orbiter` bundles (radial-evolution / conjunction branch).
- **Sibling paper-skills**: [[telloni-2021-psp-solo-radial-alignment-turbulence]] (first alignment — direct methodological predecessor), [[cuesta-2022-compressible-turbulence-psp-themis-maven]] (statistical multi-spacecraft alternative), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (radial spectral steepening context), [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (anisotropy radial evolution).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `solar-orbiter-data-mcp`, `cdflib`. The ballistic-mapping step is a candidate Stage-B synthesis skill.
- **Harness contract**: exports per-window (r_PSP, r_SO, σ_c_PSP, σ_c_SO, slope_B_PSP, slope_B_SO); HelioSI roll-up consumes it as a single-event Lagrangian row complementary to [[telloni-2021-psp-solo-radial-alignment-turbulence]].

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.12 (lists this DOI under "Telloni 2025"; verified 2026-05-19 that the published lead author is A. Silwal — inventory paraphrase, not a verified attribution).
- DOI: https://doi.org/10.3847/1538-4365/add011 (resolves to IOPscience ApJS 278 (2025))
- ADS candidate bibcode: 2025ApJS..278....3S (TODO_verify bibcode against ADS listing)
- arXiv: not located on 2026-05-19 (no verified preprint link)
- Telloni et al. 2021 — methodological predecessor (paper-skill [[telloni-2021-psp-solo-radial-alignment-turbulence]]).
