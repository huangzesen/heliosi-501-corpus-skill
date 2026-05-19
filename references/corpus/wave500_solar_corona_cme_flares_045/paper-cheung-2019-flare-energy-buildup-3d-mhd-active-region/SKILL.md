---
name: paper-cheung-2019-flare-energy-buildup-3d-mhd-active-region
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-cheung-2019-flare-energy-buildup-3d-mhd-active-region

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when the workflow needs a **3-D radiative MHD
simulation** to track the energy build-up of an active-region from the
photosphere through the corona, and the user wants to compare simulated
flare-related observables (free magnetic energy, EUV emission, X-ray
output) to observations.

Concrete symptoms:

- Estimating how much free magnetic energy is stored prior to a flare.
- Predicting EUV emission from a self-consistent 3-D MHD output.
- Reproducing an observed flare onset in a controlled numerical
  experiment.

Do NOT use this skill for analytic / 2-D analyses where the cost of a
3-D radiative MHD run is unjustified.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Comprehensive Three-Dimensional Radiative MHD Simulation
  of a Solar Flare (representative: Cheung et al. 2019, Nature
  Astronomy).
- **First author:** M. C. M. Cheung
- **Year:** 2019
- **Venue:** Nature Astronomy — TODO verify

### Claim (narrow form)

A single self-consistent 3-D radiative MHD simulation of an active
region — driven by realistic photospheric flux emergence — produces
flare-like reconnection events that reproduce a suite of observed
EUV, UV, and HXR signatures simultaneously. The narrow claim is that
the simulated pre-flare free magnetic energy and the simulated
EUV light curves are within stated agreement of the observed
analog event.

### Method assumptions

- The MURaM (or equivalent) radiative MHD code is run with realistic
  opacity and conduction.
- Photospheric boundary forcing comes from a flux-emergence model or a
  data-driven prescription.
- Radiative transfer in lines is computed in LTE / non-LTE where
  appropriate.

### Data assumptions

- Photospheric magnetograms for boundary forcing or comparison.
- Observed EUV / UV / HXR time profiles for the analog event.

### Failure modes (skill memory)

- **Numerical reconnection rate** can dominate the simulated flare
  timing if resolution is insufficient.
- **Boundary forcing prescription** is the single largest free parameter
  in the simulation.
- **Sub-grid heating / radiative losses** affect the EUV brightness
  far more than the dynamics of reconnection itself.
- **Comparison is statistical, not deterministic.** Do NOT claim the
  simulation "is" the observed flare.

### Figure / numerical targets

- TODO verify: pre-flare free magnetic energy and EUV light-curve
  shape consistent with the observed event.

### Claim boundary

**In scope.** 3-D radiative MHD simulation of one active-region's
flare cycle and statistical agreement with the observed analog.

**Out of scope — do NOT generalize:**

- Do NOT extract universal flare-onset criteria from a single
  simulation.
- Do NOT use the simulation as ground truth for individual
  reconnection events.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `mhd.radiative_setup_active_region()` | initialize stratified atmosphere |
| `mhd.boundary_driven_flux_emergence()`| photospheric forcing             |
| `mhd.run_3d()`                        | integrate MHD + radiation        |
| `diagnostics.synthesize_euv()`        | forward-model AIA channels       |
| `diagnostics.synthesize_hxr()`        | nonthermal output                |
| `metrics.observation_match()`         | compare to AIA / RHESSI          |
| `analysis.free_magnetic_energy()`     | volume-integrated E_free         |

### Procedure

1. **Initialize** a stratified atmosphere with embedded magnetic
   structure.
2. **Drive** the photospheric boundary with an emergence prescription.
3. **Integrate** until a reconnection event occurs.
4. **Synthesize** EUV/HXR observables from the simulation cube.
5. **Compare** to the analog observation.
6. **Report** free-energy time series and observable agreement.

### Validation target

- **Metric:** TODO verify — synthesized EUV light-curve shape
  agreement with observation (e.g. cross-correlation > 0.8).

---

## Layer 3 — Adapter / runtime notes (optional examples)

- The published reference adapter is MURaM (the SDO-MURaM
  flare-resolving branch).
- Synthesis: `chiantipy` for AIA temperature responses.

---

## Layer 4 — Research-generation affordances

- **Gap:** ensemble runs varying only the boundary-forcing
  prescription are missing — they would isolate the boundary as the
  dominant source of variability.
- **Tension:** the predicted ribbon timing sometimes lags
  `[[paper-flare-ribbon-photospheric-magnetic-shear]]`-derived
  reconnection rate by a fraction of the impulsive phase.
- **Hypothesis:** sub-grid Alfvén-wave heating
  (`[[paper-coronal-mhd-alfven-wave-poynting-flux-base]]`) reduces
  the simulated EUV peak ratio between 211 Å and 335 Å.

---

## Skill graph → depends_on

- `[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`
- `[[paper-titov-demoulin-2014-flux-rope-insertion-eruption]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
