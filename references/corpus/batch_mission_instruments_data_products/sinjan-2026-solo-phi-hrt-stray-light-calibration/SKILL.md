---
name: sinjan-2026-solo-phi-hrt-stray-light-calibration
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# sinjan-2026-solo-phi-hrt-stray-light-calibration

## When to use this paper-skill

Invoke when a HelioSI workflow uses **SO/PHI-HRT magnetograms or continuum
intensity** and needs to know how stray light (false light) inside the
High Resolution Telescope biases inferred magnetic fields. The Sinjan
et al. 2026 paper provides the **stray-light correction recipe** and a
**SO/PHI-HRT vs SDO/HMI re-comparison** after correction.

Typical triggers:

- An agent loads PHI-HRT vector magnetograms and must apply (or check the
  presence of) stray-light correction.
- The user asks "why are PHI-HRT fields stronger than HMI in magnetic
  features?" — answer: PHI-HRT infers stronger fields in strong-field
  regions; after stray-light correction the agreement with HMI improves
  ([Mar 2023 conjunction]).
- A footpoint / PFSS workflow uses PHI-HRT magnetograms and needs to
  understand the corrected magnetic-field scale.

Do NOT invoke this skill when:

- The dataset is SO/PHI-FDT (Full-Disk Telescope) — different optics; this
  paper concerns HRT only.
- The dataset is SDO/HMI alone — different stray-light recipe.

## Paper identity and claim boundary

- **Title:** A stray light analysis for SO/PHI-HRT and an updated comparison
  of the inferred magnetic field with SDO/HMI
