# wave500 — agent-runtime / scientific-discovery-evaluation / benchmarks / domain-knowledge-compilation (45 paper-skills)

> Generated 2026-05-18 by the HelioSI paper-to-skill factory
> (`paper_skill_factory/`, spec v0.2). Dispatcher: `HelioSI paper-to-skill factory`
> (Claude Opus 4.7). This batch grows the HelioSI paper-skill corpus from
> 96 → 141 entries on the way to the 500-object HelioSI target.

## What this batch is

A single large dispatch of **45 harness-agnostic paper-skills** drawn
from:

- **AI scientist / scientific agent-runtime systems** (Lu 2024, Yamada
  2025, Schmidgall 2025, Gottweis 2025, Su 2024, Boiko 2023, Bran 2024,
  Ghafarollahi 2025, Lyu 2026, Wu 2026 Medical, Wu 2026 Ranking, Younis
  2026 CoDHy, Rahgozar 2026, Goel 2025, Hong 2023 MetaGPT, Zheng 2024
  OpenDevin)
- **Scientific-discovery evaluation / benchmarks** (Yin 2024 Turing
  Tests, Son 2025 SPOT, Panigrahi 2026 HeurekaBench-construction,
  Jansen 2024 DiscoveryWorld, Majumder 2024 DiscoveryBench, Tian 2024
  SciCode, Mialon 2023 GAIA, Zhou 2023 WebArena, Jimenez 2024 SWE-bench)
- **Foundational agent methods** (Yao 2022 ReAct, Shinn 2023 Reflexion,
  Wang 2023 Voyager, Park 2023 Generative Agents, Yang 2024 SWE-agent)
- **AI-scientist comparison / surveys / critiques** (Wei 2025 Agentic
  Science survey, Zhu 2025 Implementation critique, Xie 2025 How Far,
  Guo 2024 Multi-Agents survey, Xi 2023 LLM-Agents survey, Kambhampati
  2024 LLM-Modulo, Bommasani 2021 Foundation Models, llmtreesearch-2026
  multi-pathogen + 3d-photovoltaic)
- **Domain knowledge compilation / domain-specific foundation models**
  (Romera-Paredes 2024 FunSearch, Trinh 2024 AlphaGeometry, Jumper 2021
  AlphaFold2, Merchant 2023 GNoME)
- **Heliophysics-specific evaluation/design** (McGranaghan 2021,
  Camporeale 2019)

These complement — and do not duplicate — the 3 positioning skills
already in `pilot_2026_and_runtime/` (Bisht 2026 critique, MIND 2026,
HeurekaBench 2026 positioning), and the 88 heliophysics-method skills
in the other batches.

## How each entry is structured

Every entry follows the v0.2 four-layer model. For positioning /
evaluation / design-pattern skills the layer loading is shifted:

| Layer | What it carries here |
|-------|----------------------|
| L1 — Scientific invariant | The paper's narrow claim + `claim_boundary` + failure modes |
| L2 — Executable protocol | The paper's method as an abstract callable a runtime can borrow |
| L3 — Adapter binding examples | Intentionally **empty** for this batch (harness-agnostic) |
| L4 — Research-generation affordance | **Explicit statement of how the paper helps HelioSI generate or evaluate new heliophysics ideas** |

Layer 4 is the load-bearing layer of this batch: each SKILL.md ends with
a `gap` / `tension` / `hypothesis` / `minimal_experiment` block whose
target is "useful for the HelioSI Stage-D research-generation loop" —
not "useful for heliophysics data analysis on its own".

## Honest tier + executable_status labelling

All 45 entries are marked at:

- **quality**: `positioning-skill-not-executable-science`
- **harness_agnostic**: `true`
- **source_type**: one of
  `agent-runtime-positioning` / `scientific-discovery-evaluation` /
  `domain-knowledge-compilation`
- **executable_status**: one of
  `design-pattern-extractor` / `manuscript-checklist-only` /
  `benchmark-protocol-template`

A reader who sees these tags should understand: these skills do not
process mission data. Composing them into a heliophysics data pipeline
is a category error. They EITHER (a) audit HelioSI manuscript/benchmark
claims, OR (b) supply design patterns the HelioSI runtime can borrow,
OR (c) seed the Stage-D hypothesis-generation loop.

## Coverage table (45 entries)

