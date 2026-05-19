# HelioSI Paper-Skill Corpus — Roll-up Index (v2)

- **Generated**: 2026-05-18
- **Generator**: HelioSI paper-to-skill factory (Claude Opus 4.7) — corpus_manifest_v2 aggregator
- **Corpus root**: `sioulas-reproduction/results/paper_skill_corpus/`
- **Totals**: 18 batches (96 baseline + 405 wave500) · 501 skills · 501 SKILL.md · 501 metadata.yaml · counts_match=**True** · unique_slugs=501 · duplicate_slugs=**none**

## 1. Why this corpus exists — HelioSI project framing

HelioSI restructures heliophysics-domain knowledge into harness-agnostic, agent-native scientific objects to industrialize the open discovery loop 'generate new ideas -> propose hypotheses -> execute discoveries'. Skills are the load-bearing objects; LingTai, Claude Code, Python, MCP servers, and .library/custom adapters are runtime examples, not the essence of the corpus.

**Open discovery loop (the loop HelioSI is built to industrialize):**

1. INGEST — paper-skills compile literature into runtime-neutral scientific objects.
2. GENERATE — Layer-4 affordances expose gaps, tensions, hypothesis seeds across skills.
3. PROPOSE — hypotheses tie cross-skill tensions to concrete minimal experiments.
4. EXECUTE — Layer-2 abstract capabilities are bound to runtime adapters (Layer-3).
5. RESULTS — new findings flow back into the corpus as refined or new paper-skills.

**Consumers (any general-purpose agent runtime):**

- LingTai mailbox / agent network
- Claude Code harness
- Codex, Cursor, custom agent harnesses
- Plain-Python execution + MCP servers when configured

**Explicit non-consumers / runtime examples only:**

