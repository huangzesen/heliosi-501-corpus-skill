# ervin-2024-slow-alfvenic-source-regions-psp

A paper-skill compiled from T. Ervin et al. 2024 (arXiv preprint, arXiv:2407.09684).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- In PSP E4–E14, the slow Alfvenic solar wind (SASW) splits into two source populations via PFSS + ballistic mapping: predominantly low-B0 (small coronal holes / over-expanded boundaries) and a smaller high-B0 fraction with distinct heavy-ion signatures.
- The skill applies to: PSP E4–E14 near-perihelion intervals, SASW class only, PFSS-based source mapping; not an open-flux closure claim.

### When NOT to use it

- Do not infer slow non-Alfvenic source statistics from this skill.
- Do not extend to encounter sets outside E4–E14 without re-running the mapping.

### Claim boundary

PSP E4–E14 near-perihelion intervals, SASW class only, PFSS-based source mapping; not an open-flux closure claim.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

In PSP E4–E14, the slow Alfvenic solar wind (SASW) splits into two source populations via PFSS + ballistic mapping: predominantly low-B0 (small coronal holes / over-expanded boundaries) and a smaller high-B0 fraction with distinct heavy-ion signatures.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz | PSP E4–E14 perihelia | SPDF/CDAWeb |
| PSP/SWEAP SPC/SPAN-I | L3 moments | encounter cadence | PSP E4–E14 | SPDF/CDAWeb |
| GONG/ADAPT synoptic magnetogram | synoptic | Carrington-rate | matching CRs | NSO/GONG, NSO/ADAPT |

### 2.4 Failure modes (skill memory)

- PFSS source-surface radius choice biases footpoint location.
- Alfvenicity threshold sensitive to averaging window; report L.
- Synoptic-map epoch mismatch produces footpoint drift on rapidly evolving boundaries.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### PFSS source-surface extrapolation

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Ballistic back-trace from PSP to source surface

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Alfvenicity classifier (σ_c, σ_r) for stream selection

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

- **Gap** — No skill maps the heavy-ion contrast inside SASW intervals to the same dual-source picture. Related: [[rivera-2024-mixed-source-signatures-switchback-patches-heavy-ions]].
- **Hypothesis** — If low-B0 SASW dominates at solar minimum, fraction should drop at solar max — testable using late-mission PSP encounters. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2407.09684
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §12`

## Skill graph

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-sunkit-magex-magnetic-field-extrapolation]]
- [[damicis-2021-alfvenic-nonalfvenic-psp]]
