---
name: sharma-2026-sub-ion-current-sheets-kinetic-alfven-turbulence
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# sharma-2026-sub-ion-current-sheets-kinetic-alfven-turbulence

A paper-skill compiled from J. Sharma et al. 2026 (arXiv preprint, arXiv:2601.18131).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Particle-in-cell simulations of kinetic Alfvén wave turbulence resolving electron scales produce intermittent current sheets and coherent structures at sub-ion scales, tying dissipation to small-scale geometry consistent with PSP kinetic-range spectral signatures.
- The skill applies to: 2D/3D PIC simulation with electron-scale resolution; KAW turbulence regime; structural diagnostic, not a heating-rate budget.

### When NOT to use it

- Do not extrapolate dissipation rates from PIC to in-situ without scaling argument.
- PIC mass-ratio may not be realistic — report.

### Claim boundary

2D/3D PIC simulation with electron-scale resolution; KAW turbulence regime; structural diagnostic, not a heating-rate budget.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Particle-in-cell simulations of kinetic Alfvén wave turbulence resolving electron scales produce intermittent current sheets and coherent structures at sub-ion scales, tying dissipation to small-scale geometry consistent with PSP kinetic-range spectral signatures.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

No in-situ / remote data dependencies (theory or methods paper).

### 2.4 Failure modes (skill memory)

- Reduced mass-ratio in PIC compresses ion-electron scale separation.
- 2D vs 3D differences in coherent-structure morphology.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Particle-in-cell simulation of KAW turbulence

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Current-sheet identification at sub-ion scales

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### PVI/coherent-structure statistics in synthetic data

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

- **Hypothesis** — Sub-ion current-sheet fraction (PVI > τ at sub-ion lag) increases inward — testable on PSP near-Sun burst MAG. Related: (no explicit sibling).
- **Minimal_experiment** — Compute PVI at fixed sub-ion lag (~ρ_p) across PSP E1–E20; compare to PIC distribution shape. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2601.18131
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 §3`

## Skill graph

- [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]
- [[pecora-2022-coherent-structures-proton-electron-heating]]
