---
name: kelvin-helmholtz-cme-large-scale-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# kelvin-helmholtz-cme-large-scale-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from + co-authors (TODO verify full list) et al. 2025 (TODO_verify_journal; arXiv:2512.19942).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify Kelvin–Helmholtz (KH) instability features along CME-sheath boundaries.
- Quantify KH-wave amplitudes and wavelengths from imagery and in-situ shear measurements.

### When NOT to use it

- KH at switchback boundaries — separate.

### Claim boundary

Event-level analysis combining imaging + in-situ data on a CME-driven KH event. Linear KH-threshold check.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Specific CME event drives large-scale KH instability with paper-reported wavelengths and amplitudes consistent with linear KH threshold.

### 2.2 Equations / method

- KH linear stability threshold for shear flows with magnetic field.
- Wavelength scaling with shear width.

### 2.3 Data assumptions

- Coronagraph or in-situ shear-boundary measurements.

### 2.4 Failure modes (skill memory)

- **Projection ambiguity** in 2D imagery.
- **Shear width** estimation noise.

### 2.5 Figure / numerical targets

- KH wavelength matches linear-theory expectation (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-IMAGE-LOAD-CME**.
- **C-IN-SITU-SHEAR**.
- **C-KH-LINEAR**.

### 3.2 Procedure

1. C-IMAGE-LOAD-CME.
2. C-IN-SITU-SHEAR.
3. C-KH-LINEAR: compare predicted vs observed wavelength.

### 3.3 Minimum reproduction artifacts

- KH event report.

---

## 4. Adapter / runtime notes (optional examples)

- LASCO/COR pipelines example.

---

## 5. Research-generation affordance

- **Composability with reconnection-event skills**: KH at boundaries may seed reconnection — joint event analysis.
- **Open hypothesis**: Is KH activity statistically associated with enhanced suprathermal-particle generation downstream?

---

## Links

- arXiv: https://arxiv.org/abs/2512.19942
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2512.19942`

## Skill graph

- [[hcs-reconnection-statistics-psp-encounter-2025]]

