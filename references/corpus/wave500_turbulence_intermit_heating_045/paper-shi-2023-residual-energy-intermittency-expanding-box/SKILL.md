---
name: paper-shi-2023-residual-energy-intermittency-expanding-box
description: >-
  Use when working with the central claim of Chen Shi et al. 2023 — 3D MHD expanding-box
  simulations of decaying Alfvenic turbulence generate negative residual energy at all
  sigma_c with E_r proportional to k_perp^(-2) and a typical S_2(b) proportional to
  l_perp^(1/2) scaling; intermittency growth is enhanced by expansion. (arXiv:2308.12376;
  venue TODO verify).
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
  title: "Evolution of MHD turbulence in the expanding solar wind: residual energy and intermittency"
  first_author: "Chen Shi"
  authors:
    - "Chen Shi"
    - "Nikos Sioulas"
    - "Zesen Huang"
    - "Marco Velli"
    - "Anna Tenerani"
    - "Victor Réville"
  year: 2023
  venue: "arXiv preprint (journal TODO verify)"
  doi: null
  arxiv_id: "2308.12376"
  ads_bibcode: null
domain:
  primary_theme: turbulence
  secondary_themes: [expanding-box, residual-energy, intermittency, simulation]
  missions: [n/a]
  regime: [MHD-scale, fluid]
trigger_keywords:
  - "expanding box model"
  - "negative residual energy"
  - "E_r ~ k_perp^-2"
  - "intermittency growth"
  - "S_2(b) ~ l_perp^1/2"
  - "Shi Sioulas Huang Velli Tenerani Reville 2023"
  - "decaying MHD turbulence"
data_products: []
algorithms:
  - name: "3D MHD expanding-box simulation"
    equation_refs: ["TODO verify"]
  - name: "Second-order structure functions S_2(b), S_2(u)"
    equation_refs: ["TODO verify"]
  - name: "Residual-energy spectrum E_r(k_perp)"
    equation_refs: ["TODO verify"]
  - name: "Higher-order intermittency statistics"
    equation_refs: ["TODO verify"]
validation_target: null
links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2308.12376"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Within the simulated parameter range (initial sigma_c, expansion rate, compressibility)
    the expanding-box MHD decay produces negative residual energy at k_perp^(-2) and S_2(b) at
    l_perp^(1/2).
  out_of_scope:
    - "Do not export the residual-energy slope to non-expanding decaying turbulence without re-fit."
    - "Do not assert causal residual-energy-to-intermittency link from the simulations; the paper notes the link is weak."
    - "Do not extrapolate to kinetic scales unresolved in the simulation."
failure_modes:
  - "Expanding-box boundary conditions affect outer-scale energy."
  - "Finite resolution at small k_perp distorts S_2(u)."
  - "Initial isotropic spectrum is idealised."
  - "Per-run statistical variance with limited realisations."
depends_on:
  - sioulas-2024-higher-order-3d-anisotropy
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If the simulated E_r proportional to k_perp^(-2) law is universal, PSP-measured E_r at high σ_c should follow it within tolerance."
  - type: minimal_experiment
    statement: "Fit E_r vs k_perp on PSP perpendicular-anisotropy bins and compare to k^(-2)."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2308.12376v2)"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, turbulence]
---

# Chen Shi et al. 2023 — Evolution of MHD turbulence in the expanding solar wind: res... — paper-skill

> Compiled from arXiv:2308.12376. Quality tier `stub` — many numerical values are TODO verify against the full text.

## 1. Trigger  *(Layer 1)*

Use when:

- 3D MHD expanding-box simulations of decaying Alfvenic turbulence generate negative residual energy at all sigma_c with E_r proportional to k_perp^(-2) and a typical S_2(b) proportional to l_perp^(1/2) scaling; intermittency growth is enhanced by expansion.
- Deciding whether turbulence-related observations fit the paper's analytic/observational rule.

Do NOT use when:

- non-expanding scenario
- kinetic-scale extrapolation

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** 3D MHD expanding-box simulations of decaying Alfvenic turbulence generate negative residual energy at all sigma_c with E_r proportional to k_perp^(-2) and a typical S_2(b) proportional to l_perp^(1/2) scaling; intermittency growth is enhanced by expansion.

**Verifiable task.** A reproduction succeeds when an agent recovers the qualitative result reported by the paper under the same conditioning rule; exact numerical tolerances are TODO verify against the published figures/tables.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### 3D MHD expanding-box simulation
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Second-order structure functions S_2(b), S_2(u)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Residual-energy spectrum E_r(k_perp)
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

### Higher-order intermittency statistics
- Paper reference: TODO verify.
- Abstract procedure: see paper for exact derivation; the runtime must supply the capability listed in §4.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote data dependencies (theory-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires extracting numerical targets from the paper's figures and populating `validation_target`.

## 6. Failure modes → skill memory  *(Layer 1)*

- Expanding-box boundary conditions affect outer-scale energy.
- Finite resolution at small k_perp distorts S_2(u).
- Initial isotropic spectrum is idealised.
- Per-run statistical variance with limited realisations.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Within the simulated parameter range (initial sigma_c, expansion rate, compressibility) the expanding-box MHD decay produces negative residual energy at k_perp^(-2) and S_2(b) at l_perp^(1/2).

**Out of scope — do NOT generalize beyond:**

- Do not export the residual-energy slope to non-expanding decaying turbulence without re-fit.
- Do not assert causal residual-energy-to-intermittency link from the simulations; the paper notes the link is weak.
- Do not extrapolate to kinetic scales unresolved in the simulation.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO verify
- arXiv: https://arxiv.org/abs/2308.12376
- ADS: TODO verify
- Code: n/a (no public repo on file)
- Data: n/a

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges):**
- [[sioulas-2024-higher-order-3d-anisotropy]] — sibling/upstream context for the same physics domain.

**Affordances.**

- **Hypothesis** — If the simulated E_r proportional to k_perp^(-2) law is universal, PSP-measured E_r at high σ_c should follow it within tolerance.
- **Minimal_experiment** — Fit E_r vs k_perp on PSP perpendicular-anisotropy bins and compare to k^(-2).
