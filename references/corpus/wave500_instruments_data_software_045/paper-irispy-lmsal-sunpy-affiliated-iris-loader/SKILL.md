---
name: paper-irispy-lmsal-sunpy-affiliated-iris-loader
description: >-
  Use when reading IRIS Slit-Jaw Imager (SJI) or spectrograph (SG) Level-2 data
  in Python — central claim is that irispy-lmsal (a sunraster-based, SunPy-
  affiliated package maintained at LMSAL) is the official Python replacement for
  IDL iris_obj_load (no standalone publication located in local inventory).
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
  title: irispy-lmsal — IRIS spectrograph data loading in Python
  first_author: irispy-lmsal developers
  year: 2024
  venue: software package (SunPy affiliated; no dedicated paper in local inventory)
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
  - irispy-lmsal
  - IRIS Python
  - IRIS spectrograph
  - IRIS SJI
  - IRIS L2 loader
data_products:
  - instrument: IRIS SJI (slit-jaw imager)
    level: L2
    cadence: raster-dependent
    interval: 2013-present
    archive: LMSAL IRIS
  - instrument: IRIS SG (spectrograph)
    level: L2
    cadence: raster-dependent
    interval: 2013-present
    archive: LMSAL IRIS
algorithms:
  - name: SJI co-alignment with SG via WCS metadata
    equation_refs: []
    external_implementations:
      - "https://github.com/LM-SAL/irispy-lmsal"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/LM-SAL/irispy-lmsal"
  data_repo: null
claim_boundary:
  scope: >-
    irispy-lmsal: provides Raster + SJICube readers for IRIS L2 SJI/SG; built on
    sunraster + ndcube. Co-aligns SJI with SG, handles per-observation OBS-IDs.
  out_of_scope:
    - Do not assume irispy-lmsal handles IRIS L1.5 — it consumes L2 files.
    - "Do not bypass LMSAL's documented response curve when computing absolute irradiance."
failure_modes:
  - Some early IRIS OBS-IDs have mis-aligned SJI/SG pointing; check the obs-id index.
depends_on:
  - paper-sunraster-sunpy-affiliated-raster-spectra
adapter_notes: []
research_generation_affordances: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# irispy-lmsal — IRIS spectrograph data loading in Python — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when reading IRIS Slit-Jaw Imager (SJI) or spectrograph (SG) Level-2 data in Python — central claim is that irispy-lmsal (a sunraster-based, SunPy-affiliated package maintained at LMSAL) is the official Python replacement for IDL iris_obj_load (no standalone publication located in local inventory).

Do NOT use this skill when:

- Do not assume irispy-lmsal handles IRIS L1.5 — it consumes L2 files.
- Do not bypass LMSAL's documented response curve when computing absolute irradiance.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** irispy-lmsal: provides Raster + SJICube readers for IRIS L2 SJI/SG; built on sunraster + ndcube. Co-aligns SJI with SG, handles per-observation OBS-IDs.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### SJI co-alignment with SG via WCS metadata

- External implementation(s): https://github.com/LM-SAL/irispy-lmsal
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| IRIS SJI (slit-jaw imager) | L2 | raster-dependent | 2013-present | LMSAL IRIS |
| IRIS SG (spectrograph) | L2 | raster-dependent | 2013-present | LMSAL IRIS |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Some early IRIS OBS-IDs have mis-aligned SJI/SG pointing; check the obs-id index.

## 7. Claim boundary  *(Layer 1)*

**In scope.** irispy-lmsal: provides Raster + SJICube readers for IRIS L2 SJI/SG; built on sunraster + ndcube. Co-aligns SJI with SG, handles per-observation OBS-IDs.

**Out of scope — do NOT generalize beyond:**

- Do not assume irispy-lmsal handles IRIS L1.5 — it consumes L2 files.
- Do not bypass LMSAL's documented response curve when computing absolute irradiance.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://github.com/LM-SAL/irispy-lmsal
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

- `[[paper-sunraster-sunpy-affiliated-raster-spectra]]`

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- No standalone publication located; citation TODO
