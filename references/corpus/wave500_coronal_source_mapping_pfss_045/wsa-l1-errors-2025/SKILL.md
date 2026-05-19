# wsa-l1-errors-2025

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when diagnosing WSA solar-wind speed forecast errors at L1 by decomposing them into PFSS, expansion-factor, and SC-distance terms.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** What Causes Errors in Wang-Sheeley-Arge Solar Wind Modeling at L1?
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2506.09676 (posted 2025-06-11)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

WSA L1-speed forecast errors decompose into measurable contributions from PFSS topology, the f-vs-d expansion-factor kernel, and magnetogram product, with PFSS topology errors dominating for ~half of the studied period.

### Method assumptions

- WSA decomposition into PFSS + expansion-factor kernel is valid.
- L1 speed ground truth (OMNI) is bias-free for the metric.
- Magnetogram-product swap is a controlled experiment.

### Data assumptions

- OMNI L1 speed.
- Multiple synoptic Br products (GONG/HMI/ADAPT).
- WSA kernel parameters (paper-stated).

### Failure modes (skill memory)

- Decomposition assumes additivity; cross-terms exist.
- WSA kernel parameters drift with cycle phase.
- OMNI gaps mid-CR bias the validation.

### Figure / numerical targets

- WSA-error decomposition by component vs time.
- Per-product error histograms.
- Topology-vs-kernel attribution map.

### Claim boundary

**In scope.** The paper's WSA configuration and validation interval.

**Out of scope — do NOT generalize:**

- Do NOT cite the decomposition for non-WSA solar-wind models.
- Do NOT assume topology-vs-kernel attribution holds outside the validated cycle phase.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | synoptic Br products | GONG/HMI/ADAPT |
| `pfss.solve()` | PFSS topology |  |
| `expansion_factor.compute()` | f at source surface |  |
| `wsa.predict_speed()` | WSA predicted L1 speed | kernel params |
| `omni.fetch_speed()` | L1 speed truth | 1h |
| `error.decompose()` | topology vs kernel vs product |  |

### Procedure

1. Fetch synoptic Br for the validation interval (each product).
2. Solve PFSS; compute expansion factor.
3. Run WSA kernel; predict L1 speed.
4. Fetch OMNI speed; compute error.
5. Decompose error into topology vs kernel vs product.

### Validation target

Reproduce the topology-dominant fraction of error reported by the paper.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss for PFSS; WSA kernel implementations vary by site (no canonical adapter asserted).

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-dingding-2025-pfss-source-surface-height-optimization]]: optimizing R_ss should shift the topology-vs-kernel attribution.
- Tension with [[paper-sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field]]: the topology error here may be largely magnetogram completeness in disguise.

---

## Skill graph → depends_on

- [[paper-dingding-2025-pfss-source-surface-height-optimization]]
- [[paper-sasi-2025-uncertainty-solar-wind-incomplete-magnetic-field]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2506.09676
- arXiv HTML: https://arxiv.org/html/2506.09676
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- WSA kernel parameters
- validation interval
