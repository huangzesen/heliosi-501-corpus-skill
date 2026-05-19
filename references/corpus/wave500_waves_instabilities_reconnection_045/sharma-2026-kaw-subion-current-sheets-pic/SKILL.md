# sharma-2026-kaw-subion-current-sheets-pic

A paper-skill compiled from J. Sharma, C. Akshath Kumar, K. D. Makwana et al. 2026 (TODO_verify_journal; arXiv:2601.18131).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Predict the thickness/length/width statistics of current sheets formed in KAW turbulence at sub-ion / electron scales.
- Decide whether observed sub-ion-scale current-sheet thickness in solar-wind/magnetosheath data is consistent with electron-skin-depth scaling.

### When NOT to use it

- Macroscopic reconnection events — this is the *dissipation-structure* layer, not the global reconnection topology.
- Inertial-range turbulence statistics (use turbulence-spectrum skills).

### Claim boundary

Driven 3D PIC simulations initialized with KAW eigenvector relations from a two-fluid model. Statistics computed via BFS and DBSCAN clustering. Scaling claims are over the ion-to-electron mass ratio scan performed.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Average sub-ion-scale current-sheet thickness scales as ~ (m_i/m_e)^(-1/2), i.e. close to the electron skin depth d_e. Widths and lengths show weaker scaling. Scale-dependent kurtosis confirms enhanced intermittency at electron scales.

### 2.2 Equations / method

- Two-fluid KAW eigenvector relations for initialization.
- Electron skin depth d_e = c/ω_pe.
- Scale-dependent kurtosis κ(ℓ) of B-field increments.
- BFS / DBSCAN clustering on |J|-threshold mask.

### 2.3 Data assumptions

- 3D PIC simulation domain large enough to capture sub-ion and electron scales.
- Initial KAW spectrum prescribed; reduced m_i/m_e values used.
- Current-density mask threshold and clustering algorithm specified.

### 2.4 Failure modes (skill memory)

- **Mass-ratio extrapolation** to physical m_i/m_e = 1836 is uncalibrated.
- **Threshold choice** for |J|-mask alters thickness distribution.
- **Clustering algorithm** (BFS vs DBSCAN) yields slightly different tails — report both.
- **Initial-spectrum choice** sets a transient artifact regime that should be excluded.
- **Numerical resistivity** may set thickness instead of d_e at insufficient resolution.

### 2.5 Figure / numerical targets

- Thickness ∝ (m_i/m_e)^(-1/2) within stated tolerance (TODO verify).
- Width/length scaling exponents weaker than thickness (TODO verify exponents).
- Scale-dependent kurtosis enhancement at electron scales reproduced.

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-PIC-3D**: 3D PIC integrator with prescribable mass ratio.
- **C-KAW-INIT**: initialize fields from two-fluid KAW eigenvectors.
- **C-SHEET-MASK**: |J| threshold mask + BFS or DBSCAN clustering.
- **C-INTERMITTENCY**: scale-dependent kurtosis of B-increments.

### 3.2 Procedure

1. C-KAW-INIT with prescribed spectrum.
2. C-PIC-3D: evolve to a saturated turbulent state.
3. C-SHEET-MASK: extract current-sheet objects (BFS and DBSCAN).
4. Measure thickness/length/width distributions; fit mass-ratio scaling.
5. C-INTERMITTENCY: compute κ(ℓ) and compare against magnetosheath references.

### 3.3 Minimum reproduction artifacts

- Current-sheet object catalog (per simulation, per algorithm).
- Mass-ratio scaling fits.
- κ(ℓ) curves across scales.

---

## 4. Adapter / runtime notes (optional examples)

- Any 3D PIC code with field-eigenvector initialization satisfies the contracts.
- VPIC, Pencil-PIC, EPOCH are example Layer-3 bindings.

---

## 5. Research-generation affordance

- **Composability with [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]**: compare scale-dependent kurtosis exponents from PIC to PSP measurements vs r.
- **Composability with [[bowen-2023-landau-damping-proton-electron-heating]]**: locate Landau-damping sites at the sub-ion-current-sheet boundaries to test whether dissipation lives on sheets vs in waves.
- **Open hypothesis**: Does observed inertial-electron-scale break in PSP magnetic-spectra coincide with d_e of the local thermal plasma?
- **Methodological experiment**: vary the |J|-mask threshold and quantify how thickness scaling exponents shift — a publishable systematic uncertainty.

---

## Links

- arXiv: https://arxiv.org/abs/2601.18131
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2601.18131`

## Skill graph

- [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]]
- [[bowen-2023-landau-damping-proton-electron-heating]]
- [[zhao-2022-3d-anisotropy-kinetic-scales-psp]]

