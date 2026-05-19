---
name: multi-constraint-pfss-extrapolation-model
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# multi-constraint-pfss-extrapolation-model

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow needs a **coronal magnetic field
extrapolation that goes beyond plain PFSS but stops short of full
NLFFF / MHD** — i.e. when the user wants to inject *physical or
observational priors* (loop geometry, divergence, force-free residual)
into a PFSS-style solve.

Concrete symptoms:

- Traced coronal loops from EUV / X-ray imagery are available and the
  user asks whether a PFSS-like field can respect them.
- A downstream skill (open-flux, source-mapping) is sensitive to
  photospheric-Br residual and the user wants to reduce it without
  invoking NLFFF cost / non-uniqueness.
- Building a head-to-head with baseline PFSS on a shared magnetogram set.

Do NOT use this skill when fully non-potential coronal currents are
required (use NLFFF) or for pure analytic solver verification (use the
PFSS test-problem skill).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** A New Multi-Constraint Potential Field Source Surface
  (PFSS) Extrapolation Model
- **First author:** TODO verify
- **arXiv:** 2603.20142
- **Year:** 2026
- **Venue:** TODO verify

### Claim (narrow form)

The paper proposes a PFSS-framework extrapolation in which the baseline
Laplace BVP is augmented by optimization-style penalty terms borrowed
from NLFFF (divergence-free, loop-geometry conformity, force-free
residual). The narrow claim is that this multi-constraint formulation
is *feasible inside the PFSS framework* and improves agreement with
the chosen constraints relative to baseline PFSS on the cases shown.

### Method assumptions

- A PFSS-style outer boundary (source surface) is retained.
- The constraint set is finite and explicit (`div`, loop conformity,
  force-free residual; possibly more).
- A weighted multi-term objective is minimized over a field
  representation (basis or grid; TODO verify which).
- Photospheric `B_r` boundary residual is one of the terms.

### Data assumptions

- Synoptic `B_r` (GONG / HMI / ADAPT) is the mandatory boundary input.
- Loop tracings (from EUV imagery) are optional and enable the loop-
  conformity term.
- Vector magnetograms are optional and enable the force-free residual
  term.

### Failure modes (skill memory)

- **Weight tuning sensitivity.** Multi-objective formulations are
  notoriously sensitive to `(w_div, w_loop, w_ff, w_data)`; reporting
  results without the weight vector is meaningless.
- **Loop-tracing bias.** Loop tracings are subjective and observatory-
  dependent (171 Å vs 193 Å vs X-ray). "Improvement" can vanish under
  re-tracing.
- **Non-uniqueness.** Multi-constraint optimization admits multiple
  local minima; report initial guess and optimizer settings.
- **Footpoint drift.** A constrained field can move open-field
  footpoints by 10s of degrees vs baseline PFSS; downstream source-
  mapping skills must be re-validated.
- **Source-surface region weighting.** Whether the loop-conformity term
  acts in the layer adjacent to `R_ss` is a methodological choice that
  biases the result.

### Figure / numerical targets

- TODO verify residual metric (likely median angular misfit between
  modelled and traced loops, in degrees) and the paper's reference
  figure.

### Claim boundary

**In scope.** Constrained PFSS-framework extrapolation as defined by
the paper's objective, on the paper's magnetogram set, with the
paper's reported weight choices.

**Out of scope — do NOT generalize:**

- Do NOT report "constrained PFSS outperforms NLFFF"; the paper does
  not make that claim per inventory.
- Do NOT claim the method works for active-region zoom-ins at HMI
  resolution without testing — the paper's context is synoptic.
- Do NOT reuse the paper's weights on a new dataset; weights are not
  portable.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `magnetogram.fetch_synoptic_br()`   | photospheric `B_r` for solve           | one of GONG / HMI / ADAPT |
| `imagery.fetch_euv()`               | loop-tracing source (optional)         | only if loop term enabled |
| `imagery.trace_loops()`             | extract coronal-loop geometry          | optional |
| `vector_mag.fetch()`                | vector magnetogram (optional)          | only if force-free term enabled |
| `pfss.solve_baseline()`             | initial guess via standard PFSS        | precondition |
| `optimization.minimize_objective()` | multi-term objective solver            | gradient-based or basis-fitting |
| `field.diagnostics()`               | per-term residuals on output field     | local computation |

### Procedure

1. **Load** synoptic `B_r`; optionally loop tracings and vector
   magnetograms.
2. **Compute baseline PFSS** as initial guess.
3. **Define objective:**
   `J = w_div ||∇·B||² + w_loop D_loop(B) + w_ff ||(J×B)/|B|²||² +
   w_data ||B_r(R_sun) − B_r_obs||²` (functional form TODO verify).
4. **Minimize** with respect to the field representation.
5. **Diagnose per-term residuals** at convergence; flag runs where any
   term explodes vs baseline.
6. **Emit** 3-D field + per-term residual JSON + optimization log.

### Validation target

- **Metric:** TODO verify (placeholder: median angular misfit between
  modelled and traced loops, in degrees).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `pfss.solve_baseline` to `sunkit-magex.pfss`,
  `optimization.minimize_objective` to SciPy / JAX, and loop tracing to
  any of several community pipelines.
- The skill is agnostic about field representation; basis-coefficient,
  finite-difference, or finite-element variants are all admissible.
- Loop-tracing pipelines (manual, semi-automated, ML) are pluggable
  behind `imagery.trace_loops`.

LingTai's `[[pfss-tracing]]` custom skill provides one binding of
`pfss.solve_baseline` but is not required.

---

## Layer 4 — Research-generation affordances

- **Gap:** baseline PFSS minimizes only `w_data` (boundary residual);
  this paper opens the question of which constraint *set* best
  explains observed corona without leaving the potential-like regime.
- **Tension:** constrained PFSS and `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`
  attack the "PFSS is too smooth" critique with different surgical
  moves — constraints in the volume vs deformation of the outer
  boundary. Composing both on the same Carrington rotation should
  reveal whether the open-flux gap is closed by volumetric currents
  (constraints) or by source-surface shape (NSSS).
- **New hypothesis to test:** weight-vector portability — if a paper
  publishes `(w_*)` chosen for one CR, do those weights generalize
  across cycle phase, or do they covary with polar-field strength?
- **Composable experiment:** apply this method to the eclipse benchmark
  set (`[[paper-eclipse-white-light-benchmark-pfss-models]]`) and check
  whether visual streamer agreement improves where loop tracings exist.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  solver must reduce to a verified PFSS in the limit
  `(w_loop, w_ff) → 0`.
- `[[paper-flare-precursor-fine-scale-topology-extrapolation]]` —
  loop-aware extrapolation paper that may share methodological
  ingredients.
- `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]` —
  alternative approach to enhance PFSS realism.

## Links

- arXiv: https://arxiv.org/abs/2603.20142
- arXiv (HTML mirror): https://arxiv.org/html/2603.20142
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.2 and §2.10
