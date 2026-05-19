---
name: ofman-2025-large-scale-kelvin-helmholtz-cme-driven
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# ofman-2025-large-scale-kelvin-helmholtz-cme-driven

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from L. Ofman et al. 2025 (arXiv preprint, arXiv:2512.19942).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Remote-sensing identification of a large-scale Kelvin–Helmholtz wave on the flank of a CME in the upper corona, with vortex roll-up consistent with the shear-flow Alfvénic-threshold criterion.
- The skill applies to: Single CME event, upper-corona altitudes (above streamer cusp), KHI vortex identification in coronagraph and EUV imagery; not an in-situ in-situ statistical study.

### When NOT to use it

- Do not extend to lower-coronal KHI (different driver) or to in-situ shear instabilities downstream of the shock.
- Not a claim about KHI prevalence — only one event analysed.

### Claim boundary

Single CME event, upper-corona altitudes (above streamer cusp), KHI vortex identification in coronagraph and EUV imagery; not an in-situ in-situ statistical study.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Remote-sensing identification of a large-scale Kelvin–Helmholtz wave on the flank of a CME in the upper corona, with vortex roll-up consistent with the shear-flow Alfvénic-threshold criterion.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| STEREO/SECCHI COR or analogous coronagraph | L1/L2 | imaging cadence | CME event (TODO date) | SDAC / SOAR |
| SDO/AIA | L1 | 12 s / 304–171 Å | CME event | JSOC |

### 2.4 Failure modes (skill memory)

- Vortex visibility depends on viewing geometry — line-of-sight ambiguity.
- Shear-velocity estimate uncertain in coronagraph; threshold check is qualitative.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Vortex identification in coronagraph difference images

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Alfvénic-threshold (KH criterion) computation along flank

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

- **Gap** — No companion in-situ KHI skill at inner heliosphere; PSP/SolO flank crossings could be searched. Related: (no explicit sibling).
- **Minimal_experiment** — Search PSP MAG/SWA for KH-like B/v oscillations on the flank of catalogued CMEs (CDPP). Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2512.19942
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §4`

## Skill graph

(no paper-skill dependencies — self-contained)
