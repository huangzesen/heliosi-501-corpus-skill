---
name: wu-2026-nonspherical-coronal-magnetic-field-open-flux
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# wu-2026-nonspherical-coronal-magnetic-field-open-flux

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow is **addressing the open-flux
problem** — the long-standing factor-~2 discrepancy between PFSS-derived
open magnetic flux and in-situ-inferred open flux at 1 au — using a
non-spherical source surface (NSSS) PFSS extension.

Concrete symptoms:

- Baseline PFSS under-estimates open flux at the 1.5–2× level vs in-situ.
- A downstream source-mapping skill needs a coronal field that respects
  active-region-pressed-down loop heights without invoking MHD.
- The user explicitly references Wu et al. 2026 / NSPF / NSSS for a CR.

Do NOT use this skill when full NLFFF / MHD coronal currents are
required, or when a spherical PFSS suffices.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Addressing the Open Flux Problem with a Non-Spherical Solar
  Coronal Magnetic Field Model
- **First author:** Wu (TODO verify initials)
- **Other named authors per available context:** He, Hou (TODO verify
  full list)
- **arXiv:** 2604.01028
- **Year:** 2026
- **Venue:** TODO verify

### Claim (narrow form)

The paper replaces the conventional *spherical* PFSS source surface with
a *non-spherical source surface* (NSSS) extracted as the
`|B| = max|B|_SS` isosurface of a baseline PFSS solve, then re-solves
the potential field between the photosphere and NSSS. The narrow claim
is that this NSPF extension **raises the open-flux estimate** for the
case shown — specifically GONG CR 2282 at `R_init = 2.5 R_sun` — toward
in-situ values, without invoking non-potential physics.

### Method assumptions

- A baseline spherical PFSS is solvable on the same input `B_r`.
- The `|B|` field from the baseline solution is regular enough that an
  isosurface can be extracted by marching cubes on a regular grid.
- The deformed shell between photosphere and smoothed NSSS supports
  Laplace's equation with mixed BCs.
- Photospheric Br Neumann data and Dirichlet `Φ = 0` on NSSS are the
  boundary conditions.

### Data assumptions

- A synoptic Br product (GONG validated specifically) covering the
  target CR.
- Optional EUV imagery (AIA 193 Å) for open-field-map comparison.
- Optional coronagraph imagery (LASCO C2) for field-line overlay.
- Optional spacecraft ephemerides (e.g. PSP) for in-situ comparison.

### Failure modes (skill memory)

- **Mesh-coordinate sync.** A deformed mesh built in NumPy whose
  coordinates are never synced back to the mesh tool writes the
  un-deformed shell — open flux looks like baseline PFSS and the user
  wrongly concludes "NSPF does nothing."
- **P1 vs P2 elements.** Piecewise-constant gradient (P1) under-
  estimates open flux ~10%; P2 reaches < 1% on analytic tests.
- **Mesh resolution.** Coarse meshes can *over*-estimate open flux
  (148% reported at mesh size 0.25 in the reproduction context);
  finer mesh (~0.09) converges to ~99% of the paper. Always report
  mesh size + DOFs.
- **Magnetogram averaging.** Single-snapshot Br vs N-magnetogram CR
  average changes the open-flux number by ~1% in the reproduction.
- **NSSS smoothing parameters.** `L_max` and regularization `λ` affect
  the NSSS minimum radius and therefore open flux.
- **Missing PFCS layer.** Tracing field lines outside NSSS without a
  current-sheet layer between NSSS and an exit sphere truncates
  downstream geometry, even if open flux still matches at the surface
  integral.
- **Br Neumann sign convention.** Outward-normal sign on the inner
  boundary depends on derivation; a flipped sign returns a negative
  open flux.

### Figure / numerical targets

- **Open flux:** paper reports 9.19 G·R²_sun for GONG CR 2282 at
  `R_init = 2.5`; one independent reproduction reached 9.09 (1.1%
  error) at mesh size 0.09.
- **NSPF / PFSS ratio:** paper reports ~1.98; reproduction context
  reports ~1.82.
- **Reference figures (numbering TODO verify):** open-field map vs
  AIA 193 Å; field-line overlay on LASCO C2; PSP ballistic-back-mapping
  panel.

### Claim boundary

**In scope.** NSPF on GONG-class synoptic Br at the specific CR(s)
shown, with the paper's NSSS construction and FEM solve. Validated
specifically for GONG CR 2282, `R_init = 2.5`.

**Out of scope — do NOT generalize:**

- Do NOT claim NSPF closes the open-flux problem cycle-wide on one CR.
- Do NOT use as absolute calibration for in-situ open flux.
- Do NOT swap GONG for HMI or ADAPT without re-running; NSSS depends
  on the synoptic Br product.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `magnetogram.fetch_synoptic_br()`   | GONG (validated) or similar `B_r`      | per CR |
