# Batch: heliophysics software & data-infrastructure paper-skills

Generated 2026-05-18 by the HelioSI paper-to-skill factory (HelioSI paper-to-skill factory).

This batch compiles 12 **software-paper / software-package / data-archive**
entries into agent-native skills following the factory spec
(`sioulas-reproduction/results/paper_skill_factory/paper_to_skill_factory_spec.md`).
Unlike Stage-A science paper-skills, these compile *infrastructure* into
the skill graph: data clients, ecosystem maps, formulary libraries, and
archives that every downstream in-situ / coronal paper-skill ultimately
resolves through.

## Framing: infrastructure compiled into Anthropic-style Skills

The compilation table (spec §0) applies, with infrastructure-specific
bindings:

| Source element | Agent-native form |
|---|---|
| Package APIs / data products | → **MCP / tool contracts** (§4 in each SKILL.md) |
| Documented workflows | → **Executable workflows** (§3) |
| Maintainer-known pitfalls | → **Skill memory** (§6 failure_modes) |
| Test problems / smoke tests | → **Benchmark targets** (§5 validation_target) |
| Companion publications | → **Bibliographic anchor** (frontmatter `paper`) |
| Ecosystem contracts (e.g., sunpy affiliated-package) | → **Skill graph** (depends_on) |

Each entry's `source_type` is one of:

- `software-paper` — a paper that *describes* a software package
  (SunPy 2023, SpacePy 2022, Solar-MACH 2022, Bobra 2019, SunPy 2015,
  Stansby 2022 pfsspy test-problem companion).
- `software-package` — a package without a single canonical paper in
  local inventory (sunkit-magex, pySPEDAS, cdflib, sw-scanner, PlasmaPy,
  pfsspy itself — the pfsspy entry has *both* aspects).
- `data-archive` (sub-category of software-package) — CDAWeb / SPDF as
  service-level infrastructure with no software publication.

`source_record` for every skill points to a real path under
`.library/custom/heliophysics-skills/` or
`sioulas-reproduction/results/`. No citations are invented; weak fields
(DOI, exact figure IDs, full author lists) are flagged inline as
**TODO verify** and centralized in the manifest's `weak_entries_needing_full_text_verification`.

## Entries

| # | Slug | source_type | arXiv / Code | Quality tier | Role |
|---|---|---|---|---|---|
| 1 | [paper-sunpy-2023-interoperable-ecosystem](./paper-sunpy-2023-interoperable-ecosystem/SKILL.md) | software-paper | arXiv 2304.09794 / github.com/sunpy/sunpy | stub | SunPy ecosystem root (current) |
| 2 | [paper-sunpy-2015-python-solar-physics](./paper-sunpy-2015-python-solar-physics/SKILL.md) | software-paper | arXiv 1505.02563 / github.com/sunpy/sunpy | stub | SunPy ecosystem root (historical anchor) |
| 3 | [paper-stansby-2020-pfsspy-python-pfss](./paper-stansby-2020-pfsspy-python-pfss/SKILL.md) | software-package | arXiv 2201.07783 / github.com/sunpy/pfsspy | method-ready | PFSS Python (predecessor) |
| 4 | [paper-sunkit-magex-magnetic-field-extrapolation](./paper-sunkit-magex-magnetic-field-extrapolation/SKILL.md) | software-package | github.com/sunpy/sunkit-magex | method-ready | PFSS Python (successor) |
| 5 | [paper-spacepy-2022-twelve-years](./paper-spacepy-2022-twelve-years/SKILL.md) | software-paper | arXiv 2208.10447 / github.com/spacepy/spacepy | stub | Space-physics toolkit (radiation belt + coords) |
| 6 | [paper-pyspedas-multimission-data-access](./paper-pyspedas-multimission-data-access/SKILL.md) | software-package | github.com/spedas/pyspedas | method-ready | Multi-mission in-situ data loader |
| 7 | [paper-cdflib-cdf-reader](./paper-cdflib-cdf-reader/SKILL.md) | software-package | github.com/MAVENSDC/cdflib | method-ready | Pure-Python CDF reader (lightweight) |
| 8 | [paper-gieseler-2022-solar-mach-magnetic-connection](./paper-gieseler-2022-solar-mach-magnetic-connection/SKILL.md) | software-paper | arXiv 2210.00819 / github.com/sunpy/solar-mach | method-ready | Multi-spacecraft Parker-spiral connection |
| 9 | [paper-sioulas-sw-scanner-js-segmentation](./paper-sioulas-sw-scanner-js-segmentation/SKILL.md) | software-package | github.com/nicosioulas/sw-scanner | method-ready | JS-divergence scalogram segmentation |
| 10 | [paper-plasmapy-plasma-physics-python](./paper-plasmapy-plasma-physics-python/SKILL.md) | software-package | github.com/PlasmaPy/PlasmaPy | stub | Plasma formulary + particles |
| 11 | [paper-bobra-2019-python-heliophysics-overview](./paper-bobra-2019-python-heliophysics-overview/SKILL.md) | software-paper | arXiv 1901.00143 | stub | Python-in-heliophysics ecosystem map (2019) |
| 12 | [paper-cdaweb-heliophysics-archive](./paper-cdaweb-heliophysics-archive/SKILL.md) | software-package (data-archive) | cdaweb.gsfc.nasa.gov | method-ready | NASA SPDF data archive root |

