---
name: paper-li-2020-solar-wind-supervised-extension-multi-mission
description: >-
  Use when selecting or benchmarking a supervised ML model family (KNN, SVM, RF,
  GBM, NN, ...) on the Xu–Borovsky 4-class solar-wind labels at 1 au — central
  paper claim is that an 8-dim feature subset (B_T, N_p, T_p, V_p, N_alpha/N_p,
  T_exp/T_p, S_p, M_f) with KNN reaches 92.8% overall accuracy on the four
  classes (Li, Wang, Tu, Xu 2020, Earth & Space Science, doi:10.1029/2019EA000997,
  arXiv:1811.02323).
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
  title: "Machine Learning Approach for Solar Wind Categorization"
  first_author: "H. Li"
  authors:
    - "H. Li"
    - "C. Wang"
    - "C. Tu"
    - "F. Xu"
  authors_verified: false
  year: 2020
  venue: "Earth and Space Science, 7(5), e2019EA000997"
  doi: "10.1029/2019EA000997"
  arxiv_id: "1811.02323"
  ads_bibcode: "2020E&SS....700997L"
domain:
  primary_theme: solar_wind_segmentation
  secondary_themes: ["machine-learning", "supervised-classification", "ten-model-benchmark", "1au"]
  missions: ["ACE"]
  regime: ["1au"]
trigger_keywords: ["solar-wind", "classification", "knn", "svm", "random-forest", "benchmark", "1au", "xu-borovsky", "li-2020"]
data_products: []
algorithms: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1029/2019EA000997"
  arxiv_url: "https://arxiv.org/abs/1811.02323"
  ads_url: "https://ui.adsabs.harvard.edu/abs/2020E%26SS....700997L/abstract"
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Li, Wang, Tu, & Xu (2020) benchmark 10 supervised classifiers on the
    Xu–Borovsky four-class solar-wind labelling at 1 au using ACE-derived
    hourly data. After exhaustive feature-subset enumeration over 13
    candidate parameters, an 8-dim subset (B_T, N_p, T_p, V_p,
    N_alpha/N_p, T_exp/T_p, S_p, M_f) with KNN attains the highest
    reported overall accuracy of 92.8% across the four classes. The slug
    name retains "extension-multi-mission" for stable cross-references,
    but the primary paper is single-source (ACE-derived); a true
    multi-mission generalisation is out of scope.
  out_of_scope:
    - "Do NOT extrapolate the 92.8% headline accuracy to Wind, STEREO, PSP, or Solar Orbiter — the paper does NOT cross-train across missions."
    - "Do NOT use this slug to anchor 'multi-mission' claims — those belong to follow-up work that has not yet been bound to this slug."
    - "Do NOT bind the executable protocol to a specific runtime / MCP / plugin until method-ready promotion."
failure_modes:
  - "Treating 92.8% as a per-class accuracy — the abstract reports overall accuracy; per-class accuracy / F1 / confusion-matrix entries remain TODO_verify_with_full_text against the published tables."
  - "Misattributing the paper to E. Camporeale — sibling slugs in this batch (paper-camporeale-2017-knn-supervised-comparison-ten-models, paper-camporeale-2018-knn-solar-wind-classification-validation) carry the same arXiv ID (1811.02323) but list E. Camporeale as first_author; this is the factory misattribution we surface here. The arXiv ID 1811.02323 corresponds to the Li-Wang-Tu-Xu paper, not Camporeale."
  - "Promoting beyond stub without checking whether the 'manual classification scheme' baseline in the ~9.6 pp improvement claim refers to Xu-Borovsky 2015 vs Zhao 2009 vs another reference — this is currently TODO_verify_with_full_text."
