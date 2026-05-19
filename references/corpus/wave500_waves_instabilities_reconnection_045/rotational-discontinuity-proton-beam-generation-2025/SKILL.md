# rotational-discontinuity-proton-beam-generation-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2512.10406).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict generation of proton beams at switchback-boundary-like rotational discontinuities.
- Decide whether observed beams downstream of RDs match the predicted generation.

### When NOT to use it

- Reconnection at switchback boundaries — see [[phan-2022-switchback-boundary-reconnection-psp]].

### Claim boundary

Hybrid PIC simulations of RDs in solar-wind-like backgrounds; observed PSP RD events compared.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

RDs with switchback-boundary-like properties produce proton beams via wave-particle interaction; predicted beam drift matches observed downstream of PSP RDs.

### 2.2 Equations / method

- RD jump conditions vs reconnection-exhaust.
- Wave-particle resonance condition at RD.

### 2.3 Data assumptions

- Hybrid simulation of an RD.
- PSP RD-event candidates.

### 2.4 Failure modes (skill memory)

- **RD-vs-reconnection-exhaust ambiguity**.
- **Cadence vs RD thickness**.

### 2.5 Figure / numerical targets

- Predicted beam drift within in-situ range (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-RD-INIT**.
- **C-HYBRID-RD**.
- **C-RD-EVENT-MATCH**.

### 3.2 Procedure

1. C-RD-INIT.
2. C-HYBRID-RD: simulate.
3. C-RD-EVENT-MATCH: compare to PSP RDs.

### 3.3 Minimum reproduction artifacts

- Beam-drift predictions per RD event.

---

## 4. Adapter / runtime notes (optional examples)

- dHybridR, CAMELIA example Layer-3.

---

## 5. Research-generation affordance

- **Composability with [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]**: beams have two sources — AW-driven (interior) and RD-driven (boundaries) — joint catalog.
- **Tension with [[phan-2022-switchback-boundary-reconnection-psp]]**: RD-driven beams vs reconnection-exhaust beams — separability.
- **Open hypothesis**: Are PSP beam-event statistics dominated by RD or AW driving?

---

## Links

- arXiv: https://arxiv.org/abs/2512.10406
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.10406`

## Skill graph

- [[bianco-2025-alfven-wave-proton-beam-evolution-hebox]]
- [[phan-2022-switchback-boundary-reconnection-psp]]

