---
name: paper-cme-flux-rope-self-similar-expansion-near-sun
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-cme-flux-rope-self-similar-expansion-near-sun

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when a workflow needs the **self-similar expansion
assumption** of a CME flux rope between ~2 and ~20 R_sun — i.e. how its
size, density, and magnetic flux scale with heliocentric distance.

Concrete symptoms:

- Forward-modeling needs a single scaling law for shell width vs. height.
- Density inversion of coronagraph brightness requires a known
  expansion profile.
- Magnetic-cloud size at 1 au needs to be back-extrapolated.

Do NOT use this skill in regimes where the rope is still forming
(< 2 R_sun) or after the rope has interacted with another structure.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Self-Similar Expansion of CME Flux Ropes (representative
  family — Démoulin & Dasso, Wang+ etc.)
- **First author:** TODO verify
- **Year:** TODO verify (canonical 2009–2014 era)
- **Venue:** A&A / Sol. Phys. — TODO verify

### Claim (narrow form)

The flux rope's transverse radius `a(t)` and axial length `L(t)` both
scale as `~h(t)^k` with a single exponent `k ≈ 1` (within stated
range), and density scales as `~h^(-α)` with `α ≈ 2–3`. The narrow
claim is that within the 2–20 R_sun window, **the rope's
non-dimensional shape parameters are time-independent** (self-similar).

### Method assumptions

- Magnetic flux through any cross-section is conserved during the
  expansion.
- Force-free or near-force-free interior.
- No mass loss or accretion across the rope's outer boundary.

### Data assumptions

- Multi-viewpoint coronagraph time series of the same rope.
- Optional: photospheric magnetogram for total reconnection flux.

### Failure modes (skill memory)

- **Non-self-similar early phase.** Between 1.5 and 2 R_sun the rope
  geometry is still being formed and `k` is not constant.
- **Interaction events.** If the rope hits a streamer or another CME,
  self-similarity breaks.
- **Mass overestimation.** Coronagraph brightness inversion that
  assumes self-similarity overestimates mass during deceleration if
  the rope is non-self-similar in reality.

### Figure / numerical targets

- TODO verify: e.g. `a/h` constant within 10% over the 2–20 R_sun
  window for the benchmark event.

### Claim boundary

**In scope.** Single, non-interacting flux ropes in the 2–20 R_sun
window.

**Out of scope — do NOT generalize:**

- Do NOT extrapolate the same `k`, `α` to 1 au without an external
  drag model.
- Do NOT use for CME–CME interaction events.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                              | Purpose                       |
|-----------------------------------------|-------------------------------|
| `geometry.fit_gcs_trajectory()`         | shape parameters per frame    |
| `scaling.fit_powerlaw_aspect()`         | k for a/h                     |
| `scaling.fit_powerlaw_density()`        | α for density                 |
| `metrics.scatter_residual()`            | residual from self-similar    |
| `filesystem.write_report()`             | tabulated `(k, α)` per event  |

### Procedure

1. **Fit** GCS at each time step.
2. **Tabulate** `(h, a, L, ρ)`.
3. **Fit** power-laws `a(h)`, `L(h)`, `ρ(h)`.
4. **Test** the residual against the self-similar null.
5. **Emit** `(k, α)` and a self-similarity confidence metric per
   event.

### Validation target

- **Metric:** TODO verify — `|k − 1| < 0.1` and `α ∈ [2, 3]` for
  benchmark events.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Python: `numpy.polyfit` on `log(h)` vs `log(a)`; pairs naturally
  with the GCS adapter chain.

---

## Layer 4 — Research-generation affordances

- **Gap:** the self-similar exponent's variation with CME speed has
  not been mapped — `[[paper-cme-kinematics-three-phase-acceleration-profile]]`
  provides the speed catalog needed.
- **Tension:** density inversion from
  `[[paper-cme-true-mass-stereo-cor2-density-inversion]]` sometimes
  disagrees with self-similar predictions in the deceleration phase.
- **Hypothesis:** non-self-similar events systematically have
  upstream-shock evidence in
  `[[paper-shock-driver-standoff-distance-cme-flux-rope]]`.
- **Experiment:** classify events into self-similar / non-self-similar
  buckets and correlate with shock presence and in-situ flux-rope
  radial size at 1 au.

---

## Skill graph → depends_on

- `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
