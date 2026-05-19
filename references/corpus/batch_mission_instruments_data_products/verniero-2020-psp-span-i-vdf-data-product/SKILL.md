---
name: verniero-2020-psp-span-i-vdf-data-product
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# verniero-2020-psp-span-i-vdf-data-product

## When to use this paper-skill

Invoke when a HelioSI workflow needs **PSP/SWEAP SPAN-Ai 3D ion VDFs**
operationalized as a callable data product — the worked example from
Verniero et al. 2020 demonstrating how to load SPAN-Ai VDFs during high
ion-scale wave-power intervals, isolate proton-beam populations, and feed
the VDFs into linear-Vlasov stability analysis. Typical triggers:

- An agent must read SPAN-Ai L2/L3 ion VDFs (`spi_sf00`) and reduce them
  to 2D / 1D distributions.
- A wave–particle / ion-cyclotron-instability workflow is needed.
- An agent is choosing between SPC moments and SPAN-Ai VDFs for proton
  microphysics (see [[kasper-2016-sweap-investigation-psp]]).

Do NOT invoke this skill when:

- Only bulk moments are needed (use SPC products).
- The interval lies outside SPAN-Ai's FoV with no beam coverage — VDF
  shape will be biased.

## Paper identity and claim boundary

- **Title:** Parker Solar Probe Observations of Proton Beams Simultaneous
  with Ion-Scale Waves
- **First author:** J. L. Verniero
- **Authors:** J. L. Verniero, D. E. Larson, R. Livi, A. Rahmati, et al.
  ("+ co-authors per inventory")
- **Year:** 2020
- **Venue:** The Astrophysical Journal Supplement Series, 248, 5
- **DOI:** 10.3847/1538-4365/ab86af (confirmed in
  `apj_aa_heliophysics_papers.md`)
- **arXiv:** 2004.03009 — in local inventory.
- **Claim boundary:** Operationalizes SPAN-Ai 3D VDFs during PSP first
  encounter (E1) on intervals identified as containing high ion-scale
  wave power. Bounded to the encounter(s) and event windows analyzed in
  the paper — the methodology generalizes, but the *numerical* beam
  characteristics and instability identifications do not extend beyond
  the analyzed intervals without re-running.

## Scientific or methodological claim to operationalize

> During PSP intervals with high ion-scale wave power, SPAN-Ai 3D ion VDFs
> reveal **field-aligned proton beams** that drive linear-Vlasov
> instabilities — ion-cyclotron and/or magnetosonic — identifiable in the
> dispersion-relation analysis of the measured VDF. The SPAN-Ai VDF
> product, together with FIELDS MAG, is sufficient to perform this
> identification.

A HelioSI skill operationalizes this by: given a PSP interval, fetch
SPAN-Ai VDFs and FIELDS MAG; rotate VDFs into the field-aligned frame;
extract proton core + beam parameters; run a linear-Vlasov solver; report
the unstable mode (if any).

## Required data / instruments / code / archives

- **PSP/SWEAP SPAN-Ai L2/L3 ion VDFs** (`spi_sf00` 3D distributions;
  cadence ~ 0.87 s at E1 (TODO verify) per [[kasper-2016-sweap-
  investigation-psp]]).
- **PSP/FIELDS MAG L2** (RTN B at matching cadence) per
  [[bale-2016-fields-instrument-suite-psp]].
- **Linear-Vlasov solver:** community tools such as `PLUME`, `LEOPARD`,
  `NHDS` — exact tool used by authors TODO verify with full text.
- **Archives:** NASA SPDF / CDAWeb; SWEAP Berkeley data center.

## Algorithm / workflow steps

1. **Identify candidate interval** with elevated ion-scale wave power
   (e.g. FIELDS MAG PSD in the 0.1–5 Hz band above a threshold).
2. **Fetch SPAN-Ai VDFs** for the interval; verify FoV completeness (beam
   not occluded; cf. [[kasper-2016-sweap-investigation-psp]] failure mode).
3. **Rotate VDFs** into field-aligned coordinates using the matching
   FIELDS MAG B direction.
4. **Fit core + beam** populations as bi-Maxwellians; extract n_b/n_c,
   v_b/v_A, parallel/perpendicular temperatures.
