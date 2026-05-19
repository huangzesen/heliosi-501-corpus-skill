---
name: paper-ccmc-iswa-integrated-space-weather-analysis
description: >-
  Use when assembling near-real-time and historical multi-source space-weather
  displays (in-situ L1, magnetograms, SWMF/ENLIL forecasts, kp/dst, GOES X-ray)
  without having to manually fetch each source — central claim is that iSWA at
  CCMC aggregates dozens of data and model layers into a single configurable
  dashboard with API access (Pulkkinen 2011 Space Weather).
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
  title: CCMC iSWA — Integrated Space Weather Analysis platform
  first_author: CCMC team (Pulkkinen et al.)
  year: 2010
  venue: (CCMC iSWA project documentation; companion Pulkkinen 2011 Space Weather)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - 1au
trigger_keywords:
  - iSWA
  - CCMC iSWA
  - Pulkkinen 2011
  - integrated space weather analysis
  - near real time space weather
  - ENLIL viewer
data_products:
  - instrument: ACE/Wind real-time IMF + plasma via iSWA
    level: L1 RT
    cadence: real-time
    interval: null
    archive: CCMC iSWA
  - instrument: ENLIL forecast (heliospheric MHD)
    level: forecast
    cadence: run-based
    interval: null
    archive: CCMC iSWA
algorithms: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://iswa.ccmc.gsfc.nasa.gov/"
claim_boundary:
  scope: >-
    iSWA: 'Integrated Space Weather Analysis' system at CCMC/GSFC. Hosts near-
    real-time data feeds and CCMC simulation outputs, exposes image/timeseries
    APIs, and offers user-configurable layouts.
  out_of_scope:
    - Do not assume iSWA hosts science-grade Level-2 — it pulls real-time / Level-1 streams.
    - Do not use iSWA as the authoritative archive for any single instrument — go to the source.
failure_modes:
  - Real-time feeds may show artifact dropouts the science-quality product later corrects.
  - iSWA aggregator caches images; stale tile may appear unless force-refreshed.
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
# CCMC iSWA — Integrated Space Weather Analysis platform — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when assembling near-real-time and historical multi-source space-weather displays (in-situ L1, magnetograms, SWMF/ENLIL forecasts, kp/dst, GOES X-ray) without having to manually fetch each source — central claim is that iSWA at CCMC aggregates dozens of data and model layers into a single configurable dashboard with API access (Pulkkinen 2011 Space Weather).

Do NOT use this skill when:

- Do not assume iSWA hosts science-grade Level-2 — it pulls real-time / Level-1 streams.
- Do not use iSWA as the authoritative archive for any single instrument — go to the source.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** iSWA: 'Integrated Space Weather Analysis' system at CCMC/GSFC. Hosts near-real-time data feeds and CCMC simulation outputs, exposes image/timeseries APIs, and offers user-configurable layouts.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

This skill is primarily a *contract* (instrument / data product / archive); see §4 for the abstract tool contract. No standalone algorithm is teach-able from this skill alone.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| ACE/Wind real-time IMF + plasma via iSWA | L1 RT | real-time | — | CCMC iSWA |
| ENLIL forecast (heliospheric MHD) | forecast | run-based | — | CCMC iSWA |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Real-time feeds may show artifact dropouts the science-quality product later corrects.
- iSWA aggregator caches images; stale tile may appear unless force-refreshed.

## 7. Claim boundary  *(Layer 1)*

**In scope.** iSWA: 'Integrated Space Weather Analysis' system at CCMC/GSFC. Hosts near-real-time data feeds and CCMC simulation outputs, exposes image/timeseries APIs, and offers user-configurable layouts.

**Out of scope — do NOT generalize beyond:**

- Do not assume iSWA hosts science-grade Level-2 — it pulls real-time / Level-1 streams.
- Do not use iSWA as the authoritative archive for any single instrument — go to the source.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://iswa.ccmc.gsfc.nasa.gov/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- No single canonical iSWA paper; Pulkkinen 2011 Space Weather covers GEM context
