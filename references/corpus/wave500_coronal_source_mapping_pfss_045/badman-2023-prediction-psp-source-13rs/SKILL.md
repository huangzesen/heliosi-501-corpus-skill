# badman-2023-prediction-psp-source-13rs

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when predicting + verifying PSP solar-wind source regions at 13.3 R_sun via PFSS + ballistic back-mapping, with full pre/post-encounter verification.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Prediction and Verification of Parker Solar Probe Solar Wind Sources at 13.3 R_sun
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2023
- **arXiv:** 2303.04852 (posted 2023-03-08)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

PFSS+ballistic back-mapping predicts PSP source regions at 13.3 R_sun with verifiable accuracy when paired with the correct synoptic Br product, and the verification framework is reusable for future perihelia.

### Method assumptions

- Ballistic back-mapping from PSP to 13.3 R_sun is valid.
- PFSS source-surface at ~2.5 R_sun gives meaningful footpoints.

### Data assumptions

- PSP FIELDS + SWEAP for in-situ verification.
- Synoptic Br for the relevant CR.

### Failure modes (skill memory)

- 13.3 R_sun is beyond R_ss; ballistic step dominates.
- Synoptic-product swap shifts predicted source.

### Figure / numerical targets

- Predicted vs verified source-region overlay.
- Per-encounter accuracy table.

### Claim boundary

**In scope.** The studied PSP perihelion windows.

**Out of scope — do NOT generalize:**

- Do NOT extend to outside-perihelion intervals.
- Do NOT collapse the verification framework into a single-step prediction.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `psp.fields_b()` | PSP B |  |
| `psp.sweap_n_v()` | PSP plasma |  |
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `backmap.ballistic()` | PSP→13.3 R_sun |  |

### Procedure

1. Pre-encounter: predict source via PFSS+ballistic.
2. Post-encounter: fetch PSP B+vsw; verify polarity/source.
3. Iterate across encounters; tabulate accuracy.

### Validation target

Recover per-encounter accuracy table.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss + .library/custom/pfss-tracing/ for the ballistic step.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-koukras-2022-backmapping-uncertainty-fast-wind]] for prediction-with-uncertainty.
- Generative hypothesis: ballistic-vs-MHD-driven back-mapping discrepancy diagnoses encounter intervals where PFSS is incomplete.

---

## Skill graph → depends_on

- [[paper-koukras-2022-backmapping-uncertainty-fast-wind]]
- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-dakeyo-2026-source-alignment-psp-solo-method-link]]

## Links

- arXiv: https://arxiv.org/abs/2303.04852
- arXiv HTML: https://arxiv.org/html/2303.04852
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- encounters list
- accuracy metric
