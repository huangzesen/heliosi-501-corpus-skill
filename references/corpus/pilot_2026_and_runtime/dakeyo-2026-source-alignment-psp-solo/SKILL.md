# dakeyo-2026-source-alignment-psp-solo

## When to use this paper-skill

Invoke when a HelioSI workflow needs to follow *the same solar wind parcel*
between PSP and Solar Orbiter (SO), or more generally between any two inner-
heliosphere spacecraft, to study radial evolution of plasma and field
properties. Typical triggers:

- The user asks "did this PSP stream evolve into the SO stream a few days
  later?"
- A reasoning agent needs to test radial-acceleration claims (e.g.
  acceleration continuing beyond ~15 R_s) using a properly aligned pair of
  in-situ intervals.
- Building a `psp-so-conjunction-finder` skill that scores candidate
  intervals.

Do not invoke for purely remote-sensing source mapping (use a PFSS skill);
this paper-skill assumes one already has in-situ time series at both
spacecraft.

## Paper identity and claim boundary

- **Title:** On the Radial Evolution of the Solar Wind: The Source
  Alignment Method Applied to Parker Solar Probe and Solar Orbiter
  Observations
- **Authors:** J.-B. Dakeyo, T. Ervin, S. D. Bale, P. Démoulin, N. Sioulas,
  V. Réville, et al. (13 total)
- **arXiv:** 2605.01511 (v1, 2026-05-02)
- **Journal:** A&A (submitted) / ApJ — TODO verify final venue
- **Claim boundary:** The paper refines prior radial-/Parker-spiral
  alignment techniques into an explicit *source alignment method*
  applicable to PSP × SO. It argues that the same wind parcel can undergo
  significant acceleration even beyond ~15 R_s, the primary acceleration
  region. The method itself is the deliverable; the radial-acceleration
  claim is the headline application.

## Scientific or methodological claim to operationalize

> Given near-simultaneous PSP and SO in-situ intervals, the source
> alignment method maps both spacecraft footpoints back to a common solar
> source using magnetic-footpoint mapping + ballistic + Parker-spiral
> propagation, and identifies time-shifted PSP/SO sub-intervals that
> sampled the same plasma parcel. The matched pair can then be differenced
> to estimate radial evolution of bulk speed, density, temperature, and
> Alfvénicity.

A HelioSI skill operationalizes this by emitting, for a candidate window:
`(PSP_subinterval, SO_subinterval, alignment_score, Δv, Δn, Δσc, ...)`.

## Required data / instruments / code / archives

- **PSP:** SWEAP (SPC / SPAN-I) bulk moments; FIELDS MAG RTN.
- **SO:** SWA-PAS bulk moments; MAG RTN.
- **Solar context for footpoint mapping:** ADAPT / HMI synoptic maps for
  PFSS extrapolation; ENLIL or WSA only if needed for downstream
  comparison.
- **Coordinate / ephemeris tools:** SPICE kernels for PSP and SO.
- **Archives:** NASA CDAWeb (PSP); SOAR (SO); GONG/ADAPT for synoptic
  maps; JPL NAIF for SPICE.
- **Code:** any of the established footpoint-mapping toolchains, e.g.
  `pfsspy`, `sunpy`, or the Bale-group internal mapper. TODO verify the
  exact tool used by the authors.

## Algorithm / workflow steps

1. **Identify candidate window.** Pick a date range where PSP and SO are
   approximately radially aligned (within a few degrees in HGI longitude)
   or where ballistic propagation predicts an overlap.
2. **Footpoint mapping at each spacecraft.** Use the spacecraft ephemeris
   to project to source surface via ballistic back-tracing, then onto the
   photosphere via PFSS.
3. **Source-region matching.** Identify a common source region (e.g. a
   coronal hole boundary). If footpoints differ by more than a tolerance,
   reject.
4. **Parker-spiral propagation between spacecraft.** Compute the predicted
   arrival time at SO of the PSP-observed parcel using locally measured
   bulk speed and a Parker spiral.
