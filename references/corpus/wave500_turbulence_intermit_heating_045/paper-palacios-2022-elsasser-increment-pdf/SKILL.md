---
name: paper-palacios-2022-elsasser-increment-pdf
description: >-
  Use when working with the central claim of Juan C. Palacios et al. 2022 — PDFs of Elsasser
  increments at 1 au (WIND 1995-2017) and 2048^3 reduced-MHD simulations share an
  exponential-tail decrement alpha_l proportional to l^(-mu) under Alfvenicity conditioning.
  (arXiv:2209.09152; venue TODO verify).
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
  title: "On the Statistics of Elsässer Increments in Solar Wind and Magnetohydrodynamic Turbulence"
  first_author: "Juan C. Palacios"
  authors:
    - "Juan C. Palacios"
    - "Sofiane Bourouaine"
    - "Jean C. Perez"
  year: 2022
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2209.09152"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [intermittency, statistics, simulation-comparison]
  missions: [Wind, other]
  regime: [1au, MHD-scale]
trigger_keywords:
  - "Elsasser increment PDF"
  - "exponential tail decrement"
  - "reduced MHD comparison"
  - "alpha_l scale dependence"
  - "WIND statistics"
  - "Palacios Bourouaine Perez 2022"
  - "universality test"
data_products:
  - {instrument: "Wind/MFI MAG", level: "L2", cadence: "TODO verify", interval: "1995-2017", archive: "CDAWeb / SPDF"}
  - {instrument: "Wind/SWE plasma", level: "L2", cadence: "TODO verify", interval: "Same", archive: "CDAWeb / SPDF"}
  - {instrument: "2048^3 reduced-MHD simulation", level: "derived", cadence: "n/a", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "Elsasser increment PDF construction"
    equation_refs: ["TODO verify Eq."]
  - name: "Exponential-tail decrement fit alpha_l(l)"
    equation_refs: ["TODO verify"]
  - name: "Alfvenicity-conditioned PDF subsamples"
    equation_refs: ["TODO verify"]
  - name: "Observation vs simulation overlay"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2209.09152"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    WIND 1995-2017 1-au z± increment PDFs and matched 2048^3 reduced-MHD simulations share an
    exponential-tail decrement alpha_l scaling with lag.
  out_of_scope:
    - "Do not extend the universality claim to PSP near-Sun data without re-running the analysis."
    - "Do not equate observational and simulation tails when sample sizes differ by orders of magnitude without resampling."
    - "Do not interpret the tail exponent as a single intermittency parameter; it is a PDF-shape decrement, not a structure-function index."
failure_modes:
  - "Sample-size mismatch between WIND and simulation distorts tail estimation."
  - "Detrending choice for slow-varying mean B shifts the increment PDF symmetry."
  - "Alfvenicity cut threshold biases which intervals enter the conditional PDF."
  - "Simulation reduced-MHD assumptions (low compressibility) need an in-situ δn/n filter to match."
depends_on:
  - sioulas-2022-magnetic-field-intermittency-psp-solo
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No sibling skill provides a PSP near-Sun version of the same exponential-tail decrement test."
  - type: hypothesis
    statement: "If the decrement is truly universal, near-Sun PSP Elsasser PDFs should obey alpha_l proportional to l^(-mu) with mu within tolerance of the 1-au value."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/solar_wind_turbulence_2020_2026.md #2022 item 8"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Juan C. Palacios et al. 2022 — On the Statistics of Elsässer Increments in Solar Wind and M... — paper-skill

> Compiled from arXiv:2209.09152. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- PDFs of Elsasser increments at 1 au (WIND 1995-2017) and 2048^3 reduced-MHD simulations share an exponential-tail decrement alpha_l proportional to l^(-mu) under Alfvenicity conditioning.
- Reproducing or extending the analysis around Wind/MFI MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- near-Sun PSP analysis without re-running
- direct structure-function exponent extraction

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** PDFs of Elsasser increments at 1 au (WIND 1995-2017) and 2048^3 reduced-MHD simulations share an exponential-tail decrement alpha_l proportional to l^(-mu) under Alfvenicity conditioning.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Elsasser increment PDF construction
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Exponential-tail decrement fit alpha_l(l)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Alfvenicity-conditioned PDF subsamples
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Observation vs simulation overlay
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Wind/MFI MAG | L2 | TODO verify | 1995-2017 | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| Wind/SWE plasma | L2 | TODO verify | Same | CDAWeb / SPDF | fetch+decode CDF; subset by time |
| 2048^3 reduced-MHD simulation | derived | n/a | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Sample-size mismatch between WIND and simulation distorts tail estimation.
- Detrending choice for slow-varying mean B shifts the increment PDF symmetry.
- Alfvenicity cut threshold biases which intervals enter the conditional PDF.
- Simulation reduced-MHD assumptions (low compressibility) need an in-situ δn/n filter to match.

## 7. Claim boundary  *(Layer 1)*

**In scope.** WIND 1995-2017 1-au z± increment PDFs and matched 2048^3 reduced-MHD simulations share an exponential-tail decrement alpha_l scaling with lag.

**Out of scope — do NOT generalize beyond:**

- Do not extend the universality claim to PSP near-Sun data without re-running the analysis.
- Do not equate observational and simulation tails when sample sizes differ by orders of magnitude without resampling.
- Do not interpret the tail exponent as a single intermittency parameter; it is a PDF-shape decrement, not a structure-function index.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2209.09152
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[sioulas-2022-magnetic-field-intermittency-psp-solo]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Gap** — No sibling skill provides a PSP near-Sun version of the same exponential-tail decrement test.
- **Hypothesis** — If the decrement is truly universal, near-Sun PSP Elsasser PDFs should obey alpha_l proportional to l^(-mu) with mu within tolerance of the 1-au value.
