---
name: bowen-2023-landau-damping-proton-electron-heating
description: Use when partitioning solar-wind turbulent dissipation between protons and electrons via a Howes-class quasilinear Landau-damping cascade model constrained by measured PSP magnetic spectra — central paper claim is that the cascade model accurately describes the observed energy spectrum in ≥39.4 % of PSP E1–E2 intervals and predicts Q_p / Q_e ratios that depend strongly on plasma beta and are consistent with empirical heating estimates (Shankarappa, Klein, & Martinović 2023, ApJ 946; DOI 10.3847/1538-4357/acb542; arXiv 2301.09713). Slug retained for backwards compatibility — the published lead author is Shankarappa, not Bowen (verified 2026-05-19).
version: 0.1.0
tags: [psp, turbulence, heating, landau-damping, vlasov, proton-electron-partition, fields]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "N. Shankarappa"
  authors:
    - "N. Shankarappa"
    - "K. G. Klein"
    - "M. M. Martinović"
  authors_verified: true
  doi: "10.3847/1538-4357/acb542"
  arxiv_id: "2301.09713"
  year: 2023
  venue: "The Astrophysical Journal 946 (2023)"
---

# Shankarappa 2023 — Landau-Damping Proton/Electron Heating Partition (PSP) (slug: bowen-2023-…)

> **Attribution note (verified 2026-05-19).** The published version of this paper at DOI 10.3847/1538-4357/acb542 (ApJ 946, 2023) lists **N. Shankarappa, K. G. Klein, M. M. Martinović** as authors — T. A. Bowen is *not* an author. The inventory `apj_aa_heliophysics_papers.md §1.6` paraphrases this paper with a "Bowen et al." attribution that does not match the published record. The corpus slug `bowen-2023-…` is retained for backwards compatibility but the cited lead author is now **N. Shankarappa**; use Shankarappa, Klein, & Martinović 2023, ApJ 946 when citing this entry in a manuscript. (Mirrors the slug-retention pattern previously applied to `telloni-2025-psp-solo-radial-alignment-2022-december`.)

## When to use this paper-skill

Load this skill when you need to:

- estimate the **proton vs electron heating-rate partition** from a measured turbulence spectrum using a Howes-class quasilinear Landau-damping cascade model,
- combine a linear Vlasov dispersion solver (returning γ(k) for damped modes) with a forward-cascade transport equation constrained by PSP FIELDS spectra,
- compare model-predicted Q_p / Q_e ratios to PSP-derived empirical heating rates during the first two perihelia (E1, E2).

Skip this skill if your task is cyclotron-resonant ion heating (use [[bowen-2024-extended-cyclotron-resonant-heating]] / [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]), coherent-structure heating ([[pecora-2022-coherent-structures-proton-electron-heating]]), or reflection-driven AW heating ([[martinovic-2024-slow-wind-imbalanced-alfven-wave-heating]]).

## Paper identity and claim boundary