5. **Run linear-Vlasov solver** with measured parameters; identify the
   most-unstable mode and its frequency / growth rate.
6. **Cross-check** the mode against the observed FIELDS MAG / DFB wave
   spectrum.

```python
def span_ai_proton_beam_instability(interval):
    vdf = load_span_ai_sf00(interval)             # 3D ion VDF
    b_rtn = load_fields_mag_l2(interval)
    vdf_par = rotate_to_field_aligned(vdf, b_rtn)
    core, beam = fit_bi_maxwellians(vdf_par)
    mode = solve_linear_vlasov(core, beam)        # PLUME/LEOPARD/NHDS
    return {"interval": interval, "core": core, "beam": beam, "mode": mode}
```

## Minimal executable benchmark or validation target

- **Claim:** During the named E1 intervals with high ion-scale wave power,
  the inferred unstable mode matches the observed wave frequency (ion-
  cyclotron or magnetosonic).
- **Metric:** Predicted vs observed wave frequency in proton-rest frame.
- **Tolerance:** within a factor of 2 (TODO refine with full text).
- **Reference figure:** TODO identify figure number in Verniero+ 2020
  (inventory snippet refers to "linear Vlasov stability analysis; ion-
  cyclotron / magnetosonic instability identification").

## Known pitfalls / failure modes

- **SPAN-Ai partial FoV at perihelion.** If the proton beam center lies in
  the heat-shield-shadow occluded cone, the fitted beam density is biased
  low (or the beam is missed entirely).
- **Coarse angular bins.** Thin beams may occupy 1–2 angle bins; fit
  uncertainties are large.
- **Doppler-shift to proton frame.** Observed frequency must be Doppler-
  shifted from spacecraft frame to plasma frame using V_sw and B
  direction.
- **Bi-Maxwellian assumption.** Some VDFs are tri-component or non-
  Maxwellian; fit residuals must be inspected.
- **Mag vs SPAN time alignment.** Use the same cadence / interpolation
  scheme; mismatches change the rotated VDF shape.
- **Solver convergence.** Linear-Vlasov solvers can return spurious modes
  in extreme parameter regimes — apply known guardrails (k ranges,
  starting frequency).

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — proton beams + ion-scale waves explained by linear-Vlasov modes | **Verifiable task:** `span_ai_proton_beam_instability(interval) -> {core, beam, mode}` |
| Methods — VDF rotation, bi-Maxwellian fits, linear-Vlasov solver | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — SPAN-Ai VDFs + FIELDS MAG | **MCP / tool contracts:** SWEAP + FIELDS L2 fetches via harness fallback |
| Caveats — partial FoV, coarse bins, Doppler shift, fit ambiguity | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures / table — beam parameters and dispersion comparison | **Benchmark artifacts:** VDF slice PNG + dispersion overlay |

## Claim boundary

**In scope.** SPAN-Ai 3D VDF workflow applied to PSP **first encounter (E1)
intervals with high ion-scale wave power**, restricted to the events in
the paper. The skill is a callable VDF + stability pipeline within this
scope.

**Out of scope — do NOT generalize beyond:**

- Do not extend numerical beam densities / drift speeds to other
  encounters or wind types without re-running.
- Do not claim that SPAN-Ai resolves all proton-beam populations — partial
  FoV and angular resolution limit detectability
  ([[kasper-2016-sweap-investigation-psp]]).
- Do not assume the matched linear mode is unique without cross-checking
  alternative modes in the solver.

## Links

- DOI: https://doi.org/10.3847/1538-4365/ab86af
- arXiv: https://arxiv.org/abs/2004.03009
- ADS: TODO_verify_with_full_text.
- Code: TODO — solver (PLUME / LEOPARD / NHDS) — exact tool TODO verify.
- Data: NASA SPDF / CDAWeb (`PSP_SWP_SPI_SF00*`, `PSP_FLD_L2_MAG_RTN_*`).

## Skill graph → depends_on

- `[[kasper-2016-sweap-investigation-psp]]` — SPAN-Ai sensor description.
- `[[bale-2016-fields-instrument-suite-psp]]` — paired FIELDS MAG.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — E1 encounter
  identification.

## References

- Verniero et al. (2020), *ApJS*, 248, 5; DOI 10.3847/1538-4365/ab86af;
  arXiv:2004.03009. Inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md §2.7`.
