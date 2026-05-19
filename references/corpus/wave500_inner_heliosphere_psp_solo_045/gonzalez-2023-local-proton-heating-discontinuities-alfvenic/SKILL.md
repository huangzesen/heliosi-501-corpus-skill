---
name: gonzalez-2023-local-proton-heating-discontinuities-alfvenic
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# gonzalez-2023-local-proton-heating-discontinuities-alfvenic

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from C. A. Gonzalez et al. 2023 (arXiv preprint, arXiv:2309.07862).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- PSP intervals show distinct kinetic signatures of local proton heating at magnetic discontinuities depending on Alfvenicity of the surrounding stream — indicating two different energization channels for the same structural class.
- The skill applies to: PSP near-Sun intervals, discontinuity-conditioned VDF analysis, Alfvenicity-classified streams.

### When NOT to use it

- Do not extend to outer-heliosphere discontinuities without re-running the classifier.
- Not a global heating-budget claim — local kinetic signature only.

### Claim boundary

PSP near-Sun intervals, discontinuity-conditioned VDF analysis, Alfvenicity-classified streams.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

PSP intervals show distinct kinetic signatures of local proton heating at magnetic discontinuities depending on Alfvenicity of the surrounding stream — indicating two different energization channels for the same structural class.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst | PSP encounter intervals | SPDF/CDAWeb |
| PSP/SWEAP SPAN-I | L3 VDF | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- PVI threshold sensitive to window length L.
- VDF sampling sparse compared to MAG burst — conditional averaging required.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Discontinuity identification (PVI, rotation angle)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Alfvenicity classification (σ_c)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional VDF anisotropy/temperature analysis at discontinuities

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

- **Hypothesis** — Heating-channel split tracks σ_c continuously, not via a single Alfvenic/non-Alfvenic dichotomy. Related: (no explicit sibling).
- **Minimal_experiment** — Re-bin PSP intervals by continuous σ_c quartiles and measure conditional T-jump at discontinuities. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2309.07862
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 2 §9`

## Skill graph

- [[pecora-2022-coherent-structures-proton-electron-heating]]
- [[damicis-2021-alfvenic-nonalfvenic-psp]]
