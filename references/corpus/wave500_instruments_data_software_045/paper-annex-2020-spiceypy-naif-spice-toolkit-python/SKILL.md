---
name: paper-annex-2020-spiceypy-naif-spice-toolkit-python
description: >-
  Use when computing spacecraft ephemerides, body positions, light-time, or
  frame transforms for heliophysics missions (PSP, Solar Orbiter, MAVEN,
  BepiColombo, etc.) — central claim is that SpiceyPy is the Python wrapper
  around NAIF's SPICE C toolkit (Annex et al. 2020, JOSS) and unlocks kernel-
  driven ephemeris/geometry computation in scientific Python.
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
  title: "SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit"
  first_author: "Annex, A. M."
  year: 2020
  venue: Journal of Open Source Software
  doi: 10.21105/joss.02050
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - PSP
    - Solar Orbiter
    - Wind
    - ACE
    - MAVEN
    - MESSENGER
    - STEREO
    - Ulysses
  regime:
    - 1au
    - inner-heliosphere
    - outer-heliosphere
trigger_keywords:
  - SpiceyPy
  - Annex 2020
  - SPICE Python
  - NAIF kernel
  - spkpos
  - spacecraft ephemeris
  - PSP ephemeris
  - Solar Orbiter ephemeris
  - frame transform SPICE
data_products:
  - instrument: SPICE kernels (PSP/Solar Orbiter/MAVEN SPK)
    level: ephemeris kernel
    cadence: n/a
    interval: mission lifetime
    archive: NAIF + mission archives
algorithms:
  - name: spkpos / spkezr — position + state of body relative to observer
    equation_refs: []
    external_implementations:
      - "https://github.com/AndrewAnnex/SpiceyPy"
  - name: pxform / sxform — frame transform matrices
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.21105/joss.02050"
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/AndrewAnnex/SpiceyPy"
  data_repo: null
claim_boundary:
  scope: >-
    SpiceyPy: thin ctypes wrapper around the NAIF CSPICE library, exposing
    spkpos / spkezr / pxform / sce2c etc. as Python calls. Requires furnsh-
    loaded SPICE kernel set (SPK, PCK, FK, IK, LSK).
  out_of_scope:
    - Do not assume SpiceyPy ships kernels — fetch them from NAIF / mission archive.
    - Do not call spice functions without loading a leapseconds kernel (LSK) — time conversions fail silently.
    - Do not assume thread safety; SpiceyPy holds a global SPICE state.
failure_modes:
  - "Loading conflicting kernels (newer + older SPK for same body) — last loaded wins; use `kclear` to reset."
  - Forgetting LSK kernel → ET / UTC conversions return wrong times silently.
  - "Light-time toggle (`LT`, `LT+S`, `NONE`) drastically changes returned positions."
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
tags: [heliophysics, paper-skill, software-paper]
source_type: software-paper
---
# SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `method-ready` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when computing spacecraft ephemerides, body positions, light-time, or frame transforms for heliophysics missions (PSP, Solar Orbiter, MAVEN, BepiColombo, etc.) — central claim is that SpiceyPy is the Python wrapper around NAIF's SPICE C toolkit (Annex et al. 2020, JOSS) and unlocks kernel-driven ephemeris/geometry computation in scientific Python.

Do NOT use this skill when:

- Do not assume SpiceyPy ships kernels — fetch them from NAIF / mission archive.
- Do not call spice functions without loading a leapseconds kernel (LSK) — time conversions fail silently.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SpiceyPy: thin ctypes wrapper around the NAIF CSPICE library, exposing spkpos / spkezr / pxform / sce2c etc. as Python calls. Requires furnsh-loaded SPICE kernel set (SPK, PCK, FK, IK, LSK).

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### spkpos / spkezr — position + state of body relative to observer

- External implementation(s): https://github.com/AndrewAnnex/SpiceyPy
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### pxform / sxform — frame transform matrices

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SPICE kernels (PSP/Solar Orbiter/MAVEN SPK) | ephemeris kernel | n/a | mission lifetime | NAIF + mission archives |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `method-ready`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Loading conflicting kernels (newer + older SPK for same body) — last loaded wins; use `kclear` to reset.
- Forgetting LSK kernel → ET / UTC conversions return wrong times silently.
- Light-time toggle (`LT`, `LT+S`, `NONE`) drastically changes returned positions.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SpiceyPy: thin ctypes wrapper around the NAIF CSPICE library, exposing spkpos / spkezr / pxform / sce2c etc. as Python calls. Requires furnsh-loaded SPICE kernel set (SPK, PCK, FK, IK, LSK).

**Out of scope — do NOT generalize beyond:**

- Do not assume SpiceyPy ships kernels — fetch them from NAIF / mission archive.
- Do not call spice functions without loading a leapseconds kernel (LSK) — time conversions fail silently.
- Do not assume thread safety; SpiceyPy holds a global SPICE state.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.21105/joss.02050
- arXiv: n/a
- Code: https://github.com/AndrewAnnex/SpiceyPy
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.
