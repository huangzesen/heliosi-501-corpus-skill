---
name: koukras-2022-backmapping-uncertainty-fast-wind
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# koukras-2022-backmapping-uncertainty-fast-wind

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when propagating uncertainty in PFSS + ballistic back-mapping into fast-wind source-region attribution.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Estimating Uncertainties in the Back-Mapping of the Fast Solar Wind
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2022
- **arXiv:** 2212.11553 (posted 2022-12-22)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Fast-wind backmapping uncertainty is dominated by vsw variability and R_ss choice, not by magnetogram product, and is quantifiable as an ellipse on the source surface.

### Method assumptions

- Ballistic back-mapping is valid up to the source surface.
- Uncertainty propagates linearly for small perturbations.

### Data assumptions

- Fast-wind in-situ catalog with vsw uncertainty.
- Synoptic Br per CR.

### Failure modes (skill memory)

- Slow streams violate linear-uncertainty assumption.
- R_ss sensitivity dominates near CH boundaries.

### Figure / numerical targets

- Uncertainty ellipse on the source surface.
- Decomposition: vsw vs R_ss vs product.

### Claim boundary

**In scope.** Fast-wind streams (vsw>~500 km/s) per paper.

**Out of scope — do NOT generalize:**

- Do NOT extend the linear approximation to slow wind.
- Do NOT collapse uncertainty into a single scalar without the ellipse shape.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `backmap.ballistic()` | backmap |  |
| `uncertainty.ellipse_on_surface()` | uncertainty ellipse | linearized |

### Procedure

1. Fetch fast-wind stream list.
2. Solve PFSS; back-map each stream.
3. Propagate vsw + R_ss + product uncertainty to ellipse.
4. Tabulate per-stream ellipse axes.

### Validation target

Reproduce the ellipse-axis decomposition.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; pyspedas for in-situ.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field]] for a unified uncertainty framework.
- Generative hypothesis: outflowpy ellipses should be systematically smaller for fast streams from CH cores.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field]]

## Links

- arXiv: https://arxiv.org/abs/2212.11553
- arXiv HTML: https://arxiv.org/html/2212.11553
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- fast-wind definition
- linearization assumption
