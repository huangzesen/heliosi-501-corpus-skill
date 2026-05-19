---
name: nayak-2024-coronal-null-extrapolation-generation-annihilation
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# nayak-2024-coronal-null-extrapolation-generation-annihilation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when cataloguing 3-D magnetic-null generation/annihilation events in NLFFF + PFSS sequences.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Generation and Annihilation of Three-Dimensional Magnetic Nulls in Extrapolated Solar Coronal Magnetic Field
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2404.12034 (posted 2024-04-18)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

3-D null pair generation/annihilation in NLFFF+PFSS extrapolations follows a statistically robust rate set by AR flux-emergence cadence, with isolated null lifetimes consistent with reconnection-event durations.

### Method assumptions

- Null detection is converged at the chosen grid.
- Null lifetimes are robust to small parameter perturbations.

### Data assumptions

- HMI vector + LoS Br time series.
- Synoptic Br for PFSS.

### Failure modes (skill memory)

- Null counts depend on resolution.
- AR-edge nulls are spurious if NLFFF boundary is unstable.

### Figure / numerical targets

- Null-generation/annihilation rate vs flux-emergence.
- Null-lifetime distribution.

### Claim boundary

**In scope.** Studied AR sequences.

**Out of scope — do NOT generalize:**

- Do NOT cite null statistics without grid resolution and NLFFF boundary preparation.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_hmi_vector()` | HMI vector |  |
| `pfss.solve()` | background |  |
| `nlfff.solve()` | AR volume |  |
| `topology.identify_nulls_3d()` | null catalog |  |
| `topology.track_null_lifetime()` | lifetime tracker |  |

### Procedure

1. Solve PFSS+NLFFF time sequence.
2. Identify 3-D nulls at each step.
3. Track null lifetimes.
4. Correlate with flux-emergence.

### Validation target

Reproduce null-rate vs flux-emergence relation.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; NLFFF code paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-mackay-2026-tracking-magnetic-topology-change-corona]] for a unified null+separator topology timeline.
- Generative hypothesis: null-rate fingerprints sympathetic-flare preferred separations.

---

## Skill graph → depends_on

- [[paper-mackay-2026-tracking-magnetic-topology-change-corona]]
- [[paper-flare-precursor-fine-scale-topology-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2404.12034
- arXiv HTML: https://arxiv.org/html/2404.12034
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- null detection algorithm
- grid resolution
