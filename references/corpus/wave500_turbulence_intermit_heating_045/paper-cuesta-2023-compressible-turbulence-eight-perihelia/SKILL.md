---
name: paper-cuesta-2023-compressible-turbulence-eight-perihelia
description: >-
  Use when working with the central claim of Manuel Enrique Cuesta et al. 2023 — Across
  PSP's first eight perihelia, compressible turbulence diagnostics (density-fluctuation
  amplitude δn/n, density spectral slope) show measurable radial trends and stream-
  dependence in the near-Sun environment. (arXiv:2305.03566; venue TODO verify).
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
  title: "Compressible Turbulence in the Near-Sun Solar Wind: Parker Solar Probe's First Eight Perihelia"
  first_author: "Manuel Enrique Cuesta"
  authors:
    - "Manuel Enrique Cuesta"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2305.03566"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [compressible, density-fluctuation, near-Sun, PSP]
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]
trigger_keywords:
  - "compressible turbulence PSP"
  - "first eight perihelia"
  - "density fluctuation amplitude"
  - "density spectral slope"
  - "Cuesta 2023 compressible"
  - "near-Sun"
data_products:
  - {instrument: "PSP/SWEAP SPC/SPAN-I", level: "L3", cadence: "~1 Hz", interval: "PSP P1-P8", archive: "CDAWeb / SPDF"}
  - {instrument: "PSP/FIELDS density (from quasi-thermal noise or sc-potential, TODO verify)", level: "derived", cadence: "TODO verify", interval: "Same", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Density-fluctuation δn/n statistics per perihelion"
    equation_refs: ["TODO verify"]
  - name: "Density PSD and slope estimation"
    equation_refs: ["TODO verify"]
  - name: "Radial-trend and stream-conditioning analysis"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2305.03566"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Compressible-turbulence diagnostics (δn/n, density-PSD slope) across PSP perihelia 1-8 on
    the analysed intervals.
  out_of_scope:
    - "Do not export trends to perihelia after P8 without re-running."
    - "Do not equate density-PSD slope with a unique cascade closure."
    - "Do not use intervals with low-confidence density retrievals."
failure_modes:
  - "Density-retrieval method (QTN vs sc-pot) introduces systematic bias."
  - "Plasma-moment cadence mismatch with MAG."
  - "Compressibility may interact with non-stationarity."
  - "Per-perihelion sample size differs."
depends_on:
  - cuesta-2022-compressible-turbulence-psp-themis-maven
  - paper-fu-2022-density-fluctuations-compressible-mhd-scaling
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill extends the analysis to PSP P9-P19."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2305.03566v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Manuel Enrique Cuesta et al. 2023 — Compressible Turbulence in the Near-Sun Solar Wind: Parker S... — paper-skill

> Compiled from arXiv:2305.03566. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Across PSP's first eight perihelia, compressible turbulence diagnostics (density-fluctuation amplitude δn/n, density spectral slope) show measurable radial trends and stream-dependence in the near-Sun environment.
- Reproducing or extending the analysis around PSP/SWEAP SPC/SPAN-I.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- low-confidence density retrievals
- P9+ extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Across PSP's first eight perihelia, compressible turbulence diagnostics (density-fluctuation amplitude δn/n, density spectral slope) show measurable radial trends and stream-dependence in the near-Sun environment.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Density-fluctuation δn/n statistics per perihelion
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Density PSD and slope estimation
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Radial-trend and stream-conditioning analysis
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/SWEAP SPC/SPAN-I | L3 | ~1 Hz | PSP P1-P8 | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| PSP/FIELDS density (from quasi-thermal noise or sc-potential, TODO verify) | derived | TODO verify | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Density-retrieval method (QTN vs sc-pot) introduces systematic bias.
- Plasma-moment cadence mismatch with MAG.
- Compressibility may interact with non-stationarity.
- Per-perihelion sample size differs.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Compressible-turbulence diagnostics (δn/n, density-PSD slope) across PSP perihelia 1-8 on the analysed intervals.

**Out of scope — do NOT generalize beyond:**

- Do not export trends to perihelia after P8 without re-running.
- Do not equate density-PSD slope with a unique cascade closure.
- Do not use intervals with low-confidence density retrievals.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2305.03566
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[cuesta-2022-compressible-turbulence-psp-themis-maven]] — sibling/upstream context for the same physics domain.
- [[paper-fu-2022-density-fluctuations-compressible-mhd-scaling]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill extends the analysis to PSP P9-P19.
