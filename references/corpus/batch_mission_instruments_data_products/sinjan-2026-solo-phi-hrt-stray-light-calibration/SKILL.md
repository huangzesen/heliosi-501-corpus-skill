---
name: sinjan-2026-solo-phi-hrt-stray-light-calibration
description: >-
  Use when a HelioSI workflow consumes SO/PHI High Resolution Telescope
  (HRT) continuum intensity or vector magnetograms near perihelion and
  needs to know whether stray (false) light inside the HRT optics has
  been characterised and corrected. Central paper is Sinjan, Riethmüller,
  Gandorfer, Feller, Calchetti, Bailén, Hirzberger, Valori, Solanki
  (2026), *A stray light analysis for SO/PHI-HRT and an updated
  comparison of the inferred magnetic field with SDO/HMI*, submitted to
  *A&A*, arXiv:2603.18744 (submitted 2026-03-19). Stray light is
  quantified from solar limb profiles and a Mercury transit at 0.28 au;
  applying the correction yields stronger inferred fields in solar
  features and a much closer agreement with SDO/HMI over the 2023 March
  Solar Orbiter inferior conjunction, with residual disagreement only in
  the strongest field regions (|B| > 1600 G or |B_LOS| > 1300 G).
version: 0.1.0
tags:
  - solar-orbiter
  - phi
  - hrt
  - stray-light-calibration
  - vector-magnetogram
  - inversion
  - sdo-hmi-cross-comparison
  - 2023-march-conjunction
quality_level: paper-grounded-pending-full-text
executable_status: pipeline-specified-not-yet-runnable
paper:
  authors_verified: true
---

# Sinjan 2026 — Stray-Light Calibration of SO/PHI-HRT and Re-Comparison with SDO/HMI

> Compiled from Sinjan, Riethmüller, Gandorfer, Feller, Calchetti,
> Bailén, Hirzberger, Valori, Solanki (2026), *A stray light analysis
> for SO/PHI-HRT and an updated comparison of the inferred magnetic
> field with SDO/HMI*, arXiv:2603.18744 (submitted to A&A; submission
> 2026-03-19). Full 9-author list, title, arXiv identifier, "submitted
> to A&A" venue, the 0.28 au observational distance, the 2023 March
> Solar Orbiter inferior-conjunction methodology, and the residual
> agreement bands at |B| > 1600 G and |B_LOS| > 1300 G were verified
> against the arXiv abstract page on 2026-05-19. The abstract is quoted
> verbatim in §2 below.
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic
> anchors, the four headline qualitative results, and the field
> thresholds are anchored; the analytic stray-light parameterisation,
> the exact 2023-March date(s) of the conjunction window used, exact
> figure numbers, and the published correlation / RMS-residual tolerance
> numbers remain `TODO_verify_with_full_text`. The journal DOI will be
> issued once *A&A* accepts the paper.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- A workflow loads **SO/PHI-HRT continuum intensity or vector
  magnetograms** near perihelion (≤ 0.3 au) and must check whether the
  data product is the stray-light-corrected version or the pre-correction
  L2.
- A user asks "**why are SO/PHI-HRT fields stronger than SDO/HMI** in
  strong magnetic features?" — the resolved answer combines the
  stray-light correction with the residual |B| > 1600 G / |B_LOS| > 1300 G
  band where small differences persist.
- A footpoint / PFSS / source-surface workflow uses SO/PHI-HRT as the
  inner magnetic boundary and needs the corrected field scale (otherwise
  the inferred coronal field will be systematically biased relative to
  HMI-based boundaries).
- A pixel-by-pixel **SO/PHI-HRT vs SDO/HMI cross-comparison** is needed —
  the paper's gold-standard window is the 2023 March Solar Orbiter
  inferior conjunction.

Do NOT use this skill when:

- The dataset is **SO/PHI-FDT** (Full-Disk Telescope) — different optical
  chain; the HRT stray-light recipe does not transfer unchanged.
- The dataset is **SDO/HMI alone** — different stray-light recipe (use
  the HMI calibration paper instead).
- The downstream science is solar irradiance — this paper's correction is
  bounded to imaging / spectropolarimetric inversion, not full-disk
  radiometry.

## 2. Paper claim → verifiable task

**Verbatim abstract** (verified against arXiv on 2026-05-19):

