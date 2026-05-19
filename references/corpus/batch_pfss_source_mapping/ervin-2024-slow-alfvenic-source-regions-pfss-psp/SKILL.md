# ervin-2024-slow-alfvenic-source-regions-pfss-psp

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow needs to **map slow Alfvénic solar
wind (SASW) intervals at PSP back to their solar source regions**, in
the inner heliosphere, using PFSS-driven footpoint mapping.

Concrete symptoms:

- SASW intervals at PSP are flagged and the user asks whether they come
  from coronal holes or somewhere else.
- A source-mapping skill needs the *two-population* prior that Ervin
  et al. 2024 established (low-`B_0` small CHs / over-expanded
  boundaries vs. high-field-strength sources).
- Cross-checking source-mapping results against heavy-ion composition
  to disambiguate CH-origin vs non-CH-origin SASW.

Do NOT use this skill for fast-Alfvénic wind classification or for
ICME/CME source mapping.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Characteristics and Source Regions of Slow Alfvénic Solar
  Wind Observed by Parker Solar Probe
- **First author:** Tamar Ervin
- **Authors:** T. Ervin, K. Jaffarove, S. T. Badman, J. Huang,
  Y. J. Rivera, S. D. Bale
- **arXiv:** 2407.09684 (v2)
- **Year:** 2024 (published 2024-07-12)
- **Venue:** TODO verify

### Claim (narrow form)

Using a heliocentric-distance-based classification scheme on PSP
Encounters 4–14 near-perihelion data, Ervin et al. apply PFSS +
ballistic mapping to identify the source regions of slow Alfvénic
solar wind. The narrow claim from inventory is that SASW has **two
source populations**:

1. A *primary* population from **low-`B_0` regions**, likely small
   coronal holes and their **over-expanded boundaries**.
2. A *secondary* population from **high-field-strength source regions**
   (details TODO verify from full text).

### Method assumptions

- A distance-conditioned SW-type classification flags SASW intervals.
- PFSS is solved on a synoptic Br matched to each interval.
- Ballistic back-mapping from PSP to the source surface is the first
  step of footpoint mapping; field-line tracing handles the second.
- Source typing is by photospheric `B_0` at the footpoint patch,
  optionally cross-checked with heavy-ion composition.

### Data assumptions

- PSP FIELDS MAG L2 (RTN) covers Encounters 4–14 perihelia.
- PSP SWEAP bulk moments + Alfvénicity diagnostics available.
- Heavy-ion composition available (TODO verify exact source / instrument).
- Synoptic Br fetchable for matched dates.
- Ephemeris available (Horizons or SPICE).

### Failure modes (skill memory)

- **Ballistic-only vs Parker-spiral.** Slow wind is more sensitive to
  the choice than fast wind. Document and consider the source-alignment
  link (`[[paper-dakeyo-2026-source-alignment-psp-solo-method-link]]`).
- **`R_ss` choice.** Footpoints near CH boundaries are sensitive to
  `R_ss`; report and sweep.
- **Synoptic vs synchronic Br.** Encounters 4–14 span enough time that
  CR-averaged synoptic maps can misrepresent the relevant farside Br;
  see `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]`.
- **SASW classification ambiguity.** "Slow Alfvénic" lacks a single
  community definition; the threshold on `|σ_c|` and `v_sw` biases the
  partition.
- **Composition vs MAG cadence.** Composition is typically much lower
  cadence; an interval that looks composition-CH-like at coarse
  resolution can be confounded by fine-scale embedded structures.
- **Overexpanded boundary sub-resolution.** Mapping footprint patches
  smaller than the PFSS spatial resolution mis-types overexpanded
  boundaries as CH interiors.

### Figure / numerical targets

- TODO verify: likely fraction of SASW intervals mapping to low-`B_0`
  sources vs high-field-strength sources; reference figure identifier
  TODO verify.

### Claim boundary

**In scope.** Two-population source-region typing for SASW intervals
in PSP Encounters 4–14, near perihelion, with the paper's
classification and PFSS parameters.

**Out of scope — do NOT generalize:**

- Do NOT generalize to non-Alfvénic slow wind — distinct literature
  and source-region landscape.
- Do NOT use to declare individual stream provenance without
  per-stream uncertainty.
