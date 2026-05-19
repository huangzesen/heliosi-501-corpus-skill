---
name: paper-lin-1995-wind-3dp-plasma-energetic-electrons
description: >-
  Use when retrieving full 3D electron / ion distribution functions and
  energetic-particle pitch-angle data from Wind/3DP at L1 (~3 eV–400 keV
  electrons; ~3 eV–6 MeV ions) — central claim is that 3DP delivers full 3D
  distributions every spin (3 s) with overlapping electrostatic and solid-state
  telescopes (Lin et al. 1995, Space Sci. Rev.).
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
  title: A three-dimensional plasma and energetic particle investigation for the Wind spacecraft
  first_author: "Lin, R. P."
  year: 1995
  venue: Space Science Reviews
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: energetic_particles
  secondary_themes: []
  missions:
    - Wind
  regime:
    - 1au
trigger_keywords:
  - Wind 3DP
  - Lin 1995
  - Wind electron PAD
  - PESA
  - EESA
  - SST telescope
  - Wind energetic electrons
  - strahl electrons
  - Wind suprathermal electrons
data_products:
  - instrument: Wind/3DP PESA
    level: L2
    cadence: 3 s (full 3D)
    interval: null
    archive: SPDF
  - instrument: Wind/3DP EESA
    level: L2
    cadence: 3 s
    interval: null
    archive: SPDF
  - instrument: Wind/3DP SST electrons
    level: L2
    cadence: 3 s
    interval: null
    archive: SPDF
algorithms:
  - name: 3D distribution-function moment integration
    equation_refs:
      - §4 Lin 1995
    external_implementations: []
  - name: Pitch-angle distribution from look-direction bins
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/pub/data/wind/3dp/"
claim_boundary:
  scope: >-
    Wind/3DP: PESA-L/H electrostatic analyzers for thermal ions, EESA-L/H for
    thermal electrons, and SST telescopes for suprathermal ions/electrons. Full
    3D angle/energy coverage every spin.
  out_of_scope:
    - Do not treat 3DP as a high-cadence (sub-second) plasma instrument; spin-period is the floor for full 3D.
    - Do not use SST below ~25 keV electrons or ~25 keV ions; ESA range applies there.
failure_modes:
  - Electron pitch-angle distributions are contaminated by spacecraft potential — correct using SWE potential or fit-derived value.
  - SST one-sided efficiency drops; cross-check L and H telescopes.
  - Strahl identification requires careful subtraction of returning halo population in opposite hemisphere.
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
# A three-dimensional plasma and energetic particle investigation for the Wind spacecraft — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving full 3D electron / ion distribution functions and energetic-particle pitch-angle data from Wind/3DP at L1 (~3 eV–400 keV electrons; ~3 eV–6 MeV ions) — central claim is that 3DP delivers full 3D distributions every spin (3 s) with overlapping electrostatic and solid-state telescopes (Lin et al. 1995, Space Sci. Rev.).

Do NOT use this skill when:

- Do not treat 3DP as a high-cadence (sub-second) plasma instrument; spin-period is the floor for full 3D.
- Do not use SST below ~25 keV electrons or ~25 keV ions; ESA range applies there.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Wind/3DP: PESA-L/H electrostatic analyzers for thermal ions, EESA-L/H for thermal electrons, and SST telescopes for suprathermal ions/electrons. Full 3D angle/energy coverage every spin.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### 3D distribution-function moment integration

- Paper reference: §4 Lin 1995
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Pitch-angle distribution from look-direction bins

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Wind/3DP PESA | L2 | 3 s (full 3D) | — | SPDF |
| Wind/3DP EESA | L2 | 3 s | — | SPDF |
| Wind/3DP SST electrons | L2 | 3 s | — | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Electron pitch-angle distributions are contaminated by spacecraft potential — correct using SWE potential or fit-derived value.
- SST one-sided efficiency drops; cross-check L and H telescopes.
- Strahl identification requires careful subtraction of returning halo population in opposite hemisphere.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Wind/3DP: PESA-L/H electrostatic analyzers for thermal ions, EESA-L/H for thermal electrons, and SST telescopes for suprathermal ions/electrons. Full 3D angle/energy coverage every spin.

**Out of scope — do NOT generalize beyond:**

- Do not treat 3DP as a high-cadence (sub-second) plasma instrument; spin-period is the floor for full 3D.
- Do not use SST below ~25 keV electrons or ~25 keV ions; ESA range applies there.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://cdaweb.gsfc.nasa.gov/pub/data/wind/3dp/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Space Sci. Rev. 71, 125 (1995)