| # | Slug | arXiv / DOI | Year | Category | Source type | Executable status |
|---|------|-------------|------|----------|-------------|-------------------|
| 1 | [paper-lu-2024-ai-scientist-fully-automated-discovery](./paper-lu-2024-ai-scientist-fully-automated-discovery/SKILL.md) | arXiv:2408.06292 | 2024 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 2 | [paper-yamada-2025-ai-scientist-v2-agentic-tree-search](./paper-yamada-2025-ai-scientist-v2-agentic-tree-search/SKILL.md) | arXiv:2504.08066 | 2025 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 3 | [paper-schmidgall-2025-agent-laboratory-research-assistants](./paper-schmidgall-2025-agent-laboratory-research-assistants/SKILL.md) | arXiv:2501.04227 | 2025 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 4 | [paper-gottweis-2025-ai-co-scientist-multi-agent-gemini](./paper-gottweis-2025-ai-co-scientist-multi-agent-gemini/SKILL.md) | arXiv:2502.18864 | 2025 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 5 | [paper-su-2024-virsci-multi-agent-idea-generation](./paper-su-2024-virsci-multi-agent-idea-generation/SKILL.md) | arXiv:2410.09403 | 2024 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 6 | [paper-boiko-2023-coscientist-autonomous-chemistry-nature](./paper-boiko-2023-coscientist-autonomous-chemistry-nature/SKILL.md) | doi:10.1038/s41586-023-06792-0 | 2023 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 7 | [paper-bran-2024-chemcrow-augmenting-llms-chemistry-tools](./paper-bran-2024-chemcrow-augmenting-llms-chemistry-tools/SKILL.md) | doi:10.1038/s42256-024-00832-8 | 2024 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 8 | [paper-ghafarollahi-2025-sciagents-bioinspired-multi-agent-graph](./paper-ghafarollahi-2025-sciagents-bioinspired-multi-agent-graph/SKILL.md) | doi:10.1002/adma.202413523 | 2025 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 9 | [paper-wei-2025-agentic-science-survey-autonomous-discovery](./paper-wei-2025-agentic-science-survey-autonomous-discovery/SKILL.md) | arXiv:2508.14111 | 2025 | survey | agent-runtime-positioning | manuscript-checklist-only |
| 10 | [paper-zhu-2025-ai-scientists-fail-without-implementation](./paper-zhu-2025-ai-scientists-fail-without-implementation/SKILL.md) | arXiv:2506.01372 | 2025 | critique | agent-runtime-positioning | manuscript-checklist-only |
| 11 | [paper-xie-2025-how-far-ai-scientists-changing-world](./paper-xie-2025-how-far-ai-scientists-changing-world/SKILL.md) | arXiv:2507.23276 | 2025 | survey | agent-runtime-positioning | manuscript-checklist-only |
| 12 | [paper-yin-2024-turing-tests-ai-scientist-benchmark](./paper-yin-2024-turing-tests-ai-scientist-benchmark/SKILL.md) | arXiv:2405.13352 | 2024 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 13 | [paper-lyu-2026-evoscientist-evolving-multi-agent](./paper-lyu-2026-evoscientist-evolving-multi-agent/SKILL.md) | arXiv:2603.08127 | 2026 | ai-scientist-system | agent-runtime-positioning | design-pattern-extractor |
| 14 | [paper-hwu-2026-medical-ai-scientist-clinical-research](./paper-hwu-2026-medical-ai-scientist-clinical-research/SKILL.md) | arXiv:2603.28589 | 2026 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 15 | [paper-liweiwu-2026-ai-co-scientist-ranking-search-models](./paper-liweiwu-2026-ai-co-scientist-ranking-search-models/SKILL.md) | arXiv:2603.22376 | 2026 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 16 | [paper-younis-2026-codhy-biomarker-drug-hypothesis](./paper-younis-2026-codhy-biomarker-drug-hypothesis/SKILL.md) | arXiv:2603.00612 | 2026 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 17 | [paper-rahgozar-2026-ai-co-scientist-knowledge-synthesis-medical](./paper-rahgozar-2026-ai-co-scientist-knowledge-synthesis-medical/SKILL.md) | arXiv:2601.11825 | 2026 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 18 | [paper-goel-2025-rubric-rewards-training-ai-co-scientists](./paper-goel-2025-rubric-rewards-training-ai-co-scientists/SKILL.md) | arXiv:2512.23707 | 2025 | training-methodology | agent-runtime-positioning | design-pattern-extractor |
| 19 | [paper-son-2025-spot-benchmark-verification-scientific](./paper-son-2025-spot-benchmark-verification-scientific/SKILL.md) | arXiv:2505.11855 | 2025 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 20 | [paper-panigrahi-2026-heurekabench-pipeline-construction-method](./paper-panigrahi-2026-heurekabench-pipeline-construction-method/SKILL.md) | arXiv:2601.01678 | 2026 | benchmark-construction-method | scientific-discovery-evaluation | benchmark-protocol-template |
| 21 | [paper-llmtreesearch-2026-multi-pathogen-disease-forecasting](./paper-llmtreesearch-2026-multi-pathogen-disease-forecasting/SKILL.md) | arXiv:2605.16238 | 2026 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 22 | [paper-llmtreesearch-2026-3d-photovoltaic-structures](./paper-llmtreesearch-2026-3d-photovoltaic-structures/SKILL.md) | arXiv:2605.16191 | 2026 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 23 | [paper-guo-2024-llm-multi-agents-progress-challenges-survey](./paper-guo-2024-llm-multi-agents-progress-challenges-survey/SKILL.md) | arXiv:2402.01680 | 2024 | survey | agent-runtime-positioning | manuscript-checklist-only |
| 24 | [paper-jansen-2024-discoveryworld-virtual-discovery-benchmark](./paper-jansen-2024-discoveryworld-virtual-discovery-benchmark/SKILL.md) | arXiv:2406.06769 | 2024 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 25 | [paper-majumder-2024-discoverybench-data-driven-discovery](./paper-majumder-2024-discoverybench-data-driven-discovery/SKILL.md) | arXiv:2407.01725 | 2024 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 26 | [paper-tian-2024-scicode-research-coding-benchmark](./paper-tian-2024-scicode-research-coding-benchmark/SKILL.md) | arXiv:2407.13168 | 2024 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 27 | [paper-mialon-2023-gaia-general-ai-assistants-benchmark](./paper-mialon-2023-gaia-general-ai-assistants-benchmark/SKILL.md) | arXiv:2311.12983 | 2023 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 28 | [paper-yao-2022-react-reasoning-acting-language-models](./paper-yao-2022-react-reasoning-acting-language-models/SKILL.md) | arXiv:2210.03629 | 2022 | foundational-method | agent-runtime-positioning | design-pattern-extractor |
| 29 | [paper-shinn-2023-reflexion-verbal-reinforcement-agents](./paper-shinn-2023-reflexion-verbal-reinforcement-agents/SKILL.md) | arXiv:2303.11366 | 2023 | foundational-method | agent-runtime-positioning | design-pattern-extractor |
| 30 | [paper-wang-2023-voyager-open-ended-embodied-agent-llm](./paper-wang-2023-voyager-open-ended-embodied-agent-llm/SKILL.md) | arXiv:2305.16291 | 2023 | foundational-method | agent-runtime-positioning | design-pattern-extractor |
| 31 | [paper-park-2023-generative-agents-interactive-simulacra](./paper-park-2023-generative-agents-interactive-simulacra/SKILL.md) | arXiv:2304.03442 | 2023 | foundational-method | agent-runtime-positioning | design-pattern-extractor |
| 32 | [paper-zhou-2023-webarena-realistic-web-agent-benchmark](./paper-zhou-2023-webarena-realistic-web-agent-benchmark/SKILL.md) | arXiv:2307.13854 | 2023 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 33 | [paper-jimenez-2024-swebench-resolving-github-issues](./paper-jimenez-2024-swebench-resolving-github-issues/SKILL.md) | arXiv:2310.06770 | 2024 | benchmark | scientific-discovery-evaluation | benchmark-protocol-template |
| 34 | [paper-yang-2024-swe-agent-language-model-software-engineer](./paper-yang-2024-swe-agent-language-model-software-engineer/SKILL.md) | arXiv:2405.15793 | 2024 | agent-system | agent-runtime-positioning | design-pattern-extractor |
| 35 | [paper-romera-paredes-2024-funsearch-mathematical-program-search](./paper-romera-paredes-2024-funsearch-mathematical-program-search/SKILL.md) | doi:10.1038/s41586-023-06924-6 | 2024 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 36 | [paper-trinh-2024-alphageometry-neuro-symbolic-olympiad](./paper-trinh-2024-alphageometry-neuro-symbolic-olympiad/SKILL.md) | doi:10.1038/s41586-023-06747-5 | 2024 | domain-specific-ai-scientist | agent-runtime-positioning | design-pattern-extractor |
| 37 | [paper-jumper-2021-alphafold2-protein-structure-prediction](./paper-jumper-2021-alphafold2-protein-structure-prediction/SKILL.md) | doi:10.1038/s41586-021-03819-2 | 2021 | domain-specific-foundation-model | domain-knowledge-compilation | design-pattern-extractor |
| 38 | [paper-merchant-2023-gnome-graph-networks-materials-discovery](./paper-merchant-2023-gnome-graph-networks-materials-discovery/SKILL.md) | doi:10.1038/s41586-023-06735-9 | 2023 | domain-specific-foundation-model | domain-knowledge-compilation | design-pattern-extractor |
| 39 | [paper-bommasani-2021-foundation-models-opportunities-risks](./paper-bommasani-2021-foundation-models-opportunities-risks/SKILL.md) | arXiv:2108.07258 | 2021 | survey | agent-runtime-positioning | manuscript-checklist-only |
| 40 | [paper-xi-2023-rise-potential-llm-agents-survey](./paper-xi-2023-rise-potential-llm-agents-survey/SKILL.md) | arXiv:2309.07864 | 2023 | survey | agent-runtime-positioning | manuscript-checklist-only |
| 41 | [paper-kambhampati-2024-llm-modulo-frameworks-planning-verifier](./paper-kambhampati-2024-llm-modulo-frameworks-planning-verifier/SKILL.md) | arXiv:2402.01817 | 2024 | critique | agent-runtime-positioning | design-pattern-extractor |
| 42 | [paper-mcgranaghan-2021-machine-learning-heliophysics-perspective](./paper-mcgranaghan-2021-machine-learning-heliophysics-perspective/SKILL.md) | (TODO_verify) | 2021 | heliophysics-evaluation-design | agent-runtime-positioning | manuscript-checklist-only |
| 43 | [paper-camporeale-2019-challenge-machine-learning-space-weather](./paper-camporeale-2019-challenge-machine-learning-space-weather/SKILL.md) | doi:10.1029/2018SW002061 | 2019 | heliophysics-evaluation-design | agent-runtime-positioning | manuscript-checklist-only |
| 44 | [paper-hong-2023-metagpt-meta-programming-multi-agent](./paper-hong-2023-metagpt-meta-programming-multi-agent/SKILL.md) | arXiv:2308.00352 | 2023 | agent-system | agent-runtime-positioning | design-pattern-extractor |
| 45 | [paper-zheng-2024-opendevin-open-platform-ai-software-developers](./paper-zheng-2024-opendevin-open-platform-ai-software-developers/SKILL.md) | arXiv:2407.16741 | 2024 | agent-system | agent-runtime-positioning | design-pattern-extractor |

