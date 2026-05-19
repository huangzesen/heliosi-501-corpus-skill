---
name: kasper-2016-sweap-investigation-psp
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# kasper-2016-sweap-investigation-psp

## When to use this paper-skill

Invoke when a HelioSI workflow needs the **canonical PSP/SWEAP instrument
description** — Solar Probe Cup (SPC) and SPAN-{Ai, Ae, B} field-of-view,
energy ranges, moment vs VDF products, and partial-FoV caveats. Typical
triggers:

- An agent is about to load PSP proton moments (`spi_moms` / `spc_l3i`) or
  3D ion VDFs (`spi_sf00`) and must choose between SPC and SPAN-Ai.
- The user asks "why is SPC saturated near perihelion?" or "is SPAN-Ai
  view complete?".
- A switchback / Alfvénicity / cross-helicity workflow needs the *plasma
  moment contract* paired with FIELDS B
  ([[bale-2016-fields-instrument-suite-psp]]).
- A wave-particle / ion-beam analysis needs full-3D VDFs
  (see [[verniero-2020-psp-span-i-vdf-data-product]]).

Do NOT invoke this skill when:

- The question is purely about FIELDS magnetic / electric measurements.
- The science is about energetic particles > ~ 20 keV/q — that is ISʘIS
  ([[mccomas-2016-isois-energetic-particle-investigation-psp]]).

## Paper identity and claim boundary

- **Title:** Solar Wind Electrons Alphas and Protons (SWEAP) Investigation —
  Design of the Solar Wind and Coronal Plasma Instrument Suite for Solar
  Probe Plus
