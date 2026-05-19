# heliosi-501-corpus — Bundle validation

Generated: 2026-05-18  
Bundle root: this repository (`heliosi-501-corpus-skill/`).

## 0. Reproducing this report

Every check below is also wrapped in a single reproducible entry point
(see GitHub issue #38):

```bash
bash scripts/validate.sh        # quiet on success, non-zero on first failure
bash scripts/validate.sh -v     # verbose: echo each individual check
```

The script asserts §1 filesystem counts, the §2 manifest cross-check,
§3 v2 roll-up file presence, and the §4a–§4d helper-script smoke commands
(plus a §4e `--version` consistency check). It uses Python 3 stdlib + bash
only and resolves paths relative to itself, so it can be run from any cwd
as long as the bundle layout is intact.

## 1. Structural counts

| Check | Expected | Actual | Pass |
|---|---:|---:|:---:|
| Aggregator `SKILL.md` at bundle root | 1 | 1 | ✓ |
| Batch directories under `references/corpus/` | 18 | 18 | ✓ |
| Per-entry `SKILL.md` under `references/corpus/` (excludes aggregator) | 501 | 501 | ✓ |
| Per-entry `metadata.yaml` under `references/corpus/` | 501 | 501 | ✓ |
| Bundle size on disk | ~7–10 MB | **7.8 MB** | ✓ |

Per-entry SKILL.md count produced by:

```bash
find references/corpus -mindepth 2 -maxdepth 3 -name 'SKILL.md' | wc -l   # → 501
find references/corpus -name 'metadata.yaml' | wc -l                       # → 501
ls -d references/corpus/*/ | wc -l                                         # → 18
```

The bundle's own `SKILL.md` (the aggregator) lives at `./SKILL.md` and is **not** under `references/corpus/`, so it is explicitly excluded from the 501 count.

## 2. Manifest JSON validation

`references/corpus_manifest_v2.json` parses with Python 3 stdlib `json.load`. Required cross-checks:

```text
schema_version:                  rollup-2.0
totals.batches:                  18
totals.skills_in_manifests:      501
totals.unique_slugs:             501
totals.duplicate_slugs:          {}
len(entries):                    501
len(batches):                    18
```

Re-verification one-liner (from the bundle root):

```bash
python3 -c "import json; m=json.load(open('references/corpus_manifest_v2.json')); t=m['totals']; assert t['skills_in_manifests']==len(m['entries'])==501; assert t['batches']==len(m['batches'])==18; assert not t['duplicate_slugs']; print('OK', t)"
```

## 3. Top-level v2 roll-up files present

| File | Present | Size |
|---|:---:|---:|
| `references/corpus_index_v2.md` | ✓ | ~27 KB |
| `references/corpus_qa_report_v2.md` | ✓ | ~20 KB |
| `references/corpus_manifest_v2.json` | ✓ | ~565 KB |

## 4. Helper-script smoke tests

### 4a. `python3 scripts/search_corpus.py --query PFSS --limit 5`

```
matches: 60 (showing 5)  query='PFSS'  in=manifest
--------------------------------------------------------------------------------
paper-stansby-2020-pfsspy-python-pfss
  batch: batch_heliophysics_software_infrastructure  year: 2020
  quality: method-ready  status: pipeline-specified-runnable-from-cached-magnetogram
  title: pfsspy: a Python package for Potential Field Source Surface extrapolations ...
paper-sunkit-magex-magnetic-field-extrapolation
  batch: batch_heliophysics_software_infrastructure  year: 2023
  quality: method-ready  status: pipeline-specified-not-yet-benchmarked
  title: sunkit-magex: SunPy-affiliated magnetic-field extrapolation package
pfss-test-problems-solar-stellar-magnetic-fields
  batch: batch_pfss_source_mapping  year: 2022
  quality: paper-grounded-pending-full-text  status: pipeline-specified-not-yet-runnable
  title: Test Problems for Potential Field Source Surface Extrapolations ...
multi-constraint-pfss-extrapolation-model
  batch: batch_pfss_source_mapping  year: 2026
  quality: paper-grounded-pending-full-text  status: pipeline-specified-not-yet-runnable
  title: A New Multi-Constraint Potential Field Source Surface (PFSS) Extrapolation Model
ai-farside-synchronic-coronal-field-extrapolation
  batch: batch_pfss_source_mapping  year: 2020
  quality: paper-grounded-pending-full-text  status: pipeline-specified-not-yet-runnable
  title: Solar Coronal Magnetic Field Extrapolation from Synchronic Data with AI-generated Farside
```

→ 60 total hits across the corpus, 5 shown. Confirms the manifest is wired, fields render, and paths exist.

### 4b. `python3 scripts/search_corpus.py --maturity`

```
maturity tiers (from corpus_manifest_v2.json)
--------------------------------------------------------------------------------
  T1_locally_reproduced                            1
  T2_method_ready_executable_pilot                22
  T3_paper_grounded_pending_full_text            260
  T4_stub_or_scaffold_paper_grounded             164
  T5_agent_runtime_or_design_precedent            52
  T6_link_only_or_routing                          1
  T7_weak_attribution_or_citation_todo             1
--------------------------------------------------------------------------------
  TOTAL                                          501
```

→ Tier counts match `corpus_qa_report_v2.md` §4 (1 + 22 + 260 + 164 + 52 + 1 + 1 = 501).

### 4c. `python3 scripts/search_corpus.py --batches`

18 rows, total = 501. Per-batch counts match the QA report §1 table exactly:

```
batch_heliophysics_software_infrastructure      12
batch_mission_instruments_data_products         12
batch_pfss_source_mapping                       10
batch_psp_switchbacks_magnetic                  12
batch_sep_energetic_particles                   12
batch_solar_wind_segmentation_ml                12
batch_turbulence_heating_apj                    10
pilot_2026_and_runtime                           8
pilot_turbulence                                 8
wave500_agent_runtime_eval_design_045           45
wave500_coronal_source_mapping_pfss_045         45
wave500_inner_heliosphere_psp_solo_045          45
wave500_instruments_data_software_045           45
wave500_sep_shocks_space_weather_045            45
wave500_solar_corona_cme_flares_045             45
wave500_sw_classification_ml_foundation_045     45
wave500_turbulence_intermit_heating_045         45
wave500_waves_instabilities_reconnection_045    45
--------------------------------------------------------------------------------
total skills:                                  501
```

### 4d. `python3 scripts/search_corpus.py --show wu-2026-nonspherical-coronal-magnetic-field-open-flux`

Returns absolute paths for both `SKILL.md` and `metadata.yaml`, both reported `exists=True`. This is the sole T1 (locally reproduced) entry.

### 4e. `python3 scripts/audit_internalization_readiness.py --top 30`

Scores all 501 entries on bibliographic anchor + Layer-1 claim + Layer-2 protocol + validation + Layer-4 affordance + identity, with a TODO-density penalty. Exits 0 by default and prints a ranked worst-debt list; intended as a **non-blocking** debt thermometer rather than a CI gate. The optional `--strict-active` mode raises a non-zero exit only when entries flagged as active drop below `--min-active-score` (default 55), keeping the corpus's existing 85 % T3+T4 debt out of CI.

Companion artifacts under `reports/`:

- `reports/internalization_readiness_report.md` — worst-debt ranking, per-batch recommendations, and concrete next parallel batches for content-internalization daemons.
- `reports/internalization_readiness_audit.json` — compact JSON summary (top-100 worst entries, per-batch / per-quality means, top-30 worst active).

Stability invariants are pinned by `tests/test_internalization_readiness.py` (22 tests: 7 unit signal tests, 5 fixture-corpus tests, 10 live-corpus invariants).

## 5. SKILL.md aggregator integrity

- Frontmatter present with `name: heliosi-501-corpus`, trigger-only `description`, `allowed-tools: Read, Grep, Glob, Bash`.
- Body instructs Claude to start from `references/corpus_index_v2.md` and `corpus_qa_report_v2.md`, then use `scripts/search_corpus.py` or grep, then read at most a few per-entry SKILL.md files.
- Workflows for (1) inventory, (2) topical search, (3) hypothesis from cross-skill tension, (4) full-text-verification triage, and (5) corpus-entry → runtime experiment plan are all enumerated.
- Safe / unsafe claim lists copy faithfully from `corpus_qa_report_v2.md` §3 and §5.

## 6. Acceptance summary

| Requirement | Status |
|---|:---:|
| Exactly 501 per-entry SKILL.md under `references/corpus` (aggregator excluded) | ✓ |
| Exactly 501 metadata.yaml under `references/corpus` | ✓ |
| 18 batch directories under `references/corpus` | ✓ |
| `corpus_manifest_v2.json` parses; declares 501 skills + 18 batches; `duplicate_slugs == {}` | ✓ |
| v2 roll-up files (`corpus_index_v2.md`, `corpus_qa_report_v2.md`, `corpus_manifest_v2.json`) copied | ✓ |
| `scripts/search_corpus.py` runs stdlib-only; `--query`, `--maturity`, `--batches`, `--show` all green | ✓ |
| Aggregator `SKILL.md` with trigger-only description, four workflows, claim boundaries | ✓ |
| `README.md` with Claude Code install instructions + smoke command | ✓ |
| Bundle self-contained (no symlinks out, no network) | ✓ |
| Source corpus untouched; `.library/custom` untouched | ✓ |

**Bundle is ready to install and smoke-test.**
