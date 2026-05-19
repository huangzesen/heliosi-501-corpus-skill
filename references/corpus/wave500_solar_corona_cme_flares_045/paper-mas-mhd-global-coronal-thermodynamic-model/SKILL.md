---
name: paper-mas-mhd-global-coronal-thermodynamic-model
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# paper-mas-mhd-global-coronal-thermodynamic-model

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when using the **MAS (Magnetohydrodynamics
Around a Sphere) thermodynamic global coronal model** (Predictive
Science Inc.) as background field / plasma for shock or
SEP-connectivity studies.

## Layer 1 — Scientific invariant

- **Paper identity:** MAS Thermodynamic Global Coronal MHD Model
  (representative: Mikic+ 1999; Lionello+ 2009; Riley+ 2019).
- **Year:** 2009.
- **Venue:** ApJ — TODO verify.

### Claim (narrow form)

The MAS thermodynamic model solves resistive MHD with thermal
conduction, radiative losses, and parameterized heating to produce
coronal `(B, n, T, v)` consistent with white-light + EUV observables
at the eclipse / synoptic level.

### Method assumptions

- Synoptic Br boundary; equilibrium initial condition iterated.
- Parameterized coronal heating (Alfvén-wave or empirical).
- Static or relaxed quasi-steady output.

### Failure modes (skill memory)

- **Heating prescription** dominates Alfvén speed and density.
- **Transient processes** are not captured by steady solutions.
- **Resolution** in the low corona affects open-flux integration.

### Claim boundary

**In scope.** Quasi-steady global coronal background fields for
synoptic-scale studies.

**Out of scope.** Do NOT use as time-resolved CME-driven background.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                  |
|-----------------------------------------|--------------------------|
| `mhd.global_thermodynamic_solve()`      | MAS-class run            |
| `magnetogram.fetch_synoptic_br()`       | boundary                 |
| `diagnostics.synthesize_wl_euv()`       | observable comparison    |
| `metrics.eclipse_streamer_agreement()`  | white-light validation   |

### Procedure

1. Set synoptic Br boundary.
2. Run MAS thermodynamic until steady.
3. Synthesize white-light and EUV; compare to observation.

### Validation target

TODO verify — eclipse-streamer agreement consistent with published
benchmarks.

## Layer 3 — Adapter / runtime notes (optional examples)

- The PSI-`mas` archive and `psipy` Python interface are reference
  adapters.

## Layer 4 — Research-generation affordances

- **Gap:** comparison with AWSoM background for the same CR has
  rarely been quantified — pair with
  `[[paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure]]`.
- **Hypothesis:** MAS-vs-AWSoM `v_A` discrepancy explains differences
  in `[[paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal]]`-style
  shock-parameter maps.

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
