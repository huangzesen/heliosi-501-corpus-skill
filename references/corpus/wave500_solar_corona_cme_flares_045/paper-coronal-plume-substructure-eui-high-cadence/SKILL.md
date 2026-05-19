# paper-coronal-plume-substructure-eui-high-cadence

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when characterizing **coronal-plume fine
substructure** (plumelets) in high-cadence EUI/HRI imagery as the
suspected source of solar-wind microstructures (e.g. switchbacks
or "Alfvenic spikes").

## Layer 1 — Scientific invariant

- **Paper identity:** Coronal Plume Substructure / Plumelets at EUI
  High Cadence (representative: Uritsky+ 2021; Berghmans+ 2021;
  Kumar+ 2022).
- **Year:** 2021–2022.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

EUI HRI at ~1–3 s cadence resolves transverse `~1–2 Mm` "plumelets"
inside the canonical coronal plume, with Doppler-like brightness
oscillations and apparent transverse motions. The narrow claim is
that plumelets are the **fine substructure** of plumes, not separate
objects, and likely seed solar-wind microstructures.

### Method assumptions

- EUI HRI 174 Å L2 imagery available.
- Plume identified at base by AIA/EUI FSI.
- Substructure isolation via unsharp masking / wavelet filtering.

### Failure modes (skill memory)

- **Pointing jitter** can mimic substructure motions.
- **Channel limitations.** HRI 174 Å samples a narrow temperature
  range; plumelets at hotter/cooler `T` may be missed.
- **Boundary identification** between adjacent plumelets is
  intensity-threshold-sensitive.

### Claim boundary

**In scope.** EUI HRI plume substructure during coordinated
Solar-Orbiter / PSP observation windows.

**Out of scope.** Do NOT generalize to non-plume CH regions without
re-evaluating thresholds.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_eui_hri()`               | HRI 174 Å frames         |
| `image.unsharp_filter()`                | substructure isolation   |
| `tracking.plumelet_segments()`          | per-plumelet trace       |
| `analysis.transverse_motion()`          | apparent velocity        |
| `statistics.substructure_population()`  | size/lifetime histogram  |

### Procedure

1. Fetch EUI HRI sequence over a known plume.
2. Apply unsharp-masking; detect plumelets.
3. Track transverse motions; compute apparent velocity.
4. Tabulate plumelet sizes and lifetimes.

### Validation target

TODO verify — plumelet size/lifetime distributions consistent with
paper-published values.

## Layer 3 — Adapter / runtime notes (optional examples)

- EUI L2 via the EUI Data Release; `sunpy` + `scikit-image` for
  filtering.

## Layer 4 — Research-generation affordances

- **Gap:** plumelet kinematic spectra have not been compared to PSP
  near-perihelion in-situ microstructure densities.
- **Hypothesis:** plumelets are the photospheric / chromospheric
  source of `[[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]`
  switchback packets.

## Skill graph → depends_on

- `[[paper-eui-fsi-hri-coronal-bright-points-statistics]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
