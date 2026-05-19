# mackay-2026-tracking-magnetic-topology-change-corona

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when explicitly *tracking* magnetic-topology change (skeleton, separators, nulls) in a time-dependent coronal model, not just at single snapshots.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Tracking Magnetic Topological Change in a Time-Dependent Coronal Model
- **First author:** D. H. Mackay
- **Authors:** D. H. Mackay, TODO_verify
- **Year:** 2026
- **arXiv:** 2604.21639 (posted 2026-04-23)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A skeleton-based tracking algorithm follows nulls and separators continuously through a time-dependent simulation, exposing reconnection-driven topology changes that snapshot-PFSS analyses miss.

### Method assumptions

- Skeleton extraction is converged at the chosen grid.
- Topology-change events can be timestamped from skeleton evolution.

### Data assumptions

- Time-dependent coronal-field run.
- Validation snapshots from PFSS or NLFFF.

### Failure modes (skill memory)

- Null detection is sensitive to numerical noise.
- Separator continuity can break at coarse cadence.

### Figure / numerical targets

- Null-trajectory over time.
- Separator-cluster topology-change timeline.

### Claim boundary

**In scope.** The simulation interval studied.

**Out of scope — do NOT generalize:**

- Do NOT extend the topology-tracking framework to coarse-cadence snapshots.
- Do NOT cite null-count statistics outside the validated resolution.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `coronal.time_dependent_solve()` | time-dependent run |  |
| `topology.skeleton_extract()` | skeleton + nulls + separators |  |
| `topology.track_through_time()` | continuous tracking |  |
| `pfss.solve()` | validation snapshot |  |

### Procedure

1. Run time-dependent simulation.
2. Extract skeleton at each step.
3. Track nulls / separators continuously.
4. Validate against PFSS or NLFFF snapshots.

### Validation target

Match null/separator counts at validation snapshots.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- Time-dependent code is paper-specific; sunkit-magex.pfss for validation.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-lapenta-2026-magnetic-connectivity-time-dependent-corona]] for a unified topology+connectivity framework.
- Generative hypothesis: topology-change rate should correlate with sympathetic-flare angular-separation peaks ([[paper-milligan-2024-flares-sympathetic-angular-separation]]).

---

## Skill graph → depends_on

- [[paper-lapenta-2026-magnetic-connectivity-time-dependent-corona]]

## Links

- arXiv: https://arxiv.org/abs/2604.21639
- arXiv HTML: https://arxiv.org/html/2604.21639
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- skeleton-extraction code
