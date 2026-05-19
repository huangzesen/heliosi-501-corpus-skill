---
name: paper-veronig-2018-eit-wave-dome-shock-3d
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-veronig-2018-eit-wave-dome-shock-3d

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when an EUV-wave dome is identified in
high-cadence AIA data and the user wants to reconstruct the **3-D
dome geometry as a shock surface** during the impulsive phase.

Concrete symptoms:

- The EUV wave shows a hemispherical dome visible at multiple AIA
  channels and STEREO-A EUVI off-limb.
- The user wants to associate the dome with a coronal shock and
  read off radial / lateral expansion speeds.

Do NOT use this skill for purely 2-D wavefront kinematics that no
off-limb data covers.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** EIT-Wave Dome as a 3-D Coronal Shock (representative:
  Veronig et al. 2010 / 2018; Kwon & Vourlidas 2017).
- **Year:** TODO verify (2010 / 2018 family)
- **Venue:** ApJL — TODO verify

### Claim (narrow form)

The hemispherical EUV dome observed off-limb during the impulsive
phase of an eruption represents the **3-D shock surface** driven
ahead of the CME flux rope. Its radial expansion velocity matches
the coronagraph-derived CME-shock leading-edge speed within stated
uncertainty, and its lateral expansion at the surface matches the
EUV-wavefront speed on the disk.

### Method assumptions

- Two viewpoints (SDO on-disk + STEREO off-limb) allow 3-D dome
  reconstruction by ellipsoid fitting.
- The shock surface is approximately ellipsoidal during the brief
  fitting window.
- The dome-radial expansion is identified with the shock speed (not
  the driver speed).

### Data assumptions

- High-cadence AIA + STEREO EUVI (or EUI/FSI in the modern era).
- Spacecraft ephemeris.

### Failure modes (skill memory)

- **Ellipsoid bias.** Non-ellipsoidal dome shapes (interaction with
  streamer) produce a systematic underestimate of the radial speed.
- **Driver-vs-shock confusion.** The CME flux rope sits inside the
  dome; do NOT identify the dome with the rope.
- **Off-limb contrast** is harder than on-disk; small projection
  errors in the dome's apex propagate into the radial speed.

### Figure / numerical targets

- TODO verify: dome radial speed and lateral surface speed within
  ~10–20% of CME-shock kinematics.

### Claim boundary

**In scope.** Off-limb 3-D dome reconstruction during the brief
impulsive phase of strong, on-limb / off-limb eruptions.

**Out of scope — do NOT generalize:**

- Do NOT identify every EUV dome with a fast-mode shock; weak events
  may show a wave dome without shock formation.
- Do NOT extrapolate the dome's geometry beyond the fitting window.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `imagery.fetch_aia()`                 | on-disk EUV                      |
| `imagery.fetch_stereo_euvi()`         | off-limb EUV                     |
| `geometry.fit_ellipsoid_dome()`       | 3-D ellipsoid fit                |
| `kinematics.dome_speed_radial()`      | radial expansion                 |
| `kinematics.dome_speed_lateral()`     | surface expansion                |
| `metrics.dome_vs_shock_consistency()` | dome vs coronagraph CME shock    |

### Procedure

1. **Fetch** simultaneous AIA + EUVI imagery covering the impulsive
   phase.
2. **Identify** the dome rim in each viewpoint.
3. **Fit** an ellipsoid using viewpoint geometry.
4. **Compute** radial and lateral expansion speeds.
5. **Compare** to coronagraph shock kinematics.
6. **Emit** the dome geometry time series + consistency report.

### Validation target

- **Metric:** TODO verify — dome radial speed within ~20% of
  coronagraph shock speed.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python runtime can bind `geometry.fit_ellipsoid_dome` to
  scipy.optimize.least_squares on edge-detected dome points.
- The Kwon "GCS-like" ellipsoidal shock model is one published
  adapter.

---

## Layer 4 — Research-generation affordances

- **Gap:** dome / shock geometry has not been compared with in-situ
  shock-normal angles for the same event.
- **Tension:** Dome-derived radial speed sometimes exceeds the
  GCS leading-edge speed in
  `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]` — by how
  much, systematically?
- **Hypothesis:** the dome / driver speed ratio correlates with
  type-II radio drift rate.

---

## Skill graph → depends_on

- `[[paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
