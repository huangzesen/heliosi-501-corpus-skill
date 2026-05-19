# paper-flare-ribbon-photospheric-magnetic-shear

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when measuring the **reconnection flux** and
**photospheric magnetic shear** swept up by expanding flare ribbons,
to estimate the total reconnected magnetic flux in a flare.

Concrete symptoms:

- A user wants the reconnection-rate time profile for a flare.
- Comparing total reconnected flux to CME flux-rope poloidal flux.

Do NOT use this skill for ribbons without simultaneous photospheric
magnetograms.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Photospheric Magnetic-Flux Reconnection Rate from Flare
  Ribbon Expansion (representative: Qiu+ 2002; Kazachenko+ 2017).
- **Year:** TODO verify
- **Venue:** ApJ — TODO verify

### Claim (narrow form)

The total reconnected magnetic flux during a flare is
`Φ_rec = ∫ dt ∫_ribbon |B_LOS| dA`, where the time-derivative gives
the instantaneous reconnection rate. The narrow claim is that this
ribbon-integrated reconnection flux is approximately equal to the
**poloidal flux of the associated CME flux rope** within stated
uncertainty.

### Method assumptions

- Ribbons are co-spatial with photospheric footprints of newly
  reconnected field lines.
- LOS magnetogram is a good proxy for the radial component near
  disk-center.
- Saturated UV / Hα emission can be detected and time-stamped at
  high cadence.

### Data assumptions

- HMI / MDI LOS magnetogram.
- AIA 1600 Å or comparable UV ribbon imagery.
- For CME comparison: in-situ flux-rope fit or coronagraph
  flux-rope poloidal flux.

### Failure modes (skill memory)

- **Saturated UV** can clip the ribbon area, biasing reconnection
  rate low.
- **LOS ≠ radial** off-disk-center; apply a μ-correction.
- **Background flux confusion** when ribbons cross sunspot
  penumbrae.
- **Pre-existing brightenings** must be masked.

### Figure / numerical targets

- TODO verify: `Φ_rec` vs CME poloidal flux within factor ~2.

### Claim boundary

**In scope.** Photospheric reconnection-flux estimate for eruptive
flares with clear ribbon expansion on the disk.

**Out of scope — do NOT generalize:**

- Do NOT use on limb flares without disambiguation.
- Do NOT identify `Φ_rec` with the *total* CME poloidal flux at 1 au
  without a propagation model.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `imagery.fetch_aia_1600()`            | UV ribbon imagery                |
| `magnetogram.fetch_los()`             | HMI LOS                          |
| `ribbon.detect_mask()`                | per-frame ribbon mask            |
| `ribbon.accumulate_swept_flux()`      | integrate `|B_LOS|` newly swept  |
| `metrics.compare_to_cme_flux()`       | vs flux-rope poloidal flux       |

### Procedure

1. **Fetch** simultaneous UV ribbon imagery and LOS magnetogram.
2. **Detect** newly brightened pixels (excluding persistent ones).
3. **Integrate** `|B_LOS|` over newly-swept pixels and accumulate.
4. **Derive** the reconnection-rate time series.
5. **Compare** to CME poloidal flux.

### Validation target

- **Metric:** TODO verify — `Φ_rec / Φ_CME_pol` within factor ~2.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Python: `aiapy` + `sunpy.net.Fido`; mask via `scikit-image`
  thresholding on running-difference.

---

## Layer 4 — Research-generation affordances

- **Gap:** the apparent factor-2 discrepancy between `Φ_rec` and
  in-situ flux-rope poloidal flux has competing explanations;
  pair with
  `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]`.
- **Tension:** UV-derived `Φ_rec` is systematically larger than
  Hα-derived estimates on the same event.
- **Hypothesis:** the discrepancy scales with the AR's pre-flare
  free magnetic energy
  (`[[paper-cheung-2019-flare-energy-buildup-3d-mhd-active-region]]`).

---

## Skill graph → depends_on

- `[[paper-aulanier-2012-standard-flare-model-3d-tether-cutting]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
