---
name: paper-so-phi-hrt-vector-magnetogram-radial-distance
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-so-phi-hrt-vector-magnetogram-radial-distance

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when working with **Solar Orbiter SO/PHI HRT
vector magnetograms** taken at heliocentric distances `0.3–0.5 au`,
where stray light and orbital geometry alter the effective inversion
chain relative to HMI.

## Layer 1 — Scientific invariant

- **Paper identity:** SO/PHI HRT Vector Magnetogram at Variable
  Heliocentric Distance (representative: Solanki+ 2020;
  Sinjan+ 2026; del Toro Iniesta+ 2017).
- **Year:** TODO verify.
- **Venue:** A&A — TODO verify.

### Claim (narrow form)

After stray-light deconvolution and on-board MILOS inversion, SO/PHI
HRT delivers per-pixel vector magnetograms with sensitivity
comparable to HMI in strong-field regions; quiet-Sun sensitivity
varies with heliocentric distance and exposure budget.

### Method assumptions

- On-board / ground MILOS inversion of Fe I 6173 Å.
- Stray-light PSF measured in flight.
- Solar Orbiter ephemeris is precisely known.

### Failure modes (skill memory)

- **Stray-light correction** is the largest systematic at small
  heliocentric distance.
- **Pointing jitter** affects fine-scale features.
- **On-board compression** can lose Stokes-V tail amplitude.

### Claim boundary

**In scope.** SO/PHI HRT during Solar Orbiter encounters
0.3–0.5 au; strong-field AR cores.

**Out of scope.** Do NOT generalize to FDT data products or to
non-AR quiet Sun without separate calibration.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `vector_mag.fetch_so_phi_hrt_l2()`      | L2 product               |
| `image.straylight_deconvolve()`         | PSF correction           |
| `vector_mag.invert_milos()`             | Stokes → B               |
| `metrics.compare_to_hmi()`              | conjunction baseline     |

### Procedure

1. Fetch SO/PHI HRT L2 over an encounter window.
2. Apply stray-light PSF deconvolution if not yet done.
3. (Re-)invert via MILOS if Stokes profiles are available.
4. Cross-compare to HMI during an Earth-Sun-line viewing.

### Validation target

TODO verify — `B_los` agreement with HMI within calibration
tolerance.

## Layer 3 — Adapter / runtime notes (optional examples)

- `sophi-tools` Python package; ESA Solar Orbiter Archive.

## Layer 4 — Research-generation affordances

- **Gap:** the cross-calibration of SO/PHI HRT vs SO/PHI FDT vs HMI
  is incomplete and varies with orbit — schedule a campaign.
- **Hypothesis:** SO/PHI HRT enables radial-distance-resolved
  source-mapping for `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]`
  when PSP–SO are in conjunction.

## Skill graph → depends_on

- `[[paper-hmi-vector-magnetogram-disambiguation-acute-angle]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
