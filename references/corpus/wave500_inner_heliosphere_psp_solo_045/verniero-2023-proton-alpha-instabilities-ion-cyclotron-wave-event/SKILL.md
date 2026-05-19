---
name: verniero-2023-proton-alpha-instabilities-ion-cyclotron-wave-event
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# verniero-2023-proton-alpha-instabilities-ion-cyclotron-wave-event

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from J. L. Verniero et al. 2023 (arXiv preprint, arXiv:2310.14136).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Linear-Vlasov stability analysis using PSP SPAN-I 3D VDFs during a single ion-cyclotron wave event identifies the proton and alpha free-energy sources driving the observed wave activity.
- The skill applies to: Single ion-cyclotron wave event, multi-species Vlasov analysis from 3D VDF input; not a statistical claim.

### When NOT to use it

- Do not generalise to all ion-cyclotron events — single-case study.
- Alpha VDF measurement is harder than proton VDF — document caveats.

### Claim boundary

Single ion-cyclotron wave event, multi-species Vlasov analysis from 3D VDF input; not a statistical claim.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Linear-Vlasov stability analysis using PSP SPAN-I 3D VDFs during a single ion-cyclotron wave event identifies the proton and alpha free-energy sources driving the observed wave activity.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/SWEAP SPAN-I + SPAN-Ai | L3 VDF | encounter cadence | single event (TODO verify) | SPDF/CDAWeb |
| PSP/FIELDS MAG + DFB | L2 | burst | matching window | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Bi-Maxwellian fits to proton+alpha VDFs lose structure relevant to instability.
- Alpha density uncertainty propagates to growth rate.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Multi-species linear-Vlasov solver from measured VDFs

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Free-energy source attribution per species

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

- **Gap** — Single-event study; no skill maps proton vs alpha contribution across many ICW events. Related: (no explicit sibling).
- **Minimal_experiment** — Apply the same multi-species solver to the Shankarappa 2025 LH-wave event catalog. Related: [[shankarappa-2025-free-energy-sources-ion-scale-waves-psp]].

---

## Links

- arXiv: https://arxiv.org/abs/2310.14136
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §3.6`

## Skill graph

- [[verniero-2020-proton-beams-ion-scale-waves]]
- [[shankarappa-2025-free-energy-sources-ion-scale-waves-psp]]
