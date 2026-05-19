---
name: cuesta-2022-compressible-turbulence-psp-themis-maven
description: Use when characterising the radial evolution of compressible (density-fluctuation) solar-wind turbulence between 0.17 and 1.5 au using PSP, THEMIS, and MAVEN — central paper claim is that density-fluctuation spectra and compressibility evolve systematically from the inner heliosphere (PSP) to ~1.5 au (MAVEN), with THEMIS at 1 au as the intermediate anchor (Cuesta et al. 2022, ApJ; DOI 10.3847/1538-4357/ac0af5).
version: 0.1.0
tags: [psp, themis, maven, compressible-turbulence, density-fluctuations, radial-evolution, multi-spacecraft]
quality_level: pilot
executable_status: scaffold
---

# Cuesta 2022 — Compressible Solar-Wind Turbulence PSP/THEMIS/MAVEN

## When to use this paper-skill

Load this skill when you need to:

- characterise the **radial evolution of compressible turbulence** (density-fluctuation spectra and compressibility) between ~0.17 au (PSP) and ~1.5 au (MAVEN),
- combine **three spacecraft** (PSP, THEMIS, MAVEN) into a single multi-mission radial-evolution dataset,
- benchmark a compressibility / density-spectrum estimator across heliocentric distance.

Skip this skill if your interest is purely incompressible MHD inertial range (use the Bandyopadhyay / Sioulas pilot skills) or 1/f outer-range scaling ([[huang-2023-psp-one-over-f-spectrum]]).

## Paper identity and claim boundary

- **Citation**: Cuesta, M. M., Chhiber, R., Parashar, T. N., Matthaeus, W. H., et al. (2022). *Evolution of Compressible Solar Wind Turbulence in the Inner Heliosphere: PSP, THEMIS, and MAVEN Observations.* **ApJ**.
- **DOI**: 10.3847/1538-4357/ac0af5
- **arXiv**: TODO verify.
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.10.

**Claim boundary** — only the inventory-supported claim is treated as fixed:

> Density-fluctuation spectra and compressibility of solar-wind turbulence evolve systematically with heliocentric distance from ~0.17 au to ~1.5 au, as observed by PSP, THEMIS, and MAVEN.

Out-of-scope: extending the conclusion to outer-heliosphere distances (Ulysses, Voyager) without separate evidence; conflating MAVEN-derived solar-wind density with Martian foreshock signatures; collapsing across stream classes when the paper conditions on a particular class (TODO verify exact stream conditioning).

## Scientific claim to reproduce or operationalize

Density (and compressibility) of solar-wind turbulence is not radially constant. Density-fluctuation spectra and compressibility indicators measured at PSP, THEMIS, and MAVEN show a systematic dependence on heliocentric distance over 0.17–1.5 au. The skill operationalises this as a multi-spacecraft radial-evolution table for compressibility-related observables.

## Required data/instruments and likely files/archives

| Instrument | Quantity | Cadence/level | Archive |
| --- | --- | --- | --- |
| PSP FIELDS MAG | B_RTN, |B| | L2 | CDAWeb / PSP SOC |
| PSP SWEAP/SPC | n_p, V_RTN, T_p | L3 | CDAWeb / PSP SOC |
| THEMIS FGM | B (GSE/GSM) | L2 | CDAWeb / THEMIS data center |
| THEMIS ESA | n_p, V, T_p | L2 | CDAWeb / THEMIS data center |
| MAVEN MAG | B | L2 | PDS / CDAWeb |
| MAVEN SWIA | solar-wind n_p, V, T_p (upstream of bow shock only) | L2 | PDS |

MAVEN intervals must be restricted to clean upstream solar-wind segments outside the Martian bow shock — TODO verify the specific selection criterion used in the paper.

## Algorithm/workflow steps

