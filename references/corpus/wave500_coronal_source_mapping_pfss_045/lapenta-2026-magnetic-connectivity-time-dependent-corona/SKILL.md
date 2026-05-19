# lapenta-2026-magnetic-connectivity-time-dependent-corona

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when handling magnetic-connectivity evolution on day-to-hour timescales, where steady PFSS is insufficient and a time-dependent coronal model is required.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Magnetic Connectivity in the Time-Dependent Corona and Heliosphere
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2026
- **arXiv:** 2603.22440 (posted 2026-03-23)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A time-dependent coronal/heliospheric model produces connectivity sequences whose discontinuities (rapid footpoint jumps) coincide with reconnection events identified in EUV / in-situ — a behaviour invisible to single-CR PFSS.

### Method assumptions

- Time-dependent model is converged on relevant sub-day cadence.
- Connectivity jumps are robust to small parameter perturbations.

### Data assumptions

- High-cadence magnetogram driver (HMI 720s / vector).
- Reference PFSS snapshots for comparison.

### Failure modes (skill memory)

- Driver-cadence vs internal timestep mismatch.
- PFSS snapshots may falsely smooth real jumps.

### Figure / numerical targets

- Footpoint-trajectory time series with jumps annotated.
- Connectivity discontinuity vs EUV reconnection event.

### Claim boundary

**In scope.** The paper's window + time-dependent model.

**Out of scope — do NOT generalize:**

- Do NOT cite the discontinuity correspondence outside the validated event sample.
- Do NOT replace steady PFSS with the time-dependent model where convergence is not demonstrated.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_high_cadence()` | HMI 720s |  |
| `coronal.time_dependent_solve()` | time-dependent model |  |
| `connectivity.trace_footpoint()` | footpoint over time |  |
| `imagery.fetch_aia()` | reconnection-event imagery |  |
| `pfss.solve()` | steady-PFSS comparison |  |

### Procedure

1. Drive time-dependent model with HMI 720s.
2. Trace footpoint trajectories for observers of interest.
3. Mark discontinuities; correlate with EUV reconnection events.
4. Compare to steady-PFSS-snapshot footpoints.

### Validation target

Reproduce the discontinuity–event correspondence.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss for steady-PFSS reference; time-dependent code is paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-mackay-2026-tracking-magnetic-topology-change-corona]] for a unified topology-change tracking framework.
- Generative hypothesis: discontinuities classified by amplitude predict switchback occurrence at PSP ([[paper-raouafi-2025-switchback-coronal-jet-precursors]]).

---

## Skill graph → depends_on

- [[paper-mackay-2026-tracking-magnetic-topology-change-corona]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2603.22440
- arXiv HTML: https://arxiv.org/html/2603.22440
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- time-dependent code identity
