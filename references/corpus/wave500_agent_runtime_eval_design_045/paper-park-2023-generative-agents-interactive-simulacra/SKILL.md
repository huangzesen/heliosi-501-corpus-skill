---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-park-2023-generative-agents-interactive-simulacra
description: >-
  Use when the agent is positioning the consuming agent/manuscript against foundational-method literature, borrowing a agent-runtime-memory-reflection-planning design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "A generative-agent architecture (observation -> memory stream -> reflection -> planning) produces believable individual + emergent social behaviors in a sandbox" (arXiv preprint / UIST 2023 2023).
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
  title: "Generative Agents: Interactive Simulacra of Human Behavior"
  first_author: "Park, J. S."
  authors: ["Joon Sung Park", "Joseph C. O'Brien", "Carrie J. Cai", "Meredith Ringel Morris", "Percy Liang", "Michael S. Bernstein"]
  year: 2023
  venue: "arXiv preprint / UIST 2023"
  doi: null
  arxiv_id: "2304.03442"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "agent-runtime-memory-reflection-planning"]
  missions: []
  regime: []

trigger_keywords:
  - "foundational-method"
  - "agent-runtime-memory-reflection-planning"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "agent-runtime-positioning"
  - "arxiv:2304.03442"

data_products: []
algorithms:
  - name: "Observation memory stream with importance scoring"
  - name: "Periodic reflection that synthesizes higher-order memories"
  - name: "Plan-and-act loop"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2304.03442"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Bounded to social-simulation behaviors in a constructed sandbox; the architecture is the contribution, not any specific behavior.
  out_of_scope:
  - "Do not interpret 'believable' as 'scientifically valid'."
  - "Do not assume the memory stream scales without summarization."

failure_modes:
  - "Memory retrieval depends on a fragile importance heuristic."
  - "Believability is human-rated; not a discovery metric."

depends_on:
  - paper-shinn-2023-reflexion-verbal-reinforcement-agents

adapter_notes: []

research_generation_affordances:
  - type: hypothesis
    statement: "HelioSI's agent network is structurally similar: observation (mission data) -> memory (paper-skill corpus + LingTai durable memory) -> reflection (Stage D affordances) -> planning (Stage B/C routing)."
  - type: minimal_experiment
    statement: "Add an importance-weighted retrieval over the paper-skill corpus to the existing HelioSI planner; measure whether retrieval relevance improves on a held-out heliophysics question."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2304.03442, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# Generative Agents: Interactive Simulacra of Human Behavior - paper-skill (wave500)

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

- drafting/revising HelioSI manuscript sections that compare against foundational-method systems
- designing a HelioSI benchmark or evaluation that should reflect the agent-runtime-memory-reflection-planning pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** A generative-agent architecture (observation -> memory stream -> reflection -> planning) produces believable individual + emergent social behaviors in a sandbox town of 25 agents.

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

### Method 1: Observation memory stream with importance scoring

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Periodic reflection that synthesizes higher-order memories

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Plan-and-act loop

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

- Memory retrieval depends on a fragile importance heuristic.
- Believability is human-rated; not a discovery metric.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Bounded to social-simulation behaviors in a constructed sandbox; the architecture is the contribution, not any specific behavior.

**Out of scope - do NOT generalize beyond:**

- Do not interpret 'believable' as 'scientifically valid'.
- Do not assume the memory stream scales without summarization.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
- ADS: n/a
- Code: n/a
- Data: n/a

Adapter notes intentionally empty for this batch - the skill remains
executable from §3-§5 alone on any agent harness that supports
filesystem reads + skill-catalog walks.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).**

- `[[paper-shinn-2023-reflexion-verbal-reinforcement-agents]]` - paper-skill within the same wave500 batch (sibling positioning/design-pattern source).

**Research-generation affordances - how this paper helps HelioSI (or
any heliophysics agent) generate or evaluate new scientific ideas:**

- **Hypothesis** - HelioSI's agent network is structurally similar: observation (mission data) -> memory (paper-skill corpus + LingTai durable memory) -> reflection (Stage D affordances) -> planning (Stage B/C routing). Related: n/a.
- **Minimal_experiment** - Add an importance-weighted retrieval over the paper-skill corpus to the existing HelioSI planner; measure whether retrieval relevance improves on a held-out heliophysics question. Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
