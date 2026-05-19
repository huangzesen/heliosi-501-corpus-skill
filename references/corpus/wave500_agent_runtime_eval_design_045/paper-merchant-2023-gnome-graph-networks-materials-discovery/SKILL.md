---
# === PaperSkill frontmatter (v0.2 - wave500 harness-agnostic batch) ===
name: paper-merchant-2023-gnome-graph-networks-materials-discovery
description: >-
  Use when the agent is positioning HelioSI against domain-specific-foundation-model literature, borrowing a domain-knowledge-compilation-foundation-model design pattern, or auditing a benchmark/manuscript claim related to it - central claim is "GNoME (graph networks for materials exploration) discovers >2.2M new crystal structures predicted to be stable, by scaling graph-neural-network training + activ" (Nature 2023).
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
  title: "Scaling deep learning for materials discovery (GNoME)"
  first_author: "Merchant, A."
  authors: ["Amil Merchant"]
  authors_complete: false
  year: 2023
  venue: "Nature"
  doi: "10.1038/s41586-023-06735-9"
  arxiv_id: null
  ads_bibcode: null

domain:
  primary_theme: other
  secondary_themes: ["agent-runtime", "domain-knowledge-compilation-foundation-model"]
  missions: []
  regime: []

trigger_keywords:
  - "domain-specific-foundation-model"
  - "domain-knowledge-compilation-foundation-model"
  - "agent-runtime"
  - "ai-scientist"
  - "positioning"
  - "domain-knowledge-compilation"
  - "doi:10.1038/s41586-023-06735-9"

data_products: []
algorithms:
  - name: "Graph neural networks over crystal candidates"
  - name: "Active learning + DFT-as-evaluator"
  - name: "Massive candidate generation + cascade filtering"

validation_target: null

links:
  doi_url: "https://doi.org/10.1038/s41586-023-06735-9"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Bounded to crystal-structure stability prediction at DFT fidelity; experimental validation rate is much lower than the prediction set.
  out_of_scope:
  - "Do not equate 'predicted stable' with 'experimentally synthesized'."
  - "Do not generalize the active-learning loop to fields without an analogous high-fidelity simulator."

failure_modes:
  - "DFT calibration errors propagate."
  - "Active-learning loop biases toward stable regions, missing edge cases."

depends_on:
  - paper-jumper-2021-alphafold2-protein-structure-prediction

adapter_notes: []

research_generation_affordances:
  - type: hypothesis
    statement: "Heliophysics analog: scale a GNN over (magnetogram, r_ss, model-choice) candidate configurations + use PFSS/NSPF-FEM solvers as evaluators; emit a catalog of plausible coronal-field configurations matching given in-situ constraints."
  - type: minimal_experiment
    statement: "Sketch a 1000-candidate sweep of (CR magnetogram, r_ss in [1.5, 3.0]) configurations; rank by match to open-flux constraint; benchmark HelioSI's open-flux skill (wu-2026)."

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) - wave500_agent_runtime_eval_design_045"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/paper_skill_corpus/wave500_agent_runtime_eval_design_045/manifest.json and sioulas-reproduction/results/agent_runtime_paper_scan_raw.md / agent_runtime_2026_only_synthesis.md (arxiv:n/a, doi:10.1038/s41586-023-06735-9)"
  verified_by: null
  verified_at: null

tags: [agent-runtime, paper-skill, positioning, ai-scientist, scientific-discovery-evaluation]
---

# Scaling deep learning for materials discovery (GNoME) - paper-skill (wave500)

> **Skill type**: positioning / evaluation / design-pattern-extractor.
> This is NOT a heliophysics method. Loaded by the HelioSI runtime (or any
> agent harness) to (a) audit manuscript/benchmark/positioning claims,
> (b) reuse design patterns from non-heliophysics AI-scientist work, and
> (c) seed research-generation affordances for heliophysics-specific
> runtime upgrades. See §9 for the Layer-4 affordances.
>
> **Source type:** `domain-knowledge-compilation`. **Executable status:** `design-pattern-extractor`.

---

## 1. Trigger  *(Layer 1)*

Invoke this skill when an agent (HelioSI manuscript writer, benchmark
designer, runtime architect, or any other harness consumer) is:

- drafting/revising HelioSI manuscript sections that compare against domain-specific-foundation-model systems
- designing a HelioSI benchmark or evaluation that should reflect the domain-knowledge-compilation-foundation-model pattern
- deciding whether a HelioSI subsystem should borrow this paper's design choices or explicitly reject them

Do NOT use this skill as a heliophysics data-pipeline component - it
has no `data_products[]` and no executable scientific workflow over
mission data.

## 2. Paper claim -> verifiable task  *(Layer 1)*

**Claim (narrow form).** GNoME (graph networks for materials exploration) discovers >2.2M new crystal structures predicted to be stable, by scaling graph-neural-network training + active learning loops over DFT calculations; ~380k candidates pass higher-fidelity filters.

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

### Method 1: Graph neural networks over crystal candidates

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 2: Active learning + DFT-as-evaluator

- Paper role: explicit named method/component of the paper's contribution.
- Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript/benchmark/sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference.

### Method 3: Massive candidate generation + cascade filtering

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

- DFT calibration errors propagate.
- Active-learning loop biases toward stable regions, missing edge cases.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Bounded to crystal-structure stability prediction at DFT fidelity; experimental validation rate is much lower than the prediction set.

**Out of scope - do NOT generalize beyond:**

- Do not equate 'predicted stable' with 'experimentally synthesized'.
- Do not generalize the active-learning loop to fields without an analogous high-fidelity simulator.

If a downstream task asks for a generalization listed above, refuse it
and return a reference to a sibling paper-skill that covers it (or
report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: [10.1038/s41586-023-06735-9](https://doi.org/10.1038/s41586-023-06735-9)
- arXiv: n/a
- ADS: n/a
- Code: n/a
- Data: n/a

Adapter notes intentionally empty for this batch - the skill remains
executable from §3-§5 alone on any agent harness that supports
filesystem reads + skill-catalog walks.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).**

- `[[paper-jumper-2021-alphafold2-protein-structure-prediction]]` - paper-skill within the same wave500 batch (sibling positioning/design-pattern source).

**Research-generation affordances - how this paper helps HelioSI (or
any heliophysics agent) generate or evaluate new scientific ideas:**

- **Hypothesis** - Heliophysics analog: scale a GNN over (magnetogram, r_ss, model-choice) candidate configurations + use PFSS/NSPF-FEM solvers as evaluators; emit a catalog of plausible coronal-field configurations matching given in-situ constraints. Related: n/a.
- **Minimal_experiment** - Sketch a 1000-candidate sweep of (CR magnetogram, r_ss in [1.5, 3.0]) configurations; rank by match to open-flux constraint; benchmark HelioSI's open-flux skill (wu-2026). Related: n/a.

## Notes

- This SKILL.md is a `wave500_agent_runtime_eval_design_045` batch
  entry. It is harness-agnostic by construction; do not bind it to a
  specific runtime without converting Layer-3 `adapter_notes[]` to
  populated.
- The `provenance.source_record` field points to the inventory anchor
  used to write this skill; full-text verification of all identifiers
  is pending and any `TODO_verify_with_full_text` token must be
  resolved before promoting past stub tier.
