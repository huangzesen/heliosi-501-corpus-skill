---
name: li-2026-mercury-orbit-solar-wind-turbulence
description: Per-entry paper-skill in pilot_2026_and_runtime (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# li-2026-mercury-orbit-solar-wind-turbulence

## When to use this paper-skill

Invoke when a HelioSI workflow needs a statistical baseline of solar-wind
turbulence properties in the 0.31–0.47 au range, e.g. inertial-range
spectral slope, kinetic-range slope, and their radial evolution near
Mercury's orbit. Typical triggers:

- The user asks "what is the typical kinetic-range spectral index near
  Mercury's orbit?" or wants a reference point for PSP comparisons at
  intermediate distances.
- An agent is constructing a radial profile of turbulence indices and
  needs a high-statistics MESSENGER-MAG anchor between PSP near-Sun and
  Wind/ACE at 1 au.
- Building a `mag-only-spectral-index-estimator` benchmark skill.

Do not invoke for plasma diagnostics that require ion moments — MESSENGER
MAG provides field only; bulk plasma must come from a different source.

## Paper identity and claim boundary

- **Title:** Properties and Radial Evolution of Solar Wind Turbulence Near
  Mercury's Orbit
- **Authors:** Xinmin Li, Chuanfei Dong, Lina Z. Hadid, et al.
- **arXiv:** 2604.21196 (2026)
- **Claim boundary:** Statistical analysis of >17,000 hours of MESSENGER
  magnetometer data over 0.31–0.47 au. Reports inertial-range and kinetic-
  range spectral slopes and the *radial-evolution trend* of the kinetic-
  range index. The paper is a magnetic-field-only statistical survey; it
  does NOT claim a kinetic theory derivation, and it does NOT have plasma
  bulk moments at MESSENGER cadence.

## Scientific or methodological claim to operationalize

> The trace power spectrum of `B` measured by MESSENGER in 0.31–0.47 au
> exhibits an inertial-range slope and a steeper kinetic-range slope; the
> *kinetic-range* slope trends with heliocentric distance in a direction
> reported by the paper (TODO verify direction and quantitative range from
> full text — abstract says "radial-evolution trending of the kinetic-
> range index" without sign in our inventory).

A HelioSI skill operationalizes this by producing, per MESSENGER orbit
segment in 0.31–0.47 au, a tuple `(slope_inertial, slope_kinetic,
break_freq, r_au)` and a radial-evolution regression.

## Required data / instruments / code / archives

- **MESSENGER MAG:** Level-2 magnetic-field time series in solar-wind
  intervals (excluding Mercury magnetosphere and magnetosheath); typical
  cadence 20 Hz.
- **Solar-wind interval list:** an authoritative MESSENGER solar-wind
  filter (e.g. Korth+ catalog, or threshold-based on |B|, plasma proxies).
- **Archives:** PDS-PPI for MESSENGER MAG L2.
- **Code:** scientific Python — `numpy`, `scipy.signal`, optional
  `pyspedas`; trace-PSD estimator via Welch or multitaper.

## Algorithm / workflow steps

1. **Load MESSENGER MAG L2** for selected orbit ranges with
   `0.31 au ≤ r ≤ 0.47 au`.
2. **Filter to solar-wind intervals** using the authoritative catalog;
   exclude magnetosphere, magnetosheath, FIPS-flagged disturbed periods.
3. **Window the time series** into chunks long enough to resolve the
   inertial range and short enough to be stationary (e.g. 30–60 min).
4. **Compute trace power spectral density** `P_trace(f) = P_x + P_y +
   P_z` per chunk using Welch (Hann window, 50% overlap).
5. **Fit two power laws** in the inertial range and the kinetic range,
   separated by the spectral break `f_b`. Use a simultaneous broken-
   power-law fit.
6. **Aggregate per heliocentric-distance bin** in 0.31–0.47 au.
7. **Regress kinetic-range slope vs. r_au** and report sign, slope, and
   uncertainty.

## Minimal executable benchmark or validation target

A HelioSI benchmark version of this skill should:

- Process the published MESSENGER solar-wind set and recover the paper's
  inertial- and kinetic-range slope distributions (means within ±0.1 in
  slope).
- Reproduce the radial-evolution trend of the kinetic-range slope with
  the same sign as the paper (TODO verify sign from full text).
- Pass criterion: regression sign matches; slope-vs-r gradient within a
  factor of 2 of the paper's.

## Known pitfalls / failure modes

- **Magnetosphere contamination.** Including bow-shock-affected intervals
  biases slopes shallower. Always use a vetted solar-wind catalog.
- **Aliasing.** The 20 Hz cadence sets a Nyquist limit; the kinetic-range
  fit must respect it.
- **Stationarity.** Long chunks violate stationarity; short chunks have
  poor frequency resolution. Document chunk length and run sensitivity.
- **Sampling bias.** MESSENGER's elliptical orbit visits different `r_au`
  with different durations, biasing bin-averages.
- **No plasma moments.** Slopes cannot be converted to a wavenumber axis
  without an assumed Taylor-hypothesis velocity; if `V_sw` is taken from a
  proxy or model, document it.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2604.21196 as an Anthropic-
style Skill loadable by the HelioSI runtime:

| Paper element | Agent-native form |
|---|---|
| Claim — "MESSENGER MAG at 0.31–0.47 au exhibits inertial + kinetic ranges with a radial trend in the kinetic-range slope" | **Verifiable task:** `survey_messenger_turbulence(r_bin) -> {slope_inertial, slope_kinetic, f_break, count}` per bin + regression vs `r_au` |
| Methods / equations — trace PSD via Welch; broken-power-law fit; per-`r_au` aggregation + regression | **Executable workflow:** §"Algorithm / workflow steps" 1–7 with chunk length, window, break-frequency prior, and `r_au` bin edges as explicit parameters |
| Data / instruments / code — MESSENGER MAG L2 from PDS-PPI; solar-wind interval catalog | **MCP / tool contracts:** `pds-ppi-mcp.get_messenger_mag(...)`, `pds-ppi-mcp.get_sw_catalog(...)`, optional `cdaweb-mcp` mirror |
| Caveats / failure modes — magnetosphere contamination; Nyquist; stationarity; orbital sampling bias; no plasma moments | **Skill memory:** §"Known pitfalls / failure modes" — runtime rejects intervals failing the SW filter and reports stationarity-test failures |
| Figures / results — slope-distribution histograms + slope-vs-`r_au` regression | **Benchmark artifacts:** per-bin slope histograms, regression plot, `metrics.json` with `(slope_inertial, slope_kinetic, β_r)` |

The Skill compiles a *MESSENGER-only* survey into a HelioSI-callable
turbulence anchor at intermediate heliocentric distance.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** dispatches a `mag-only-turbulence-survey` sub-graph;
  used as a reference anchor in radial-profile composites.
- **Skills it composes with:**
  - [[messenger-mag-loader]] — TODO create
  - [[messenger-solar-wind-filter]] — TODO create
  - [[trace-psd-broken-power-law-fitter]] — TODO create
- **MCPs it would use:** `pds-ppi-mcp` for MESSENGER, optional
  `cdaweb-mcp` if mirrored.
- **HelioSI manuscript role:** demonstrates that HelioSI's skill graph
  spans more than PSP — it can ingest a MESSENGER-only study and provide
  an intermediate-distance anchor between PSP near-Sun and Wind/ACE at
  1 au, which is exactly the kind of cross-mission integration 2026
  reviewers expect.

## References

- Li, X., Dong, C., Hadid, L. Z., et al. (2026). arXiv:2604.21196.
- Inventory: `sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md`
  entry #15.
