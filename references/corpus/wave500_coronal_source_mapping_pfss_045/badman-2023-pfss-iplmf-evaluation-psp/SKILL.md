---
name: badman-2023-pfss-iplmf-evaluation-psp
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# badman-2023-pfss-iplmf-evaluation-psp

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when scoring PFSS-derived coronal + interplanetary magnetic-field extrapolations against PSP in-situ B at perihelion.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Evaluation of Coronal and Interplanetary Magnetic Field Extrapolation Using PSP Solar Wind Observation
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2023
- **arXiv:** 2305.12124 (posted 2023-05-20)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

PFSS+Parker-spiral extrapolations validated against PSP perihelion |B| / B_R sign achieve a quantified pass rate that varies with magnetogram product and R_ss.

### Method assumptions

- Parker-spiral extension is valid outside the source surface.
- PSP perihelion windows are unambiguous.

### Data assumptions

- PSP FIELDS B per encounter.
- Synoptic Br products (GONG/HMI/ADAPT) per CR.

### Failure modes (skill memory)

- Product swap shifts pass rate.
- Parker assumption breaks near sub-Alfvénic regions.

### Figure / numerical targets

- Per-encounter pass-rate table.
- Polarity-agreement vs R_ss curve.

### Claim boundary

**In scope.** The studied PSP encounters with paper's protocol.

**Out of scope — do NOT generalize:**

- Do NOT cite the headline pass rate outside the studied encounters.
- Do NOT mix magnetogram products mid-comparison.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `psp.fields_b()` | PSP B |  |
| `magnetogram.fetch_synoptic_br()` | Br products |  |
| `pfss.solve()` | PFSS |  |
| `parker.spiral_extend()` | Parker extension |  |
| `polarity.evaluate_in_situ()` | in-situ polarity vote |  |

### Procedure

1. For each encounter, solve PFSS on each Br product.
2. Extend via Parker spiral to PSP position.
3. Score polarity agreement and |B| ratio.
4. Tabulate per-product / per-R_ss results.

### Validation target

Reproduce per-encounter pass-rate table.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; PSP data via pyspedas / .library/custom/psp-data-analysis/.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-dingding-2025-pfss-source-surface-height-optimization]] — pass rate vs optimal R_ss should be coherent.
- Generative hypothesis: replacing Parker spiral with the Fisk field ([[paper-macneice-2024-fisk-heliospheric-field-source-mapping]]) should change perihelion polarity-agreement scores.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-dingding-2025-pfss-source-surface-height-optimization]]

## Links

- arXiv: https://arxiv.org/abs/2305.12124
- arXiv HTML: https://arxiv.org/html/2305.12124
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- encounters list
- exact pass-rate metric
- magnetogram products
