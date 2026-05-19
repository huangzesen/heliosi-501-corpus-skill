---
name: paper-good-2026-correlation-length-magnetic-clouds
description: >-
  Use when working with the central claim of S. W. Good et al. 2026 — Force-free flux-rope
  detrending of PSP MAG time series inside two magnetic clouds yields correlation lengths of
  2.7e4 d_p (0.77 au) and 1.6e4 d_p (0.39 au), significantly smaller than non-detrended
  estimates; inertial-range scaling remains ~k^(-5/3). (arXiv:2602.05450; venue TODO
  verify).
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
  title: "The Correlation Length of Turbulence in Magnetic Clouds"
  first_author: "S. W. Good"
  authors:
    - "S. W. Good"
    - "J. Lalueza Puértolas"
    - "A. -S. M. Jylhä"
    - "E. K. J. Kilpua"
  year: 2026
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2602.05450"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [correlation-length, magnetic-clouds, detrending]
  missions: [PSP]
  regime: [inner-heliosphere, 1au, MHD-scale]
trigger_keywords:
  - "correlation length magnetic cloud"
  - "flux-rope detrending"
  - "ICME turbulence"
  - "outer-scale d_p normalisation"
  - "Good Lalueza Puertolas Jylha Kilpua 2026"
  - "force-free fit"
data_products:
  - {instrument: "PSP/FIELDS MAG", level: "L2", cadence: "~1 vec/s", interval: "Two magnetic-cloud crossings at 0.77 au and 0.39 au", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Force-free flux-rope fit and detrending"
    equation_refs: ["TODO verify Eq."]
  - name: "Auto-correlation function and λ_C on detrended series"
    equation_refs: ["TODO verify"]
  - name: "Inertial-range PSD on detrended series"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.05450"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Detrended correlation length values 2.7e4 d_p (0.77 au) and 1.6e4 d_p (0.39 au), with
    k^(-3) flux-rope contribution and k^(-5/3) inertial-range scaling, for the two PSP
    magnetic-cloud crossings studied.
  out_of_scope:
    - "Do not apply the specific λ_C/d_i numbers to other magnetic clouds without independently detrending."
    - "Do not assume the flux-rope contribution is k^(-3) universally."
    - "Do not extrapolate to non-magnetic-cloud ICME structures."
failure_modes:
  - "Force-free fit quality determines residual-flux-rope leakage."
  - "λ_C estimator (e-folding vs integral) shifts numbers."
  - "d_p normalisation requires accurate density."
  - "Sample of two clouds is small."
depends_on: []
adapter_notes: []
research_generation_affordances:
  - type: minimal_experiment
    statement: "Run the same detrending pipeline on a larger PSP magnetic-cloud catalogue and report λ_C/d_p distribution."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2602.05450v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# S. W. Good et al. 2026 — The Correlation Length of Turbulence in Magnetic Clouds — paper-skill

> Compiled from arXiv:2602.05450. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Force-free flux-rope detrending of PSP MAG time series inside two magnetic clouds yields correlation lengths of 2.7e4 d_p (0.77 au) and 1.6e4 d_p (0.39 au), significantly smaller than non-detrended estimates; inertial-range scaling remains ~k^(-5/3).
- Reproducing or extending the analysis around PSP/FIELDS MAG.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- non-magnetic-cloud ICME structures
- cross-cloud λ_C extrapolation without detrend

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Force-free flux-rope detrending of PSP MAG time series inside two magnetic clouds yields correlation lengths of 2.7e4 d_p (0.77 au) and 1.6e4 d_p (0.39 au), significantly smaller than non-detrended estimates; inertial-range scaling remains ~k^(-5/3).

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### Force-free flux-rope fit and detrending
- Paper reference: TODO verify Eq..
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Auto-correlation function and λ_C on detrended series
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Inertial-range PSD on detrended series
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| PSP/FIELDS MAG | L2 | ~1 vec/s | Two magnetic-cloud crossings at 0.77 au and 0.39 au | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Force-free fit quality determines residual-flux-rope leakage.
- λ_C estimator (e-folding vs integral) shifts numbers.
- d_p normalisation requires accurate density.
- Sample of two clouds is small.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Detrended correlation length values 2.7e4 d_p (0.77 au) and 1.6e4 d_p (0.39 au), with k^(-3) flux-rope contribution and k^(-5/3) inertial-range scaling, for the two PSP magnetic-cloud crossings studied.

**Out of scope — do NOT generalize beyond:**

- Do not apply the specific λ_C/d_i numbers to other magnetic clouds without independently detrending.
- Do not assume the flux-rope contribution is k^(-3) universally.
- Do not extrapolate to non-magnetic-cloud ICME structures.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2602.05450
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

No paper-skill dependencies (self-contained).

**Affordances.**

- **Minimal_experiment** — Run the same detrending pipeline on a larger PSP magnetic-cloud catalogue and report λ_C/d_p distribution.
