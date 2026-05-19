---
name: paper-glogowski-2019-drms-jsoc-data-client
description: >-
  Use when querying or exporting SDO/HMI or SDO/AIA data series from JSOC (Joint
  Science Operations Center) directly in Python — central claim is that drms
  wraps JSOC's HTTP+JSOC query language so that DRMS series, segments, and
  exports work natively in Python (Glogowski et al. 2019, JOSS).
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
  title: "drms: A Python package for accessing HMI and AIA data"
  first_author: "Glogowski, K."
  year: 2019
  venue: Journal of Open Source Software
  doi: 10.21105/joss.01614
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
  regime:
    - corona
trigger_keywords:
  - drms
  - JSOC client
  - Glogowski 2019
  - HMI Python download
  - AIA Python download
  - JSOC query Python
  - DRMS series
data_products:
  - instrument: "JSOC DRMS series (hmi.M_45s, aia.lev1_euv_12s, etc.)"
    level: L1.5 / L2
    cadence: series-dependent
    interval: 2010-04..present
    archive: JSOC (drms client)
algorithms:
  - name: JSOC export_from_id polling + retrieval
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/drms"
  - name: DRMS query language pass-through
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.21105/joss.01614"
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/sunpy/drms"
  data_repo: null
claim_boundary:
  scope: >-
    drms: Python client for JSOC DRMS (Data Record Management System). Supports
    query, info, export_from_id, series listing. Underlies sunpy's JSOC Fido
    client.
  out_of_scope:
    - "Do not bypass drms's export rate-limit logic — JSOC throttles batch jobs."
    - "Do not use drms for non-JSOC archives (CDAWeb, SOAR)."
    - Do not assume immediate download — large exports queue for minutes-hours.
failure_modes:
  - Long-running export requests may silently expire; check request status before download.
  - Email-required exports (registered user) needed for large requests; anonymous client limited.
  - JSOC maintenance windows on Sundays produce intermittent timeouts.
depends_on:
  - paper-sunpy-2023-interoperable-ecosystem
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# drms: A Python package for accessing HMI and AIA data — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when querying or exporting SDO/HMI or SDO/AIA data series from JSOC (Joint Science Operations Center) directly in Python — central claim is that drms wraps JSOC's HTTP+JSOC query language so that DRMS series, segments, and exports work natively in Python (Glogowski et al. 2019, JOSS).

Do NOT use this skill when:

- Do not bypass drms's export rate-limit logic — JSOC throttles batch jobs.
- Do not use drms for non-JSOC archives (CDAWeb, SOAR).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** drms: Python client for JSOC DRMS (Data Record Management System). Supports query, info, export_from_id, series listing. Underlies sunpy's JSOC Fido client.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### JSOC export_from_id polling + retrieval

- External implementation(s): https://github.com/sunpy/drms
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### DRMS query language pass-through

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| JSOC DRMS series (hmi.M_45s, aia.lev1_euv_12s, etc.) | L1.5 / L2 | series-dependent | 2010-04..present | JSOC (drms client) |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Long-running export requests may silently expire; check request status before download.
- Email-required exports (registered user) needed for large requests; anonymous client limited.
- JSOC maintenance windows on Sundays produce intermittent timeouts.

## 7. Claim boundary  *(Layer 1)*

**In scope.** drms: Python client for JSOC DRMS (Data Record Management System). Supports query, info, export_from_id, series listing. Underlies sunpy's JSOC Fido client.

**Out of scope — do NOT generalize beyond:**

- Do not bypass drms's export rate-limit logic — JSOC throttles batch jobs.
- Do not use drms for non-JSOC archives (CDAWeb, SOAR).
- Do not assume immediate download — large exports queue for minutes-hours.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.21105/joss.01614
- arXiv: n/a
- Code: https://github.com/sunpy/drms
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`

**Research-generation affordances.**

No research-generation affordances identified yet.
