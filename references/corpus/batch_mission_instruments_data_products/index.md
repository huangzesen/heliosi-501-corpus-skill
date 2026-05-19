# Batch: mission_instruments_data_products

Generated **2026-05-18** by the HelioSI paper-to-skill factory.

This batch compiles **12 mission / instrument / data-product / coordinate-
system / calibration papers** into Anthropic-style paper-skills for the
HelioSI runtime. Unlike the science-result batches (turbulence, switchbacks,
PFSS), the entries here form the **contract layer**: any downstream science
paper-skill that touches PSP or Solar Orbiter data must compose with one or
more of these contracts to know **which sensor, level, cadence, frame, and
caveats** apply.

The framing is identical to the rest of the corpus:

| Paper element | Agent-native form |
|---|---|
| Claims | → **Verifiable tasks** |
| Methods / equations | → **Executable workflows** |
| Data / instruments / code | → **MCP / tool contracts** |
| Caveats / failure modes | → **Skill memory** (loaded each invocation) |
| Figures / results | → **Benchmark artifacts** |

The **general-purpose harness remains the runtime**; this batch is a
mission-instrumentation slice of the heliophysics domain instantiation.
Named MCPs (`cdaweb-mcp`, `soar-mcp`, `pfsspy-mcp`) are referenced
abstractly — the harness's `Read`, `Bash`, `WebFetch`, `cdflib`,
`pyspedas`, `spiceypy` stack is the only guaranteed surface.

## Parker Solar Probe — mission, ephemeris, in-situ + remote sensing

| # | Slug | Year | Role | Inventory? |
|---|---|---|---|---|
| 1 | [fox-2016-psp-mission-design-orbit-encounters](./fox-2016-psp-mission-design-orbit-encounters/SKILL.md) | 2016 | PSP mission / orbit ladder / encounter taxonomy / SPICE ephemeris | not-in-local-inventory |
| 2 | [bale-2016-fields-instrument-suite-psp](./bale-2016-fields-instrument-suite-psp/SKILL.md) | 2016 | PSP/FIELDS sensor inventory + contract | not-in-local-inventory |
| 3 | [kasper-2016-sweap-investigation-psp](./kasper-2016-sweap-investigation-psp/SKILL.md) | 2016 | PSP/SWEAP SPC + SPAN-Ai/Ae/B sensor inventory + contract | not-in-local-inventory |
| 4 | [mccomas-2016-isois-energetic-particle-investigation-psp](./mccomas-2016-isois-energetic-particle-investigation-psp/SKILL.md) | 2016 | PSP/ISʘIS EPI-Lo + EPI-Hi (LET/HET) sensor inventory + contract | not-in-local-inventory |
| 5 | [vourlidas-2016-wispr-imaging-instrument-psp](./vourlidas-2016-wispr-imaging-instrument-psp/SKILL.md) | 2016 | PSP/WISPR Inner + Outer heliospheric imagers + contract | not-in-local-inventory |
| 6 | [pulupa-2020-fields-merged-scm-fluxgate-product](./pulupa-2020-fields-merged-scm-fluxgate-product/SKILL.md) | 2020 | PSP/FIELDS merged SCaM L3 broadband-B product | in-inventory (arXiv 2001.04587) |
| 7 | [verniero-2020-psp-span-i-vdf-data-product](./verniero-2020-psp-span-i-vdf-data-product/SKILL.md) | 2020 | PSP/SWEAP SPAN-Ai 3D VDF → linear-Vlasov stability workflow | in-inventory (arXiv 2004.03009; DOI confirmed) |

## Solar Orbiter — mission and instrument suite

| # | Slug | Year | Role | Inventory? |
|---|---|---|---|---|
| 8 | [muller-2020-solar-orbiter-mission-overview](./muller-2020-solar-orbiter-mission-overview/SKILL.md) | 2020 | SO mission / orbit ladder / RSW gating / SOAR | not-in-local-inventory |
| 9 | [horbury-2020-solo-mag-vector-magnetometer](./horbury-2020-solo-mag-vector-magnetometer/SKILL.md) | 2020 | SO/MAG IBS + OBS sensor inventory + contract | not-in-local-inventory |
| 10 | [owen-2020-solo-swa-plasma-suite](./owen-2020-solo-swa-plasma-suite/SKILL.md) | 2020 | SO/SWA PAS + EAS + HIS sensor inventory + contract | not-in-local-inventory |
| 11 | [sinjan-2026-solo-phi-hrt-stray-light-calibration](./sinjan-2026-solo-phi-hrt-stray-light-calibration/SKILL.md) | 2026 | SO/PHI-HRT stray-light correction recipe vs SDO/HMI (2023 conjunction) | in-inventory (arXiv 2603.18744) |
| 12 | [damicis-2025-solo-swa-alfvenic-streams-validation](./damicis-2025-solo-swa-alfvenic-streams-validation/SKILL.md) | 2025 | SO/SWA full-suite end-to-end Alfvénic-stream classification + source backmap (Sep 2022) | in-inventory (arXiv 2512.20098) |

## Local-inventory grounding vs project-knowledge anchors

