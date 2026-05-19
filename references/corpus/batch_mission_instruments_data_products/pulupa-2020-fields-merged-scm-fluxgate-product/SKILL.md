---
name: pulupa-2020-fields-merged-scm-fluxgate-product
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# pulupa-2020-fields-merged-scm-fluxgate-product

## When to use this paper-skill

Invoke when a HelioSI workflow needs **broadband (DC to ~ kHz) PSP/FIELDS
magnetic-field time series** that combines the DC-accurate fluxgate (MAG)
with the high-frequency search-coil (SCM) — i.e. the **merged SCaM
product** described in Pulupa et al. 2020. Typical triggers:

- Turbulence / wave-event workflows requiring a single continuous B
  spectrum across the inertial → ion-kinetic → electron-kinetic range.
- Switchback-boundary analysis where the gradient lies above the MAG
  Nyquist but below the SCM rolloff.
- Helmholtz / spectral-break analyses that fail when MAG alone is used
  because of aliasing near Nyquist.
- Cross-comparison of MAG vs SCM measurements during calibration.

Do NOT invoke this skill when:

- The workflow needs only inertial-range MHD turbulence — MAG L2 alone
  suffices (see [[bale-2016-fields-instrument-suite-psp]]).
- The workflow needs only AC bursts above 10 Hz — SCM alone may suffice.

## Paper identity and claim boundary

- **Title:** A Merged Search-Coil and Fluxgate Magnetometer Data Product
  for Parker Solar Probe FIELDS
- **First author:** Marc Pulupa (TODO verify with full text — inventory
  records arXiv ID only)
- **Authors:** M. Pulupa et al. ("+ FIELDS team co-authors — TODO verify
  full list with primary source")
- **Year:** 2020
- **Venue:** Journal of Geophysical Research: Space Physics (TODO verify)
- **DOI:** TODO_verify_with_full_text
- **arXiv:** 2001.04587 — in local inventory
  (`arxiv_papers/extended_search.md §3.3` and §3.9 mirror).
- **Claim boundary:** Describes a **merged data product** combining MAG
  and SCM channels in their respective optimal frequency ranges with a
  documented blending function. The claim is bounded to the SCaM product
  as released, on PSP encounters available at publication
  (E1–E4 era).

## Scientific or methodological claim to operationalize

> The Search-Coil and Magnetometer (SCaM) product merges the DC-accurate
> fluxgate (MAG) measurement with the high-frequency search-coil (SCM)
> measurement using a frequency-domain blending function so that the
> resulting time series is **valid from DC to the SCM upper bandwidth**,
> while remaining noise-floor-limited only by the better sensor in each
> band.

A HelioSI skill operationalizes this by: given an encounter interval,
return a contract for the SCaM product (cadence, blending crossover, gain
limitations) and a validation that its PSD smoothly interpolates between
the MAG and SCM PSDs over the crossover band.

## Required data / instruments / code / archives

- **PSP/FIELDS MAG L2** (fluxgate vector B, ~ 4 Sa/cyc default; up to ~ 293
  Sa/s burst — TODO verify).
- **PSP/FIELDS SCM L2** (search-coil 3-axis; up to ~ MHz).
- **PSP/FIELDS SCaM L3** (merged product; cadence and naming TODO verify
  with primary source — likely `PSP_FLD_L3_MERGED_MAG_SCM_*`).
- **Archives:** NASA SPDF / CDAWeb; FIELDS Berkeley data center.
- **Reference frames:** RTN by default; SC frame on request.
- **Inventory snippet:** "FIELDS instrument provides in-situ EM-field
  measurements via two fluxgate magnetometers and a search-coil
  magnetometer; merged data product is described."
  (`extended_search.md §3.3`)

## Algorithm / workflow steps

1. **Resolve interval, encounter, frame** using
   [[fox-2016-psp-mission-design-orbit-encounters]].
2. **Load SCaM L3** for the interval; on miss, fall back to loading MAG
   L2 + SCM L2 and merging locally per the paper's blending recipe (TODO
   reproduce blending function from full text).
3. **Identify crossover band** (Hz range where MAG noise floor crosses
   SCM noise floor; ~ 1 – 10 Hz, TODO verify exact band).