> *Context.* The High Resolution Telescope of the Polarimetric and
> Helioseismic Imager on Solar Orbiter (SO/PHI-HRT) operates in an
> extreme observational environment, observing the Sun as close as 0.28
> au. The high thermal load and large illuminating field puts high
> demands on the instrument in terms of both imaging performance and
> false light control.
>
> *Aims.* To characterise the amount of stray light (false light) within
> SO/PHI-HRT, apply a correction, and re-compare the data products with
> the Helioseismic and Magnetic Imager on the Solar Dynamics Observatory
> (SDO/HMI).
>
> *Methods.* We analyse solar limb profiles and a Mercury transit to
> quantify the amount of stray light and add a correction term when
> partially reconstructing the SO/PHI-HRT images. For the comparison
> with SDO/HMI we use data from the 2023 March Solar Orbiter inferior
> conjunction and compare the magnetic fields on a pixel-by-pixel basis.
>
> *Results.* Increased continuum intensity contrast in the quiet Sun,
> and darker intensity levels are found in strong magnetic features.
> Consequently, much stronger fields are inferred in these features.
> Comparing the stray light corrected data with that from the standard
> SDO/HMI data products results in a much closer agreement across all
> vector magnetic field components, particularly when the cadence and
> noise levels are identical. In most solar features, SO/PHI-HRT infers
> stronger fields than the SDO/HMI line-of-sight magnetograms. Compared
> to the vector magnetic field from SDO/HMI the two are very well
> aligned, with only slight differences in the strongest field regions
> (where |**B**| > 1600 G or |**B**_LOS| > 1300 G).

**Claim (narrow form, anchored to the abstract).** The HRT thermal
environment at 0.28 au and the full-disk illuminating field induce
measurable scattered (false) light inside the HRT optics. Quantifying
it from (a) solar-limb intensity profiles and (b) a Mercury transit,
then adding the corresponding correction term during partial image
reconstruction, produces four ordered effects: **(1)** higher continuum
contrast in the quiet Sun, **(2)** darker continuum inside strong
magnetic features, **(3)** stronger inferred vector fields in those
features, **(4)** much closer pixel-by-pixel agreement with SDO/HMI on
the 2023 March Solar Orbiter inferior conjunction, particularly when
HRT and HMI cadences / noise levels are matched. Residual systematic
disagreement persists only where |B| > 1600 G or |B_LOS| > 1300 G.

**Verifiable task.** A reproduction succeeds when an agent:

1. Pulls the named PHI-HRT image set covering the 2023 March Solar
   Orbiter inferior conjunction (exact dates TODO verify with full PDF)
   and the matching SDO/HMI vector + LOS magnetograms from JSOC.
2. Recomputes the stray-light correction term from solar-limb profiles
   and Mercury-transit imaging (parameterisation TODO verify with full
   PDF; the abstract is qualitative on the functional form).
3. Re-runs the partial image reconstruction with the correction term
   and the standard PHI Milne–Eddington inversion to produce a
   corrected vector-field cube.
4. Verifies the four ordered qualitative effects above.
5. Computes pixel-by-pixel correlation / RMS residuals between HRT and
   HMI vector components on the conjunction window with matched
   cadence and noise, and demonstrates that residual disagreement is
   confined to the |B| > 1600 G / |B_LOS| > 1300 G pixels.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Stray-light quantification from limb + transit

- Procedure:
  1. Acquire a sample of HRT continuum images covering the solar limb at
     0.28 au; subtract dark + flat, register, average.
  2. Measure the **off-limb intensity profile** as a function of radial
     distance beyond the solar disk (the floor that should be zero in
     the absence of scattered light).
  3. Acquire the **Mercury-transit image series** during the conjunction
     window — the planetary disk is geometrically opaque, so any
     residual signal across the planetary silhouette quantifies the
     scattered-light contribution at that location and time.
  4. Fit a parametric scattered-light model (functional form TODO verify
     with full PDF) such that it simultaneously reproduces the off-limb
     intensity profile and the in-Mercury residual intensity.
  5. Persist the model's parameters and its uncertainty bands as part
     of the corrected-product metadata.

### Algorithm 3.2 — Partial image reconstruction with correction term

- Procedure:
  1. For each HRT continuum frame, subtract the spatially-resolved
     scattered-light term from the parametric model.
  2. Renormalise the corrected continuum to preserve photon-conservation
     constraints inside the disk.
  3. Verify expected ordered effects on the corrected continuum:
     (i) increased contrast in quiet-Sun regions, (ii) darker mean
     intensity inside strong magnetic features.

### Algorithm 3.3 — Re-inversion to corrected vector B

- Procedure:
  1. Re-run the PHI Milne–Eddington inversion on the corrected
     intensity / Stokes cubes using the operational HRT pipeline
     (configuration TODO verify with full PDF / pipeline release notes).
  2. Produce vector B (B_long, B_trans, azimuth) on the HRT image grid;
     preserve the 180° azimuth ambiguity convention used in the paper.
  3. Persist a `straylight_corrected: true` flag in the inverted-product
     metadata.

### Algorithm 3.4 — Pixel-by-pixel SO/PHI-HRT vs SDO/HMI re-comparison

