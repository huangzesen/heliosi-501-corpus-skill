---
name: woodham-2024-alpha-proton-differential-flow-young-solar-wind
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# woodham-2024-alpha-proton-differential-flow-young-solar-wind

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from L. D. Woodham (TODO verify first author) et al. 2024 (arXiv preprint, arXiv:2401.10457).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Alpha-proton differential flow speed across the sub-/super-Alfvénic transition in young Alfvénic streams shows reduced drift on the sub-Alfvénic side, suggesting wave-mediated coupling that activates beyond the Alfvén surface.
- The skill applies to: PSP sub-Alfvénic and super-Alfvénic intervals classified by M_A; alpha-proton drift measurement from SPAN-I + SPAN-Ai.

### When NOT to use it

- Do not extend to non-Alfvenic streams — selection-conditioned analysis.
- Alpha measurement requires SPAN-Ai availability — encounter-specific.

### Claim boundary

PSP sub-Alfvénic and super-Alfvénic intervals classified by M_A; alpha-proton drift measurement from SPAN-I + SPAN-Ai.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Alpha-proton differential flow speed across the sub-/super-Alfvénic transition in young Alfvénic streams shows reduced drift on the sub-Alfvénic side, suggesting wave-mediated coupling that activates beyond the Alfvén surface.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/SWEAP SPAN-I (proton) | L3 VDF/moments | encounter cadence | sub/super-Alfvenic intervals | SPDF/CDAWeb |
| PSP/SWEAP SPAN-Ai (alpha) | L3 VDF/moments | encounter cadence | matching intervals | SPDF/CDAWeb |
| PSP/FIELDS MAG | L2 | 1 Hz | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Alpha-particle moment calibration sensitive to fit-routine choice.
- M_A boundary uncertainty propagates to sub/super classification.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### M_A classification (sub vs super)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Alpha-proton drift speed estimation per species moment

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

- **Hypothesis** — Drift suppression sub-Alfvenic is wave-driven — predicts correlation with local ion-cyclotron wave power. Related: [[shankarappa-2025-free-energy-sources-ion-scale-waves-psp]].
- **Minimal_experiment** — Jointly bin drift speed and LH-wave occurrence across the Alfvén surface crossings. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2401.10457
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md §4.7`

## Skill graph

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[jiao-2023-steady-sub-alfvenic-solar-wind-psp]]
