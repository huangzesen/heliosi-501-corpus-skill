---
name: paper-kouloumvakos-2026-iva-shock-properties
description: >-
  Use when interpreting "nose-shaped" SEP energy spectrograms where high-
  energy particles arrive later than mid-energy ones (inverse velocity
  arrival; IVA) — Kouloumvakos+ 2026 (arXiv:2604.13962) link IVA to the
  evolving 3D shock geometry along the connected field line: connectivity
  starts on weak flanks of CME-driven shocks and shifts toward stronger
  shock apex, producing delayed high-energy arrivals consistent with
  time-dependent diffusive shock acceleration.
version: 0.1.0
kind: paper-skill
quality: stub

paper:
  title: "Shock properties for solar energetic particle events with signatures of inverse velocity arrival"
  first_author: "Kouloumvakos, A."
  authors:
    - "Kouloumvakos, A."
    - "Lario, D."
    - "Mason, G. M."
    - "Vourlidas, A."
    - "Allen, R. C."
    - "Wijsen, N."
  year: 2026
  venue: "Journal — TODO verify"
  doi: null
  arxiv_id: "2604.13962"
  ads_bibcode: null

domain:
  primary_theme: energetic_particles
  secondary_themes:
    - cme-driven-shocks
    - inverse-velocity-arrival
    - 3d-shock-reconstruction
    - diffusive-shock-acceleration
    - magnetic-connectivity
  missions: [PSP, "Solar Orbiter"]
  regime: [inner-heliosphere]

trigger_keywords:
  - "inverse velocity arrival"
  - "IVA"
  - "nose-shaped spectrogram"
  - "CME-driven shock"
  - "shock 3D reconstruction"
  - "magnetic connectivity"
  - "diffusive shock acceleration"
  - "time-dependent DSA"
  - "shock flank"
  - "shock apex"
  - "delayed high-energy arrival"
  - "transition energy"

data_products:
  - instrument: "SO/EPD (SIS, HET, EPT, STEP)"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "26 IVA-SEP events 2018-2025 (TODO verify event list)"
    archive: "SOAR"
  - instrument: "PSP/ISʘIS EPI-Lo + EPI-Hi"
    level: "L2/L3"
    cadence: "instrument-native"
    interval: "subset of IVA events"
    archive: "NASA CDAWeb / PSP SOC"
  - instrument: "Coronagraph (LASCO, STEREO/SECCHI, SO/Metis)"
    level: "L1"
    cadence: "instrument-native"
    interval: "associated CMEs"
    archive: "various (LASCO, STEREO SC, ESA SO archive)"
  - instrument: "Coronal MHD model output (TODO verify exact model)"
    level: "derived"
    cadence: "snapshot per event"
    interval: "per event"
    archive: "model-team archive"

algorithms:
  - name: "IVA event identification + transition-energy extraction"
    equation_refs: []
    external_implementations: []
  - name: "3D shock-front reconstruction from coronagraph imagery"
    equation_refs: []
    external_implementations: []
  - name: "Connected-field-line tracing through coronal MHD"
    equation_refs: []
    external_implementations: []
  - name: "Shock-strength profile along connectivity (flank → apex)"
    equation_refs: []
    external_implementations: []
  - name: "Time-dependent DSA consistency check"
    equation_refs: []
    external_implementations: []

validation_target: null

links:
  doi_url: null
  arxiv_url: "https://arxiv.org/abs/2604.13962"
  ads_url: null
  code_repo: null
  data_repo: null

claim_boundary:
  scope: >-
    Analyzes 26 SEP events 2018-2025 observed by Solar Orbiter and Parker
    Solar Probe that show inverse velocity arrival (IVA) — high-energy
    particles arrive after mid-energy ones. Reconstructs the 3D CME-driven
    shock front and uses kinematic modeling + coronal MHD to derive shock
    parameters along magnetic-connectivity field lines. Concludes the IVA
    signature reflects the spatial and temporal evolution of shock
    properties as connectivity shifts from weak flanks toward stronger
    apex, with a correlation between transition energy at which IVA
    begins and shock speed along the connected line, consistent with
    time-dependent diffusive shock acceleration.
  out_of_scope:
    - "Do not extend the IVA-as-shock-evolution interpretation to events without 3D shock reconstruction."
    - "Do not generalize the transition-energy vs shock-speed correlation across acceleration mechanisms outside DSA."
    - "Do not infer source connectivity from spacecraft position alone — the paper relies on coronal MHD."
    - "Do not assert IVA implies shock acceleration in every event — instrumental and transport effects are co-listed by Xu+ 2026 ([[paper-xu-2026-psp-iva-sep-events]])."

