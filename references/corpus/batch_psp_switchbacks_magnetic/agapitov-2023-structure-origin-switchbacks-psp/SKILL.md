# agapitov-2023-structure-origin-switchbacks-psp

A paper-skill compiled from Agapitov, Mozer, Drake, Dudok de Wit, et al.
2023 (ApJ; doi:10.3847/1538-4357/acd17e).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent (human or AI) to do, in terms of abstract *capability
contracts*. Any runtime — Claude Code, LingTai, Codex, a researcher in
a notebook — may satisfy those contracts; nothing below mandates a
particular harness.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol against abstract capability contracts;
(4) optional adapter / runtime examples; plus (5) research-generation
affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- An agent must decide if a switchback boundary is an RD (rotational
  discontinuity) or a TD (tangential) — or a hybrid/ambiguous case.
- A statistical PSP baseline is needed for switchback boundary
  classification across multiple encounters.
- Composing population-level boundary statistics with event-level
  diagnostics (e.g. reconnection exhaust).

### When NOT to use it

- The *generation-mechanism* question (turbulence vs. interchange) —
  see [[shoda-2021-turbulence-switchback-generation-alfvenic]] and
  [[bale-2021-solar-source-switchbacks-magnetic-funnels]].
- Single-event topology questions where multi-instrument particle
  signatures matter — see
  [[phan-2023-switchback-boundaries-closed]].

### Claim boundary

A statistical PSP survey of switchback boundaries with geometric
classification (RD / TD / hybrid / ambiguous) using MVA + Walén
diagnostics. Origin claims are bounded to *what the boundary geometry
implies*, not to a specific solar-surface mechanism.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Across multiple PSP encounters, a measurable fraction of switchback
boundaries satisfy RD criteria (`B_n` above noise floor; Walén slope
close to ±1). The distribution of boundary types constrains the family
of viable origin scenarios.

### 2.2 Equations / method

- Switchback identification by deflection threshold on `B_R / |B|`.
- Boundary localisation at entry / exit edges.
- Minimum-variance analysis on `B` across each boundary → LMN frame,
  `B_n` estimate.
- Walén test: `ΔV` vs. `ΔV_A = ΔB / √(μ_0 ρ)` linear regression.
- Per-boundary classification:
  - **RD**: `|B_n| / |B|` above noise floor AND Walén slope ≈ ±1.
  - **TD**: `|B_n| / |B|` near zero AND Walén slope ≈ 0.
  - **Hybrid / ambiguous** otherwise.

### 2.3 Data assumptions

- High-cadence vector magnetic field across the boundary (sub-second to
  few-Hz windows).
- Co-temporal bulk-velocity and density estimates at matching cadence.
- A switchback event catalog with documented deflection threshold.

### 2.4 Failure modes (skill memory)

- **MVA noise floor.** Small `B_n` may be RD or noise; report the floor
  and run sensitivity.
- **Walén sign convention.** Different communities flip the sign;
  standardise inside the skill output.
- **Density-proxy choice.** Proton vs. electron density shifts `V_A`
  by a few percent.
- **Boundary thickness.** Finite-thickness boundaries blur MVA; sweep
  window length.
- **Encounter-coverage bias.** Comparison to the paper only holds if
  the encounter set matches.

### 2.5 Figure / numerical targets

- Non-zero fraction of RD-classified boundaries across the encounters.
- Walén-slope distribution peaked near ±1 for the RD subset.
- Exact reported fractions and encounter list — **TODO verify with
  full text**.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG**: retrieve a high-cadence vector magnetic field over
  a chosen PSP interval.
- **C-FETCH-BULK**: retrieve co-temporal bulk velocity + density.
- **C-CATALOG**: provide or generate a switchback event list with
  documented deflection threshold.
- **C-MVA**: compute MVA on a 3-vector time series and return the LMN
  basis and eigenvalues.
- **C-WALEN**: compute linear regression of `ΔV` on `ΔV_A` across a
  boundary window with explicit reference-interval selection.
- **C-AGGREGATE**: count per-class fractions over the event set.

### 3.2 Procedure

1. C-FETCH-MAG + C-FETCH-BULK over the analysis window.
2. C-CATALOG to identify switchback events.
3. For each event, locate entry/exit boundaries.
4. C-MVA on `B` across each boundary window of fixed length.
5. C-WALEN on the same boundary with documented upstream reference.
6. Apply the §2.2 classification rule.
7. C-AGGREGATE: per-class fractions over the encounter set.

### 3.3 Minimum reproduction artifacts

- `boundary_classification.csv` (per-event class + diagnostics).
- Walén-slope histogram for the RD subset.
- Fraction-vs-encounter JSON, with the encounter set and MVA-window
  length explicitly recorded.

---

## 4. Adapter / runtime notes (optional examples)

- **Claude Code / Codex:** C-FETCH-* via `WebFetch` + a CDF reader the
  agent invokes from `Bash`; C-MVA/C-WALEN via `numpy`/`scipy` in an
  edited Python file.
- **LingTai HelioSI instantiation:** the contracts may be wired to a
  `cdaweb` MCP adapter and to internal `mva` / `walen` skills; these
  bindings are LingTai-specific, **not** required by the science.
- **Researcher notebook:** the same contracts may be satisfied
  manually.

---

## 5. Research-generation affordance

- **Composability with [[phan-2022-switchback-boundary-reconnection-psp]]**:
  the RD subset is the natural superset of reconnection-exhaust
  candidates; the joint statistic *(RD-fraction, exhaust-fraction
  within RD subset)* is unreported in the inventory and is a natural
  follow-up.
- **Cross-test of [[shoda-2021-turbulence-switchback-generation-alfvenic]]**:
  generate switchbacks in a turbulence-origin simulation, apply this
  paper-skill's classifier, and compare the predicted RD fraction
  against the empirical fraction. A model that fails the RD-fraction
  test is falsified.
- **Open hypothesis**: does the RD-fraction depend monotonically on
  heliocentric distance? The paper's encounter-stratified statistic is
  partially reported (TODO verify) and a missing trend study is an
  obvious gap.
- **Open hypothesis**: do RD-classified switchbacks preferentially
  carry energetic-particle signatures consistent with reconnection?
  Composing with [[phan-2023-switchback-boundaries-closed]]'s particle
  diagnostic gives the experiment.

---

## Links

- DOI: https://doi.org/10.3847/1538-4357/acd17e
- arXiv: TODO verify with full text
- Code: TODO verify
- Data: PSP FIELDS + SWEAP public archives
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.5

## Skill graph

- [[phan-2022-switchback-boundary-reconnection-psp]] — event-level
  reconnection diagnostic on the RD subset.
- [[phan-2023-switchback-boundaries-closed]] — topology follow-up.
- [[shoda-2021-turbulence-switchback-generation-alfvenic]] — generation
  hypothesis tested by the RD-fraction.
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — boundary-
  detection foundation for the same time series.
