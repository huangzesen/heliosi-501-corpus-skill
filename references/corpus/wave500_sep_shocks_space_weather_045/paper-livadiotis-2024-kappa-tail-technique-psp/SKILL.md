---
name: paper-livadiotis-2024-kappa-tail-technique-psp
description: >-
  Use when kappa-tail technique or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: The kappa-tail technique provides a closed-form fit to the high-energy tail of a kappa distribution and is applied to PSP/IS☉IS energetic-particle spectra to extract κ, T_EP, n_EP. (arXiv:2407.04188, 2024).
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
  title: "Kappa-tail technique: Modeling and application to Solar Energetic Particles observed by Parker Solar Probe"
  first_author: "Livadiotis, G."
  authors:
    - "Livadiotis, G."
    - "Cuesta, M. E."
    - "Cummings, A. T."
    - "McComas, D. J."
  year: 2024
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2407.04188"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "kappa-tail technique"
  - "Livadiotis kappa formalism"
  - "high-energy SEP tail fit"
  - "PSP/IS☉IS EPI-Hi"
  - "non-Maxwellian distribution"

data_products:
  - instrument: "PSP/IS☉IS EPI-Hi"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "Application events (TODO_verify)"
    archive: "PSP SOC"

algorithms:
  - name: "Kappa-tail closed-form derivation"
    equation_refs: []
    external_implementations: []
  - name: "Spectral fit (κ, T_EP, n_EP)"
    equation_refs: []
    external_implementations: []
  - name: "Residual / goodness-of-fit diagnostics"
    equation_refs: []
    external_implementations: []
  - name: "Comparison against full kappa fit"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2407.04188"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Methodology paper + PSP application; closed-form kappa-tail formula; spectral fit and parameter extraction.
  out_of_scope:
    - "Do not use the closed form outside its derivation range."
    - "Do not interpret κ as a unique thermodynamic indicator without context."

failure_modes:
  - "Tail-only fit underdetermined when energy coverage is narrow"
  - "Mis-application to non-kappa power-law tails"

depends_on:
  - "paper-cuesta-2024-kappa-distributions-energetic-protons"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "Tool-skill candidate: a standardized kappa-tail-fit library is missing across the corpus."
    related_skills: []
  - type: "hypothesis"
    statement: "The kappa-tail closed form is more robust than full-kappa fit when energy coverage is < 1 decade."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Run both methods on PSP E14–E16 spectra; compare RMS residual."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2407.04188"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Kappa-tail technique: Modeling and application to Solar Energetic Particles observed by Parker Solar Probe — paper-skill

> Compiled from arXiv:2407.04188 (2024), Livadiotis, G. et al.
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

- kappa-tail technique
- Livadiotis kappa formalism
- high-energy SEP tail fit

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** The kappa-tail technique provides a closed-form fit to the high-energy tail of a kappa distribution and is applied to PSP/IS☉IS energetic-particle spectra to extract κ, T_EP, n_EP.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Closed-form vs full kappa fit consistency on PSP spectra (TODO_verify numerics). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Kappa-tail closed-form derivation

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Kappa-tail closed-form derivation as a callable on the data products in §4.

### Spectral fit (κ, T_EP, n_EP)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Spectral fit (κ, T_EP, n_EP) as a callable on the data products in §4.

### Residual / goodness-of-fit diagnostics

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Residual / goodness-of-fit diagnostics as a callable on the data products in §4.

### Comparison against full kappa fit

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Comparison against full kappa fit as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| PSP/IS☉IS EPI-Hi | L2/L3 | instrument-native | Application events (TODO_verify) | PSP SOC | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Closed-form vs full kappa fit consistency on PSP spectra (TODO_verify numerics).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Tail-only fit underdetermined when energy coverage is narrow
- Mis-application to non-kappa power-law tails

## 7. Claim boundary  *(Layer 1)*

**In scope.** Methodology paper + PSP application; closed-form kappa-tail formula; spectral fit and parameter extraction.

**Out of scope — do NOT generalize beyond:**

- Do not use the closed form outside its derivation range.
- Do not interpret κ as a unique thermodynamic indicator without context.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2407.04188
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-cuesta-2024-kappa-distributions-energetic-protons]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — Tool-skill candidate: a standardized kappa-tail-fit library is missing across the corpus.
- **Hypothesis** — The kappa-tail closed form is more robust than full-kappa fit when energy coverage is < 1 decade.
- **Minimal_experiment** — Run both methods on PSP E14–E16 spectra; compare RMS residual.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
