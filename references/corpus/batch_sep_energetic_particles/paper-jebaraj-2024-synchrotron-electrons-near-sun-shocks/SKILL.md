---
name: paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks
description: >-
  Use when correlating relativistic-electron distributions with synchrotron
  photon emission across heliospheric traveling shocks intercepted by PSP at
  close encounters — Jebaraj+ 2024 (arXiv:2410.15933) report the first
  in-situ shock synchrotron measurements and find strong quasi-parallel
  shocks emit at higher intensities than quasi-perpendicular shocks, due to
  efficient ultra-relativistic electron acceleration.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Direct Measurements of Synchrotron-Emitting Electrons at Near-Sun Shocks"
  first_author: "Jebaraj, I. C."
  authors:
    - "Jebaraj, I. C."
    - "Agapitov, O. V."
    - "Gedalin, M."
    - "Vuorinen, L."
    - "Miceli, M."
    - "Vainio, R."
  year: 2024
  venue: "Journal — TODO verify (ApJL likely)"
  doi: null
  arxiv_id: "2410.15933"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - heliospheric-shocks
    - shock-electron-acceleration
    - synchrotron-emission
    - psp-fields
    - quasi-parallel-vs-perpendicular
  missions: [PSP]
  regime: [inner-heliosphere, kinetic]

trigger_keywords:
  - "synchrotron-emitting electrons"
  - "shock acceleration"
  - "near-Sun shock"
  - "PSP close encounter"
  - "relativistic electrons"
  - "quasi-parallel shock"
  - "quasi-perpendicular shock"
  - "shock obliquity"
  - "photon emission"
  - "PSP FIELDS"
  - "supernova remnant analog"
  - "electron injection problem"

data_products:
  - instrument: "PSP/FIELDS (DC + AC E and B)"
    level: "L2/L3"
    cadence: "high cadence (waveform when available)"
    interval: "near-Sun shock crossings during PSP close encounters (TODO verify event list)"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/ISʘIS EPI-Hi + electron channels"
    level: "L2"
    cadence: "instrument-native"
    interval: "near-Sun shock crossings"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/SWEAP"
    level: "L3"
    cadence: "instrument-native"
    interval: "near-Sun shock crossings"
    archive: "NASA CDAWeb / PSP SOC"

algorithms:
  - name: "Shock crossing identification + obliquity classification"
    equation_refs: []
    external_implementations: []
  - name: "Relativistic-electron spectrum extraction"
    equation_refs: []
    external_implementations: []
  - name: "Synchrotron photon-emission diagnostic"
    equation_refs: []
    external_implementations: []
  - name: "Quasi-parallel vs quasi-perpendicular intensity contrast"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2410.15933"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    First in-situ direct measurements of synchrotron-emitting electrons at
    heliospheric traveling shocks intercepted by PSP during close encounters,
    showing that strong quasi-parallel shocks emit at substantially higher
    intensities than quasi-perpendicular shocks because they accelerate
    ultra-relativistic electrons more efficiently. The claim is bounded to
    the near-Sun heliospheric-traveling-shock regime sampled by PSP and to
    the obliquity contrast at strong shocks.
  out_of_scope:
    - "Do not extrapolate the quasi-parallel ↔ stronger-emission ordering to all shock strengths — the paper analyzes strong shocks."
    - "Do not extend the result to standing planetary bow shocks or to corotating-interaction-region (CIR) shocks at 1 au."
    - "Do not equate near-Sun shock synchrotron with supernova remnant synchrotron numerically — the analogy is qualitative."
    - "Do not infer electron injection mechanism from intensity alone; pitch-angle/anisotropy diagnostics are required."

failure_modes:
  - "Misclassifying shock obliquity due to noisy upstream B — average over a stable upstream window."
  - "Confusing ambient relativistic electrons with shock-accelerated electrons; check timing and spatial localization."
  - "Treating PSP near-Sun shocks as a uniformly strong-shock sample — strength varies."
  - "Naively converting PSP photon flux to a remote-observer expectation without geometry / line-of-sight corrections."
  - "Conflating Type-II radio (plasma emission) with synchrotron emission — they are different processes."

depends_on:
  - "paper-trotta-2025-ip-shock-variability-multi-spacecraft"
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2410.15933"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, shock, electrons, psp]
---

# Synchrotron-Emitting Electrons at Near-Sun Shocks — paper-skill

> Compiled from Jebaraj, I. C.; Agapitov, O. V.; Gedalin, M.; Vuorinen, L.;
> Miceli, M.; Vainio, R. (2024), "Direct Measurements of Synchrotron-
> Emitting Electrons at Near-Sun Shocks," arXiv:2410.15933.
> **Quality tier**: `stub`.

This skill compiles the first in-situ heliospheric-shock synchrotron
measurement. It is the canonical anchor for any reasoning step that uses
shock-driven electron synchrotron as a proxy for relativistic-electron
acceleration efficiency.

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

- A PSP close-encounter shock crossing shows enhanced relativistic-electron
  flux + an in-situ photon-emission signature — is the electron-radiation
  link consistent with Jebaraj+ 2024?
- Comparing quasi-parallel vs quasi-perpendicular shock acceleration of
  electrons at near-Sun shocks.
- Drawing an analogy to supernova-remnant electron acceleration — what is
  the heliospheric in-situ counterpart?
- Designing a synchrotron-emission diagnostic for a heliospheric shock
  modeling pipeline.

Do NOT use this skill when:

- The shock is at a planetary bow or magnetospheric scale — different
  geometry.
- The scientific question is about *ion* acceleration only — different
  paper-skill family.

## 2. Paper claim → verifiable task

