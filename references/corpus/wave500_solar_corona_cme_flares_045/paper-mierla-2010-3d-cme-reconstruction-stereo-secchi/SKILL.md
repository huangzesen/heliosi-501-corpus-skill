---
name: paper-mierla-2010-3d-cme-reconstruction-stereo-secchi
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-mierla-2010-3d-cme-reconstruction-stereo-secchi

> Runtime-neutral paper-skill. Four layers: invariants → executable
> protocol (abstract) → adapter notes → research affordances.

## Trigger

Reach for this skill when the workflow needs a **3-D CME reconstruction
review** — what reconstruction techniques exist (tie-pointing, polarization
ratio, mask fitting, forward modeling, GCS) and which assumptions /
viewpoints each requires.

Concrete symptoms:

- Selecting a 3-D reconstruction technique appropriate to the available
  STEREO/SECCHI viewpoints and CME geometry.
- Comparing reconstruction outputs across methods on the same event.
- Bounding the systematic spread between methods before propagating into
  arrival-time / shock studies.

Do NOT use this skill to *do* the reconstruction itself — it is the
**method-selection** skill; the per-method skill (e.g.
`[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]`) is the operator.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Review of 3-D CME Reconstruction Techniques (STEREO/SECCHI era)
- **First author:** M. Mierla — TODO verify
- **Year:** 2010
- **Venue:** Annales Geophysicae — TODO verify

### Claim (narrow form)

The paper organizes the published 3-D CME reconstruction techniques into
a taxonomy (tie-pointing, mask fitting, polarization ratio, forward
modeling, GCS, harmonic mean), compares outputs on common events, and
shows that the **method-to-method scatter on a single event is a
non-negligible fraction of the parameter** (longitude/latitude ≲ tens of
degrees, height ≲ a few percent), bounding any downstream "the CME was
at X°" claim.

### Method assumptions

- All techniques assume Thomson-scattering brightness as the
  observable; coronagraph calibration is taken as given.
- Viewpoint separation is held fixed during the comparison window.
- Forward models assume self-similar expansion within the comparison
  window.

### Data assumptions

- STEREO A/B SECCHI COR2 (and optionally COR1/EUVI) calibrated white-light.
- LASCO C2/C3 when available.

### Failure modes (skill memory)

- **No "ground truth".** Disagreement between techniques on a single
  event is the only available consistency check; cross-method agreement
  does NOT prove correctness.
- **Halo geometry** breaks tie-pointing entirely.
- **Polarization ratio** assumes a single-point scatterer along the
  LOS — fails for line-of-sight overlap of CME and streamer.
- **Forward-modeling priors** drive the answer when the cost surface
  is flat.

### Figure / numerical targets

- TODO verify: typical inter-method spread on a benchmark event
  (placeholder: ≲ 20° in lon, ≲ 10° in lat, ≲ 5% in height).

### Claim boundary

**In scope.** Taxonomy of pre-2010 SECCHI-era 3-D CME reconstruction
methods and inter-method scatter on benchmark events.

**Out of scope — do NOT generalize:**

- Do NOT claim a "best" method universally; the right method depends on
  geometry and S/N for the event in question.
- Do NOT use the inter-method scatter as a formal uncertainty in a
  Bayesian sense — it is empirical, not statistical.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `imagery.fetch_stereo_cor2()`         | A/B COR2 white-light             |
| `imagery.fetch_lasco()`               | C2/C3 white-light                |
| `geometry.tie_point()`                | identify same feature in 2 views |
| `geometry.polarization_ratio()`       | LOS distance from pB ratio       |
| `geometry.mask_fit()`                 | CME boundary masking             |
| `geometry.forward_model()`            | parametric shell model           |
| `ephemeris.spacecraft()`              | viewpoint geometry               |
| `metrics.method_agreement()`          | cross-method scatter             |

### Procedure

1. **Fetch** all available coronagraph viewpoints for the event.
2. **Apply** each candidate technique that the viewpoint geometry
   supports.
3. **Tabulate** the resulting `(lon, lat, height, width)` per method.
4. **Compute** the inter-method scatter; flag the dominant
   methodological systematic.
5. **Emit** a method-comparison report.

### Validation target

- **Metric:** TODO verify — reproduce the paper's inter-method
  scatter on its benchmark event(s).
- **Tolerance:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python runtime can bind `geometry.tie_point()` to SunPy's
  WCS-aware reprojection plus a manual click-list; polarization-ratio
  to the SECCHI `secchi_prep` pipeline; GCS to `gcs_python`.
- IDL/SolarSoft remains the historical reference adapter for SECCHI
  reconstruction.

---

## Layer 4 — Research-generation affordances

- **Gap:** no public benchmark gives all methods the *same* preprocessed
  event with a shared truth proxy.
- **Tension:** GCS aspect ratios tend to be larger than mask-fit
  widths on the same event — composing with
  `[[paper-thernisien-2011-gcs-fitting-cme-flux-rope]]` would quantify
  the bias.
- **Hypothesis:** the inter-method scatter is dominated by viewpoint
  separation, not by event morphology.
- **Experiment:** rerun all methods on STEREO conjunction periods
  (small viewpoint separation) and on quadrature periods, and see
  which methods degrade.

---

## Skill graph → depends_on

- (none — this is a meta-skill that organizes per-method skills)

## Links

- DOI: TODO verify
- ADS: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
