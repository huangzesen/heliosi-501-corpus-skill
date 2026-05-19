---
name: paper-coronal-mhd-alfven-wave-poynting-flux-base
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-coronal-mhd-alfven-wave-poynting-flux-base

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when the coronal-base **Alfvén-wave Poynting
flux** must be measured or specified for a wave-driven coronal MHD
model (AWSoM, ZEPHYR, or similar).

## Layer 1 — Scientific invariant

- **Paper identity:** Coronal-Base Alfvén-Wave Poynting Flux
  (representative: van der Holst+ 2014 AWSoM; Verdini & Velli 2007;
  Cranmer & van Ballegooijen 2005).
- **Year:** TODO verify.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

A photospheric-base outgoing Alfvén-wave Poynting flux of
`F_A0 ~ 10^5 erg cm^-2 s^-1`, partitioned among observed photospheric
motions, is consistent with chromospheric Doppler swaying and
matches the required heliospheric energy flux at 1 au within stated
agreement.

### Method assumptions

- Photospheric flow spectrum is known (Hinode SOT / SDO HMI).
- Wave propagation is WKB or weakly-turbulent.
- Frequency-dependent reflection at the transition region.

### Failure modes (skill memory)

- **Sub-resolution motions** can be missed if not properly extrapolated.
- **Single-frequency-mode assumptions** can over-/under-predict
  damping.

### Claim boundary

**In scope.** Quiet-Sun and CH base Poynting flux derivation for
wave-driven coronal models.

**Out of scope.** Do NOT use as ground truth for AR-base Poynting
flux.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_sdo_dopplergrams()`      | photospheric motion      |
| `spectro.power_spectrum_motion()`       | velocity PSD             |
| `mhd.alfven_wave_poynting_estimate()`   | F_A0                     |
| `metrics.compare_to_awsom_required()`   | model match              |

### Procedure

1. Estimate photospheric horizontal motions; build PSD.
2. Compute the Alfvén-wave Poynting flux estimate.
3. Compare to AWSoM-required base values.

### Validation target

TODO verify — F_A0 ~ 10^5 erg cm^-2 s^-1 within published bounds.

## Layer 3 — Adapter / runtime notes (optional examples)

- `sunpy` + `numpy` for power spectra; AWSoM `SWMF` for downstream.

## Layer 4 — Research-generation affordances

- **Gap:** SO/PHI dopplergrams at high cadence have not been used
  for F_A0 mapping vs HMI — pair with
  `[[paper-so-phi-hrt-vector-magnetogram-radial-distance]]`.
- **Hypothesis:** F_A0 spatial heterogeneity at the CH-edge
  predicts the slow-Alfvénic wind population in
  `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]`.

## Skill graph → depends_on

- `[[paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
