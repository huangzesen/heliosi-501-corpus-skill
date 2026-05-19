---
name: paper-trotta-2025-ip-shock-variability-multi-spacecraft
description: >-
  Use when quantifying how energetic-particle responses at a single strong
  interplanetary shock vary across multi-spacecraft observers separated by
  0.02-0.2 au — Trotta+ 2025 (arXiv 2508.19812) cross-correlate particle
  profiles from Wind/ACE at 1 au and Solar Orbiter at 0.8 au and attribute
  high-energy (>0.5 MeV) profile differences to shock evolution and
  ambient/shock spatial irregularities.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Variability in energetic particle observations at strong interplanetary shocks: Multi-spacecraft observations"
  first_author: "Trotta, D."
  authors:
    - "Trotta, D."
    - "Horbury, T. S."
    - "Giacalone, J."
  year: 2025
  venue: "Journal — TODO verify (A&A or ApJ likely)"
  doi: null
  arxiv_id: "2508.19812"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - interplanetary-shocks
    - multi-spacecraft
    - shock-evolution
    - cross-correlation
  missions: [Wind, ACE, "Solar Orbiter"]
  regime: [inner-heliosphere, 1au]

trigger_keywords:
  - "interplanetary shock"
  - "energetic storm particles"
  - "ESP"
  - "multi-spacecraft"
  - "shock variability"
  - "Wind"
  - "ACE"
  - "Solar Orbiter"
  - "cross-correlation"
  - "shock evolution"
  - "0.8 au"
  - "spatial irregularities"
  - "particle profile"

data_products:
  - instrument: "Wind/3DP + EPACT"
    level: "L2"
    cadence: "instrument-native"
    interval: "candidate strong IP shock (TODO verify event date)"
    archive: "NASA CDAWeb"
  - instrument: "ACE/EPAM + MAG + SWEPAM"
    level: "L2"
    cadence: "instrument-native"
    interval: "candidate strong IP shock"
    archive: "NASA CDAWeb"
  - instrument: "SO/EPD + MAG + SWA/PAS"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "candidate strong IP shock"
    archive: "SOAR"

algorithms:
  - name: "Multi-spacecraft shock identification + Rankine-Hugoniot"
    equation_refs: []
    external_implementations: []
  - name: "Cross-correlation of energetic-particle profiles"
    equation_refs: []
    external_implementations: []
  - name: "Shock-evolution attribution (radial vs spatial-irregularity)"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2508.19812"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Uses a single strong interplanetary shock observed by three radially
    aligned missions — Wind and ACE at 1 au, Solar Orbiter at 0.8 au —
    spanning 0.02-0.2 au separations. Develops a cross-correlation
    technique on energetic-particle profiles and shows that ions at
    different energies respond differently to the shock passage. High-
    energy (>0.5 MeV) profile shapes differ between 0.8 au and 1 au, which
    the paper attributes to shock evolution (less efficient high-energy
    production at 1 au than at 0.8 au) and to spatial irregularities in
    shock and ambient plasma.
  out_of_scope:
    - "Do not generalize to all strong IP shocks — this is a case-study scope."
    - "Do not equate the cross-correlation technique with a model of acceleration; it is a phenomenological diagnostic."
    - "Do not extrapolate the 0.8 au vs 1 au high-energy-efficiency contrast to <0.5 MeV without re-checking."
    - "Do not assume the spatial irregularities the authors invoke are the unique explanation; alternative interpretations (e.g., transport-only) are possible."

failure_modes:
  - "Cross-correlation peaks can be biased by background drift — detrend before correlating."
  - "Radial alignment imperfect; report HGI longitude offsets and time-of-flight corrections."
  - "Wind / ACE energy channels differ from SO/EPD — re-grid to a common axis."
  - "Treating 1 au observations as 'downstream' of 0.8 au assumes the shock propagates outward unmodified — this is exactly what the paper challenges."
  - "Strong-shock criterion threshold (e.g. Mach number) should be reported explicitly."

depends_on:
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"
  - "paper-kouloumvakos-2026-iva-shock-properties"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2508.19812"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, esp, shock, multi-spacecraft]
---

# Multi-Spacecraft IP-Shock Energetic-Particle Variability — paper-skill

> Compiled from Trotta, D.; Horbury, T. S.; Giacalone, J. (2025),
> "Variability in energetic particle observations at strong interplanetary
> shocks: Multi-spacecraft observations," arXiv:2508.19812.
> **Quality tier**: `stub`.

This skill compiles the multi-spacecraft cross-correlation technique for
energetic-particle profiles at strong interplanetary shocks. It is the
canonical methodological reference for any pipeline that quantifies
shock-related energetic-particle variability across radially aligned
observers in the 0.02-0.2 au separation regime.

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

- Designing a multi-spacecraft (Wind + ACE + SO, or similar) cross-
  correlation pipeline for an IP-shock energetic-particle event.
- Asking why two radially aligned observers see different high-energy
  particle profiles at the same shock.
- Differentiating *shock-evolution* contributions from *spatial-
  irregularity* contributions in IP-shock-driven ESP events.
- Establishing the energy-dependence of profile-shape changes.

Do NOT use this skill when:

