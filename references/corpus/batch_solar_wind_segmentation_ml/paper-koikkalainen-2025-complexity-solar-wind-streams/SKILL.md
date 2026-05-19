---
name: koikkalainen-2025-complexity-solar-wind-streams
description: >-
  Use when differentiating solar-wind stream types (fast / slow / magnetic-cloud / sheath)
  using information-theory complexity — Jensen-Shannon and Fisher-Shannon planes built
  from permutation entropy and horizontal-visibility-graph (HVG) degree distributions —
  central claim is that magnetic clouds stand out across all metrics and Fisher-Shannon
  gives broader spread than Jensen-Shannon (Koikkalainen et al. 2025, arXiv:2510.05873;
  venue TODO verify).
version: 0.1.0
tags: [machine-learning, information-theory, complexity, entropy, permutation-entropy, hvg, solar-wind, stream-classification, segmentation]
quality_level: pilot
executable_status: scaffold
---

# Koikkalainen 2025 — Complexity Measures for Solar-Wind Stream Classification

> Compiled from Koikkalainen, V., Kilpua, E., Good, S., Osmane, A. (2025), *Exploring Complexity Measures for Analysis of Solar Wind Structures and Streams*, arXiv:2510.05873 (venue TODO verify).
> **Quality tier**: `pilot scaffold` — anchored to the inventory abstract. Permutation embedding order/lag, HVG construction details, and the time-lag scan are TODO verify.

This file is the agent-native compiled form of the paper, not a summary.

---

## 1. Trigger

A future agent should reach for this skill when:

- Building **feature engineering** for downstream supervised solar-wind classifiers (cf. [[paper-camporeale-2017-knn-solar-wind-categorization]], [[paper-bloch-2024-uncertainty-nn-solar-wind-types]]) that leverages **information-theory complexity** instead of raw moments.
- Differentiating **magnetic clouds, sheaths, fast streams, slow streams** using entropy-complexity / Fisher-Shannon plane diagnostics.
- Choosing between **permutation entropy** (global ordinal statistics) and **HVG degree distribution** (local structure) as the entropy source.
- Reporting an **interpretable** classification rather than an opaque NN.

Do NOT use this skill when:

- The downstream task is per-event boundary detection — see [[paper-rudisser-2022-icme-unet-automatic-detection]].
- A simple K-Means / NN classifier on raw moments is already adequate — the complexity features add cost; verify they add accuracy.
- Time-series are short (< several permutation-embedding lengths) — the permutation entropy estimator is biased on short series.

## 2. Paper claim → verifiable task

**Claim (narrow form).** Across **four** solar-wind stream types — fast streams, slow streams, magnetic clouds, sheath regions — entropy-complexity (Jensen-Shannon) and information-plane (Fisher-Shannon) diagnostics built from **permutation entropy** and **HVG degree distributions** yield similar overall classifications, but **Fisher-Shannon** (local) produces a **broader spread** in the entropy-complexity plane than Jensen-Shannon. **Magnetic clouds stand out** across all approaches, particularly in the magnetic-field-magnitude channel. Type-to-type differences become more distinct at **larger time lags**, suggesting universality of small-scale fluctuations.

**Verifiable task.** A reproduction succeeds when an agent:

1. Reproduces the per-interval (entropy, complexity) coordinates for the same labelled stream-type set (TODO verify the catalog source — likely Kilpua-led ICME / sheath / stream catalogs).
2. Reproduces the magnetic-cloud-vs-rest separation in the |B| channel.
3. Reproduces the time-lag-dependent separation trend (small lag → similar, large lag → distinct, except magnetic clouds).

## 3. Methods / equations → executable workflow

### Algorithm 3.1 — Interval selection + labelling

- Procedure:
  1. Use a curated catalog assigning each interval to {fast, slow, magnetic cloud, sheath}. Catalog source TODO verify.
  2. Per interval, pull the time series channel(s) of interest — at minimum |B|; possibly V_sw, n_p.

### Algorithm 3.2 — Permutation entropy + Jensen-Shannon complexity

- Procedure:
  1. Choose embedding order d (typical d=5 or d=6) and lag τ — TODO verify.
  2. Compute permutation entropy H_PE over the d! ordinal patterns.
  3. Compute Jensen-Shannon complexity C_JS = D_JS(P, P_uniform) · H_PE (after normalisation).
  4. Plot (H_PE, C_JS) — the entropy-complexity plane.

### Algorithm 3.3 — Horizontal-visibility-graph entropy

- Procedure:
  1. Build HVG from the time series (nodes = samples; edges = horizontal-visibility links).
  2. Compute degree distribution P(k); compute Shannon entropy of P(k) and its complexity.

### Algorithm 3.4 — Fisher-Shannon information plane

- Procedure:
  1. Compute Fisher information F (local, derivative-based) from the same probability distribution.
  2. Plot (H, F) — the information plane.

