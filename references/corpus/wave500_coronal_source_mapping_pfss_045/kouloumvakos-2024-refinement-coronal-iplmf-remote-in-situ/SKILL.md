---
name: kouloumvakos-2024-refinement-coronal-iplmf-remote-in-situ
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# kouloumvakos-2024-refinement-coronal-iplmf-remote-in-situ

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when *jointly* refining PFSS+IP field extrapolations against simultaneous remote-sensing (eclipse, EUV) and in-situ (L1, PSP, SolO) observations.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Refinement of Global Coronal and Interplanetary Magnetic Field Extrapolations Constrained by Remote-Sensing and In-Situ Observations
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2024
- **arXiv:** 2405.18665 (posted 2024-05-29)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A joint remote+in-situ refinement of PFSS+Parker-spiral extrapolations achieves better polarity-agreement at multiple spacecraft and improved eclipse-morphology matching than the baseline PFSS at fixed magnetogram product.

### Method assumptions

- Multi-observable cost function is well-defined.
- Remote and in-situ observables are mutually compatible up to uncertainty.

### Data assumptions

- Synoptic Br for the studied interval.
- Eclipse imagery (where available).
- L1+PSP+SolO in-situ B.

### Failure modes (skill memory)

- Multi-objective optimization weights drive the optimum.
- Eclipse availability is sparse.

### Figure / numerical targets

- Multi-observable cost surface.
- Per-spacecraft polarity-agreement improvement table.

### Claim boundary

**In scope.** The studied intervals with multi-spacecraft coverage.

**Out of scope — do NOT generalize:**

- Do NOT cite the improvement scale outside the multi-observable coverage window.
- Do NOT collapse the joint refinement to a single-observable tune.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | Br |  |
| `pfss.solve()` | PFSS |  |
| `eclipse.angles()` | eclipse-morphology metric |  |
| `polarity.evaluate_multi_sc()` | multi-spacecraft polarity | L1/PSP/SolO |
| `optim.multi_objective()` | joint refinement | weights |

### Procedure

1. Build multi-objective cost: eclipse + polarity.
2. Sweep PFSS parameters (R_ss, product).
3. Optimize; record per-observable contribution.

### Validation target

Reproduce per-spacecraft improvement table.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss; pyspedas for in-situ.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-rice-2026-outflowpy-outflow-fields-pfss-alternative]] for a joint refinement under outflow physics.
- Generative hypothesis: cost-surface valleys identify regimes where additional physics (NSPF, multi-constraint PFSS) gives diminishing returns.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-eclipse-white-light-benchmark-pfss-models]]

## Links

- arXiv: https://arxiv.org/abs/2405.18665
- arXiv HTML: https://arxiv.org/html/2405.18665
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- multi-objective weights
- intervals studied
