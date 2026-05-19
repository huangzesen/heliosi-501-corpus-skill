---
name: stevens-2022-reconciling-psp-mhd-theory-plasma-frame
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# stevens-2022-reconciling-psp-mhd-theory-plasma-frame

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from M. L. Stevens et al. 2022 (arXiv preprint, arXiv:2206.11514).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Cross-comparison of PSP plasma-frame magnetic-fluctuation amplitudes to MHD turbulence predictions reconciles the inertial-range slopes by accounting for spacecraft-frame Doppler effects and local-mean-field decomposition.
- The skill applies to: PSP near-Sun intervals, plasma-frame correction methodology, inertial-range slope reconciliation with MHD theory.

### When NOT to use it

- Do not extend correction methodology naively to kinetic scales.
- Plasma-frame correction depends on local Alfven speed — flag.

### Claim boundary

PSP near-Sun intervals, plasma-frame correction methodology, inertial-range slope reconciliation with MHD theory.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Cross-comparison of PSP plasma-frame magnetic-fluctuation amplitudes to MHD turbulence predictions reconciles the inertial-range slopes by accounting for spacecraft-frame Doppler effects and local-mean-field decomposition.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst | PSP near-Sun intervals | SPDF/CDAWeb |
| PSP/SWEAP | L3 moments | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Doppler-correction sensitivity to plasma-velocity calibration.
- Local-mean-field window L choice biases slope.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Plasma-frame Doppler correction

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Local-mean-field-frame inertial-range slope fit

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

- **Tension** — Plasma-frame-corrected slopes differ from spacecraft-frame slopes — re-check Huang 2023 1/f scaling. Related: [[huang-2023-psp-one-over-f-spectrum]].
- **Minimal_experiment** — Apply the correction to Huang 2023 intervals; report corrected slope. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2206.11514
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §3.2`

## Skill graph

- [[huang-2023-psp-one-over-f-spectrum]]
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]
