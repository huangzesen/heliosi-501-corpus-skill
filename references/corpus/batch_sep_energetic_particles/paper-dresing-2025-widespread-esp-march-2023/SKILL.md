---
name: paper-dresing-2025-widespread-esp-march-2023
description: >-
  Use when interpreting a *circumsolar* energetic-storm-particle event with
  in-situ shock crossings at six well-separated heliospheric observers —
  Dresing+ 2025 (arXiv:2502.06332) analyze the 13 March 2023 widespread
  SEP/ESP event using PSP, SO, BepiColombo, STEREO-A, near-Earth and MAVEN,
  and run MHD with multiple CME injections to test (a) single circumsolar
  blast-wave-like shock vs (b) multi-CME combined shocks; the blast-wave
  scenario performs slightly better on the global ESP signature.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "On the reason for the widespread energetic storm particle event of 13 March 2023"
  first_author: "Dresing, N."
  authors:
    - "Dresing, N."
    - "Jebaraj, I. C."
    - "Wijsen, N."
    - "Palmerio, E."
    - "Rodríguez-García, L."
    - "Palmroos, C."
  year: 2025
  venue: "Journal — TODO verify (likely A&A)"
  doi: null
  arxiv_id: "2502.06332"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - widespread-sep
    - energetic-storm-particles
    - circumsolar-shock
    - multi-cme
    - mhd-modeling
    - multi-spacecraft
  missions: [PSP, "Solar Orbiter", STEREO, MAVEN, MESSENGER, ACE, Wind]
  regime: [inner-heliosphere, 1au]

trigger_keywords:
  - "widespread SEP event"
  - "13 March 2023"
  - "circumsolar shock"
  - "ESP event"
  - "blast wave"
  - "multi-CME"
  - "BepiColombo"
  - "MAVEN"
  - "global heliospheric shock"
  - "MHD CME injection"
  - "pre-event CMEs"
  - "magnetic connectivity"

data_products:
  - instrument: "PSP/ISʘIS + FIELDS + SWEAP"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "2023-03-13 SEP/ESP event window"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "SO/EPD + MAG + SWA"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "2023-03-13 event"
    archive: "SOAR"
  - instrument: "BepiColombo/BERM + magnetic field"
    level: "L2"
    cadence: "instrument-native"
    interval: "2023-03-13 event"
    archive: "ESA BepiColombo archive"
  - instrument: "STEREO-A/IMPACT + PLASTIC + MAG"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "2023-03-13 event"
    archive: "STEREO archive / CDAWeb"
  - instrument: "Near-Earth (ACE, Wind, GOES)"
    level: "L2"
    cadence: "instrument-native"
    interval: "2023-03-13 event"
    archive: "CDAWeb"
  - instrument: "MAVEN/SEP + MAG"
    level: "L2"
    cadence: "instrument-native"
    interval: "2023-03-13 event"
    archive: "PDS"
  - instrument: "Coronagraph imagery (LASCO + STEREO/SECCHI + SO/Metis)"
    level: "L1"
    cadence: "instrument-native"
    interval: "associated CMEs"
    archive: "various"
  - instrument: "MHD solar-wind + CME injection model"
    level: "derived"
    cadence: "per scenario"
    interval: "event window"
    archive: "model-team archive (TODO verify)"

algorithms:
  - name: "Multi-spacecraft shock + ESP-onset cataloging"
    equation_refs: []
    external_implementations: []
  - name: "Magnetic-connectivity estimation per observer"
    equation_refs: []
    external_implementations: []
  - name: "MHD CME-injection scenarios (single blast wave vs multi-CME)"
    equation_refs: []
    external_implementations: []
  - name: "Scenario comparison via simulation-vs-observation fit"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2502.06332"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Analyzes the 13 March 2023 widespread SEP/ESP event observed in situ
    at six well-separated heliospheric observers (PSP, SO, BepiColombo,
    STEREO-A, near-Earth, MAVEN). Documents shock crossings and ESP
    enhancements at all inner-heliospheric observers, consistent with a
    circumsolar shock extending all around the Sun. MHD with two scenarios
    (single blast-wave shock vs multi-CME combined shocks) — both fit the
    global ESP signature, with the blast-wave scenario performing slightly
    better.
  out_of_scope:
    - "Do not claim the blast-wave scenario as a uniqueness result — both scenarios are consistent within model uncertainties."
    - "Do not extrapolate the circumsolar-shock interpretation to other widespread events without re-running both scenarios."
    - "Do not assert mechanism transferability without running the same MHD model on the candidate event."
    - "Do not infer single-source interpretations from multi-observer ESP onset alone — pre-event CMEs are a critical confounder."

