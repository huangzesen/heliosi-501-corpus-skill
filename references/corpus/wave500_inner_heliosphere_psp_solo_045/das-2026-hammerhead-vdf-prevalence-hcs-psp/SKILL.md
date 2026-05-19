---
name: das-2026-hammerhead-vdf-prevalence-hcs-psp
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# das-2026-hammerhead-vdf-prevalence-hcs-psp

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from S. B. Das et al. 2026 (arXiv preprint, arXiv:2603.11329).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Across PSP encounters 1–20 (cumulative), hammerhead-shaped proton VDFs are strongly prevalent within heliospheric-current-sheet-adjacent intervals, implicating local plasma processes (not solar-source preconditioning) in shaping the VDF near the HCS.
- The skill applies to: 20 PSP encounters, HCS-adjacent intervals, hammerhead VDF identification from SPAN-I 3D moments, statistical prevalence study only.

### When NOT to use it

- Do not claim the hammerhead VDF is unique to the HCS — it occurs elsewhere but not as densely.
- Not a claim about the physical generation mechanism of the VDF shape.

### Claim boundary

20 PSP encounters, HCS-adjacent intervals, hammerhead VDF identification from SPAN-I 3D moments, statistical prevalence study only.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Across PSP encounters 1–20 (cumulative), hammerhead-shaped proton VDFs are strongly prevalent within heliospheric-current-sheet-adjacent intervals, implicating local plasma processes (not solar-source preconditioning) in shaping the VDF near the HCS.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/SWEAP SPAN-I | L2/L3 VDF | ~7 s cadence (encounter mode) | PSP E1–E20 | SPDF/CDAWeb |
| PSP/FIELDS MAG | L2 | 1 Hz | PSP E1–E20 | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Hammerhead detection depends on SPAN-I energy-angle resolution and FOV coverage — incomplete VDFs cause false negatives.
- HCS boundary uncertainty: polarity gradient threshold and smoothing window choices alter the adjacency set.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Hammerhead VDF shape classifier (anisotropy + secondary lobe geometry)

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### HCS-adjacent interval definition from polarity reversal in MAG

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Conditional prevalence statistics

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

- **Gap** — No skill yet links hammerhead VDF prevalence to upstream/downstream wave activity in the same window. Related: (no explicit sibling).
- **Minimal_experiment** — Cross-correlate hammerhead-VDF detections with ion-cyclotron wave detections (Verniero 2020) on the same intervals. Related: [[verniero-2020-proton-beams-ion-scale-waves]].

---

## Links

- arXiv: https://arxiv.org/abs/2603.11329
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 2 §5`

## Skill graph

- [[kasper-2016-sweap-investigation-psp]]
- [[verniero-2020-psp-span-i-vdf-data-product]]
