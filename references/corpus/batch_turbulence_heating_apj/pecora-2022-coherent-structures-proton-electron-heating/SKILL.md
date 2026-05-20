---
name: pecora-2022-coherent-structures-proton-electron-heating
description: Use when attributing differential proton-over-electron heating in PSP first-perihelion data to coherent structures identified by Partial Variance of Increments — central paper claim is that conditional averaging around regions with strong gradients in the magnetic field (high-PVI / current-sheet events) shows preferential proton over electron heating during PSP E1, consistent with a nonlinear-turbulent-cascade heating mechanism in the nascent solar wind (Sioulas et al. 2022, ApJL 935; DOI 10.3847/2041-8213/ac85de; arXiv:2206.10671). Slug retained for backwards compatibility — the published lead author is Sioulas, not Pecora (verified 2026-05-19).
version: 0.1.0
tags: [psp, turbulence, heating, coherent-structures, pvi, current-sheets, fields, sweap]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "N. Sioulas"
  authors:
    - "N. Sioulas"
    - "C. Shi"
    - "Z. Huang"
    - "M. Velli"
  authors_verified: true
  doi: "10.3847/2041-8213/ac85de"
  arxiv_id: "2206.10671"
  year: 2022
  venue: "The Astrophysical Journal Letters 935 (2022)"
---

# Sioulas 2022 — Preferential Proton over Electron Heating from Coherent Structures (PSP E1) (slug: pecora-2022-…)

> **Attribution note (verified 2026-05-19).** The arXiv landing page for 2206.10671 and the IOPscience page for DOI 10.3847/2041-8213/ac85de both list **N. Sioulas, C. Shi, Z. Huang, M. Velli** as the four authors — F. Pecora, R. Bandyopadhyay, D. Ruffolo, W. H. Matthaeus, T. N. Parashar, R. Chhiber, A. Chasapis are *not* authors of this paper. The inventory `apj_aa_heliophysics_papers.md §1.7` attributes the paper to "Pecora et al." which does not match the published record (this may be a confusion with a different Pecora-led PSP-PVI paper from the same era). The corpus slug `pecora-2022-…` is retained for backwards compatibility but the cited lead author is now **N. Sioulas**; use Sioulas, Shi, Huang, & Velli 2022, ApJL 935 when citing this entry in a manuscript. (Mirrors the slug-retention pattern previously applied to other batch entries.)

## When to use this paper-skill

Load this skill when you need to:

- detect **coherent structures** (regions of strong gradients in the magnetic field) in PSP FIELDS data via a **Partial Variance of Increments (PVI)** or equivalent intermittency diagnostic,
- conditionally average proton and electron temperatures around high-PVI / strong-gradient events,
- test whether preferential **proton over electron** heating is associated with coherent structures, consistent with a nonlinear-turbulent-cascade heating mechanism in the nascent solar wind.

Skip this skill if your interest is wave-mediated heating partitioning (use the Bowen-batch / Shankarappa 2023 skills) or general intermittency scaling without a heating link (use [[sioulas-2022-magnetic-field-intermittency-psp-solo]] from `pilot_turbulence/`).

## Paper identity and claim boundary