## Cross-corpus integration notes

- **No duplicate slugs** with the existing 96-skill corpus (verified
  against all 9 batches via filesystem walk on 2026-05-18).
- The three 2026 positioning skills already in
  `pilot_2026_and_runtime/` (Bisht critique 2026, MIND 2026,
  HeurekaBench 2026 positioning) remain authoritative for their
  papers; this batch covers a *different* angle for the Panigrahi
  HeurekaBench paper (the **construction method**, slug
  `paper-panigrahi-2026-heurekabench-pipeline-construction-method`),
  not the same positioning slug.
- The 11 ML/segmentation skills in
  `batch_solar_wind_segmentation_ml/` are the natural Layer-4 targets
  for the McGranaghan 2021 and Camporeale 2019 design-review skills
  here.
- Layer-4 affordances frequently reference sibling heliophysics
  paper-skills via `[[paper-...]]` links; these are graph-walker hints,
  not hard dependencies.

## Source inventories used

- `sioulas-reproduction/results/agent_runtime_paper_scan_raw.md`
- `sioulas-reproduction/results/agent_runtime_2026_only_synthesis.md`
- `sioulas-reproduction/results/agent_runtime_additional_exact_metadata.md`
- `sioulas-reproduction/results/agent_runtime_comparable_papers_synthesis.md`
- `sioulas-reproduction/results/heliosi_similar_papers_requirements_gap_plan.md`
- External arXiv IDs / Nature DOIs (foundational agent literature and
  domain-knowledge-compilation precedents — DiscoveryWorld,
  DiscoveryBench, SciCode, GAIA, ReAct, Reflexion, Voyager, Generative
  Agents, WebArena, SWE-bench, SWE-agent, FunSearch, AlphaGeometry,
  AlphaFold2, GNoME, Foundation Models report, Xi 2023 survey,
  Kambhampati LLM-Modulo, MetaGPT, OpenDevin, McGranaghan 2021,
  Camporeale 2019). All such external identifiers carry an explicit
  TODO_verify_with_full_text expectation in the per-skill metadata
  before any promotion past stub tier.

## Validation summary

- Total directories under this batch: **45** (excluding `manifest.json`,
  `index.md`).
- Total `SKILL.md` files: **45**.
- Total `metadata.yaml` files: **45**.
- Duplicate slugs vs. existing 96-skill corpus: **0**.
- All entries marked `harness_agnostic: true`; all entries carry
  populated `claim_boundary.scope` + `claim_boundary.out_of_scope` +
  `failure_modes` + `research_generation_affordances`.

## Corpus running total after this batch

| Stage | Count | Source |
|-------|------:|--------|
| Baseline (before wave500) | 96 | `corpus_manifest.json` totals |
| wave500_agent_runtime_eval_design_045 (this batch) | +45 | this `index.md` |
| **New running total** | **141** | toward 500-object target |
