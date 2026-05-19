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
- **DOI**: 10.3847/1538-4365/ab5dae
- **arXiv**: [1912.02959](https://arxiv.org/abs/1912.02959)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.1.

**Claim boundary** — only the following claim from the inventory is treated as supported here:

> Cascade rate near the Sun is ~100× the 1-au value, estimated from the Politano–Pouquet third-order incompressible-MHD law and the von Kármán decay law applied to PSP FIELDS + SWEAP data near first perihelion.

Any tighter numerical statement (e.g. exact ε in J kg⁻¹ s⁻¹, exact heliocentric distance binning, sub-interval count) is **TODO verify in full paper**.

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

**Target**: on PSP E1 with the workflow above, the estimated cascade rate at ~0.17 au is ~10² × the chosen 1-au reference, with PP and vK estimates consistent to within a factor of ~2 (TODO verify exact factor against full paper).

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
