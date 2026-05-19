---
name: gurram-2026-mms-cme-sub-alfvenic-wind-1au
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# gurram-2026-mms-cme-sub-alfvenic-wind-1au

A paper-skill compiled from H. Gurram et al. 2026 (arXiv preprint, arXiv:2604.12000).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- MMS multi-point observations of a sub-Alfvénic interval inside a magnetic cloud at 1 au show negligible cross helicity in magnetic-field fluctuations, suggesting CME passage suppresses Alfvénic correlations even where PSP near-Sun sub-Alfvénic intervals retain them.
- The skill applies to: Single magnetic-cloud event at 1 au with MMS multi-point coverage; sub-Alfvénic interval cross-helicity measurement.

### When NOT to use it

- Do not generalise to all 1 au sub-Alfvénic intervals — this is one event.
- Not a comparison to all PSP sub-Alfvénic intervals — use Jiao 2023 or Adhikari 2026 as sibling baseline.

### Claim boundary

Single magnetic-cloud event at 1 au with MMS multi-point coverage; sub-Alfvénic interval cross-helicity measurement.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

MMS multi-point observations of a sub-Alfvénic interval inside a magnetic cloud at 1 au show negligible cross helicity in magnetic-field fluctuations, suggesting CME passage suppresses Alfvénic correlations even where PSP near-Sun sub-Alfvénic intervals retain them.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| MMS FGM + FPI | L2 | burst | magnetic-cloud event (TODO date) | SDC / SPDF |

### 2.4 Failure modes (skill memory)

- Cross-helicity normalisation sensitive to plasma-density calibration.
- Single-event statistical significance is limited.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Cross-helicity σ_c computation

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Sub-Alfvénic interval extraction from M_A < 1

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

- **Tension** — Sub-Alfvénic σ_c at 1 au (≈0) contrasts with PSP near-Sun sub-Alfvénic σ_c (non-trivial) — radial vs context-driven difference. Related: [[jiao-2023-steady-sub-alfvenic-solar-wind-psp]].
- **Minimal_experiment** — Restrict σ_c statistics to PSP sub-Alfvénic intervals inside vs outside ICME context; compare. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2604.12000
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §1`

## Skill graph

- [[jiao-2023-steady-sub-alfvenic-solar-wind-psp]]
