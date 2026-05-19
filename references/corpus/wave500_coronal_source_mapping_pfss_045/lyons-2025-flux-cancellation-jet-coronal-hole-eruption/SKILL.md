# lyons-2025-flux-cancellation-jet-coronal-hole-eruption

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when interpreting CH-jet onsets via flux-cancellation in flux-emergence MHD simulations, with PFSS framing the global ambient.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Magnetic Flux Cancellation in a Flux-Emergence MHD Simulation of Coronal-Hole Eruptions and Jets
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2505.21155 (posted 2025-05-27)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

In flux-emergence MHD CH simulations, flux cancellation at the polarity-inversion line drives jet onset on a timescale set by the cancellation rate — a behaviour reproducible from observed Br evolution with PFSS providing the ambient field.

### Method assumptions

- Flux-emergence + cancellation can be parameterized from HMI.
- PFSS ambient is consistent with the simulation domain.

### Data assumptions

- HMI Br + vector at the CH-jet site.
- Synoptic Br for PFSS.
- AIA EUV for jet observation.

### Failure modes (skill memory)

- Cancellation rate estimate is grid-dependent.
- PFSS ambient mismatches simulation boundary.

### Figure / numerical targets

- Jet onset vs cancellation-rate scatter.
- Simulated vs observed AIA jet kinematics.

### Claim boundary

**In scope.** The simulated parameter range.

**Out of scope — do NOT generalize:**

- Do NOT extend the onset-time scaling outside the simulated cancellation-rate range.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_hmi()` | HMI |  |
| `flux.cancellation_rate()` | cancellation diagnostic |  |
| `mhd.flux_emergence_run()` | FE MHD |  |
| `pfss.solve()` | ambient |  |
| `imagery.fetch_aia()` | EUV jet |  |

### Procedure

1. Estimate cancellation rate from HMI evolution.
2. Drive MHD FE simulation.
3. Use PFSS as ambient.
4. Compare simulated jet kinematics to AIA.

### Validation target

Onset-time vs cancellation-rate scaling.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; MHD code paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-raouafi-2025-switchback-coronal-jet-precursors]] for a jet-onset → switchback-precursor causal chain.
- Generative hypothesis: cancellation-rate distribution across PSP encounter footpoints should predict switchback occurrence.

---

## Skill graph → depends_on

- [[paper-raouafi-2025-switchback-coronal-jet-precursors]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2505.21155
- arXiv HTML: https://arxiv.org/html/2505.21155
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- MHD code
- cancellation-rate estimator
