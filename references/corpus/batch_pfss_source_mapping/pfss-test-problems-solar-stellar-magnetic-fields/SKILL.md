---
name: pfss-test-problems-solar-stellar-magnetic-fields
description: Per-entry paper-skill in batch_pfss_source_mapping (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# pfss-test-problems-solar-stellar-magnetic-fields

> Runtime-neutral paper-skill. The body below is layered: (1) scientific
> invariants, (2) executable protocol against abstract capabilities,
> (3) adapter notes (optional examples only), (4) research-generation
> affordances. No specific harness, agent framework, or MCP is required.

## Trigger

Reach for this skill when a workflow must **verify or benchmark a
Potential Field Source Surface (PFSS) solver** — solar or stellar —
against a controlled analytic baseline before trusting its output on
real magnetograms. Concrete symptoms:

- A candidate PFSS implementation (spherical-harmonic, finite-difference,
  finite-element) needs a regression test independent of observations.
- A new code path (different grid, BC implementation, `l_max`,
  source-surface height) has been added and the user must check
  correctness, not just runnability.
- Solar PFSS code is being reused on stellar ZDI maps and the user must
  show the solver is correct outside its training regime.

Do NOT use this skill to validate the PFSS *model* against the Sun (use
observational-benchmark skills); this is a *solver* check.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Test Problems for Potential Field Source Surface
  Extrapolations of Solar and Stellar Magnetic Fields
- **First author:** D. Stansby
- **arXiv:** 2201.07783
- **Year:** 2022
- **Venue:** TODO verify

### Claim (narrow form)

The paper defines a suite of analytic / semi-analytic test problems with
closed-form (or otherwise rigorously specified) PFSS solutions, intended
as a *verification baseline* for solar and stellar PFSS solvers. A
solver that passes the suite at the stated tolerances is *consistent
with the canonical PFSS formulation* (Altschuler–Newkirk 1969 /
Schatten 1969) within the test space the suite covers.

### Method assumptions

- PFSS = Laplace BVP on `[R_sun, R_ss]` with photospheric Neumann data
  `B_r` and outer boundary `B_horizontal = 0` at `r = R_ss`.
- Solver is being asked to recover an analytic solution of that BVP, not
  to model a corona.
- `l_max`, source-surface height, and Br input class are drawn from the
  paper's test set.

### Data assumptions

Theory-grade paper — no observational data required. The "data" are
*paper-defined analytic test inputs* and reference solutions.

### Failure modes (skill memory)

- **Spherical-harmonic vs finite-difference solvers diverge differently.**
  A test problem may exercise truncation error (SH) versus
  discretization error (FD / FEM); conflating these mistakes a regime
  mismatch for a solver bug.
- **Source-surface boundary convention.** Some implementations apply
  `B_horizontal = 0` at `R_ss`, others apply `B_theta = B_phi = 0`.
  They agree for clean analytic inputs but diverge on real magnetograms.
  Record the convention.
- **`l_max` truncation.** Choosing `l_max` too low can hide solver bugs
  by smoothing the problem below the test's design intent.
- **Coordinate frame.** Carrington vs heliographic, `sin(lat)` vs `lat`,
  longitude direction — wiring mismatches produce L_2 ≈ O(1) errors that
  are not really solver bugs.
- **Open-flux integration weighting.** Integrating `|B_r|` at `R_ss` on
  a non-equal-area grid silently mis-weights polar caps.

### Figure / numerical targets

- TODO verify exact L_2 / L_inf tolerances per test case in the paper.
- TODO verify reference figure / table identifier (likely a table of
  L_2 vs `l_max` per problem).

### Claim boundary

**In scope.** Verification of a PFSS solver against the paper's curated
set of analytic test problems within the defined `l_max`, source-
surface height(s), and Br input classes.

**Out of scope — do NOT generalize:**

- Do NOT report "PFSS validated against observations" because a solver
  passes this suite. Solver check, not model check.
- Do NOT certify the solver on Br classes outside the paper's set
  without re-running analogous problems.
- Do NOT use pass/fail to compare PFSS against MHD or NLFFF — different
  problem statements entirely.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                       | Purpose                                  | Notes |
|----------------------------------|------------------------------------------|-------|
| `pfss.solve(Br, l_max, rss)`     | candidate solver under test              | the unit of verification |
| `analytics.testcase_generate()`  | produce paper-defined Br + reference B   | bundled with this skill if reproducible from paper text |
| `numerics.error_norms()`         | L_2, L_inf over a probe grid             | trivially local |
| `filesystem.write_report()`      | persist per-test JSON                    | any harness has this |

No remote service is required.

### Procedure

1. **Materialize test suite.** For each paper-defined test case, emit
   (a) the input synoptic `B_r` on `(N_theta, N_phi)`, (b) the reference
   solution `B_ref(r, theta, phi)` at probe points or as an analytic
   expression.
2. **Run candidate solver** at the paper-specified `(l_max, rss, grid)`
   and capture `(B_r, B_theta, B_phi)` and the open-flux integral.
3. **Compute error norms** L_inf and L_2 of `B_candidate − B_ref` and
   the open-flux error.
4. **Convergence sweep** over `(l_max, N_theta, N_phi)`; verify the
   expected order.
5. **Report** per-test JSON with metrics and pass/fail vs paper-stated
   tolerance.

### Validation target

- **Metric:** L_2 norm of `B − B_ref`, units G.
- **Tolerance:** TODO verify from full text (placeholder: 1% of
  `max|B|` on the test grid).
- **Reference figure:** TODO verify (likely a table of L_2 vs `l_max`).

---

## Layer 3 — Adapter / runtime notes (optional examples)

A given runtime may bind the abstract capabilities differently. None of
these bindings are *required* by the skill.

- A general-purpose Python harness can bind `pfss.solve` to
  `sunkit-magex.pfss` or an in-house solver, and use NumPy / SciPy for
  error norms.
- A finite-element runtime can supply its own solver; the skill is
  intentionally agnostic about the discretization family.
- An agent framework with file I/O permissions writes JSON test reports
  directly; one without can stream them to stdout.

LingTai's `[[pfss-tracing]]` and `[[nspf-fem]]` are concrete *adapter
implementations* of `pfss.solve` and are useful when running this skill
inside that ecosystem, but they are not assumed by the skill.

---

## Layer 4 — Research-generation affordances

When this skill is composed with sibling skills, it enables:

- **Solver-regression as prerequisite gate.** Any downstream PFSS-based
  paper-skill (open-flux, source-mapping, eclipse benchmark) can declare
  this skill as a *precondition*; without it, observational
  disagreements cannot be cleanly attributed to model or solver.
- **Cross-implementation triangulation.** Running the same test suite
  against multiple solvers (`[[paper-multi-constraint-pfss-extrapolation-model]]`
  reduced to its unconstrained limit; `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`
  with NSSS → spherical limit) exposes whether published differences are
  solver-induced or genuinely physical.
- **Stellar-PFSS audit.** Reusing a solar-validated solver on ZDI maps
  of cool stars implies a new test-case class outside the paper's set;
  this skill formalizes the gap and motivates a stellar-test extension.
- **Hypothesis:** convergence-order anomalies on specific test cases may
  correlate with regimes where solvers disagree on real magnetograms —
  a path from controlled tests to interpretable model-difference maps.

---

## Skill graph → depends_on

- `[[paper-multi-constraint-pfss-extrapolation-model]]` — its
  unconstrained limit should regression-test through this suite.
- `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]` —
  the FEM solver underneath NSPF inherits this verification need.
- `[[paper-comparison-coronal-extrapolation-cycle-24-hmi]]` — model
  comparison is meaningless if the solvers being compared are not
  individually verified.

## Links

- arXiv: https://arxiv.org/abs/2201.07783
- DOI: TODO verify
- ADS: TODO verify
- Code: no canonical repo asserted in inventory; TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.1
