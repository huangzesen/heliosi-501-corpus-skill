---
name: zhao-2022-3d-anisotropy-kinetic-scales-psp
description: Use when characterising inertial-range 2D-plus-slab anisotropy of magnetic-field fluctuations on PSP FIELDS data over the first seven orbits (0.1–0.6 au) — central paper claim is that spectral indices and magnetic compressibility in the inertial range are consistent with a 2D + slab turbulence-transport framework, with the 2D power fraction diminishing toward the Sun (Zhao, Zank, Adhikari, & Nakanotani 2022, ApJL 924, L21; DOI 10.3847/2041-8213/ac4415).
version: 0.1.0
tags: [psp, turbulence, inertial-range, 2d-slab-decomposition, magnetic-compressibility, fields, mean-field-frame, transport-theory]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "L.-L. Zhao"
  authors:
    - "L.-L. Zhao"
    - "G. P. Zank"
    - "L. Adhikari"
    - "M. Nakanotani"
  authors_verified: true
  doi: "10.3847/2041-8213/ac4415"
  arxiv_id: null
  year: 2022
  venue: "The Astrophysical Journal Letters 924, L21 (2022)"
---

# Zhao 2022 — Inertial-range Magnetic-fluctuation Anisotropy from PSP First Seven Orbits

> **Title / scope note (verified 2026-05-19).** The IOPscience page for DOI 10.3847/2041-8213/ac4415 lists the published title as *"Inertial-range Magnetic-fluctuation Anisotropy Observed from Parker Solar Probe's First Seven Orbits"* and a four-author list (Zhao, Zank, Adhikari, Nakanotani). The inventory entry `apj_aa_heliophysics_papers.md §1.3` paraphrases this paper as *"Three-Dimensional Anisotropy and Scaling Properties of Solar Wind Turbulence at Kinetic Scales..."* — the published paper is in fact about the **inertial range** under a **2D + slab transport-theory framework**, not a kinetic-range three-axis local-frame structure-function decomposition. The corpus slug `zhao-2022-3d-anisotropy-kinetic-scales-psp` is retained for backwards compatibility but the cited scope is corrected here to the published inertial-range 2D + slab result. Prior content that read this as a kinetic-range three-axis structure-function paper has been replaced.

## When to use this paper-skill

Load this skill when you need to:

