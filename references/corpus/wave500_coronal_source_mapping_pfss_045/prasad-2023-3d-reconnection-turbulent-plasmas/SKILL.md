---
name: prasad-2023-3d-reconnection-turbulent-plasmas
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# prasad-2023-3d-reconnection-turbulent-plasmas

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when identifying 3-D reconnection sites in turbulent coronal-MHD or PIC data, with PFSS / NLFFF establishing the large-scale topological context.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** A Method for Determining the Locations and Configurations of Magnetic Reconnection within 3-D Turbulent Plasmas
- **First author:** A. Prasad
- **Authors:** A. Prasad, TODO_verify
- **Year:** 2023
- **arXiv:** 2312.15589 (posted 2023-12-25)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A topology-based diagnostic locates 3-D reconnection sites in turbulent coronal plasmas with a recall rate matching ground-truth flux-rope and separator configurations.

### Method assumptions

- Topology diagnostic is robust to noise.
- Ground-truth reconnection events are independently labelled.

### Data assumptions

- MHD or PIC turbulent simulation data.
- PFSS or NLFFF large-scale context.

### Failure modes (skill memory)

- Numerical noise leads to spurious nulls.
- Ground-truth labelling is incomplete.

### Figure / numerical targets

- Recall-vs-precision curve.
- Reconnection-site map.

### Claim boundary

**In scope.** The simulated configurations.

**Out of scope — do NOT generalize:**

- Do NOT cite recall outside the labelled regime.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `mhd.turbulence_run()` | turbulent MHD/PIC |  |
| `topology.reconnection_diagnostic()` | diagnostic |  |
| `pfss.solve()` | context |  |

### Procedure

1. Run turbulent simulation.
2. Apply topology diagnostic.
3. Score against labelled ground-truth.
4. Compare with PFSS context.

### Validation target

Recall-vs-precision curve.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Simulation codes paper-specific; sunkit-magex.pfss for context.

---

## Layer 4 — Research-generation affordances

- Compose with [[brennan-2024-tracing-reconnecting-expanding-field-lines]] for a unified reconnection-vs-expansion classification framework.
- Generative hypothesis: turbulent-reconnection-site density predicts switchback occurrence at footpoints ([[raouafi-2025-switchback-coronal-jet-precursors]]).

---

## Skill graph → depends_on

- [[brennan-2024-tracing-reconnecting-expanding-field-lines]]

## Links

- arXiv: https://arxiv.org/abs/2312.15589
- arXiv HTML: https://arxiv.org/html/2312.15589
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- labelling protocol
- simulation code
