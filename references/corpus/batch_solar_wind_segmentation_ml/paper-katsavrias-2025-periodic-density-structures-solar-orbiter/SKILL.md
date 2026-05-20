---
name: katsavrias-2025-periodic-density-structures-solar-orbiter
description: >-
  Use when detecting and cataloguing quasi-Periodic Density Structures (PDSs) in Solar
  Orbiter density data with Multitaper + wavelet, and quantifying their radial-length-scale
  evolution between 0.3 and 1 au — central claim is slow-wind PDSs expand at ~10% and
  fast-wind PDSs compress at ~10% across that range (Katsavrias et al. 2025,
  arXiv:2511.15518; venue TODO verify).
version: 0.1.0
tags: [solar-orbiter, density-structures, mesoscale, wavelet, multitaper, detection-pipeline, radial-evolution, catalog]
quality_level: pilot
executable_status: scaffold
---

# Katsavrias 2025 — Solar Orbiter Periodic Density Structures: Detection + Radial Evolution

> Compiled from Katsavrias, C., Di Matteo, S., Kepko, L., Viall, N., Walsh, A. (2025), *Identification of periodic density structures in Solar Orbiter data: Radial evolution*, arXiv:2511.15518 (venue TODO verify).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. Multitaper time-bandwidth parameter, wavelet mother function, and PDS-acceptance thresholds require the full text.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Detecting **quasi-periodic density structures** (PDSs) — trains of advected mesoscale density variations on minute-to-hour timescales — in Solar Orbiter density data.
- Producing a **catalog** of PDS events with radial-length-scale measurements between 0.3 and 1 au.
- Quantifying **slow-wind expansion** vs **fast-wind compression** of PDSs as a function of heliocentric distance.
- Coupling PDS detections to **interchange-reconnection source-region** hypotheses near the Sun.

Do NOT use this skill when:

- Detecting **switchbacks** (different signature — magnetic-field reversals, not density modulations); see [[bale-2021-solar-source-switchbacks-magnetic-funnels]].
- Detecting **shocks / discontinuities** ([[paper-hu-2022-deep-swim-cnn-discontinuities]]).
- Working at 1 au only — the value-add is the **radial evolution** from 0.3 au upward.

## 2. Paper claim → verifiable task

**Claim (narrow form).** A combined Multitaper + wavelet pipeline applied to Solar Orbiter density measurements between **0.3 and 1 au** identifies a publicly released catalog of PDSs. PDSs advected with **slow wind expand at ~10%** in radial length scale L_R across the inner heliosphere, while PDSs detected in **fast-wind segments compress at a similar ~10% rate**. PDS radial-length scales fall in the **100–10,000 Mm** range (i.e., mesoscale).

**Verifiable task.** A reproduction succeeds when an agent:

1. Re-runs the Multitaper + wavelet pipeline on the same Solar Orbiter density data set.
2. Recovers a catalog whose total event count agrees within tolerance (TODO verify).
3. Reproduces the slow-wind +10% expansion and fast-wind −10% compression trends as a function of heliocentric distance.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Density ingestion (Solar Orbiter)

- Procedure:
  1. Pull Solar Orbiter density: RPW spacecraft-potential-derived n_e (cf. [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]]) and/or SWA/PAS n_p moments. The specific product the paper uses is TODO verify.
  2. Restrict to the heliocentric-distance range 0.3–1 au and quality-flag-clean intervals.

### Algorithm 3.2 — Multitaper spectral detection

- Procedure:
  1. Apply Slepian-taper multitaper PSD to sliding windows of length L (TODO verify; minutes-to-hours).
  2. Test each frequency for significance against a red-noise null (TODO verify the null model).
  3. Mark windows with significant periodic peaks as candidate PDS intervals.

### Algorithm 3.3 — Wavelet time-frequency confirmation

- Procedure:
  1. Compute continuous wavelet transform (mother function TODO verify; Morlet is standard).
  2. Confirm the multitaper-detected peak persists in time-frequency space.
  3. Extract per-PDS centre frequency f_0, duration Δt, and the corresponding radial length L_R = V_sw / f_0.

### Algorithm 3.4 — Radial-evolution analysis

- Procedure:
  1. Bin PDS detections by heliocentric distance r.
  2. Separately for slow-wind (V_sw < threshold) and fast-wind (V_sw > threshold) populations, fit L_R(r) (or log L_R vs log r).
  3. Report the expansion (slow) / compression (fast) rates and compare to the paper's ~10% values.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once windowing + significance thresholds are pinned.
