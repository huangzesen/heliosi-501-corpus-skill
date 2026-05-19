---
name: paper-desai-2024-hcs-reconnection-400kev-protons
description: >-
  Use when validating or interpreting in-situ evidence that magnetic
  reconnection at the near-Sun heliospheric current sheet accelerates protons
  to ~400 keV inside the reconnection exhaust — Desai+ 2024 (ApJL, in press;
  arXiv:2410.16539) report PSP observations at ~16.25 R_sun with a -5
  power-law spectrum and kglobal-model interpretation invoking merging
  magnetic islands with a guide field of 0.2-0.3 of the reconnecting field.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Magnetic reconnection-driven energization of protons up to 400 keV at the near-Sun heliospheric current sheet"
  first_author: "Desai, M. I."
  authors:
    - "Desai, M. I."
    - "Drake, J. F."
    - "Phan, T."
    - "Yin, Z."
    - "Swisdak, M."
    - "McComas, D. J."
  year: 2024
  venue: "ApJL (in press, 2024)"
  doi: null
  arxiv_id: "2410.16539"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - reconnection-acceleration
    - heliospheric-current-sheet
    - psp-isois
    - merging-islands
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale, kinetic]

trigger_keywords:
  - "HCS reconnection"
  - "heliospheric current sheet"
  - "reconnection exhaust"
  - "trapped energetic protons"
  - "merging magnetic islands"
  - "guide field"
  - "kglobal model"
  - "PSP ISOIS"
  - "power-law spectrum index -5"
  - "near-Sun reconnection"
  - "Sunward propagating ions"
  - "particle acceleration"

data_products:
  - instrument: "PSP/ISʘIS EPI-Lo"
    level: "L2"
    cadence: "instrument-native"
    interval: "single HCS crossing at ~16.25 R_sun (TODO verify date from full text)"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/ISʘIS EPI-Hi"
    level: "L2"
    cadence: "instrument-native"
    interval: "same crossing"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/FIELDS MAG"
    level: "L2"
    cadence: "high cadence (~ms)"
    interval: "same crossing"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "PSP/SWEAP SPAN-I"
    level: "L3"
    cadence: "instrument-native"
    interval: "same crossing"
    archive: "NASA CDAWeb / PSP SOC"

algorithms:
  - name: "HCS reconnection-exhaust identification"
    equation_refs: []
    external_implementations: []
  - name: "Trapped-proton spectral fit (power-law -5)"
    equation_refs: []
    external_implementations: []
  - name: "kglobal merging-islands acceleration model"
    equation_refs: []
    external_implementations:
      - "github.com (Drake group; TODO verify exact repo)"
  - name: "Guide-field estimate from upstream/exhaust B"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2410.16539"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Reports a single PSP HCS crossing at ~16.25 R_sun (TODO verify date) in
    which energetic protons up to ~400 keV are trapped inside the reconnection
    exhaust, with Sunward-propagating reconnection jets, a pure-power-law
    spectrum of index ~ -5, and a kglobal-model interpretation invoking
    merging magnetic islands with guide field ~0.2-0.3 of the reconnecting
    field. The claim is bounded to this near-Sun HCS exhaust at this distance
    and to the kglobal merging-islands acceleration model class.
  out_of_scope:
    - "Do not extrapolate the -5 spectral index to other HCS crossings without re-fitting."
    - "Do not generalize the merging-islands acceleration to bursty/Hall reconnection regimes — kglobal is large-scale MHD with embedded islands."
    - "Do not claim HCS reconnection is the dominant acceleration channel for SEPs in general — the paper only shows it produces a significant near-Sun energetic-proton population at this crossing."
    - "Do not assume the same guide-field fraction (0.2-0.3) applies to every HCS exhaust."

failure_modes:
  - "Mistaking a switchback or local kink for an HCS crossing — confirm sector reversal with electron strahl and composition."
  - "Fitting the power-law over too wide an energy range — pure-power-law -5 is bounded by the trapped population's energy window."
  - "Ignoring the propagation direction — the paper relies on Sunward jets + Sunward energetic protons to localize the reconnection X-line beyond PSP."
  - "Treating the kglobal guide-field estimate as a direct measurement — it is inferred via model comparison."
  - "Confusing trapped energetic protons in the exhaust with external SEPs streaming through — pitch-angle and propagation direction discriminate."

depends_on:
  - "paper-murtas-2024-compression-acceleration-hcs"
  - "paper-reames-2026-physics-of-seps"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2410.16539"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, psp, reconnection]
