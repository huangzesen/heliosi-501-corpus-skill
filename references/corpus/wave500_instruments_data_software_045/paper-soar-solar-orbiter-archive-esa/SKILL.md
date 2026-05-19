---
name: paper-soar-solar-orbiter-archive-esa
description: >-
  Use when programmatically accessing Solar Orbiter Level-1/Level-2/Level-3 data
  (MAG, SWA, EPD, EUI, METIS, PHI, SPICE, STIX, RPW) — central claim is that
  SOAR (ESAC) is the canonical Solar Orbiter archive exposing a REST + TAP
  interface and the only authoritative source for SO L2+ products.
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
  title: The Solar Orbiter Archive (SOAR)
  first_author: ESAC Solar Orbiter Archive team
  year: 2021
  venue: "(ESA Solar Orbiter Archive documentation; companion paper Sanchez et al. 2024 A&A)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_orbiter
  secondary_themes: []
  missions:
    - Solar Orbiter
  regime:
    - inner-heliosphere
    - corona
trigger_keywords:
  - SOAR archive
  - Solar Orbiter Archive
  - ESAC SOAR
  - Sanchez 2024 SOAR
  - SOAR TAP query
  - Solar Orbiter L2 data
  - ESA Solar Orbiter archive
data_products:
  - instrument: SO/MAG
    level: L2
    cadence: 8 Hz normal
    interval: null
    archive: SOAR
  - instrument: SO/SWA
    level: L2
    cadence: varies
    interval: null
    archive: SOAR
  - instrument: SO/EUI
    level: L2
    cadence: varies
    interval: null
    archive: SOAR
  - instrument: SO/METIS
    level: L2
    cadence: campaign-dependent
    interval: null
    archive: SOAR
  - instrument: SO/EPD
    level: L2
    cadence: varies
    interval: null
    archive: SOAR
algorithms:
  - name: TAP (Table Access Protocol) query for SO observations
    equation_refs: []
    external_implementations:
      - "https://soar.esac.esa.int/soar/"
  - name: sunpy.net.Fido SOAR provider
    equation_refs: []
    external_implementations:
      - sunpy.net.dataretriever.SOARClient
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://soar.esac.esa.int/"
claim_boundary:
  scope: >-
    SOAR: Solar Orbiter Archive at ESAC. Browser + sunpy Fido client
    (`sunpy.net.dataretriever.SOARClient`) + ESA Datalabs. Houses calibrated
    L1+L2 (and some L3) products. Older encounters released after data-rights
    periods expire.
  out_of_scope:
    - Do not assume SOAR has every Level-3 product — some are in PI repositories first.
    - Do not bypass calibration version; SOAR keeps a release-notes page per instrument.
    - Do not assume CDAWeb mirrors are complete — SO data is primarily SOAR-side.
failure_modes:
  - Recent encounters have proprietary periods (typically 3 months); a query may return empty for in-flight data.
  - TAP query columns differ between L1 and L2 tables — read schema.
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
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# The Solar Orbiter Archive (SOAR) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when programmatically accessing Solar Orbiter Level-1/Level-2/Level-3 data (MAG, SWA, EPD, EUI, METIS, PHI, SPICE, STIX, RPW) — central claim is that SOAR (ESAC) is the canonical Solar Orbiter archive exposing a REST + TAP interface and the only authoritative source for SO L2+ products.

Do NOT use this skill when:

- Do not assume SOAR has every Level-3 product — some are in PI repositories first.
- Do not bypass calibration version; SOAR keeps a release-notes page per instrument.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SOAR: Solar Orbiter Archive at ESAC. Browser + sunpy Fido client (`sunpy.net.dataretriever.SOARClient`) + ESA Datalabs. Houses calibrated L1+L2 (and some L3) products. Older encounters released after data-rights periods expire.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### TAP (Table Access Protocol) query for SO observations

- External implementation(s): https://soar.esac.esa.int/soar/
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### sunpy.net.Fido SOAR provider

- External implementation(s): sunpy.net.dataretriever.SOARClient
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SO/MAG | L2 | 8 Hz normal | — | SOAR |
| SO/SWA | L2 | varies | — | SOAR |
| SO/EUI | L2 | varies | — | SOAR |
| SO/METIS | L2 | campaign-dependent | — | SOAR |
| SO/EPD | L2 | varies | — | SOAR |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Recent encounters have proprietary periods (typically 3 months); a query may return empty for in-flight data.
- TAP query columns differ between L1 and L2 tables — read schema.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SOAR: Solar Orbiter Archive at ESAC. Browser + sunpy Fido client (`sunpy.net.dataretriever.SOARClient`) + ESA Datalabs. Houses calibrated L1+L2 (and some L3) products. Older encounters released after data-rights periods expire.

**Out of scope — do NOT generalize beyond:**

- Do not assume SOAR has every Level-3 product — some are in PI repositories first.
- Do not bypass calibration version; SOAR keeps a release-notes page per instrument.
- Do not assume CDAWeb mirrors are complete — SO data is primarily SOAR-side.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://soar.esac.esa.int/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[muller-2020-solar-orbiter-mission-overview]]`

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- Companion paper Sanchez et al. 2024 A&A; verify exact DOI