- The shock is near-Sun (PSP) — load
  [[paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks]] instead.
- The interest is single-spacecraft Rankine-Hugoniot only.

## 2. Paper claim → verifiable task

**Claim (narrow form).** For a single strong interplanetary shock observed
in radial alignment by Wind, ACE (1 au) and Solar Orbiter (0.8 au),
cross-correlating energetic-particle profiles shows that ions at different
energies respond differently to the shock passage across observer
separations of 0.02-0.2 au. High-energy (>0.5 MeV) profile shapes differ
between 0.8 au and 1 au, attributed to shock evolution making high-energy
production less efficient at 1 au than at 0.8 au, and to spatial
irregularities in shock and ambient plasma.

**Verifiable task.** A reproduction succeeds when an agent, given the
event date (TODO verify) and the three-mission data, reproduces the
cross-correlation curves vs energy and the qualitative ordering
(0.8 au > 1 au efficiency above 0.5 MeV) within ±0.1 in correlation
coefficient.

## 3. Methods / equations → executable workflow

### Multi-spacecraft shock identification + Rankine-Hugoniot

- Procedure:
  1. Load Wind, ACE, SO MAG + plasma data around the suspected shock time.
  2. Identify the shock at each observer via classical jump conditions.
  3. Compute Mach number; verify "strong shock" classification.
  4. Record observer separations (radial + longitudinal).

### Cross-correlation of energetic-particle profiles

- Procedure:
  1. Re-grid Wind, ACE, SO energetic-particle profiles to a common energy
     axis.
  2. Detrend each profile (background subtraction).
  3. Compute pairwise cross-correlation as a function of energy bin.
  4. Tabulate correlation coefficient and time lag per energy bin.

### Shock-evolution attribution (radial vs spatial-irregularity)

- Procedure:
  1. Compare correlation drop with radial separation — if monotonic with
     separation, attribute to shock evolution.
  2. Identify ambient + shock spatial irregularities (B fluctuations,
     density spikes) and check coincidence with correlation drops.
  3. Report relative contribution of each (qualitatively).

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| Wind/3DP + EPACT | L2 | instrument-native | IP-shock window | CDAWeb | general-purpose: WebFetch + cdflib |
| ACE/EPAM + MAG + SWEPAM | L2 | instrument-native | IP-shock window | CDAWeb | general-purpose |
| SO/EPD + MAG + SWA/PAS | L2/L3 | instrument-native | IP-shock window | SOAR | general-purpose |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires the event date and
the exact energy-bin scheme (TODO verify) and reproducing Figure (TODO
verify) showing the energy-dependent correlation pattern.

## 6. Failure modes → skill memory

- Background drift biases cross-correlation — always detrend.
- Imperfect alignment requires HGI-longitude offset reporting + time-of-
  flight corrections.
- Cross-mission energy-channel mismatch — re-grid first.
- "Strong shock" threshold (Mach number) must be explicit.
- Spatial-irregularity attribution is not unique — transport-only
  explanations remain viable.

## 7. Claim boundary

**In scope.** Single strong IP shock; three-mission cross-correlation;
0.02-0.2 au separations; energy-dependent profile variability;
shock-evolution + spatial-irregularity attribution.

**Out of scope — do NOT generalize beyond:**

- Multiple-shock statistics — this is a case study.
- Near-Sun PSP shocks.
- Transport-only or acceleration-only interpretations as a uniqueness
  claim.

If a downstream task wants near-Sun PSP shock physics, refuse and route to
the appropriate PSP shock skill.

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2508.19812
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: Wind/ACE/SO archives — see tool contracts

## 9. Skill graph → depends_on

- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` —
  inner-heliosphere environment.
- `[[paper-kouloumvakos-2026-iva-shock-properties]]` — extends the
  shock-evolution interpretation to PSP/SO IVA events.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (energy-resolved variability law).** The cross-correlation
  *decreases* with energy in the paper's single event. No general
  energy-decorrelation law has been derived. Compose with [[paper-
  walker-2026-icme-radial-particle-acceleration-statistics]]
  (multipoint catalog) to fit a decorrelation function across many
  shocks.
- **Tension (shock evolution vs ambient irregularities).** The paper
  attributes variability to both shock-time-evolution AND ambient
  irregularities, without separating the two. New hypothesis: the
  two contributions are separable using radial-alignment vs
  longitudinal-offset partial regression. Composes with [[paper-
  kouloumvakos-2026-iva-shock-properties]] (connected-line shock
  evolution) for the evolution term.
- **Experiment (radial-shock vs longitudinal-shock atlas).** For each
  Walker-2026 multipoint event, decompose into radial (1 au vs <1 au)
  vs longitudinal (E/W) pairs; fit separate decorrelation laws.
- **New hypothesis (forecasting).** Decorrelation laws constrain the
  predictive horizon of ICME-driven SEP forecasts. A direct
  composition with operational SEP-forecast skills (e.g.,
  PARASOL — in `theme_energetic_particles.json`, not yet in this
  batch).

## Notes

The cross-correlation diagnostic technique developed here is the most
portable artifact of the paper. A synthesis skill
`[[multi-spacecraft-particle-profile-correlation]]` could lift it out of
this paper into a standalone helper.
