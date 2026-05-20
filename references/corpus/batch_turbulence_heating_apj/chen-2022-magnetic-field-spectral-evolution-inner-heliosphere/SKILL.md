---
name: chen-2022-magnetic-field-spectral-evolution-inner-heliosphere
description: Use when characterising the radial evolution of the magnetic-field inertial-range spectral slope across PSP, Helios, and Wind — central paper claim is that the inertial range is narrow with α_B ≈ -3/2 near the Sun and broadens / steepens toward α_B ≈ -5/3 with heliocentric distance, with slower / less Alfvénic streams showing steeper spectra than Alfvénic intervals (Sioulas et al. 2023, ApJL 943; DOI 10.3847/2041-8213/acaeff; arXiv:2209.02451). Slug retained for backwards compatibility — the published lead author is Sioulas, not Chen (verified 2026-05-19).
version: 0.1.0
tags: [psp, helios, wind, solar-orbiter, magnetic-field, spectral-slope, radial-evolution, turbulence]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "N. Sioulas"
  authors:
    - "N. Sioulas"
    - "Z. Huang"
    - "C. Shi"
    - "M. Velli"
    - "A. Tenerani"
    - "T. A. Bowen"
    - "S. D. Bale"
    - "J. Huang"
    - "L. Vlahos"
    - "L. D. Woodham"
    - "T. S. Horbury"
    - "T. Dudok de Wit"
    - "D. Larson"
    - "J. Kasper"
    - "C. J. Owen"
    - "M. L. Stevens"
    - "A. Case"
    - "M. Pulupa"
    - "D. M. Malaspina"
    - "J. W. Bonnell"
    - "R. Livi"
    - "K. Goetz"
    - "P. R. Harvey"
    - "R. J. MacDowall"
    - "M. Maksimović"
    - "P. Louarn"
    - "A. Fedorov"
  authors_verified: true
  doi: "10.3847/2041-8213/acaeff"
  arxiv_id: "2209.02451"
  year: 2023
  venue: "The Astrophysical Journal Letters 943 (2023)"
---

# Sioulas 2023 — Magnetic Field Spectral Evolution (PSP/SolO) (slug: chen-2022-…)

> **Attribution note (verified 2026-05-19).** The arXiv landing page for 2209.02451 and the IOPscience page for DOI 10.3847/2041-8213/acaeff both list **N. Sioulas** as first author. The corresponding published paper is ApJL **943** (2023), *not* a 2022 Chen et al. paper. The inventory `apj_aa_heliophysics_papers.md §1.15` ("Chen et al., 2022, arXiv:2209.02451") is an attribution and year error. The corpus slug `chen-2022-…` is retained for backwards compatibility but the cited lead author is now **N. Sioulas**, and the publication year is **2023**, not 2022; use Sioulas et al. 2023, ApJL 943 when citing this entry in a manuscript. (Mirrors the slug-retention pattern previously applied to other batch entries.)

## When to use this paper-skill

Load this skill when you need to:

- combine **PSP + Solar Orbiter** (and 1-au reference) magnetic-field PSDs into a radial-evolution dataset spanning ~0.1 au to ~1 au,
- characterise the **inertial-range slope** that is narrow and near α_B ≈ -3/2 close to the Sun and broadens / steepens toward α_B ≈ -5/3 with heliocentric distance,
- benchmark how the slope evolution differs by **magnetic energy level and Alfvénicity** — slower / less Alfvénic streams show steeper spectra than Alfvénic intervals.

Skip this skill if your interest is the 1/f outer range ([[huang-2023-psp-one-over-f-spectrum]]), compressible / density-channel turbulence ([[cuesta-2022-compressible-turbulence-psp-themis-maven]], [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]]), or kinetic-scale anisotropy ([[zhao-2022-3d-anisotropy-kinetic-scales-psp]]).

## Paper identity and claim boundary

