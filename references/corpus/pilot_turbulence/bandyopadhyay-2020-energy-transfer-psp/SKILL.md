---
name: bandyopadhyay-2020-energy-transfer-psp
description: Reproduce the near-Sun energy cascade-rate estimate for solar wind turbulence from PSP Encounter-1 data (Bandyopadhyay et al. 2020, ApJS 246, 48).
version: 0.1.0
tags: [psp, turbulence, cascade-rate, politano-pouquet, von-karman, fields, sweap]
quality_level: pilot
executable_status: scaffold
---

# Bandyopadhyay 2020 — Enhanced Energy Transfer Rate near the Sun (PSP)

## When to use this paper-skill

Load this skill when you need to:

- estimate the turbulent energy cascade rate ε of solar wind MHD turbulence using PSP FIELDS + SWEAP data near the first perihelion,
- compare cascade-rate estimates from the **Politano–Pouquet (PP) third-order law** against the **von Kármán decay law**,
- benchmark any new cascade-rate diagnostic on a published "anchor" intervals set (PSP Encounter 1, ~0.17 au).

Skip this skill if your question is about kinetic-range dissipation, switchback morphology, or PFSS source mapping (use the relevant skills).

## Paper identity and claim boundary

- **Citation**: Bandyopadhyay, R., Goldstein, M. L., Maruca, B. A., Matthaeus, W. H., Parashar, T. N., Ruffolo, D., Chhiber, R., Usmanov, A., Chasapis, A., Qudsi, R., et al. (2020). *Enhanced Energy Transfer Rate in Solar Wind Turbulence Observed near the Sun from Parker Solar Probe*. **ApJS 246, 48**.
- **DOI**: [10.3847/1538-4365/ab5dae](https://doi.org/10.3847/1538-4365/ab5dae)
- **arXiv**: [1912.02959](https://arxiv.org/abs/1912.02959)
- **ADS**: [2020ApJS..246...48B](https://ui.adsabs.harvard.edu/abs/2020ApJS..246...48B)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.1.

**Evidence boundary — what the abstract supports (verified 2026-05-19 via arXiv 1912.02959 abs):**

- The paper analyses PSP first-orbit data over heliocentric distances 54–36 R☉ (≈0.25–0.17 au) and provides "direct evidence of an inertial-range turbulent energy cascade".
- Two independent estimators are used: the Politano–Pouquet (PP) exact third-order MHD law and the von Kármán phenomenological decay law.
- The reported claim recoverable from abstract-level inspection is **a substantially enhanced cascade rate near the Sun compared with 1 au**.

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact numerical ratio ε(PSP) / ε(1 au) (paraphrased as "~100×" in the inventory) is **not** quoted in the arXiv-abstract surface accessible here; treat the "two orders of magnitude" framing as inventory-paraphrase, not verified from the paper.
- The exact von-Kármán constant *C* used and the per-interval sub-selection criteria are TODO_verify in full text.
- Whether the cascade-rate enhancement is uniform across the 36–54 R☉ window or concentrated in a sub-interval is TODO_verify.

> **Assumptions and failure modes** (load-bearing): the PP exact third-order law requires statistical homogeneity and stationarity; ε_vK depends sensitively on the correlation-length convention; both estimators are *incompressible*-MHD limits whose validity in streamer-belt intervals (δρ/ρ non-negligible) is itself part of the paper's scrutiny.

## Scientific claim to reproduce or operationalize

The turbulent cascade rate ε measured near the Sun (~0.17 au) is roughly **two orders of magnitude larger** than typical 1-au values, when estimated from two independent methods — the Politano–Pouquet exact third-order law for incompressible MHD turbulence, and the von Kármán phenomenological decay law — applied to PSP first-perihelion magnetic-field and plasma data.

This skill operationalizes that claim as a reproducible benchmark: given PSP E1 FIELDS + SWEAP data, the workflow should return ε estimates that agree (within scatter) with two independent methods and exceed the 1-au reference by ~10²×.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, |B| | L2, RTN, ~1 vec/s (or higher Burst-mode) | CDAWeb / PSP SOC (`psp_fld_l2_mag_rtn_*.cdf`) |
| PSP SWEAP/SPC | proton density n_p, bulk velocity V_RTN, temperature T_p | L3 | CDAWeb / PSP SOC (`psp_swp_spc_l3i_*.cdf`) |
| (optional) PSP SWEAP/SPAN-I | ion VDFs for cross-check | L3 | PSP SOC |

Time range: PSP Encounter 1, perihelion ~2018-11-06, ~0.17 au. Use FIELDS-cadence MAG limited to intervals where SPC has valid plasma moments.

1-au reference values for the comparison can be drawn from any standard inertial-range cascade-rate compilation (e.g., Helios / Wind / ACE literature); document the chosen reference in the run log.

## Algorithm/workflow steps

1. **Interval selection** — Identify quasi-stationary intervals in PSP E1 with continuous SPC + MAG coverage. Drop intervals containing identified shocks or pressure-balance structures.
2. **Resampling** — Resample B_RTN and V_RTN to a common cadence (e.g., 1 s) preserving the inertial-range bandwidth.
3. **Elsässer fields** — Compute z± = V ± B/√(μ₀ ρ) with proton mass density ρ = n_p m_p.
4. **Third-order structure functions** — Compute mixed third-order moments Y±(ℓ) = ⟨|δz∓|² δz±_∥⟩ along the radial separation ℓ.
5. **PP cascade rate** — From the Politano–Pouquet exact law, ε_PP = −(1/4) (Y⁺ + Y⁻)/ℓ in the inertial range; estimate ε in the scaling plateau.
6. **von Kármán decay** — Independently estimate ε_vK = C (δZ²)^(3/2) / L, with δZ² the total Elsässer energy and L the correlation length (from the autocorrelation of B or z±). Choose C consistent with prior solar-wind work (TODO verify constant used in original paper).
7. **Comparison to 1 au** — Quote ε at PSP E1 against a documented 1-au baseline.
8. **Acceptance** — ε_PSP / ε_1AU ~ 10² within order-of-magnitude scatter, and ε_PP and ε_vK agree to within their stated uncertainty.

## Minimal executable benchmark or validation target

**Primary target** (order-of-magnitude, verified at abstract level): on PSP E1 (heliocentric distance ~36–54 R☉ ≈ 0.17–0.25 au) the workflow returns ε(PSP) substantially enhanced relative to a documented 1-au baseline, by both the PP and von-Kármán estimators.

**Quantitative refinement** (full-text-pending, TODO verify): the inventory paraphrases the enhancement as `~100×` (factor 10² TODO_verify) and the inter-method agreement as a factor ~2 (TODO_verify); these tighter numerical statements must be confirmed against §3 / Table 1 of the full paper before being quoted as a reproduction tolerance.

Recommended check artifacts:

- `bandyopadhyay2020_e1_pp_vs_vk.csv` — one row per interval: (t_start, t_end, ε_PP, ε_vK, δZ², L, n_p).
- a log-log scatter of ε_PP vs ε_vK with a 1:1 reference line.
- a single-number summary: ratio ε_PSP / ε_1AU.

## Known pitfalls / failure modes

- **Stationarity**: the third-order law assumes statistical homogeneity; violating it (e.g., by including stream interfaces or shocks) inflates ε.
- **Density gaps**: SPC plasma density gaps are common in E1; ε estimates collapse without ρ — interpolation choices matter.
- **Correlation length L**: the choice of integration limit on the autocorrelation strongly drives ε_vK. Document the convention.
- **Compressibility**: PP in the strict incompressible form ignores δρ. If δρ/ρ is non-negligible (E1 streamer-belt intervals can be), the incompressible PP under-/over-estimates.
- **Cadence / aliasing**: too aggressive a resampling truncates the inertial range and can bias the plateau detection.

## Paper-as-Skill compilation

This paper is compiled into an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "ε near the Sun ~100× the 1-au value" becomes the validation target in the section above (ε_PSP / ε_1AU ~ 10²; PP and vK consistent).
- **Methods / equations → executable workflows**: the Politano–Pouquet third-order law and the von Kármán decay law are encoded as the workflow steps 4–6; each step is a callable unit operating on the data contract below.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2, PSP SWEAP/SPC L3 (and optionally SPAN-I) CDF time series in the RTN frame and to resample them onto a shared common cadence; the runtime supplies concrete adapters bound to those capabilities (see Layer 3 for example bindings).
- **Caveats / failure modes → skill memory**: the "Known pitfalls" section is persistent skill memory — stationarity, density-gap handling, integration-limit conventions, compressibility, and aliasing — and is the first thing the harness consults when a downstream skill reports an out-of-range ε.
- **Figures / results → benchmark artifacts**: the per-interval CSV (`bandyopadhyay2020_e1_pp_vs_vk.csv`), the ε_PP vs ε_vK scatter, and the single-number ratio ε_PSP / ε_1AU are the exported benchmark artifacts that the harness checks for reproducibility.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**, and this paper-skill is a single leaf within that graph.

## Layer 4 — Research-generation affordances

- **Gap:** the paper anchors ε(PSP) at one orbit (E1, ~0.17–0.25 au). Whether the enhancement scales smoothly as r^−α between E1 and 1 au or jumps at a particular sub-Alfvénic / streamer-belt threshold is *not* answered by E1 alone — compose with [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (multi-encounter radial bins) and [[telloni-2025-psp-solo-radial-alignment-2022-december]] (single-event Lagrangian) to test r-dependence vs sub-Alfvénic-state dependence.
- **Tension:** PP and von-Kármán agree only when the inertial range is well-resolved AND the correlation length L is unambiguous. In streamer-belt slow wind ([[chen-2021-near-sun-streamer-belt-turbulence]]) compressibility and ambiguous L can drive method disagreement larger than the "factor ~2" the inventory paraphrases — the disagreement itself is a *measurement* of compressibility's effect on the incompressible estimators.
- **Hypothesis:** stratifying intervals by Alfvénicity (σ_c) before applying PP / vK collapses the inter-method scatter — i.e. the residual factor between ε_PP and ε_vK is a function of σ_c rather than of heliocentric distance. Testable with [[damicis-2021-alfvenic-nonalfvenic-psp]] as the stratifier on the same E1 intervals.
- **Minimal_experiment:** re-run PP and vK on E1 using *both* the published radial-separation pipeline and a local-mean-field-corrected variant (per the [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] convention) and report the ratio (ε_radial / ε_LMF) per σ_c bin. A ratio that stays near unity validates ε(PSP) as a wind-type-independent anchor; a systematic σ_c-dependence shifts ε(PSP) from a scalar anchor into a stratified roll-up.
- **Composable experiment:** feed the per-interval ε(PSP) into [[bowen-2023-landau-damping-proton-electron-heating]] as the upstream cascade-flux constraint; this lets the Landau-damping partition be benchmarked against an *observed* (not modelled) cascade rate, which is the most natural composition the abstract enables.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: this paper-skill is a leaf inside the HelioSI `solar-wind-turbulence` sub-graph (parent: `.library/custom/heliophysics-skills/SKILL.md`, theme "turbulence").
- **Sibling paper-skills**: [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (companion radial-evolution + anisotropy), [[telloni-2021-psp-solo-radial-alignment-turbulence]] (cross-helicity / residual energy radial trend), [[chen-2021-near-sun-streamer-belt-turbulence]] (E4 inbound/outbound spectra).
- **MCPs used**:
  - `psp-data-mcp` (or equivalent CDAWeb client) — for L2/L3 retrieval.
  - `cdflib` / `pyspedas` — for CDF I/O.
  - `sw-scanner` (Sioulas) — only if interval pre-segmentation by Alfvénicity is desired.
- **Harness contract**: the validation target above is the leaf benchmark; HelioSI roll-up should treat ε_PSP / ε_1AU ≈ 10² as the single reproducible scalar exported by this skill.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.1.
- IOPscience: https://iopscience.iop.org/article/10.3847/1538-4365/ab5dae
- arXiv: https://arxiv.org/abs/1912.02959
- Politano & Pouquet (1998), Geophys. Res. Lett. 25, 273 — exact third-order law (foundational, not from inventory).
- von Kármán & Howarth (1938) — decay-law origin (foundational, not from inventory).
