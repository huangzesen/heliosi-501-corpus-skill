---
name: paper-mccomas-1998-ace-swepam-solar-wind-electron-proton-alpha
description: >-
  Use when retrieving L1 thermal solar-wind ion and electron bulk moments + 3D
  distributions from ACE/SWEPAM (Aug 1997–present) — central claim is that the
  SWEPAM ion (SWEPAM-I) and electron (SWEPAM-E) electrostatic analyzers deliver
  64 s ion moments and 2D electron distributions sufficient for routine solar-
  wind monitoring and CME identification (McComas et al. 1998).
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
  title: Solar Wind Electron Proton Alpha Monitor (SWEPAM) for the Advanced Composition Explorer
  first_author: "McComas, D. J."
  year: 1998
  venue: Space Science Reviews
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: []
  missions:
    - ACE
  regime:
    - 1au
trigger_keywords:
  - ACE SWEPAM
  - McComas 1998
  - ACE solar wind monitor
  - L1 plasma monitor
  - SWEPAM ion moments
  - SWEPAM electron
data_products:
  - instrument: ACE/SWEPAM-I
    level: L2
    cadence: 64 s (moments)
    interval: null
    archive: SPDF / ACE Science Center
  - instrument: ACE/SWEPAM-E
    level: L2
    cadence: 64 s (moments)
    interval: null
    archive: SPDF
algorithms:
  - name: SWEPAM nonlinear ion-moment fit
    equation_refs:
      - §4 McComas 1998
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/pub/data/ace/swepam/"
claim_boundary:
  scope: >-
    ACE/SWEPAM-I (top-hat ESA, ions ~0.26-36 keV/q) and SWEPAM-E (electrons
    ~1-1350 eV) at L1; standard 64 s moments; 'h0' (1 min) and 'h2' (12 s) high-
    res ion files exist.
  out_of_scope:
    - Do not use SWEPAM-I for composition — it is mass-blind. Pair with SWICS for composition.
    - "Do not assume continuous operation — SWEPAM-I cathode aged out around 2011, switched to redundant cathode; data quality varies."
failure_modes:
  - "Post-2011 cathode degradation: cross-check with OMNI or Wind/SWE for science-grade epochs."
  - Alpha contamination at low energies during slow wind.
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
# Solar Wind Electron Proton Alpha Monitor (SWEPAM) for the Advanced Composition Explorer — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving L1 thermal solar-wind ion and electron bulk moments + 3D distributions from ACE/SWEPAM (Aug 1997–present) — central claim is that the SWEPAM ion (SWEPAM-I) and electron (SWEPAM-E) electrostatic analyzers deliver 64 s ion moments and 2D electron distributions sufficient for routine solar-wind monitoring and CME identification (McComas et al. 1998).

Do NOT use this skill when:

- Do not use SWEPAM-I for composition — it is mass-blind. Pair with SWICS for composition.
- Do not assume continuous operation — SWEPAM-I cathode aged out around 2011, switched to redundant cathode; data quality varies.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** ACE/SWEPAM-I (top-hat ESA, ions ~0.26-36 keV/q) and SWEPAM-E (electrons ~1-1350 eV) at L1; standard 64 s moments; 'h0' (1 min) and 'h2' (12 s) high-res ion files exist.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### SWEPAM nonlinear ion-moment fit

- Paper reference: §4 McComas 1998
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| ACE/SWEPAM-I | L2 | 64 s (moments) | — | SPDF / ACE Science Center |
| ACE/SWEPAM-E | L2 | 64 s (moments) | — | SPDF |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Post-2011 cathode degradation: cross-check with OMNI or Wind/SWE for science-grade epochs.
- Alpha contamination at low energies during slow wind.

## 7. Claim boundary  *(Layer 1)*

**In scope.** ACE/SWEPAM-I (top-hat ESA, ions ~0.26-36 keV/q) and SWEPAM-E (electrons ~1-1350 eV) at L1; standard 64 s moments; 'h0' (1 min) and 'h2' (12 s) high-res ion files exist.

**Out of scope — do NOT generalize beyond:**

- Do not use SWEPAM-I for composition — it is mass-blind. Pair with SWICS for composition.
- Do not assume continuous operation — SWEPAM-I cathode aged out around 2011, switched to redundant cathode; data quality varies.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://cdaweb.gsfc.nasa.gov/pub/data/ace/swepam/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Space Sci. Rev. 86, 563 (1998)
