---
name: vourlidas-2016-wispr-imaging-instrument-psp
description: >-
  Use when a HelioSI workflow needs the canonical Parker Solar Probe
  Wide-Field Imager (WISPR) instrument contract — the two nested heliospheric
  imagers (Inner, Outer) covering a combined 95° (radial) × 58° (transverse)
  field of view, their APS CMOS detectors, the L1/L2/L3 visible-light
  product hierarchy with F-corona subtraction at L3, and the polarisation
  / vignetting / stray-light caveats that govern any white-light analysis
  from PSP. Central paper is Vourlidas, Howard, Plunkett, Korendyke,
  Thernisien, Wang, Rich, Carter, Chua, Socker, Linton, Morrill, Lynch,
  Thurn, Van Duyne, Hagood, Clifford, Grey, Velli, Liewer, Hall, DeJong,
  Mikic, Rochus, Mazy, Bothmer, Rodmann (2016), *Space Science Reviews*
  204, 83–130, doi:10.1007/s11214-014-0114-y (PSP special issue;
  online 2015-02-11).
version: 0.1.0
tags:
  - parker-solar-probe
  - wispr
  - heliospheric-imager
  - visible-light
  - f-corona-subtraction
  - j-map
  - cme-tracking
  - dust-detection
  - aps-cmos
quality_level: paper-grounded-pending-full-text
executable_status: contract-spec-only-not-yet-runnable
paper:
  authors_verified: true
---

# Vourlidas 2016 — The Wide-Field Imager for Solar Probe Plus (WISPR)

> Compiled from Vourlidas, Howard, Plunkett, Korendyke, Thernisien, Wang,
> Rich, Carter, Chua, Socker, Linton, Morrill, Lynch, Thurn, Van Duyne,
> Hagood, Clifford, Grey, Velli, Liewer, Hall, DeJong, Mikic, Rochus,
> Mazy, Bothmer, Rodmann (2016), *The Wide-Field Imager for Solar Probe
> Plus (WISPR)*, Space Science Reviews 204, 83–130
> (doi:10.1007/s11214-014-0114-y; online 2015-02-11; PSP special issue).
> Title, full 27-author list, journal volume/page range, DOI, and 2015
> online-publication date were verified against api.crossref.org on
> 2026-05-19. Combined-FoV (95° radial × 58° transverse), the
> two-nested-telescope architecture, and the radiation-hardened
> 2K × 2K APS CMOS detectors were verified against the NRL WISPR
> instrument page and the JHU-APL/PSP Wikipedia summary on 2026-05-19.
> Per-camera elongation ranges and pixel scales are paper-internal and
> the precise breakdown remains `TODO_verify_with_full_text` (Vourlidas+
> 2016 §2 reports them; the placeholder ranges used in §4 below reflect
> the inventory record and are *not* corroborated by an independent
> live fetch).
> **Quality tier**: `paper-grounded-pending-full-text` — bibliographic
> anchor, mission affiliation, combined FoV, detector technology, and
> the L1/L2/L3 product hierarchy framing are anchored; per-camera FoV
> breakdown and exact pixel scale require the full PDF.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- A workflow must load **PSP WISPR visible-light images** for a CME /
  streamer / dust / fluctuation-photometry / switchback-imaging study
  and choose between the Inner (closer-to-Sun) and Outer (wider-angle)
  cameras.
- A user asks "**how does WISPR's J-map convention work**?" / "what is
  WISPR's vignetting function or F-corona subtraction strategy?" —
  answer requires the L2 vs L3 contract Vourlidas+ 2016 establishes.
- A wave / fluctuation-photometry workflow needs **L3 background-
  subtracted images** with a documented F-corona model (rolling vs
  static) and a `kept_signal_metadata[]` flag.
- A CME-kinematic study needs the **WCS frame** for the two cameras
  (SPICE-derived) before geometric distortion at the wide-FoV edges
  biases the inferred trajectory.

Do NOT use this skill when:

- The science requires *in-situ* magnetic / plasma data — that is
  FIELDS / SWEAP / ISʘIS.
- The science is about Solar Orbiter imagers (METIS, SoloHI, EUI) —
  separate paper-skills.
