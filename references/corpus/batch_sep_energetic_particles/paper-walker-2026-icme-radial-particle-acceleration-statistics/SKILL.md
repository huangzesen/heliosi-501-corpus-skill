---
name: paper-walker-2026-icme-radial-particle-acceleration-statistics
description: >-
  Use when assessing how ICME-driven-shock SEP/ESP acceleration efficiency
  depends on heliocentric distance — Walker+ 2026 (arXiv:2605.00163) build
  a 39-event multipoint ICME catalog (2016-2023; PSP, SO, ACE, Wind,
  STEREO-A) and find local-shock spectral-shape parameters consistent with
  *increasing* shock acceleration efficiency inside ~0.7 au and *decreasing*
  efficiency beyond.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Radial Dependency of ICME-associated Particle Acceleration Processes: Statistical Multipoint Observations from 2016-2023"
  first_author: "Walker, M. H."
  authors:
    - "Walker, M. H."
    - "Allen, R. C."
    - "Ho, G. C."
    - "Mason, G. M."
    - "Cohen, C. M. S."
    - "Lee, C."
  year: 2026
  venue: "Journal — TODO verify"
  doi: null
  arxiv_id: "2605.00163"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - icme-shocks
    - radial-evolution
    - multi-spacecraft
    - sep-esp-spectra
  missions: [PSP, "Solar Orbiter", ACE, Wind, STEREO]
  regime: [inner-heliosphere, 1au]

trigger_keywords:
  - "ICME shock"
  - "radial dependency"
  - "shock efficiency"
  - "multipoint ICME catalog"
  - "ESP spectral shape"
  - "SEP spectral shape"
  - "spectral break"
  - "0.7 au"
  - "shock evolution"
  - "PSP Solar Orbiter ACE Wind STEREO"
  - "ion composition"

data_products:
  - instrument: "PSP/ISʘIS + FIELDS MAG + SWEAP"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "39 multipoint ICME events 2016-2023 (TODO verify list)"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "SO/EPD + MAG + SWA"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "39 multipoint ICME events"
    archive: "SOAR"
  - instrument: "ACE/EPAM + ULEIS + MAG + SWEPAM"
    level: "L2"
    cadence: "instrument-native"
    interval: "subset"
    archive: "NASA CDAWeb"
  - instrument: "Wind/3DP + EPACT + MFI + 3DP/PESA"
    level: "L2"
    cadence: "instrument-native"
    interval: "subset"
    archive: "NASA CDAWeb"
  - instrument: "STEREO-A/IMPACT (LET, HET, SEPT) + PLASTIC + MAG"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "subset"
    archive: "STEREO archive / CDAWeb"

algorithms:
  - name: "Multipoint ICME-event identification + observer-pairing"
    equation_refs: []
    external_implementations: []
  - name: "Local shock-condition derivation (Rankine-Hugoniot per spacecraft)"
    equation_refs: []
    external_implementations: []
  - name: "ESP spectral-shape fit (Band / double-power-law / break)"
    equation_refs: []
    external_implementations: []
  - name: "Radial-trend regression of shock-acceleration efficiency"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2605.00163"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Compiles 39 multipoint ICME events 2016-2023 observed in situ by at
    least two of {PSP, SO, ACE, Wind, STEREO-A}. Derives local shock
    parameters (Rankine-Hugoniot) and ESP spectral-shape parameters per
    spacecraft. Finds shock-acceleration efficiency increasing with
    heliocentric distance while the parent ICME is within ~0.7 au, and
    decreasing efficiency at larger distances. Bounded to the 39-event
    sample, the 2016-2023 epoch, and the spacecraft set listed.
  out_of_scope:
    - "Do not treat the ~0.7 au inflection as a sharp physical boundary; it is a phenomenological turn-over."
    - "Do not extend the conclusion to single-spacecraft datasets without re-deriving multipoint context."
    - "Do not infer mechanism (DSA vs stochastic) from spectral-shape evolution alone."
    - "Do not apply the radial trend to ICMEs outside the 2016-2023 epoch without checking solar-cycle context."

