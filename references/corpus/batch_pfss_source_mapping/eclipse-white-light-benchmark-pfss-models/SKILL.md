---
name: eclipse-white-light-benchmark-pfss-models
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# eclipse-white-light-benchmark-pfss-models

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow needs to **benchmark a PFSS
coronal model against observed coronal morphology** using total solar
eclipse white-light images as visual ground truth.

Concrete symptoms:

- A PFSS solution exists for an eclipse epoch and the user asks whether
  the model reproduces the observed streamer / helmet pattern.
- A new PFSS variant (multi-constraint, NSPF) needs an *observational*
  acceptance test independent of in-situ open flux.
- Cycle-dependence question: "is PFSS more reliable at solar minimum
  than at maximum, observationally?"

Do NOT use this skill for in-situ open-flux benchmarks (use the open-
flux skill) or for non-eclipse white-light contexts.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Total Solar Eclipse White Light Images as a Benchmark for
  PFSS Coronal Magnetic Field Models
- **First author:** TODO verify
- **arXiv:** 2408.16149
- **Year:** 2024
- **Venue:** TODO verify

### Claim (narrow form)

The paper compares PFSS coronal field predictions against total solar
eclipse white-light images across a solar cycle, using the eclipses as
visual ground truth for streamer / closed-field-region morphology. The
narrow claim is that PFSS agreement with eclipse morphology is
quantifiable and varies systematically with cycle phase.

### Method assumptions

- PFSS field is projected onto a plane-of-sky image as viewed from
  Earth on each eclipse epoch.
- Streamer and helmet-streamer structures in the eclipse image are
  treated as proxies for closed-field-region projections.
- An agreement metric is defined that operates on the projected
  field-line image and the eclipse image.

### Data assumptions

- Eclipse white-light images for the paper's set are available (TODO
  verify source: Druckmüller-processed, expedition repositories, etc.).
- Synoptic Br for each eclipse epoch is fetchable.
- Optional LASCO C2 / C3 imagery for augmentation.

### Failure modes (skill memory)

- **Eclipse-image processing differs by source.** Druckmüller-processed
  enhances low-contrast structure differently than other pipelines; the
  agreement metric can flip with processing.
- **Plane-of-sky projection.** Streamer "edges" are line-of-sight
  integrals; projecting field lines without LOS integration over a
  density model over-or-understates apparent agreement.
- **`R_ss` sensitivity.** Streamer cusp heights depend on `R_ss`;
  reporting agreement without `R_ss` is meaningless.
- **Synoptic-vs-instantaneous offset.** Eclipses are instantaneous;
  CR-averaged synoptic Br can mismatch by days of farside evolution.
- **Cycle-phase confounding.** Solar maximum has more transient CMEs in
  eclipse images that PFSS *cannot* model regardless of solver quality.
- **Coordinate frame.** Heliocentric vs heliographic, ecliptic vs
  Carrington — frame mis-wirings produce "PFSS is rotated" errors.

### Figure / numerical targets

- TODO verify: likely (a) angular offset of streamer cusps in degrees;
  (b) IoU between closed-region projection mask and eclipse-bright
  structure; cycle-spanning multi-eclipse panel TODO verify identifier.

### Claim boundary

**In scope.** PFSS field projections compared to eclipse white-light
imagery, across the paper's eclipse set, with the paper's choice of
processing and PFSS parameters.

**Out of scope — do NOT generalize:**

- Do NOT use to declare PFSS "right" or "wrong" — eclipse benchmarks
  are visual; the comparison is sensitivity, not certification.
- Do NOT generalize to non-eclipse coronal imagery.
- Do NOT carry agreement metric across PFSS variants without re-running
  on the same eclipse set.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `eclipse.fetch_image()`             | white-light image for given eclipse    | manual / archive |
| `imagery.fetch_lasco()` (optional)  | augmentation                           | external |
| `magnetogram.fetch_synoptic_br()`   | matched-date Br                        | per eclipse |
| `pfss.solve()`                      | global PFSS                            | precondition |
| `field.trace_streamer_belt_seeds()` | dense seeding along neutral line       | local |
| `field.project_to_pos()`            | plane-of-sky projection                | local heliocentric transforms |
| `metrics.streamer_agreement()`      | paper-defined metric (TODO verify)     | local |

### Procedure

1. **For each eclipse:** identify date, sub-Earth heliographic
   coordinates, plane-of-sky orientation.
2. **Fetch matched synoptic Br** (closest CR; consider synchronic
   product if available).
3. **Compute PFSS** at chosen `R_ss`, `l_max`.
4. **Trace field lines:** dense seeds along the model neutral line at
   `R_ss` + a sparse global seed grid.
5. **Project** traced lines onto the plane of sky from the eclipse
   geometry; render as a synthetic field-line image.
6. **Compare** to the eclipse image:
   - Streamer-cusp angular positions.
   - Helmet-streamer base width.
   - Closed-region latitudinal extent.
   Compute paper-defined agreement metric.
7. **Aggregate** across eclipses and stratify by cycle phase.

### Validation target

- **Metric:** TODO verify (cusp offset deg; IoU; or paper's own).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `pfss.solve` to `sunkit-magex.pfss` and
  `field.project_to_pos` to sunpy WCS / heliocentric transforms.
- Eclipse image acquisition currently has no standard remote contract;
  the user provides a local image archive or a manual fetch.
- LingTai's `[[pfss-tracing]]` binds `pfss.solve` +
  `field.trace_streamer_belt_seeds` end-to-end, but is not required.

---

## Layer 4 — Research-generation affordances

- **Gap:** the paper benchmarks PFSS only. The same protocol with
  `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`,
  `[[paper-multi-constraint-pfss-extrapolation-model]]`, and HCCSSS
  from `[[paper-comparison-coronal-extrapolation-cycle-24-hmi]]` lets a
  workflow ask which extension *most* improves eclipse agreement at
  each cycle phase.
- **Tension:** if PFSS-vs-eclipse agreement degrades at maximum, that
  could reflect (a) PFSS missing currents, (b) magnetograph polar
  weakness, or (c) transient CME confounders. A composable experiment
  separates these by replacing PFSS with NSPF/multi-constraint while
  also swapping HMI for synchronic + AI-farside Br.
- **New hypothesis:** the agreement metric should improve more on
  synchronic-driven runs at high activity than on synoptic-driven runs,
  because farside ARs evolve fastest then.
- **Composable experiment:** project density via a coronal density
  model rather than treating streamer brightness as a thresholded
  field-line image; this isolates magnetic-topology agreement from
  density-distribution agreement.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  solver used must be verified before observational benchmarking.
- `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]` —
  alternative model benchmarked against the same eclipses for a fair
  comparison.
- `[[paper-comparison-coronal-extrapolation-cycle-24-hmi]]` — sibling
  benchmark using HCS / open flux rather than eclipse imagery.

## Links

- arXiv: https://arxiv.org/html/2408.16149
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.9
