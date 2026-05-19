# paper-coronal-hole-pseudostreamer-boundary-classification

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when distinguishing **coronal-hole boundaries
from pseudostreamer separatrices**, since the two surfaces appear
similar in EUV but have different topological / connectivity
implications.

## Layer 1 — Scientific invariant

- **Paper identity:** Coronal-Hole vs Pseudostreamer Boundary
  Classification (representative: Wang+ 2007/2012; Riley+ 2015).
- **Year:** TODO verify.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

Some apparent CH boundaries are in fact **pseudostreamer separatrices
between two unipolar regions of the same polarity**; the boundary
behaves as an open–closed-open transition rather than open–closed.
The narrow claim is that PFSS-based topology classification
distinguishes the two boundary types with **agreement vs EUV
appearance ≈ 70–85%** on a benchmark sample.

### Method assumptions

- A coronal `B` model exists (PFSS, CSSS, MHD).
- Field-line tracing classifies each photospheric point as
  open / closed / pseudostreamer.

### Failure modes (skill memory)

- **Pseudostreamer detection is solver-sensitive.** PFSS and CSSS can
  give different classifications.
- **Synoptic-vs-synchronic** input affects fast-evolving boundaries.
- **EUV proxy** itself is imperfect; do not over-trust either label.

### Claim boundary

**In scope.** Topological classification of CH-vs-pseudostreamer
boundaries using a coronal field model + EUV proxy.

**Out of scope.** Do NOT use as ground truth for in-situ
connectivity claims.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `pfss.solve()`                          | global coronal B         |
| `field.trace_to_photosphere()`          | open / closed map        |
| `topology.classify_boundary()`          | pseudostreamer vs CH     |
| `imagery.fetch_aia()`                   | EUV proxy                |
| `metrics.label_agreement()`             | topology vs EUV          |

### Procedure

1. Solve PFSS / CSSS on the synoptic Br.
2. Map open/closed and label pseudostreamers (cusp-pair geometry).
3. Compare to EUV CH masks.
4. Report disagreement statistics.

### Validation target

TODO verify — label agreement consistent with published 70–85%.

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind PFSS to `sunkit-magex`, the topology
  classifier to a Q-map-based heuristic.

## Layer 4 — Research-generation affordances

- **Gap:** few studies cross-validate pseudostreamer classification
  with in-situ HCS/HPS crossings; pair with
  `[[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]`.
- **Hypothesis:** SASW source regions in
  `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]` are
  systematically at pseudostreamer boundaries, not at CH boundaries.

## Skill graph → depends_on

- `[[paper-coronal-hole-boundary-detection-suvi-segmentation]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
