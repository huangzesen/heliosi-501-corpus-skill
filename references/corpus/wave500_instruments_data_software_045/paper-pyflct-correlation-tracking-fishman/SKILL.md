---
name: paper-pyflct-correlation-tracking-fishman
description: >-
  Use when estimating horizontal velocity fields from a sequence of solar
  magnetograms or intensity images (flux transport, helicity flux, ARDoS) —
  central claim is that the Fourier Local Correlation Tracking (FLCT, Fisher &
  Welsch 2008) algorithm, packaged as pyflct, computes (vx, vy) from two image
  frames via windowed FFT cross-correlation.
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
  title: pyflct / FLCT — Fourier Local Correlation Tracking for solar magnetograms
  first_author: "Fisher, G. H."
  year: 2008
  venue: "(Fisher & Welsch 2008, ASP Conf. Ser. — FLCT method)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - SDO
  regime:
    - corona
trigger_keywords:
  - FLCT
  - pyflct
  - Fisher Welsch 2008
  - local correlation tracking
  - magnetogram velocity
  - flux transport
  - ARD horizontal flow
data_products: []
algorithms:
  - name: FLCT windowed FFT cross-correlation velocity field
    equation_refs:
      - "Fisher & Welsch 2008 §2"
    external_implementations:
      - "https://github.com/PyDL/pyflct"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://cgem.ssl.berkeley.edu/cgi-bin/cgem/FLCT/home"
  data_repo: null
claim_boundary:
  scope: >-
    FLCT / pyflct: takes two images + a Gaussian window σ; outputs (vx, vy) per
    pixel. Standard for HMI magnetograms in flux-transport and helicity-flux
    studies.
  out_of_scope:
    - Do not treat FLCT velocities as 3D — it is LOS-orthogonal apparent motion only.
    - Do not use FLCT on saturated active regions without masking.
    - Do not chain multiple frame pairs without consistent σ.
failure_modes:
  - Gaussian window σ trades smoothing for spatial resolution; verify against synthetic test.
  - FLCT fails near data masks; pad or mask explicitly.
  - Outflows near polarity inversion lines are biased by intensity gradients.
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
tags: [heliophysics, paper-skill, software-package]
source_type: software-package
---
# pyflct / FLCT — Fourier Local Correlation Tracking for solar magnetograms — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: software-package`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when estimating horizontal velocity fields from a sequence of solar magnetograms or intensity images (flux transport, helicity flux, ARDoS) — central claim is that the Fourier Local Correlation Tracking (FLCT, Fisher & Welsch 2008) algorithm, packaged as pyflct, computes (vx, vy) from two image frames via windowed FFT cross-correlation.

Do NOT use this skill when:

- Do not treat FLCT velocities as 3D — it is LOS-orthogonal apparent motion only.
- Do not use FLCT on saturated active regions without masking.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** FLCT / pyflct: takes two images + a Gaussian window σ; outputs (vx, vy) per pixel. Standard for HMI magnetograms in flux-transport and helicity-flux studies.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### FLCT windowed FFT cross-correlation velocity field

- Paper reference: Fisher & Welsch 2008 §2
- External implementation(s): https://github.com/PyDL/pyflct
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

No in-situ / remote-sensing data dependencies (this skill is purely software / infrastructure or coordinate-only).

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Gaussian window σ trades smoothing for spatial resolution; verify against synthetic test.
- FLCT fails near data masks; pad or mask explicitly.
- Outflows near polarity inversion lines are biased by intensity gradients.

## 7. Claim boundary  *(Layer 1)*

**In scope.** FLCT / pyflct: takes two images + a Gaussian window σ; outputs (vx, vy) per pixel. Standard for HMI magnetograms in flux-transport and helicity-flux studies.

**Out of scope — do NOT generalize beyond:**

- Do not treat FLCT velocities as 3D — it is LOS-orthogonal apparent motion only.
- Do not use FLCT on saturated active regions without masking.
- Do not chain multiple frame pairs without consistent σ.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: https://cgem.ssl.berkeley.edu/cgi-bin/cgem/FLCT/home
- Data / archive: n/a

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- Original Fisher & Welsch 2008 in ASP Conf. Ser. 383 — verify exact citation
