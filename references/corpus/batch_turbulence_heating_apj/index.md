# Batch — APJ/A&A Turbulence, Heating, Intermittency Expansion

- **Generated**: 2026-05-18
- **Theme**: solar-wind-turbulence × coronal-heating × waves-instabilities (APJ / ApJL / ApJS / A&A / Nature Astronomy)
- **Status**: pilot scaffold — claims grounded in the curated inventory; numerical specifics flagged `TODO verify in full paper` per skill.
- **Source inventory**:
  - `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §§1.3, 1.6, 1.7, 1.8, 1.9, 1.10, 1.12, 1.14, 1.15, 1.16
- **Parent skill**: `.library/custom/heliophysics-skills/SKILL.md` (themes: turbulence, coronal_heating, waves_instabilities)
- **Prior batch**: `sioulas-reproduction/results/paper_skill_corpus/pilot_turbulence/` (re-used cross-references via `[[slug]]` only — pilot files **not** modified)

## Skills

| # | Slug | Year | Lead | Venue | DOI / arXiv | Core claim (one line) | Quality | Status |
|---|------|------|------|-------|-------------|------------------------|---------|--------|
| 1 | `zhao-2022-3d-anisotropy-kinetic-scales-psp` | 2022 | L.-L. Zhao | ApJL 924, L21 | DOI 10.3847/2041-8213/ac4415 | PSP kinetic-scale magnetic fluctuations show direction-dependent (3D) anisotropy in a local mean-field frame. | pilot | scaffold |
| 2 | `bowen-2023-landau-damping-proton-electron-heating` | 2023 | T. A. Bowen | ApJ submitted (TODO verify) | arXiv 2301.09713 | Linear-Vlasov + quasilinear Landau-damping cascade model constrained by PSP spectra partitions Q_p / Q_e during PSP E1–E2. | pilot | scaffold |
| 3 | `pecora-2022-coherent-structures-proton-electron-heating` | 2022 | F. Pecora | MNRAS / ApJ (TODO verify) | arXiv 2206.10671 | Conditional averaging on PVI-flagged coherent structures in PSP E1 shows preferential proton over electron heating. | pilot | scaffold |
| 4 | `bowen-2024-extended-cyclotron-resonant-heating` | 2024 | T. A. Bowen | ApJ (TODO verify) | arXiv 2406.10446 | Left-handed circularly polarised ICWs at the spectral break drive extended cyclotron-resonant heating in PSP fast streams over ~15–55 R☉. | pilot | scaffold |
| 5 | `bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance` | 2024 | T. A. Bowen | Nature Astronomy (PMID 38659611) | DOI TODO verify | Ion-scale PSP polarisation signatures + resonance overlap imply cyclotron resonance mediates collisionless turbulent dissipation. | pilot | scaffold |
| 6 | `cuesta-2022-compressible-turbulence-psp-themis-maven` | 2022 | M. M. Cuesta | ApJ | DOI 10.3847/1538-4357/ac0af5 | Compressibility / density-fluctuation spectra of solar-wind turbulence evolve systematically from 0.17 au (PSP) to ~1.5 au (MAVEN). | pilot | scaffold |
| 7 | `telloni-2025-psp-solo-radial-alignment-2022-december` | 2025 | D. Telloni | ApJS | DOI 10.3847/1538-4365/add011 | 2022-December PSP–SO radial alignment recovers structure-function spectral evolution and cross-helicity radial trend in approximately the same plasma parcel. | pilot | scaffold |
| 8 | `carbone-2021-electron-density-turbulence-ion-cyclotron-waves` | 2021 | F. Carbone | A&A 656, A16 | DOI 10.1051/0004-6361/202140931 · arXiv 2105.07790 | SO RPW spacecraft-potential-derived n_e at ~0.5 au yields density turbulence statistics and wavelet-identified ion-cyclotron-wave events. | pilot | scaffold |
| 9 | `chen-2022-magnetic-field-spectral-evolution-inner-heliosphere` | 2022 | C. H. K. Chen | TODO verify | arXiv 2209.02451 | Combined PSP+Helios+Wind PSDs show inertial-range slope steepening from ~-3/2 near the Sun to ~-5/3 by ~0.6 au. | pilot | scaffold |
| 10 | `martinovic-2024-slow-wind-imbalanced-alfven-wave-heating` | 2024 | M. M. Martinović | TODO verify | arXiv 2403.17352 | Reflection-driven imbalanced AW cascade model fitted to PSP+SO slow-wind intervals matches empirical Q_p from 0.06 to 1 au. | pilot | scaffold |

## Topical grouping (compiler view)

- **Kinetic-scale anisotropy & spectral break**: skills 1, 4, 5 (paired with [[zhao-2022-3d-anisotropy-kinetic-scales-psp]] / `bowen-2024-*`).
- **Heating channels**: Landau (2), coherent-structure (3), cyclotron (4, 5), AW-cascade slow-wind (10). The corpus now hosts four distinct dissipation-channel paper-skills — they share inputs (cascade-rate normalisation from [[bandyopadhyay-2020-energy-transfer-psp]]) but expose different `validation_target`s.
- **Radial evolution / conjunctions**: skills 6 (statistical, PSP/THEMIS/MAVEN), 7 (2022-12 Lagrangian PSP/SO alignment), 9 (PSP/Helios/Wind pooled slope). These compose with [[telloni-2021-psp-solo-radial-alignment-turbulence]] from `pilot_turbulence/`.
- **Density-channel turbulence at ~0.5 au**: skill 8 (SO RPW n_e + wavelet ICW); complements compressibility skill 6 with an SO-specific instrument contract.

## Cross-cutting infrastructure shared with `pilot_turbulence/`

Re-used by reference — these building blocks are candidate Stage-B synthesis skills, **not** duplicated as new paper-skill files in this batch:

- **PSP / SO data MCP contract** — PSP FIELDS MAG L2, SWEAP (SPC + SPAN-I + SPAN-e) L3; SO MAG L2, SWA/PAS L2/L3, RPW L2/L3 (new in this batch).
- **Helios & Wind data MCP contract** — Helios reprocessed MAG L2 (new), Wind MFI / 3DP / SWE L2 (new).
- **THEMIS & MAVEN data MCP contract** — THEMIS FGM / ESA L2 (new), MAVEN MAG / SWIA L2 with bow-shock-exclusion logic (new).
- **Elsässer-field computation** (re-used from pilot).
- **Cross-helicity / residual energy σ_c, σ_R** (re-used from pilot).
- **PVI** (re-used from pilot; explicit downstream consumer here is skill 3).
- **Trace PSD (Welch / multitaper)** (re-used from pilot).
- **Wavelet magnetic-helicity σ_m(f, t) and ellipticity ε(f)** (new; consumed by skills 4, 5, 8).
- **Cyclotron-resonance overlap integral** (new; consumed by skills 4, 5).
- **Quasilinear cascade-transport equation** (new; consumed by skill 2 and indirectly by 4, 5).
- **Reflection-driven AW cascade model evaluator** (new; consumed by skill 10).
- **Linear Vlasov solver (PLUME / NHDS / LEOPARD-class)** (new; consumed by skill 2, indirectly by 5).
- **Ballistic plasma-parcel mapping** (new; consumed by skill 7).

These are proposed contracts. Named MCPs do **not** exist as runtime — the general-purpose harness (Read, Bash, WebFetch + cdflib / pyspedas / external solver invocations) is the only guaranteed surface.

## Weak entries flagged for full-text verification

| Slug | Issue | Recommended action |
|------|-------|--------------------|
| `bowen-2023-landau-damping-proton-electron-heating` | Inventory lists "ApJ / submitted (arXiv 2301.09713)"; publication venue and DOI absent. | Pull the arXiv abstract page and journal record; freeze the Vlasov-solver name actually used. |
| `pecora-2022-coherent-structures-proton-electron-heating` | Inventory ambiguous — "MNRAS / ApJ 2022"; no DOI. | Confirm venue, DOI, and the exact PVI threshold + averaging window in the paper. |
| `bowen-2024-extended-cyclotron-resonant-heating` | "ApJ (arXiv preprint)" — venue and DOI not in inventory. | Confirm published venue and the closed-form Q_p,ICW formula. |
| `bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance` | Nature Astronomy via PMID 38659611; DOI not in inventory. | Resolve the Nature Astronomy DOI; freeze the LH/RH polarisation convention used (sign-sensitive). |
| `cuesta-2022-compressible-turbulence-psp-themis-maven` | No arXiv ID in inventory; compressibility-metric definition not specified. | Confirm arXiv ID, exact C_n definition, and MAVEN bow-shock-exclusion criterion. |
| `telloni-2025-psp-solo-radial-alignment-2022-december` | Author list truncated ("D. Telloni and collaborators"); no arXiv ID. | Resolve full author list; pin the conjunction time window from the paper. |
| `carbone-2021-electron-density-turbulence-ion-cyclotron-waves` | Encounter list and RPW V_sc → n_e calibration version not in inventory. | Pull paper to record encounter selection and calibration panel / bias setting. |
| `chen-2022-magnetic-field-spectral-evolution-inner-heliosphere` | arXiv-only in inventory (no venue / DOI); single-author truncation. | Resolve published-version reference and stream-class conditioning. |
| `martinovic-2024-slow-wind-imbalanced-alfven-wave-heating` | "M. M. Martinović and collaborators" — incomplete attribution; venue not in inventory. | Resolve full author list, venue, and the exact reflection-driven AW model variant. |
| `zhao-2022-3d-anisotropy-kinetic-scales-psp` | No arXiv ID in inventory (DOI + ADS only); per-axis exponents not specified. | Cross-check arXiv against ADS 2022ApJ...924L..21Z; freeze per-axis numerical slopes. |

The first nine entries are venue / convention / formula-level TODOs that require the full-text PDF; the Zhao 2022 entry needs only an arXiv cross-check.

## Roll-up reproducibility targets

A HelioSI harness consuming this batch + the pilot batch should be able to roll the eighteen skill outputs into:

- A **heating-channel partition table** — Q_p / Q_e by Landau (skill 2), coherent-structure (3), cyclotron (4, 5), and AW-cascade slow-wind (10); per heliocentric-distance bin.
- An **inner-heliosphere magnetic-spectral evolution panel** — α_B(r) from skill 9 plus the 1/f outer-range mapping from [[huang-2023-psp-one-over-f-spectrum]] (pilot) and the ion-break mapping from skill 4.
- A **kinetic-range anisotropy table** — per-axis (α_∥, α_⊥, α_disp) from skill 1 vs heliocentric distance.
- A **compressibility radial-evolution panel** — skill 6 (PSP/THEMIS/MAVEN) + skill 8 (SO RPW at ~0.5 au).
- A **PSP–SO conjunction series** — [[telloni-2021-psp-solo-radial-alignment-turbulence]] (pilot) + skill 7 (2022-12).
- A **slow-wind heating-energetics sheet** — skill 10 Q_AW / Q_p_empirical conditioned on Alfvénicity from [[damicis-2021-alfvenic-nonalfvenic-psp]] (pilot).

## Compilation note (per factory spec §0)

Each SKILL.md is the *agent-native compiled form* of one paper, **not** a summary:

| Paper element | Compiled form per skill | Where it lives |
|---|---|---|
| Claims / results | "Scientific claim to reproduce" + acceptance criteria | §3 + §5 |
| Methods / equations | "Algorithm/workflow steps" | §4 |
| Data / instruments | "Required data" tool-contract table | §4 |
| Caveats / pitfalls | "Known pitfalls / failure modes" | §6 |
| Figures / numerical results | "Validation target" + check-artifact list | §5 |
| Corpus / citations | "Relation to HelioSI" sibling list + `[[slug]]` links | §8 |

The Claude Code harness is the **general-purpose runtime**; HelioSI is the **domain instantiation** of that runtime as a skill graph. This corpus is the compiled artifact; topic bundles (Stage B per spec §6) and the HelioSI graph (Stage C) consume these skills by `slug` reference — they do not re-inline content.
