---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-lu-2024-ai-scientist-fully-automated-discovery
description: >-
  Use when the agent is positioning the consuming agent/manuscript against ai-scientist-system literature, borrowing a agent-runtime-full-pipeline design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "A general LLM-driven framework can execute the full open-ended ML-research loop (idea -> code -> experiment -> visualization -> paper -> simulated review) at <U" (arXiv preprint 2024).
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
  title: "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"
  first_author: "Lu, C."
  authors: ["Chris Lu", "Cong Lu", "Robert Tjarko Lange", "Jakob Foerster", "Jeff Clune", "David Ha"]
  year: 2024
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2408.06292"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "agent-runtime-full-pipeline"]
  missions: []
  regime: []

trigger_keywords:
  - "ai-scientist-system"
  - "agent-runtime-full-pipeline"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "agent-runtime-positioning"
  - "arxiv:2408.06292"

data_products: []
algorithms:
  - name: "Idea-generation prompt loop with novelty checks"
  - name: "Template-based experiment code generation"
  - name: "Iterative experiment execution and revision"
  - name: "Paper writeup with figure insertion"
  - name: "Automated reviewer scoring with score calibration against ICLR-style rubric"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2408.06292"
  ads_url: null
  code_repo: "https://github.com/SakanaAI/AI-Scientist"
  data_repo: null

claim_boundary:
  scope: >-
    Claim applies to ML-paper generation in three named subfields with author-supplied code templates, evaluated by the paper's own automated reviewer; not to natural-science domains, not without templates, and not to human-graded acceptance.
  out_of_scope:
  - "Do not generalize to non-ML scientific domains (chemistry, heliophysics, biology) without re-grounding the workflow in domain data/tools."
  - "Do not treat the automated reviewer score as equivalent to peer review by the field."

failure_modes:
  - "Template dependency: the v1 system requires human-authored experiment templates per subfield."
  - "Single-turn benchmark style: reviewer is itself an LLM, so reviewer-author correlation can mask real-world weaknesses."
  - "Domain narrowness: extending to natural-science domains requires rebuilding data/tool integration from scratch."

depends_on:
  []

adapter_notes: []

research_generation_affordances:
  - type: gap
    statement: "AI Scientist v1 has no in-situ scientific data/instrument tools; HelioSI fills this gap with mission archives + Layer-2 capability contracts."
    proposed_action: "Use the v1 paper as the positioning anchor for 'why a heliophysics-specific runtime is needed' in HelioSI's introduction."
  - type: minimal_experiment
    statement: "Apply the v1 idea-generation prompt loop to a single heliophysics paper-skill (e.g. [[paper-sioulas-2023-anisotropic-scaling]]) and measure how many of the generated follow-up ideas survive a sibling paper-skill consistency check."
  - type: hypothesis
    statement: "If the AI Scientist loop is grounded in heliophysics paper-skills + mission MCPs, the cost-per-idea will rise relative to ML-only generation but the rate of contract-passing benchmark artifacts will be measurably higher."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2408.06292, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery - paper-skill (wave500)

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
- designing a HelioSI benchmark or evaluation that should reflect the agent-runtime-full-pipeline pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** A general LLM-driven framework can execute the full open-ended ML-research loop (idea -> code -> experiment -> visualization -> paper -> simulated review) at <US$15 per generated paper, on three ML subfields (diffusion, transformer LM, learning dynamics), evaluated by a co-developed automated reviewer.

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

### Method 1: Idea-generation prompt loop with novelty checks

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Template-based experiment code generation

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Iterative experiment execution and revision

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 4: Paper writeup with figure insertion

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 5: Automated reviewer scoring with score calibration against ICLR-style rubric

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

- Template dependency: the v1 system requires human-authored experiment templates per subfield.
- Single-turn benchmark style: reviewer is itself an LLM, so reviewer-author correlation can mask real-world weaknesses.
- Domain narrowness: extending to natural-science domains requires rebuilding data/tool integration from scratch.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Claim applies to ML-paper generation in three named subfields with author-supplied code templates, evaluated by the paper's own automated reviewer; not to natural-science domains, not without templates, and not to human-graded acceptance.

**Out of scope - do NOT generalize beyond:**

- Do not generalize to non-ML scientific domains (chemistry, heliophysics, biology) without re-grounding the workflow in domain data/tools.
- Do not treat the automated reviewer score as equivalent to peer review by the field.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2408.06292](https://arxiv.org/abs/2408.06292)
- ADS: n/a
- Code: [repo](https://github.com/SakanaAI/AI-Scientist)
- Data: n/a

Adapter notes intentionally empty for this batch - the skill remains
executable from §3-§5 alone on any agent harness that supports
filesystem reads + skill-catalog walks.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained positioning/design-pattern source).

**Research-generation affordances - how this paper helps HelioSI (or
any heliophysics agent) generate or evaluate new scientific ideas:**

- **Gap** - AI Scientist v1 has no in-situ scientific data/instrument tools; HelioSI fills this gap with mission archives + Layer-2 capability contracts. Related: n/a. Proposed: Use the v1 paper as the positioning anchor for 'why a heliophysics-specific runtime is needed' in HelioSI's introduction.
- **Minimal_experiment** - Apply the v1 idea-generation prompt loop to a single heliophysics paper-skill (e.g. [[paper-sioulas-2023-anisotropic-scaling]]) and measure how many of the generated follow-up ideas survive a sibling paper-skill consistency check. Related: n/a.
- **Hypothesis** - If the AI Scientist loop is grounded in heliophysics paper-skills + mission MCPs, the cost-per-idea will rise relative to ML-only generation but the rate of contract-passing benchmark artifacts will be measurably higher. Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
