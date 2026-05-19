# iizawa-2025-inverse-cascade-magnetic-helicity-inner-heliosphere

A paper-skill compiled from M. Iizawa et al. 2025 (arXiv preprint, arXiv:2507.13213).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Reduced magnetic-helicity spectra from PSP exhibit a persistent inverse-cascade signature (low-k pile-up) from near-Sun out toward Mercury's orbit, consistent with helicity transport upscale in the inner heliosphere.
- The skill applies to: PSP magnetic-helicity spectral analysis across encounters spanning 0.05–0.5 au, single-spacecraft reduced helicity from FIELDS MAG.

### When NOT to use it

- Do not extend the cascade-direction claim past 1 au without additional spacecraft data.
- Single-spacecraft reduced helicity ≠ full 3D helicity — report this caveat.

### Claim boundary

PSP magnetic-helicity spectral analysis across encounters spanning 0.05–0.5 au, single-spacecraft reduced helicity from FIELDS MAG.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Reduced magnetic-helicity spectra from PSP exhibit a persistent inverse-cascade signature (low-k pile-up) from near-Sun out toward Mercury's orbit, consistent with helicity transport upscale in the inner heliosphere.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 Hz/burst | PSP E1–E18 (TODO verify range) | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Single-spacecraft reduced helicity has sign ambiguities at intermediate angles to k.
- Mean-field rotation contaminates low-k signal if intervals are too long.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Reduced magnetic-helicity spectrum from spacecraft-frame B(t)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Spectral decomposition into ω-bins

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Inverse-cascade detection: low-k pile-up signature

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

- **Tension** — Inverse cascade signature contrasts with forward-cascade turbulent-heating picture (Bandyopadhyay 2020) — both can coexist if scales are separate. Related: [[bandyopadhyay-2020-energy-transfer-psp]].
- **Minimal_experiment** — Joint reduced-helicity + cascade-rate analysis on PSP E10 perihelion interval; check whether scale separation is real. Related: [[bandyopadhyay-2020-energy-transfer-psp]].

---

## Links

- arXiv: https://arxiv.org/abs/2507.13213
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 §7`

## Skill graph

- [[huang-2023-psp-one-over-f-spectrum]]
- [[sioulas-2023-anisotropic-scaling-inner-heliosphere]]
