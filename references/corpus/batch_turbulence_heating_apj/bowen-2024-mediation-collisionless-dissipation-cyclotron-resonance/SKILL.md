---
name: bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance
description: Use when arguing that cyclotron resonance — not Landau / KAW damping alone — mediates collisionless turbulent dissipation in the inner heliosphere — central paper claim is that PSP FIELDS ion-scale magnetic spectra exhibit circular-polarisation signatures and resonant-heating diagnostics consistent with ion-cyclotron waves providing a major pathway for solar-wind dissipation and plasma heating (Bowen et al. 2024, Nat. Astron. 8(4), 482–490; DOI 10.1038/s41550-023-02186-4; PMID 38659611).
version: 0.1.0
tags: [psp, cyclotron-resonance, collisionless-dissipation, ion-scale, polarisation, nature-astronomy, fields]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "T. A. Bowen"
  authors:
    - "T. A. Bowen"
    - "S. D. Bale"
    - "B. D. G. Chandran"
    - "A. Chasapis"
    - "C. H. K. Chen"
    - "T. Dudok de Wit"
    - "A. Mallet"
    - "R. Meyrand"
    - "J. Squire"
  authors_verified: true
  doi: "10.1038/s41550-023-02186-4"
  pmid: "38659611"
  arxiv_id: null
  year: 2024
  venue: "Nature Astronomy 8(4), 482–490 (2024)"
---

# Bowen 2024 — Mediation of Collisionless Dissipation by Cyclotron Resonance (PSP)

## When to use this paper-skill

Load this skill when you need to:

- test whether the **collisionless dissipation** of solar-wind turbulence is mediated by **cyclotron resonance** rather than by KAW / Landau damping alone,
- inspect ion-scale magnetic spectra for **circular-polarisation signatures** that constrain the dissipation mechanism,
- combine PSP FIELDS spectra with resonant-heating diagnostics to argue for a specific dissipation pathway.

Skip this skill if your question is the observational detection of ICW peaks in fast streams (use [[bowen-2024-extended-cyclotron-resonant-heating]]) or the Landau-channel proton/electron partition (use [[bowen-2023-landau-damping-proton-electron-heating]]).

## Paper identity and claim boundary

