---
name: paper-magnetogram-noise-floor-quiet-sun-disambiguation
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-magnetogram-noise-floor-quiet-sun-disambiguation

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when noise-floor in quiet-Sun magnetograms must
be measured (and the floor used to threshold subsequent NLFFF /
flux-budget studies).

## Layer 1 — Scientific invariant

- **Paper identity:** Quiet-Sun Magnetogram Noise Floor (representative:
  Liu+ 2012; Bobra+ 2014; Hoeksema 2014).
- **Year:** 2012–2014.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

The 1-σ noise of HMI `B_LOS` per 720-s magnetogram is `~6–10 G`;
vector components are noisier `~80–120 G` in transverse field at
quiet-Sun. Time-averaging reduces noise as `~ N^(-1/2)`.

### Method assumptions

- Quiet-Sun masking via `|B|` threshold.
- Noise estimate via spatial variance in flat regions.

### Failure modes (skill memory)

- **Convective flows** can be mistaken for noise.
- **Limb pixels** have higher apparent noise.
- **Calibration drift** must be checked over the analysis interval.

### Claim boundary

**In scope.** HMI 720-s products; quiet-Sun disambiguation.

**Out of scope.** Do NOT apply to ground-based or vector pre-pipeline
products.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `magnetogram.fetch_los()`               | HMI LOS series           |
| `mask.quiet_sun()`                      | quiet patches            |
| `statistics.spatial_variance()`         | per-frame noise          |
| `statistics.time_average_n12()`         | √N reduction             |

### Procedure

1. Fetch HMI LOS series.
2. Mask quiet patches.
3. Estimate spatial variance → 1-σ noise.
4. Validate `N^(-1/2)` scaling.

### Validation target

TODO verify — recovered 1-σ `B_LOS ~ 6–10 G`.

## Layer 3 — Adapter / runtime notes (optional examples)

- Python `drms` + `numpy`.

## Layer 4 — Research-generation affordances

- **Gap:** noise budgets for SO/PHI HRT under different exposure
  modes are incomplete — pair with
  `[[paper-so-phi-hrt-vector-magnetogram-radial-distance]]`.

## Skill graph → depends_on

- `[[paper-hmi-vector-magnetogram-disambiguation-acute-angle]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