## Skill-graph summary

Most heliophysics in-situ paper-skills will resolve through this batch:

```
[science paper-skill]
        │
        ├──► paper-cdaweb-heliophysics-archive   (root data access)
        │           │
        │           └──► paper-cdflib-cdf-reader   (CDF read)
        │
        ├──► paper-pyspedas-multimission-data-access   (mission loader)
        │
        ├──► paper-sw-scanner-js-segmentation         (segmentation, if needed)
        │
        ├──► paper-sunpy-2023-interoperable-ecosystem (solar imaging root)
        │           │
        │           ├──► paper-stansby-2020-pfsspy-python-pfss
        │           ├──► paper-sunkit-magex-magnetic-field-extrapolation
        │           └──► paper-gieseler-2022-solar-mach-magnetic-connection
        │
        └──► paper-spacepy-2022-twelve-years          (radiation belt / coords)
```

`paper-plasmapy-plasma-physics-python` and
`paper-bobra-2019-python-heliophysics-overview` are *standalone* in the
graph today (self-contained library; ecosystem map). The 2015 SunPy
skill is a *historical anchor* pointing forward to the 2023 successor.

## Compilation-table mapping per category

- **APIs and data sources → MCP/tool contracts.** Each SKILL.md §4
  enumerates instrument / level / cadence / archive / fetch hint per data
  product. Named MCPs (`mcp:cdaweb`, `mcp:jsoc`) are **not asserted** —
  the spec §9.6 forbids that. The fallback is always the general-purpose
  harness (Read, Bash, WebFetch + pip).
- **Common workflows → executable workflows.** Each SKILL.md §3 gives
  imperative step-by-step procedures with Python skeleton code where
  available. At `method-ready` tier the snippets compile and call out
  to the named package; at `executable` tier they run end-to-end on a
  cached input.
- **Pitfalls → skill memory.** Each §6 enumerates 4–6 community-known
  failure modes (units, epoch type, cadence harmonization, kernel
  staleness, etc.). These are the "skill memory" rows of the
  compilation table — they ride with the skill on every invocation.
- **Validation → smoke tests / benchmark targets.** Each §5 documents
  the validation target. At `method-ready`+, this is a concrete
  numerical or behavioral check (e.g., epoch round-trip, pfsspy
  dipole-test convergence, Solar-MACH footpoint within ±5°). Stub-tier
  skills explicitly read "Not benchmarked yet" per spec §7.

## Source inventories consulted

All entries derive from local files; no external citations were
fabricated. Primary sources:

- `.library/custom/heliophysics-skills/SKILL.md` (databases table,
  segmentation row, repository overview)
- `.library/custom/heliophysics-skills/sub-skills/github-repos.md`
  (canonical github list with installation guide)
- `.library/custom/heliophysics-skills/sub-skills/pfss-modeling.md`
  (pfsspy + sunkit-magex code patterns)
- `.library/custom/heliophysics-skills/reference/databases.md`
  (CDAWeb / SPDF / OMNI / PSP SOC / SOAR / VSO entries; cdflib usage
  pattern)
- `sioulas-reproduction/results/arxiv_papers/extended_search.md` §7
  (Python-heliophysics paper batch — SunPy 2015 / 2023, SpacePy 2022,
  Solar-MACH 2022, Bobra 2019; explicit note that no pySPEDAS dedicated
  paper surfaced)
- `sioulas-reproduction/results/github_repos/consolidated_repos.json`
  (canonical software-and-databases inventory)

## What is NOT in this batch

By design, this batch excludes:

- **Solver-class kinetic codes** (ALPS, PLUME, OSIRIS, Pegasus++) —
  those belong in a dedicated `batch_wave_kinetic_solvers` once their
  primary publications are anchored.
- **ML-tool wrappers** (FNO/SFNO, SEP-Prediction) — already covered as
  science papers in existing batches; the *library* PlasmaPy and
  *infrastructure* CDAWeb are the right level here.
- **Mission SOC frontends** (PSP SOC, SOAR, JSOC `drms`) — referenced
  inside individual skills but not promoted to standalone skills until
  a dedicated batch.

## Weak entries summary

See `manifest.json#weak_entries_needing_full_text_verification` for the
authoritative list. Common gaps:

- DOI / ADS bibcode for software-paper companions not in local inventory.
- Full author lists for community packages (large `et al.` lists).
- Exact reference-figure IDs in companion publications (need full text).
- Existence of any JOSS paper for cdflib / PlasmaPy / pySPEDAS / sunkit-magex.

## Promotion roadmap

Most entries are `stub` or `method-ready`. Promotion to `executable`
requires, for each:

1. A cached / synthetic input the skill can ingest.
2. A small `scripts/` artifact running the §3 workflow end-to-end.
3. A `metrics.json` output checked against §5.

A future Stage-B `heliosi-python-stack-bundle` hub should route across
these 12 skills by task type (load data → cdflib / pySPEDAS; compute
PFSS → sunkit-magex; visualize connection → Solar-MACH; segment →
sw-scanner; formulary → PlasmaPy; archive root → CDAWeb).
