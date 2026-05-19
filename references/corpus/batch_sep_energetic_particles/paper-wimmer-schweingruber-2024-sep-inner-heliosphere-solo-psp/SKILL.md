---
name: paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp
description: >-
  Use when scoping the inner-heliosphere SEP / ESP / ACR / planetary-bow-shock
  energetic-particle environment using joint Solar Orbiter (EPD) and Parker
  Solar Probe (ISʘIS) observations — Wimmer-Schweingruber+ 2024 (arXiv
  2408.02330) review the multi-source heliospheric energetic-particle
  background and the inner-heliosphere acceleration/transport diagnostics it
  enables.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "SEP environment in the inner heliosphere from Solar Orbiter and Parker Solar Probe"
  first_author: "Wimmer-Schweingruber, R. F."
  authors:
    - "Wimmer-Schweingruber, R. F."
    - "Rodriguez-Pacheco, J."
    - "Ho, G. C."
    - "Cohen, C. M."
    - "Mason, G. M."
    - "the Solar Orbiter EPD team"
  year: 2024
  venue: "Proceedings / Review — TODO verify"
  doi: null
  arxiv_id: "2408.02330"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - inner-heliosphere
    - anomalous-cosmic-rays
    - energetic-storm-particles
    - planetary-bow-shocks
    - multi-mission-conjunction
  missions: [PSP, "Solar Orbiter", ACE, STEREO]
  regime: [inner-heliosphere, 1au]

trigger_keywords:
  - "SEP environment"
  - "energetic storm particles"
  - "ESP"
  - "anomalous cosmic rays"
  - "ACR"
  - "Solar Orbiter EPD"
  - "PSP ISʘIS"
  - "planetary bow shock"
  - "inner heliosphere"
  - "multi-mission conjunction"
  - "background variability"
  - "particle acceleration sites"

data_products:
  - instrument: "SO/EPD (SIS, HET, EPT, STEP)"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "SO orbit 2020-present"
    archive: "SOAR (Solar Orbiter Archive)"
  - instrument: "PSP/ISʘIS EPI-Lo + EPI-Hi"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "PSP encounters E1-present"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "ACE / STEREO energetic-particle suites"
    level: "L2"
    cadence: "instrument-native"
    interval: "cross-reference 1 au"
    archive: "NASA CDAWeb / SPDF"

algorithms:
  - name: "Multi-source energetic-particle background decomposition"
    equation_refs: []
    external_implementations: []
  - name: "SEP vs ESP vs ACR vs bow-shock-particle classifier"
    equation_refs: []
    external_implementations: []
  - name: "Inner-heliosphere conjunction-window selector"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2408.02330"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Reviews the multi-source energetic-particle environment of the inner
    heliosphere — SEPs accelerated at the Sun, ESPs at CME-driven shocks,
    anomalous cosmic rays from interstellar pickup ions, and particles
    accelerated at planetary bow shocks — as observed by Solar Orbiter EPD
    and Parker Solar Probe ISʘIS together with cross-reference at 1 au
    (ACE/STEREO). Restricted to the inner heliosphere and to the mission
    epochs the authors cover (TODO verify cutoff).
  out_of_scope:
    - "Do not extrapolate to the outer-heliosphere ACR origin debate; that requires Voyager/IBEX context."
    - "Do not use this review for new numerical fluences or spectral indices; defer to primary references."
    - "Do not infer mechanism from background-level intensities alone."
    - "Do not apply the multi-source decomposition to single-instrument data without cross-mission cross-check."

failure_modes:
  - "Confusing ACR composition (singly-ionized heavies) with reaccelerated impulsive ions — composition signatures differ."
  - "Treating quiet-time backgrounds as instrument noise — they are physical and include ACRs/Jovian electrons (TODO verify Jovian electrons in the paper)."
  - "Mismatching SO/EPD and PSP/ISʘIS energy channels when comparing conjunctions — recalibrate to a common energy grid."
  - "Picking conjunctions on heliocentric distance alone — magnetic-connectivity (Parker spiral + sector polarity) is required."

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-cuesta-2024-kappa-distributions-energetic-protons"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2408.02330"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, esp, acr, multi-mission, review]
---

