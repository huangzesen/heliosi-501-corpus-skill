---
name: raouafi-2023-psp-four-years-discoveries-solar-minimum
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# raouafi-2023-psp-four-years-discoveries-solar-minimum

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from N. Raouafi et al. 2023 (Space Science Reviews 219, 8, arXiv:2301.02727).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A community review synthesising PSP encounter-1 through encounter-12 results on coronal heating, switchback origin, Alfvén-surface crossings, and energetic-particle physics during solar cycle minimum.
- The skill applies to: Review-paper synthesis; not a primary observation — collected references through E12.

### When NOT to use it

- Do not use as primary citation for any specific physics claim — back to primary papers.
- Frozen at E12 (2023); later encounters not included.

### Claim boundary

Review-paper synthesis; not a primary observation — collected references through E12.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A community review synthesising PSP encounter-1 through encounter-12 results on coronal heating, switchback origin, Alfvén-surface crossings, and energetic-particle physics during solar cycle minimum.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

No in-situ / remote data dependencies (theory or methods paper).

### 2.4 Failure modes (skill memory)

- Stale beyond 2023 — late-mission encounters not included.
- Solar-minimum framing not applicable to late-mission (approaching solar max) data.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Topic-clustered review-synthesis methodology

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

- **Gap** — No companion review covers E13+ (approaching solar max) — update needed. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2301.02727
- DOI: https://doi.org/10.1007/s11214-023-00952-4
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §4.4`

## Skill graph

- [[fox-2016-psp-mission-design-orbit-encounters]]
- [[bale-2016-fields-instrument-suite-psp]]
- [[kasper-2016-sweap-investigation-psp]]
- [[mccomas-2016-isois-energetic-particle-investigation-psp]]
- [[vourlidas-2016-wispr-imaging-instrument-psp]]
