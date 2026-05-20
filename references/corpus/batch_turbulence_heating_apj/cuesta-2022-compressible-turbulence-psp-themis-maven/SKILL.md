---
name: cuesta-2022-compressible-turbulence-psp-themis-maven
description: Use when characterising the radial evolution of compressible (density-fluctuation) solar-wind turbulence between 0.17 and 1.5 au using PSP, THEMIS, and MAVEN — inventory-attributed to Cuesta et al. 2022 but the DOI 10.3847/1538-4357/ac0af5 cited in inventory resolves to Andrés et al. 2021 (compressible cascade-rate measurements 0.2–1.7 au, PSP + THEMIS + MAVEN). Both papers are real and topically related; the corpus entry's canonical identifier is currently disputed and pending curator resolution.
version: 0.1.0
tags: [psp, themis, maven, compressible-turbulence, density-fluctuations, radial-evolution, multi-spacecraft, identifier-disputed]
quality_level: pilot
executable_status: scaffold
paper:
  first_author: "M. M. Cuesta"
  authors:
    - "M. M. Cuesta"
    - "R. Chhiber"
    - "T. N. Parashar"
    - "W. H. Matthaeus"
  authors_verified: false
  doi: null
  arxiv_id: null
  year: 2022
  venue: "TODO_verify (identifier dispute — see banner below)"
---

# Cuesta 2022 — Compressible Solar-Wind Turbulence PSP/THEMIS/MAVEN

> **Identifier dispute (verified 2026-05-19).** The inventory `apj_aa_heliophysics_papers.md §1.10` attributes this entry to *Cuesta et al. 2022, ApJ, DOI 10.3847/1538-4357/ac0af5*. The DOI 10.3847/1538-4357/ac0af5 was verified on 2026-05-19 to resolve to **Andrés, Sahraoui, Hadid, Huang, Romanelli, Galtier, DiBraccio, & Halekas (2021)**, *"The Evolution of Compressible Solar Wind Turbulence in the Inner Heliosphere: PSP, THEMIS, and MAVEN Observations"*, ApJ **919** (2021) — same title verbatim, same three-spacecraft scope, but lead author is Andrés (not Cuesta) and year is 2021 (not 2022). Either (a) the inventory paraphrase confused two papers that share a title family, or (b) a separate Cuesta-led 2022 paper exists at a different DOI. Until a curator pass resolves the ambiguity, this entry's canonical DOI is set to null and the identifier is flagged as disputed in `verification_flags`. The pipeline framing below (multi-spacecraft compressible-turbulence radial evolution across PSP, THEMIS, MAVEN) is topically valid for *either* candidate paper, and is retained on that basis. Do *not* cite this entry with the Andrés DOI under the Cuesta attribution in a manuscript without resolving the dispute first.

## When to use this paper-skill

Load this skill when you need to:

- characterise the **radial evolution of compressible turbulence** (density-fluctuation spectra and compressibility) between ~0.17 au (PSP) and ~1.5 au (MAVEN),
- combine **three spacecraft** (PSP, THEMIS, MAVEN) into a single multi-mission radial-evolution dataset,
- benchmark a compressibility / density-spectrum estimator across heliocentric distance.

Skip this skill if your interest is purely incompressible MHD inertial range (use the Bandyopadhyay / Sioulas pilot skills) or 1/f outer-range scaling ([[huang-2023-psp-one-over-f-spectrum]]).

## Paper identity and claim boundary

- **Claimed citation (inventory)**: Cuesta, M. M., Chhiber, R., Parashar, T. N., Matthaeus, W. H., et al. (2022). *Evolution of Compressible Solar Wind Turbulence in the Inner Heliosphere: PSP, THEMIS, and MAVEN Observations.* **ApJ** (per inventory).
- **Resolved DOI (verified 2026-05-19)**: 10.3847/1538-4357/ac0af5 resolves to **Andrés et al. 2021**, ApJ **919** — same title verbatim and same PSP + THEMIS + MAVEN scope (over **0.2–1.7 au** per the Andrés abstract; the inventory paraphrase quotes 0.17–1.5 au). The eight-author Andrés list is: N. Andrés, F. Sahraoui, L. Z. Hadid, S. Y. Huang, N. Romanelli, S. Galtier, G. DiBraccio, J. Halekas.
- **Corpus DOI / arXiv**: deliberately set to null pending curator resolution (see banner above).
- **Source inventory**: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.10 (lists DOI 10.3847/1538-4357/ac0af5 with a "Cuesta et al. 2022" attribution — this attribution does not match the DOI as resolved on 2026-05-19).

**Evidence boundary — what can be asserted under the dispute (verified 2026-05-19 via IOPscience for DOI 10.3847/1538-4357/ac0af5):**

