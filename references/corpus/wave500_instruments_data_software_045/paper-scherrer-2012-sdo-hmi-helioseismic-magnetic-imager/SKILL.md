---
name: paper-scherrer-2012-sdo-hmi-helioseismic-magnetic-imager
description: >-
  Use when retrieving SDO/HMI line-of-sight or vector magnetograms,
  Dopplergrams, and continuum intensitygrams (Fe I 6173 Å) — central claim is
  that HMI delivers 45 s LOS magnetograms (4096²) and 12-min vector magnetograms
  with photospheric accuracy on a continuous mission cadence (Scherrer et al.
  2012, Sol. Phys.).
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
  title: The Helioseismic and Magnetic Imager (HMI) Investigation for the Solar Dynamics Observatory
  first_author: "Scherrer, P. H."
  year: 2012
  venue: Solar Physics
  doi: 10.1007/s11207-011-9834-2
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
  regime:
    - corona
trigger_keywords:
  - SDO HMI
  - Scherrer 2012
  - HMI vector magnetogram
  - SHARP
  - JSOC HMI
  - photospheric magnetic field SDO
  - VFISV
  - Carrington synoptic magnetogram HMI
data_products:
  - instrument: SDO/HMI LOS magnetogram
    level: L1.5
    cadence: 45 s
    interval: 2010-05..present
    archive: JSOC
  - instrument: SDO/HMI vector magnetogram
    level: L2
    cadence: 12 min
    interval: 2010-05..present
    archive: JSOC
  - instrument: "SDO/HMI synoptic map (hmi.synoptic_*)"
    level: synoptic
    cadence: Carrington rotation
    interval: 2010-05..present
    archive: JSOC
  - instrument: SDO/HMI SHARP cutouts
    level: derived
    cadence: 12 min
    interval: 2010-05..present
    archive: JSOC
algorithms:
  - name: VFISV Milne-Eddington vector inversion
    equation_refs:
      - §5 Scherrer 2012; Hoeksema 2014
    external_implementations:
      - github.com/asensior-hub
  - name: 180° azimuth disambiguation (minimum-energy)
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1007/s11207-011-9834-2"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "http://jsoc.stanford.edu/"
claim_boundary:
  scope: >-
    SDO/HMI imaged Fe I 6173 Å with two cameras (front and side), producing LOS
    magnetograms at 45 s and vector magnetograms at 12 min via Milne-Eddington
    inversion. Synoptic Carrington-rotation maps and SHARP (Spaceweather Active
    Region Patch) cutouts are standard derived products.
  out_of_scope:
    - Do not treat 720 s vector products and 45 s LOS products as the same — they are independently calibrated.
    - Do not use HMI vector data near the limb without disambiguation flags (Hoeksema 2014).
    - Do not skip the 180° azimuth disambiguation step.
failure_modes:
  - Daily eclipse season (SDO velocity through Earth shadow) injects pointing offsets; check QUALITY keyword.
  - Limb data noisier; SHARPs near limb biased.
  - "Magnetic activity-dependent saturation, especially during X-class flares."
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
# The Helioseismic and Magnetic Imager (HMI) Investigation for the Solar Dynamics Observatory — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving SDO/HMI line-of-sight or vector magnetograms, Dopplergrams, and continuum intensitygrams (Fe I 6173 Å) — central claim is that HMI delivers 45 s LOS magnetograms (4096²) and 12-min vector magnetograms with photospheric accuracy on a continuous mission cadence (Scherrer et al. 2012, Sol. Phys.).

Do NOT use this skill when:

- Do not treat 720 s vector products and 45 s LOS products as the same — they are independently calibrated.
- Do not use HMI vector data near the limb without disambiguation flags (Hoeksema 2014).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SDO/HMI imaged Fe I 6173 Å with two cameras (front and side), producing LOS magnetograms at 45 s and vector magnetograms at 12 min via Milne-Eddington inversion. Synoptic Carrington-rotation maps and SHARP (Spaceweather Active Region Patch) cutouts are standard derived products.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### VFISV Milne-Eddington vector inversion

- Paper reference: §5 Scherrer 2012; Hoeksema 2014
- External implementation(s): github.com/asensior-hub
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### 180° azimuth disambiguation (minimum-energy)

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| SDO/HMI LOS magnetogram | L1.5 | 45 s | 2010-05..present | JSOC |
| SDO/HMI vector magnetogram | L2 | 12 min | 2010-05..present | JSOC |
| SDO/HMI synoptic map (hmi.synoptic_*) | synoptic | Carrington rotation | 2010-05..present | JSOC |
| SDO/HMI SHARP cutouts | derived | 12 min | 2010-05..present | JSOC |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Daily eclipse season (SDO velocity through Earth shadow) injects pointing offsets; check QUALITY keyword.
- Limb data noisier; SHARPs near limb biased.
- Magnetic activity-dependent saturation, especially during X-class flares.

## 7. Claim boundary  *(Layer 1)*

**In scope.** SDO/HMI imaged Fe I 6173 Å with two cameras (front and side), producing LOS magnetograms at 45 s and vector magnetograms at 12 min via Milne-Eddington inversion. Synoptic Carrington-rotation maps and SHARP (Spaceweather Active Region Patch) cutouts are standard derived products.

**Out of scope — do NOT generalize beyond:**

- Do not treat 720 s vector products and 45 s LOS products as the same — they are independently calibrated.
- Do not use HMI vector data near the limb without disambiguation flags (Hoeksema 2014).
- Do not skip the 180° azimuth disambiguation step.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1007/s11207-011-9834-2
- arXiv: n/a
- Code: n/a
- Data / archive: http://jsoc.stanford.edu/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.
