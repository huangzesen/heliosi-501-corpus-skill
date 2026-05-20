---
name: paper-gong-network-synoptic-magnetogram-product
description: >-
  Use when ingesting GONG (Global Oscillation Network Group) ground-based
  synoptic line-of-sight magnetograms — daily updated Earthside maps plus
  per-Carrington-rotation synoptic maps — as the photospheric boundary
  condition for PFSS / global MHD coronal models, or as the long-baseline
  alternative to space-based MDI/HMI synoptic Br products. Central
  verifiable anchor at this slug is the GONG project paper: Harvey, Hill,
  Hubbard, Kennedy, Leibacher, et al. (1996), "The Global Oscillation
  Network Group (GONG) Project", Science 272, 1284 (DOI
  10.1126/science.272.5266.1284, CrossRef-verified 2026-05-19), which
  defines the six-station ground network and its observational design.
  Modern GONG synoptic-magnetogram products are operated by NSO's
  Integrated Synoptic Program; specific calibration/cross-validation
  papers (Petrie+ 2014, Riley+ 2014 multi-observatory comparisons) are
  referenced but not anchored at this slug.
paper:
  authors_verified: true
---

# Harvey 1996 — The GONG Network as a Synoptic Magnetogram Source

> Compiled with verified anchor to:
>   Harvey, J. W.; Hill, F.; Hubbard, R. P.; Kennedy, J. R.; Leibacher,
>   J. W.; Pintar, J. A.; Gilman, P. A.; Noyes, R. W.; Title, A. M.;
>   Toomre, J.; Ulrich, R. K.; Bhatnagar, A.; Kennewell, J. A.;
>   Marquette, W.; Patrón, J.; Saá, O.; Yasukawa, E. (1996),
>   *The Global Oscillation Network Group (GONG) Project*,
>   Science **272**, 1284–1286.
>   DOI: 10.1126/science.272.5266.1284 (CrossRef-verified, 2026-05-19,
>   17 co-authors).
> Note: the Harvey+ 1996 paper anchors the **GONG project and network**
> as a six-station Doppler/helioseismic facility. The dedicated
> *magnetogram* product line and its cross-calibration to MDI/HMI rest
> on a later body of NSO Integrated Synoptic Program work (Petrie+
> 2014, Riley+ 2014, Bertello+ 2014 / Hughes+ 2016 family). Those
> downstream calibration papers are referenced below but their specific
> DOIs / arXiv IDs are **TODO_verify** at this verification pass.

This file is the agent-native compiled form of the GONG synoptic
magnetogram product, not a paper summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Selecting a **photospheric Br boundary condition** for a PFSS or global coronal MHD model in an interval where SDO/HMI is unavailable (pre-2010), where Earthside continuity is critical, or where the SDO/MDI gap (post-2010 / pre-HMI) must be bridged.
- Using **GONG daily synoptic maps** for near-real-time coronal modeling (the daily product blends Earthside-observed flux with a far-side extrapolation, in contrast to a true end-of-rotation Carrington synoptic).
- Driving a **long-baseline PFSS / open-flux ladder** that spans multiple solar cycles where space-based magnetographs do not provide unbroken coverage; GONG's continuous ground-based operation since the mid-1990s anchors the long baseline.
- Comparing **MDI ↔ HMI ↔ GONG** synoptic flux for cross-instrument calibration ([[paper-mdi-hmi-cross-calibration-synoptic-flux]] is the SOHO-SDO bridge; GONG is the ground-based long-baseline alternative).
- Testing the **open-flux problem** sensitivity to boundary-condition choice ([[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]) by swapping the input synoptic map between HMI and GONG and measuring the open-flux delta.

Do NOT use this skill when:

- The science target requires per-pixel strong-field vector inversion — GONG is line-of-sight only, ground-based; for vector magnetograms route to [[paper-hmi-vector-magnetogram-disambiguation-acute-angle]] or SO/PHI.
- The product is needed on sub-arcsec spatial scales — GONG's ground-based resolution is degraded by seeing; use the GONG synoptic as a *patch-integrated* Br product, not as a pixel-resolved magnetogram.
- Polar Br is the load-bearing input — polar field is filled in by NSO ISP via extrapolation/historical interpolation; reliability degrades near solar minimum (the polar-fill-in problem).

## 2. Paper claim → verifiable task

**Anchored claim (Harvey+ 1996 Science 272, 1284).** GONG is a network
of **six identical ground-based instruments** distributed in longitude
to provide near-continuous (`~93 %` site-network duty cycle) Doppler
and intensity observations of the Sun for **helioseismology**. The
1996 anchor paper describes the network design, sites, instrument
identity, observing programme, and the original helioseismology goals
(global p-mode mode-frequency monitoring, time-distance helio-
seismology, far-side imaging). Magnetograms are produced from the
GONG instruments' polarization-modulation channel (the GONG+
upgrade extended this capability through the late 1990s and 2000s);
**the magnetogram product line as it exists today is an extension of
the Harvey+ 1996 design, operated by NSO's Integrated Synoptic Program
(ISP).**

