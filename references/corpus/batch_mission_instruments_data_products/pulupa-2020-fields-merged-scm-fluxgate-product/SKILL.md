---
name: pulupa-2020-fields-merged-scm-fluxgate-product
description: >-
  Use when a HelioSI workflow needs the PSP/FIELDS merged search-coil and
  fluxgate magnetometer ("SCaM") product — a single broadband B time series
  whose merge of MAG and SCM channels provides usable PSD power from DC to
  the SCM upper bandwidth (~1 MHz at the highest burst rate). Central paper
  is Bowen, Bale, Bonnell, Dudok de Wit, Goetz, Goodrich, Gruesbeck,
  Harvey, Jannet, Koval, MacDowall, Malaspina, Pulupa, Revillet, Sheppard,
  Szabo (2020), *JGR: Space Physics* 125(5) e2020JA027813,
  doi:10.1029/2020JA027813 (arXiv:2001.04587). The legacy slug retains
  "pulupa-2020" for cross-batch link stability; verified first author is
  T. A. Bowen.
version: 0.1.0
tags:
  - parker-solar-probe
  - fields
  - mag
  - scm
  - scam
  - merged-data-product
  - broadband-magnetic-field
  - psd-continuity
  - turbulence
  - waves
quality_level: paper-grounded-pending-full-text
executable_status: pipeline-specified-not-yet-runnable
paper:
  authors_verified: true
---

# Bowen 2020 — Merged Search-Coil + Fluxgate (SCaM) Broadband B Product for PSP/FIELDS

> Compiled from Bowen, Bale, Bonnell, Dudok de Wit, Goetz, Goodrich,
> Gruesbeck, Harvey, Jannet, Koval, MacDowall, Malaspina, Pulupa,
> Revillet, Sheppard, Szabo (2020), *A Merged Search-Coil and Fluxgate
> Magnetometer Data Product for Parker Solar Probe FIELDS*, JGR Space
> Physics 125(5) e2020JA027813, doi:10.1029/2020JA027813 (arXiv:2001.04587).
> Title, full 16-author list, journal/volume/article, DOI, and the
> abstract's "bandwidth ranging from DC to 1 MHz" claim were
> cross-checked via api.crossref.org and arxiv.org on 2026-05-19. The
> legacy slug `pulupa-2020-…` is retained for cross-batch link stability;
> verified first author is **T. A. Bowen** (UC Berkeley / SSL).
> **Quality tier**: `paper-grounded-pending-full-text` — citation,
> author order, DOI, bandwidth headline, and the algorithm's optimal-SNR
> framing are anchored to the live abstract / journal metadata; exact
> crossover frequencies, blending-filter coefficients, and figure
> numbers remain `TODO_verify_with_full_text` until the full PDF is
> available.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- A workflow needs a **single, continuous PSP/FIELDS B time series** that
  is valid through the MHD inertial range *and* into the ion-kinetic and
  electron-kinetic ranges (i.e. spans the MAG Nyquist and beyond) — the
  use-case the merged "SCaM" product was built for.
- An analysis requires **broadband PSDs of B without an inertial-to-kinetic
  spectral step** caused by MAG aliasing near Nyquist or SCM low-frequency
  rolloff.
- Switchback-boundary, kinetic-wave, or stochastic-heating workflows need
  gradients that lie **above MAG Nyquist but below the SCM upper
  bandwidth**.
- Cross-comparison of MAG vs SCM measurements during calibration or
  inter-instrument validation.

Do NOT use this skill when:

- Only inertial-range MHD turbulence is needed — MAG L2 alone usually
  suffices (see [[bale-2016-fields-instrument-suite-psp]]).
- Only AC bursts above ~10 Hz are needed — SCM L2 alone may suffice.
- The science requires wave-mode identification from the full DFB burst
  product (different L2/L3 stream; not the SCaM merge).

## 2. Paper claim → verifiable task