def katsavrias2025_pds(density_timeseries, vsw_timeseries, r_timeseries):
    candidates = multitaper_peaks(density_timeseries, window_len="paper_len", null="red_noise")
    pds_events = wavelet_confirm(candidates)
    for event in pds_events:
        event.L_R = vsw_timeseries[event.center] / event.f0
    return fit_radial_trend(pds_events, vsw_timeseries, r_timeseries)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Solar Orbiter RPW | spacecraft-potential-derived n_e | L2 / L3 | 0.3–1 au coverage window TODO verify | SOAR / ESA | `solarmach` / cdflib |
| Solar Orbiter SWA/PAS | n_p moments | L2 | Same | SOAR | `cdflib` |
| Solar Orbiter MAG | B for context | L2 | Same | SOAR | `cdflib` |
| Heliocentric distance r | s/c position | derived | Same | NAIF SPICE | `spiceypy` |

The paper's catalog itself is the **central artifact** ("we compiled and made publicly available an extensive list of PDSs") — the public catalog location is TODO verify.

## 5. Validation target → benchmark artifact

- **Claim**: PDS L_R ∈ [100, 10,000] Mm; slow-wind PDSs expand at ~10%, fast-wind PDSs compress at ~10% across 0.3–1 au.
- **Metric**: per-population fitted slope of L_R(r); event-count tolerance.
- **Tolerance**: TODO verify (±2% on the slope is a plausible benchmark).
- **Reference figure**: TODO verify — likely a L_R-vs-r scatter coloured by slow/fast.

Recommended check artifacts:

- `katsavrias2025_pds_catalog.csv` — per-event (t_start, t_end, f0, L_R, r_au, V_sw, slow_fast).
- `katsavrias2025_radial_trend.png` — L_R vs r split by population.

## 6. Failure modes → skill memory

- **n_e from V_sc calibration.** RPW spacecraft-potential-to-density conversion is bias-setting-dependent; the calibration version matters.
- **Red-noise null choice.** PSD red-noise nulls (AR(1), Markov, AR(p)) give different significance verdicts.
- **Wavelet edge effects.** PDS at the start/end of an interval may be cut by the cone of influence; flag these.
- **V_sw frame.** L_R = V_sw / f_0 assumes Taylor's hypothesis; for slow wind near 0.3 au this is borderline, and ion-bulk velocities may differ from electron-derived n_e timestamps.
- **Slow / fast threshold.** The slow / fast cut (e.g., 400 / 500 km s⁻¹) shapes both populations' inferred trends.
- **Heliocentric-distance binning.** Coarse bins hide the trend; over-fine bins inflate uncertainty.
- **Multitaper time-bandwidth product.** Higher NW averages more, but blurs the peak detection.

## 7. Claim boundary

**In scope.** PDS detection and radial-length-scale evolution from 0.3 to 1 au in Solar Orbiter density data using Multitaper + wavelet, with slow-wind expansion and fast-wind compression at ~10%.

**Out of scope — do NOT generalise beyond:**

- 1-au-only studies (insufficient radial coverage to test the expansion / compression claim).
- Density structures with periods outside the paper's frequency band.
- Causal claims about reconnection mechanisms at the Sun — the paper's link to interchange / magnetic reconnection is a *consistency* claim, not a *causal* one.
- PSP near-Sun PDS statistics — instrument cadence and density-derivation differ; rerun the pipeline on the relevant data.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2511.15518
- ADS: TODO verify.
- Code: TODO verify.
- Data: Solar Orbiter via SOAR (public); the paper's PDS catalog is described as publicly released — TODO verify URL.

## 9. Skill graph → depends_on

- `[[paper-carbone-2021-electron-density-turbulence-ion-cyclotron-waves]]` — RPW V_sc → n_e methodology and uncertainty.
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — sibling unsupervised time-series-mining approach.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — sibling event-cataloguing pipeline (different signature).
- `[[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]` — sibling near-Sun source-region hypothesis; PDSs and switchbacks may share footpoint structures.

## Notes

- The PDS catalog is itself a load-bearing artifact; before benchmarked-tier promotion, the catalog hosting URL and a fingerprint (e.g., event-count + parameter ranges) must be pinned.
