---
name: paper-cme-kinematics-three-phase-acceleration-profile
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-cme-kinematics-three-phase-acceleration-profile

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when CME kinematics need to be decomposed into the
canonical **slow-rise → impulsive-acceleration → propagation** phases
(Zhang & Dere 2006-family), in particular when aligning the impulsive
phase with flare-impulsive timing.

Concrete symptoms:

- Pairing a CME's acceleration peak with an HXR/microwave flare peak.
- Estimating the energy partition between flare and CME by phase.
- Setting up a flux-rope eruption model with phased boundary forcing.

Do NOT use this skill for purely gradual / failed-eruption CMEs whose
kinematics never show an impulsive phase.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Three-Phase CME Kinematic Profile (representative:
  Zhang & Dere 2006; Bein+ 2011; Vrsnak+ 2007).
- **Year:** TODO verify
- **Venue:** ApJ — TODO verify

### Claim (narrow form)

Most impulsive CMEs follow a three-phase height-time profile:
(i) slow rise with `a ≲ a_slow`, (ii) impulsive acceleration with
`a` peaking at `a_peak ~ 100–10000 m/s²`, (iii) post-acceleration
propagation with near-constant or weakly decelerating velocity. The
impulsive acceleration peak overlaps in time with the flare's
HXR/microwave impulsive peak within `~5–10 minutes`.

### Method assumptions

- The CME's leading edge can be tracked monotonically across viewpoints.
- The three-phase decomposition is morphological, not derived from a
  force balance.
- Time resolution is fine enough to resolve the impulsive phase
  (~minutes).

### Data assumptions

- High-cadence coronagraph or EUV imagery covering the eruption
  onset.
- Flare HXR/microwave time profile (RHESSI/STIX/GOES/Nobeyama) for
  alignment.

### Failure modes (skill memory)

- **Cadence undersampling.** LASCO C2 cadence misses fast impulsive
  phases entirely.
- **Mixed CMEs.** Two overlapping events conflate two impulsive
  peaks.
- **Phase-boundary ambiguity.** The transition between phases is
  fit-dependent; report uncertainty in `(t_slow→imp, t_imp→prop)`.
- **HXR-impulse / a-peak misalignment** can be a real physical
  result, not a data artifact — do NOT auto-correct it.

### Figure / numerical targets

- TODO verify: peak acceleration vs. flare HXR-peak time correlation
  coefficient (Zhang & Dere 2006 reports `~0.6–0.8`).

### Claim boundary

**In scope.** Impulsive CMEs with clear three-phase morphology in
EUV+coronagraph imagery.

**Out of scope — do NOT generalize:**

- Do NOT impose the three-phase profile on gradual / streamer-blowout
  CMEs.
- Do NOT use phase boundaries as MHD-derived flow features without
  independent confirmation.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `imagery.fetch_aia()`                 | EUV onset                        |
| `imagery.fetch_lasco()`               | coronagraph propagation          |
| `kinematics.height_time_extract()`    | leading-edge `h(t)`              |
| `kinematics.derive_velocity_accel()`  | smooth/derivative                |
| `kinematics.fit_three_phase()`        | piecewise fit + phase boundaries |
| `flare.fetch_hxr_timeprofile()`       | RHESSI/STIX                      |
| `metrics.timing_correlation()`        | a-peak vs HXR-peak lag           |

### Procedure

1. **Track** the CME leading edge in EUV (onset) and coronagraph
   (propagation).
2. **Smooth** and **differentiate** `h(t) → v(t) → a(t)`.
3. **Fit** a three-phase model with explicit `(t_1, t_2)` phase
   boundaries.
4. **Cross-correlate** `a_peak` time with flare HXR peak time.
5. **Emit** `(a_peak, t_peak, phase boundaries, HXR lag)`.

### Validation target

- **Metric:** TODO verify — `a-peak / HXR-peak` lag distribution
  consistent with Zhang & Dere 2006.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python runtime can bind `kinematics.derive_velocity_accel` to a
  Savitzky-Golay derivative; `kinematics.fit_three_phase` to a
  piecewise-affine fit on log-h.

---

## Layer 4 — Research-generation affordances

- **Gap:** few studies join the three-phase profile with the in-situ
  flux-rope size at 1 au — pairing with
  `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]`
  could connect impulsive `a_peak` to flux-rope volume.
- **Tension:** STIX HXR peak times in
  `[[paper-microflare-stix-nonthermal-electron-spectra]]` sometimes
  precede the EUV impulsive peak — re-examine on Solar Orbiter
  conjunctions.
- **Hypothesis:** `a_peak` correlates more tightly with the
  pre-eruption decay index than with flare power.

---

## Skill graph → depends_on

- `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
