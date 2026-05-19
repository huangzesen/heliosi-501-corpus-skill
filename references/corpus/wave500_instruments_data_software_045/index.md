# Wave 500 — Instruments / Data Products / Software / Archives (45)

Generated 2026-05-18 by the HelioSI paper-to-skill factory (HelioSI paper-to-skill factory).

This wave adds **45 harness-agnostic paper-skills** for heliophysics **infrastructure**: instruments, data products, software packages, archives, and open-science services. It complements the existing `batch_mission_instruments_data_products/` and `batch_heliophysics_software_infrastructure/` batches (12+12=24 entries) and brings the corpus from **96 → 141** objects.

Spec version: **v0.2** (harness-agnostic, four-layer). Every skill carries `harness_agnostic: true`, the four-layer `layers:` block, and structured `research_generation_affordances[]` where applicable.

## Framing — infrastructure compiled into v0.2 paper-skills

| Source element                         | Agent-native form (§ of SKILL.md)                    |
|---|---|
| Instrument / data product specification | abstract tool contract (§4)                          |
| Documented prep / calibration workflow  | executable protocol (§3, runtime-neutral)            |
| Maintainer / instrument-team pitfalls   | skill memory (§6 failure_modes)                      |
| Smoke tests / cross-mission consistency | benchmark targets (§5 validation_target, executable+)|
| Companion publications                  | bibliographic anchor (paper frontmatter)              |
| Cross-instrument dependencies           | skill graph (`depends_on`, `[[slug]]` refs)           |

`source_type` taxonomy:

- `paper` — peer-reviewed publication (instrument, data-product, or method paper)
- `software-paper` — a paper that *describes* a software package
- `software-package` — a package or archive without a single canonical paper in local inventory (citation TODOs flagged in `weak_entries`)

## Sections

### Instruments (12)

| # | Slug | Source type | Citation / code | Quality |
|---|---|---|---|---|
| 1 | [paper-lepping-1995-wind-mfi-magnetometer](./paper-lepping-1995-wind-mfi-magnetometer/SKILL.md) | paper | — | stub |
| 2 | [paper-ogilvie-1995-wind-swe-faraday-cup](./paper-ogilvie-1995-wind-swe-faraday-cup/SKILL.md) | paper | — | stub |
| 3 | [paper-lin-1995-wind-3dp-plasma-energetic-electrons](./paper-lin-1995-wind-3dp-plasma-energetic-electrons/SKILL.md) | paper | — | stub |
| 4 | [paper-smith-1998-ace-mag-vector-helium-magnetometer](./paper-smith-1998-ace-mag-vector-helium-magnetometer/SKILL.md) | paper | — | stub |
| 5 | [paper-mccomas-1998-ace-swepam-solar-wind-electron-proton-alpha](./paper-mccomas-1998-ace-swepam-solar-wind-electron-proton-alpha/SKILL.md) | paper | — | stub |
| 6 | [paper-gloeckler-1998-ace-swics-composition-spectrometer](./paper-gloeckler-1998-ace-swics-composition-spectrometer/SKILL.md) | paper | — | stub |
| 7 | [paper-delaboudiniere-1995-soho-eit-extreme-uv-telescope](./paper-delaboudiniere-1995-soho-eit-extreme-uv-telescope/SKILL.md) | paper | — | stub |
| 8 | [paper-brueckner-1995-soho-lasco-coronagraph-suite](./paper-brueckner-1995-soho-lasco-coronagraph-suite/SKILL.md) | paper | https://cdaw.gsfc.nasa.gov/CME_list/ | stub |
| 9 | [paper-scherrer-1995-soho-mdi-michelson-doppler-imager](./paper-scherrer-1995-soho-mdi-michelson-doppler-imager/SKILL.md) | paper | — | stub |
| 10 | [paper-lemen-2012-sdo-aia-atmospheric-imaging-assembly](./paper-lemen-2012-sdo-aia-atmospheric-imaging-assembly/SKILL.md) | paper | 10.1007/s11207-011-9776-8 | stub |
| 11 | [paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager](./paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager/SKILL.md) | paper | 10.1007/s11207-011-9834-2 | stub |
| 12 | [paper-howard-2008-stereo-secchi-imaging-suite](./paper-howard-2008-stereo-secchi-imaging-suite/SKILL.md) | paper | 10.1007/s11214-008-9341-4 | stub |

