---
name: damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from R. D'Amicis et al. 2026 (A&A).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Three-spacecraft tracking of Alfvénic slow-wind parcels from a common solar source through PSP (near-Sun), SolO (intermediate), and Wind (1 au) documents the radial evolution of σ_c, residual energy, and bulk speed in a single source stream.
- The skill applies to: Triple-spacecraft alignment events with PSP–SolO–Wind on the same source stream; parcel-tracking methodology; ASW class.

### When NOT to use it

- Do not generalise the radial-evolution claim to non-Alfvénic slow streams.
- Triple-alignment events are rare; sample size small.

### Claim boundary

Triple-spacecraft alignment events with PSP–SolO–Wind on the same source stream; parcel-tracking methodology; ASW class.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Three-spacecraft tracking of Alfvénic slow-wind parcels from a common solar source through PSP (near-Sun), SolO (intermediate), and Wind (1 au) documents the radial evolution of σ_c, residual energy, and bulk speed in a single source stream.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS MAG + SWEAP | L2/L3 | encounter cadence | triple-alignment events (TODO verify dates) | SPDF/CDAWeb |
| Solar Orbiter/MAG + SWA | L2 | vector cadence | triple-alignment events | SOAR |
| Wind/MFI + SWE | L2 | vector cadence | triple-alignment events | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- PFSS source-surface radius choice biases parcel matching.
- Multi-decade longitude drift in parcel back-mapping when v_sw evolves.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Parcel back-mapping (PFSS + ballistic + Parker-spiral)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### σ_c and σ_r evolution per parcel

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Triple-spacecraft alignment selection rules

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

- **Hypothesis** — σ_c evolution per parcel should match the WKB-Alfvenic-amplitude radial scaling — testable on each ASW parcel. Related: (no explicit sibling).
- **Gap** — No skill yet propagates the parcel approach to non-Alfvenic slow wind for contrast. Related: (no explicit sibling).

---

## Links

- arXiv: TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md cross-cutting refs (D'Amicis 2026 A&A)`

## Skill graph

- [[damicis-2021-alfvenic-nonalfvenic-psp]]
- [[damicis-2025-solo-swa-alfvenic-streams-validation]]
- [[dakeyo-2026-source-alignment-psp-solo-method-link]]