depends_on: ["paper-camporeale-2017-knn-solar-wind-categorization", "paper-xu-borovsky-categorization-extension-1au"]
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Per-class accuracy / F1 / confusion-matrix entries are not yet anchored — the overall 92.8% headline does not tell us whether 'ejecta' is the weak class (typical in 4-class solar-wind work due to severe class imbalance)."
    related_skills: ["paper-camporeale-2017-knn-solar-wind-categorization", "paper-xu-borovsky-categorization-extension-1au"]
    proposed_action: "Read Li et al. 2020 §4 confusion matrices, transcribe per-class precision/recall/F1, and add to validation_target."
  - type: minimal_experiment
    statement: "Re-derive the 92.8% headline accuracy by training KNN on the 8-dim feature subset over ACE hourly with Xu-Borovsky labels and reporting 5-fold cross-validated accuracy."
    related_skills: ["paper-xu-borovsky-categorization-extension-1au"]
    proposed_action: "Use the published 8-dim feature subset and the same Xu-Borovsky labels; expect overall accuracy to land within a few percentage points of 92.8% (tolerance TODO_verify_with_full_text)."
  - type: open_question
    statement: "Does the Li 2020 ranking (KNN > Random Forest > XGBoost > ...) hold when the labels come from a probabilistic Xu-Borovsky variant (e.g. Camporeale 2017 Gaussian Process soft labels) rather than the hard Xu-Borovsky cuts? The 10-model ranking may shift under soft labels."
    related_skills: ["paper-camporeale-2017-knn-solar-wind-categorization"]
    proposed_action: "Re-run the 10-model benchmark with GP-soft labels and compare the model ranking."
provenance:
  generated_by: "HelioSI paper-to-skill factory (wave500 batch, 2026-05-18, Claude Code)"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_solar_wind_segmentation.json"
  verified_by: "Claude Code internalization session (bibliographic anchor web-verified via Wiley AGU + Semantic Scholar + arXiv)"
  verified_at: "2026-05-19T00:00:00Z"
tags: [heliophysics, paper-skill, solar-wind-classification, stub]
---

# Li 2020 supervised solar-wind categorization (10-model benchmark, 8-dim feature subset, KNN best) — paper-skill (stub)

> Anchored in Li, H., Wang, C., Tu, C., Xu, F. (2020), "Machine Learning Approach for Solar Wind Categorization", *Earth and Space Science*, 7(5), e2019EA000997, doi:10.1029/2019EA000997, arXiv:1811.02323 (ADS: 2020E&SS....700997L). Bibliographic anchor web-verified 2026-05-19. The slug name retains "extension-multi-mission" for stable cross-references, but the primary paper is single-source (ACE-derived at 1 au); the "multi-mission extension" framing in the original stub is removed here in favour of the verified single-source benchmark.
> **Quality tier**: `stub` — Layer 1 is populated against the verified abstract; Layer 2 (executable protocol) requires reading the published §3-§5 to transcribe the 10-model hyperparameters and per-class confusion matrices.
>
> **Four-layer reminder (spec §4)**:
> - L1 (scientific invariant) → §1, §2, §6, §7
> - L2 (executable protocol, abstract contracts) → §3, §4, §5 — *populated at method-ready promotion*
> - L3 (adapter examples, optional) → §8 sub-block + `adapter_notes[]` — *empty at stub*
> - L4 (research-generation affordance) → §9 sub-block + `research_generation_affordances[]`

This file is the agent-native compiled form of the paper above, **not a summary**.
At stub tier Layer 1 is anchored in the verified abstract; Layer 2 and Layer 3 are intentionally
left as TODOs for promotion.

---

## 1. Trigger  *(Layer 1)*

A future agent should reach for this skill when:

- Selecting a supervised ML model family for 1-au solar-wind class assignment over the Xu-Borovsky 4-class labels.
- Choosing an 8-dim feature subset for an ACE-derived hourly solar-wind classifier (B_T, N_p, T_p, V_p, N_alpha/N_p, T_exp/T_p, S_p, M_f).
- Comparing a new classifier against the Li 2020 published 10-model benchmark.
- Building on the Li 2020 results as a baseline before introducing probabilistic (Camporeale 2017) or Bayesian (Narock 2024) classifiers.

Do NOT use this skill when:

- The task is at radial distances substantially away from 1 au (PSP/Solar Orbiter inner heliosphere) — the feature subset and benchmark are validated only at 1 au.
- The task requires per-class precision/recall/F1 — those are not yet transcribed from §4 of the paper.
- The task requires a cross-mission generalisation (Wind ↔ ACE ↔ STEREO) — the paper does not cross-train.
- The task crosses the claim-boundary scope below (§7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Li, Wang, Tu, Xu (2020) benchmark 10 supervised classifiers on the Xu-Borovsky 4-class labels (coronal-hole, streamer-belt, sector-reversal, ejecta) using ACE-derived 1-au hourly data. After exhaustive enumeration over 8,191 feature combinations on 13 candidate parameters, the best 8-dim subset is (B_T, N_p, T_p, V_p, N_alpha/N_p, T_exp/T_p, S_p, M_f). On that subset, KNN achieves the highest overall classification accuracy: **92.8%** across the four classes (Li et al. 2020 abstract).

**Verifiable task.** Reproduce the headline benchmark:
- Fetch ACE-derived hourly data covering the period used in Li et al. 2020 (period TODO_verify_with_full_text).
- Compute the 8-dim feature vector per hourly sample.
- Apply the Xu-Borovsky 2015 algebraic scheme to derive ground-truth labels.
- Train KNN with the published hyperparameters (k value, distance metric TODO_verify_with_full_text), 5-fold or k-fold cross-validation (split TODO_verify_with_full_text).
- Report overall accuracy across the four classes — target: within a small tolerance of 92.8% (tolerance TODO_verify_with_full_text against §4 tables).
- Optionally repeat for the other 9 models (linear SVM, RBF SVM, Decision Tree, Random Forest, AdaBoost, Neural Network, Gaussian Naive Bayes, Quadratic Discriminant Analysis, XGBoost) and confirm KNN remains top-ranked.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract — STUB)*

Layer 2 is sketched conceptually here; explicit hyperparameters and per-fold splits are pending re-read of §3-§4:

1. **Feature derivation.** Compute the 8-dim feature vector per hourly ACE sample:
   - B_T = magnetic field magnitude
   - N_p = proton number density
   - T_p = proton temperature
   - V_p = proton bulk speed
   - N_alpha/N_p = alpha-to-proton density ratio
   - T_exp/T_p = ratio of velocity-dependent expected temperature to observed proton temperature (TODO_verify_with_full_text — which T_exp(v_sw) form? Lopez 1987 vs Xu-Borovsky 2015 fit)
   - S_p = T_p / N_p^{2/3} (proton-specific entropy proxy)
   - M_f = fast-magnetosonic Mach number (TODO_verify_with_full_text — exact denominator definition)
2. **Label derivation.** Apply Xu-Borovsky 2015 algebraic decision tree to obtain hard 4-class labels.
3. **Train / test split.** k-fold cross-validation; k value and stratification by class TODO_verify_with_full_text.
4. **Model bench.** Train 10 supervised classifiers with hyperparameters TODO_verify_with_full_text per Li et al. 2020 Table (TODO_verify_with_full_text); report overall accuracy + per-class precision/recall/F1 (TODO_verify_with_full_text).

Do not bind to a specific runtime / MCP / plugin in this section — keep all bindings in §8 (`adapter_notes`).

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract — STUB)*

Pending method-ready promotion, the required data products:

- **ACE/SWEPAM hourly**: 1-au proton plasma (n_p, T_p, V_p, N_alpha/N_p). Cadence: 1 h. Archive: SPDF/CDAWeb or ACE Science Center. Capability: fetch, decode, subset by time.
- **ACE/MAG hourly**: 1-au magnetic field (B_T magnitude + components). Cadence: 1 h. Same archive. Capability: align to SWEPAM hourly grid.
- **Xu-Borovsky 2015 label generator**: companion skill `[[paper-xu-borovsky-categorization-extension-1au]]` produces 4-class ground-truth labels per hourly sample.

Empty `data_products[]` in frontmatter is acceptable at stub tier.

## 5. Validation target → benchmark artifact  *(Layer 2 — STUB)*

> Validation target: **KNN overall accuracy = 92.8% across the four Xu-Borovsky classes (TODO_verify_with_full_text against §4 table — exact figure/table number and per-class breakdown needed).** Promotion to `executable` requires setting `validation_target.metric = "overall_classification_accuracy"`, `validation_target.target = 0.928` (TODO_verify_with_full_text), and a numeric tolerance against §4 of Li et al. 2020.

## 6. Failure modes → skill memory  *(Layer 1)*

