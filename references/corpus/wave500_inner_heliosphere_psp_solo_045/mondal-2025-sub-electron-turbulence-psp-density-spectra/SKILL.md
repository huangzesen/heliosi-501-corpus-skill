---
name: mondal-2025-sub-electron-turbulence-psp-density-spectra
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# mondal-2025-sub-electron-turbulence-psp-density-spectra

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from S. Mondal et al. 2025 (arXiv preprint, arXiv:2509.17061).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- PSP density spectra derived from spacecraft-potential measurements steepen near ρ_e with slopes near −10/3 while the magnetic spectrum steepens more strongly — evidence that sub-ρ_e turbulence is dominated by electrostatic fluctuations consistent with an electron-entropy cascade.
- The skill applies to: PSP encounter intervals with high-cadence spacecraft-potential telemetry, sub-electron-scale frequency band, single-spacecraft spectrum analysis.

### When NOT to use it

- Do not infer global electron heating rate from spectral slope alone.
- Density-from-potential calibration is encounter-specific — document.

### Claim boundary

PSP encounter intervals with high-cadence spacecraft-potential telemetry, sub-electron-scale frequency band, single-spacecraft spectrum analysis.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

PSP density spectra derived from spacecraft-potential measurements steepen near ρ_e with slopes near −10/3 while the magnetic spectrum steepens more strongly — evidence that sub-ρ_e turbulence is dominated by electrostatic fluctuations consistent with an electron-entropy cascade.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS spacecraft potential | L2/L3 (density proxy) | burst cadence | PSP encounter windows (TODO verify) | SPDF/CDAWeb |
| PSP/FIELDS MAG | L2 | burst | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Spacecraft-potential→density calibration drifts with photoelectron environment.
- Aliasing/Nyquist effects near sub-electron scales require careful filtering.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Density derivation from spacecraft potential (calibration)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Density power-spectral-density computation

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Spectral-slope fitting in sub-electron range

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

- **Hypothesis** — If electrostatic dominance is universal at sub-ρ_e, then magnetic-spectrum index becomes a poor probe of electron heating — needs cross-check with electron-temperature gradient. Related: (no explicit sibling).
- **Gap** — No paper-skill yet links sub-electron density spectrum to electron heating-rate budget. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2509.17061
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §8`

## Skill graph

- [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]
- [[pulupa-2020-fields-merged-scm-fluxgate-product]]
