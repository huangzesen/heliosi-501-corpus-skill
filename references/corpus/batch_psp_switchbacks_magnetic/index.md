# Batch — PSP switchbacks, magnetic structures, and magnetic-field analysis

Generated 2026-05-18 by the HelioSI paper-to-skill factory (batch
`batch_psp_switchbacks_magnetic`).

This batch compiles 12 PSP-era papers into **harness-agnostic, runtime-
neutral** paper-skills spanning switchback generation, switchback
structure, boundary reconnection / topology, the Alfvén transition,
coronal-hole radial evolution, and small-scale magnetic structures.

## Framing — runtime-neutral by construction

Each `SKILL.md` is written so that the science is independent of *how*
an agent or human executes it. **LingTai and Claude Code are adapters,
not assumptions.** A skill is callable from any harness whose tools can
satisfy the abstract *capability contracts* declared in the skill.

Every paper-skill in this batch is organised in **four layers**:

| Layer | Purpose |
|---|---|
| **1. Trigger + claim boundary** | When to use the skill; what the paper does and explicitly does not say. |
| **2. Scientific invariant layer** | Claims, equations, methods, data assumptions, failure modes, figure / numerical targets. Runtime-independent. |
| **3. Executable protocol layer** | Abstract capability contracts (`C-FETCH-*`, `C-MVA`, `C-WALEN`, ...) and a step-by-step procedure stated against those contracts. |
| **4. Adapter / runtime notes** | *Optional examples only.* Illustrative bindings to Claude Code, LingTai, or a researcher notebook. None are requirements. |

Plus a fifth section, **Research-generation affordance**, that lists
gaps, tensions, and candidate experiments unlocked by composing this
paper with siblings in the corpus.

The compilation map from the factory spec still holds, but it is now
phrased without any runtime-specific terms:

| Paper element | Agent-native form |
|---|---|
| Claims / results | → **Verifiable tasks** anchored by `claim_boundary` |
| Methods / equations | → **Executable procedure** stated against capability contracts |
| Data / instruments / code | → **Capability contracts** (instrument, level, cadence, archive — no MCP names asserted) |
| Caveats / failure modes | → **Skill memory** (the §2.4 list) |
| Figures / numerical results | → **Benchmark targets** (§2.5) |
| Corpus / citations | → **Skill graph** (`[[paper-...]]` edges in the final section) |

No skill below names a specific runtime tool as a *requirement*. The
only thing the skill demands is that a runtime can, by *some* means,
satisfy the capability contracts in §3.

## Skills

| # | Slug | arXiv / DOI | Year | Theme | Compilation type | Key validation target |
|---|---|---|---|---|---|---|
| 1 | [shoda-2021-turbulence-switchback-generation-alfvenic](./shoda-2021-turbulence-switchback-generation-alfvenic/SKILL.md) | doi:10.3847/1538-4357/abfdbc | 2021 | Switchback generation (turbulence) | scientific-method (pilot/stub) | Occurrence-vs-`r` monotonic trend; spherical-polarisation metric ≲ 0.1 inside packets |
| 2 | [agapitov-2023-structure-origin-switchbacks-psp](./agapitov-2023-structure-origin-switchbacks-psp/SKILL.md) | doi:10.3847/1538-4357/acd17e | 2023 | Switchback structure / origin | scientific-method (pilot) | Non-zero RD-classified fraction; Walén-slope peak near ±1 |
| 3 | [adhikari-2026-alfven-transition-young-solar-wind-solar-max](./adhikari-2026-alfven-transition-young-solar-wind-solar-max/SKILL.md) | doi:10.3847/1538-4357/ae2c78 | 2026 | Alfvén-transition statistics | scientific-method (pilot) | Sub-Alfvénic interval recovery; `M_A` PDF match |
| 4 | [verniero-2020-proton-beams-ion-scale-waves](./verniero-2020-proton-beams-ion-scale-waves/SKILL.md) | doi:10.3847/1538-4365/ab86af | 2020 | Beam-driven ion-scale waves | scientific-method (pilot) | Linear-Vlasov positive growth + handedness match |
| 5 | [perrone-2022-coronal-hole-wind-psp-solo-conjunction](./perrone-2022-coronal-hole-wind-psp-solo-conjunction/SKILL.md) | doi:10.1051/0004-6361/202243989 | 2022 | PSP × SO coronal-hole conjunction | scientific-method (pilot) | σ_c trend sign + magnitude; slope at SO |
| 6 | [kasper-2021-psp-enters-magnetically-dominated-corona](./kasper-2021-psp-enters-magnetically-dominated-corona/SKILL.md) | doi:10.1103/PhysRevLett.127.255101 | 2021 | First sub-Alfvénic PSP intervals | scientific-method (pilot) | Encounter-8 sub-Alfvénic interval boundaries within ~1 min |
| 7 | [phan-2022-switchback-boundary-reconnection-psp](./phan-2022-switchback-boundary-reconnection-psp/SKILL.md) | arXiv:2101.06279 | 2022 | Switchback-boundary reconnection | scientific-method (pilot) | Walén slope ≈ ±1 with high corr on named event |
| 8 | [bale-2021-solar-source-switchbacks-magnetic-funnels](./bale-2021-solar-source-switchbacks-magnetic-funnels/SKILL.md) | arXiv:2109.01069 | 2021 | Switchback origin (solar funnels) | scientific-method (pilot) | Patch-spacing within ×2 of supergranulation scale |
| 9 | [mozer-2021-magnetic-pressure-balance-domains-psp](./mozer-2021-magnetic-pressure-balance-domains-psp/SKILL.md) | arXiv:2110.08506 | 2021 | Pressure-balance domains | scientific-method (pilot) | Per-PBD `corr(δP_B, δP_th) < −0.5`; PBD duration shape |
| 10 | [agapitov-2020-localized-magnetic-structures-boundaries](./agapitov-2020-localized-magnetic-structures-boundaries/SKILL.md) | arXiv:2003.05409 | 2020 | Localized structures + boundaries | scientific-method (pilot) | Full-reversal population in named interval |
| 11 | [wang-2020-magnetic-holes-psp-solar-wind](./wang-2020-magnetic-holes-psp-solar-wind/SKILL.md) | arXiv:2010.14008 | 2020 | Magnetic-hole catalog | scientific-method (pilot) | Hole count ±25% on named encounter |
| 12 | [phan-2023-switchback-boundaries-closed](./phan-2023-switchback-boundaries-closed/SKILL.md) | arXiv:2310.12134 | 2023 | Switchback-boundary topology | scientific-method (pilot) | Per-event topology label agreement ≥ 75% |

