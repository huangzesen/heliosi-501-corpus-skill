# vourlidas-2016-wispr-imaging-instrument-psp

## When to use this paper-skill

Invoke when a HelioSI workflow needs the **canonical PSP/WISPR
imaging-instrument description** — the two heliospheric imagers (WISPR-Inner,
WISPR-Outer), their elongation FoVs, intended L2/L3 image-product names,
and the polarization / vignetting / F-corona caveats that govern any
visible-light imaging analysis from PSP. Typical triggers:

- An agent must load PSP WISPR images for a CME / streamer / dust /
  switchback-imaging study and choose between Inner (~ 13.5° – 53.5°
  elongation) and Outer (~ 50.5° – 108.5°) cameras
  (TODO verify exact angles with primary source).
- The user asks "what is WISPR's vignetting function / J-map convention?"
- A wave-imaging / fluctuation-photometry workflow needs L3 background-
  subtracted images with documented F-corona model.

Do NOT invoke this skill when:

- The science requires *in-situ* magnetic / plasma data — those are
  FIELDS / SWEAP / ISʘIS.
- The question is about Solar Orbiter imagers (METIS, SoloHI, EUI) —
  separate paper-skills.

## Paper identity and claim boundary

- **Title:** The Wide-Field Imager for Solar Probe Plus (WISPR)
- **First author:** Angelos Vourlidas
- **Authors:** A. Vourlidas, R. A. Howard, S. P. Plunkett, C. M. Korendyke,
  A. F. R. Thernisien, D. Wang, et al. ("+ co-authors — TODO verify
  full list with primary source")
- **Year:** 2016
- **Venue:** Space Science Reviews — *Parker Solar Probe* special issue
- **DOI:** 10.1007/s11214-014-0114-y (TODO verify with primary source)
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes WISPR **as designed**: two cameras with
  unpolarized + polarized visible-light imaging, intended cadences, F-
  corona / K-corona separation strategy, and stray-light suppression. On-
  orbit photometric calibration is documented in later commissioning
  papers (e.g. Hess+ 2020, Howard+ 2022 — TODO add to corpus when needed).

## Scientific or methodological claim to operationalize

> WISPR images the corona and heliosphere in **white light** from two
> heliospheric imagers (Inner ~ 13.5° – 53.5° and Outer ~ 50.5° – 108.5°
> elongation) on PSP's ram side, producing L2 calibrated images and L3
> background-subtracted (F-corona removed) images suitable for CME / streamer
> / dust dynamics from inside Mercury's orbit. The agent contract for PSP
> visible-light imaging is set by this paper.

A HelioSI skill operationalizes this by: given an encounter / interval /
target (CME, streamer, dust), return the *imaging contract* (camera, level,
cadence, FoV, F-corona subtraction strategy).

## Required data / instruments / code / archives

Sensors / products described:

- **WISPR-Inner:** white-light imager, ~ 13.5° – 53.5° elongation
  (TODO verify), Bayer-pattern CCD or 2K APS (TODO verify); cadences
  ~ minutes at encounter.
- **WISPR-Outer:** ~ 50.5° – 108.5° elongation; lower spatial resolution.
- **Products:** L1 raw, L2 calibrated, L3 background-subtracted (F-
  corona model removed). Exact CDF / FITS product naming TODO verify with
  primary source (likely `PSP_WISPR_L2_*` / `PSP_WISPR_L3_*`).
- **Archives:** NASA SPDF; NRL WISPR data center.
- **Frames:** Helioprojective / world coordinates (HPC, HCI) via SPICE
  kernels; J-map (elongation–time) for CME tracking.

## Algorithm / workflow steps (data-contract construction)

1. **Choose camera.** Target < ~ 50° elongation → Inner; > ~ 50° → Outer;
   wide-angle CME tracking → both.
2. **Pick level.** Visual inspection → L2 calibrated; quantitative
   photometry of CME / fluctuation → L3 background-subtracted.
3. **Set cadence.** Encounter-mode burst cadence vs cruise; load the
   matching exposure / integration metadata.
4. **F-corona subtraction strategy.** Document whether L3 uses a static
   F-corona model or a rolling-window subtraction; this choice changes
   apparent CME brightness.
5. **WCS alignment.** Use SPICE-kernel WCS (see
   [[fox-2016-psp-mission-design-orbit-encounters]]) to convert pixel to
   elongation / HCI position angle.
6. **Persist contract** with camera, level, cadence, background strategy,
   and SPICE kernel version.

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that opens an L3 WISPR encounter dataset, generates a
J-map for a known CME, and reproduces the published time–elongation track
within an angular tolerance of ~ 1° at fixed time. TODO supply concrete
event and figure reference from a follow-up paper.

## Known pitfalls / failure modes

- **F-corona subtraction artifacts.** Static F-corona models leave
  residuals along the symmetry axis; rolling-window subtractions remove
  slow CME signal. Choose explicitly.
- **Dust impacts / particle hits.** Cosmic-ray and dust-grain hits leave
  saturated pixels; clean using paired exposures.
- **Vignetting.** Off-axis vignetting is strong toward elongation edges;
  apply published vignetting function before photometry.
- **Stray-light residuals.** Sun-shield diffraction patterns persist; mask
  the known fixed pattern.
- **Geometric distortion.** WISPR's wide FoV requires SPICE WCS — pixel-
  level Cartesian assumptions break by ~ 1° at edges.
- **Time tagging.** Image timestamps refer to start-of-exposure; use mid-
  exposure for kinematics.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — WISPR Inner+Outer camera inventory and intended product hierarchy | **Verifiable task:** `wispr_contract(target, encounter, interval) -> JSON` |
| Methods — camera selection, level/cadence, F-corona subtraction | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — WISPR-I, WISPR-O, L1/L2/L3 images | **MCP / tool contracts:** harness fallback (`WebFetch` + FITS reader) — no MCP assumed |
| Caveats — F-corona artifacts, vignetting, stray light, distortion, time-tag | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — FoV diagram (Fig 4) | **Benchmark artifacts:** J-map PNG + WCS-validated overlay |

## Claim boundary

**In scope.** WISPR **as-designed** instrument — FoVs, intended products,
intended calibration strategy. The skill returns the imaging contract; it
does not certify on-orbit photometric accuracy.

**Out of scope — do NOT generalize beyond:**

- Do not assert absolute photometric calibration without citing a
  commissioning paper (e.g. Hess+ 2020 — TODO add).
- Do not infer Solar Orbiter coronagraph contracts (METIS, SoloHI) from
  this paper.
- Do not produce CME-kinematic conclusions from this paper alone — those
  are event papers.

## Links

- DOI: 10.1007/s11214-014-0114-y — TODO verify with primary source.
- arXiv: n/a.
- ADS: TODO_verify_with_full_text.
- Code: SunPy / sunkit-image WISPR readers (community) — no official link.
- Data: NASA SPDF; NRL WISPR data center.

## Skill graph → depends_on

- `[[fox-2016-psp-mission-design-orbit-encounters]]` — SPICE WCS context.
- `[[bale-2016-fields-instrument-suite-psp]]` — joint analyses combine in-
  situ B with WISPR imaging.

## References

- Vourlidas et al. (2016), *Space Science Reviews*; PSP special issue —
  not-in-local-inventory; bibliographic fields TODO verify.
