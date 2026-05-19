---
name: paper-murtas-2024-compression-acceleration-hcs
description: >-
  Use when modeling multi-species ion acceleration at the reconnecting
  heliospheric current sheet via the *compression-acceleration* channel —
  Murtas, Li, Guo 2024 (arXiv:2408.10445) solve the Parker transport equation
  over large-scale MHD reconnection simulations to obtain power-law spectra
  and Q/A-controlled E_max scaling E_max ∝ (Q/M)^α with α ≈ 0.4 from
  quasilinear-Kolmogorov diffusion, vs α ≈ 0.7 observed by PSP.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Compression Acceleration of Protons and Heavier Ions at the Heliospheric Current Sheet"
  first_author: "Murtas, G."
  authors:
    - "Murtas, G."
    - "Li, X."
    - "Guo, F."
  year: 2024
  venue: "ApJ (in press, 2024) — TODO verify final venue"
  doi: null
  arxiv_id: "2408.10445"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - reconnection-acceleration
    - parker-transport-equation
    - heliospheric-current-sheet
    - multi-species
  missions: [PSP]
  regime: [inner-heliosphere, MHD-scale]

trigger_keywords:
  - "compression acceleration"
  - "Parker transport equation"
  - "HCS reconnection"
  - "heliospheric current sheet"
  - "multi-species ions"
  - "heavy ion acceleration"
  - "Q/M scaling"
  - "E_max scaling"
  - "MHD simulation"
  - "diffusion coefficient"
  - "quasilinear theory"
  - "Kolmogorov power spectrum"

data_products:
  - instrument: "PSP/ISʘIS"
    level: "L2/L3 (reference dataset for spectral-index comparison)"
    cadence: "event-integrated"
    interval: "HCS-crossing SEP events (specific events TODO verify)"
    archive: "NASA CDAWeb / PSP SOC"

algorithms:
  - name: "Large-scale 2D MHD reconnection simulation"
    equation_refs: []
    external_implementations:
      - "github.com (Guo / Li group code; TODO verify exact repo)"
  - name: "Parker transport equation (SDE Monte Carlo)"
    equation_refs: ["Parker 1965 transport eq."]
    external_implementations: []
  - name: "Multi-species injection with Q/A-dependent diffusion"
    equation_refs: []
    external_implementations: []
  - name: "Power-law spectrum + E_max ∝ (Q/M)^α fit"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2408.10445"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Solves the energetic-particle transport equation over a large-scale 2D
    MHD reconnection simulation of the HCS, with multi-species (Q/A-resolved)
    injection. Produces nonthermal power-law ion distributions consistent
    with the spectral index reported by PSP, with proton high-energy cutoff
    E_max ~ 0.1-1 MeV depending on assumed diffusion coefficients; the Q/A
    scaling exponent α in E_max ∝ (Q/M)^α is α ≈ 0.4 under
    quasilinear-Kolmogorov assumption vs α ≈ 0.7 reported by PSP.
  out_of_scope:
    - "Do not extend the (Q/M)^α scaling beyond the species set the paper analyzed (TODO verify the exact species list)."
    - "Do not claim the model resolves kinetic-scale reconnection physics — it is large-scale MHD with embedded transport, complementary to kglobal."
    - "Do not treat the α discrepancy (0.4 vs 0.7) as a flaw of one side — the paper highlights it as an open issue dependent on diffusion-coefficient assumptions."
    - "Do not generalize the model to interplanetary shock acceleration — the assumed geometry is HCS reconnection."

failure_modes:
  - "Adopting a non-Kolmogorov turbulence spectrum without re-deriving the diffusion tensor changes α and E_max."
  - "Treating the MHD reconnection as a stationary background — finite-duration acceleration windows alter E_max."
  - "Using a Maxwellian-thermal seed when the actual seed is supra-thermal (or vice versa) shifts E_max by an order of magnitude."
  - "Comparing simulated to observed α without matching the species set."
  - "Misinterpreting the simulated power-law index as the *injection* index instead of the *escaped* spectrum."

