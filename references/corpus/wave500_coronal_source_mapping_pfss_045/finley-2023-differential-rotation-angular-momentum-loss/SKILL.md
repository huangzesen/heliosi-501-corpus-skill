---
name: finley-2023-differential-rotation-angular-momentum-loss
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# finley-2023-differential-rotation-angular-momentum-loss

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when including differential rotation in angular-momentum-loss-rate calculations on top of PFSS-derived open-flux maps.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Accounting for Differential Rotation in Calculations of the Sun's Angular Momentum-Loss Rate
- **First author:** A. J. Finley
- **Authors:** A. J. Finley, TODO_verify
- **Year:** 2023
- **arXiv:** 2302.12700 (posted 2023-02-24)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Differential rotation modifies the inferred angular-momentum-loss rate by a measurable fraction relative to rigid-rotation assumptions, when paired with PFSS-derived open-flux maps.

### Method assumptions

- Differential-rotation profile is well-characterized.
- Open-flux map is consistent with the rotation profile.

### Data assumptions

- Synoptic Br + PFSS open-flux map.
- Rotation profile from helioseismology or surface tracers.

### Failure modes (skill memory)

- Rotation-profile uncertainty propagates into the loss-rate.
- PFSS R_ss sets the open-flux baseline.

### Figure / numerical targets

- Loss-rate vs differential vs rigid rotation.
- Latitude-resolved loss-rate density.

### Claim boundary

**In scope.** The studied cycle window.

**Out of scope — do NOT generalize:**

- Do NOT cite differential-rotation correction outside the studied latitude band.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `rotation.differential_profile()` | rotation profile |  |
| `pfss.solve()` | open-flux map |  |
| `torque.with_diff_rotation()` | loss-rate calc |  |

### Procedure

1. Fetch rotation profile.
2. Solve PFSS; obtain open-flux map.
3. Compute loss-rate with and without differential rotation.
4. Tabulate the differential correction.

### Validation target

Reproduce the differential vs rigid correction.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; rotation profile via paper-specific source.

---

## Layer 4 — Research-generation affordances

- Compose with [[ervin-2025-alfven-surface-wind-braking-psp]] for differential-rotation effects in the Alfvén-surface wind-braking estimate.
- Generative hypothesis: differential-rotation corrections rank-correlate with the equatorial-dipole share of OSF ([[tahtinen-2026-dipole-flux-transport-open-flux]]).

---

## Skill graph → depends_on

- [[ervin-2025-alfven-surface-wind-braking-psp]]
- [[tahtinen-2026-dipole-flux-transport-open-flux]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2302.12700
- arXiv HTML: https://arxiv.org/html/2302.12700
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- rotation-profile source
- headline correction magnitude
