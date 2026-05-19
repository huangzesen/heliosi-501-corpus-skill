# murtas-2026-hcs-reconnection-ion-energization

## When to use this paper-skill

Invoke when a HelioSI workflow needs to model or interpret heavy-ion and
proton energization at heliospheric current sheet (HCS) crossings observed by
Parker Solar Probe (PSP) near the Sun. Typical triggers:

- A PSP encounter dataset (E14+) shows enhanced suprathermal protons or
  heavier ions coincident with an HCS crossing, and the user asks "could
  reconnection have produced these?"
- A skill needs an end-to-end pipeline that couples a large-scale 2D MHD
  reconnection simulation to the Parker transport equation and predicts
  ion-species spectra (spectral index and high-energy cutoff `E_max`) for
  direct comparison with PSP in-situ data.
- A higher-level reasoning agent needs a vetted baseline before exploring
  alternative HCS energization mechanisms (compression, stochastic Fermi,
  turbulent acceleration).

Do not invoke for flare reconnection, magnetotail reconnection, or
laboratory-scale reconnection — those have different geometries, drivers,
and boundary conditions.

## Paper identity and claim boundary

- **Title:** The Role of Magnetic Reconnection in Energizing Protons and
  Heavier Ions at the Heliospheric Current Sheet
- **Authors:** G. Murtas, X. Li, F. Guo, G. Arrò, J. Seo, C. Haggerty
- **arXiv:** 2605.15068 (v1, 2026-05-14)
- **Journal:** ApJ (in press, 2026)
- **Claim boundary:** The paper claims that a *large-scale 2D MHD
  reconnection simulation coupled to the Parker transport equation* produces
  multi-species power-law ion spectra whose spectral index and `E_max` are
  consistent with PSP HCS-crossing observations of protons and heavier ions
  up to tens-to-hundreds of keV/nucleon. It does NOT claim a 3D first-
  principles kinetic derivation, nor that reconnection is the unique
  energization mechanism — only that this coupled-MHD+transport model can
  reproduce the observed spectra under PSP-relevant HCS parameters.

## Scientific or methodological claim to operationalize

The reusable operational claim is the *pipeline*:

> Given a PSP HCS crossing with in-situ ion-spectra, a 2D MHD reconnection
> simulation initialized with the inferred local HCS plasma parameters,
> coupled to the Parker transport equation solved over the simulated
> reconnection geometry, produces species-resolved power-law spectra whose
> spectral index and high-energy cutoff can be compared quantitatively to
> the observed in-situ spectra.

A future HelioSI agent should be able to take a candidate HCS crossing as
input and emit (spectral index per species, `E_max` per species, residual
diagnostics) using this pipeline.

## Required data / instruments / code / archives

- **PSP in-situ ion data** for the candidate HCS crossing:
  - ISʘIS/EPI-Lo and EPI-Hi for suprathermal proton + heavy-ion spectra.
  - SWEAP/SPAN-I for bulk proton parameters (for setting MHD initial
    conditions).
  - FIELDS MAG for `B`, current sheet identification.
  - Source archives: NASA CDAWeb (`PSP_ISOIS-EPILO_*`, `PSP_SWP_SPI_SF00`,
    `PSP_FLD_L2_MAG_RTN`).
- **2D MHD reconnection solver** — TODO verify with full text which code is
  used (candidates from the author group: `Athena++`, `MHD4`/`HOTB`, or a
  custom solver from the Los Alamos / UAH group). Mark as
  `code:TODO_verify_solver`.
- **Parker transport equation solver** — typically a stochastic-differential-
  equation (SDE) Monte Carlo integrator on top of the MHD flow/`B` field.
  TODO verify the specific code release.
- **Heavy-ion composition** — Q/A ratios for H, He, C, O, Fe.

## Algorithm / workflow steps

1. **Identify HCS crossing.** Use FIELDS MAG sector-polarity reversal and
   bulk-flow gradients in SPAN-I to bracket the HCS interval. Record start /
   end timestamps and PSP heliocentric distance.
2. **Extract local MHD initial conditions.** Bulk `n_p`, `T_p`, `|B|`,
   shear angle, and current-sheet half-thickness (from MAG variance
   analysis) at the crossing.
3. **Run 2D MHD reconnection simulation.** Use the initial conditions to
   set up a Harris-like current sheet in a 2D MHD box; let reconnection
   develop self-consistently. Record the time-dependent flow `U(x,y,t)` and
   magnetic field `B(x,y,t)`.
4. **Solve the Parker transport equation** for each ion species using its
   `Q/A`:
   `df/dt = ∇·(κ∇f) − U·∇f + (1/3)(∇·U)(∂f/∂ln p) + Q_source`,
   injecting a thermal seed population at the reconnection inflow.
5. **Extract per-species spectra.** Compute differential intensity vs.
   energy/nucleon for protons and heavy ions; fit power-law slope and
   `E_max`.
