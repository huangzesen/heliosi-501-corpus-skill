# agapitov-2023-constraints-alfvenicity-switchbacks

A paper-skill compiled from O. V. Agapitov et al. 2023 (arXiv preprint, arXiv:2312.01011).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- The departure from Alfvenicity within individual switchbacks (delta-v vs Alfven-prediction ratio) increases with deflection-angle amplitude, with a sharp non-Alfvenic excess at deflections >120°.
- The skill applies to: PSP-observed switchback events with measured proton bulk velocity and B; ratio test inside switchback only; not at the boundary.

### When NOT to use it

- Do not apply at switchback boundaries — different physics (reconnection, Phan 2022).
- Not a generation-mechanism claim.

### Claim boundary

PSP-observed switchback events with measured proton bulk velocity and B; ratio test inside switchback only; not at the boundary.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

The departure from Alfvenicity within individual switchbacks (delta-v vs Alfven-prediction ratio) increases with deflection-angle amplitude, with a sharp non-Alfvenic excess at deflections >120°.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz | PSP encounters with classified switchbacks | SPDF/CDAWeb |
| PSP/SWEAP SPC/SPAN-I | L3 moments | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Density estimate uncertainty propagates into Alfvén-speed and ratio.
- Deflection-angle definition (background-B baseline) shifts the bin assignment.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Switchback event detection with documented threshold

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### delta-v vs ±delta-B/√(μ_0 ρ) ratio computation inside the event

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional binning by deflection angle

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

- **Hypothesis** — Non-Alfvenic excess at large deflection is the signature of reconnection-driven boundaries leaking inward into the event interior. Related: (no explicit sibling).
- **Minimal_experiment** — Stack PSP switchbacks by deflection-angle bin and compare delta-v residuals near vs far from documented reconnection-exhaust boundaries. Related: [[phan-2022-switchback-boundary-reconnection-psp]].

---

## Links

- arXiv: https://arxiv.org/abs/2312.01011
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §14`

## Skill graph

- [[phan-2022-switchback-boundary-reconnection-psp]]
- [[agapitov-2023-structure-origin-switchbacks-psp]]
