---
name: paper-coronal-plume-substructure-eui-high-cadence
description: >-
  Use when characterizing coronal-plume fine substructure ("plumelets") in
  high-cadence EUV imagery from Solar Orbiter EUI High-Resolution Imager
  (HRI) or SDO/AIA, where the science target is the population statistics
  and propagating-disturbance kinematics of plumelets — dynamic filamentary
  threads that comprise the bulk of the plume EUV emission. Central paper
  claim, verified at this slug, is Uritsky, DeForest, Karpen, DeVore, Kumar,
  Raouafi, Wyper (2021), "Plumelets: Dynamic Filamentary Structures in
  Solar Coronal Plumes", ApJ 907, 1 (arXiv:2012.05728; DOI
  10.3847/1538-4357/abd186): a bright coronal plume observed 2016-07-02/03
  resolves into ~10-Mm-wide plumelets carrying upwardly propagating phase-
  speed-190–260 km/s disturbances whose dominant frequency matches the
  solar p-mode band. Companion driver-side paper (verified): Kumar, Karpen,
  Uritsky, DeForest, Raouafi, DeVore (2022), "Quasiperiodic Energy Release
  and Jets at the Base of Solar Coronal Plumes" (arXiv:2204.13871).
paper:
  authors_verified: true
---

# Uritsky 2021 — Plumelets as the Filamentary Fine Structure of Coronal Plumes

> Compiled with verified anchor to:
>   Uritsky, V. M.; DeForest, C. E.; Karpen, J. T.; DeVore, C. R.;
>   Kumar, P.; Raouafi, N. E.; Wyper, P. F. (2021),
>   *Plumelets: Dynamic Filamentary Structures in Solar Coronal Plumes*,
>   The Astrophysical Journal **907**, 1.
>   arXiv:2012.05728; published DOI 10.3847/1538-4357/abd186.
> Companion (verified): Kumar et al. (2022), *Quasiperiodic Energy
>   Release and Jets at the Base of Solar Coronal Plumes*,
>   arXiv:2204.13871.
> Solar-Orbiter EUI HRI / FSI campfire context is supplied by Berghmans+
> (2021) A&A 656 L4 (arXiv:2104.03382; DOI 10.1051/0004-6361/202140380),
> verified independently at this pass; it is referenced here as the
> high-cadence EUV instrument anchor when EUI HRI is the imager.

This file is the agent-native compiled form of the plumelet
substructure result, not a paper summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Resolving **filamentary fine structure within coronal plumes** above polar or quiet-Sun coronal holes in high-cadence EUV imagery (SDO/AIA 171 / 193 Å at native cadence; Solar Orbiter EUI HRI 174 Å during coordinated campaigns).
- Measuring the **propagating-disturbance phase speed** along plume axes (the Uritsky+ 2021 claim band is `~190–260 km/s`) to test whether plume disturbances are slow magnetoacoustic waves, kink waves, or recurrent reconnection outflows.
- Comparing observed **plumelet frequencies** to the photospheric p-mode 5-minute band as a test of the wave-driver hypothesis.
- Connecting plume-base **quasiperiodic interchange-reconnection jets** ([[paper-coronal-hole-jet-population-statistics-aia]], [[paper-coronal-hole-pseudostreamer-boundary-classification]]) upward to plume sub-structure, following the Kumar+ 2022 companion picture.
- Building a candidate source-region picture for **PSP near-Sun microstructures** (switchback packets, Alfvenic spikes) where the candidate seed is plume-internal substructure rather than a single CH-boundary footpoint.

Do NOT use this skill when:

- The target product is the *plume* (envelope) — not the *plumelet* (sub-structure). Population statistics differ between the two by an order of magnitude in cross-section and lifetime; mixing them invalidates the Uritsky+ 2021 narrow claim.
- The cadence is below ~30 s — at lower cadences the propagating disturbances are aliased and the phase-speed inference becomes ill-posed.
- The imager has insufficient resolution to resolve `~10-Mm`-wide threads (the Uritsky+ 2021 measurement uses ~1–2 arcsec angular scales from SDO/AIA; for EUI HRI at perihelion the threshold drops to ~`200–500 km`).
- The science target requires a **temperature** measurement — single-channel EUV (171 or 174 Å) is band-limited and does not by itself yield DEM; route to [[paper-suvi-multi-wavelength-temperature-dem-corona]] or AIA multi-channel.

## 2. Paper claim → verifiable task

