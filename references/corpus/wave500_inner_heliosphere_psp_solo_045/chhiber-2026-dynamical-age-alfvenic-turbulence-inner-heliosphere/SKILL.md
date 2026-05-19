---
name: chhiber-2026-dynamical-age-alfvenic-turbulence-inner-heliosphere
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# chhiber-2026-dynamical-age-alfvenic-turbulence-inner-heliosphere

A paper-skill compiled from R. Chhiber et al. 2026 (arXiv preprint, arXiv:2603.25989).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A reformulated turbulence-age parameter accounting for Alfvenicity tracks the radial evolution of inner-heliosphere turbulence using PSP plus complementary spacecraft, showing systematic 'aging' with distance from the Sun consistent with reduced cross helicity at larger r.
- The skill applies to: Inner-heliosphere multi-mission survey, Alfvenicity-corrected turbulence-age parameter, statistical radial trend.

### When NOT to use it

- Do not infer absolute turbulence cascade-rate from age parameter alone.
- Aging-with-r is a statistical claim — individual streams may behave differently.

### Claim boundary

Inner-heliosphere multi-mission survey, Alfvenicity-corrected turbulence-age parameter, statistical radial trend.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A reformulated turbulence-age parameter accounting for Alfvenicity tracks the radial evolution of inner-heliosphere turbulence using PSP plus complementary spacecraft, showing systematic 'aging' with distance from the Sun consistent with reduced cross helicity at larger r.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG + SWEAP | L2/L3 | encounter cadence | PSP E1–E20 | SPDF/CDAWeb |
| Solar Orbiter/MAG + SWA | L2 | vector cadence | matching radial bins | SOAR |
| Wind/MFI + 3DP/SWE | L2 | various | 1 au comparison | SPDF/CDAWeb |
| Helios/E2,E3 MAG + plasma | archive (legacy) | archive cadence | 0.3–0.7 au legacy bins | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Correlation-length definition (integral vs Taylor) shifts age parameter.
- Helios legacy data have different calibration tier; flag separately.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Nonlinear-time computation from correlation lengths + δb amplitude

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Alfvenicity (σ_c, σ_r) classifier

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Alfvenicity-corrected turbulence-age formula

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

- **Gap** — No sibling skill measures the same age parameter using high-cadence kinetic-range correlation lengths. Related: (no explicit sibling).
- **Minimal_experiment** — Compute turbulence age on aligned PSP–SolO conjunction intervals; check radial trend within a single source. Related: [[telloni-2021-psp-solo-radial-alignment-turbulence]].

---

## Links

- arXiv: https://arxiv.org/abs/2603.25989
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §9`

## Skill graph

- [[sioulas-2022-magnetic-field-intermittency-psp-solo]]
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]
- [[telloni-2021-psp-solo-radial-alignment-turbulence]]