- **5 / 12 papers (#6, #7, #11, #12, partially #5)** have a primary-source
  anchor inside `sioulas-reproduction/results/arxiv_papers/` and therefore
  carry a concrete `source_record` and at least one resolvable
  `links.arxiv_url`.
- **7 / 12 papers (#1–5, #8–10)** are famous mission / instrument
  description papers that are NOT in the local inventory. They are
  compiled from project knowledge with **all bibliographic fields marked
  `TODO_verify_with_full_text`** and `source_record` set to a
  `project-knowledge:` placeholder. Each carries an explicit
  `claim_boundary` and a sole-claim discipline against overclaiming.
- Per spec §8 ("citation-only-from-source rule"), these `TODO_verify`
  entries cannot promote past **stub** until a reviewer confirms the
  primary source.

## Skill-graph wiring (intra-batch + cross-batch)

Cross-references created by this batch:

- All science contracts upstream of `[[fox-2016-psp-mission-design-orbit-
  encounters]]` (encounter ID, SPICE state vector).
- PSP plasma diagnostics composing `[[bale-2016-fields-instrument-suite-
  psp]]` ↔ `[[kasper-2016-sweap-investigation-psp]]`.
- PSP broadband-B turbulence composing `[[bale-2016-fields-instrument-
  suite-psp]]` ↔ `[[pulupa-2020-fields-merged-scm-fluxgate-product]]`.
- PSP ion microphysics composing `[[kasper-2016-sweap-investigation-psp]]`
  ↔ `[[verniero-2020-psp-span-i-vdf-data-product]]`.
- SO plasma diagnostics composing `[[horbury-2020-solo-mag-vector-
  magnetometer]]` ↔ `[[owen-2020-solo-swa-plasma-suite]]` ↔
  `[[damicis-2025-solo-swa-alfvenic-streams-validation]]`.
- SO calibration: `[[sinjan-2026-solo-phi-hrt-stray-light-calibration]]`
  pairs with `[[muller-2020-solar-orbiter-mission-overview]]` for RSW
  context.
- Cross-batch links: `[[bale-2021-solar-source-switchbacks-magnetic-
  funnels]]` (existing `batch_psp_switchbacks_magnetic`) and
  `[[dakeyo-2026-source-alignment-psp-solo]]` (existing
  `pilot_2026_and_runtime`).
- Unresolved `[[raouafi-2023-psp-four-years-discoveries-review]]`,
  `[[paper-hmi-vector-magnetogram-reference]]`, and
  `[[stverak-2026-solo-swa-eas-spacecraft-electron-contamination]]`
  marked for future entries.

## Weak entries needing full-text verification

| Slug | Items flagged TODO verify |
|---|---|
| fox-2016-psp-mission-design-orbit-encounters | full author list, DOI, exact perihelion ladder, encounter-threshold definition |
| bale-2016-fields-instrument-suite-psp | full author list, DOI, exact MAG burst cadence, CDF variable names |
| kasper-2016-sweap-investigation-psp | full author list, DOI, exact energy ranges, exact SPC encounter cadence, SPC↔SPAN-Ai cross-calibration tolerance |
| mccomas-2016-isois-energetic-particle-investigation-psp | full author list, DOI, exact energy ranges per telescope, L3 product names, concrete validation event |
| vourlidas-2016-wispr-imaging-instrument-psp | full author list, DOI, exact elongation ranges, detector chip, exact L1/L2/L3 naming, concrete CME validation event |
| pulupa-2020-fields-merged-scm-fluxgate-product | full author list, DOI, journal, exact crossover band, exact SCaM L3 product name, validation interval |
| verniero-2020-psp-span-i-vdf-data-product | exact solver used, figure number for dispersion comparison, refined tolerance |
| muller-2020-solar-orbiter-mission-overview | full author list, DOI, exact RSW schedule, exact phase-transition dates, exact validation r/lat |
| horbury-2020-solo-mag-vector-magnetometer | full author list, DOI, exact burst cadence, validation interval |
| owen-2020-solo-swa-plasma-suite | full author list, DOI, exact EAS contamination threshold, validation interval |
| sinjan-2026-solo-phi-hrt-stray-light-calibration | DOI, journal, exact correction term, figure indices, exact agreement tolerance |
| damicis-2025-solo-swa-alfvenic-streams-validation | DOI, journal, complete author list, figure table reference |

All 12 entries default to **`quality: stub` → `paper-grounded-pending-full-text`**;
none have been promoted to `method-ready` because at least one TODO_verify
item blocks each (per spec §7 promotion gates).

## Source inventories consulted

- `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
- `sioulas-reproduction/results/arxiv_papers/extended_search.md`
- `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md`
- `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md`
- `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md`
- `sioulas-reproduction/results/arxiv_papers/theme_solar_orbiter.json`
- `sioulas-reproduction/results/arxiv_papers/theme_psp_data.json`

## Cross-batch deduplication

Checked all existing batches (`batch_pfss_source_mapping`,
`batch_psp_switchbacks_magnetic`, `batch_turbulence_heating_apj`,
`pilot_2026_and_runtime`, `pilot_turbulence`) — **no duplicates**: those
batches contain science-result papers, not instrument descriptions.

## Notes

- Each `metadata.yaml` follows the established lightweight batch
  convention (slug + title + authors + year + journal + doi + arxiv +
  theme + quality_level + executable_status + required_data + methods +
  validation_targets + source_inventory + provenance). It is intentionally
  *not* the canonical `paper_skill_schema.json` frontmatter inside
  `SKILL.md` — to stay consistent with sibling batches
  (`batch_psp_switchbacks_magnetic`, `pilot_2026_and_runtime`). A future
  promotion pass will lift each to schema-conformant frontmatter when
  primary-source verification is complete.
- No file in `.library/custom/` or in any existing batch was modified.
- This batch deliberately concentrates **mission / instrument / data-
  product** contracts so that later science batches can be wired against
  stable upstream nodes.
