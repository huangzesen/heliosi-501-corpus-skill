---
name: rivera-2024-mixed-source-signatures-switchback-patches-heavy-ions
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# rivera-2024-mixed-source-signatures-switchback-patches-heavy-ions

A paper-skill compiled from Y. J. Rivera et al. 2024 (arXiv preprint, arXiv:2409.03645).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Heavy-ion composition within adjacent switchback patches sampled by PSP and Solar Orbiter during P11 lineup shows internally mixed source signatures, inconsistent with a single coronal-hole origin for all patches.
- The skill applies to: PSP P11 lineup with Solar Orbiter, adjacent magnetic switchback patches, composition contrast across patches via heavy-ion charge states and elemental ratios.

### When NOT to use it

- Do not extrapolate the mixed-source result to all PSP encounters without re-running the lineup analysis.
- Not a claim about individual switchback origin — operates at patch-mixture level.

### Claim boundary

PSP P11 lineup with Solar Orbiter, adjacent magnetic switchback patches, composition contrast across patches via heavy-ion charge states and elemental ratios.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Heavy-ion composition within adjacent switchback patches sampled by PSP and Solar Orbiter during P11 lineup shows internally mixed source signatures, inconsistent with a single coronal-hole origin for all patches.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz or higher | PSP P11 (2022 Feb) | SPDF/CDAWeb |
| Solar Orbiter/SWA HIS | L2 | heavy-ion composition | PSP P11 SolO lineup | SOAR |
| Solar Orbiter/MAG | L2 | vector cadence | PSP P11 SolO lineup | SOAR |

### 2.4 Failure modes (skill memory)

- Cadence mismatch — heavy-ion samples are much sparser than B; conditional binning required.
- Patch definition sensitive to clustering threshold; report explicitly.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Patch-by-patch heavy-ion composition contrast (Q_Fe, He/H ratios)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### PFSS + ballistic mapping to compare back to photospheric source

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### 3.2 Capability contracts

The runtime must supply:

- **C-FETCH-DATA**: time-series read of the instruments listed in §2.3.
- **C-CLASSIFIER**: event/interval classifier (paper-specific).
- **C-METRIC**: numerical comparison to a paper figure/table (TODO verify full text).

These contracts name no MCP, plugin, or harness command. Adapter binding
examples (if any) live in §4 and `adapter_notes[]` in the frontmatter; the
contract itself remains runtime-neutral.

### 3.3 Minimum reproduction artifacts

- A run log capturing data interval(s), thresholds, and algorithm parameters.
- One numerical scalar or shape statistic comparable to a paper figure/table.
- A JSON/CSV side-car recording inputs, parameters, and the comparison metric.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness capable of CDF I/O + standard time-series analysis can satisfy
  the contracts; named tools (pyspedas, sunpy, sunkit-magex, pfsspy,
  sw-scanner) are *example* adapters, not requirements.
- Encounter-specific data ranges should be obtained from the paper's full
  text; adapter glue is the runtime's responsibility.

---

## 5. Research-generation affordance

- **Tension** — Composition heterogeneity inside patches challenges single-funnel origin assumption from Bale 2021. Related: [[bale-2021-solar-source-switchbacks-magnetic-funnels]].
- **Gap** — No sibling skill quantifies the heavy-ion contrast threshold above which two patches are 'different sources'. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2409.03645
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §10`

## Skill graph

- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
- [[ervin-2024-slow-alfvenic-source-regions-pfss-psp]]
- [[owen-2020-solo-swa-plasma-suite]]
