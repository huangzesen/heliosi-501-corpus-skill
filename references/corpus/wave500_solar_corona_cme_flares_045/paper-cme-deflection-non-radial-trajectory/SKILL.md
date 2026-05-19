# paper-cme-deflection-non-radial-trajectory

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when a CME's observed propagation direction in
the outer corona is **systematically offset from the radial above its
photospheric source**, and the workflow needs a deflection model.

Concrete symptoms:

- GCS longitudes drift between successive frames in a way inconsistent
  with self-similar radial expansion.
- A CME launched from a high-latitude AR arrives at the equator.
- Coronal-hole geometry is suspected of steering the CME.

Do NOT use this skill for narrow-angle slow CMEs propagating quasi-
radially in solar-minimum conditions.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** CME Deflection by the Ambient Coronal Field
  (TODO verify exact title; representative paper family —
  Gui+ 2011, Kay+ 2015, Wang+ 2014).
- **First author:** TODO verify
- **Year:** TODO verify (canonical: 2011–2015 era)
- **Venue:** ApJ / Sol. Phys. — TODO verify

### Claim (narrow form)

The narrow claim shared by this paper family is that the angular
position of a CME in the outer corona can be modeled as a sum of
**radial propagation + a deflection term driven by the gradient of
the magnetic-energy density in the surrounding coronal field**.
The deflection scales with the magnetic-pressure gradient over the
CME's path and converges as the CME crosses the Alfvén radius.

### Method assumptions

- A global background coronal magnetic field is available (PFSS,
  NLFFF, or MHD).
- The CME is light enough vs. the ambient corona that the deflection
  is a perturbation, not a regime change.
- The deflection is azimuthal-plus-meridional; full 3-D dynamics in
  some implementations is reduced to a guiding-center model.

### Data assumptions

- Coronagraph 3-D angular trajectory `(lon(t), lat(t))`.
- Background coronal `B(r,θ,φ)` from PFSS or MHD.

### Failure modes (skill memory)

- **Background-field staleness.** A 27-day-averaged synoptic
  background fails for CMEs launched into a fresh active-region
  complex.
- **Strong deflection invalidates perturbation.** Very fast/wide CMEs
  reshape the background as they propagate; the assumption breaks.
- **Open/closed field discontinuity.** Crossing a coronal-hole
  boundary produces a non-smooth deflection that perturbative models
  miss.

### Figure / numerical targets

- TODO verify: e.g. reproduce a benchmark event's
  `(lon(t), lat(t))` trajectory within ~5–10° over the 2–10 R_sun
  range.

### Claim boundary

**In scope.** Perturbative deflection of single CMEs through a known
ambient coronal field, in the 2–20 R_sun range.

**Out of scope — do NOT generalize:**

- Do NOT use this for CME–CME interaction (cannibalism).
- Do NOT use the model after Alfvén-radius crossing — heliospheric
  drag dominates there.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                                 | Purpose                  |
|--------------------------------------------|--------------------------|
| `geometry.fit_gcs_trajectory()`            | observed angular path    |
| `pfss.solve()` or `mhd.background_field()` | ambient coronal field    |
| `dynamics.compute_deflection_force()`      | grad(B²/8π) along path   |
| `dynamics.integrate_trajectory()`          | propagate guiding-center |
| `metrics.angular_residual()`               | compare to observation   |

### Procedure

1. **Fit** observed CME centerline `(lon(t), lat(t), h(t))`.
2. **Compute** background coronal `B` over the relevant volume.
3. **Integrate** the deflection ODE from the photospheric source
   outward.
4. **Compare** modeled `(lon(t), lat(t))` to observed.
5. **Emit** angular-residual time series + parameter sensitivity.

### Validation target

- **Metric:** TODO verify — angular residual at 10 R_sun.
- **Tolerance:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python runtime can bind `pfss.solve()` to `sunkit-magex` and
  the deflection ODE to `scipy.integrate.solve_ivp`.
- The ForeCAT (Kay et al.) family of codes is one published adapter.

---

## Layer 4 — Research-generation affordances

- **Gap:** the deflection model's accuracy is rarely tested against
  in-situ arrival longitudes; pairing with
  `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]`
  could close the loop.
- **Tension:** PFSS-driven and MHD-driven deflections give different
  answers for the same event — quantify with
  `[[paper-mas-mhd-global-coronal-thermodynamic-model]]`.
- **Hypothesis:** deflection magnitude correlates with the
  coronal-hole-boundary distance at the source, testable using
  `[[paper-coronal-hole-boundary-detection-suvi-segmentation]]`.

---

## Skill graph → depends_on

- `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]`
- `[[paper-mas-mhd-global-coronal-thermodynamic-model]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
