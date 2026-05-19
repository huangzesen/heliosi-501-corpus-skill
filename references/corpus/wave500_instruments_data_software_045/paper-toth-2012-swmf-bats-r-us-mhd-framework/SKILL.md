---
name: paper-toth-2012-swmf-bats-r-us-mhd-framework
description: >-
  Use when running or interpreting Space Weather Modeling Framework (SWMF) /
  BATS-R-US MHD simulations of the heliosphere, magnetosphere, or ionosphere —
  central claim is that the SWMF couples solar / inner-helio / magnetosphere /
  ionosphere domain models through a single framework with adaptive mesh
  refinement (Tóth et al. 2012, JCP).
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
  title: Adaptive numerical algorithms in space weather modeling
  first_author: "Tóth, G."
  year: 2012
  venue: Journal of Computational Physics
  doi: 10.1016/j.jcp.2011.02.006
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - MHD-scale
trigger_keywords:
  - SWMF
  - BATS-R-US
  - Tóth 2012
  - space weather modeling framework
  - CCMC
  - AMR MHD heliosphere
  - MHD magnetosphere model
data_products:
  - instrument: SWMF CCMC run output
    level: L2 simulation output
    cadence: run-specific
    interval: null
    archive: CCMC iSWA / runs-on-request
algorithms:
  - name: BATS-R-US adaptive mesh MHD solver
    equation_refs:
      - Tóth 2012 §2-§4
    external_implementations:
      - "https://github.com/MSTEM-QUDA"
  - name: Framework coupling via MPI domain bridges
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1016/j.jcp.2011.02.006"
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/MSTEM-QUDA"
  data_repo: "https://ccmc.gsfc.nasa.gov/results/"
claim_boundary:
  scope: >-
    SWMF: framework coupling SC (Solar Corona, BATS-R-US), IH (Inner
    Heliosphere, BATS-R-US), GM (Global Magnetosphere, BATS-R-US), IM (Inner
    Magnetosphere, RCM/RAM), IE (Ionospheric Electrodynamics, Ridley), and other
    modules. Available via runs-on-request at CCMC.
  out_of_scope:
    - Do not run SWMF without a domain-coupling validated config — coupling combinations are not all certified.
    - Do not assume CCMC runs are reproducible bit-for-bit — versions may drift.
    - Do not treat SWMF MHD as kinetic — it does not capture pickup-ion or pitch-angle physics.
failure_modes:
  - Coupled-domain CFL constraints can cause silent slowdowns; check log timestep.
  - Magnetogram-driven SC runs depend heavily on input map quality.
  - Diff-pre-shock parameters can blow up if photoshpere upper boundary too far in.
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
# Adaptive numerical algorithms in space weather modeling — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when running or interpreting Space Weather Modeling Framework (SWMF) / BATS-R-US MHD simulations of the heliosphere, magnetosphere, or ionosphere — central claim is that the SWMF couples solar / inner-helio / magnetosphere / ionosphere domain models through a single framework with adaptive mesh refinement (Tóth et al. 2012, JCP).

Do NOT use this skill when:

- Do not run SWMF without a domain-coupling validated config — coupling combinations are not all certified.
- Do not assume CCMC runs are reproducible bit-for-bit — versions may drift.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SWMF: framework coupling SC (Solar Corona, BATS-R-US), IH (Inner Heliosphere, BATS-R-US), GM (Global Magnetosphere, BATS-R-US), IM (Inner Magnetosphere, RCM/RAM), IE (Ionospheric Electrodynamics, Ridley), and other modules. Available via runs-on-request at CCMC.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### BATS-R-US adaptive mesh MHD solver

- Paper reference: Tóth 2012 §2-§4
- External implementation(s): https://github.com/MSTEM-QUDA
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Framework coupling via MPI domain bridges

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SWMF CCMC run output | L2 simulation output | run-specific | — | CCMC iSWA / runs-on-request |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Coupled-domain CFL constraints can cause silent slowdowns; check log timestep.
- Magnetogram-driven SC runs depend heavily on input map quality.
- Diff-pre-shock parameters can blow up if photoshpere upper boundary too far in.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SWMF: framework coupling SC (Solar Corona, BATS-R-US), IH (Inner Heliosphere, BATS-R-US), GM (Global Magnetosphere, BATS-R-US), IM (Inner Magnetosphere, RCM/RAM), IE (Ionospheric Electrodynamics, Ridley), and other modules. Available via runs-on-request at CCMC.

**Out of scope — do NOT generalize beyond:**

- Do not run SWMF without a domain-coupling validated config — coupling combinations are not all certified.
- Do not assume CCMC runs are reproducible bit-for-bit — versions may drift.
- Do not treat SWMF MHD as kinetic — it does not capture pickup-ion or pitch-angle physics.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1016/j.jcp.2011.02.006
- arXiv: n/a
- Code: https://github.com/MSTEM-QUDA
- Data / archive: https://ccmc.gsfc.nasa.gov/results/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.
