---
name: paper-delaboudiniere-1995-soho-eit-extreme-uv-telescope
description: >-
  Use when retrieving SOHO/EIT full-disk EUV images (171, 195, 284, 304 Å) from
  1996 onward for chromosphere/corona context — central claim is that EIT
  produces 12-min cadence (synoptic) full-disk EUV in four bandpasses with ~2.6"
  pixels, suitable for long-baseline coronal/cycle studies (Delaboudinière et
  al. 1995, Sol. Phys.).
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
  title: "EIT: Extreme-ultraviolet Imaging Telescope for the SOHO mission"
  first_author: "Delaboudinière, J.-P."
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
  - SOHO EIT
  - Delaboudinière 1995
  - EUV imager corona
  - Fe XII 195
  - He II 304
  - synoptic EUV
  - SOHO coronal imaging
data_products:
  - instrument: SOHO/EIT
    level: L1 quick-look + L2 calibrated
    cadence: ~12 min (synoptic)
    interval: 1996-present
    archive: SOHO archive / SPDF / VSO
algorithms:
  - name: "EIT prep (flat field, CCD bias, degradation correction)"
    equation_refs:
      - §5 Delaboudinière 1995
    external_implementations:
      - SolarSoft eit_prep.pro
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://sohowww.nascom.nasa.gov/"
claim_boundary:
  scope: >-
    SOHO/EIT: normal-incidence multilayer EUV imager, 1024×1024 CCD, four
    bandpasses (Fe IX/X 171 Å, Fe XII 195 Å, Fe XV 284 Å, He II 304 Å). Operates
    since 1996; full-disk synoptic cadence ~12 min plus campaign modes.
  out_of_scope:
    - Do not use EIT for short-timescale (sub-30 s) imaging — operates at ~minute cadence.
    - Do not assume CCD response constant — flat-field and degradation correction required.
    - Do not extend EIT calibration claims to non-Fe (e.g. 304 Å He II) without separate radiometric checks.
failure_modes:
  - "Long-term CCD degradation: response in 195 Å dropped ~20% over years 1-3; use degradation curves."
  - Bake-out periods produce data gaps; mask before time-series.
  - Off-pointing campaigns shift FOV; check pointing keyword.
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
# EIT: Extreme-ultraviolet Imaging Telescope for the SOHO mission — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving SOHO/EIT full-disk EUV images (171, 195, 284, 304 Å) from 1996 onward for chromosphere/corona context — central claim is that EIT produces 12-min cadence (synoptic) full-disk EUV in four bandpasses with ~2.6" pixels, suitable for long-baseline coronal/cycle studies (Delaboudinière et al. 1995, Sol. Phys.).

Do NOT use this skill when:

- Do not use EIT for short-timescale (sub-30 s) imaging — operates at ~minute cadence.
- Do not assume CCD response constant — flat-field and degradation correction required.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SOHO/EIT: normal-incidence multilayer EUV imager, 1024×1024 CCD, four bandpasses (Fe IX/X 171 Å, Fe XII 195 Å, Fe XV 284 Å, He II 304 Å). Operates since 1996; full-disk synoptic cadence ~12 min plus campaign modes.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### EIT prep (flat field, CCD bias, degradation correction)

- Paper reference: §5 Delaboudinière 1995
- External implementation(s): SolarSoft eit_prep.pro
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SOHO/EIT | L1 quick-look + L2 calibrated | ~12 min (synoptic) | 1996-present | SOHO archive / SPDF / VSO |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Long-term CCD degradation: response in 195 Å dropped ~20% over years 1-3; use degradation curves.
- Bake-out periods produce data gaps; mask before time-series.
- Off-pointing campaigns shift FOV; check pointing keyword.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SOHO/EIT: normal-incidence multilayer EUV imager, 1024×1024 CCD, four bandpasses (Fe IX/X 171 Å, Fe XII 195 Å, Fe XV 284 Å, He II 304 Å). Operates since 1996; full-disk synoptic cadence ~12 min plus campaign modes.

**Out of scope — do NOT generalize beyond:**

- Do not use EIT for short-timescale (sub-30 s) imaging — operates at ~minute cadence.
- Do not assume CCD response constant — flat-field and degradation correction required.
- Do not extend EIT calibration claims to non-Fe (e.g. 304 Å He II) without separate radiometric checks.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://sohowww.nascom.nasa.gov/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Sol. Phys. 162, 291 (1995)