- **Citation**: Sioulas, N., Shi, C., Huang, Z., & Velli, M. (2022). *Preferential Heating of Protons over Electrons from Coherent Structures during the First Perihelion of the Parker Solar Probe.* **ApJL 935** (2022).
- **DOI**: [10.3847/2041-8213/ac85de](https://doi.org/10.3847/2041-8213/ac85de)
- **arXiv**: [2206.10671](https://arxiv.org/abs/2206.10671)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.7 (lists this DOI / arXiv ID under "Pecora et al." — see attribution note above).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via arXiv.org for 2206.10671 and IOPscience for DOI 10.3847/2041-8213/ac85de):**

- The paper analyses PSP **first-perihelion (Encounter 1)** data (abstract-verified).
- The empirical observation is that **"regions of space with strong gradients in the magnetic field"** show protons experiencing **"significantly greater temperature increases compared to electrons"** (abstract-verified phrasing).
- The proposed interpretation is **"a heating mechanism in the nascent solar wind environment facilitated by a nonlinear turbulent cascade"** (abstract-verified phrasing — the abstract attributes the heating to the *cascade* / coherent-structure ensemble rather than to a specific dissipation operator).
- The verified author list is Sioulas, Shi, Huang, Velli (four authors).
- Published as ApJL **935** (2022), DOI 10.3847/2041-8213/ac85de.

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- Whether the paper uses the PVI metric specifically (vs another increment-amplitude diagnostic such as |ΔB| / σ_ΔB without the rolling-window normalisation) and the exact gradient-identification threshold are **TODO_verify** against §2 of the published paper. The abstract uses the more general phrase "regions with strong gradients in the magnetic field."
- The quantitative ΔT_p / ΔT_e magnitude (the abstract says "significantly greater" but does not give a ratio) is TODO_verify.
- Whether the conditional-averaging window length and the background-baseline construction match the standard Greco et al. PVI conventions is TODO_verify.

Out-of-scope (the entry deliberately refuses these): extending the conclusion beyond PSP E1 (the abstract is explicit that this is a first-perihelion result; other encounters with different stream classes are not in the abstract scope); claiming coherent-structure heating is the dominant channel everywhere; merging it with a Landau-damping or cyclotron partition without explicit cross-paper analysis (cf. [[bowen-2023-landau-damping-proton-electron-heating]] / [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]]).

> **Assumptions and failure modes** (load-bearing): the gradient-identification step requires an explicit threshold and an averaging window — results depend on both, so they must be quoted; T_e from SPAN-e can be biased by photoelectron contamination in some intervals; superposed-epoch averaging can leak between events that are too close together; conditional correlation does not establish causal heating without a non-event baseline.

## Scientific claim to reproduce or operationalize

A subset of solar-wind turbulent dissipation in the nascent (near-Sun) solar wind is hosted by coherent intermittent structures — regions of strong magnetic-field gradients identified through increment-amplitude diagnostics. Conditional averages of T_p, T_e around these high-gradient events during PSP E1 show that T_p increases significantly more than T_e near the structures, consistent with a nonlinear turbulent cascade as the underlying heating channel that preferentially energises protons over electrons.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, |B| | L2, ~1 vec/s | CDAWeb / PSP SOC |
| PSP SWEAP/SPC | n_p, V_RTN, T_p | L3 | CDAWeb / PSP SOC |
| PSP SWEAP/SPAN-e | T_e | L3 | CDAWeb / PSP SOC |

Time range: PSP Encounter 1, ~2018-11-06, ~0.17 au. Use intervals with valid simultaneous SPC and SPAN-e moments.

## Algorithm/workflow steps

1. **Interval selection** — Continuous PSP E1 intervals with valid SPC + SPAN-e moments and clean MAG.
2. **Increment field** — Compute ΔB(t, τ) = B(t + τ) − B(t) for one or more lag scales τ matched to the inertial range.
3. **Gradient / PVI metric** — Compute PVI(t, τ) = |ΔB(t, τ)| / √(⟨|ΔB|²⟩_T) over a sliding averaging window T, or the equivalent normalised gradient metric used by the paper (TODO_verify whether the paper's exact diagnostic matches PVI or a related metric).
4. **Event catalog** — Build a list of t_i where the metric exceeds threshold θ (e.g. PVI > 3 in the Greco convention); record event amplitudes.
5. **Conditional averaging** — For a lag window ±Δt around each event, compute ⟨T_p⟩ and ⟨T_e⟩ as functions of relative time.
6. **Background comparison** — Repeat conditional averaging at random non-event times to estimate the baseline.
7. **Heating-signature scalar** — Compute (ΔT_p / ⟨T_p⟩) − (ΔT_e / ⟨T_e⟩) at the event; positive value implies preferential proton heating (abstract-verified sign).
8. **Acceptance** — Conditional ΔT_p significantly exceeds ΔT_e on average for high-gradient events at PSP E1 (qualitative sign matches the paper); quantitative magnitude / ratio TODO_verify against ApJL 935 figures.

## Minimal executable benchmark or validation target

**Target**: conditional averaging of T_p, T_e around strong-magnetic-gradient events in PSP E1 returns ΔT_p significantly larger than ΔT_e (abstract-verified qualitative sign — "significantly greater"); exact numerical ratio TODO_verify against figures of ApJL 935 (2022).

Recommended check artifacts:

- `sioulas2022_pvi_heating.csv` — one row per (interval, threshold): (t_start, t_end, threshold, N_events, mean_ΔT_p, mean_ΔT_e, ratio).
- Superposed-epoch plot of T_p(t), T_e(t) around high-gradient events.
- Single scalar QC: mean ratio (ΔT_p / ⟨T_p⟩) / (ΔT_e / ⟨T_e⟩) at the chosen threshold (target: > 1).

## Known pitfalls / failure modes

- **Gradient-metric threshold sensitivity**: results depend on θ — quote θ explicitly and run a θ-sweep (e.g. 2, 3, 4, 6) and report stability.
- **Averaging window L**: PVI depends on the normalisation window length; report L (e.g. 30 min, 1 h) explicitly.
- **SPAN-e contamination**: T_e from SPAN-e can be biased by photoelectrons; flag affected intervals.
- **SPC moments at non-radial flow**: SPC field-of-view assumes radial flow; non-radial intervals bias T_p, n_p.
- **Causality of association**: conditional correlation ≠ causal heating; control with random-time baselines.
- **Superposed-epoch leakage**: events close in time leak into one another's windows — enforce a minimum spacing.
- **"Significantly greater" vs quantitative**: the abstract uses qualitative language; do not silently widen this to "ΔT_p = N × ΔT_e" without verifying the figures.
- **PVI vs paper's exact diagnostic**: the paper abstract refers to "regions of strong magnetic-field gradients" without naming the PVI normalisation explicitly — use PVI as the default operationalisation but log the choice as a TODO_verify against the paper's §2.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "preferential proton over electron heating at coherent structures in PSP E1" becomes the conditional-averaging CSV + the (ΔT_p / T_p) / (ΔT_e / T_e) scalar.
- **Methods / equations → executable workflows**: gradient / PVI computation + thresholding + conditional averaging are steps 2–5.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP SPC + SPAN-e L3 time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings).
- **Caveats → skill memory**: θ + L sensitivity, SPAN-e bias, SPC non-radial-flow issue, "significantly greater" wording boundary.
- **Figures / results → benchmark artifacts**: per-interval CSV + superposed-epoch plot.

## Layer 4 — Research-generation affordances

- **Gap:** the abstract names the cascade as the heating mechanism but does not separate the contribution from coherent structures vs from a smooth wave-driven background. A composable experiment that runs the conditional-averaging protocol here AND the polarisation / cyclotron protocol from [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] on the same PSP E1 windows would partition the E1 heating signal between coherent-structure and wave-driven channels — neither paper alone constrains the balance.
- **Tension:** [[bowen-2023-landau-damping-proton-electron-heating]] (Shankarappa et al. 2023) reports the Landau-channel partition depends strongly on β, with Q_p / Q_e increasing toward higher β; the present paper reports preferential proton heating at coherent structures *without* β-stratification (per abstract). If the high-PVI ensemble is preferentially drawn from high-β regions of PSP E1, the two papers' conclusions overlap; if not, they are genuinely independent channel attributions. Testable by reporting the β distribution of PVI-flagged windows.
- **Hypothesis:** the per-event preferential proton heating signal ΔT_p − ΔT_e scales with the local PVI amplitude rather than being binary; i.e., the heating is set by the *strength* of the coherent structure, not just by its presence above threshold. Testable by reporting ΔT_p − ΔT_e binned by PVI amplitude (above the detection threshold).
- **Minimal_experiment:** rerun the conditional averaging at PVI thresholds θ ∈ {2, 3, 4, 6} and report whether the (ΔT_p / T_p) − (ΔT_e / T_e) signal is monotonic in θ; non-monotonicity would indicate a finite event-population effect (small-N noise dominates at large θ) and would set the floor on the paper's robustness claim.
- **Composable experiment:** join the per-event ΔT_p / ΔT_e table with [[bandyopadhyay-2020-energy-transfer-psp]] cascade-rate ε on the same windows; if (∑ events ΔT_p × n_event) / ε is O(1), coherent structures alone can account for the cascade-rate energy budget; if much smaller, a continuous wave-mediated channel must carry the residual.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `coronal_heating` (coherent-structure-mediated branch) and `solar-wind-turbulence` (intermittency).
- **Sibling paper-skills**: [[sioulas-2022-magnetic-field-intermittency-psp-solo]] (PVI definition + intermittency context, same PVI pipeline, same lead author), [[bowen-2023-landau-damping-proton-electron-heating]] (alternative wave-mediated heating partition; Shankarappa lead-author dispute documented there), [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (cyclotron alternative).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `cdflib`. The PVI estimator itself is a building block shared with [[sioulas-2022-magnetic-field-intermittency-psp-solo]] and is a candidate synthesis-skill in Stage B.
- **Harness contract**: this skill exports {ΔT_p, ΔT_e, ratio} per (interval, θ); HelioSI roll-up consumes it as the coherent-structure heating row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.7 (attributes the paper to "Pecora et al." — paraphrase, not a verified attribution; see banner above).
- Publisher: ApJL 935 (2022) — DOI [10.3847/2041-8213/ac85de](https://doi.org/10.3847/2041-8213/ac85de) (verified 2026-05-19).
- arXiv: [2206.10671](https://arxiv.org/abs/2206.10671) (verified 2026-05-19 — Sioulas, Shi, Huang, Velli).
- ADS bibcode: TODO_verify (`2022ApJ...935L..27S` is the natural guess but not directly verified on 2026-05-19).
- Greco et al. (2008) — PVI definition (foundational, not from inventory).
- Osman et al. (2012) — PVI heating association (foundational, not from inventory).
