---
name: paper-xu-borovsky-categorization-extension-1au
description: >-
  Use when applying or refining the Xu–Borovsky physical 4-class
  (coronal-hole / streamer-belt / sector-reversal / ejecta) labelling at 1 au —
  central claim is the three-parameter algebraic scheme over
  (S_p, v_A, T_p/T_exp) anchored in Xu & Borovsky 2015 (JGR Space Phys
  120(1):70-100, doi:10.1002/2014JA020412); ML-style accuracy is reported by
  downstream classifiers, not by the parent scheme.
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
  title: "A new four-plasma categorization scheme for the solar wind (parent scheme; extension lineage anchor)"
  first_author: "F. Xu"
  authors:
    - "F. Xu"
    - "J. E. Borovsky"
  authors_verified: false
  year: 2015
  venue: "Journal of Geophysical Research: Space Physics, 120(1), 70-100"
  doi: "10.1002/2014JA020412"
  arxiv_id: null
  ads_bibcode: "2015JGRA..120...70X"
domain:
  primary_theme: solar_wind_segmentation
  secondary_themes: ["machine-learning", "labelling-rules", "1au"]
  missions: ["ACE", "Wind", "OMNI"]
  regime: ["1au"]
trigger_keywords: ["xu-borovsky", "solar-wind", "labelling", "categorization", "1au", "supervised", "four-class"]
data_products: []
algorithms: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1002/2014JA020412"
  arxiv_url: null
  ads_url: "https://ui.adsabs.harvard.edu/abs/2015JGRA..120...70X/abstract"
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Parent (Xu & Borovsky 2015): a three-parameter algebraic scheme on
    (proton-specific entropy S_p = T_p / n_p^{2/3}, proton Alfvén speed
    v_A, and proton temperature T_p compared to a velocity-dependent
    expected temperature T_exp(v_sw)) classifies 1-au solar wind into
    four plasma types — coronal-hole-origin, streamer-belt-origin,
    sector-reversal-region, and ejecta. Validated on OMNI2 1963-2013 and
    ACE 1998-2008. The "extension to 1 au" lineage in the slug name is
    NOT anchored to a single verified extension paper; downstream
    extension work is enumerated as L4 research affordances.
  out_of_scope:
    - "Do NOT use the four-class boundaries away from 1 au without an explicit re-derivation — the thresholds are tuned to ACE/OMNI in-ecliptic conditions."
    - "Do NOT report ML-style class-balanced accuracy from the parent scheme — the parent paper does not train a classifier; it defines a deterministic labelling rule."
    - "Do NOT bind the executable protocol to a specific runtime / MCP / plugin until method-ready promotion."
failure_modes:
  - "Mistaking the rule-based labelling for a probabilistic classifier — class boundaries are hard cuts in (S_p, v_A, T_p/T_exp) space; downstream supervised work (e.g. Li 2020, Camporeale 2017) is what produces accuracy/F1 figures."
  - "Misattributing a downstream re-thresholding paper to this slug — the slug intentionally anchors the parent scheme; bind a specific extension paper only when a verified extension citation has been added to provenance."
depends_on: ["paper-camporeale-2017-knn-solar-wind-categorization"]
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "No single verified 'Xu-Borovsky 1-au extension' paper is anchored at stub tier; candidate extensions (re-thresholding, ML soft-labelling, multi-mission ports) are tracked in §9."
    related_skills: ["paper-camporeale-2017-knn-solar-wind-categorization", "paper-li-2020-solar-wind-supervised-extension-multi-mission"]
    proposed_action: "Promote to method-ready by selecting a specific extension paper, re-anchoring the bibliographic block, and populating §3/§4/§5 against its full text."
  - type: minimal_experiment
    statement: "Reproduce the four-class label assignment on a 1-month OMNI2 slice and confirm fractional class populations match Xu & Borovsky 2015 Figure 5 (coronal-hole / streamer-belt / sector-reversal / ejecta proportions over a solar cycle)."
    related_skills: ["paper-camporeale-2017-knn-solar-wind-categorization"]
    proposed_action: "Compute (S_p, v_A, T_p/T_exp) from hourly OMNI2, apply the published thresholds, and compare the resulting class fractions to Figure 5 of the parent paper."
provenance:
  generated_by: "HelioSI paper-to-skill factory (wave500 batch, 2026-05-18, Claude Code)"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_solar_wind_segmentation.json"
  verified_by: "Claude Code internalization session (parent scheme web-verified via ADS/AGU)"
  verified_at: "2026-05-19T00:00:00Z"
tags: [heliophysics, paper-skill, solar-wind-classification, stub]
---

# Xu–Borovsky 4-class 1-au solar-wind labelling (parent scheme; extension-lineage anchor) — paper-skill (stub)

