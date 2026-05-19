---
name: tenerani-2026-spherically-polarized-magnetic-fields
description: Per-entry paper-skill in pilot_2026_and_runtime (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# tenerani-2026-spherically-polarized-magnetic-fields

## When to use this paper-skill

Invoke when a HelioSI workflow needs to *construct*, *test*, or *interpret*
three-dimensional, exactly spherically polarized (constant-|B|) magnetic
fields — the canonical "spherical-polarization" ansatz that underlies the
modern theory of Alfvénic solar-wind turbulence and switchback geometry.
Typical triggers:

- The user asks "is this PSP interval consistent with constant |B|?" and
  wants a theoretically grounded reference field to compare against.
- A reasoning agent needs to model a switchback as a smooth 3D rotation in
  a spherically polarized background and is choosing between a smooth
  global field vs. patched discontinuous fields.
- Building or stress-testing a `synthetic-switchback-generator` skill that
  must obey `|B| = const`.

Do not invoke as a *generation* mechanism for switchbacks — the paper is a
geometric/constructive existence result, not a coronal-physics generation
claim.

## Paper identity and claim boundary

- **Title:** Three dimensional, spherically polarized magnetic fields
- **Authors:** Anna Tenerani, Marco Velli
- **arXiv:** 2605.04285 (2026)
- **Claim boundary:**
  1. *Constructive:* a numerical scheme that produces exactly spherically
     polarized (constant-`|B|`) 3D magnetic fields.
  2. *Analytic:* an argument that such fields cannot smoothly fill arbitrary
     volumes — discontinuities (rotational discontinuities, RDs) between
     polarized patches are *unavoidable*.
  3. *Implication:* switchback geometry observed by PSP is naturally
     interpreted as patched spherically polarized regions separated by RDs.
  The paper does NOT claim a generation mechanism for switchbacks, nor a
  full MHD-turbulence cascade.

## Scientific or methodological claim to operationalize

> Exactly spherically polarized 3D `B`-fields exist and can be constructed
> numerically, but they cannot smoothly tile arbitrary volumes: any
> volume-filling spherically polarized field must contain rotational
> discontinuities between patches.

A HelioSI skill operationalizes this by exposing two callable functions:

- `construct_spherically_polarized_field(geometry, params) -> B(x,y,z)`
  with `|B| = const`.
- `find_rotational_discontinuities(B(x,y,z)) -> mask, locations`.

These let downstream skills (synthetic switchback generators, geometric
PSP-trace simulators) start from a theoretically clean baseline.

## Required data / instruments / code / archives

- This is a *theoretical/constructive* skill — primary deliverable is
  code, not data. Optional PSP/FIELDS data for validation.
- **Code dependencies:** `numpy`, `scipy`; an ODE/PDE integrator for the
  constructive scheme; visualization with `matplotlib` or `pyvista`.

## Algorithm / workflow steps

1. **Choose a domain and boundary condition.** A simple choice: a periodic
   3D box with a background `B_0` direction, parameterized by an amplitude
   `|B|` and a rotation profile.
2. **Implement the constructive numerical scheme** described in the paper.
   TODO verify exact scheme: the abstract names it as constructive but the
   inventory does not capture the equations.
3. **Verify `|B| = const`** numerically to machine precision across the
   domain.
4. **Identify rotational discontinuities** where smooth continuation
   fails: jumps in `B̂` across surfaces.
5. **Compute geometric diagnostics:** rotation angle distribution along
   1D traverses, curvature, helicity density.
6. **Project onto a 1D path** simulating a spacecraft traversal; output
   the would-be PSP time series of `B_R`, `B_T`, `B_N`, `|B|`.

## Minimal executable benchmark or validation target

A HelioSI benchmark version of this skill should:

- Construct a 3D field with `std(|B|)/mean(|B|) < 1e-10` over the bulk.
- Demonstrate the impossibility-of-smooth-tiling claim by attempting to
  glue two patches and showing that the boundary requires a rotational
  discontinuity (non-zero jump in `B̂`).
- Reproduce qualitatively the published figure (TODO verify exact figure
  identifier from full text) showing a 3D constant-|B| field with embedded
  RDs.

## Known pitfalls / failure modes

- **Numerical leakage from `|B|=const`.** Generic ODE/PDE schemes drift
  off the constant-|B| manifold; the constructive scheme must be
  projection-preserving.
- **Confusing this with switchback *origin*.** This is a *kinematic*
  existence result; it does not address coronal generation.
- **Boundary conditions matter.** Spherical polarization globally needs
  RDs; choosing periodic or open boundaries changes where RDs appear.
- **Mistaking RDs for tangential discontinuities (TDs)** in PSP data —
  the paper's interpretation specifically calls for RDs (Walén-test
  positive); validation should enforce that.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2605.04285 as an Anthropic-
style Skill loadable by the HelioSI runtime:

| Paper element | Agent-native form |
|---|---|
| Claim — "exactly spherically polarized 3D `B`-fields are constructible but require RDs to tile a volume" | **Verifiable task:** `construct_spherically_polarized_field(geometry, params) -> B(x,y,z)` with `std(|B|)/mean(|B|) < 1e-10`; `find_rotational_discontinuities(B) -> mask` |
| Methods / equations — constructive numerical scheme (TODO verify equations from full text) | **Executable workflow:** §"Algorithm / workflow steps" 1–6 with domain, boundary conditions, and projection-preserving integrator as explicit parameters |
| Data / instruments / code — theoretical only; `numpy`/`scipy`/PDE integrator; optional PSP FIELDS for downstream validation | **MCP / tool contracts:** none required for construction; optional `cdaweb-mcp.get_psp_fields_mag(...)` for projection-to-spacecraft validation; visualization via `matplotlib`/`pyvista` |
| Caveats / failure modes — drift off the `|B|=const` manifold; BC dependence; RD vs TD confusion | **Skill memory:** §"Known pitfalls / failure modes" — runtime monitors `|B|` drift each integration step and re-projects if needed |
| Figures / results — 3D constant-|B| field with embedded RDs (TODO verify figure ID) | **Benchmark artifacts:** 3D rendering, `metrics.json` (`std|B|/mean|B|, RD count`), 1D-traversal `B_RTN` time series |

The Skill compiles a *theoretical existence + impossibility* result into a
HelioSI-callable field generator that other skills (synthetic switchback,
Walén-test validator) can build on.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** theoretical-construction sub-graph; baseline field
  generator for synthetic data pipelines.
- **Skills it composes with:**
  - [[synthetic-switchback-generator]] — TODO create
  - [[psp-walen-test-classifier]] — TODO create
  - [[rotational-discontinuity-finder-mhd]] — TODO create
- **MCPs it would use:** none required for construction; optional
  `cdaweb-mcp` for downstream validation against PSP intervals.
- **HelioSI manuscript role:** provides the theoretical anchor for a
  unified "switchbacks = traversals of spherically polarized 3D fields"
  framing in HelioSI's switchback case studies. Pairs cleanly with the
  Huang–Velli–Ding 2025 "What are Switchbacks?" preprint (arXiv
  2512.12585), which models switchbacks as solitary Alfvén waves
  preserving constant `|B|`.

## References

- Tenerani, A., Velli, M. (2026). Three dimensional, spherically polarized
  magnetic fields. arXiv:2605.04285.
- Huang, Z., Velli, M., Ding, Y. (2025). What are Switchbacks?
  arXiv:2512.12585. (companion / related)
- Inventory: `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md`
  entry #16.
