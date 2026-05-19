---
name: mccomas-2016-isois-energetic-particle-investigation-psp
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# mccomas-2016-isois-energetic-particle-investigation-psp

## When to use this paper-skill

Invoke when a HelioSI workflow needs the **canonical PSP/ISʘIS instrument
description** — EPI-Lo (low-energy) + EPI-Hi (high-energy) telescope
inventory, energy / species coverage, look directions, and L2/L3 product
names. Typical triggers:

- An agent is about to load PSP energetic-particle (SEP / suprathermal /
  ACR) time series and must choose EPI-Lo vs EPI-Hi and the correct look
  direction.
- The user asks "what are the ISʘIS energy ranges and pixel layout?"
- A heliospheric-current-sheet / reconnection / SEP-event workflow
  (e.g. [[murtas-2026-hcs-reconnection-ion-energization]] in
  `pilot_2026_and_runtime/`) needs the energetic-particle contract paired
  with FIELDS B + SWEAP plasma.

Do NOT invoke this skill when:

- The question is about thermal plasma (< ~ 20 keV) — that is SWEAP
  ([[kasper-2016-sweap-investigation-psp]]).
- The question is about magnetic / electric fields — that is FIELDS
  ([[bale-2016-fields-instrument-suite-psp]]).

## Paper identity and claim boundary

- **Title:** Integrated Science Investigation of the Sun (ISʘIS) — Design
  of the Energetic Particle Investigation