> Anchored in Xu, F. & Borovsky, J. E. (2015), "A new four-plasma categorization scheme for the solar wind", *Journal of Geophysical Research: Space Physics*, 120(1), 70-100, doi:10.1002/2014JA020412 (ADS: 2015JGRA..120...70X). The "extension to 1 au" lineage in the slug name is intentionally not anchored to a single extension paper at stub tier; downstream extension work (re-thresholding, ML soft-labelling, multi-mission ports) is enumerated in §9 as research affordances rather than fabricated as a single citation.
> **Quality tier**: `stub` — Layer 1 is populated against the verified parent scheme; Layer 2 (executable protocol) and Layer 3 (adapter bindings) remain to be filled at method-ready promotion.
>
> **Four-layer reminder (spec §4)**:
> - L1 (scientific invariant) → §1, §2, §6, §7
> - L2 (executable protocol, abstract contracts) → §3, §4, §5 — *populated at method-ready promotion*
> - L3 (adapter examples, optional) → §8 sub-block + `adapter_notes[]` — *empty at stub*
> - L4 (research-generation affordance) → §9 sub-block + `research_generation_affordances[]`

This file is the agent-native compiled form of the paper above, **not a summary**.
At stub tier Layer 1 is anchored in the verified parent scheme; Layer 2 and Layer 3 are intentionally
left as TODOs for promotion to a specific extension paper.

---

## 1. Trigger  *(Layer 1)*

A future agent should reach for this skill when:

- Classifying 1-au solar-wind intervals into the Xu-Borovsky four physical origin classes (coronal-hole, streamer-belt, sector-reversal, ejecta).
- Selecting label targets for a supervised ML solar-wind classifier (e.g. KNN/SVM/RF) that wants the Xu-Borovsky boundaries as ground truth.
- Reproducing the deterministic labelling rule on OMNI2 / ACE hourly data and comparing fractional class populations across a solar cycle.

Do NOT use this skill when:

- The task is at radial distances substantially away from 1 au — the algebraic thresholds are tuned to ACE/OMNI in-ecliptic conditions and are not validated against PSP/Solar Orbiter inner-heliosphere data.
- The task requires a probabilistic class assignment — the parent scheme returns hard labels, not class probabilities.
- The task crosses the claim-boundary scope below (§7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** Xu & Borovsky (2015) define a three-parameter algebraic classifier on (S_p = T_p / n_p^{2/3}, v_A, T_p / T_exp(v_sw)) that assigns each 1-au solar-wind hourly sample to exactly one of four origin classes: coronal-hole-origin, streamer-belt-origin, sector-reversal-region, ejecta. Four input measurements (n_p, T_p, B, v_sw) are sufficient.

**Verifiable task.** Implement the published thresholds, apply them to a 1-au hourly stream (OMNI2 or ACE/SWEPAM+MAG L2), and confirm the resulting class fractions match the solar-cycle phasing reported in the parent paper. Numerical reproduction targets:
- Compute (S_p, v_A, T_p/T_exp) from (n_p, T_p, B, v_sw) per the parent paper §3 (TODO_verify_with_full_text — equation numbers).
- Apply the four-class decision tree per parent §4 (TODO_verify_with_full_text — threshold values).
- Aggregate hourly labels into fractional class populations per year over 1963-2013 (OMNI2) or 1998-2008 (ACE).
- Confirm coronal-hole-origin / streamer-belt-origin / sector-reversal / ejecta fractions match Figure 5 of the parent paper (target: same qualitative solar-cycle modulation; quantitative tolerance TODO_verify_with_full_text).

## 3. Methods / equations → executable protocol  *(Layer 2, abstract — STUB)*

Layer 2 is anchored at the conceptual level here; explicit equation numbers and threshold values are pending re-read of the parent §3-§4. To promote to `method-ready`:

1. Read Xu & Borovsky (2015) §3 and transcribe the three derived parameters (S_p, v_A, T_p/T_exp(v_sw)) into `algorithms[]` with their equation references.
2. Read §4 and transcribe the four-class decision tree (threshold values in S_p, v_A, T_p/T_exp space) into a runtime-neutral procedure.
3. Identify whether the parent's "T_exp" velocity-dependent temperature uses Lopez 1987 or a Xu-Borovsky-specific fit (TODO_verify_with_full_text), and record the choice.
4. Add a `data_products[]` entry for OMNI2 hourly and a separate entry for ACE/SWEPAM+MAG L2 hourly.

Do not bind to a specific runtime / MCP / plugin in this section — keep all bindings in §8 (`adapter_notes`).

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract — STUB)*

Pending method-ready promotion, the required data products are sketched here:

- **OMNI2 hourly**: 1963-2013 baseline used by parent (Xu & Borovsky 2015). Fields: n_p, T_p, B (magnitude), v_sw. Cadence: 1 h. Archive: SPDF/CDAWeb. Capability requirement: fetch and decode CDF; subset by time range.
- **ACE/SWEPAM (proton plasma) + ACE/MAG (magnetic field), L2 hourly**: 1998-2008 cross-check baseline. Fields: n_p, T_p, B, v_sw. Cadence: 1 h. Archive: SPDF/CDAWeb or ACE Science Center. Capability requirement: align SWEPAM and MAG to a common hourly grid.

Empty `data_products[]` in frontmatter is acceptable at stub tier; the field will be populated when method-ready promotion lands.

