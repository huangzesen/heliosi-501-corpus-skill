---
name: paper-sun-2026-counterfactual-sep-prediction-ml
description: >-
  Use when physics-guided ml or related diagnostics surface in a SEP / shock / space-weather workflow — central claim: A physics-guided counterfactual explanation framework on multivariate time series identifies which input features (solar wind / radio / X-ray) drive a SEP prediction, improving scalability and interpretability over black-box ML. (arXiv:2601.08999, 2026).
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
  title: "Physics-Guided Counterfactual Explanations for Large-Scale Multivariate Time Series: Application in Scalable and Interpretable SEP Event Prediction"
  first_author: null
  authors: []
  authors_verified: false
  year: 2026
  venue: "Journal — TODO_verify_with_full_text"
  doi: null
  arxiv_id: "2601.08999"
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
  - "physics-guided ML"
  - "counterfactual explanations"
  - "SEP prediction"
  - "multivariate time series"
  - "interpretability"

data_products:
  - instrument: "GOES SEM/SEISS proton"
    level: "L2"
    cadence: "5-min"
    interval: "Training window TODO_verify"
    archive: "NOAA SWPC"
  - instrument: "SDO/AIA flare"
    level: "L1.5"
    cadence: "12s"
    interval: "Training window"
    archive: "JSOC"
  - instrument: "Wind/WAVES type II/III"
    level: "L2"
    cadence: "minute"
    interval: "Training window"
    archive: "NASA CDAWeb"

algorithms:
  - name: "Multivariate time-series encoder"
    equation_refs: []
    external_implementations: []
  - name: "Physics-guided regularization (e.g. constrain to known shock/flare-association)"
    equation_refs: []
    external_implementations: []
  - name: "Counterfactual generator (minimum perturbation flipping the prediction)"
    equation_refs: []
    external_implementations: []
  - name: "Per-feature attribution score"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2601.08999"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    ML framework with counterfactual layer; training set from public SEP catalogs (TODO_verify); evaluation on hold-out SEP events; only the explanation framework and per-feature attribution is claimed.
  out_of_scope:
    - "Do not use the explanation framework as a causal-mechanism proof."
    - "Do not generalize to events / energies outside the training distribution."

failure_modes:
  - "Training-set imbalance (rare SEP events vs many non-events)"
  - "Counterfactuals can lie outside physical region without explicit constraints"
  - "Cross-cycle generalization (cycle 24 → 25) under-tested"

depends_on:
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"
  - "paper-meng-2025-sepnet-multi-task-ml"

adapter_notes: []

research_generation_affordances:
  - type: "gap"
    statement: "No multi-mission ground-truth (Earth + STEREO + PSP + SOLO) consensus label set for SEP-prediction ML."
    related_skills: []
  - type: "hypothesis"
    statement: "Counterfactual attributions concentrate on type II radio bursts more strongly than on X-ray flux for the largest events."
    related_skills: ["paper-duan-2026-sep-type-ii-radio-source-regions"]
  - type: "minimal_experiment"
    statement: "Train on Earth-only labels, test on STEREO-A-only ground truth; evaluate counterfactual stability."
    related_skills: []

provenance:
  generated_by: "HelioSI paper-to-skill factory (Claude Opus 4.7) — wave500 SEP/shocks/space-weather batch"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2601.08999"
  verified_by: null
  verified_at: null

tags: ['heliophysics', 'paper-skill', 'sep', 'shocks', 'space-weather']
---

# Physics-Guided Counterfactual Explanations for Large-Scale Multivariate Time Series: Application in Scalable and Interpretable SEP Event Prediction — paper-skill

> Compiled from arXiv:2601.08999 (2026), unverified author et al.
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

- physics-guided ML
- counterfactual explanations
- SEP prediction

Do NOT use this skill when:

- The science target is outside the claim boundary in §7.
- The numeric specifics required exceed what an arXiv-abstract-grounded
  stub can supply (promote first per spec §7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** A physics-guided counterfactual explanation framework on multivariate time series identifies which input features (solar wind / radio / X-ray) drive a SEP prediction, improving scalability and interpretability over black-box ML.

**Verifiable task.** A reproduction succeeds when an agent reads the
abstract capability contract in §3–§4 and reproduces Hold-out F1 / TSS / ROC-AUC (numerics TODO_verify); counterfactual sparsity per event. within
the tolerance stated by the published figure / table (TODO_verify
specific tolerance from the full text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract)*

Each algorithm below is described as an **abstract capability** the
runtime must supply. Do not name a specific MCP, plugin, or harness
command here — those belong to §8 / `adapter_notes[]`.

### Multivariate time-series encoder

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Multivariate time-series encoder as a callable on the data products in §4.

### Physics-guided regularization (e.g. constrain to known shock/flare-association)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Physics-guided regularization (e.g. constrain to known shock/flare-association) as a callable on the data products in §4.

### Counterfactual generator (minimum perturbation flipping the prediction)

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Counterfactual generator (minimum perturbation flipping the prediction) as a callable on the data products in §4.

### Per-feature attribution score

- Procedure (abstract, runtime-neutral):
  1. TODO_verify_with_full_text — paraphrased from inventory abstract only.
- Capability requirements:
  - Per-feature attribution score as a callable on the data products in §4.


## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract)*

Each `data_products[]` entry is rendered as a **tool contract**: what
must be fetchable, at what level, at what cadence, from what archive.
**The contract does not assume any specific MCP, plugin, or harness
command exists.**

| Instrument | Level | Cadence | Interval | Archive | Capability requirement |
|------------|-------|---------|----------|---------|------------------------|
| GOES SEM/SEISS proton | L2 | 5-min | Training window TODO_verify | NOAA SWPC | abstract: load + decode + subset |
| SDO/AIA flare | L1.5 | 12s | Training window | JSOC | abstract: load + decode + subset |
| Wind/WAVES type II/III | L2 | minute | Training window | NASA CDAWeb | abstract: load + decode + subset |

## 5. Validation target → benchmark artifact  *(Layer 2)*

Not benchmarked yet. Promotion to `executable` requires the named
numeric specifics (TODO_verify_with_full_text) and the figure / table
reference. The target is: Hold-out F1 / TSS / ROC-AUC (numerics TODO_verify); counterfactual sparsity per event.

## 6. Failure modes → skill memory  *(Layer 1)*

Pitfalls a future agent applying this skill must remember:

- Training-set imbalance (rare SEP events vs many non-events)
- Counterfactuals can lie outside physical region without explicit constraints
- Cross-cycle generalization (cycle 24 → 25) under-tested

## 7. Claim boundary  *(Layer 1)*

**In scope.** ML framework with counterfactual layer; training set from public SEP catalogs (TODO_verify); evaluation on hold-out SEP events; only the explanation framework and per-feature attribution is claimed.

**Out of scope — do NOT generalize beyond:**

- Do not use the explanation framework as a causal-mechanism proof.
- Do not generalize to events / energies outside the training distribution.

If a downstream task asks for a generalization listed above, refuse it
and route to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional)*

- DOI: TODO_verify_with_full_text
- arXiv: https://arxiv.org/abs/2601.08999
- ADS: TODO_verify_with_full_text
- Code: none on file
- Data: per §4 tool contracts

No adapter examples on file yet.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill assumes the
following sibling paper-skills (one line of justification each).
Unresolved links remain as `[[slug]]` until they exist in the corpus.

- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` — assumed for context (see linked skill).
- `[[paper-meng-2025-sepnet-multi-task-ml]]` — assumed for context (see linked skill).

**Research-generation affordances** (also in
`research_generation_affordances[]` so a graph walker can ingest them
without re-parsing prose):

- **Gap** — No multi-mission ground-truth (Earth + STEREO + PSP + SOLO) consensus label set for SEP-prediction ML.
- **Hypothesis** — Counterfactual attributions concentrate on type II radio bursts more strongly than on X-ray flux for the largest events. Related: `[[paper-duan-2026-sep-type-ii-radio-source-regions]]`.
- **Minimal_experiment** — Train on Earth-only labels, test on STEREO-A-only ground truth; evaluate counterfactual stability.

## Notes

All numerics, event dates, DOIs, ADS bibcodes, code repositories, and
exact tolerances are flagged `TODO_verify_with_full_text` — this stub
was compiled from the arXiv-inventory abstract only and must not be
treated as a verified reproduction artifact (see spec §1, §7).