failure_modes:
  - "Multipoint event selection bias — events seen by ≥ 2 spacecraft are biased toward wide longitudinal extents."
  - "Rankine-Hugoniot fitting requires clean upstream/downstream windows; turbulent SIR-disturbed events are noisy."
  - "Spectral break fitting depends on energy coverage at each instrument; cross-mission re-gridding required."
  - "Shock efficiency proxy choice (cutoff, slope, intensity) affects the radial trend; document the proxy."
  - "Composition-based event categorization needs cross-mission calibration."

depends_on:
  - "paper-trotta-2025-ip-shock-variability-multi-spacecraft"
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2605.00163"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, esp, icme, multi-spacecraft, statistical]
---

# Radial Evolution of ICME-Shock SEP Acceleration (39-Event Catalog) — paper-skill

> Compiled from Walker, M. H.; Allen, R. C.; Ho, G. C.; Mason, G. M.;
> Cohen, C. M. S.; Lee, C. (2026), "Radial Dependency of ICME-associated
> Particle Acceleration Processes: Statistical Multipoint Observations
> from 2016-2023," arXiv:2605.00163.
> **Quality tier**: `stub`.

This skill compiles the 39-event multipoint statistical analysis of
ICME-shock SEP/ESP acceleration efficiency vs heliocentric distance. It
generalizes the single-event Walker 2024 case study (Solar Orbiter +
ACE; arXiv:2410.01885) to a population.

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

- Asking whether shock acceleration efficiency increases or decreases
  with heliocentric distance.
- Building a radial-evolution diagnostic for an ICME-shock SEP/ESP
  pipeline.
- Comparing PSP / SO / ACE / Wind / STEREO observations of the same
  ICME.
- Cross-referencing single-event multipoint studies (e.g., Trotta+
  2025) against population statistics.

Do NOT use this skill when:

- The single event of interest is outside the catalog and you want a
  per-event diagnostic — use the methods skeleton but check applicability.
- The interest is *impulsive* SEP composition — different paper-skill
  family.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Across 39 multipoint ICME events 2016-2023
observed in situ by ≥ 2 of {PSP, SO, ACE, Wind, STEREO-A}, ESP spectral-
shape parameters and local-shock conditions are derived per spacecraft.
The statistical analysis reveals shock-acceleration efficiency
*increasing* with heliocentric distance while the parent ICME is within
~0.7 au, and *decreasing* efficiency beyond ~0.7 au.

**Verifiable task.** A reproduction succeeds when an agent, given the
39 events (TODO verify list), derives per-event local-shock parameters
and ESP spectral-shape parameters and reproduces the radial trend
(efficiency-vs-distance turn-over near ~0.7 au) qualitatively, with
quantitative agreement within ±20% on the efficiency proxy.

## 3. Methods / equations → executable workflow

### Multipoint ICME-event identification + observer-pairing

- Procedure:
  1. Compile candidate ICME events 2016-2023.
  2. For each event, identify all spacecraft (PSP / SO / ACE / Wind /
     STEREO-A) that observed the ICME in situ.
  3. Require ≥ 2 multipoint observers.
  4. Record observer heliocentric distance and longitudinal offset per
     spacecraft.

### Local shock-condition derivation (Rankine-Hugoniot per spacecraft)

- Procedure:
  1. For each (event, spacecraft) pair, identify the shock crossing in
     MAG + plasma data.
  2. Apply Rankine-Hugoniot to compute compression ratio, Mach number,
     obliquity θ_Bn.

### ESP spectral-shape fit (Band / double-power-law / break)

- Procedure:
  1. Extract per-spacecraft ESP spectra (energy-vs-intensity) at the
     shock passage.
  2. Fit a Band / double-power-law / single-break form.
  3. Record cutoff / break energy, low-energy slope, high-energy slope.