- Do NOT extend to Encounters outside 4–14 or to PSP-aphelion windows
  without re-mapping.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `in_situ.fetch_psp_mag()`           | PSP FIELDS MAG L2 RTN                  | per perihelion |
| `in_situ.fetch_psp_sweap()`         | bulk moments + Alfvénicity             | per perihelion |
| `in_situ.fetch_psp_composition()`   | heavy-ion comp. (where available)      | TODO verify source |
| `magnetogram.fetch_synoptic_br()`   | matched-date Br                        | per interval |
| `ephemeris.psp()`                   | PSP position                           | local-or-remote |
| `pfss.solve()`                      | PFSS field per epoch                   | precondition |
| `mapping.ballistic_to_source_surface()` | PSP → SS footprint                 | local |
| `field.trace_to_photosphere()`      | SS → photosphere footpoint             | tracer-tool-agnostic |
| `classification.label_sw_type()`    | SASW per paper's scheme                | local |
| `classification.label_source_region()` | low-`B_0` CH boundary vs high-field | local |
| `statistics.aggregate_populations()`| population split                       | local |

### Procedure

1. **Define perihelion intervals** for PSP Encounters 4–14.
2. **Classify SASW** per paper's scheme: compute solar-wind speed and
   Alfvénicity at PSP; apply distance-dependent thresholds
   (TODO verify thresholds).
3. **For each SASW interval:**
   a. Ballistically back-map PSP to source surface; PFSS-trace to
      photosphere.
   b. Sample photospheric `B_0` at the footpoint patch.
   c. Cross-check with heavy-ion composition (e.g. O7+/O6+ proxy).
4. **Type sources:** low-`B_0` (CH / over-expanded boundary) vs
   high-field-strength.
5. **Aggregate:** distribution of source types across all SASW
   intervals in E4–E14.
6. **Report** population split and compare to paper's two-population
   finding.

### Validation target

- **Metric:** fraction of SASW intervals mapping to low-`B_0` sources
  vs high-field-strength sources.
- **Tolerance:** TODO verify; ±10 percentage points of the paper's
  reported split as a starting pass band.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `pfss.solve` and `field.trace_to_photosphere`
  to `sunkit-magex` + FortranTracer; in-situ fetch to `pyspedas` /
  Fido against CDAWeb; ephemeris to `sunpy.coordinates`.
- The skill is agnostic about agent harness; nothing in Layer 2
  requires a specific framework.

LingTai supplies bindings via `[[pfss-tracing]]` and an in-situ skill
in `.library/custom/psp-data-analysis/`, but those are not assumed.

---

## Layer 4 — Research-generation affordances

- **Gap:** the two-population partition is established statistically.
  A natural follow-on is per-stream uncertainty quantification —
  composing with `[[paper-dakeyo-2026-source-alignment-psp-solo-method-link]]`
  to track individual SASW parcels between PSP and SO would test
  whether each parcel remains in its assigned population at 1 au.
- **Tension with `[[paper-coronal-hole-loop-statistics-potential-field-modeling]]`.**
  The CH-population skill characterizes CH-interior topology; this
  skill characterizes solar-wind origins. The two should mutually
  predict each other: low-`B_0` small CHs / over-expanded boundaries
  in the 702-CH sample should be the loci where SASW originates.
  Confirming this is a composable experiment.
- **New hypothesis:** the high-field-strength SASW source population
  may be sensitive to the synoptic-vs-synchronic boundary choice
  more than the low-`B_0` population, because over-expanded boundaries
  are slower to migrate.
- **Composable experiment:** repeat the entire mapping pipeline with
  NSPF (`[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`)
  in place of baseline PFSS and ask whether the partition holds, or
  whether NSSS-deformation moves a fraction of intervals between
  populations.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  PFSS solver inside per-interval source typing should be verified.
- `[[paper-dakeyo-2026-source-alignment-psp-solo-method-link]]` —
  source-mapping method that adds Parker-spiral propagation and
  matched-pair selection between spacecraft.
- `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]` —
  alternative boundary condition.
- `[[paper-coronal-hole-loop-statistics-potential-field-modeling]]` —
  CH-population prior the SASW partition should be consistent with.

## Links

- arXiv: https://arxiv.org/abs/2407.09684
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md` §12
