---
name: paper-cuesta-2024-kappa-distributions-energetic-protons
description: >-
  Use when fitting kappa distributions to PSP/ISʘIS EPI-Hi solar-energetic
  proton spectra (10-60 MeV) across an ICME and its driven shock and
  deriving thermodynamic parameters (κ, T_EP, n_EP, entropy) for SEPs —
  Cuesta+ 2024 (arXiv:2407.20343) report κ ≈ 3.5 peaks in CME ejecta,
  anti-correlated T_EP and n_EP (sub-isothermal polytropic), and positively
  correlated T_EP and κ (increasing entropy).
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Observations of Kappa Distributions in Solar Energetic Protons and Derived Thermodynamic Properties"
  first_author: "Cuesta, M. E."
  authors:
    - "Cuesta, M. E."
    - "Cummings, A. T."
    - "Livadiotis, G."
    - "McComas, D. J."
    - "Cohen, C. M. S."
    - "Khoo, L. Y."
  year: 2024
  venue: "Journal — TODO verify (likely ApJ)"
  doi: null
  arxiv_id: "2407.20343"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - kappa-distributions
    - thermodynamics
    - icme
    - cme-shock
    - psp-isois
  missions: [PSP]
  regime: [inner-heliosphere]

trigger_keywords:
  - "kappa distribution"
  - "solar energetic protons"
  - "ICME thermodynamics"
  - "CME-driven shock"
  - "non-Maxwellian"
  - "polytropic"
  - "entropy"
  - "PSP ISʘIS EPI-Hi"
  - "Livadiotis kappa"
  - "high-energy tail fitting"

data_products:
  - instrument: "PSP/ISʘIS EPI-Hi HET"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "ICME + driven-shock interval (TODO verify event date)"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/FIELDS MAG"
    level: "L2"
    cadence: "high cadence"
    interval: "ICME + driven-shock interval"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/SWEAP SPAN-I"
    level: "L3"
    cadence: "instrument-native"
    interval: "ICME + driven-shock interval"
    archive: "NASA CDAWeb / PSP SOC"

algorithms:
  - name: "Kappa-distribution fit to high-energy tail"
    equation_refs: []
    external_implementations: []
  - name: "Thermodynamic-parameter extraction (T_EP, n_EP, κ)"
    equation_refs: []
    external_implementations: []
  - name: "ICME-region tagging (pre-shock / sheath / ejecta / trailing)"
    equation_refs: []
    external_implementations: []
  - name: "Polytropic / entropy diagnostic"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2407.20343"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Fits a kappa distribution to the PSP/ISʘIS EPI-Hi high-energy-tail
    spectra (10-60 MeV) for a single ICME passage and its driven shock,
    yielding kappa parameter κ_EP increasing from pre-ICME, peaking in
    the CME ejecta (κ_EP ≈ 3.5), then decreasing in the trailing CME.
    Finds T_EP and n_EP anti-correlated (consistent with sub-isothermal
    polytropic processes) and T_EP and κ_EP positively correlated
    (interpreted as increasing entropy). Bounded to the single event and
    energy range studied.
  out_of_scope:
    - "Do not extend κ_EP ≈ 3.5 peak as a universal ICME-ejecta value; this is one event."
    - "Do not extrapolate the 10-60 MeV thermodynamic interpretation to lower energies (suprathermal) or higher energies (GeV)."
    - "Do not use the polytropic diagnostic as a hard equation of state — it is a phenomenological signature."
    - "Do not interpret entropy increase as global; it is a within-event tracking."

failure_modes:
  - "Forcing a kappa fit on a power-law-like tail can mis-converge — verify residuals."
  - "ICME-region tagging boundaries are subjective; sensitivity to boundary placement should be reported."
  - "EPI-Hi HET response above ~60 MeV is calibration-limited; do not fit beyond the stated energy range."
  - "Comparing κ_EP across events with different shock geometries can blur the entropy interpretation."

depends_on:
  - "paper-reames-2026-physics-of-seps"
  - "paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2407.20343"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, kappa-distribution, thermodynamics, icme]
---

# Kappa Distributions in Solar Energetic Protons — paper-skill

> Compiled from Cuesta, M. E.; Cummings, A. T.; Livadiotis, G.; McComas,
> D. J.; Cohen, C. M. S.; Khoo, L. Y. (2024), "Observations of Kappa
> Distributions in Solar Energetic Protons and Derived Thermodynamic
> Properties," arXiv:2407.20343.
> **Quality tier**: `stub`.

This skill compiles the first kappa-distribution thermodynamic analysis of
PSP/ISʘIS EPI-Hi protons across an ICME + driven shock. It is the
canonical primary observational source for kappa-based SEP thermodynamics.

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

- A PSP ICME crossing shows a non-Maxwellian energetic-proton tail and the
  user asks "is this consistent with a kappa distribution?".
- Comparing kappa parameter κ across ICME regions (pre-shock / sheath /
  ejecta / trailing).
- Deriving polytropic / entropy properties of SEP populations.
- Cross-referencing with Livadiotis-style kappa theory.

Do NOT use this skill when:

- The energy range is below 10 MeV — the paper's analysis is bounded to
  10-60 MeV.
- The interest is electrons — different paper-skill family.

## 2. Paper claim → verifiable task