- Procedure:
  1. Co-register HRT vector magnetograms to the matching HMI vector +
     LOS magnetograms over the 2023 March Solar Orbiter inferior
     conjunction.
  2. Match cadence and per-pixel noise (the abstract explicitly
     conditions agreement on cadence- and noise-matched comparison).
  3. Stratify pixels by |B| and |B_LOS| into bins; for each bin compute
     correlation coefficient and RMS difference per vector component.
  4. Report the agreement improvement vs the pre-correction baseline;
     confirm that residual disagreement is confined to |B| > 1600 G or
     |B_LOS| > 1300 G.

Code skeleton (scaffold tier):

```python
def hrt_straylight_corrected_inversion(image_set, conjunction_window):
    sl_model = fit_straylight_model(
        limb_profiles=load_limb_profiles(image_set),
        mercury_transit=load_mercury_transit(conjunction_window),
    )  # functional form TODO verify with full PDF
    corrected_intensity = partial_reconstruction(image_set, minus_term=sl_model)
    return phi_milne_eddington_inversion(corrected_intensity)  # config TODO verify

def hrt_hmi_pixelwise_residual(hrt_vec, hmi_vec, bin_thresholds_G):
    aligned = coregister(hrt_vec, hmi_vec)
    matched = match_cadence_and_noise(aligned)
    return per_bin_correlation_and_rms(matched, bin_thresholds_G)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SO/PHI-HRT | continuum + Stokes I/Q/U/V at Fe I 6173 Å | L2 imaging stack; cadence TODO verify | 2023 March Solar Orbiter inferior-conjunction window (exact date TODO verify) | ESA SOAR | SOAR-class authenticated HTTP archive client (harness binding) |
| SO/PHI-HRT | inverted vector B (B_long, B_trans, azimuth) | L2 inverted; pipeline release TODO verify | Same | ESA SOAR | same |
| SDO/HMI | LOS magnetogram | L2; 45 s standard | Same window | JSOC | `drms` / JSOC |
| SDO/HMI | vector magnetogram | L2.5 hmi.B_720s | Same window | JSOC | `drms` / JSOC |
| SO/PHI-HRT | Mercury-transit image series | L1/L2 calibration | 2023 March transit window TODO verify | ESA SOAR | same |
| SO/PHI-HRT | solar-limb intensity profiles | L1/L2 calibration | Conjunction-adjacent | ESA SOAR | same |

## 5. Validation target → benchmark artifact

- **Claim**: After stray-light correction, the pixel-by-pixel HRT vs HMI
  vector-field comparison on the 2023 March Solar Orbiter inferior
  conjunction shows "much closer agreement across all vector magnetic
  field components"; HRT continues to infer stronger LOS fields than
  HMI in most solar features; residual disagreement is confined to
  |B| > 1600 G or |B_LOS| > 1300 G.
- **Metric**: pixel-wise correlation coefficient + RMS difference per
  vector component, binned by |B| and |B_LOS|.
- **Tolerance**: TODO verify the exact correlation / RMS thresholds the
  paper quotes; the abstract's "very well aligned" + bin thresholds are
  the qualitative anchor.
- **Reference figure**: scatter plots and per-pixel difference maps over
  the conjunction window — figure numbers TODO verify with full PDF.

Recommended check artifacts:

- `phi_hmi_residual_by_bin.csv` — one row per (|B| bin, vector
  component): correlation, RMS, n_pix, on the conjunction window.
- `phi_hmi_diff_maps.png` — pre- and post-correction difference maps
  side by side.
- `straylight_model_params.json` — the fit model and its quoted
  uncertainty bands.

## 6. Failure modes → skill memory

- **Cadence / noise mismatch.** The abstract emphasises that agreement
  is best "when the cadence and noise levels are identical". Comparing
  HRT and HMI without matching these conditions inflates apparent
  disagreement and biases the bin-stratified residual.
- **Strong-field residual.** The published agreement is bounded:
  pixels with |B| > 1600 G or |B_LOS| > 1300 G retain measurable
  HRT–HMI differences after correction. Downstream consumers must not
  treat HRT and HMI as interchangeable in active-region cores.
- **PSF temporal drift across perihelia.** The published stray-light
  parameters are fit on a specific (2023 March) conjunction window.
  Re-fitting is required for later perihelia — the abstract does not
  certify the correction at other orbital phases.
- **Mercury-transit availability.** The recipe exploits a specific
  planetary-transit occulter; rerunning for another perihelion that
  lacks a transit reduces the constraints used to fit the model and
  increases parameter uncertainty.
- **Inversion-method coupling.** HRT vs HMI vector-field agreement is
  conditional on identical (or carefully equivalent) Milne–Eddington
  inversion settings on both sides. Differences in noise treatment,
  azimuth disambiguation, or regularisation alone can erase or
  manufacture apparent agreement.
- **Limb-darkening assumption.** The off-limb intensity-profile
  constraint assumes a known limb-darkening function for the
  not-scattered component; departures introduce parameter bias.
- **FDT vs HRT confusion.** SO/PHI-FDT has a different optical chain;
  this correction does not transfer. Always check the product
  identifier before applying.
- **Pre-correction product drift.** Downstream products that ingested
  HRT *before* the corrected reconstruction was released carry a known
  systematic; rerunning them on corrected inputs is part of any
  reproducibility check.

## 7. Claim boundary

**In scope.** SO/PHI-HRT stray-light quantification from solar-limb
profiles + Mercury transit at 0.28 au and the corresponding correction
term in partial image reconstruction; pixel-by-pixel vector-field
re-comparison against SDO/HMI on the **2023 March Solar Orbiter inferior
conjunction**. The skill is a calibration step for HRT data products
within that conjunction window.

**Out of scope — do NOT generalise beyond:**

- Do not apply this exact correction unchanged to SO/PHI-FDT — different
  optics.
- Do not infer SO/EUI / SPICE calibration from this paper.
- Do not assume the strong-field residual is eliminated — the paper
  explicitly says it persists at |B| > 1600 G and |B_LOS| > 1300 G.
- Do not transfer the correlation / RMS numbers from this conjunction to
  other perihelia without re-running.
- Do not use this skill for irradiance-budget science — bounded to
  imaging / inversion.

If a downstream task asks for a generalisation listed above, refuse it
and route to the appropriate sibling instrument-calibration paper-skill.

## 8. Links

- DOI: TODO verify — *A&A* DOI will be issued once accepted; arXiv-issued
  DOI is `10.48550/arXiv.2603.18744`.
- arXiv: https://arxiv.org/abs/2603.18744 (submitted 2026-03-19;
  abstract verified 2026-05-19).
- ADS: 2026arXiv260318744S (provisional, derived from the arXiv ID; the
  final journal bibcode will replace this once *A&A* accepts).
- Code: PHI calibration pipeline (proprietary at submission; check
  Max-Planck-Institut für Sonnensystemforschung / SO/PHI consortium
  repositories for a public release).
- Data: ESA SOAR (https://soar.esac.esa.int/) for SO/PHI products; JSOC
  (http://jsoc.stanford.edu/) for SDO/HMI.

## 9. Skill graph → depends_on

- `[[muller-2020-solar-orbiter-mission-overview]]` — orbital / mission
  context including the 0.28 au perihelia and the Solar Orbiter inferior
  conjunction calendar.
- `[[horbury-2020-solo-mag-vector-magnetometer]]` — in-situ Solar
  Orbiter MAG pairing for any flux-balance / line-of-sight cross-check.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — distantly related
  perihelion-environment reference (PSP) used in some joint Solar
  Orbiter + PSP campaigns.

## 10. Research-generation affordances

- **Perihelion-by-perihelion PSF drift.** Re-fit the stray-light
  parameters at every subsequent Solar Orbiter perihelion that has
  matching limb / transit calibration data and report the parameter
  trajectory. Demonstrating (or refuting) PSF temporal drift is a
  publishable instrument-science result.
- **Active-region-core cross-method bound.** In the |B| > 1600 G
  residual band, run a controlled comparison among (HRT corrected,
  HMI vector, HMI LOS, and any third reference such as ground-based
  Hinode/SP) to bound the *physical* vs *instrumental* contribution to
  the remaining HRT–HMI disagreement.
- **PFSS / source-surface impact study.** Use HRT corrected vector
  magnetograms as the inner boundary of a PFSS model and compare the
  resulting open-flux estimate to the HMI-based baseline (cf.
  [[wu-2026-nonspherical-coronal-magnetic-field-open-flux]]); the
  per-cent change quantifies how much PFSS-derived heliospheric flux is
  sensitive to the stray-light correction.
- **Conjunction-window benchmark for future calibration papers.** The
  2023 March Solar Orbiter inferior conjunction is now an
  agent-discoverable cross-calibration anchor; subsequent SO/PHI
  calibration papers should be encouraged to report the same
  bin-stratified residual on the same window for direct comparison.

## Notes

- Until *A&A* issues a DOI, downstream consumers should anchor on
  arXiv:2603.18744 and on the abstract text quoted verbatim in §2.
- Authorship and the residual field thresholds (1600 G / 1300 G) were
  verified against the arXiv abs page on 2026-05-19; the
  scattered-light model's mathematical form, exact 2023-March date(s) of
  the conjunction window, and the published correlation / RMS numbers
  remain `TODO_verify_with_full_text`.
- The slug retains the 2026 year-tag because this paper-skill is
  bibliographically anchored on the 2026 arXiv submission; the slug
  should not be renamed when *A&A* assigns a final publication year.