depends_on:
  - "paper-desai-2024-hcs-reconnection-400kev-protons"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2408.10445"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, reconnection, mhd, transport]
---

# Compression Acceleration of Ions at the HCS — paper-skill

> Compiled from Murtas, G.; Li, X.; Guo, F. (2024), "Compression Acceleration
> of Protons and Heavier Ions at the Heliospheric Current Sheet,"
> arXiv:2408.10445.
> **Quality tier**: `stub`.

This skill is the upstream methodological anchor for HCS reconnection-driven
SEP modeling. It pairs naturally with [[paper-desai-2024-hcs-reconnection-400kev-protons]]
(near-Sun observation) and the 2026 Murtas pilot skill (extended
PSP+heavy-ion case).

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

- Setting up an MHD + transport pipeline to predict HCS-reconnection SEP
  spectra for protons + heavy ions.
- Comparing simulated (Q/M)^α scaling to PSP heavy-ion observations.
- Deciding whether merging-islands ([[paper-desai-2024-hcs-reconnection-400kev-protons]])
  or compression-acceleration (this skill) is the appropriate framework
  for a candidate event.
- Selecting a diffusion-coefficient prescription for HCS acceleration.

Do NOT use this skill when:

- The acceleration site is a shock, not reconnection — load a DSA-based
  skill instead.
- The geometry is 3D / kinetic — this skill is 2D MHD with embedded
  Parker-transport.

## 2. Paper claim → verifiable task

**Claim (narrow form).** A 2D MHD reconnecting HCS simulation, coupled with
the Parker transport equation, produces multi-species power-law ion
distributions whose spectral index is consistent with PSP observations,
with proton high-energy cutoff E_max ~ 0.1-1 MeV (depending on the assumed
diffusion coefficients). The (Q/M)^α scaling of E_max across species has
α ≈ 0.4 for quasilinear-Kolmogorov diffusion vs α ≈ 0.7 observed by PSP.

**Verifiable task.** A reproduction succeeds when an agent runs the pipeline
and emits `{γ_proton, E_max_proton, α_scaling, species_set}` matching the
paper's reported values within factor-of-2 for E_max and ±0.1 for α.

## 3. Methods / equations → executable workflow

### Large-scale 2D MHD reconnection simulation