failure_modes:
  - "Pre-event CMEs perturb the solar-wind background and the MHD initial state; document the pre-event injection list."
  - "MAVEN energetic-particle calibration vs near-Earth instruments is the principal cross-mission systematic."
  - "BepiColombo cruise-phase data has unique geometry/calibration constraints — document."
  - "Magnetic connectivity assumed from ballistic + Parker spiral; in this event SIRs/CMEs are present — connectivity may be distorted."
  - "Single-blast-wave scenario fit only 'slightly better' — do not promote that to a strong preference without statistical testing."

depends_on:
  - "paper-walker-2026-icme-radial-particle-acceleration-statistics"
  - "paper-kouloumvakos-2026-iva-shock-properties"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2502.06332"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, esp, widespread, multi-spacecraft, mhd]
---

# Widespread ESP Event of 13 March 2023 — paper-skill

> Compiled from Dresing, N.; Jebaraj, I. C.; Wijsen, N.; Palmerio, E.;
> Rodríguez-García, L.; Palmroos, C. (2025), "On the reason for the
> widespread energetic storm particle event of 13 March 2023,"
> arXiv:2502.06332.
> **Quality tier**: `stub`.

This skill compiles the 13 March 2023 widespread SEP/ESP analysis into
agent-callable form, including the MHD scenario comparison. It is the
canonical anchor for circumsolar-shock reasoning during the May-2024-era
solar maximum.

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

- Interpreting a widespread SEP/ESP event where shocks are seen at six
  or more separated observers.
- Choosing between a single-blast-wave-shock interpretation and a
  multi-CME-combined-shock interpretation for a circumsolar event.
- Testing magnetic connectivity from PSP / SO / BepiColombo / MAVEN /
  STEREO-A / near-Earth to a flare site on the Sun's far side.

Do NOT use this skill when:

- The event is single-vantage — apply a single-spacecraft method.
- The event is not widespread — different mechanisms dominate.

## 2. Paper claim → verifiable task

**Claim (narrow form).** The 13 March 2023 event produced ESP signatures
at six well-separated heliospheric observers (PSP, SO, BepiColombo,
STEREO-A, near-Earth, MAVEN), with in-situ shock crossings at all
inner-heliospheric observers. MHD simulations with (a) a single
circumsolar blast-wave-like shock and (b) multi-CME combined shocks both
fit the global ESP signature; the blast-wave scenario performs slightly
better.

