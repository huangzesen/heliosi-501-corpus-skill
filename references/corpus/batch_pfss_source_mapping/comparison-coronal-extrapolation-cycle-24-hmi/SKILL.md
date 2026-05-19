# comparison-coronal-extrapolation-cycle-24-hmi

> Runtime-neutral paper-skill. Layered: (1) scientific invariants,
> (2) executable protocol against abstract capabilities, (3) adapter
> notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when a workflow must **choose between PFSS and a
current-sheet-source-surface (CSSS / HCCSSS) family** of coronal models
for a Cycle-24 HMI-driven analysis.

Concrete symptoms:

- A heliospheric-current-sheet (HCS) prediction misses observed warp and
  the user asks whether a current-sheet-aware model closes the gap.
- An open-flux estimate from PFSS disagrees with in-situ at 1 au / PSP.
- A reviewer asks the agent to defend the choice of extrapolation method
  for a Cycle-24 case study.

Do NOT use this skill for single-CR PFSS work (use baseline PFSS) or for
cycles other than 24 without re-running the comparison.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Comparison of Coronal Extrapolation Methods for Cycle 24
  Using HMI Data
- **First author:** TODO verify
- **arXiv:** 1603.04385
- **Year:** 2016
- **Venue:** TODO verify

### Claim (narrow form)

The paper compares an HCCSSS-class (horizontal-current current-sheet-
source-surface) extrapolation against a standard PFSS model, both driven
by SDO/HMI synoptic `B_r`, for Cycle 24. The narrow claim is that the
two methods differ specifically in their treatment of coronal currents
and therefore in quantities sensitive to those currents — HCS warp and
integrated open flux.

### Method assumptions

- Both methods take the same HMI synoptic `B_r` as boundary data.
- PFSS solves the Laplace BVP up to a spherical source surface at `R_ss`.
- HCCSSS-class solves a modified problem permitting horizontal coronal
  currents and a current-sheet surface at `R_cs`.
- Comparison is performed at a matched upper boundary or via a defined
  projection of one onto the other.

### Data assumptions

- HMI synoptic `B_r` available for the paper's CR range (TODO verify
  exact range).
- Optional 1-au in-situ sector data (Wind / ACE) for downstream context.

### Failure modes (skill memory)

- **HMI synoptic flavour matters.** `hmi.synoptic_mr_polfil` (pole-
  filled) vs raw differ substantially near poles; the comparison can
  flip with the wrong product.
- **Source-surface vs current-sheet-surface heights are not the same
  parameter.** Comparing PFSS at `R_ss=2.5` against HCCSSS with a
  different outer radius confounds model differences with parameter
  differences.
- **Open-flux integration grid.** Equal-area vs uniform-lat grids give
  different numerical open flux at the few-percent level.
- **HCCSSS code availability.** If the paper's solver is not public, a
  reproduction is a re-implementation; document the version used.
- **Cycle-phase bias.** Cycle 24 has weak polar fields; conclusions may
  not transfer to cycles with stronger polar Br.

### Figure / numerical targets

- TODO verify: (a) max latitudinal HCS difference in degrees; (b)
  percent change in integrated open flux; (c) reference figure / table.

### Claim boundary

**In scope.** PFSS vs HCCSSS-class on HMI synoptic `B_r`, Cycle 24,
paper's CR range, paper's parameter choices.

**Out of scope — do NOT generalize:**

- Do NOT extend to MHD / NLFFF comparisons.
- Do NOT declare a "winner" — the paper is positional, not evaluative
  against truth.
- Do NOT generalize across magnetograph sources (GONG vs HMI vs ADAPT)
  without re-running.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                          | Purpose                                  | Notes |
|-------------------------------------|------------------------------------------|-------|
| `magnetogram.fetch_synoptic_br()`   | HMI synoptic for CR range                | guaranteed via Fido-class fetcher |
| `pfss.solve()`                      | baseline PFSS solve                      | precondition |
| `csss.solve()`                      | HCCSSS-class solve                       | external solver, TODO verify availability |
| `field.extract_hcs()`               | HCS latitude vs longitude at upper bdry  | local |
| `field.integrate_open_flux()`       | open-flux scalar per run                 | local |
| `in_situ.fetch_sector()` (optional) | 1-au sector pattern from Wind / ACE      | for context |

### Procedure

1. **Fetch HMI synoptic `B_r`** for paper's CR range.
2. **Run PFSS** at standard `R_ss` (paper choice TODO verify) and
   `l_max`.
3. **Run HCCSSS-class model** with paper-specified parameters (`R_cs`,
   current-sheet thickness; TODO verify).
4. **Extract HCS** from each model at the matching upper boundary.
5. **Compute diagnostics:**
   - HCS shape: per-longitude latitude of `B_r = 0` at upper boundary.
   - Open flux: surface integral of `|B_r|`.
6. **Per-CR difference vectors** and aggregate statistics.
7. **(Optional)** Compare to in-situ sector pattern at 1 au.

### Validation target

- **Metric:** TODO verify (HCS max-latitude offset deg; open-flux %).
- **Tolerance:** TODO verify.
- **Reference figure:** TODO verify.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A Python adapter can bind `pfss.solve` to `sunkit-magex.pfss`; the
  CSSS-family binding may require a re-implementation of the paper's
  solver, since the inventory does not assert public code.
- HMI synoptic fetch is satisfied by `sunpy.net.Fido` against JSOC.

LingTai's `[[pfss-tracing]]` supplies one binding of `pfss.solve`; no
LingTai-specific binding for `csss.solve` is offered.

---

## Layer 4 — Research-generation affordances

- **Gap:** the paper compares only two models. Composing with
  `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]` and
  `[[paper-multi-constraint-pfss-extrapolation-model]]` extends the
  comparison to a four-model family along the "how to add physics to
  PFSS" axis — different surgical moves on the same boundary problem.
- **Tension:** if HCCSSS and NSPF both close fractions of the open-flux
  gap, are they additive or redundant? A controlled experiment
  comparing both against the same HMI synoptic set would expose whether
  current sheets and source-surface deformation are alternative
  *descriptions* of the same missing physics or independent ones.
- **New hypothesis:** the cycle-phase dependence of PFSS-vs-CSSS
  disagreement should track polar-field strength; a multi-cycle
  re-running would test this and connect to the eclipse-benchmark
  cycle-phase finding.
- **Experiment:** at each HCS-warp disagreement window, fetch matched
  1-au sector data and rank the two models by sector-prediction
  accuracy.

---

## Skill graph → depends_on

- `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]` — the
  PFSS solver under test must pass the verification suite.
- `[[paper-multi-constraint-pfss-extrapolation-model]]` — sibling
  approach inside the PFSS framework.
- `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]` —
  another framework attempting to close the open-flux gap.

## Links

- arXiv: https://arxiv.org/abs/1603.04385
- DOI: TODO verify
- ADS: TODO verify
- Code: TODO verify (HCCSSS solver availability)
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md` §2.4
