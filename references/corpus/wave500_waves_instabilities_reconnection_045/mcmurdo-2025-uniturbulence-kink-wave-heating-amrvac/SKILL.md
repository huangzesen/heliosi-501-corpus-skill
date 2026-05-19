# mcmurdo-2025-uniturbulence-kink-wave-heating-amrvac

A paper-skill compiled from M. McMurdo, T. Van Doorsselaere, N. Magyar et al. 2025 (TODO_verify_journal; arXiv:2510.27553).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Decide whether kink-wave driving alone (UAWSoM) can sustain a coronal atmosphere without ad-hoc background heating.
- Compare kink-wave-driven heating rate against pure Alfvén-wave models at matched energy injection.

### When NOT to use it

- In-situ ion-scale wave diagnostics — see kinetic-wave skills.
- Photospheric driver-generation mechanism.

### Claim boundary

MPI-AMRVAC extensions implementing additional kink-wave and Alfvén-wave energy contributions plus a radiative-cooling module. Comparison runs span Alfvén-only and kink-only forcings. Validation against Python-side simulations of the UAWSoM module is performed.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

UAWSoM kink-wave-driven heating sustains coronal-like temperature and density without artificial background-heating terms; pure Alfvén-only models require ad-hoc heating to match the same atmosphere.

### 2.2 Equations / method

- MHD with additional Alfvén-wave and kink-wave energy equations.
- Wave-action conservation with reflection coefficient set by V_A(r) gradients.
- Radiative cooling Λ(T) curve.

### 2.3 Data assumptions

- Spherically symmetric or 1D flux-tube domain.
- Photospheric wave energy injection prescription.
- Radiative-cooling curve and chromospheric heating cutoff.

### 2.4 Failure modes (skill memory)

- **Reflection-rate prescription** dominates the kink–Alfvén comparison; sweep.
- **Radiative-cooling treatment** differs between Python and AMRVAC modules — calibrate.
- **Energy-injection ratio** between kink and Alfvén drives entire comparison; report.
- **1D assumption** suppresses cross-field mixing of kink/Alfvén energies.

### 2.5 Figure / numerical targets

- Sustained T(r), n(r) without ad-hoc heating in UAWSoM (TODO verify exact T,n).
- Python-vs-AMRVAC agreement to stated tolerance.
- Increased kink-wave heating rate vs Alfvén at matched injection.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-MHD-WAVES**: MHD with multi-wave-energy budgets.
- **C-COOLING**: radiative cooling module.
- **C-PROFILE-COMPARE**: T(r), n(r) comparison harness.
- **C-AW-VS-KINK-INJECTION**: switchable injection ratio.

### 3.2 Procedure

1. Initialize 1D flux tube with chromospheric base.
2. C-MHD-WAVES + C-COOLING: evolve to quasi-steady atmosphere.
3. Run pure-Alfvén baseline and UAWSoM kink-driven case.
4. C-PROFILE-COMPARE: report T(r), n(r) match.
5. C-AW-VS-KINK-INJECTION: vary ratio and document.

### 3.3 Minimum reproduction artifacts

- Steady-state T(r), n(r) per run.
- Energy-budget breakdown vs r.
- Comparison plot Python-vs-AMRVAC.

---

## 4. Adapter / runtime notes (optional examples)

- Any compressible MHD code with multi-wave action equations satisfies the contracts.
- MPI-AMRVAC UAWSoM module is one Layer-3 binding.

---

## 5. Research-generation affordance

- **Composability with [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]**: extend UAWSoM into the heliosphere with PS background and test whether kink-driven heating still dominates outside 0.3 AU.
- **Tension with pure-Alfvén AWSoM literature**: most space-weather operational codes use AWSoM; if UAWSoM removes the need for ad-hoc heating, operational implications are substantial.
- **Open hypothesis**: Are observed transverse-MHD oscillations in coronal loops the kink modes carrying the heating in UAWSoM?

---

## Links

- arXiv: https://arxiv.org/abs/2510.27553
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2510.27553`

## Skill graph

- [[abbas-squire-2026-parker-spiral-reflection-driven-turbulence]]