**Verifiable task.** A reproduction succeeds when an agent, for the
2023-03-13 event window, (a) catalogs the shock + ESP onsets at all six
observers within ±15 min (TODO_verify — provisional until the
paper-side tolerance is cited to a specific line or table of Dresing+
2025; see issue #39), (b) runs both MHD scenarios (TODO verify code),
and (c) reproduces the qualitative ordering (blast-wave ≳ multi-CME)
within the paper's stated tolerance.

## 3. Methods / equations → executable workflow

### Multi-spacecraft shock + ESP-onset cataloging

- Procedure:
  1. For each of six observers, identify the shock crossing and ESP
     onset in the 2023-03-13 event window.
  2. Record times, observer positions, and local plasma parameters.

### Magnetic-connectivity estimation per observer

- Procedure:
  1. Use ballistic + Parker-spiral propagation to map each observer
     back to a coronal footpoint.
  2. Compare footpoint longitude to the flare location.

### MHD CME-injection scenarios (single blast wave vs multi-CME)

- Procedure:
  1. Initialize an MHD solar-wind model (TODO verify model: ENLIL?
     EUHFORIA? Predictive Science / MAS?).
  2. Scenario A: inject a single circumsolar blast-wave-like
     disturbance at the eruption time.
  3. Scenario B: inject the actual list of pre-event + simultaneous
     CMEs (TODO verify the CME list).
  4. Propagate both scenarios.

### Scenario comparison via simulation-vs-observation fit

- Procedure:
  1. Sample the simulated shock crossing time + strength at each
     observer's position.
  2. Compare to observed values.
  3. Compute a goodness-of-fit metric.
  4. Report ordering (blast-wave ≳ multi-CME slightly).

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/ISʘIS + FIELDS + SWEAP | L2/L3 | instrument-native | 2023-03-13 | CDAWeb / PSP SOC | general-purpose |
| SO/EPD + MAG + SWA | L2/L3 | instrument-native | 2023-03-13 | SOAR | general-purpose |
| BepiColombo/BERM + MAG | L2 | instrument-native | 2023-03-13 | ESA archive | general-purpose |
| STEREO-A/IMPACT + PLASTIC + MAG | L2/L3 | instrument-native | 2023-03-13 | STEREO archive / CDAWeb | general-purpose |
| Near-Earth (ACE, Wind, GOES) | L2 | instrument-native | 2023-03-13 | CDAWeb | general-purpose |
| MAVEN/SEP + MAG | L2 | instrument-native | 2023-03-13 | PDS | general-purpose |
| Coronagraph LASCO + STEREO/SECCHI + SO/Metis | L1 | instrument-native | associated CMEs | various | general-purpose |
| MHD solar-wind + CME injection | derived | per scenario | event window | model-team | TODO verify access |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires the exact MHD
model identity, CME-injection list (TODO verify), and observer-side
catalog (TODO verify times). The target is reproducing the global ESP
signature under both scenarios within the paper's stated tolerance.

## 6. Failure modes → skill memory

- Pre-event CMEs perturb the background; document them.
- MAVEN energetic-particle calibration — cross-mission systematic.
- BepiColombo cruise-phase geometry — document carefully.
- Magnetic connectivity assumes ballistic + Parker spiral — distorted
  in this event.
- Blast-wave preference is "slight"; do not over-claim.

## 7. Claim boundary

**In scope.** Single widespread SEP/ESP event 2023-03-13; six observers;
two MHD scenarios; blast-wave scenario performs slightly better.

**Out of scope — do NOT generalize beyond:**

- Uniqueness of the blast-wave interpretation.
- Other widespread events.
- Mechanism transfer without re-running MHD.

If a downstream task wants a statistical statement on circumsolar
shocks, refuse and route to a population-statistics skill (TODO).

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2502.06332
- ADS: n/a — TODO add at promotion
- Code: n/a — MHD model identity TODO verify
- Data: see tool contracts

## 9. Skill graph → depends_on

- `[[paper-walker-2026-icme-radial-particle-acceleration-statistics]]` —
  multipoint catalog framing complementing this single-event analysis.
- `[[paper-kouloumvakos-2026-iva-shock-properties]]` — 3D shock + MHD
  modeling shares technique.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Tension (single blast-wave vs multi-CME).** Both scenarios fit;
  blast-wave performs *slightly* better. New hypothesis: the
  scenarios are distinguishable by a multi-spacecraft *timing-
  residual* statistic the paper does not compute. Composes with
  [[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]
  (cross-correlation framework) and [[paper-kouloumvakos-2026-iva-
  shock-properties]] (3D shock reconstruction).
- **Gap (widespread-event template).** No reusable "widespread-event
  MHD-scenario template" exists across the corpus. New paper-skill:
  composes Dresing-2025 with [[paper-walker-2026-icme-radial-
  particle-acceleration-statistics]] to write the template.
- **Experiment (BepiColombo + MAVEN as out-of-ecliptic anchors).**
  The paper's six-observer geometry is unique. Apply to next
  widespread event with similar geometry; test scenario
  generalizability.
- **New hypothesis (HCS as longitudinal barrier).** If the
  widespread event crossed the HCS at multiple longitudes, the HCS
  may have been a transport modulator. Composes with the (not-yet-
  in-batch) Han-2026 electron-HCS-crossing skill.

## Notes

The 13 March 2023 event is a key test case for any "global ESP" /
"circumsolar shock" reasoning skill. The MHD CME-injection list is a
critical reproducibility artifact that this skill flags as TODO verify.
