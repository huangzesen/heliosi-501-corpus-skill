---
name: paper-thernisien-2011-gcs-fitting-cme-flux-rope
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-thernisien-2011-gcs-fitting-cme-flux-rope

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow needs **3-D flux-rope geometry**
fitted to multi-viewpoint coronagraph imagery (STEREO COR2 ± LASCO C2/C3),
i.e. a Graduated Cylindrical Shell (GCS) fit to a CME.

Concrete symptoms:

- A CME observed simultaneously from two or three viewpoints, where the
  user needs `(longitude, latitude, tilt, half-angle, aspect ratio,
  height)` time series.
- A source-mapping or shock-driver study needs the geometric centerline
  trajectory of the flux rope rather than a single plane-of-sky height.
- Cross-comparison of CME parameters between independent fits / authors.

Do NOT use this skill for narrow plane-of-sky kinematics where a single
LASCO viewpoint suffices, or for halo CMEs without an off-Sun-Earth
viewpoint (degenerate geometry).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Implementation of the Graduated Cylindrical Shell Model
  for the 3D Reconstruction of Coronal Mass Ejections
- **First author:** A. Thernisien
- **arXiv:** TODO verify
- **Year:** 2011
- **Venue:** ApJS — TODO verify final volume/page

### Claim (narrow form)

The paper introduces a parametric, single-tube "croissant" flux-rope
shell (GCS) whose forward-modeled white-light projections can be fit
visually or by least-squares to multi-viewpoint coronagraph images.
The narrow claim is that 6 free parameters
`(lon, lat, tilt, half-angle, aspect-ratio, height)` reproduce the
**bright outer envelope** of a CME flux rope across STEREO-A, STEREO-B
and LASCO views within the observational uncertainty of the period.

### Method assumptions

- The CME is a single, self-similar, hollow flux-rope shell with
  Gaussian density across the tube cross-section.
- Thomson-scattered brightness is dominated by the shell electrons.
- The shape parameters are constant during the fit window (self-similar
  expansion).
- Plane-of-sky and 3-D position-angle parameters are decoupled from
  velocity (separate kinematic fit).

### Data assumptions

- Two or more simultaneous coronagraph viewpoints during the same
  observation cadence.
- Image preprocessing (background subtraction, polarization, calibration)
  is already done.
- Carrington/HEEQ frame for the geometry; spacecraft ephemeris available.

### Failure modes (skill memory)

- **Halo geometry degeneracy.** Single-viewpoint or near-halo geometry
  makes `(lon, lat)` and `(aspect-ratio, height)` largely
  unidentifiable.
- **Visual fitting bias.** Manually-drawn shell overlays carry an
  operator-dependent bias of `~10° in lon/lat`, `~0.05` in
  aspect-ratio. Cross-author scatter dominates the formal uncertainty.
- **Shell vs. driver gas mismatch.** GCS fits the bright leading edge,
  not the (hotter, denser) core; shock standoff and core kinematics
  must be derived separately.
- **Self-similarity breaks** for deflected or interacting CMEs and in
  the very low corona (< 2 R_sun) where the flux rope is still
  forming.
- **Brightness depth.** Multiple structures along the line of sight
  can be over-fit as one shell.

### Figure / numerical targets

- TODO verify exact figure: typical demonstration is a multi-event
  table of GCS parameters and a residual-image overlay.

### Claim boundary

**In scope.** Parametric flux-rope geometry from coronagraph
white-light during a CME's outer-corona propagation phase, for
events with ≥2 viewpoints separated by ~tens of degrees.

**Out of scope — do NOT generalize:**

- Do NOT use GCS parameters as the CME's dynamical/MHD model; it is a
  geometry, not a force balance.
- Do NOT extract internal magnetic-field orientation from GCS tilt
  without independent confirmation.
- Do NOT apply unmodified GCS to driver-shock geometry; the shock is
  outside the shell.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          | Notes |
|---------------------------------------|----------------------------------|-------|
| `imagery.fetch_lasco()`               | LASCO C2/C3 frames               | per CME time window |
| `imagery.fetch_stereo_cor2()`         | STEREO-A/B COR2 frames           | matched cadence |
| `imagery.preprocess_running_diff()`   | background-suppressed views      | local |
| `geometry.project_gcs_shell()`        | forward-model shell on each view | local |
| `optimization.fit_shell_visual()`     | interactive / LSQ shell fit      | local |
| `ephemeris.spacecraft()`              | viewpoint geometry (A/B/L1)      | mission ephemeris |
| `filesystem.write_report()`           | JSON of fit + residual stack     | local |

### Procedure

1. **Fetch** matched coronagraph frames across all available
   viewpoints during the event window.
2. **Preprocess** to running-difference or fixed-base-difference.
3. **Initialize** GCS parameters from a coarse visual fit.
4. **Project** the GCS shell into each viewpoint using spacecraft
   ephemeris.
5. **Optimize** parameters (visual or LSQ) until projected shell
   matches the bright envelope in every view.
6. **Repeat** at successive times to build `(t, height, lon, lat,
   tilt, ...)` series.
7. **Emit** JSON parameter time series + residual image stack.

### Validation target

- **Metric:** TODO verify (placeholder: parameter scatter vs. an
  independent re-fit of the same event ≤ ~10° in lon/lat).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- The GCS forward-model is small enough to be a NumPy routine; common
  Python adapters: `gcs_python`, custom IDL `rtsccguicloud`. The skill
  is agnostic about the implementation.
- `imagery.fetch_*` can bind to `sunpy.net.Fido` for LASCO and STEREO.
- An interactive runtime can bind `optimization.fit_shell_visual()` to
  a GUI; a batch runtime can use a least-squares cost on residual
  images.

---

## Layer 4 — Research-generation affordances

- **Gap:** every multi-viewpoint CME catalog (e.g. HELCATS, DONKI) uses
  GCS with different operator conventions; cross-catalog inter-operator
  bias is not formally propagated into downstream arrival-time models.
- **Tension:** GCS-derived flux-rope tilt sometimes disagrees with
  in-situ magnetic-cloud rotation from
  `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]`.
- **New hypothesis to test:** does the GCS-vs-in-situ tilt residual
  correlate with CME deflection traces in
  `[[paper-cme-deflection-non-radial-trajectory]]`?
- **Experiment:** fit GCS to a curated set of events already mapped by
  `[[paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal]]` and check
  whether shock standoff scales with GCS aspect ratio.

---

## Skill graph → depends_on

- `[[paper-mierla-2010-3d-cme-reconstruction-stereo-secchi]]` — the
  multi-viewpoint reconstruction framework the GCS sits inside.
- `[[paper-cme-flux-rope-self-similar-expansion-near-sun]]` — the
  self-similarity assumption GCS makes explicit.

## Links

- arXiv: TODO verify
- DOI: TODO verify
- ADS: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` (CME 3-D reconstruction section)