**Claim (narrow form).** PSP at close encounters intercepts heliospheric
traveling shocks and directly measures both the relativistic-electron
distribution and synchrotron photon emission across the shock. Strong
quasi-parallel shocks emit at significantly higher intensities than strong
quasi-perpendicular shocks because they accelerate ultra-relativistic
electrons more efficiently.

**Verifiable task.** A reproduction succeeds when an agent, for each Jebaraj+
2024 shock event (TODO verify event list), emits `{shock_obliquity,
relativistic_e_spectrum, synchrotron_intensity, qpara_qperp_ordering}` and
the ordering (qpara > qperp at strong shocks) is reproduced.

## 3. Methods / equations → executable workflow

### Shock crossing identification + obliquity classification

- Procedure:
  1. Load PSP/FIELDS MAG + SWEAP at high cadence around suspected shock
     times during PSP close encounters.
  2. Apply Rankine-Hugoniot to compute Mach number; classify strength.
  3. Compute the shock-normal direction via minimum-variance / multi-method
     and compute θ_Bn (angle between upstream B and shock normal).
  4. Classify as quasi-parallel (θ_Bn ≲ 45°) vs quasi-perpendicular.

### Relativistic-electron spectrum extraction

- Procedure:
  1. Load PSP/ISʘIS electron channels (or appropriate FIELDS-derived
     diagnostic; TODO verify which channels Jebaraj+ use).
  2. Extract differential intensity vs. energy / Lorentz factor across the
     shock window.
  3. Fit a power-law in the relativistic range.

### Synchrotron photon-emission diagnostic

- Procedure:
  1. Use the in-situ photon-emission diagnostic the paper introduces (TODO
     verify the exact instrument / waveform / FFT processing).
  2. Identify intensity bursts coincident with the shock crossing.
  3. Cross-correlate photon-burst timing with the relativistic-electron
     enhancement.

### Quasi-parallel vs quasi-perpendicular intensity contrast

- Procedure:
  1. Bin shock crossings by obliquity (qpara, qperp) and Mach number.
  2. Compute mean synchrotron intensity per bin.
  3. Verify qpara > qperp at strong shocks; report effect size.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/FIELDS (DC + AC E and B) | L2/L3 | high cadence / waveform | shock crossings | CDAWeb / PSP SOC | general-purpose: WebFetch + cdflib |
| PSP/ISʘIS EPI-Hi + electron channels | L2 | instrument-native | shock crossings | CDAWeb / PSP SOC | general-purpose |
| PSP/SWEAP | L3 | instrument-native | shock crossings | CDAWeb / PSP SOC | general-purpose |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires the exact event list
+ photon-diagnostic procedure (TODO verify from full text) and reproducing
Figure (TODO verify) showing qpara > qperp intensity contrast.

## 6. Failure modes → skill memory

- Obliquity classification noise — use stable upstream windows of ≥ 5
  ion gyroperiods.
- Ambient vs shock-accelerated relativistic electrons — check timing.
- Misattributed photon-emission process — synchrotron vs plasma emission.
- Bias by shock strength — restrict to strong-shock subset for qpara/qperp
  contrast.
- Anisotropy assumed isotropic when not — pitch-angle distribution must be
  recorded.

## 7. Claim boundary

**In scope.** Near-Sun PSP-traveling-shock synchrotron-electron in-situ
measurements; quasi-parallel ↔ stronger emission at strong shocks.

**Out of scope — do NOT generalize beyond:**

- 1-au or outer-heliosphere shocks.
- Standing bow shocks.
- Numerical match to supernova-remnant synchrotron — qualitative only.
- Inferring injection physics from intensity alone.

If a downstream task wants a CIR / 1-au shock electron acceleration claim,
refuse and route to a 1-au-specific skill (TODO).

## 8. Links

- DOI: n/a (in-press at writing) — TODO add at promotion
- arXiv: https://arxiv.org/abs/2410.15933
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: PSP archive — see tool contracts

## 9. Skill graph → depends_on

- `[[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]` — sister
  multi-spacecraft shock-acceleration variability paper.
- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` —
  inner-heliosphere SEP-environment review context.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (mechanism uniqueness).** Quasi-parallel ≫ quasi-perpendicular
  synchrotron-electron emission is the headline; the alternative
  (instrumental selection effect) has not been ruled out across a
  full near-Sun shock catalog. Compose with [[paper-trotta-2025-ip-
  shock-variability-multi-spacecraft]] and [[paper-kouloumvakos-2026-
  iva-shock-properties]] to write a θ_Bn-dependent ultra-relativistic
  electron diagnostic across multi-spacecraft shocks.
- **Tension (theory expectation).** Classical DSA theory predicts the
  *opposite* obliquity preference for the highest-energy electrons.
  New hypothesis: SDA or stochastic-Fermi acceleration at the quasi-
  parallel shock outpaces DSA at quasi-perpendicular shocks at near-
  Sun parameters. Testable with PIC re-runs at PSP-relevant
  parameters.
- **Experiment (population audit).** Cross-check whether the
  identified ultra-relativistic electrons co-arrive with type-II
  bursts ([[paper-duan-2026-...]] — not in this batch; add later)
  or with the trapped electron populations in [[paper-han-2026-
  electrons-cross-heliospheric-current-sheet]] — not yet in this
  batch.
- **New hypothesis (heliosheath analogy).** If quasi-parallel shocks
  dominate ultra-relativistic-electron acceleration near the Sun, the
  same may hold at termination/bow shocks. A cross-domain follow-up.

## Notes

The paper draws an explicit analogy to supernova-remnant shock electron
acceleration. The analogy is qualitative; do not import SNR numerical
values directly into a heliospheric pipeline.