- .library/custom/* is NOT modified by this roll-up.
- Domain MCPs (sunkit-magex, pfss-tracing, sw-scanner, lingtai xhelio-spice, ...) are Layer-3 example adapters, not requirements. Only xhelio-spice has an implemented contract; other domain MCP contracts in batches are proposed/abstract.

## 2. Harness-agnostic four-layer model (up to four layers, populated as the entry matures)

Each paper-skill is authored against a stack of **up to four** conceptual layers. The corpus itself is runtime-neutral; specific skills, MCPs, and Python adapters are runtime-supplied and substitutable. The paper-skill must be loadable by LingTai, Claude Code, Codex, or any future agent harness.

The "four-layer model" is the **authoring spec**, not a per-entry invariant — Layer 1 (scientific invariant) is present on every entry, but Layers 2/3/4 are populated as each entry matures (stub → method-ready → reproduced). Entries that author an explicit `layers:` boolean frontmatter block declare per-layer presence directly; entries without that block encode layer coverage prose-side (numbered sections or `## Layer N — …` headers, audited by `scripts/audit_layer_schemas.py`). See `corpus_qa_report_v2.md` §9 for the fully-populated vs partially-populated breakdown (issue #58).

| Layer | Role |
|---|---|
| **layer_1_scientific_invariant** | Narrow-form claim, claim_boundary, methods/equations as assumptions, failure modes, figure/numerical targets. Load-bearing for reproducibility. |
| **layer_2_executable_protocol** | Capability-typed procedure naming abstract capabilities (e.g. pfss.solve, magnetogram.fetch_synoptic_br, kappa_fit.tail) and validation targets. Names protocols, not products. |
| **layer_3_adapter_runtime_binding_optional** | Optional examples of concrete bindings in one runtime (.library/custom/, sunkit-magex, lingtai mcp xhelio-spice). Substitutable; absence does not break the skill. |
| **layer_4_research_generation_affordance** | Gaps, tensions, hypothesis opportunities, minimal experiments enabled by combining this skill with siblings. Powers the 'generate new ideas' end of the discovery loop. |

**Compilation table — paper element → layer:**

| Paper element | Layer placement |
|---|---|
| claims | Layer 1 narrow-form claim + claim_boundary |
| methods_equations | Layer 1 assumptions + Layer 2 procedure |
| data_instruments | Layer 1 data assumptions + Layer 2 abstract capabilities |
| caveats_failure_modes | Layer 1 failure modes (skill memory) |
| figures_results | Layer 1 figure/numerical targets + Layer 2 validation target |
| citations | depends_on edges at end of SKILL.md |
| generative_implications | Layer 4 research-generation affordance |

**Explicit `layers:` boolean authoring across all 501 entries** (counts entries that author the inline `layers:` block on the SKILL.md frontmatter; many baseline-batch skills express layer content as prose in SKILL.md / metadata.yaml and are not counted here. Live numbers via `python3 scripts/audit_layer_population.py`; consistency pinned by `tests/test_layer_population.py`):

| Surface | Entries with explicit block | Fully populated (4/4) | Partially populated (<4/4) |
|---|---:|---:|---:|
| SKILL.md frontmatter `layers:` | 225 / 501 | 0 | 225 |
| metadata.yaml top-level `layers:` | 90 / 501 | 45 | 45 |

**SKILL.md frontmatter — distribution of partial-population (issue #58):**

| # layers true | Entries | Batches |
|---:|---:|---|
| 1 / 4 | 90 | `wave500_instruments_data_software_045` (45), `wave500_sw_classification_ml_foundation_045` (45) |
| 2 / 4 | 45 | `wave500_turbulence_intermit_heating_045` (45) |
| 3 / 4 | 90 | `wave500_agent_runtime_eval_design_045` (45), `wave500_sep_shocks_space_weather_045` (45) |
| 4 / 4 | 0 | (none on this surface) |

**Per-layer `true` counts (SKILL.md frontmatter, among the 225 entries with the block):**

| Layer | Entries with `layers.<key>: true` |
|---|---:|
| scientific_invariant | 225 |
| executable_protocol | 90 |
| adapter_binding_examples | 0 |
| research_generation_affordance | 135 |

> Counts reflect entries that EXPLICITLY author a `layers:` block in the SKILL.md frontmatter (or metadata.yaml). Many baseline-batch skills predate the booleans; their layer coverage is described prose-side and is audited by `scripts/audit_layer_schemas.py` instead (see `corpus_qa_report_v2.md` §8). The two surfaces agree on every entry where both are present (0 parity mismatches; verified by `audit_layer_population.py --strict`).

## 3. Claim boundaries (read before quoting any skill)

This v2 roll-up is a structural and metadata aggregate across 18 batches (9 baseline + 9 wave500). It re-states what each batch manifest already asserts and adds a corpus-wide maturity taxonomy. It does NOT verify any paper-grounded claim against full text.

**Out of scope — do NOT generalize beyond these:**

- Do NOT treat any paper-skill in this corpus as full-text verified. Most entries are 'paper-grounded-pending-full-text', 'stub', 'scaffold', 'pilot', or 'positioning-skill-not-executable-science'.
- Do NOT assume the abstract capabilities in Layer 2 are bound to a working MCP. Named tools (sunkit-magex, lingtai mcp xhelio-spice, scripts/) appear only as example Layer-3 adapters that may or may not exist on a given runtime.
- Do NOT treat executable_status values that include 'scaffold', 'pipeline-specified-not-yet-runnable', 'contract-spec-only-not-yet-runnable', 'design-pattern-extractor', 'manuscript-checklist-only', 'architecture-template-only', 'benchmark-design-template', 'review-routing-not-runnable' as a claim that any workflow has been run end-to-end.
- Do NOT treat the research_generation_map as a publication-ready research agenda. Tensions/gaps/hypotheses are corpus-internal seeds.
- Do NOT propagate identifiers (DOIs, arXiv IDs, ADS bibcodes) marked TODO_verify_with_full_text, TODO verify, or null as if they were verified — many manifests carry these tokens explicitly.
- Do NOT cite the `first_author` / `authors` (or `paper.first_author` / `paper.authors`) field of any per-entry file without independent verification. As of the issue #8 hygiene pass, TODO/TBD placeholder strings have been canonicalized out of authorship fields — unverified entries are `null` / `[]` with `authors_verified: false`, partial author lists are flagged `authors_complete: false`. The surname embedded in a slug is not asserted as the verified first author.
- Do NOT treat agent-runtime/positioning skills in wave500_agent_runtime_eval_design_045 as heliophysics workflows; they are design-pattern extracts for HelioSI runtime upgrades, not executable science.
- Do NOT treat instrument/data-product contract skills as runnable pipelines; they document expected L1/L2/L3 product semantics and validation tolerances.

**Sole batch-claimed numerical reproduction across all 501 skills:**

- *Paper*: Wu 2026 nonspherical coronal magnetic field / open flux
- *Result*: Local NSPF-FEM reproduction (.library/custom/nspf-fem/) — open flux 9.09 vs paper 9.19 G·R^2_sun (1.1% error) on GONG CR 2282 Rini=2.5
- *Note*: This remains the only batch-claimed numerical reproduction across all 501 skills.

**Domain MCP caution:**

- *Implemented contract*: xhelio-spice (LingTai MCP) — implemented and exercised on PSP/SO ephemeris.
- *Proposed / abstract contracts (Layer-3 example only)*:
  - sunkit-magex / pfsspy adapters for pfss.solve
  - sw-scanner for solar-wind segmentation
  - pyspedas/cdaweb/HAPI loaders
  - kglobal / ENLIL / EUHFORIA / MAS bindings for SEP/CME shock modelling
  - Surya foundation-model loaders
- *Caution*: When the corpus mentions any of the proposed adapters above, treat as Layer-3 example only. The Layer-2 capability is the contract; the named tool is a placeholder until a runtime owner certifies it.

## 4. Maturity / evidence taxonomy

Each of the 501 skills falls into exactly one bucket. The bucket is derived deterministically from `quality` + `executable_status` per the rule in `corpus_manifest_v2.json` (`maturity_taxonomy.counts`). Buckets are descriptive, not promotion gates.

| Tier | Definition | Count |
|---|---|---|
| T1_locally_reproduced | End-to-end numerical reproduction achieved locally. | 1 |
| T2_method_ready_executable_pilot | Method-ready or runnable-from-* status; pipeline bound to ≥1 runtime example. | 22 |
| T3_paper_grounded_pending_full_text | Claim and Layer-2 contract authored; full-text / DOI / figure tolerance verification pending. | 260 |
| T4_stub_or_scaffold_paper_grounded | Stub, scaffold, or contract-spec-only; paper-anchored but methods/equations not yet authored to method-ready. | 164 |
| T5_agent_runtime_or_design_precedent | Agent-runtime, benchmark, review-routing, ecosystem-diff, or historical-citation skill. Compiled design precedent, not executable heliophysics. | 52 |
| T6_link_only_or_routing | Cross-batch link or routing-hub; validation flows to the canonical skill it points at. | 1 |
| T7_weak_attribution_or_citation_todo | Citation/authorship TODO blocks promotion past stub. | 1 |
| **TOTAL** | _501_ | **501** |

## 5. Per-batch table

Each batch's `manifest.json` is authoritative for its own claims; this index aggregates without rewriting. `counts_match` requires manifest skill count == filesystem subdir count == filesystem SKILL.md count == filesystem metadata.yaml count.

| Batch | Path | Count | counts_match | Top quality tier | Top exec. status | Maturity buckets |
|---|---|---|---|---|---|---|
| `batch_heliophysics_software_infrastructure` | `sioulas-reproduction/results/paper_skill_corpus/batch_heliophysics_software_infrastructure/` | 12 | **True** | `method-ready` | `pipeline-specified-not-yet-benchmarked` | T2=8, T3=2, T5=2 |
| `batch_mission_instruments_data_products` | `sioulas-reproduction/results/paper_skill_corpus/batch_mission_instruments_data_products/` | 12 | **True** | `paper-grounded-pending-full-text` | `contract-spec-only-not-yet-runnable` | T3=12 |
| `batch_pfss_source_mapping` | `sioulas-reproduction/results/paper_skill_corpus/batch_pfss_source_mapping/` | 10 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T1=1, T3=8, T6=1 |
| `batch_psp_switchbacks_magnetic` | `sioulas-reproduction/results/paper_skill_corpus/batch_psp_switchbacks_magnetic/` | 12 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T3=12 |
| `batch_sep_energetic_particles` | `sioulas-reproduction/results/paper_skill_corpus/batch_sep_energetic_particles/` | 12 | **True** | `stub` | `pipeline-specified-not-yet-runnable` | T3=10, T5=2 |
| `batch_solar_wind_segmentation_ml` | `sioulas-reproduction/results/paper_skill_corpus/batch_solar_wind_segmentation_ml/` | 12 | **True** | `pilot` | `scaffold` | T4=12 |
| `batch_turbulence_heating_apj` | `sioulas-reproduction/results/paper_skill_corpus/batch_turbulence_heating_apj/` | 10 | **True** | `pilot` | `scaffold` | T4=10 |
| `pilot_2026_and_runtime` | `sioulas-reproduction/results/paper_skill_corpus/pilot_2026_and_runtime/` | 8 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T2=1, T3=4, T5=3 |
| `pilot_turbulence` | `sioulas-reproduction/results/paper_skill_corpus/pilot_turbulence/` | 8 | **True** | `pilot` | `scaffold` | T4=7, T7=1 |
| `wave500_agent_runtime_eval_design_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/` | 45 | **True** | `positioning-skill-not-executable-science` | `design-pattern-extractor` | T5=45 |
| `wave500_coronal_source_mapping_pfss_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_coronal_source_mapping_pfss_045/` | 45 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T3=45 |
| `wave500_inner_heliosphere_psp_solo_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_inner_heliosphere_psp_solo_045/` | 45 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T3=45 |
| `wave500_instruments_data_software_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/` | 45 | **True** | `stub` | `contract-specified-not-yet-benchmarked` | T2=13, T3=32 |
| `wave500_sep_shocks_space_weather_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_sep_shocks_space_weather_045/` | 45 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T3=45 |
| `wave500_solar_corona_cme_flares_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_solar_corona_cme_flares_045/` | 45 | **True** | `paper-grounded-pending-full-text` | `pipeline-specified-not-yet-runnable` | T3=45 |
| `wave500_sw_classification_ml_foundation_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_sw_classification_ml_foundation_045/` | 45 | **True** | `stub` | `stub` | T4=45 |
| `wave500_turbulence_intermit_heating_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_turbulence_intermit_heating_045/` | 45 | **True** | `stub` | `null` | T4=45 |
| `wave500_waves_instabilities_reconnection_045` | `sioulas-reproduction/results/paper_skill_corpus/wave500_waves_instabilities_reconnection_045/` | 45 | **True** | `stub` | `contract-spec-only-not-yet-runnable` | T4=45 |

**Per-batch composition (read together with the per-batch manifests):**

### `batch_heliophysics_software_infrastructure` (12 skills)

- *Framing*: general-purpose harness; HelioSI = heliophysics domain instantiation; software/data-infrastructure skills are the root substrate every in-situ paper-skill depends on
- *Quality distribution*: method-ready=7, stub=5
- *Executable-status distribution*: pipeline-specified-not-yet-benchmarked=4, contract-specified-not-yet-benchmarked=1, ecosystem-diff-procedure-only=1, examples-only-not-yet-benchmarked=1, historical-citation-only=1, pipeline-specified-runnable-from-cached-magnetogram=1, pipeline-specified-runnable-from-cdas-or-hapi=1, pipeline-specified-runnable-from-pyspedas=1, pipeline-specified-runnable-from-spice=1
- *Year distribution*: 2022=3, 2023=3, 2018=2, 1996=1, 2015=1, 2019=1, 2020=1
- *Weak entries (per batch manifest)*: 12

### `batch_mission_instruments_data_products` (12 skills)

- *Framing*: general-purpose harness; HelioSI = heliophysics domain instantiation; skills + MCPs + harness triple
- *Quality distribution*: paper-grounded-pending-full-text=12
- *Executable-status distribution*: contract-spec-only-not-yet-runnable=8, pipeline-specified-not-yet-runnable=4
- *Year distribution*: 2016=5, 2020=5, 2025=1, 2026=1
- *Weak entries (per batch manifest)*: 12

### `batch_pfss_source_mapping` (10 skills)

- *Framing*: RUNTIME-NEUTRAL. Paper-skills do not assume a specific harness or agent framework. LingTai and Claude Code appear only as example adapters in Layer 3. .library/custom/pfss-tracing/
- *Quality distribution*: paper-grounded-pending-full-text=8, link-only-cross-batch=1, paper-grounded-locally-reproduced=1
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=8, locally-reproduced-via-nspf-fem=1, see-pilot-2026-and-runtime-skill=1
- *Year distribution*: 2026=4, 2024=2, 2016=1, 2020=1, 2022=1, 2023=1
- *Weak entries (per batch manifest)*: 10

### `batch_psp_switchbacks_magnetic` (12 skills)

- *Framing*: {"principle": "Paper-skills are harness-agnostic. LingTai, Claude Code, Codex, and notebook-driven workflows are adapters, not assumptions in the skill body.", 
- *Quality distribution*: paper-grounded-pending-full-text=12
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=12
- *Year distribution*: 2021=4, 2020=3, 2022=2, 2023=2, 2026=1
- *Weak entries (per batch manifest)*: 12

### `batch_sep_energetic_particles` (12 skills)

- *Framing*: Skills are runtime-neutral: loadable by any general-purpose agent runtime (Claude Code, LingTai, Codex, Cursor, OpenAI Assistants, …). Named runtimes / MCPs / repos appear only as 
- *Theme*: `solar-energetic-particles-and-heliospheric-shocks`
- *Quality distribution*: stub=12
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=10, review-routing-not-runnable=2
- *Year distribution*: 2024=5, 2026=5, 2025=2
- *Weak entries (per batch manifest)*: 12

### `batch_solar_wind_segmentation_ml` (12 skills)

- *Framing*: general-purpose harness; HelioSI = heliophysics domain instantiation; skills + (proposed) MCPs + harness triple
- *Theme*: `solar_wind_segmentation`
- *Quality distribution*: pilot=12
- *Executable-status distribution*: scaffold=12
- *Year distribution*: 2025=6, 2022=2, 2026=2, 2018=1, 2024=1
- *Weak entries (per batch manifest)*: 12

### `batch_turbulence_heating_apj` (10 skills)

- *Framing*: solar-wind-turbulence-heating-apj-aa
- *Theme*: `solar-wind-turbulence-heating-apj-aa`
- *Quality distribution*: pilot=10
- *Executable-status distribution*: scaffold=10
- *Year distribution*: 2022=4, 2024=3, 2021=1, 2023=1, 2025=1
- *Weak entries (per batch manifest)*: 10

### `pilot_2026_and_runtime` (8 skills)

- *Framing*: general-purpose harness; HelioSI = heliophysics domain instantiation; skills + MCPs + harness triple
- *Quality distribution*: paper-grounded-pending-full-text=5, positioning-skill-not-executable-science=3
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=4, architecture-template-only=1, benchmark-design-template=1, constructive-pipeline-specified=1, manuscript-checklist-only=1
- *Year distribution*: 2026=8
- *Weak entries (per batch manifest)*: 6

### `pilot_turbulence` (8 skills)

- *Framing*: solar-wind-turbulence
- *Theme*: `solar-wind-turbulence`
- *Quality distribution*: pilot=7, pilot_weak_attribution=1
- *Executable-status distribution*: scaffold=8
- *Year distribution*: 2021=3, 2023=2, 2020=1, 2022=1, 2024=1
- *Weak entries (per batch manifest)*: 4

### `wave500_agent_runtime_eval_design_045` (45 skills)

- *Framing*: general-purpose harness; HelioSI = heliophysics domain instantiation; paper-skills are harness-agnostic agent-native scientific objects
- *Quality distribution*: positioning-skill-not-executable-science=45
- *Executable-status distribution*: design-pattern-extractor=28, benchmark-protocol-template=9, manuscript-checklist-only=8
- *Year distribution*: 2024=14, 2023=9, 2025=9, 2026=8, 2021=3, 2019=1, 2022=1

### `wave500_coronal_source_mapping_pfss_045` (45 skills)

- *Framing*: RUNTIME-NEUTRAL. Paper-skills do not assume a specific harness or agent framework. LingTai / Claude Code / Codex appear only as example adapters in Layer 3. .library/custom/pfss-tr
- *Quality distribution*: paper-grounded-pending-full-text=45
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=45
- *Year distribution*: 2025=15, 2026=12, 2024=11, 2023=5, 2022=2

### `wave500_inner_heliosphere_psp_solo_045` (45 skills)

- *Framing*: {"principle": "Paper-skills are harness-agnostic. LingTai, Claude Code, Codex, MCP servers, and notebook-driven workflows are adapters, not assumptions in the s
- *Quality distribution*: paper-grounded-pending-full-text=45
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=45
- *Year distribution*: 2025=13, 2026=10, 2023=9, 2024=9, 2022=4
- *Weak entries (per batch manifest)*: 45

### `wave500_instruments_data_software_045` (45 skills)

- *Framing*: general-purpose harness; HelioSI = heliophysics domain instantiation; this wave adds infrastructure (instruments, data products, software, archives, open-science services) that eve
- *Quality distribution*: stub=32, method-ready=13
- *Executable-status distribution*: contract-specified-not-yet-benchmarked=45
- *Year distribution*: 2020=9, 1995=6, 2024=6, 1998=4, 2012=4, 2008=2, 2010=2, 2018=2, 1996=1, 1997=1, 2002=1, 2005=1, 2009=1, 2013=1, 2016=1, 2019=1, 2021=1, 2022=1

### `wave500_sep_shocks_space_weather_045` (45 skills)

- *Framing*: Skills are runtime-neutral and loadable by any general-purpose agent runtime (Claude Code, LingTai, Codex, Cursor, OpenAI Assistants, …). Named runtimes / MCPs / repos appear only 
- *Theme*: `solar-energetic-particles-shocks-icmes-cirs-space-weather-transients`
- *Quality distribution*: paper-grounded-pending-full-text=45
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=45
- *Year distribution*: 2026=21, 2025=17, 2024=7
- *Weak entries (per batch manifest)*: 45

### `wave500_solar_corona_cme_flares_045` (45 skills)

- *Framing*: RUNTIME-NEUTRAL. Paper-skills do not assume a specific harness or agent framework. LingTai and Claude Code appear only as example adapters in Layer 3 of individual SKILL.md files. 
- *Quality distribution*: paper-grounded-pending-full-text=45
- *Executable-status distribution*: pipeline-specified-not-yet-runnable=45
- *Year distribution*: TODO_verify=25, 2014=4, 2019=3, 2021=2, 1995=1, 2003=1, 2008=1, 2009=1, 2010=1, 2011=1, 2012=1, 2013=1, 2015=1, 2017=1, 2020=1
- *Weak entries (per batch manifest)*: 1

### `wave500_sw_classification_ml_foundation_045` (45 skills)

- *Framing*: harness-agnostic v0.2 — paper-skills + tool-skills are agent-native scientific objects; any sufficiently capable runtime (LingTai, Claude Code, MCP, Python notebook) is an adapter.
- *Theme*: `solar_wind_classification_segmentation_ml_foundation_event_detection_benchmarks`
- *Quality distribution*: stub=45
- *Executable-status distribution*: stub=45
- *Year distribution*: 2025=21, 2024=6, 2018=4, 2020=4, 2022=4, 2019=2, 2023=2, 2014=1, 2017=1

### `wave500_turbulence_intermit_heating_045` (45 skills)

- *Theme*: `turbulence, intermittency, heating, cascade physics (paper-skills)`
- *Quality distribution*: stub=45
- *Executable-status distribution*: null=45
- *Year distribution*: 2025=12, 2023=10, 2024=9, 2022=6, 2021=3, 2026=3, 2020=2

### `wave500_waves_instabilities_reconnection_045` (45 skills)

- *Framing*: {"principle": "Paper-skills are harness-agnostic. LingTai, Claude Code, Codex, Cursor, OpenAI Assistants are adapter examples, not assumptions in the skill body
- *Quality distribution*: stub=45
- *Executable-status distribution*: contract-spec-only-not-yet-runnable=45
- *Year distribution*: 2025=21, 2026=8, 2024=7, 2023=5, 2022=2, 2010=1, 2018=1
- *Weak entries (per batch manifest)*: 45

## 6. Global distributions across all 501 skills

### 6a. Quality tier

| Quality tier | Count |
|---|---|
| `paper-grounded-pending-full-text` | 217 |
| `stub` | 184 |
| `positioning-skill-not-executable-science` | 48 |
| `pilot` | 29 |
| `method-ready` | 20 |
| `paper-grounded-locally-reproduced` | 1 |
| `link-only-cross-batch` | 1 |
| `pilot_weak_attribution` | 1 |

### 6b. Executable status

| Executable status | Count |
|---|---|
| `pipeline-specified-not-yet-runnable` | 218 |
| `contract-spec-only-not-yet-runnable` | 53 |
| `contract-specified-not-yet-benchmarked` | 46 |
| `stub` | 45 |
| `null` | 45 |
| `scaffold` | 30 |
| `design-pattern-extractor` | 28 |
| `manuscript-checklist-only` | 9 |
| `benchmark-protocol-template` | 9 |
| `pipeline-specified-not-yet-benchmarked` | 4 |
| `review-routing-not-runnable` | 2 |
| `historical-citation-only` | 1 |
| `pipeline-specified-runnable-from-cached-magnetogram` | 1 |
| `pipeline-specified-runnable-from-spice` | 1 |
| `pipeline-specified-runnable-from-pyspedas` | 1 |
| `examples-only-not-yet-benchmarked` | 1 |
| `ecosystem-diff-procedure-only` | 1 |
| `pipeline-specified-runnable-from-cdas-or-hapi` | 1 |
| `locally-reproduced-via-nspf-fem` | 1 |
| `see-pilot-2026-and-runtime-skill` | 1 |
| `constructive-pipeline-specified` | 1 |
| `architecture-template-only` | 1 |
| `benchmark-design-template` | 1 |

### 6c. Source type / category

| Source type | Count |
|---|---|
| `null` | 120 |
| `heliophysics-method` | 104 |
| `scientific-method` | 102 |
| `agent-runtime-positioning` | 34 |
| `primary-observation` | 21 |
| `paper` | 21 |
| `software-package` | 19 |
| `software-paper` | 17 |
| `primary-observation-modeling` | 12 |
| `scientific-discovery-evaluation` | 9 |
| `data-contract-spec` | 8 |
| `primary-observation-statistical` | 7 |
| `primary-simulation` | 5 |
| `primary-observation-methodology` | 3 |
| `positioning-comparison` | 3 |
| `data-product-spec` | 2 |
| `review-routing-hub` | 2 |
| `primary-modeling` | 2 |
| `primary-observation-catalog` | 2 |
| `domain-knowledge-compilation` | 2 |
| `primary-observation-ml` | 2 |
| `calibration-recipe` | 1 |
| `applied-suite-workflow` | 1 |
| `cross-batch-link` | 1 |
| `primary-method` | 1 |

> `null` here means the batch did not author a `source_type`/`category`/`compilation_type` field for the entry — it uses `theme`/`primary_theme` only. Treat such entries as `scientific-paper` by default.

### 6d. Year distribution

| Year | Count |
|---|---|
| 1995 | 7 |
| 1996 | 2 |
| 1997 | 1 |
| 1998 | 4 |
| 2002 | 1 |
| 2003 | 1 |
| 2005 | 1 |
| 2008 | 3 |
| 2009 | 2 |
| 2010 | 4 |
| 2011 | 1 |
| 2012 | 5 |
| 2013 | 2 |
| 2014 | 5 |
| 2015 | 2 |
| 2016 | 7 |
| 2017 | 2 |
| 2018 | 10 |
| 2019 | 8 |
| 2020 | 27 |
| 2021 | 17 |
| 2022 | 33 |
| 2023 | 49 |
| 2024 | 81 |
| 2025 | 118 |
| 2026 | 83 |
| TODO_verify | 25 |

### 6e. Harness-agnostic flag (where authored)

| `harness_agnostic` value | Count |
|---|---|
| `True` | 225 |
| `null` | 276 |

> `None` means the entry does not author the field — under v0.2 migration it should be treated as `true` for paper-skills authored as harness-agnostic and reviewed individually otherwise.

## 7. Research-generation map (v1 carried forward; v2 extension seeds)

*Authoritative v1 map*: `corpus_index.md §8 / corpus_manifest.json research_generation_map`. It enumerates 9 tensions (T1–T9) and 6 gaps (G1–G6) across the 96 baseline skills.

**v2 extension**:

The 9 tensions and 6 gaps from the v1 map carry forward unchanged. The wave500 batches add new cross-skill substrate (45 agent-runtime/eval design skills, 45 CME/coronal-imaging skills, expanded SEP/shock/wave catalog, etc). v2 does NOT author new tensions/gaps blindly — Layer-4 affordance authoring is a follow-up curation pass.

**Where wave500 batches plug into the v1 tensions/gaps (Layer-4 authoring TODO):**

- wave500_agent_runtime_eval_design_045 — design-pattern transplants (e.g. FunSearch search loop → PFSS-parameter search).
- wave500_coronal_source_mapping_pfss_045 — extends the open-flux/PFSS tension network (T6 in v1).
- wave500_solar_corona_cme_flares_045 — adds the CME-3D-reconstruction <-> SEP-connectivity bridge (new tension T10 candidate).
- wave500_sep_shocks_space_weather_045 — extends the IVA/VDA-bias and HCS-reconnection tensions (T4, T5 in v1).
- wave500_waves_instabilities_reconnection_045 — extends cyclotron / PDI / reconnection mechanism competition (T1 in v1).
- wave500_sw_classification_ml_foundation_045 — extends the segmentation-method overlap tension (T7 in v1).
- wave500_turbulence_intermit_heating_045 — extends 1/f / inertial-slope / anisotropy tension (T3 in v1).
- wave500_inner_heliosphere_psp_solo_045 — extends switchback-origin and PSP-SO radial-alignment tensions (T2, T8 in v1).
- wave500_instruments_data_software_045 — fills G1 (loader gap) for ISʘIS/EPD/Wind-MFI and pyspedas-style contracts.

These mappings are *seeds*, not authored Layer-4 affordances. A curation pass is required to write per-skill `research_generation_affordances[]` blocks tying specific wave500 skills to specific v1 tensions/gaps; this v2 roll-up does not perform that authoring (see `corpus_qa_report_v2.md` §6 for the recommended pass).

## 8. Where to look next

- `corpus_manifest_v2.json` — machine-readable form of every block in this index; one entry per skill (501 entries).
- `corpus_qa_report_v2.md` — explicit count audit, claim-boundary discipline, weak-entry detail by batch, recommended next curation steps.
- `corpus_manifest.json` / `corpus_index.md` / `corpus_qa_report.md` — v1 baseline (96-skill snapshot). Preserved unchanged for diff-able provenance.
- Each `<batch>/manifest.json` — authoritative per-batch source of truth; this index re-states.
- Each `<batch>/index.md` — batch-authored prose (theme, methodology, occasional Layer-4 affordances).
- `sioulas-reproduction/results/paper_skill_factory/` — factory spec, schema, template, migration note, README. Read `harness_agnostic_migration_note.md` for the v0.1 → v0.2 framing rules that underpin the whole corpus.
