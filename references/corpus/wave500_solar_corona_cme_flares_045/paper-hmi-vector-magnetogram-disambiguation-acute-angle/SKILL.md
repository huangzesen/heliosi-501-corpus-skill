---
name: paper-hmi-vector-magnetogram-disambiguation-acute-angle
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-hmi-vector-magnetogram-disambiguation-acute-angle

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when working with **HMI vector magnetograms**
where the 180° azimuthal ambiguity must be resolved before any
NLFFF / SHARP-derived analysis.

## Layer 1 — Scientific invariant

- **Paper identity:** HMI Vector Magnetogram 180° Disambiguation
  (representative: Hoeksema+ 2014; Bobra+ 2014; Leka & Barnes ME0
  method).
- **Year:** 2014.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

The HMI vector pipeline solves the 180° azimuthal ambiguity using a
minimum-energy (ME0) annealing approach, achieving a per-pixel
disambiguation accuracy `> 95%` in strong-field regions (`|B| >
~200 G`) but degrading in weak-field areas.

### Method assumptions

- Inversion of Stokes profiles by VFISV (or equivalent).
- ME0 / acute-angle disambiguation per pixel.
- Reference is taken at strong-field cores.

### Failure modes (skill memory)

- **Weak-field noise** makes disambiguation unreliable below
  ~100 G.
- **Penumbral regions** show systematic flips that propagate into
  current helicity.
- **Borders** between strong-field patches can show seam artifacts.

### Claim boundary

**In scope.** HMI vector magnetograms during the SDO era,
strong-field regions.

**Out of scope.** Do NOT trust per-pixel disambiguation in
quiet-Sun areas without independent verification.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `vector_mag.fetch_hmi_stokes()`         | Stokes I/Q/U/V           |
| `vector_mag.invert_vfisv()`             | inversion to B vec       |
| `vector_mag.disambiguate_me0()`         | 180° resolution          |
| `vector_mag.qa_strength_threshold()`    | reliability mask         |

### Procedure

1. Fetch Stokes profiles.
2. Invert via VFISV.
3. Apply ME0 disambiguation.
4. Mask weak-field pixels for downstream NLFFF.

### Validation target

TODO verify — per-pixel accuracy `> 95%` in `|B| > 200 G`.

## Layer 3 — Adapter / runtime notes (optional examples)

- The official `hmi.B_720s` data series is the standard adapter.
- IDL `vfisv` and Fortran `ME0` are reference implementations.

## Layer 4 — Research-generation affordances

- **Gap:** ML-based disambiguation alternatives have only recently
  appeared — pair with
  `[[paper-flare-forecasting-sharp-features-deep-learning]]`.
- **Hypothesis:** disambiguation noise in penumbrae biases
  NLFFF-derived QSL maps near sunspots
  (`[[paper-flare-qsl-pre-eruption-topology-decay-index]]`).

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
