---
name: paper-opie-2024-temperature-anisotropy-velocity-shears
description: >-
  Use when working with the central claim of Simon Opie et al. 2024 — Intermittent velocity
  shears in the solar wind drive temperature-anisotropy instability crossings statistically
  more often than ambient turbulence, observable in conditioned T_perp/T_par vs beta_par
  diagrams. (arXiv:2409.18849; venue TODO verify).
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
  title: "Temperature anisotropy instabilities driven by intermittent velocity shears in the solar wind"
  first_author: "Simon Opie"
  authors:
    - "Simon Opie"
  year: 2024
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2409.18849"
  ads_bibcode: null
domain:
  primary_theme: waves_instabilities
  secondary_themes: [temperature-anisotropy, velocity-shear, intermittency]
  missions: [other]
  regime: [1au, ion-scale]
trigger_keywords:
  - "temperature anisotropy instability"
  - "intermittent velocity shear"
  - "T_perp T_par diagram"
  - "Opie 2024 instability"
  - "conditioned beta-anisotropy"
data_products:
  - {instrument: "In-situ plasma moments + MAG (mission TODO verify)", level: "L2/L3", cadence: "TODO verify", interval: "TODO verify", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "PVI-based velocity-shear event identification"
    equation_refs: ["TODO verify"]
  - name: "Conditioned T_perp/T_par vs beta_par diagram"
    equation_refs: ["TODO verify"]
  - name: "Instability-threshold crossing-rate statistics"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2409.18849"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    In the analysed sample, intermittent-shear-conditioned subsamples cross temperature-
    anisotropy instability thresholds more often than ambient.
  out_of_scope:
    - "Do not equate threshold crossing with active wave growth without wave-detection cross-check."
    - "Do not generalise the shear definition outside the PVI threshold tested."
    - "Do not assume the same statistics at near-Sun PSP."
failure_modes:
  - "PVI threshold for shear identification is choice-dependent."
  - "Plasma-moment uncertainty inflates anisotropy estimate."
  - "Stream-mixed intervals confound shear vs Alfvenicity attribution."
  - "Instability-threshold model dependence (linear-Vlasov)."
depends_on:
  - paper-soljento-2023-imbalanced-turbulence-velocity-shears
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If shear drives instability crossings, near-Sun PSP shear-conditioned subsamples should show the same enhancement."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2409.18849v1)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, waves_instabilities]
---

# Simon Opie et al. 2024 — Temperature anisotropy instabilities driven by intermittent ... — paper-skill

> Compiled from arXiv:2409.18849. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- Intermittent velocity shears in the solar wind drive temperature-anisotropy instability crossings statistically more often than ambient turbulence, observable in conditioned T_perp/T_par vs beta_par diagrams.
- Reproducing or extending the analysis around In-situ plasma moments + MAG (mission TODO verify).
- Deciding whether waves_instabilities-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- near-Sun extrapolation without re-run
- active-wave-growth claim without wave detection

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Intermittent velocity shears in the solar wind drive temperature-anisotropy instability crossings statistically more often than ambient turbulence, observable in conditioned T_perp/T_par vs beta_par diagrams.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### PVI-based velocity-shear event identification
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Conditioned T_perp/T_par vs beta_par diagram
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Instability-threshold crossing-rate statistics
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive | Capability |
|---|---|---|---|---|---|
| In-situ plasma moments + MAG (mission TODO verify) | L2/L3 | TODO verify | TODO verify | CDAWeb / SPDF | fetch+decode CDF; subset by time |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- PVI threshold for shear identification is choice-dependent.
- Plasma-moment uncertainty inflates anisotropy estimate.
- Stream-mixed intervals confound shear vs Alfvenicity attribution.
- Instability-threshold model dependence (linear-Vlasov).

## 7. Claim boundary  *(Layer 1)*

**In scope.** In the analysed sample, intermittent-shear-conditioned subsamples cross temperature-anisotropy instability thresholds more often than ambient.

**Out of scope — do NOT generalize beyond:**

- Do not equate threshold crossing with active wave growth without wave-detection cross-check.
- Do not generalise the shear definition outside the PVI threshold tested.
- Do not assume the same statistics at near-Sun PSP.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2409.18849
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[paper-soljento-2023-imbalanced-turbulence-velocity-shears]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If shear drives instability crossings, near-Sun PSP shear-conditioned subsamples should show the same enhancement.
