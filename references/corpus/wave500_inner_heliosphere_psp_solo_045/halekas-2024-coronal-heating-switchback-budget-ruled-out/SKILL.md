# halekas-2024-coronal-heating-switchback-budget-ruled-out

A paper-skill compiled from J. Halekas et al. 2024 (ApJ).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Cross-comparison of PSP perihelion in-situ temperature, heat flux, and switchback occurrence shows the switchback energy flux is too small to balance the coronal-heating budget at the relevant radii — switchbacks are not the dominant coronal-heating channel.
- The skill applies to: PSP perihelion intervals, in-situ heating-budget closure, switchback-flux upper-bound estimate.

### When NOT to use it

- Do not rule out switchbacks as a local heating channel — claim is at coronal-heating-budget scale.
- Heating budget closure is mission-encounter-specific.

### Claim boundary

PSP perihelion intervals, in-situ heating-budget closure, switchback-flux upper-bound estimate.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Cross-comparison of PSP perihelion in-situ temperature, heat flux, and switchback occurrence shows the switchback energy flux is too small to balance the coronal-heating budget at the relevant radii — switchbacks are not the dominant coronal-heating channel.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/SWEAP SPC/SPAN-I + electron moments | L3 | encounter cadence | PSP perihelia | SPDF/CDAWeb |
| PSP/FIELDS MAG | L2 | 1 Hz/burst | PSP perihelia | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Heat-flux estimation requires electron moments which are intermittent on PSP.
- T-gradient inference is window-length and stream-type sensitive.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Heating-rate inference from in-situ T(r) gradient

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Switchback-flux energy estimate

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Closure check vs known coronal-heating budget

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

- **Tension** — Switchback ruled out for coronal-heating budget (Halekas 2024) — but Bowen 2024 cyclotron-resonant heating remains viable. Related: [[bowen-2024-extended-cyclotron-resonant-heating]].
- **Minimal_experiment** — On the same intervals, compute both cyclotron-resonant heating rate (Bowen 2024) and switchback-flux contribution; quantify the gap. Related: (no explicit sibling).

---

## Links

- arXiv: TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §4.3`

## Skill graph

- [[bowen-2023-landau-damping-proton-electron-heating]]
- [[bandyopadhyay-2020-energy-transfer-psp]]
