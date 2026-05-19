# vech-2022-anisotropy-kinetic-scales-psp

A paper-skill compiled from D. Vech et al. 2022 (arXiv preprint, arXiv:2203.10475).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- PSP inner-heliosphere FIELDS data analysed in a local-mean-field frame show angle-dependent break-scale of the kinetic-range spectrum, evidencing sub-ion-scale anisotropy that varies with the angle between flow and mean-B.
- The skill applies to: PSP inner-heliosphere intervals, sub-ion-scale FIELDS spectra, local-mean-field-frame angle-resolved break scale.

### When NOT to use it

- Do not generalise to 1 au without re-running the angle-resolved decomposition.
- Break-scale depends on ρ_p definition; document.

### Claim boundary

PSP inner-heliosphere intervals, sub-ion-scale FIELDS spectra, local-mean-field-frame angle-resolved break scale.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

PSP inner-heliosphere FIELDS data analysed in a local-mean-field frame show angle-dependent break-scale of the kinetic-range spectrum, evidencing sub-ion-scale anisotropy that varies with the angle between flow and mean-B.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst (~290 Sa/s) | PSP encounter perihelion windows | SPDF/CDAWeb |
| PSP/SWEAP | L3 moments | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Local-mean-field window length L affects angle assignment.
- Doppler effects shift sub-ion-scale break at high flow-speed angles.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Local-mean-field-frame decomposition

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Angle-conditioned PSD computation

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Break-scale fit per angle bin

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

- **Tension** — Angle-dependent break may bias single-direction inertial-range slope claims. Related: (no explicit sibling).
- **Minimal_experiment** — Re-do Huang 2023 1/f spectral fit conditioned on flow-angle bin and check slope robustness. Related: [[huang-2023-psp-one-over-f-spectrum]].

---

## Links

- arXiv: https://arxiv.org/abs/2203.10475
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §2.14`

## Skill graph

- [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]
- [[sioulas-2023-anisotropic-scaling-inner-heliosphere]]
