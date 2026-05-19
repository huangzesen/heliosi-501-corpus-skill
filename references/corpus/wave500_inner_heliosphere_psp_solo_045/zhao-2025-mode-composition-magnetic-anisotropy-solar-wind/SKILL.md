---
name: zhao-2025-mode-composition-magnetic-anisotropy-solar-wind
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# zhao-2025-mode-composition-magnetic-anisotropy-solar-wind

A paper-skill compiled from S. Zhao et al. 2025 (arXiv preprint, arXiv:2510.25636).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- MHD-eigenmode decomposition of solar-wind fluctuations shows compressible (slow/fast) modes concentrate quasi-parallel to the mean field while Alfvénic modes spread more broadly, explaining observed magnetic-anisotropy patterns.
- The skill applies to: MHD-scale solar-wind fluctuations, single-spacecraft eigenmode decomposition (sub-divergence + sub-curl projection); theory-and-observation comparison.

### When NOT to use it

- Do not apply mode-decomposition naively at kinetic scales (requires kinetic eigenmodes).
- Single-spacecraft decomposition has known sign/angle ambiguities — document.

### Claim boundary

MHD-scale solar-wind fluctuations, single-spacecraft eigenmode decomposition (sub-divergence + sub-curl projection); theory-and-observation comparison.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

MHD-eigenmode decomposition of solar-wind fluctuations shows compressible (slow/fast) modes concentrate quasi-parallel to the mean field while Alfvénic modes spread more broadly, explaining observed magnetic-anisotropy patterns.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 Hz | PSP encounter intervals (TODO verify) | SPDF/CDAWeb |
| Wind/MFI | L2 | 3 s | 1 au comparison intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Mode-decomposition assumes plane-wave geometry — fails in strongly intermittent intervals.
- Slow/fast contrast sensitive to plasma-β; report.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### MHD-eigenmode decomposition into Alfvén/slow/fast components

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional anisotropy histogram per mode

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

- **Hypothesis** — Parallel-mode concentration of slow/fast should explain spectral-break angular dependence — testable on PSP angle-conditioned spectra. Related: (no explicit sibling).
- **Gap** — No sibling skill applies kinetic-eigenmode decomposition (KAW, ICW) consistently to inner-heliosphere data. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2510.25636
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 §5`

## Skill graph

- [[sioulas-2023-anisotropic-scaling-inner-heliosphere]]
- [[cuesta-2022-compressible-turbulence-psp-themis-maven]]