- **First author:** David J. McComas
- **Authors:** D. J. McComas, N. Alexander, N. Angold, S. Bale, C. Beebe,
  B. Birdwell, M. Boyle, J. M. Burgum, J. A. Burnham, et al. ("+ many co-
  authors — TODO verify full list with primary source")
- **Year:** 2016
- **Venue:** Space Science Reviews — *Parker Solar Probe* special issue
- **DOI:** 10.1007/s11214-014-0059-1 (TODO verify with primary source)
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes ISʘIS **as designed**: EPI-Lo (8 octagonal
  Time-of-Flight + energy windows) and EPI-Hi (LET / HET silicon
  telescopes). On-orbit performance, pixel-by-pixel response calibration,
  and event-by-event background subtractions are documented separately.

## Scientific or methodological claim to operationalize

> ISʘIS measures energetic ions and electrons from suprathermal to ~ 100
> MeV/nuc, separating species via Time-of-Flight + residual-energy
> (EPI-Lo, ~ keV/nuc – 1 MeV/nuc) and ΔE-E silicon stacks
> (EPI-Hi LETA/B, HETA/B; ~ 1 – 100 MeV/nuc). The pixelated FoVs allow
> first-order pitch-angle reconstruction relative to the local FIELDS
> magnetic field. The agent contract for PSP energetic-particle access is
> set by this paper.

A HelioSI skill operationalizes this by: given an interval and energy /
species of interest, return the *energetic-particle contract* (telescope,
pixel set, energy bin, product, archive).

## Required data / instruments / code / archives

Sensors / products described:

- **EPI-Lo:** 8 wedges of TOF + energy detectors covering ~ 30 keV/nuc –
  ~ 1 MeV/nuc protons; H, He, heavier ion separation; electrons up to
  ~ 100 keV (TODO verify exact ranges).
- **EPI-Hi LETA / LETB:** Low-Energy Telescopes A / B, ~ 1 – 20 MeV/nuc ions.
- **EPI-Hi HETA / HETB:** High-Energy Telescopes A / B, ~ 10 – 100 MeV/nuc
  ions; up to several MeV electrons.
- **Products:** `PSP_ISOIS_EPILO_L2_*`, `PSP_ISOIS_EPIHI_L2_*`,
  `PSP_ISOIS_L3_SUMMARY_*` (TODO verify exact L3 product names).
- **Archives:** NASA SPDF / CDAWeb; ISʘIS / PSP SOC at Princeton.
- **Frames:** Sky-pixel / look-direction frame; pitch-angle derived from
  FIELDS MAG B.

## Algorithm / workflow steps (data-contract construction)

1. **Identify energy / species.** Map science question to one telescope:
   suprathermal ions → EPI-Lo; SEP > ~ 1 MeV/nuc → EPI-Hi LET; SEP >
   ~ 10 MeV/nuc → EPI-Hi HET; relativistic electrons → EPI-Hi HET.
2. **Pick product.** L2 differential intensities by default; L3 summary
   for event onset / fluence statistics.
3. **Pick pixels / look directions.** Use the full pixel set for
   omnidirectional intensities; subset for pitch-angle reconstruction.
4. **Anchor pitch angle to B.** Provide the matching FIELDS MAG L2 product
   (cadence to match the ISʘIS bin width).
5. **Identify SEP-event onset.** Use L3 onset flags or compute by
   intensity thresholds.
6. **Persist contract** with pixel selection, energy bins, and matched B.

```python
def isois_contract(species, energy_range_MeV, interval, encounter):
    telescope = pick_telescope(species, energy_range_MeV)  # epilo | leta | letb | heta | hetb
    pixels = pick_pixels(species)                          # int or list
    product = pick_product(telescope, level="L2")
    return {"telescope": telescope, "product": product, "pixels": pixels,
            "energy_range_MeV": energy_range_MeV, "interval": interval,
            "encounter": encounter, "archive": "SPDF/CDAWeb"}
```

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that, given a known SEP event interval (e.g. encounter
with a published event in [[mccomas-2016-isois-energetic-particle-
investigation-psp]] follow-ups), produces an onset-time estimate and
power-law fit reproducing the published values within ~ 20 %. TODO supply
concrete event reference from full text.

## Known pitfalls / failure modes

- **Look-direction biases.** Single-pixel intensities are anisotropic;
  always state which pixels were summed.
- **Background separation.** Galactic and anomalous cosmic-ray backgrounds
  contaminate quiet-time spectra at the high-energy end; subtract per
  product spec.
- **Cross-channel pile-up.** In intense SEP events, EPI-Hi channels can
  pile up; check live-time flags.
- **Electrons vs ions confusion at low energies.** EPI-Lo separation
  depends on TOF/E; verify with anti-coincidence flags.
- **Pitch-angle ambiguity at sector boundaries.** Pixel boundary regions
  have lower effective area — pitch-angle bins should track the matching
  FIELDS B with the same cadence; mismatched cadences smear PA.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — ISʘIS telescope inventory and intended energy / species coverage | **Verifiable task:** `isois_contract(species, energy_range_MeV, interval) -> JSON` |
| Methods — telescope / pixel selection, pitch-angle anchoring | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — EPI-Lo + EPI-Hi LETA/B, HETA/B | **MCP / tool contracts:** `cdaweb-mcp.get_psp_isois_*` or harness fallback |
| Caveats — look-direction bias, background, pile-up, e–p confusion, PA bin mismatch | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — telescope layout (Fig 4, Fig 6) | **Benchmark artifacts:** pixel-overlay plot for an encounter |

## Claim boundary

**In scope.** ISʘIS **as-designed** energetic-particle suite — telescopes,
energy ranges, species coverage, pixel layout, intended L2/L3 products.
The skill returns contracts, not science conclusions.

**Out of scope — do NOT generalize beyond:**

- Do not quote numerical energy spectra without a specific event reference
  (event-specific paper-skills do that).
- Do not infer thermal-plasma / magnetic-field contracts from this paper.
- Do not assume omnidirectional response without pixel averaging.

## Links

- DOI: 10.1007/s11214-014-0059-1 — TODO verify with primary source.
- arXiv: n/a.
- ADS: TODO_verify_with_full_text.
- Code: n/a (instrument paper).
- Data: NASA SPDF / CDAWeb — `PSP_ISOIS_*`; Princeton SOC mirror.

## Skill graph → depends_on

- `[[bale-2016-fields-instrument-suite-psp]]` — required for pitch-angle
  reconstruction.
- `[[kasper-2016-sweap-investigation-psp]]` — thermal-suprathermal anchor.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — encounter context.

## References

- McComas et al. (2016), *Space Science Reviews*; PSP special issue —
  not-in-local-inventory; bibliographic fields TODO verify.
