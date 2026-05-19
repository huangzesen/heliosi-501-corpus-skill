# paper-eui-euv-wave-fast-mode-mhd-front

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when an EUV wave (a.k.a. EIT wave / large-scale
coronal bright front) is identified in high-cadence EUV imagery
(AIA/EUI/SUVI) and must be classified as **fast-mode MHD front vs.
field-line opening signature**.

Concrete symptoms:

- A wavefront expands quasi-circularly from a CME source region.
- The user needs to test the fast-mode prediction: speed `~ v_A` and
  reflection / refraction at coronal-hole boundaries.
- Pairing the wave kinematics with a type-II radio onset.

Do NOT use this skill for "stationary EUV brightenings" or for
brightenings explained by streamer compression alone.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** EUV Wave as a Fast-Mode MHD Front (representative:
  Patsourakos & Vourlidas 2012; Long+ 2017; Liu+ 2018).
- **Year:** TODO verify
- **Venue:** ApJL / Sol. Phys. — TODO verify

### Claim (narrow form)

The bright EUV front that propagates away from a CME source region
travels at a speed consistent with the local fast-magnetosonic speed
and shows reflection / refraction at coronal-hole boundaries — the
canonical signature of a fast-mode MHD wave. The narrow claim is that
the observed front velocity in the quiet corona is
`v_obs ≈ 200–1000 km/s ≈ v_fast(corona)` within stated uncertainty.

### Method assumptions

- The wavefront can be tracked at ≤ 1-min cadence (AIA 12s, EUI HRI
  up to 1-2s).
- Coronal Alfvén-speed maps are available (from DEM + PFSS).
- Front identification is consistent across two or more EUV channels.

### Data assumptions

- High-cadence multi-channel EUV imagery.
- A coronal `v_A(θ,φ)` map for comparison.

### Failure modes (skill memory)

- **Front identification.** Running-difference highlights gradients
  but biases speed estimates; base-difference biases position.
- **Channel mixing.** 193 Å and 211 Å fronts disagree subtly because
  of DEM differences; pick one and report.
- **Pseudo-waves.** Some "EUV waves" are field-line opening
  signatures with no MHD wave nature — co-temporal stationary
  brightenings are the giveaway.
- **`v_A` maps are uncertain** by factors of 2 in the quiet corona;
  reflection / refraction is a stronger discriminant than absolute
  speed.

### Figure / numerical targets

- TODO verify: front kinematic time profile in two channels +
  reflection-angle comparison at a CH boundary.

### Claim boundary

**In scope.** Fast-mode classification of EUV waves driven by impulsive
CME eruptions in the quiet corona.

**Out of scope — do NOT generalize:**

- Do NOT claim every EUV brightening is a fast-mode wave.
- Do NOT use this skill in regions saturated by the AIA channels.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                  |
|---------------------------------------|--------------------------|
| `imagery.fetch_aia()`                 | 171/193/211 Å            |
| `imagery.fetch_eui_fsi()`             | EUI full-Sun imager      |
| `imagery.running_diff()` / `base_diff()` | wavefront enhancement |
| `kinematics.front_track()`            | radial profile vs time   |
| `coronal_dem.compute_alfven_map()`    | `v_A(θ,φ)` map           |
| `metrics.fastmode_consistency()`      | refraction / reflection  |

### Procedure

1. **Fetch** EUV imagery in 2+ channels at high cadence.
2. **Enhance** the front (running- and base-difference).
3. **Track** the front along radial sectors away from the source.
4. **Compute** an `v_A` map.
5. **Compare** front velocity to `v_A` and look for refraction at
   CH boundaries.
6. **Emit** a fast-mode-consistency report.

### Validation target

- **Metric:** TODO verify — front speed within factor ~2 of `v_A`
  AND reflection at CH boundary.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Python: `aiapy` for AIA prep; `sunpy.net.Fido` for fetch; SunPy's
  reprojection for sector extraction.
- EUI L2 files via the EUI Data Release.

---

## Layer 4 — Research-generation affordances

- **Gap:** EUI HRI sub-cadence wavefronts have not been linked to
  type-II radio onset timing systematically.
- **Tension:** `[[paper-warmuth-2015-large-scale-coronal-waves-review]]`
  notes a population of slower (~200 km/s) waves that may not fit
  the fast-mode picture cleanly.
- **Hypothesis:** the slow-wave population is dominated by
  field-line-opening pseudo-waves at coronal-hole edges.
- **Experiment:** classify a sample of EUV waves into fast vs slow
  using `v_A` maps and check the proportion of pseudo-wave
  signatures.

---

## Skill graph → depends_on

- `[[paper-warmuth-2015-large-scale-coronal-waves-review]]`
- `[[paper-suvi-multi-wavelength-temperature-dem-corona]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