- **First author:** Jonas Sinjan
- **Authors:** J. Sinjan, T. L. Riethmüller, A. Gandorfer, A. Feller,
  D. Calchetti, ("+ co-authors per inventory abstract — TODO complete
  with full text")
- **Year:** 2026 (published 2026-03-19; inventory)
- **Venue:** TODO_verify_with_full_text (likely Astronomy & Astrophysics —
  TODO verify)
- **DOI:** TODO_verify_with_full_text
- **arXiv:** 2603.18744 (in local inventory
  `theme_solar_orbiter.json`).
- **Claim boundary:** Bounded to **SO/PHI-HRT** observations near
  perihelion 0.28 au, using the **2023 March inferior conjunction with
  SDO/HMI** for cross-comparison. The numerical comparisons (e.g. better
  alignment after correction; vector-field differences only in regions
  with |B|>1600 G or |B_LOS|>1300 G) are bounded to that conjunction.

## Scientific or methodological claim to operationalize

> The high thermal load and large illuminating field at perihelion induce
> measurable stray light inside SO/PHI-HRT. Quantifying the stray light
> via **solar-limb profiles and a Mercury transit** and applying a
> correction term during image reconstruction yields:
>
> 1. **Increased continuum-intensity contrast** in the quiet Sun,
> 2. **Darker intensity levels** inside strong magnetic features,
> 3. **Better pixel-by-pixel agreement** of the inferred magnetic field
>    with SDO/HMI during the 2023 March conjunction,
> 4. Residual differences only at the strongest fields (|B|>1600 G or
>    |B_LOS|>1300 G).
>
> PHI-HRT continues to infer stronger LOS fields than HMI line-of-sight
> magnetograms.

A HelioSI skill operationalizes this by: given a PHI-HRT product,
either (a) confirm that the corrected product version is loaded, or
(b) compute the stray-light correction following the paper's recipe.

## Required data / instruments / code / archives

- **SO/PHI-HRT L2 continuum + vector magnetograms** (SOAR products;
  exact name TODO verify with full text — likely
  `solo_L2_phi-hrt-*`).
- **SDO/HMI vector + LOS magnetograms** during the 2023 March inferior
  conjunction (JSOC).
- **Solar-limb profile data and Mercury-transit imaging** for stray-light
  quantification.
- **Code:** PHI calibration pipeline (proprietary at publication; check
  Max Planck Solar System Research PHI repos) + community tools (`sunpy`,
  `sunkit-image`).
- **Archives:** ESA SOAR; JSOC for HMI.

## Algorithm / workflow steps

1. **Quantify stray light** from solar-limb profiles (intensity beyond the
   limb) and Mercury transit (occulting body): determine PSF wings
   amplitude.
2. **Construct correction term** parameterizing scattered-light fraction
   (TODO derive exact form from full text).
3. **Apply correction** during partial image reconstruction of the L1 →
   L2 inversion stack.
4. **Verify continuum-intensity contrast** increases in quiet Sun and
   strong-feature intensities decrease.
5. **Re-derive inferred B** from the corrected images via the standard PHI
   Milne–Eddington inversion (or equivalent).
6. **Cross-compare** to SDO/HMI on the 2023 March conjunction pixel-by-
   pixel.

## Minimal executable benchmark or validation target

- **Claim:** After correction, PHI-HRT vector magnetic field agrees with
  HMI pixel-by-pixel "very well aligned" with only slight differences in
  |B|>1600 G or |B_LOS|>1300 G regions.
- **Metric:** Pixel-by-pixel correlation coefficient or RMS difference in
  vector components.
- **Tolerance:** Reproduce the paper's correlation curve / scatter plot
  within the published agreement bands (TODO specify exact tolerance from
  full text).
- **Reference figure:** TODO identify figure number in Sinjan+ 2026 full
  text — inventory abstract refers to "much closer agreement across all
  vector magnetic field components".

## Known pitfalls / failure modes

- **Cadence + noise-level matching.** The paper notes agreement is much
  better when HMI and PHI-HRT cadences and noise are matched; do not
  cross-compare without equalizing.
- **Strong-field regime.** PHI-HRT continues to infer stronger fields than
  HMI LOS magnetograms in strong fields; this is not eliminated by
  stray-light correction.
- **Mercury transit availability.** The stray-light recipe leverages
  specific transit data; rerunning for a different perihelion may not
  have the same calibration opportunity.
- **PSF temporal drift.** Optics performance may drift over the mission;
  the correction parameterization at the 2023 conjunction may not hold
  unchanged at later perihelia — recheck.
- **Inversion-method coupling.** The inferred-field comparison depends on
  the Milne-Eddington inversion settings; identical settings on both
  sides are required.
- **Limb-darkening assumption.** Limb-profile stray-light estimation
  assumes a known limb-darkening function; departures introduce bias.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — stray-light correction improves PHI-HRT vs HMI agreement | **Verifiable task:** `straylight_corrected_phi_hrt(interval) -> ImageStack` + correlation report |
| Methods — limb-profile + transit-based PSF quantification + correction | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — PHI-HRT L2 + HMI vector magnetograms + transit/limb data | **MCP / tool contracts:** SOAR + JSOC via harness fallback |
| Caveats — strong-field residual, cadence matching, PSF drift, inversion coupling | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — comparison plots (TODO identify figure numbers) | **Benchmark artifacts:** scatter-plot + per-pixel difference map |

## Claim boundary

**In scope.** Stray-light analysis of **SO/PHI-HRT** at 0.28 au using
**solar-limb profiles + Mercury transit**, and cross-comparison with
**SDO/HMI during the 2023 March inferior conjunction**. The skill is a
calibration step for PHI-HRT data products, bounded to that conjunction
window.

**Out of scope — do NOT generalize beyond:**

- Do not apply this exact correction unchanged to SO/PHI-FDT — different
  optical chain.
- Do not infer SO/EUI / SPICE calibration recipes from this paper.
- Do not assume the strong-field residual is resolved — the abstract
  states it persists at |B|>1600 G.
- Do not generalize the correlation numbers to perihelia other than the
  2023 March conjunction without re-running.

## Links

- DOI: TODO_verify_with_full_text.
- arXiv: https://arxiv.org/abs/2603.18744
- ADS: TODO_verify_with_full_text.
- Code: TODO — PHI calibration pipeline; community tools.
- Data: ESA SOAR (PHI-HRT); JSOC (HMI).

## Skill graph → depends_on

- `[[muller-2020-solar-orbiter-mission-overview]]` — orbit context.
- `[[horbury-2020-solo-mag-vector-magnetometer]]` — in-situ pairing for
  flux-balance checks.
- `[[paper-hmi-vector-magnetogram-reference]]` — TODO add HMI reference
  paper-skill when needed.

## References

- Sinjan et al. (2026), arXiv:2603.18744. Inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_solar_orbiter.json`
  (entry with arxiv_id "2603.18744v1").
