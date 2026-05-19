---
name: paper-liu-2026-3d-coronal-shock-longitudinal-sep
description: >-
  Use when 3d coronal shock reconstruction or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: A 3D coronal shock reconstructed from multi-vantage remote-sensing produces a longitudinal SEP intensity distribution at multiple observers that is consistent with the shock's local θ_Bn / Mach number across longitude. (arXiv:2601.13692, 2026).
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
  title: "Three-dimensional properties of a coronal shock and the longitudinal distribution of its related solar energetic particles"
  first_author: "Liu, R. (TODO verify)"
  authors:
    - "TODO verify"
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2601.13692"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [STEREO-A, SOHO, SDO, Solar Orbiter, PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "3D coronal shock reconstruction"
  - "longitudinal SEP distribution"
  - "EUV wave"
  - "type II"
  - "multi-vantage point reconstruction"

data_products:
  - instrument: "STEREO-A SECCHI COR/EUVI"
    level: "L1.5"
    cadence: "event"
    interval: "Event window"
    archive: "STEREO archive"
  - instrument: "SOHO/LASCO + SDO/AIA"
    level: "L1.5"
    cadence: "event"
    interval: "Event window"
    archive: "CDAW catalog / JSOC"
  - instrument: "Solar Orbiter EUI + Metis"
    level: "L1.5"
    cadence: "event"
    interval: "Event window"
    archive: "ESA SOAR"
  - instrument: "Multi-mission SEP intensity (IS☉IS / EPD / EPAM / SEPT)"
    level: "L2"
    cadence: "instrument-native"
    interval: "Event window"
    archive: "agency archives"

algorithms:
  - name: "3D shock surface reconstruction (ellipsoid / freeform)"
    equation_refs: []
    external_implementations: []
  - name: "θ_Bn, Mach number tabulation along the surface"
    equation_refs: []
    external_implementations: []
  - name: "Per-observer connectivity (PFSS + ballistic) to the shock surface"
    equation_refs: []
    external_implementations: []
  - name: "Longitudinal SEP intensity ↔ local shock-parameter regression"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2601.13692"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single event (TODO_verify date); multi-vantage SECCHI/COR/EUVI; 3D shock surface fit; per-observer SEP peak intensity.
  out_of_scope:
    - "Do not extrapolate shock surface beyond observed time window without an MHD propagator."

failure_modes:
  - "Shock surface fit degenerate with limited viewpoints"
  - "θ_Bn determination depends on coronal field model"
  - "Cross-instrument SEP intensity homogenization needed"

depends_on:
  - "paper-kouloumvakos-2026-iva-shock-properties"
  - "paper-allen-2025-shock-evolution-2023-march-13-event"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No longitudinal-distribution survey with consistent 3D shock fitting across the SO+PSP era catalog."
    related_skills: []
  - type: "hypothesis"
    statement: "SEP longitudinal width is set primarily by local shock obliquity rather than cross-field diffusion."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Re-fit a sub-sample of the IVA-shock catalog with the same 3D shock procedure and test the obliquity-vs-width correlation."
    related_skills: ["paper-kouloumvakos-2026-iva-shock-properties"]

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2601.13692"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Three-dimensional properties of a coronal shock and the longitudinal distribution of its related solar energetic particles — paper-skill

> Compiled from arXiv:2601.13692 (2026), Liu, R. (TODO verify) et al.
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

- 3D coronal shock reconstruction
- longitudinal SEP distribution
- EUV wave

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A 3D coronal shock reconstructed from multi-vantage remote-sensing produces a longitudinal SEP intensity distribution at multiple observers that is consistent with the shock's local θ_Bn / Mach number across longitude.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Longitudinal SEP intensity vs local shock θ_Bn / Mach number correlation (sign + qualitative trend; numerics TODO_verify). within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### 3D shock surface reconstruction (ellipsoid / freeform)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - 3D shock surface reconstruction (ellipsoid / freeform) as a callable on the data products in §4.

### θ_Bn, Mach number tabulation along the surface

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - θ_Bn, Mach number tabulation along the surface as a callable on the data products in §4.

### Per-observer connectivity (PFSS + ballistic) to the shock surface

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-observer connectivity (PFSS + ballistic) to the shock surface as a callable on the data products in §4.

### Longitudinal SEP intensity ↔ local shock-parameter regression

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Longitudinal SEP intensity ↔ local shock-parameter regression as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| STEREO-A SECCHI COR/EUVI | L1.5 | event | Event window | STEREO archive | abstract: load + decode + subset |
| SOHO/LASCO + SDO/AIA | L1.5 | event | Event window | CDAW catalog / JSOC | abstract: load + decode + subset |
| Solar Orbiter EUI + Metis | L1.5 | event | Event window | ESA SOAR | abstract: load + decode + subset |
| Multi-mission SEP intensity (IS☉IS / EPD / EPAM / SEPT) | L2 | instrument-native | Event window | agency archives | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Longitudinal SEP intensity vs local shock θ_Bn / Mach number correlation (sign + qualitative trend; numerics TODO_verify).

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Shock surface fit degenerate with limited viewpoints
- θ_Bn determination depends on coronal field model
- Cross-instrument SEP intensity homogenization needed

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single event (TODO_verify date); multi-vantage SECCHI/COR/EUVI; 3D shock surface fit; per-observer SEP peak intensity.

**Out of scope — do NOT generalize beyond:**

- Do not extrapolate shock surface beyond observed time window without an MHD propagator.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2601.13692
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-kouloumvakos-2026-iva-shock-properties]]` — assumed for context (see linked skill).
- `[[paper-allen-2025-shock-evolution-2023-march-13-event]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No longitudinal-distribution survey with consistent 3D shock fitting across the SO+PSP era catalog.
- **Hypothesis** — SEP longitudinal width is set primarily by local shock obliquity rather than cross-field diffusion.
- **Minimal_experiment** — Re-fit a sub-sample of the IVA-shock catalog with the same 3D shock procedure and test the obliquity-vs-width correlation. Related: `[[paper-kouloumvakos-2026-iva-shock-properties]]`.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
