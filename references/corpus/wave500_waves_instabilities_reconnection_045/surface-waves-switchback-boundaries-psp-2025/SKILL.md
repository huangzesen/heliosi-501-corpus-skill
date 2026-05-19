# surface-waves-switchback-boundaries-psp-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2507.01252).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify surface-wave activity at switchback boundaries in PSP data.
- Distinguish surface-wave vs reconnection-vs-rotational-discontinuity at SB boundaries.

### When NOT to use it

- Boundary-reconnection-only diagnosis — see [[phan-2022-switchback-boundary-reconnection-psp]].

### Claim boundary

PSP event-level identification of surface-wave signatures at SB boundaries; comparison against alternative boundary-class hypotheses.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

PSP-observed SB boundaries host surface-wave activity with paper-quantified frequencies and amplitudes; some boundaries previously classified as exhausts are better explained as surface-wave-bearing.

### 2.2 Equations / method

- Surface-wave dispersion at MHD interface.
- Boundary classifier across (Walén, surface-wave, KH).

### 2.3 Data assumptions

- PSP MAG + plasma at SB boundary cadence.
- Boundary-classifier rubric.

### 2.4 Failure modes (skill memory)

- **Single-spacecraft ambiguity** across boundary classes.
- **Cadence vs surface-wave frequency**.

### 2.5 Figure / numerical targets

- Surface-wave occurrence fraction at SB boundaries (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-SB-BOUNDARY-DETECT**.
- **C-SURFACE-WAVE-DISPERSION**.
- **C-BOUNDARY-CLASSIFIER**.

### 3.2 Procedure

1. C-SB-BOUNDARY-DETECT.
2. C-SURFACE-WAVE-DISPERSION: predict dispersion.
3. C-BOUNDARY-CLASSIFIER: assign class.

### 3.3 Minimum reproduction artifacts

- Per-boundary class assignment table.

---

## 4. Adapter / runtime notes (optional examples)

- PSP catalog harness + analytic surface-wave routines.

---

## 5. Research-generation affordance

- **Composability with [[phan-2022-switchback-boundary-reconnection-psp]]**: complementary boundary class; joint classifier improves both.
- **Composability with [[shoda-2021-turbulence-switchback-generation-alfvenic]]**: surface-wave-bearing boundaries point to wave-mediated SB generation.
- **Open hypothesis**: Are surface-wave-bearing SB boundaries preferentially in high-amplitude SBs?

---

## Links

- arXiv: https://arxiv.org/abs/2507.01252
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2507.01252`

## Skill graph

- [[phan-2022-switchback-boundary-reconnection-psp]]
- [[shoda-2021-turbulence-switchback-generation-alfvenic]]
- [[agapitov-2020-localized-magnetic-structures-boundaries]]

