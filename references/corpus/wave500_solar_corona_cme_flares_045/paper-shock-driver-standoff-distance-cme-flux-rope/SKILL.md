---
name: paper-shock-driver-standoff-distance-cme-flux-rope
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-shock-driver-standoff-distance-cme-flux-rope

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when the workflow needs the **standoff distance**
between a CME's driver flux rope and its shock front — a diagnostic of
flux-rope curvature and ambient sonic/Alfvénic Mach number.

Concrete symptoms:

- A coronagraph shows a clear sheath-shock pair ahead of the rope.
- A user is testing the analogy `Δ/R_c ∝ f(M_A)` between solar and
  planetary bow-shock standoff scaling.

Do NOT use this skill without geometric estimates of both the shock
surface and the flux-rope leading edge (separately).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Standoff Distance of Shocks Driven by CME Flux Ropes
  (representative: Maloney & Gallagher 2011; Savani+ 2012; Hess +
  Zhang 2015).
- **Year:** TODO verify
- **Venue:** ApJ — TODO verify

### Claim (narrow form)

The ratio of standoff distance to flux-rope radius of curvature
`Δ / R_c` scales with the upstream Alfvénic Mach number `M_A` similarly
to a planetary bow shock, allowing `M_A` to be inferred from geometry
alone when in-situ measurements are unavailable.

### Method assumptions

- Both the shock surface and the rope leading edge can be identified
  independently.
- The flux rope's radius of curvature can be estimated (e.g. GCS).
- The upstream Alfvén speed is taken from a coronal model.

### Data assumptions

- Multi-viewpoint coronagraph imagery.
- A coronal MHD or hybrid `v_A` map.

### Failure modes (skill memory)

- **R_c ambiguity** when the flux rope is non-circular in cross-section.
- **Shock-rope blending** when the standoff is smaller than the
  imaging resolution.
- **Coronal `v_A` uncertainty** dominates `M_A` inference (≳ factor 2).
- **Geometry must be self-consistent**: don't mix a GCS shell with an
  ellipsoidal shock fit on a different time stamp.

### Figure / numerical targets

- TODO verify: `Δ/R_c` vs `M_A` consistent with the planetary
  bow-shock empirical curve.

### Claim boundary

**In scope.** Geometric standoff diagnostic for impulsive CMEs with
clearly resolved sheaths in the outer corona (3–20 R_sun).

**Out of scope — do NOT generalize:**

- Do NOT use `Δ/R_c` to infer plasma β.
- Do NOT extrapolate to the heliosphere without coupling to a
  propagation model.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                              | Purpose                          |
|-----------------------------------------|----------------------------------|
| `geometry.fit_gcs_shell()`              | flux-rope geometry               |
| `geometry.fit_ellipsoid_dome()`         | shock geometry                   |
| `geometry.compute_curvature()`          | R_c at leading edge              |
| `geometry.standoff_distance()`          | Δ = shock − rope leading edge    |
| `mhd.background_alfven_speed()`         | v_A at the standoff location     |
| `metrics.bow_shock_scaling()`           | Δ/R_c vs inferred M_A            |

### Procedure

1. **Fit** rope and shock geometries at matched time stamps.
2. **Compute** R_c at the nose of the rope and Δ along the
   normal.
3. **Sample** `v_A` at the standoff location.
4. **Compare** to the planetary bow-shock scaling.
5. **Emit** `(Δ, R_c, M_A)` time series.

### Validation target

- **Metric:** TODO verify — `Δ/R_c` consistent with the chosen
  scaling within ~30%.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python runtime can use the GCS+ellipsoid adapters from the
  earlier skills; v_A from MAS via `psipy`.

---

## Layer 4 — Research-generation affordances

- **Gap:** the analogy with planetary bow shocks is asserted more
  than tested; a multi-event scan in the 3–20 R_sun range is
  missing.
- **Tension:** Δ/R_c-inferred M_A sometimes disagrees with the
  in-situ M_A at 1 au — pair with
  `[[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]`.
- **Hypothesis:** Δ/R_c-inferred M_A converges to in-situ M_A only
  for events where flux-rope deformation is small (test by combining
  with `[[paper-cme-flux-rope-self-similar-expansion-near-sun]]`).

---

## Skill graph → depends_on

- `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]`
- `[[paper-veronig-2018-eit-wave-dome-shock-3d]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