- analyse PSP FIELDS magnetic-field fluctuations in the **inertial range** over the first seven orbits (~0.1–0.6 au),
- decompose the fluctuations into **two-dimensional (2D) + slab** components and test consistency with a 2D + slab turbulence-transport framework,
- examine how the **2D power fraction** evolves with heliocentric distance, in particular its diminishing toward the Sun (the paper's headline result).

Skip this skill if your interest is local-frame three-axis (∥, ⊥, displacement) anisotropy in the *kinetic* range (use [[sioulas-2024-higher-order-3d-anisotropy]] from `pilot_turbulence/`), MHD-range Goldreich–Sridhar anisotropy ([[sioulas-2023-anisotropic-scaling-inner-heliosphere]]), the 1/f outer range ([[huang-2023-psp-one-over-f-spectrum]]), or proton/electron heating partition (use the Bowen / Sioulas heating skills in this batch).

## Paper identity and claim boundary

- **Citation**: Zhao, L.-L., Zank, G. P., Adhikari, L., & Nakanotani, M. (2022). *Inertial-range Magnetic-fluctuation Anisotropy Observed from Parker Solar Probe's First Seven Orbits.* **ApJL 924, L21** (2022).
- **DOI**: [10.3847/2041-8213/ac4415](https://doi.org/10.3847/2041-8213/ac4415)
- **ADS bibcode**: `2022ApJ...924L..21Z` (inventory anchor; not directly re-verified against ADS on 2026-05-19).
- **arXiv**: not located on 2026-05-19 (TODO_verify whether a preprint exists).
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.3 (lists this DOI with a paraphrased title that mismatches the published "inertial-range" / "2D + slab" scope — see title note above).

**Evidence boundary — what the abstract supports (verified 2026-05-19 via IOPscience for DOI 10.3847/2041-8213/ac4415):**

- The analysis uses **PSP FIELDS data from the first seven orbits**, spanning approximately **0.1–0.6 au** (abstract-verified radial range).
- The paper analyses **spectral indices and magnetic compressibility within the inertial range** (abstract-verified scope — inertial, not kinetic).
- Observations are tested against a **two-dimensional (2D) + slab turbulence-transport framework**, determining the power distribution between the two components (abstract-verified theoretical framework).
- Results are reported as **consistent with the 2D + slab model**, and the **2D component power fraction diminishes approaching the Sun** (abstract-verified headline result on radial trend).
- Verified four-author list: Zhao, Zank, Adhikari, Nakanotani.

**Out-of-evidence-boundary at this verification depth (still pending full-text verification):**

- The exact per-bin 2D / slab power fractions and the precise heliocentric distance at which the 2D fraction begins to decrease are **TODO_verify** against the published figures.
- The numerical inertial-range spectral index recovered (the abstract refers to "spectral indices" without giving a value) is TODO_verify.
- The exact criterion used to separate 2D vs slab on PSP single-spacecraft data (e.g. magnetic-compressibility threshold, k_perp / k_parallel inference) is TODO_verify.

Out-of-scope (the entry deliberately refuses these): extending the 2D + slab fraction beyond ~0.6 au into the outer heliosphere (the paper's anchor is first-seven-orbits PSP only); applying this to the kinetic / sub-ion range (the paper restricts to the inertial range — the prior "kinetic-scales" framing in the inventory and earlier SKILL.md draft was incorrect); reading the radial trend as a population statement about all stream classes without verifying the conditioning.

> **Assumptions and failure modes** (load-bearing): the 2D + slab decomposition is a transport-theory framework, not a direct k_perp / k_parallel measurement — separating the components on single-spacecraft PSP data leans on magnetic-compressibility and / or spectral-index ratios; the conclusion that the 2D fraction diminishes toward the Sun is sensitive to how 2D vs slab are operationalised, so the decomposition rule must be documented.

## Scientific claim to reproduce or operationalize

In the inertial range of PSP FIELDS magnetic-field fluctuations from the first seven orbits (0.1–0.6 au), measured spectral indices and magnetic compressibility are consistent with a 2D + slab turbulence-transport framework. The 2D component carries a non-trivial fraction of the inertial-range power, but this 2D power fraction decreases with decreasing heliocentric distance — i.e. closer to the Sun, the slab component is more prominent. This skill operationalises that statement as a per-interval (slope, magnetic-compressibility) pipeline whose outputs are fed into a 2D + slab inversion to recover the per-bin 2D power fraction.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, \|B\| | L2, RTN, ≥1 vec/s | CDAWeb / PSP SOC (`psp_fld_l2_mag_rtn_*.cdf`, `*_4_per_cycle_*.cdf`) |
| PSP SWEAP/SPC or SPAN-I | n_p, V_RTN (for V_A, ρ_i context) | L3 | CDAWeb / PSP SOC |

Time range: **PSP Orbits 1–7** (approximately 0.1–0.6 au; abstract-verified). Exact per-orbit windowing **TODO_verify** against §2 of ApJL 924, L21.

## Algorithm/workflow steps

1. **Interval selection** — Build clean inertial-range PSP intervals across Orbits 1–7 with continuous FIELDS MAG and valid SWEAP plasma moments; exclude shocks / CMEs / HCS crossings.
2. **Trace and compressibility PSDs** — Per interval, compute the trace magnetic PSD and the \|B\| (parallel) PSD; report the inertial-range bandwidth.
3. **Inertial-range fits** — Fit the spectral index of the trace PSD; report magnetic compressibility C(f) = PSD(\|B\|) / PSD(B_trace) per interval.
4. **2D + slab inversion** — Apply a 2D + slab transport-framework inversion (Bieber-class) to the measured spectral index and compressibility to recover the (2D / slab) power partition per interval. Document the inversion convention.
5. **Radial binning** — Bin (slope, compressibility, 2D fraction) per heliocentric-distance bin across 0.1–0.6 au.
6. **Radial trend** — Show the 2D power fraction diminishing approaching the Sun (the paper's abstract-verified headline result).
7. **Acceptance** — Recover the qualitative radial trend (∂(2D fraction)/∂r > 0 across the 0.1–0.6 au range); per-bin numerical 2D fractions and inertial-range slope TODO_verify against ApJL 924, L21 figures.

## Minimal executable benchmark or validation target

**Target**: across PSP Orbits 1–7 (0.1–0.6 au), the inertial-range (spectral index, magnetic compressibility) pair inverts to a 2D + slab decomposition whose **2D power fraction increases monotonically with heliocentric distance** (abstract-verified qualitative result — "the 2D component power fraction diminishes approaching the Sun"). Exact per-orbit 2D / slab fractions and inertial-range slope values TODO_verify against figures of ApJL 924, L21.

Recommended check artifacts:

- `zhao2022_inertial_2d_slab.csv` — one row per interval × distance bin: (t_start, t_end, r_au, orbit, slope_B_trace, magnetic_compressibility, fraction_2D, fraction_slab).
- Trace and \|B\| PSD overlay panel for one representative interval per orbit.
- Single scalar QC: monotonic-increase test on fraction_2D vs r across the 0.1–0.6 au bins (target: Spearman ρ > 0).

## Known pitfalls / failure modes

- **2D + slab inversion convention**: the partition is theory-dependent — different inversion conventions (Bieber-class, Saur-class, others) give different fractions. Document the choice.
- **Magnetic compressibility estimator**: C(f) = PSD(\|B\|) / PSD(B_trace) is the standard single-spacecraft proxy but it is sensitive to the choice of frequency band over which it is computed.
- **Inertial-range bounds**: the slope (and the corresponding compressibility-based inversion) depend on f_low and f_high; near the Sun (PSP ~0.1 au) the inertial range is narrow (cf. [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] / Sioulas et al. 2023), so the inversion is particularly fragile in the near-Sun bins.
- **Single-spacecraft inference**: PSP cannot directly measure k_perp / k_parallel; the 2D vs slab decomposition is *inferred*, not observed.
- **Spin-tone / instrument artefacts**: residual spin lines in MAG inflate parallel-axis power and bias C(f).
- **"Diminishes toward the Sun"** — the abstract phrases this qualitatively; do not silently widen to "vanishes" or to a specific functional form.

## Paper-as-Skill compilation

This paper is compiled into an agent-native Anthropic-style Skill:

- **Claims → verifiable tasks**: "PSP inertial-range observations are consistent with 2D + slab, and the 2D fraction diminishes toward the Sun (Orbits 1–7, 0.1–0.6 au)" becomes the per-interval CSV + fraction_2D(r) curve + the Spearman-trend scalar.
- **Methods / equations → executable workflows**: trace + compressibility PSDs + inertial-range fits + 2D + slab inversion + radial binning are workflow steps 2–5.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS MAG L2 and SWEAP plasma-moment time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces — the harness uses Read/Bash/WebFetch + cdflib as the guaranteed substrate).
- **Caveats → skill memory**: 2D + slab inversion convention, single-spacecraft inference caveat, near-Sun narrow inertial-range fragility, "diminishes" wording boundary.
- **Figures / results → benchmark artifacts**: fraction_2D(r) curve + per-interval CSV + per-orbit PSD overlay.

The Claude Code harness is the **general-purpose runtime**; HelioSI is its **domain instantiation as a skill graph**, and this paper-skill is a leaf within that graph.

## Layer 4 — Research-generation affordances

- **Gap:** the paper's 2D vs slab fractions are *inferred* from single-spacecraft compressibility, not measured directly. A composable experiment that joins this skill's per-interval (slope, compressibility, fraction_2D) table with [[telloni-2021-psp-solo-radial-alignment-turbulence]] and [[telloni-2025-psp-solo-radial-alignment-2022-december]] (Silwal et al. 2025) PSP–SO conjunction windows would let cross-spacecraft increment-direction information *test* the 2D-vs-slab inversion against an independent direction-of-k constraint.
- **Tension:** the abstract reports that the 2D fraction *diminishes* approaching the Sun (so the slab fraction is relatively *larger* near the Sun); [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (Sioulas et al. 2023) reports that the inertial-range slope is *shallower* (closer to -3/2) near the Sun and steepens toward -5/3 with distance. A slab-dominated inertial range with -3/2 scaling versus a more-2D inertial range with -5/3 scaling is a non-trivial joint statement — testable by overlaying (slope, fraction_2D) per (r, stream class) on a single plot.
- **Hypothesis:** the radial trend ∂(fraction_2D)/∂r > 0 is *driven* by the radial trend in Alfvénicity rather than by the cascade dynamics — i.e. near the Sun, more Alfvénic streams have higher slab fraction because Alfvénic outward propagation is intrinsically slab-like. Testable by stratifying (fraction_2D, r) by σ_c-quartile (Alfvénicity).
- **Minimal_experiment:** rerun the 2D + slab inversion with two compressibility estimators (e.g. C from \|B\|/B_trace at a fixed bandwidth, vs C from the eigenvalues of the spectral matrix); report whether the "fraction_2D decreases toward the Sun" result is robust under both — quantifies the inversion-convention sensitivity that the abstract does not bound.
- **Composable experiment:** join (slope, compressibility, fraction_2D, r) per interval with [[bandyopadhyay-2020-energy-transfer-psp]] cascade-rate ε and [[bowen-2024-extended-cyclotron-resonant-heating]] (Bowen, Vasko, Bale et al. 2024) ICW activity on the same intervals; if the slab-dominated near-Sun intervals are also the highest-ε and highest-ICW intervals, the inertial-to-dissipation pipeline is *slab-channelled* near the Sun and *2D-channelled* farther out — a stronger statement than the present paper alone supports.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` sub-graph (inertial-range / transport-theory branch).
- **Sibling paper-skills**: [[sioulas-2023-anisotropic-scaling-inner-heliosphere]] (MHD-range Goldreich–Sridhar counterpart), [[sioulas-2024-higher-order-3d-anisotropy]] (higher-order, imbalanced-Alfvénic regime; *the actual* kinetic-range 3D anisotropy skill in this corpus, not this one), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (radial inertial-range slope steepening context; Sioulas lead-author dispute documented there), [[bowen-2024-extended-cyclotron-resonant-heating]] (ion-cyclotron waves at the spectral break — neighbouring scale regime).
- **MCPs (proposed contracts, not assumed runtime)**: `psp-data-mcp` for FIELDS / SWEAP retrieval; `cdflib` / `pyspedas` for I/O. The 2D + slab inversion is a candidate Stage-B synthesis skill.
- **Harness contract**: this skill exports {slope_B_trace, magnetic_compressibility, fraction_2D, fraction_slab} per heliocentric-distance bin; HelioSI roll-up consumes it as the inertial-range 2D + slab decomposition row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.3 (paraphrases the title as "Three-Dimensional Anisotropy and Scaling Properties of Solar Wind Turbulence at Kinetic Scales..." — published paper is in fact the inertial-range 2D + slab result; see title note above).
- Publisher: ApJL 924, L21 (2022) — DOI [10.3847/2041-8213/ac4415](https://doi.org/10.3847/2041-8213/ac4415) (verified 2026-05-19 — four-author list Zhao, Zank, Adhikari, Nakanotani; "Inertial-range Magnetic-fluctuation Anisotropy Observed from PSP's First Seven Orbits" title; 2D + slab framework; 2D fraction diminishes toward the Sun).
- ADS: `2022ApJ...924L..21Z` (inventory anchor; not directly verified against ADS on 2026-05-19).
- Bieber et al. — 2D + slab transport framework (foundational, not from inventory).
