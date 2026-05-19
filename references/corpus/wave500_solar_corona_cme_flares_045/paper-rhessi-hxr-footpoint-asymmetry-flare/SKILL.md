---
name: paper-rhessi-hxr-footpoint-asymmetry-flare
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-rhessi-hxr-footpoint-asymmetry-flare

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when a two-footpoint flare's **HXR brightness
asymmetry** must be interpreted in terms of asymmetric magnetic
mirroring / magnetic-bottle return current.

## Layer 1 — Scientific invariant

- **Paper identity:** HXR Footpoint Asymmetry as a Magnetic-Mirror
  Diagnostic (representative: Saint-Hilaire+ 2008; Battaglia +
  Benz 2007).
- **Year:** TODO verify.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

Two-footpoint flares observed by RHESSI show HXR brightness ratios
typically `< 5` between footpoints; the brightness ratio scales
inversely with the **photospheric magnetic-field strength ratio**
at the footpoints, consistent with asymmetric magnetic-mirror
trapping.

### Method assumptions

- Footpoint identification in 25–100 keV CLEAN images.
- LOS magnetogram at footpoint positions.
- Thick-target injection assumption.

### Failure modes (skill memory)

- **Photospheric-vs-corona footpoint mismatch.** The mirror ratio
  matters at the corona base, not at z=0.
- **CLEAN sidelobes** can bias the dimmer footpoint.
- **Single-footpoint flares** are excluded by definition.

### Claim boundary

**In scope.** Two-footpoint impulsive flares observed by RHESSI in
25–100 keV.

**Out of scope.** Do NOT generalize to ribbons or to STIX microflares
without instrument-specific re-calibration.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `imagery.fetch_rhessi()`                | RHESSI L1                |
| `imagery.clean_image()`                 | CLEAN reconstruction     |
| `footpoint.identify_pair()`             | two-footpoint matching   |
| `magnetogram.sample_at_position()`      | photospheric B at footp. |
| `metrics.asymmetry_vs_mirror()`         | brightness vs B ratio    |

### Procedure

1. Fetch RHESSI L1; reconstruct CLEAN image at flare peak.
2. Identify two HXR footpoints.
3. Sample LOS B at each footpoint.
4. Compute brightness ratio and B ratio; correlate across event
   sample.

### Validation target

TODO verify — reproduce the published brightness-vs-B-ratio relation.

## Layer 3 — Adapter / runtime notes (optional examples)

- IDL/SolarSoft `hessi_clean` and OSPEX is the historical adapter.
- Modern Python options: `sunkit-instruments` for RHESSI counts.

## Layer 4 — Research-generation affordances

- **Gap:** STIX-era equivalent of the same diagnostic is incomplete
  — pair with `[[paper-microflare-stix-nonthermal-electron-spectra]]`
  and `[[paper-rhessi-hxr-footpoint-asymmetry-flare]]`.
- **Hypothesis:** footpoint asymmetry correlates with NLFFF-derived
  twist
  (`[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`).

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