**Anchored claim (Uritsky+ 2021 §1, §4).** Inside a bright coronal
plume observed on 2016-07-02 / 03 by SDO/AIA at high cadence and
denoised by Multiscale Gaussian Normalization, **time-evolving
filamentary substructures** ("plumelets") of cross-section `~10 Mm`
account for most of the plume's EUV emission. Plumelets carry
**upwardly propagating periodic intensity disturbances** with phase
speeds in the band `190–260 km/s`. The dominant temporal frequency of
these disturbances coincides with the photospheric p-mode 5-minute
band, supporting a picture where photospheric p-mode flows leak into
plumelets and propagate outward, providing a *seed population* for
fine structure detectable in the near-Sun solar wind.

**Companion claim (Kumar+ 2022, arXiv:2204.13871).** Plume bases host
**recurring jets and brightenings** consistent with quasi-periodic
interchange reconnection at the base of the plume; the jets'
recurrence period overlaps the Uritsky+ 2021 plumelet frequency band,
linking the photospheric-driver picture to a reconnection-driver
alternative at the plume base. This places the Uritsky+ 2021 wave
picture in a *driver-degeneracy* with reconnection-driven outflows.

**Verifiable task.** A reproduction succeeds when an agent:

1. Selects a coronal plume on a polar or low-latitude coronal-hole boundary in a known SDO/AIA window or in a coordinated SO EUI HRI campaign.
2. Co-aligns the EUV cube (171 or 193 Å for AIA; 174 Å for EUI HRI) to a common heliocentric reference frame and corrects for solar rotation.
3. Applies **Multiscale Gaussian Normalization (MGN)** or an equivalent multi-scale contrast filter to expose fine structure (the Uritsky+ 2021 reference choice).
4. Tracks plumelets along their axis via slits / time-distance maps; recovers a phase speed in or compatible with the band `190–260 km/s`.
5. Tabulates plumelet **cross-section widths** (target `~10 Mm` at the published spatial scale) and **lifetimes** (TODO_verify exact range — readable from the paper's tables/figures).
6. Computes the **dominant frequency** of the propagating disturbances and verifies it lies in the photospheric p-mode 5-minute band (`~3.3 mHz`).
7. (If running the companion Kumar+ 2022 analysis on the same window) Identifies recurrent base brightenings/jets and demonstrates an overlap between their recurrence period and the plumelet disturbance frequency band.

Numerical lifetime distributions and per-plumelet apparent-velocity
percentiles are TODO_verify (readable from the paper's figures /
tables); the *headline* phase-speed band, p-mode frequency coincidence,
and `~10-Mm` width are anchored and reproducible from the abstract /
§4.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — High-cadence EUV cube assembly

- Procedure:
  1. Fetch the SDO/AIA 171 Å (and optionally 193 Å) cube at native cadence (12 s for AIA) over the target window. For Solar-Orbiter campaigns use the EUI HRI 174 Å L2 sequence at the encounter's downlinked cadence.
  2. Apply standard calibration (`aiaprep`/`aia.prep` for AIA; the EUI L2 release for HRI).
  3. Co-align frames to a common reference frame; apply solar rotation tracking on the plume's foot.
  4. (Optional, recommended) **Multiscale Gaussian Normalization (MGN)** for fine-structure enhancement; the Uritsky+ 2021 paper relies on this step to expose plumelet boundaries.

### Algorithm 3.2 — Plumelet identification + tracking

- Procedure:
  1. Place spatial slits perpendicular and parallel to the plume axis.
  2. Extract time-distance maps along each slit.
  3. Identify diagonal stripes in the time-distance map (propagating intensity disturbances) and fit their slopes to obtain apparent **phase speed** along the plume axis.
  4. Identify perpendicular slits where the cross-section width exposes individual plumelets; record per-plumelet widths and centroid trajectories.

### Algorithm 3.3 — Frequency analysis vs p-mode driver

- Procedure:
  1. Per-slit, compute the temporal power spectrum of the disturbance.
  2. Compare the dominant frequency to the photospheric p-mode 5-minute band centred at `~3.3 mHz` (`~5 min` period).
  3. Report the coherence (or simply spectral overlap) between the plumelet disturbance band and the p-mode band.

### Algorithm 3.4 — Base-jet companion (optional Kumar+ 2022)

- Procedure:
  1. From the same EUV cube extract a base region of the plume.
  2. Identify recurrent brightenings / jet signatures (Kumar+ 2022 reports these from a combination of AIA, IRIS, and Hinode/XRT in their event-study window — adapt to whatever multi-channel context is available).
  3. Compute the recurrence period of base jets and check for overlap with the Uritsky+ 2021 plumelet disturbance band.

Code skeleton (scaffold tier; assumes SunPy is the conventional
adapter — not LingTai-bound):

```python
# Pseudocode aligned with Uritsky+ 2021 §3–§4.
import numpy as np
import sunpy.map

def plumelet_track(cube_data, t, slit_xy_axis, slit_xy_perp):
    # cube_data: (nt, ny, nx) co-aligned, MGN-enhanced EUV cube.
    td_axis = sample_along_slit(cube_data, slit_xy_axis)
    td_perp = sample_along_slit(cube_data, slit_xy_perp)
    phase_speed_km_s = fit_diagonal_stripes(td_axis, dt=t[1]-t[0])
    plumelet_widths_Mm = perp_widths(td_perp)
    freq_hz, power = welch_along_time(td_axis)
    return phase_speed_km_s, plumelet_widths_Mm, freq_hz, power
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| SDO/AIA | 171 Å (and 193 Å) intensity | L1; 12 s cadence | 2010 onwards | JSOC | `drms` / `sunpy` |
| Solar Orbiter EUI HRI | 174 Å intensity | L2; encounter-dependent cadence (sub-second to seconds during HRI campaigns) | 2020-02 onwards | SOAR | EUI Data Release loader |
| Solar Orbiter EUI FSI | 174 / 304 Å context | L2 | 2020-02 onwards | SOAR | EUI Data Release loader |
| Solar Orbiter ephemeris | `R_helio`, sub-spacecraft position | per-frame | Mission | `xhelio-spice` (LingTai-bound MCP) | SPICE-based |

LingTai-bound MCPs cover the ephemeris side only; an EUI / AIA loader
remains an external adapter the runtime must wire (do not invent a
binding — surface as a prerequisite).

## 5. Validation target → benchmark artifact

- **Anchored, reproducible targets (Uritsky+ 2021):**
  - Plumelet **cross-section** `~10 Mm` (within the published plume window 2016-07-02 / 03).
  - **Phase speed** along plume axis in the band `190–260 km/s`.
  - **Dominant disturbance frequency** coincident with the photospheric p-mode 5-minute band (`~3.3 mHz`).
- **TODO_verify (numerical detail readable from figures / tables of the paper but not anchored at this slug):**
  - Per-plumelet lifetime percentiles (lower and upper percentiles of the duration distribution).
  - Distribution of cross-sections beyond the headline `~10 Mm`.
  - The exact number of plumelets identified in the published event.
- **Companion (Kumar+ 2022) target:**
  - Recurrence period of base jets vs plumelet frequency — qualitative overlap.

Recommended check artifacts:

- `plumelet_kinematics.csv` — one row per identified plumelet trace: `(t_start, t_end, lifetime_s, width_Mm, phase_speed_km_s, slit_id)`.
- `plumelet_spectra.json` — per-slit power spectrum and the dominant-frequency report.
- A time-distance figure analogous to Uritsky+ 2021 Fig. 6 (for visual QA).

## 6. Failure modes → skill memory

- **Spatial-scale aliasing.** Plumelets are ~10 Mm; at AIA's 0.6 arcsec/px ≈ 435 km/px (1 au) they are well-resolved, but binning, smoothing, or limited cadence can blur threads into a single envelope and recover the *plume* phase speed instead of the *plumelet* phase speed.
- **MGN choice matters.** Without MGN (or an equivalent multi-scale enhancement) plumelet boundaries are not separable from background EUV emission; the Uritsky+ 2021 measurement is **MGN-dependent** in practice. Reproductions that skip MGN tend to under-count plumelets and inflate apparent widths.
- **Cadence floor for phase speed.** With `dt > 30 s` the apparent disturbances near `~200 km/s` over a ~50-Mm slit produce only `~3` samples; the slope fit becomes ill-posed. EUI HRI at sub-second cadence resolves the disturbance with margin; AIA at 12 s is on the safe side.
- **Driver degeneracy: p-modes vs reconnection.** A frequency coincidence with the p-mode band does **not** prove p-mode driving — Kumar+ 2022 demonstrates that quasi-periodic base reconnection jets share the same recurrence band and can produce the same propagating-disturbance signature. Treat the Uritsky+ 2021 wave picture and the Kumar+ 2022 reconnection picture as a *driver pair*, not as mutually exclusive.
- **Plume identification is intensity-threshold dependent.** Especially at the limb, the envelope of the plume is sensitive to the chosen intensity cut-off; documented thresholds in §3 of Uritsky+ 2021 should be reproduced rather than re-tuned.
- **Channel limitations.** SDO/AIA 171 Å samples a narrow temperature band centred near `log T ~ 5.85`; plumelets at hotter or cooler temperatures would be missed. The Uritsky+ 2021 conclusions are *channel-conditional*.
- **EUI HRI orbit dependence.** EUI HRI's effective image scale changes with `R_helio` (the same caveat as SO/PHI HRT — see [[paper-so-phi-hrt-vector-magnetogram-radial-distance]]). Cross-encounter comparisons must hold image scale fixed or weight by the per-encounter `km/px`.
- **PSP-side connection is hypothesis, not measurement.** The paper *suggests* plumelets could seed PSP-detected microstructure but does not measure the in-situ end of the chain; do not over-claim a verified plume → switchback link.

## 7. Claim boundary

**In scope.** Plumelet-scale fine substructure within coronal plumes
above polar / quiet-Sun CHs in high-cadence EUV imagery, the
propagating-disturbance phase-speed and frequency analysis on the
Uritsky+ 2021 event, the Kumar+ 2022 base-jet companion picture.

**Out of scope — do NOT generalise beyond:**

- The plume *envelope* — the substructure measurement is plumelet-specific.
- Plume substructure in regions other than polar / quiet-Sun CHs without separate validation.
- A claim that p-modes are the *unique* driver of plumelet disturbances — Kumar+ 2022 supplies an explicit alternative.
- Single-channel temperature claims — plumelets are characterized in intensity, not DEM.
- Direct in-situ connection to PSP-observed microstructures beyond a *hypothesis*.

If a downstream task asks for any of the above, refuse it and route to
a sibling paper-skill.

## 8. Links

- arXiv: https://arxiv.org/abs/2012.05728 (verified 2026-05-19).
- Published DOI: https://doi.org/10.3847/1538-4357/abd186 (ApJ 907, 1; published 2021; verified via arXiv abs page mapping 2026-05-19).
- Companion arXiv (Kumar+ 2022 base jets): https://arxiv.org/abs/2204.13871 (verified 2026-05-19 via the same arXiv search).
- Berghmans+ 2021 campfires (EUV high-cadence anchor): https://arxiv.org/abs/2104.03382 ; https://doi.org/10.1051/0004-6361/202140380 (verified 2026-05-19).
- ADS: TODO verify (no bibcode fetched at this pass).
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`.

## 9. Skill graph → depends_on

- `[[paper-eui-fsi-hri-coronal-bright-points-statistics]]` — EUI HRI is the high-cadence EUV instrument anchor for the Solar-Orbiter side of the analysis.
- `[[paper-coronal-hole-jet-population-statistics-aia]]` — Kumar+ 2022's base-jet picture connects plumelets to the CH-jet population statistics.
- `[[paper-coronal-hole-pseudostreamer-boundary-classification]]` — boundary identification for the host CH region.
- `[[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]` — downstream-hypothesis consumer for the PSP-side seed-population argument (do not treat as a measured chain).

## 10. Research-generation affordances

- **Driver disambiguation campaign.** A coordinated EUI HRI + IRIS + AIA + Hinode/XRT observation of a single plume over an extended window would let the Uritsky-2021 wave picture and the Kumar-2022 reconnection picture be tested *jointly* on the same event: if the disturbance frequency tracks the base-jet recurrence as that recurrence drifts, reconnection is the dominant driver; if it tracks p-modes independently of base-jet activity, the wave picture is reinforced.
- **PSP↔SO conjunction follow-through.** When SO points at a plume during a PSP near-perihelion encounter, the plumelet kinematic spectrum (cross-section, phase-speed, frequency band) is the *predicted* near-Sun source-side population for the in-situ microstructure seed argument; this is currently a hypothesis ([[bale-2021-solar-source-switchbacks-magnetic-funnels]] makes the case from in-situ side only). The composite measurement is missing in the corpus.
- **Plumelet population statistics across CH classes.** Uritsky+ 2021 analyses one event; a population study across polar-CH, low-latitude-CH, and CH-boundary plumes would measure the heterogeneity of the `190–260 km/s` band — currently presented as a single number with implicit population spread.
- **Reproducibility of MGN dependence.** A controlled test that re-derives plumelet boundaries with MGN vs an alternative multi-scale enhancement (wavelet, NUWT, unsharp-masking) would quantify how much of the headline claim is MGN-conditional.
- **Cross-encounter EUI HRI replication.** EUI HRI's image scale shrinks at perihelion; a replication that sweeps `km/px` by encounter and measures whether the `~10-Mm` width is intrinsic or scale-conditional would directly test resolution sensitivity.
