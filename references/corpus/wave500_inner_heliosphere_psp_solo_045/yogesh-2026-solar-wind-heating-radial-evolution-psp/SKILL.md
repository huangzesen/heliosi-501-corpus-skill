---
name: yogesh-2026-solar-wind-heating-radial-evolution-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# yogesh-2026-solar-wind-heating-radial-evolution-psp

A paper-skill compiled from Yogesh et al. 2026 (arXiv preprint, arXiv:2602.10275).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A PSP-based radial-evolution survey shows that magnetic-field fluctuations carry sufficient free energy to generate proton beams and drive wave-particle heating in the near-Sun solar wind, with a clear radial-distance trend.
- The skill applies to: PSP encounter survey, near-Sun radial bins, magnetic-fluctuation free-energy + proton-beam co-occurrence statistics.

### When NOT to use it

- Do not infer global heating-budget closure from this study.
- Do not generalise the radial trend beyond PSP's perihelion range.

### Claim boundary

PSP encounter survey, near-Sun radial bins, magnetic-fluctuation free-energy + proton-beam co-occurrence statistics.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A PSP-based radial-evolution survey shows that magnetic-field fluctuations carry sufficient free energy to generate proton beams and drive wave-particle heating in the near-Sun solar wind, with a clear radial-distance trend.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz/burst | PSP encounters | SPDF/CDAWeb |
| PSP/SWEAP SPAN-I | L3 VDF | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Free-energy estimate sensitive to scale partition.
- VDF beam-classifier threshold needs documentation.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Free-energy estimate from δB^2 with appropriate scale partition

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Proton-beam identification in VDF

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional radial-bin statistics

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

- **Hypothesis** — Free-energy budget exceeds beam-generation cost by factor F(r); F should saturate near sub-Alfvenic transition. Related: (no explicit sibling).
- **Minimal_experiment** — Compute F(r) per encounter; check saturation near M_A → 1. Related: [[adhikari-2025-trans-alfvenic-region-psp-e8-e19]].

---

## Links

- arXiv: https://arxiv.org/abs/2602.10275
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §4`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[shankarappa-2025-free-energy-sources-ion-scale-waves-psp]]
