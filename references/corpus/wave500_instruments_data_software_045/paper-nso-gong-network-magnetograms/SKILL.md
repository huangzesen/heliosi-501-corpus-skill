---
name: paper-nso-gong-network-magnetograms
description: >-
  Use when needing continuous, near-real-time, ground-based full-disk LOS
  magnetograms (alternate to MDI/HMI when space-based data are unavailable) or
  pseudo-synoptic magnetograms for PFSS / WSA / ENLIL inputs — central claim is
  that the GONG network (Harvey et al. 1996, Science) provides minute-cadence
  ground-based magnetograms from a six-station global ring.
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
  title: The Global Oscillation Network Group (GONG) ground-based magnetograms
  first_author: "Harvey, J. W."
  year: 1996
  venue: Science
  doi: 10.1126/science.272.5266.1284
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - n/a
  regime:
    - corona
trigger_keywords:
  - GONG
  - Harvey 1996
  - ground-based magnetogram
  - pseudo-synoptic magnetogram GONG
  - NSO GONG
  - PFSS GONG input
  - ENLIL boundary
data_products:
  - instrument: GONG full-disk magnetogram
    level: L1/L2
    cadence: 1 min (network)
    interval: 1995-present
    archive: NSO GONG
  - instrument: GONG pseudo-synoptic / zero-point-corrected synoptic
    level: synoptic
    cadence: Carrington rotation
    interval: null
    archive: NSO GONG
algorithms:
  - name: Site-stitched 1-min magnetogram from network sites
    equation_refs:
      - Harvey 1996
    external_implementations: []
  - name: Synoptic-map assembly with longitude wedge averaging
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1126/science.272.5266.1284"
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://gong.nso.edu/"
claim_boundary:
  scope: >-
    GONG: six-station global network (Big Bear, Mauna Loa, Learmonth, Udaipur,
    El Teide, Cerro Tololo) imaging Ni I 6768 Å. Standard products: 1-min
    magnetograms, integrated synoptic maps, NRT magnetograms used by NOAA SWPC
    and CCMC.
  out_of_scope:
    - Do not treat GONG magnetograms as substitutes for HMI in absolute calibration — there are systematic offsets.
    - Do not use GONG-NRT for science without checking quality flags.
failure_modes:
  - Site-handover artifacts produce ~degree-scale stripes at handover times.
  - Seeing-dependent noise; nighttime sites have systematic offsets.
  - "Zero-level: GONG synoptic maps need NSO's pole-correction script for PFSS."
depends_on:
  []
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: No paper-skill yet covers the ADAPT data-assimilation product (Arge 2010) that ingests GONG into a flux-transport model for synoptic-map quality.
    related_skills: []
    proposed_action: compile an Arge ADAPT paper-skill
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: sioulas-reproduction/results/paper_skill_corpus/wave500_instruments_data_software_045/ (citation TODOs flagged for software-package stubs)
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, paper]
source_type: paper
---
# The Global Oscillation Network Group (GONG) ground-based magnetograms — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when needing continuous, near-real-time, ground-based full-disk LOS magnetograms (alternate to MDI/HMI when space-based data are unavailable) or pseudo-synoptic magnetograms for PFSS / WSA / ENLIL inputs — central claim is that the GONG network (Harvey et al. 1996, Science) provides minute-cadence ground-based magnetograms from a six-station global ring.

Do NOT use this skill when:

- Do not treat GONG magnetograms as substitutes for HMI in absolute calibration — there are systematic offsets.
- Do not use GONG-NRT for science without checking quality flags.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** GONG: six-station global network (Big Bear, Mauna Loa, Learmonth, Udaipur, El Teide, Cerro Tololo) imaging Ni I 6768 Å. Standard products: 1-min magnetograms, integrated synoptic maps, NRT magnetograms used by NOAA SWPC and CCMC.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Site-stitched 1-min magnetogram from network sites

- Paper reference: Harvey 1996
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### Synoptic-map assembly with longitude wedge averaging

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| GONG full-disk magnetogram | L1/L2 | 1 min (network) | 1995-present | NSO GONG |
| GONG pseudo-synoptic / zero-point-corrected synoptic | synoptic | Carrington rotation | — | NSO GONG |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Site-handover artifacts produce ~degree-scale stripes at handover times.
- Seeing-dependent noise; nighttime sites have systematic offsets.
- Zero-level: GONG synoptic maps need NSO's pole-correction script for PFSS.

## 7. Claim boundary  *(Layer 1)*

**In scope.** GONG: six-station global network (Big Bear, Mauna Loa, Learmonth, Udaipur, El Teide, Cerro Tololo) imaging Ni I 6768 Å. Standard products: 1-min magnetograms, integrated synoptic maps, NRT magnetograms used by NOAA SWPC and CCMC.

**Out of scope — do NOT generalize beyond:**

- Do not treat GONG magnetograms as substitutes for HMI in absolute calibration — there are systematic offsets.
- Do not use GONG-NRT for science without checking quality flags.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: https://doi.org/10.1126/science.272.5266.1284
- arXiv: n/a
- Code: n/a
- Data / archive: https://gong.nso.edu/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

- **Gap** — No paper-skill yet covers the ADAPT data-assimilation product (Arge 2010) that ingests GONG into a flux-transport model for synoptic-map quality. Proposed: compile an Arge ADAPT paper-skill.
