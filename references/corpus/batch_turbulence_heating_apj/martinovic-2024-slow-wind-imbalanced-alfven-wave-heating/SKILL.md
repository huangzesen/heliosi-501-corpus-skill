---
name: martinovic-2024-slow-wind-imbalanced-alfven-wave-heating
description: Use when fitting a reflection-driven imbalanced Alfvén-wave cascade heating model to combined PSP + Solar Orbiter slow-wind intervals between 0.06 au and 1 au — central paper claim is that the imbalanced-AW-cascade dissipation rate has a radial profile similar to the empirical proton heating rate from temperature gradients, supporting AW turbulence as a significant contributor to slow-wind ion heating (Bourouaine, Perez, Chandran, Jagarlamudi, Raouafi, Halekas 2024, ApJL accepted; arXiv:2403.17352). Slug retained for backwards compatibility — the published lead author is Bourouaine, not Martinović (verified 2026-05-19).
version: 0.1.0
tags: [psp, solar-orbiter, slow-wind, alfven-wave-cascade, imbalanced-turbulence, reflection-driven, heating]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "S. Bourouaine"
  authors:
    - "S. Bourouaine"
    - "J. C. Perez"
    - "B. D. G. Chandran"
    - "V. K. Jagarlamudi"
    - "N. E. Raouafi"
    - "J. S. Halekas"
  authors_verified: true
  doi: null
  arxiv_id: "2403.17352"
  year: 2024
  venue: "ApJL accepted (arXiv:2403.17352; TODO_verify final ApJL volume/page)"
---

# Bourouaine 2024 — Slow-Wind Imbalanced AW Heating (PSP + SO) (slug: martinovic-2024-…)

> **Attribution note (verified 2026-05-19).** The arXiv landing page for 2403.17352 lists **S. Bourouaine, J. C. Perez, B. D. G. Chandran, V. K. Jagarlamudi, N. E. Raouafi, J. S. Halekas** as authors — M. M. Martinović is *not* an author. The inventory `apj_aa_heliophysics_papers.md §1.16` paraphrases this paper as "Martinović and collaborators" which does not match the published record. The corpus slug `martinovic-2024-…` is retained for backwards compatibility but the cited lead author is now **S. Bourouaine**; use Bourouaine, Perez, Chandran et al. 2024 (ApJL accepted; arXiv:2403.17352) when citing this entry in a manuscript. (Mirrors the slug-retention pattern previously applied to `telloni-2025-psp-solo-radial-alignment-2022-december` and `bowen-2023-landau-damping-proton-electron-heating`.)

## When to use this paper-skill

Load this skill when you need to:

- fit a **reflection-driven imbalanced Alfvén-wave** cascade heating model to PSP + Solar Orbiter slow-wind intervals between 0.06 and 1 au,
- compare model-predicted heating rates to **empirical** proton heating rates derived from radial temperature gradients,
- assess whether AW-cascade heating can sustain slow-wind proton temperatures over this range.

Skip this skill if your interest is fast-wind cyclotron heating ([[bowen-2024-extended-cyclotron-resonant-heating]]), Landau-channel partition ([[bowen-2023-landau-damping-proton-electron-heating]]), or coherent-structure heating ([[pecora-2022-coherent-structures-proton-electron-heating]]).

## Paper identity and claim boundary

