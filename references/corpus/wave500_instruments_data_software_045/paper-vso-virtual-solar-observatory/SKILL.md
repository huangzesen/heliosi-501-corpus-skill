---
name: paper-vso-virtual-solar-observatory
description: >-
  Use when discovering or fetching solar imagery / spectra across multiple
  providers (NSO, JSOC, NASA/GSFC, MSU, KSO, etc.) with a single search —
  central claim is that the Virtual Solar Observatory federates instrument-and-
  provider metadata into one search API, with sunpy's Fido as the primary Python
  client (Hill et al. 2009).
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
  title: The Virtual Solar Observatory (VSO)
  first_author: "Hill, F."
  year: 2009
  venue: (VSO project paper / documentation; cite Hill et al. 2009 Earth Moon Planets for original VSO description)
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - other
    - SDO
    - STEREO
  regime:
    - corona
trigger_keywords:
  - Virtual Solar Observatory
  - VSO
  - Hill 2009
  - Fido search VSO
  - federated solar archive
data_products:
  - instrument: SDO/AIA via VSO
    level: L1
    cadence: 12 s
    interval: 2010-04..present
    archive: VSO mediator → JSOC
  - instrument: SOHO/EIT via VSO
    level: L1/L2
    cadence: varies
    interval: 1996-present
    archive: VSO mediator
algorithms:
  - name: sunpy.net.vso Fido client query/get
    equation_refs: []
    external_implementations:
      - "https://github.com/sunpy/sunpy"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://sdac.virtualsolar.org/cgi/search"
claim_boundary:
  scope: >-
    VSO: federated discovery service at GSFC/NSO. Mediates queries across
    providers; resolves to provider-side URLs. Exposed via sunpy's
    `sunpy.net.vso` client (`Fido.search(a.vso.*)`).
  out_of_scope:
    - Do not assume VSO has every dataset — provider coverage is partial.
    - Do not assume VSO returns absolute paths into a single host; the URLs route to provider servers.
    - Do not bypass provider download rules; VSO does not centralize quotas.
failure_modes:
  - "VSO mediator latency: a multi-provider search can take tens of seconds."
  - Some providers offline intermittently — VSO returns partial results without erroring.
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
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# The Virtual Solar Observatory (VSO) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when discovering or fetching solar imagery / spectra across multiple providers (NSO, JSOC, NASA/GSFC, MSU, KSO, etc.) with a single search — central claim is that the Virtual Solar Observatory federates instrument-and-provider metadata into one search API, with sunpy's Fido as the primary Python client (Hill et al. 2009).

Do NOT use this skill when:

- Do not assume VSO has every dataset — provider coverage is partial.
- Do not assume VSO returns absolute paths into a single host; the URLs route to provider servers.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** VSO: federated discovery service at GSFC/NSO. Mediates queries across providers; resolves to provider-side URLs. Exposed via sunpy's `sunpy.net.vso` client (`Fido.search(a.vso.*)`).

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### sunpy.net.vso Fido client query/get

- External implementation(s): https://github.com/sunpy/sunpy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SDO/AIA via VSO | L1 | 12 s | 2010-04..present | VSO mediator → JSOC |
| SOHO/EIT via VSO | L1/L2 | varies | 1996-present | VSO mediator |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- VSO mediator latency: a multi-provider search can take tens of seconds.
- Some providers offline intermittently — VSO returns partial results without erroring.

## 7. Claim boundary  *(Layer 1)*

**In scope.** VSO: federated discovery service at GSFC/NSO. Mediates queries across providers; resolves to provider-side URLs. Exposed via sunpy's `sunpy.net.vso` client (`Fido.search(a.vso.*)`).

**Out of scope — do NOT generalize beyond:**

- Do not assume VSO has every dataset — provider coverage is partial.
- Do not assume VSO returns absolute paths into a single host; the URLs route to provider servers.
- Do not bypass provider download rules; VSO does not centralize quotas.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://sdac.virtualsolar.org/cgi/search

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunpy-2023-interoperable-ecosystem]]`

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- Hill et al. 2009 Earth Moon Planets 104, 315 — verify DOI
