---
name: magyar-2024-synthetic-modeling-plasma-frame-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# magyar-2024-synthetic-modeling-plasma-frame-psp

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from N. Magyar et al. 2024 (arXiv preprint, arXiv:2405.12547).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A synthetic-MHD/turbulence-aided toolkit translates single-spacecraft PSP time series into the plasma frame, mitigating Taylor-hypothesis errors and sharpening comparison with turbulence theory.
- The skill applies to: Methodology paper; synthetic MHD/turbulence models + observed PSP time series; single-spacecraft Taylor-hypothesis bias correction.

### When NOT to use it

- Do not treat as a unique plasma-frame estimator — competes with multi-spacecraft approaches.
- Synthetic-model assumptions (isotropy, slab/2D fraction) bias the correction.

### Claim boundary

Methodology paper; synthetic MHD/turbulence models + observed PSP time series; single-spacecraft Taylor-hypothesis bias correction.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A synthetic-MHD/turbulence-aided toolkit translates single-spacecraft PSP time series into the plasma frame, mitigating Taylor-hypothesis errors and sharpening comparison with turbulence theory.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz/burst | PSP encounter test intervals | SPDF/CDAWeb |
| PSP/SWEAP | L3 | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Model class strongly biases the inferred plasma-frame spectrum.
- Local-versus-global mean-field assumption affects mapping.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Synthetic MHD/turbulence model generator

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Spacecraft-frame → plasma-frame mapping via model-data matching

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

- **Gap** — No skill compares model-corrected plasma-frame spectra to ML-inferred (Bloch-style) classifications. Related: [[paper-bloch-2024-uncertainty-nn-solar-wind-types]].
- **Minimal_experiment** — Apply the toolkit to a PSP–SolO conjunction interval and check that corrected spectra match across spacecraft. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2405.12547
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 2 §7`

## Skill graph

- [[stevens-2022-reconciling-psp-mhd-theory-plasma-frame]]
