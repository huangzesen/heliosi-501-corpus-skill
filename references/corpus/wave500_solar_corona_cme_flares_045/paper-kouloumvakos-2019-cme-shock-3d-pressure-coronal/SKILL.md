---
name: paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when a workflow needs **3-D coronal shock
properties (compression ratio, normal angle, Mach number, density-jump)**
over the dome's surface, not just at one footpoint, for an SEP / radio
study.

Concrete symptoms:

- Comparing shock-normal angle to SEP onset across multiple
  spacecraft.
- Locating where a flux rope's shock first becomes super-Alfvénic.
- Pairing radio band-splitting with shock compression ratio.

Do NOT use this skill without a 3-D shock surface from
`[[paper-veronig-2018-eit-wave-dome-shock-3d]]` or equivalent.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** 3-D Coronal Shock Properties from Multi-Viewpoint
  EUV/coronagraph Modeling (representative: Kouloumvakos et al. 2019).
- **Year:** 2019
- **Venue:** ApJ — TODO verify

### Claim (narrow form)

By combining a 3-D shock surface (ellipsoidal or GCS-like) with a
known coronal background `(B, n_e, T)`, one can compute spatially
resolved shock parameters across the surface. The narrow claim is
that **the parameter that maps best onto SEP onset is the
shock-normal angle's connectivity to the observing spacecraft**, not
the maximum Mach number.

### Method assumptions

- The shock surface geometry is reconstructed independently.
- A coronal MHD or hybrid `(B, n_e, T)` background is available.
- The shock is treated as a stationary surface at each time step
  (snapshot assumption).

### Data assumptions

- Multi-viewpoint EUV+coronagraph for the shock surface.
- Coronal MHD model output (MAS, EUHFORIA, AWSoM) for background.

### Failure modes (skill memory)

- **Background MHD bias.** The coronal `B` is the largest single
  uncertainty; switching MHD models changes Mach numbers by factors
  of 2+.
- **Snapshot assumption.** Time-dependent ramp effects are lost.
- **Connectivity tracing** is sensitive to the source-surface
  radius — coordinate with
  `[[paper-source-surface-radius-optimization-eclipse-streamer]]`.

### Figure / numerical targures

- TODO verify: shock-parameter maps and SEP-onset correlation
  scores.

### Claim boundary

**In scope.** Spatially-resolved shock parameters over a 3-D
reconstructed shock surface in a known coronal background.

**Out of scope — do NOT generalize:**

- Do NOT propagate shock parameters into the heliosphere without an
  external propagation model.
- Do NOT treat the inferred Mach number as a measurement; it is a
  model-dependent inference.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                              | Purpose                          |
|-----------------------------------------|----------------------------------|
| `geometry.fit_ellipsoid_dome()` or `geometry.fit_gcs_shell()` | shock geometry |
| `mhd.background_field()`                | `(B, n_e, T)` everywhere         |
| `shock.compute_normal()`                | per-point shock normal           |
| `shock.compute_mach_compression()`      | per-point shock parameters       |
| `field.trace_lines()`                   | spacecraft connectivity          |
| `metrics.parameter_vs_sep_onset()`      | correlate with SEP onset         |

### Procedure

1. **Reconstruct** the 3-D shock surface at each snapshot.
2. **Sample** the MHD background at each surface point.
3. **Compute** shock-normal angle, density ratio, Mach number
   per point.
4. **Trace** field lines from each surface point and check whether
   they intersect spacecraft locations.
5. **Correlate** the per-point parameters with observed SEP onsets.

### Validation target

- **Metric:** TODO verify — SEP-onset correlation with
  shock-normal connectivity exceeds baseline (e.g. radial
  separation).

---

## Layer 3 — Adapter / runtime notes (optional examples)

- The published reference adapter is the SUSANOO / MAS MHD model
  output combined with the PFSS+ellipsoid Kouloumvakos pipeline.
- Python: connect to MAS via the `psipy` package as one example.

---

## Layer 4 — Research-generation affordances

- **Gap:** the same event has not been run through MAS *and* EUHFORIA
  *and* AWSoM with this skill to bound the model-dependence of
  Mach-number maps.
- **Tension:** shock-normal-connectivity predictions sometimes
  conflict with the simple "radial separation" predictor of
  `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]`.
- **Hypothesis:** the shock-parameter map's predictive value
  depends most strongly on the source-surface radius choice.

---

## Skill graph → depends_on

- `[[paper-veronig-2018-eit-wave-dome-shock-3d]]`
- `[[paper-mas-mhd-global-coronal-thermodynamic-model]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
