---
name: mostl-2022-alfven-wave-solar-wind-ip-scintillation
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# mostl-2022-alfven-wave-solar-wind-ip-scintillation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when validating Alfvén-wave-driven solar-wind models against IPS-derived vsw maps, using PFSS to constrain source-region magnetic geometry.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Testing the Alfvén-Wave Model of the Solar Wind with Interplanetary Scintillation
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2022
- **arXiv:** 2202.10768 (posted 2022-02-22)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Alfvén-wave-driven wind models reproduce IPS-derived global vsw maps within tolerance when PFSS provides realistic expansion-factor inputs; residuals are dominated by polar / high-latitude regions.

### Method assumptions

- IPS inversion gives reliable vsw on a global grid.
- Alfvén-wave model is consistent with expansion-factor inputs.

### Data assumptions

- IPS vsw maps for the studied interval.
- Synoptic Br for PFSS.

### Failure modes (skill memory)

- IPS inversion is grid-resolution-dependent.
- Polar coverage is sparse in IPS.

### Figure / numerical targets

- Model-vs-IPS vsw map.
- Residuals vs heliographic latitude.

### Claim boundary

**In scope.** The IPS coverage + paper's Alfvén-wave model.

**Out of scope — do NOT generalize:**

- Do NOT cite the model agreement for polar latitudes outside IPS coverage.
- Do NOT extend to non-IPS-validated intervals.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `ips.fetch_vsw_map()` | IPS-derived vsw |  |
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `expansion_factor.compute()` | f at SS |  |
| `alfven_wave.model_speed()` | AW-model vsw |  |

### Procedure

1. Fetch IPS vsw maps.
2. Solve PFSS; compute f at SS.
3. Run AW model; predict vsw on the global grid.
4. Compare to IPS; quantify residuals by latitude.

### Validation target

Recover the global agreement and polar residuals.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; AW model is paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-mostl-2022-alfven-wave-solar-wind-ip-scintillation]] + [[paper-reville-2025-solo-psp-open-closed-magnetic-outflows]] for IPS↔in-situ joint validation.
- Generative hypothesis: IPS residuals at high latitudes correlate with polar-completeness ensembles ([[paper-sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field]]).

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2202.10768
- arXiv HTML: https://arxiv.org/html/2202.10768
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- IPS dataset
- AW model identity
