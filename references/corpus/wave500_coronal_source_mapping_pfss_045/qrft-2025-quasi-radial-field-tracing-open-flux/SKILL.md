---
name: qrft-2025-quasi-radial-field-tracing-open-flux
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# qrft-2025-quasi-radial-field-tracing-open-flux

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when adaptively segmenting the open-flux corona by quasi-radial field-line tracing, producing a sharper open–closed boundary than PFSS gridded tracers.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** The Quasi-Radial Field-Line Tracing (QRaFT): An Adaptive Segmentation of the Open-Flux Solar Corona
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2506.14894 (posted 2025-06-17)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

QRaFT adaptive segmentation produces an open-flux mask whose boundary is more consistent with EUV-CH boundaries than the PFSS gridded tracer at matched cost.

### Method assumptions

- Quasi-radial seeding is robust to small Br perturbations.
- Adaptive refinement converges to the open-closed boundary.

### Data assumptions

- Synoptic Br for the relevant CR.
- EUV-CH ground truth.

### Failure modes (skill memory)

- Seeding density sets the boundary sharpness.
- Quasi-radial assumption breaks near current sheets.

### Figure / numerical targets

- QRaFT mask vs PFSS-gridded open-field map.
- Boundary-IoU vs EUV-CH.

### Claim boundary

**In scope.** The studied CRs.

**Out of scope — do NOT generalize:**

- Do NOT use QRaFT in current-sheet-dominated regions without augmenting.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `qraft.adaptive_segment()` | QRaFT | seeding density knob |
| `ch.detect_from_euv()` | EUV CH |  |
| `metric.boundary_iou()` | IoU |  |

### Procedure

1. Solve PFSS.
2. Run QRaFT adaptive segmentation.
3. Compare boundary to EUV CH.

### Validation target

Boundary IoU improvement at matched cost.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; QRaFT is paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-brightness-magnetically-open-corona-2025]] for brightness-classified open-flux atlas.
- Generative hypothesis: QRaFT-OCB sharpness predicts in-situ slow-wind/OCB association sharpness ([[paper-stansby-2025-open-closed-flux-boundary-slow-wind]]).

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-brightness-magnetically-open-corona-2025]]

## Links

- arXiv: https://arxiv.org/abs/2506.14894
- arXiv HTML: https://arxiv.org/html/2506.14894
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- seeding-density convention
- comparison-cost matching
