---
name: paper-laitinen-2026-vda-turbulent-heliosphere
description: >-
  Use when applying or interpreting Velocity Dispersion Analysis (VDA) of
  Solar Energetic Particle onset times — Laitinen & Dalla 2026
  (arXiv:2603.06433) use full-orbit proton simulations in 2D-dominant
  turbulence superposed on a Parker spiral to show that VDA-derived solar
  injection times are biased 2-16 minutes late and path lengths exceed
  the Parker spiral by 0.2-0.3 au (weak/moderate turbulence) or >5 au
  (strong turbulence), and that pre-event proton background spectra
  introduce additional 5-20-minute injection-time biases.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Velocity dispersion of Solar Energetic Particles in turbulent heliosphere"
  first_author: "Laitinen, T."
  authors:
    - "Laitinen, T."
    - "Dalla, S."
  year: 2026
  venue: "Journal — TODO verify"
  doi: null
  arxiv_id: "2603.06433"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - velocity-dispersion-analysis
    - sep-transport
    - full-orbit-simulation
    - turbulence
    - parker-spiral
  missions: ["n/a"]
  regime: [inner-heliosphere, 1au]

trigger_keywords:
  - "velocity dispersion analysis"
  - "VDA"
  - "SEP onset time"
  - "solar injection time"
  - "path length"
  - "Parker spiral"
  - "2D turbulence"
  - "slab turbulence"
  - "full-orbit simulation"
  - "background spectrum"
  - "onset threshold"
  - "SEP transport"

data_products: []

algorithms:
  - name: "Full-orbit proton simulation in IMF + turbulence"
    equation_refs: []
    external_implementations: []
  - name: "Analytical 2D-dominant + slab turbulence model"
    equation_refs: []
    external_implementations: []
  - name: "VDA fitting with onset threshold"
    equation_refs: []
    external_implementations: []
  - name: "Background-spectrum sensitivity sweep"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2603.06433"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Uses full-orbit simulations of 1-100 MeV SEP protons propagating in a
    Parker-spiral IMF superposed with analytically prescribed turbulence
    (dominant 2D transverse modes + a minor slab contribution). Applies VDA
    on simulated SEP onset times across three turbulence strengths and
    using an SEP-onset threshold mimicking a realistic pre-event proton
    background. Finds: weak/moderate turbulence → VDA injection time bias
    +2-16 min, path length 0.2-0.3 au longer than the Parker spiral;
    strong turbulence → path length >5 au; pre-event background spectrum
    shape adds 5-20 min injection-time bias depending on heliolongitude.
  out_of_scope:
    - "Do not extrapolate the (2D-dominant + minor slab) turbulence prescription to fundamentally different power-spectrum models without re-simulating."
    - "Do not apply these bias values to event-by-event VDA results uniformly — they are simulation-averaged."
    - "Do not treat the path-length bias as a measurement of the actual IMF length — it is a VDA-method bias."
    - "Do not generalize the strong-turbulence-large-path-length conclusion to events known to have low turbulence."

failure_modes:
  - "VDA assumes a delta-function injection; spatially or temporally extended sources change the bias."
  - "Onset-threshold dependence: lower threshold gives earlier onsets and changes the bias."
  - "Background-spectrum proxy: energy-dependence of the background must be measured per event."
  - "Turbulence prescription bias: 2D-dominant vs slab-dominant turbulence gives different scattering and hence path lengths."
  - "Applying VDA to events with field-line meandering not captured by the analytical model can over- or under-correct."

depends_on:
  - "paper-xu-2026-psp-iva-sep-events"
  - "paper-reames-2026-physics-of-seps"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2603.06433"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, transport, vda, turbulence]
---

# VDA in Turbulent Heliosphere — paper-skill

> Compiled from Laitinen, T. & Dalla, S. (2026), "Velocity dispersion of
> Solar Energetic Particles in turbulent heliosphere," arXiv:2603.06433.
> **Quality tier**: `stub`.

This skill compiles the simulated biases of Velocity Dispersion Analysis
in a turbulent heliosphere. It is the methodological caveat companion to
any SEP-onset / injection-time skill (e.g.,
[[paper-xu-2026-psp-iva-sep-events]]).

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

- Computing or quoting a VDA-derived solar injection time t_sun and
  path length s for an SEP event.
- Asking whether a path length significantly larger than the Parker
  spiral (e.g. s ~ 1.5-2 au) is "anomalous" or just a turbulence bias.
- Designing a VDA bias correction for a pipeline.
- Sanity-checking SEP-onset times claimed in adjacent observational
  papers.

Do NOT use this skill when:

- The interest is the *acceleration time* of an SEP event derived by
  non-VDA methods (e.g., gamma-ray timing).
- The simulations assume a specific turbulence prescription
  inappropriate for the candidate event (e.g., slab-dominant).

## 2. Paper claim → verifiable task

