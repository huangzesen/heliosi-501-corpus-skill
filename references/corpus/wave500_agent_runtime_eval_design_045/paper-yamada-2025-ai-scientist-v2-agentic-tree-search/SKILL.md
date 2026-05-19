---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-yamada-2025-ai-scientist-v2-agentic-tree-search
description: >-
  Use when the agent is positioning the consuming agent/manuscript against ai-scientist-system literature, borrowing a agent-runtime-tree-search design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "Removing v1's reliance on human-authored code templates and adding a progressive agentic-tree-search managed by an experiment-manager agent enables one workshop" (arXiv preprint 2025).
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
  title: "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search"
  first_author: "Yamada, Y."
  authors: ["Yutaro Yamada", "Robert Tjarko Lange", "Cong Lu", "Shengran Hu", "Chris Lu", "Jakob Foerster", "Jeff Clune", "David Ha"]
  year: 2025
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2504.08066"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "agent-runtime-tree-search"]
  missions: []
  regime: []

trigger_keywords:
  - "ai-scientist-system"
  - "agent-runtime-tree-search"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "agent-runtime-positioning"
  - "arxiv:2504.08066"

data_products: []
algorithms:
  - name: "Progressive agentic tree search over experiment branches"
  - name: "Dedicated experiment-manager agent for branch pruning/expansion"
  - name: "Template-free code generation"
  - name: "VLM-based iterative figure refinement loop"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2504.08066"
  ads_url: null
  code_repo: "https://github.com/SakanaAI/AI-Scientist-v2"
  data_repo: null

claim_boundary:
  scope: >-
    Claim is bounded to one workshop-level acceptance out of three submissions in ML subfields, with v2's specific experiment-manager + tree-search + VLM-figure-loop architecture.
  out_of_scope:
  - "Do not generalize 'workshop-acceptance' to main-conference acceptance or to peer-reviewed natural-science journals."
  - "Do not treat the experiment-manager + tree-search as universally applicable; the paper does not test it in non-ML domains."

failure_modes:
  - "Workshop venue is not equivalent to peer-reviewed journal evidence of scientific contribution."
  - "Tree-search budget may explode without strong branch-pruning heuristics; the paper does not generalize budget claims."
  - "Domain transfer (e.g. to heliophysics) requires re-grounding 'experiment' in mission data / simulation calls, which v2 does not address."

depends_on:
  - paper-lu-2024-ai-scientist-fully-automated-discovery

adapter_notes: []

research_generation_affordances:
  - type: minimal_experiment
    statement: "Adopt the experiment-manager pattern in HelioSI: have a manager agent expand/prune a tree of heliophysics workflow candidates (e.g. PSP interval x analysis-skill pairs) and benchmark which branches reproduce a known finding."
  - type: gap
    statement: "v2's tree-search has no scientific-simulation verifier per node; HelioSI can plug in PFSS / sw-scanner / sunkit-magex as verifiers per branch."
    proposed_action: "Define a 'verifier MCP contract' the experiment manager calls before keeping a branch."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2504.08066, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search - paper-skill (wave500)

> **Skill type**: positioning / evaluation / design-pattern-extractor.
> This is NOT a heliophysics method. Loaded by the HelioSI runtime (or any
> agent harness) to (a) audit manuscript/benchmark/positioning claims,
> (b) reuse design patterns from non-heliophysics AI-scientist work, and
> (c) seed research-generation affordances for heliophysics-specific
> runtime upgrades. See §9 for the Layer-4 affordances.
>
> **Source type:** `agent-runtime-positioning`. **Executable status:** `design-pattern-extractor`.

---

## 1. Trigger  *(Layer 1)*

Invoke this skill when an agent (HelioSI manuscript writer, benchmark
designer, runtime architect, or any other harness consumer) is:

- drafting/revising HelioSI manuscript sections that compare against ai-scientist-system systems
- designing a HelioSI benchmark or evaluation that should reflect the agent-runtime-tree-search pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** Removing v1's reliance on human-authored code templates and adding a progressive agentic-tree-search managed by an experiment-manager agent enables one workshop-accepted, end-to-end AI-generated manuscript at an ICLR 2025 workshop, with a VLM feedback loop refining figure aesthetics.

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

### Method 1: Progressive agentic tree search over experiment branches

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Dedicated experiment-manager agent for branch pruning/expansion

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Template-free code generation

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 4: VLM-based iterative figure refinement loop

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

- Workshop venue is not equivalent to peer-reviewed journal evidence of scientific contribution.
- Tree-search budget may explode without strong branch-pruning heuristics; the paper does not generalize budget claims.
- Domain transfer (e.g. to heliophysics) requires re-grounding 'experiment' in mission data / simulation calls, which v2 does not address.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Claim is bounded to one workshop-level acceptance out of three submissions in ML subfields, with v2's specific experiment-manager + tree-search + VLM-figure-loop architecture.

**Out of scope - do NOT generalize beyond:**

- Do not generalize 'workshop-acceptance' to main-conference acceptance or to peer-reviewed natural-science journals.
- Do not treat the experiment-manager + tree-search as universally applicable; the paper does not test it in non-ML domains.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2504.08066](https://arxiv.org/abs/2504.08066)
- ADS: n/a
- Code: [repo](https://github.com/SakanaAI/AI-Scientist-v2)
- Data: n/a

Adapter notes intentionally empty for this batch - the skill remains
executable from §3-§5 alone on any agent harness that supports
filesystem reads + skill-catalog walks.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).**

- `[[paper-lu-2024-ai-scientist-fully-automated-discovery]]` - paper-skill within the same wave500 batch (sibling positioning/design-pattern source).

**Research-generation affordances - how this paper helps HelioSI (or
any heliophysics agent) generate or evaluate new scientific ideas:**

- **Minimal_experiment** - Adopt the experiment-manager pattern in HelioSI: have a manager agent expand/prune a tree of heliophysics workflow candidates (e.g. PSP interval x analysis-skill pairs) and benchmark which branches reproduce a known finding. Related: n/a.
- **Gap** - v2's tree-search has no scientific-simulation verifier per node; HelioSI can plug in PFSS / sw-scanner / sunkit-magex as verifiers per branch. Related: n/a. Proposed: Define a 'verifier MCP contract' the experiment manager calls before keeping a branch.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
