---
name: shankarappa-2025-free-energy-sources-ion-scale-waves-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# shankarappa-2025-free-energy-sources-ion-scale-waves-psp

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from N. Shankarappa et al. 2025 (arXiv preprint, arXiv:2512.11182).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A mission-wide PSP survey ties circularly-polarised ion-scale waves to specific free-energy sources in proton VDFs; left-handed waves grow toward the Sun reaching ~30% occurrence in near-Sun intervals.
- The skill applies to: PSP encounters with full-cadence FIELDS spectra + SPAN-I VDFs, ion-scale circular-polarisation detection, conditional VDF-instability map.

### When NOT to use it

- Do not extend free-energy attribution to non-circularly-polarised waves.
- Do not infer wave-particle energy transfer rates — this is occurrence and free-energy attribution only.

### Claim boundary

PSP encounters with full-cadence FIELDS spectra + SPAN-I VDFs, ion-scale circular-polarisation detection, conditional VDF-instability map.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A mission-wide PSP survey ties circularly-polarised ion-scale waves to specific free-energy sources in proton VDFs; left-handed waves grow toward the Sun reaching ~30% occurrence in near-Sun intervals.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~290 Sa/s burst | PSP E1–E19 | SPDF/CDAWeb |
| PSP/SWEAP SPAN-I | L3 VDF | encounter cadence | PSP E1–E19 | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Polarisation sign-convention ambiguity near radial-field intervals.
- Vlasov solver assumes bi-Maxwellian fits — multi-component VDFs may bias growth rates.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Circular-polarisation classifier for ion-scale waves

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Linear Vlasov–Maxwell instability solver applied to measured VDFs

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional free-energy attribution (beam, anisotropy, drift)

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

- **Hypothesis** — Left-handed-wave fraction's radial increase reflects rising parallel beam drift — testable on E14–E20. Related: (no explicit sibling).
- **Gap** — No skill yet quantifies the wave-particle heating rate from this LH-wave population. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2512.11182
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §7`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[kasper-2016-sweap-investigation-psp]]
