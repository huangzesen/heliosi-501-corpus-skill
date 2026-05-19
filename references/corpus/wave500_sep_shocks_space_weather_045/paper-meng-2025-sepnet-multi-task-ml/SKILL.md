---
name: paper-meng-2025-sepnet-multi-task-ml
description: >-
  Use when sepnet or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: SEPNET is a multi-task deep-learning model that simultaneously predicts SEP-event occurrence, peak proton flux, and spectral index, outperforming single-task baselines on a hold-out catalog. (arXiv:2512.12786, 2025).
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
  title: "Solar Energetic Particle Forecasting with Multi-Task Deep Learning: SEPNET"
  first_author: null
  authors: []
  authors_verified: false
  year: 2025
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2512.12786"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - sep
    - shocks
    - space-weather
  missions: [GOES, SDO, STEREO, Wind]
  regime: [inner-heliosphere]

trigger_keywords:
  - "SEPNET"
  - "multi-task deep learning"
  - "SEP forecast"
  - "joint occurrence / peak-flux / spectral-index head"
  - "operational SEP prediction"

data_products:
  - instrument: "GOES SEISS/EPS proton"
    level: "L2"
    cadence: "5-min"
    interval: "Training catalog"
    archive: "NOAA SWPC"
  - instrument: "SDO/HMI + AIA active-region context"
    level: "L1.5"
    cadence: "12s/720s"
    interval: "Training window"
    archive: "JSOC"
  - instrument: "Wind/WAVES + STEREO/WAVES radio"
    level: "L2"
    cadence: "minute"
    interval: "Training window"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Multi-task neural-network head (occurrence + peak flux + spectral index)"
    equation_refs: []
    external_implementations: []
  - name: "Class-imbalance loss"
    equation_refs: []
    external_implementations: []
  - name: "Time-series convolution / transformer backbone (TODO_verify)"
    equation_refs: []
    external_implementations: []
  - name: "Probability-calibration check"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2512.12786"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Single-spacecraft training (GOES/SDO/STEREO/Wind — TODO_verify); standard event-driven train/val/test split; predictive performance only, not operational deployment.
  out_of_scope:
    - "Do not deploy operationally without an independent uncertainty-quantification check."
    - "Do not apply outside the training-window energy bands."

failure_modes:
  - "Class imbalance — false-positive rate may be unacceptable for operations"
  - "Concept drift across solar cycles"
  - "Joint-task gradient interference — single-task can outperform on individual heads"

depends_on:
  - "paper-sun-2026-counterfactual-sep-prediction-ml"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No cross-mission deep-learning baseline that conditions on PSP/SOLO connectivity."
    related_skills: []
  - type: "hypothesis"
    statement: "Adding magnetic-connectivity features (PFSS+ballistic) measurably reduces peak-flux RMSE."
    related_skills: []
  - type: "minimal_experiment"
    statement: "Re-train SEPNET with PFSS+ballistic footpoint as a static feature; compare RMSE."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2512.12786"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Solar Energetic Particle Forecasting with Multi-Task Deep Learning: SEPNET — paper-skill

> Compiled from arXiv:2512.12786 (2025), unverified author et al.
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

- SEPNET
- multi-task deep learning
- SEP forecast

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** SEPNET is a multi-task deep-learning model that simultaneously predicts SEP-event occurrence, peak proton flux, and spectral index, outperforming single-task baselines on a hold-out catalog.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Hold-out TSS / Heidke / RMSE per head (numerics TODO_verify); calibration plot. within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Multi-task neural-network head (occurrence + peak flux + spectral index)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Multi-task neural-network head (occurrence + peak flux + spectral index) as a callable on the data products in §4.

### Class-imbalance loss

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Class-imbalance loss as a callable on the data products in §4.

### Time-series convolution / transformer backbone (TODO_verify)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Time-series convolution / transformer backbone (TODO_verify) as a callable on the data products in §4.

### Probability-calibration check

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Probability-calibration check as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| GOES SEISS/EPS proton | L2 | 5-min | Training catalog | NOAA SWPC | abstract: load + decode + subset |
| SDO/HMI + AIA active-region context | L1.5 | 12s/720s | Training window | JSOC | abstract: load + decode + subset |
| Wind/WAVES + STEREO/WAVES radio | L2 | minute | Training window | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Hold-out TSS / Heidke / RMSE per head (numerics TODO_verify); calibration plot.

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Class imbalance — false-positive rate may be unacceptable for operations
- Concept drift across solar cycles
- Joint-task gradient interference — single-task can outperform on individual heads

## 7. Claim boundary  *(Layer 1)*

**In scope.** Single-spacecraft training (GOES/SDO/STEREO/Wind — TODO_verify); standard event-driven train/val/test split; predictive performance only, not operational deployment.

**Out of scope — do NOT generalize beyond:**

- Do not deploy operationally without an independent uncertainty-quantification check.
- Do not apply outside the training-window energy bands.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2512.12786
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-sun-2026-counterfactual-sep-prediction-ml]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No cross-mission deep-learning baseline that conditions on PSP/SOLO connectivity.
- **Hypothesis** — Adding magnetic-connectivity features (PFSS+ballistic) measurably reduces peak-flux RMSE.
- **Minimal_experiment** — Re-train SEPNET with PFSS+ballistic footpoint as a static feature; compare RMSE.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
