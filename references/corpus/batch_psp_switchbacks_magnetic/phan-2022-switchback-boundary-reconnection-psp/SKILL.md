# phan-2022-switchback-boundary-reconnection-psp

A paper-skill compiled from Phan, Lavraud, Halekas, Zhang, Bale,
Kasper, et al. 2022 (ApJ; arXiv:2101.06279).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Decide whether a specific switchback boundary is an active magnetic-
  reconnection exhaust.
- Validate reconnection-exhaust detection against a documented PSP
  case study.

### When NOT to use it

- Switchback *topology* (closed vs. open kinks) — see
  [[phan-2023-switchback-boundaries-closed]].
- Switchback *generation*; this paper-skill is about boundary-local
  reconnection, not how switchbacks form.

### Claim boundary

Direct evidence for magnetic reconnection at the boundaries of selected
PSP switchback events via the Walén test. The claim is bounded to the
analysed events; the paper does not estimate a population fraction of
reconnecting boundaries.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

At a subset of PSP switchback boundaries, plasma + field jumps satisfy
the Walén relation `ΔV ≈ ±ΔV_A` with high correlation, consistent with
a localised reconnection exhaust crossed by the spacecraft.

### 2.2 Equations / method

- Upstream reference values of `V`, `B`, `ρ` taken just outside the
  boundary.
- `ΔV_A = ΔB / √(μ_0 ρ)` across the boundary.
- Walén linear regression: `ΔV` vs. `ΔV_A`, recording slope and
  Pearson correlation.
- Reconnection-exhaust verdict if `|slope| ≈ 1` with high correlation.

### 2.3 Data assumptions

- High-cadence vector `B` and bulk velocity sufficient to resolve the
  boundary jump.
- A switchback event catalog with boundary timestamps.
- A density estimate suitable for `V_A`.

### 2.4 Failure modes (skill memory)

- **Upstream-reference window length** controls Walén slope; sweep
  and report sensitivity.
- **Density-proxy choice** shifts `ΔV_A` and the slope.
- **Cadence vs. boundary thickness.** Under-sampled boundaries blur
  jumps.
- **Sign convention.** ±1 depends on which side is "upstream".
- **Single-spacecraft ambiguity.** A Walén-consistent jump may also
  be a passing wave train; supporting evidence (temperature jump,
  energetic-particle signature) tightens the verdict.

### 2.5 Figure / numerical targets

- Walén slope ≈ ±1 with high correlation on a paper-named event
  (TODO verify list).
- Sign of `ΔV` (Alfvénic outflow direction) matches paper.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG / C-FETCH-BULK / C-FETCH-NE**: vector `B`, bulk
  velocity, density at the boundary cadence.
- **C-CATALOG**: switchback event list with boundary timestamps.
- **C-WALEN**: Walén regression with explicit reference-interval
  selection.
- **C-EXHAUST**: verdict given slope, correlation, and a documented
  tolerance.

### 3.2 Procedure

1. C-CATALOG over the analysis window.
2. C-FETCH-MAG + C-FETCH-BULK + C-FETCH-NE for each event window.
3. Locate boundary crossings (entry + exit).
4. Choose an upstream reference interval just outside the boundary.
5. C-WALEN: compute slope + correlation.
6. C-EXHAUST: apply verdict rule with explicit tolerance.
7. Aggregate per-event verdicts; compare to paper events.

### 3.3 Minimum reproduction artifacts

- Per-event Walén-fit JSON.
- Regression PNG with explicit reference-window length.
- Verdict CSV with tolerance and sign convention recorded.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with CDF I/O + linear regression + a sign convention can
  satisfy the contracts.
- LingTai HelioSI may bind C-CATALOG to an internal switchback-finder
  skill; this is one binding among many.

---

## 5. Research-generation affordance

- **Composability with [[agapitov-2023-structure-origin-switchbacks-psp]]**:
  restrict C-EXHAUST evaluation to the RD-classified subset and
  estimate the *conditional* exhaust fraction within RDs — a tight
  statistic that the two papers don't compute jointly in the
  inventory.
- **Composability with [[phan-2023-switchback-boundaries-closed]]**:
  intersect exhaust events with the *closed*-topology subset; whether
  exhausts are over-represented inside closed kinks (or vice versa) is
  an open empirical question.
- **Open hypothesis**: dependence of exhaust fraction on heliocentric
  distance is sparsely characterised; a systematic encounter-scan
  using identical Walén-tolerance parameters is a natural follow-up.
- **Methodological experiment**: vary the upstream-window length and
  measure how exhaust counts change — the sensitivity is a quantifiable
  systematic the field has not reported.

---

## Links

- arXiv: https://arxiv.org/abs/2101.06279
- DOI: TODO verify with full text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §2.10;
  `extended_search.md` §3.1

## Skill graph

- [[agapitov-2023-structure-origin-switchbacks-psp]] — RD-subset
  conditioning.
- [[phan-2023-switchback-boundaries-closed]] — topology cross-test.
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — boundary-
  detection foundation.
