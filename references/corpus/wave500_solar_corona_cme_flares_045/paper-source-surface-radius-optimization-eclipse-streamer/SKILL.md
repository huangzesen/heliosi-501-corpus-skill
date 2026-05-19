---
name: paper-source-surface-radius-optimization-eclipse-streamer
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-source-surface-radius-optimization-eclipse-streamer

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when **optimizing the PFSS source-surface
radius `R_ss`** for a given Carrington rotation by maximizing
agreement with eclipse white-light streamer geometry or pB
neutral-line crossings.

## Layer 1 — Scientific invariant

- **Paper identity:** PFSS Source-Surface Radius Optimization via
  Eclipse / Streamer Comparison (representative: Lee+ 2011; Badman+
  2020/2022).
- **Year:** TODO verify.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

The "best" `R_ss` for a given CR varies between `~1.5` and `~3.0
R_sun` and is determined by maximizing the agreement between the
PFSS neutral line at `R_ss` and observed eclipse-streamer mean
plane / pB neutral-line crossing. The narrow claim is that
**fixed `R_ss = 2.5 R_sun` is wrong cycle-phase-by-cycle-phase**.

### Method assumptions

- PFSS solver accepts variable `R_ss`.
- Eclipse white-light image (or pB streamer trace) is available.
- Agreement metric is a chosen geometric distance.

### Failure modes (skill memory)

- **Eclipse cadence** is rare; PSP / SO pB conjunctions can
  substitute but with different systematics.
- **Streamer-band thickness** introduces a residual floor.
- **Polar fill-in** affects the apparent neutral-line position.

### Claim boundary

**In scope.** PFSS `R_ss` optimization on individual CRs given
suitable observations.

**Out of scope.** Do NOT extrapolate the best `R_ss` to other CRs
without re-fitting.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `pfss.solve()` (R_ss parameterized)     | run grid                 |
| `eclipse.fetch_image()` or `imagery.fetch_lasco_pb()` | obs |
| `geometry.compare_neutral_line()`       | agreement metric         |
| `optimization.scan_r_ss()`              | choose best R_ss         |

### Procedure

1. Fix CR; choose observation (eclipse or pB).
2. Run PFSS over a grid of R_ss ∈ [1.5, 3.5] R_sun.
3. Compare neutral-line geometry to observation.
4. Pick R_ss minimizing the chosen metric.

### Validation target

TODO verify — chosen R_ss reproduces published "best" value within
~0.1 R_sun.

## Layer 3 — Adapter / runtime notes (optional examples)

- `sunkit-magex.pfss` supports parameterized R_ss; eclipse images
  via processed JPEGs or pB from LASCO.

## Layer 4 — Research-generation affordances

- **Gap:** R_ss optimization has rarely been combined with the
  open-flux problem
  (`[[paper-open-flux-problem-in-situ-vs-pfss-discrepancy]]`) on
  matched CRs.
- **Hypothesis:** the optimal R_ss correlates with WSA coefficient
  drift in `[[paper-arge-2003-wsa-model-source-surface-wind-prediction]]`.

## Skill graph → depends_on

- `[[paper-eclipse-white-light-benchmark-pfss-models]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
