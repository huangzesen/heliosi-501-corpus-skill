---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-wang-2023-voyager-open-ended-embodied-agent-llm
description: >-
  Use when the agent is positioning the consuming agent/manuscript against foundational-method literature, borrowing a agent-runtime-skill-library-acquisition design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "Voyager continuously acquires, refines, and stores executable skills in Minecraft via a self-improving curriculum, an iterative prompting mechanism, and a skill" (arXiv preprint 2023).
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
  title: "Voyager: An Open-Ended Embodied Agent with Large Language Models"
  first_author: "Wang, G."
  authors: ["Guanzhi Wang", "Yuqi Xie", "Yunfan Jiang", "Ajay Mandlekar", "Chaowei Xiao", "Yuke Zhu", "Linxi Fan", "Anima Anandkumar"]
  year: 2023
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2305.16291"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "agent-runtime-skill-library-acquisition"]
  missions: []
  regime: []

trigger_keywords:
  - "foundational-method"
  - "agent-runtime-skill-library-acquisition"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "agent-runtime-positioning"
  - "arxiv:2305.16291"

data_products: []
algorithms:
  - name: "Iterative-prompting LLM curriculum"
  - name: "Executable skill library with retrieval"
  - name: "Self-verification loop"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2305.16291"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Bounded to the Minecraft sandbox with the paper's specific curriculum + skill-library design.
  out_of_scope:
  - "Do not generalize 'open-ended' to physical environments without physics-faithful simulators."
  - "Do not assume the skill library transfers without a domain-grounding step."

failure_modes:
  - "Skill quality depends on the verifier in Minecraft; transfer requires a domain verifier."
  - "Curriculum may bias toward easy-to-verify skills."

depends_on:
  []

adapter_notes: []

research_generation_affordances:
  - type: hypothesis
    statement: "HelioSI's paper-skill corpus IS the heliophysics analogue of Voyager's skill library, but populated from published literature rather than self-discovery. A Stage-D self-discovery loop is the missing piece."
  - type: minimal_experiment
    statement: "Run a Voyager-style curriculum over HelioSI: starting from one anchor paper-skill, generate child hypothesis-tier skills and store them as paper-hyp-* nodes; measure curriculum branching factor."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2305.16291, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# Voyager: An Open-Ended Embodied Agent with Large Language Models - paper-skill (wave500)

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
- designing a HelioSI benchmark or evaluation that should reflect the agent-runtime-skill-library-acquisition pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** Voyager continuously acquires, refines, and stores executable skills in Minecraft via a self-improving curriculum, an iterative prompting mechanism, and a skill library, outperforming prior approaches on exploration breadth + item-acquisition speed.

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

### Method 1: Iterative-prompting LLM curriculum

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Executable skill library with retrieval

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Self-verification loop

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

- Skill quality depends on the verifier in Minecraft; transfer requires a domain verifier.
- Curriculum may bias toward easy-to-verify skills.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Bounded to the Minecraft sandbox with the paper's specific curriculum + skill-library design.

**Out of scope - do NOT generalize beyond:**

- Do not generalize 'open-ended' to physical environments without physics-faithful simulators.
- Do not assume the skill library transfers without a domain-grounding step.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)
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

- **Hypothesis** - HelioSI's paper-skill corpus IS the heliophysics analogue of Voyager's skill library, but populated from published literature rather than self-discovery. A Stage-D self-discovery loop is the missing piece. Related: n/a.
- **Minimal_experiment** - Run a Voyager-style curriculum over HelioSI: starting from one anchor paper-skill, generate child hypothesis-tier skills and store them as paper-hyp-* nodes; measure curriculum branching factor. Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
