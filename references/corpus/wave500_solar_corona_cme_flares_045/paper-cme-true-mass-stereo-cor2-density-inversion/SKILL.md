# paper-cme-true-mass-stereo-cor2-density-inversion

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when a workflow needs the **true (3-D-corrected)
mass** of a CME from coronagraph brightness, separating
plane-of-sky projection from the actual line-of-sight integral.

Concrete symptoms:

- Mass derived from single-viewpoint LASCO is suspected of being a
  lower bound.
- Multi-view STEREO/SECCHI data are available and the user needs the
  geometric correction factor.
- Mass time series is needed for a kinematic energy partition study.

Do NOT use this skill for CMEs without a coronagraph view sufficiently
far from the Sun–Earth line (geometric correction is degenerate).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** True CME Mass from Multi-Viewpoint Coronagraph Density
  Inversion (representative: Colaninno & Vourlidas 2009; Carley+ 2012).
- **Year:** TODO verify
- **Venue:** ApJ — TODO verify

### Claim (narrow form)

By inverting Thomson-scattering brightness from multi-viewpoint
coronagraph images and assuming a known 3-D geometry (GCS or mask),
one recovers the CME's "true mass" — the line-of-sight-integrated
electron column density mapped onto the assumed shell. The narrow
claim is that this true mass is **typically 1.5–3× the plane-of-sky
mass** estimated from a single LASCO viewpoint, depending on the
true longitude of the CME.

### Method assumptions

- Thomson scattering dominates the coronagraph brightness above
  ~3 R_sun.
- The 3-D geometry of the CME body is known (from GCS or equivalent).
- A reference background coronal density is subtracted (pre-event
  base difference).

### Data assumptions

- Multi-viewpoint coronagraph time series.
- Polarized brightness available for at least one viewpoint
  (optional but tightens the inversion).

### Failure modes (skill memory)

- **Geometry assumption dominates.** If the 3-D shell is wrong, the
  mass is wrong; mass and geometry must be reported together.
- **Background subtraction.** Pre-event base must be on quiet
  conditions; an ongoing event in the background biases the mass.
- **Plate-scale and calibration drift** in long event windows can
  produce spurious mass-loss / mass-gain trends.
- **Shock vs body separation.** If a shock sheath is included in the
  mask, mass is over-counted relative to the flux rope itself.

### Figure / numerical targets

- TODO verify: ratio of true to POS mass on benchmark events
  (placeholder 1.5–3×).

### Claim boundary

**In scope.** CME body mass from multi-viewpoint Thomson-scattering
inversion above ~3 R_sun.

**Out of scope — do NOT generalize:**

- Do NOT use to infer flux-rope plasma β.
- Do NOT include the shock sheath unless explicitly modeled.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `imagery.fetch_stereo_cor2()`         | A/B COR2                         |
| `imagery.fetch_lasco()`               | C2/C3                            |
| `imagery.preprocess_base_diff()`      | background-subtracted brightness |
| `geometry.fit_gcs_shell()`            | 3-D shape per frame              |
| `radiation.thomson_invert_density()`  | brightness → Ne column           |
| `geometry.integrate_mass()`           | Ne mapped onto shell             |
| `metrics.true_vs_pos_ratio()`         | correction factor                |

### Procedure

1. **Fetch** multi-viewpoint coronagraph time series.
2. **Subtract** pre-event background per viewpoint.
3. **Fit** 3-D geometry; lock to the chosen shell.
4. **Invert** Thomson brightness to electron column density.
5. **Integrate** the column density over the projected shell area
   to get the CME mass per viewpoint.
6. **Cross-check** mass between viewpoints; emit the consensus mass
   and POS-correction factor.

### Validation target

- **Metric:** TODO verify (placeholder: mass ratio between viewpoints
  within ~30% on benchmark events).

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `radiation.thomson_invert_density` to the
  Billings/Howard scattering kernel.
- IDL `secchi_prep` is one published adapter for the preprocessing
  pipeline.

---

## Layer 4 — Research-generation affordances

- **Gap:** the POS-correction factor's distribution across the CME
  population has not been re-evaluated with modern multi-viewpoint
  catalogs.
- **Tension:** mass derived from
  `[[paper-metis-coronal-polarized-brightness-electron-density]]`
  inversions in the 3–6 R_sun range can disagree with COR2-derived
  mass in the 6–15 R_sun range on the same event.
- **Hypothesis:** mass-loss between 3 R_sun and 15 R_sun is mostly
  an artifact of geometry mismatch, not real mass loss.
- **Experiment:** apply both inversions to a Metis–LASCO conjunction
  event and check whether the mass-loss disappears once geometry is
  shared.

---

## Skill graph → depends_on

- `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]`
- `[[paper-metis-coronal-polarized-brightness-electron-density]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
