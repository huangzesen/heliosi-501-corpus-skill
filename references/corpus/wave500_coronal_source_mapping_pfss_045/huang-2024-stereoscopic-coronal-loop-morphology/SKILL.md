---
name: huang-2024-stereoscopic-coronal-loop-morphology
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# huang-2024-stereoscopic-coronal-loop-morphology

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when reconstructing coronal-loop 3-D morphology from stereoscopic EUV imagery and comparing to PFSS / NLFFF extrapolations.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Stereoscopic Observations Reveal Coherent Morphology and Evolution of Solar Coronal Loops
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2411.16943 (posted 2024-11-25)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Stereoscopic-EUV-reconstructed loop geometries match PFSS+NLFFF extrapolations to within a paper-stated angular-deviation metric on a non-trivial fraction of cases, with the residual fraction localizing model defects.

### Method assumptions

- Stereoscopic reconstruction is geometrically valid.
- Loop identification across viewpoints is consistent.

### Data assumptions

- STEREO-A/B + SDO/AIA paired EUV imagery.
- HMI vector Br for NLFFF.
- Synoptic Br for PFSS background.

### Failure modes (skill memory)

- Loop-pair identification is the dominant error source.
- NLFFF boundary preparation biases the comparison.

### Figure / numerical targets

- Reconstructed loop overlaid on PFSS+NLFFF traces.
- Angular-deviation histogram.

### Claim boundary

**In scope.** The studied loop sample.

**Out of scope — do NOT generalize:**

- Do NOT generalize the deviation statistic to AR cores where loop coverage is sparse.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `imagery.fetch_aia()` | AIA EUV |  |
| `imagery.fetch_stereo()` | STEREO EUV |  |
| `loop.stereoscopic_reconstruct()` | 3-D loop |  |
| `magnetogram.fetch_hmi_vector()` | HMI vector |  |
| `nlfff.solve()` | AR NLFFF |  |
| `pfss.solve()` | background |  |
| `metric.angular_deviation()` | loop-vs-trace metric |  |

### Procedure

1. Pair stereoscopic loop tracings.
2. Reconstruct 3-D loop morphology.
3. Solve PFSS+NLFFF.
4. Compare loop to extrapolation traces.

### Validation target

Reproduce angular-deviation distribution.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- SunPy/aiapy + STEREO pipelines; sunkit-magex.pfss; NLFFF paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[multi-constraint-pfss-extrapolation-model]] — this loop sample is exactly the kind of input that paper consumes.
- Generative hypothesis: residual deviations should localize in AR cores where [[vanderlinden-2024-flux-rope-magneto-friction-electric-field]] predicts non-potential currents.

---

## Skill graph → depends_on

- [[multi-constraint-pfss-extrapolation-model]]
- [[flare-precursor-fine-scale-topology-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2411.16943
- arXiv HTML: https://arxiv.org/html/2411.16943
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- loop-sample identity
- angular-deviation tolerance
