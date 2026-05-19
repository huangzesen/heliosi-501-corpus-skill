# HelioSI Paper-Skill Corpus — QA Report (v2)

- **Generated**: 2026-05-18
- **Generator**: HelioSI paper-to-skill factory (Claude Opus 4.7) — corpus_manifest_v2 aggregator
- **Companion files**: `corpus_manifest_v2.json`, `corpus_index_v2.md` (this report's prose foregrounds the same harness-agnostic framing).
- **v1 baseline preserved**: `corpus_manifest.json`, `corpus_index.md`, `corpus_qa_report.md` (96-skill snapshot, unchanged).

This report restates, audits, and bounds the v2 corpus claims. Read it together with the v0.2 harness-agnostic factory spec (`sioulas-reproduction/results/paper_skill_factory/paper_to_skill_factory_spec.md`) and migration note (`harness_agnostic_migration_note.md`). The factory framing is: paper-skills are harness-agnostic, agent-native scientific objects; LingTai, Claude Code, Python, MCPs, and `.library/custom/` adapters are runtime examples, not the essence of the corpus.

## 1. Count audit (filesystem ↔ batch manifests ↔ v2 roll-up)

| Counter | Value | Expected |
|---|---|---|
| Batches | 18 | 18 (9 baseline + 9 wave500) |
| Skills (sum of batch manifests) | 501 | 501 |
| Filesystem skill subdirs | 501 | 501 |
| Filesystem SKILL.md count | 501 | 501 |
| Filesystem metadata.yaml count | 501 | 501 |
| Unique slugs | 501 | 501 |
| Duplicate slugs across batches | **0** | 0 |
| All counters equal? | **True** | True |

Per batch:

| Batch | Manifest skills | FS subdirs | FS SKILL.md | FS metadata.yaml | Match |
|---|---|---|---|---|---|
| `batch_heliophysics_software_infrastructure` | 12 | 12 | 12 | 12 | **True** |
| `batch_mission_instruments_data_products` | 12 | 12 | 12 | 12 | **True** |
| `batch_pfss_source_mapping` | 10 | 10 | 10 | 10 | **True** |
| `batch_psp_switchbacks_magnetic` | 12 | 12 | 12 | 12 | **True** |
| `batch_sep_energetic_particles` | 12 | 12 | 12 | 12 | **True** |
| `batch_solar_wind_segmentation_ml` | 12 | 12 | 12 | 12 | **True** |
| `batch_turbulence_heating_apj` | 10 | 10 | 10 | 10 | **True** |
| `pilot_2026_and_runtime` | 8 | 8 | 8 | 8 | **True** |
| `pilot_turbulence` | 8 | 8 | 8 | 8 | **True** |
| `wave500_agent_runtime_eval_design_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_coronal_source_mapping_pfss_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_inner_heliosphere_psp_solo_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_instruments_data_software_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_sep_shocks_space_weather_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_solar_corona_cme_flares_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_sw_classification_ml_foundation_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_turbulence_intermit_heating_045` | 45 | 45 | 45 | 45 | **True** |
| `wave500_waves_instabilities_reconnection_045` | 45 | 45 | 45 | 45 | **True** |

**Method**: the aggregator script (`/tmp/build_corpus_v2_rollup.py`) reads each `<batch>/manifest.json`, counts `len(skills)`, and independently `os.listdir`s each batch directory and checks for `SKILL.md` and `metadata.yaml` in every subdir. All four counters must agree per batch.

## 2. JSON validation

- `corpus_manifest_v2.json` parses with `json.load` (Python 3 stdlib).
- Required top-level keys present: `schema_version` (`rollup-2.0`), `generated_at`, `corpus_root`, `framing`, `four_layer_model`, `claim_boundaries`, `totals`, `maturity_taxonomy`, `global_distributions`, `batches`, `entries`, `weak_entries_by_batch`, `validation`, `research_generation_map_pointer`.
- `len(entries)` = 501 == `totals.skills_in_manifests` = 501 == 501.
- `len(batches)` = 18 == `totals.batches` = 18 == 18.
- `totals.duplicate_slugs` = {}.

Re-verification one-liner (run from corpus root):

```bash
python3 -c "import json; m=json.load(open('corpus_manifest_v2.json')); t=m['totals']; assert t['skills_in_manifests']==t['fs_SKILL_md_files']==t['fs_metadata_yaml_files']==t['unique_slugs']==501; assert t['batches']==18; assert not t['duplicate_slugs']; print('OK', t)"
```

## 3. Claim boundaries — repeated for emphasis

This v2 roll-up is a structural and metadata aggregate across 18 batches (9 baseline + 9 wave500). It re-states what each batch manifest already asserts and adds a corpus-wide maturity taxonomy. It does NOT verify any paper-grounded claim against full text.

- Do NOT treat any paper-skill in this corpus as full-text verified. Most entries are 'paper-grounded-pending-full-text', 'stub', 'scaffold', 'pilot', or 'positioning-skill-not-executable-science'.
- Do NOT assume the abstract capabilities in Layer 2 are bound to a working MCP. Named tools (sunkit-magex, sw-scanner, scripts/, ...) appear only as example Layer-3 adapters that may or may not exist on a given runtime. The two first-class companion MCPs — `xhelio-spice` (ephemeris) and `xhelio-cdaweb` (CDAWeb data access) — live in external repositories (see SKILL.md / README.md `Companion MCP adapters`) and must still be installed by the consumer; mentioning them is not a runtime claim.
- Do NOT treat executable_status values that include 'scaffold', 'pipeline-specified-not-yet-runnable', 'contract-spec-only-not-yet-runnable', 'design-pattern-extractor', 'manuscript-checklist-only', 'architecture-template-only', 'benchmark-design-template', 'review-routing-not-runnable' as a claim that any workflow has been run end-to-end.
- Do NOT treat the research_generation_map as a publication-ready research agenda. Tensions/gaps/hypotheses are corpus-internal seeds.
- Do NOT propagate identifiers (DOIs, arXiv IDs, ADS bibcodes) marked TODO_verify_with_full_text, TODO verify, or null as if they were verified — many manifests carry these tokens explicitly.
- Do NOT cite `first_author` / `authors` from any per-entry `metadata.yaml` or `SKILL.md` frontmatter without independent verification against the live arXiv / DOI / ADS record. Authorship placeholders have been canonicalized to `null` / `[]` and flagged with `authors_verified: false` (or `authors_complete: false` for partial lists) — see README "Authorship fields are intentionally null / unverified" and `scripts/validate.sh` section S4d for the enforced invariant. The surname embedded in a slug is not asserted as the verified first author.
- Do NOT treat agent-runtime/positioning skills in wave500_agent_runtime_eval_design_045 as heliophysics workflows; they are design-pattern extracts for HelioSI runtime upgrades, not executable science.
- Do NOT treat instrument/data-product contract skills as runnable pipelines; they document expected L1/L2/L3 product semantics and validation tolerances.

**Sole batch-claimed numerical reproduction across all 501 skills:**
- Paper: Wu 2026 nonspherical coronal magnetic field / open flux
- Result: Local NSPF-FEM reproduction (.library/custom/nspf-fem/) — open flux 9.09 vs paper 9.19 G·R^2_sun (1.1% error) on GONG CR 2282 Rini=2.5
- Note: This remains the only batch-claimed numerical reproduction across all 501 skills.

**Domain-MCP caution (first-class companion MCPs vs Layer-3 examples):**
- *First-class companion MCPs (external repositories, NOT bundled in this skill — see SKILL.md / README.md `Companion MCP adapters`)*:
  - `xhelio-spice` — SPICE-based ephemeris, orbit geometry, frame transforms for PSP / Solar Orbiter / SDO / ACE etc. Repository: https://github.com/huangzesen/xhelio-spice
  - `xhelio-cdaweb` — CDAWeb / SPDF heliophysics data access (FIELDS, SWEAP, IS☉IS, SWA, MAG, EPD, ...). Repository: https://github.com/huangzesen/xhelio-cdaweb
  - Both must still be installed and configured by the consumer; their presence on a given runtime is **not** guaranteed and **not** a verification claim about any paper-skill.
- *Proposed / abstract (Layer-3 example only — do not assume runnable)*:
  - sunkit-magex / pfsspy adapters for pfss.solve
  - sw-scanner for solar-wind segmentation
  - pyspedas / HAPI / cdaweb Python loaders (note: `xhelio-cdaweb` is the recommended MCP binding for CDAWeb fetches, but these loaders may still be cited in entries that predate the MCP)
  - kglobal / ENLIL / EUHFORIA / MAS bindings for SEP/CME shock modelling
  - Surya foundation-model loaders
- *Caution*: When the corpus mentions any of the proposed adapters above, treat as Layer-3 example only. The Layer-2 capability is the contract; the named tool is a placeholder until a runtime owner certifies it. The two companion MCPs are recommended bindings when available but never required by Layer-2.

## 4. Maturity / evidence taxonomy across the 501 skills

Buckets are derived deterministically from `quality` + `executable_status` per the rule in `corpus_manifest_v2.json` (`maturity_taxonomy.counts`). They are *descriptive*, not promotion gates.

| Tier | Description | Count |
|---|---|---|
| `T1_locally_reproduced` | End-to-end numerical reproduction against published numbers achieved locally. | 1 |
| `T2_method_ready_executable_pilot` | Method-ready or runnable from a real data product / cached input; the named pipeline can be exercised under at least one runtime example. | 22 |
| `T3_paper_grounded_pending_full_text` | Bibliographic anchor identified, claim and Layer-2 contract specified, full-text verification still pending. Largest tier. | 260 |
| `T4_stub_or_scaffold_paper_grounded` | Stub or scaffold whose claim is paper-anchored but methods/equations and validation tolerances are not yet authored to method-ready. | 164 |
| `T5_agent_runtime_or_design_precedent` | Agent-runtime, benchmark, review-routing, ecosystem-diff, or historical-citation skill. Useful as compiled design precedent, not as executable heliophysics science. | 52 |
| `T6_link_only_or_routing` | Cross-batch link or routing-hub. Validation flows to the canonical skill it points at. | 1 |
| `T7_weak_attribution_or_citation_todo` | Software/package or team-paper entry with a citation/authorship TODO that blocks promotion past stub. | 1 |
| **TOTAL** | _501_ | **501** |

**Per-batch maturity composition:**

| Batch | Maturity buckets |
|---|---|
| `batch_heliophysics_software_infrastructure` | T2=8, T3=2, T5=2 |
| `batch_mission_instruments_data_products` | T3=12 |
| `batch_pfss_source_mapping` | T1=1, T3=8, T6=1 |
| `batch_psp_switchbacks_magnetic` | T3=12 |
| `batch_sep_energetic_particles` | T3=10, T5=2 |
| `batch_solar_wind_segmentation_ml` | T4=12 |
| `batch_turbulence_heating_apj` | T4=10 |
| `pilot_2026_and_runtime` | T2=1, T3=4, T5=3 |
| `pilot_turbulence` | T4=7, T7=1 |
| `wave500_agent_runtime_eval_design_045` | T5=45 |
| `wave500_coronal_source_mapping_pfss_045` | T3=45 |
| `wave500_inner_heliosphere_psp_solo_045` | T3=45 |
| `wave500_instruments_data_software_045` | T2=13, T3=32 |
| `wave500_sep_shocks_space_weather_045` | T3=45 |
| `wave500_solar_corona_cme_flares_045` | T3=45 |
| `wave500_sw_classification_ml_foundation_045` | T4=45 |
| `wave500_turbulence_intermit_heating_045` | T4=45 |
| `wave500_waves_instabilities_reconnection_045` | T4=45 |

**Audit note on T2 (22 entries)**: thirteen of the T2 entries come from `wave500_instruments_data_software_045` and carry `quality=method-ready` with `executable_status=contract-specified-not-yet-benchmarked`. That status means the package contract is specified but the pipeline has not been benchmarked end-to-end; the `method-ready` label is the batch author's assessment that a working Python adapter exists upstream (sunpy, sunkit-magex, spiceypy, drms, hapi-server, soar, jsoc, psp-soc, …). Treat these as Layer-3-bindable but not evidence of executed numerical agreement; promotion past T2 requires a benchmarked Layer-2 run.

## 5. Safe vs unsafe claims

**Safe to assert (load-bearing for downstream agents):**

- The corpus contains exactly **501** paper-skill directories under `sioulas-reproduction/results/paper_skill_corpus/`, each with a `SKILL.md` and a `metadata.yaml`, distributed across **18** batches (96 baseline + 405 wave500). All counters cross-match (manifest ↔ filesystem ↔ subdir ↔ unique slugs).
- Slugs are globally unique across batches (`duplicate_slugs={}`).
- The corpus is authored under the v0.2 harness-agnostic framing: Layer 1 (scientific invariant) + Layer 2 (abstract executable protocol) + Layer 3 (optional adapter binding) + Layer 4 (research-generation affordance).
- Exactly **one** skill (Wu 2026 NSPF) has a documented batch-level numerical reproduction (open flux 9.09 vs 9.19 G·R²_sun, 1.1% error).
- The v1 research-generation map (9 tensions T1–T9, 6 gaps G1–G6) carries forward unchanged; the wave500 batches add new substrate but do not yet author new tensions inline in their SKILL.md files (Layer-4 authoring is inconsistent; see G4 in v1 map).

**Unsafe to assert (do NOT claim):**

- That all 501 skills are full-text verified. Most are `paper-grounded-pending-full-text` (217), `stub` (184), `pilot` (29), `positioning-skill-not-executable-science` (48), or `method-ready` (20). Only the Wu 2026 NSPF entry is locally reproduced.
- That any specific MCP (sunkit-magex, sw-scanner, kglobal, ENLIL, EUHFORIA, Surya foundation model) is bound and runnable in the consumer harness. Those names are Layer-3 example adapters. The two first-class companion MCPs (`xhelio-spice` for SPICE/ephemeris and `xhelio-cdaweb` for CDAWeb data access) are external GitHub repositories that the consumer must install separately — neither is bundled in this skill, and listing them is not a runtime guarantee.
- That `executable_status` values like `pipeline-specified-not-yet-runnable`, `contract-spec-only-not-yet-runnable`, `scaffold`, `stub`, `design-pattern-extractor`, `manuscript-checklist-only`, `architecture-template-only`, `benchmark-design-template`, `review-routing-not-runnable`, `historical-citation-only`, `ecosystem-diff-procedure-only` mean *runnable*. They explicitly mean *not yet run end-to-end*.
- That DOIs / arXiv IDs / ADS bibcodes marked `TODO_verify_with_full_text`, `TODO verify`, or null are verified. Many are placeholders for the next curation pass.
- That the research-generation map describes an externally validated research agenda. It is corpus-internal seed material.
- That `wave500_agent_runtime_eval_design_045` (45 skills) is heliophysics-executable. It collects agent-runtime / AI-scientist / benchmark / co-scientist design patterns as positioning skills for HelioSI runtime evolution.

## 6. Weak entries / TODO classes by batch

Per-batch counts (from each batch manifest's `weak_entries_needing_full_text_verification` / `weak_entries` / `todos` fields). Detailed per-skill TODO lists are reproduced in each batch manifest and the v1 QA report; v2 does not duplicate them per-skill.

| Batch | Skills | Weak entries (per manifest) | Share |
|---|---|---|---|
| `batch_heliophysics_software_infrastructure` | 12 | 12 | 100% |
| `batch_mission_instruments_data_products` | 12 | 12 | 100% |
| `batch_pfss_source_mapping` | 10 | 10 | 100% |
| `batch_psp_switchbacks_magnetic` | 12 | 12 | 100% |
| `batch_sep_energetic_particles` | 12 | 12 | 100% |
| `batch_solar_wind_segmentation_ml` | 12 | 12 | 100% |
| `batch_turbulence_heating_apj` | 10 | 10 | 100% |
| `pilot_2026_and_runtime` | 8 | 6 | 75% |
| `pilot_turbulence` | 8 | 4 | 50% |
| `wave500_agent_runtime_eval_design_045` | 45 | 0 | 0% |
| `wave500_coronal_source_mapping_pfss_045` | 45 | 0 | 0% |
| `wave500_inner_heliosphere_psp_solo_045` | 45 | 45 | 100% |
| `wave500_instruments_data_software_045` | 45 | 0 | 0% |
| `wave500_sep_shocks_space_weather_045` | 45 | 45 | 100% |
| `wave500_solar_corona_cme_flares_045` | 45 | 1 | 2% |
| `wave500_sw_classification_ml_foundation_045` | 45 | 0 | 0% |
| `wave500_turbulence_intermit_heating_045` | 45 | 0 | 0% |
| `wave500_waves_instabilities_reconnection_045` | 45 | 45 | 100% |
| **TOTAL** | **501** | **226** | **45%** |

**Dominant TODO classes (qualitative, carried forward from v1 + extended by wave500):**

- *C1 — bibliographic gaps*: DOI, ADS bibcode, journal/venue, full author list. Affects the majority of paper-grounded-pending-full-text entries (217 across the corpus).
- *C2 — numerical tolerances / figure identifiers*: required for promotion past `method-ready` per factory spec §7. Missing in essentially all paper-grounded entries.
- *C3 — solver / model identity*: ML architecture, MHD code, kappa form, PFSS solver, foundation-model checkpoints. Common across SEP, segmentation, PFSS, turbulence, coronal-imaging, agent-runtime batches.
- *C4 — encounter / event lists*: specific PSP encounter, conjunction window, ICME / CME / IVA / HCS event date. Common across PSP-switchback, SEP, CME, instruments batches.
- *C5 — cross-attribution conflicts*: a small number of arXiv IDs are attributed to two papers in different source inventories (carried over from `pilot_turbulence`).
- *C6 — software-package citation TODOs*: many wave500_instruments_data_software_045 entries note `not in local inventory; cite Space Sci. Rev. ... (year) when verifying`. These block promotion past method-ready / contract-specified-not-yet-benchmarked.
- *C7 — Layer-4 affordance authoring*: a structural TODO. Layer-4 affordances are explicitly authored only in three baseline batches (`batch_pfss_source_mapping`, `batch_sep_energetic_particles`, `batch_psp_switchbacks_magnetic`). For the other 15 batches, Layer-4 content lives in the roll-up `research_generation_map` and batch index.md, not inline in each SKILL.md.
- *C8 — agent-runtime design-pattern transplant scoping*: wave500_agent_runtime_eval_design_045 entries propose heliophysics transplants of patterns from non-heliophysics agentic AI work (e.g. FunSearch on PFSS-parameter search). These are seeds, not validated transplants.

## 7. Recommended next curation steps

Listed in order of expected value-per-effort. None require new data acquisition; all are curation passes over the existing 501-entry corpus.

1. **Bibliographic verification pass (C1)**. Resolve DOI / ADS bibcode / venue / full author list for the 217 `paper-grounded-pending-full-text` entries against arXiv + ADS. This is the single largest weak class and the prerequisite for any C2 promotion. Estimate ~217 lookups (most already have arXiv IDs).
2. **Layer-4 affordance authoring pass (C7 / G4 in v1 map)**. For each wave500 batch, write per-skill `research_generation_affordances[]` blocks that tie its entries to the v1 tensions/gaps and to its sibling wave500 batches. Use the seed table in `corpus_index_v2.md` §7 as the starting point. Promote G4 from open to in-progress.
3. **Promotion of T4→T3 stubs in wave500_sw_classification_ml_foundation_045, wave500_turbulence_intermit_heating_045, wave500_waves_instabilities_reconnection_045** (135 stub-tier entries). For each, populate `core_claim`, `methods/equations`, and `validation_targets` against the full text; flip `executable_status` from `scaffold/stub` to `pipeline-specified-not-yet-runnable` once Layer-2 is authored.
4. **Software-package citation pass (C6)** for wave500_instruments_data_software_045 to remove the 13 `contract-specified-not-yet-benchmarked` entries' citation TODO. Most are findable JOSS / SSR / arXiv references.
5. **Cross-runtime loadability test (G5 in v1 map)**. Author a smoke test that loads N skills under each candidate harness (LingTai, Claude Code, Codex, Cursor) and verifies the trigger sentence + Layer-2 capability surface is dispatchable. This is the load-bearing test of the 'harness-agnostic' claim.
6. **Stage-B synthesis hub creation (G2 in v1 map)**. Promote the cross-skill primitives — Politano-Pouquet third-order law, Walén test, PVI, Elsässer decomposition, GCS fitting, kappa fitting, PFSS+source-mapping pipeline, VDA — into named tool-skills with abstract Layer-2 contracts.
7. **Slug-collision regression test**. Add a CI-style check that re-runs the v2 aggregator and asserts `duplicate_slugs == {}` whenever a new skill or batch is added. The current `duplicate_slugs={}` invariant is the load-bearing identity guarantee for cross-batch reference (`depends_on` edges).
8. **Adapter-binding inventory under `.library/custom/`** (curation-side, NOT inside this corpus). For each wave500 capability mentioned in Layer 2 (e.g. `pfss.solve`, `gcs.fit`, `kappa_fit.tail`, `swa.load`), record whether a real adapter exists, where, and under which runtime. The single existing implemented contract (xhelio-spice) should be the template.

## 8. Layer-rendering schemas per batch (issue #13)

The 501 per-entry `SKILL.md` files do **not** share a single layer-
rendering schema. Three independent authoring passes (96-baseline →
wave500 → factory-template iterations) produced six distinct H2-header
families across 18 batches. Full corpus regeneration to unify the
schema was judged too risky for this hygiene batch; instead we **document
the six families honestly** and ship a reproducible classifier
(`scripts/audit_layer_schemas.py`) so the table below stays in sync
with the actual filesystem.

The six families are:

- `numbered_layer_v0_2_explicit` — `## 1. Trigger *(Layer 1)*`, `## 2. Paper claim → verifiable task *(Layer 1)*`, … `## 9. Skill graph + research-generation affordances *(Layer 4)*`. Layer membership is annotated *inline* in the H2. Used by the v0.2 factory wave500 batches that explicitly tag every section with its layer.
- `numbered_layer_v0_2_abbreviated` — same nine-section spine as `numbered_layer_v0_2_explicit` but with the inline `*(Layer N)*` tags stripped (`## 1. Trigger` / `## 9. Skill graph + affordances`). Appears as a minor variant inside `wave500_turbulence_intermit_heating_045`.
- `numbered_executable_workflow_v1` — `## 1. Trigger`, `## 2. Paper claim → verifiable task`, … `## 9. Skill graph → depends_on`. Executable-workflow framing rather than four-layer framing; this is the older 96-baseline rendering. Some batches additionally have `## 10. Research-generation affordances (harness-agnostic)`.
- `five_layer_scientific_invariant` — `## 1. Trigger and claim boundary`, `## 2. Scientific invariant layer`, `## 3. Executable protocol layer`, `## 4. Adapter / runtime notes`, `## 5. Research-generation affordance`. A more compact five-section schema; this is also the rendering whose Layer-3 algorithm sub-sections contain the issue #14 placeholder phrase for the 45 psp_solo entries.
- `prose_engineering_instrument` — prose H2s `## When to use this paper-skill`, `## Paper identity and claim boundary`, `## Scientific or methodological claim to operationalize`, … rather than numbered Layer-N headers. Used for instrument and software papers where the "Layer-2 executable protocol" framing is a poor fit (FIELDS suite, CDAWeb, etc.).
- `prose_pfss_layered` — `> Runtime-neutral paper-skill` blockquote + prose `## Trigger` followed by `## Layer 1 — Scientific invariant`, `## Layer 2 — Executable protocol`, … . A hybrid that uses prose section names but explicit Layer-N headers; common in the PFSS/CME batches.

Per-batch rendering distribution (auto-generated via
`python3 scripts/audit_layer_schemas.py --json --strict`):

| Batch | Skills | Rendering family/families | Notes |
|---|---:|---|---|
| `batch_heliophysics_software_infrastructure` | 12 | `numbered_executable_workflow_v1` × 12 |  |
| `batch_mission_instruments_data_products` | 12 | `prose_engineering_instrument` × 12 |  |
| `batch_pfss_source_mapping` | 10 | `prose_pfss_layered` × 10 |  |
| `batch_psp_switchbacks_magnetic` | 12 | `five_layer_scientific_invariant` × 12 |  |
| `batch_sep_energetic_particles` | 12 | `numbered_executable_workflow_v1` × 12 |  |
| `batch_solar_wind_segmentation_ml` | 12 | `numbered_executable_workflow_v1` × 12 |  |
| `batch_turbulence_heating_apj` | 10 | `prose_engineering_instrument` × 10 |  |
| `pilot_2026_and_runtime` | 8 | `prose_engineering_instrument` × 8 |  |
| `pilot_turbulence` | 8 | `prose_engineering_instrument` × 8 |  |
| `wave500_agent_runtime_eval_design_045` | 45 | `numbered_layer_v0_2_explicit` × 45 |  |
| `wave500_coronal_source_mapping_pfss_045` | 45 | `prose_pfss_layered` × 45 |  |
| `wave500_inner_heliosphere_psp_solo_045` | 45 | `five_layer_scientific_invariant` × 45 | all 45 are Layer-2 stubs (issue #14) |
| `wave500_instruments_data_software_045` | 45 | `numbered_layer_v0_2_explicit` × 45 |  |
| `wave500_sep_shocks_space_weather_045` | 45 | `numbered_layer_v0_2_explicit` × 45 |  |
| `wave500_solar_corona_cme_flares_045` | 45 | `prose_pfss_layered` × 45 |  |
| `wave500_sw_classification_ml_foundation_045` | 45 | `numbered_layer_v0_2_explicit` × 45 |  |
| `wave500_turbulence_intermit_heating_045` | 45 | `numbered_layer_v0_2_explicit` × 41 + `numbered_layer_v0_2_abbreviated` × 4 | mixed: 41 entries carry the inline `*(Layer N)*` tag, 4 use the abbreviated form |
| `wave500_waves_instabilities_reconnection_045` | 45 | `five_layer_scientific_invariant` × 45 | includes 10 curated short Layer-2 stubs (issue #14) |

**How to read this table:**

- The six family labels are stable across reads; re-running the
  classifier should produce the same per-batch distribution until the
  underlying SKILL.md headers change.
- A "mixed" row lists every family present; agents that grep against H2
  headers must handle each variant.
- The `prose_engineering_instrument` family does NOT carry numbered
  Layer-N headers; "Layer 2" content lives in *Scientific or methodological
  claim to operationalize* + *Data assumptions and tool contracts*
  sub-sections. Tooling that depends on `## 2.` / `## 3.` headers to
  locate Layer-2 content will miss it for those four batches.
- Three families (`numbered_layer_v0_2_explicit`, `numbered_layer_v0_2_abbreviated`,
  `numbered_executable_workflow_v1`) share the nine-section
  `## 1.`–`## 9.` spine but differ in their inline-layer-tag wording;
  two families (`five_layer_scientific_invariant`,
  `prose_pfss_layered`) use a five-section / Layer-N spine;
  one family (`prose_engineering_instrument`) uses prose headers only.

**Reproducibility:** `python3 scripts/audit_layer_schemas.py --strict`
re-emits the rendering distribution and exits non-zero if any entry is
unclassified. The classifier is regex-based and stdlib-only; the test
suite (`tests/test_layer_schemas.py`) pins the per-batch distribution so
any drift surfaces as a test failure in CI.

## 9. Acceptance summary

| Requirement | Status |
|---|---|
| (1) Count all 501 skills across 18 batches; manifest ↔ filesystem ↔ unique-slugs match | ✓ — see §1 |
| (2) Per-batch summary with path, count, theme/framing, quality + status distributions | ✓ — `corpus_index_v2.md` §5 + `corpus_manifest_v2.json` `batches` |
| (3) Per-entry record with batch/slug/path/title/year/quality/exec-status/source-type/Layer-4 presence | ✓ — `corpus_manifest_v2.json` `entries` (501 records) |
| (4) Foreground HelioSI project framing + four-layer model + open discovery loop | ✓ — `corpus_index_v2.md` §1–2 + `corpus_manifest_v2.json` `framing` / `four_layer_model` |
| (5) Maturity / evidence taxonomy distinguishing reproduced vs scaffold vs design-precedent | ✓ — §4 here + `corpus_manifest_v2.json` `maturity_taxonomy` |
| (6) Claim boundaries with safe/unsafe lists; MCP caution | ✓ — §3 + §5 here + `corpus_index_v2.md` §3 |
| (7) Weak entries / TODO classes by batch | ✓ — §6 + per-batch manifests (unchanged) |
| (8) Validate JSON parses; counts match 501; duplicate slugs zero; three v2 files exist | ✓ — §1–2; one-liner provided |
| Do not touch `.library/custom/` or live skill catalog | ✓ — only writes are under `paper_skill_corpus/` |
| Do not overwrite v1 roll-up files | ✓ — `corpus_manifest.json`, `corpus_index.md`, `corpus_qa_report.md` preserved unchanged; v2 files are new |
| Do not rewrite existing paper-skills | ✓ — only the three v2 roll-up files were written |
| Treat LingTai/Claude Code/Python/MCP/PFSS scripts as adapter examples | ✓ — §3 here + `corpus_index_v2.md` §1 non-consumers |
