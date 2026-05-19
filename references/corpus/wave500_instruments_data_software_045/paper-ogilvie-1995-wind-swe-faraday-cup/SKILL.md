---
name: paper-ogilvie-1995-wind-swe-faraday-cup
description: >-
  Use when fetching solar-wind proton/alpha bulk moments and 3D distribution
  snapshots from Wind/SWE Faraday cups at L1 — central claim is that the two SWE
  Faraday cups (FC1/FC2) plus electron analyzers deliver 92 s ion moments (Vp,
  np, Tp, Va, na) usable as the canonical L1 in-situ plasma reference (Ogilvie
  et al. 1995, Space Sci. Rev.).
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
  title: "SWE, a comprehensive plasma instrument for the Wind spacecraft"
  first_author: "Ogilvie, K. W."
  year: 1995
  venue: Space Science Reviews
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - Wind
  regime:
    - 1au
trigger_keywords:
  - Wind SWE
  - Faraday cup
  - Ogilvie 1995
  - Wind plasma instrument
  - Wind ion moments
  - L1 solar wind plasma
  - Wind alpha proton
  - SWE nonlinear moments
data_products:
  - instrument: Wind/SWE FC
    level: L2
    cadence: 92 s (ion moments)
    interval: null
    archive: SPDF / CDAWeb
  - instrument: Wind/SWE NL moments
    level: L2
    cadence: 92 s
    interval: null
    archive: SPDF
  - instrument: Wind/SWE VEIS electrons
    level: L2
    cadence: 3-12 s (mode-dependent)
    interval: null
    archive: SPDF
algorithms:
  - name: Faraday-cup nonlinear Maxwellian fit
    equation_refs:
      - §3 Ogilvie 1995
    external_implementations: []
  - name: Key-parameter (KP) moment pipeline
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/pub/data/wind/swe/"
claim_boundary:
  scope: >-
    Wind/SWE comprises two Faraday cups (FC1, FC2) tilted ±15° to spin axis and
    a vector electron-ion analyzer (VEIS). Ion moments at ~92 s; non-linear-fit
    'key-parameter' (KP) products and 'NL' (nonlinear) moments are derived from
    raw current-vs-voltage curves.
  out_of_scope:
    - "Do not use SWE moments without checking quality flags — KP and NL pipelines disagree in unusual streams (high beta, deep CMEs)."
    - Do not extrapolate VEIS electron distributions below ~10 eV; the analyzer is energy-limited.
failure_modes:
  - "KP moments are publishable for monitoring but coarse; for science prefer NL or 'h0' files."
  - Alpha-proton separation requires sufficient thermal separation in V-space; fast streams may merge peaks.
  - Spin-axis tilt and aberration must be removed before frame transforms.
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
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# SWE, a comprehensive plasma instrument for the Wind spacecraft — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when fetching solar-wind proton/alpha bulk moments and 3D distribution snapshots from Wind/SWE Faraday cups at L1 — central claim is that the two SWE Faraday cups (FC1/FC2) plus electron analyzers deliver 92 s ion moments (Vp, np, Tp, Va, na) usable as the canonical L1 in-situ plasma reference (Ogilvie et al. 1995, Space Sci. Rev.).

Do NOT use this skill when:

- Do not use SWE moments without checking quality flags — KP and NL pipelines disagree in unusual streams (high beta, deep CMEs).
- Do not extrapolate VEIS electron distributions below ~10 eV; the analyzer is energy-limited.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Wind/SWE comprises two Faraday cups (FC1, FC2) tilted ±15° to spin axis and a vector electron-ion analyzer (VEIS). Ion moments at ~92 s; non-linear-fit 'key-parameter' (KP) products and 'NL' (nonlinear) moments are derived from raw current-vs-voltage curves.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Faraday-cup nonlinear Maxwellian fit

- Paper reference: §3 Ogilvie 1995
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Key-parameter (KP) moment pipeline

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Wind/SWE FC | L2 | 92 s (ion moments) | — | SPDF / CDAWeb |
| Wind/SWE NL moments | L2 | 92 s | — | SPDF |
| Wind/SWE VEIS electrons | L2 | 3-12 s (mode-dependent) | — | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- KP moments are publishable for monitoring but coarse; for science prefer NL or 'h0' files.
- Alpha-proton separation requires sufficient thermal separation in V-space; fast streams may merge peaks.
- Spin-axis tilt and aberration must be removed before frame transforms.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Wind/SWE comprises two Faraday cups (FC1, FC2) tilted ±15° to spin axis and a vector electron-ion analyzer (VEIS). Ion moments at ~92 s; non-linear-fit 'key-parameter' (KP) products and 'NL' (nonlinear) moments are derived from raw current-vs-voltage curves.

**Out of scope — do NOT generalize beyond:**

- Do not use SWE moments without checking quality flags — KP and NL pipelines disagree in unusual streams (high beta, deep CMEs).
- Do not extrapolate VEIS electron distributions below ~10 eV; the analyzer is energy-limited.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://cdaweb.gsfc.nasa.gov/pub/data/wind/swe/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Space Sci. Rev. 71, 55 (1995)
