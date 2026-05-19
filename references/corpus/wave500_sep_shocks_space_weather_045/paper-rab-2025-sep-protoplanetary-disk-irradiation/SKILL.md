---
name: paper-rab-2025-sep-protoplanetary-disk-irradiation
description: >-
  Use when protoplanetary disk or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: Modeling of SEP irradiation in the young Sun's protoplanetary disk constrains the radial extent over which energetic particles can drive isotopic anomalies (e.g. 10Be) under plausible early-Sun activity scaling. (arXiv:2512.03184, 2025).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true

layers:
  scientific_invariant: true
  executable_protocol: true
  adapter_binding_examples: false
  research_generation_affordance: true

paper:
  title: "The Extent of Solar Energetic Particle Irradiation in the Sun's Protoplanetary Disk"
  first_author: "TODO verify"
  authors:
    - "TODO verify"
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2512.03184"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [Modeling-only (TODO_verify)]
  regime: [inner-heliosphere]

trigger_keywords:
  - "protoplanetary disk"
  - "young Sun SEP"
  - "T Tauri"
  - "SEP irradiation extent"
  - "isotopic anomalies"
  - "Be-10 / 26Al chondritic constraint"

data_products: []  # theory / modeling-only

algorithms:
  - name: "Young-Sun SEP flux scaling (T Tauri activity proxies)"
    equation_refs: []
    external_implementations: []
  - name: "Disk gas/dust model + ionization / SEP propagation"
    equation_refs: []
    external_implementations: []
  - name: "Isotope-yield bookkeeping (10Be, 26Al — TODO_verify)"
    equation_refs: []
    external_implementations: []
  - name: "Radial / vertical penetration map"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2512.03184"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Modeling study (TODO_verify code); young-Sun activity scaling; radial / vertical SEP penetration in a disk-model; isotopic-yield bounds only.
  out_of_scope:
    - "Do not generalize to non-solar / extreme-young-star regimes."
    - "Do not use as a stand-alone explanation for short-lived radionuclides without combined GCR/stellar-flare model."

failure_modes:
  - "Young-Sun activity proxies are uncertain by 1–2 orders of magnitude"
  - "Disk magnetic structure (shielding / focusing) not fully specified"
  - "Comparison against chondritic isotope data is indirect"

depends_on:
  - "paper-koppl-2026-electron-acr-cold-clouds-radiation"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No combined SEP + protostellar flare + GCR model with a single isotope-yield budget."
    related_skills: []
  - type: "hypothesis"
    statement: "If young-Sun SEP fluxes were 10^4–10^6× modern, the irradiation radius extends beyond a few au."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Run the model with high-activity scaling and compute the 10Be radial yield; compare with chondritic anomalies."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2512.03184"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# The Extent of Solar Energetic Particle Irradiation in the Sun's Protoplanetary Disk — paper-skill

> Compiled from arXiv:2512.03184 (2025), TODO verify et al.
> **Quality tier**: `stub`. All numeric specifics not present in the
> arXiv-inventory abstract are marked `TODO_verify_with_full_text`.

---

## Layer map (harness-agnostic)

This SKILL.md is structured to be loadable by *any* general-purpose agent
runtime (Claude Code, LingTai, Codex, Cursor, OpenAI Assistants, …).
Named runtimes / MCPs / repos appear only as *adapter examples*; the
contract itself is runtime-neutral. Sections map onto four layers:

1. **Scientific invariant layer** — §1 trigger, §2 narrow claim, §6
   failure modes, §7 claim boundary. Mission- / instrument- / physics-
   level statements; runtime-neutral.
2. **Executable protocol layer (abstract capability contracts)** — §3
   procedures and §4 tool contracts describe what *capabilities* are
   needed (e.g., "load IS☉IS energetic-particle spectra", "compute
   power-law fit") without binding to any particular API, MCP, or
   harness tool. Any runtime that fulfils the named capability satisfies
   the contract.
3. **Adapter / runtime notes (optional examples)** — wherever a named
   tool, MCP, repo, or library would appear, it is exactly one *example
   adapter* satisfying the abstract contract above; substitutable.
4. **Research-generation affordances** — §9 lists gaps, tensions, new
   hypotheses, and follow-up experiments enabled when this skill is
   composed with prior skills in the corpus.

A consuming agent MUST honour Layers 1 and 2; Layer 3 mentions (if any)
are substitutable; Layer 4 entries are seeds for new work, not claims.

---

## 1. Trigger  *(Layer 1)*

A future agent should reach for this skill when:

- protoplanetary disk
- young Sun SEP
- T Tauri

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Modeling of SEP irradiation in the young Sun's protoplanetary disk constrains the radial extent over which energetic particles can drive isotopic anomalies (e.g. 10Be) under plausible early-Sun activity scaling.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Predicted 10Be radial-distribution profile; consistency with chondritic constraint (TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Young-Sun SEP flux scaling (T Tauri activity proxies)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Young-Sun SEP flux scaling (T Tauri activity proxies) as a callable on the data products in §4.

### Disk gas/dust model + ionization / SEP propagation

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Disk gas/dust model + ionization / SEP propagation as a callable on the data products in §4.

### Isotope-yield bookkeeping (10Be, 26Al — TODO_verify)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Isotope-yield bookkeeping (10Be, 26Al — TODO_verify) as a callable on the data products in §4.

### Radial / vertical penetration map

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Radial / vertical penetration map as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

No in-situ / remote data dependencies.

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Predicted 10Be radial-distribution profile; consistency with chondritic constraint (TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Young-Sun activity proxies are uncertain by 1–2 orders of magnitude
- Disk magnetic structure (shielding / focusing) not fully specified
- Comparison against chondritic isotope data is indirect

## 7. Claim boundary  *(Layer 1)*

**In scope.** Modeling study (TODO_verify code); young-Sun activity scaling; radial / vertical SEP penetration in a disk-model; isotopic-yield bounds only.

**Out of scope — do NOT generalize beyond:**

- Do not generalize to non-solar / extreme-young-star regimes.
- Do not use as a stand-alone explanation for short-lived radionuclides without combined GCR/stellar-flare model.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2512.03184
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-koppl-2026-electron-acr-cold-clouds-radiation]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No combined SEP + protostellar flare + GCR model with a single isotope-yield budget.
- **Hypothesis** — If young-Sun SEP fluxes were 10^4–10^6× modern, the irradiation radius extends beyond a few au.
- **Minimal_experiment** — Run the model with high-activity scaling and compute the 10Be radial yield; compare with chondritic anomalies.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