failure_modes:
  - "Coronagraph 3D reconstruction depends on viewing geometry — single-vantage events are less reliable."
  - "Coronal MHD model choice affects connectivity; report the model and run."
  - "Transition-energy fitting depends on the IVA-detection method; document the contour-line / intensity-threshold algorithm."
  - "Instrumental sensitivity at low energies can spoof IVA — cross-check with multiple energy ranges."
  - "Magnetic-connectivity field lines drift in time; report the time-of-acceleration vs time-of-observation lag."

depends_on:
  - "paper-xu-2026-psp-iva-sep-events"
  - "paper-trotta-2025-ip-shock-variability-multi-spacecraft"
  - "paper-reames-2026-physics-of-seps"

provenance:
  generated_by: "HelioSI paper-to-skill factory @ 2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json#arxiv:2604.13962"
  verified_by: null
  verified_at: null

tags: [heliophysics, paper-skill, sep, shock, iva]
---

# Inverse-Velocity-Arrival Shock Properties — paper-skill

> Compiled from Kouloumvakos, A.; Lario, D.; Mason, G. M.; Vourlidas, A.;
> Allen, R. C.; Wijsen, N. (2026), "Shock properties for solar energetic
> particle events with signatures of inverse velocity arrival,"
> arXiv:2604.13962.
> **Quality tier**: `stub`.

This skill compiles the link between observed "nose-shaped" IVA
spectrograms and the time-and-space evolving CME-driven shock geometry
along the connected magnetic field line. It pairs with
[[paper-xu-2026-psp-iva-sep-events]] (PSP IVA event catalog).

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

- A PSP/SO SEP event shows a nose-shaped intensity spectrogram (IVA).
- Asking why high-energy particles arrive delayed relative to mid-energy.
- Linking IVA signatures to CME-driven-shock geometry and time-dependent
  DSA.
- Pulling 3D shock-front reconstruction into any downstream pipeline (e.g., a HelioSI / Claude Code workflow — example adapter).

Do NOT use this skill when:

- The IVA signature is suspected to be transport- or instrument-driven
  only — load [[paper-xu-2026-psp-iva-sep-events]] for the broader IVA
  catalog and per-event diagnostic checklist.
- The event has no CME-driven shock context.

## 2. Paper claim → verifiable task

**Claim (narrow form).** For 26 IVA-SEP events 2018-2025 observed by SO
and PSP, 3D shock-front reconstruction + coronal-MHD-derived connectivity
shows that the spacecraft's connected field line samples weak shock
flanks at event onset and stronger apex regions later. This evolution
produces delayed high-energy arrivals and progressive spectral
hardening. The transition energy at which IVA begins correlates with the
shock speed along the connected line, consistent with time-dependent DSA.

**Verifiable task.** A reproduction succeeds when an agent, for each of
the 26 events (TODO verify list), emits `{transition_energy, shock_speed_
along_connectivity, flank_vs_apex_label}` and reproduces the transition-
energy vs shock-speed correlation within ±20%.

## 3. Methods / equations → executable workflow

### IVA event identification + transition-energy extraction

- Procedure:
  1. Load SO/EPD or PSP/ISʘIS energy-time spectrograms across the event.
  2. Apply the contour-line / intensity-threshold detector for the "nose"
     structure (TODO verify exact threshold from full text).
  3. Extract the transition energy at which IVA begins.

### 3D shock-front reconstruction from coronagraph imagery

- Procedure:
  1. Combine LASCO + STEREO/SECCHI (+ SO/Metis when available)
     coronagraph imagery.
  2. Apply ellipsoid / GCS fit (TODO verify which method) to recover the
     3D shock front.
  3. Propagate the shock front using a kinematic CME model.

### Connected-field-line tracing through coronal MHD

- Procedure:
  1. Use a coronal MHD model (TODO verify model name; candidates: ENLIL,
     EUHFORIA, MAST/Predictive Science) to obtain the global magnetic
     field topology.
  2. Trace the field line from each spacecraft's footpoint to the corona.
  3. Identify the shock-front intersection point on the connected line.

### Shock-strength profile along connectivity (flank → apex)

- Procedure:
  1. Along the connected line, evaluate shock speed, obliquity, Mach
     number using the kinematic + MHD model.
  2. Tabulate strength evolution from flank to apex.

### Time-dependent DSA consistency check

- Procedure:
  1. Compute expected DSA cutoff energy vs time given shock speed and
     diffusion-coefficient prescription.
  2. Compare to observed transition energy and IVA onset time.