4. **Validate PSD continuity** by computing PSD of SCaM and comparing to
   MAG-only PSD below crossover and SCM-only PSD above; require a smooth
   transition (no step).
5. **Carry caveat metadata** into downstream products: SCaM gain
   transitions in burst-mode regions, SCM low-frequency rolloff, MAG
   bandwidth limit.

```python
def load_scam(encounter, interval, frame="RTN"):
    cdf = fetch_cdf("PSP_FLD_L3_MERGED_MAG_SCM_*", interval)  # TODO verify product name
    return SCaM(b_vec=cdf["B"], frame=frame, cadence=cdf["CADENCE"],
                caveats=["check_gain_transition", "scm_rolloff_low",
                         "mag_nyquist_high"])
```

## Minimal executable benchmark or validation target

- **Claim:** SCaM PSD smoothly interpolates between MAG and SCM PSDs.
- **Metric:** | log10(PSD_SCaM) − log10(PSD_blend(MAG, SCM)) | over the
  crossover band.
- **Tolerance:** ≤ 0.05 dex on average across the crossover band on at
  least one named encounter interval (TODO supply specific interval from
  full text).
- **Reference figure:** Figure showing combined PSD (TODO identify figure
  number from full text).

## Known pitfalls / failure modes

- **Gain transitions.** SCM electronics include gain-switching; merged
  product can show step artefacts at transitions — flag using gain bits.
- **SCM low-frequency rolloff.** Below ~ 10 Hz the SCM transfer function
  rolls off; the blending function must give weight to MAG there. Using
  SCM alone for inertial-range slopes is incorrect.
- **MAG aliasing near Nyquist.** When MAG alone is used at 4 Sa/cyc
  cadence, power above Nyquist aliases into the inertial range; SCaM
  avoids this.
- **Frame mismatch between MAG and SCM.** Internal frames differ; merging
  requires consistent rotation to a common frame before blending.
- **Time-tag alignment.** MAG and SCM may have small (ms) timing offsets;
  resampling onto a common grid is required.
- **Burst-mode availability.** SCaM cadence drops outside burst windows;
  do not assume uniform sampling across an encounter.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — SCaM merged broadband B product | **Verifiable task:** `load_scam(encounter, interval) -> SCaM` + PSD-continuity check |
| Methods — frequency-domain blending of MAG + SCM | **Executable workflow:** §"Algorithm / workflow steps" 1–5 |
| Data / instruments — MAG L2, SCM L2, SCaM L3 | **MCP / tool contracts:** `cdaweb-mcp.get_psp_fld_*` or harness fallback |
| Caveats — gain transitions, rolloff, aliasing, frame, time-tag, burst gaps | **Skill memory:** §"Known pitfalls / failure modes" |
| Figure — combined PSD example | **Benchmark artifact:** PSD overlay PNG comparing MAG / SCM / SCaM |

## Claim boundary

**In scope.** The merged SCaM product as released for PSP/FIELDS,
restricted to encounters available at publication (E1–E4 era; TODO verify
explicit list with full text). The skill validates broadband B for use
across inertial, ion-kinetic, and electron-kinetic ranges only inside
this restriction.

**Out of scope — do NOT generalize beyond:**

- Do not assume the same blending function applies unchanged to later
  encounters / firmware updates without checking the L3 product version.
- Do not infer that SCaM removes spin / shadow biases — those caveats from
  [[bale-2016-fields-instrument-suite-psp]] still apply.
- Do not use SCaM as a substitute for full DFB AC-bandwidth bursts in
  wave-mode identification — different products.

## Links

- DOI: TODO_verify_with_full_text.
- arXiv: https://arxiv.org/abs/2001.04587
- ADS: TODO_verify_with_full_text.
- Code: TODO — community FIELDS-Berkeley readers may exist.
- Data: NASA SPDF / CDAWeb; FIELDS Berkeley data center.

## Skill graph → depends_on

- `[[bale-2016-fields-instrument-suite-psp]]` — FIELDS sensor inventory and
  caveats.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — encounter / burst-
  window context.

## References

- Pulupa et al. (2020), arXiv:2001.04587. Inventory entry:
  `sioulas-reproduction/results/arxiv_papers/extended_search.md §3.3`
  (and §3.9 mirror).
