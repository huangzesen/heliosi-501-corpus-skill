---
name: paper-hapi-2020-heliophysics-api-time-series
description: >-
  Use when a workflow needs uniform programmatic access to time-series
  heliophysics data across multiple data centers (SPDF, ESAC, LATMOS, INPE) via
  a common REST API — central claim is that HAPI defines a streaming time-series
  API spec implemented by many archives, removing the need for per-archive
  client logic (Weigel et al. 2020 / HAPI 3.x spec).
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
  title: "The Heliophysics Application Programmer's Interface (HAPI)"
  first_author: "Weigel, R. S."
  year: 2020
  venue: Frontiers in Astronomy and Space Sciences (and JOSS specification)
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
    - inner-heliosphere
    - outer-heliosphere
trigger_keywords:
  - HAPI heliophysics API
  - Weigel 2020
  - hapiclient
  - CDAWeb HAPI
  - heliophysics REST API
  - time series uniform access
data_products:
  - instrument: Wind/MFI via HAPI
    level: L2 via HAPI
    cadence: "3 s, 1 min"
    interval: null
    archive: "https://cdaweb.gsfc.nasa.gov/hapi"
  - instrument: ACE/MAG via HAPI
    level: L2 via HAPI
    cadence: "16 s, 1 min"
    interval: null
    archive: "https://cdaweb.gsfc.nasa.gov/hapi"
  - instrument: OMNI via HAPI
    level: L2 via HAPI
    cadence: "1 min, 1 hour"
    interval: null
    archive: "https://cdaweb.gsfc.nasa.gov/hapi"
algorithms:
  - name: HAPI /data streaming with start/stop ISO times
    equation_refs: []
    external_implementations:
      - "https://github.com/hapi-server/client-python"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/hapi-server/client-python"
  data_repo: "https://hapi-server.org/"
claim_boundary:
  scope: >-
    HAPI: REST API spec with five endpoints (/about, /capabilities, /catalog,
    /info, /data). HAPI servers run at SPDF (CDAWeb-HAPI), CCMC, ESAC, LATMOS,
    INPE, etc. Python clients: hapiclient, pysat-hapi.
  out_of_scope:
    - Do not assume every CDAWeb dataset is HAPI-exposed; the catalog endpoint is authoritative.
    - "Do not stream raw CDF binary through HAPI — HAPI returns CSV or binary numeric blocks, not the CDF wrapper."
    - "Do not rely on HAPI for non-time-series products (images, catalogs)."
failure_modes:
  - Default response is CSV — large requests are slow; use binary format for high-volume.
  - "Time format must be strict ISO 8601 with 'Z' suffix; ambiguity rejected."
  - "Cross-server inconsistencies on optional fields (units, fill values) — read /info before /data."
depends_on:
  - paper-cdaweb-heliophysics-archive
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: HAPI does not standardize coordinate-system metadata — independent CT/transform layer still needed.
    related_skills:
      - paper-franz-2002-heliospheric-coordinate-systems
    proposed_action: propose a HAPI v3+ profile that requires Fränz-Harper-compatible frame strings
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# The Heliophysics Application Programmer's Interface (HAPI) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when a workflow needs uniform programmatic access to time-series heliophysics data across multiple data centers (SPDF, ESAC, LATMOS, INPE) via a common REST API — central claim is that HAPI defines a streaming time-series API spec implemented by many archives, removing the need for per-archive client logic (Weigel et al. 2020 / HAPI 3.x spec).

Do NOT use this skill when:

- Do not assume every CDAWeb dataset is HAPI-exposed; the catalog endpoint is authoritative.
- Do not stream raw CDF binary through HAPI — HAPI returns CSV or binary numeric blocks, not the CDF wrapper.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** HAPI: REST API spec with five endpoints (/about, /capabilities, /catalog, /info, /data). HAPI servers run at SPDF (CDAWeb-HAPI), CCMC, ESAC, LATMOS, INPE, etc. Python clients: hapiclient, pysat-hapi.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### HAPI /data streaming with start/stop ISO times

- External implementation(s): https://github.com/hapi-server/client-python
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Wind/MFI via HAPI | L2 via HAPI | 3 s, 1 min | — | https://cdaweb.gsfc.nasa.gov/hapi |
| ACE/MAG via HAPI | L2 via HAPI | 16 s, 1 min | — | https://cdaweb.gsfc.nasa.gov/hapi |
| OMNI via HAPI | L2 via HAPI | 1 min, 1 hour | — | https://cdaweb.gsfc.nasa.gov/hapi |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Default response is CSV — large requests are slow; use binary format for high-volume.
- Time format must be strict ISO 8601 with 'Z' suffix; ambiguity rejected.
- Cross-server inconsistencies on optional fields (units, fill values) — read /info before /data.

## 7. Claim boundary  *(Layer 1)*

**In scope.** HAPI: REST API spec with five endpoints (/about, /capabilities, /catalog, /info, /data). HAPI servers run at SPDF (CDAWeb-HAPI), CCMC, ESAC, LATMOS, INPE, etc. Python clients: hapiclient, pysat-hapi.

**Out of scope — do NOT generalize beyond:**

- Do not assume every CDAWeb dataset is HAPI-exposed; the catalog endpoint is authoritative.
- Do not stream raw CDF binary through HAPI — HAPI returns CSV or binary numeric blocks, not the CDF wrapper.
- Do not rely on HAPI for non-time-series products (images, catalogs).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://github.com/hapi-server/client-python
- Data / archive: https://hapi-server.org/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-cdaweb-heliophysics-archive]]`

**Research-generation affordances.**

- **Gap** — HAPI does not standardize coordinate-system metadata — independent CT/transform layer still needed. Proposed: propose a HAPI v3+ profile that requires Fränz-Harper-compatible frame strings.

## Weak entries / citation TODOs

- DOI lookup TODO — HAPI is maintained as a community spec (hapi-server.org) with companion publications scattered