All entries are at **`paper-grounded-pending-full-text`** quality level
— bibliographic anchor, claim boundary, capability contracts, procedure,
failure modes, and figure targets are present and inventory-grounded,
but specific numerical thresholds, exact figure fractions, and DOIs /
journal venues marked `TODO verify with full text` must be tightened by
a reviewer-agent pass against the primary source before promotion past
`method-ready` per the factory spec §7.

## Relation to the 2026 pilot batch

The pilot batch under `../pilot_2026_and_runtime/` overlaps thematically
and is *cross-referenced*, not duplicated:

- `mozer-2026-switchback-nonideal-dissipation` (pilot) ⇄ this batch's
  switchback-boundary reconnection / structure / topology skills
  (#2, #7, #12).
- `dakeyo-2026-source-alignment-psp-solo` (pilot) ⇄ this batch's
  `perrone-2022-coronal-hole-wind-psp-solo-conjunction` (#5).
- `tenerani-2026-spherically-polarized-magnetic-fields` (pilot) ⇄
  this batch's `shoda-2021-turbulence-switchback-generation-alfvenic`
  (#1) — competing geometric vs. turbulent framing of the same
  `|B|` ≈ const invariant.

Skill-graph edges live in each `SKILL.md`'s final section as
`[[paper-slug]]` references.

## Research-generation surface

The five new §5 sections (one per skill) collectively expose a set of
*composed* experiments that none of the individual papers performs.
Highlights:

- **Origin-hypothesis bake-off** between turbulence (#1) and solar
  funnels (#8) via *joint* statistics over patch spacing and
  spherical-polarisation; both quantities are produced by the
  respective skills' protocols on the same PSP interval.
- **Reconnection-fraction conditioned on RD/TD class**: composing #2,
  #7, #12 gives the conditional probability `P(exhaust | RD)` that no
  single paper computes.
- **PBD × hole × sub-Alfvénic intersection**: composing #6 (or #3), #9,
  #11 produces a 3-way intersection catalog of plasma-pressure-
  segmented intervals.
- **Cycle effect on Alfvén transition**: applying the *same* detector
  parameters from #6 to #3 separates cycle physics from methodological
  drift.

These are deliberately listed as *gaps and tensions* rather than as
prescriptive plans, so that downstream research-generation skills (the
fifth-layer prompts) can pick them up without being locked to a
specific runtime.

## Weak entries needing full-text verification

| Skill | Items flagged TODO verify |
|---|---|
| shoda-2021 | arXiv ID; exact simulation grid + equation set; exact occurrence-vs-`r` numerics; existence of public code repo |
| agapitov-2023 | arXiv ID; full author list; exact reported RD-fraction; encounter list |
| adhikari-2026 | arXiv ID; full author list; exact sub-Alfvénic interval list; PFSS tool + source-surface height |
| verniero-2020 | arXiv ID; linear-Vlasov solver identity; exact event intervals; SPAN-I cadence used |
| perrone-2022 | exact conjunction dates; PSD method; σ_c trend direction |
| kasper-2021 | full author list; exact Encounter-8 interval timestamps; density proxy (QTN vs. SPC); reported Alfvén radius |
| phan-2022 | DOI; exact event list; reported Walén-slope tolerance; sign convention |
| bale-2021 | DOI; full author list; encounter list; PFSS tool / source-surface height |
| mozer-2021 | DOI; full author list; exact PBD residual threshold; whether `T_e` used |
| agapitov-2020 | DOI; full author list; deflection threshold; analyzed interval list |
| wang-2020 | DOI; full author list; detection threshold and depth peak; encounter coverage |
| phan-2023 | DOI / venue; full author list; reported topology fraction; event list |

## Source inventories

- `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §2.4–2.13, 3.1, 3.3
- `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md` (sibling support)
- `sioulas-reproduction/results/arxiv_papers/extended_search.md` §3.1, 3.2, 3.7

## Compilation invariants this batch preserves

- **Runtime neutrality.** No skill body mandates LingTai-specific APIs
  (e.g. `mcp:cdaweb`, named LingTai skills) as requirements. Such
  bindings appear only in §4 "Adapter / runtime notes" as illustrative
  examples; the capability contracts in §3 are the contract.
- **Claim boundary in every SKILL.md.** Each skill explicitly refuses
  one or more generalisations beyond the paper's sampled conditions.
- **No hallucinated citations.** Every `paper.*` field traces to the
  inventory entries listed in §"Source inventories" above. Anything
  not in the inventory is flagged `TODO verify with full text`.
- **Skill graph is explicit.** Each SKILL.md ends with a `[[...]]` edge
  list; sibling and competing-hypothesis skills are cross-referenced
  rather than duplicated.
- **Research-generation affordance is a first-class layer**, not a
  postscript: each skill articulates the gaps, tensions, and candidate
  experiments it opens up when composed with siblings.
