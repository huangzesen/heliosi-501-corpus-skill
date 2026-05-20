---
name: carbone-2021-electron-density-turbulence-ion-cyclotron-waves
description: Use when characterising electron-density turbulence and ion-cyclotron-wave statistics in the inner heliosphere from Solar Orbiter RPW spacecraft-potential-derived density — central paper claim is that 36 intervals analysed in June 2020 show three distinct turbulence groups, with 21 exhibiting standard Kolmogorov-like inertial-range scaling and others displaying anomalous features, and that regions with enhanced ion-cyclotron wave activity correlate with reduced intermittency (Carbone et al. 2021, A&A 656, A16; DOI 10.1051/0004-6361/202140931; arXiv:2105.07790).
version: 0.1.0
tags: [solar-orbiter, rpw, electron-density, ion-cyclotron-waves, intermittency, wavelet, aanda]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "F. Carbone"
  authors:
    - "F. Carbone"
    - "L. Sorriso-Valvo"
    - "Yu. V. Khotyaintsev"
    - "K. Steinvall"
    - "A. Vecchio"
    - "D. Telloni"
    - "E. Yordanova"
    - "D. B. Graham"
    - "N. J. T. Edberg"
    - "A. I. Eriksson"
    - "E. P. G. Johansson"
    - "C. L. Vásconez"
    - "M. Maksimovic"
    - "R. Bruno"
    - "R. D'Amicis"
    - "S. D. Bale"
    - "T. Chust"
    - "V. Krasnoselskikh"
    - "M. Kretzschmar"
    - "E. Lorfèvre"
    - "D. Plettemeier"
    - "J. Souček"
    - "M. Steller"
    - "Š. Štverák"
    - "P. Trávníček"
    - "A. Vaivads"
    - "T. S. Horbury"
    - "H. O'Brien"
    - "V. Angelini"
    - "V. Evans"
  authors_verified: true
  doi: "10.1051/0004-6361/202140931"
  arxiv_id: "2105.07790"
  year: 2021
  venue: "Astronomy & Astrophysics 656, A16 (2021)"
---

# Carbone 2021 — Electron-Density Turbulence + ICWs (Solar Orbiter, June 2020)

## When to use this paper-skill

Load this skill when you need to:

- compute **electron-density turbulence spectra and intermittency** from Solar Orbiter RPW spacecraft-potential-derived n_e during early-cruise intervals (the paper's anchor is June 2020),
- statistically identify **ion-cyclotron waves** via wavelet analysis on the same intervals and correlate ICW activity with density-fluctuation intermittency,
- complement PSP-based ICW detection (cf. [[bowen-2024-extended-cyclotron-resonant-heating]]) with a Solar Orbiter density-channel measurement.

Skip this skill if your interest is magnetic-field-only turbulence ([[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]) or PSP-specific cyclotron heating ([[bowen-2024-extended-cyclotron-resonant-heating]]).

## Paper identity and claim boundary

- **Citation**: Carbone, F., Sorriso-Valvo, L., Khotyaintsev, Yu. V., Steinvall, K., Vecchio, A., Telloni, D., Yordanova, E., Graham, D. B., Edberg, N. J. T., Eriksson, A. I., et al. (2021). *Statistical Study of Electron Density Turbulence and Ion-Cyclotron Waves in the Inner Heliosphere: Solar Orbiter Observations.* **A&A 656, A16** (2021).
- **DOI**: [10.1051/0004-6361/202140931](https://doi.org/10.1051/0004-6361/202140931)
- **arXiv**: [2105.07790](https://arxiv.org/abs/2105.07790)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.14.

**Evidence boundary — what the abstract supports (verified 2026-05-19 via aanda.org DOI page for 10.1051/0004-6361/202140931):**

- The paper analyses Solar Orbiter RPW spacecraft-potential-derived electron density across **36 intervals in June 2020** (abstract-verified concrete sample size and time window).
- The analysis uses **empirical mode decomposition** to characterise the density-fluctuation statistics (abstract-verified method).
- The 36 intervals separate into **three distinct groups**, with **21 of them exhibiting standard turbulence properties consistent with Kolmogorov scaling** (abstract-verified split — 21 / 36 ≈ 58 %).
- Most intervals show **"a well-defined inertial range with power-law scaling"** in the density spectra (abstract-verified).
- The paper reports that **regions with enhanced ion-cyclotron wave activity correlate with reduced intermittency**, interpreting both as driven by Alfvénic fluctuations at different scales (abstract-verified relation between ICW activity and intermittency suppression).
- A full 30-author list is verified (Carbone first; Sorriso-Valvo, Khotyaintsev, Steinvall, Vecchio, Telloni, Yordanova, Graham, Edberg, Eriksson, Johansson, Vásconez, Maksimovic, Bruno, D'Amicis, Bale, Chust, Krasnoselskikh, Kretzschmar, Lorfèvre, Plettemeier, Souček, Steller, Štverák, Trávníček, Vaivads, Horbury, O'Brien, Angelini, Evans).
- Published as A&A **656, A16** (2021).

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact spacecraft-potential-to-density calibration version (Pedersen-class) used by the paper is **TODO_verify** against §2 of the published version.
- The quantitative density-PSD inertial-range slope (the abstract says Kolmogorov-consistent for the 21-interval subgroup but does not give a numeric exponent) is TODO_verify.
- The quantitative ICW-occurrence rate (events / hour) at ~0.5 au and the threshold used to define "enhanced ICW activity" are TODO_verify.
- The identity of the third group beyond "21 standard + anomalous" (i.e. whether the abstract's three groups are 21 + 7 + 8 or some other split) is TODO_verify.

Out-of-scope (the entry deliberately refuses these): extending the result to PSP-distance regimes without independent analysis; collapsing the ICW–intermittency correlation across all SO encounters when the paper's sample is explicitly June 2020 only; treating "Kolmogorov-consistent" as a precise -5/3 exponent (the abstract uses qualitative wording).

> **Assumptions and failure modes** (load-bearing): the V_sc → n_e calibration is mission-, panel-, and bias-dependent — use a version-pinned RPW calibration; the empirical-mode-decomposition step is sensitive to mode-mixing artefacts and to the chosen number of intrinsic mode functions; ICW detection at the start / end of intervals suffers cone-of-influence edge effects; the 36-interval sample is small for population claims so per-interval uncertainties should be reported.

## Scientific claim to reproduce or operationalize

Electron-density fluctuations measured by Solar Orbiter RPW (via the spacecraft potential) during June 2020 exhibit a well-defined inertial range with power-law scaling in most of the 36 analysed intervals; 21 of them (~58 %) are consistent with standard (Kolmogorov-like) turbulence properties, while others show anomalous features. Concurrent wavelet analysis on MAG data statistically identifies ion-cyclotron-wave activity, and intervals with enhanced ICW activity correlate with reduced density intermittency — consistent with Alfvénic fluctuations driving both phenomena at different scales.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| SO RPW (Radio and Plasma Waves) | spacecraft potential V_sc → n_e | L2/L3 | SOAR / CDAWeb |
| SO MAG | B_RTN | L2 | SOAR / CDAWeb |
| SO SWA/PAS | n_p, V_RTN, T_p (cross-check) | L2 | SOAR |

Time range: **June 2020** Solar Orbiter cruise-phase intervals — 36 intervals analysed (abstract-verified sample); precise per-interval timestamps and heliocentric distances **TODO_verify** against §2 of A&A 656, A16.

## Algorithm/workflow steps

1. **Interval selection** — Identify 36 clean June 2020 SO intervals with simultaneous RPW, MAG, and SWA-PAS coverage (matching the paper's selection rule — TODO_verify rule).
2. **n_e from V_sc** — Convert RPW spacecraft potential to electron density via a version-pinned empirical calibration (TODO_verify exact calibration version used by the paper).
3. **Density PSD via EMD** — Apply empirical mode decomposition to n_e; characterise the inertial-range slope per interval.
4. **Intermittency on n_e** — Compute scale-dependent kurtosis (or PDF tails) on n_e or on its EMD modes.
5. **Wavelet analysis on B** — Wavelet transform B_RTN; compute reduced magnetic helicity σ_m(f, t).
6. **ICW detection** — Identify wavelet events with LH-circular polarisation near the proton-cyclotron frequency band; build an event catalog per interval.
7. **Group classification** — Cluster the 36 intervals into the paper's three groups based on density-PSD shape + intermittency + ICW presence (TODO_verify clustering rule).
8. **Joint statistics** — Aggregate; verify that 21 / 36 intervals are Kolmogorov-consistent (abstract-verified target) and that enhanced-ICW intervals have reduced intermittency.
9. **Acceptance** — Recover the abstract-verified split (21 / 36 standard) and the qualitative ICW-vs-intermittency anti-correlation; exact slopes and ICW rates TODO_verify.

## Minimal executable benchmark or validation target

**Target**: across 36 SO June 2020 intervals, RPW-derived n_e shows a well-defined inertial-range power law in most intervals; 21 of them are Kolmogorov-like (abstract-verified count); intervals with enhanced ICW activity show reduced density-intermittency (abstract-verified anti-correlation). Exact PSD slopes and ICW occurrence rates TODO_verify against A&A 656, A16 figures.

Recommended check artifacts:

- `carbone2021_ne_icw.csv` — one row per interval: (t_start, t_end, r_au, slope_n_e_PSD, kurtosis_exponent, ICW_count, ICW_rate, group_label).
- Wavelet σ_m(f, t) panel with ICW events marked.
- Single scalar QC: fraction of intervals in the Kolmogorov-consistent group (target: ≈ 21 / 36).
- Two-panel QC: ICW_rate vs kurtosis_exponent scatter (target: monotonic negative correlation).

## Known pitfalls / failure modes

- **V_sc → n_e calibration**: the spacecraft-potential-to-density calibration is mission-, panel-, and bias-dependent; use the published SO RPW calibration and document its version.
- **EMD mode-mixing**: empirical mode decomposition is sensitive to noise and to the number of intrinsic mode functions extracted; report the cutoff and avoid over-decomposing.
- **Calibration outliers**: low spacecraft-potential intervals (e.g. shadow, photoemission shifts) yield biased n_e — flag and exclude.
- **Wavelet boundary effects**: ICW detection at the start / end of intervals suffers cone-of-influence edge effects; mask boundaries.
- **MAG cadence vs proton cyclotron frequency**: ensure MAG cadence resolves f_cp at ~0.5 au (~few Hz) — survey-mode may be insufficient.
- **Doppler shift**: spacecraft-frame frequencies are Doppler-shifted (cf. [[bowen-2024-extended-cyclotron-resonant-heating]]).
- **Sample size N = 36**: statistical claims have small N — quote per-interval uncertainties and avoid asymptotic-statistics phrasing.
- **"Kolmogorov-consistent" vs exact −5/3**: the abstract uses qualitative wording; do not silently widen to "α_n = −5/3 exactly" without verifying figures.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "21 / 36 SO June 2020 intervals are Kolmogorov-consistent in n_e PSD; ICW activity correlates with reduced intermittency" becomes the per-interval CSV + the Kolmogorov-group fraction scalar + the ICW-vs-kurtosis scatter.
- **Methods / equations → executable workflows**: V_sc → n_e calibration + EMD + PSD + intermittency + wavelet ICW detection are steps 2–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve Solar Orbiter RPW, MAG, and SWA-PAS time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces).
- **Caveats → skill memory**: V_sc calibration version dependency, EMD mode-mixing, wavelet edge effects, Doppler shift, cadence requirement, small-N caveat.
- **Figures / results → benchmark artifacts**: wavelet σ_m panel + per-interval CSV + ICW-vs-kurtosis scatter.

## Layer 4 — Research-generation affordances

- **Gap:** the paper's sample is 36 intervals in a single month (June 2020). A composable experiment that repeats the same V_sc → n_e + EMD + wavelet pipeline on a *later* SO cruise window (e.g. 2022 mid-cruise) would test whether the "21 / 36 Kolmogorov + ICW–intermittency anti-correlation" finding is *time-stable* or *epoch-dependent* — neither paper alone constrains this.
- **Tension:** the abstract attributes both the inertial-range scaling and the ICW-driven intermittency suppression to Alfvénic fluctuations at different scales; [[damicis-2021-alfvenic-nonalfvenic-psp]] reports that Alfvénicity in the inner heliosphere is *bimodal* across stream classes. If the 36 June 2020 intervals are themselves bimodal in Alfvénicity, the "21 Kolmogorov + others anomalous" split may simply be the Alfvénicity classification in disguise. Testable by stratifying the per-interval group labels by σ_c.
- **Hypothesis:** the kurtosis_exponent and ICW_rate are *not* anti-correlated within the Kolmogorov-group subset alone, but across all 36 intervals because of an underlying confound (e.g. Alfvénicity or local β). Testable by reporting the partial correlation kurtosis–ICW | σ_c stratification.
- **Minimal_experiment:** rerun the V_sc → n_e calibration with two RPW calibration versions (the published one + the most recent ROC version) and report whether the 21 / 36 Kolmogorov-group count is robust — quantifies the calibration-version sensitivity that the abstract does not bound.
- **Composable experiment:** join the per-interval (slope_n_e, ICW_rate) table with [[bowen-2024-extended-cyclotron-resonant-heating]] (Bowen, Vasko, Bale et al. 2024) PSP-side ICW catalogs and [[cuesta-2022-compressible-turbulence-psp-themis-maven]] compressibility statistics on matched heliocentric distance bins; cross-instrument agreement (PSP MAG-derived vs SO RPW-derived ICW rates) would be the first multi-mission ICW-occurrence reference at ~0.5 au.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar_orbiter` + `waves_instabilities` bundles (ICW + density-turbulence branch).
- **Sibling paper-skills**: [[bowen-2024-extended-cyclotron-resonant-heating]] (PSP-side ICW detection — independent instrument, lead-author + arXiv anchor verified), [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (cyclotron-resonance mediation argument), [[cuesta-2022-compressible-turbulence-psp-themis-maven]] (density-fluctuation multi-spacecraft context), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (magnetic spectral context at similar distance; Sioulas lead-author dispute documented in that entry).
- **MCPs (proposed contracts)**: `solar-orbiter-data-mcp`, `cdflib`, optional `wavelet-polarisation-mcp` synthesis candidate.
- **Harness contract**: exports {slope_n_e, kurtosis_exponent, ICW_rate, group_label} per interval at ~0.5 au; HelioSI roll-up consumes it as the SO density-channel ICW row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.14.
- Publisher: A&A 656, A16 (2021) — DOI [10.1051/0004-6361/202140931](https://doi.org/10.1051/0004-6361/202140931) (verified 2026-05-19, full 30-author list confirmed).
- arXiv: [2105.07790](https://arxiv.org/abs/2105.07790)
- ADS bibcode: TODO_verify (`2021A&A...656A..16C` is the natural guess but not directly verified on 2026-05-19).
- Pedersen et al. — RPW V_sc → n_e calibration (foundational, not from inventory).
