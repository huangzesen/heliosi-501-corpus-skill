---
name: paper-eui-fsi-hri-coronal-bright-points-statistics
description: >-
  Use when characterizing the small-scale transient brightening ("campfire")
  population in Solar Orbiter EUI HRI 174 Å imagery — short-duration coronal
  bright points spanning ~400–4000 km in size and ~10–200 s in duration,
  seen near `R_helio ~ 0.55 au` in the discovery dataset. Central verifiable
  anchor at this slug: Berghmans, Auchère, Long, Soubrié, Mierla, et al.
  (2021), "Extreme UV quiet Sun brightenings observed by Solar Orbiter/EUI",
  A&A 656, L4 (arXiv:2104.03382; DOI 10.1051/0004-6361/202140380). The
  paper documents an EUV brightening class distinct from previously known
  AR transients; downstream campfire-statistics papers (Narang+ 2025;
  Chitta+ 2022; Huang+ 2023) extend the population and spectroscopy and
  are tracked as companions.
paper:
  authors_verified: true
---

# Berghmans 2021 — EUI HRI "Campfire" Coronal Bright Points

> Compiled with verified anchor to:
>   Berghmans, D.; Auchère, F.; Long, D. M.; Soubrié, E.; Mierla, M.;
>   et al. (2021), *Extreme UV quiet Sun brightenings observed by
>   Solar Orbiter/EUI*, Astronomy & Astrophysics **656**, L4.
>   arXiv:2104.03382 (verified 2026-05-19);
>   DOI 10.1051/0004-6361/202140380 (verified via arXiv abs metadata
>   2026-05-19; CrossRef confirmation TODO).
> Companion / follow-on (referenced; arXiv-confirmed at this pass):
>   Narang et al. 2025, *Extreme-ultraviolet transient brightenings in
>   the quiet-Sun corona*, A&A 699, A138 (arXiv:2505.03656);
>   Huang et al. 2023, *Imaging and spectroscopic observations of
>   extreme-ultraviolet brightenings using EUI and SPICE on board Solar
>   Orbiter*, A&A 673, A82 (arXiv:2303.15979).

This file is the agent-native compiled form of the campfire population,
not a paper summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Detecting and tabulating **EUV transient brightenings** in EUI HRI 174 Å sequences over quiet-Sun fields, where the science target is the campfire size–duration–temperature population in the discovery regime (`R_helio ~ 0.55 au` to nominal-mission distances).
- Comparing **campfire-scale brightenings** to the broader nanoflare / microflare / flare ladder ([[paper-microflare-stix-nonthermal-electron-spectra]], [[paper-cheung-2019-flare-energy-buildup-3d-mhd-active-region]]) on the small-event end.
- Cross-referencing campfire positions against **photospheric magnetogram polarities** to test mixed-polarity / cancellation triggers.
- Building a downstream-spectroscopy follow-on with **SPICE + EUI** ([[paper-microflare-stix-nonthermal-electron-spectra]] is the X-ray side; SPICE is the EUV-spectroscopy side, covered in Huang+ 2023 as a companion paper).
- Designing a quiet-Sun coronal-heating budget study, where campfires' aggregate energy contribution is contested (the Berghmans+ 2021 discovery paper does **not** claim the energy budget is closed by campfires; it only documents the population's existence).

Do NOT use this skill when:

- The target is a flare, microflare, or active-region nanoflare — campfires were discovered in **quiet-Sun** regions and the published size/duration envelope (`~400–4000 km`, `~10–200 s`) is for that regime.
- The instrument is SDO/AIA or GOES/SUVI at lower resolution — the discovery paper's detection threshold is set by EUI HRI's image scale and DEM; AIA cannot resolve the small end of the population.
- The science requires absolute thermal energy budget for individual events — DEM-based temperature inference in Berghmans+ 2021 is broad-band (`log T ~ 6.1–6.15`) and per-event energy estimation has large uncertainty.
- The viewing distance `R_helio` is materially different from the discovery dataset's `~0.556 au` without re-validating detection thresholds.

## 2. Paper claim → verifiable task