### Radial-trend regression of shock-acceleration efficiency

- Procedure:
  1. Define an efficiency proxy (e.g., normalized cutoff energy or
     normalized integrated intensity above a threshold).
  2. Plot efficiency vs heliocentric distance.
  3. Fit a piecewise model with a turn-over near ~0.7 au.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/ISʘIS + FIELDS MAG + SWEAP | L2/L3 | instrument-native | 39 events 2016-2023 | CDAWeb / PSP SOC | general-purpose |
| SO/EPD + MAG + SWA | L2/L3 | instrument-native | 39 events | SOAR | general-purpose |
| ACE/EPAM + ULEIS + MAG + SWEPAM | L2 | instrument-native | subset | CDAWeb | general-purpose |
| Wind/3DP + EPACT + MFI + 3DP/PESA | L2 | instrument-native | subset | CDAWeb | general-purpose |
| STEREO-A/IMPACT + PLASTIC + MAG | L2/L3 | instrument-native | subset | STEREO archive / CDAWeb | general-purpose |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires the event list
and the efficiency-proxy definition (TODO verify), then reproduction of
the radial trend with turn-over near ~0.7 au.

## 6. Failure modes → skill memory

- Multipoint selection bias toward wide-longitude events.
- Rankine-Hugoniot fitting noisy in SIR-disturbed plasma.
- Spectral break fits depend on instrument energy coverage; re-grid.
- Efficiency proxy choice affects the radial trend shape.
- Composition needs cross-mission calibration.

## 7. Claim boundary

**In scope.** 39-event multipoint ICME catalog 2016-2023; ESP spectral-
shape and local-shock-condition statistics; radial efficiency trend
(increase < 0.7 au; decrease beyond).

**Out of scope — do NOT generalize beyond:**

- Single-event statements.
- Solar-cycle epochs outside 2016-2023.
- Single-spacecraft catalogs.
- Mechanism inference (DSA vs stochastic) without companion analysis.

If a downstream task wants impulsive SEP composition, refuse and route
to a Reames-canonical skill.

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2605.00163
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: see tool contracts

## 9. Skill graph → depends_on

- `[[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]` —
  case-study multi-spacecraft technique that this skill generalizes
  statistically.
- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` —
  inner-heliosphere environment context.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (efficiency-proxy definition).** The "shock-acceleration
  efficiency" proxy is paper-specific (TODO verify with full text).
  No batch-wide standard proxy yet. Compose with [[paper-trotta-
  2025-ip-shock-variability-multi-spacecraft]] (cross-correlation
  metric) to propose a runtime-neutral efficiency definition.
- **Tension (~0.7 au turnover).** The increase-then-decrease at ~0.7
  au is the central empirical claim. New hypothesis: the turnover
  reflects competition between (i) shock strengthening as it
  decelerates and (ii) decreasing seed-population density beyond
  ~0.7 au. Testable by running [[paper-murtas-2024-compression-
  acceleration-hcs]] across the 39-event catalog with crossing-
  specific seed populations.
- **Experiment (shock-obliquity stratification).** Split the 39-event
  catalog by θ_Bn; does the 0.7-au turnover hold within each
  obliquity bin? Composes with [[paper-jebaraj-2024-synchrotron-
  electrons-near-sun-shocks]] (obliquity-dependent acceleration).
- **New hypothesis (composition trend).** If efficiency turnover
  reflects seed-density depletion, FIP-bias and κ should also vary
  with radial distance. Composes with [[paper-cuesta-2024-kappa-
  distributions-energetic-protons]] and [[paper-reames-2026-physics-
  of-seps]].

## Notes

A companion single-event paper (Walker+ 2024, "Radial Evolution of
ICME-Associated Particle Acceleration..." arXiv:2410.01885) is a candidate
for a dedicated paper-skill in a future batch
[[paper-walker-2024-icme-shock-solo-ace-radial-evolution]].