- A real published paper at DOI 10.3847/1538-4357/ac0af5 exists; it is by **Andrés et al. (2021)**, **ApJ 919**, and reports the **first measurements of compressible cascade rates** across PSP, THEMIS, and MAVEN spanning ~0.2–1.7 au using an exact isothermal-MHD framework.
- The Andrés abstract specifically notes that compressibility levels **reach up to 25 % near PSP's closest approach** (abstract-verified), with the compressible-cascade contribution becoming non-negligible relative to the incompressible cascade at these distances.
- The Andrés abstract connects the observation to ion temperature variations and advances understanding of solar-wind heating mechanisms (abstract-verified relevance to the corpus's heating-batch scope).

**Out-of-evidence-boundary at this verification depth (pending dispute resolution):**

- Whether a distinct *Cuesta et al. 2022* paper exists in ApJ (or in MNRAS / A&A) with the same three-spacecraft scope but a different DOI is **TODO_verify** by a future curator pass (ADS search by first author + title keywords).
- If the inventory is in fact paraphrasing Andrés 2021 under a wrong first-author attribution, the corpus slug `cuesta-2022-…` is misattributed and should eventually be reconciled (mirroring the slug-retention pattern applied elsewhere in this batch).
- All quantitative numerical targets below are written for the **inventory-paraphrased scope** (0.17–1.5 au compressibility radial trend); they should be re-verified against whichever paper the curator decides is canonical.

Out-of-scope (the entry deliberately refuses these): extending the conclusion to outer-heliosphere distances (Ulysses, Voyager) without separate evidence; conflating MAVEN-derived solar-wind density with Martian foreshock signatures; collapsing across stream classes when the paper(s) condition on a particular class; **propagating the Andrés DOI under a Cuesta attribution in a manuscript** — that would propagate the identifier dispute downstream.

> **Assumptions and failure modes** (load-bearing): MAVEN-derived solar-wind moments require strict upstream-of-bow-shock conditioning; PSP / THEMIS / MAVEN sample at different cadences and must be bandwidth-matched before pooling; per-instrument density-moment definitions (SPC, ESA, SWIA) carry per-instrument biases; the radial trend across three missions is a statistical, not Lagrangian, statement.

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

## Layer 4 — Research-generation affordances

- **Gap:** the identifier dispute itself is a Layer-4 affordance — it surfaces an unresolved provenance question that no other paper-skill in the corpus addresses. A composable experiment that runs the multi-mission compressibility pipeline below on the same PSP + THEMIS + MAVEN intervals and compares results to (a) the inventory-attributed Cuesta 2022 numbers and (b) the resolved Andrés 2021 numbers would force the dispute to a verdict, while delivering a reproducible multi-mission compressibility table either way.
- **Tension:** Andrés et al. 2021 (the paper actually at the inventory's DOI) reports the *compressible cascade rate* via an exact isothermal-MHD framework — a *third-order* statistic; the inventory-paraphrased "Cuesta 2022" scope is the *spectral / second-order* compressibility radial evolution. These are distinct observables — third-order cascade-rate trends and second-order PSD-compressibility trends do not necessarily co-vary. If the corpus needs both, the resolved entries should sit as *two* paper-skills rather than one disputed entry.
- **Hypothesis:** the radial trend in compressibility / density-PSD slope between 0.17 (PSP) and 1.5 au (MAVEN) is *dominated* by stream-class mixing rather than by intrinsic radial evolution — the population of clean MAVEN upstream intervals is biased toward slow streams, while PSP samples a more mixed population. Testable by stratifying the per-mission compressibility metric by V_sw and by Alfvénicity classes before binning by r.
- **Minimal_experiment:** on three matched intervals — one PSP E1 near-perihelion, one THEMIS slow-stream at 1 au, one MAVEN upstream segment at 1.5 au — compute the density-PSD slope and the magnetic-compressibility C(f) with identical bandwidth and report the (slope, C) pair per interval. This is the smallest reproducible "radial trend" test and does not depend on the identifier dispute.
- **Composable experiment:** join the per-mission (slope_n_psd, C_n, r) table with [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] SO RPW-derived density statistics at ~0.5 au; the four-mission overlay (PSP, SO, THEMIS, MAVEN) would deliver the first cross-instrument density-turbulence radial-evolution reference from 0.17 to 1.5 au — useful regardless of which Cuesta-vs-Andrés-vs-other paper the curator settles on.

## Relation to HelioSI harness + skills + MCPs

- **Parent skill**: HelioSI `solar-wind-turbulence` (compressible-evolution branch) + multi-mission infrastructure.
- **Sibling paper-skills**: [[telloni-2021-psp-solo-radial-alignment-turbulence]] (Lagrangian conjunction case), [[telloni-2025-psp-solo-radial-alignment-2022-december]] (follow-up alignment), [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] (incompressible / magnetic spectral radial evolution), [[carbone-2021-electron-density-turbulence-ion-cyclotron-waves]] (density spectra at ~0.5 au from SO).
- **MCPs (proposed contracts)**: `psp-data-mcp`, `themis-data-mcp`, `maven-data-mcp`, `cdflib` / PDS readers.
- **Harness contract**: exports per-mission per-interval (slope_n_psd, C_n, r_au); HelioSI roll-up consumes it as the compressibility radial-evolution row.

## References

- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` §1.10 (lists DOI 10.3847/1538-4357/ac0af5 under "Cuesta et al. 2022" — attribution dispute, see banner).
- DOI 10.3847/1538-4357/ac0af5 resolves (verified 2026-05-19) to **Andrés, N. et al. 2021**, ApJ 919, *"The Evolution of Compressible Solar Wind Turbulence in the Inner Heliosphere: PSP, THEMIS, and MAVEN Observations"* — [10.3847/1538-4357/ac0af5](https://doi.org/10.3847/1538-4357/ac0af5).
- Whether a distinct Cuesta-led 2022 paper at a different DOI exists is TODO_verify by a curator ADS search; no canonical Cuesta identifier is asserted by this entry.
- Matthaeus & Goldstein (1982) — early solar-wind compressibility (foundational, not from inventory).
