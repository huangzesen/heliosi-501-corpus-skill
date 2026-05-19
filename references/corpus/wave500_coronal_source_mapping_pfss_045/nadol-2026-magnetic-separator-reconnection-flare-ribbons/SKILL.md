---
name: nadol-2026-magnetic-separator-reconnection-flare-ribbons
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# nadol-2026-magnetic-separator-reconnection-flare-ribbons

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when interpreting complex flare-ribbon morphology via PFSS+NLFFF-identified magnetic separators and quantifying separator-reconnection flux.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** The Role of Reconnection at Magnetic Separators in Complex Solar Flare Ribbons
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2026
- **arXiv:** 2603.23789 (posted 2026-03-24)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Complex flare ribbons trace PFSS+NLFFF magnetic separators for a non-trivial fraction of events; separator-reconnection flux estimated from ribbon morphology agrees with NLFFF-predicted separator energy within tolerance.

### Method assumptions

- Separator extraction is robust at the chosen grid.
- Ribbon morphology can be mapped to separator footprints.

### Data assumptions

- AIA 1600/304 Å ribbon imagery.
- HMI vector magnetograms.
- Synoptic Br for PFSS background.

### Failure modes (skill memory)

- Ribbon mask quality depends on threshold.
- Separator extraction at AR-edge boundaries is noisy.

### Figure / numerical targets

- Ribbon overlay on PFSS+NLFFF separators.
- Separator-reconnection-flux vs ribbon-flux scatter.

### Claim boundary

**In scope.** Studied complex flare-ribbon events.

**Out of scope — do NOT generalize:**

- Do NOT generalize to simple two-ribbon flares without re-extracting separators.
- Do NOT cite the separator-flux match independent of NLFFF boundary preparation.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `imagery.fetch_aia()` | AIA 1600/304 |  |
| `magnetogram.fetch_hmi_vector()` | HMI vector |  |
| `pfss.solve()` | background |  |
| `nlfff.solve()` | AR volume |  |
| `topology.extract_separators()` | separators |  |
| `flux.separator_reconnection()` | separator flux estimate |  |

### Procedure

1. Identify ribbon masks.
2. Solve PFSS+NLFFF.
3. Extract separators; project on photosphere.
4. Compute separator-reconnection flux.
5. Compare to ribbon-flux estimate.

### Validation target

Reproduce the separator-flux–ribbon-flux scatter.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; NLFFF code is paper-specific.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-mackay-2026-tracking-magnetic-topology-change-corona]] — track separator continuity across ribbon evolution.
- Generative hypothesis: ribbon→separator alignment quality predicts dimming morphology ([[paper-razquin-2026-coronal-dimming-magnetic-flux-may2024]]).

---

## Skill graph → depends_on

- [[paper-mackay-2026-tracking-magnetic-topology-change-corona]]
- [[paper-flare-precursor-fine-scale-topology-extrapolation]]

## Links

- arXiv: https://arxiv.org/abs/2603.23789
- arXiv HTML: https://arxiv.org/html/2603.23789
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- NLFFF code
- ribbon threshold