- **Citation**: Bowen, T. A., Bale, S. D., Chandran, B. D. G., Chasapis, A., Chen, C. H. K., Dudok de Wit, T., Mallet, A., Meyrand, R., & Squire, J. (2024). *Mediation of Collisionless Turbulent Dissipation Through Cyclotron Resonance.* **Nature Astronomy** 8(4), 482–490.
- **DOI**: [10.1038/s41550-023-02186-4](https://doi.org/10.1038/s41550-023-02186-4)
- **PubMed**: 38659611
- **arXiv**: not located on 2026-05-19 (Nature Astronomy submission — TODO_verify whether a preprint exists, e.g. via ADS abstract).
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.9.

**Evidence boundary — what the abstract supports (verified 2026-05-19 via PubMed citation page resolving DOI 10.1038/s41550-023-02186-4):**

- The paper is published in **Nature Astronomy volume 8, issue 4, pages 482–490 (2024)** with a full nine-author list led by T. A. Bowen (abstract / metadata-verified).
- The central claim is that **"ion cyclotron waves provide a major pathway for dissipation and plasma heating in the solar wind"** — i.e. cyclotron resonance is identified as a *major* pathway (not necessarily the unique pathway), supporting theoretical predictions about ion-scale turbulence behaviour in the inner heliosphere (abstract-verified phrasing).
- The empirical basis is PSP FIELDS observations of ion-scale fluctuations connecting cyclotron resonance to ion-scale energy conversion (abstract-verified at the source-vs-mechanism level).

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact ion-scale frequency band, the per-encounter polarisation diagnostics, the quantitative Q_p,cyc estimate and any Q_p,cyc / Q_p,Landau ratio are **TODO_verify** against §3 / Figs. of Nat. Astron. 8 (2024).
- Whether the paper presents the resonance-overlap integral or only a reduced-helicity / ellipticity diagnostic in support of the cyclotron-mediation claim is TODO_verify against the methods section.
- The encounter list and per-encounter heliocentric distance range covered are TODO_verify.

Out-of-scope (the entry deliberately refuses these): claiming cyclotron resonance is the **unique** dissipation channel everywhere (the abstract says "a major pathway", not "the sole pathway"); collapsing the statement onto a single perihelion or encounter when the paper's heliophysics scope is broader; extending to electron-scale dissipation without separate evidence; treating this Nature Astronomy paper as interchangeable with [[bowen-2024-extended-cyclotron-resonant-heating]] (which is the radially extended fast-stream observational identification skill — same lead author, same physics class, but a distinct paper and arXiv submission).

> **Assumptions and failure modes** (load-bearing): polarisation handedness is sensitive to the +B₀ convention — an inverted convention reverses the conclusion; spacecraft give reduced (1D) helicity, so 3D polarisation requires k-orientation assumptions; the cyclotron-resonance overlap integral depends on the assumed v_∥ distribution, which for PSP is only well measured for protons (SPC field-of-view limitations).

## Scientific claim to reproduce or operationalize

At ion scales, PSP FIELDS magnetic spectra exhibit polarisation signatures (handedness, ellipticity, helicity) characteristic of cyclotron resonance with the proton population; combined with resonant-heating diagnostics, these features place the dissipation channel in the cyclotron-resonant regime as a major pathway alongside (rather than instead of) Landau / KAW damping. The paper's verifiable target is the **identification of an ion-cyclotron-wave-mediated dissipation pathway** in PSP ion-scale fluctuations, not a unique exclusion of competing channels.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, full-vector PSD, magnetic helicity σ_m | L2, ≥1 vec/s; Burst-mode for ion-scale resolution | CDAWeb / PSP SOC |
| PSP SWEAP/SPC, SPAN-I | n_p, V_RTN, T_p⊥, T_p∥ | L3 | CDAWeb / PSP SOC |

Time range: representative PSP intervals covering a range of stream classes and heliocentric distances — exact encounter list **TODO_verify** against the published Methods section.

## Algorithm/workflow steps

1. **Interval selection** — Quasi-stationary PSP intervals with FIELDS Burst-mode or high-cadence MAG and valid SPC / SPAN-I plasma moments.
2. **Mean-field-aligned frame** — Compute scale-dependent local B₀ and rotate B into a (∥, ⊥1, ⊥2) frame. Document the +B₀ convention explicitly.
3. **Polarisation diagnostics** — Compute reduced normalised magnetic helicity σ_m(f), ellipticity ε(f), polarisation angle relative to B₀.
4. **Cyclotron signature** — Identify frequencies / wavenumbers where σ_m is strongly LH (under the documented convention) and ellipticity → 1 (circular).
5. **Resonance overlap** — Combine the local proton distribution function with the cyclotron resonance condition ω − k_∥ v_∥ = ±Ω_p; compute the fraction of proton phase space resonant with the wave band.
6. **Heating-rate diagnostic** — Estimate Q_p,cyc from quasilinear theory using the measured wave amplitude and resonance overlap; compare to alternative channels (Landau / KAW) — exact comparison formula **TODO_verify** against full text.
7. **Acceptance** — Circular-polarisation signature + resonance overlap together imply cyclotron resonance is *a major* dissipation pathway (the abstract-verified claim); a unique-channel claim is out-of-scope.

## Minimal executable benchmark or validation target

**Target**: ion-scale PSP magnetic spectra show LH-circular-polarised signatures with resonance overlap to the proton distribution; the implied Q_p,cyc is consistent with the paper's conclusion that ion-cyclotron waves are a major dissipation pathway (TODO_verify per-encounter magnitudes against figures of Nat. Astron. 8 (2024), pp. 482–490).

Recommended check artifacts:

- `bowen2024_mediation_cyclotron.csv` — one row per interval: (t_start, t_end, r_au, σ_m_band, ε_band, resonance_overlap, Q_p,cyc, Q_p,Landau, ratio).
- σ_m(f) / ellipticity diagnostic panel per representative interval.
- Single scalar QC: Q_p,cyc / Q_p,Landau median across the interval set (qualitative target — the paper claims cyclotron is a *major* pathway, so the QC test is "Q_p,cyc is non-negligible relative to Q_p,Landau", not "Q_p,cyc > Q_p,Landau").

## Known pitfalls / failure modes

- **Frame and handedness convention**: same caveat as [[bowen-2024-extended-cyclotron-resonant-heating]] — the LH/RH sign depends on the chosen +B₀ direction; an inverted convention trivially reverses the conclusion. Document the convention before computing σ_m.
- **Reduced vs full helicity**: spacecraft give reduced helicity (1D measurement along V_sw); inferring 3D polarisation from this requires assumptions about k orientation.
- **Resonance-overlap estimate**: the overlap integral depends sensitively on the assumed parallel-velocity distribution, which is only well measured for protons (SPC field-of-view limitations); be honest about SPAN-I / SPAN-e coverage gaps per interval.
- **Wave-vs-structure ambiguity**: not all narrow-band features at ion scales are waves; some may be coherent structures (cf. [[pecora-2022-coherent-structures-proton-electron-heating]]) — control with structure metrics.
- **Cadence requirement**: ion-scale polarisation needs Burst-mode cadence; survey-mode aliases the signal.
- **"Major pathway" vs "unique channel"**: do not silently widen the abstract's "a major pathway" wording to "the dominant" or "the sole" channel — the paper is consistent with co-existing Landau / KAW dissipation.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "ion-cyclotron waves provide a major dissipation pathway in PSP ion-scale data" becomes the per-interval CSV + the Q_p,cyc vs Q_p,Landau scalar (interpreted as a "non-negligible" check, not a strict majority check).
- **Methods / equations → executable workflows**: mean-field frame + reduced helicity + ellipticity + resonance overlap + quasilinear Q_p,cyc are steps 2–6.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 Burst and SWEAP plasma-moment time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces).
- **Caveats → skill memory**: convention sensitivity, reduced-vs-full helicity caveat, wave-vs-structure ambiguity, and the "major" vs "unique" wording boundary.
- **Figures / results → benchmark artifacts**: σ_m / ellipticity diagnostic panel + per-interval CSV.

