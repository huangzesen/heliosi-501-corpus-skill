---
name: milligan-2024-flares-sympathetic-angular-separation
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# milligan-2024-flares-sympathetic-angular-separation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when testing magnetic-connection hypotheses for sympathetic flares using PFSS-traced AR-to-AR topology distances on the source surface.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Flaring Together: A Preferred Angular Separation Between Sympathetic Flares on the Sun
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2412.10143 (posted 2024-12-13)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Sympathetic flare pairs cluster at a preferred angular separation that aligns with PFSS-traced AR connectivity rather than great-circle distance alone.

### Method assumptions

- Flare pairs can be operationally defined within Δt window.
- PFSS connectivity between ARs is meaningful for sympathy.

### Data assumptions

- GOES flare list with AR identifiers.
- Synoptic Br for the studied cycle.

### Failure modes (skill memory)

- Δt window defines the sympathy population.
- PFSS misses sub-resolution AR substructure.

### Figure / numerical targets

- Sympathy frequency vs angular separation.
- PFSS-connected vs unconnected pair histograms.

### Claim boundary

**In scope.** Paper's flare-list and PFSS configuration.

**Out of scope — do NOT generalize:**

- Do NOT cite preferred separation outside the modelled cycle.
- Do NOT attribute sympathy solely to PFSS connectivity.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `flare.fetch_goes_list()` | flare list |  |
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `topology.ar_connectivity()` | AR-to-AR PFSS distance |  |

### Procedure

1. Build flare-pair list within Δt window.
2. Solve PFSS for each pair's CR.
3. Compute PFSS-distance and great-circle distance per pair.
4. Histogram sympathy fraction vs separation.

### Validation target

Reproduce the preferred-separation feature.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss for the PFSS step; flare list via SunPy/HEK.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-jiang-2024-nested-active-regions-hcs-reversal]] to test whether nested-AR phases enhance sympathy.
- Generative hypothesis: PFSS connectivity should be replaced by fluxon connectivity ([[paper-deforest-2024-flux-fluxon-coronal-modeling]]) to resolve the preferred-separation tail.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-jiang-2024-nested-active-regions-hcs-reversal]]

## Links

- arXiv: https://arxiv.org/abs/2412.10143
- arXiv HTML: https://arxiv.org/html/2412.10143
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- Δt window
- flare-pair definition