## 4. Data / instruments → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Fetch hint |
|------------|-------|---------|----------|---------|------------|
| SO/EPD (SIS, HET, EPT, STEP) | L2/L3 | instrument-native | IVA events 2018-2025 | SOAR | general-purpose: WebFetch + SOAR API |
| PSP/ISʘIS EPI-Lo + EPI-Hi | L2/L3 | instrument-native | subset | CDAWeb / PSP SOC | general-purpose |
| LASCO + STEREO/SECCHI + SO/Metis | L1 | instrument-native | associated CMEs | various | general-purpose |
| Coronal MHD model output | derived | per event | per event | model-team | TODO verify access path |

## 5. Validation target → benchmark artifact

Not benchmarked yet. Promotion to `executable` requires the IVA-detection
threshold, coronal-MHD model identity, and event list (all TODO verify),
and reproduction of the transition-energy vs shock-speed correlation
plot within tolerance.

## 6. Failure modes → skill memory

- Single-vantage coronagraph reconstruction is unreliable — require
  multi-view.
- Coronal-MHD model identity and run snapshot must be reported.
- IVA-detection threshold sensitivity sweep is essential.
- Instrumental sensitivity at low energies can spoof IVA.
- Connectivity drifts in time — record acceleration-vs-observation lag.

## 7. Claim boundary

**In scope.** 26 IVA-SEP events 2018-2025 observed by SO + PSP; 3D shock
reconstruction; connectivity-along-shock evolution from flank to apex;
transition-energy vs shock-speed correlation; time-dependent DSA
consistency.

**Out of scope — do NOT generalize beyond:**

- IVA events without 3D shock reconstruction.
- Non-DSA acceleration mechanisms.
- Spacecraft-position-only connectivity claims.
- Universal IVA-as-shock-evolution interpretation (Xu+ 2026 catalogs
  competing mechanisms).

If a downstream task wants a per-event mechanism diagnosis, refuse and
route to [[paper-xu-2026-psp-iva-sep-events]] for the broader checklist.

## 8. Links

- DOI: n/a — TODO add at promotion
- arXiv: https://arxiv.org/abs/2604.13962
- ADS: n/a — TODO add at promotion
- Code: n/a
- Data: SOAR + CDAWeb + coronagraph archives

## 9. Skill graph → depends_on

- `[[paper-xu-2026-psp-iva-sep-events]]` — PSP IVA event catalog and
  diagnostic checklist (companion).
- `[[paper-trotta-2025-ip-shock-variability-multi-spacecraft]]` — shock-
  evolution variability framing.
- `[[paper-reames-2026-physics-of-seps]]` — places IVA in the broader
  SEP-acceleration narrative.

## 10. Research-generation affordances (harness-agnostic)

When this paper-skill is composed with prior skills in the corpus, it enables the following research moves. These are *seeds*, not claims — they fall outside the original paper's `claim_boundary.scope` and require new work to land.

- **Gap (IVA mechanism uniqueness).** Time-dependent DSA at a
  connectivity-evolving shock is *one* IVA explanation; transport
  effects in turbulent heliosphere ([[paper-laitinen-2026-vda-
  turbulent-heliosphere]]) is another. No paper-skill yet emits a
  per-event mechanism-likelihood vector. Compose with [[paper-xu-
  2026-psp-iva-sep-events]] and [[paper-laitinen-2026-vda-turbulent-
  heliosphere]] to write one.
- **Tension (transition-energy vs shock-speed correlation).** The
  paper reports the correlation; its slope and intercept are
  diagnostics of the diffusion coefficient. New hypothesis:
  fitting the correlation across the IVA catalog yields a κ_‖(p)
  prescription distinct from quasi-linear theory. Composes with
  [[paper-laitinen-2026-vda-turbulent-heliosphere]] (turbulence
  prescription) for theory comparison.
- **Experiment (cross-mission IVA atlas).** Extend the 26-event
  list with all PSP IVA events from [[paper-xu-2026-psp-iva-sep-
  events]] (14 events) and any SO/HET-only events; build a
  ~40-event atlas with consistent shock reconstruction.
- **New hypothesis (operational IVA-forecast).** Connectivity-
  evolution prediction can be turned into an IVA-onset-time
  forecast given a fast/wide CME — composes with operational SEP-
  forecast pipelines.

## Notes

The paper's main contribution is the *connectivity-evolution* explanation
for IVA, distinguishing it from purely transport-based or instrumental
explanations. Be careful not to overgeneralize this as a unique mechanism.