# Inner-Heliosphere SEP Environment from SO + PSP — paper-skill

> Compiled from Wimmer-Schweingruber, R. F.; Rodriguez-Pacheco, J.; Ho,
> G. C.; Cohen, C. M.; Mason, G. M.; and the Solar Orbiter EPD team (2024),
> "SEP environment in the inner heliosphere from Solar Orbiter and Parker
> Solar Probe," arXiv:2408.02330.
> **Quality tier**: `stub`.

This review skill is the navigation-layer entry for joint SO + PSP
energetic-particle analyses. It compiles the menu of energetic-particle
populations (SEP, ESP, ACR, bow-shock-accelerated) into a routing table
used by other paper-skills in this batch.

---

## Layer map (harness-agnostic)

This skill is structured for any general-purpose agent runtime (e.g., Claude
Code, LingTai, Codex, Cursor, OpenAI Assistants) — those names are
*adapter examples*, not requirements. Sections compile into four layers:

1. **Scientific invariant layer** — claims, equations, methods, data
   assumptions, failure modes, and figure / numerical targets. Sections
   2, 3 (algorithm bodies), 5 (validation target), 6 (failure modes),
   7 (claim boundary). Mission-, instrument-, and physics-level
   statements; runtime-neutral.
2. **Executable protocol layer (abstract capability contracts)** —
   Section 3 (procedures) and Section 4 (tool contracts) describe what
   *capabilities* are needed (e.g., "load PSP/ISʘIS L2 ion spectra",
   "compute power-law fit") without binding to any particular API,
   MCP, or harness tool. Any runtime that can fulfil the named
   capability satisfies the contract.
3. **Adapter / runtime notes (optional examples)** — wherever a named
   tool, MCP, repo, or library appears (e.g., `cdf-tools`, `pyspedas`,
   `Athena++`), it is one *example adapter* satisfying the abstract
   contract above; substitution by any equivalent is allowed.
4. **Research-generation affordances** — Section 10 lists the gaps,
   tensions, new hypotheses, and follow-up experiments this paper
   enables when composed with prior skills in the corpus. This is what
   makes the paper a *generative* node in the skill graph, not just a
   reference.

A consuming agent MUST honour the scientific invariants (layer 1) and the
abstract capability contracts (layer 2); adapter mentions (layer 3) are
substitutable; affordances (layer 4) are seeds for new work, not claims.

---

## 1. Trigger

A future agent should reach for this skill when:

- Asking what energetic-particle populations contribute to a quiet-time
  inner-heliosphere background.
- Designing a SO + PSP joint observation pipeline and needing to pick which
  energy channels overlap.
- Identifying the appropriate parent paper-skill family (SEP vs ESP vs ACR
  vs planetary-bow-shock).

Do NOT use this skill when:

- The question is outer-heliosphere ACR origin — different paper-skill
  family.
- A specific event-class numerical claim is needed — defer to primary papers.

## 2. Paper claim → verifiable task

**Claim (narrow form).** The inner-heliospheric energetic-particle
environment is a superposition of SEPs (accelerated near the Sun), ESPs
(accelerated at CME-driven shocks), anomalous cosmic rays (interstellar
pickup ions accelerated in the heliosphere), and planetary-bow-shock-
accelerated particles. Joint SO/EPD + PSP/ISʘIS observations resolve these
populations and their acceleration/transport at multiple locations in the
inner heliosphere.

**Verifiable task.** A reproduction succeeds when an agent, given a quiet-
time or event window covered by SO + PSP, decomposes the energetic-particle
background into the four named source classes and labels each with the
appropriate paper-skill family.

## 3. Methods / equations → executable workflow

### Multi-source energetic-particle background decomposition

- Procedure:
  1. Pull SO/EPD (SIS, HET, EPT, STEP) and PSP/ISʘIS (EPI-Lo, EPI-Hi)
     fluxes for the window of interest.
  2. Tabulate composition + energy spectrum per instrument.
  3. Identify SEP signatures (impulsive vs gradual; route to Reames
     skills).
  4. Identify ESP signatures (shock-localized intensity spikes).
  5. Identify ACR signatures (singly-ionized heavy composition, energy
     range).
  6. Identify planetary-bow-shock signatures (Earth/Mars magnetic
     connectivity).

