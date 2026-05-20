---
name: paper-so-phi-hrt-vector-magnetogram-radial-distance
description: >-
  Use when working with Solar Orbiter SO/PHI High-Resolution Telescope (HRT)
  vector magnetograms taken at heliocentric distances spanning 0.28–1.0 au
  during cruise and the nominal mission, where the orbit-modulated stray-light
  PSF, on-board MILOS inversion, lossy compression, and changing image scale
  (km/px) shift the effective sensitivity envelope relative to ground-based
  inversions or to SDO/HMI at 1 au. The narrow paper-anchored claim is the
  Solanki et al. 2020 SO/PHI instrument paper (A&A 642, A11; arXiv:1903.11061;
  DOI 10.1051/0004-6361/201935325) which specifies the HRT optical design,
  the on-board MILOS Milne-Eddington inversion of the Fe I 617.3 nm line, and
  the polarimetric sensitivity envelope (~1e-3 of continuum after on-board
  accumulation). Per-encounter stray-light / calibration corrections that
  vary with heliocentric distance are pending: the Sinjan+ 2024/2026 line of
  in-flight stray-light papers is referenced by the corpus but the specific
  bibliographic anchor has not been verified at this slug's verification
  pass (2026-05-19).
paper:
  authors_verified: true
  slug_includes_product_descriptor: true
---

# SO/PHI HRT Vector Magnetograms at Variable Heliocentric Distance

> Compiled with verified anchor to the SO/PHI instrument paper —
> Solanki, del Toro Iniesta, Woch, Gandorfer, Hirzberger, et al. (2020),
> *The Polarimetric and Helioseismic Imager on Solar Orbiter*,
> A&A 642, A11. arXiv:1903.11061; DOI 10.1051/0004-6361/201935325;
> CrossRef confirms 144 co-authors. The instrument paper anchors the
> hardware, MILOS inversion baseline, and polarimetric-sensitivity
> envelope but **does not** by itself specify the orbit-resolved
> stray-light correction; the in-flight Sinjan+ stray-light line cited
> in `metadata.yaml` is TODO_verify.

This file is the agent-native compiled form of the SO/PHI HRT vector-
magnetogram product, not a paper summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Pulling **SO/PHI HRT L2 vector magnetograms** (`B_los`, `B_t`, inclination, azimuth) from the Solar Orbiter Archive (SOAR) at any heliocentric distance `R_helio` between perihelion (`~0.28 au` in the nominal mission) and aphelion, and the downstream product needs the *radial-distance-dependent* part of the calibration chain to be explicit.
- Performing **PSP↔SO conjunction** source-region magnetic mapping, where SO/PHI HRT supplies a high-resolution photospheric Br patch that PFSS or NLFFF then propagates outward to PSP's footpoint estimate.
- Cross-comparing SO/PHI HRT against **SDO/HMI** during Earth-Sun-line viewing windows for cross-calibration; the inversion engines differ (MILOS on-board for PHI vs VFISV for HMI) and the comparison must hold image scale and noise floor explicitly.
- Selecting a high-resolution photospheric magnetogram for **vector-mag-driven coronal extrapolation** ([[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]], [[paper-hmi-vector-magnetogram-disambiguation-acute-angle]]) at sub-arcsec scales in AR cores during dedicated SO encounters.

Do NOT use this skill when:

- The target product is the SO/PHI **Full-Disc Telescope (FDT)** data stream — the FDT has a different optical design and stray-light envelope and is documented in a separate section of Solanki+ 2020 §3 ([[paper-source-surface-radius-optimization-eclipse-streamer]] and synoptic-product skills use FDT-class data, not HRT).
- The science question requires polar magnetic field — Solar Orbiter's high-latitude phase begins later in the mission and is out of scope for this slug.
- The agent is doing quiet-Sun internetwork polarimetry at the **photon-noise floor** without verifying that the encounter's on-board accumulation depth matches the targeted sensitivity (the published 1e-3 continuum sensitivity is an envelope, not a per-pixel guarantee at all distances).

## 2. Paper claim → verifiable task

**Anchored claim (Solanki+ 2020 §1, §3, §6).** SO/PHI on Solar Orbiter
provides two complementary telescopes — the **High-Resolution Telescope
(HRT)** with `~0.5 arcsec` per pixel imaging the Fe I 617.3 nm line with
a tunable LiNbO₃ Fabry-Perot etalon, and the **Full-Disc Telescope (FDT)**
covering the full Sun. On-board electronics perform a Milne-Eddington
inversion (**MILOS**) of the Stokes I, Q, U, V profiles to deliver
**vector magnetic field**, line-of-sight velocity, and continuum
intensity at the instrument's polarimetric-sensitivity envelope of
`~1e-3` of the continuum after accumulation. The instrument is the
first magnetograph operating far from the Sun–Earth line; per-pixel
spatial resolution scales with `R_helio` because the telescope has a
fixed angular resolution. The on-board telescope window pre-filters
incident light to `<4 %` of the unconcentrated solar flux to manage
heat load near perihelion.

