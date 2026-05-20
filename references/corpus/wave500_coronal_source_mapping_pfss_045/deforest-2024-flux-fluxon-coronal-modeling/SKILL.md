---
name: deforest-2024-flux-fluxon-coronal-modeling
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# deforest-2024-flux-fluxon-coronal-modeling

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when modelling the coronal field with *fluxons* (discrete flux-tube primitives) rather than a grid, particularly when sub-grid topology matters.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Field Line Universal relaXer (FLUX): A Fluxon Approach to Coronal Magnetic Field Modeling
- **First author:** C. E. DeForest
- **Authors:** C. E. DeForest, TODO_verify
- **Year:** 2024
- **arXiv:** 2402.10370 (posted 2024-02-15)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

The FLUX fluxon model reproduces PFSS open-field maps at comparable cost while exposing sub-grid topology (e.g., fluxon entrapment in active-region complexes) that gridded PFSS smears out.

### Method assumptions

- Photospheric Br can be decomposed into discrete flux elements.
- Fluxon relaxation converges to a force-free / potential state within tolerance.
- Fluxon density is sufficient to resolve relevant topology.

### Data assumptions

- Synoptic or full-disk Br.
- Optional EUV imagery for validation.

### Failure modes (skill memory)

- Fluxon-count insufficient for AR-rich CRs.
- Relaxation can stall in nontrivial topologies.
- Comparison to gridded PFSS depends on density-equivalent.

### Figure / numerical targets

- Fluxon open-field map vs PFSS open-field map.
- Fluxon connectivity diagram for an AR complex.
- Cost-vs-resolution table.

### Claim boundary

**In scope.** FLUX as released; representative CRs.

**Out of scope — do NOT generalize:**

- Do NOT cite FLUX for current-carrying NLFFF problems without a non-potential extension.
- Do NOT compare FLUX to PFSS at incompatible resolutions.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `fluxon.decompose_br()` | Br→fluxons | density knob |
| `fluxon.relax_to_potential()` | FLUX relaxation |  |
| `fluxon.open_field_map()` | open-field map |  |
| `pfss.solve()` | reference PFSS |  |

### Procedure

1. Decompose Br into fluxons.
2. Relax to potential state.
3. Build fluxon open-field map.
4. Compare to gridded PFSS at matched effective resolution.

### Validation target

Match gridded-PFSS open-field map at convergence.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- FLUX is a paper-specific code; sunkit-magex.pfss for reference.

---

## Layer 4 — Research-generation affordances

- Compose with [[raouafi-2025-switchback-coronal-jet-precursors]] — fluxon connectivity should expose jet-driven switchback footpoints missed by gridded PFSS.
- Generative hypothesis: fluxon-density convergence rate is a topology-complexity diagnostic at the CR level.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2402.10370
- arXiv HTML: https://arxiv.org/html/2402.10370
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- FLUX version
- fluxon-density convention
