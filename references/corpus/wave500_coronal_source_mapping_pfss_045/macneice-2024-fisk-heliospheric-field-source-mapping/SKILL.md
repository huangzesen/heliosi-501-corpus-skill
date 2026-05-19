---
name: macneice-2024-fisk-heliospheric-field-source-mapping
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# macneice-2024-fisk-heliospheric-field-source-mapping

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when source-mapping L1 disturbances with a *Fisk*-style heliospheric field rather than a pure Parker spiral on top of PFSS.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Identifying Coronal Sources of L1 Solar Wind Disturbances Using the Fisk Heliospheric Magnetic Field and Potential Field Source Surface Model
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2404.11219 (posted 2024-04-17)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Combining Fisk-field connectivity with PFSS source-surface topology yields source-region identifications for L1 disturbances that are statistically more consistent with EUV coronal-hole boundaries than Parker-only mapping.

### Method assumptions

- Fisk field can be parameterized for the studied interval.
- PFSS provides the source-surface topology.
- L1 disturbance catalog is independent of mapping.

### Data assumptions

- OMNI L1 disturbance catalog.
- Synoptic Br for the studied window.
- AIA-derived CH boundary maps.

### Failure modes (skill memory)

- Fisk-field parameters drift with cycle phase.
- PFSS R_ss sensitivity propagates into Fisk extension.
- CH-boundary segmentation drives the comparison metric.

### Figure / numerical targets

- Fisk-vs-Parker source-mapping comparison.
- Source-region overlap with EUV CH boundary.
- Per-disturbance attribution table.

### Claim boundary

**In scope.** The paper's window + Fisk-field parameterization.

**Out of scope — do NOT generalize:**

- Do NOT generalize to non-disturbance slow wind.
- Do NOT cite Fisk advantage outside the validated cycle phase.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `fisk.heliospheric_field()` | Fisk-field topology | parameter knob |
| `backmap.fisk_or_parker()` | back-mapping under both |  |
| `ch.detect_from_euv()` | CH boundary |  |
| `omni.fetch_disturbance_list()` | L1 disturbances |  |

### Procedure

1. Build L1 disturbance list.
2. Solve PFSS; build Fisk extension.
3. Back-map each disturbance under Parker and Fisk.
4. Compare source overlap with EUV CH boundary.

### Validation target

Recover Fisk-vs-Parker comparison statistic.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; Fisk-field implementation is paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-koukras-2022-backmapping-uncertainty-fast-wind]] for a unified backmapping-uncertainty framework.
- Generative hypothesis: replacing PFSS with outflowpy under the Fisk topology should change source-region attribution by amounts predictable from latitude.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-koukras-2022-backmapping-uncertainty-fast-wind]]

## Links

- arXiv: https://arxiv.org/abs/2404.11219
- arXiv HTML: https://arxiv.org/html/2404.11219
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- Fisk parameterization
- disturbance catalog