1. **Multi-mission interval selection** — Build a per-mission catalog of clean solar-wind intervals; for MAVEN, restrict to upstream segments outside the bow shock.
2. **Density-fluctuation time series** — Extract n_p time series per interval; remove instrumental gaps and outliers.
3. **Spectral estimation** — Compute density PSD via Welch / multitaper with explicit window length and overlap; compute trace magnetic PSD on the same interval for compressibility.
4. **Compressibility metric** — Compute C_n = (δn/n)² / (δ|B|²/B² + δn²/n²) (or paper-specific definition — TODO verify).
5. **Radial binning** — Bin spectra and compressibility metrics in heliocentric-distance bins spanning 0.17–1.5 au.
6. **Radial trend** — Fit a power-law or empirical trend to compressibility-related observables vs r.
7. **Acceptance** — Recover the systematic radial trend reported in the paper (sign and qualitative magnitude match Fig. in paper; TODO verify exact power-law slope).

## Minimal executable benchmark or validation target

**Target**: compressibility metric C_n exhibits the systematic radial trend reported in Cuesta et al. 2022 between 0.17 au and 1.5 au across PSP / THEMIS / MAVEN intervals (TODO verify exact slope / values).

Recommended check artifacts:

- `cuesta2022_compressible_evolution.csv` — one row per (mission, interval): (mission, t_start, t_end, r_au, slope_n_psd, C_n).
- Three-panel PSD comparison plot at representative r ∈ {0.2, 1.0, 1.5} au.
- Single scalar QC: fitted slope of C_n vs r.

## Known pitfalls / failure modes

- **MAVEN bow-shock contamination**: MAVEN SWIA / MAG segments inside the bow shock or foreshock are not solar wind — strict exclusion criteria are required.
- **Inter-instrument cadence mismatch**: PSP, THEMIS, MAVEN sample at different cadences; spectra must be computed with matched bandwidth before comparison.
- **Density-moment definitions**: SPC, ESA, and SWIA derive n_p with different methods; per-instrument biases must be acknowledged.
- **Stream-class conditioning**: aggregating fast and slow streams in one radial bin can mask the physical trend — split by class.
- **Spacecraft separation**: PSP / THEMIS / MAVEN are not co-aligned; the radial-evolution statement is statistical, not Lagrangian (cf. [[telloni-2021-psp-solo-radial-alignment-turbulence]] for the conjunction case).
- **Outlier intervals**: large density spikes (e.g. CIRs, CMEs) skew spectra — exclude via shock catalogs.

## Paper-as-Skill compilation

- **Claims → verifiable tasks**: "compressibility evolves between 0.17 and 1.5 au" becomes the multi-mission radial-evolution CSV + the C_n vs r slope.
- **Methods / equations → executable workflows**: density PSD + compressibility metric + radial binning are steps 3–5.
- **Data / instruments → capability contracts**: the protocol requires capabilities to retrieve PSP FIELDS + SWEAP, THEMIS FGM + ESA, and MAVEN MAG + SWIA time series at the required cadence; runtimes bind concrete adapters (see Layer 3 for example bindings, which remain proposed surfaces — only general-purpose Read/Bash/WebFetch + CDF / PDS tooling is guaranteed).
- **Caveats → skill memory**: bow-shock exclusion, inter-instrument cadence, density-moment biases.
- **Figures / results → benchmark artifacts**: multi-mission PSD comparison + C_n vs r curve.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` (compressible-evolution branch) + multi-mission infrastructure.
- **Sibling paper-skills**: [[telloni-2021-psp-solo-radial-alignment-turbulence]] (Lagrangian conjunction case), [[telloni-2025-psp-solo-radial-alignment-2022-december]] (follow-up alignment), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (incompressible / magnetic spectral radial evolution), [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] (density spectra at ~0.5 au from SO).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `themis-data-mcp`, `maven-data-mcp`, `cdflib` / PDS readers.
- **Harness contract**: exports per-mission per-interval (slope_n_psd, C_n, r_au); HelioSI roll-up consumes it as the compressibility radial-evolution row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.10.
- DOI: https://doi.org/10.3847/1538-4357/ac0af5
- Matthaeus & Goldstein (1982) — early solar-wind compressibility (foundational, not from inventory).
