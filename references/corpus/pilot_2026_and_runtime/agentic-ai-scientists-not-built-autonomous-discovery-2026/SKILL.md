---
name: agentic-ai-scientists-not-built-autonomous-discovery-2026
description: Per-entry paper-skill in pilot_2026_and_runtime (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# agentic-ai-scientists-not-built-autonomous-discovery-2026

> **Skill type:** *positioning / comparison* skill. This is **not** a
> heliophysics method. It guides HelioSI manuscript design and evaluation
> by encoding what the 2026 critique paper expects of any agentic AI
> scientist.

## When to use this paper-skill

Invoke when:

- Drafting or revising the HelioSI manuscript introduction, motivation, or
  related-work section.
- Reviewing a HelioSI claim of "autonomous research" or "agentic
  scientist" — the skill encodes the failure modes this critique paper
  identifies, so the agent must check each before letting the claim
  through.
- Defining evaluation criteria for HelioSI benchmarks (single-turn QA vs.
  end-to-end runs; persistent vs. static memory; expert-in-loop vs. fully
  autonomous).
- Designing a rebuttal to a reviewer who asks "isn't this just an
  LLM-agent demo?"

Do not invoke as a heliophysics workflow component — it has no data
products and no executable scientific pipeline.

## Paper identity and claim boundary

- **Title:** Agentic AI Scientists Are Not Built For Autonomous Scientific
  Discovery
- **Authors:** Harshit Bisht, Vinay Kumar, Kevin Maik Jablonka, Mausam,
  N. M. Anoop Krishnan
- **arXiv:** 2605.08956 (v1, 2026-05-09)
- **Type:** position / critique paper
- **Claim boundary:** The paper argues that current agentic AI scientists
  function as *co-scientists*, not autonomous discoverers. Its scope is
  *methodological critique and recommendations*, not a system. It does NOT
  claim that AI co-scientists are useless — it claims they are
  misnamed/mis-evaluated when called "autonomous discoverers".

## Methodological claim to operationalize (for HelioSI manuscript design)

The paper identifies five recurring failure modes; HelioSI's manuscript
and evaluation should explicitly address each. The skill encodes them as a
*checklist* the manuscript agent must pass before claiming autonomy:

1. **McNamara fallacy in problem selection** — optimizing what is easy to
   measure. *Apply:* HelioSI problem selection is human-driven (HelioSI PI);
   document this explicitly.
2. **Missing tacit procedural / failure knowledge** in LLM training data.
   *Apply:* HelioSI's skill library encodes procedural and failure
   knowledge as durable artifacts; cite this as the answer.
3. **Diversity collapse from preference optimization.** *Apply:* HelioSI
   benchmarks should measure diversity of reproduced workflows, not just
   pass/fail on canonical tasks.
4. **Single-turn benchmarks with no physical feedback.** *Apply:* HelioSI
   benchmarks must be end-to-end and use heliophysics data/code as the
   verifier.
5. **Tool-affordance-driven application choice.** *Apply:* HelioSI tasks
   must be motivated by heliophysics scientific need, not by what an LLM
   happens to do well.

The paper also offers four recommendations; HelioSI's runtime and
benchmarks should be cross-walked against them:

- Scientific simulations as verifiers.
- Persistent world models.
- Preregistration of hypotheses.
- Application driven by scientific need, not tool affordance.

## Required data / instruments / code / archives

- None for direct execution. The skill is a *checklist generator*.
- Required artifacts for using the skill in a manuscript context: the
  current HelioSI manuscript draft (`heliosi_manuscript_draft.md`), the
  HelioSI benchmark spec, and the harness/skills/MCPs architecture
  document.

## Algorithm / workflow steps

When invoked by the HelioSI manuscript or benchmark-design agent:

1. **Ingest the current manuscript draft and benchmark spec.**
2. **Run the 5-failure-mode checklist** against the draft. For each
   failure mode, locate the manuscript paragraph that addresses it; if
   none exists, emit a TODO.
3. **Run the 4-recommendation checklist** against the runtime/benchmark
   architecture. For each recommendation, locate the implementation; if
   none exists, emit a TODO.
4. **Emit a structured report:** `{failure_mode: addressed_paragraph |
   TODO, recommendation: implementation_pointer | TODO}`.
5. **Suggest specific rebuttal phrasings** for the related-work section,
   drawing on the canonical 2026 framing already captured in
   `sioulas-reproduction/results/agent_runtime_2026_only_synthesis.md`
   §1.1 and `heliosi_similar_papers_requirements_gap_plan.md` §1.4.

## Minimal executable benchmark or validation target

The "benchmark" for a positioning skill is *manuscript coverage*:

- A passing manuscript addresses all 5 failure modes and 4
  recommendations with explicit paragraphs.
- A passing benchmark spec includes at least one end-to-end paper-
  grounded workflow (not single-turn QA) and at least one
  scientific-simulation verifier (PSP turbulence reproduction, PFSS
  comparison, etc.).
- A passing autonomy claim is explicitly bounded: HelioSI claims
  *co-scientist autonomy* with expert-in-loop, not full autonomous
  discovery.

## Known pitfalls / failure modes (for using this skill)

- **Over-citing the critique to look conformant.** Reviewers will spot
  this; the manuscript must actually instantiate the recommendations, not
  merely reference them.
- **Conflating co-scientist and autonomous.** HelioSI is the former; never
  claim the latter without preregistered, simulation-verified, expert-
  reviewed evidence.
- **Using this skill as a heliophysics method.** It is positioning only.
  Composing it into a heliophysics data pipeline is a category error.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2605.08956 as an Anthropic-
style **comparison / evaluation Skill** — not a heliophysics method.
The HelioSI runtime loads it the same way it loads any other Skill, but
its purpose is to audit the HelioSI manuscript and benchmark spec, not
to process scientific data.

| Paper element | Agent-native form |
|---|---|
| Claim — "agentic AI scientists today function as co-scientists, not autonomous discoverers" | **Verifiable task:** `audit_autonomy_claim(manuscript, bench_spec) -> {addressed[5_failure_modes], implemented[4_recommendations], over_claim_flags}` |
| Methods / arguments — 5 failure-mode taxonomy + 4 recommendations | **Executable workflow:** §"Algorithm / workflow steps" 1–5 — checklist run over the manuscript draft, with concrete TODO emissions per missing item |
| Data / sources / code — the *manuscript draft, benchmark spec, architecture doc* themselves are the "data" | **MCP / tool contracts:** filesystem reader for the HelioSI manuscript repo; optional citation/docs MCP for reference linking |
| Caveats / failure modes — over-citing critique; conflating co-scientist vs autonomous; using as a heliophysics method | **Skill memory:** §"Known pitfalls / failure modes" — runtime refuses to compose this Skill into a data pipeline |
| Figures / results — checklist tables + suggested rebuttal phrasings | **Benchmark artifacts:** `audit_report.json` (per-failure-mode coverage), `rebuttal_snippets.md`, manuscript-diff suggestions |

Compiling this paper as a Skill means HelioSI's manuscript and benchmark
artifacts can be re-validated against the 2026 critique on every change,
not only at submission time.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** invoked by the *manuscript writing* and *benchmark
  design* sub-graphs, not the science-execution sub-graph.
- **Skills it composes with:**
  - [[mind-ai-co-scientist-material-research-2026]] (sibling positioning
    skill) for in-silico-verifier framing.
  - [[heurekabench-2026-end-to-end-co-scientist-evaluation]] (sibling
    positioning skill) for benchmark design.
- **MCPs it would use:** none directly; could be paired with a
  documentation/citation MCP if available.
- **HelioSI manuscript role:** primary anchor for the Introduction's
  "generic AI scientists are insufficient" move and for the Discussion's
  "operational autonomy" framing. The Bisht critique is the *single most
  important 2026 paper to cite explicitly* per the gap plan
  (`heliosi_similar_papers_requirements_gap_plan.md` §1.4).

## References

- Bisht, H., Kumar, V., Jablonka, K. M., Mausam, Krishnan, N. M. A.
  (2026). Agentic AI Scientists Are Not Built For Autonomous Scientific
  Discovery. arXiv:2605.08956.
- Inventory: `sioulas-reproduction/results/agent_runtime_2026_only_synthesis.md`
  §1.1; `agent_runtime_additional_exact_metadata.md` entry "Agentic AI
  Scientists..."; `heliosi_similar_papers_requirements_gap_plan.md` §1.4.
