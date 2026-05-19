# sun-2024-magnetic-island-wispr-psp

A paper-skill compiled from W. Sun (et al., TODO verify) et al. 2024 (arXiv preprint, arXiv:2407.07216).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A single magnetic-island/flux-rope structure imaged in WISPR white-light is reconstructed via 3D forward-modelling of the heliospheric flank; geometry and Thomson-scattering profile place the structure in the inner heliosphere.
- The skill applies to: Single event, WISPR-A/B imaging only, geometric and Thomson-scattering reconstruction.

### When NOT to use it

- Do not infer in-situ flux-rope topology from imaging alone.
- Single event — no statistical claim.

### Claim boundary

Single event, WISPR-A/B imaging only, geometric and Thomson-scattering reconstruction.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A single magnetic-island/flux-rope structure imaged in WISPR white-light is reconstructed via 3D forward-modelling of the heliospheric flank; geometry and Thomson-scattering profile place the structure in the inner heliosphere.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/WISPR-i + WISPR-o | L3 imaging | encounter cadence | single near-Sun pass (TODO verify date) | SPDF/CDAWeb / NRL WISPR archive |

### 2.4 Failure modes (skill memory)

- Line-of-sight ambiguity inherent to single-vantage white-light imaging.
- Thomson-scattering model assumes electron density profile — degenerate with structure thickness.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Thomson-scattering forward model for white-light reconstruction

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Magnetic-island flux-rope geometric fit

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

- **Gap** — No skill systematically pairs WISPR magnetic-island imaging with downstream PSP in-situ flux-rope catalog. Related: (no explicit sibling).
- **Minimal_experiment** — For each WISPR-imaged structure, search PSP MAG/SWEAP for the corresponding in-situ flux-rope crossing. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2407.07216
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md §3.10`

## Skill graph

- [[vourlidas-2016-wispr-imaging-instrument-psp]]
