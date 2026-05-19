---
name: paper-sioulas-sw-scanner-js-segmentation
description: >-
  Use when an agent needs to segment a solar-wind time series into regimes
  using Jensen-Shannon-divergence scalograms (multiscale change-point
  detection) — central claim is that sw-scanner implements the JS-scalogram
  segmentation method used by Sioulas and collaborators for solar-wind regime
  classification (software package backing Sioulas et al. solar-wind
  segmentation work; HelioSI reproduction target).
version: 0.1.0
kind: paper-skill
quality: method-ready
paper:
  title: "sw-scanner: solar-wind regime segmentation via Jensen-Shannon-divergence scalograms"
  first_author: "Sioulas, N."
  year: 2023
  venue: "software package (companion to Sioulas et al. solar-wind segmentation papers; HelioSI reproduction context)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_wind_segmentation
  secondary_themes: ["turbulence", "psp_data"]
  missions: ["PSP", "Solar Orbiter", "Wind", "ACE"]
  regime: ["inner-heliosphere", "1au"]
trigger_keywords:
  - "sw-scanner"
  - "Jensen-Shannon divergence"
  - "JS divergence"
  - "scalogram"
  - "solar wind segmentation"
  - "regime classification"
  - "change-point detection"
  - "wavelet scalogram"
  - "Sioulas"
data_products:
  - instrument: "PSP/FIELDS MAG L2"
    level: "L2"
    cadence: "4 Sa/cyc"
    interval: null
    archive: "SPDF / PSP SOC"
  - instrument: "PSP/SWEAP SPC or SPAN-I"
    level: "L2"
    cadence: "0.2 Hz"
    interval: null
    archive: "SPDF"
algorithms:
  - name: "JS-divergence scalogram"
    equation_refs: ["D_JS(P||Q) = 0.5 * KL(P||M) + 0.5 * KL(Q||M), M = 0.5(P+Q)"]
    external_implementations:
      - "https://github.com/nicosioulas/sw-scanner"
  - name: "Multiscale change-point segmentation"
    equation_refs: []
    external_implementations:
      - "https://github.com/nicosioulas/sw-scanner"
validation_target:
  claim: "sw-scanner reproduces JS-scalogram segmentation panels from Sioulas et al. solar-wind regime papers"
  metric: "JS-divergence scalogram intensity (color-scale) and identified regime boundaries on a published PSP encounter"
  tolerance: "regime boundaries within ±1 wavelet scale + ±1 minute in time"
  reference_figure: "Sioulas et al. PSP scalogram figures (TODO verify per-paper figure IDs)"
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/nicosioulas/sw-scanner"
  data_repo: null
claim_boundary:
  scope: >-
    sw-scanner computes Jensen-Shannon-divergence scalograms for a chosen
    multivariate solar-wind time series (typically |B|, B_components,
    plasma moments) at multiple scales and emits scalogram + segmentation
    artifacts. It is the canonical implementation used in the HelioSI
    reproduction pipeline.
  out_of_scope:
    - "Do not interpret a JS-scalogram boundary as a physical discontinuity without independent verification (composition / electron strahl / plasma moments)."
    - "Do not treat the scalogram threshold as universal; thresholds are tuned per encounter and per instrument cadence."
    - "Do not use sw-scanner outputs to claim turbulence-cascade properties directly — those need separate paper-skills."
failure_modes:
  - "Histogram-bin choice for JS divergence matters; too few bins underflows D_JS, too many overestimates noise. Always sweep."
  - "Mixed cadence inputs (e.g., 4 Sa/cyc MAG + 0.2 Hz SPC) must be resampled consistently before scalogram."
  - "Data gaps produce spurious high-divergence segments; mask gaps before scoring."
  - "Window length controls the smallest detectable transition; document window size with every output."
  - "Co-rotating vs spacecraft frame: scalograms in raw timestamps confound spatial vs temporal structure."
  - "Color-scale choice changes which structures are visually salient; report quantitative thresholds, not just plots."
depends_on:
  - paper-pyspedas-multimission-data-access
  - paper-cdflib-cdf-reader
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: ".library/custom/heliophysics-skills/sub-skills/github-repos.md (sw-scanner entry); .library/custom/heliophysics-skills/SKILL.md (segmentation row); sioulas-reproduction/results/github_repos/consolidated_repos.json (sw-scanner entry)"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "segmentation", "infrastructure"]
source_type: software-package
---

# sw-scanner — paper-skill

