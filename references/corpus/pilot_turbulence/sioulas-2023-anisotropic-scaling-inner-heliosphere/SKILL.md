---
name: sioulas-2023-anisotropic-scaling-inner-heliosphere
description: Map the radial evolution of wavevector-anisotropic scaling and spectral index of MHD turbulence using a merged PSP + Solar Orbiter dataset (Sioulas et al. 2023, ApJ).
version: 0.1.0
tags: [psp, solar-orbiter, turbulence, anisotropy, structure-functions, local-mean-field]
quality_level: pilot
executable_status: scaffold
---

# Sioulas 2023 — Anisotropic Scaling of MHD Turbulence in the Inner Heliosphere

> **⚠ Identifier attribution unresolved (verified 2026-05-19).** Independent resolution shows that the DOI `10.3847/1538-4357/acd053` listed below actually points to **Yoshida, Shimizu & Toriumi 2023** (a different ApJ paper on solar magnetic-field component vs interplanetary-field evolution), and arXiv `2303.10810` points to **Wu, He, Huang, Yang, Wang & Yuan** ("Scaling anisotropy with stationary background field in the near-Sun solar wind turbulence", ApJ). The Sioulas+ 2023 paper this skill *intends* to compile has a different (still-unresolved) DOI/arXiv pair. Treat both identifiers as PENDING corrections — do not cite this entry's DOI / arXiv in a manuscript until a curator locates the canonical identifiers (e.g. via ADS author-affiliation search). The Layer-1 claim boundary about parallel/perpendicular anisotropy and its radial evolution remains *paraphrase-only* until the canonical paper is located.

## When to use this paper-skill

Load this skill when you need to:

- measure the **wavevector anisotropy of power** in solar wind MHD turbulence parallel vs perpendicular to the local mean field,
- track its **radial evolution** between ~0.1 au and 1 au using a single homogeneous methodology applied across PSP and Solar Orbiter,
- extract multi-order structure-function scaling exponents binned by heliocentric distance.

Use [[sioulas-2024-higher-order-3d-anisotropy]] for the follow-up that resolves the *3D* anisotropy (with the fluctuation-direction axis), and [[chen-2021-near-sun-streamer-belt-turbulence]] for streamer-belt-specific inbound/outbound spectra.

## Paper identity and claim boundary