## Layer 4 — Research-generation affordances

- **Gap:** the inventory pairs this Nat. Astron. paper with [[bowen-2024-extended-cyclotron-resonant-heating]] (arXiv 2406.10446) as if they are the same observational thread, but the Nat. Astron. paper is a *mechanism-mediation* argument while 2406.10446 is a *radially extended observational identification* over 15–55 R☉. A composable experiment that runs both protocols on the same PSP encounter set and reports whether the per-interval Q_p,cyc estimates *agree* between the two analyses would explicitly test whether the "mediation" and the "extended" claims are consistent on shared windows, or whether one is a stronger condition than the other.
- **Tension:** [[bowen-2023-landau-damping-proton-electron-heating]] (actually Shankarappa et al. 2023, see slug-attribution note in that entry) reports that a Landau-damping cascade model accurately describes the spectrum in ≥39% of PSP E1–E2 intervals; the present paper's "cyclotron is a major pathway" claim is not in formal contradiction (both channels can co-exist) but the *fraction* of intervals where each channel dominates is an open empirical question that neither paper resolves on a shared interval set. A side-by-side per-interval re-analysis is the natural resolution.
- **Hypothesis:** in PSP intervals with simultaneously high β_p (favouring Landau-channel KAW damping) AND a clean LH-circular ICW peak at the spectral break, **both** Q_p,cyc and Q_p,Landau are non-zero and their ratio is bounded by O(1) — neither channel asymptotically dominates. Testable by stratifying matched windows by β_p and reporting (Q_p,cyc, Q_p,Landau) per (β_p, r_au) bin.
- **Minimal_experiment:** on five representative PSP E1–E4 Burst-mode intervals, compute (σ_m_band, ε_band, resonance_overlap, Q_p,cyc) per this skill *and* (Q_p_model_Landau) per [[bowen-2023-landau-damping-proton-electron-heating]] (Shankarappa et al. 2023); report the per-interval ratio and the median across the five. Even without full-text validation tolerances, the per-interval consistency between two distinct channel estimates is a non-trivial test.
- **Composable experiment:** join (Q_p,cyc, Q_p,Landau) per interval with [[pecora-2022-coherent-structures-proton-electron-heating]] (actually Sioulas et al. 2022, see slug-attribution note in that entry) coherent-structure-conditioned ΔT_p; the three-channel decomposition (cyclotron / Landau / coherent-structure) on a shared interval set would be the first empirical attempt to budget collisionless proton heating across the inner heliosphere on a paper-grounded basis rather than in a model-only synthesis.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `waves_instabilities` + `coronal_heating` bundles (collisionless-dissipation mechanism branch).
- **Sibling paper-skills**: [[bowen-2024-extended-cyclotron-resonant-heating]] (observational fast-stream identification — same author, distinct paper), [[bowen-2023-landau-damping-proton-electron-heating]] (Landau channel — the explicit alternative this paper contrasts with; note Shankarappa lead-author attribution dispute documented in that entry), [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] (independent ICW evidence from Solar Orbiter density), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (spectral-break radial evolution context; note Sioulas lead-author dispute), [[zhao-2022-3d-anisotropy-kinetic-scales-psp]] (kinetic-scale anisotropy context).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `cdflib`, optional `wavelet-polarisation-mcp` (shared synthesis candidate with the extended-cyclotron skill).
- **Harness contract**: exports {σ_m_band, ε_band, Q_p,cyc, Q_p,Landau, ratio} per interval; HelioSI roll-up consumes it as the cyclotron-mediation row complementary to the Landau-partition row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.9.
- Publisher: Nature Astronomy 8(4), 482–490 (2024) — DOI [10.1038/s41550-023-02186-4](https://doi.org/10.1038/s41550-023-02186-4).
- PubMed citation: [PMID 38659611](https://pubmed.ncbi.nlm.nih.gov/38659611/) (verified 2026-05-19).
- ADS candidate bibcode: TODO_verify (`2024NatAs...8..482B` is the natural guess but not directly verified on 2026-05-19).
- Howes (2008) and Klein & Howes — kinetic-cascade theory (foundational, not from inventory).
