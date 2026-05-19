---
name: paper-reames-2026-physics-of-seps
description: >-
  Use when deciding whether a candidate SEP event is impulsive (3He/heavy-ion-rich,
  reconnection-jet origin) versus gradual (CME-shock origin), or when interpreting
  streaming-limit-flattened low-energy spectra, downstream "reservoir" plateaus,
  and FIP-biased composition — Reames 2026 (arXiv preprint review) compiles the
  two-mechanism picture and its canonical diagnostics.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "The Physics of Solar Energetic Particles"
  first_author: "Reames, D. V."
  authors:
    - "Reames, D. V."
  year: 2026
  venue: "arXiv preprint"
  doi: null
  arxiv_id: "2602.18617"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - heliospheric-shocks
    - composition-FIP
    - reservoirs
    - streaming-limit
  missions: [Wind, ACE, STEREO, PSP, Solar Orbiter]
  regime: [inner-heliosphere, 1au]

trigger_keywords:
  - "solar energetic particles"
  - "SEP"
  - "impulsive event"
  - "gradual event"
  - "3He-rich"
  - "heavy-ion enhancement"
  - "CME-driven shock"
  - "streaming limit"
  - "reservoir"
  - "type III burst"
  - "Alfven wave amplification"
  - "FIP bias"
  - "seed population"
  - "reacceleration"
  - "shock acceleration"

data_products: []

algorithms:
  - name: "Impulsive-vs-gradual classification by composition"
    equation_refs: []
    external_implementations: []
  - name: "Streaming-limit spectrum interpretation"
    equation_refs: []
    external_implementations: []
  - name: "Reservoir adiabatic-volume scaling"
    equation_refs: []
    external_implementations: []
  - name: "FIP-bias diagnosis of coronal seed origin"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.18617"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Reviews — does not produce new data — the two canonical SEP production
    mechanisms (impulsive jets/flares via magnetic reconnection on open field;
    gradual events via fast/wide CME-driven shocks accelerating ambient and
    residual-impulsive seed ions), together with their observable diagnostics
    (3He enrichment, increasingly heavy-ion enhancement on open lines vs.
    streaming-limit-flattened spectra and post-shock reservoirs in gradual
    events). Composition-as-corona-sample claims are bounded to elements whose
    SEP abundance the literature has shown to obey a FIP-dependent
    SEP/photosphere ratio.
  out_of_scope:
    - "Do not use this skill to assign mechanism (impulsive vs. gradual) from intensity time-history alone — composition + radio + magnetic-connectivity context is required."
    - "Do not extrapolate the reservoir adiabatic scaling beyond the volume-filling regime behind a single fast CME-driven shock."
    - "Do not treat the FIP-bias picture as a temperature thermometer; it constrains the seed population's coronal origin, not its instantaneous temperature."
    - "Do not promote this review to a primary observational source — cite the underlying primary papers when a numerical value is needed."

failure_modes:
  - "Mistaking a 3He-poor event for impulsive because radio type-III is present — type-III alone does not establish impulsive composition."
  - "Reading streaming-limit-flattened low-energy spectra as a source spectrum — they are a transport-modified signature near the shock."
  - "Treating downstream-reservoir intensities as new acceleration — the reservoir is shed by an expanding shock and decays adiabatically."
  - "Confusing residual-impulsive seed ions with a fresh impulsive event; the heavy-ion enhancement is a reacceleration fingerprint."
  - "Assuming FIP-biased SEP composition matches the slow solar wind 1:1 — the FIP factor magnitudes differ; cite a primary paper if you need numbers."

depends_on:
  - "paper-desai-2024-hcs-reconnection-400kev-protons"
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2602.18617"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, review, canonical]
---

# The Physics of Solar Energetic Particles — paper-skill

> Compiled from Reames, D. V. (2026), "The Physics of Solar Energetic Particles,"
> arXiv:2602.18617.
> **Quality tier**: `stub` — review skill; serves as a canonical anchor for
> impulsive-vs-gradual decisions but should not be promoted to `executable`
> without grounding to a primary observational paper.

This file is the *agent-native compiled form* of Reames's 2026 review. It
compiles the field's two-mechanism narrative into decision support: when an
agent sees an SEP event in PSP / Solar Orbiter / STEREO / ACE / Wind data, this
skill is the routing table that picks the diagnostic family and downstream
primary-source skill to load.

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

- It must classify a candidate SEP event as **impulsive** vs. **gradual**, or
  decide what diagnostics to compute.