- **Headline-overreach.** The 92.8% figure is overall accuracy across all four classes; if "ejecta" is severely under-represented (typical for 4-class solar-wind work), KNN may still mis-classify most ejecta samples while reporting high overall accuracy. Per-class metrics are TODO_verify_with_full_text.
- **Author misattribution risk.** Sibling slugs in this batch carry the same arXiv ID (1811.02323) but wrongly list E. Camporeale as first author (paper-camporeale-2017-knn-supervised-comparison-ten-models, paper-camporeale-2018-knn-solar-wind-classification-validation). The arXiv ID 1811.02323 corresponds to **Li, Wang, Tu, Xu (2020)**, not Camporeale. Do not silently merge those slugs into this one without an audit-log entry.
- **Cross-mission leakage.** The paper trains and tests on ACE-derived data only. Inferring Wind / STEREO / PSP performance from the 92.8% headline is unsupported.
- **Baseline-identity ambiguity.** The "~9.6 pp improvement over manual / earlier classification schemes" abstract claim does not specify the baseline; do not silently equate it to a specific named scheme (Zhao 2009, Stakhiv 2015, etc.) without checking §4.
- **Adapter leakage risk at promotion.** When Layer 2 is populated, ensure no runtime / MCP / plugin name appears in §3 / §4 / §5; all such names belong in `adapter_notes[]`.
- **Slug-stability contract.** Once this slug is referenced by another paper-skill via `depends_on`, it must not be renamed without a `provenance` audit entry.

## 7. Claim boundary  *(Layer 1)*

**In scope.** A 10-model supervised benchmark on the Xu-Borovsky 4-class labelling at 1 au using ACE-derived hourly data; an exhaustive feature-selection result identifying an 8-dim subset (B_T, N_p, T_p, V_p, N_alpha/N_p, T_exp/T_p, S_p, M_f); KNN as the top-ranked model with 92.8% overall accuracy on the test split.

**Out of scope — do NOT generalise beyond:**

- Distances substantially away from 1 au (PSP / Solar Orbiter / Ulysses).
- Cross-mission generalisation (Wind ↔ ACE ↔ STEREO) — the paper does not cross-train; the slug name's "multi-mission" tail is a research-affordance label, not a paper-side claim.
- Sub-hourly cadence applications — the paper is built and validated on hourly data.
- Per-class accuracy / F1 / confusion-matrix claims — those are TODO_verify_with_full_text.
- Any runtime / MCP / plugin assumption — this skill is harness-agnostic; bindings live in `adapter_notes[]`.

If a downstream task asks for a generalisation listed above, refuse it and return a reference to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional — empty at stub)*

**Canonical links to the published artifact:**

- DOI: https://doi.org/10.1029/2019EA000997
- arXiv: https://arxiv.org/abs/1811.02323
- ADS: 2020E&SS....700997L — https://ui.adsabs.harvard.edu/abs/2020E%26SS....700997L/abstract
- Code: n/a — no public reference implementation identified at stub tier.
- Data: ACE/SWEPAM + ACE/MAG L2 hourly (SPDF/CDAWeb).

**Adapter binding examples (optional, illustrative only):** none recorded at stub tier;
`adapter_notes[]` is intentionally empty.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill builds on:

- `[[paper-xu-borovsky-categorization-extension-1au]]` — the Xu-Borovsky 2015 parent labelling scheme that supplies ground-truth labels for the Li 2020 benchmark.
- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — earlier Gaussian-Process probabilistic classifier on the same labels (different paper, despite the arXiv-ID confusion in sibling Camporeale-titled slugs).

**Research-generation affordances.** Forward-pointing surface of the skill (spec §4 Layer 4):

- **Gap** — Per-class precision/recall/F1 and the identity of the "~9.6 pp baseline" are not yet anchored; transcribing §4 tables would close this gap.
- **Minimal experiment** — Re-derive the 92.8% headline accuracy with KNN on the 8-dim feature subset over ACE hourly with Xu-Borovsky labels.
- **Cross-mission extension** — Replay the same 10-model benchmark on Wind/SWE+MFI and STEREO/PLASTIC+IMPACT hourly to test the "extension-multi-mission" hypothesis the slug name suggests. (This is a research target; the original paper does not claim cross-mission generalisation.)
- **Open question** — Does the KNN > RF > XGBoost ranking hold under probabilistic (Camporeale 2017 GP) labels rather than hard Xu-Borovsky cuts?

## Notes

This slug is the verified anchor for the Li, Wang, Tu, Xu (2020) paper "Machine Learning Approach for Solar Wind Categorization" (Earth & Space Science, doi:10.1029/2019EA000997, arXiv:1811.02323). The slug name's "extension-multi-mission" tail is preserved for stable cross-references but does not reflect a paper-side claim — the primary paper is single-source (ACE-derived at 1 au). A true cross-mission generalisation is enumerated as a Layer-4 research affordance in §9.
