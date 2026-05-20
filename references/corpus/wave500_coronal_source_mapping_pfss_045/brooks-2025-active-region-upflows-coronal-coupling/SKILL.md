---
name: brooks-2025-active-region-upflows-coronal-coupling
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# brooks-2025-active-region-upflows-coronal-coupling

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when characterizing AR upflows as slow-wind source candidates, tying EIS/SPICE upflow patches to PFSS open-field connectivity and to lower-atmosphere drivers.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Active Region Upflows in Various Coronal Structures and Their Coupling to the Lower Atmosphere
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2509.02157 (posted 2025-09-02)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

AR-edge upflows correspond to open-field foots in PFSS for a non-trivial fraction of the events studied; upflow strength correlates with lower-atmosphere drivers (waves, granular buffeting) more than with overlying coronal-loop temperature.

### Method assumptions

- EIS/SPICE Doppler shifts are calibrated against a quiet-Sun reference.
- AR-edge upflow patches are robust to thresholding.
- PFSS captures AR-edge open-vs-closed footpoint identity.

### Data assumptions

- EIS Fe XII 195 Å or SPICE Ne VIII Doppler maps.
- AIA EUV + HMI Br for the same AR.
- Synoptic Br for PFSS over the AR's CR.

### Failure modes (skill memory)

- Doppler-calibration drift biases the upflow population.
- PFSS misclassifies fan-loop / quasi-open structures.
- Lower-atmosphere driver association is correlational, not causal.

### Figure / numerical targets

- Upflow patches overlaid on PFSS open-field map.
- Upflow-strength vs lower-atmosphere proxy scatter.
- Quiet-Sun-referenced Doppler-shift histograms.

### Claim boundary

**In scope.** The paper's AR sample with EIS/SPICE coverage.

**Out of scope — do NOT generalize:**

- Do NOT claim every PFSS-open AR edge is an upflow without EIS/SPICE confirmation.
- Do NOT attribute slow-wind origin globally to AR upflows on this evidence alone.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `doppler.fetch_eis_spice()` | Doppler maps | Fe XII / Ne VIII |
| `doppler.quiet_sun_reference()` | calibration | QS patch |
| `imagery.fetch_aia()` | context EUV |  |
| `magnetogram.fetch_hmi()` | AR Br | L1.5 |
| `pfss.solve()` | AR-edge open vs closed |  |
| `ar.identify_upflow_patch()` | upflow patches | threshold knob |

### Procedure

1. Build Doppler maps; calibrate against QS reference.
2. Identify upflow patches at AR edges.
3. Solve PFSS for the AR's CR; project open-field footpoints.
4. Co-locate upflows with PFSS-open footpoints.
5. Correlate upflow strength with lower-atmosphere proxies.

### Validation target

Reproduce the open-field fraction of upflow patches and the lower-atmosphere-driver correlation.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- EIS / SPICE pipelines; SunPy / aiapy for AIA; sunkit-magex.pfss for PFSS.

---

## Layer 4 — Research-generation affordances

- Compose with [[brightness-magnetically-open-corona-2025]] — do upflows live in the *bright* or *dim* open-field patches?
- Generative hypothesis: AR-edge upflows that map (via PFSS) to PSP perihelion footpoints predict slow-Alfvénic streams in [[ervin-2024-slow-alfvenic-source-regions-pfss-psp]].

---

## Skill graph → depends_on

- [[ervin-2024-slow-alfvenic-source-regions-pfss-psp]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2509.02157
- arXiv HTML: https://arxiv.org/html/2509.02157
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- AR sample list
- Doppler calibration policy
