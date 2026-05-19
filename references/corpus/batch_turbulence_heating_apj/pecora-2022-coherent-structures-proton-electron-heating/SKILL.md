---
name: pecora-2022-coherent-structures-proton-electron-heating
description: Use when attributing differential proton-over-electron heating in PSP first-perihelion data to coherent structures identified by Partial Variance of Increments — central paper claim is that conditional averaging around high-PVI (current-sheet) events shows preferential proton over electron heating during PSP E1 (Pecora et al. 2022, arXiv:2206.10671; venue TODO verify).
version: 0.1.0
tags: [psp, turbulence, heating, coherent-structures, pvi, current-sheets, fields, sweap]
quality_level: pilot
executable_status: scaffold
---

# Pecora 2022 — Coherent-Structure Proton/Electron Heating (PSP E1)

## When to use this paper-skill

Load this skill when you need to:

- detect **coherent structures** (current sheets) in PSP FIELDS magnetic-field data via the **Partial Variance of Increments (PVI)** method,
- conditionally average proton and electron temperatures around high-PVI events,
- test whether preferential **proton over electron** heating is associated with coherent structures, as opposed to a wave-driven heating channel.

Skip this skill if your interest is wave-mediated heating partitioning (use the Bowen 2023 / 2024 skills in this batch) or general intermittency scaling without a heating link (use [[sioulas-2022-magnetic-field-intermittency-psp-solo]] from `pilot_turbulence/`).

## Paper identity and claim boundary

- **Citation**: Pecora, F., Bandyopadhyay, R., Ruffolo, D., Matthaeus, W. H., Parashar, T. N., Chhiber, R., Chasapis, A., et al. (2022). *Preferential Proton over Electron Heating from Coherent Structures during the First Perihelion of Parker Solar Probe.* arXiv:2206.10671. **Venue (MNRAS / ApJ 2022) TODO verify.**
- **DOI**: TODO verify.
- **arXiv**: [2206.10671](https://arxiv.org/abs/2206.10671)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.7.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> Coherent structures (current sheets) identified by PVI in PSP first-perihelion FIELDS data correlate with conditionally enhanced proton temperatures relative to electrons, supporting preferential proton over electron heating at these structures.

Out-of-scope: extending the conclusion beyond PSP E1 (other encounters with different stream classes have not been shown in inventory), claiming this is the dominant heating channel everywhere, or merging it with a Landau-damping partition without explicit cross-paper analysis (cf. [[bowen-2023-landau-damping-proton-electron-heating]]).

## Scientific claim to reproduce or operationalize

A subset of solar-wind turbulent dissipation is hosted by coherent intermittent structures (e.g. current sheets). PVI thresholding identifies these structures; conditional averages of T_p, T_e around high-PVI events during PSP E1 show that T_p increases more than T_e near the structures, implying a heating channel that preferentially heats protons.

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
3. **PVI** — Compute PVI(t, τ) = |ΔB(t, τ)| / √(⟨|ΔB|²⟩_T) over a sliding averaging window T; pick threshold θ (e.g. PVI > 3).
4. **Event catalog** — Build a list of t_i where PVI > θ; record event amplitudes.
5. **Conditional averaging** — For a lag window ±Δt around each event, compute ⟨T_p⟩ and ⟨T_e⟩ as functions of relative time.
6. **Background comparison** — Repeat conditional averaging at random non-event times to estimate the baseline.
7. **Heating-signature scalar** — Compute ΔT_p / ⟨T_p⟩ − ΔT_e / ⟨T_e⟩ at the event — positive value implies preferential proton heating.
8. **Acceptance** — Conditional ΔT_p exceeds ΔT_e on average for high-PVI events at PSP E1 (qualitative sign matches paper; TODO verify exact magnitude / Fig. in full text).

## Minimal executable benchmark or validation target

**Target**: conditional averaging of T_p, T_e around PVI-flagged PSP E1 events returns ΔT_p > ΔT_e (preferential proton heating signature) with the sign and qualitative magnitude reported in the paper (TODO verify numerical ratio).

Recommended check artifacts:

- `pecora2022_pvi_heating.csv` — one row per (interval, PVI threshold): (t_start, t_end, θ, N_events, mean_ΔT_p, mean_ΔT_e, ratio).
- Superposed-epoch plot of T_p(t), T_e(t) around high-PVI events.
- Single scalar QC: mean ratio ΔT_p / ΔT_e at θ = 3.

## Known pitfalls / failure modes

- **PVI threshold sensitivity**: results depend on θ — quote θ explicitly and run a θ-sweep (e.g. 2, 3, 4, 6).
- **Averaging window L**: PVI depends on the normalisation window length; report L (e.g. 30 min, 1 h) explicitly.
- **SPAN-e contamination**: T_e from SPAN-e can be biased by photoelectrons; flag affected intervals.
- **SPC moments at non-radial flow**: SPC field-of-view assumes radial flow; non-radial intervals bias T_p, n_p.
- **Causality of association**: conditional correlation ≠ causal heating; control with random-time baselines.
- **Superposed-epoch leakage**: events close in time leak into one another's windows — enforce a minimum spacing.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "preferential proton heating at coherent structures in PSP E1" becomes the conditional-averaging CSV + ΔT_p / ΔT_e scalar.
- **Methods / equations → executable workflows**: PVI computation + thresholding + conditional averaging are steps 2–5.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP SPC + SPAN-e L3 time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings).
- **Caveats → skill memory**: θ + L sensitivity, SPAN-e bias, SPC non-radial-flow issue.
- **Figures / results → benchmark artifacts**: per-interval CSV + superposed-epoch plot.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `coronal_heating` (coherent-structure-mediated branch) and `solar-wind-turbulence` (intermittency).
- **Sibling paper-skills**: [[sioulas-2022-magnetic-field-intermittency-psp-solo]] (PVI definition + intermittency context, same PVI pipeline), [[bowen-2023-landau-damping-proton-electron-heating]] (alternative wave-mediated heating partition), [[bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance]] (cyclotron alternative).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `cdflib`. The PVI estimator itself is a building block shared with [[sioulas-2022-magnetic-field-intermittency-psp-solo]] and is a candidate synthesis-skill in Stage B.
- **Harness contract**: this skill exports {ΔT_p, ΔT_e, ratio} per (interval, θ); HelioSI roll-up consumes it as the coherent-structure heating row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.7.
- arXiv: https://arxiv.org/abs/2206.10671
- Greco et al. (2008) — PVI definition (foundational, not from inventory).
- Osman et al. (2012) — PVI heating association (foundational, not from inventory).
