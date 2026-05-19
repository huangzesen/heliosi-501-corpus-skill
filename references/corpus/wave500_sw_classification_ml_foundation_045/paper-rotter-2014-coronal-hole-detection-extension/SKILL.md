---
name: paper-rotter-2014-coronal-hole-detection-extension
description: >-
  Use when applying or refining the threshold + morphological classical CH-detection baseline against modern ML methods — central paper claim is
  Threshold + morphology baselines remain competitive on stable cycles but degrade vs ACWE / CNN methods during cycle minima (TODO verify (Solar Physics or JGR Space Physics) 2014).
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
  title: "Threshold-and-morphology baseline coronal-hole detection (Rotter 2014 baseline lineage)"
  first_author: "T. Rotter"
  authors: []
  year: 2014
  venue: "TODO verify (Solar Physics or JGR Space Physics)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: solar_wind_segmentation
  secondary_themes: ["image-segmentation", "coronal-hole", "threshold-method", "classical-baseline"]
  missions: ["SOHO", "SDO"]
  regime: []  # TODO verify (sub-Alfvenic | super-Alfvenic | inner-heliosphere | 1au | corona | ...)
trigger_keywords: ["coronal-hole", "threshold", "morphology", "classical-baseline", "extension"]
data_products: []   # TODO verify — abstract tool contracts to be filled at method-ready promotion
algorithms: []      # TODO verify — abstract algorithm contracts to be filled at method-ready promotion
validation_target: null   # required at executable+ and hypothesis tiers
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Stub: Threshold + morphology baselines remain competitive on stable cycles but degrade vs ACWE / CNN methods during cycle minima. The narrow scope (mission, distance range, wind type, time-window) is TODO verify against the primary source. At stub tier this skill is referenced by slug and listed in the wave-level index; do not inherit the headline numbers as benchmarked claims.
  out_of_scope:
    - "Do NOT generalise this claim beyond the specific mission / distance / time-window the primary source documents."
    - "Do NOT bind the executable protocol to a specific runtime / MCP / plugin until method-ready promotion."
failure_modes:
  - "Bibliographic anchor not yet verified against the primary source — DOI / venue / author list flagged TODO verify."
  - "Numerical thresholds and benchmark figures are absent at stub tier; downstream consumers must NOT inherit them as claims."
depends_on: ["paper-jarolim-2023-coronal-hole-acwe-consistency"]
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Stub skill — methods, data contracts, and validation target not yet compiled from the primary source."
    related_skills: ["paper-jarolim-2023-coronal-hole-acwe-consistency"]
    proposed_action: "Promote to method-ready by populating §3/§4/§5 against the full text of the primary source."
provenance:
  generated_by: "HelioSI paper-to-skill factory (wave500 batch, 2026-05-18, Claude Code)"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_solar_wind_segmentation.json"
  verified_by: null
  verified_at: null
tags: [heliophysics, paper-skill, solar-wind-classification, stub]
---

# Threshold-and-morphology baseline coronal-hole detection (Rotter 2014 baseline l — paper-skill (stub)

> Compiled from T. Rotter (2014), "Threshold-and-morphology baseline coronal-hole detection (Rotter 2014 baseline lineage)", TODO verify (Solar Physics or JGR Space Physics), TODO verify arXiv ID.
> **Quality tier**: `stub` — promote per spec §7 (factory v0.2) before relying on procedure / validation.
>
> **Four-layer reminder (spec §4)**:
> - L1 (scientific invariant) → §1, §2, §6, §7
> - L2 (executable protocol, abstract contracts) → §3, §4, §5 — *populated at method-ready promotion*
> - L3 (adapter examples, optional) → §8 sub-block + `adapter_notes[]` — *empty at stub*
> - L4 (research-generation affordance) → §9 sub-block + `research_generation_affordances[]`

This file is the agent-native compiled form of the paper above, **not a summary**.
At stub tier only Layer 1 + Layer 4 are populated; Layer 2 and Layer 3 are intentionally
left as TODOs for promotion.

---

## 1. Trigger  *(Layer 1)*

A future agent should reach for this skill when:

- Applying or refining the threshold + morphological classical CH-detection baseline against modern ML methods.
- Deciding between this and a sibling slug listed in §9 (see `depends_on`).

Do NOT use this skill when:

