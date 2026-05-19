# poynting-flux-alfven-polar-coronal-holes-cycle24-2025

A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2501.13673).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Quantify the Poynting flux of low-frequency Alfvénic waves in polar coronal holes over solar cycle 24.
- Decide whether the inferred wave-energy flux is sufficient to drive the fast solar wind.

### When NOT to use it

- Wave generation mechanism at the photospheric base.
- In-situ ion-scale-wave heating downstream.

### Claim boundary

Long-baseline remote-sensing (likely EUV / Hinode-EIS or analogous) measurements of nonthermal line-width broadening converted into δv_⊥, combined with magnetic-field estimates to compute Poynting flux F = ρ δv_⊥² V_A. Coverage limited to polar coronal-hole pixels per cycle.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Polar-coronal-hole Poynting flux varies systematically across cycle 24; the inferred F sits in the right order of magnitude to power fast-wind acceleration.

### 2.2 Equations / method

- Nonthermal width → δv_⊥: σ_nt² = σ_obs² − σ_thermal² − σ_inst².
- F = ρ ⟨δv_⊥²⟩ V_A.
- Cycle-binned aggregates over polar CH masks.

### 2.3 Data assumptions

- EUV spectroscopy with adequate cadence to bin cycle phases.
- Density estimate (line-ratio) and magnetic-field proxy.
- Polar-coronal-hole pixel mask per epoch.

### 2.4 Failure modes (skill memory)

- **Instrumental σ_inst** drift over years biases δv_⊥.
- **Density estimate** depends on assumed line-ratio diagnostic.
- **Polar projection** through inclined lines of sight underestimates δv_⊥.
- **Cycle-phase coverage** unevenness biases trend.

### 2.5 Figure / numerical targets

- F in 10^5 erg cm^-2 s^-1 range (TODO verify exact).
- Cycle-binned trend reproduced.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-EUV-LINE-WIDTH**: nonthermal-width extraction from EUV spectra.
- **C-CH-MASK**: polar coronal-hole pixel masking.
- **C-POYNTING**: F = ρ δv_⊥² V_A integrator.

### 3.2 Procedure

1. C-EUV-LINE-WIDTH for chosen line.
2. Subtract thermal and instrumental contributions.
3. C-CH-MASK per epoch.
4. C-POYNTING: aggregate F over mask.
5. Bin by cycle phase.

### 3.3 Minimum reproduction artifacts

- F(epoch) curve.
- Cycle-phase aggregate JSON.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with EUV-spectroscopy access satisfies the contracts.
- Hinode-EIS / IRIS pipelines are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[mcmurdo-2025-uniturbulence-kink-wave-heating-amrvac]]**: feed the observed F as the AW-injection boundary condition.
- **Composability with [[alfven-surface-wind-braking-torque-psp-2025]]**: F at polar CH constrains the AW driver at the Alfvén-surface base.
- **Open hypothesis**: Does Poynting-flux variation track in-situ fast-wind speed at 1 AU per cycle?

---

## Links

- arXiv: https://arxiv.org/abs/2501.13673
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2501.13673`

## Skill graph

- [[mcmurdo-2025-uniturbulence-kink-wave-heating-amrvac]]
- [[alfven-surface-wind-braking-torque-psp-2025]]

