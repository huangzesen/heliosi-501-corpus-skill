---
name: brightness-magnetically-open-corona-2025
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# brightness-magnetically-open-corona-2025

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when interpreting EUV-CH brightness as a diagnostic of heating + density structure, with PFSS providing the open-vs-closed topological map.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** What Determines the Brightness of the Magnetically Open Solar Corona? Insights from Three-Dimensional Radiative MHD
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2504.14049 (posted 2025-04-18)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

In 3-D radiative-MHD coronal-hole simulations, brightness of magnetically open regions is set by a combination of footpoint heating amplitude and column density, not by open-vs-closed identity alone — and PFSS open-field maps are necessary but not sufficient to predict CH brightness.

### Method assumptions

- 3-D radiative MHD captures the dominant heating modes for CH plasma.
- EUV-band synthetic observables are calibrated against AIA.
- PFSS open-field footpoints can be projected onto the simulation domain.

### Data assumptions

- Comparison AIA EUV CH brightness.
- Simulation-internal MHD state + radiative-transfer post-processing.

### Failure modes (skill memory)

- Synthetic-vs-observed AIA calibration is non-trivial.
- Heating prescription dominates the result — sensitivity test required.
- PFSS open-field map at the simulation footprint depends on synoptic-map choice.

### Figure / numerical targets

- Synthetic AIA-vs-PFSS-open-field-map overlay.
- Brightness-vs-column-density scatter at open footpoints.
- Heating-amplitude sensitivity panel.

### Claim boundary

**In scope.** The paper's RMHD setup + AIA comparison; quiet-CH regime.

**Out of scope — do NOT generalize:**

- Do NOT use the brightness/topology argument for AR-edge dim regions.
- Do NOT cite the heating-vs-density partition outside the modelled range.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `rmhd.coronal_hole_run()` | RMHD CH simulation |  |
| `synth.aia_lines()` | synthetic AIA images |  |
| `pfss.solve()` | open-field overlay |  |
| `imagery.fetch_aia()` | AIA comparison |  |
| `ch.detect_from_euv()` | CH boundary |  |

### Procedure

1. Run RMHD CH simulation; post-process to AIA bands.
2. Solve PFSS on the matching synoptic Br.
3. Overlay PFSS open-field map on synthetic and observed AIA.
4. Quantify brightness vs column density at open footpoints.
5. Sweep heating amplitude; record the brightness response.

### Validation target

Reproduce the paper's brightness-vs-heating-amplitude scaling at fixed column density.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- RMHD code is paper-specific; SunPy/aiapy for AIA; sunkit-magex.pfss for the PFSS overlay.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-brooks-2025-active-region-upflows-coronal-coupling]]: do AR-edge upflows live in bright or dim open regions?
- Generative hypothesis: pairing this with the QRaFT-segmented open-flux map ([[paper-qrft-2025-quasi-radial-field-tracing-open-flux]]) yields a brightness-classified open-flux atlas.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-brooks-2025-active-region-upflows-coronal-coupling]]

## Links

- arXiv: https://arxiv.org/abs/2504.14049
- arXiv HTML: https://arxiv.org/html/2504.14049
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- RMHD code identity
- heating prescription