**Claim (narrow form).** PSP/ISʘIS EPI-Hi proton high-energy tails (10-60
MeV) across a single ICME + driven shock are well-fit by a kappa
distribution. The kappa parameter κ_EP rises from pre-ICME, peaks at ≈ 3.5
in the CME ejecta, then decreases in the trailing CME. T_EP and n_EP are
anti-correlated (sub-isothermal polytropic), and T_EP and κ_EP are
positively correlated (increasing entropy).

**Verifiable task.** A reproduction succeeds when an agent, given the
named PSP ICME passage (TODO verify date), fits kappa per region and
emits `{κ(region), T_EP(region), n_EP(region)}` reproducing the κ_EP
peak ≈ 3.5 in the ejecta and the anti-correlated T_EP / n_EP behavior
within tolerance (±20% on κ, sign-correct on the correlations).

## 3. Methods / equations → executable workflow

### Kappa-distribution fit to high-energy tail

- Procedure:
  1. Load PSP/ISʘIS EPI-Hi HET proton differential intensity (10-60 MeV)
     for the ICME interval (per-region).
  2. Convert to phase-space density f(E).
  3. Fit a kappa distribution
     `f(E) ∝ [1 + (E−E_0) / (κ·k·T_EP)]^(-κ-1)`
     (TODO verify exact functional form from the Livadiotis companion).
  4. Extract κ, T_EP, normalization → n_EP.

### Thermodynamic-parameter extraction (T_EP, n_EP, κ)

- Procedure:
  1. Tabulate κ, T_EP, n_EP per ICME sub-region.
  2. Compute κ time series across the event.

### ICME-region tagging (pre-shock / sheath / ejecta / trailing)

- Procedure:
  1. Use PSP/FIELDS MAG + SWEAP SPAN-I to tag pre-shock, sheath, ejecta,
     trailing regions following standard ICME-classification criteria.
  2. Record region boundaries; perform sensitivity analysis.

### Polytropic / entropy diagnostic

- Procedure:
  1. Plot T_EP vs n_EP; check anti-correlation (sub-isothermal polytropic).
  2. Plot T_EP vs κ_EP; check positive correlation (entropy interpretation).
  3. Compute event-integrated entropy change.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/ISʘIS EPI-Hi HET | L2/L3 | instrument-native | ICME + driven-shock | CDAWeb / PSP SOC | general-purpose: WebFetch + cdflib |
| PSP/FIELDS MAG | L2 | high cadence | ICME + driven-shock | CDAWeb / PSP SOC | general-purpose |
| PSP/SWEAP SPAN-I | L3 | instrument-native | ICME + driven-shock | CDAWeb / PSP SOC | general-purpose |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires the named ICME
event date (TODO verify), the kappa functional form (TODO verify from
Livadiotis companion), and the region-boundary list. The target is the
κ_EP peak ≈ 3.5 in CME ejecta and the sign-correct T_EP/n_EP and
T_EP/κ_EP correlations.

## 6. Failure modes → skill memory

- Kappa fit can mis-converge on a power-law tail — check residuals.
- ICME-region tagging is subjective; do a sensitivity sweep.
- EPI-Hi HET calibration limits — stay within 10-60 MeV.
- Cross-event κ comparison requires matched shock geometry.
- Polytropic interpretation is phenomenological, not a strict EOS.

## 7. Claim boundary

**In scope.** Single PSP ICME + driven-shock event; kappa fits to 10-60
MeV proton spectra; κ_EP, T_EP, n_EP region time series; T_EP/n_EP and
T_EP/κ_EP correlations.

**Out of scope — do NOT generalize beyond:**

- Universal κ ≈ 3.5 in ICME ejecta — single event.
- Lower (suprathermal) or higher (GeV) energy ranges.
- Strict EOS / hydrostatic interpretation.
- Cross-event global statistics — not a survey.

If a downstream task wants a statistical κ distribution, refuse and route
to a multi-event paper-skill (TODO).

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2407.20343
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: PSP archive — see tool contracts

## 9. Skill graph → depends_on

- `[[paper-reames-2026-physics-of-seps]]` — places kappa-distribution
  observations in the broader SEP framework.
- `[[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]` —
  inner-heliosphere environment context.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (multi-event kappa atlas).** Cuesta+ 2024 reports κ for a
  single ICME crossing. No multi-event atlas. Compose with [[paper-
  walker-2026-icme-radial-particle-acceleration-statistics]] and
  [[paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp]]
  to build one across the 2016–2023 ICME catalog.
- **Tension (thermodynamic consistency across the shock).** Paper
  reports anti-correlated T_EP and n_EP (sub-isothermal polytropic)
  and positively correlated T_EP and κ (entropy increases). New
  hypothesis: the polytropic index and entropy slope are
  diagnostics of shock-acceleration regime (compressive vs.
  stochastic). Composes with [[paper-murtas-2024-compression-
  acceleration-hcs]] for the modeling side.
- **Experiment (kappa at HCS vs ICME).** Apply the Livadiotis kappa
  fit to [[paper-desai-2024-hcs-reconnection-400kev-protons]] HCS
  intervals; compare κ distributions. Are reconnection-jet protons
  more strongly non-Maxwellian than shock-accelerated protons?
- **New hypothesis (κ as classification feature).** κ may serve as
  an *additional* impulsive/gradual classifier in Reames-2026's
  decision table. Test by adding κ to the diagnostic set.

## Notes

The Livadiotis 2024 companion (arXiv:2407.04188) provides the theoretical
kappa formalism. Future skill could be `[[paper-livadiotis-2024-kappa-tail-technique]]`.