**Claim (narrow form).** Full-orbit proton simulations in a Parker-spiral
IMF + 2D-dominant (+ minor slab) turbulence give VDA estimates of t_sun
that are 2-16 min later than the true injection time for weak/moderate
turbulence, and apparent path lengths 0.2-0.3 au longer than the Parker
spiral. For strong turbulence the apparent path length exceeds 5 au,
much longer than typical observational VDA results. Different pre-event
background-spectrum shapes shift VDA injection times by 5-20 min,
depending on heliolongitude.

**Verifiable task.** A reproduction succeeds when an agent runs full-orbit
SEP simulations with the paper's three turbulence strengths and recovers
(within tolerance) the VDA bias ranges (Δt_sun, Δs) above.

## 3. Methods / equations → executable workflow

### Full-orbit proton simulation in IMF + turbulence

- Procedure:
  1. Set up the Parker-spiral IMF.
  2. Superpose 2D-dominant transverse fluctuations + minor slab modes
     (TODO verify exact spectral parameters).
  3. Inject 1-100 MeV protons at a chosen near-Sun location.
  4. Integrate full Lorentz orbits.

### Analytical 2D-dominant + slab turbulence model

- Procedure:
  1. Use the analytical turbulence form the paper prescribes (TODO verify
     the exact form from §"Model").
  2. Tune turbulence strength across (weak, moderate, strong).

### VDA fitting with onset threshold

- Procedure:
  1. Compute simulated SEP intensity time series per energy bin.
  2. Apply an onset-threshold detector (mimicking a realistic energetic-
     proton background).
  3. Fit t_onset(E) vs 1/v(E); extract t_sun and apparent path length s.

### Background-spectrum sensitivity sweep

- Procedure:
  1. Vary the assumed pre-event background spectrum shape.
  2. Re-apply VDA; record (Δt_sun, Δs).
  3. Repeat for several heliolongitudes.

## 4. Data / instruments → tool contracts

Theory + simulation only. No in-situ data products. Tool contract is a
local HPC SDE / full-orbit code — research-group internal.

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires re-implementing
the turbulence model + full-orbit integrator (TODO verify exact
parameters) and reproducing the (Δt_sun, Δs) ranges within ±20%.

## 6. Failure modes → skill memory

- VDA assumes delta-function injection — extended sources break the
  bias estimate.
- Onset-threshold choice affects bias.
- Background-spectrum shape per event must be measured.
- Turbulence prescription is the strongest model dependency.
- Field-line meandering not captured by analytical models can be
  important in some events.

## 7. Claim boundary

**In scope.** Simulated VDA biases under (2D-dominant + minor slab)
turbulence in a Parker-spiral IMF, for 1-100 MeV protons, across three
turbulence strengths, with an SEP-onset threshold mimicking a realistic
pre-event background.

**Out of scope — do NOT generalize beyond:**

- Other turbulence prescriptions.
- Event-by-event direct quote of the bias values without re-checking the
  per-event turbulence and background spectrum.
- Acceleration-time inference — this paper is transport-only.

If a downstream task wants acceleration-time inference, refuse and route
to a flare / shock acceleration timing skill.

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2603.06433
- ADS: n/a — TODO add at promotion
- Code: n/a — TODO verify Laitinen / Dalla group public repo
- Data: n/a — simulation only

## 9. Skill graph → depends_on

- `[[paper-xu-2026-psp-iva-sep-events]]` — IVA features are often
  interpreted via VDA; this skill quantifies the VDA bias.
- `[[paper-reames-2026-physics-of-seps]]` — general SEP-acceleration
  context.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (VDA bias correction in published catalogs).** The 2–16 min
  injection-time bias and 0.2–0.3 au path-length bias have not been
  back-applied to published VDA injection-time catalogs. New paper-
  skill: a *bias-aware VDA* primary that consumes existing catalogs
  and emits corrected injection times. Composes with [[paper-xu-
  2026-psp-iva-sep-events]] and [[paper-kouloumvakos-2026-iva-shock-
  properties]] for the IVA-context.
- **Tension (turbulence-spectrum dependence).** Paper's biases assume
  a 2D-dominant + minor-slab IMF turbulence prescription. Different
  prescriptions (e.g., slab-dominant, scale-dependent dynamic
  alignment) would give different biases. New hypothesis: VDA biases
  are a *diagnostic* of the IMF turbulence prescription. Composes
  with the turbulence batch (`pilot_turbulence`) — specifically
  `huang-2023-psp-one-over-f-spectrum` and `sioulas-2024-higher-
  order-3d-anisotropy`.
- **Experiment (cross-prescription sweep).** Re-run the full-orbit
  proton sims under three IMF prescriptions; report bias ranges.
- **New hypothesis (Mars/outer-heliosphere).** Bias should grow with
  heliocentric distance; testable with Tianwen-1 / MAVEN data
  (composes with the not-yet-in-batch Cao-2026 SEP-rise-time skill).

## Notes

A natural pairing with [[paper-cao-2026-sep-rise-time-earth-mars]],
which uses VDA-adjacent rise-time fitting to constrain transport-
parameter rigidity dependence; both papers should be loaded together
when reasoning about SEP transport bias.
