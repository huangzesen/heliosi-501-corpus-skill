---
name: cuesta-2023-scaling-anisotropy-stationary-background-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# cuesta-2023-scaling-anisotropy-stationary-background-psp

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from M. M. Cuesta et al. 2023 (arXiv preprint, arXiv:2303.10810).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- On PSP near-Sun intervals, conditioning anisotropy estimation on background-field stationarity sharpens the parallel/perpendicular structure-function contrast, modifying earlier reported MHD-scale anisotropy slopes.
- The skill applies to: PSP near-Sun intervals, MHD-scale structure functions, stationarity-conditioned anisotropy methodology.

### When NOT to use it

- Do not apply to non-stationary intervals — methodology specifically excludes them.
- Stationarity criterion is window-length dependent; document.

### Claim boundary

PSP near-Sun intervals, MHD-scale structure functions, stationarity-conditioned anisotropy methodology.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

On PSP near-Sun intervals, conditioning anisotropy estimation on background-field stationarity sharpens the parallel/perpendicular structure-function contrast, modifying earlier reported MHD-scale anisotropy slopes.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz/burst | PSP near-Sun intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Stationarity-test threshold biases the surviving interval set.
- Survivor bias: stationarity selection may correlate with stream type.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Stationarity-test for background-field (mean direction drift)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Local-mean-field structure-function method conditioned on stationarity

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

- **Tension** — Stationarity-conditioned anisotropy slopes differ from unconditioned estimates (Sioulas 2023) — methodological comparison needed. Related: [[sioulas-2023-anisotropic-scaling-inner-heliosphere]].
- **Minimal_experiment** — Run both methods on the same intervals and report slope deltas with statistical error bars. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2303.10810
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §3.5`

## Skill graph

- [[sioulas-2023-anisotropic-scaling-inner-heliosphere]]
- [[bowen-2022-anisotropic-turbulence-radial-evolution-psp]]
