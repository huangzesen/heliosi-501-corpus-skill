# horbury-2020-solo-mag-vector-magnetometer

## When to use this paper-skill

Invoke when a HelioSI workflow needs the **canonical SO/MAG instrument
description** — dual fluxgate boom geometry (IBS inboard, OBS outboard),
sensor noise floors, intended L1/L2 vector products (normal / burst /
calibrated normal mode), and coordinate-frame conventions (SRF, RTN, SC).
Typical triggers:

- An agent must load SO MAG vector B for a turbulence / wave / discontinuity
  workflow and pick IBS vs OBS.
- The user asks "why are SO MAG L2 burst gaps present?" or "which is the
  default science frame?"
- A PSP × SO joint analysis needs SO B in a frame matching FIELDS MAG
  ([[bale-2016-fields-instrument-suite-psp]]).

Do NOT invoke this skill when:

- The question is about RPW search-coil B (high-frequency only) — different
  product.
- The question is about Solar Orbiter ephemeris — use
  [[muller-2020-solar-orbiter-mission-overview]].

## Paper identity and claim boundary

- **Title:** The Solar Orbiter Magnetometer
- **First author:** Timothy S. Horbury
- **Authors:** T. S. Horbury, H. O'Brien, I. Carrasco Blázquez,
  M. Bendyk, P. Brown, R. Hudson, V. Evans, et al. ("+ co-authors —
  TODO verify full list with primary source")
- **Year:** 2020
- **Venue:** Astronomy & Astrophysics, 642, A9 (Solar Orbiter special issue)
- **DOI:** 10.1051/0004-6361/201937257 (TODO verify with primary source)
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes MAG **as designed and commissioned in
  2020**: sensors, electronics, observing modes (normal / burst), nominal
  noise floors and timing precision, and the intended L1/L2 product
  hierarchy. On-orbit performance under maneuvers / VGAs is documented
  separately.

## Scientific or methodological claim to operationalize

> SO/MAG consists of two redundant fluxgate sensors mounted on the
> deployable boom — the **Inboard Sensor (IBS)** and **Outboard Sensor
> (OBS)** — each providing vector B sampling. Normal-mode cadence is
> typically 8 vec/s, burst-mode up to 64 vec/s (TODO verify exact values).
> L2 products are calibrated, despun, and rotated to the **science frames
> (RTN, SRF)**. The agent contract for SO magnetic-field access is set by
> this paper.

A HelioSI skill operationalizes this by: given an interval and science
question, return the *MAG contract* (sensor, level, mode, cadence, frame,
known caveats).

## Required data / instruments / code / archives

- **SO/MAG IBS L2 (normal):** ~ 8 vec/s; primary inertial-range product.
- **SO/MAG OBS L2 (normal):** ~ 8 vec/s; cross-check / spacecraft-field
  removal.
- **SO/MAG burst L2:** ~ 64 vec/s (TODO verify); event-triggered.
- **Frames:** RTN (default), SRF (spacecraft reference frame), J2000 / HCI
  via SPICE.
- **Archives:** ESA SOAR (`solo_L2_mag-*-normal*`,
  `solo_L2_mag-*-burst*`); CDAWeb mirror.

## Algorithm / workflow steps

1. **Pick sensor.** Default IBS for science; OBS for cross-check; both
   when characterizing spacecraft-generated fields.
2. **Pick mode.** Normal for inertial-range / large-scale; burst for
   wave-mode / shock-crossing analyses.
3. **Pick cadence.** Match downstream analysis Nyquist; do not assume
   continuous burst availability.
4. **Pick frame.** RTN by default; SRF for spacecraft-attitude
   diagnostics.
5. **Cross-check IBS vs OBS.** Subtract OBS – IBS to estimate spacecraft-
   generated magnetic background — flag intervals with anomalous
   residuals.
6. **Persist contract** with sensor, mode, cadence, frame, and SPICE
   kernel version.

```python
def so_mag_contract(question, interval, frame="RTN"):
    sensor = pick_sensor(question)        # IBS | OBS | BOTH
    mode = pick_mode(question)            # normal | burst
    cadence = {"normal": "8 vec/s", "burst": "64 vec/s"}[mode]
    return {"instrument": "SO/MAG", "sensor": sensor, "mode": mode,
            "cadence": cadence, "frame": frame, "interval": interval,
            "archive": "SOAR"}
```

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that loads SO/MAG L2 normal-mode IBS for a sample 2022
interval, computes |B| stats, and matches published median |B| values to
within ~ 5 % at 0.3 au heliocentric distance (TODO supply specific
interval and target from full text).

## Known pitfalls / failure modes

- **Spacecraft-generated fields.** OBS – IBS residual reveals spacecraft-
  generated DC fields modulated by heater / wheel / reaction-control
  activity; always flag.
- **Burst-mode gaps.** Burst is event-triggered; do not assume continuous
  coverage.
- **Frame mismatch.** Mixing SRF and RTN silently corrupts cross-mission
  analyses with PSP.
- **Maneuver / VGA exclusion.** Around Venus gravity assists, MAG data
  should be flagged because attitude changes invalidate despin.
- **Time-tag offsets.** SO/MAG and SO/SWA use independent timing; require
  interpolation onto common grid before joint moments / Alfvénic
  diagnostics.
- **Boom-deployment effect on baseline.** Early-mission intervals may
  retain residual baseline offsets while boom thermal equilibration was
  ongoing — see commissioning reports.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — SO/MAG IBS+OBS sensor inventory and modes | **Verifiable task:** `so_mag_contract(question, interval) -> JSON` |
| Methods — sensor / mode / frame selection, IBS–OBS cross-check | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — IBS L2, OBS L2, burst L2 | **MCP / tool contracts:** SOAR REST / `pyspedas.solar_orbiter` |
| Caveats — spacecraft fields, burst gaps, frame, VGA exclusion, time-tag | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — boom geometry, sensor noise floor | **Benchmark artifacts:** noise-floor + residual plot |

## Claim boundary

**In scope.** SO/MAG **as designed and commissioned in 2020** — sensors,
modes, nominal cadence, calibration plan, intended L2 products.

**Out of scope — do NOT generalize beyond:**

- Do not assert on-orbit noise floors below the published nominal values
  without later commissioning sources.
- Do not infer SWA / RPW / EPD contracts from this paper.
- Do not use SO/MAG burst as a substitute for RPW B (high-frequency).

## Links

- DOI: 10.1051/0004-6361/201937257 — TODO verify with primary source.
- arXiv: n/a.
- ADS: TODO_verify_with_full_text.
- Code: `pyspedas.solar_orbiter.mag` loaders.
- Data: ESA SOAR; CDAWeb mirror.

## Skill graph → depends_on

- `[[muller-2020-solar-orbiter-mission-overview]]` — orbit / ephemeris
  context.
- `[[owen-2020-solo-swa-plasma-suite]]` — paired plasma contract.
- `[[damicis-2025-solo-swa-alfvenic-streams-validation]]` — Alfvénic
  workflow using SO/MAG + SWA.

## References

- Horbury et al. (2020), *Astronomy & Astrophysics*, 642, A9 —
  not-in-local-inventory; bibliographic fields TODO verify with full text.
