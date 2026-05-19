# trotta-2023-interplanetary-shock-psp-solo-0p07au-0p7au

A paper-skill compiled from D. Trotta et al. 2023 (arXiv preprint, arXiv:2312.05983).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A CME-driven shock observed by PSP at 0.07 au and SolO at 0.7 au (2022-09-05) is characterized at both points; shock parameters (jump conditions, small-scale boundary features) differ in expected ways under radial expansion.
- The skill applies to: Single shock event 2022-09-05, two radial-aligned spacecraft, jump-condition fitting + small-scale boundary diagnostics.

### When NOT to use it

- Do not treat as a statistical radial-evolution claim — single event.
- Do not infer shock geometry from PSP single-point alone — multi-point context required.

### Claim boundary

Single shock event 2022-09-05, two radial-aligned spacecraft, jump-condition fitting + small-scale boundary diagnostics.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A CME-driven shock observed by PSP at 0.07 au and SolO at 0.7 au (2022-09-05) is characterized at both points; shock parameters (jump conditions, small-scale boundary features) differ in expected ways under radial expansion.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst | 2022-09-05 near-perihelion | SPDF/CDAWeb |
| PSP/SWEAP | L3 | encounter cadence | 2022-09-05 | SPDF/CDAWeb |
| Solar Orbiter/MAG | L2 | vector cadence | 2022-09-05 | SOAR |
| Solar Orbiter/SWA | L2 | moments | 2022-09-05 | SOAR |

### 2.4 Failure modes (skill memory)

- MVA-based shock normal sensitive to noise; multiple methods recommended.
- Plasma-moment cadence at 0.07 au limits jump-precision; document interval averaging.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Rankine–Hugoniot fitting

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Shock-normal estimation from coplanarity/MVA

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Cross-radial shock-parameter comparison

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

- **Gap** — No systematic catalog yet of dual-spacecraft shock observations under PSP–SolO radial alignment. Related: (no explicit sibling).
- **Minimal_experiment** — Build a multi-event catalog of PSP–SolO aligned shocks and fit radial evolution per shock class. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2312.05983
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §13`

## Skill graph

- [[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]
- [[muller-2020-solar-orbiter-mission-overview]]
