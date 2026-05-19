# dingding-2025-pfss-source-surface-height-optimization

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when you need to choose R_ss adaptively rather than at the canonical 2.5 R_sun, by minimizing an empirical observation-vs-PFSS mismatch metric.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Empirical Optimization of the Source-Surface Height in the PFSS Extrapolation
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2510.05513 (posted 2025-10-07)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

R_ss is not universal — an optimal R_ss minimizing an empirical mismatch metric varies systematically with solar-cycle phase and the chosen synoptic magnetogram, with material effects on open-flux estimates and back-mapped footpoints.

### Method assumptions

- Mismatch metric is well-defined (e.g., open-field-map vs EUV CH; in-situ polarity agreement).
- PFSS is sufficiently fast to scan R_ss on a grid.
- Optimal R_ss is unique to within tolerance for a given CR.

### Data assumptions

- Synoptic Br across a chosen interval (HMI/GONG/ADAPT).
- EUV-based CH map or in-situ polarity catalog as ground truth.

### Failure modes (skill memory)

- Mismatch metric is multimodal in R_ss for complex CRs.
- EUV-CH segmentation choices propagate to R_ss optima.
- ADAPT vs GONG vs HMI give different R_ss optima — pin product.

### Figure / numerical targets

- Optimal R_ss vs CR / cycle phase.
- Mismatch metric vs R_ss curve at representative CRs.
- OSF vs R_ss curve under each magnetogram product.

### Claim boundary

**In scope.** Paper's CR window + the empirical mismatch metric used.

**Out of scope — do NOT generalize:**

- Do NOT recommend a single optimal R_ss for all studies — it's metric-dependent.
- Do NOT mix magnetogram products mid-scan.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `pfss.solve()` | PFSS on a R_ss grid | scan |
| `ch.detect_from_euv()` | ground-truth CH mask | AIA/EUVI |
| `metric.openfield_vs_ch()` | PFSS-vs-EUV CH agreement | f1 or IoU |
| `metric.polarity_agreement()` | in-situ polarity vs PFSS footpoint | L1/PSP |
| `optim.scalar()` | 1-D minimization | golden section |

### Procedure

1. Define mismatch metric.
2. For each target CR, scan R_ss ∈ [1.5, 3.5] R_sun.
3. Locate optimum; record metric curve.
4. Cross-product against magnetogram products and metrics.
5. Aggregate optimal-R_ss vs cycle phase.

### Validation target

Reproduce systematic cycle-phase variation of optimal R_ss reported by the paper.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss for the scan; SunPy/aiapy for EUV-CH masks.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-rice-2026-outflowpy-outflow-fields-pfss-alternative]] — outflowpy eliminates R_ss; the residual mismatch between optimal-R_ss PFSS and outflowpy should isolate the outflow physics contribution.
- Generative hypothesis: optimal R_ss correlates with the effective harmonic degree of the global field ([[paper-hore-2026-dominant-spatial-scales-coronal-field]]).

---

## Skill graph → depends_on

- [[paper-eclipse-white-light-benchmark-pfss-models]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2510.05513
- arXiv HTML: https://arxiv.org/html/2510.05513
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- full author list
- venue/DOI
- exact mismatch metric formula
- EUV-CH segmentation algorithm
