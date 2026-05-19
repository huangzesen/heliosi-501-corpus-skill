---
name: schwadron-2022-switchback-deflections-beyond-early-encounters
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# schwadron-2022-switchback-deflections-beyond-early-encounters

A paper-skill compiled from N. M. Schwadron et al. 2022 (MNRAS, 517, 1001).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Magnetic-deflection statistics for PSP encounters 4–8 show a clear radial-trend dependence in switchback occurrence rate beyond the very early encounters, with implications for switchback longevity.
- The skill applies to: PSP E4–E8 magnetic-deflection statistics, radial-trend fit, occurrence-rate metric only.

### When NOT to use it

- Do not extend the trend to encounters after E8 without re-running the classifier.
- Single-classifier dependence — robustness sweep recommended.

### Claim boundary

PSP E4–E8 magnetic-deflection statistics, radial-trend fit, occurrence-rate metric only.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Magnetic-deflection statistics for PSP encounters 4–8 show a clear radial-trend dependence in switchback occurrence rate beyond the very early encounters, with implications for switchback longevity.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz | PSP E4–E8 | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Threshold dependence on classifier definition.
- Radial-bin width choice impacts trend slope.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Deflection-angle classifier with documented threshold

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Radial-bin occurrence-rate statistic

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

- **Gap** — No skill extends this trend through E20 with a consistent classifier. Related: (no explicit sibling).
- **Minimal_experiment** — Apply Schwadron classifier verbatim to PSP E9–E20; report radial trend continuity. Related: (no explicit sibling).

---

## Links

- arXiv: TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §3.4`

## Skill graph

- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
- [[agapitov-2023-structure-origin-switchbacks-psp]]
