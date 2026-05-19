---
name: huang-2025-what-are-switchbacks-solitary-alfven-wave-model
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# huang-2025-what-are-switchbacks-solitary-alfven-wave-model

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from Z. Huang et al. 2025 (arXiv preprint, arXiv:2512.12585).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A 3D solitary Alfvén wave on open field lines with embedded rotational discontinuities reproduces large-amplitude 1D field reversals at constant |B|, providing a geometric interpretation of PSP-observed switchbacks as traversals of strongly curved open flux.
- The skill applies to: 3D model of constant-|B| field reversals as solitary structures interpreting PSP 1D time-series switchbacks; not a generation mechanism, not a statistical inversion of patch occurrence.

### When NOT to use it

- Do not treat this as a switchback-origin claim — it is a geometric interpretation, not a generation mechanism.
- Do not apply to non-Alfvénic streams or to compressible kinked structures.

### Claim boundary

3D model of constant-|B| field reversals as solitary structures interpreting PSP 1D time-series switchbacks; not a generation mechanism, not a statistical inversion of patch occurrence.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A 3D solitary Alfvén wave on open field lines with embedded rotational discontinuities reproduces large-amplitude 1D field reversals at constant |B|, providing a geometric interpretation of PSP-observed switchbacks as traversals of strongly curved open flux.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz or higher | PSP encounters with switchback patches | SPDF/CDAWeb |
| PSP/SWEAP SPC/SPAN-I | L3 | moments | matching encounters | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Sampling-direction dependence — different virtual paths through the same structure yield different 1D signatures.
- Does not predict patch occurrence rates or supergranulation spacing.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### 3D solitary Alfvén wave construction with embedded RDs (paper ref: Sec. 2–3)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### 1D virtual spacecraft sampling of curved open field (paper ref: Sec. 4)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Constant-|B| validation of synthetic time series

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

- **Tension** — Geometric interpretation vs. funnel-origin (Bale 2021) — both can be true simultaneously; mixture model needed. Related: [[bale-2021-solar-source-switchbacks-magnetic-funnels]].
- **Minimal_experiment** — Apply the solitary-wave virtual-sampling method to PSP E10–E16 to test whether 1D B-magnitude flatness predicts switchback geometry class. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2512.12585
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §6`

## Skill graph

- [[tenerani-2026-spherically-polarized-magnetic-fields]]
- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