- **Citation**: Shankarappa, N., Klein, K. G., & Martinović, M. M. (2023). *Estimation of Turbulent Proton and Electron Heating Rates via Landau Damping Constrained by Parker Solar Probe Observations.* **ApJ 946** (2023).
- **DOI**: [10.3847/1538-4357/acb542](https://doi.org/10.3847/1538-4357/acb542)
- **arXiv**: [2301.09713](https://arxiv.org/abs/2301.09713)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.6 (lists the paper under "Bowen et al." — see attribution note above).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via IOPscience for DOI 10.3847/1538-4357/acb542 and arXiv.org for 2301.09713):**

- The paper applies the **Howes cascade model** to PSP magnetic-field and plasma data **from the first two PSP encounters (E1, E2)** (abstract-verified).
- The model is reported to "accurately describe the observed energy spectrum from **over 39.4 % of the intervals**" (abstract-verified numeric).
- The Q_p / Q_e ratio is reported to exhibit **strong dependencies on thermal-to-magnetic pressure** (β), with Landau damping appearing more viable at higher β (abstract-verified).
- The model heating rates are described as "consistent with critical balance assumptions in turbulent cascades" and to align with "independent empirical estimates from complementary techniques" (abstract-verified).

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact linear Vlasov dispersion solver used (PLUME / NHDS / LEOPARD / other) is **TODO_verify** against §2 of the published paper.
- The propagation-angle distribution assumed for γ(k, θ_kB) and how the residual ~60 % of intervals are characterised (Landau-channel inapplicability, data-quality cuts, or other model failure modes) are TODO_verify.
- The per-interval β_p, β_e binning of (Q_p_model, Q_e_model) and the exact tolerance against the empirical comparison are TODO_verify.

Out-of-scope (the entry deliberately refuses these): extending the partition to solar-minimum 1-au streams, to non-Landau (e.g. cyclotron) channels — explicitly the domain of sibling Bowen 2024 skills — or to electron temperature anisotropy; claiming Landau damping is the unique dissipation channel on the 39 % of "well-fit" intervals (the abstract reports model adequacy, not channel exclusivity).

> **Assumptions and failure modes** (load-bearing): the linear Vlasov solver assumes small-amplitude, locally homogeneous plasma — the cascade itself is nonlinear and amplitudes near the break can violate this; γ(k) depends exponentially on β so plasma-moment uncertainties propagate strongly; SPAN-e electron moments can be biased by photoelectron contamination in some intervals; empirical Q_p, Q_e from radial T-gradients require a clean per-interval Lagrangian mapping.

## Scientific claim to reproduce or operationalize

Turbulent cascade energy reaching kinetic scales is dissipated via Landau-resonant damping of compressible / kinetic-Alfvén branches; the wavevector-dependent damping rate γ(k) computed from a linear Vlasov solver on the locally measured plasma parameters, combined with the measured magnetic-spectrum amplitude, allows the cascade flux to be split into Q_p (proton heating) and Q_e (electron heating) channels. The paper's verifiable claim is that the resulting Howes-class cascade model accurately describes the observed energy spectrum in ≥39.4 % of PSP E1–E2 intervals, with the partition Q_p / Q_e exhibiting strong β dependence consistent with critical balance and with independent empirical estimates.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, trace PSD | L2, ~1 vec/s and Burst-mode | CDAWeb / PSP SOC |
| PSP SWEAP/SPC, SPAN-I, SPAN-e | n_p, V_RTN, T_p, T_e, β_p, β_e | L3 | CDAWeb / PSP SOC |
| Linear Vlasov solver | γ(k), real-frequency ω(k) per mode | external code (e.g. PLUME, NHDS, LEOPARD — exact choice TODO_verify) | TODO_verify which solver the paper uses |

Time range: PSP Encounters 1 and 2 (perihelia 2018-11 and 2019-04, ~0.17 au) — abstract-verified. Restrict to intervals with simultaneously valid n_p, T_p, T_e and clean MAG PSDs.

## Algorithm/workflow steps

1. **Interval selection** — Quasi-stationary PSP E1 / E2 intervals with valid SPC / SPAN-e moments.
2. **Plasma parameters** — Extract n, T_p, T_e, β_p, β_e, V_A per interval.
3. **Measured magnetic PSD** — Compute the trace magnetic PSD on FIELDS data, with the inertial → kinetic transition (ion break) resolved.
4. **Linear Vlasov spectrum** — Run a linear Vlasov solver (PLUME-class) over the relevant k range and propagation angles θ_kB; extract γ(k, θ) for the relevant damped branches (KAW + ion-acoustic / slow-mode).
5. **Howes cascade transport** — Apply the Howes-class quasilinear cascade equation: ∂ε(k)/∂t + ∇_k · F(k) = −2 γ(k) ε(k); solve for the dissipation profile per branch.
6. **Spectral-fit gating** — Accept only intervals where the Howes-model spectrum reproduces the observed PSD shape within the paper's tolerance (the abstract reports this fraction is ≥39.4 %).
7. **Partition** — Integrate γ_e(k) ε(k) over k → Q_e; integrate γ_p(k) ε(k) → Q_p (per-branch contribution attributed to species by the linear damping coefficient).
8. **Empirical comparison** — Compute empirical Q_p, Q_e from radial temperature gradients and PSP velocity profiles; compare to model partition and to the β dependence reported in the abstract.
9. **Acceptance** — Fraction of accepted intervals ≥39.4 % (abstract-verified); model Q_p / Q_e exhibits strong β dependence; consistency with independent empirical estimates is qualitative (TODO_verify quantitative tolerance from the paper).

## Minimal executable benchmark or validation target

**Target**: on PSP E1 + E2 windows passing data-quality cuts, the Howes-class quasilinear Landau-damping model is shown to accurately describe the observed kinetic-range spectrum in ≥39.4 % of intervals (abstract-verified), and the resulting Q_p / Q_e exhibits strong β dependence consistent with independent empirical estimates (qualitative target; exact numerical Q_p / Q_e values TODO_verify against ApJ 946 figures).

Recommended check artifacts:

- `shankarappa2023_landau_heating.csv` — one row per interval: (t_start, t_end, r_au, β_p, β_e, model_fit_ok, Q_p_model, Q_e_model, Q_p_empirical, Q_e_empirical, ratio_model, ratio_empirical).
- Linear-Vlasov γ(k) spectrum panel per representative interval.
- Single scalar QC: fraction of intervals with model_fit_ok = True (target: ≥0.394).

## Known pitfalls / failure modes

- **Linear-theory limit**: the Vlasov solver assumes small-amplitude, locally homogeneous plasma; the cascade itself is nonlinear and amplitudes near the break can violate this — quote δB/B explicitly.
- **Propagation-angle assumption**: γ(k) depends strongly on θ_kB; assuming a single dominant angle (e.g. perpendicular KAW) over-/underestimates Q_e.
- **β sensitivity**: damping rates are exponentially sensitive to β_p, β_e — moment uncertainties propagate strongly. The β-dependence is also part of the paper's headline result, so β estimation must be defended.
- **Empirical Q_p estimation**: radial temperature gradients require a clean per-interval Lagrangian mapping; mis-mapping inflates the empirical Q_p and breaks the comparison.
- **SPAN-e electron moments**: T_e from PSP can be biased by photoelectron contamination in some intervals; flag and exclude.
- **Cascade-rate normalisation**: the cascade flux must be calibrated to the inertial-range ε (e.g. PP / vK) before the partition; use [[bandyopadhyay-2020-energy-transfer-psp]] as the upstream input.
- **39.4 % vs 100 %**: do not silently widen the abstract's "≥39.4 % of intervals" to "the model works in PSP E1–E2"; the model's domain of validity is the qualifying subset, and the failure mode in the remaining ~60 % is not characterised in the abstract.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "Howes cascade model fits ≥39.4 % of PSP E1–E2 intervals; Q_p / Q_e depends strongly on β" becomes the per-interval CSV + the model_fit_ok fraction scalar + a (Q_p / Q_e) vs β scatter.
- **Methods / equations → executable workflows**: linear-Vlasov γ(k) + Howes cascade transport + integration over k → Q_p, Q_e are workflow steps 4–7.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP SPC / SPAN-I / SPAN-e L3 time series at the required cadence, plus a linear-Vlasov dispersion-solver capability (PLUME / NHDS / LEOPARD-class); runtimes bind concrete adapters (see Layer 3 for example bindings — the Vlasov-solver surface in particular is a proposed interface, not an existing runtime adapter).
- **Caveats → skill memory**: β sensitivity, angle assumption, SPAN-e photoelectron bias, cascade-rate normalisation requirement, and the 39.4 % domain-of-validity wording.
- **Figures / results → benchmark artifacts**: per-interval Q_p / Q_e CSV + γ(k) panel + (Q_p / Q_e) vs β scatter form the exported reproducibility set.

## Layer 4 — Research-generation affordances

- **Gap:** the abstract reports the model is accurate on ≥39.4 % of intervals but does not characterise the failure mode of the remaining ~60 %. A natural composable experiment: take the per-interval (model_fit_ok = False) windows, run the polarisation analysis from [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] and the ICW-band identification from [[bowen-2024-extended-cyclotron-resonant-heating]], and ask whether the "Landau model fails" subset coincides with the "LH-circular ICW peak present" subset — directly testing whether the two heating channels are *complementary* (each covers what the other does not) or *overlapping* (some intervals support both).
- **Tension:** the β-dependence of Q_p / Q_e reported here predicts that Landau damping should be strongest in high-β intervals; the cyclotron channel is expected to be most efficient in low-β / strongly Alfvénic streams. If the PSP E1–E2 β distribution is bimodal (fast vs slow streams), the partition should track the bimodality — testable by joint stratification on β and Alfvénicity using [[damicis-2021-alfvenic-nonalfvenic-psp]].
- **Hypothesis:** the residual ~60 % of intervals where the Howes cascade model fails to describe the observed kinetic-range spectrum are systematically associated with **either** (a) high-amplitude (δB/B > 0.5) magnetic structures violating the small-amplitude assumption, **or** (b) the presence of LH-circular ICW peaks at the break (i.e. cyclotron-dominated dissipation). Testable on PSP E1–E2 intervals by reporting (model_fit_ok, δB/B, σ_m_band) per window.
- **Minimal_experiment:** rerun the Howes-model fitting on PSP E1 and E2 windows with and without the propagation-angle assumption (perpendicular-only vs broadband θ_kB distribution) and report whether the fit fraction stays at ≥39.4 % or drops significantly — quantifies the angle-assumption sensitivity that the abstract does not explicitly bound.
- **Composable experiment:** join the per-interval (Q_p_model, Q_e_model) with [[bandyopadhyay-2020-energy-transfer-psp]] cascade-rate ε estimates on the same windows; compute (Q_p_model + Q_e_model) / ε per interval and ask whether the Landau channel alone balances the cascade rate or whether a non-trivial residual remains — that residual is the empirical room for the cyclotron / coherent-structure channels.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `coronal_heating` / `waves_instabilities` cross-bundle (compressible-cascade / Landau-channel dissipation branch).
- **Sibling paper-skills**: [[bandyopadhyay-2020-energy-transfer-psp]] (upstream ε), [[bowen-2024-extended-cyclotron-resonant-heating]] (cyclotron channel — alternative dissipation pathway), [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (mediating role of cyclotron resonance), [[pecora-2022-coherent-structures-proton-electron-heating]] (alternative coherent-structure partition; lead-author dispute documented there).
- **MCPs (proposed contracts, not assumed runtime)**: `psp-data-mcp`, `vlasov-solver-mcp` (PLUME / NHDS / LEOPARD-class), `cdflib`.
- **Harness contract**: this skill exports {Q_p_model, Q_e_model, Q_p_empirical, Q_e_empirical, β_p, β_e, model_fit_ok} per interval; HelioSI roll-up consumes it as the Landau-channel row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.6 (attributes the paper to "Bowen et al." — paraphrase, not a verified attribution; see banner above).
- Publisher: ApJ 946 (2023) — DOI [10.3847/1538-4357/acb542](https://doi.org/10.3847/1538-4357/acb542) (verified 2026-05-19).
- arXiv: [2301.09713](https://arxiv.org/abs/2301.09713) (verified 2026-05-19 — Shankarappa, Klein, Martinović).
- ADS bibcode: TODO_verify (`2023ApJ...946...20S` is the natural guess but not directly verified on 2026-05-19).
- Howes et al. (2008) — kinetic cascade model (foundational, not from inventory).
- Klein & Howes — PLUME solver (foundational, not from inventory).