- Paper reference: §"Model" (TODO verify section number).
- Procedure:
  1. Initialize a 2D MHD box with a Harris-like current sheet representing
     the HCS.
  2. Set plasma parameters n_p, T_p, |B|, current-sheet thickness from a
     PSP HCS context (or use the paper's defaults; TODO list defaults).
  3. Evolve MHD reconnection self-consistently; output U(x,y,t), B(x,y,t).

### Parker transport equation (SDE Monte Carlo)

- Paper reference: §"Transport equation".
- Procedure:
  1. Solve
     `df/dt = ∇·(κ∇f) − U·∇f + (1/3)(∇·U)(∂f/∂ln p) + Q_source`
     on the MHD flow + magnetic field.
  2. Use a stochastic-differential-equation Monte Carlo integrator.
  3. Inject seed particles at a chosen energy and location (typically thermal
     seed in the reconnection inflow region).

### Multi-species injection with Q/A-dependent diffusion

- Paper reference: §"Diffusion coefficients".
- Procedure:
  1. For each species (H, He, C, O, Fe — TODO verify Murtas species list),
     compute the diffusion tensor using quasilinear theory with a
     Kolmogorov magnetic power spectrum.
  2. Inject and evolve each species separately under the same MHD background.

### Power-law spectrum + E_max ∝ (Q/M)^α fit

- Paper reference: §"Results", paper figures (TODO verify figure numbers).
- Procedure:
  1. For each species, build the differential intensity vs. energy/nucleon
     spectrum after a fixed elapsed simulation time.
  2. Fit a power law in the inertial-energy range; extract spectral index γ.
  3. Identify E_max (rollover / cutoff).
  4. Fit log(E_max) vs log(Q/M) across species; extract α.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| PSP/ISʘIS (reference for spectral comparison) | L2/L3 | event-integrated | HCS-crossing events | CDAWeb / PSP SOC | general-purpose: WebFetch + cdflib |

The MHD + SDE codes are research codes. Treat their execution as a separate
HPC job with no MCP binding asserted.

## 5. Validation target → benchmark artifact

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires either (a) re-running the simulation with the paper's parameters
and reproducing Figure (TODO verify) within tolerance, or (b) reproducing
the (Q/M)^α plot end-to-end on synthetic inputs.

## 6. Failure modes → skill memory

- Non-Kolmogorov turbulence spectrum changes the diffusion-tensor prescription
  and shifts α.
- Stationary-background MHD assumption underestimates effective acceleration
  time.
- Seed-population choice (Maxwellian vs supra-thermal) shifts E_max by an
  order of magnitude.
- α-comparison only valid across matched species sets.
- Simulated power-law is for accelerated spectrum at the simulation
  diagnostic surface — observed power-law has transport modifications;
  compare carefully.

## 7. Claim boundary

**In scope.** 2D MHD reconnecting HCS with Parker-transport-equation
multi-species acceleration; proton E_max ~ 0.1-1 MeV; α ≈ 0.4 under
quasilinear-Kolmogorov assumption.

**Out of scope — do NOT generalize beyond:**

- Kinetic / first-principles reconnection physics.
- Shock acceleration.
- Non-HCS reconnection sites.
- Species not in the paper's analysis set.

If a downstream task wants a kinetic-PIC-level statement, refuse and route
to a PIC-based skill (TODO: identify or create).

## 8. Links

- DOI: n/a (in-press at writing) — TODO add at promotion
- arXiv: https://arxiv.org/abs/2408.10445
- ADS: n/a — TODO add at promotion
- Code: n/a — TODO verify Guo/Li group public repo
- Data: n/a — purely simulation paper

## 9. Skill graph → depends_on

- `[[paper-desai-2024-hcs-reconnection-400kev-protons]]` — companion PSP
  observation that motivates the model and provides the α ≈ 0.7 observational
  benchmark.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Tension (α_model ≈ 0.4 vs α_obs ≈ 0.7).** The central numerical
  gap. New hypothesis: the discrepancy reflects (i) under-resolved
  kinetic scales in 2D MHD, (ii) wrong diffusion-tensor prescription,
  or (iii) missing merging-island stage from [[paper-desai-2024-hcs-
  reconnection-400kev-protons]]. Each is independently testable;
  ranking them is a research question this skill enables.
- **Gap (3D extension).** All quoted results are 2D MHD. A 3D run
  with the same initial conditions has not been published. Compose
  with the runtime-2026 sibling [[paper-murtas-2026-hcs-
  reconnection-ion-energization]] (which extends the same group's
  pipeline) to write a 2D-vs-3D comparison skill.
- **Experiment (PSP HCS sweep).** Run the pipeline across the Desai
  2024 HCS-crossing list with crossing-specific initial conditions,
  not a fixed configuration. Predict per-crossing spectra; compare
  to PSP/ISʘIS measurements.
- **New hypothesis (composition diagnostic).** Predicted (Q/A)^α
  scaling for heavy ions is a coronal-seed-composition diagnostic.
  Composing with FIP-bias diagnostics ([[paper-reames-2026-physics-
  of-seps]]) yields a model-data closure test.

## Notes

The α ≈ 0.4 (model) vs ≈ 0.7 (PSP) tension is the paper's key open
question. A future skill could compare diffusion-coefficient prescriptions
to close the gap; flag for follow-up.
