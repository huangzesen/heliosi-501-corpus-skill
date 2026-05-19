---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-hwu-2026-medical-ai-scientist-clinical-research
description: >-
  Use when the agent is positioning the consuming agent/manuscript against domain-specific-ai-scientist literature, borrowing a agent-runtime-domain-specific-pattern-transfer design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "Medical AI Scientist is the first autonomous research framework tailored to clinical research, providing clinically-grounded ideation by transforming surveyed l" (arXiv preprint 2026).
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
  title: "Towards a Medical AI Scientist"
  first_author: "Wu, H."
  authors: ["Hongtao Wu", "Boyun Zheng", "Dingjie Song", "Yu Jiang", "Jianfeng Gao", "Lei Xing"]
  year: 2026
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2603.28589"
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "agent-runtime-domain-specific-pattern-transfer"]
  missions: []
  regime: []

trigger_keywords:
  - "domain-specific-ai-scientist"
  - "agent-runtime-domain-specific-pattern-transfer"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "agent-runtime-positioning"
  - "arxiv:2603.28589"

data_products: []
algorithms:
  - name: "Literature-to-evidence transformation pipeline"
  - name: "Clinician-engineer co-reasoning protocol"
  - name: "Idea traceability ledger"
  - name: "Evidence-grounded manuscript drafting"

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2603.28589"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Bounded to clinical medicine with the paper's clinician-engineer co-reasoning protocol; 'first' claim refers to clinical-medicine domain.
  out_of_scope:
  - "Do not generalize 'first autonomous framework' beyond clinical medicine."
  - "Do not assume the co-reasoning protocol transfers without redesign."

failure_modes:
  - "Co-reasoning protocol requires named expert roles; HelioSI must define heliophysicist-engineer pairing explicitly."
  - "Evidence-grounding requires a citation graph; reuse demands a heliophysics citation graph."

depends_on:
  []

adapter_notes: []

research_generation_affordances:
  - type: hypothesis
    statement: "The Medical AI Scientist paper is the strongest 2026 rhetorical template for HelioSI's introduction. Replace 'clinical' with 'heliophysics' verbatim and the claim structure transfers."
  - type: minimal_experiment
    statement: "Implement traceability of HelioSI-generated ideas back to specific paper-skills; report the fraction of ideas with full citation paths as a 'clinical-grade traceability' metric."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:2603.28589, doi:n/a)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# Towards a Medical AI Scientist - paper-skill (wave500)

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

- drafting/revising HelioSI manuscript sections that compare against domain-specific-ai-scientist systems
- designing a HelioSI benchmark or evaluation that should reflect the agent-runtime-domain-specific-pattern-transfer pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** Medical AI Scientist is the first autonomous research framework tailored to clinical research, providing clinically-grounded ideation by transforming surveyed literature into actionable evidence through clinician-engineer co-reasoning, with traceability of generated research ideas and evidence-grounded manuscript drafting.

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

### Method 1: Literature-to-evidence transformation pipeline

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Clinician-engineer co-reasoning protocol

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Idea traceability ledger

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 4: Evidence-grounded manuscript drafting

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

- Co-reasoning protocol requires named expert roles; HelioSI must define heliophysicist-engineer pairing explicitly.
- Evidence-grounding requires a citation graph; reuse demands a heliophysics citation graph.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Bounded to clinical medicine with the paper's clinician-engineer co-reasoning protocol; 'first' claim refers to clinical-medicine domain.

**Out of scope - do NOT generalize beyond:**

- Do not generalize 'first autonomous framework' beyond clinical medicine.
- Do not assume the co-reasoning protocol transfers without redesign.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: n/a
- arXiv: [arXiv:2603.28589](https://arxiv.org/abs/2603.28589)
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

- **Hypothesis** - The Medical AI Scientist paper is the strongest 2026 rhetorical template for HelioSI's introduction. Replace 'clinical' with 'heliophysics' verbatim and the claim structure transfers. Related: n/a.
- **Minimal_experiment** - Implement traceability of HelioSI-generated ideas back to specific paper-skills; report the fraction of ideas with full citation paths as a 'clinical-grade traceability' metric. Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