5. **Align sub-intervals.** Cross-correlate PSP and SO time series shifted
   by the predicted transit time; pick the best-aligned sub-interval.
6. **Compute radial-evolution diagnostics:** Δv, Δn, ΔT, change in cross-
   helicity σ_c, residual energy σ_R, spectral index of trace power
   spectrum.
7. **Report quality flags:** longitudinal separation, source-region
   overlap, alignment confidence.

## Minimal executable benchmark or validation target

A HelioSI benchmark version of this skill should:

- Reproduce at least one matched PSP × SO pair from the paper's interval
  list (TODO verify intervals from full text).
- Recover the paper's reported radial-acceleration trend (Δv > 0 above
  ~15 R_s, sign and order of magnitude consistent with the paper).
- Pass criterion: matched-interval Δv within ±20% of the published value
  for a named conjunction.

## Known pitfalls / failure modes

- **PFSS source-surface height.** The 2.5 R_s convention is not universal;
  the choice biases footpoint location. Report the value used.
- **Ballistic vs. Parker-spiral propagation.** The choice changes the
  predicted SO arrival time by hours; document and sweep.
- **Stream-interaction regions (SIRs).** A parcel that crosses an SIR
  between PSP and SO is not the same parcel by the time it arrives — the
  matching will silently fail.
- **Cross-helicity sign convention.** Different communities define σ_c
  with opposite signs; standardize in the skill output.
- **Coordinate frame.** Mixing RTN at PSP and SRF at SO without rotation
  produces spurious differences.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2605.01511 as an Anthropic-
style Skill loadable by the HelioSI runtime:

| Paper element | Agent-native form |
|---|---|
| Claim — "PSP × SO source alignment recovers same-parcel evolution; significant acceleration above ~15 R_s" | **Verifiable task:** `align_psp_so(window) -> {PSP_sub, SO_sub, alignment_score, Δv, Δn, Δσc}` |
| Methods / equations — magnetic-footpoint mapping + ballistic + Parker-spiral propagation + cross-correlation | **Executable workflow:** §"Algorithm / workflow steps" 1–7 with PFSS source-surface radius, propagation mode, and SIR-rejection rule as explicit parameters |
| Data / instruments / code — PSP SWEAP+FIELDS, SO SWA-PAS+MAG, ADAPT/HMI, SPICE | **MCP / tool contracts:** `cdaweb-mcp.get_psp_*`, `soar-mcp.get_so_*`, `pfsspy-mcp.extrapolate(...)`, `spice-mcp.get_ephemeris(...)` |
| Caveats / failure modes — PFSS height choice; ballistic vs spiral; SIR contamination; sign convention; frame mixing | **Skill memory:** §"Known pitfalls / failure modes" — runtime enforces single sign convention and rejects SIR-spanning windows |
| Figures / results — matched-pair time-series overlays + radial-evolution table | **Benchmark artifacts:** matched-pair PNG, `metrics.json` (`Δv, Δn, ΔT, Δσc`), quality-flag JSON |

The Skill compiles the source-alignment *methodology* — the paper's
deliverable in its own framing — directly into a callable HelioSI tool.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** dispatches a `psp-so-conjunction` sub-graph for radial-
  evolution case studies.
- **Skills it composes with:**
  - [[psp-sweap-bulk-loader]] — TODO create
  - [[so-swa-bulk-loader]] — TODO create
  - [[pfss-footpoint-mapper]] — TODO create
  - [[parker-spiral-propagator]] — TODO create
- **MCPs it would use:** `cdaweb-mcp`, `soar-mcp`, `pfsspy-mcp`,
  `spice-mcp` for ephemerides.
- **HelioSI manuscript role:** lead candidate for the Figure-4 panel on
  "literature-grounded multi-spacecraft radial evolution" — the alignment
  method is exactly the kind of executable methodology HelioSI is designed
  to make first-class.

## References

- Dakeyo, J.-B. et al. (2026). arXiv:2605.01511.
- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.3; `psp_analysis_2020_2026.md` entry #3.