**Verifiable task.** A reproduction succeeds when an agent:

1. Fetches an **SO/PHI HRT L2 vector magnetogram** from SOAR for a known encounter (e.g. one of the calibrated cruise-phase or early nominal-mission encounters) with the encounter's `R_helio` recorded in the FITS header.
2. Verifies the on-board MILOS inversion provenance flag in the L2 FITS metadata (no off-line re-inversion was needed for this verification).
3. Computes the **per-pixel image scale** `km/px = R_helio (km) × pixel_scale (rad/px)` and confirms it matches the published HRT spec.
4. Reports `B_los` and `|B|` histograms for both an AR-core patch and a quiet-Sun patch in the same image; checks that the AR-core noise floor is below the published `~1e-3` polarimetric sensitivity envelope and that the quiet-Sun patch sensitivity scales as expected with the encounter's accumulation depth.
5. (When in conjunction with HMI) Co-registers a co-temporal HMI vector magnetogram, applies a common spatial scale, and computes the **strong-field regime `B_los` cross-correlation** vs HMI within an AR core. The exact cross-calibration tolerance is **TODO_verify** against a still-pending in-flight cross-calibration paper.

The numerical *radial-distance-resolved* targets (stray-light residual
per encounter, MILOS inversion convergence rate per `R_helio` bin)
require the Sinjan+ stray-light line cited in `metadata.yaml`; that
anchor is not verified at this pass and the numerical target is
explicitly TODO at this slug.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — SO/PHI HRT L2 fetch + provenance verification

- Procedure:
  1. Resolve the target encounter and obtain the encounter window from a Solar Orbiter ephemeris source ([[paper-source-surface-radius-optimization-eclipse-streamer]] uses ephemeris but is out of scope; an in-house ephemeris MCP such as `xhelio-spice` is the only LingTai-bound option).
  2. Query SOAR for `SO/PHI HRT L2` magnetogram products in the encounter window.
  3. Open each FITS file and read: image scale (`CDELT*`), heliocentric distance (`DSUN_OBS`), inversion provenance flag (typically a header keyword indicating MILOS on-board vs ground re-inversion), and the L2 processing level marker.
  4. Reject files where the inversion provenance is ambiguous or where the on-board accumulation depth is below the science target.

### Algorithm 3.2 — Stray-light context (provenance-only; numerical correction is TODO)

- Procedure:
  1. Record the encounter's `R_helio` and the optical-window throughput specification (`<4 %` of unconcentrated solar flux per Solanki+ 2020 §3).
  2. Flag the file with the published HRT stray-light PSF identifier *if* the L2 metadata includes one; otherwise mark the file as `straylight_provenance=unverified`.
  3. Do **not** re-apply a numerical stray-light correction unless the agent has loaded a verified per-encounter PSF from a downstream paper (the Sinjan+ line referenced in `metadata.yaml` is the candidate but its anchor is **TODO_verify**).

### Algorithm 3.3 — MILOS re-inversion (optional, when Stokes profiles are available)

- Procedure:
  1. If the encounter's L1.5 Stokes I/Q/U/V data are available (not always; on-board telemetry budget limits download), load the Stokes cube.
  2. Run a Milne-Eddington inversion (MILOS or equivalent) on Fe I 617.3 nm under the same continuum-normalisation and weak-field assumptions documented in Solanki+ 2020 §6.
  3. Compare to the on-board MILOS L2 vector magnetogram pixel-by-pixel; report median residuals.
  4. **Do not** generalise residual statistics to encounters where Stokes profiles were not telemetered — the on-board inversion is the only available product in many encounters by design.

### Algorithm 3.4 — Co-aligned HMI cross-comparison (when in conjunction)

- Procedure:
  1. Identify an HMI vector magnetogram (typically the 12-min cadence `hmi.B_720s`) co-temporal with the SO/PHI HRT frame *and* with the SO/PHI viewing direction within an Earth–Sun-line conjunction tolerance.
  2. Reproject HMI onto SO/PHI's view using the Solar Orbiter ephemeris (de-projection from Earth view onto SO view; SunPy `differential_rotate` and `reproject` patterns).
  3. Apply a common spatial scale via downsampling HMI to SO/PHI HRT's image scale at the encounter's `R_helio`.
  4. Compute the AR-core `B_los` Pearson correlation and the strong-field slope `(B_los_PHI = m · B_los_HMI + c)`.
  5. Numerical target for the slope is **TODO_verify** — no published numerical target survives a verification pass at this slug.

Code skeleton (scaffold tier; runnable once a fetcher MCP is wired):

