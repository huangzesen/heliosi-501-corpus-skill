---
name: rice-2026-outflowpy-outflow-fields-pfss-alternative
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# rice-2026-outflowpy-outflow-fields-pfss-alternative

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when you need a PFSS alternative that couples coronal field to solar-wind outflow and reduces the in-situ open-flux discrepancy without a fixed source-surface.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Global Coronal Equilibria with Solar Wind Outflow II — Optimizing the Outflow Model (outflowpy)
- **First author:** O. Rice
- **Authors:** O. Rice, A. R. Yeates
- **Year:** 2026
- **arXiv:** 2603.22159 (posted 2026-03-23)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Outflow Fields tuned by an evolutionary algorithm over 2000–2022 reduce the in-situ open-flux discrepancy from ~45% (PFSS) to ~24% and improve eclipse field-line matching; released as outflowpy.

### Method assumptions

- A magneto-frictional outflow equilibrium is solvable on the same synoptic Br as PFSS.
- Eclipse-image field-line angles are a fair morphology test.
- An EA can tune the outflow parameters to a multi-metric objective.

### Data assumptions

- Synoptic Br 2000–2022.
- Eclipse images with extracted field-line angles.
- OMNI |B|R² for in-situ OSF.

### Failure modes (skill memory)

- Eclipse-angle extraction is image-processing-sensitive.
- EA can overfit the multi-metric objective; held-out cycle needed.
- OSF baseline depends on R_ss convention; pin it.

### Figure / numerical targets

- Field-line angle distribution: eclipse vs PFSS vs outflowpy.
- OSF time series vs OMNI.
- Optimized-parameter table.

### Claim boundary

**In scope.** 2000–2022 with the paper's eclipse set and OMNI OSF reconstruction.

**Out of scope — do NOT generalize:**

- Do NOT cite the 45→24% gap as a generic OSF closure.
- Do NOT replace outflowpy with full MHD-driven solutions and quote the same numbers.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | synoptic Br | per CR |
| `coronal_eq.solve_outflow()` | Outflow Fields | outflow params |
| `optim.evolutionary()` | EA for outflow params | metric weights |
| `eclipse.angles()` | extract from white-light | image proc |
| `osf.in_situ_from_omni()` | 1-au OSF | |B|R² |
| `pfss.solve()` | baseline PFSS | for gap |

### Procedure

1. Define EA objective: eclipse-angle KL + OSF-gap.
2. Sweep outflow params via EA.
3. For each candidate, solve outflow equilibrium on train set.
4. Evaluate on a held-out cycle.
5. Compare to PFSS baseline.

### Validation target

Recover ~45% → ~24% gap reduction within tolerance and eclipse-angle improvement.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- outflowpy is the canonical adapter; PFSS reference can use sunkit-magex.pfss. Both runtime-supplied examples.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]: NSPF deforms the outer boundary; outflowpy modifies the equation. Stacking the two partitions OSF closure between geometry and physics.
- Generative hypothesis: outflowpy-optimal params rank-correlate with [[paper-yoshida-2026-sunspot-evolution-open-flux-cycle24-max]]'s BMR-driven OSF rises.

---

## Skill graph → depends_on

- [[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]
- [[paper-eclipse-white-light-benchmark-pfss-models]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2603.22159
- arXiv HTML: https://arxiv.org/html/2603.22159
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- journal
- outflowpy version
- EA metric weights
- held-out cycle
