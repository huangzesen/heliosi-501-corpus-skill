# Batch: PFSS / coronal magnetic extrapolation / source mapping

Generated 2026-05-18 by the HelioSI paper-to-skill factory
(`paper_skill_factory/paper_to_skill_factory_spec.md`). Revised
2026-05-18 to a **runtime-neutral** four-layer SKILL.md structure per
HelioSI project requirement: paper-skills must be harness-agnostic. LingTai
and Claude Code are *adapters*, not assumptions in the skill body.

## Framing — harness-agnostic, four-layer compilation

Every SKILL.md in this batch is organized as four explicit layers:

1. **Scientific invariant layer.** Paper claims (narrow form),
   methodological assumptions, data assumptions, failure modes
   (skill memory), figure / numerical targets, claim boundaries.
   This layer is stable across runtimes.
2. **Executable protocol layer.** A capability-typed procedure. Each
   step names *abstract capabilities* (e.g. `pfss.solve`,
   `magnetogram.fetch_synoptic_br`) — never a specific MCP / framework /
   API. Validation target sits here.
3. **Adapter / runtime notes (optional examples).** Concrete bindings
   that *one* runtime might use (e.g. `sunkit-magex` for `pfss.solve`;
   `sunpy.net.Fido` for fetches; FEniCSx for FEM). Examples only.
4. **Research-generation affordances.** What gaps, tensions, new
   hypotheses, and composable experiments this paper-skill enables
   when combined with siblings. This is the layer that lets the corpus
   *generate research direction*, not just record it.

LingTai's existing custom skills (`.library/custom/pfss-tracing/`,
`.library/custom/nspf-fem/`) appear in this batch only as *example
adapters* in Layer 3, never as Layer-1 or Layer-2 requirements. The
custom skills are NOT modified.

## Compilation mapping (unchanged)

| Paper element | Agent-native form (under the 4 layers) |
|---|---|
| Claims | → Layer 1 — narrow-form claim + claim_boundary |
| Methods / equations | → Layer 1 (assumptions) + Layer 2 (procedure) |
| Data / instruments | → Layer 1 (data assumptions) + Layer 2 (abstract capabilities) |
| Caveats | → Layer 1 — failure modes (skill memory) |
| Figures / results | → Layer 1 (figure / numerical targets) + Layer 2 (validation target) |
| Citations | → `depends_on` skill graph at the end |
| Generative implications | → Layer 4 — research-generation affordances |

## Skills in this batch

| # | Slug | arXiv | Year | Aspect | Validation target |
|---|---|---|---|---|---|
| 1 | [pfss-test-problems-solar-stellar-magnetic-fields](./pfss-test-problems-solar-stellar-magnetic-fields/SKILL.md) | 2201.07783 | 2022 | PFSS solver verification | Pass paper-defined L_2/L_inf on analytic test problems |
| 2 | [multi-constraint-pfss-extrapolation-model](./multi-constraint-pfss-extrapolation-model/SKILL.md) | 2603.20142 | 2026 | Optimization-augmented PFSS | Reduce stated residual vs baseline PFSS at chosen weights |
| 3 | [ai-farside-synchronic-coronal-field-extrapolation](./ai-farside-synchronic-coronal-field-extrapolation/SKILL.md) | 2010.07553 | 2020 | Synchronic Br via AI farside | Reproduce synchronic-vs-synoptic PFSS comparison |
| 4 | [comparison-coronal-extrapolation-cycle-24-hmi](./comparison-coronal-extrapolation-cycle-24-hmi/SKILL.md) | 1603.04385 | 2016 | PFSS vs CSSS family | HCS / open-flux ordering on Cycle 24 HMI |
| 5 | [wu-2026-nonspherical-coronal-magnetic-field-open-flux](./wu-2026-nonspherical-coronal-magnetic-field-open-flux/SKILL.md) | 2604.01028 | 2026 | NSPF / NSSS open-flux | 9.19 G·R²_sun at GONG CR 2282, R_init=2.5 (one independent reproduction matches to 1.1%) |
| 6 | [coronal-hole-loop-statistics-potential-field-modeling](./coronal-hole-loop-statistics-potential-field-modeling/SKILL.md) | 2601.11080 | 2026 | CH-interior topology statistics | Reproduce 702-CH (2010–2019) distributions |
| 7 | [flare-precursor-fine-scale-topology-extrapolation](./flare-precursor-fine-scale-topology-extrapolation/SKILL.md) | 2306.03226 | 2023 | Pre-flare fine-scale topology | Reproduce precursor `Q` / null time series for named event |
| 8 | [eclipse-white-light-benchmark-pfss-models](./eclipse-white-light-benchmark-pfss-models/SKILL.md) | 2408.16149 | 2024 | Eclipse benchmark of PFSS | Recover cycle-phase ordering of PFSS-vs-eclipse agreement |
| 9 | [dakeyo-2026-source-alignment-psp-solo-method-link](./dakeyo-2026-source-alignment-psp-solo-method-link/SKILL.md) | 2605.01511 | 2026 | **link** to canonical pilot-batch skill (source-mapping aspect) | see canonical |
| 10 | [ervin-2024-slow-alfvenic-source-regions-pfss-psp](./ervin-2024-slow-alfvenic-source-regions-pfss-psp/SKILL.md) | 2407.09684 | 2024 | SASW source-region mapping (PSP E4–E14) | Two-population SASW source split |

## Abstract capability surface used in this batch

The batch's Layer-2 protocols collectively name the following abstract
capabilities. None are bound to a specific MCP / API in the skill
bodies — runtimes provide their own bindings.

