---
name: raouafi-2025-switchback-coronal-jet-precursors
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# raouafi-2025-switchback-coronal-jet-precursors

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when testing whether coronal jets are precursors of PSP-observed magnetic switchbacks by back-mapping switchback footpoints via PFSS to candidate jet sites.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Tracing Magnetic Switchbacks to Their Source: An Assessment of Solar Coronal Jets as Switchback Precursors
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2501.12340 (posted 2025-01-21)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A statistically significant subset of PSP switchback patches back-maps via PFSS to coronal-hole jet locations within the paper's spatial-temporal tolerance, supporting (but not uniquely proving) jet-driven switchback formation.

### Method assumptions

- Switchback patches at PSP are correctly identified.
- PFSS + ballistic back-mapping is accurate enough at the relevant scales.
- Coronal-hole jet catalog is complete in the relevant window.

### Data assumptions

- PSP FIELDS + SWEAP for switchback identification.
- AIA EUV for jet catalog.
- Synoptic Br for PFSS.

### Failure modes (skill memory)

- Switchback-patch boundaries depend on deflection threshold.
- Back-mapping uncertainty broadens at low vsw.
- Jet catalog completeness varies by AIA channel.

### Figure / numerical targets

- Switchback footpoint overlay on EUV jet sites.
- Time-distance plot of switchback occurrence vs jet activity.
- Statistical significance test panel.

### Claim boundary

**In scope.** The paper's PSP encounter window and jet catalog.

**Out of scope — do NOT generalize:**

- Do NOT claim jets cause *all* switchbacks.
- Do NOT cite the precursor association without re-checking under alternate switchback definitions.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `psp.fields_b()` | PSP MAG | burst+survey |
| `sw.identify_switchback_patch()` | switchback patches | threshold knob |
| `imagery.fetch_aia()` | EUV for jets |  |
| `jet.detect_coronal_hole()` | jet catalog | automated/manual |
| `pfss.solve()` | footpoint mapping |  |
| `backmap.ballistic()` | ballistic backmap |  |

### Procedure

1. Identify switchback patches at PSP.
2. Back-map each patch to source surface (ballistic + PFSS).
3. Build jet catalog from EUV imagery.
4. Co-locate footpoints and jets; assess significance.

### Validation target

Recover the paper's jet–switchback association significance.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss + ballistic backmap example in .library/custom/pfss-tracing/.

---

## Layer 4 — Research-generation affordances

- Tension with [[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]: funnel-driven vs jet-driven switchback origins; the footpoint atlas separates them.
- Generative hypothesis: re-running with [[paper-deforest-2024-flux-fluxon-coronal-modeling]]'s fluxon-based connectivity should reveal jet associations missed by gridded PFSS.

---

## Skill graph → depends_on

- [[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2501.12340
- arXiv HTML: https://arxiv.org/html/2501.12340
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- jet catalog identity
- switchback threshold
