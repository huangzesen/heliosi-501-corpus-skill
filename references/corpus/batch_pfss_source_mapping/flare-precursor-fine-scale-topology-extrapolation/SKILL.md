---
name: flare-precursor-fine-scale-topology-extrapolation
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# flare-precursor-fine-scale-topology-extrapolation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow analyzes **fine-scale topology of
the pre-flare coronal field** — null points, separators, quasi-
separatrix layers (QSLs), squashing factor `Q` — via field
extrapolation rather than purely photospheric proxies.

Concrete symptoms:

- A named flare is under study and the user asks what topology was
  developing in the hours before the flare.
- A flare-precursor classifier needs a topology-derived feature time
  series.
- A reviewer wants `Q` maps or null-point inventories from an
  extrapolated field for a specified AR window.

Do NOT use this skill for global / synoptic PFSS studies (insufficient
AR context) or for non-extrapolation flare-prediction methods.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Coronal Magnetic Field Extrapolation and Topological
  Analysis of Fine-Scale Structures during Solar Flare Precursors
- **First author:** TODO verify
- **arXiv:** 2306.03226
- **Year:** 2023
- **Venue:** TODO verify

### Claim (narrow form)

The paper performs coronal field extrapolation on pre-flare HMI vector
magnetograms and analyses the resulting topology, focusing on fine-
scale structures. The narrow claim is that fine-scale topological
features (QSLs, nulls) can be identified and tracked in the precursor
phase of solar flares and that their evolution is informative about
the flare onset.

### Method assumptions

- A field extrapolation is performed on pre-flare HMI vector data; the
  family is NLFFF-class (TODO verify which solver the paper uses).
- Vector magnetograms are preprocessed to be force-free-consistent.
- Topology diagnostics (`Q`, null search, separator tracing) are
  computed on a fine 3-D grid in the AR cutout volume.

### Data assumptions

- HMI vector magnetograms (`hmi.B_*` or `hmi.sharp_cea_720s`) cover the
  precursor window at the chosen cadence (typically 12 min).
- AIA EUV imagery is available for cross-validation of features.
- Optional IRIS / RHESSI / GOES for flare-event context.

### Failure modes (skill memory)

- **NLFFF preprocessing.** Vector magnetograms must be preprocessed
  (force-free consistent) before NLFFF, or the solver diverges /
  converges to non-force-free residuals.
- **Cadence vs convergence trade-off.** NLFFF per 12-min frame at full
  HMI resolution is expensive; coarsening hides fine-scale topology.
- **`Q` noise on coarse grids.** `Q` is logarithmically sensitive;
  coarse field-line integration produces high-`Q` artifacts at cell
  boundaries that mimic real QSLs.
- **Spurious nulls.** Interpolation can produce Poincaré-index ±1
  features that are not real nulls; cross-check by `|B|` gradient.
- **Coordinate frame.** SHARP CEA cutouts use a local frame; mixing
  with full-disk coordinates without rotation produces nonsense
  topology.
- **Pre-flare contamination.** Windows too close to onset can pick up
  flare-driven changes; document the cutoff.

### Figure / numerical targets

- TODO verify: likely (a) max `log10 Q` time series, (b) null count,
  (c) QSL area on the chromospheric base; reference figure TODO verify.

### Claim boundary

**In scope.** Topology diagnostics from coronal field extrapolations on
HMI vector data, in the precursor window of specific named flares.

**Out of scope — do NOT generalize:**

- Do NOT claim a calibrated flare-onset time prediction.
- Do NOT extend to limb events (HMI vector quality degrades near the
  limb).
- Do NOT use PFSS as the extrapolation method for fine-scale AR
  topology — PFSS is too smooth.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `vector_mag.fetch_sharp()`          | HMI SHARP CEA cutouts                  | per cadence |
| `vector_mag.preprocess_ff()`        | force-free preprocessing               | required for NLFFF |
| `extrapolation.solve_nlfff()`       | non-linear force-free field            | external solver family |
| `topology.find_nulls()`             | Poincaré-index null detection          | local |
| `topology.trace_separators()`       | separators from null pairs             | local |
| `topology.compute_q_map()`          | squashing factor `Q` on a slice        | external code or local |
| `imagery.fetch_aia()` (optional)    | EUV brightenings overlay               | per cadence |
| `imagery.fetch_rhessi_goes()` (opt) | flare-event context                    | external |

### Procedure

1. **Select event window** (pre-flare, e.g. t-6 h to onset).
2. **Fetch HMI vector** magnetograms at chosen cadence.
3. **Preprocess** each frame (force-free).
4. **Run NLFFF** per frame.
5. **Per frame** compute null inventory, separator surfaces, `Q` map.
6. **Time series** of topological metrics across the window.
7. **Cross-overlay** with AIA brightenings for spatial co-location.

### Validation target

- **Metric:** TODO verify (max `log10 Q`, null count, or QSL area).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- The NLFFF capability is satisfied by any of: Wiegelmann optimization,
  magnetofrictional, Grad–Rubin, or paper-released code; this skill is
  agnostic about solver.
- `Q`-map computation can use community codes (e.g. QSL3D, FastQSL) or
  local implementations.
- AIA / RHESSI / GOES fetch is satisfied by Fido-class APIs against
  JSOC / VSO / NCEI.

This skill is intentionally agnostic about agent harness; no LingTai-
specific binding is required.

---

## Layer 4 — Research-generation affordances

- **Gap:** the paper analyses *precursors*, not prediction. Composing
  this skill with a calibrated event-time classifier over many flares
  would test whether topology features lead, lag, or co-evolve with
  onset.
- **Tension with `[[paper-multi-constraint-pfss-extrapolation-model]]`.**
  Both inject observational priors into extrapolation, at very
  different scales (synoptic vs AR-fine). A natural experiment is
  whether the multi-constraint formulation, applied at AR scale,
  reproduces NLFFF-derived QSL maps without the cost.
- **New hypothesis:** fine-scale QSL area evolution should correlate
  with photospheric proxies (`R_value`, free-energy estimators) on a
  case-by-case basis; if it does not, the field topology is providing
  independent information.
- **Composable experiment:** apply the same topology pipeline to
  *non-flaring* ARs as a negative control and ask which precursor
  signatures actually discriminate.

---

## Skill graph → depends_on

- `[[paper-multi-constraint-pfss-extrapolation-model]]` — methodological
  sibling at AR scale.

## Links

- arXiv: https://arxiv.org/abs/2306.03226
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify (extrapolation + QSL toolchain)
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.7
