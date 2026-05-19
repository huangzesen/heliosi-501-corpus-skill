---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-su-2024-virsci-multi-agent-idea-generation
description: >-
  Use when the agent is positioning HelioSI against ai-scientist-system literature, borrowing a agent-runtime-team-roles design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "A virtual team of specialist LLM agents (VirSci) outperforms single-agent baselines on scientific idea generation in benchmarked novelty metrics; collaboration " (arXiv preprint 2024).
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
  title: "Many Heads Are Better Than One: Improved Scientific Idea Generation by A LLM-Based Multi-Agent System (VirSci)"
  first_author: "Su, H."
  authors: ["Haoyang Su", "Renqi Chen", "Shixiang Tang", "Zhenfei Yin", "Xinzhe Zheng", "Jinzhe Li", "Biqing Qi", "Qi Wu", "Hui Li", "Wanli Ouyang", "Philip Torr", "Bowen Zhou"]
  year: 2024
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2410.09403"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "agent-runtime-team-roles"]
  missions: []
  regime: []

trigger_keywords:
  - "ai-scientist-system"
  - "agent-runtime-team-roles"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "agent-runtime-positioning"
  - "arxiv:2410.09403"

data_products: []
algorithms:
  - name: "Role-typed multi-agent team"
  - name: "Iterative generate-critique-refine loop"
  - name: "Novelty metric over generated ideas vs. single-agent baseline"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2410.09403"
  ads_url: null
  code_repo: "https://github.com/open-sciencelab/Virtual-Scientists"
  data_repo: null

claim_boundary:
  scope: >-
    Bounded to the paper's idea-generation benchmark with the specific role taxonomy and refinement protocol; novelty is measured by the paper's chosen metric, not by field acceptance.
  out_of_scope:
  - "Do not claim higher novelty in domains the paper does not test."
  - "Do not assume the same role taxonomy is optimal in physics or heliophysics."

failure_modes:
  - "Novelty metric is benchmark-internal; field-level novelty needs human review."
  - "Role assignment overhead grows with team size; the paper does not characterize the inflection point."

depends_on:
  []

adapter_notes: []

research_generation_affordances:
  - type: minimal_experiment
    statement: "Map HelioSI's existing agent roles (literature, data, PFSS, turbulence, benchmark, writing) onto VirSci's collaboration mechanism and measure idea-generation novelty against [[paper-gottweis-2025-ai-co-scientist-multi-agent-gemini]]'s tournament baseline."
    related_skills:
      - paper-gottweis-2025-ai-co-scientist-multi-agent-gemini
  - type: hypothesis
    statement: "Heliophysics-specific role specialization (e.g. PSP-data agent + PFSS agent + turbulence agent) increases the rate of cross-paper-skill ideas that survive verification."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2410.09403, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# Many Heads Are Better Than One: Improved Scientific Idea Generation by A LLM-Based Multi-Agent System (VirSci) - paper-skill (wave500)

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
- designing a HelioSI benchmark or evaluation that should reflect the agent-runtime-team-roles pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** A virtual team of specialist LLM agents (VirSci) outperforms single-agent baselines on scientific idea generation in benchmarked novelty metrics; collaboration mechanisms (diverse roles, refinement loops) explain the gain.

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

### Method 1: Role-typed multi-agent team

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Iterative generate-critique-refine loop

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Novelty metric over generated ideas vs. single-agent baseline

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

- Novelty metric is benchmark-internal; field-level novelty needs human review.
- Role assignment overhead grows with team size; the paper does not characterize the inflection point.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Bounded to the paper's idea-generation benchmark with the specific role taxonomy and refinement protocol; novelty is measured by the paper's chosen metric, not by field acceptance.

**Out of scope - do NOT generalize beyond:**

- Do not claim higher novelty in domains the paper does not test.
- Do not assume the same role taxonomy is optimal in physics or heliophysics.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2410.09403](https://arxiv.org/abs/2410.09403)
- ADS: n/a
- Code: [repo](https://github.com/open-sciencelab/Virtual-Scientists)
- Data: n/a

Adapter notes intentionally empty for this batch - the skill remains
executable from §3-§5 alone on any agent harness that supports
filesystem reads + skill-catalog walks.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained positioning/design-pattern source).

**Research-generation affordances - how this paper helps HelioSI (or
any heliophysics agent) generate or evaluate new scientific ideas:**

- **Minimal_experiment** - Map HelioSI's existing agent roles (literature, data, PFSS, turbulence, benchmark, writing) onto VirSci's collaboration mechanism and measure idea-generation novelty against [[paper-gottweis-2025-ai-co-scientist-multi-agent-gemini]]'s tournament baseline. Related: `[[paper-gottweis-2025-ai-co-scientist-multi-agent-gemini]]`.
- **Hypothesis** - Heliophysics-specific role specialization (e.g. PSP-data agent + PFSS agent + turbulence agent) increases the rate of cross-paper-skill ideas that survive verification. Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