### Algorithm 3.5 — Time-lag scan

- Procedure: repeat 3.2–3.4 at multiple τ; track the (H, C) coordinates per stream type as a function of τ. Identify the τ at which stream-type separation is maximised.

Code skeleton (pseudocode at stub tier):

```python
# Pseudocode — runnable at executable+ tier once (d, τ, catalog) are pinned.
def koikkalainen2025_complexity(timeseries, d=5, tau=1):
    h_pe = permutation_entropy(timeseries, order=d, delay=tau)
    c_js = jensen_shannon_complexity(timeseries, order=d, delay=tau)
    hvg_h, hvg_f = hvg_entropy_and_fisher(timeseries)
    return dict(h_pe=h_pe, c_js=c_js, hvg_h=hvg_h, hvg_f=hvg_f)
```

## 4. Data / instruments → tool contracts

| Instrument | Quantity | Level / cadence | Interval | Archive | Fetch hint |
|---|---|---|---|---|---|
| (Likely) Wind MFI | B (GSE) | L2 | Decadal window TODO verify | CDAWeb / SPDF | `cdflib` |
| (Likely) Wind SWE | n_p, V_sw, T_p | L2 | Same | CDAWeb / SPDF | `cdflib` |
| Stream-type catalog | per-interval labels | derived | Same | Kilpua-led catalogs — TODO verify exact citation | n/a |

## 5. Validation target → benchmark artifact

- **Claim**: Fisher-Shannon gives broader spread than Jensen-Shannon; magnetic clouds stand out; type differences grow with τ.
- **Metric**: cluster-separation score in (H, C) plane (e.g., silhouette / Davies-Bouldin); per-type centroid shift with τ.
- **Tolerance**: TODO verify.
- **Reference figure**: TODO verify — the entropy-complexity scatter coloured by stream type and the τ scan are the natural targets.

Recommended check artifacts:

- `koikkalainen2025_features.csv` — per-interval (interval_id, stream_type, channel, τ, H_PE, C_JS, HVG_H, F).
- `koikkalainen2025_plane.png` — entropy-complexity scatter coloured by stream type.

## 6. Failure modes → skill memory

- **Permutation-entropy bias on short series.** Estimator bias scales as 1/N for series shorter than ~5·d! samples.
- **Embedding-order sensitivity.** d=4 vs d=5 vs d=6 shift the C_JS coordinate; the paper's choice is load-bearing.
- **Tie-breaking in permutation patterns.** Ties (equal values) require a tie-breaking rule; sub-optimal handling biases C_JS.
- **HVG is sensitive to noise spikes.** Single-sample outliers create high-degree hubs; despike before HVG construction.
- **Magnetic-cloud rotation pattern.** MCs have a smooth rotation that *minimises* permutation entropy at certain τ — this is the "standout" signature; do not interpret it as "low complexity" in absolute terms.
- **Stationarity assumption.** Both PE and HVG assume the underlying process is at least weakly stationary within the interval; ICME sheaths often violate this.
- **Catalog identity.** Different stream-type catalogs (Kilpua, Möstl, Richardson-Cane) disagree at boundaries; (H, C) statistics inherit the catalog choice.

## 7. Claim boundary

**In scope.** Information-theory complexity features (Jensen-Shannon + Fisher-Shannon planes from permutation entropy and HVG) on 1-au solar-wind time series, used to differentiate four stream types.

**Out of scope — do NOT generalise beyond:**

- Other distance regimes (PSP near-Sun) without re-establishing the (H, C) topology.
- Stream-type definitions other than the paper's four (e.g., CIR, ICME sheaths separated from sheaths, ejecta).
- Per-sample segmentation — the features are interval-aggregated.
- Causal claims about underlying physical processes — the features are statistical.

If a downstream task asks for a generalisation listed above, refuse it and route to a sibling paper-skill (or report none).

## 8. Links

- DOI: TODO verify.
- arXiv: https://arxiv.org/abs/2510.05873
- ADS: TODO verify.
- Code: TODO verify (`pyEntropyHub`, `ts2vg` are common implementations).
- Data: Wind / OMNI L2 (public).

## 9. Skill graph → depends_on

- `[[paper-camporeale-2017-knn-solar-wind-categorization]]` — supervised baseline; complexity features can be added to its feature vector.
- `[[paper-bloch-2024-uncertainty-nn-solar-wind-types]]` — sibling supervised NN; complexity features as input.
- `[[paper-cipher-2025-isax-hdbscan-solar-wind-segmentation]]` — symbolic-clustering alternative.
- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — per-event detector (ICME / MC) consumer of these features.
- `[[paper-kilpua-2022-icme-sheath-psp-segmentation]]` — sibling sheath-structure study (not in this batch).

## Notes

- The "universality at small scales" claim is a strong universality assertion; before benchmarked-tier promotion, verify both the τ-dependence trend *and* the universality range.
