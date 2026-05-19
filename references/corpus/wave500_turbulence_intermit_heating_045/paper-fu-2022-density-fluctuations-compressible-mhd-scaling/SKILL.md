---
name: paper-fu-2022-density-fluctuations-compressible-mhd-scaling
description: >-
  Use when working with the central claim of Xiangrong Fu et al. 2022 — Compressible-MHD
  simulations characterise the scaling of density-fluctuation amplitude with turbulent Mach
  number and beta and predict an observable signature in solar-wind density spectra.
  (arXiv:2207.09490; venue TODO verify).
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
  title: "Nature and Scalings of Density Fluctuations of Compressible MHD Turbulence with Applications to the Solar Wind"
  first_author: "Xiangrong Fu"
  authors:
    - "Xiangrong Fu"
  year: 2022
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2207.09490"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [compressible, density-fluctuations, scaling-law, simulation]
  missions: [n/a]
  regime: [MHD-scale, fluid]
trigger_keywords:
  - "compressible MHD density scaling"
  - "turbulent Mach number"
  - "beta dependence"
  - "density amplitude scaling"
  - "Fu 2022 compressible"
  - "solar-wind density spectrum"
data_products:
  - {instrument: "Compressible-MHD simulation output", level: "derived", cadence: "TODO verify dt", interval: "n/a", archive: "Authors' archive (TODO verify)"}
algorithms:
  - name: "Compressible-MHD simulation across (Ms, beta) range"
    equation_refs: ["TODO verify"]
  - name: "Density-amplitude scaling extraction"
    equation_refs: ["TODO verify"]
  - name: "Predicted in-situ-observable signature"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2207.09490"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the simulated (Ms, beta) parameter range, the derived density-amplitude scaling and
    predicted observable signature.
  out_of_scope:
    - "Do not assume the simulation scaling holds outside the simulated parameter envelope."
    - "Do not equate simulation density with in-situ density measurements without conditioning on the same Ms and beta."
    - "Do not export to compressible kinetic regimes."
failure_modes:
  - "Box size truncates outer scale."
  - "Numerical compressibility issues at large Ms."
  - "Limited per-snapshot statistics."
  - "Parameter envelope coverage gaps."
depends_on:
  - cuesta-2022-compressible-turbulence-psp-themis-maven
  - paper-du-2023-density-fluctuations-3d-simulation-anisotropy
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "Conditioning PSP density-fluctuation amplitudes on (Ms, beta) should reproduce the simulation scaling."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2207.09490v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Xiangrong Fu et al. 2022 — Nature and Scalings of Density Fluctuations of Compressible ... — paper-skill

> Compiled from arXiv:2207.09490. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Compressible-MHD simulations characterise the scaling of density-fluctuation amplitude with turbulent Mach number and beta and predict an observable signature in solar-wind density spectra.
- Reproducing or extending the analysis around Compressible-MHD simulation output.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- outside-parameter-envelope extrapolation
- kinetic-regime applicability

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Compressible-MHD simulations characterise the scaling of density-fluctuation amplitude with turbulent Mach number and beta and predict an observable signature in solar-wind density spectra.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Compressible-MHD simulation across (Ms, beta) range
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Density-amplitude scaling extraction
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Predicted in-situ-observable signature
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| Compressible-MHD simulation output | derived | TODO verify dt | n/a | Authors' archive (TODO verify) | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Box size truncates outer scale.
- Numerical compressibility issues at large Ms.
- Limited per-snapshot statistics.
- Parameter envelope coverage gaps.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the simulated (Ms, beta) parameter range, the derived density-amplitude scaling and predicted observable signature.

**Out of scope — do NOT generalize beyond:**

- Do not assume the simulation scaling holds outside the simulated parameter envelope.
- Do not equate simulation density with in-situ density measurements without conditioning on the same Ms and beta.
- Do not export to compressible kinetic regimes.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2207.09490
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[cuesta-2022-compressible-turbulence-psp-themis-maven]] — sibling/upstream context for the same physics domain.
- [[paper-du-2023-density-fluctuations-3d-simulation-anisotropy]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — Conditioning PSP density-fluctuation amplitudes on (Ms, beta) should reproduce the simulation scaling.
