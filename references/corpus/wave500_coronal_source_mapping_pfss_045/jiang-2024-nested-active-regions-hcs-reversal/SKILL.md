---
name: jiang-2024-nested-active-regions-hcs-reversal
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# jiang-2024-nested-active-regions-hcs-reversal

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when explaining HCS-reversal stalls during cycle maximum by anchoring at *nested* active-region complexes, identifiable by PFSS+SFT modelling.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Nested Active Regions Anchor the Heliospheric Current Sheet and Stall the Reversal of the Coronal Magnetic Field
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2410.18244 (posted 2024-10-23)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Nested-AR emergence anchors the HCS at preferred longitudes and stalls polar-field reversal — operationally identifiable via PFSS HCS contours and SFT-driven polar-field tracking.

### Method assumptions

- Nested ARs are identifiable in HMI synoptic Br.
- PFSS HCS is a meaningful proxy for in-situ HCS anchor longitude.
- SFT correctly evolves polar field given the BMR catalog.

### Data assumptions

- HMI synoptic Br across the studied maximum.
- BMR/AR catalog with emergence locations.

### Failure modes (skill memory)

- AR catalog completeness varies; missing ARs erase the anchor.
- PFSS HCS is sensitive to R_ss.
- SFT meridional-flow knob changes the reversal-stall claim.

### Figure / numerical targets

- PFSS HCS longitude vs time.
- Polar field vs time with stall windows.
- Nested-AR overlay on HCS contour.

### Claim boundary

**In scope.** Cycle-maximum interval studied in the paper.

**Out of scope — do NOT generalize:**

- Do NOT extend to cycle minima.
- Do NOT cite the anchor mechanism for isolated single ARs.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | HMI synoptic Br |  |
| `ar.identify_nested()` | nested-AR catalog |  |
| `pfss.solve()` | PFSS |  |
| `hcs.extract()` | HCS contour |  |
| `sft.polar_field()` | polar-field time series |  |

### Procedure

1. Build nested-AR catalog over the cycle window.
2. Solve PFSS per CR; extract HCS contour.
3. Run SFT for polar-field evolution.
4. Correlate nested-AR longitude with HCS-stall longitude.

### Validation target

Reproduce the longitude-locked HCS stalls.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; SFT is paper-internal.

---

## Layer 4 — Research-generation affordances

- Compose with [[yoshida-2026-sunspot-evolution-open-flux-cycle24-max]]: AR 12192 nested-AR effects vs OSF rise.
- Generative hypothesis: anchor longitudes should leave a fingerprint on sympathetic flares ([[milligan-2024-flares-sympathetic-angular-separation]]).

---

## Skill graph → depends_on

- [[yoshida-2026-sunspot-evolution-open-flux-cycle24-max]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2410.18244
- arXiv HTML: https://arxiv.org/html/2410.18244
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- nested-AR definition
- SFT parameters
