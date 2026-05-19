# paper-gong-network-synoptic-magnetogram-product

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when using the **GONG ground-based synoptic
magnetogram product** (NSO Integrated Synoptic Program) as boundary
condition for PFSS / global coronal MHD.

## Layer 1 — Scientific invariant

- **Paper identity:** GONG Network Synoptic Magnetogram Product
  (representative: Harvey+ 1996; Petrie+ 2014).
- **Year:** TODO verify.
- **Venue:** Sol. Phys. — TODO verify.

### Claim (narrow form)

GONG synoptic maps assembled from six ground stations provide
continuous global Br coverage with **daily updates and a Carrington
synoptic at end-of-rotation**, calibrated to MDI/HMI within stated
tolerance.

### Method assumptions

- Sub-rotation merging weights spatially nearer central meridian.
- Cross-calibration against MDI/HMI on overlap.

### Failure modes (skill memory)

- **Ground-based seeing** degrades quiet-Sun S/N.
- **Polar fill-in** is uncertain in solar minimum.
- **Daily synoptic** mixes farside extrapolation with measured Earthside.

### Claim boundary

**In scope.** Global Br maps suitable for PFSS / MHD boundary
conditions.

**Out of scope.** Do NOT use individual GONG pixels as a strong-
field magnetogram; integrate over patches.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `magnetogram.fetch_gong_synoptic()`     | NSO GONG product         |
| `magnetogram.qa_polar_fill()`           | polar reasonableness     |
| `magnetogram.resample_grid()`           | downstream PFSS grid     |

### Procedure

1. Fetch GONG synoptic Br for the target CR.
2. QA polar fill-in (replace if implausible).
3. Resample to PFSS grid.

### Validation target

TODO verify — unsigned-flux agreement with HMI synoptic to ~10%.

## Layer 3 — Adapter / runtime notes (optional examples)

- NSO GONG data are accessible via JSOC / NSO archive.

## Layer 4 — Research-generation affordances

- **Gap:** systematic cycle-phase QA of polar fill-in is missing —
  pair with `[[paper-mdi-hmi-cross-calibration-synoptic-flux]]`.
- **Hypothesis:** GONG-driven PFSS underestimates polar open flux in
  minimum vs HMI-driven PFSS in
  `[[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]`.

## Skill graph → depends_on

- (none)

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
