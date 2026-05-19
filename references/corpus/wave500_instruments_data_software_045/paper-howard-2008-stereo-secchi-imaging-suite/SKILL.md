---
name: paper-howard-2008-stereo-secchi-imaging-suite
description: >-
  Use when retrieving STEREO-A/B SECCHI EUV imager (EUVI), coronagraphs (COR1,
  COR2), and heliospheric imagers (HI1, HI2) for stereo-view CME tracking —
  central claim is that the SECCHI suite provides 4× nested FOV (0–215 R☉) on
  two spacecraft for 3D CME reconstruction (Howard et al. 2008, Space Sci.
  Rev.).
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
  title: Sun Earth Connection Coronal and Heliospheric Investigation (SECCHI)
  first_author: "Howard, R. A."
  year: 2008
  venue: Space Science Reviews
  doi: 10.1007/s11214-008-9341-4
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - STEREO
  regime:
    - corona
    - inner-heliosphere
trigger_keywords:
  - STEREO SECCHI
  - Howard 2008
  - EUVI
  - COR1 COR2
  - HI1 HI2 heliospheric imager
  - STEREO CME 3D
  - stereoscopic corona
data_products:
  - instrument: STEREO/SECCHI EUVI A/B
    level: L0/L1
    cadence: 2.5 min - 10 min (mode-dependent)
    interval: 2006-10..present (A); ..2014 (B)
    archive: STEREO Science Center / SPDF / VSO
  - instrument: STEREO/SECCHI COR1 / COR2
    level: L0/L1
    cadence: ~10 min
    interval: null
    archive: STEREO Science Center
  - instrument: STEREO/SECCHI HI1 / HI2
    level: L1/L2
    cadence: 40 min / 2 hr
    interval: null
    archive: STEREO Science Center
algorithms:
  - name: "secchi_prep (bias, flat, distortion, exposure normalization)"
    equation_refs:
      - §6 Howard 2008
    external_implementations:
      - SolarSoft secchi_prep.pro
  - name: J-map (time-elongation) from HI1+HI2 for CME tracking
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1007/s11214-008-9341-4"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://stereo-ssc.nascom.nasa.gov/"
claim_boundary:
  scope: >-
    STEREO/SECCHI: EUVI (full-Sun EUV, 4 bands 171/195/284/304 Å), COR1 (1.4–4
    R☉ K-cor), COR2 (2.5–15 R☉), HI1 (12-84 R☉), HI2 (66-318 R☉). Twin
    spacecraft A and B; B lost contact 2014; A continues.
  out_of_scope:
    - Do not use STEREO-B after 2014-10-01.
    - Do not treat HI photometry as absolute — F-corona and stellar background dominate.
    - Do not assume EUVI calibration matches AIA — separate radiometric calibrations.
failure_modes:
  - STEREO-B comms loss in 2014 — confirm spacecraft availability for any post-2014 query.
  - HI background subtraction requires running-difference or F-corona model; raw images do not show CMEs cleanly.
  - Cosmic-ray hit rate high beyond COR2; despiking essential.
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
# Sun Earth Connection Coronal and Heliospheric Investigation (SECCHI) — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving STEREO-A/B SECCHI EUV imager (EUVI), coronagraphs (COR1, COR2), and heliospheric imagers (HI1, HI2) for stereo-view CME tracking — central claim is that the SECCHI suite provides 4× nested FOV (0–215 R☉) on two spacecraft for 3D CME reconstruction (Howard et al. 2008, Space Sci. Rev.).

Do NOT use this skill when:

- Do not use STEREO-B after 2014-10-01.
- Do not treat HI photometry as absolute — F-corona and stellar background dominate.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** STEREO/SECCHI: EUVI (full-Sun EUV, 4 bands 171/195/284/304 Å), COR1 (1.4–4 R☉ K-cor), COR2 (2.5–15 R☉), HI1 (12-84 R☉), HI2 (66-318 R☉). Twin spacecraft A and B; B lost contact 2014; A continues.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### secchi_prep (bias, flat, distortion, exposure normalization)

- Paper reference: §6 Howard 2008
- External implementation(s): SolarSoft secchi_prep.pro
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### J-map (time-elongation) from HI1+HI2 for CME tracking

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| STEREO/SECCHI EUVI A/B | L0/L1 | 2.5 min - 10 min (mode-dependent) | 2006-10..present (A); ..2014 (B) | STEREO Science Center / SPDF / VSO |
| STEREO/SECCHI COR1 / COR2 | L0/L1 | ~10 min | — | STEREO Science Center |
| STEREO/SECCHI HI1 / HI2 | L1/L2 | 40 min / 2 hr | — | STEREO Science Center |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- STEREO-B comms loss in 2014 — confirm spacecraft availability for any post-2014 query.
- HI background subtraction requires running-difference or F-corona model; raw images do not show CMEs cleanly.
- Cosmic-ray hit rate high beyond COR2; despiking essential.

## 7. Claim boundary  *(Layer 1)*

**In scope.** STEREO/SECCHI: EUVI (full-Sun EUV, 4 bands 171/195/284/304 Å), COR1 (1.4–4 R☉ K-cor), COR2 (2.5–15 R☉), HI1 (12-84 R☉), HI2 (66-318 R☉). Twin spacecraft A and B; B lost contact 2014; A continues.

**Out of scope — do NOT generalize beyond:**

- Do not use STEREO-B after 2014-10-01.
- Do not treat HI photometry as absolute — F-corona and stellar background dominate.
- Do not assume EUVI calibration matches AIA — separate radiometric calibrations.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1007/s11214-008-9341-4
- arXiv: n/a
- Code: n/a
- Data / archive: https://stereo-ssc.nascom.nasa.gov/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.