- It needs to interpret a **flattened low-energy spectrum upstream of a CME-driven shock** (streaming limit) or a **plateau intensity downstream** (reservoir).
- It is asked whether **3He-rich / heavy-ion-enhanced** composition implies a
  reconnection-jet origin or a reaccelerated-residual-impulsive seed at a
  later shock.
- It needs a one-stop entry point before drilling into a specific event-class
  paper-skill (Desai 2024, Cuesta 2024, Kouloumvakos 2026, ...).

Do NOT use this skill when:

- The task is to derive a new numerical exponent / threshold — cite the
  primary paper instead.
- The task is non-SEP energetic-particle physics (ACRs, galactic CRs,
  magnetospheric particles).

## 2. Paper claim → verifiable task

**Claim (narrow form).** Two physical mechanisms dominate SEP production:
(a) magnetic reconnection in solar jets on *open* field lines yields impulsive
events with 3He-rich and heavy-ion-enhanced composition and outward
type-III-driving electron streams; (b) fast/wide CME-driven shocks accelerate
ambient + residual-impulsive seed ions into gradual events whose upstream
low-energy spectra flatten at a streaming limit and whose downstream forms a
volume-expanding reservoir that decays adiabatically.

**Verifiable task.** A reproduction succeeds when an agent, given a candidate
event, emits a decision triple `{mechanism ∈ {impulsive, gradual, mixed},
diagnostic_set, primary_source_skill}` and the diagnostic set names the
canonical signatures Reames lists (3He/4He, Fe/O, type-III presence,
streaming-limit, reservoir shape, FIP ordering).

## 3. Methods / equations → executable workflow

### Impulsive-vs-gradual classification by composition

- Paper reference: Reames 2026 §"Impulsive events" and §"Gradual events".
- Procedure:
  1. Compute event-integrated **3He/4He** and **Fe/O** abundance ratios from
     in-situ ion composition data (STEREO/SIT, ACE/ULEIS, PSP/ISʘIS,
     SO/SIS).
  2. Compute Fe/C, Ne/Mg, and selected heavy/light ratios for "increasingly
     heavy" enhancement check.
  3. Cross-check with associated radio bursts (type-III for open-line jets;
     type-II for CME-driven shocks).
  4. Apply the classification table: high 3He/4He + heavy-ion enhancement +
     type-III ⇒ impulsive; large CME + type-II + streaming-limit-flattened
     low-energy spectrum + extended angular reach ⇒ gradual.
  5. Mixed signatures route to "residual-impulsive seed at later shock"
     branch — flag for further analysis.

### Streaming-limit spectrum interpretation

- Paper reference: Reames 2026 §"Streaming limit"; canonical Reames & Ng
  primary references (TODO verify exact list at promotion).
- Procedure:
  1. Identify the upstream low-energy proton spectrum near a fast CME-driven
     shock.
  2. If the spectrum is flatter than the source spectrum and saturates at
     a roughly time-independent intensity at low energies, attribute the
     flattening to Alfvén-wave-amplification-driven self-confinement rather
     than to a source-spectral feature.
  3. Report streaming-limited intensity and the energy at which the
     flattening sets in.

### Reservoir adiabatic-volume scaling

- Paper reference: Reames 2026 §"Reservoir".
- Procedure:
  1. After the shock has passed the observer, identify the spatially uniform
     "reservoir" of trapped SEPs downstream.
  2. Track intensity decay; check consistency with adiabatic loss as the
     reservoir volume expands with the CME.
  3. Use the reservoir as a candidate seed population for any subsequent
     multi-shock event.

### FIP-bias diagnosis of coronal seed origin

- Paper reference: Reames 2026 §"SEP abundances as coronal samples".
- Procedure:
  1. Compute element abundance ratios relative to photospheric values.
  2. Order by first ionization potential (FIP).
  3. Verify the SEP/photosphere ratio drops monotonically with FIP — this is
     the canonical coronal-seed signature.

## 4. Data / instruments → tool contracts

This is a review paper. It depends conceptually on the data products used by
the primary papers it cites; it does not introduce its own measurement
pipeline. The tool contracts below are the recurring composition/radio/MAG
products that a reproducing agent would load, abstractly:

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| ACE/ULEIS, STEREO/SIT | L2 | event-integrated | per SEP event | NASA CDAWeb / SPDF | general-purpose: WebFetch + cdflib |
| PSP/ISʘIS EPI-Lo, EPI-Hi | L2/L3 | event-integrated | PSP perihelia | PSP SOC / CDAWeb | general-purpose harness + ISʘIS Python tools |
| SO/EPD SIS, HET, EPT | L2 | event-integrated | per SEP event | SOAR | general-purpose harness |
| ground / space radio (WIND/WAVES, STEREO/WAVES, PSP/RFS) | L2/L3 | sweep | event window | CDAWeb / SOAR | general-purpose harness |

