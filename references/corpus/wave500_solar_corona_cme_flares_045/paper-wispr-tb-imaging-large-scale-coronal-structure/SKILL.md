# paper-wispr-tb-imaging-large-scale-coronal-structure

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when **PSP / WISPR** total-brightness imagery
must be used to identify large-scale coronal structures (streamers,
pseudo-streamers, CME flux ropes) from close to the Sun.

## Layer 1 — Scientific invariant

- **Paper identity:** WISPR Total Brightness Imaging of Large-Scale
  Coronal Structures (representative: Vourlidas+ 2016; Howard+ 2019;
  Hess+ 2020).
- **Year:** 2016–2020.
- **Venue:** ApJS — TODO verify.

### Claim (narrow form)

WISPR-I and WISPR-O total-brightness images, after F-corona
subtraction and J-map construction, reveal coronal streamers,
pseudo-streamers, and CME structures **closer than 0.5 au** with
spatial resolution unique among heliospheric imagers.

### Method assumptions

- Strong-baseline F-corona subtraction near PSP perihelion.
- PSP ephemeris and pointing precisely known.
- J-map (elongation-vs-time) construction along a chosen position
  angle.

### Failure modes (skill memory)

- **Stray-light from Venus / planets** must be masked.
- **F-corona model** dominates large-elongation residuals.
- **Geometric perspective** changes rapidly through perihelion.

### Claim boundary

**In scope.** Inner-heliosphere imaging from PSP between 0.05 and
0.5 au; large-scale, persistent structures.

**Out of scope.** Do NOT use as a calibrated brightness inversion
without F-corona subtraction validation.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_wispr_l3()`              | L3 frames                |
| `image.fcorona_subtract_baseline()`     | residual brightness      |
| `imagery.construct_jmap()`              | elongation-time map      |
| `morphology.identify_streamer()`        | structure ID             |

### Procedure

1. Fetch WISPR L3 over an encounter.
2. Subtract a baseline F-corona model.
3. Build J-maps along chosen position angles.
4. Identify and label structures.

### Validation target

TODO verify — recover known streamer / CME tracks from a published
encounter list.

## Layer 3 — Adapter / runtime notes (optional examples)

- NRL WISPR L3 archive; `sunpy` + `numpy`.

## Layer 4 — Research-generation affordances

- **Gap:** WISPR-derived structure tracks have not been combined
  rigorously with Metis pB structures during conjunctions — pair with
  `[[paper-metis-coronal-polarized-brightness-electron-density]]`.
- **Hypothesis:** WISPR J-map streamer kinematics map onto in-situ
  HCS crossings via
  `[[paper-source-surface-radius-optimization-eclipse-streamer]]`.

## Skill graph → depends_on

- `[[paper-vourlidas-2016-wispr-imaging-instrument-psp]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
