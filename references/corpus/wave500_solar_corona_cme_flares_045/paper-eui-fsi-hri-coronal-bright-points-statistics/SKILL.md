# paper-eui-fsi-hri-coronal-bright-points-statistics

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when characterizing the **coronal-bright-point**
population (the so-called "campfires") in EUI/HRI 174 Å at high
cadence.

## Layer 1 — Scientific invariant

- **Paper identity:** EUI HRI Coronal Bright Points / Campfires
  (representative: Berghmans+ 2021; Chitta+ 2022).
- **Year:** 2021.
- **Venue:** A&A — TODO verify.

### Claim (narrow form)

EUI HRI resolves transient `~1–4 Mm`, `~10–200 s` brightenings —
"campfires" — at a density of `~1 event Mm^-2 hr^-1` in quiet-Sun
regions. The narrow claim is that campfires share statistical
properties with chromospheric jets but at coronal temperatures.

### Method assumptions

- HRI 174 Å L2 imagery.
- Threshold + persistence-based event detection.
- Photospheric magnetogram cross-reference.

### Failure modes (skill memory)

- **Cosmic-ray hits** can mimic short-duration events; mask.
- **Pointing jitter** causes false elongated tracks.
- **Detection threshold** sets the small-end limit.

### Claim boundary

**In scope.** EUI HRI 174 Å bright points in quiet Sun.

**Out of scope.** Do NOT generalize to AIA / SUVI at lower
resolution without re-calibrating thresholds.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_eui_hri()`               | HRI 174 Å series         |
| `event.detect_persistent_brightening()` | bright-point pipeline    |
| `morphology.size_lifetime()`            | event geometry           |
| `magnetogram.cospatial_polarity()`      | photospheric polarity    |

### Procedure

1. Fetch HRI 174 Å.
2. Detect bright points with threshold + persistence.
3. Tabulate size/lifetime; fit distributions.
4. Cross-reference photospheric polarity.

### Validation target

TODO verify — recover `~1 event Mm^-2 hr^-1` and published size /
lifetime histograms.

## Layer 3 — Adapter / runtime notes (optional examples)

- Python `sunpy` + `scikit-image`.

## Layer 4 — Research-generation affordances

- **Gap:** the campfire population's contribution to coronal
  heating is contested — pair with
  `[[paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure]]`
  to set the energy budget.
- **Hypothesis:** campfire occurrence correlates with mixed-polarity
  emergence detected in HMI noise floor
  (`[[paper-magnetogram-noise-floor-quiet-sun-disambiguation]]`).

## Skill graph → depends_on

- `[[paper-coronal-plume-substructure-eui-high-cadence]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