| `pfss.solve_baseline()`             | initial spherical PFSS                 | precondition |
| `geometry.extract_isosurface()`     | marching cubes on `\|B\|` at SS       | NSSS extraction |
| `geometry.smooth_spherical_harmonic()` | SH fit + regularization + clip      | NSSS smoothing |
| `mesh.build_deformed_shell()`       | 3-D mesh between `r=1` and NSSS        | mesh-tool-specific binding |
| `fem.solve_laplace()`               | Φ on shell with mixed BCs              | P2 elements preferred |
| `field.compute_b_from_phi()`        | `B = −∇Φ` via element interpolation    | local |
| `field.integrate_open_flux()`       | `∫|B_r| dA` over NSSS                  | local |
| `imagery.fetch_aia193()` (optional) | open-field-map comparison              | for diagnostics |
| `imagery.fetch_lasco_c2()` (optional)| field-line overlay                    | for diagnostics |
| `ephemeris.psp()` (optional)        | for in-situ ballistic-mapping panel    | local-or-remote |

### Procedure

1. **Solve baseline PFSS** with chosen `R_init` (2.5 R_sun default).
2. **Extract NSSS** by marching cubes on `|B|` at the source-surface
   height; keep the largest connected component.
3. **Smooth NSSS** by spherical-harmonic fit (`L_max ≈ 30`,
   regularization `λ ≈ 1e-4`); clip `r` to `[1.0, 2.5] R_sun`.
4. **Build deformed mesh** between `r = 1` and NSSS; ensure mesh-tool
   coordinates are synced before writing.
5. **FEM solve** `∇²Φ = 0` with Neumann `∂Φ/∂n = B_r` on photosphere,
   Dirichlet `Φ = 0` on NSSS (P2 elements recommended).
6. **Post-process** `B = −∇Φ` and integrate `|B_r|` on NSSS.
7. **Compare** open flux to the paper's value; compare open-field map
   to AIA 193 Å; overlay field lines on LASCO C2.

### Validation target

- **Metric:** open-flux integral, units G·R²_sun.
- **Tolerance:** ±5% as a healthy pass band on a fresh run (one
  reproduction hits 1.1% at mesh size 0.09).
- **Reference:** paper Table 1 (TODO verify identifier) for the
  GONG CR 2282, `R_init = 2.5` row.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Bindings used by *one* reproduction: `pfss.solve_baseline` →
  `sunkit-magex.pfss`; `mesh.build_deformed_shell` → Gmsh;
  `fem.solve_laplace` → FEniCSx 0.10.0 (P2). These are *examples*, not
  requirements. Any FEM stack with mixed BCs and P2 elements works.
- Equivalent bindings: deal.II + CGAL; PETSc + custom mesher; FEnics
  legacy; spherical-harmonic basis truncated at NSSS via reduced-basis
  methods.
- LingTai supplies a working binding in `.library/custom/nspf-fem/`,
  validated to 1.1% open-flux error vs paper for GONG CR 2282. That
  binding is *one* implementation; nothing in this SKILL.md requires
  the LingTai harness.

---

## Layer 4 — Research-generation affordances

- **Gap:** baseline PFSS systematically under-estimates open flux.
  NSPF closes a large fraction of this gap by deforming the outer
  boundary; the residual gap (~few percent in reproduction) suggests
  the *remaining* missing physics may live in a PFCS layer or in
  cycle-phase polar-field weakness.
- **Tension with `[[paper-multi-constraint-pfss-extrapolation-model]]`.**
  NSPF deforms the *outer* boundary; the multi-constraint paper
  augments the *interior* with NLFFF-style terms. Both have evidence
  for moving open flux. Composing them — multi-constraint solve
  *inside* an NSSS-bounded volume — is a new experiment.
- **New hypothesis:** if NSSS is constructed from a Carrington-averaged
  synoptic, then re-running NSPF with synchronic + AI-farside Br
  (`[[paper-ai-farside-synchronic-coronal-field-extrapolation]]`)
  should shift NSSS in ways that correlate with active-region rotation
  rather than long-term polar evolution.
- **Composable experiment:** run NSPF on every CR in the
  `[[paper-coronal-hole-loop-statistics-potential-field-modeling]]`
  sample and ask whether the two-population CH topology and NSPF
  open-flux enhancement are correlated.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  baseline PFSS solver inside NSPF must be verified.
- `[[paper-comparison-coronal-extrapolation-cycle-24-hmi]]` — sibling
  in the "open-flux family" of comparison studies.
- `[[paper-eclipse-white-light-benchmark-pfss-models]]` — observational
  acceptance test for the NSPF output morphology.

## Links

- arXiv: https://arxiv.org/abs/2604.01028
- arXiv (HTML mirror): https://arxiv.org/html/2604.01028
- DOI: TODO verify
- ADS: TODO verify
- Code: no canonical repo asserted in inventory; one reproduction
  exists at `.library/custom/nspf-fem/` (LingTai-internal example
  adapter; not a requirement)
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.5 and §2.8
