---
name: paper-open-flux-problem-in-situ-vs-pfss-discrepancy
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-open-flux-problem-in-situ-vs-pfss-discrepancy

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when reconciling **in-situ unsigned `B_r` × r²**
("Ulysses-equal-flux" / "open-flux problem") against PFSS-derived
open flux across the cycle.

## Layer 1 — Scientific invariant

- **Paper identity:** Open-Flux Problem: In-Situ vs PFSS Discrepancy
  (representative: Linker+ 2017; Wallace+ 2019; Riley+ 2019).
- **Year:** 2017–2019.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

In-situ unsigned magnetic-flux integrals (Ulysses, ACE/Wind) yield
**factor 1.5–2× more open flux** than PFSS reconstructions using HMI/
GONG synoptic maps with standard `R_ss = 2.5 R_sun`, in solar
minimum. The discrepancy persists across multiple PFSS solvers and
input magnetogram products.

### Method assumptions

- In-situ unsigned `|B_r| × r²` is the open-flux proxy.
- PFSS open flux integrated over outward field at `R_ss`.
- Time-averaging over at least one Carrington rotation.

### Failure modes (skill memory)

- **Switchback contamination** in PSP near-Sun data can inflate
  in-situ `|B_r|`.
- **`R_ss` choice** changes PFSS open flux significantly.
- **Polar fill-in** in synoptic maps biases minimum-phase open
  flux.

### Claim boundary

**In scope.** Cycle-averaged open-flux comparison.

**Out of scope.** Do NOT attribute the discrepancy to a single cause
without testing the alternative explanations: NSPF, AI-farside,
CSSS, etc.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `in_situ.fetch_unsigned_br()`           | Ulysses / ACE / Wind     |
| `pfss.solve()`                          | PFSS                     |
| `field.integrate_open_flux()`           | PFSS open flux           |
| `metrics.in_situ_vs_pfss_ratio()`       | discrepancy ratio        |

### Procedure

1. Aggregate in-situ `|B_r| × r²` over each CR.
2. Compute PFSS open flux at matched CR.
3. Tabulate ratio over solar cycle.

### Validation target

TODO verify — ratio `~1.5–2.0` in minimum.

## Layer 3 — Adapter / runtime notes (optional examples)

- Python: `cdflib` + `numpy`; PFSS via `sunkit-magex`.

## Layer 4 — Research-generation affordances

- **Gap:** the open-flux problem has rarely been re-evaluated with
  PSP-era near-Sun in-situ data — pair with
  `[[paper-bale-2021-solar-source-switchbacks-magnetic-funnels]]`
  to bound switchback-inflated `|B_r|`.
- **Hypothesis:** combining
  `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`
  NSPF + AI-farside + CSSS closes the gap in minimum but not in
  maximum.

## Skill graph → depends_on

- `[[paper-csss-current-sheet-source-surface-non-radial-open-flux]]`
- `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