**Anchored claim (Berghmans+ 2021).** EUI HRI 174 Å imagery from
Solar Orbiter at `R_helio = 0.556 au` reveals a population of
**small-scale, short-lived EUV brightenings** in the quiet Sun — the
"campfires" — with characteristic sizes `~400–4000 km` and durations
`~10–200 s`. Stereoscopic triangulation against SDO/AIA places the
brightenings at heights `~1000–5000 km` above the photosphere.
Differential emission measure (DEM) inference puts the bulk of the
campfire emission at `log T ~ 6.1–6.15` (`~1.3–1.4 MK`), consistent
with low-coronal temperatures. Campfires are interpreted as a **new
class within the flare/microflare/nanoflare spectrum** — distinct from
previously known AR transients and chromospheric bright points by
their quiet-Sun host, small spatial extent, short duration, and low
coronal temperature.

**Verifiable task.** A reproduction succeeds when an agent:

1. Fetches an EUI HRI 174 Å sequence covering a quiet-Sun field at a distance comparable to the discovery dataset (`R_helio ~ 0.5–0.6 au` is the best-anchored regime; lower or higher requires explicit threshold re-validation).
2. Applies cosmic-ray and pointing-jitter masking.
3. Detects persistent brightenings (threshold + persistence detector; threshold typically expressed as a multiple of the local quiet-Sun standard deviation, with persistence ≥ 2 consecutive frames).
4. Records per-event: spatial size (typical Mm-scale from the published distribution), duration (typical 10–200 s), and host region (quiet-Sun verified).
5. (When SDO/AIA is co-temporal and EUI–SDO baseline gives a non-degenerate triangulation) Triangulates event heights and verifies they fall in the `~1000–5000 km` envelope of the discovery paper.
6. (Optional, requires multi-channel data) Runs DEM inference and checks that the temperature peak falls near `log T ~ 6.1–6.15`.

The **per-event detection density** — i.e. campfires per unit area per
unit time — is in the discovery paper but its specific numerical value
is **TODO_verify** at the level of an exact density target (the paper
documents the population's existence and the size/duration envelope
as the headline; downstream papers like Narang+ 2025 publish refined
densities for the full population over multiple encounters).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — EUI HRI L2 fetch + QA

- Procedure:
  1. Fetch the EUI HRI 174 Å L2 cube for the target encounter window.
  2. Read encounter metadata (`R_helio`, image scale `km/px`, accumulation depth).
  3. Mask cosmic-ray hits (single-frame, single-pixel spikes) and dropped frames.
  4. Co-align using stellar / limb-feature tracking; verify pointing-jitter envelope before event extraction.

### Algorithm 3.2 — Threshold + persistence detection

- Procedure:
  1. Compute a local quiet-Sun statistic (running median + std) over a sliding spatial-temporal window large enough to contain background but smaller than the largest event.
  2. Define an event candidate: intensity excursion above `k·σ` (`k ~ 5` is the discovery-paper neighbourhood; exact value **TODO_verify**) lasting at least `N_persistence` frames (`N ≥ 2` at the discovery cadence; **TODO_verify** exact value).
  3. Cluster pixels into connected components; record per-event spatial footprint and time profile.
  4. Reject events overlapping known AR boundaries or off-limb / on-disk masks where the quiet-Sun assumption breaks.

### Algorithm 3.3 — Triangulation against SDO/AIA (optional)

- Procedure:
  1. Identify SDO/AIA 171 Å frames co-temporal with EUI HRI events.
  2. Solve for event centroid in heliocentric coordinates using the Solar Orbiter ↔ SDO baseline.
  3. Triangulate event height above photosphere; expect bulk to fall in `~1000–5000 km`.

### Algorithm 3.4 — DEM inference (optional, multi-channel)

- Procedure:
  1. If multi-channel data (EUI HRI 174 Å + AIA 131/171/193/211/335 Å) are co-temporal, run a DEM inversion at each campfire pixel during the brightening peak.
  2. Confirm the DEM peak temperature falls near `log T ~ 6.1–6.15`.

Code skeleton (scaffold tier; assumes SunPy is the conventional
adapter — not LingTai-bound):

