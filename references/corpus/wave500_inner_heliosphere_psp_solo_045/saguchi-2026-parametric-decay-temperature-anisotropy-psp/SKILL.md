---
name: saguchi-2026-parametric-decay-temperature-anisotropy-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# saguchi-2026-parametric-decay-temperature-anisotropy-psp

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from H. Saguchi et al. 2026 (arXiv preprint, arXiv:2604.22489).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- In PSP-constrained expanding-box conditions, temperature anisotropy substantially enhances the Alfvén-wave parametric-decay-instability growth rate, shaping the compressive-fluctuation budget in the near-Sun solar wind.
- The skill applies to: Expanding-box simulation constrained by PSP parameters, anisotropic-pressure PDI growth-rate analysis.

### When NOT to use it

- Do not infer absolute PDI saturation amplitudes from growth rate alone.
- Do not extend to non-Alfvenic streams — PDI seed wave assumed.

### Claim boundary

Expanding-box simulation constrained by PSP parameters, anisotropic-pressure PDI growth-rate analysis.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

In PSP-constrained expanding-box conditions, temperature anisotropy substantially enhances the Alfvén-wave parametric-decay-instability growth rate, shaping the compressive-fluctuation budget in the near-Sun solar wind.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 1 Hz | PSP encounters used to constrain expansion conditions | SPDF/CDAWeb |
| PSP/SWEAP | L3 VDF + moments | encounter cadence | matching intervals | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Closure choice (CGL vs higher-moment) shifts growth rate.
- Expanding-box assumes radial expansion only — neglects stream interaction.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Expanding-box MHD or hybrid simulation with anisotropic-pressure closure

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### PDI dispersion-relation analysis for anisotropic plasma

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

- **Hypothesis** — PDI enhancement by anisotropy explains observed compressible-fluctuation rise near the Sun (Gonzalez 2026) — testable via correlation of T_perp/T_par with slow-mode amplitude. Related: [[gonzalez-2026-compressible-fluctuations-balanced-imbalanced]].
- **Minimal_experiment** — Bin PSP intervals by T_perp/T_par and check slow-mode amplitude correlation. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2604.22489
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §5`

## Skill graph

- [[shoda-2021-turbulence-switchback-generation-alfvenic]]