- On-orbit absolute photometric calibration is the central requirement —
  use the WISPR commissioning / on-orbit calibration papers (e.g.
  Howard et al. 2019, Hess et al. 2020 — TODO add as separate
  paper-skills).

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the verified abstract framing).**
WISPR is two nested, **un-occulted heliospheric imagers** mounted on
the ram side of PSP, sharing a combined **95° × 58° (radial × transverse)
field of view** that begins inside Mercury's orbit. Inner-camera (closer
to the Sun) and Outer-camera (wider angle) sub-fields together image
the corona and inner heliosphere in visible (white) light, producing
**L1 raw**, **L2 calibrated**, and **L3 background-subtracted** image
products suitable for CME / streamer / dust / fluctuation dynamics from
inside Mercury's orbit. Detector technology is **radiation-hardened
2K × 2K APS CMOS**; image cadence at perihelion is up to 1 image per
second. The paper sets the *instrument contract* — sensor inventory,
intended cadences, F-corona subtraction strategy, and stray-light
suppression design — that every downstream WISPR analysis inherits.

**Verifiable task.** A reproduction succeeds when an agent, given an
encounter / interval / target (CME, streamer, dust), returns a JSON
*imaging contract* containing:

1. The selected camera (Inner / Outer / both) and the rationale (target
   elongation band).
2. The product level (L2 vs L3) and the rationale (visual vs
   quantitative photometry).
3. The cadence and exposure metadata from the chosen level.
4. The F-corona subtraction strategy (static model vs rolling window)
   and what it removes from the kept signal.
5. The SPICE-WCS kernel version used to convert pixel ↔ HCI /
   helioprojective coordinates.
6. The vignetting-correction status (applied or not, with paper-cited
   functional form) and the stray-light caveats that apply.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Camera selection and product-level choice

- Procedure:
  1. Resolve the target's elongation band from SPICE (using the
     encounter / interval metadata; see
     [[fox-2016-psp-mission-design-orbit-encounters]]).
  2. If the target elongation falls entirely inside the Inner-camera
     band, choose Inner; if entirely above the Inner upper cut, choose
     Outer; if it spans the join, choose both and prepare to mosaic
     across cameras.
  3. For visual inspection / morphology, take **L2 calibrated**; for
     quantitative photometry / fluctuation work, take **L3
     background-subtracted** and record the background-subtraction
     strategy in the contract.

### Algorithm 3.2 — F-corona subtraction strategy

- Procedure:
  1. Determine whether the L3 product uses a **static F-corona model**
     (leaves residuals along the symmetry axis, preserves slow CME
     signal) or a **rolling-window subtraction** (removes slow CME
     signal, suppresses residuals).
  2. Document this choice in the imaging contract — it changes apparent
     CME brightness directly.
  3. For any new L3-style analysis, validate the subtraction strategy
     against a published CME event with known kinematics.

### Algorithm 3.3 — WCS alignment via SPICE

- Procedure:
  1. Load the SPICE kernels for the spacecraft attitude and the WISPR
     camera optical-distortion model for the chosen encounter.
  2. Convert pixel coordinates to helioprojective (HPC) and
     heliocentric-inertial (HCI) coordinates using the SPICE-WCS
     transformation; pixel-level Cartesian assumptions break by ~ 1° at
     the FoV edges because of the wide field.
  3. Persist the kernel version in the imaging contract.

### Algorithm 3.4 — Time-tag convention

- Procedure:
  1. Image timestamps refer to start-of-exposure by default; for
     kinematic studies, **shift to mid-exposure** before computing
     velocities.
  2. Persist the convention used in the imaging contract.

Code skeleton (contract-spec tier; no end-to-end runnable benchmark yet):