- **First author:** Justin C. Kasper
- **Authors:** J. C. Kasper, R. Abiad, G. Austin, M. Balat-Pichelin,
  S. D. Bale, J. W. Belcher, P. Berg, et al. ("+ many co-authors —
  TODO verify full list with primary source")
- **Year:** 2016
- **Venue:** Space Science Reviews — *Parker Solar Probe* special issue
- **DOI:** 10.1007/s11214-015-0206-3 (TODO verify with primary source)
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes SWEAP's **as-designed** capability:
  SPC (Faraday cup pointing at the Sun through the heat shield) and SPAN
  (electrostatic analyzers — SPAN-Ai, SPAN-Ae, SPAN-B). On-orbit
  performance, partial-FoV biases at perihelion, and SPAN-Ai vs SPC
  cross-calibration are addressed in later commissioning literature, not
  in this paper.

## Scientific or methodological claim to operationalize

> SWEAP measures the solar-wind core ions and electrons via two complementary
> sensors: **SPC** — sun-pointed Faraday cup, optimized for fast core proton/α
> moments in the Sun-directed beam; **SPAN-Ai/Ae/B** — top-hat ESAs giving
> 3D ion (Ai) and electron (Ae, B) VDFs with broader fields of view but
> partial occlusion by the heat shield. SWEAP delivers L2 moments
> (`sweap_spc_l3i`, `spi_moms`, `spe_moms`) and L2/L3 VDFs (`spi_sf00`).
> The agent contract for plasma-moment access on PSP is set by this paper.

A HelioSI skill operationalizes this by: given a PSP encounter / interval /
science question, return the *moment / VDF contract* (sensor, level,
cadence, frame, FoV-completeness flag).

## Required data / instruments / code / archives

Sensors / products described:

- **SPC (Solar Probe Cup):** Sun-pointed Faraday cup; differential energy
  per charge ~ 100 V – 8 kV; cadence up to ~ 0.87 s (1 Sa/NYS) in encounter
  mode (TODO verify exact value).
- **SPAN-Ai:** Top-hat ion ESA; 3D VDFs; energy ~ a few eV/q to ~ 20 keV/q
  (TODO verify); partial FoV due to heat-shield occultation.
- **SPAN-Ae, SPAN-B:** Electron ESAs on ±Y panels; combine for ~ 4π
  electron coverage modulo spacecraft-body occultation.
- **Data products:** `PSP_SWP_SPC_L3I` (proton moments), `PSP_SWP_SPI_SF00`
  (ion VDFs), `PSP_SWP_SPI_MOMS` (ion moments), `PSP_SWP_SPE_*` (electron).
- **Archives:** NASA SPDF / CDAWeb; SWEAP Berkeley Data Center.
- **Frames:** Default RTN for moments; instrument frame for VDFs.

Harness fallback: `pyspedas`, `cdflib`, plain WebFetch — no MCP assumed.

## Algorithm / workflow steps (data-contract construction)

1. **Choose sensor.** If task needs core proton bulk speed near
   perihelion → SPC (direct Sun-line). If task needs 3D ion VDF / beams /
   α populations off-axis → SPAN-Ai. If electrons → SPAN-Ae/B.
2. **Pick level / product.** Moments by default
   (`spc_l3i`, `spi_moms`, `spe_moms`); raw VDFs only when the science
   requires distribution shape.
3. **Check FoV completeness.** Flag intervals where the beam is partially
   outside SPAN-Ai FoV (causes biased moments); compare with SPC where both
   are available.
4. **Set frame.** RTN for moments; instrument frame for VDF analyses
   (with a documented rotation to RTN).
5. **Pair with FIELDS.** For any Alfvénicity / cascade workflow, the contract
   must list the matching FIELDS MAG product and cadence — see
   [[bale-2016-fields-instrument-suite-psp]].
6. **Persist contract** as JSON.

```python
def sweap_contract(question, encounter, interval, frame="RTN"):
    sensor = pick_sensor(question)           # SPC | SPAN-Ai | SPAN-Ae | SPAN-B
    product, cadence = pick_product(question)  # spc_l3i | spi_moms | spi_sf00 | ...
    fov_caveat = "partial_FoV_at_perihelion" if sensor=="SPAN-Ai" else None
    return {"sensor": sensor, "product": product, "cadence": cadence,
            "frame": frame, "fov_caveat": fov_caveat,
            "encounter": encounter, "interval": interval,
            "archive": "SPDF/CDAWeb"}
```

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that, given an encounter perihelion interval, returns
SPC + SPAN-Ai contracts, fetches both products from SPDF, and confirms
that the moment time series agree within ~ 10 % in regions where both
sensors are unsaturated and the beam is in SPAN-Ai FoV.
TODO verify quantitative cross-calibration target with full text.

## Known pitfalls / failure modes

- **SPC saturation / dynamic range.** Near perihelion, ion fluxes can
  exceed SPC's design dynamic range; the resulting moments are biased low.
- **SPAN-Ai partial FoV.** The heat-shield occults part of the Sun-ward
  cone; if the proton beam center lies in the occulted cone, SPAN-Ai
  moments are systematically *low* in density and *biased* in speed.
- **VDF angular resolution.** SPAN-Ai energy/angle bins are coarse; thin
  beams (ion-beam events) may be in only 1–2 bins. Do not over-interpret
  derivative moments.
- **Electron secondary / photoelectron contamination.** Below ~ 20 eV the
  ESA spectra contain spacecraft-produced electrons; use cuts.
- **Time-tag offsets between SPC and SPAN.** Different DPUs / instrument
  timing; require explicit re-interpolation when computing cross-products.
- **Coordinate frame.** Default RTN for moments; some L2 products are
  published in spacecraft frame — always check the CDF metadata.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — SPC + SPAN sensor inventory and intended products | **Verifiable task:** `sweap_contract(question, encounter, interval) -> JSON` |
| Methods — sensor & product selection, FoV gating | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — SPC, SPAN-Ai/Ae/B, L2 moments + L2/L3 VDFs | **MCP / tool contracts:** `cdaweb-mcp.get_psp_swp_*` or harness fallback |
| Caveats — SPC saturation, SPAN partial FoV, VDF resolution, e- contamination | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — sensor field-of-view diagrams (Fig 4–6) | **Benchmark artifacts:** sensor-overlay plot for an encounter |

## Claim boundary

**In scope.** SWEAP **as-designed** sensor suite, intended data products,
nominal cadences, and field-of-view geometry. The skill is a *contract
provider* — it does not certify on-orbit numerical performance.

**Out of scope — do NOT generalize beyond:**

- Do not assert SPC/SPAN cross-calibration ratios as numerical values —
  those come from later commissioning papers.
- Do not produce science results (e.g. switchback proton beams) — those are
  separate paper-skills (e.g.
  [[verniero-2020-psp-span-i-vdf-data-product]]).
- Do not infer ISʘIS or FIELDS contracts from this paper.

## Links

- DOI: 10.1007/s11214-015-0206-3 — TODO verify with primary source.
- arXiv: n/a (Space Science Reviews; not in local inventory).
- ADS: TODO_verify_with_full_text.
- Code: n/a.
- Data: NASA SPDF / CDAWeb — `PSP_SWP_*`.

## Skill graph → depends_on

- `[[bale-2016-fields-instrument-suite-psp]]` — paired magnetic-field
  contract; both required for plasma diagnostics.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — encounter / orbit
  context for FoV reasoning.
- `[[verniero-2020-psp-span-i-vdf-data-product]]` — concrete SPAN-Ai VDF
  use case.

## References

- Kasper et al. (2016), *Space Science Reviews*; PSP special issue —
  not-in-local-inventory; bibliographic fields TODO verify with full text.