**Claim (narrow form, anchored to the verified abstract).** Combining
the two PSP/FIELDS fluxgate magnetometers (MAGs) with the inductively
coupled search-coil magnetometer (SCM) into a single merged "SCaM"
waveform product yields B(t) measurements whose noise floor in each
frequency band is set by the more-sensitive sensor for that band, with a
**total bandwidth from DC to ~1 MHz** at the highest burst sample rate.
The merge algorithm operates on FIELDS waveform telemetry from multiple
sensors with optimal signal-to-noise characteristics.

**Verifiable task.** A reproduction succeeds when an agent:

1. Loads, for a named PSP encounter interval, the canonical SCaM
   waveform product (CDAWeb / Berkeley FIELDS archive product name TODO
   verify against the v01/v02 CDF naming used by the FIELDS team) and
   the corresponding MAG L2 and SCM L2 streams.
2. Computes trace PSDs of all three (MAG-only, SCM-only, SCaM) over a
   quiet-interval window inside the same encounter.
3. Confirms that SCaM PSD tracks the MAG PSD below the crossover band
   (within instrumental noise), tracks the SCM PSD above the crossover
   band (within instrumental noise), and shows **no step / kink at the
   crossover band**.
4. Carries instrument-caveat metadata (SCM gain transitions, SCM
   low-frequency rolloff, MAG bandwidth limit, burst-mode availability)
   into all downstream products that use the merged stream.
5. (Promotion criterion) Reports the crossover band, blending-filter
   form, and tolerance numbers from the full PDF — currently TODO.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Source-stream load and frame harmonization

- Procedure:
  1. Pull PSP/FIELDS MAG L2 vector B (RTN or SC) at its native cadence
     for the requested interval.
  2. Pull PSP/FIELDS SCM L2 vector B (search-coil) at its native cadence
     for the same interval; record the burst-mode availability mask.
  3. Rotate to a common frame (RTN by default). MAG and SCM internal
     reference frames differ; merging requires a consistent rotation
     before any waveform blending.
  4. Resample both streams onto a common uniform time grid (millisecond
     timing offsets between sensors must be removed; the FIELDS pipeline
     uses sub-survey-period alignment).

### Algorithm 3.2 — Frequency-domain blending (SCaM merge contract)

- Procedure:
  1. Window the aligned MAG and SCM streams; take per-channel DFTs.
  2. Apply the published merge weights — high weight to MAG at f below
     the SCM low-frequency rolloff (~order 10 Hz; **exact crossover band
     TODO verify with full PDF**) and high weight to SCM above MAG's
     useful upper bandwidth.
  3. Invert the merged spectrum to time-domain B(t) on the common grid.
  4. Persist caveat metadata: `gain_state[]` time series for the SCM
     analog chain, `mag_burst_state[]` for the MAG, and a SCaM
     `quality_flag[]` per sample carrying "good", "gain-transition",
     "scm-rolloff", "mag-nyquist", or "burst-edge".

### Algorithm 3.3 — PSD-continuity check (validation contract)

- Procedure:
  1. Pick a quiet sub-interval inside the same encounter (no shocks, no
     gain-state transitions, no burst-edge artifacts).
  2. Compute trace PSDs of MAG L2, SCM L2, and SCaM over the same
     window (Welch periodogram with matched detrend / overlap).
  3. Quantify the SCaM-vs-blend residual `|log10 PSD_SCaM − log10
     PSD_blend(MAG, SCM)|` band-by-band across the crossover band.
  4. Report the median residual and worst-frequency residual. (Numerical
     tolerance: TODO supply from full PDF — the SKILL has historically
     used a 0.05-dex placeholder.)

Code skeleton (scaffold tier; runnable once the product name and merge
weights are wired):

