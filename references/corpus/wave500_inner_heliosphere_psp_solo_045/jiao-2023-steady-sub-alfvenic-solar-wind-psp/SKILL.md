---
name: jiao-2023-steady-sub-alfvenic-solar-wind-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# jiao-2023-steady-sub-alfvenic-solar-wind-psp

A paper-skill compiled from Y. Jiao et al. 2023 (arXiv preprint, arXiv:2311.15622).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Ten+ steady sub-Alfvénic intervals identified across PSP E8–E14 share reduced density and velocity, suppress switchbacks, and trace back via magnetic source-mapping to coronal-hole boundaries or pseudostreamer/streamer interfaces.
- The skill applies to: PSP E8–E14, steady (>several-hour) sub-Alfvénic intervals only, magnetic source-mapping by PFSS + ballistic propagation.

### When NOT to use it

- Do not extend the switchback-suppression claim to transient (<hour) sub-Alfvénic excursions.
- Do not infer global Alfvén-surface geometry from this discrete-interval list.

### Claim boundary

PSP E8–E14, steady (>several-hour) sub-Alfvénic intervals only, magnetic source-mapping by PFSS + ballistic propagation.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Ten+ steady sub-Alfvénic intervals identified across PSP E8–E14 share reduced density and velocity, suppress switchbacks, and trace back via magnetic source-mapping to coronal-hole boundaries or pseudostreamer/streamer interfaces.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz | PSP E8–E14 | SPDF/CDAWeb |
| PSP/SWEAP SPC/SPAN-I + QTN | L3 | encounter cadence | PSP E8–E14 | SPDF/CDAWeb |
| Synoptic magnetograms | synoptic | CR | matching encounters | GONG/ADAPT |

### 2.4 Failure modes (skill memory)

- Density proxy choice (QTN vs SPC) shifts v_A and M_A.
- Duration threshold sensitivity not always reported — varies the interval count.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Alfvén Mach number M_A = v_sw / v_A computation

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Steady-interval extraction with documented duration threshold

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### PFSS + ballistic source-mapping

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

- **Tension** — Switchback suppression in sub-Alfvénic intervals (this paper) vs presence of small-amplitude deflections in Adhikari 2026 — definition of 'switchback' affects the disagreement. Related: [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]].
- **Minimal_experiment** — Apply uniform amplitude threshold to both papers' interval lists and recount. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2311.15622
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §15`

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]
