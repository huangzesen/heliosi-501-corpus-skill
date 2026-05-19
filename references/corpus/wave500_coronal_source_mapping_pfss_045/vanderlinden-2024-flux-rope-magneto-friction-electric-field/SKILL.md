---
name: vanderlinden-2024-flux-rope-magneto-friction-electric-field
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# vanderlinden-2024-flux-rope-magneto-friction-electric-field

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when forming + erupting a flux rope in a magneto-friction model driven by time-dependent E-field boundary inversion, with PFSS as the global background.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Simulating the Formation and Eruption of Flux Rope by Magneto-Friction Model Driven by Time-Dependent Electric Field
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2409.14045 (posted 2024-09-21)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A magneto-friction simulation driven by inverted time-dependent E-fields forms and erupts a flux rope at the observed timing, with PFSS embedding providing the open–closed exterior topology.

### Method assumptions

- E-field inversion from B is uniquely defined up to gauge.
- Magneto-friction converges to the relevant force-free state.

### Data assumptions

- HMI vector Br time series.
- AIA EUV for eruption observation.
- Synoptic Br for PFSS.

### Failure modes (skill memory)

- E-field gauge choice changes flux-rope buildup rate.
- PFSS exterior is too coarse for fine eruption morphology.

### Figure / numerical targets

- Flux-rope buildup vs time.
- Eruption-onset comparison with AIA.

### Claim boundary

**In scope.** The simulated AR event.

**Out of scope — do NOT generalize:**

- Do NOT cite onset-time independent of the E-field gauge.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_hmi_vector()` | HMI vector |  |
| `efield.invert_from_b()` | E-field inversion | gauge choice |
| `mhd.magneto_friction_run()` | MF run |  |
| `pfss.solve()` | background |  |
| `imagery.fetch_aia()` | AIA EUV |  |

### Procedure

1. Invert E-field from HMI B-evolution.
2. Drive magneto-friction simulation.
3. Embed in PFSS background.
4. Compare eruption-onset to AIA.

### Validation target

Match eruption-onset time.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; MF code paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-ross-2025-data-constrained-mhd-filament-eruption]] for an MHD-vs-MF comparison framework.
- Generative hypothesis: E-field gauge tracking should fingerprint which CRs are eligible for [[paper-multi-constraint-pfss-extrapolation-model]] loop augmentation.

---

## Skill graph → depends_on

- [[paper-ross-2025-data-constrained-mhd-filament-eruption]]
- [[paper-flare-precursor-fine-scale-topology-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2409.14045
- arXiv HTML: https://arxiv.org/html/2409.14045
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- gauge convention
- MF code
