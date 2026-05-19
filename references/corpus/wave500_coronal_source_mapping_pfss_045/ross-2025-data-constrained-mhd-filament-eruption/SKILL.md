---
name: ross-2025-data-constrained-mhd-filament-eruption
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# ross-2025-data-constrained-mhd-filament-eruption

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when initializing a data-constrained MHD eruption simulation from PFSS + NLFFF + observed flow drivers for a specific AR/CME event.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Data-Constrained Magnetohydrodynamic Simulation of a Filament Eruption in a Decaying Active Region 13079 on 2022-08-17
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2504.15069 (posted 2025-04-21)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

For AR 13079 on 17 Aug 2022, a data-constrained MHD eruption initialized from PFSS+NLFFF reproduces the observed filament morphology and eruption-onset timing within the paper's tolerance.

### Method assumptions

- PFSS+NLFFF gives a valid initial state for the MHD run.
- Observed flow-driver (e.g., electric field) is consistent with the AR's evolution.
- MHD code is converged at the chosen grid.

### Data assumptions

- HMI vector magnetograms for the AR.
- AIA + SDO context EUV.
- GOES flare timing.

### Failure modes (skill memory)

- NLFFF non-uniqueness — boundary preparation matters.
- MHD grid coarseness alters reconnection rate and onset.
- Flow-driver inversion has gauge ambiguity.

### Figure / numerical targets

- Pre-eruption flux-rope topology.
- Filament-eruption morphology vs AIA.
- Onset timing comparison.

### Claim boundary

**In scope.** AR 13079 on 2022-08-17 with the paper's MHD setup.

**Out of scope — do NOT generalize:**

- Do NOT generalize the onset-time match to other ARs without re-running.
- Do NOT cite flux-rope topology independent of the NLFFF boundary prep.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_hmi_vector()` | AR vector Br |  |
| `nlfff.solve()` | AR-volume NLFFF | boundary prep |
| `pfss.solve()` | global background |  |
| `mhd.eruption_run()` | data-constrained MHD | grid + driver |
| `imagery.fetch_aia()` | EUV validation |  |

### Procedure

1. Prepare HMI vector boundary; solve NLFFF.
2. Embed in PFSS global background.
3. Drive MHD simulation with observed flow / E-field.
4. Track flux-rope rise; compare onset time and morphology to AIA.

### Validation target

Match observed eruption-onset time within the paper's tolerance and morphology qualitatively.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- PFSS via sunkit-magex.pfss; MHD via paper-specific code (not asserted here).

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-razquin-2026-coronal-dimming-magnetic-flux-may2024]] for an end-to-end dimming-vs-MHD-eruption reconciliation skill.
- Generative hypothesis: replacing NLFFF interior with [[paper-multi-constraint-pfss-extrapolation-model]] should shift the simulated onset time by a measurable amount.

---

## Skill graph → depends_on

- [[paper-multi-constraint-pfss-extrapolation-model]]
- [[paper-flare-precursor-fine-scale-topology-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2504.15069
- arXiv HTML: https://arxiv.org/html/2504.15069
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- MHD code identity
- NLFFF boundary-prep method