**Status of the synoptic-magnetogram product line.** The specific
*synoptic Br* products (daily updated Earthside maps plus end-of-
rotation Carrington maps), their flux calibration vs MDI/HMI, and the
polar-fill-in scheme rest on a body of post-1996 NSO ISP work (Petrie+
2014; Riley+ 2014 multi-observatory comparisons; Bertello+ 2014 /
Hughes+ 2016 series). **At this verification pass none of these
downstream calibration papers has been bibliographically anchored at
this slug**; the slug's narrow paper-grounded claim is the Harvey+
1996 anchor only, and the calibration/cross-validation numbers
referenced below are **TODO_verify**.

**Verifiable task.** A reproduction succeeds when an agent:

1. Resolves a target Carrington Rotation (CR) and fetches the corresponding GONG synoptic Br map from NSO's GONG data portal (or via JSOC where mirrored).
2. Records the product class (`mrnqs` / `mrmqs` / similar — NSO ISP product code; **TODO_verify** the canonical handle), the spatial grid, and the polar-fill-in provenance.
3. Resamples to the downstream PFSS / MHD grid (e.g. a regular `(lon, lat)` grid at the model's resolution).
4. Computes unsigned total flux `Φ_unsigned = ∫|Br| dA` and signed Br net flux as a global integrity check; expects the **sign-balanced** invariant within the synoptic-map noise floor.
5. (When MDI/HMI overlap is available) Compares unsigned total flux against the co-rotation HMI synoptic; the expected qualitative behaviour is that **GONG and HMI agree at the 10 %–30 % level** on unsigned flux, with GONG underestimating polar flux near minima (the precise tolerance, by CR and by cycle phase, is **TODO_verify** against Riley+ 2014 / Petrie+ 2014).
6. Drives the downstream PFSS / MHD model with the resampled map and surfaces any open-flux discrepancy vs an HMI-driven run.

The numerical 10 %–30 % flux-agreement band stated above is *folk
knowledge* from the NSO ISP / community-reference body of work; it is
**not** anchored at this slug and should be retrieved from the relevant
calibration paper before being asserted.

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — GONG synoptic Br fetch + provenance

- Procedure:
  1. Resolve the target CR from a chronology table.
  2. Query the NSO GONG synoptic product server for the corresponding **end-of-rotation Carrington Br synoptic map** (or, for near-real-time work, the **daily updated synoptic** at the target date).
  3. Open the FITS file and record: spatial grid, time stamp, product code, polar-fill-in flag, and any noted observatory outages during the CR.
  4. Reject maps where extended outages or polar-fill-in flags indicate the product is below the science-target quality bar.

### Algorithm 3.2 — Grid resampling + PFSS / MHD ingest

- Procedure:
  1. Resample the GONG Br map onto the downstream model's lat-lon grid (e.g. a 180×360 or 360×720 regular grid) preserving signed Br via area-weighted interpolation.
  2. Renormalise net flux if the downstream PFSS / MHD code requires sign-balanced input (PFSS does; many MHD ingest pipelines do).
  3. Pass to the PFSS / global MHD solver.

### Algorithm 3.3 — Integrity checks

- Procedure:
  1. Unsigned total flux `Φ_unsigned` vs the previous CR (expect smooth variation; jumps flag outages).
  2. Signed net flux ≈ 0 within map noise.
  3. (Optional, when MDI/HMI overlap exists) Unsigned-flux ratio `Φ_GONG / Φ_HMI` on the same CR — qualitative expectation 0.7–1.3 (Riley+ 2014 / Petrie+ 2014 family; **TODO_verify**).

Code skeleton (scaffold tier; assumes SunPy + drms-style adapters —
not LingTai-bound):

```python
# Pseudocode aligned with NSO ISP synoptic product conventions.
import sunpy.map
import numpy as np

def ingest_gong_synoptic(cr_number, gong_client):
    f = gong_client.fetch_synoptic_carrington(cr_number)
    m = sunpy.map.Map(f.local_path)
    flux_unsigned = np.sum(np.abs(m.data) * cell_area(m))
    flux_net = np.sum(m.data * cell_area(m))
    polar_provenance = m.meta.get('POLAR_FILL', 'unverified')
    return m, flux_unsigned, flux_net, polar_provenance
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| GONG (six-station network) | Line-of-sight magnetogram (full-disc, daily) | L2 magnetogram + daily/CR synoptic Br | 1995-onwards (network); modern magnetogram product since the GONG+ upgrade era — exact start date TODO_verify | NSO GONG data portal | HTTP / FITS |
| GONG synoptic Br | Br on a regular lat-lon grid | per-CR Carrington synoptic + daily updated synoptic | Same | NSO GONG | FITS reader |
| SDO/HMI (cross-comparison) | Synoptic Br | per-CR | 2010 onwards | JSOC | `drms` |
| SOHO/MDI (cross-comparison) | Synoptic Br | per-CR | 1996–2010 | JSOC | `drms` |

The NSO GONG portal is publicly accessible. No LingTai-bound MCP is
known; a SunPy / drms-style adapter must be wired by the consuming
runtime — surface as a prerequisite rather than invent a binding.

## 5. Validation target → benchmark artifact

- **Anchored, reproducible target (Harvey+ 1996):** The GONG network is six-station, ground-based, with `~93 %` network-level observing duty cycle; the project's design is for **near-continuous** observation of the Sun.
- **TODO_verify (numerical targets typically reported in calibration papers downstream of Harvey+ 1996):**
  - Unsigned-flux agreement vs HMI synoptic to within `~10 %–30 %` per CR (Riley+ 2014 / Petrie+ 2014 family — anchor not verified at this pass).
  - Polar-fill-in reliability near solar minimum (the dominant systematic for PFSS open-flux estimates).
  - Daily-synoptic farside-extrapolation scheme description (the daily product blends Earthside-observed flux with a farside model; the exact scheme is an NSO ISP product spec).

Recommended check artifacts:

- `gong_synoptic_provenance.csv` — one row per CR: `(CR, t_start, t_end, polar_fill_flag, outage_minutes, Φ_unsigned, Φ_signed)`.
- `gong_vs_hmi_unsigned_flux.csv` — per-CR ratios where overlap exists.
- A PFSS open-flux ladder driven by GONG (one CR per row) for an open-flux problem sensitivity test.

## 6. Failure modes → skill memory

- **Polar fill-in is the dominant systematic.** Near solar minimum, the polar Br is sparsely sampled (low-latitude orbit + viewing geometry); NSO ISP fills using a combination of historical interpolation and a smoothing scheme. PFSS open-flux estimates driven by GONG underestimate polar open flux during minima — pair the entry with [[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]] when interpreting open-flux ladders.
- **Daily synoptic ≠ Carrington synoptic.** The daily product mixes Earthside-observed flux with a farside extrapolation; treating it as a fully-observed map biases the farside region. For PFSS in steady-state mode, prefer the end-of-rotation Carrington synoptic; for near-real-time space-weather work, accept the daily product but flag the farside provenance.
- **Ground-based seeing degrades quiet-Sun S/N.** The published unsigned-flux numbers are mostly driven by active-region flux; quiet-Sun internetwork is below the GONG noise floor. Do not use individual GONG pixels as a strong-field magnetogram — integrate over patches.
- **Site outages cluster.** Bad-weather correlations across nearby stations (e.g. all three Southern-hemisphere stations during a weather event) reduce coverage in specific Carrington-longitude bands; the per-CR map's effective coverage is *not* uniform in longitude. The product file's outage log is the load-bearing diagnostic.
- **Cross-instrument flux calibration is cycle-phase-dependent.** GONG/MDI calibration constants and GONG/HMI calibration constants differ; do not promote a single ratio to all cycles. Anchor the calibration to the relevant downstream paper before asserting a number.
- **The slug's narrow paper anchor is the Harvey+ 1996 project paper.** Magnetogram-product-specific numerical claims (10 %–30 % HMI agreement, polar-fill-in reliability tolerance, etc.) live in *separate* downstream calibration papers (Petrie+ 2014, Riley+ 2014, Bertello+ 2014). Until those are anchored at this slug, treat them as folk-knowledge guidance, not paper-grounded targets.

## 7. Claim boundary

**In scope.** GONG synoptic Br as a PFSS / global MHD boundary
condition, the long-baseline ground-based alternative to MDI/HMI, and
cross-comparison against MDI/HMI on overlapping CRs.

**Out of scope — do NOT generalise beyond:**

- Per-pixel strong-field magnetogram products — GONG is patch-integrated, not a pixel-resolved magnetogram.
- Polar Br claims during solar minimum without explicitly accepting the polar-fill-in caveat.
- Daily synoptic Br on the farside without recording the farside-extrapolation provenance.
- Vector magnetic field — GONG is LOS only.
- Specific numerical cross-calibration tolerances against HMI/MDI — those depend on calibration papers **TODO_verify** at this slug.

If a downstream task asks for any of the above, refuse it and route to
a sibling paper-skill or surface the missing calibration anchor as a
prerequisite.

## 8. Links

- DOI: https://doi.org/10.1126/science.272.5266.1284 (Harvey+ 1996 Science 272, 1284–1286; CrossRef-verified 2026-05-19, 17 co-authors).
- arXiv: not applicable — the 1996 Science paper predates routine arXiv deposition for solar physics; no arXiv ID expected.
- ADS: TODO verify (no bibcode fetched at this pass; expected bibcode 1996Sci...272.1284H).
- NSO GONG data portal: https://gong.nso.edu/data/ (public).
- Downstream calibration papers referenced but **TODO_verify** at this slug: Petrie+ 2014, Riley+ 2014 multi-observatory comparison, Bertello+ 2014 / Hughes+ 2016 NSO ISP series.
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`.

## 9. Skill graph → depends_on

- (no upstream paper-skill in the corpus — GONG is itself the boundary-condition source)

## Skill graph → consumed by

- `[[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]` — open-flux ladder; the boundary-condition choice (GONG vs HMI) is a load-bearing knob.
- `[[paper-mdi-hmi-cross-calibration-synoptic-flux]]` — analogous cross-calibration concept; GONG is the third leg in the long-baseline triangle.
- `[[paper-source-surface-radius-optimization-eclipse-streamer]]` — PFSS source-surface tuning; sensitive to the input synoptic map.
- `[[paper-csss-current-sheet-source-surface-non-radial-open-flux]]` — CSSS model boundary condition.
- `[[paper-arge-2003-wsa-model-source-surface-wind-prediction]]` — WSA empirical model; long-baseline runs use GONG.

## 10. Research-generation affordances

- **Systematic cycle-phase QA of polar fill-in.** A campaign that re-runs PFSS open-flux estimates on every CR from 1996 to today using **only** GONG, then again using HMI/MDI, would expose the polar-fill-in systematic as a function of cycle phase. The expected signature: GONG/HMI open-flux ratio dips at minima. Tying this to the open-flux-problem literature ([[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]) is a high-value cross-batch experiment.
- **Long-baseline cross-instrument triangulation.** GONG + MDI/HMI + Wilcox Solar Observatory + ground-based VSM/SOLIS form a four-instrument long-baseline ladder; a coordinated unsigned-flux audit across the four would yield a *cycle-resolved* cross-calibration table that the corpus currently lacks.
- **Daily-synoptic-driven near-real-time PFSS.** The daily GONG synoptic is the only continuously-updating Br product suitable for routine space-weather PFSS; quantifying the open-flux error introduced by the daily product's farside extrapolation (vs the end-of-rotation Carrington synoptic) is a directly actionable forecasting question.
- **Cross-batch coupling to [[paper-arge-2003-wsa-model-source-surface-wind-prediction]] (WSA).** WSA-driven solar-wind predictions are sensitive to boundary-condition choice; an explicit GONG-vs-HMI WSA forecast skill comparison would be a clean cross-batch experiment.
- **Anchor-completion.** A high-priority follow-on for this slug is to anchor the Petrie+ 2014 / Riley+ 2014 / Bertello+ 2014 calibration papers at the corpus level so the numerical cross-calibration claims become paper-grounded rather than folk-knowledge.
