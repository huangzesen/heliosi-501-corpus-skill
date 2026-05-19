---
name: paper-scherrer-1995-soho-mdi-michelson-doppler-imager
description: >-
  Use when retrieving SOHO/MDI line-of-sight magnetograms, Dopplergrams, and
  continuum intensitygrams (1996–2010) for helioseismology and synoptic field
  mapping — central claim is that MDI's Michelson interferometer produces 96-min
  full-disk LOS magnetograms with ~2" pixel that serve as the canonical pre-HMI
  synoptic-field reference (Scherrer et al. 1995, Sol. Phys.).
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
  title: The Solar Oscillations Investigation — Michelson Doppler Imager
  first_author: "Scherrer, P. H."
  year: 1995
  venue: Solar Physics
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - other
  regime:
    - corona
trigger_keywords:
  - SOHO MDI
  - Scherrer 1995
  - MDI magnetogram
  - MDI Doppler
  - MDI synoptic map
  - helioseismology MDI
  - Michelson Doppler Imager
data_products:
  - instrument: SOHO/MDI LOS magnetogram
    level: L2
    cadence: 96 min full-disk
    interval: 1996-04..2010-12
    archive: JSOC / VSO
  - instrument: SOHO/MDI synoptic map
    level: L2 synoptic
    cadence: Carrington rotation
    interval: 1996-04..2010-12
    archive: JSOC
algorithms:
  - name: MDI line-fit Doppler/magnetogram retrieval
    equation_refs:
      - §4-5 Scherrer 1995
    external_implementations: []
  - name: MDI saturation correction (Liu et al. 2012)
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "http://jsoc.stanford.edu/MDI/"
claim_boundary:
  scope: >-
    SOHO/MDI imaged Ni I 6768 Å with two Michelson interferometers, returning
    intensity, Doppler, and LOS magnetograms in normal (96 min full-disk) and
    high-res (1024×1024 cropped) modes. Operational 1996-04 through 2010-12.
  out_of_scope:
    - Do not extend MDI coverage past 2010-12 (HMI succeeded it).
    - Do not use raw MDI synoptic maps for absolute flux without saturation correction (Liu et al. 2012).
    - MDI vector field is NOT provided — it is LOS only.
failure_modes:
  - MDI saturates above ~1500 G; high-flux sunspots are biased low — apply correction factor.
  - Synoptic-map pole interpolation prior to ~2003 is unreliable; use latitude limits.
  - Cosmic-ray streaks; flat-field changes across cooling cycles.
depends_on:
  []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: HMI succeeded MDI in 2010; cross-calibration between MDI and HMI needs explicit treatment when stitching multi-cycle synoptic maps.
    related_skills:
      - paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager
    proposed_action: compile a Liu-2012 MDI–HMI cross-calibration paper-skill
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# The Solar Oscillations Investigation — Michelson Doppler Imager — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving SOHO/MDI line-of-sight magnetograms, Dopplergrams, and continuum intensitygrams (1996–2010) for helioseismology and synoptic field mapping — central claim is that MDI's Michelson interferometer produces 96-min full-disk LOS magnetograms with ~2" pixel that serve as the canonical pre-HMI synoptic-field reference (Scherrer et al. 1995, Sol. Phys.).

Do NOT use this skill when:

- Do not extend MDI coverage past 2010-12 (HMI succeeded it).
- Do not use raw MDI synoptic maps for absolute flux without saturation correction (Liu et al. 2012).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SOHO/MDI imaged Ni I 6768 Å with two Michelson interferometers, returning intensity, Doppler, and LOS magnetograms in normal (96 min full-disk) and high-res (1024×1024 cropped) modes. Operational 1996-04 through 2010-12.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### MDI line-fit Doppler/magnetogram retrieval

- Paper reference: §4-5 Scherrer 1995
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### MDI saturation correction (Liu et al. 2012)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SOHO/MDI LOS magnetogram | L2 | 96 min full-disk | 1996-04..2010-12 | JSOC / VSO |
| SOHO/MDI synoptic map | L2 synoptic | Carrington rotation | 1996-04..2010-12 | JSOC |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- MDI saturates above ~1500 G; high-flux sunspots are biased low — apply correction factor.
- Synoptic-map pole interpolation prior to ~2003 is unreliable; use latitude limits.
- Cosmic-ray streaks; flat-field changes across cooling cycles.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SOHO/MDI imaged Ni I 6768 Å with two Michelson interferometers, returning intensity, Doppler, and LOS magnetograms in normal (96 min full-disk) and high-res (1024×1024 cropped) modes. Operational 1996-04 through 2010-12.

**Out of scope — do NOT generalize beyond:**

- Do not extend MDI coverage past 2010-12 (HMI succeeded it).
- Do not use raw MDI synoptic maps for absolute flux without saturation correction (Liu et al. 2012).
- MDI vector field is NOT provided — it is LOS only.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: http://jsoc.stanford.edu/MDI/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

- **Gap** — HMI succeeded MDI in 2010; cross-calibration between MDI and HMI needs explicit treatment when stitching multi-cycle synoptic maps. Proposed: compile a Liu-2012 MDI–HMI cross-calibration paper-skill.

## Weak entries / citation TODOs

- DOI not in local inventory; Sol. Phys. 162, 129 (1995)