---

# HCS Reconnection-Driven Proton Energization to 400 keV — paper-skill

> Compiled from Desai, M. I.; Drake, J. F.; Phan, T.; Yin, Z.; Swisdak, M.;
> McComas, D. J. (2024), "Magnetic reconnection-driven energization of
> protons up to 400 keV at the near-Sun heliospheric current sheet,"
> arXiv:2410.16539.
> **Quality tier**: `stub`.

This skill compiles the Desai+ 2024 PSP observation into agent-callable form
for any reconnection-driven SEP analysis at the near-Sun HCS. It is the
companion observational anchor to [[paper-murtas-2024-compression-acceleration-hcs]]
and to the 2026 Murtas pilot skill in `pilot_2026_and_runtime/`.

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

- A PSP encounter near 16 R_sun shows a clear HCS crossing with enhanced
  >100 keV proton intensities and Sunward jets — is this Desai+ 2024?
- A model produces trapped energetic protons in a reconnection exhaust and
  needs an observational counterpart for benchmarking spectral index.
- An agent considers whether HCS reconnection contributes a near-Sun
  SEP-seed population.
- Validating a kglobal-model run against in-situ data.

Do NOT use this skill when:

- The candidate event is far from the Sun (>0.5 au) — Desai+ 2024 is
  explicitly a near-Sun result.
- The candidate event is at the HCS but lacks reconnection-exhaust
  signatures (Walen-like jet + sector reversal + ion heating).

## 2. Paper claim → verifiable task

**Claim (narrow form).** At a single PSP HCS crossing at ~16.25 R_sun, PSP
detects trapped energetic protons up to ~400 keV co-located with a
Sunward-propagating reconnection exhaust; the differential spectrum is a
pure power-law of index ~ -5; kglobal simulations reproduce the trapping
and acceleration with merging magnetic islands and a guide field of
~0.2-0.3 of the reconnecting field.

**Verifiable task.** A reproduction succeeds when an agent, given the named
PSP crossing, emits `{E_max_protons, gamma_spectrum, exhaust_propagation_dir,
guide_field_fraction}` and matches Desai+ 2024 within tolerance: E_max ≈
400 keV ±20%, gamma ≈ -5 ±0.3, Sunward propagation direction, guide field
0.2-0.3 (within model-comparison uncertainty).

## 3. Methods / equations → executable workflow

### HCS reconnection-exhaust identification

- Paper reference: §"Observations" (TODO verify section number from full
  text).
- Procedure:
  1. Load PSP/FIELDS MAG RTN at high cadence. Find a magnetic sector
     reversal (sign flip of B_R, accounting for the local Parker spiral).
  2. Load PSP/SWEAP SPAN-I. Verify the proton bulk-flow component along
     the magnetic field exhibits a Walen-like jet on at least one side of
     the current sheet.
  3. Confirm proton heating (T_p enhancement) and electron strahl-polarity
     reversal across the sheet (suggesting topological reversal).
  4. Record exhaust start/end times and PSP heliocentric distance.

### Trapped-proton spectral fit (power-law -5)

- Paper reference: §"Energetic-particle spectrum".
- Procedure:
  1. Load PSP/ISʘIS EPI-Lo + EPI-Hi proton differential intensity within
     the exhaust window.
  2. Identify the Sunward-pitch-angle-dominant subpopulation (trapped /
     inward).
  3. Fit a single power-law in energy across the energy range over which
     the trapped population is well-resolved.
  4. Compare fitted index to ~ -5.

### kglobal merging-islands acceleration model

- Paper reference: §"Model".
- External implementations: Drake-group kglobal code — TODO verify
  repository handle.
- Procedure:
  1. Initialize a kglobal large-scale reconnection geometry with the
     locally inferred plasma parameters (n_p, T_p, |B|, sheet thickness).
  2. Embed merging-islands acceleration physics with a tunable guide field
     fraction.
  3. Scan guide-field fraction over [0.1, 0.5].
  4. Compare simulated trapped-proton spectrum to fitted spectrum; report
     best-fit guide field.

### Guide-field estimate from upstream/exhaust B

- Paper reference: §"Magnetic configuration".
- Procedure:
  1. Decompose upstream B into reconnection and guide components using the
     exhaust geometry.
  2. Report guide/reconnect ratio.
  3. Cross-check against kglobal model best-fit.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/ISʘIS EPI-Lo | L2 | instrument-native | HCS crossing window | CDAWeb / PSP SOC | general-purpose: WebFetch + cdflib |
