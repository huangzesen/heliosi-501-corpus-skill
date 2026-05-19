# paper-aulanier-2012-standard-flare-model-3d-tether-cutting

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when interpreting flare ribbon and arcade
geometry in terms of the **3-D extension of the standard CSHKP /
tether-cutting flare model** (Aulanier et al. 2012, 2013).

Concrete symptoms:

- Mapping the J-shape of flare ribbons to the underlying flux-rope
  footprint.
- Reconciling apparent two-ribbon vs. circular-ribbon morphologies.
- Predicting which side of the polarity-inversion-line reconnects
  first.

Do NOT use this skill for purely 2.5-D reconnection models or models
without a coherent flux rope.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Standard Solar Flare Model in 3-D — Tether-Cutting
  Reconnection (representative: Aulanier et al. 2012, 2013).
- **First author:** G. Aulanier
- **Year:** 2012
- **Venue:** A&A — TODO verify

### Claim (narrow form)

A 3-D flux-rope-eruption MHD simulation reproduces the canonical
flare observables (two J-shaped ribbons, post-flare arcade, flux-rope
exit) and predicts that **ribbon hooks coincide with the flux rope's
footpoints** and **the polarity-inversion-line cuts the
ribbon-separation distance**.

### Method assumptions

- Zero-β / low-β MHD simulation of a pre-existing flux rope.
- Photospheric boundary holds the rope in equilibrium until the
  decay-index threshold is crossed.
- Reconnection is anomalous-resistivity-driven; no kinetic effects.

### Data assumptions

- Vector magnetogram for boundary inversion (or analytic setup).
- Observed ribbon morphology for comparison.

### Failure modes (skill memory)

- **Resistivity choice** dominates reconnection rate and ribbon
  expansion speed.
- **Pre-existing rope assumption.** The standard model takes the
  rope as given; flux-emergence-driven ropes may behave differently.
- **Ribbon hooks** depend on the rope footpoint definition; pick a
  consistent convention.
- **Confined eruptions** are not the model's intended regime.

### Figure / numerical targets

- TODO verify: simulated ribbon morphology matches observed J-shape
  for the analog event.

### Claim boundary

**In scope.** 3-D standard flare model for eruptive flares with
clear flux-rope footpoint signatures.

**Out of scope — do NOT generalize:**

- Do NOT extend conclusions to confined flares or jet flares.
- Do NOT use the simulated reconnection rate as ground truth.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `mhd.setup_flux_rope_equilibrium()`   | initial Titov-Démoulin rope      |
| `mhd.run_zero_beta()`                 | integrate eruption               |
| `topology.find_qsl_footprint()`       | flux-rope feet trace             |
| `imagery.map_ribbons_uv()`            | observed ribbon outline          |
| `metrics.ribbon_footprint_overlap()`  | model–obs comparison             |

### Procedure

1. **Initialize** a Titov-Démoulin rope in equilibrium.
2. **Trigger** loss of equilibrium (decay-index threshold).
3. **Run** the zero-β MHD simulation.
4. **Trace** flux-rope footpoints in 3-D.
5. **Compare** model footpoints to observed UV ribbons.

### Validation target

- **Metric:** TODO verify — area-overlap or contour-distance of
  model footpoints vs UV ribbons.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- The published reference adapter is the OHM / Aulanier-group MHD
  code; modern open-source analogs include `Lare3d`, `PENCIL`,
  `Pluto`.

---

## Layer 4 — Research-generation affordances

- **Gap:** the standard model has rarely been tested on circular-
  ribbon flares where the topology is null-point-driven.
- **Tension:** observed ribbon-hook positions sometimes lie
  off-PIL — does this require a non-standard flux-rope topology, or
  is the offset within model uncertainty? Compose with
  `[[paper-flare-ribbon-photospheric-magnetic-shear]]`.
- **Hypothesis:** ribbon-footpoint overlap with model footpoints
  improves when the NLFFF extrapolation
  (`[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`) is
  used to seed the rope geometry.

---

## Skill graph → depends_on

- `[[paper-titov-demoulin-2014-flux-rope-insertion-eruption]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
