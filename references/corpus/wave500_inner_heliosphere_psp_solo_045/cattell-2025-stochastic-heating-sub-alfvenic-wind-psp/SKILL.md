---
name: cattell-2025-stochastic-heating-sub-alfvenic-wind-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# cattell-2025-stochastic-heating-sub-alfvenic-wind-psp

A paper-skill compiled from C. Cattell (et al., PSP team) et al. 2025 (Physical Review Letters, arXiv:2509.20654).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Stochastic-heating diagnostic δB_perp / B applied to PSP E14+ sub-Alfvenic intervals shows substantial heating rates, with implications for the local energy budget in the magnetically dominated regime.
- The skill applies to: PSP E14+ sub-Alfvénic intervals only, stochastic-heating diagnostic via fluctuation amplitudes; not a closure budget.

### When NOT to use it

- Do not extend rate estimate to super-Alfvenic neighbours without re-running the diagnostic.
- Stochastic-heating theory has β-dependent threshold — flag.

### Claim boundary

PSP E14+ sub-Alfvénic intervals only, stochastic-heating diagnostic via fluctuation amplitudes; not a closure budget.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Stochastic-heating diagnostic δB_perp / B applied to PSP E14+ sub-Alfvenic intervals shows substantial heating rates, with implications for the local energy budget in the magnetically dominated regime.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz/burst | PSP E14+ sub-Alfvenic intervals | SPDF/CDAWeb |
| PSP/SWEAP | L3 moments | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Threshold-amplitude assumption (chaotic-gyromotion onset) is theoretical; sub-Alfvenic regime under-tested.
- Density / v_A calibration uncertainty propagates.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Stochastic-heating-rate formula from Chandran et al. with δB_perp / B input

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Sub-Alfvenic interval definition (M_A < 1)

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

- **Hypothesis** — Stochastic-heating rate should peak just inside Alfvén surface and drop deeper sub-Alfvenic. Related: (no explicit sibling).
- **Minimal_experiment** — Apply the diagnostic on a continuous E14 sub-Alfvenic crossing and bin by depth (1 − M_A). Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2509.20654
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §1.20`

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[jiao-2023-steady-sub-alfvenic-solar-wind-psp]]
