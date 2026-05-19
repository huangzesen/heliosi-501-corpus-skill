# adhikari-2025-trans-alfvenic-region-psp-e8-e19

A paper-skill compiled from S. Adhikari et al. 2025 (arXiv preprint, arXiv:2510.07472).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Across PSP E8–E19, sub-Alfvénic intervals exhibit smaller normalized magnetic-fluctuation amplitudes and stronger turbulence anisotropy than super-Alfvénic neighbours; no polarity-reversing (>90°) switchbacks appear in the sub-Alfvénic sample.
- The skill applies to: PSP E8–E19, fluctuation-amplitude and anisotropy statistics segmented by Alfvén Mach number, switchback occurrence absence in sub-Alfvenic.

### When NOT to use it

- Do not extrapolate fluctuation-anisotropy contrast to the corona — boundary effects dominate.
- Polarity-reversing claim is amplitude-threshold dependent; report threshold.

### Claim boundary

PSP E8–E19, fluctuation-amplitude and anisotropy statistics segmented by Alfvén Mach number, switchback occurrence absence in sub-Alfvenic.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Across PSP E8–E19, sub-Alfvénic intervals exhibit smaller normalized magnetic-fluctuation amplitudes and stronger turbulence anisotropy than super-Alfvénic neighbours; no polarity-reversing (>90°) switchbacks appear in the sub-Alfvénic sample.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 Hz / burst | PSP E8–E19 | SPDF/CDAWeb |
| PSP/SWEAP SPC/SPAN-I | L3 | encounter cadence | PSP E8–E19 | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- δB/B is window-length dependent; report window.
- Polarity-reversing threshold (>90°) is arbitrary; sensitivity sweep advised.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Alfvén Mach number segmentation

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Normalized fluctuation amplitude (δB/B) statistics

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Switchback occurrence rate by deflection-angle bin

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

- **Gap** — No sibling skill measures the perpendicular-cascade timescale ratio sub/super-Alfvenic. Related: (no explicit sibling).
- **Hypothesis** — If anisotropy contrast scales with M_A, then trans-Alfvenic boundary acts as a filter on perpendicular cascade — testable via structure-function method. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2510.07472
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 §6`

## Skill graph

- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]
- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[jiao-2023-steady-sub-alfvenic-solar-wind-psp]]