6. **Compare to PSP spectra.** Overlay simulated vs. observed spectra on a
   log-log plot; report (spectral index, `E_max`) for each species and the
   residual.

## Minimal executable benchmark or validation target

A HelioSI benchmark version of this skill should:

- Reproduce the paper's Figure ~3 (or equivalent): multi-species power-law
  spectra from the coupled simulation, with a spectral index in the range
  reported by the paper (TODO verify exact value from full text).
- Reproduce `E_max` ordering across species (heavier ions reaching lower
  `E_max/nuc` than protons, but TODO verify direction with full text — the
  abstract is consistent with a Q/A-controlled cutoff but does not state
  the numerical ordering).
- Pass a quantitative tolerance, e.g. `|γ_sim − γ_obs| < 0.3` for the
  proton power-law index on a published PSP HCS crossing.

The benchmark **must** be paper-grounded in the HeurekaBench sense: input =
named PSP interval; expected output = published spectral parameters;
artifact = log-log spectrum figure plus a `metrics.json`.

## Known pitfalls / failure modes

- **2D-MHD geometry under-resolves kinetic effects.** Quantitative agreement
  with kinetic PIC results is not guaranteed; do not over-claim.
- **Initial-condition sensitivity.** Reported spectra depend strongly on the
  current-sheet half-thickness and shear angle. Always include a
  sensitivity sweep.
- **Seed-population assumption.** The Parker equation needs an injection
  spectrum; assuming Maxwellian-thermal vs. supra-thermal seeds can shift
  `E_max` by an order of magnitude.
- **HCS misidentification.** A magnetic-sector reversal driven by a
  switchback or local kink is NOT a true HCS. Cross-check with
  composition (`O7/O6`) and electron strahl-polarity reversal.
- **κ tensor choice.** The diffusion tensor in the Parker equation is often
  a free parameter; document the assumption explicitly per run.

## Compilation into an Anthropic-style agent-native Skill

This SKILL.md is the *compiled form* of arXiv 2605.15068 as an
Anthropic-style Skill: the paper is not consumed as prose but as a
machine-loadable bundle that the HelioSI runtime can dispatch. The
compilation mapping is:

| Paper element | Agent-native form |
|---|---|
| Claim — "MHD reconnection + Parker transport reproduce per-species PSP HCS spectra" | **Verifiable task:** `validate_per_species_spectra(hcs_crossing) -> {γ_species, E_max_species, residual}` |
| Methods / equations — 2D MHD reconnection + Parker transport equation | **Executable workflow:** §"Algorithm / workflow steps" steps 1–6 with `κ`, seed-spectrum, `Q/A` as explicit parameters |
| Data / instruments / code — PSP ISʘIS, SWEAP, FIELDS; MHD solver; SDE integrator | **MCP / tool contracts:** `cdaweb-mcp.get_psp_isois(...)`, `cdaweb-mcp.get_psp_fields_mag(...)`, `hpc-runner-mcp.run_mhd_2d(...)`, `pyspedas-mcp.fit_power_law(...)` |
| Caveats / failure modes — 2D under-resolves kinetic; IC sensitivity; HCS misID | **Skill memory:** §"Known pitfalls / failure modes" persists across runs; each pitfall is a guard the runtime invokes before accepting a result |
| Figures / results — multi-species power-law spectra figure (TODO verify figure ID) | **Benchmark artifacts:** log-log spectrum figure + `metrics.json` (`{γ_species, E_max_species, residual}`) emitted by §"Minimal executable benchmark or validation target" |

HelioSI is the *domain instantiation*; the general-purpose harness loads
this compiled Skill the same way it loads any other.

## Relation to HelioSI harness + skills + MCPs

- **Harness role:** general-purpose orchestrator dispatches a
  "reconnection-driven SEP" sub-graph including this skill, a data-loader
  skill, and a spectrum-fitter skill.
- **Skills it composes with:**
  - [[psp-isois-epi-data-loader]] — TODO create
  - [[psp-fields-mag-hcs-identifier]] — TODO create
  - [[parker-transport-sde-solver]] — TODO create
- **MCPs it would use:** a `cdaweb-mcp` for PSP archive access; an
  `hpc-runner-mcp` for the MHD simulation step; a `pyspedas-mcp` for the
  ion-spectrum fitting.
- **HelioSI manuscript role:** candidate end-to-end case study for the
  "reconnection-driven SEP at PSP" panel in Figure 4. Cleanly fits the
  literature → simulation → in-situ comparison pattern that 2026 reviewers
  expect.

## References

- Murtas, G., Li, X., Guo, F., Arrò, G., Seo, J., Haggerty, C. (2026).
  arXiv:2605.15068.
- Parker, E. N. (1965). Planet. Space Sci. 13, 9. (transport equation
  foundation)
- Inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §2.1; `psp_analysis_2020_2026.md` entry #1.
