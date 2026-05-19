---
name: mind-ai-co-scientist-material-research-2026
description: Per-entry paper-skill in pilot_2026_and_runtime (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# mind-ai-co-scientist-material-research-2026

> **Skill type:** *positioning / comparison* skill. Encodes the MIND
> system's domain-specific co-scientist pattern so HelioSI can borrow its
> hypothesis → in-silico experiment → debate-validation loop and frame
> heliophysics computational experiments as analogous verifiers.

## When to use this paper-skill

Invoke when:

- Drafting the HelioSI architecture section and naming the
  hypothesis-refinement → computational-experiment → debate-validation
  loop.
- Designing HelioSI's verification layer: choosing which heliophysics
  computational experiments (PFSS, SPICE, PSP plasma analysis, JS
  scalogram, sw-scanner) play the role MIND assigns to ML interatomic
  potentials.
- Drawing a runtime architecture figure that needs a sibling/precedent
  reference for the "agent network with in-silico verifier" pattern.
- Designing a modular skill registry so additional domain modules can be
  added — MIND's modular-experiment-module idea.

Do not invoke as a materials-science workflow inside HelioSI; the skill
is about *runtime pattern transfer*, not materials methods.

## Paper identity and claim boundary

- **Title:** MIND: AI Co-Scientist for Material Research (canonical title
  as captured in the inventory)
- **arXiv:** 2604.13699 (2026-04-15)
- **Authors:** Geonhee Ahn et al. (TODO verify full author list from full
  text)
- **Type:** domain-specific AI co-scientist system paper
- **Claim boundary:** MIND is a multi-agent LLM-driven framework for
  *automated hypothesis validation in materials research*. Validation is
  performed via ML interatomic potentials (e.g. SevenNet-Omni) as
  scalable in-silico experiments. The paper does NOT claim a general-
  purpose scientist; it claims a domain-specific co-scientist with a
  clearly defined scientific loop.

## Methodological pattern to operationalize (for HelioSI design)

The transferable pattern is a four-step scientific loop:

1. **Hypothesis refinement** — turn a vague research question into a
   testable claim.
2. **Experimentation** — execute an in-silico experiment that produces
   quantitative output.
3. **Debate-based validation** — multi-agent critique of the result
   before it is accepted.
4. **Modular extension** — additional experimental modules can be plugged
   in.

**HelioSI mapping:**

| MIND step | HelioSI analogue |
|---|---|
| Hypothesis refinement | Research goal → skill-graph task DAG via the orchestrator |
| Experimentation | PFSS extrapolation, SPICE ephemerides, PSP plasma analysis, sw-scanner, JS scalogram, turbulence diagnostics |
| Debate validation | Benchmark agent + PI-in-loop |
| Modular extension | Additional heliophysics skills + MCPs registered into the catalog |

The skill encodes this mapping as the canonical HelioSI architecture
template.

## Required data / instruments / code / archives

- None for direct execution. The skill is a *runtime architecture
  template generator*.
- Required artifacts for using the skill: the current HelioSI architecture
  document, the skill catalog, and the benchmark spec.

## Algorithm / workflow steps

When invoked by the HelioSI architecture-design agent:

1. **Load the current HelioSI architecture description.**
2. **Map each HelioSI component onto a MIND step** using the table above.
   Emit a coverage map.
3. **Identify gaps:** any MIND step without a clear HelioSI analogue is
   flagged as a TODO. (As of the inventory's gap plan, "debate validation"
   is *partial* — a benchmark agent exists but multi-agent critique is
   not yet wired in.)
4. **Suggest writing moves** drawing on the canonical phrasing in
   `agent_runtime_2026_only_synthesis.md` §1.2 ("Like recent material-
   science co-scientist systems that integrate in-silico experiments for
   hypothesis validation, HelioSI couples LLM agents to heliophysics
   computational experiments: PFSS extrapolation, spacecraft ephemerides,
   PSP plasma analysis, turbulence diagnostics and solar-wind
   segmentation").
5. **Emit a figure spec** for an architecture diagram that mirrors the
   MIND four-step loop with heliophysics modules in each box.

## Minimal executable benchmark or validation target

The "benchmark" for this positioning skill is *architecture coverage*:

- HelioSI architecture explicitly names all four loop steps.
- Each step has at least one implementing skill or MCP.
- The architecture figure (Figure 2 in the manuscript) shows the four-
  step loop visibly.

## Known pitfalls / failure modes (for using this skill)

- **Direct domain transfer.** MIND's ML interatomic potentials are not
  analogous to *every* heliophysics tool; the closest analogue is a fast
  physics surrogate (e.g. a reduced PFSS solver). Naming PSP raw data
  loading as "in-silico experiment" is a category error.
- **Over-claiming debate validation.** A single benchmark-agent pass is
  not the same as multi-agent debate; only claim debate validation when
  the runtime actually instantiates it.
- **Borrowing the loop without the verifier.** The MIND contribution is
  not the loop alone — it is the loop *plus* a credible verifier. HelioSI
  must name its verifiers explicitly.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2604.13699 as an Anthropic-
style **architecture-design Skill** — not a materials-science method and
not a heliophysics method. It is loaded by the HelioSI runtime to
generate architecture coverage maps and figure specs.

| Paper element | Agent-native form |
|---|---|
| Claim — "domain-specific co-scientist = hypothesis → in-silico experiment → debate validation → modular extension loop" | **Verifiable task:** `audit_architecture(heliosi_arch_doc) -> {step1_components, step2_components, step3_components, step4_components, gap_list}` |
| Methods / arguments — four-step loop + ML-IP verifier role | **Executable workflow:** §"Algorithm / workflow steps" 1–5 — coverage map generator + figure spec emitter, using the MIND↔HelioSI mapping table |
| Data / sources / code — HelioSI architecture description, skill catalog, benchmark spec | **MCP / tool contracts:** filesystem reader for the HelioSI architecture/manuscript repo; figure-spec emitter targeting Figure 2 |
| Caveats / failure modes — direct domain transfer; over-claiming debate validation; borrowing the loop without a verifier | **Skill memory:** §"Known pitfalls / failure modes" — runtime refuses to label a single benchmark-agent pass as "debate validation" |
| Figures / results — MIND four-step architecture figure | **Benchmark artifacts:** HelioSI Figure-2 spec (JSON) + coverage-map markdown + per-step TODO list |

Compiling this paper as a Skill turns the MIND pattern into a re-runnable
architecture linter rather than a one-time literature reading.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** invoked by the architecture-design and figure-
  generation sub-graphs.
- **Skills it composes with:**
  - [[agentic-ai-scientists-not-built-autonomous-discovery-2026]] (sibling
    positioning skill) — provides the failure-mode framing the MIND-style
    loop must address.
  - [[heurekabench-2026-end-to-end-co-scientist-evaluation]] — provides
    the benchmark counterpart to MIND's verifier.
- **MCPs it would use:** none directly; references all HelioSI MCPs
  (`cdaweb-mcp`, `pfsspy-mcp`, `spice-mcp`, `pyspedas-mcp`, `soar-mcp`,
  ...) as candidate components of the experimentation step.
- **HelioSI manuscript role:** primary template for Figure 2 (multi-
  agent runtime architecture) and for the Methods section paragraph on
  the four-step scientific loop.

## References

- Ahn, G., et al. (2026). MIND: AI Co-Scientist for Material Research.
  arXiv:2604.13699.
- Inventory: `sioulas-reproduction/results/agent_runtime_2026_only_synthesis.md`
  §1.2; `heliosi_similar_papers_requirements_gap_plan.md` §1 and §2.
