# hore-2026-dominant-spatial-scales-coronal-field

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when you need to justify low-resolution synoptic magnetograms for global coronal modelling via a modal-power argument across Cycle 24.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Uncovering the Dominant Spatial Scales of the Sun's Magnetic Field in Solar Cycle 24
- **First author:** A. Hore
- **Authors:** A. Hore, P. Bhowmik
- **Year:** 2026
- **arXiv:** 2604.10144 (posted 2026-04-11)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

>80% of MDI+HMI modal power lives at low harmonic degrees (spatial scale ~145 Mm), and effective harmonic degree of the PFSSE coronal field drops with height — so low-resolution magnetograms capture global coronal structure.

### Method assumptions

- LoS-to-Br conversion is acceptable outside the polar cap.
- PFSSE is spectrum-preserving up to truncation.
- Modal-power-vs-degree is a meaningful summary statistic.

### Data assumptions

- MDI (pre-2010) and HMI (post-2010) synoptic Br for Cycle 24.
- Consistent SH grid across the mission boundary.

### Failure modes (skill memory)

- High-latitude noise dominates l→high tail — truncate the polar zone.
- SH leakage at Nyquist degree fakes high-l power.
- Effective-degree decrease with height depends on source-surface choice.

### Figure / numerical targets

- Modal-power-vs-degree at the photosphere.
- Effective harmonic degree vs height.
- Truncated-Br reconstruction comparison.

### Claim boundary

**In scope.** Cycle 24 global structure with MDI+HMI and PFSSE.

**Out of scope — do NOT generalize:**

- Do NOT extend to AR-internal scales or NLFFF studies.
- Do NOT use as license to replace HMI with very low-res magnetograms for transient-event work.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_full_disk_br()` | MDI/HMI full-disk Br | LoS→Br |
| `magnetogram.build_synoptic()` | stitch synoptic | polar fill |
| `sph_harm.decompose()` | modal power per l | truncation |
| `pfss.solve()` | coronal field | for height-vs-l |
| `sph_harm.effective_degree()` | summary statistic |  |

### Procedure

1. Build Cycle-24 synoptic stream.
2. SH-decompose each map; record power-vs-l.
3. Solve PFSSE; decompose each shell.
4. Compute effective degree at each height.
5. Quantify reconstruction loss as a function of truncation.

### Validation target

>80% modal power at low l and monotonic effective-degree decrease with height.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- SH adapters: pyshtools / healpy / custom Gauss–Legendre. PFSS via sunkit-magex.pfss as an example.

---

## Layer 4 — Research-generation affordances

- Generative hypothesis: residual high-l power that leaks upward at limb-side ARs predicts where loop-constrained corrections ([[paper-multi-constraint-pfss-extrapolation-model]]) matter most.
- Composable experiment: re-run on stellar ZDI magnetograms to test low-degree dominance across late-type stars.

---

## Skill graph → depends_on

- [[paper-stansby-2020-pfsspy-python-pfss]]
- [[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]

## Links

- arXiv: https://arxiv.org/abs/2604.10144
- arXiv HTML: https://arxiv.org/html/2604.10144
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- exact 80%-degree cutoff
- PFSSE truncation degree
- polar fill-in policy
- DOI
