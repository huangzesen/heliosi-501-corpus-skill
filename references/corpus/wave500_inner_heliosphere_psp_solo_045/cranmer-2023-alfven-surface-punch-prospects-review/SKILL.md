---
name: cranmer-2023-alfven-surface-punch-prospects-review
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# cranmer-2023-alfven-surface-punch-prospects-review

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from S. R. Cranmer et al. 2023 (arXiv preprint, arXiv:2310.05887).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A review synthesising PSP Alfvén-surface crossings and forecasting PUNCH white-light imaging diagnostics of the corona/heliosphere interface; identifies imaging signatures that should correlate with in-situ M_A < 1 intervals.
- The skill applies to: Review paper; in-situ + imaging diagnostics; not a primary observational claim.

### When NOT to use it

- Do not use as primary observational evidence — refer to Kasper 2021, Adhikari 2025, Jiao 2023 for in-situ.
- PUNCH predictions are mission-design forecasts.

### Claim boundary

Review paper; in-situ + imaging diagnostics; not a primary observational claim.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A review synthesising PSP Alfvén-surface crossings and forecasting PUNCH white-light imaging diagnostics of the corona/heliosphere interface; identifies imaging signatures that should correlate with in-situ M_A < 1 intervals.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

No in-situ / remote data dependencies (theory or methods paper).

### 2.4 Failure modes (skill memory)

- Review-frozen prediction list; check post-2023 updates.
- Imaging signatures are line-of-sight averaged — beware degeneracy.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Imaging-signature catalog construction for Alfvén-surface crossings

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

- **Gap** — No skill maps PUNCH simulation to PSP in-situ M_A < 1 catalog for one-to-one comparison. Related: (no explicit sibling).
- **Minimal_experiment** — Build a synthetic PUNCH-style image from a PSP Alfvén-surface crossing model and check imaging-signature predictions. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2310.05887
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 2 §8`

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[adhikari-2026-alfven-transition-young-solar-wind-solar-max]]
- [[adhikari-2025-trans-alfvenic-region-psp-e8-e19]]