```python
def wispr_contract(encounter, interval, target):
    elong = spice_elongation_band(encounter, interval, target)
    cam = pick_camera(elong)  # Inner / Outer / both
    level = "L3" if target.requires_photometry else "L2"
    return {
        "camera": cam,
        "level": level,
        "cadence_s": fetch_cadence_metadata(cam, level, interval),
        "f_corona_strategy": detect_f_corona_strategy(cam, level, interval),  # static | rolling
        "wcs_kernel_version": pinned_spice_kernel_version(encounter),
        "vignetting_applied": True,
        "time_tag_convention": "start-of-exposure (use +0.5*exposure for kinematics)",
        "caveats": ["dust-hits", "stray-light-residual", "geometric-distortion-edges"],
    }
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| WISPR-Inner | white-light image, closer-to-Sun camera | L1 raw / L2 calibrated / L3 F-corona-subtracted; up to 1 image/s at perihelion | E1+ (PSP launch 2018-08; first encounter 2018-11) | NASA SPDF / CDAWeb; NRL WISPR data center | `WebFetch` + FITS reader (no canonical MCP) |
| WISPR-Outer | white-light image, wider-angle camera | Same product hierarchy; lower spatial resolution than Inner | E1+ | NASA SPDF / CDAWeb; NRL WISPR data center | `WebFetch` + FITS reader |
| SPICE ephemeris + WISPR optical-distortion kernels | spacecraft attitude, camera distortion | L1 | Mission | NAIF + NRL | `spiceypy` |
| Per-camera elongation breakdown | Inner ~ 13.5°–53.5° / Outer ~ 50.5°–108.5° (TODO verify exact ranges with §2 of full PDF) | Instrument constant | Mission | Vourlidas+ 2016 | n/a |
| Combined FoV | 95° (radial) × 58° (transverse), verified against NRL WISPR page on 2026-05-19 | Instrument constant | Mission | NRL WISPR page | n/a |
| Detector | radiation-hardened 2K × 2K APS CMOS (verified against NRL page) | Instrument constant | Mission | NRL WISPR page | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: The WISPR imaging contract (camera, level, cadence,
  F-corona strategy, WCS, vignetting) is sufficient to reproduce the
  time–elongation track of a known CME on the L3 product.
- **Metric**: angular separation between agent-reproduced J-map track
  and a published-event track at matched timestamps.
- **Tolerance**: ~ 1° at fixed time on the L3 product (in-corpus
  benchmark target; the exact tolerance for any specific event is
  TODO supply with a named follow-up paper).
- **Reference figure**: the WISPR FoV diagram (Vourlidas+ 2016 — figure
  number TODO verify with full PDF); plus a published-CME J-map
  reference (event TODO identify).

Recommended check artifacts:

- `wispr_jmap_recovery.csv` — agent-reproduced time–elongation track of
  a named CME on the L3 product.
- `wispr_contract.json` — the per-event contract produced by §3.

## 6. Failure modes → skill memory

- **F-corona subtraction artifacts.** Static F-corona models leave
  residuals along the symmetry axis; rolling-window subtraction removes
  slow CME signal. Pick explicitly and persist the choice.
- **Dust / cosmic-ray hits.** Particle impacts leave saturated streaks;
  cleaning uses paired exposures or median stacking with knock-down
  thresholds.
- **Vignetting.** Off-axis vignetting is strong toward the elongation
  edges; the published vignetting function must be applied before
  photometry — its mathematical form is paper-internal (TODO verify
  with full PDF).
- **Stray-light residuals.** Sun-shield diffraction patterns leave a
  fixed pattern that must be masked; on-orbit calibration papers
  refine the mask over time.
- **Geometric distortion at FoV edges.** WISPR's wide FoV requires
  SPICE-WCS for accurate sky-coordinate conversion; pixel-level
  Cartesian assumptions break by ~ 1° at the edges.
- **Time-tag convention drift.** Image timestamps refer to
  start-of-exposure; use mid-exposure for kinematic computations.
- **Inner / Outer mosaic seam.** Mosaicking across cameras at the
  elongation join requires both cameras' vignetting functions and WCS
  to be applied identically; seam discontinuities are a common pitfall.
- **Polarisation product confusion.** WISPR supports both unpolarised
  total-brightness and polarised-brightness products; consumers must
  check the polarisation flag before any K-corona / F-corona splitting.
- **Detector radiation aging.** The APS CMOS detectors operate in a
  high-radiation environment; long-term hot-pixel growth requires
  refreshed bad-pixel masks per encounter.

## 7. Claim boundary

**In scope.** WISPR **as-designed** instrument contract — two nested
imagers with combined 95° × 58° FoV, APS CMOS detectors, L1/L2/L3
product hierarchy, F-corona / K-corona separation strategy, intended
cadences, and stray-light suppression design. The skill returns the
imaging contract; it does not certify on-orbit photometric accuracy or
absolute radiometry.

**Out of scope — do NOT generalise beyond:**

- Do not assert absolute photometric calibration without citing the
  on-orbit commissioning papers (e.g. Howard et al. 2019, Hess et al.
  2020 — TODO add as separate paper-skills when needed).
- Do not infer Solar Orbiter coronagraph contracts (METIS, SoloHI)
  from this paper — different optics and different L-product
  conventions.
- Do not draw CME-kinematic conclusions from this paper alone — those
  are reserved for dedicated event papers.
- Do not transfer the per-camera elongation breakdown beyond the
  inventory's `~ 13.5°–53.5°` / `~ 50.5°–108.5°` placeholders until the
  full PDF has been read; corroborating against §2 of Vourlidas+ 2016
  is a prerequisite.

If a downstream task asks for a generalisation listed above, refuse it
and route to the appropriate WISPR commissioning / event paper-skill.

## 8. Links

- DOI: https://doi.org/10.1007/s11214-014-0114-y — verified via
  Crossref on 2026-05-19.
- arXiv: not-in-local-inventory (the WISPR paper was published directly
  in SSRv; no arXiv preprint surfaced via search). If a preprint exists,
  TODO add.
- ADS: 2016SSRv..204...83V — derived from journal coordinates (SSRv
  204, 83–130); not directly fetched.
- Code: `sunpy` + `sunkit-image` community readers handle WISPR FITS
  files; no canonical instrument-team Python reader is published with
  this paper.
- Data: NASA SPDF (https://spdf.gsfc.nasa.gov/); NRL WISPR instrument
  data center (https://wispr.nrl.navy.mil/).

## 9. Skill graph → depends_on

- `[[fox-2016-psp-mission-design-orbit-encounters]]` — orbital /
  SPICE-WCS context; required to translate pixel coordinates to
  helioprojective / HCI frames.
- `[[bale-2016-fields-instrument-suite-psp]]` — paired in-situ B-field
  context for joint imaging + in-situ event studies (e.g. CME shock
  arrival).

## 10. Research-generation affordances

- **F-corona subtraction strategy benchmark.** Reproduce a published
  CME's J-map under both static and rolling-window subtraction and
  quantify the apparent-brightness delta per elongation. The mapping
  from subtraction choice → inferred kinematic / mass uncertainty is
  rarely reported as a single number; it should be.
- **Cross-camera mosaic continuity at the elongation join.** Build the
  per-encounter median residual at the Inner–Outer seam after applying
  the vignetting function and WCS uniformly. Trends across encounters
  flag in-flight optical-system drift not visible in any single
  encounter.
- **Detector aging tracker.** Persist a bad-pixel mask per encounter
  and report the hot-pixel growth rate. This makes a load-bearing
  instrument-housekeeping metric agent-discoverable.
- **Cross-mission heliospheric-imager bridge.** Compare WISPR vs Solar
  Orbiter SoloHI vs STEREO-A HI on shared streamer / CME events; the
  WISPR contract built here is the structural prerequisite for the
  cross-instrument intercept.

## Notes

- The per-camera elongation breakdown (`~ 13.5°–53.5°` Inner / `~
  50.5°–108.5°` Outer) carried in §4 derives from the local inventory
  records that built this skill and is *not* corroborated by an
  independent live fetch — §2 of the published Vourlidas+ 2016 PDF is
  the source of record and should be read to certify the exact
  numbers. The combined-FoV (95° × 58°) and the APS-CMOS detector
  technology were verified live against the NRL WISPR instrument page
  on 2026-05-19.
- The instrument's full author list, journal coordinates, and DOI were
  verified via Crossref on 2026-05-19; the *online* publication date
  was 2015-02-11 with the volume year typed as 2016, hence the 2016
  attribution on the slug.