**Important:** no named tool / MCP is *required*; any general-purpose agent runtime that can `read`, `fetch`, and run Python on cached files satisfies these contracts.

## 5. Validation target → benchmark artifact

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires choosing one of the canonical events Reames cites (TODO: identify the
specific impulsive and gradual events Reames uses as worked examples) and
running the classification workflow end-to-end against published composition
ratios.

## 6. Failure modes → skill memory

- 3He enhancement without type-III is suspect — confirm radio context.
- Streaming-limit interpretation requires upstream proximity to a shock and
  a sustained source; don't apply it to decayed events.
- Reservoir scaling assumes a coherent shock-bounded volume; multi-CME
  interaction breaks the assumption.
- FIP-bias diagnosis is statistical across many elements; do not infer
  coronal origin from a single ratio.
- Residual-impulsive seed signatures (heavy-ion-enhanced gradual event) can
  be mistaken for a true impulsive event — check temporal association with
  prior jets and the host CME.

## 7. Claim boundary

**In scope.** Reames 2026 as a *decision-support review skill* for sorting an
SEP event into impulsive/gradual/mixed, with the diagnostic-signature menu
the paper itemizes.

**Out of scope — do NOT generalize beyond:**

- New numerical values (spectral indices, streaming-limit intensities, FIP
  factors) — go to a primary observational source.
- Non-solar contexts (stellar particle events) — Reames notes the
  extrapolation but does not derive it here.
- Anomalous cosmic rays / galactic cosmic rays — handled by separate skills.

If a downstream task asks for a numerical claim, refuse the review-only
answer and route to the appropriate primary-source paper-skill.

## 8. Links

- DOI: n/a (preprint at posting)
- arXiv: https://arxiv.org/abs/2602.18617
- ADS: n/a — TODO add at promotion
- Code: n/a — review paper
- Data: n/a — review paper

## 9. Skill graph → depends_on

This paper-skill is the **routing hub** of the SEP/energetic-particle batch.
It expects the following sibling paper-skills:

- `[[paper-desai-2024-hcs-reconnection-400kev-protons]]` — primary
  observational source for reconnection-driven acceleration in the near-Sun
  HCS.
- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` —
  primary multi-mission SEP-environment review that anchors numerical
  references.
- `[[paper-cuesta-2024-kappa-distributions-energetic-protons]]` — primary
  observation extending the picture into kappa-distributed proton tails.
- `[[paper-kouloumvakos-2026-iva-shock-properties]]` and
  `[[paper-xu-2026-psp-iva-sep-events]]` — IVA branch refining the
  shock-acceleration story.
- `[[paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks]]` —
  relativistic-electron branch.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

This review is a *routing hub*; its generative value is what composes
*from it*:

- **Gap (decision automation).** No paper-skill in this batch yet
  emits a single-call `classify_event(event) -> {impulsive | gradual |
  mixed, confidence, diagnostic_witnesses}`. Compose Reames-2026 with
  the composition primary skills (e.g., [[paper-cuesta-2024-kappa-
  distributions-energetic-protons]]), the IVA branch ([[paper-xu-2026-
  psp-iva-sep-events]] + [[paper-kouloumvakos-2026-iva-shock-
  properties]]), and the HCS branch ([[paper-desai-2024-hcs-
  reconnection-400kev-protons]]) to write that synthesis skill.
- **Tension (mixed-signature events).** The classification table
  treats "residual-impulsive seed at a later gradual shock" as a sub-
  case; the empirical frequency at PSP perihelion is unknown. New
  hypothesis: at <0.3 au, the residual-impulsive fraction is higher
  than at 1 au because the reservoir has not adiabatically decayed.
  Testable using the PSP/ISʘIS catalog versus the Reames classical
  catalogs.
- **Experiment (review-vs-primary regression).** Take each numerical
  threshold Reames quotes and regress against the underlying primary
  paper-skills in the batch. Discrepancies indicate either a Reames
  shortcut or a primary-skill TODO-verify failure.
- **New hypothesis (PSP perihelion FIP scan).** FIP-ratio statistics
  on PSP/ISʘIS events at <0.2 au may differ from 1 au because the
  source-region sampling differs. Compose with the PFSS source-
  mapping batch (`batch_pfss_source_mapping`) to test.

## Notes

Reames's review consolidates ~40 years of his and the community's work. Many
numerical claims in §3 and §4 of this skill *originate* in earlier Reames
papers, not in the 2026 review itself. Treat the 2026 review as a navigation
map, not a citation of last resort.
