---
name: prasad-2026-blowout-jet-magnetic-topology
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# prasad-2026-blowout-jet-magnetic-topology

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when relating an AR blowout-jet trigger to a PFSS+NLFFF magnetic-topology configuration (fan-spine, nulls, QSLs).

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Investigation of Magnetic Topology and Triggering Mechanisms of a C-Class Flare and Active-Region Blowout Jet
- **First author:** A. Prasad
- **Authors:** A. Prasad, TODO_verify
- **Year:** 2026
- **arXiv:** 2602.01742 (posted 2026-02-02)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

The studied blowout-jet onset is triggered at a fan-spine null identified by PFSS+NLFFF, with QSLs aligning with the observed jet base — a topology that recurs in a paper-identified subclass of blowout jets.

### Method assumptions

- Fan-spine null is robust to small NLFFF perturbations.
- QSL extraction is reproducible.

### Data assumptions

- HMI vector + LoS Br.
- AIA EUV time series.
- Synoptic Br for PFSS background.

### Failure modes (skill memory)

- QSL extraction depends on Q-factor threshold.
- Null identity drifts with NLFFF boundary prep.

### Figure / numerical targets

- Fan-spine topology with null overlay.
- QSL footprint at jet base.

### Claim boundary

**In scope.** The studied event.

**Out of scope — do NOT generalize:**

- Do NOT generalize the fan-spine trigger to all blowout jets.
- Do NOT cite QSL alignment independent of Q-threshold.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_hmi_vector()` | HMI vector |  |
| `imagery.fetch_aia()` | AIA EUV |  |
| `pfss.solve()` | background |  |
| `nlfff.solve()` | AR volume |  |
| `topology.identify_fan_spine_null()` | fan-spine null |  |
| `topology.qsl_q_factor()` | QSLs | Q threshold |

### Procedure

1. Solve PFSS+NLFFF.
2. Identify fan-spine null near AR core.
3. Extract QSLs; project to photosphere.
4. Overlay AIA jet base.

### Validation target

Match QSL footprint to AIA jet base.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; NLFFF + Q-factor codes paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[raouafi-2025-switchback-coronal-jet-precursors]] — blowout-jet topologies as switchback precursors.
- Generative hypothesis: fan-spine subclass should correlate with [[nadol-2026-magnetic-separator-reconnection-flare-ribbons]] complex ribbons.

---

## Skill graph → depends_on

- [[raouafi-2025-switchback-coronal-jet-precursors]]
- [[flare-precursor-fine-scale-topology-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2602.01742
- arXiv HTML: https://arxiv.org/html/2602.01742
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- Q-factor threshold
- NLFFF code
