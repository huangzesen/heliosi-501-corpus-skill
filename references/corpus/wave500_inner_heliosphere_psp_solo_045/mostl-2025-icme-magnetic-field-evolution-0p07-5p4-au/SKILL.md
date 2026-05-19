---
name: mostl-2025-icme-magnetic-field-evolution-0p07-5p4-au
description: Per-entry paper-skill in wave500_inner_heliosphere_psp_solo_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# mostl-2025-icme-magnetic-field-evolution-0p07-5p4-au

A paper-skill compiled from C. Möstl et al. 2025 (arXiv preprint, arXiv:2512.04730).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A unified 1976-event ICME catalog across 11 missions (1990–2025) supports power-law radial scaling of magnetic-cloud peak |B| and duration from 0.07 au (PSP) to 5.4 au, with revised exponents vs. earlier single-mission fits.
- The skill applies to: Statistical catalog work; radial scaling fit of magnetic cloud properties; multi-mission boundary harmonisation.

### When NOT to use it

- Do not treat catalog entries as event-level physical models — catalog is event boundaries + summary properties only.
- Do not infer internal ICME flux-rope topology from catalog statistics alone.

### Claim boundary

Statistical catalog work; radial scaling fit of magnetic cloud properties; multi-mission boundary harmonisation.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A unified 1976-event ICME catalog across 11 missions (1990–2025) supports power-law radial scaling of magnetic-cloud peak |B| and duration from 0.07 au (PSP) to 5.4 au, with revised exponents vs. earlier single-mission fits.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Multi-mission ICME catalogs (Möstl, Richardson–Cane, etc.) | derived | n/a | 1990–2025 | Möstl ICMECAT, HELIO archives |
| Mission MAG L2 products (PSP, SolO, Wind, ACE, STEREO, etc.) | L2 | varies | 1990–2025 | SPDF/CDAWeb / SOAR / Möstl ICMECAT |

### 2.4 Failure modes (skill memory)

- Boundary definition heterogeneity across catalogs biases scaling exponents.
- Selection effect: PSP perihelia oversample near-Sun ICMEs; statistical correction required.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Magnetic-obstacle boundary identification

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Power-law radial scaling fit (peak |B|, duration vs r)

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

- **Gap** — No sibling skill currently quantifies how ICME radial scaling depends on solar-cycle phase. Related: (no explicit sibling).
- **Minimal_experiment** — Restrict the fit to cycle-23 and cycle-24 maxima separately and compare exponents. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2512.04730
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §8`

## Skill graph

- [[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]
