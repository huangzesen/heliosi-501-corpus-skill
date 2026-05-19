---
name: paper-lepping-1995-wind-mfi-magnetometer
description: >-
  Use when fetching, interpreting, or calibrating Wind/MFI dual triaxial
  fluxgate magnetic field data at L1 (and pre-L1 lunar swing-by orbits) —
  central claim is that Wind MFI provides 11 Hz / 22 Hz / spin-tagged vector B
  with 0.025 nT resolution and is the long-baseline 1 au magnetic-field
  reference (Lepping et al. 1995, Space Sci. Rev.).
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
  title: The WIND Magnetic Field Investigation
  first_author: "Lepping, R. P."
  year: 1995
  venue: Space Science Reviews
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: magnetic_field
  secondary_themes: []
  missions:
    - Wind
  regime:
    - 1au
trigger_keywords:
  - Wind MFI
  - Wind magnetic field
  - L1 fluxgate
  - Lepping 1995
  - Wind vector magnetic field
  - 1 au magnetometer
  - Wind triaxial fluxgate
  - WIND mission magnetometer
data_products:
  - instrument: Wind/MFI
    level: L2
    cadence: "3 s (key), 1 min, 1 hour"
    interval: null
    archive: SPDF / CDAWeb
  - instrument: Wind/MFI high-resolution
    level: L2
    cadence: 11 Hz / 22 Hz
    interval: null
    archive: SPDF
algorithms:
  - name: Wind/MFI despin and offset correction
    equation_refs:
      - §4 Lepping 1995
    external_implementations: []
  - name: Range-auto-switch validity flag interpretation
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/pub/data/wind/mfi/"
claim_boundary:
  scope: >-
    Wind/MFI is a dual-redundant triaxial fluxgate magnetometer on a sun-pointed
    spinning platform (~20 s spin) on the Wind spacecraft. Cadence options reach
    11 sample/s (high-rate) or 22 sample/s on demand; standard L2 is at 3 s, 1
    min, 1 hour averages. Quoted resolution 0.025 nT; ranges ±4 to ±65536 nT
    auto-switched.
  out_of_scope:
    - Do not treat MFI as a corona-touching mission instrument — Wind is at L1 / lunar swing-by.
    - Do not use MFI for E-field or wave electric studies; pair with WAVES instrument.
failure_modes:
  - Spin tone (~20 s) survives in raw spacecraft-frame data; subtract spin axis or use GSE-rotated products.
  - Auto-range switching produces step artifacts in raw counts; only L2 should be used for science.
  - Zero-level (offset) calibration drifts with thermal cycles; periodic in-flight offset re-determinations are documented in instrument team notes.
depends_on:
  []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: No sibling skill covers Wind/WAVES electric-field counterpart needed for joint MFI+WAVES wave analyses.
    related_skills: []
    proposed_action: compile a Wind/WAVES Bougeret-1995 paper-skill
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# The WIND Magnetic Field Investigation — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when fetching, interpreting, or calibrating Wind/MFI dual triaxial fluxgate magnetic field data at L1 (and pre-L1 lunar swing-by orbits) — central claim is that Wind MFI provides 11 Hz / 22 Hz / spin-tagged vector B with 0.025 nT resolution and is the long-baseline 1 au magnetic-field reference (Lepping et al. 1995, Space Sci. Rev.).

Do NOT use this skill when:

- Do not treat MFI as a corona-touching mission instrument — Wind is at L1 / lunar swing-by.
- Do not use MFI for E-field or wave electric studies; pair with WAVES instrument.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Wind/MFI is a dual-redundant triaxial fluxgate magnetometer on a sun-pointed spinning platform (~20 s spin) on the Wind spacecraft. Cadence options reach 11 sample/s (high-rate) or 22 sample/s on demand; standard L2 is at 3 s, 1 min, 1 hour averages. Quoted resolution 0.025 nT; ranges ±4 to ±65536 nT auto-switched.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Wind/MFI despin and offset correction

- Paper reference: §4 Lepping 1995
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Range-auto-switch validity flag interpretation

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| Wind/MFI | L2 | 3 s (key), 1 min, 1 hour | — | SPDF / CDAWeb |
| Wind/MFI high-resolution | L2 | 11 Hz / 22 Hz | — | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Spin tone (~20 s) survives in raw spacecraft-frame data; subtract spin axis or use GSE-rotated products.
- Auto-range switching produces step artifacts in raw counts; only L2 should be used for science.
- Zero-level (offset) calibration drifts with thermal cycles; periodic in-flight offset re-determinations are documented in instrument team notes.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Wind/MFI is a dual-redundant triaxial fluxgate magnetometer on a sun-pointed spinning platform (~20 s spin) on the Wind spacecraft. Cadence options reach 11 sample/s (high-rate) or 22 sample/s on demand; standard L2 is at 3 s, 1 min, 1 hour averages. Quoted resolution 0.025 nT; ranges ±4 to ±65536 nT auto-switched.

**Out of scope — do NOT generalize beyond:**

- Do not treat MFI as a corona-touching mission instrument — Wind is at L1 / lunar swing-by.
- Do not use MFI for E-field or wave electric studies; pair with WAVES instrument.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://cdaweb.gsfc.nasa.gov/pub/data/wind/mfi/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

- **Gap** — No sibling skill covers Wind/WAVES electric-field counterpart needed for joint MFI+WAVES wave analyses. Proposed: compile a Wind/WAVES Bougeret-1995 paper-skill.

## Weak entries / citation TODOs

- DOI not in local inventory; cite Space Sci. Rev. 71, 207 (1995) when verifying