### Data products (8)

| # | Slug | Source type | Citation / code | Quality |
|---|---|---|---|---|
| 1 | [paper-king-2005-omni-1min-5min-solar-wind-dataset](./paper-king-2005-omni-1min-5min-solar-wind-dataset/SKILL.md) | paper | 10.1029/2004JA010649 | method-ready |
| 2 | [paper-franz-2002-heliospheric-coordinate-systems](./paper-franz-2002-heliospheric-coordinate-systems/SKILL.md) | paper | 10.1016/S0032-0633(01)00119-2 | method-ready |
| 3 | [paper-malaspina-2016-psp-fields-dfb-digital-fields-board](./paper-malaspina-2016-psp-fields-dfb-digital-fields-board/SKILL.md) | paper | 10.1002/2016JA022344 | method-ready |
| 4 | [paper-case-2020-psp-sweap-spc-faraday-cup-data-product](./paper-case-2020-psp-sweap-spc-faraday-cup-data-product/SKILL.md) | paper | 10.3847/1538-4365/ab5a7b | method-ready |
| 5 | [paper-rochus-2020-solar-orbiter-eui-imager](./paper-rochus-2020-solar-orbiter-eui-imager/SKILL.md) | paper | 10.1051/0004-6361/201936663 | stub |
| 6 | [paper-antonucci-2020-solar-orbiter-metis-coronagraph](./paper-antonucci-2020-solar-orbiter-metis-coronagraph/SKILL.md) | paper | 10.1051/0004-6361/201935338 | stub |
| 7 | [paper-maksimovic-2020-solar-orbiter-rpw-radio-plasma-waves](./paper-maksimovic-2020-solar-orbiter-rpw-radio-plasma-waves/SKILL.md) | paper | 10.1051/0004-6361/201936214 | stub |
| 8 | [paper-rodriguez-pacheco-2020-solar-orbiter-epd-energetic-particle-detector](./paper-rodriguez-pacheco-2020-solar-orbiter-epd-energetic-particle-detector/SKILL.md) | paper | 10.1051/0004-6361/201935287 | stub |

### Software packages / software-papers (17)

| # | Slug | Source type | Citation / code | Quality |
|---|---|---|---|---|
| 1 | [paper-astropy-2022-collaboration-community-package](./paper-astropy-2022-collaboration-community-package/SKILL.md) | software-paper | 10.3847/1538-4357/ac7c74 | method-ready |
| 2 | [paper-barnes-2020-aiapy-python-sdo-aia](./paper-barnes-2020-aiapy-python-sdo-aia/SKILL.md) | software-paper | 10.21105/joss.02801 | method-ready |
| 3 | [paper-glogowski-2019-drms-jsoc-data-client](./paper-glogowski-2019-drms-jsoc-data-client/SKILL.md) | software-paper | 10.21105/joss.01614 | method-ready |
| 4 | [paper-annex-2020-spiceypy-naif-spice-toolkit-python](./paper-annex-2020-spiceypy-naif-spice-toolkit-python/SKILL.md) | software-paper | 10.21105/joss.02050 | method-ready |
| 5 | [paper-stansby-2018-heliopy-python-heliospheric-data](./paper-stansby-2018-heliopy-python-heliospheric-data/SKILL.md) | software-paper | 10.21105/joss.01060 | method-ready |
| 6 | [paper-chiantipy-dere-1997-chianti-atomic-database-python](./paper-chiantipy-dere-1997-chianti-atomic-database-python/SKILL.md) | software-paper | https://github.com/chianti-atomic/ChiantiPy | stub |
| 7 | [paper-freeland-1998-solarsoft-ssw-idl-ecosystem](./paper-freeland-1998-solarsoft-ssw-idl-ecosystem/SKILL.md) | software-paper | https://www.lmsal.com/solarsoft/ | stub |
| 8 | [paper-toth-2012-swmf-bats-r-us-mhd-framework](./paper-toth-2012-swmf-bats-r-us-mhd-framework/SKILL.md) | software-paper | 10.1016/j.jcp.2011.02.006 | stub |
| 9 | [paper-pulkkinen-2013-kameleon-ccmc-output-reader](./paper-pulkkinen-2013-kameleon-ccmc-output-reader/SKILL.md) | software-package | 10.1002/swe.20098 | stub |
| 10 | [paper-hapi-2020-heliophysics-api-time-series](./paper-hapi-2020-heliophysics-api-time-series/SKILL.md) | software-paper | https://github.com/hapi-server/client-python | method-ready |
| 11 | [paper-thompson-2024-heliocloud-aws-shared-archive](./paper-thompson-2024-heliocloud-aws-shared-archive/SKILL.md) | software-paper | https://heliocloud.org/ | stub |
| 12 | [paper-burrell-2018-pyhc-python-heliophysics-community](./paper-burrell-2018-pyhc-python-heliophysics-community/SKILL.md) | software-paper | 10.1029/2018JA025877 | stub |
| 13 | [paper-sunkit-image-sunpy-affiliated](./paper-sunkit-image-sunpy-affiliated/SKILL.md) | software-package | https://github.com/sunpy/sunkit-image | stub |
| 14 | [paper-sunkit-instruments-sunpy-affiliated](./paper-sunkit-instruments-sunpy-affiliated/SKILL.md) | software-package | https://github.com/sunpy/sunkit-instruments | stub |
| 15 | [paper-sunraster-sunpy-affiliated-raster-spectra](./paper-sunraster-sunpy-affiliated-raster-spectra/SKILL.md) | software-package | https://github.com/sunpy/sunraster | stub |
| 16 | [paper-irispy-lmsal-sunpy-affiliated-iris-loader](./paper-irispy-lmsal-sunpy-affiliated-iris-loader/SKILL.md) | software-package | https://github.com/LM-SAL/irispy-lmsal | stub |
| 17 | [paper-pyflct-correlation-tracking-fishman](./paper-pyflct-correlation-tracking-fishman/SKILL.md) | software-package | https://cgem.ssl.berkeley.edu/cgi-bin/cgem/FLCT/home | stub |

