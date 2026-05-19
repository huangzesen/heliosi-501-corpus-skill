# Pilot batch 2: 2026 PSP papers + agent-runtime anchor papers

Generated 2026-05-18 by the HelioSI paper-to-skill factory.

This batch demonstrates that the paper-skill methodology spans both
**heliophysics domain papers** (current PSP / 2026 turbulence) and the
**AI-scientist comparison literature**. Each entry has its own
`SKILL.md` (agent-facing) and `metadata.yaml` (machine-readable).

## Framing: papers compiled into Anthropic-style Skills

Every paper in this batch is treated as being **compiled** from a static
PDF into an **agent-native, Anthropic-style Skill** that the HelioSI
runtime can load and dispatch. The compilation mapping is uniform across
all eight skills (and is repeated, with concrete bindings, in each
`SKILL.md`):

| Paper element | Agent-native form |
|---|---|
| Claims | → **Verifiable tasks** |
| Methods / equations | → **Executable workflows** |
| Data / instruments / code | → **MCP / tool contracts** |
| Caveats / failure modes | → **Skill memory** (loaded each invocation) |
| Figures / results | → **Benchmark artifacts** |

Two compilation flavours appear in this batch:

- **Heliophysics method Skills** (entries 1–5): compile into callable
  scientific workflows that consume mission data via MCPs and emit
  benchmark artifacts.
- **Comparison / evaluation / design Skills** (entries 6–8): compile the
  AI-scientist literature into manuscript and benchmark auditors. They
  are *not* heliophysics methods; the runtime refuses to compose them
  into a data pipeline.

Throughout, the **general-purpose harness remains the runtime**; HelioSI
is the **domain instantiation** — a skill graph whose nodes are these
compiled Skills.

## Heliophysics 2026 / current PSP

| # | Slug | arXiv | Year | Theme | Executable? | Key validation target |
|---|---|---|---|---|---|---|
| 1 | [murtas-2026-hcs-reconnection-ion-energization](./murtas-2026-hcs-reconnection-ion-energization/SKILL.md) | 2605.15068 | 2026 | PSP energetic particles / reconnection | pipeline-specified | Per-species power-law index from coupled 2D MHD + Parker transport vs. PSP HCS crossing |
| 2 | [mozer-2026-switchback-nonideal-dissipation](./mozer-2026-switchback-nonideal-dissipation/SKILL.md) | 2605.14114 | 2026 | PSP switchbacks / dissipation | pipeline-specified | Distribution of \|E_meas − E_ideal\| at switchback boundaries (13–40 R_s) |
| 3 | [dakeyo-2026-source-alignment-psp-solo](./dakeyo-2026-source-alignment-psp-solo/SKILL.md) | 2605.01511 | 2026 | PSP × SO radial evolution | pipeline-specified | Matched-pair Δv recovered within ±20% of paper |
| 4 | [li-2026-mercury-orbit-solar-wind-turbulence](./li-2026-mercury-orbit-solar-wind-turbulence/SKILL.md) | 2604.21196 | 2026 | Turbulence at 0.31–0.47 au (MESSENGER) | pipeline-specified | Inertial- + kinetic-range slope distributions; radial trend sign |
| 5 | [tenerani-2026-spherically-polarized-magnetic-fields](./tenerani-2026-spherically-polarized-magnetic-fields/SKILL.md) | 2605.04285 | 2026 | Switchback geometry theory | constructive | std(\|B\|)/mean(\|B\|) < 1e-10; RD between glued patches |

## Agent-runtime / AI-scientist comparison

| # | Slug | arXiv | Year | Role for HelioSI | Validation target |
|---|---|---|---|---|---|
| 6 | [agentic-ai-scientists-not-built-autonomous-discovery-2026](./agentic-ai-scientists-not-built-autonomous-discovery-2026/SKILL.md) | 2605.08956 | 2026 | Positioning / critique checklist | All 5 failure modes + 4 recommendations addressed in manuscript |
| 7 | [mind-ai-co-scientist-material-research-2026](./mind-ai-co-scientist-material-research-2026/SKILL.md) | 2604.13699 | 2026 | Architecture-template transfer | Four-step loop (hypothesis → in-silico → debate → modular) visible in Figure 2 |
| 8 | [heurekabench-2026-end-to-end-co-scientist-evaluation](./heurekabench-2026-end-to-end-co-scientist-evaluation/SKILL.md) | 2601.01678 | 2026 | Benchmark-design template | ≥ 1 paper-grounded end-to-end item executes and reproduces published finding |

## Notes

- The 8 skills are agent-facing skills, not paper summaries: each has a
  *when to use*, an *algorithm/workflow*, a *minimal executable benchmark
  or validation target*, *known pitfalls*, and a *HelioSI harness / skills
  / MCPs* relation section.
- Heliophysics skills (1–5) are operational scientific methods. Agent-
  runtime skills (6–8) are explicitly *positioning / comparison* skills
  whose job is to guide HelioSI manuscript design and benchmark
  upgrades — they do not pretend to be heliophysics workflows.
- The HelioSI framing is preserved: the **harness is general-purpose**;
  this *application domain instantiation* is heliophysics-specific.
- Every claim in the heliophysics skills is sourced to the inventories
  (`apj_aa_heliophysics_papers.md`, `psp_analysis_2020_2026.md`,
  `solar_wind_turbulence_2020_2026.md`). Quantitative details not present
  in the inventories are flagged inline as **TODO verify with full text**.

## Source inventories

- `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
- `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md`
- `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md`
- `sioulas-reproduction/results/agent_runtime_2026_only_synthesis.md`
- `sioulas-reproduction/results/agent_runtime_additional_exact_metadata.md`
- `sioulas-reproduction/results/heliosi_similar_papers_requirements_gap_plan.md`

## Weak entries needing full-text verification

| Skill | Items flagged TODO verify |
|---|---|
| murtas-2026 | DOI; exact MHD solver name; numerical spectral-index value; per-species `E_max` ordering direction |
| mozer-2026 | DOI; exact FIELDS L2 product IDs; classification-recall numeric target |
| dakeyo-2026 | Final venue (A&A vs ApJ); exact PSP × SO interval list; PFSS tool used by authors |
| li-2026 | DOI; journal; sign of kinetic-range-slope vs. r_au trend |
| tenerani-2026 | DOI; journal; exact constructive scheme equations; figure identifier |
| MIND 2026 | Full author list |
