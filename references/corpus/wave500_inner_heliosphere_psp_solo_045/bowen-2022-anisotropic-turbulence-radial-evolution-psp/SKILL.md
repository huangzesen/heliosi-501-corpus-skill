# bowen-2022-anisotropic-turbulence-radial-evolution-psp

A paper-skill compiled from T. A. Bowen et al. 2022 (arXiv preprint, arXiv:2205.14096).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Statistical distributions of magnetic-fluctuation anisotropy across multiple PSP encounters, binned by heliocentric distance, show systematic radial evolution of the anisotropy distribution shape (not just its mean).
- The skill applies to: PSP multi-encounter survey; magnetic-fluctuation anisotropy distributions per radial bin; shape statistics.

### When NOT to use it

- Do not extrapolate distributional shape to outer-heliosphere without sibling-mission cross-check.
- Mean-vs-distribution distinction matters — report both.

### Claim boundary

PSP multi-encounter survey; magnetic-fluctuation anisotropy distributions per radial bin; shape statistics.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Statistical distributions of magnetic-fluctuation anisotropy across multiple PSP encounters, binned by heliocentric distance, show systematic radial evolution of the anisotropy distribution shape (not just its mean).

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz/burst | PSP encounters (E1–E10+) | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Local-mean-field window L choice biases anisotropy assignment.
- Radial bin overlap with stream type may confound — condition.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Local-mean-field anisotropy estimator

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Radial-bin distribution-shape statistics (skewness, kurtosis)

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

- **Gap** — No skill links distributional shape to source-region class via PFSS mapping. Related: (no explicit sibling).
- **Hypothesis** — Distribution skewness should peak at the streamer-belt / coronal-hole boundary radial bin. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2205.14096
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §2.15`

## Skill graph

- [[sioulas-2022-magnetic-field-intermittency-psp-solo]]
- [[vech-2022-anisotropy-kinetic-scales-psp]]
