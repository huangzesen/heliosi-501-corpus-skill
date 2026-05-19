---
name: coronal-hole-loop-statistics-potential-field-modeling
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# coronal-hole-loop-statistics-potential-field-modeling

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow needs **statistical PFSS topology
inside coronal holes** — open/closed populations, loop-length
distributions, expansion-factor histograms — across many CH realizations
rather than a single case.

Concrete symptoms:

- A coronal-hole catalog (or detection pipeline) exists and the user
  asks for the open-flux / closed-loop topology distribution inside CHs.
- A source-mapping skill needs CH-interior priors (e.g. expected
  expansion-factor range) before footpoint matching.
- Cycle-dependence question: "does CH topology change between minimum
  and maximum?"

Do NOT use this skill for single-event case studies or for non-CH
active-region topology.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Magnetic Topology and Loop Statistics in Observed Coronal
  Holes Using Potential Field Modeling
- **First author:** TODO verify
- **arXiv:** 2601.11080
- **Year:** 2026
- **Venue:** TODO verify

### Claim (narrow form)

The paper applies PFSS-based topology and loop-statistics analysis to
**702 observed coronal holes between 2010 and 2019**. The narrow claim
is that within this sample, statistical distributions of CH-interior
loop topology (open/closed populations, lengths, expansion factors)
are characterizable and show cycle-phase dependence.

### Method assumptions

- A CH catalog or detection pipeline defines boundaries.
- PFSS is solved per CH on a matched-date synoptic Br.
- Field lines are seeded inside each CH boundary; open/closed
  classification is derived from tracing outcome.
- Loop length (closed) and expansion factor
  `f = (R_sun/R_ss)² (B_r(photosphere)/B_r(R_ss))` (open) are computed
  from traced lines.

### Data assumptions

- AIA 193 Å imagery (or equivalent EUV channel) for CH detection.
- Synoptic Br (HMI / GONG) matched to each CH observation date.
- A CH catalog whose detection criteria are documented.

### Failure modes (skill memory)

- **CH boundary definition is fuzzy.** Different detectors (SPoCA,
  CHIMERA, paper's own) yield different "inside-CH" seed populations.
- **Seed density bias.** Equal-area vs equal-`sin(lat)` vs uniform on
  `(theta, phi)` seeding biases the statistics; report the convention.
- **`R_ss` choice.** Expansion factor scales with `R_ss`; using 2.0 vs
  2.5 R_sun shifts the distributions meaningfully.
- **Synoptic Br matching.** Using a CR-centered synoptic when the CH
  observation is far from CR center under-samples relevant photospheric
  Br.
- **Polar CHs.** Polar CHs are particularly sensitive to polar-Br
  extrapolation (polar-filled vs raw choice).
- **Selection bias.** A catalog that picks only dark-EUV CHs misses
  weak-contrast CHs at solar maximum; cycle-dependence inherits this.

### Figure / numerical targets

- TODO verify: (a) median expansion-factor histogram by cycle phase or
  (b) open/closed ratio per CH; reference figure identifier TODO verify
  (likely multi-panel histogram by year).

### Claim boundary

**In scope.** Statistics of CH-interior PFSS topology over the paper's
702-CH sample (2010–2019), with the paper's CH detection and PFSS
parameter choices.

**Out of scope — do NOT generalize:**

- Do NOT claim "all coronal holes have property X" — the conclusion is
  a distribution, not a per-CH guarantee.
- Do NOT extend beyond 2010–2019 without re-running with consistent
  detection and Br products.
- Do NOT use the result to predict in-situ solar-wind properties
  directly — the link is at best statistical via expansion factor.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `ch_catalog.iterate()`              | enumerate (date, boundary) entries     | any catalog binding |
| `imagery.fetch_aia193()`            | EUV CH boundary verification           | per CH date |
| `magnetogram.fetch_synoptic_br()`   | matched-date Br                        | per CH date |
| `pfss.solve()`                      | PFSS field per CH date                 | precondition |
| `field.seed_field_lines()`          | seed pattern inside CH boundary        | document convention |
| `field.trace_lines()`               | classify open/closed; compute length   | tracer-tool-agnostic |
| `field.expansion_factor()`          | per-line `f`                           | local |
| `statistics.aggregate_histograms()` | per-CH + cycle-phase histograms        | trivially local |

### Procedure

1. **Iterate** over CH catalog (702 entries in the paper).
2. **For each CH** (date, boundary mask):
   a. Fetch matched-date synoptic `B_r`.
   b. Compute PFSS at chosen `R_ss`, `l_max`.
   c. Seed field lines inside the CH boundary; document seed convention.
   d. Trace each line; classify open/closed.
   e. Compute loop length (closed) and expansion factor (open).
3. **Per-CH record:** `{date, lat, lon, area, N_open, N_closed,
   mean_loop_len, mean_expansion}`.
4. **Aggregate histograms** by year / cycle phase.
5. **Compare** to paper-reported distributions.

### Validation target

- **Metric:** TODO verify (likely median expansion-factor histogram by
  cycle phase, or open/closed ratio per CH).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `pfss.solve` to `sunkit-magex.pfss` and
  `field.trace_lines` to FortranTracer / PythonTracer.
- CH detection can be served by any of SPoCA, CHIMERA, custom AIA
  thresholding, or the paper's own pipeline; the skill is agnostic.
- The 702-CH loop is embarrassingly parallel — the skill works with
  any concurrency framework or a serial run.

LingTai's `[[pfss-tracing]]` binds `pfss.solve` + `field.trace_lines`
end-to-end with FortranTracer and PSP-style ballistic mapping, but is
not assumed by this skill.

---

## Layer 4 — Research-generation affordances

- **Gap:** the paper reports CH-interior topology *distributions* but
  the link to in-situ solar-wind properties is statistical. Composing
  with `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]`
  bridges to SASW origin, asking whether expansion-factor distributions
  in low-B_0 small CHs match the SASW two-population partition.
- **Tension:** if conclusions depend on CH detection, then independent
  detectors (SPoCA / CHIMERA / paper's own) should be reproducible
  *into* the same distribution. Re-running the pipeline with a
  different detector on the same 702-CH sample exposes how much of the
  cycle dependence is real vs detection-induced.
- **New hypothesis:** the cycle-phase dependence of CH-interior topology
  should correlate with the cycle-phase dependence of PFSS-vs-eclipse
  agreement (`[[paper-eclipse-white-light-benchmark-pfss-models]]`),
  since both ultimately depend on the same boundary Br.
- **Composable experiment:** run the NSPF solver
  (`[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`)
  on each CH's epoch and ask whether NSSS deformation shifts open-line
  seed counts relative to spherical PFSS.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  PFSS solver used 702 times must be verified.
- `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]` — would
  affect CH-interior topology for CHs near the farside boundary; a
  sensitivity check.

## Links

- arXiv: https://arxiv.org/abs/2601.11080
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.6