```python
# Pseudocode aligned with Solanki+ 2020 §3, §6.
import sunpy.map  # SunPy is the conventional adapter; not LingTai-bound.

def so_phi_hrt_fetch_and_qa(encounter_id, soar_client):
    files = soar_client.query_l2_hrt(encounter_id)
    qa = []
    for f in files:
        m = sunpy.map.Map(f.local_path)
        r_helio_au = m.meta['DSUN_OBS'] / 1.495978707e11
        px_arcsec = m.meta['CDELT1']
        km_per_px = (m.meta['DSUN_OBS'] / 1e3) * (px_arcsec / 206265.0)
        inv = m.meta.get('INVERSION', 'unknown').lower()
        qa.append({
            'file': f.local_path,
            'R_helio_au': r_helio_au,
            'km_per_px': km_per_px,
            'milos_onboard': inv.startswith('milos'),
            'straylight_provenance': m.meta.get('STRAYLT', 'unverified'),
        })
    return qa
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| Solar Orbiter SO/PHI HRT | `B_los`, `B_t`, inclination, azimuth, V_los, I_c | L2 vector mag (on-board MILOS inversion); cadence varies per observing programme | Cruise + nominal mission (2020-02 launch; primary science from 2022 onwards) | ESA Solar Orbiter Archive (SOAR) | SOAR HTTP / TAP query; FITS reader; verify inversion provenance |
| SDO/HMI | Vector magnetogram | `hmi.B_720s` 12-min cadence | 2010 onwards | JSOC | `drms` / `sunpy` |
| Solar Orbiter ephemeris | `R_helio`, sub-spacecraft (Lon, Lat) | per-frame | Mission | `xhelio-spice` (LingTai-bound MCP) or SPICE kernels | SPICE-based |
| SO/PHI L1.5 Stokes (optional) | I, Q, U, V cubes | L1.5; only when telemetered | Selected encounter windows | SOAR | FITS; large download |

The only LingTai-bound MCP is `xhelio-spice` (PSP/SO ephemeris). A
SOAR-aware fetcher and a SunPy-style L2 reader are required adapters
that are **not** currently bound in the corpus; surface them as
prerequisites to the runtime rather than invent a binding.

## 5. Validation target → benchmark artifact

- **Verifiable invariants from Solanki+ 2020 (anchored):**
  - HRT angular pixel scale is fixed; per-encounter `km/px` scales as `R_helio · pixel_scale`.
  - On-board polarimetric sensitivity envelope is `~1e-3` of the continuum after accumulation; agents reproducing AR-core `B_los` noise floors should land within this envelope when the on-board accumulation depth matches the published nominal observing programme.
  - On-board entrance window pre-filters `<4 %` of unconcentrated solar flux (thermal design constraint, not a polarimetric tolerance).
- **TODO_verify — not anchored at this slug:**
  - Per-encounter stray-light residual after the in-flight PSF correction (requires the Sinjan+ stray-light paper).
  - Quantitative HMI ↔ HRT cross-calibration slope `(m, c)` and residual scatter in AR cores.
  - The radial-distance-dependent `B_los` agreement tolerance referenced in earlier scaffold revisions.

Recommended check artifacts:

- `so_phi_hrt_provenance.csv` — one row per L2 file: `(t, R_helio_au, km_per_px, milos_onboard, straylight_provenance)`.
- `so_phi_hrt_vs_hmi_ar_core.json` — pairwise `B_los` cross-correlation and strong-field slope per conjunction window.
- A QA panel checking the AR-core `|B|` histogram against the `~1e-3` polarimetric sensitivity envelope.

## 6. Failure modes → skill memory

- **Stray-light is the dominant unmodelled systematic near perihelion.** Solanki+ 2020 §3 documents the entrance-window pre-filter (`<4 %` throughput) but the *in-flight* PSF correction varies per encounter and is the subject of a separate calibration line; treating an L2 file as fully calibrated without a stray-light provenance check overstates polarimetric sensitivity, especially for quiet-Sun targets.
- **Image scale at perihelion ≠ image scale at aphelion.** At `R_helio = 0.28 au` the km/px is ~3.6× finer than at 1 au. Population-statistics studies (e.g. magnetic-element size distributions) must hold image scale fixed across the sample or weight by the encounter's `km/px`.
- **On-board MILOS is the only inversion available for many encounters.** Telemetry budget often precludes downlinking the full Stokes I/Q/U/V cube; agents cannot re-invert and must accept the on-board MILOS L2 as the science product. This is a hard constraint, not a workaround.
- **On-board lossy compression** of Stokes profiles can clip Stokes-V tail amplitudes for weak-field pixels — quiet-Sun signed-flux statistics are sensitive to this and should be cross-checked against a co-temporal HMI patch where possible.
- **Pointing jitter** on small spatial scales (sub-200-km at perihelion) propagates into apparent transverse motions that can mimic flux emergence; smoothing on the published jitter envelope is required before fine-structure tracking ([[paper-coronal-plume-substructure-eui-high-cadence]] runs the analogous failure mode for EUI HRI).
- **The slug's product descriptor "radial distance" is a binning convention, not a single paper.** The corpus name suggests the calibration is *resolved* as a function of `R_helio`, but the canonical SO/PHI instrument paper (Solanki+ 2020) describes the design envelope only; the per-encounter calibration line is a body of separate papers (the Sinjan+ stray-light series is the most likely anchor, **TODO_verify**).
- **FDT ≠ HRT.** Do not mix a SO/PHI FDT product into an HRT workflow without re-validating spatial scale, accumulation depth, and inversion provenance.

## 7. Claim boundary

**In scope.** SO/PHI HRT L2 vector magnetograms across the encounter
envelope (cruise + nominal mission, `R_helio ∈ ~[0.28, 1.0] au`), AR-core
strong-field polarimetry, conjunction cross-checks against SDO/HMI,
and provenance-aware downstream use in NLFFF / PFSS extrapolations.

**Out of scope — do NOT generalise beyond:**

- The SO/PHI **FDT** product family.
- High-latitude (polar) SO/PHI observations beyond the nominal-mission envelope until the mission inclination ramp is complete.
- Quiet-Sun internetwork polarimetry at the photon-noise floor without verifying the encounter's accumulation depth.
- Per-encounter numerical stray-light or HMI cross-calibration targets — those depend on calibration papers not anchored at this slug (the Sinjan+ stray-light line is the candidate; **TODO_verify**).
- Inversion engines other than MILOS without re-running validation against the on-board MILOS L2.

If a downstream task asks for any of the above, refuse it and route to
a sibling paper-skill or surface the missing calibration anchor as a
prerequisite.

## 8. Links

- DOI: https://doi.org/10.1051/0004-6361/201935325 (Solanki+ 2020 A&A 642, A11; verified via CrossRef 2026-05-19, 144 co-authors).
- arXiv: https://arxiv.org/abs/1903.11061 (verified 2026-05-19).
- ADS: TODO verify (no fetched bibcode at this pass).
- SOAR product portal: https://soar.esac.esa.int/ (publicly accessible; specific HRT product handle TODO verify).
- Sinjan+ stray-light line referenced in `metadata.yaml`: TODO_verify_with_full_text — the specific arXiv/DOI was not anchored at this verification pass.

## 9. Skill graph → depends_on

- `[[paper-hmi-vector-magnetogram-disambiguation-acute-angle]]` — sets the disambiguation convention for the HMI side of any cross-comparison; the corresponding SO/PHI side is documented in Solanki+ 2020 §6 as the on-board MILOS azimuth disambiguation.
- `[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]` — downstream NLFFF that consumes vector magnetograms; HRT supplies the photospheric boundary condition during encounters.
- `[[paper-mdi-hmi-cross-calibration-synoptic-flux]]` — analogous cross-calibration concept across the SOHO→SDO boundary; SO/PHI ↔ HMI is the SDO→Solar-Orbiter analogue and shares the strong-field-saturating-mapping pattern.

## 10. Research-generation affordances

- **Per-encounter HMI ↔ HRT cross-calibration.** The instrument paper anchors the envelope but a *per-encounter* slope and residual-scatter ladder across the nominal-mission encounter set has not been compiled at the corpus level; a scheduled campaign would feed every downstream NLFFF/PFSS skill that consumes vector magnetograms during SO conjunctions.
- **Stray-light residual ↔ km/px.** The dominant systematic (stray-light) is also the one whose *signature* most varies with `R_helio`; an experiment that holds an AR target fixed across two encounters at very different `R_helio` and compares the `B_los` histogram after stray-light correction would directly test whether the correction is closure-tight.
- **PSP↔SO conjunction source-mapping.** SO/PHI HRT enables radial-distance-resolved photospheric boundary conditions for in-situ-anchored source-mapping ([[ervin-2024-slow-alfvenic-source-regions-pfss-psp]] is a candidate consumer when an encounter conjunction exists).
- **Cross-instrument vector-mag campaign.** SO/PHI HRT, SDO/HMI, and Hinode/SP each invert Fe I 617.3 / 630.2 with different forward models; a tri-instrument simultaneous comparison on a shared AR (when geometry permits) would directly quantify how MILOS vs VFISV vs SIR responds to the same Stokes input — the closest the community can get to a ground-truth check on photospheric vector inversions.
- **Polar-phase preparation.** The mission's later inclination ramp will deliver the first sustained polar magnetograms; pre-defining the QA pipeline (image-scale tracking, stray-light provenance, on-board accumulation depth) at this slug means the polar phase can be folded in without re-authoring the four layers.
