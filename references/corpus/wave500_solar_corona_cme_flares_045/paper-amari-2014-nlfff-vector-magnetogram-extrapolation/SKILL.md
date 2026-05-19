---
name: paper-amari-2014-nlfff-vector-magnetogram-extrapolation
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-amari-2014-nlfff-vector-magnetogram-extrapolation

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when computing **non-linear force-free field
(NLFFF)** extrapolations from vector magnetograms (typically SHARP),
to recover 3-D AR field for topology / decay-index analysis.

## Layer 1 — Scientific invariant

- **Paper identity:** Optimization / Grad-Rubin NLFFF Extrapolation
  Family (representative: Amari+ 2014; Wiegelmann 2004; Inoue+
  2014).
- **Year:** 2014.
- **Venue:** Nature / ApJ — TODO verify.

### Claim (narrow form)

A SHARP vector magnetogram, after force-free pre-processing, admits
an NLFFF extrapolation via optimization or Grad-Rubin methods that
matches the observed loop morphology and stores **>10× the
potential-field free energy** on the strongly twisted ARs studied.

### Method assumptions

- Force-freeness pre-processing reduces Lorentz residuals.
- Iterative method (optimization, MHD-relaxation, Grad-Rubin).
- Box-domain assumption with bottom boundary the magnetogram.

### Failure modes (skill memory)

- **Non-force-free photosphere** biases all NLFFF schemes.
- **Boundary-domain mismatch** when ARs are larger than the
  cutout.
- **Helicity sign** can flip depending on disambiguation.

### Claim boundary

**In scope.** Strongly twisted ARs in SHARP CEA cutouts.

**Out of scope.** Do NOT trust NLFFF in quiet-Sun extrapolations.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `vector_mag.fetch_sharp()`              | SHARP cutout             |
| `vector_mag.preprocess_ff()`            | force-free prep          |
| `extrapolation.solve_nlfff()`           | optimization / GR        |
| `metrics.lorentz_residual()`            | force-freeness QC        |
| `morphology.compare_loops()`            | EUV-loop overlap         |

### Procedure

1. Fetch SHARP CEA vector magnetogram.
2. Preprocess for force-freeness.
3. Solve NLFFF (optimization or Grad-Rubin).
4. Validate via residual + loop overlay.

### Validation target

TODO verify — Lorentz residual `< 10%` and loop overlay match.

## Layer 3 — Adapter / runtime notes (optional examples)

- Reference adapters: Wiegelmann optimization (C/Fortran); Inoue
  MHD-relaxation; FastQSL.

## Layer 4 — Research-generation affordances

- **Gap:** NLFFF ensembles using different solvers on the same
  SHARP have not been catalogued — would bound the systematic.
- **Hypothesis:** NLFFF twist correlates with the
  `[[paper-rhessi-hxr-footpoint-asymmetry-flare]]` brightness ratio.

## Skill graph → depends_on

- `[[paper-hmi-vector-magnetogram-disambiguation-acute-angle]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