```python
# Pseudocode aligned with Berghmans+ 2021 §3.
import numpy as np
import sunpy.map

def detect_campfires(cube_data, t, k_sigma=5.0, persistence_frames=2):
    bg_med, bg_std = local_quiet_sun_stats(cube_data)
    above = (cube_data - bg_med) > k_sigma * bg_std
    events = persistent_connected_components(above, persistence=persistence_frames)
    return [
        {
            't_start': t[ev.t0],
            't_end': t[ev.t1],
            'duration_s': t[ev.t1] - t[ev.t0],
            'area_Mm2': ev.area_Mm2,
            'centroid': ev.centroid_helio,
        }
        for ev in events
    ]
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Solar Orbiter EUI HRI | 174 Å intensity | L2; encounter-dependent (seconds to sub-second) | 2020-02 onwards | SOAR | EUI Data Release loader |
| SDO/AIA | 171 / 193 Å intensity | L1; 12 s | 2010 onwards | JSOC | `drms` |
| SDO/HMI | LOS magnetogram (cross-reference) | L1 720 s or `hmi.M_45s` | 2010 onwards | JSOC | `drms` |
| Solar Orbiter SPICE (optional, follow-on) | EUV spectroscopy | L2 | 2020-02 onwards | SOAR | SPICE loader |
| Solar Orbiter ephemeris | `R_helio`, geometry | per-frame | Mission | `xhelio-spice` (LingTai-bound MCP) | SPICE-based |

The LingTai-bound MCP covers the ephemeris side only; EUI / SDO
loaders remain external adapters the runtime must wire.

## 5. Validation target → benchmark artifact

- **Anchored, reproducible targets (Berghmans+ 2021):**
  - Campfire size envelope `~400–4000 km`.
  - Duration envelope `~10–200 s`.
  - Height above photosphere `~1000–5000 km` (from stereoscopic triangulation).
  - DEM-peak temperature `log T ~ 6.1–6.15` (`~1.3–1.4 MK`).
  - Quiet-Sun host (campfires are **not** AR transients).
- **TODO_verify (numerical specifics readable from the paper but not anchored at this slug):**
  - Exact detection density (events Mm⁻² hr⁻¹) at the discovery operating point.
  - Exact `k·σ` detection threshold and persistence-frame count.
  - Per-event DEM dispersion (the published `log T ~ 6.1–6.15` is the peak; tails are not anchored).
- **Companion-paper targets (Narang+ 2025; Huang+ 2023):**
  - Refined population densities across multiple encounters (Narang+ 2025).
  - Spectroscopic signatures via SPICE (Huang+ 2023).

Recommended check artifacts:

- `campfire_catalog.csv` — one row per detected event: `(t_start, t_end, duration_s, area_Mm2, centroid_helio, peak_intensity, R_helio_au)`.
- `campfire_size_duration_hist.json` — population histograms for cross-paper comparison.
- A triangulation panel against AIA for any events with co-temporal SDO viewing.

## 6. Failure modes → skill memory

- **Detection-threshold dependence.** The published campfire envelope is conditional on the discovery paper's `k·σ + persistence` operating point. Pushing the threshold lower extends the small-end tail into the cosmic-ray and noise-floor regime; pushing higher truncates the population. Reproduce the operating point before claiming a population match.
- **Cosmic-ray contamination.** EUI HRI accumulates cosmic-ray hits between solar-physics events; single-frame, single-pixel intensity spikes look like the smallest campfires unless masked.
- **Pointing jitter** at sub-arcsec scale creates apparent brightenings on the limb of bright features; remove jitter signatures before claiming new events.
- **Image-scale variation with `R_helio`.** At perihelion the same number of detected campfires per unit angular area corresponds to *fewer* events per Mm² than at aphelion; cross-encounter density studies must normalise by `km/px`. (Same caveat as [[paper-so-phi-hrt-vector-magnetogram-radial-distance]] and [[paper-coronal-plume-substructure-eui-high-cadence]].)
- **Quiet-Sun ≠ campfire-only.** Reconnection brightenings in the quiet Sun include long-known X-ray bright points and chromospheric jets; campfires are *one* class in a busier inventory. Mis-classification at the population boundary is the dominant population-statistic systematic.
- **DEM is multi-channel-dependent.** A DEM peak at `log T ~ 6.1–6.15` from a single channel (HRI 174 Å) is **not** measurable — the published DEM uses HRI + AIA jointly. Single-channel temperature claims overstate the inference.
- **Energy budget is contested, not closed.** Berghmans+ 2021 documents the population; it does **not** claim campfires close the quiet-Sun coronal heating budget. Treat the heating-budget question as **open** (the campfire literature includes both yes-they-contribute and no-they-don't lines).
- **Discovery-encounter ≠ all encounters.** The headline numbers are at `R_helio = 0.556 au`. Subsequent encounters and population studies (Narang+ 2025) refine the picture; cite the appropriate paper for the specific encounter / population regime.

## 7. Claim boundary

**In scope.** EUI HRI 174 Å campfire detection in quiet-Sun fields at
`R_helio ~ 0.5–0.6 au` (discovery regime) and extensions in nominal-
mission encounters where the threshold + persistence operating point
is re-validated; population statistics on size, duration, height, and
DEM-peak temperature.

**Out of scope — do NOT generalise beyond:**

- Active-region transients, microflares, or X-class flares.
- Imagers other than EUI HRI without re-validating the detection threshold.
- A single-channel temperature claim — DEM requires multi-channel data.
- A heating-budget closure claim — the Berghmans+ 2021 anchor does not deliver this.
- Quiet-Sun events at `R_helio` materially outside `~0.5–0.6 au` without per-encounter threshold re-validation.

If a downstream task asks for any of the above, refuse it and route to
a sibling paper-skill.

## 8. Links

- arXiv: https://arxiv.org/abs/2104.03382 (verified 2026-05-19).
- DOI: https://doi.org/10.1051/0004-6361/202140380 (verified via arXiv abs-page metadata 2026-05-19; CrossRef double-confirmation TODO).
- ADS: TODO verify (expected bibcode 2021A&A...656L...4B).
- Companion paper arXiv: https://arxiv.org/abs/2505.03656 (Narang et al. 2025; A&A 699, A138; verified via arXiv search 2026-05-19).
- Companion paper arXiv: https://arxiv.org/abs/2303.15979 (Huang et al. 2023; A&A 673, A82; verified via arXiv search 2026-05-19).
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`.

