---
name: tahtinen-2026-dipole-flux-transport-open-flux
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# tahtinen-2026-dipole-flux-transport-open-flux

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when you need a fast emulator of SFT-driven dipole evolution that is also a usable open-flux proxy — e.g. for scanning thousands of BMR-configuration counterfactuals.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Ultra-Fast Simulations of the Solar Dipole and Open Flux
- **First author:** I. Tähtinen
- **Authors:** I. Tähtinen, T. Asikainen, K. Mursula
- **Year:** 2026
- **arXiv:** 2604.11342 (posted 2026-04-13)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Compressed propagator-matrix DFT reproduces SFT dipole within ~1% over Cycle 24 at 50–50,000× speedup; |dipole| tracks PFSS-OSF closely enough to serve as an OSF emulator.

### Method assumptions

- SFT linearizes into propagators over a fixed synoptic basis.
- Compression ratio <1e-4 preserves dipole accuracy.
- |dipole| ≈ OSF empirically over Cycle 24.

### Data assumptions

- BMR emergence stream for the simulation window.
- Reference PFSS-OSF time series.

### Failure modes (skill memory)

- Linearity breaks when diffusion/flow varies outside the bake-in.
- |dipole| ≈ OSF degrades in cycles dominated by higher multipoles.
- Compression ratio is a knob — log it.

### Figure / numerical targets

- DFT vs SFT dipole over Cycle 24.
- DFT-derived OSF vs PFSS-OSF.
- Wall-clock speedup table.

### Claim boundary

**In scope.** Cycle 24 with the paper's BMR catalog and DFT settings.

**Out of scope — do NOT generalize:**

- Do NOT use DFT to forecast HCS shape — it tracks only the dipole.
- Do NOT extend to grand-minima or non-dipole-dominated regimes.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `sft.basis_propagator()` | build linear propagator | fixed flow/diffusion |
| `sft.compress_propagator()` | vector-sum compression | ratio param |
| `dipole.from_synoptic()` | extract dipole vector from Br | SH |
| `pfss.solve()` | reference OSF | for validation |
| `bmr.emergence_stream()` | BMR driver | input |

### Procedure

1. Choose synoptic basis; build propagator matrices.
2. Compress with vector-sum method; record ratio.
3. Drive with BMR stream; integrate dipole forward.
4. Snapshot PFSS-OSF on selected CRs for validation.
5. Tabulate speedup vs SFT baseline.

### Validation target

≤1% disagreement on dipole vs SFT; tight |dipole|–OSF rank-correlation.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- PFSS reference can use sunkit-magex.pfss. DFT itself is paper-internal; no canonical adapter asserted.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-yoshida-2026-sunspot-evolution-open-flux-cycle24-max]] to scan AR-12192-ablation counterfactuals at 10^3 throughput.
- Residual between DFT-|dipole|-OSF and NSPF-OSF ([[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]) is a clean budget for non-dipolar open flux.

---

## Skill graph → depends_on

- [[paper-yoshida-2026-sunspot-evolution-open-flux-cycle24-max]]
- [[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2604.11342
- arXiv HTML: https://arxiv.org/html/2604.11342
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- journal
- compression-ratio for headline numbers
- BMR catalog identity
