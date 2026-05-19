---
name: paper-shankarappa-2025-ion-scale-waves-free-energy-survey
description: >-
  Use when working with the central claim of Niranjana Shankarappa et al. 2025 — A mission-
  wide PSP survey links left-handed circularly polarised ion-scale waves to specific free-
  energy sources in proton VDFs and finds the left-handed wave occurrence rises closer to
  the Sun, reaching ~30 percent. (arXiv:2512.11182; venue TODO verify).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: true
paper:
  title: "Free Energy Sources of Ion-scale Waves Observed by Parker Solar Probe"
  first_author: "Niranjana Shankarappa"
  authors:
    - "Niranjana Shankarappa"
    - "Kristopher G. Klein"
    - "Mihailo M. Martinović"
    - "Trevor A. Bowen"
    - "Davin E. Larson"
    - "Roberto Livi"
  year: 2025
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2512.11182"
  ads_bibcode: null
domain:
  primary_theme: waves_instabilities
  secondary_themes: [ion-scale-waves, free-energy, turbulence, heating]
  missions: [PSP]
  regime: [inner-heliosphere, ion-scale]
trigger_keywords:
  - "ion-scale waves PSP"
  - "left-handed circular polarised wave"
  - "free-energy source VDF"
  - "Shankarappa 2025 survey"
  - "wave-particle interaction"
  - "mission-wide statistics"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "burst", interval: "Mission-wide PSP", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/SWEAP SPAN-I", level: "L3", cadence: "~1 Hz VDFs", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Mission-wide PSP ion-scale wave identification"
    equation_refs: ["TODO verify"]
  - name: "Per-wave-type free-energy-source attribution using SPAN-I VDFs"
    equation_refs: ["TODO verify"]
  - name: "Radial-distance occurrence rate"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2512.11182"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    PSP mission-wide statistics on ion-scale wave occurrence and free-energy-source
    attribution, conditioned on the paper's wave-identification rule.
  out_of_scope:
    - "Do not assume the same occurrence rate outside PSP's perihelion range."
    - "Do not generalise the free-energy attribution to electron-scale waves."
    - "Do not equate left-handed wave occurrence with absolute heating rate."
failure_modes:
  - "Wave-identification rule (band, polarisation threshold) biases occurrence count."
  - "SPAN-I VDF cadence limits per-event free-energy attribution."
  - "Burst-mode duty cycle creates window-selection bias."
  - "Local-mean-field direction estimator dependency."
depends_on:
  - bowen-2024-extended-cyclotron-resonant-heating
  - verniero-2020-proton-beams-ion-scale-waves
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill systematically links wave occurrence to ion-heating-rate inferences from radial-temperature gradients."
  - type: minimal_experiment
    statement: "Condition heating-rate inferences from radial gradients on wave-occurrence bins and report joint correlation."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md item 7"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, waves_instabilities]
---

# Niranjana Shankarappa et al. 2025 — Free Energy Sources of Ion-scale Waves Observed by Parker So... — paper-skill

> Compiled from arXiv:2512.11182. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- A mission-wide PSP survey links left-handed circularly polarised ion-scale waves to specific free-energy sources in proton VDFs and finds the left-handed wave occurrence rises closer to the Sun, reaching ~30 percent.
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether waves_instabilities-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- electron-scale wave extrapolation
- absolute heating rate from occurrence alone

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A mission-wide PSP survey links left-handed circularly polarised ion-scale waves to specific free-energy sources in proton VDFs and finds the left-handed wave occurrence rises closer to the Sun, reaching ~30 percent.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Mission-wide PSP ion-scale wave identification
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Per-wave-type free-energy-source attribution using SPAN-I VDFs
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Radial-distance occurrence rate
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | burst | Mission-wide PSP | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/SWEAP SPAN-I | L3 | ~1 Hz VDFs | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Wave-identification rule (band, polarisation threshold) biases occurrence count.
- SPAN-I VDF cadence limits per-event free-energy attribution.
- Burst-mode duty cycle creates window-selection bias.
- Local-mean-field direction estimator dependency.

## 7. Claim boundary  *(Layer 1)*

**In scope.** PSP mission-wide statistics on ion-scale wave occurrence and free-energy-source attribution, conditioned on the paper's wave-identification rule.

**Out of scope — do NOT generalize beyond:**

- Do not assume the same occurrence rate outside PSP's perihelion range.
- Do not generalise the free-energy attribution to electron-scale waves.
- Do not equate left-handed wave occurrence with absolute heating rate.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2512.11182
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[bowen-2024-extended-cyclotron-resonant-heating]] — sibling/upstream context for the same physics domain.
- [[verniero-2020-proton-beams-ion-scale-waves]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill systematically links wave occurrence to ion-heating-rate inferences from radial-temperature gradients.
- **Minimal_experiment** — Condition heating-rate inferences from radial gradients on wave-occurrence bins and report joint correlation.
