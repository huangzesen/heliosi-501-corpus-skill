---
name: paper-malaspina-2016-psp-fields-dfb-digital-fields-board
description: >-
  Use when retrieving PSP/FIELDS DFB-derived AC/DC waveform, bandpass, and
  spectrogram products (electric and magnetic spectra) — central claim is that
  DFB digital filtering produces compressed AC spectra, waveform captures, and
  band-integrated power that are the routine FIELDS science products for waves
  and turbulence (Malaspina et al. 2016, JGR-Space).
version: 0.1.0
kind: paper-skill
quality: method-ready
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: The Digital Fields Board for the FIELDS Instrument Suite on Parker Solar Probe
  first_author: "Malaspina, D. M."
  year: 2016
  venue: "Journal of Geophysical Research: Space Physics"
  doi: 10.1002/2016JA022344
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: psp_data
  secondary_themes: []
  missions:
    - PSP
  regime:
    - inner-heliosphere
    - ion-scale
    - MHD-scale
trigger_keywords:
  - PSP FIELDS DFB
  - Malaspina 2016
  - digital fields board
  - PSP wave spectrum
  - PSP electric field
  - FIELDS waveform capture
  - PSP band-integrated power
data_products:
  - instrument: PSP/FIELDS DFB AC spectrum
    level: L2
    cadence: 1 min
    interval: null
    archive: SPDF / PSP SOC
  - instrument: PSP/FIELDS DFB band-integrated power
    level: L2
    cadence: 2 s
    interval: null
    archive: SPDF
  - instrument: PSP/FIELDS DFB waveform captures
    level: L1/L2 burst
    cadence: event-based
    interval: null
    archive: SPDF
algorithms:
  - name: Cascaded biquad + FFT digital filter chain
    equation_refs:
      - §4 Malaspina 2016
    external_implementations: []
  - name: Antenna effective length calibration
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1002/2016JA022344"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://spdf.gsfc.nasa.gov/pub/data/psp/fields/"
claim_boundary:
  scope: >-
    DFB filters and digitizes signals from the V1-V4 antennas, SCM, MAG.
    Standard products: AC spectrum (32-channel, 1 min cadence), DC spectrum,
    waveform captures (burst), band-integrated power, cross-products.
  out_of_scope:
    - Do not treat DFB AC spectra as calibrated E in V/m without antenna effective-length correction.
    - Do not use DC-coupled DFB voltages as wind-velocity proxy without SWEAP cross-calibration.
    - Do not assume waveform captures are routinely downlinked — many are burst-triggered.
failure_modes:
  - Probe biasing changes (current bias setting) alter sensitivity — read bias keywords.
  - Antenna sheath rectification can corrupt low-frequency E spectra near perihelion.
  - DFB compression introduces frequency aliasing if a burst is decimated.
depends_on:
  - bale-2016-fields-instrument-suite-psp
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# The Digital Fields Board for the FIELDS Instrument Suite on Parker Solar Probe — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving PSP/FIELDS DFB-derived AC/DC waveform, bandpass, and spectrogram products (electric and magnetic spectra) — central claim is that DFB digital filtering produces compressed AC spectra, waveform captures, and band-integrated power that are the routine FIELDS science products for waves and turbulence (Malaspina et al. 2016, JGR-Space).

Do NOT use this skill when:

- Do not treat DFB AC spectra as calibrated E in V/m without antenna effective-length correction.
- Do not use DC-coupled DFB voltages as wind-velocity proxy without SWEAP cross-calibration.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** DFB filters and digitizes signals from the V1-V4 antennas, SCM, MAG. Standard products: AC spectrum (32-channel, 1 min cadence), DC spectrum, waveform captures (burst), band-integrated power, cross-products.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Cascaded biquad + FFT digital filter chain

- Paper reference: §4 Malaspina 2016
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Antenna effective length calibration

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| PSP/FIELDS DFB AC spectrum | L2 | 1 min | — | SPDF / PSP SOC |
| PSP/FIELDS DFB band-integrated power | L2 | 2 s | — | SPDF |
| PSP/FIELDS DFB waveform captures | L1/L2 burst | event-based | — | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Probe biasing changes (current bias setting) alter sensitivity — read bias keywords.
- Antenna sheath rectification can corrupt low-frequency E spectra near perihelion.
- DFB compression introduces frequency aliasing if a burst is decimated.

## 7. Claim boundary  *(Layer 1)*

**In scope.** DFB filters and digitizes signals from the V1-V4 antennas, SCM, MAG. Standard products: AC spectrum (32-channel, 1 min cadence), DC spectrum, waveform captures (burst), band-integrated power, cross-products.

**Out of scope — do NOT generalize beyond:**

- Do not treat DFB AC spectra as calibrated E in V/m without antenna effective-length correction.
- Do not use DC-coupled DFB voltages as wind-velocity proxy without SWEAP cross-calibration.
- Do not assume waveform captures are routinely downlinked — many are burst-triggered.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1002/2016JA022344
- arXiv: n/a
- Code: n/a
- Data / archive: https://spdf.gsfc.nasa.gov/pub/data/psp/fields/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[bale-2016-fields-instrument-suite-psp]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
