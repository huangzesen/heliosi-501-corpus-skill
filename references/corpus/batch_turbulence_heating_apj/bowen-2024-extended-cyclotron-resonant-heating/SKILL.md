---
name: bowen-2024-extended-cyclotron-resonant-heating
description: Use when diagnosing ion-cyclotron resonant heating at the magnetic-spectral break in PSP fast streams — central paper claim is that transition-range steepening at ion scales over ≈15–55 R☉ is associated with significant left-hand circularly polarised ion-cyclotron-scale waves whose quasilinear cyclotron-resonant heating rate is a significant fraction of the turbulent cascade rate (Bowen, Vasko, Bale et al. 2024, arXiv:2406.10446; venue TODO_verify ApJ).
version: 0.1.0
tags: [psp, fast-wind, ion-cyclotron-waves, cyclotron-resonance, heating, spectral-break, fields, polarisation]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "T. A. Bowen"
  authors:
    - "T. A. Bowen"
    - "I. Y. Vasko"
    - "S. D. Bale"
    - "B. D. G. Chandran"
    - "A. Chasapis"
    - "T. Dudok de Wit"
    - "A. Mallet"
    - "M. McManus"
    - "R. Meyrand"
    - "M. Pulupa"
    - "J. Squire"
  authors_verified: true
  doi: null
  arxiv_id: "2406.10446"
  year: 2024
  venue: "arXiv:2406.10446 (TODO_verify ApJ journal-ref)"
---

# Bowen 2024 — Extended Cyclotron-Resonant Heating (PSP Fast Wind)

## When to use this paper-skill

Load this skill when you need to:

- identify **left-hand circularly polarised ion-cyclotron waves (ICWs)** at the magnetic-spectral break / transition range in PSP FIELDS data,
- estimate the cyclotron-resonant heating rate associated with those waves in PSP intervals between ~15–55 R☉,
- argue for an **extended** cyclotron-heating channel (i.e. extending over a wide near-Sun radial range), as opposed to a single-distance result.

Skip this skill if you need the more theoretical mediation argument (use [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]) or Landau-channel partitioning (use [[bowen-2023-landau-damping-proton-electron-heating]]).

## Paper identity and claim boundary

