---
name: gonzalez-2026-compressible-fluctuations-balanced-imbalanced
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# gonzalez-2026-compressible-fluctuations-balanced-imbalanced

A paper-skill compiled from C. A. Gonzalez et al. 2026 (arXiv preprint, arXiv:2602.17606).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Multi-spacecraft (PSP + SolO) analysis attributes most compressible fluctuation power near the Sun to slow magnetosonic modes and finds non-trivial contributions to local heating in both balanced and imbalanced streams.
- The skill applies to: PSP + SolO inner-heliosphere streams classified by imbalance σ_c, compressible-mode decomposition + heating-budget contribution.

### When NOT to use it

- Do not infer a single dominant compressible mode in outer-heliosphere streams from this study.
- Heating-budget contribution is local — not an aggregate energetics claim.

### Claim boundary

PSP + SolO inner-heliosphere streams classified by imbalance σ_c, compressible-mode decomposition + heating-budget contribution.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Multi-spacecraft (PSP + SolO) analysis attributes most compressible fluctuation power near the Sun to slow magnetosonic modes and finds non-trivial contributions to local heating in both balanced and imbalanced streams.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz | PSP near-Sun intervals | SPDF/CDAWeb |
| PSP/SWEAP | L3 | encounter cadence | matching intervals | SPDF/CDAWeb |
| Solar Orbiter/MAG + SWA | L2 | vector cadence | PSP–SolO conjunction set | SOAR |

### 2.4 Failure modes (skill memory)

- Mode decomposition assumes plane-wave geometry — fails for intermittent slow-mode structures.
- Heating-rate inference depends on damping-rate model (Landau, transit-time, etc.).

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Mode-decomposition: Alfvén/slow/fast partitioning

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### σ_c imbalance classifier

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Local heating-rate contribution from compressible modes

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

- **Gap** — No skill quantifies the imbalance threshold above which slow-mode heating dominates Alfvénic heating near the Sun. Related: (no explicit sibling).
- **Hypothesis** — If slow-mode heating dominates the imbalanced near-Sun fraction, electron-vs-proton heating ratio should track imbalance — testable with PSP electron moments. Related: [[bowen-2023-landau-damping-proton-electron-heating]].

---

## Links

- arXiv: https://arxiv.org/abs/2602.17606
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §3`

## Skill graph

- [[cuesta-2022-compressible-turbulence-psp-themis-maven]]
- [[zhao-2025-mode-composition-magnetic-anisotropy-solar-wind]]
