---
name: heurekabench-2026-end-to-end-co-scientist-evaluation
description: Per-entry paper-skill in pilot_2026_and_runtime (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# heurekabench-2026-end-to-end-co-scientist-evaluation

> **Skill type:** *positioning / comparison* skill. Encodes the
> HeurekaBench benchmarking pattern so HelioSI can upgrade from a smoke-
> test benchmark (9/9 in 6.02 s) to paper-grounded, end-to-end co-
> scientist evaluation.

## When to use this paper-skill

Invoke when:

- Designing HelioSI's next-generation benchmark beyond the current
  smoke-test (9/9 skills execute in 6.02 s).
- Justifying benchmark scope to a reviewer who asks "how do you evaluate
  end-to-end scientific research, not single-turn answers?".
- Building a paper-grounded benchmark item: input = paper + repo + data
  product; expected output = published finding; artifact = report +
  metrics.
- Writing the Benchmark / Evaluation section of the HelioSI manuscript.

Do not invoke as a heliophysics computational skill — this is a benchmark-
design pattern, not a science workflow.

## Paper identity and claim boundary

- **Title:** HeurekaBench: A Benchmarking Framework for AI Co-scientist
- **Authors:** Siba Smarak Panigrahi, Jovana Videnović, Maria Brbić
- **arXiv:** 2601.01678 (2026-01-04)
- **Type:** benchmark framework paper
- **Claim boundary:** HeurekaBench proposes evaluating AI co-scientist
  systems via realistic, end-to-end research scenarios that integrate
  data analysis, interpretation, and the generation of new insights from
  experimental data. Each benchmark item is grounded in a scientific
  study and its corresponding code repository; a semi-automated pipeline
  extracts insights and candidate workflows and verifies them against
  reported findings. The paper does NOT prescribe a single domain; it
  prescribes a *pattern* applicable to any AI co-scientist.

## Methodological pattern to operationalize (for HelioSI benchmark design)

A HeurekaBench-style item has five required parts; HelioSI's next-level
benchmark should adopt all of them:

1. **Anchor paper** — a published heliophysics study with a clear claim.
2. **Code repository** — the official repo or a reproducible community
   one.
3. **Data product** — named archive items (e.g. PSP encounter X SWEAP +
   FIELDS L2 for date Y).
4. **Expected finding** — a published quantitative result (spectral
   index, conjunction Δv, classification rate, ...).
5. **Verification pipeline** — semi-automated extraction of the
   candidate workflow and comparison to the expected finding.

**HelioSI mapping:**

| HeurekaBench part | HelioSI realization |
|---|---|
| Anchor paper | Each paper-skill in this corpus (e.g. murtas-2026, mozer-2026, dakeyo-2026) is a candidate anchor |
| Code repository | HelioSI skill executable + cited author repo |
| Data product | CDAWeb / SOAR / PDS-PPI artifact ID + interval |
| Expected finding | The validation_targets field in each skill's metadata.yaml |
| Verification pipeline | HelioSI benchmark agent ingests skill, runs it, diffs against validation_targets |

## Required data / instruments / code / archives

- None for direct execution of this positioning skill.
- Required artifacts for using the skill: the HelioSI skill catalog
  (with each skill's `validation_targets` field), the benchmark agent
  source, and a reproducibility log format.

## Algorithm / workflow steps

When invoked by the benchmark-design agent:

1. **Enumerate paper-skills** in the corpus that have non-empty
   `validation_targets`.
2. **For each candidate, build a HeurekaBench-style item:**
   `{anchor_paper, repo, data_product, expected_finding,
   verification_pipeline}`.
3. **Reject** items lacking a paper-grounded `expected_finding` (mark
   "smoke test only").
4. **Sort items by feasibility.** Per the gap plan, the PSP turbulence
   reproduction (Sioulas-style; the existing
   `psp_turbulence_reproduction_panel.md`) is the cheapest and most
   defensible first item; the Murtas-2026 SEP-from-reconnection item is
   the most ambitious.
5. **Emit a benchmark manifest** with pass criteria, expected runtime,
   required compute, and required MCPs.
6. **Run** each item via the HelioSI benchmark agent and produce a per-
   item `metrics.json` and a top-level `summary.json`.

## Minimal executable benchmark or validation target

The "benchmark" for the benchmark-design skill is *meta*:

- HelioSI's benchmark set must contain at least **one paper-grounded
  HeurekaBench-style item** before claiming end-to-end evaluation.
- The item must execute end-to-end (data fetch → method → comparison)
  and produce a reproducible artifact set.
- Pass criterion: published finding reproduced within stated tolerance,
  artifact reproducible by an external reviewer.

## Known pitfalls / failure modes (for using this skill)

- **Reproducing the paper's numbers ≠ reproducing the paper's science.**
  If the published number was wrong (or the data has been re-calibrated),
  matching it can be misleading. Document the calibration version.
- **Reviewer-grade artifacts.** A HeurekaBench-style item must include
  enough to let an external reviewer rerun the pipeline; missing data
  citations or code commit hashes break the bench.
- **Cherry-picked items.** Choosing only the easiest reproductions is the
  HeurekaBench analogue of a McNamara fallacy (cf. Bisht critique).
  Include at least one hard case.
- **Confusing throughput with rigor.** Reporting "9/9 in 6.02 s" without
  a paper-grounded item is a *smoke test*, not a HeurekaBench score.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2601.01678 as an Anthropic-
style **benchmark-design Skill** — not a heliophysics method. It is
loaded by the HelioSI runtime to build, schedule, and score paper-
grounded end-to-end benchmark items.

| Paper element | Agent-native form |
|---|---|
| Claim — "co-scientist evaluation needs realistic, end-to-end, paper+repo+data+expected-finding items" | **Verifiable task:** `build_bench_item(paper_skill_slug) -> {anchor, repo, data_product, expected_finding, verification_pipeline}` |
| Methods / arguments — 5-part item structure + semi-automated workflow extraction | **Executable workflow:** §"Algorithm / workflow steps" 1–6 — enumerate paper-skills, construct items, sort by feasibility, run, score |
| Data / sources / code — the HelioSI skill catalog and each skill's `validation_targets` *are* the input data | **MCP / tool contracts:** filesystem reader for the skill corpus; `cdaweb-mcp`/`soar-mcp`/`pds-ppi-mcp` for data fetching; `hpc-runner-mcp` for compute; `git-mcp` for artifact versioning |
| Caveats / failure modes — reproducing numbers ≠ reproducing science; reviewer-grade artifacts; cherry-picked items; throughput vs rigor | **Skill memory:** §"Known pitfalls / failure modes" — runtime rejects bench items lacking commit-hash + data-version + tolerance |
| Figures / results — benchmark score tables / item dashboards | **Benchmark artifacts:** per-item `metrics.json`, top-level `summary.json`, reproducibility manifest |

Compiling this paper as a Skill is what *upgrades* HelioSI's current
9/9-in-6.02-s smoke test into a defensible HeurekaBench-style score —
the cheapest first item being the PSP turbulence reproduction noted in
the gap plan.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** invoked by the benchmark-design and manuscript-
  evaluation sub-graphs.
- **Skills it composes with:**
  - [[agentic-ai-scientists-not-built-autonomous-discovery-2026]] —
    end-to-end benchmarking is one of Bisht's explicit recommendations.
  - [[mind-ai-co-scientist-material-research-2026]] — provides the
    architecture loop that HeurekaBench items measure.
  - All heliophysics paper-skills in this pilot corpus — they are the
    *candidate anchor papers*.
- **MCPs it would use:** `cdaweb-mcp`, `soar-mcp`, `pds-ppi-mcp` for
  data fetching; `hpc-runner-mcp` for compute; `git-mcp` for repo
  versioning of bench artifacts.
- **HelioSI manuscript role:** the dominant template for the Benchmark
  / Evaluation section. The gap plan flags upgrading from smoke-test to
  HeurekaBench-style evaluation as the single most impactful next move
  (`heliosi_similar_papers_requirements_gap_plan.md` §0).

## References

- Panigrahi, S. S., Videnović, J., Brbić, M. (2026). HeurekaBench: A
  Benchmarking Framework for AI Co-scientist. arXiv:2601.01678.
- Inventory: `sioulas-reproduction/results/agent_runtime_2026_only_synthesis.md`
  §1.8; `heliosi_similar_papers_requirements_gap_plan.md` §0 and §2.2.
