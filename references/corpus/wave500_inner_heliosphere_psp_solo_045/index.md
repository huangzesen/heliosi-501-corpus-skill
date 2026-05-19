# wave500_inner_heliosphere_psp_solo_045 — Batch Index

Wave 500 batch #045 of the HelioSI paper-to-skill factory (v0.2).

**Scope**: 45 harness-agnostic paper-skills focused on PSP / Solar Orbiter /
Helios / inner-heliosphere observations — switchbacks, magnetic structures,
alignments, near-Sun phenomena. All skills are runtime-neutral; named tools
(pyspedas, sunkit-magex, sw-scanner, etc.) appear only as example adapters,
never as required contracts.

**Quality**: all 45 are `paper-grounded-pending-full-text`. Promotion to
`method-ready` / `executable` requires lifting the per-paper reproducible
anchor (Fig/Table) into `validation_target` after full-text verification.

**Cross-batch hygiene**: candidate slug list diffed against the 96 existing
directories under `paper_skill_corpus/*/`. No duplicates introduced.

## Skills (45)

| # | Slug | First author | Year | Primary theme | Missions |
|---|------|--------------|------|----------------|----------|
| 1 | `huang-2025-what-are-switchbacks-solitary-alfven-wave-model` | Z. Huang | 2025 | switchbacks | PSP |
| 2 | `rivera-2024-mixed-source-signatures-switchback-patches-heavy-ions` | Y. J. Rivera | 2024 | switchbacks | PSP, Solar Orbiter |
| 3 | `das-2026-hammerhead-vdf-prevalence-hcs-psp` | S. B. Das | 2026 | psp_data | PSP |
| 4 | `sun-2026-compound-reconnection-exhaust-mirror-modes-hcs` | W. Sun | 2026 | reconnection | PSP |
| 5 | `ofman-2025-large-scale-kelvin-helmholtz-cme-driven` | L. Ofman | 2025 | other | PSP, Solar Orbiter, other |
| 6 | `shankarappa-2025-free-energy-sources-ion-scale-waves-psp` | N. Shankarappa | 2025 | waves_instabilities | PSP |
| 7 | `martinovic-2025-oblique-drift-instability-solar-wind-heating` | M. M. Martinović | 2025 | waves_instabilities | PSP |
| 8 | `mostl-2025-icme-magnetic-field-evolution-0p07-5p4-au` | C. Möstl | 2025 | other | PSP, Solar Orbiter, Wind, ACE, MESSENGER, STEREO |
| 9 | `choi-2024-whistler-waves-young-solar-wind-psp` | K.-E. Choi | 2024 | waves_instabilities | PSP |
| 10 | `touresse-2024-untwisting-jets-super-alfvenic-wind-switchback` | J. Touresse | 2024 | switchbacks | PSP |
| 11 | `ervin-2024-slow-alfvenic-source-regions-psp` | T. Ervin | 2024 | solar_orbiter | PSP |
| 12 | `jiao-2023-steady-sub-alfvenic-solar-wind-psp` | Y. Jiao | 2023 | psp_data | PSP |
| 13 | `agapitov-2023-constraints-alfvenicity-switchbacks` | O. V. Agapitov | 2023 | switchbacks | PSP |
| 14 | `trotta-2023-interplanetary-shock-psp-solo-0p07au-0p7au` | D. Trotta | 2023 | other | PSP, Solar Orbiter |
| 15 | `sun-2024-magnetic-island-wispr-psp` | W. Sun (et al., TODO verify) | 2024 | other | PSP |
| 16 | `adhikari-2025-trans-alfvenic-region-psp-e8-e19` | S. Adhikari | 2025 | psp_data | PSP |
| 17 | `iizawa-2025-inverse-cascade-magnetic-helicity-inner-heliosphere` | M. Iizawa | 2025 | turbulence | PSP |
| 18 | `jiang-2025-third-order-law-angular-dependence-anisotropic-mhd` | B. Jiang | 2025 | turbulence | n/a |
| 19 | `zhao-2025-mode-composition-magnetic-anisotropy-solar-wind` | S. Zhao | 2025 | turbulence | PSP, Wind |
| 20 | `sharma-2026-sub-ion-current-sheets-kinetic-alfven-turbulence` | J. Sharma | 2026 | turbulence | PSP |
| 21 | `mondal-2025-sub-electron-turbulence-psp-density-spectra` | S. Mondal | 2025 | turbulence | PSP |
| 22 | `chhiber-2026-dynamical-age-alfvenic-turbulence-inner-heliosphere` | R. Chhiber | 2026 | turbulence | PSP, Solar Orbiter, Wind, Helios |
| 23 | `gurram-2026-mms-cme-sub-alfvenic-wind-1au` | H. Gurram | 2026 | other | other |
| 24 | `gonzalez-2026-compressible-fluctuations-balanced-imbalanced` | C. A. Gonzalez | 2026 | turbulence | PSP, Solar Orbiter |
| 25 | `yogesh-2026-solar-wind-heating-radial-evolution-psp` | Yogesh | 2026 | coronal_heating | PSP |
| 26 | `saguchi-2026-parametric-decay-temperature-anisotropy-psp` | H. Saguchi | 2026 | waves_instabilities | PSP |
| 27 | `wyper-2026-switchback-formation-mechanisms-review` | P. F. Wyper | 2026 | switchbacks | PSP |
| 28 | `good-2025-residual-energy-mhd-shocks-interplanetary` | S. W. Good | 2025 | other | PSP, Solar Orbiter, Wind |
| 29 | `gonzalez-2023-local-proton-heating-discontinuities-alfvenic` | C. A. Gonzalez | 2023 | coronal_heating | PSP |
| 30 | `magyar-2024-synthetic-modeling-plasma-frame-psp` | N. Magyar | 2024 | other | PSP |
| 31 | `bandyopadhyay-2025-helios-mission-archival-reanalysis` | R. Bandyopadhyay (TODO verify first author) | 2025 | turbulence | Helios, PSP, Solar Orbiter |
| 32 | `cattell-2025-stochastic-heating-sub-alfvenic-wind-psp` | C. Cattell (et al., PSP team) | 2025 | coronal_heating | PSP |
| 33 | `schwadron-2022-switchback-deflections-beyond-early-encounters` | N. M. Schwadron | 2022 | switchbacks | PSP |
| 34 | `vech-2022-anisotropy-kinetic-scales-psp` | D. Vech | 2022 | turbulence | PSP |
| 35 | `bowen-2022-anisotropic-turbulence-radial-evolution-psp` | T. A. Bowen | 2022 | turbulence | PSP |
| 36 | `cuesta-2023-scaling-anisotropy-stationary-background-psp` | M. M. Cuesta | 2023 | turbulence | PSP |
| 37 | `verniero-2023-proton-alpha-instabilities-ion-cyclotron-wave-event` | J. L. Verniero | 2023 | waves_instabilities | PSP |
| 38 | `stevens-2022-reconciling-psp-mhd-theory-plasma-frame` | M. L. Stevens | 2022 | turbulence | PSP |
| 39 | `chen-2023-relation-switchbacks-turbulence-inner-heliosphere` | C. H. K. Chen (et al.) | 2023 | switchbacks | PSP |
| 40 | `gao-2024-emergence-two-inertial-subranges-solar-wind-turbulence` | A. Gao (TODO verify first author) | 2024 | turbulence | PSP |
| 41 | `woodham-2024-alpha-proton-differential-flow-young-solar-wind` | L. D. Woodham (TODO verify first author) | 2024 | psp_data | PSP |
| 42 | `cranmer-2023-alfven-surface-punch-prospects-review` | S. R. Cranmer | 2023 | other | PSP, other |
| 43 | `halekas-2024-coronal-heating-switchback-budget-ruled-out` | J. Halekas | 2024 | coronal_heating | PSP |
| 44 | `raouafi-2023-psp-four-years-discoveries-solar-minimum` | N. Raouafi | 2023 | psp_data | PSP |
| 45 | `damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind` | R. D'Amicis | 2026 | solar_orbiter | PSP, Solar Orbiter, Wind |

## Layer hygiene

Each SKILL.md follows the 5-layer authoring pattern carried over from
`batch_psp_switchbacks_magnetic`, which is the v0.2 four-layer model plus an
explicit Trigger layer (§1). No SKILL.md text names a specific MCP, plugin,
or harness command in §2–§3; adapter examples (if any) are confined to §4.

## Research-generation seeds

Affordances are machine-readable in
`manifest.json[skills[].research_generation_affordances]` and prose-rendered
in each `SKILL.md` §5. Stage-D walkers should pick up gaps/tensions/
hypotheses/minimal-experiments from there.

## Provenance

- Generated: 2026-05-18 by HelioSI paper-to-skill factory v0.2
- Source inventories used:
  - `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  - `sioulas-reproduction/results/arxiv_papers/extended_search.md`
  - `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md`
  - `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md`