- **Citation**: Bowen, T. A., Vasko, I. Y., Bale, S. D., Chandran, B. D. G., Chasapis, A., Dudok de Wit, T., Mallet, A., McManus, M., Meyrand, R., Pulupa, M., Squire, J. (2024). *Extended Cyclotron Resonant Heating of the Turbulent Solar Wind.* arXiv:2406.10446 — **venue (ApJ) and journal DOI TODO_verify**.
- **DOI**: not located on 2026-05-19 (TODO_verify against ADS / IOPscience once a journal version is registered).
- **arXiv**: [2406.10446](https://arxiv.org/abs/2406.10446)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.8.

**Evidence boundary — what the arXiv abstract supports (verified 2026-05-19 via arXiv.org metadata page for 2406.10446):**

- The paper analyses Parker Solar Probe data over the heliocentric distance range **≈15–55 R☉** (abstract-verified).
- The principal observational claim is that **"transition-range steepening at ion-scales is associated with the presence of significant left-handed ion-kinetic scale waves"** (abstract-verified phrasing).
- The heating-rate estimate is built using **quasilinear theory and empirical velocity distributions**, and the resulting Q is compared to the **turbulent energy cascade rate**, with the abstract concluding that cyclotron heating is "a significant dissipation mechanism in solar wind dynamics" (abstract-verified).
- The full author tail is verified on the arXiv landing page: Bowen, Vasko, Bale, Chandran, Chasapis, Dudok de Wit, Mallet, McManus, Meyrand, Pulupa, Squire.

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact spectral-break frequency definition, the per-encounter list, the per-interval Q_p,ICW magnitude, and the ratio Q_p,ICW / ε (cascade rate) are **TODO_verify** against the figures / Methods of the full text.
- The cyclotron resonance condition formula used (with vs. without Doppler shift) is TODO_verify.
- Whether the paper restricts conditioning to "fast wind" or to all Alfvénic intervals across 15–55 R☉ is TODO_verify; the abstract refers to "the turbulent solar wind" without an explicit fast-wind threshold.

Out-of-scope (the entry deliberately refuses these): extending the claim to slow non-Alfvénic wind, to 1 au, or to electron heating; conflating with stochastic-heating diagnostics ([[chandran-2010-stochastic-heating-perp-alfven]] in upstream literature) without explicit cross-paper analysis; treating this paper as identical to [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] — they share authors and physics class but are distinct submissions (the Nat. Astron. paper is the mediation/mechanism argument; this preprint is the radially extended observational identification).

> **Assumptions and failure modes** (load-bearing): polarisation handedness sign depends on the +B₀ reference convention; spacecraft-frame frequencies are Doppler-shifted relative to the plasma frame so ICW identification requires either an inertial-frame correction or an explicit argument that the shift is small; quasilinear heating-rate formulas assume small-amplitude (δB/B₀ ≪ 1) waves at the band of interest, which should be verified per interval.

## Scientific claim to reproduce or operationalize

A persistent feature near the magnetic-spectral / transition-range break in PSP data over 15–55 R☉ is a left-handed circularly polarised wave population identified with ion-cyclotron / ion-kinetic-scale waves. Their amplitude, combined with the proton velocity distribution and the cyclotron resonance condition, implies a quasilinear cyclotron-resonant heating rate Q_p,ICW that is a *significant* fraction of the turbulent cascade rate ε; the channel is active across a wide radial range rather than being localised to a single perihelion.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, full-vector PSD at ion-scale frequencies | L2, ≥1 vec/s, Burst-mode preferred | CDAWeb / PSP SOC |
| PSP FIELDS DFB AC | high-cadence B for ICW resolution (optional) | L2 | PSP SOC |
| PSP SWEAP/SPC, SPAN-I | n_p, V_RTN, T_p, T_p⊥ / T_p∥ | L3 | CDAWeb / PSP SOC |

Time range: PSP intervals spanning ~15–55 R☉ — multi-encounter coverage. Whether the paper restricts to high-Alfvénicity ("fast-wind") intervals is TODO_verify.

## Algorithm/workflow steps

1. **Interval selection** — Identify intervals between ~15 and 55 R☉ across PSP encounters. If the full text imposes an Alfvénicity / σ_c threshold, mirror it; otherwise document the choice.
2. **Spectral / transition-range break** — Determine the magnetic-spectral break (or transition-range knee) frequency f_b per interval from the trace PSD; use it as the central frequency for ICW search.
3. **Polarisation analysis** — Compute magnetic helicity / signed normalised reduced helicity σ_m(f, t) (e.g. via wavelet or short-time FFT in mean-field-aligned coordinates); identify left-hand circularly polarised peaks near f_b. Document the +B₀ convention.
4. **ICW band integration** — Define a band around f_b and integrate the LH-polarised power δB_ICW².
5. **Resonance condition** — Estimate the resonant velocity v_res from ω − k_∥ v_res = ±Ω_p (cyclotron condition) using local plasma parameters. Apply Doppler-shift correction if spacecraft-frame frequencies are used.
6. **Heating-rate estimate** — Convert δB_ICW² + resonance overlap with the empirical proton velocity distribution to a quasilinear heating rate Q_p,ICW per interval (exact closed-form expression is TODO_verify against the paper's Methods).
7. **Cascade-rate normalisation** — Compute the turbulent energy cascade rate ε (e.g. via [[bandyopadhyay-2020-energy-transfer-psp]] or a structure-function-based estimator) for the same intervals; report Q_p,ICW / ε.
8. **Radial aggregation** — Bin Q_p,ICW (and Q_p,ICW / ε) vs heliocentric distance over 15–55 R☉; show channel persistence.
9. **Acceptance** — LH ICW peak near the break is detected over the majority of qualifying intervals across the radial range, with Q_p,ICW a *significant* fraction (not necessarily dominant) of ε (paper's abstract-verified claim).

## Minimal executable benchmark or validation target

**Target**: LH-circular-polarised ICW band identified near the spectral break across PSP intervals between ~15–55 R☉, with Q_p,ICW estimated by quasilinear theory + empirical f_p(v_∥) being a significant fraction of the turbulent cascade rate ε (abstract-verified qualitative target; quantitative per-bin magnitudes TODO_verify against Bowen+ 2024 figures).

Recommended check artifacts:

- `bowen2024_extended_cyclotron.csv` — one row per interval: (t_start, t_end, r_au, f_b, δB_ICW², Q_p,ICW, ε, ratio_Q_over_eps, σ_c, σ_m_band).
- σ_m(f, t) spectrogram per representative interval.
- Single scalar QC: fraction of qualifying intervals with detectable LH-polarised peak at f_b, and median Q_p,ICW / ε across the radial range.

## Known pitfalls / failure modes

- **Polarisation sign / handedness convention**: the LH/RH convention depends on the chosen reference frame (plasma vs spacecraft, +B₀ direction) — be explicit; an inverted sign trivially reverses the conclusion.
- **Doppler shift**: spacecraft-frame frequencies are Doppler-shifted; ICW identification requires either an inertial-frame correction or a careful argument that the shift is small at the band of interest.
- **Spin-tone leakage**: residual MAG spin lines can mimic narrow-band power near the break — exclude or notch.
- **Cadence**: low survey-mode cadence aliases the near-break power; Burst-mode is preferred.
- **Quasilinear assumption**: Q_p,ICW formula assumes small-amplitude waves — verify δB/B₀ at the band.
- **"Significant fraction" vs "dominant"**: do not silently widen the abstract's "significant dissipation mechanism" wording to "the dominant heating channel" — the paper's claim is consistent with cyclotron co-existing with Landau / KAW dissipation.
- **Stream-class ambiguity**: the abstract refers to "the turbulent solar wind" without an explicit fast/slow conditioning; if you condition on fast wind to reproduce a figure, log that choice as a deviation from the abstract scope.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "extended ICW-mediated cyclotron heating channel in PSP over 15–55 R☉" becomes the per-interval CSV + the radial Q_p,ICW(r) and Q_p,ICW / ε curves.
- **Methods / equations → executable workflows**: spectral-break detection + magnetic helicity / polarisation analysis + cyclotron resonance condition + quasilinear heating estimate are steps 2–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 (+ optional DFB AC) and SWEAP plasma-moment time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings).
- **Caveats → skill memory**: handedness convention, Doppler-shift caveat, spin-tone leakage, the "significant" wording boundary.
- **Figures / results → benchmark artifacts**: σ_m(f, t) spectrogram + radial Q_p,ICW(r) and Q_p,ICW / ε curves.

## Layer 4 — Research-generation affordances

- **Gap:** Q_p,ICW is computed quasilinearly from δB_ICW² and an empirical f_p(v_∥); the paper does not (per abstract) report whether Q_p,ICW > Q_p,Landau on the same intervals. A composable experiment that runs both this protocol and [[bowen-2023-landau-damping-proton-electron-heating]] (Shankarappa et al. 2023) on the same PSP E1–E2 + E4–E14 Burst-mode intervals would deliver the first per-interval channel-budget table for proton heating in the inner heliosphere.
- **Tension:** the radial extent (15–55 R☉) covers regions where [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (Sioulas et al. 2023; see slug-attribution note) reports inertial-range slope steepening from ≈-3/2 to ≈-5/3. If the LH-ICW peak at the transition range persists across this slope-evolution range without a corresponding shift in f_b/Ω_p, the cyclotron channel is *insensitive* to the inertial-range scaling — a non-trivial empirical constraint on cascade-into-dissipation models.
- **Hypothesis:** in PSP intervals where δB/B₀ at the spectral break exceeds ~0.1, the quasilinear Q_p,ICW estimate **overestimates** the true cyclotron heating rate (because the small-amplitude assumption is violated); testable by stratifying the per-interval Q_p,ICW table by δB/B₀ and looking for a flattening / saturation in Q_p,ICW(δB/B₀) above this threshold.
- **Minimal_experiment:** on three PSP encounters spanning the 15–55 R☉ range (e.g. E4 perihelion, E7 mid-encounter, E10 outbound), measure (f_b, δB_ICW², σ_m_band, σ_c) per 1-h window and report whether the LH ICW peak is detectable in ≥80% of qualifying windows per encounter; this tests the "extended" (not localised) claim independently of the quasilinear Q_p,ICW magnitude.
- **Composable experiment:** join the per-interval Q_p,ICW + Q_p,Landau + ε table with [[damicis-2021-alfvenic-nonalfvenic-psp]] Alfvénicity classes to ask whether the cyclotron channel's significance is conditioned on Alfvénic streams or persists across the slow-Alfvénic / non-Alfvénic boundary — a test the present paper's abstract does not constrain.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `waves_instabilities` + `coronal_heating` bundles (ion-scale wave-heating branch).
- **Sibling paper-skills**: [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (companion mechanism paper — same authors, Nat. Astron., distinct DOI), [[bowen-2023-landau-damping-proton-electron-heating]] (Landau channel — alternative dissipation pathway; lead-author attribution dispute documented in that entry), [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] (ICW identification on Solar Orbiter density data — same wave class, different instrument), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (spectral-break radial evolution context; lead-author dispute documented there).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `cdflib`, an optional `wavelet-polarisation-mcp` (the wavelet helicity estimator is a candidate synthesis-skill).
- **Harness contract**: exports {f_b, δB_ICW², Q_p,ICW, ε, ratio_Q_over_eps} per (interval, r); HelioSI roll-up consumes it as the cyclotron-channel row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.8.
- arXiv: [2406.10446](https://arxiv.org/abs/2406.10446) (verified 2026-05-19 — full 11-author list, abstract wording confirmed).
- Journal version (ApJ) DOI: TODO_verify.
- ADS bibcode: TODO_verify (no resolved bibcode on 2026-05-19).
- Marsch (2006) — solar-wind cyclotron-heating review (foundational, not from inventory).
