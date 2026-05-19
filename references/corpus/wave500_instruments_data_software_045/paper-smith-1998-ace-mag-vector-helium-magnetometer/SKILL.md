---
name: paper-smith-1998-ace-mag-vector-helium-magnetometer
description: >-
  Use when retrieving long-baseline (since Aug 1997) L1 vector magnetic field
  from ACE/MAG dual triaxial fluxgate magnetometers — central claim is that
  ACE/MAG delivers 1 / 3 / 4 / 16 / 64 / 86400 s cadence vector B at 0.01 nT
  resolution suitable as the canonical multi-decade solar-wind B reference
  (Smith et al. 1998, Space Sci. Rev.).
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
  title: The ACE Magnetic Fields Experiment
  first_author: "Smith, C. W."
  year: 1998
  venue: Space Science Reviews
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: magnetic_field
  secondary_themes: []
  missions:
    - ACE
  regime:
    - 1au
trigger_keywords:
  - ACE MAG
  - Smith 1998
  - ACE magnetometer
  - L1 long baseline B
  - ACE Science Center
  - ACE vector magnetic field
  - fluxgate L1
  - solar wind magnetic monitor
data_products:
  - instrument: ACE/MAG
    level: L2
    cadence: "1 s, 16 s, 1 min, 1 hour"
    interval: null
    archive: SPDF / CDAWeb / ACE Science Center
algorithms:
  - name: ACE/MAG offset and gain calibration
    equation_refs:
      - §3 Smith 1998
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/pub/data/ace/mag/"
claim_boundary:
  scope: >-
    ACE/MAG is a pair of triaxial fluxgate sensors on a 4.19 m boom at L1; in-
    flight since Aug 1997; vector products at 1 s, 16 s, 1 min, 1 hour, daily,
    and a high-resolution 1/3 s frame.
  out_of_scope:
    - Do not extrapolate to electron-scale dynamics — fluxgate Nyquist is sub-Hz.
    - Do not assume offsets are constant across the multi-decade mission; long-term recalibration is documented.
failure_modes:
  - Long-term zero-level drift can introduce ~0.1 nT spurious mean field unless corrected with rotational analysis.
  - "Spin tone removed in L2, but raw L1 still carries it."
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
# The ACE Magnetic Fields Experiment — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving long-baseline (since Aug 1997) L1 vector magnetic field from ACE/MAG dual triaxial fluxgate magnetometers — central claim is that ACE/MAG delivers 1 / 3 / 4 / 16 / 64 / 86400 s cadence vector B at 0.01 nT resolution suitable as the canonical multi-decade solar-wind B reference (Smith et al. 1998, Space Sci. Rev.).

Do NOT use this skill when:

- Do not extrapolate to electron-scale dynamics — fluxgate Nyquist is sub-Hz.
- Do not assume offsets are constant across the multi-decade mission; long-term recalibration is documented.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** ACE/MAG is a pair of triaxial fluxgate sensors on a 4.19 m boom at L1; in-flight since Aug 1997; vector products at 1 s, 16 s, 1 min, 1 hour, daily, and a high-resolution 1/3 s frame.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### ACE/MAG offset and gain calibration

- Paper reference: §3 Smith 1998
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| ACE/MAG | L2 | 1 s, 16 s, 1 min, 1 hour | — | SPDF / CDAWeb / ACE Science Center |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Long-term zero-level drift can introduce ~0.1 nT spurious mean field unless corrected with rotational analysis.
- Spin tone removed in L2, but raw L1 still carries it.

## 7. Claim boundary  *(Layer 1)*

**In scope.** ACE/MAG is a pair of triaxial fluxgate sensors on a 4.19 m boom at L1; in-flight since Aug 1997; vector products at 1 s, 16 s, 1 min, 1 hour, daily, and a high-resolution 1/3 s frame.

**Out of scope — do NOT generalize beyond:**

- Do not extrapolate to electron-scale dynamics — fluxgate Nyquist is sub-Hz.
- Do not assume offsets are constant across the multi-decade mission; long-term recalibration is documented.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://cdaweb.gsfc.nasa.gov/pub/data/ace/mag/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Space Sci. Rev. 86, 613 (1998)
