---
name: mozer-2026-switchback-nonideal-dissipation
description: Per-entry paper-skill in pilot_2026_and_runtime (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# mozer-2026-switchback-nonideal-dissipation

## When to use this paper-skill

Invoke when a HelioSI workflow needs to discriminate **Ideal-MHD** vs.
**Hall-MHD** dynamics across switchback boundaries observed by Parker Solar
Probe (PSP) inside ~40 R_s, or when the user asks "is dissipation happening
at this switchback?". Typical triggers:

- A switchback catalog interval near 13–40 R_s needs a non-ideal dissipation
  diagnostic.
- A reasoning agent needs an observational baseline to test whether
  switchback boundaries support generalized-Ohm's-law contributions beyond
  `−U×B`.
- Building or validating a `switchback-dissipation-classifier` skill.

Do not invoke for switchback *generation mechanism* questions (interchange
reconnection vs. turbulence-driven) — that requires different diagnostics
and the paper does not claim a generation mechanism.

## Paper identity and claim boundary

- **Title:** Direct Evidence of Non-Ideal Dissipative Dynamics in Solar
  Wind Magnetic Switchbacks
- **Authors:** F. Mozer, O. Agapitov, K.-E. Choi, R. Sydora
- **arXiv:** 2605.14114 (v1, 2026-05-13)
- **Journal:** ApJ (2026)
- **Claim boundary:** The paper uses PSP FIELDS electric-field measurements
  between 13 and 40 solar radii to *directly* compare the measured electric
  field to the `−U×B` ideal-MHD prediction across switchback boundaries.
  Departures consistent with **Hall-MHD physics** are identified. The paper
  does NOT claim a definitive origin location for switchbacks; it settles
  one specific controversy: that switchback dynamics include non-ideal
  components observable in the electric-field signal.

## Scientific or methodological claim to operationalize

> Across switchback boundaries observed by PSP in 13–40 R_s, the measured
> electric field `E_meas` deviates from the ideal-MHD prediction
> `E_ideal = −U × B` in a way that is consistent with Hall-MHD,
> i.e. with a non-negligible `(J × B)/(n_e e)` contribution.

A HelioSI skill operationalizes this by emitting, for any given switchback
boundary: `(|E_meas − E_ideal|, |E_Hall_predicted|, classification ∈
{ideal, Hall-consistent, ambiguous})`.

## Required data / instruments / code / archives

- **PSP FIELDS:**
  - Electric-field DC + AC channels (`PSP_FLD_L2_DFB_DC_*`,
    `PSP_FLD_L2_EFIELD_*`) — TODO verify exact product names used in the
    paper.
  - MAG RTN at matching cadence.
- **PSP SWEAP:**
  - SPC or SPAN-I bulk-velocity moments for `U`.
  - Electron density (or proton density × quasineutrality) for the Hall
    term.
- **Radial-distance constraint:** select intervals with 13 R_s < `r` <
  40 R_s.
- **Switchback catalog:** any of Bale+ 2021, Agapitov+ 2023, or local
  threshold-based detection on `B_R / |B|`.
- **Archives:** NASA CDAWeb, Berkeley PSP FIELDS data center.

## Algorithm / workflow steps

1. **Select switchback boundary candidates** in PSP intervals satisfying
   13 R_s < `r` < 40 R_s.
2. **Co-register** `E`, `B`, `U`, `n_e` to a common cadence; rotate into a
   boundary-normal frame (LMN) from MVA on `B` across the boundary.
3. **Compute ideal-MHD electric field** `E_ideal = −U × B`.
4. **Compute Hall correction** `E_Hall = (J × B) / (n_e e)` using
   `J = ∇ × B / μ_0` (single-spacecraft estimate via Taylor's hypothesis or
   `∂B/∂t` proxy — note the limitation).
5. **Compute residual** `δE = E_meas − E_ideal` along the normal and
   tangential directions.
6. **Classify** the boundary as `ideal` if `|δE| < threshold`, `Hall-
   consistent` if `δE ≈ E_Hall` within a tolerance, otherwise `ambiguous`.
7. **Aggregate statistics** across boundaries to reproduce the paper's
   global claim.

## Minimal executable benchmark or validation target

A HelioSI benchmark version of this skill should:

- Reproduce the paper's residual `|E_meas − E_ideal|` distribution across
  the published switchback set (TODO verify exact set from full text).
- Show a non-zero correlation between `δE` and the Hall prediction
  `E_Hall = (J × B)/(n_e e)` at switchback boundaries, consistent with the
  paper.
- Pass criterion: classification recall of `Hall-consistent` boundaries
  matches paper figure within ±15% (TODO verify with full text).

## Known pitfalls / failure modes

- **Single-spacecraft current estimation.** `J = ∇ × B/μ_0` from one probe
  requires a Taylor-hypothesis assumption; this introduces systematic
  bias and should be reported in uncertainty bars.
- **Antenna effective-length calibration.** FIELDS DC `E`-field requires a
  calibrated effective antenna length; using an uncalibrated value will
  bias `E_meas`.
- **Electron density proxy.** Using proton density for `n_e` is fine in
  quasineutral solar wind but may drift in dense ICME / sheath plasma.
- **Boundary identification ambiguity.** "Switchback boundary" thresholds
  vary across catalogs; cite the chosen threshold and run a sensitivity
  sweep.
- **Aliasing of waves.** High-frequency waves (whistlers, ion-cyclotron)
  can leak into the `E` and `B` budgets — apply consistent bandpass.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2605.14114 as an Anthropic-
style Skill loadable by the HelioSI runtime:

| Paper element | Agent-native form |
|---|---|
| Claim — "non-ideal `E`-field residuals at switchback boundaries are consistent with Hall-MHD between 13–40 R_s" | **Verifiable task:** `classify_boundary(interval) -> {ideal, Hall-consistent, ambiguous}` plus residual statistics |
| Methods / equations — `E_ideal = −U×B`, `E_Hall = (J×B)/(n_e e)`, single-spacecraft `J` via Taylor | **Executable workflow:** §"Algorithm / workflow steps" 1–7 with `n_e` source, antenna calibration, and bandpass as explicit parameters |
| Data / instruments / code — PSP FIELDS DC+AC, MAG, SWEAP, density proxy | **MCP / tool contracts:** `cdaweb-mcp.get_psp_fields_efield(...)`, `cdaweb-mcp.get_psp_fields_mag(...)`, `cdaweb-mcp.get_psp_sweap(...)`, optional `pspfields-mcp.l3_calibrated(...)` |
| Caveats / failure modes — Taylor-hypothesis bias; antenna calibration; `n_e` proxy; wave aliasing; threshold choice | **Skill memory:** §"Known pitfalls / failure modes" — runtime checks each guard before emitting a classification |
| Figures / results — boundary-classification + residual distributions | **Benchmark artifacts:** per-boundary `metrics.json`, aggregate distribution PNG, classification-confusion table |

The Skill compiles a *contested* observational claim into a reproducible
classifier; HelioSI invokes it via the same harness it uses for any other
domain skill.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** dispatches a `switchback-dissipation` sub-graph that
  composes data-loader + boundary-finder + `E`-residual + classifier.
- **Skills it composes with:**
  - [[psp-fields-efield-loader]] — TODO create
  - [[switchback-boundary-finder]] — TODO create
  - [[hall-mhd-residual-classifier]] — TODO create
- **MCPs it would use:** `cdaweb-mcp`, `pyspedas-mcp`, optional
  `pspfields-mcp` for L3 calibrated products.
- **HelioSI manuscript role:** secondary case study showing that the
  HelioSI runtime can ingest a *controversial* observational claim, render
  it as an executable diagnostic, and produce a reproducible per-boundary
  classification — directly answering the 2026 reviewer expectation of
  "end-to-end executable verification".

## References

- Mozer, F., Agapitov, O., Choi, K.-E., Sydora, R. (2026).
  arXiv:2605.14114.
- Bale, S. D. et al. (2021), ApJ. (switchback patch catalog)
- Agapitov, O. V. et al. (2023), ApJ. (PSP switchback survey)
- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.2; `psp_analysis_2020_2026.md` entry #2.