- **Citation**: Sioulas, N., Huang, Z., Shi, C., Velli, M., Tenerani, A., Bowen, T. A., Bale, S. D., Huang, J., Vlahos, L., Woodham, L. D., Horbury, T. S., Dudok de Wit, T., Larson, D., Kasper, J., Owen, C. J., Stevens, M. L., Case, A., Pulupa, M., Malaspina, D. M., Bonnell, J. W., Livi, R., Goetz, K., Harvey, P. R., MacDowall, R. J., Maksimović, M., Louarn, P., & Fedorov, A. (2023). *Magnetic Field Spectral Evolution in the Inner Heliosphere.* **ApJL 943** (2023).
- **DOI**: [10.3847/2041-8213/acaeff](https://doi.org/10.3847/2041-8213/acaeff)
- **arXiv**: [2209.02451](https://arxiv.org/abs/2209.02451)
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.15 (lists this DOI / arXiv ID under "Chen et al., 2022" — see attribution note above).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via arXiv.org for 2209.02451 and IOPscience for DOI 10.3847/2041-8213/acaeff):**

- Near the Sun, the inertial range is reported as "limited to a narrow range of scales" with α_B ≈ **-3/2** (abstract-verified).
- The inertial range "expands outward while gradually transitioning to α_B = -5/3 scaling" (abstract-verified — the transition is described as *gradual* across the inner heliosphere, not as a sharp transition at a specific heliocentric distance).
- The spectra "steepen differently depending on magnetic energy levels and Alfvénic properties," with slower solar-wind streams showing **steeper** spectra than highly Alfvénic intervals (abstract-verified).
- The data are explicitly PSP + Solar Orbiter (abstract-verified); Helios / Wind are not in the abstract.
- Authors (27 in total) and ApJL 943 (2023) venue are verified.

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact transition heliocentric distance at which α_B = -5/3 is recovered (the abstract says "gradual transition," not a specific r_au) is **TODO_verify** against the paper's figures.
- The per-stream-class quantitative α_B values (and the stratification rule used for "highly Alfvénic" vs "slower" streams) are TODO_verify.
- The exact intervals from PSP / Solar Orbiter and the inertial-range bounds per interval are TODO_verify.

Out-of-scope (the entry deliberately refuses these): extending the steepening claim beyond ~1 au into the outer heliosphere; collapsing the result onto a single encounter; treating "α_B(0.6 au) ≈ -5/3" as a verified anchor (the abstract says the transition is gradual, not that it completes at a specific distance); folding in Helios / Wind PSDs as if the paper directly used them (it does not, per abstract).

> **Assumptions and failure modes** (load-bearing): the slope α_B is sensitive to the inertial-range bounds (f_low, f_high) — outer-scale or kinetic-break contamination biases the fit; PSP and SO sample at different cadences and must be bandwidth-matched before pooling; stream-class conditioning is not optional — the abstract reports that slow vs Alfvénic streams have **different** α_B, so an unstratified mean blurs the signal.

## Scientific claim to reproduce or operationalize

The inertial-range slope α_B of the magnetic-field trace PSD is not radially constant in the inner heliosphere: near the Sun (~0.1 au, PSP) it is narrow in extent and close to -3/2; with increasing heliocentric distance the inertial range broadens and α_B gradually transitions toward -5/3. The slope-evolution rate depends on the stream class — slower / less Alfvénic streams steepen faster than highly Alfvénic intervals.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN | L2 | CDAWeb / PSP SOC |
| Solar Orbiter MAG | B_RTN | L2 | SOAR / CDAWeb |
| (optional 1-au reference) Wind MFI | B (GSE) | L2 | CDAWeb |
| (optional) PSP SWEAP, SO SWA/PAS | n_p, V_sw, Alfvénicity diagnostics | L3 / L2 | CDAWeb / SOAR |

Time range: pooled multi-mission samples covering 0.1 to ~1 au — exact interval selection **TODO_verify** against §2 of ApJL 943.

## Algorithm/workflow steps

1. **Per-mission interval catalog** — Build clean solar-wind intervals per mission (PSP, Solar Orbiter), excluding shocks / CMEs / HCS crossings.
2. **Alfvénicity / stream-class tag** — Compute σ_c (and / or |σ_c|) per interval; tag as "highly Alfvénic" or "slow / less Alfvénic" using the paper's threshold (TODO_verify exact threshold).
3. **Trace PSD** — Compute trace magnetic PSD per interval via Welch / multitaper with explicit window length and overlap; report bandwidth.
4. **Inertial-range bounds** — Determine f_low (above the 1/f / outer-scale break — cf. [[huang-2023-psp-one-over-f-spectrum]]) and f_high (below the ion break — cf. [[bowen-2024-extended-cyclotron-resonant-heating]]) per interval, including the "narrow at PSP" structural caveat.
5. **Slope fit** — Fit α_B in the inertial range; report uncertainty.
6. **Radial + stream-class binning** — Bin α_B vs (heliocentric distance, stream class) over [0.1, ~1] au.
7. **Trend** — Show α_B(r) transitioning gradually from ~-3/2 near the Sun toward ~-5/3 with distance, and α_B(slow) < α_B(Alfvénic) at fixed r (i.e. slow streams have steeper / more negative slopes).
8. **Acceptance** — Recover the qualitative radial+stream-class trend reported in the paper; exact transition r and per-bin α_B values are TODO_verify.

## Minimal executable benchmark or validation target

**Target**: pooled PSP/SO α_B vs (r, stream-class) curve shows α_B(r=0.1 au) ≈ -3/2 narrow inertial range, gradual transition toward α_B ≈ -5/3 with increasing r, and slower / less Alfvénic streams steeper than highly Alfvénic intervals at fixed r (abstract-verified qualitative; exact transition distance and per-bin α_B values TODO_verify against ApJL 943 figures).

Recommended check artifacts:

- `sioulas2023_alpha_b_vs_r.csv` — one row per (mission, interval): (mission, t_start, t_end, r_au, stream_class, alpha_B, alpha_B_err, f_low, f_high, sigma_c).
- Per-stream-class α_B(r) overlay plot (two curves: Alfvénic vs slow).
- Single scalar QC: signed difference Δα_B = α_B(slow) − α_B(Alfvénic) at a reference r bin (target: Δα_B < 0, i.e. slow steeper).

## Known pitfalls / failure modes

- **f_low / f_high definition**: the slope is sensitive to the inertial-range bounds; near the Sun the inertial range is narrow (abstract-verified), so the bounds are particularly fragile.
- **Outer-scale contamination**: if f_low encroaches into the 1/f range, α_B flattens artificially.
- **Ion-break contamination**: if f_high enters the kinetic range, α_B steepens artificially.
- **Cadence / Nyquist mismatch**: PSP and SO sample at different cadences — match bandwidth before pooling.
- **Stream-class conditioning**: aggregating fast and slow streams *will* blur the trend — the abstract reports a stream-class dependence, so unstratified pooling is wrong.
- **"Gradual" vs "transition at r*"**: do not collapse the abstract's "gradual transition" into a specific transition distance unless the figures are verified.
- **Mission scope**: the abstract uses PSP + SO; do not silently fold in Helios / Wind PSDs as if they were the same paper's product.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "α_B narrows / steepens gradually from -3/2 to -5/3 with r, with slow streams steeper than Alfvénic at fixed r" becomes the per-(mission, interval, stream-class) α_B CSV + the per-stream-class α_B(r) overlay + Δα_B scalar.
- **Methods / equations → executable workflows**: trace PSD + inertial-range bound determination + slope fit + radial + stream-class binning are steps 3–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG and Solar Orbiter MAG (+ optional 1-au reference) time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces).
- **Caveats → skill memory**: f_low / f_high sensitivity especially near the Sun, outer-scale and ion-break contamination, stream-class conditioning requirement, "gradual transition" wording boundary.
- **Figures / results → benchmark artifacts**: per-stream-class α_B(r) overlay + per-interval α_B CSV.

