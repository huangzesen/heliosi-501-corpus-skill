---
name: paper-xu-2026-psp-iva-sep-events
description: >-
  Use when detecting and cataloging PSP/ISʘIS SEP events with inverse
  velocity arrival (IVA) "nose" features and grouping them by nose
  energy (low <0.5 MeV, medium 0.5-5 MeV, high >5 MeV) — Xu+ 2026
  (arXiv:2602.12475) report 14 IVA events through end of 2024 with most
  (11/14) at medium nose energies, and a contour-line-of-intensity method
  for IVA detection.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Parker Solar Probe observations of solar energetic particle (SEP) events with inverse velocity arrival (IVA) features"
  first_author: "Xu, Z."
  authors:
    - "Xu, Z."
    - "Cohen, C. M. S."
    - "Leske, R. A."
    - "Muro, G. D."
    - "Cummings, A. C."
    - "Romeo, O. M."
  year: 2026
  venue: "Journal — TODO verify"
  doi: null
  arxiv_id: "2602.12475"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - inverse-velocity-arrival
    - psp-isois
    - shock-acceleration
    - event-catalog
  missions: [PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "inverse velocity arrival"
  - "IVA"
  - "PSP ISʘIS"
  - "Labor Day event"
  - "2022 September 5"
  - "nose energy"
  - "contour-line detection"
  - "SEP event catalog"
  - "velocity dispersion"
  - "shock obliquity"
  - "footpoint connectivity"

data_products:
  - instrument: "PSP/ISʘIS EPI-Lo"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "PSP encounters through 2024"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/ISʘIS EPI-Hi"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "PSP encounters through 2024"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "Coronagraph (LASCO + STEREO/SECCHI)"
    level: "L1"
    cadence: "instrument-native"
    interval: "associated CMEs per event"
    archive: "LASCO + STEREO archives"
  - instrument: "Flare association (GOES / EOVSA / SDO)"
    level: "L2"
    cadence: "event-trigger"
    interval: "associated flare per event"
    archive: "various"

algorithms:
  - name: "Contour-line-of-intensity IVA detector"
    equation_refs: []
    external_implementations: []
  - name: "Nose-energy classification (L/M/H bins)"
    equation_refs: []
    external_implementations: []
  - name: "Parameter-correlation analysis (radial distance, CME/shock speed, θ_Bn, footpoint separation)"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2602.12475"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Builds the first PSP/ISʘIS IVA-event catalog through the end of 2024,
    identifying 14 IVA events using a contour-line-of-intensity detection
    method on the joint EPI-Lo / EPI-Hi energy spectrogram. Groups events
    by "nose energy" (L < 0.5 MeV; M 0.5-5 MeV; H > 5 MeV) and reports
    that the majority (11/14) fall in the medium nose-energy bin.
    Explores correlations with PSP radial distance, CME/shock speed,
    shock-normal/upstream-B angle θ_Bn, and PSP footpoint vs flare
    longitude separation, motivating IVA as a probe of shock acceleration
    and propagation.
  out_of_scope:
    - "Do not extrapolate the 14-event statistics to a population-level claim about all IVA events — this is a sample-limited catalog."
    - "Do not infer mechanism from IVA presence alone; transport, acceleration and instrumental effects all contribute."
    - "Do not assume the contour-line detection generalizes unchanged to non-PSP instruments without re-calibration."
    - "Do not use the (L/M/H) nose-energy bins as universal — they are operational thresholds for this catalog."

failure_modes:
  - "Contour-line detection sensitive to spectrogram smoothing / binning; document choices."
  - "Footpoint-vs-flare-longitude separation depends on assumed solar-wind speed for ballistic mapping."
  - "θ_Bn measurement requires a stable upstream window — apply when the shock-crossing is in PSP's range."
  - "Selection bias toward bright events — flag events near sensitivity floor."
  - "Treating IVA presence as 'shock acceleration confirmed' without companion 3D-reconstruction (Kouloumvakos+) is over-claim."

depends_on:
  - "paper-kouloumvakos-2026-iva-shock-properties"
  - "paper-laitinen-2026-vda-turbulent-heliosphere"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2602.12475"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, iva, psp, catalog]
---

# PSP IVA-SEP Events — paper-skill

> Compiled from Xu, Z.; Cohen, C. M. S.; Leske, R. A.; Muro, G. D.;
> Cummings, A. C.; Romeo, O. M. (2026), "Parker Solar Probe observations
> of solar energetic particle (SEP) events with inverse velocity arrival
> (IVA) features," arXiv:2602.12475.
> **Quality tier**: `stub`.

This skill compiles the first PSP IVA event catalog and its contour-line
detection technique. It pairs with
[[paper-kouloumvakos-2026-iva-shock-properties]] which provides the 3D
shock-reconstruction explanation.

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

- Detecting IVA features in a PSP/ISʘIS spectrogram.
- Classifying an IVA event by nose energy (L / M / H).
- Looking up the canonical Labor Day event (2022 September 5) as a worked
  example.
- Deciding which IVA explanation (shock acceleration, transport,
  instrumental) is most consistent with a given event's parameters.

Do NOT use this skill when:

- The IVA event is observed on SO only — load
  [[paper-kouloumvakos-2026-iva-shock-properties]] for SO IVA-SEP
  framing.
- The event spectrogram has standard (forward) velocity dispersion.

## 2. Paper claim → verifiable task

**Claim (narrow form).** PSP/ISʘIS data through the end of 2024 contains
14 SEP events with IVA "nose" features detected by a contour-line-of-
intensity method. The nose energy distributes as: most events (11/14)
have medium nose energies (0.5-5 MeV); fewer at low (<0.5 MeV) or high
(>5 MeV). The 2022-09-05 Labor Day event is the canonical case.
Parameter correlations with radial distance, CME/shock speed, θ_Bn, and
footpoint separation are explored as observational constraints on
acceleration and propagation.

**Verifiable task.** A reproduction succeeds when an agent runs the
contour-line detector over PSP/ISʘIS data through end of 2024, recovers
≥ 12 of the 14 IVA events (with TODO verify event list), assigns the
correct L/M/H bin, and reproduces the 11/14-medium ratio.

## 3. Methods / equations → executable workflow

### Contour-line-of-intensity IVA detector

- Procedure:
  1. Load joint EPI-Lo / EPI-Hi proton spectrogram for the candidate
     interval.
  2. Smooth in energy/time (TODO verify smoothing window).
  3. Trace intensity contours; detect concave ("nose") shape.
  4. Extract the apex of the nose (= transition energy at IVA onset).

### Nose-energy classification (L/M/H bins)

- Procedure:
  1. Apply the L < 0.5 MeV / M 0.5-5 MeV / H > 5 MeV thresholds.
  2. Assign bin label.

### Parameter-correlation analysis

- Procedure:
  1. For each IVA event tabulate:
     - PSP heliocentric distance,
     - CME speed (LASCO / STEREO),
     - Shock speed (LASCO + kinematic model),
     - θ_Bn (from in-situ MAG if PSP crosses the shock; else from
       coronal-shock model),
     - PSP magnetic footpoint vs flare longitude separation.
  2. Cross-correlate with nose energy and IVA onset time.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/ISʘIS EPI-Lo | L2/L3 | instrument-native | PSP encounters through 2024 | CDAWeb / PSP SOC | general-purpose: WebFetch + cdflib |
| PSP/ISʘIS EPI-Hi | L2/L3 | instrument-native | PSP encounters through 2024 | CDAWeb / PSP SOC | general-purpose |
| Coronagraph (LASCO + STEREO/SECCHI) | L1 | instrument-native | associated CMEs | LASCO + STEREO | general-purpose |
| Flare association (GOES / EOVSA / SDO) | L2 | event-trigger | associated flare | various | general-purpose |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires:

- The exact contour-line smoothing parameters (TODO verify from full
  text);
- The complete 14-event list with dates;
- Reproduction of the 11/14-medium nose-energy ratio.

## 6. Failure modes → skill memory

- Contour-line detection is sensitive to smoothing — sweep and report.
- Footpoint mapping uses a ballistic assumption — sensitivity to
  solar-wind-speed input.
- θ_Bn requires shock crossing or coronal-shock-model fallback —
  document choice.
- Selection bias toward bright events — flag near sensitivity floor.
- IVA presence ≠ mechanism — companion paper-skill needed.

## 7. Claim boundary

**In scope.** Catalog of 14 PSP IVA events through end of 2024; L/M/H
nose-energy classification; parameter correlations.

**Out of scope — do NOT generalize beyond:**

- Population-level statistics (sample-limited).
- Mechanism inference from IVA alone.
- Non-PSP instruments without recalibration.

If a downstream task wants the connectivity-along-shock-evolution
explanation, refuse and route to
[[paper-kouloumvakos-2026-iva-shock-properties]].

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2602.12475
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: PSP archive — see tool contracts

## 9. Skill graph → depends_on

- `[[paper-kouloumvakos-2026-iva-shock-properties]]` — sister 3D shock
  reconstruction explanation.
- `[[paper-laitinen-2026-vda-turbulent-heliosphere]]` — turbulent
  transport can also produce velocity-dispersion-like features; cross-
  check.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (per-event mechanism vector).** Paper catalogs IVA events but
  does not commit per-event to a mechanism (shock-evolution vs
  transport vs instrument). Compose with [[paper-kouloumvakos-2026-
  iva-shock-properties]] and [[paper-laitinen-2026-vda-turbulent-
  heliosphere]] to emit per-event mechanism-likelihood vectors.
- **Tension (medium-energy clustering, 11/14).** The strong clustering
  of IVA in the medium nose-energy bin (0.5–5 MeV) is the central
  empirical finding; its origin is unexplained. New hypothesis: the
  clustering reflects a universal diffusion-coefficient transition
  at 0.5–5 MeV (kinematic at lower energy, scattering at higher).
  Testable by cross-fitting [[paper-laitinen-2026-vda-turbulent-
  heliosphere]] to the IVA catalog.
- **Experiment (PSP-only vs PSP+SO IVA detection).** Apply the
  contour-line detector to SO/HET-only events; compare. If the
  medium-energy clustering persists at 1 au, it is *not* a near-Sun
  feature.
- **New hypothesis (IVA as seed-population fingerprint).** If
  residual-impulsive seeds dominate the medium-energy population, the
  IVA-medium-energy peak should correlate with FIP-biased
  composition. Composes with [[paper-reames-2026-physics-of-seps]]
  and [[paper-cuesta-2024-kappa-distributions-energetic-protons]].

## Notes

The 2022-09-05 Labor Day event recurs across multiple IVA papers
(this skill, [[paper-kouloumvakos-2026-iva-shock-properties]], Chen+
2025 arXiv:2506.20322). Promote it to a dedicated event-skill if it
becomes a benchmark target.
