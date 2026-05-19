---
name: paper-arge-2003-wsa-model-source-surface-wind-prediction
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-arge-2003-wsa-model-source-surface-wind-prediction

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when applying the **Wang-Sheeley-Arge (WSA)
empirical wind model** to predict solar-wind speed at 1 au from PFSS
expansion factor `f_s` and angular distance to coronal-hole boundary
`θ_b`.

## Layer 1 — Scientific invariant

- **Paper identity:** WSA Solar Wind Speed Model (Arge & Pizzo 2000;
  Arge et al. 2003/2004).
- **First author:** C. N. Arge
- **Year:** 2003
- **Venue:** AIP / JGR — TODO verify.

### Claim (narrow form)

The WSA empirical relation
`v_SW = v_0 + a / (1+f_s)^b · g(θ_b)` maps PFSS expansion factor and
CH-boundary distance to 1-au wind speed with `~50–100 km/s` typical
RMS error, given a tuned set of `(v_0, a, b, …)` coefficients.

### Method assumptions

- A global PFSS solution provides `f_s` at the source surface.
- Coronal-hole boundary is identifiable in `B_r` open-flux map.
- Coefficients are tuned per epoch.

### Failure modes (skill memory)

- **Coefficient drift** across cycle phase.
- **Source-surface radius** choice changes `f_s` significantly.
- **Slow-wind streamer-belt regions** are under-predicted.

### Claim boundary

**In scope.** 1-au solar-wind-speed prediction in steady-state
regimes.

**Out of scope.** Do NOT use during CME-dominated intervals.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `pfss.solve()`                          | global PFSS              |
| `field.expansion_factor()`              | `f_s` at source surface  |
| `topology.distance_to_boundary()`       | `θ_b`                    |
| `wsa.predict_speed()`                   | empirical formula        |
| `metrics.rms_vs_in_situ()`              | 1-au comparison          |

### Procedure

1. Solve PFSS on the synoptic Br.
2. Compute `f_s` and `θ_b` along source-surface field lines.
3. Apply the WSA formula.
4. Compare to in-situ at 1 au.

### Validation target

TODO verify — RMS error `~50–100 km/s` on a benchmark CR.

## Layer 3 — Adapter / runtime notes (optional examples)

- The NOAA SWPC operational WSA pipeline is one adapter; `pfsspy`
  + custom WSA evaluator is another.

## Layer 4 — Research-generation affordances

- **Gap:** WSA's coefficients have rarely been retuned with the new
  GONG-ADAPT ensemble — pair with
  `[[paper-gong-network-synoptic-magnetogram-product]]`.
- **Hypothesis:** the slow-wind under-prediction correlates with
  pseudostreamer connectivity
  (`[[paper-coronal-hole-pseudostreamer-boundary-classification]]`).

## Skill graph → depends_on

- `[[paper-csss-current-sheet-source-surface-non-radial-open-flux]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
