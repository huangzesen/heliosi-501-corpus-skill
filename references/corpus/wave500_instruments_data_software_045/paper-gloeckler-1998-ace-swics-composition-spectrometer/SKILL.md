---
name: paper-gloeckler-1998-ace-swics-composition-spectrometer
description: >-
  Use when retrieving solar-wind heavy-ion charge-state and composition data
  (He, C, N, O, Ne, Mg, Si, Fe) at L1 from ACE/SWICS — central claim is that
  SWICS measures mass per charge and energy per charge using ESA + ToF + SSD to
  deliver hourly ionic charge states (e.g., O7+/O6+, Fe charge mean) (Gloeckler
  et al. 1998, Space Sci. Rev.).
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
  title: Investigation of the composition of solar and interstellar matter using SWICS and SWIMS on ACE
  first_author: "Gloeckler, G."
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
  - ACE SWICS
  - Gloeckler 1998
  - heavy-ion composition
  - O7+/O6+
  - Fe charge state
  - ICME composition signature
  - solar wind composition
data_products:
  - instrument: ACE/SWICS
    level: L2
    cadence: 1 hour (charge-state); 2 hour averages
    interval: null
    archive: SPDF / ACE Science Center
algorithms:
  - name: ToF + post-acceleration ion identification
    equation_refs:
      - §3 Gloeckler 1998
    external_implementations: []
  - name: O7+/O6+ ratio for slow/fast wind classification
    equation_refs: []
    external_implementations: []
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/pub/data/ace/swics/"
claim_boundary:
  scope: >-
    ACE/SWICS: electrostatic deflection + post-acceleration + ToF + solid-state
    detection. Heavy-ion charge-state and composition at ~hour cadence; ionic
    ratios O7+/O6+, C6+/C5+, and mean Fe charge are standard CME / solar-wind-
    source diagnostics.
  out_of_scope:
    - Do not use for proton or alpha bulk moments — use SWEPAM-I for that.
    - Do not assume sub-hour cadence is reliable for low-abundance heavies.
    - SWICS suffered an SSD anomaly in 2011; data after that has reduced PHA capability — cross-check version notes.
failure_modes:
  - "Post-2011 SSD anomaly: use 'ACE SWICS 1.1' or later reprocessed data sets only."
  - Iron charge state requires careful resolution-matrix inversion; do not use raw count maps.
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
# Investigation of the composition of solar and interstellar matter using SWICS and SWIMS on ACE — paper-skill

> Compiled as a v0.2 harness-agnostic paper-skill on 2026-05-18.
> **Quality tier**: `stub` — `source_type: paper`.
> Layer hygiene: §3/§4/§5 prose is runtime-neutral; adapter examples (if any) live in §8 / `adapter_notes[]`.

---

## 1. Trigger  *(Layer 1)*

Reach for this skill when:

- Use when retrieving solar-wind heavy-ion charge-state and composition data (He, C, N, O, Ne, Mg, Si, Fe) at L1 from ACE/SWICS — central claim is that SWICS measures mass per charge and energy per charge using ESA + ToF + SSD to deliver hourly ionic charge states (e.g., O7+/O6+, Fe charge mean) (Gloeckler et al. 1998, Space Sci. Rev.).

Do NOT use this skill when:

- Do not use for proton or alpha bulk moments — use SWEPAM-I for that.
- Do not assume sub-hour cadence is reliable for low-abundance heavies.

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** ACE/SWICS: electrostatic deflection + post-acceleration + ToF + solid-state detection. Heavy-ion charge-state and composition at ~hour cadence; ionic ratios O7+/O6+, C6+/C5+, and mean Fe charge are standard CME / solar-wind-source diagnostics.

**Verifiable task.** A reproduction succeeds when an agent loads the contracted data products listed in §4, applies the algorithm(s) named in §3 within the stated `claim_boundary`, and reports quality flags + version metadata. At `stub` tier this section names the contract; `executable+` duplicates a numerical target into `validation_target`.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

### ToF + post-acceleration ion identification

- Paper reference: §3 Gloeckler 1998
- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

### O7+/O6+ ratio for slow/fast wind classification

- Capability requirement: an agent runtime must be able to read the contracted data product(s) listed in §4 and apply this algorithm to them within the stated `claim_boundary`. No specific runtime, MCP, or harness command is asserted here.

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

| Instrument | Level | Cadence | Interval | Archive |
|---|---|---|---|---|
| ACE/SWICS | L2 | 1 hour (charge-state); 2 hour averages | — | SPDF / ACE Science Center |

Each row is a *capability requirement*: a runtime adapter must be able to discover, fetch, decode, and time-subset the named product. The contract is not bound to any specific MCP, plugin, or shell command.

## 5. Validation target → benchmark artifact  *(Layer 2)*

> Not benchmarked yet — `stub`. Promotion to `executable` requires (a) a smoke-test that exercises the §4 contract end-to-end and (b) setting `validation_target` to a numerical / observational target with tolerance.

## 6. Failure modes → skill memory  *(Layer 1)*

- Post-2011 SSD anomaly: use 'ACE SWICS 1.1' or later reprocessed data sets only.
- Iron charge state requires careful resolution-matrix inversion; do not use raw count maps.

## 7. Claim boundary  *(Layer 1)*

**In scope.** ACE/SWICS: electrostatic deflection + post-acceleration + ToF + solid-state detection. Heavy-ion charge-state and composition at ~hour cadence; ionic ratios O7+/O6+, C6+/C5+, and mean Fe charge are standard CME / solar-wind-source diagnostics.

**Out of scope — do NOT generalize beyond:**

- Do not use for proton or alpha bulk moments — use SWEPAM-I for that.
- Do not assume sub-hour cadence is reliable for low-abundance heavies.
- SWICS suffered an SSD anomaly in 2011; data after that has reduced PHA capability — cross-check version notes.

## 8. Links and adapter binding examples  *(Layer 3, optional)*

**Canonical links:**

- DOI: n/a
- arXiv: n/a
- Code: n/a
- Data / archive: https://cdaweb.gsfc.nasa.gov/pub/data/ace/swics/

No adapter binding examples recorded; the §4 contract is sufficient for any harness with read + numerical-Python capabilities.

## 9. Skill graph + research-generation affordances  *(Layer 4)*

**Skill graph (depends_on edges).**

No paper-skill dependencies (self-contained).

**Research-generation affordances.**

No research-generation affordances identified yet.

## Weak entries / citation TODOs

- DOI not in local inventory; Space Sci. Rev. 86, 497 (1998)