- **Citation**: Bourouaine, S., Perez, J. C., Chandran, B. D. G., Jagarlamudi, V. K., Raouafi, N. E., & Halekas, J. S. (2024). *On the Heating of the Slow Solar-Wind by Imbalanced Alfvén-Wave Turbulence from 0.06 au to 1 au: Parker Solar Probe and Solar Orbiter Observations.* **ApJL accepted**; **arXiv:2403.17352** (final ApJL volume / DOI TODO_verify).
- **DOI**: not located on 2026-05-19 (TODO_verify against ADS / IOPscience once the ApJL version is registered).
- **arXiv**: [2403.17352](https://arxiv.org/abs/2403.17352)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.16 (lists this paper under "Martinović and collaborators" — see attribution note above).

**Evidence boundary — what the arXiv abstract supports (verified 2026-05-19 via arXiv.org metadata page for 2403.17352):**

- The paper uses **PSP and SO data** to study how **imbalanced Alfvén-wave turbulent fluctuations** heat the solar wind between **0.06 and 1 au** (abstract-verified).
- The principal observational claim is that **"the radial profile [of the model dissipation rate] trend is similar to the proton heating rate"** (abstract-verified phrasing).
- The model dissipation rate is reported to **align with theoretical predictions** (abstract-verified qualitative).
- The authors conclude that **AW turbulence significantly contributes to ion heating in slow solar wind streams** (abstract-verified phrasing; "significantly contributes" — not "exclusively explains").
- The verified author list is Bourouaine, Perez, Chandran, Jagarlamudi, Raouafi, Halekas (six authors).

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact reflection-driven AW cascade model variant (Chandran–Hollweg-class, van Ballegooijen-class, or a paper-specific closed form) is **TODO_verify** against §2 / Methods of the accepted ApJL version.
- The slow-wind selection rule (V_sw threshold only, or also Alfvénicity / ionic-composition conditioning) is TODO_verify.
- The exact per-bin Q_AW / Q_p ratios, the radial bins used, and the tolerance against the empirical profile are TODO_verify.
- The correlation-length L estimator and integration cutoff are TODO_verify.

Out-of-scope (the entry deliberately refuses these): extending the conclusion to fast-wind streams; collapsing across stream classes when the paper conditions on slow wind; conflating Q_AW with cyclotron- or Landau-channel rates without explicit cross-paper analysis; treating "similar radial trend" as quantitative bin-by-bin agreement (the abstract claims trend similarity and significance, not unique fit).

> **Assumptions and failure modes** (load-bearing): Q_AW is strongly sensitive to the correlation length L and to the Elsässer imbalance z+² / z-² — both of which evolve radially and must be measured per interval; the slow-wind selection conditions the result (a pure V_sw threshold mixes Alfvénic and non-Alfvénic slow streams); empirical Q_p from T-gradients depends on the adiabatic-expansion baseline (spherical vs non-spherical expansion changes the answer); statistically combining PSP and SO across many intervals is a population claim, not a Lagrangian comparison.

## Scientific claim to reproduce or operationalize

Slow-wind proton heating from 0.06 to 1 au can be sustained, to a significant degree, by an imbalanced Alfvén-wave cascade driven by Alfvén-wave reflection at the inhomogeneous background. Fitting the reflection-driven cascade model to combined PSP + SO slow-wind data yields a radial profile of the model dissipation rate Q_AW that is similar in trend to the empirical Q_p from radial T_p gradients across the 0.06–1 au range.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN, T_p | L3 | CDAWeb / PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR / CDAWeb |
| Solar Orbiter SWA/PAS | n_p, V_RTN, T_p | L2 | SOAR |
| Reflection-driven AW cascade model | empirical / closed-form heating Q_AW(r, z+, z-, L) | external code | TODO_verify which model variant (Chandran–Hollweg-class, van Ballegooijen-class, paper-specific) |

Time range: combined PSP + SO slow-wind intervals spanning 0.06 au to ~1 au — exact interval selection **TODO_verify** against §2 of the accepted ApJL version.

## Algorithm/workflow steps

1. **Slow-wind selection** — Identify slow-wind intervals per spacecraft (V_sw threshold and / or Alfvénicity / ionic-composition criteria — TODO_verify the paper's exact rule).
2. **Elsässer amplitudes** — Compute z± per interval; report (z+², z-², imbalance ratio z+² / z-²).
3. **Outer scale L** — Estimate the correlation length L per interval from the autocorrelation of B or z± (cutoff convention TODO_verify against the paper).
4. **Reflection-driven AW model** — Evaluate Q_AW = f(z+², z-², L, V_A, dV_A/dr) per the chosen model (TODO_verify formula); the imbalanced cascade rate is the input.
5. **Empirical Q_p** — Compute empirical Q_p from radial T_p gradient and adiabatic-expansion baseline (spherical / non-spherical choice TODO_verify against the paper).
6. **Radial comparison** — Compare Q_AW(r) to empirical Q_p(r) per heliocentric-distance bin from 0.06 to 1 au; check trend similarity rather than per-bin equality.
7. **Acceptance** — Q_AW(r) radial trend matches Q_p(r) trend across the range (abstract-verified qualitative claim); the AW channel "significantly contributes" to slow-wind heating (abstract wording — do not silently widen to "explains").

## Minimal executable benchmark or validation target

**Target**: model Q_AW from the reflection-driven imbalanced AW cascade has a radial profile similar in trend to the empirical Q_p in PSP + SO slow-wind bins between 0.06 and 1 au (abstract-verified qualitative target). Per-bin ratio Q_AW / Q_p values and any quantitative tolerance are TODO_verify against the accepted ApJL version.

Recommended check artifacts:

- `bourouaine2024_slow_wind_aw_heating.csv` — one row per interval: (mission, t_start, t_end, r_au, V_sw, z+², z-², imbalance, L, Q_AW, Q_p_empirical, ratio).
- Q_AW(r) vs Q_p(r) radial-bin plot, with both curves overlaid.
- Single scalar QC: Spearman rank correlation between Q_AW(r) and Q_p(r) across radial bins (target: monotonic positive correlation — operationalises "similar trend" without requiring quantitative magnitude match).

## Known pitfalls / failure modes

- **Slow-wind definition**: a pure V_sw threshold mixes Alfvénic and non-Alfvénic slow streams; consider conditioning on Alfvénicity (cf. [[damicis-2021-alfvenic-nonalfvenic-psp]]).
- **Correlation-length convention**: Q_AW is strongly sensitive to L; the integration limit on the autocorrelation drives the result — document convention.
- **Adiabatic baseline for Q_p**: the empirical heating rate depends on the assumed adiabatic-expansion baseline; spherical vs non-spherical expansion changes the answer.
- **Imbalance amplification near the Sun**: reflection-driven imbalance grows toward the Sun — z+² / z-² evolves with r and must be measured per interval, not assumed.
- **PSP / SO cadence and frame matching**: as for [[telloni-2025-psp-solo-radial-alignment-2022-december]].
- **Mapping is statistical, not Lagrangian**: combining PSP and SO statistically (not Lagrangianly) means the heating-rate comparison is a population, not parcel-level, statement.
- **"Similar trend" vs "quantitative match"**: do not widen the abstract's "trend is similar" to "Q_AW = Q_p"; trend similarity is rank-correlation-level evidence, not bin-by-bin agreement.
- **"Significantly contributes" vs "explains"**: the abstract claims AW turbulence is a significant contributor, not the sole contributor.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "Q_AW(r) trend matches Q_p(r) trend in PSP + SO slow wind from 0.06 to 1 au" becomes the per-interval CSV + the radial-bin overlay plot + the Spearman-correlation scalar.
- **Methods / equations → executable workflows**: Elsässer amplitudes + correlation length + reflection-driven AW model evaluation + empirical Q_p from T_p gradient are steps 2–5.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS + SWEAP and Solar Orbiter MAG + SWA-PAS time series at the required cadence, plus an external reflection-driven Alfvén-wave cascade-model evaluator; runtimes bind concrete adapters (see Layer 3 for example bindings — the cascade-model evaluator in particular is a proposed surface, not an existing runtime adapter).
- **Caveats → skill memory**: slow-wind class mixing, correlation-length convention, adiabatic baseline, statistical-vs-Lagrangian distinction, "trend" vs "match" wording boundary.
- **Figures / results → benchmark artifacts**: Q_AW(r) vs Q_p(r) overlay + per-interval CSV.

## Layer 4 — Research-generation affordances

- **Gap:** the abstract claims trend similarity but provides no quantitative per-bin Q_AW / Q_p ratio. A composable experiment that overlays Q_AW(r) (this skill), Q_p,cyc(r) (from [[bowen-2024-extended-cyclotron-resonant-heating]]) and Q_p,Landau(r) (from [[bowen-2023-landau-damping-proton-electron-heating]] / Shankarappa et al. 2023) on the **same radial bins** would deliver the first three-channel radial decomposition of slow-wind proton heating from 0.06 to 1 au.
- **Tension:** the reflection-driven imbalanced-AW model is naturally most efficient in *slow-Alfvénic* wind where reflection generates a non-trivial z-² component; cyclotron-resonance arguments ([[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]) are typically framed for *fast Alfvénic* wind. The two should therefore be *complementary* across stream classes — testable by replicating both protocols on PSP + SO intervals stratified by [[damicis-2021-alfvenic-nonalfvenic-psp]] Alfvénicity classes.
- **Hypothesis:** in slow-wind intervals with strong Alfvénic character (high σ_c but low V_sw), the reflection-driven AW channel underestimates Q_p because the imbalance z+² / z-² is amplified by reflection from the inhomogeneous background near the Sun but not yet damped at the spacecraft location, breaking the cascade-balance assumption. Testable by stratifying the per-interval (Q_AW, Q_p_empirical) ratio by σ_c and reporting the residual at high σ_c.
- **Minimal_experiment:** rerun the cascade-model fit with two correlation-length cutoffs (e.g. e-folding scale vs zero-crossing) and report whether the "similar radial trend" claim holds under both — quantifies the L-sensitivity that the abstract does not explicitly bound.
- **Composable experiment:** join the per-interval Q_AW table with [[bandyopadhyay-2020-energy-transfer-psp]] ε estimates on the *same* slow-wind windows; if Q_AW > ε on a non-trivial fraction of intervals, the cascade-rate normalisation is internally inconsistent and the AW-channel attribution must be re-examined.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `coronal_heating` (AW-cascade branch) + `solar_orbiter` (slow-wind PSP-SO pooled).
- **Sibling paper-skills**: [[damicis-2021-alfvenic-nonalfvenic-psp]] (Alfvénic vs non-Alfvénic classification — relevant to slow-wind selection), [[bandyopadhyay-2020-energy-transfer-psp]] (upstream cascade-rate input), [[telloni-2021-psp-solo-radial-alignment-turbulence]] / [[telloni-2025-psp-solo-radial-alignment-2022-december]] (Lagrangian-conjunction context), [[bowen-2023-landau-damping-proton-electron-heating]] (alternative dissipation channel for cross-check; Shankarappa lead-author dispute documented there), [[bowen-2024-extended-cyclotron-resonant-heating]] (fast-wind cyclotron complement).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `solar-orbiter-data-mcp`, `aw-cascade-mcp` (external model evaluator), `cdflib`.
- **Harness contract**: exports {z+², z-², L, Q_AW, Q_p_empirical, ratio} per slow-wind interval; HelioSI roll-up consumes it as the slow-wind AW-heating row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.16 (attributes the paper to "Martinović and collaborators" — paraphrase, not a verified attribution; see banner above).
- arXiv: [2403.17352](https://arxiv.org/abs/2403.17352) (verified 2026-05-19 — full six-author list Bourouaine, Perez, Chandran, Jagarlamudi, Raouafi, Halekas; ApJL accepted).
- Final ApJL volume / DOI: TODO_verify (not registered as of 2026-05-19).
- ADS bibcode: TODO_verify (no resolved bibcode on 2026-05-19).
- Chandran & Hollweg / van Ballegooijen — reflection-driven AW cascade theory (foundational, not from inventory).
