---
name: dakeyo-2026-source-alignment-psp-solo-method-link
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# dakeyo-2026-source-alignment-psp-solo-method-link

> Runtime-neutral paper-skill **link entry**. The canonical paper-skill
> for Dakeyo et al. 2026 (arXiv 2605.01511) lives at
> `paper_skill_corpus/pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/`.
> This entry registers the paper under the `pfss_source_mapping` aspect
> without duplicating content. The four-layer scaffold below is filled
> with the *source-mapping-specific* slice only; the rest is at the
> canonical sibling.

## Trigger

Reach for this skill when a workflow needs to **map an in-situ
measurement back to a common solar source** between PSP and Solar
Orbiter (or any two inner-heliosphere spacecraft) using the **source-
alignment** method as a *source-mapping* technique.

Concrete symptoms:

- Building a conjunction-finder that scores candidate windows by
  source-region agreement.
- Selecting matched sub-intervals to measure radial evolution of
  `v`, `n`, `T`, `σ_c`, spectral index.
- Sanity-checking ballistic-only back-mapping against a full source-
  alignment workflow.

For the full algorithm, validation target, and data contracts, load
the canonical paper-skill at the path above.

---

## Layer 1 — Scientific invariant (source-mapping slice)

### Paper identity

- **Title:** On the Radial Evolution of the Solar Wind: The Source
  Alignment Method Applied to PSP and Solar Orbiter Observations
- **First author:** J.-B. Dakeyo
- **arXiv:** 2605.01511
- **Year:** 2026
- **Venue:** A&A (submitted) / ApJ — TODO verify

### Claim — source-mapping aspect

The paper refines prior radial- / Parker-spiral alignment techniques
into an explicit *source alignment method* applicable to PSP × SO. The
*source-mapping aspect* is that each spacecraft's footpoint is
ballistically back-traced to the source surface, then PFSS-projected
to the photosphere, and the two are matched at a *common source
region* (typically a coronal-hole boundary) within a tolerance.

### Method assumptions (source-mapping slice)

- Each spacecraft has independent PSP/SO-style ephemeris.
- A PFSS-class boundary condition (synoptic or synchronic) is shared
  between both spacecraft's source-surface projections.
- A common-source agreement tolerance in HGI longitude (or a defined
  metric) is the matching criterion.

### Data assumptions (source-mapping slice)

See the canonical skill for the full data list. The source-mapping
slice depends on:

- Two-spacecraft ephemerides.
- Per-spacecraft solar-wind speed (used for ballistic back-mapping).
- Shared synoptic / synchronic Br for PFSS.

### Failure modes (source-mapping slice)

- **PFSS source-surface height bias.** Footpoint location is sensitive
  to `R_ss`; the alignment score can change with it.
- **Ballistic-only vs Parker-spiral.** The two predict different transit
  times; the alignment is sensitive to the choice.
- **Stream-interaction regions (SIRs).** A parcel that crosses an SIR
  between spacecraft is no longer the same parcel; matching silently
  fails.
- **Synoptic vs synchronic Br.** Inherits the bias of
  `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]`.

### Claim boundary

**In scope.** The source-alignment method as a *source-mapping skill*
applied to PSP and Solar Orbiter, using PFSS-driven footpoint mapping
plus ballistic + Parker-spiral propagation, in the paper's case set.

**Out of scope — do NOT generalize:**

- Do NOT claim this method works for any pair of spacecraft without the
  longitudinal-alignment precondition.
- Do NOT carry conclusions to remote-sensing-only source mapping; the
  method depends on having in-situ time series at both spacecraft.

---

## Layer 2 — Executable protocol (capability-typed, source-mapping slice)

### Required capabilities (abstract)

| Capability                          | Purpose                                | Notes |
|-------------------------------------|----------------------------------------|-------|
| `ephemeris.spacecraft()`            | each spacecraft's position             | local-or-remote |
| `magnetogram.fetch_synoptic_br()`   | shared boundary Br                     | per window |
| `pfss.solve()`                      | source-surface field                   | precondition |
| `mapping.ballistic_to_source_surface()` | spacecraft → SS footprint          | local |
| `field.trace_to_photosphere()`      | SS → photosphere footpoint             | tracer-tool-agnostic |
| `mapping.match_common_source()`     | tolerance check between spacecraft     | local |

For the *propagation + matched-sub-interval* protocol (Parker-spiral
between spacecraft, cross-correlation alignment), load the canonical
skill.

### Procedure (source-mapping slice)

1. **For each spacecraft:** ballistically back-trace to source surface
   using local bulk speed.
2. **PFSS-trace** SS footprint to photosphere.
3. **Common-source test:** check agreement within a tolerance.
4. **If passes:** hand off to the canonical skill for the propagation +
   matched-interval workflow.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `pfss.solve` to any PFSS implementation and
  `field.trace_to_photosphere` to any tracer. LingTai's
  `[[pfss-tracing]]` provides one binding.
- Ephemeris capability is satisfied by Horizons (`sunpy.coordinates`)
  or by SPICE kernels.
- The skill is intentionally agnostic about agent harness.

---

## Layer 4 — Research-generation affordances

- **Gap:** the source-alignment method depends on the same PFSS that
  every other source-mapping skill depends on; any boundary-condition
  improvement (synchronic + AI farside, NSPF) potentially propagates
  into improved matched-pair selection.
- **Tension:** if the paper's matched-pair list is reproduced under
  PFSS but breaks under NSPF or under synchronic Br, then the radial-
  acceleration headline finding is at risk of being boundary-condition
  artefact.
- **New hypothesis:** the failure mode "SIR contamination" should be
  detectable by a stream-interface classifier applied between
  spacecraft, allowing the matching to *reject* windows automatically.
- **Composable experiment:** combine this skill with
  `[[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]` —
  applying both PSP and SO to the SASW two-population partition tests
  whether the partition holds when wind parcels are tracked rather
  than statistically aggregated.

---

## Skill graph → depends_on

- **Canonical sibling:** `[[paper-dakeyo-2026-source-alignment-psp-solo]]`
  (load this as the primary target).
- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  PFSS solver inside source alignment should be verified.
- `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]` —
  synchronic boundary conditions affect footpoint location.
- `[[paper-comparison-coronal-extrapolation-cycle-24-hmi]]` — model
  choice biases source-mapping outputs.

## Links

- arXiv: https://arxiv.org/abs/2605.01511
- DOI: TODO verify
- ADS: TODO verify
- Canonical paper-skill:
  `paper_skill_corpus/pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/SKILL.md`
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §2.3;
  `psp_analysis_2020_2026.md` entry #3
