---
name: paper-plasmapy-plasma-physics-python
description: >-
  Use when an agent needs plasma-physics primitives in Python — formulary
  functions (gyrofrequencies, thermal speeds, plasma frequencies),
  dispersion solvers, transport coefficients, particle utilities — central
  claim is that PlasmaPy is the community Python package for plasma physics
  with an astropy-units-aware API (software package).
version: 0.1.0
kind: paper-skill
quality: stub
paper:
  title: "PlasmaPy: an open-source Python package for plasma physics"
  first_author: "PlasmaPy contributors"
  year: 2018
  venue: "software package (no dedicated paper located in local inventory)"
  doi: null
  arxiv_id: null
  ads_bibcode: null
domain:
  primary_theme: other
  secondary_themes: ["waves_instabilities", "kinetic", "fluid"]
  missions: ["n/a"]
  regime: ["MHD-scale", "ion-scale", "kinetic", "fluid"]
trigger_keywords:
  - "plasmapy"
  - "plasma formulary"
  - "gyrofrequency"
  - "thermal speed"
  - "plasma frequency"
  - "Debye length"
  - "Coulomb logarithm"
  - "dispersion relation"
  - "plasma transport coefficient"
  - "particle utilities"
data_products: []
algorithms:
  - name: "Plasma formulary (plasmapy.formulary)"
    equation_refs: []
    external_implementations:
      - "https://github.com/PlasmaPy/PlasmaPy"
  - name: "Particle data classes (plasmapy.particles)"
    equation_refs: []
    external_implementations:
      - "https://github.com/PlasmaPy/PlasmaPy"
  - name: "Dispersion solvers (plasmapy.dispersion)"
    equation_refs: []
    external_implementations:
      - "https://github.com/PlasmaPy/PlasmaPy"
validation_target: null
links:
  doi_url: null
  arxiv_url: null
  ads_url: null
  code_repo: "https://github.com/PlasmaPy/PlasmaPy"
  data_repo: null
claim_boundary:
  scope: >-
    PlasmaPy provides an astropy-units-aware Python library of plasma
    formulas, particle utilities, transport-coefficient calculations, and
    simple dispersion solvers. It is suitable for *general-purpose*
    plasma-physics calculations in Python.
  out_of_scope:
    - "Do not use PlasmaPy as a substitute for specialized solvers (ALPS, PLUME) when full hot-plasma dispersion in arbitrary geometry is required."
    - "Do not assume PlasmaPy dispersion solvers cover the same parameter space as paper-specific tools — its solvers are general but limited."
    - "Do not treat PlasmaPy as a simulation framework; for PIC use OSIRIS/PICLas/Pegasus++."
failure_modes:
  - "Formulary functions silently broadcast over arrays; units must be attached or attached-aware (astropy.units), else SI vs Gaussian errors creep in."
  - "Sign conventions differ between authors; check `plasmapy.formulary.gyrofrequency` documentation for sign per species."
  - "Some formulary functions accept either temperature in eV or K; pass with units to avoid implicit conversion errors."
  - "Dispersion-solver convergence depends on initial guesses; failures are silent or return NaN."
  - "Maintaining astropy-units chain through long calculations is verbose; consider stripping units only after final result."
depends_on: []
provenance:
  generated_by: "HelioSI paper-to-skill factory@2026-05-18"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/github_repos/consolidated_repos.json (PlasmaPy entry)"
  verified_by: null
  verified_at: null
tags: ["heliophysics", "paper-skill", "software-package", "infrastructure", "plasma-physics"]
source_type: software-package
---

# PlasmaPy — paper-skill

> Compiled from the PlasmaPy software package
> (https://github.com/PlasmaPy/PlasmaPy) and local references in
> `sioulas-reproduction/results/github_repos/consolidated_repos.json`.
> **Quality tier**: `stub` — promotion requires a runnable example
> exercising formulary + particles + dispersion.

---

## 1. Trigger

Reach for this skill when:

- A workflow needs a quick formulary value (gyrofrequency, thermal speed,
  Debye length, plasma beta) and wants units enforced.
- An agent is computing transport coefficients (collision frequencies,
  resistivity) for a heliophysics setup.
- A user wants a *general-purpose* dispersion solver for sanity checks
  before reaching for ALPS/PLUME.

Do NOT use this skill when:

- The task requires a *specific* hot-plasma dispersion solver (ALPS,
  PLUME) — defer to those skills.
- The task is a kinetic PIC simulation — out of scope.

## 2. Paper claim → verifiable task

**Claim (narrow form).** PlasmaPy provides a units-aware Python library
of plasma formulas, particle utilities, and basic dispersion solvers
suitable as a community-level plasma toolkit.

**Verifiable task.** A reproduction succeeds when an agent can compute:

- `plasmapy.formulary.gyrofrequency(B=10*u.nT, particle="p+")` returns a
  value matching the analytic `qB/m` to within floating-point precision.
- A two-fluid dispersion solver returns Alfvén-wave roots that match
  the analytic limit.

## 3. Methods / equations → executable workflow

### Plasma formulary

```python
import astropy.units as u
from plasmapy.formulary import gyrofrequency, thermal_speed, plasma_frequency, Debye_length

omega_ci = gyrofrequency(B=10*u.nT, particle="p+")
v_th = thermal_speed(T=1e5*u.K, particle="p+")
omega_pe = plasma_frequency(n=5/u.cm**3, particle="e-")
lambda_D = Debye_length(T_e=1e5*u.K, n_e=5/u.cm**3)
```

### Particle data classes

```python
from plasmapy.particles import Particle
p = Particle("Fe+9")  # Fe IX
print(p.mass, p.charge, p.atomic_number)
```

### Dispersion solvers

```python
from plasmapy.dispersion import two_fluid_dispersion_solution
# parameter dict per docs
```

## 4. Data / instruments → tool contracts

No instrument-specific data. PlasmaPy is a *library*, not a data client.

## 5. Validation target → benchmark artifact

> Not benchmarked yet — `stub`. Promotion to `executable` requires a
> small notebook computing formulary values that match analytic / tabulated
> references.

## 6. Failure modes → skill memory

- **Units discipline** — pass `astropy.units` quantities or the function
  may silently treat values as SI of unspecified unit.
- **eV vs K for temperatures** — preserve units rather than relying on
  implicit conversion.
- **Sign conventions** — verify the documented sign for gyrofrequency
  (often returns absolute value by default).
- **Dispersion-solver init** — bad guesses produce NaN with no error.
- **Performance** — units propagation is slow; for large grids, strip
  units after the formula is correct.

## 7. Claim boundary

**In scope.** Units-aware plasma formulary, particle utilities, simple
dispersion solvers, transport coefficients.

**Out of scope — do NOT generalize beyond:**

- Not a hot-plasma dispersion solver of ALPS / PLUME caliber.
- Not a simulation framework.
- Not a mission data client.

## 8. Links

- DOI: n/a (no dedicated paper located locally; JOSS exists in the
  literature but not surfaced by local inventories)
- arXiv: n/a
- ADS: n/a
- Code: https://github.com/PlasmaPy/PlasmaPy
- Data: n/a

## 9. Skill graph → depends_on

- No paper-skill dependencies (self-contained library).

## Notes

- A JOSS paper for PlasmaPy is reported in the literature but not in
  local inventories. Flag for a verifier to locate; this skill does not
  invent a citation.
