---
name: paper-maksimovic-2020-solar-orbiter-rpw-radio-plasma-waves
description: >-
  Use when retrieving Solar Orbiter / RPW radio (4 kHz–16 MHz) and in-situ wave
  (DC–1 MHz) products — central claim is that RPW provides high-resolution radio
  dynamic spectra and time-domain plasma-wave waveform captures plus quasi-
  thermal noise (QTN) electron-density estimates (Maksimovic et al. 2020, A&A).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: The Solar Orbiter Radio and Plasma Waves (RPW) instrument
  first_author: "Maksimovic, M."
  year: 2020
  venue: "Astronomy & Astrophysics"
  doi: 10.1051/0004-6361/201936214
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_orbiter
  secondary_themes: []
  missions:
    - Solar Orbiter
  regime:
    - inner-heliosphere
trigger_keywords:
  - Solar Orbiter RPW
  - Maksimovic 2020
  - radio plasma waves
  - QTN density
  - TNR HFR
  - type III burst Solar Orbiter
  - SCM search coil Solar Orbiter
data_products:
  - instrument: SO/RPW TNR
    level: L2
    cadence: ~16 s spectrum
    interval: null
    archive: SOAR
  - instrument: SO/RPW HFR
    level: L2
    cadence: ~7 s spectrum
    interval: null
    archive: SOAR
  - instrument: SO/RPW TDS waveform
    level: L2 burst
    cadence: event-based
    interval: null
    archive: SOAR
  - instrument: SO/RPW LFR
    level: L2
    cadence: various
    interval: null
    archive: SOAR
algorithms:
  - name: "Quasi-thermal noise (QTN) inversion → Ne, Te"
    equation_refs:
      - §6 Maksimovic 2020
    external_implementations: []
  - name: Type-III radio burst frequency-time tracking
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1051/0004-6361/201936214"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://soar.esac.esa.int/"
claim_boundary:
  scope: >-
    SO/RPW comprises ANT (three monopole antennas), MAG-SCM (search-coil
    magnetometer), TDS (time domain sampler), TNR (thermal noise receiver,
    4-1024 kHz), HFR (high frequency receiver, 0.4-16 MHz), LFR (low frequency
    receiver, DC-100 kHz).
  out_of_scope:
    - Do not treat ANT measurements as calibrated E without antenna response model.
    - "Do not assume QTN density is reliable in dense streams (>200 cm⁻³ at 1 au) without separate validation."
    - Do not use HFR for type III bursts below 4 kHz — that is below sampling.
failure_modes:
  - Antenna bias sweep epochs leave artifact lines in spectra.
  - QTN fits unstable when local plasma frequency outside receiver band.
  - Solar array EMI features at known frequencies; consult instrument-team blacklist.
depends_on:
  - muller-2020-solar-orbiter-mission-overview
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
# The Solar Orbiter Radio and Plasma Waves (RPW) instrument — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving Solar Orbiter / RPW radio (4 kHz–16 MHz) and in-situ wave (DC–1 MHz) products — central claim is that RPW provides high-resolution radio dynamic spectra and time-domain plasma-wave waveform captures plus quasi-thermal noise (QTN) electron-density estimates (Maksimovic et al. 2020, A&A).

Do NOT use this skill when:

- Do not treat ANT measurements as calibrated E without antenna response model.
- Do not assume QTN density is reliable in dense streams (>200 cm⁻³ at 1 au) without separate validation.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SO/RPW comprises ANT (three monopole antennas), MAG-SCM (search-coil magnetometer), TDS (time domain sampler), TNR (thermal noise receiver, 4-1024 kHz), HFR (high frequency receiver, 0.4-16 MHz), LFR (low frequency receiver, DC-100 kHz).

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Quasi-thermal noise (QTN) inversion → Ne, Te

- Paper reference: §6 Maksimovic 2020
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Type-III radio burst frequency-time tracking

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SO/RPW TNR | L2 | ~16 s spectrum | — | SOAR |
| SO/RPW HFR | L2 | ~7 s spectrum | — | SOAR |
| SO/RPW TDS waveform | L2 burst | event-based | — | SOAR |
| SO/RPW LFR | L2 | various | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Antenna bias sweep epochs leave artifact lines in spectra.
- QTN fits unstable when local plasma frequency outside receiver band.
- Solar array EMI features at known frequencies; consult instrument-team blacklist.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SO/RPW comprises ANT (three monopole antennas), MAG-SCM (search-coil magnetometer), TDS (time domain sampler), TNR (thermal noise receiver, 4-1024 kHz), HFR (high frequency receiver, 0.4-16 MHz), LFR (low frequency receiver, DC-100 kHz).

**Out of scope — do NOT generalize beyond:**

- Do not treat ANT measurements as calibrated E without antenna response model.
- Do not assume QTN density is reliable in dense streams (>200 cm⁻³ at 1 au) without separate validation.
- Do not use HFR for type III bursts below 4 kHz — that is below sampling.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1051/0004-6361/201936214
- arXiv: n/a
- Code: n/a
- Data / archive: https://soar.esac.esa.int/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[muller-2020-solar-orbiter-mission-overview]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
