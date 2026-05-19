---
name: chen-2023-relation-switchbacks-turbulence-inner-heliosphere
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# chen-2023-relation-switchbacks-turbulence-inner-heliosphere

A paper-skill compiled from C. H. K. Chen (et al.) et al. 2023 (arXiv preprint, arXiv:2312.16521).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- PSP inner-heliosphere observations show that magnetic-switchback occurrence and surrounding turbulence intermittency are dynamically coupled — spectral indices and intermittency statistics shift inside vs outside switchback patches.
- The skill applies to: PSP inner-heliosphere encounter intervals, conditional-spectrum analysis inside/outside switchback patches.

### When NOT to use it

- Do not infer causation (turbulence-generates-switchback vs vice versa) from the coupling alone.
- Patch definition affects conditional set; document.

### Claim boundary

PSP inner-heliosphere encounter intervals, conditional-spectrum analysis inside/outside switchback patches.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

PSP inner-heliosphere observations show that magnetic-switchback occurrence and surrounding turbulence intermittency are dynamically coupled — spectral indices and intermittency statistics shift inside vs outside switchback patches.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst | PSP encounters with classified switchback patches | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Patch boundary smoothing affects conditional spectrum.
- Stream-type confounding — condition by σ_c.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Switchback-patch classifier

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional PSD inside/outside patches

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Intermittency moments (kurtosis) conditional on patch state

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

- **Tension** — Switchback-turbulence coupling sign depends on patch definition — Shoda 2021 generation hypothesis predicts one sign; Bale 2021 funnel-origin predicts another. Related: [[shoda-2021-turbulence-switchback-generation-alfvenic]], [[bale-2021-solar-source-switchbacks-magnetic-funnels]].
- **Minimal_experiment** — Apply both patch classifiers and compare conditional-spectrum delta-α sign. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2312.16521
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md §1.7`

## Skill graph

- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
- [[huang-2023-psp-one-over-f-spectrum]]