- The task requires numerical reproduction of the paper's headline result — this is a stub; the underlying
  algorithms / tool contracts / validation target are TODO verify against the primary source.
- The task crosses the claim-boundary scope below (§7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Threshold + morphology baselines remain competitive on stable cycles but degrade vs ACWE / CNN methods during cycle minima. The narrow form below should be tightened once the full text is verified:

> Stub: Threshold + morphology baselines remain competitive on stable cycles but degrade vs ACWE / CNN methods during cycle minima. The narrow scope (mission, distance range, wind type, time-window) is TODO verify against the primary source. At stub tier this skill is referenced by slug and listed in the wave-level index; do not inherit the headline numbers as benchmarked claims.

**Verifiable task.** At `executable` tier, a reproduction of this skill must hit `validation_target.metric`
within `validation_target.tolerance`. Both are TODO verify — see §5.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract — STUB)*

Layer 2 is not yet populated. To promote to `method-ready`:

1. Identify the named algorithms in the primary source (§3 of the paper or the methods section).
2. For each algorithm, record an abstract procedure (runtime-neutral), equation references, and capability requirements.
3. Add entries to `algorithms[]` in the frontmatter with matching names.

Do not bind to a specific runtime / MCP / plugin in this section — keep all bindings in §8 (`adapter_notes`).

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract — STUB)*

Layer 2 is not yet populated. Each `data_products[]` entry must describe:
instrument, level, cadence, interval, archive, and the capability requirement
(e.g. "fetch and decode CDF; subset by time range").

Empty `data_products[]` is acceptable only for theory-only papers; otherwise this section
must be filled before promotion past stub.

## 5. Validation target → benchmark artifact  *(Layer 2 — STUB)*

> Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable` requires setting
> `validation_target` and running the workflow end-to-end against the abstract contract above.

## 6. Failure modes → skill memory  *(Layer 1)*

- **Stub-tier reliance risk.** Treating this skill as `method-ready` without verifying the bibliographic anchor and Layer 2 contracts will propagate hallucinated procedures downstream.
- **Adapter leakage risk at promotion.** When Layer 2 is populated, ensure no runtime / MCP / plugin name appears in §3 / §4 / §5; all such names belong in `adapter_notes[]`.
- **Slug-stability contract.** Once this slug is referenced by another paper-skill via `depends_on`, it must not be renamed without a `provenance` audit entry.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Stub: Threshold + morphology baselines remain competitive on stable cycles but degrade vs ACWE / CNN methods during cycle minima. The narrow scope (mission, distance range, wind type, time-window) is TODO verify against the primary source. At stub tier this skill is referenced by slug and listed in the wave-level index; do not inherit the headline numbers as benchmarked claims.

**Out of scope — do NOT generalise beyond:**

- The specific mission / distance / time-window the primary source documents.
- The specific data product cadences and processing levels the primary source used.
- Any runtime / MCP / plugin assumption — this skill is harness-agnostic; bindings live in `adapter_notes[]`.

If a downstream task asks for a generalisation listed above, refuse it and return a reference to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional — empty at stub)*

**Canonical links to the published artifact:**

- DOI: n/a — not yet resolved (TODO verify)
- arXiv: n/a — not yet resolved (TODO verify)
- ADS: n/a — bibcode not yet resolved.
- Code: n/a — no public repository identified at stub tier.
- Data: n/a — abstract data contracts to be filled at method-ready promotion.

**Adapter binding examples (optional, illustrative only):** none recorded at stub tier;
`adapter_notes[]` is intentionally empty.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the following sibling skills (slugs):

- `[[paper-jarolim-2023-coronal-hole-acwe-consistency]]` — sibling slug; relation TODO verify in full text.

**Research-generation affordances.** Forward-pointing surface of the skill (spec §4 Layer 4):

- **Gap** — Stub skill; the executable protocol (Layer 2) is not yet compiled. Related: `[[paper-jarolim-2023-coronal-hole-acwe-consistency]]`. Proposed: promote to method-ready by populating §3/§4/§5 from the primary source.
- **Minimal experiment** — Once Layer 2 is populated, the minimal experiment is to reproduce the headline figure / table cited in `validation_target.reference_figure` and confirm the metric falls within tolerance.

## Notes

Stub anchor for the classical CH-detection baseline tradition; primary author and venue TODO verify.
