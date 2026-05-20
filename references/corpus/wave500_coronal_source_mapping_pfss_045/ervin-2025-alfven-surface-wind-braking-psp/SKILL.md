---
name: ervin-2025-alfven-surface-wind-braking-psp
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# ervin-2025-alfven-surface-wind-braking-psp

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when reconstructing the global Alfvén surface from PSP in-situ data and tying it to an angular-momentum-loss / wind-braking torque, with PFSS-derived open flux as a global constraint.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Reconstructing the Sun's Alfvén Surface and Wind-Braking Torque with Parker Solar Probe
- **First author:** TODO_verify
- **Authors:** TODO_verify (PSP/FIELDS team)
- **Year:** 2025
- **arXiv:** 2509.07088 (posted 2025-09-08)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

PSP perihelion crossings constrain a 3-D Alfvén surface whose associated wind-braking torque is consistent with a PFSS-derived open-flux budget — yielding a torque estimate that agrees with previous solar-cycle averages within the paper's stated uncertainty.

### Method assumptions

- Sub-Alfvénic intervals are correctly identified at PSP.
- Alfvén surface is reconstructible by combining sub-Alfvénic boundaries with a coronal field model.
- PFSS provides a reliable open-flux normalization.

### Data assumptions

- PSP FIELDS + SWEAP for plasma + B over multiple encounters.
- Synoptic Br for the relevant CRs.

### Failure modes (skill memory)

- Sub-Alfvénic interval boundaries depend on density estimator (QTN vs SPC); cross-check.
- Open-flux normalization carries the PFSS-vs-in-situ OSF gap.
- Wind-braking torque depends on the latitudinal-profile extrapolation.

### Figure / numerical targets

- PSP perihelion crossings on the reconstructed Alfvén surface.
- Wind-braking torque vs cycle phase.
- Open-flux budget reconciliation panel.

### Claim boundary

**In scope.** PSP encounters covered by the paper and its PFSS choice.

**Out of scope — do NOT generalize:**

- Do NOT extend the torque estimate beyond the latitude range actually constrained by PSP.
- Do NOT cite Alfvén-surface heights independent of the underlying open-flux normalization.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `psp.fields_b()` | PSP MAG/SCM B | burst+survey |
| `psp.sweap_n_v()` | PSP plasma | SPC/SPAN-I |
| `alfven.identify_subalfvenic()` | sub-Alfvénic intervals | Mach criterion |
| `surface.reconstruct()` | 3-D Alfvén surface | smoothing knob |
| `pfss.solve()` | open-flux normalization |  |
| `torque.wind_braking()` | compute angular-momentum loss |  |

### Procedure

1. Identify PSP sub-Alfvénic intervals.
2. Fit a smooth 3-D Alfvén surface to crossings.
3. Solve PFSS; obtain open-flux normalization.
4. Integrate wind-braking torque from the surface and the OSF.
5. Compare to long-baseline torque estimates.

### Validation target

Reproduce the paper's torque value within uncertainty.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss for the PFSS step; pyspedas / sunpy for PSP data access. PSP intervals can be loaded via .library/custom/psp-data-analysis/.

---

## Layer 4 — Research-generation affordances

- Tension with [[finley-2023-differential-rotation-angular-momentum-loss]] — does differential rotation matter at PSP-relevant latitudes?
- Compose with [[kasper-2021-psp-enters-magnetically-dominated-corona]] — sub-Alfvénic crossings vs OSF normalization.

---

## Skill graph → depends_on

- [[kasper-2021-psp-enters-magnetically-dominated-corona]]
- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[finley-2023-differential-rotation-angular-momentum-loss]]

## Links

- arXiv: https://arxiv.org/abs/2509.07088
- arXiv HTML: https://arxiv.org/html/2509.07088
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- exact sub-Alfvénic interval list
- OSF normalization
- DOI