### SEP vs ESP vs ACR vs bow-shock-particle classifier

- Procedure:
  1. For each detected population, check composition, energy range, and
     spatial localization.
  2. Emit a class label + confidence.

### Inner-heliosphere conjunction-window selector

- Procedure:
  1. For a given epoch, compute SO and PSP heliocentric positions and
     Parker-spiral footpoints.
  2. Define a conjunction window (magnetic connectivity tolerance in
     HGI longitude — TODO verify the threshold authors recommend).
  3. Output candidate conjunction intervals.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| SO/EPD SIS, HET, EPT, STEP | L2/L3 | instrument-native | SO 2020-present | SOAR | general-purpose: WebFetch + SOAR API |
| PSP/ISʘIS EPI-Lo, EPI-Hi | L2/L3 | instrument-native | PSP encounters | CDAWeb / PSP SOC | general-purpose: WebFetch + cdflib |
| ACE / STEREO energetic-particle suites | L2 | instrument-native | 1 au cross-reference | CDAWeb | general-purpose |

## 5. Validation target → benchmark artifact

Not benchmarked yet — review-only at stub tier.

## 6. Failure modes → skill memory

- ACRs misidentified as SEPs — composition (singly-ionized heavies) is the
  key discriminator.
- Quiet-time backgrounds dismissed as noise — they are physical.
- Cross-mission energy-channel mismatch — re-grid before comparison.
- Conjunction defined by distance only — must include magnetic connectivity.

## 7. Claim boundary

**In scope.** Inner-heliospheric energetic-particle environment as resolved
by SO + PSP + ACE/STEREO during the mission epochs covered.

**Out of scope — do NOT generalize beyond:**

- Outer-heliosphere ACR or Voyager-era contexts.
- Specific event numerical claims (use primary papers).
- New mechanism proposals — this is a review.

If a downstream task needs a primary observational claim, refuse and route
to the appropriate primary paper-skill.

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2408.02330
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: SO SOAR + PSP CDAWeb — see tool contracts

## 9. Skill graph → depends_on

- `[[paper-reames-2026-physics-of-seps]]` — SEP-mechanism-classification
  routing.
- `[[paper-cuesta-2024-kappa-distributions-energetic-protons]]` — specific
  PSP/ISʘIS kappa-distribution study used as a primary worked example.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (unified environment table).** The "SEP + ESP + ACR +
  planetary-bow-shock" decomposition is presented narratively; no
  unified table per spacecraft and per encounter has been derived
  from this paper's framing. Compose with the data-loader primary
  skills + [[paper-cuesta-2024-kappa-distributions-energetic-
  protons]] (kappa thermodynamics) to write one.
- **Tension (planetary-bow-shock contamination).** During Mercury /
  Venus / Earth flybys of PSP and SO, planetary-bow-shock-accelerated
  particles contaminate SEP intervals. New hypothesis: a substantial
  fraction of low-energy "SEP" events in the published lists are
  bow-shock events. Testable by cross-referencing flyby ephemerides
  with the inventory's event lists.
- **Experiment (joint-mission catalog).** Build a joint SO/EPD +
  PSP/ISʘIS event catalog from conjunctions, splitting by event
  class (SEP/ESP/ACR/bow). Composes with [[paper-walker-2026-icme-
  radial-particle-acceleration-statistics]] for the ICME-driven
  subset.
- **New hypothesis (ACR helium).** Anomalous-CR helium fraction
  should rise toward 1 au and outwards. Compose with the dedicated
  ACR-helium SO/HET paper (in `theme_energetic_particles.json` —
  not yet in this batch) to test.

## Notes

The Solar Orbiter EPD authorship list is collaboration-style ("the Solar
Orbiter EPD team"). For citation in any downstream manuscript (e.g., a
HelioSI synthesis paper — example adapter), expand using the EPD-team
author roster (TODO verify).
