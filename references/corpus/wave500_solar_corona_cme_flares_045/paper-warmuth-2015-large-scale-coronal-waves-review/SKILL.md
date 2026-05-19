---
name: paper-warmuth-2015-large-scale-coronal-waves-review
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-warmuth-2015-large-scale-coronal-waves-review

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when planning a study of large-scale coronal waves
and the analyst needs a **review-level taxonomy** of competing
interpretations (fast-mode, hybrid, field-line stretching, pseudo-wave)
before committing to a particular skill.

Concrete symptoms:

- A new EUV wave is observed and the user must decide which
  interpretive framework applies before running any quantitative
  pipeline.
- A study needs to acknowledge the heterogeneity of "EIT wave" findings
  in the literature.

Do NOT use this skill as the operating procedure for a single event —
defer to `[[paper-eui-euv-wave-fast-mode-mhd-front]]` or its sibling
skills for that.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Large-scale waves in the corona: review of observations
  and interpretations
- **First author:** A. Warmuth — TODO verify exact title
- **Year:** 2015
- **Venue:** Living Reviews in Solar Physics — TODO verify

### Claim (narrow form)

The review organizes large-scale coronal disturbances into competing
classes (fast-mode wave, hybrid wave/non-wave, field-line stretching,
sympathetic eruption, current-shell signature) and shows that
**no single class explains every observed event**; case-by-case
classification is required.

### Method assumptions

- Comparative literature analysis; not a method paper.
- Reference event catalogs are taken as published.

### Data assumptions

- The wave catalog inherits the bias of the EIT/SECCHI/AIA detection
  pipelines used by the underlying studies.

### Failure modes (skill memory)

- **Naming overload.** "EIT wave", "Moreton wave", "EUV wave",
  "coronal bright front" are not interchangeable terms; the skill
  must specify which.
- **Detection bias.** Slower events were undersampled in EIT-era
  catalogs; AIA-era inferences may not be portable backward.
- **Co-temporal ≠ co-causal.** Co-temporal stationary brightenings
  do not prove a pseudo-wave interpretation.

### Figure / numerical targets

- Not applicable (review skill).

### Claim boundary

**In scope.** Taxonomy of large-scale coronal disturbances and
catalog-level statistical claims.

**Out of scope — do NOT generalize:**

- Do NOT cite the review to "explain" a specific event without
  applying a per-event analysis.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                              |
|-------------------------------------|--------------------------------------|
| `literature.aggregate_catalog()`    | accumulate cataloged events          |
| `classification.assign_wave_class()`| place each event in the taxonomy     |
| `statistics.population_summary()`   | counts per class                     |
| `filesystem.write_report()`         | classified-event summary             |

### Procedure

1. **Compile** a candidate event list from existing catalogs.
2. **Classify** each event under the review's taxonomy using its
   stated diagnostic signatures.
3. **Tabulate** class frequencies and benchmark against the review's
   published distribution.
4. **Emit** the classified table + per-class signature checklist.

### Validation target

- **Metric:** TODO verify — class proportions consistent with the
  review's published numbers (within Poisson noise).

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python runtime can bind `literature.aggregate_catalog` to the
  HELIO event archive or the Long et al. SDO/AIA wave catalog.

---

## Layer 4 — Research-generation affordances

- **Gap:** there is no public unified catalog with consistent
  signature labels.
- **Tension:** AIA-era studies favor the fast-mode classification more
  often than EIT-era studies — is this physics or selection bias?
- **Hypothesis:** the residual class fraction (non-fast-mode events)
  scales with active-region complexity, not with event speed.
- **Experiment:** correlate the residual class with SHARP complexity
  measures via
  `[[paper-flare-forecasting-sharp-features-deep-learning]]`.

---

## Skill graph → depends_on

- (none — meta-skill)

## Links

- DOI: TODO verify
- ADS: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
