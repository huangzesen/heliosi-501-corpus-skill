---
name: choi-2024-whistler-waves-young-solar-wind-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# choi-2024-whistler-waves-young-solar-wind-psp

A paper-skill compiled from K.-E. Choi et al. 2024 (arXiv preprint, arXiv:2408.00736).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Whistler-wave amplitude and propagation-direction statistics from PSP E1–E11 show a substantial counter-streaming component near the Sun, sufficient to scatter strahl electrons and regulate the local heat flux.
- The skill applies to: PSP E1–E11, FIELDS spectral matrix analysis, whistler-band wave-vector reconstruction; statistics only, not a heat-flux closure budget.

### When NOT to use it

- Do not infer the global solar-wind heat-flux closure from this statistic alone.
- Do not apply outside the FIELDS frequency band (whistler range).

### Claim boundary

PSP E1–E11, FIELDS spectral matrix analysis, whistler-band wave-vector reconstruction; statistics only, not a heat-flux closure budget.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Whistler-wave amplitude and propagation-direction statistics from PSP E1–E11 show a substantial counter-streaming component near the Sun, sufficient to scatter strahl electrons and regulate the local heat flux.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS DFB + SCM | L2/L3 spectral matrices | burst mode | PSP E1–E11 | SPDF/CDAWeb |
| PSP/SWEAP electron moments (where available) | L3 | encounter cadence | PSP E1–E11 | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Spectral-matrix method assumes single plane wave per frequency bin — fails for overlapping wave packets.
- Spacecraft-frame Doppler shifts must be removed for propagation-direction inference.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### k-vector reconstruction from B-spectral matrices

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Polarisation + propagation-angle joint statistic

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

- **Hypothesis** — Counter-streaming whistler power should scale with strahl deficit — testable on encounters with strahl + whistler statistics jointly. Related: (no explicit sibling).
- **Gap** — No companion skill maps the corresponding outer-heliospheric whistler statistic; cross-mission extension proposed. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2408.00736
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §11`

## Skill graph

- [[pulupa-2020-fields-merged-scm-fluxgate-product]]
- [[bale-2016-fields-instrument-suite-psp]]