```python
def load_scam(encounter, interval, frame="RTN"):
    cdf = fetch_cdf("PSP_FLD_L3_*_MAG_SCM_MERGED_*", interval)  # TODO verify product name
    return SCaM(
        b_vec=cdf["B"],
        frame=frame,
        cadence=cdf["CADENCE"],
        gain_state=cdf.get("SCM_GAIN_STATE"),
        burst_state=cdf.get("MAG_BURST_STATE"),
        quality_flag=cdf.get("QUALITY_FLAG"),
    )

def psd_continuity_residual(mag, scm, scam, fmin_Hz, fmax_Hz):
    f, P_mag = welch(mag.b_vec)
    _, P_scm = welch(scm.b_vec)
    _, P_scam = welch(scam.b_vec)
    blend = blend_psd(P_mag, P_scm, fmin_Hz, fmax_Hz)  # TODO verify blending coefficients
    band = (f >= fmin_Hz) & (f <= fmax_Hz)
    resid = np.abs(np.log10(P_scam[band]) - np.log10(blend[band]))
    return resid.mean(), resid.max()
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| PSP/FIELDS MAG (×2 fluxgates) | B (RTN or SC), DC-accurate | L2 vector; survey-rate sampling, burst available | E1+ (PSP launch 2018-08; first encounter 2018-11) | NASA SPDF / CDAWeb; UCB FIELDS data center | `cdaweb` |
| PSP/FIELDS SCM (search-coil) | B (RTN or SC), AC, up to ~1 MHz at highest burst | L2 vector | E1+ | NASA SPDF / CDAWeb; UCB FIELDS data center | `cdaweb` |
| PSP/FIELDS SCaM (merged) | B (RTN), DC – ~1 MHz | L3 merged waveform; exact product name TODO verify | E1+ as released | UCB FIELDS data center; NASA SPDF (mirror status TODO verify) | `cdaweb` |
| SPICE ephemeris | spacecraft position, attitude, frame transforms | L1 | Mission | NAIF | `spiceypy` / `xhelio-spice` |

## 5. Validation target → benchmark artifact

- **Claim**: SCaM waveform's PSD smoothly interpolates between the MAG
  PSD (below crossover) and the SCM PSD (above crossover), with the
  merged-stream noise floor inheriting the more-sensitive sensor in each
  band.
- **Metric**: Mean and maximum of `|log10 PSD_SCaM − log10 PSD_blend|`
  over the crossover band on a quiet sub-interval of a named encounter.
- **Tolerance**: TODO verify — the in-corpus placeholder is `≤ 0.05 dex`
  mean across the crossover band on one encounter interval; the exact
  number is paper-internal and not in the abstract.
- **Reference figure**: A SCaM-vs-MAG-vs-SCM combined PSD figure exists
  in the published article (figure number TODO verify against the full
  PDF).

Recommended check artifacts:

- `scam_psd_continuity.csv` — one row per (encounter, sub-interval): the
  median and worst residuals, fmin/fmax of the crossover band used,
  Welch parameters.
- `scam_psd_overlay.png` — log–log PSD overlay of MAG, SCM, SCaM with
  the crossover band shaded.

## 6. Failure modes → skill memory

- **SCM gain transitions.** The SCM analog chain switches gain states;
  raw merging across a transition produces step artefacts. Gate on the
  SCM gain-state metadata and exclude transitions from PSD-continuity
  checks.
- **SCM low-frequency rolloff.** Below the crossover band (order 10 Hz,
  exact value TODO verify), the SCM transfer function rolls off sharply.
  Inferring inertial-range spectral slopes from SCM alone is incorrect;
  the merge places weight on MAG there for exactly this reason.
- **MAG aliasing near Nyquist.** Using MAG alone at survey-rate cadence
  aliases above-Nyquist power into the inertial range. The merged
  product is the canonical fix — but only inside the SCaM bandwidth.
- **Frame mismatch.** MAG and SCM internal frames differ; merging in
  raw frames yields a non-physical mixed-frame vector. Always rotate to
  a common frame before blending.
- **Time-tag misalignment.** Millisecond timing offsets between MAG and
  SCM channels must be removed before blending. The FIELDS pipeline
  documents sub-survey-period timing accuracy.
- **Burst-mode availability.** SCaM cadence is not uniform across an
  encounter: outside burst windows, the merged product drops back to
  survey-rate effective cadence. Do not assume a flat cadence.
- **Mission-evolution drift.** Calibration coefficients may change with
  encounter / firmware revisions. Always pin the product version when
  citing SCaM-derived numbers.
- **Spin / shadow biases.** The MAG-side spin / shadow caveats from the
  FIELDS instrument paper still apply to the merged product; SCaM does
  not eliminate them (see [[bale-2016-fields-instrument-suite-psp]]).

## 7. Claim boundary

**In scope.** The merged SCaM waveform product as released for
PSP/FIELDS — broadband B(t) from DC to ~1 MHz at highest burst rate,
operating on the FIELDS MAG + SCM telemetry, validated by PSD continuity
across the published crossover band. The SCaM contract is the canonical
way to extract a single broadband B time series from FIELDS.

**Out of scope — do NOT generalise beyond:**

- The exact crossover band, blending coefficients, and figure-numbered
  tolerances reside in the paper PDF and are TODO verify; do not quote
  numerical values for these without verifying against the source.
- Do not assume the published blending function applies unchanged to
  later FIELDS firmware revisions or future encounters without checking
  the L3 product version.
- Do not infer spin / shadow / sensor-cross-talk corrections from this
  paper — those are documented in the FIELDS instrument paper and in
  later calibration notes, not here.
- Do not use SCaM as a substitute for DFB AC-bandwidth burst products
  in wave-mode identification — those are different L2/L3 streams.

If a downstream task asks for a generalisation listed above, refuse it
and route to the FIELDS instrument paper-skill or to the appropriate
calibration paper.

## 8. Links

- DOI: https://doi.org/10.1029/2020JA027813 — verified via Crossref
  on 2026-05-19.
- arXiv: https://arxiv.org/abs/2001.04587 — abstract verified 2026-05-19;
  16-author list confirmed.
- ADS: 2020JGRA..12527813B — derived from journal coordinates (JGR Space
  Physics 125, e2020JA027813); not directly fetched.
- Code: FIELDS Berkeley readers and the SPDF CDF tools (no single
  canonical SCaM-reader repo is published with the paper).
- Data: NASA SPDF / CDAWeb; UCB FIELDS data center
  (https://fields.ssl.berkeley.edu/).

## 9. Skill graph → depends_on

- `[[bale-2016-fields-instrument-suite-psp]]` — FIELDS sensor inventory
  and instrument-level caveats (gain stages, sensor cross-talk, spin /
  shadow biases) that survive the SCaM merge.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — encounter and
  burst-window calendar; required to pick valid intervals for
  PSD-continuity validation.

## 10. Research-generation affordances

- **Cross-encounter merge-quality drift.** Repeat the PSD-continuity
  benchmark on a matched quiet sub-interval inside each PSP encounter
  (E1 onward) and report the median residual as a time series. Trend
  changes flag firmware-revision-induced merge-quality drift not visible
  in any single-encounter analysis.
- **Switchback boundary spectral leak.** Use SCaM in the immediate
  inboard / outboard neighbourhood of catalogued switchback boundaries
  (cf. switchbacks batch) and quantify how much above-Nyquist power
  would have aliased into inertial-range spectral fits if MAG-only had
  been used. This makes "use SCaM, not MAG-only" actionable rather than
  aesthetic.
- **Joint MAG/SCM cross-calibration anchor.** The PSD-continuity
  contract here is a re-usable cross-calibration anchor for any
  workflow that combines magnetic-field channels from heterogeneous
  sensors (PSP/FIELDS, but also Solar Orbiter MAG vs RPW, see
  [[horbury-2020-solo-mag-vector-magnetometer]]).
- **Wave-mode identification with continuous broadband B.** Where DFB
  bursts are unavailable, SCaM enables identification of cyclotron-
  resonant features that previously required dedicated burst snapshots.
  Quantifying detection efficiency vs the DFB-only baseline is a
  testable affordance.

## Notes

- The legacy slug `pulupa-2020-fields-merged-scm-fluxgate-product`
  reflects an earlier inventory-time misattribution; verified first
  author is **T. A. Bowen** (UC Berkeley / SSL) and the paper is
  published as Bowen et al. 2020 in *JGR: Space Physics*. The slug is
  preserved for cross-batch link stability; the
  `slug_first_author_misnomer` metadata field carries the explicit
  correction.
- The "DC to 1 MHz" bandwidth is a published headline of the merged
  product and is verified against the abstract. The exact MAG/SCM
  crossover band and the blending-filter form are paper-internal and
  remain `TODO_verify_with_full_text`.
