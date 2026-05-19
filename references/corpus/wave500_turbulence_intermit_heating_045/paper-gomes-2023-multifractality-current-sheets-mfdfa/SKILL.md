---
name: paper-gomes-2023-multifractality-current-sheets-mfdfa
description: >-
  Use when working with the central claim of Leonardo F. Gomes et al. 2023 — Multifractal-
  Detrended-Fluctuation-Analysis (MFDFA) on solar-wind magnetic-field time series shows
  current-sheet removal substantially reduces multifractality, with surrogate-data and
  volatility tests separating heavy-tail vs nonlinear-correlation contributions.
  (arXiv:2301.02118; venue TODO verify).
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
  title: "Origin of Multifractality in Solar Wind Turbulence: the Role of Current Sheets"
  first_author: "Leonardo F. Gomes"
  authors:
    - "Leonardo F. Gomes"
    - "Tiago F. P. Gomes"
    - "Erico L. Rempel"
    - "Silvio Gama"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2301.02118"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, multifractal, current-sheets]
  missions: [other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "MFDFA"
  - "multifractality"
  - "current sheets"
  - "heavy-tail surrogates"
  - "volatility analysis"
  - "Gomes Rempel Gama 2023"
  - "intermittency origin"
data_products:
  - {instrument: "In-situ MAG (mission TODO verify)", level: "L2", cadence: "TODO verify", interval: "TODO verify interval", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Multifractal-Detrended-Fluctuation-Analysis (MFDFA)"
    equation_refs: ["TODO verify Eq."]
  - name: "Current-sheet identification + removal"
    equation_refs: ["TODO verify"]
  - name: "Surrogate-data heavy-tail test (IAAFT)"
    equation_refs: ["TODO verify"]
  - name: "Volatility-series analysis"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2301.02118"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    MFDFA-derived multifractal spectrum width of solar-wind B time series reduces measurably
    after current-sheet excision; surrogate and volatility decompositions isolate heavy-tail
    vs correlation contributions.
  out_of_scope:
    - "Do not assert current sheets are the unique source of multifractality without quantifying residual width."
    - "Do not generalise MFDFA findings to compressible density turbulence without re-analysis."
    - "Do not equate the surrogate IAAFT null with a physical null model of pure-Gaussian turbulence."
failure_modes:
  - "Current-sheet detector threshold (PVI, |dB|/dt) tightly controls excision count."
  - "MFDFA q-range choice changes spectrum width."
  - "Insufficient surrogate ensemble inflates p-values."
  - "Volatility series amplifies edge effects of windowing."
depends_on:
  - sioulas-2022-magnetic-field-intermittency-psp-solo
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill applies the same MFDFA pipeline to PSP near-Sun data where current-sheet density is higher."
  - type: minimal_experiment
    statement: "Apply MFDFA before/after PVI-based current-sheet removal to PSP E1-E13 and report Δ(width)."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2023 item 10"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Leonardo F. Gomes et al. 2023 — Origin of Multifractality in Solar Wind Turbulence: the Role... — paper-skill

> Compiled from arXiv:2301.02118. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Multifractal-Detrended-Fluctuation-Analysis (MFDFA) on solar-wind magnetic-field time series shows current-sheet removal substantially reduces multifractality, with surrogate-data and volatility tests separating heavy-tail vs nonlinear-correlation contributions.
- Reproducing or extending the analysis around In-situ MAG (mission TODO verify).
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- compressible-density multifractality without re-running
- branch identification of dissipation channels

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Multifractal-Detrended-Fluctuation-Analysis (MFDFA) on solar-wind magnetic-field time series shows current-sheet removal substantially reduces multifractality, with surrogate-data and volatility tests separating heavy-tail vs nonlinear-correlation contributions.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Multifractal-Detrended-Fluctuation-Analysis (MFDFA)
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Current-sheet identification + removal
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Surrogate-data heavy-tail test (IAAFT)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Volatility-series analysis
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ MAG (mission TODO verify) | L2 | TODO verify | TODO verify interval | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Current-sheet detector threshold (PVI, |dB|/dt) tightly controls excision count.
- MFDFA q-range choice changes spectrum width.
- Insufficient surrogate ensemble inflates p-values.
- Volatility series amplifies edge effects of windowing.

## 7. Claim boundary  *(Layer 1)*

**In scope.** MFDFA-derived multifractal spectrum width of solar-wind B time series reduces measurably after current-sheet excision; surrogate and volatility decompositions isolate heavy-tail vs correlation contributions.

**Out of scope — do NOT generalize beyond:**

- Do not assert current sheets are the unique source of multifractality without quantifying residual width.
- Do not generalise MFDFA findings to compressible density turbulence without re-analysis.
- Do not equate the surrogate IAAFT null with a physical null model of pure-Gaussian turbulence.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2301.02118
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[sioulas-2022-magnetic-field-intermittency-psp-solo]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill applies the same MFDFA pipeline to PSP near-Sun data where current-sheet density is higher.
- **Minimal_experiment** — Apply MFDFA before/after PVI-based current-sheet removal to PSP E1-E13 and report Δ(width).