- **Citation**: Sioulas, N., Velli, M., Chhiber, R., Vlahos, L., Matthaeus, W. H., Bandyopadhyay, R., Stevens, M. L., Bale, R., et al. (2023). *On the Evolution of the Anisotropic Scaling of Magnetohydrodynamic Turbulence in the Inner Heliosphere*. **ApJ**.
- **DOI**: 10.3847/1538-4357/acd053
- **arXiv**: [2303.10810](https://arxiv.org/abs/2303.10810)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.2.

**Claim boundary** — the inventory supports the following:

> A merged PSP + Solar Orbiter dataset is used to compute multi-order structure functions parallel and perpendicular to the local mean field, producing a radial map of the wavevector anisotropy of power and the spectral index in MHD turbulence.

Numerical anisotropy ratios, exact spectral-index values, and per-bin counts are **TODO verify in full paper**. The apj_aa inventory cross-references "companion 2404.04055" for 3D anisotropy — note that arXiv 2303.10810 is also listed as "Scaling Anisotropy with Stationary Background Field (Cuesta+ 2023)" elsewhere in the same inventory; this skill follows the apj_aa attribution and **flags it as a cross-check to verify**.

## Scientific claim to reproduce or operationalize

Solar wind MHD turbulence shows a wavevector-anisotropic power distribution between fluctuations whose wavevectors are parallel vs perpendicular to the local mean magnetic field, and this anisotropy together with the inertial-range spectral index **evolves systematically with heliocentric distance** between PSP perihelia (~0.1 au) and Solar Orbiter aphelion (~1 au). The radial evolution is consistent within a single uniform local-mean-field structure-function pipeline applied across both spacecraft.

## Required data/instruments and likely files/archives

| Mission/Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2, RTN | CDAWeb / PSP SOC (`psp_fld_l2_mag_rtn_*.cdf`) |
| PSP SWEAP/SPC or SPAN-I | V_RTN, n_p, T_p | L3 | PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | Solar Orbiter Archive (SOAR) |
| Solar Orbiter SWA/PAS | V_RTN, n_p | L2/L3 | SOAR |

Time range: a heliocentric-distance ladder using PSP encounters spanning multiple perihelia and SO operational years to cover ~0.1–1 au.

## Algorithm/workflow steps

1. **Interval cataloging** — Build a heliocentric-distance-binned catalog of quasi-stationary intervals from PSP and SO. Bin in r/R_sun or r/au.
2. **Local mean field** — For each lag ℓ, define a local mean field B₀(t, ℓ) using a scale-dependent moving average (typical convention: window ~ a few ℓ).
3. **Angle decomposition** — For each pair separated by ℓ, compute the angle θ between ℓ (or sampling direction) and B₀(t, ℓ); bin into "parallel" (small θ) and "perpendicular" (~90°) classes.
4. **Multi-order structure functions** — Compute S_n^∥(ℓ) and S_n^⊥(ℓ) of magnetic-field increments for n = 1, 2, 3, ... .
5. **Power anisotropy** — Extract the ratio S_2^∥/S_2^⊥ (proxy for wavevector anisotropy of power) per radial bin.
6. **Spectral indices** — Fit local slopes of S_2^∥, S_2^⊥ in the inertial range; report per radial bin.
7. **Radial mapping** — Plot anisotropy ratio and spectral indices vs heliocentric distance; verify monotonic / non-monotonic trends.

## Minimal executable benchmark or validation target

**Target**: per radial bin, an anisotropy ratio S_2^∥/S_2^⊥(ℓ_ref) and an inertial-range slope, both reproduced from PSP+SO with a single uniform pipeline. The radial trend (qualitative direction of evolution from 0.1 au to 1 au) should match the published figure (TODO verify direction and slope numbers in full paper).

Suggested artifacts:

- `sioulas2023_radial_anisotropy.csv` — columns: r_bin_au, n_intervals, S2_par_at_lref, S2_perp_at_lref, slope_par, slope_perp.
- a single overview plot: anisotropy ratio and slope vs r.

## Known pitfalls / failure modes

- **Local-mean-field convention**: the choice of moving-window width relative to ℓ changes the angle θ statistics and therefore the apparent anisotropy.
- **Sampling-direction bias**: spacecraft sample one direction in space; θ statistics reflect the angle between the sampling direction and B₀, not a true 3D wavevector decomposition. The follow-up [[sioulas-2024-higher-order-3d-anisotropy]] is the *fix* for this restriction.
- **Cross-spacecraft systematics**: PSP FIELDS and SO MAG differ in noise floors, calibration, and burst-mode coverage. Use compatible cadences and harmonize gap-handling.
- **Radial sparsity**: most PSP coverage is near perihelion; many radial bins are dominated by a small set of streams.
- **Mixed wind types**: fast/slow/Alfvénic/non-Alfvénic mixtures within a bin can mask the underlying trend; stratify by σ_c.

## Paper-as-Skill compilation

Compiled as an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "anisotropy ratio and spectral index evolve with heliocentric distance" becomes the validation target — per-bin S_2^∥/S_2^⊥(ℓ_ref) and slopes with a reproduced radial trend.
- **Methods / equations → executable workflows**: local-mean-field decomposition, angle binning, and multi-order structure-function evaluation are the workflow steps 2–6, each callable on the data contract below.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG, PSP SWEAP, Solar Orbiter MAG, and Solar Orbiter SWA/PAS time series exposed in a uniform RTN frame on a shared common cadence; the runtime supplies concrete adapters bound to those capabilities (see Layer 3 for example bindings).
- **Caveats / failure modes → skill memory**: local-mean-field window convention, sampling-direction bias, cross-spacecraft systematics, radial sparsity, and wind-type mixing form the persistent memory the harness consults before trusting a radial trend.
- **Figures / results → benchmark artifacts**: the radial-bin CSV (`sioulas2023_radial_anisotropy.csv`) and the overview figure (anisotropy ratio + slope vs r) are the exported benchmark artifacts.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph.
- **Sibling paper-skills**: [[bandyopadhyay-2020-energy-transfer-psp]] (cascade rate at one perihelion), [[sioulas-2024-higher-order-3d-anisotropy]] (3D follow-up), [[telloni-2021-psp-solo-radial-alignment-turbulence]] (cross-helicity radial evolution), [[damicis-2021-alfvenic-nonalfvenic-psp]] (stratification by Alfvénicity).
- **MCPs used**:
  - `psp-data-mcp` and `solar-orbiter-data-mcp` (or pyspedas + SOAR client).
  - `sw-scanner` for Alfvénicity-based interval segmentation.
  - `numpy`/`scipy` for structure-function pipelines.
- **Harness contract**: this skill exports a "radial anisotropy table" (CSV) and a single overview figure; downstream skills can consume the table directly.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.2.
- DOI: 10.3847/1538-4357/acd053 — **disputed**: external resolution on 2026-05-19 shows this DOI resolves to Yoshida et al. 2023 (ApJ), not a Sioulas+ paper.
- arXiv: https://arxiv.org/abs/2303.10810 — **disputed**: external resolution on 2026-05-19 shows this arXiv ID resolves to Wu, He, Huang, Yang, Wang & Yuan, "Scaling anisotropy with stationary background field in the near-Sun solar wind turbulence" (ApJ).
- Cross-attribution: the apj_aa inventory §3.5 separately lists arXiv 2303.10810 under Cuesta+ 2023 ("Scaling Anisotropy with Stationary Background Field"). The independent external lookup (Wu et al.) is closer to that §3.5 title than to the Sioulas §1.2 attribution — but neither matches verbatim, so the canonical identifier set for *both* attributions in the inventory remains TODO_verify.
- Action item: locate the canonical DOI/arXiv pair for the Sioulas+ 2023 "Evolution of the Anisotropic Scaling of MHD Turbulence in the Inner Heliosphere" paper via ADS author-affiliation search before promoting this entry past T3.
