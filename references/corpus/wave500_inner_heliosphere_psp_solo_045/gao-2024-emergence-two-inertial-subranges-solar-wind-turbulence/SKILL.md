---
name: gao-2024-emergence-two-inertial-subranges-solar-wind-turbulence
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# gao-2024-emergence-two-inertial-subranges-solar-wind-turbulence

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from A. Gao (TODO verify first author) et al. 2024 (arXiv preprint, arXiv:2409.03090).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- High-resolution PSP magnetic-field data reveal two distinct sub-regimes inside the inertial range: a shallower −3/2 sub-range near the Sun (0.17 au) and a more developed −5/3 sub-range at 1 au, with a transition scale that moves with heliocentric distance.
- The skill applies to: PSP near-perihelion magnetic-field PSDs vs comparison 1 au data; sub-range identification methodology.

### When NOT to use it

- Do not extrapolate to outer heliosphere without complementary mission data.
- Sub-range fitting is window-length sensitive; document.

### Claim boundary

PSP near-perihelion magnetic-field PSDs vs comparison 1 au data; sub-range identification methodology.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

High-resolution PSP magnetic-field data reveal two distinct sub-regimes inside the inertial range: a shallower −3/2 sub-range near the Sun (0.17 au) and a more developed −5/3 sub-range at 1 au, with a transition scale that moves with heliocentric distance.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst | PSP near-perihelion intervals incl. 0.17 au | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Breakpoint search sensitive to window length and start frequency.
- Plasma-frame correction (Stevens 2022) may shift breakpoint.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### PSD computation per encounter window

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Two-segment power-law fit with breakpoint search

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

- **Hypothesis** — Sub-range breakpoint should track Alfven correlation length — testable on radial-aligned PSP–SolO conjunctions. Related: [[telloni-2025-psp-solo-radial-alignment-2022-december]].
- **Minimal_experiment** — Re-fit PSD on E10 (0.07 au) with two-segment model; compare breakpoint to expected correlation-length value. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2409.03090
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md §1.10`

## Skill graph

- [[huang-2023-psp-one-over-f-spectrum]]
- [[stevens-2022-reconciling-psp-mhd-theory-plasma-frame]]
- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]
