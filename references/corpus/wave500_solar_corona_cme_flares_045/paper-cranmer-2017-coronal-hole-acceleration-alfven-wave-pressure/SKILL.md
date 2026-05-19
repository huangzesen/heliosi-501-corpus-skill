# paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when modeling **fast solar-wind acceleration from a
coronal hole** with an Alfvén-wave-turbulence-driven model, in
particular when reproducing fast-wind speed, density, and temperature
asymptotic to ~0.3 au.

## Layer 1 — Scientific invariant

- **Paper identity:** Coronal-Hole Wind Acceleration via Alfvén-Wave
  Pressure (representative: Cranmer 2017 review; van der Holst+ 2014
  AWSoM).
- **Year:** 2017.
- **Venue:** Living Reviews in Solar Physics — TODO verify.

### Claim (narrow form)

A 1-D (or 3-D AWSoM-style) Alfvén-wave turbulence model with
photospheric wave Poynting flux `~10^5 erg cm^-2 s^-1` and
WKB+turbulent damping reproduces fast solar-wind asymptotic speed
`~700–800 km/s` and density `n_p ≈ few cm^-3` at 1 au within stated
agreement.

### Method assumptions

- Outgoing Alfvén waves at the coronal base with a chosen Poynting
  flux.
- Turbulent damping prescription (von Kármán phenomenology) closes
  the dissipation.
- Single-fluid or two-fluid extension (proton + electron).

### Failure modes (skill memory)

- **Base Poynting flux** is the single most important free parameter.
- **Slow-wind regimes** are NOT covered by this acceleration mechanism
  alone.
- **Frequency-dependent reflection** can either be omitted (WKB) or
  included (non-WKB) — choose explicitly.

### Claim boundary

**In scope.** Fast solar wind from large equatorial / polar coronal
holes.

**Out of scope.** Do NOT apply to slow streamer-belt wind or
transient ICMEs without modification.

## Layer 2 — Executable protocol (capability-typed)

| Capability                              | Purpose                          |
|-----------------------------------------|----------------------------------|
| `mhd.alfven_wave_turbulence_model()`    | 1-D / 3-D AWSoM-class run        |
| `mhd.boundary_alfven_poynting_flux()`   | base condition                   |
| `field.expansion_factor()`              | super-radial geometry            |
| `metrics.asymptotic_wind_match()`       | speed/n/T at 0.3–1 au            |

### Procedure

1. Set base Alfvén-wave Poynting flux.
2. Run AWSoM-class model along a super-radial flux tube (or 3-D).
3. Compare asymptotic `(v, n, T)` to in-situ at 0.3–1 au.

### Validation target

TODO verify — fast-wind `(v, n, T)` within ~20% of in-situ on
benchmark coronal holes.

## Layer 3 — Adapter / runtime notes (optional examples)

- AWSoM (`SWMF`) is one published adapter; ZEPHYR (Cranmer 2017) is
  another.

## Layer 4 — Research-generation affordances

- **Gap:** the same coronal hole has rarely been run through AWSoM
  *and* ZEPHYR with identical boundary conditions.
- **Tension:** the model's asymptotic density is often above PSP
  in-situ values for fast wind near perihelion — pair with
  `[[paper-adhikari-2026-alfven-transition-young-solar-wind-solar-max]]`.
- **Hypothesis:** the base Poynting flux required to match in-situ
  scales with the CH-boundary expansion factor.

## Skill graph → depends_on

- `[[paper-coronal-mhd-alfven-wave-poynting-flux-base]]`
- `[[paper-mas-mhd-global-coronal-thermodynamic-model]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