## 9. Skill graph → depends_on

- `[[paper-coronal-plume-substructure-eui-high-cadence]]` — EUI HRI is the shared instrument; plumelets and campfires are the two leading EUI-HRI population studies on small-scale dynamics.
- `[[paper-magnetogram-noise-floor-quiet-sun-disambiguation]]` — quiet-Sun mixed-polarity emergence is the candidate driver; the magnetogram noise floor sets whether the photospheric driver is detectable.
- `[[paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure]]` — heating-budget context (campfire energy budget is debated; this skill sets the alternative wave-driven baseline).
- `[[paper-microflare-stix-nonthermal-electron-spectra]]` — STIX is the X-ray side of the small-event ladder; campfires sit below the STIX microflare regime in size and temperature.

## 10. Research-generation affordances

- **Encounter-resolved population study.** Combining Berghmans+ 2021 (discovery), Huang+ 2023 (EUI + SPICE spectroscopy), and Narang+ 2025 (multi-encounter population) into an encounter-resolved campfire ladder would directly quantify whether the campfire population scales with `R_helio` (i.e., is the angular-resolution-limited tail of a more populous physical population, or a fixed solar phenomenon).
- **Cancellation / mixed-polarity coupling.** Cross-referencing EUI HRI campfire catalogs against high-resolution magnetogram noise-floor maps ([[paper-magnetogram-noise-floor-quiet-sun-disambiguation]]) would test the cancellation-trigger hypothesis the discovery paper raises but does not resolve.
- **Heating-budget closure test.** A direct test that integrates campfire energies across a quiet-Sun field and compares to the locally-required coronal heating rate (Cranmer-2017-style wave budget as the alternative) would adjudicate the contested heating contribution claim.
- **STIX co-observation.** A coordinated STIX campaign on a quiet-Sun field with EUI HRI could probe whether campfires have non-thermal electron signatures; null result is informative (it sets an upper bound on the nanoflare-like reconnection content).
- **Cross-mission ladder.** A campfire-class detector exported to SDO/AIA imagery (with the threshold + persistence operating point recalibrated to AIA's image scale) would either confirm campfires are a missed AIA population or formalise the resolution argument — both outcomes are publishable.
