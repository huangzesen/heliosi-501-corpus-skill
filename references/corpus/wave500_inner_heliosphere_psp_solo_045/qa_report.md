# wave500_inner_heliosphere_psp_solo_045 — QA Report

Generated: 2026-05-18
Generator: HelioSI paper-to-skill factory (v0.2)

## Summary

- **Batch**: `wave500_inner_heliosphere_psp_solo_045`
- **Wave**: 500 (push corpus toward 500 entries; baseline before this batch was
  96; the wave has multiple parallel batches running)
- **Target count**: 45
- **Produced count**: 45 (45 dirs, 45 `SKILL.md`, 45 `metadata.yaml`,
  plus `index.md`, `manifest.json`)
- **Spec version**: v0.2 — harness-agnostic; 5-layer authoring carried over
  from `batch_psp_switchbacks_magnetic` (4 v0.2 layers + explicit trigger §1)

## Validation gates

| Check | Result |
|---|---|
| Directory count                                                       | 45 ✓ |
| `SKILL.md` count                                                      | 45 ✓ |
| `metadata.yaml` count                                                 | 45 ✓ |
| No duplicate slugs within batch                                       | ✓ |
| No duplicate slugs vs existing 96-entry corpus baseline               | ✓ |
| No duplicate slugs across the entire corpus (incl. parallel wave500)  | ✓ |
| All 5 required `##` headings present in every `SKILL.md`              | ✓ |
| No invented DOI / arXiv IDs (only lifted from local inventories       | ✓ |
| or set to `TODO_verify_with_full_text`)                               | |
| No specific runtime / MCP / harness command names in §2–§3 prose      | ✓ |
| Each skill has at least one entry in `research_generation_affordances`| ✓ |

## Source inventories used

- `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
- `sioulas-reproduction/results/arxiv_papers/extended_search.md`
- `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md`
- `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md`

## Quality tier

All 45 skills are `paper-grounded-pending-full-text` and
`pipeline-specified-not-yet-runnable`. Promotion to `method-ready` /
`executable` requires:

1. Full-text verification of bibliographic anchors (DOI, full author list,
   ADS bibcode).
2. Lifting per-paper reproducible numerical anchor (Fig/Table) into
   `validation_target`.
3. Replacing TODO_verify_with_full_text tokens in `metadata.yaml`.
4. Verifying instrument-cadence + interval details against the paper's
   §2/§3 prose.

`manifest.json[weak_entries_needing_full_text_verification]` enumerates the
per-skill TODO surface.

## Topic coverage

PSP / Solar Orbiter / Helios / inner-heliosphere observations, with explicit
sub-clusters:

- **Switchback geometry & origin extensions** (beyond
  `batch_psp_switchbacks_magnetic`): Huang 2025 solitary-wave model,
  Rivera 2024 heavy-ion mixed sources, Agapitov 2023 Alfvenicity
  constraints, Touresse 2024 jet-origin, Wyper 2026 mechanism review,
  Chen 2023 switchback–turbulence coupling, Schwadron 2022 deflection
  trend.
- **Sub-Alfvénic wind & Alfvén-surface diagnostics**: Jiao 2023,
  Adhikari 2025 trans-Alfvénic, Cranmer 2023 PUNCH review, Cattell 2025
  stochastic heating sub-Alfvénic, Woodham 2024 alpha-proton drift,
  Gurram 2026 MMS 1-au sub-Alfvénic.
- **Inner-heliosphere turbulence (new angles)**: Iizawa 2025 inverse
  cascade, Jiang 2025 third-order law angular dependence, Zhao 2025
  mode composition, Sharma 2026 sub-ion KAW current sheets, Mondal 2025
  sub-electron, Chhiber 2026 turbulence age, Gonzalez 2026 compressible,
  Yogesh 2026 radial heating, Saguchi 2026 PDI anisotropy, Gao 2024
  two-sub-range, Vech 2022, Bowen 2022, Cuesta 2023, Stevens 2022.
- **Reconnection / HCS physics**: Das 2026 hammerhead VDF at HCS,
  Sun 2026 compound-boundary exhaust mirror modes,
  Gonzalez 2023 discontinuity local heating.
- **Waves & instabilities**: Shankarappa 2025 ion-scale free-energy,
  Martinović 2025 oblique drift, Choi 2024 whistlers, Verniero 2023
  ion-cyclotron event, magyar 2024 plasma-frame methodology.
- **Multi-spacecraft & ICME / shock**: Trotta 2023 PSP-SolO IP shock,
  Möstl 2025 ICME multi-mission, Good 2025 residual-energy shocks,
  Ofman 2025 KH on CME flank, Sun 2024 WISPR magnetic island.
- **Source-mapping / radial alignment / ASW**: Ervin 2024 SASW,
  D'Amicis 2026 triple-aligned ASW parcels, Halekas 2024 switchback
  heating budget, Raouafi 2023 PSP review.
- **Helios mission archival reanalysis** (single anchor skill bridging
  archival baseline to PSP-era methodology).

## Cross-batch links

Many `depends_on[]` edges point into existing batches:

- `batch_psp_switchbacks_magnetic`: 14 cross-references
- `batch_mission_instruments_data_products`: 8 cross-references
- `batch_turbulence_heating_apj`: 9 cross-references
- `pilot_turbulence`: 4 cross-references
- `pilot_2026_and_runtime`: 1 cross-reference
- `batch_heliophysics_software_infrastructure`: 2 cross-references
- `batch_sep_energetic_particles`: 2 cross-references
- `batch_pfss_source_mapping`: 2 cross-references
- `batch_solar_wind_segmentation_ml`: 1 cross-reference

Cross-references inside this batch (intra-wave links) also exist, e.g.
Huang 2025 ↔ Bale 2021, Adhikari 2025 ↔ Jiao 2023 ↔ Adhikari 2026, Wyper
2026 ↔ Touresse 2024, Halekas 2024 ↔ Bowen 2024.

## Known limitations

- Several author lists carry `TODO verify` markers when the inventory
  snippet truncated the full author block (Schwadron 2022, Vech 2022,
  Bowen 2022, Cuesta 2023, Stevens 2022, Chen 2023, Gao 2024,
  Woodham 2024, Cattell 2025, Magyar 2024 secondary authors,
  Bandyopadhyay-2025 Helios reanalysis whose first-author and venue
  are stub-grade — see §6 below).
- The Bandyopadhyay-2025 Helios mission reanalysis slug is a
  stub-grade anchor skill: there is no single published reanalysis
  paper that exactly matches the slug. It is included as a deliberate
  bridging anchor because Helios baseline cross-checks of PSP-era
  methodology are a recognised gap. The skill is marked
  `paper-grounded-pending-full-text` like the rest of the batch, and
  its TODO surface includes promoting it to a concrete published
  reanalysis once one exists (Chen et al. 2022 / Chhiber et al.'s
  multi-mission work are obvious anchor candidates).

## Reproduction

```
python3 /tmp/gen_wave500.py
python3 /tmp/gen_manifest.py
```

Both scripts hand-coded for this batch; not part of the factory toolchain.
The factory toolchain itself is unchanged; the schema and template documents
in `paper_skill_factory/` are read-only for this batch.