## 5. Validation target → benchmark artifact  *(Layer 2 — STUB)*

> Validation target is anchored to **Figure 5 of Xu & Borovsky (2015)** (fractional class populations over a solar cycle, OMNI2 1963-2013), but the numeric tolerance for "match" is TODO_verify_with_full_text against the figure caption. Promotion to `executable` requires setting `validation_target` with the per-class fraction targets (TODO_verify_with_full_text) and tolerance, and running the classifier end-to-end.

## 6. Failure modes → skill memory  *(Layer 1)*

- **Hard-label vs probabilistic confusion.** The Xu-Borovsky parent scheme returns one of four hard labels per hour. Treating these as soft probabilities will mis-calibrate downstream supervised models — use a probabilistic re-derivation (e.g. Camporeale 2017 GP / Li 2020 KNN) instead.
- **Radial-distance leakage.** Applying the 1-au thresholds to inner-heliosphere (PSP) or out-of-ecliptic (Ulysses) data without re-derivation will mis-classify intervals — the algebraic boundaries are tuned to ACE/OMNI ecliptic conditions.
- **Extension-paper misattribution risk.** This slug intentionally anchors the parent scheme; do NOT silently rewire the bibliographic block to a downstream re-thresholding paper without first verifying that paper independently.
- **Adapter leakage risk at promotion.** When Layer 2 is populated, ensure no runtime / MCP / plugin name appears in §3 / §4 / §5; all such names belong in `adapter_notes[]`.
- **Slug-stability contract.** Once this slug is referenced by another paper-skill via `depends_on`, it must not be renamed without a `provenance` audit entry.

## 7. Claim boundary  *(Layer 1)*

**In scope.** The Xu-Borovsky 2015 four-plasma categorization rule, evaluated on 1-au OMNI2 hourly (1963-2013) and ACE hourly (1998-2008) as in the parent paper. Four input measurements (n_p, T_p, B, v_sw) are sufficient; no composition (e.g. O7+/O6+) is required.

**Out of scope — do NOT generalise beyond:**

- Distances substantially different from 1 au (inner heliosphere / out-of-ecliptic). The algebraic thresholds are not validated there.
- Sub-hourly cadence applications. The parent scheme is built and validated on hourly data.
- Probabilistic class assignment / ML-style accuracy figures. The parent paper reports a deterministic rule, not a trained classifier; ML-style accuracy belongs to downstream slugs (Camporeale 2017, Li 2020).
- Any runtime / MCP / plugin assumption — this skill is harness-agnostic; bindings live in `adapter_notes[]`.

If a downstream task asks for a generalisation listed above, refuse it and return a reference to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional — empty at stub)*

**Canonical links to the published artifact:**

- DOI: https://doi.org/10.1002/2014JA020412
- arXiv: n/a — no arXiv preprint identified for this JGR article.
- ADS: 2015JGRA..120...70X — https://ui.adsabs.harvard.edu/abs/2015JGRA..120...70X/abstract
- Code: n/a — no public reference implementation identified at stub tier.
- Data: OMNI2 hourly (SPDF/CDAWeb); ACE/SWEPAM + ACE/MAG L2 hourly (SPDF/CDAWeb or ACE Science Center).

**Adapter binding examples (optional, illustrative only):** none recorded at stub tier;
`adapter_notes[]` is intentionally empty.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill is the parent anchor for the 1-au labelling lineage; downstream supervised classifiers (KNN, GP, soft-NN) treat it as ground truth:

- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — Gaussian-Process probabilistic classifier trained on the Xu-Borovsky labels.
- `[[paper-li-2020-solar-wind-supervised-extension-multi-mission]]` — KNN/multi-model benchmark over the Xu-Borovsky labels (Li, Wang, Tu, Xu 2020, E&SS).

**Research-generation affordances.** Forward-pointing surface of the skill (spec §4 Layer 4):

- **Gap** — No single verified "Xu-Borovsky 1-au extension" paper is anchored at stub tier; the slug's "extension to 1 au" framing is a research target, not a citation. Related: `[[paper-camporeale-2017-knn-solar-wind-categorization]]`, `[[paper-li-2020-solar-wind-supervised-extension-multi-mission]]`. Proposed: bind a specific re-thresholding paper, or promote this slug to a multi-paper "extension lineage" entry.
- **Minimal experiment** — Re-derive the (S_p, v_A, T_p/T_exp) thresholds from the parent paper, apply to a 1-month OMNI2 slice, and confirm class fractions match Figure 5 of Xu & Borovsky 2015.
- **Open question** — Whether the parent thresholds remain valid for inner-heliosphere data (PSP at perihelion). The published scheme is silent on this; a controlled test against PSP/SWEAP-SPC hourly would tell.

## Notes

This slug intentionally anchors the **parent** Xu & Borovsky 2015 categorization scheme (web-verified 2026-05-19 via ADS/AGU). The "extension to 1 au" tail of the slug name reflects an open research lineage rather than a single verified extension paper. When a specific extension paper is identified, either re-anchor this slug to that paper or split into a new slug; do not silently overwrite the bibliographic block.