| PSP/ISʘIS EPI-Hi | L2 | instrument-native | HCS crossing window | CDAWeb / PSP SOC | general-purpose |
| PSP/FIELDS MAG (RTN) | L2 | high cadence | HCS crossing window | CDAWeb / PSP SOC | general-purpose |
| PSP/SWEAP SPAN-I | L3 | instrument-native | HCS crossing window | CDAWeb / PSP SOC | general-purpose |

The kglobal model is a research code; no MCP is assumed. Treat the
simulation as a separate, manually scheduled HPC job.

## 5. Validation target → benchmark artifact

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires identifying the exact PSP encounter and crossing date (TODO verify
from full text) and reproducing the spectrum + exhaust diagnostics within
the tolerances in §2.

## 6. Failure modes → skill memory

- Misidentified HCS — a switchback or kink can spoof a sector reversal;
  always cross-check with composition + electron strahl.
- Spectrum-fit window too wide — exclude energies where the trapped
  population is not statistically resolved.
- Confusing externally streaming SEPs with trapped exhaust protons —
  pitch-angle and propagation direction discriminate.
- Treating the kglobal guide-field estimate as a direct measurement.
- Assuming the same physics at all heliocentric distances — Desai+ 2024
  emphasizes that the near-Sun (~16 R_sun) magnetic energy density makes
  this acceleration efficient; weaker at 1 au.

## 7. Claim boundary

**In scope.** Single PSP near-Sun HCS crossing with trapped energetic
protons (E ≲ 400 keV) inside a Sunward reconnection exhaust, gamma ≈ -5
spectrum, and kglobal-model guide-field interpretation.

**Out of scope — do NOT generalize beyond:**

- The same spectral index to other HCS crossings.
- The same guide-field fraction to every HCS exhaust.
- HCS reconnection as the *dominant* SEP acceleration channel — this is one
  observation establishing the mechanism's relevance.

If a downstream task asks for a statistical claim across many events, refuse
and route to a multi-event survey paper-skill (TODO: identify or create).

## 8. Links

- DOI: n/a (in-press at writing) — TODO add at promotion
- arXiv: https://arxiv.org/abs/2410.16539
- ADS: n/a — TODO add at promotion
- Code: n/a (kglobal code is research-group internal; TODO verify public
  repo)
- Data: PSP archive — see tool contracts in §4

## 9. Skill graph → depends_on

- `[[paper-murtas-2024-compression-acceleration-hcs]]` — sibling MHD +
  transport modeling of compression acceleration at the HCS, complementary
  to merging-islands picture.
- `[[paper-reames-2026-physics-of-seps]]` — places this result inside the
  two-mechanism narrative.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (HCS catalog).** No batch-wide PSP HCS-crossing catalog with
  per-crossing exhaust geometry + trapped-ion spectra. Compose with
  [[paper-murtas-2024-compression-acceleration-hcs]] (model) and the
  switchback-dissipation batch (`batch_psp_switchbacks_magnetic` →
  `phan-2022-switchback-boundary-reconnection-psp`) to build one.
- **Tension (kglobal vs MHD-Parker).** Desai's kglobal merging-islands
  picture reproduces γ ~ -5 and E_max ~ 400 keV; Murtas's 2D MHD +
  Parker transport reproduces a different (Q/A)^α scaling than
  observation (α ≈ 0.4 vs 0.7). New hypothesis: the discrepancy is
  closed by including kglobal-style merging in the MHD reconnection
  geometry. Testable by re-running Murtas's pipeline with a merged-
  island initial condition.
- **Experiment (guide-field sweep).** Sweep guide-field 0.0–0.5 in
  the kglobal model and compare E_max(proton); the paper fixes
  0.2–0.3. The sweep would constrain the guide-field requirement for
  400-keV trapping.
- **New hypothesis (heavy ions).** If the same exhaust traps protons
  to 400 keV, what about ³He, Fe? Compose with [[paper-cuesta-2024-
  kappa-distributions-energetic-protons]] (kappa-fit thermodynamics)
  and [[paper-reames-2026-physics-of-seps]] (FIP diagnosis) to write
  a heavy-ion HCS-trapping skill.

## Notes

Open question: do the trapped energetic protons subsequently leak into the
ambient solar wind as a seed population for downstream shock acceleration?
The paper raises but does not answer this; flag for future work.
