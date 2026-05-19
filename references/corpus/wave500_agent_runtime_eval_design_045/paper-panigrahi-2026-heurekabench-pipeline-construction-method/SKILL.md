---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-panigrahi-2026-heurekabench-pipeline-construction-method
description: >-
  Use when the agent is positioning HelioSI against benchmark-construction-method literature, borrowing a scientific-discovery-end-to-end-benchmark-pipeline design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "A semi-automated pipeline (multi-LLM insight extraction + workflow generation + verification against reported findings) constructs end-to-end benchmark items gr" (arXiv preprint 2026).
version: 0.1.0
kind: paper-skill
quality: positioning-skill-not-executable-science
harness_agnostic: true

layers:
  scientific_invariant: true
  executable_protocol: true
  adapter_binding_examples: false
  research_generation_affordance: true

paper:
  title: "HeurekaBench: A Benchmarking Framework for AI Co-scientist (pipeline-construction method)"
  first_author: "Panigrahi, S. S."
  authors: ["Siba Smarak Panigrahi", "Jovana Videnović", "Maria Brbić"]
  year: 2026
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2601.01678"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "scientific-discovery-end-to-end-benchmark-pipeline"]
  missions: []
  regime: []

trigger_keywords:
  - "benchmark-construction-method"
  - "scientific-discovery-end-to-end-benchmark-pipeline"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "scientific-discovery-evaluation"
  - "arxiv:2601.01678"

data_products: []
algorithms:
  - name: "Multi-LLM insight extraction from study + repo"
  - name: "Candidate workflow generation"
  - name: "Verification against reported findings"
  - name: "Semi-automation with human review checkpoints"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2601.01678"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Bounded to scientific-study-with-public-repo settings; the method is a benchmark-construction recipe, not a single static benchmark.
  out_of_scope:
  - "Do not assume any benchmark constructed by the pipeline is field-validated."
  - "Do not equate workflow recovery with novel discovery."

failure_modes:
  - "Workflow extraction quality depends on repo cleanliness."
  - "Verification step inherits LLM-as-judge limitations."

depends_on:
  []

adapter_notes: []

research_generation_affordances:
  - type: hypothesis
    statement: "HelioSI can build a heliophysics HeurekaBench by running the construction pipeline over the 8 paper-skills with 'paper-grounded-locally-reproduced' or 'pipeline-specified-runnable-from-X' status. The wu-2026 NSPF-FEM open-flux reproduction would be the first item."
  - type: minimal_experiment
    statement: "Run the construction pipeline on [[paper-stansby-2020-pfsspy-python-pfss]] + its repo; emit one benchmark item and verify it against the wu-2026 NSPF-FEM reproduction artifact already in HelioSI."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2601.01678, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# HeurekaBench: A Benchmarking Framework for AI Co-scientist (pipeline-construction method) - paper-skill (wave500)

> **Skill type**: positioning / evaluation / design-pattern-extractor.
> This is NOT a heliophysics method. Loaded by the HelioSI runtime (or any
> agent harness) to (a) audit manuscript/benchmark/positioning claims,
> (b) reuse design patterns from non-heliophysics AI-scientist work, and
> (c) seed research-generation affordances for heliophysics-specific
> runtime upgrades. See §9 for the Layer-4 affordances.
>
> **Source type:** `scientific-discovery-evaluation`. **Executable status:** `benchmark-protocol-template`.

---

## 1. Trigger  *(Layer 1)*

Invoke this skill when an agent (HelioSI manuscript writer, benchmark
designer, runtime architect, or any other harness consumer) is:

- drafting/revising HelioSI manuscript sections that compare against benchmark-construction-method systems
- designing a HelioSI benchmark or evaluation that should reflect the scientific-discovery-end-to-end-benchmark-pipeline pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** A semi-automated pipeline (multi-LLM insight extraction + workflow generation + verification against reported findings) constructs end-to-end benchmark items grounded in a scientific study and its code repository, enabling realistic AI co-scientist evaluation beyond single-turn QA.

**Verifiable task.** A reproduction of this skill's positioning value
succeeds when an agent restates the claim above with the
`claim_boundary.scope` bounds intact, refuses overclaims listed in
§7, and emits the §9 Layer-4 affordances in a form a graph walker can
consume.

## 3. Methods / equations -> executable protocol  *(Layer 2, abstract)*

Each item below is the paper's method as an **abstract capability** the
runtime would need to reproduce or borrow the design pattern. No
specific runtime (LingTai, Claude Code, an MCP server) is named here -
those belong in §8 / `adapter_notes[]`, which are intentionally empty
for this wave500 batch.

### Method 1: Multi-LLM insight extraction from study + repo

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Candidate workflow generation

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Verification against reported findings

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 4: Semi-automation with human review checkpoints

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.


## 4. Data / instruments -> abstract tool contracts  *(Layer 2, abstract)*

This paper is a positioning / evaluation / design-pattern source, not a
heliophysics-data workflow. The "data" the skill consumes is the
HelioSI manuscript draft, benchmark spec, runtime architecture
description, or sibling paper-skills.

| Input artifact | Role | Capability requirement |
|----------------|------|------------------------|
| HelioSI manuscript draft (`heliosi_manuscript_draft.md`) | Target of positioning checklist | Filesystem read |
| HelioSI benchmark spec | Target of benchmark-design template | Filesystem read |
| Sibling paper-skills (this corpus) | Source of cross-references | Skill-catalog read |
| External paper (DOI/arXiv) | Source for full-text verification (currently TODO) | Web fetch (optional) |

## 5. Validation target -> benchmark artifact  *(Layer 2)*

Not benchmarked yet - this is a `positioning-skill-not-executable-science`
entry. Promotion requires either (a) a manuscript-coverage audit
artifact, (b) a benchmark-construction prototype, or (c) a Layer-3
adapter that wires the design pattern into HelioSI and runs it
end-to-end on a heliophysics test case.

## 6. Failure modes -> skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Workflow extraction quality depends on repo cleanliness.
- Verification step inherits LLM-as-judge limitations.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Bounded to scientific-study-with-public-repo settings; the method is a benchmark-construction recipe, not a single static benchmark.

**Out of scope - do NOT generalize beyond:**

- Do not assume any benchmark constructed by the pipeline is field-validated.
- Do not equate workflow recovery with novel discovery.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2601.01678](https://arxiv.org/abs/2601.01678)
- ADS: n/a
- Code: n/a
- Data: n/a

Adapter notes intentionally empty for this batch - the skill remains
executable from §3-§5 alone on any agent harness that supports
filesystem reads + skill-catalog walks.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained positioning/design-pattern source).

**Research-generation affordances - how this paper helps HelioSI (or
any heliophysics agent) generate or evaluate new scientific ideas:**

- **Hypothesis** - HelioSI can build a heliophysics HeurekaBench by running the construction pipeline over the 8 paper-skills with 'paper-grounded-locally-reproduced' or 'pipeline-specified-runnable-from-X' status. The wu-2026 NSPF-FEM open-flux reproduction would be the first item. Related: n/a.
- **Minimal_experiment** - Run the construction pipeline on [[paper-stansby-2020-pfsspy-python-pfss]] + its repo; emit one benchmark item and verify it against the wu-2026 NSPF-FEM reproduction artifact already in HelioSI. Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