## Layer 4 — Research-generation affordances

- **Gap:** the abstract reports the stream-class dependence but does not quantify the per-stream Δα_B at any specific r. A composable experiment that overlays α_B(r, stream) from this skill, σ_c(r) from [[telloni-2025-psp-solo-radial-alignment-2022-december]] (Silwal et al. 2025), and δB/B_outer from [[huang-2023-psp-one-over-f-spectrum]] would directly test whether the slope-steepening rate is governed by the *decay rate of Alfvénicity* with r — i.e. whether ∂α_B/∂r ∝ −∂σ_c/∂r at the stream-class level.
- **Tension:** the slope steepening from -3/2 toward -5/3 with r is a *first-order* observational statement; the same authorship group's earlier inventory entry (1.4, Huang et al. 2023 on 1/f) reports a *near-Sun -3/2 inertial range together with an extended 1/f outer scale*. The composition of "1/f outer range + -3/2 inertial range" near the Sun, transitioning to "1/f-disappears + -5/3 inertial range" further out, is a stronger statement than either paper alone — testable by jointly fitting both ranges on the same interval set.
- **Hypothesis:** the residual / cross-helicity-conditioned α_B(r) curves cross at some heliocentric distance r_cross such that *below* r_cross, slower streams and Alfvénic streams have *similar* α_B (the inertial range is too narrow to discriminate them), while *above* r_cross they diverge as predicted. Testable by reporting α_B(r, σ_c-quartile) and looking for the radius at which the inter-quartile dispersion in α_B first exceeds the per-interval α_B uncertainty.
- **Minimal_experiment:** restrict to PSP E1 + E2 (near-Sun) plus SO mid-cruise intervals; fit α_B with two f_low conventions (one optimistic, one conservative) and report whether the abstract's "narrow inertial range near the Sun" statement is robust under both conventions or only the optimistic one — quantifies the f_low sensitivity that the abstract does not explicitly bound.
- **Composable experiment:** join (α_B, r, stream_class) per interval with [[bowen-2024-extended-cyclotron-resonant-heating]] (f_b at the kinetic break) and [[bandyopadhyay-2020-energy-transfer-psp]] (ε); if f_high / Ω_p, f_low and α_B all evolve consistently with r within stream classes, the slope-steepening is *cascade-internal*; if the cyclotron break shifts independently of α_B, the inertial and dissipation ranges are radially decoupled — a stronger statement than the slope paper alone supports.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` (radial-evolution branch).
- **Sibling paper-skills**: [[huang-2023-psp-one-over-f-spectrum]] (sets f_low context — outer-scale break), [[bowen-2024-extended-cyclotron-resonant-heating]] (sets f_high context — ion-scale break), [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (anisotropy radial evolution complement), [[telloni-2021-psp-solo-radial-alignment-turbulence]] / [[telloni-2025-psp-solo-radial-alignment-2022-december]] (Lagrangian counterparts; Silwal lead-author dispute documented in the 2025 entry), [[bandyopadhyay-2020-energy-transfer-psp]] (cascade rate at near-Sun anchor point).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `solar-orbiter-data-mcp`, `cdflib`. The slope-fit + range-determination pipeline is a candidate Stage-B synthesis skill.
- **Harness contract**: exports α_B(r, stream_class) curve and per-interval (r, alpha_B, f_low, f_high, sigma_c); HelioSI roll-up consumes it as the magnetic-spectral-evolution row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.15 (attributes the paper to "Chen et al., 2022" — paraphrase and year error, not a verified attribution; see banner above).
- Publisher: ApJL 943 (2023) — DOI [10.3847/2041-8213/acaeff](https://doi.org/10.3847/2041-8213/acaeff) (verified 2026-05-19).
- arXiv: [2209.02451](https://arxiv.org/abs/2209.02451) (verified 2026-05-19 — full 27-author Sioulas-led list).
- ADS bibcode: TODO_verify (`2023ApJ...943L...8S` is the natural guess but not directly verified on 2026-05-19).
- Bruno & Carbone (2013) review — solar-wind PSD slopes (foundational, not from inventory).
