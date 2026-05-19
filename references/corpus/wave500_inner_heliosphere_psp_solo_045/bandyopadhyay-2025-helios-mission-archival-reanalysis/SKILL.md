---
name: bandyopadhyay-2025-helios-mission-archival-reanalysis
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# bandyopadhyay-2025-helios-mission-archival-reanalysis

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from R. Bandyopadhyay (TODO verify first author) et al. 2025 (arXiv preprint (stub)).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A reanalysis of the Helios mission archival magnetic-field + plasma data using modern PSP-era methodology (local-mean-field structure functions, σ_c classification) cross-checks PSP-derived turbulence radial-scaling against the 0.3–1.0 au Helios baseline.
- The skill applies to: Helios E1/E2 archival data over 0.3–1.0 au; modern reanalysis methodology; cross-mission baseline check for PSP-extrapolated turbulence scaling.

### When NOT to use it

- Do not treat as a new measurement — methodology applied to legacy data; calibration differences from PSP era are real.
- Do not infer kinetic-scale physics from Helios — its cadence is insufficient.

### Claim boundary

Helios E1/E2 archival data over 0.3–1.0 au; modern reanalysis methodology; cross-mission baseline check for PSP-extrapolated turbulence scaling.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A reanalysis of the Helios mission archival magnetic-field + plasma data using modern PSP-era methodology (local-mean-field structure functions, σ_c classification) cross-checks PSP-derived turbulence radial-scaling against the 0.3–1.0 au Helios baseline.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Helios E1/E2 MAG (Helios I, II) | archive (legacy) | ≈4 s vector | 0.3–1.0 au orbits | SPDF/CDAWeb (Helios merged) |
| Helios E1/E2 plasma (proton moments) | archive | ≈40 s | 0.3–1.0 au orbits | SPDF/CDAWeb |
| PSP/FIELDS MAG + SWEAP | L2/L3 | encounter cadence | PSP encounters mapped to 0.3–0.7 au bins for comparison | SPDF/CDAWeb |

### 2.4 Failure modes (skill memory)

- Helios calibration vintage — cross-check independent reductions before claiming cross-mission consistency.
- Plasma cadence at Helios is much sparser than PSP — conditional binning must account for this.
- Source-region matching impossible at Helios resolution — comparisons remain population-statistical.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Local-mean-field structure-function methodology applied to Helios archive

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### σ_c / σ_r Alfvenicity classifier on Helios merged plasma+MAG

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Radial-bin alignment between Helios and PSP

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

- **Gap** — No paper-skill currently rehouses Helios in modern PSP-style local-mean-field structure functions on a unified slug. Related: (no explicit sibling).
- **Minimal_experiment** — Apply the Sioulas 2022 PVI / structure-function pipeline to Helios E1 merged data on a 0.3-au shell and check kurtosis-scaling consistency with PSP-derived trends. Related: [[sioulas-2022-magnetic-field-intermittency-psp-solo]].

---

## Links

- arXiv: TODO_verify_with_full_text
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §1.15 (PSP+Helios+Wind spectral evolution)`

## Skill graph

- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]
- [[chhiber-2026-dynamical-age-alfvenic-turbulence-inner-heliosphere]]
