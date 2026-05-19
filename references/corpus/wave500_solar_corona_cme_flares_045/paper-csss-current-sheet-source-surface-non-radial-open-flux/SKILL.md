# paper-csss-current-sheet-source-surface-non-radial-open-flux

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when comparing **CSSS (current-sheet
source-surface)** to PFSS, especially when the user is sensitive to
non-radial open-flux estimates and pseudostreamer reconnection
geometry.

## Layer 1 — Scientific invariant

- **Paper identity:** Current-Sheet Source-Surface (CSSS) Model
  (representative: Zhao & Hoeksema 1995; Schatten 1971 lineage).
- **Year:** 1995.
- **Venue:** JGR — TODO verify.

### Claim (narrow form)

CSSS replaces the PFSS source-surface boundary with a thin current
sheet at `R_cs`, producing **higher open-flux estimates** and
non-radial near-Sun fields. Open-flux from CSSS exceeds PFSS by
`~20–50%` depending on cycle phase.

### Method assumptions

- Spherical harmonic expansion to a chosen cusp radius `R_cp` and
  current-sheet radius `R_cs`.
- Choice of `(R_cp, R_cs)` is per-author convention.

### Failure modes (skill memory)

- **`(R_cp, R_cs)` choice** dominates the open-flux delta.
- **Non-uniqueness** for the same magnetogram input.
- **Polar fill-in** uncertainty propagates strongly.

### Claim boundary

**In scope.** Global coronal field model with current sheet as
alternative to pure PFSS.

**Out of scope.** Do NOT treat CSSS open-flux as ground truth.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `magnetogram.fetch_synoptic_br()`       | Br on a CR               |
| `csss.solve()`                          | CSSS coefficients        |
| `field.integrate_open_flux()`           | open-flux integral       |
| `metrics.pfss_vs_csss_delta()`          | open-flux difference     |

### Procedure

1. Fetch synoptic Br.
2. Solve CSSS at chosen `(R_cp, R_cs)`.
3. Integrate open flux; compare to PFSS open flux.

### Validation target

TODO verify — open-flux delta consistent with published `~20–50%`.

## Layer 3 — Adapter / runtime notes (optional examples)

- Reference adapter: Wang/Zhao CSSS Fortran code; modern Python
  re-implementation exists in some PFSS codes.

## Layer 4 — Research-generation affordances

- **Gap:** few studies compare CSSS, NSPF, and the AWSoM open flux
  on a single CR.
- **Hypothesis:** the CSSS-vs-PFSS open-flux delta correlates with
  the WSA slow-wind under-prediction
  (`[[paper-arge-2003-wsa-model-source-surface-wind-prediction]]`).

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
