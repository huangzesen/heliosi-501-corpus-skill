---
name: reville-2025-solo-psp-open-closed-magnetic-outflows
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# reville-2025-solo-psp-open-closed-magnetic-outflows

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when characterizing slow-wind outflows from open–closed boundary regions during PSP–SolO conjunctions, with PFSS providing source-region context.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Investigating Solar Wind Outflows from Open–Closed Magnetic Field Structures Using Coordinated Solar Orbiter and PSP Observations
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2502.08290 (posted 2025-02-12)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

During PSP–SolO conjunctions, in-situ slow-wind streams trace back via PFSS to open–closed boundary regions, with PSP and SolO seeing consistent composition signatures consistent with an interchange-reconnection origin.

### Method assumptions

- PSP–SolO conjunction definition is robust.
- Backmapping accuracy is sufficient at ~0.3–0.5 au.
- Composition (heavy-ion) signatures discriminate source regions.

### Data assumptions

- PSP FIELDS+SWEAP + SolO MAG+SWA over conjunction.
- Synoptic Br for the relevant CR.
- Heavy-ion composition (SWA-HIS).

### Failure modes (skill memory)

- Conjunction definition (radial vs longitudinal) shifts the sample.
- Heavy-ion composition is sparse for many slow streams.
- PFSS OCB sensitive to R_ss.

### Figure / numerical targets

- PSP/SolO vsw + composition vs time-of-flight.
- OCB overlay with backmapped footpoints.
- Composition vs OCB-distance scatter.

### Claim boundary

**In scope.** Studied conjunction windows.

**Out of scope — do NOT generalize:**

- Do NOT extend to non-conjunction slow streams.
- Do NOT cite interchange origin without composition.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `psp.fields_b()` | PSP B |  |
| `psp.sweap_n_v()` | PSP plasma |  |
| `solo.mag_b()` | SolO B |  |
| `solo.swa_his()` | SolO heavy-ion composition |  |
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `ocb.extract()` | OCB |  |
| `backmap.ballistic()` | back-mapping |  |

### Procedure

1. Identify conjunction windows.
2. Fetch PSP + SolO in-situ + composition.
3. Solve PFSS; extract OCB.
4. Back-map both observers to OCB.
5. Test composition–OCB-distance correlation.

### Validation target

Reproduce the conjunction-window OCB association.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; pyspedas for PSP/SolO; SolO-SWA-HIS pipeline.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-stansby-2025-open-closed-flux-boundary-slow-wind]] — OCB as a unified slow-wind origin framework.
- Generative hypothesis: replacing PFSS with outflowpy should shift the OCB by amounts predictable from this conjunction dataset.

---

## Skill graph → depends_on

- [[paper-stansby-2025-open-closed-flux-boundary-slow-wind]]
- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-dakeyo-2026-source-alignment-psp-solo-method-link]]

## Links

- arXiv: https://arxiv.org/abs/2502.08290
- arXiv HTML: https://arxiv.org/html/2502.08290
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- conjunction definition
- composition product