- `pfss.solve()`, `pfss.solve_baseline()`
- `csss.solve()`
- `fem.solve_laplace()`, `geometry.extract_isosurface()`,
  `geometry.smooth_spherical_harmonic()`,
  `mesh.build_deformed_shell()`
- `extrapolation.solve_nlfff()`, `vector_mag.preprocess_ff()`
- `optimization.minimize_objective()`
- `field.trace_lines()`, `field.seed_field_lines()`,
  `field.trace_to_photosphere()`, `field.expansion_factor()`,
  `field.integrate_open_flux()`, `field.project_to_pos()`,
  `field.diagnose_neutral_line()`, `field.compute_b_from_phi()`
- `topology.find_nulls()`, `topology.trace_separators()`,
  `topology.compute_q_map()`
- `mapping.ballistic_to_source_surface()`, `mapping.match_common_source()`
- `magnetogram.fetch_synoptic_br()`,
  `magnetogram.fetch_earthside_los()`,
  `magnetogram.fuse_synchronic()`
- `vector_mag.fetch_sharp()`, `vector_mag.fetch()`
- `imagery.fetch_aia193()`, `imagery.fetch_aia()`,
  `imagery.fetch_euv()`, `imagery.fetch_lasco_c2()`,
  `imagery.fetch_lasco()`, `imagery.trace_loops()`,
  `eclipse.fetch_image()`, `imagery.fetch_rhessi_goes()`
- `farside.infer_br()`
- `ch_catalog.iterate()`
- `in_situ.fetch_psp_mag()`, `in_situ.fetch_psp_sweap()`,
  `in_situ.fetch_psp_composition()`, `in_situ.fetch_sector()`
- `ephemeris.psp()`, `ephemeris.spacecraft()`
- `classification.label_sw_type()`,
  `classification.label_source_region()`
- `statistics.aggregate_histograms()`,
  `statistics.aggregate_populations()`
- `metrics.streamer_agreement()`, `numerics.error_norms()`
- `analytics.testcase_generate()`
- `filesystem.write_report()`

Any runtime can bind these — Python + sunpy stack, Julia, MATLAB,
agent harness with MCPs, or hand-rolled scripts. The bindings used
inside LingTai are documented in Layer 3 of each skill *as examples*
and may be ignored by other runtimes.

## Cross-batch link entry

Entry #9, `dakeyo-2026-source-alignment-psp-solo-method-link`, is a
**link entry**, not a duplicate paper-skill. The canonical paper-skill
for Dakeyo et al. 2026 lives at:

```
paper_skill_corpus/pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/
```

This batch registers the paper under its source-mapping aspect (and
contributes the source-mapping-specific Layer-1 slice + Layer-4
generative affordances) but does not duplicate the canonical content.

## Skill-graph summary

Edges declared by `depends_on` across this batch:

- `pfss-test-problems-solar-stellar-magnetic-fields` is depended on by
  `wu-...-open-flux`, `comparison-...-cycle-24-hmi`,
  `eclipse-white-light-benchmark-pfss-models`,
  `coronal-hole-loop-statistics-potential-field-modeling`,
  `multi-constraint-pfss-extrapolation-model`,
  `ai-farside-synchronic-coronal-field-extrapolation`,
  `ervin-2024-slow-alfvenic-source-regions-pfss-psp`,
  `dakeyo-2026-...-method-link` — every PFSS-consuming skill in this
  batch requires the solver to be verified first.
- `dakeyo-2026-source-alignment-psp-solo-method-link` cross-points to
  the canonical Dakeyo skill in `pilot_2026_and_runtime`.

## Weak entries needing full-text verification

| Skill | Items flagged TODO verify |
|---|---|
| pfss-test-problems-... | venue; exact list of test problems; numeric L_2/L_inf tolerances; reference figure / table |
| multi-constraint-pfss-... | first author + author list; venue; DOI; exact objective form `J`; weights; solver |
| ai-farside-synchronic-... | first author + author list; venue; DOI; AI architecture; training set; weights availability; agreement metric |
| comparison-...-cycle-24-hmi | first author + author list; venue; DOI; HCCSSS solver + parameters; CR range; reference figure |
| wu-2026-...-open-flux | full author list (Wu, He, Hou + others); venue; DOI; reference figure identifiers; whether PFCS layer is required for the paper's final numbers |
| coronal-hole-loop-statistics-... | first author + author list; venue; DOI; CH catalog source; seed convention; aggregate distribution metric and tolerance |
| flare-precursor-fine-scale-topology-... | first author + author list; venue; DOI; extrapolation family (NLFFF assumed not confirmed); event list; metrics |
| eclipse-white-light-... | first author + author list; venue; DOI; eclipse-image source / processing; agreement metric and tolerance; reference figure |
| dakeyo-2026-...-method-link | inherits canonical TODOs: final venue, exact PSP × SO interval list, PFSS tool used by authors |
| ervin-2024-... | venue; DOI; SW-type classification thresholds; high-field-strength source population details; heavy-ion composition source/instrument; synoptic Br product used |

## Source inventories

- `sioulas-reproduction/results/arxiv_papers/extended_search.md`
  (entries §2.1, §2.2, §2.3, §2.4, §2.5/§2.8, §2.6, §2.7, §2.9, §2.10)
- `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §2.3 (Dakeyo)
- `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md`
  §12 (Ervin), entry #3 (Dakeyo)
- Example adapters (not assumed): `.library/custom/pfss-tracing/`,
  `.library/custom/nspf-fem/`
