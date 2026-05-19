---
name: paper-stansby-2018-heliopy-python-heliospheric-data
description: >-
  Use when working with heliopy v0.x data loaders for in-situ heliophysics
  (Helios, Ulysses, Wind, ACE, MMS, PSP) and SPICE ephemeris — central claim is
  that heliopy unified Python downloaders/parsers for legacy + modern missions
  (Stansby 2018, JOSS); note that as of late 2022 the library is in maintenance
  mode and pyspedas/sunpy are the recommended successors.
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
  title: "HelioPy: Python for heliospheric and planetary physics"
  first_author: "Stansby, D."
  year: 2018
  venue: Journal of Open Source Software
  doi: 10.21105/joss.01060
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - Helios
    - Ulysses
    - Wind
    - ACE
    - PSP
  regime:
    - 1au
    - inner-heliosphere
trigger_keywords:
  - heliopy
  - Stansby 2018
  - Helios mission Python
  - Ulysses Python
  - in-situ Python loader
data_products:
  - instrument: Helios E1/E2 plasma+B
    level: L2
    cadence: various
    interval: 1974-1985
    archive: heliopy fetcher → SPDF
  - instrument: Ulysses SWOOPS+VHM
    level: L2
    cadence: various
    interval: 1990-2009
    archive: heliopy → SPDF / NSSDCA
algorithms:
  - name: "Mission-specific loader (heliopy.data.helios.merged, heliopy.data.ulysses.swoops)"
    equation_refs: []
    external_implementations:
      - "https://github.com/heliopython/heliopy"
  - name: SPICE-based trajectory wrapper
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.21105/joss.01060"
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/heliopython/heliopy"
  data_repo: null
claim_boundary:
  scope: >-
    heliopy: data fetchers (heliopy.data.<mission>), trajectory utilities
    (heliopy.spice on top of SpiceyPy), and helpers for solar-wind
    classification. Last release v0.15.x (2022); now in maintenance mode.
  out_of_scope:
    - Do not assume new mission loaders will be added — heliopy is unmaintained for new development.
    - Do not treat heliopy as a replacement for pyspedas for current missions; consult sunpy + pyspedas.
    - "Do not use heliopy's plotting; it predates many sunpy improvements."
failure_modes:
  - "Reliance on a `.heliopy/` config file with cache path; corrupted cache silently breaks loaders."
  - Some Helios products require an older parser version; newer heliopy may reject.
  - "Maintenance-mode status: bug-fix turnaround slow; pin versions."
depends_on:
  - paper-annex-2020-spiceypy-naif-spice-toolkit-python
  - paper-astropy-2022-collaboration-community-package
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: heliopy is the canonical Python Helios-mission loader; no replacement skill in the corpus yet covers Helios E1/E2 specifically.
    related_skills: []
    proposed_action: compile a Helios mission-instrument paper-skill (Schwenn/Marsch instrument suite)
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# HelioPy: Python for heliospheric and planetary physics — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when working with heliopy v0.x data loaders for in-situ heliophysics (Helios, Ulysses, Wind, ACE, MMS, PSP) and SPICE ephemeris — central claim is that heliopy unified Python downloaders/parsers for legacy + modern missions (Stansby 2018, JOSS); note that as of late 2022 the library is in maintenance mode and pyspedas/sunpy are the recommended successors.

Do NOT use this skill when:

- Do not assume new mission loaders will be added — heliopy is unmaintained for new development.
- Do not treat heliopy as a replacement for pyspedas for current missions; consult sunpy + pyspedas.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** heliopy: data fetchers (heliopy.data.<mission>), trajectory utilities (heliopy.spice on top of SpiceyPy), and helpers for solar-wind classification. Last release v0.15.x (2022); now in maintenance mode.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Mission-specific loader (heliopy.data.helios.merged, heliopy.data.ulysses.swoops)

- External implementation(s): https://github.com/heliopython/heliopy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### SPICE-based trajectory wrapper

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Helios E1/E2 plasma+B | L2 | various | 1974-1985 | heliopy fetcher → SPDF |
| Ulysses SWOOPS+VHM | L2 | various | 1990-2009 | heliopy → SPDF / NSSDCA |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Reliance on a `.heliopy/` config file with cache path; corrupted cache silently breaks loaders.
- Some Helios products require an older parser version; newer heliopy may reject.
- Maintenance-mode status: bug-fix turnaround slow; pin versions.

## 7. Claim boundary  *(Layer 1)*

**In scope.** heliopy: data fetchers (heliopy.data.<mission>), trajectory utilities (heliopy.spice on top of SpiceyPy), and helpers for solar-wind classification. Last release v0.15.x (2022); now in maintenance mode.

**Out of scope — do NOT generalize beyond:**

- Do not assume new mission loaders will be added — heliopy is unmaintained for new development.
- Do not treat heliopy as a replacement for pyspedas for current missions; consult sunpy + pyspedas.
- Do not use heliopy's plotting; it predates many sunpy improvements.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.21105/joss.01060
- arXiv: n/a
- Code: https://github.com/heliopython/heliopy
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-annex-2020-spiceypy-naif-spice-toolkit-python]]`
- `[[paper-astropy-2022-collaboration-community-package]]`

**Research-generation affordances.**

- **Gap** — heliopy is the canonical Python Helios-mission loader; no replacement skill in the corpus yet covers Helios E1/E2 specifically. Proposed: compile a Helios mission-instrument paper-skill (Schwenn/Marsch instrument suite).

## Weak entries / citation TODOs

- heliopy currently in maintenance mode; verify last-release status before integration
