---
name: paper-helioseismic-farside-detection-acoustic-holography
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-helioseismic-farside-detection-acoustic-holography

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when **detecting farside active regions** via
helioseismic acoustic holography (GONG / HMI), to complement AI-based
farside reconstruction.

## Layer 1 — Scientific invariant

- **Paper identity:** Acoustic-Holography Farside Active-Region
  Detection (representative: Lindsey & Braun 2000; Liewer+ 2014).
- **Year:** TODO verify.
- **Venue:** Science / Sol. Phys. — TODO verify.

### Claim (narrow form)

Phase-shift maps from helioseismic acoustic holography identify
strong farside ARs with **detection probability `~80%`** for
`|B| ≳ 500 G` complexes; spatial localization is `~5–10°` heliographic.

### Method assumptions

- Phase-shift inversion of Doppler signals.
- AR strength above the detection threshold.
- Carrington time-averaging of multiple measurement windows.

### Failure modes (skill memory)

- **Weak/diffuse farside flux** below detection threshold.
- **Edge effects** near limb-of-detection are noisy.
- **Phase wrapping** in long-window inversions.

### Claim boundary

**In scope.** Strong farside ARs (`|B| ≳ 500 G`) within the
acoustic-holography detection window.

**Out of scope.** Do NOT use to claim a quantitative farside Br
map; phase shift is a strength proxy, not a calibrated flux.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `helioseismology.fetch_dopplergrams()`  | GONG / HMI Doppler       |
| `holography.invert_phase_shift()`       | farside phase map        |
| `detection.farside_ar()`                | AR catalog               |
| `metrics.detection_vs_earthside()`      | predicted-vs-emerged AR  |

### Procedure

1. Fetch Doppler series; build phase-shift inversion.
2. Detect farside ARs and tabulate.
3. Cross-reference with later Earthside emergence.

### Validation target

TODO verify — `> 80%` of strong ARs detected.

## Layer 3 — Adapter / runtime notes (optional examples)

- NSO / GONG and Stanford / HMI farside data products are reference
  adapters.

## Layer 4 — Research-generation affordances

- **Gap:** acoustic holography and AI farside
  (`[[paper-ai-farside-synchronic-coronal-field-extrapolation]]`) have
  not been quantitatively combined into a single farside Br
  estimator.
- **Hypothesis:** combining the two would reduce open-flux problem
  discrepancy in
  `[[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]`.

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
