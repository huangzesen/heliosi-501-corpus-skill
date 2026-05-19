---
name: paper-titov-demoulin-2014-flux-rope-insertion-eruption
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-titov-demoulin-2014-flux-rope-insertion-eruption

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when constructing an **analytic flux-rope
initial condition** (Titov-Démoulin / TDm) inserted into a
photospheric magnetogram for an MHD eruption simulation.

## Layer 1 — Scientific invariant

- **Paper identity:** Titov-Démoulin Flux-Rope Insertion (Titov &
  Démoulin 1999; Titov+ 2014 modified TDm).
- **Year:** 2014.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

The TD (or TDm) flux rope provides a self-consistent equilibrium of a
twisted toroidal rope embedded above a polarity-inversion line, with
controllable major/minor radii, twist, and inserted poloidal flux.
The narrow claim is that this rope, inserted into a chosen
magnetogram and let go, reproduces standard eruption trajectories.

### Method assumptions

- Toroidal-rope ansatz; analytic external field.
- Pre-equilibrium relaxation under MHD.
- Boundary fixed at the photospheric magnetogram.

### Failure modes (skill memory)

- **Insertion mismatch.** Internal-vs-external field discontinuities
  produce numerical transients.
- **Trigger choice.** Eruption is triggered by perturbations whose
  amplitude affects the outcome.
- **Photospheric driving** is typically suppressed in TDm
  experiments.

### Claim boundary

**In scope.** Analytic flux-rope initial conditions for MHD
eruption studies.

**Out of scope.** Do NOT identify the TDm rope's interior with the
real observed flux-rope's interior field.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `extrapolation.tdm_rope()`              | analytic rope            |
| `magnetogram.match_pil()`               | photospheric anchor      |
| `mhd.relax_to_equilibrium()`            | pre-eruption relax       |
| `mhd.run_zero_beta()`                   | eruption integration     |

### Procedure

1. Choose target AR magnetogram and PIL.
2. Insert TDm rope; relax.
3. Trigger eruption.
4. Track flux-rope ascent.

### Validation target

TODO verify — flux-rope ascent profile matches paper benchmark.

## Layer 3 — Adapter / runtime notes (optional examples)

- The Aulanier-group OHM code, `Lare3d`, `MPI-AMRVAC` are reference
  adapters.

## Layer 4 — Research-generation affordances

- **Gap:** observation-constrained TDm parameters from NLFFF have
  not been used systematically — pair with
  `[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`.
- **Hypothesis:** TDm parameters tuned to NLFFF reproduce
  `[[paper-cme-kinematics-three-phase-acceleration-profile]]`'s
  a-peak distribution.

## Skill graph → depends_on

- `[[paper-aulanier-2012-standard-flare-model-3d-tether-cutting]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
