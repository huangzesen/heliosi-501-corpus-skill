---
name: paper-noaa-swpc-real-time-space-weather
description: >-
  Use when fetching real-time space-weather indices (Kp, Dst proxy, F10.7, GOES
  X-ray, ACE/SWEPAM real-time, ENLIL ensemble forecasts, NOAA Solar Activity
  reports) — central claim is that NOAA SWPC is the authoritative operational
  provider of real-time space-weather information (NOAA SWPC; no single
  canonical paper in local inventory).
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
  title: NOAA Space Weather Prediction Center (SWPC) real-time data and alerts
  first_author: NOAA Space Weather Prediction Center
  year: 2024
  venue: (NOAA SWPC operational documentation; companion review Singer et al. or Onsager — TODO verify)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - ACE
  regime:
    - 1au
trigger_keywords:
  - NOAA SWPC
  - real-time space weather
  - Kp Dst real time
  - GOES XRS real time
  - WSA Enlil forecast
  - space weather alerts
  - services.swpc.noaa.gov
data_products:
  - instrument: GOES XRS real-time
    level: L1 RT
    cadence: 1 min
    interval: null
    archive: NOAA SWPC
  - instrument: ACE real-time IMF + plasma
    level: L1 RT
    cadence: real-time
    interval: null
    archive: NOAA SWPC
  - instrument: WSA-Enlil ensemble forecast
    level: forecast
    cadence: daily / event-based
    interval: null
    archive: NOAA SWPC
algorithms:
  - name: JSON time-series fetch from services.swpc.noaa.gov
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://www.swpc.noaa.gov/"
claim_boundary:
  scope: >-
    NOAA SWPC operational services: real-time products at
    https://services.swpc.noaa.gov/json/, image alerts at
    https://www.swpc.noaa.gov/, ENLIL ensemble forecasts, NOAA-scaled events
    (G/S/R scales). Many products run from CCMC / WSA-Enlil.
  out_of_scope:
    - "Do not use SWPC real-time as a scientific archive — products are operational, not science-quality."
    - Do not assume back-coverage; many JSON endpoints serve only last days/weeks.
    - Do not assume SWPC ENLIL is identical to CCMC runs-on-request ENLIL.
failure_modes:
  - "Real-time data revisions: Kp is provisional for ~hours then re-published."
  - JSON endpoints subject to schema change without notice; pin a date-stamped snapshot.
depends_on:
  []
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# NOAA Space Weather Prediction Center (SWPC) real-time data and alerts — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when fetching real-time space-weather indices (Kp, Dst proxy, F10.7, GOES X-ray, ACE/SWEPAM real-time, ENLIL ensemble forecasts, NOAA Solar Activity reports) — central claim is that NOAA SWPC is the authoritative operational provider of real-time space-weather information (NOAA SWPC; no single canonical paper in local inventory).

Do NOT use this skill when:

- Do not use SWPC real-time as a scientific archive — products are operational, not science-quality.
- Do not assume back-coverage; many JSON endpoints serve only last days/weeks.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** NOAA SWPC operational services: real-time products at https://services.swpc.noaa.gov/json/, image alerts at https://www.swpc.noaa.gov/, ENLIL ensemble forecasts, NOAA-scaled events (G/S/R scales). Many products run from CCMC / WSA-Enlil.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### JSON time-series fetch from services.swpc.noaa.gov

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| GOES XRS real-time | L1 RT | 1 min | — | NOAA SWPC |
| ACE real-time IMF + plasma | L1 RT | real-time | — | NOAA SWPC |
| WSA-Enlil ensemble forecast | forecast | daily / event-based | — | NOAA SWPC |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Real-time data revisions: Kp is provisional for ~hours then re-published.
- JSON endpoints subject to schema change without notice; pin a date-stamped snapshot.

## 7. Claim boundary  *(Layer 1)*

**In scope.** NOAA SWPC operational services: real-time products at https://services.swpc.noaa.gov/json/, image alerts at https://www.swpc.noaa.gov/, ENLIL ensemble forecasts, NOAA-scaled events (G/S/R scales). Many products run from CCMC / WSA-Enlil.

**Out of scope — do NOT generalize beyond:**

- Do not use SWPC real-time as a scientific archive — products are operational, not science-quality.
- Do not assume back-coverage; many JSON endpoints serve only last days/weeks.
- Do not assume SWPC ENLIL is identical to CCMC runs-on-request ENLIL.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://www.swpc.noaa.gov/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- No single canonical publication located; operational documentation is the primary source
