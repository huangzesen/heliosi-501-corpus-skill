---
name: sachdeva-2024-global-simulation-psp-2018-2022
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# sachdeva-2024-global-simulation-psp-2018-2022

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when validating a global MHD solar-wind simulation against PSP over multiple encounters, with PFSS providing inner-boundary structure.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Global Simulation of the Solar Wind: A Comparison with Parker Solar Probe Observations During 2018–2022
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2410.23157 (posted 2024-10-30)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A global MHD simulation initialized from PFSS reproduces PSP vsw / |B| / density at the encounter level (10–30 R_sun) within tolerance over Encounters 1–14, with systematic residuals tied to magnetogram completeness.

### Method assumptions

- Global MHD inner boundary derived from PFSS is consistent at 1.1 R_sun.
- PSP timing → encounter-windows is unambiguous.
- Residuals are dominated by boundary, not MHD numerics.

### Data assumptions

- PSP FIELDS + SWEAP per encounter.
- Synoptic Br per encounter CR.

### Failure modes (skill memory)

- MHD grid coarseness biases inner-encounter results.
- Inner-boundary heating prescription dominates plasma comparisons.
- Synoptic Br aging across the encounter affects the comparison.

### Figure / numerical targets

- PSP encounter overlays (vsw, |B|, n).
- Residual maps in heliographic longitude / latitude.
- Boundary-completeness sensitivity panel.

### Claim boundary

**In scope.** PSP Encounters 1–14 with the paper's MHD configuration.

**Out of scope — do NOT generalize:**

- Do NOT generalize to non-PSP latitudes without re-running.
- Do NOT cite the agreement level outside the encounter windows.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | synoptic Br |  |
| `pfss.solve()` | inner-boundary scaffolding |  |
| `mhd.global_run()` | global MHD run |  |
| `psp.fields_b()` | PSP MAG |  |
| `psp.sweap_n_v()` | PSP plasma |  |

### Procedure

1. Fetch synoptic Br per CR; solve PFSS.
2. Drive MHD inner boundary from PFSS.
3. Run global MHD for the encounter window.
4. Compare to PSP in-situ along the trajectory.
5. Attribute residuals to boundary completeness.

### Validation target

Reproduce per-encounter agreement level.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; MHD code is paper-specific (AWSoM/EUHFORIA/ENLIL — TODO).

---

## Layer 4 — Research-generation affordances

- Compose with [[wsa-l1-errors-2025]] for an MHD↔WSA error reconciliation.
- Generative hypothesis: PFSS-vs-NSPF inner boundary should shift PSP encounter agreement systematically.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[wu-2026-nonspherical-coronal-magnetic-field-open-flux]]

## Links

- arXiv: https://arxiv.org/abs/2410.23157
- arXiv HTML: https://arxiv.org/html/2410.23157
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- MHD code identity
- encounter list with CRs