### Archives / open-science infrastructure (8)

| # | Slug | Source type | Citation / code | Quality |
|---|---|---|---|---|
| 1 | [paper-soar-solar-orbiter-archive-esa](./paper-soar-solar-orbiter-archive-esa/SKILL.md) | software-package | https://soar.esac.esa.int/ | method-ready |
| 2 | [paper-psp-soc-science-operations-center-archive](./paper-psp-soc-science-operations-center-archive/SKILL.md) | software-package | https://fields.ssl.berkeley.edu/ | method-ready |
| 3 | [paper-jsoc-stanford-aia-hmi-archive](./paper-jsoc-stanford-aia-hmi-archive/SKILL.md) | software-package | http://jsoc.stanford.edu/ | method-ready |
| 4 | [paper-vso-virtual-solar-observatory](./paper-vso-virtual-solar-observatory/SKILL.md) | software-package | https://sdac.virtualsolar.org/cgi/search | stub |
| 5 | [paper-hek-heliophysics-event-knowledgebase](./paper-hek-heliophysics-event-knowledgebase/SKILL.md) | software-paper | 10.1007/s11207-010-9624-2 | stub |
| 6 | [paper-ccmc-iswa-integrated-space-weather-analysis](./paper-ccmc-iswa-integrated-space-weather-analysis/SKILL.md) | software-package | https://iswa.ccmc.gsfc.nasa.gov/ | stub |
| 7 | [paper-nso-gong-network-magnetograms](./paper-nso-gong-network-magnetograms/SKILL.md) | paper | 10.1126/science.272.5266.1284 | stub |
| 8 | [paper-noaa-swpc-real-time-space-weather](./paper-noaa-swpc-real-time-space-weather/SKILL.md) | software-package | https://www.swpc.noaa.gov/ | stub |

## Audit

- Skill count (target / actual): **45 / 45**
- Unique slugs in wave: 45
- Slugs colliding with existing corpus: **0** (verified pre-write against `corpus_manifest.json`).
- Each directory contains exactly: `SKILL.md` + `metadata.yaml`.
- Each SKILL.md has the nine §1–§9 H2 headings from spec §4, plus optional Notes / weak-entry block.
- `harness_agnostic: true` for every skill; §3/§4/§5 prose carries no runtime / MCP / harness command.