> Compiled from the sw-scanner software package
> (https://github.com/nicosioulas/sw-scanner) and local references in
> `.library/custom/heliophysics-skills/SKILL.md` (segmentation row) and
> `sub-skills/github-repos.md`. **Quality tier**: `method-ready` —
> workflow specified; promotion to `executable` requires running on a
> cached PSP encounter and reproducing a published scalogram panel.

---

## 1. Trigger

Reach for this skill when:

- A workflow needs to **segment** a solar-wind interval into regimes
  (e.g., switchback patches, streamer-belt vs coronal-hole boundaries).
- An agent is reproducing a Sioulas-style JS-scalogram figure.
- A reasoning agent must choose between sw-scanner and a generic
  change-point library — sw-scanner is the multivariate JS-divergence
  variant used in the HelioSI reproduction.

Do NOT use this skill when:

- The task is *spectral* turbulence analysis (PSD, structure functions);
  use the relevant turbulence paper-skills.
- The task is supervised ML classification (use Camporeale-style ML
  classifiers).

## 2. Paper claim → verifiable task

**Claim (narrow form).** sw-scanner computes JS-divergence scalograms
across scales for multivariate solar-wind time series and produces
segmentation boundaries used in published Sioulas et al. work.

**Verifiable task.** Reproduction succeeds when an agent:

1. Loads a known PSP encounter window via pySPEDAS / cdflib.
2. Runs sw-scanner with declared window and bin parameters.
3. Saves the scalogram figure and segmentation boundary list.
4. Compares against a reference panel within tolerance.

## 3. Methods / equations → executable workflow

### JS-divergence scalogram

- Reference: Sioulas et al. solar-wind segmentation work; sw-scanner repo.
- Equation: for two adjacent windows with empirical distributions `P`,
  `Q`, `D_JS(P||Q) = 0.5 KL(P||M) + 0.5 KL(Q||M)` with `M = 0.5(P+Q)`.
- Procedure:
  1. Choose multivariate features (e.g., `|B|`, `B_R`, `B_T`, `B_N`,
     `n_p`, `v_R`).
  2. Choose window length `W` and number of bins `n_b`.
  3. For each scale `s` and each time `t`, compute `D_JS` between left
     and right windows of length `s` centered at `t`.
  4. Plot `D_JS(s, t)` as a scalogram.

### Multiscale change-point segmentation

- Procedure:
  1. Threshold `D_JS(s, t) > τ(s)`.
  2. Aggregate across scales to produce boundary timestamps.
  3. Optionally cluster boundaries within ε to deduplicate.

```python
# Conceptual outline; see sw-scanner repo for canonical API.
from sw_scanner import JSScalogram
js = JSScalogram(features, window=W, bins=n_b)
js.fit(time, data)
fig = js.plot()
boundaries = js.segments(threshold=tau)
```

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Archive | Fetch hint |
|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | 4 Sa/cyc | SPDF | pySPEDAS `psp.fields(datatype="mag_rtn_4_sa_per_cyc")` |
| PSP/SWEAP SPC | L2 | 0.2 Hz | SPDF | pySPEDAS `psp.spc(...)` |
| PSP/SWEAP SPAN-I | L2 | 0.2 Hz | SPDF | pySPEDAS `psp.spi(...)` |

## 5. Validation target → benchmark artifact

- **Claim**: sw-scanner reproduces JS-scalogram from a chosen Sioulas et
  al. paper panel.
- **Metric**: visual + quantitative match — boundary timestamps from
  thresholding `D_JS` agree with published boundaries.
- **Tolerance**: ±1 wavelet scale + ±1 minute in time.
- **Reference figure**: TODO verify per-paper (e.g., Sioulas 2023 anisotropic
  scaling, Sioulas et al. 2022 segmentation).

## 6. Failure modes → skill memory

- **Histogram-bin sensitivity** — `D_JS` is sensitive to `n_b`; sweep.
- **Cadence harmonization** — multivariate inputs must share a common
  cadence; resample carefully (median per bin for moments, decimation
  for MAG).
- **Data-gap artifacts** — masked / interpolated gaps produce spurious
  high `D_JS`. Mask before fitting.
- **Window length** — too small → noisy; too large → missed boundaries.
- **Spacecraft-frame vs co-rotating** — boundaries in raw spacecraft
  time mix radial transit and intrinsic structure.
- **Threshold choice** — `τ(s)` should be data-driven (per-scale
  percentile), not global.

## 7. Claim boundary

**In scope.** Multiscale JS-divergence segmentation of multivariate
solar-wind time series; publication-style scalogram visualization.

**Out of scope — do NOT generalize beyond:**

- Not a physical-discontinuity classifier; boundaries need cross-validation
  with composition / strahl / plasma criteria.
- Not a turbulence-spectrum tool.
- Not an ML classifier with training/test splits.

## 8. Links

- DOI: n/a (software repo)
- arXiv: n/a (no dedicated software paper located locally)
- ADS: n/a
- Code: https://github.com/nicosioulas/sw-scanner
- Data: n/a

## 9. Skill graph → depends_on

- `[[paper-pyspedas-multimission-data-access]]` — typical data loader
  upstream.
- `[[paper-cdflib-cdf-reader]]` — minimal CDF read path.

## Notes

- sw-scanner is the **HelioSI reproduction substrate** for solar-wind
  segmentation (see `.library/custom/heliophysics-skills/SKILL.md`
  segmentation row); promotion of this skill is high priority for the
  Sioulas-reproduction track.
- Local source notes that sw-scanner has been used by 5+ recent papers;
  enumerate during `executable` promotion.
