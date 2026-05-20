---
name: bale-2016-fields-instrument-suite-psp
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# bale-2016-fields-instrument-suite-psp

## When to use this paper-skill

Invoke this skill when a HelioSI workflow needs the **canonical PSP/FIELDS
instrument description** — sensor inventory, antenna/boom geometry,
coordinate-frame conventions, data-product hierarchy, and noise/saturation
caveats. Typical triggers:

- An agent is about to load PSP FIELDS magnetometer (MAG/SCM) or electric-field
  (V1–V5, dV12–dV34) time series and must know which sensor, level, and
  cadence to request.
- The user asks "what is the FIELDS antenna configuration / coordinate frame
  / nominal noise floor?"
- A reproduction script needs to convert between **FIELDS SC frame**,
  **RTN**, and **SPP-spacecraft body frame** for B or E vectors.
- A switchback / wave / interval-segmentation workflow must decide between
  MAG-fluxgate, MAG-SCM, or merged SCaM products
  (see [[pulupa-2020-fields-merged-scm-fluxgate-product]]).

Do NOT invoke this skill when:

- The question is about a **science result** computed from FIELDS (e.g.
  switchback statistics) — those have their own paper-skills.
- The question is about SWEAP, ISʘIS or WISPR — separate instrument skills.

## Paper identity and claim boundary

- **Title:** The FIELDS Instrument Suite for Solar Probe Plus — Measuring the
  Coronal Plasma and Magnetic Field, Plasma Waves and Turbulence, and Radio
  Signatures of Solar Transients
- **First author:** Stuart D. Bale
- **Authors:** 83-author paper: S. D. Bale, K. Goetz, P. R. Harvey,
  P. Turin, J. W. Bonnell, T. Dudok de Wit, R. E. Ergun, R. J. MacDowall,
  M. Pulupa, M. Andre, M. Bolton, J.-L. Bougeret, T. A. Bowen,
  D. Burgess, C. A. Cattell, B. D. G. Chandran, C. C. Chaston, C. H. K.
  Chen, M. K. Choi, J. E. Connerney, S. Cranmer, M. Diaz-Aguado,
  W. Donakowski, J. F. Drake, W. M. Farrell, P. Fergeau, J. Fermin,
  J. Fischer, N. Fox, D. Glaser, M. Goldstein, D. Gordon, E. Hanson,
  S. E. Harris, L. M. Hayes, J. J. Hinze, J. V. Hollweg, T. S. Horbury,
  R. A. Howard, V. Hoxie, G. Jannet, M. Karlsson, J. C. Kasper,
  P. J. Kellogg, M. Kien, J. A. Klimchuk, V. V. Krasnoselskikh,
  S. Krucker, J. J. Lynch, M. Maksimovic, D. M. Malaspina, S. Marker,
  P. Martin, J. Martinez-Oliveros, J. McCauley, D. J. McComas,
  T. McDonald, N. Meyer-Vernet, M. Moncuquet, S. J. Monson, F. S. Mozer,
  S. D. Murphy, J. Odom, R. Oliverson, J. Olson, E. N. Parker,
  D. Pankow, T. Phan, E. Quataert, T. Quinn, S. W. Ruplin, C. Salem,
  D. Seitz, D. A. Sheppard, A. Siy, K. Stevens, D. Summers, A. Szabo,
  M. Timofeeva, A. Vaivads, M. Velli, A. Yehle, D. Werthimer,
  J. R. Wygant — full 83-author list verified via api.crossref.org on
  2026-05-19.
- **Year:** 2016 (online December 2016; SSRv volume 204 issue 1–4)
- **Venue:** *Space Science Reviews* 204, 49–82 — *Parker Solar Probe*
  special issue
- **DOI:** 10.1007/s11214-016-0244-5 — verified via Crossref on
  2026-05-19.
- **ADS:** 2016SSRv..204...49B (derived from journal coordinates; not
  fetched directly).
- **arXiv:** not-in-local-inventory — paper not present in
  `arxiv_papers/*.md`; cited directly from the SSRv-published article.
- **Claim boundary:** This paper describes the **engineering design and
  intended data products** of FIELDS as launched in 2018. It does not
  certify on-orbit performance over Encounters 1–N — encounter-specific
  noise / cross-talk / glitch reports come from later commissioning and
  pipeline papers (e.g. [[pulupa-2020-fields-merged-scm-fluxgate-product]]).

## Scientific or methodological claim to operationalize

> FIELDS provides PSP with two redundant **fluxgate magnetometers (MAGs)**
> on the boom, one **search-coil magnetometer (SCM)** at the boom tip, and
> five **electric-field antennas** (V1–V4 in the heat-shield shadow plane,
> V5 axial), feeding a Digital Fields Board (DFB) and RFS receiver. The
> nominal coordinate conventions, sensor sampling, and Level-1/Level-2
> definitions described in this paper are the **agent's contract** for
> downstream PSP magnetic and electric-field workflows.

A HelioSI skill operationalizes this by: given a PSP encounter / interval,
return the *contract* for FIELDS access — sensor IDs, frames, cadences,
archives, and the named caveats that must propagate into any analysis.

## Required data / instruments / code / archives

Sensors / signals described:

- **MAG (fluxgate):** two units (MAG_i, MAG_o) on boom; nominal vector
  cadence 292.97 Sa/s for Level-2 burst / merged products
  (TODO verify exact value with full text).
- **SCM (search-coil):** 3-axis on boom tip; signal up to ~ 1 MHz.
- **V1–V5 antennas:** four shadow-plane stub antennas (V1–V4, in the heat-
  shield shadow) and one axial whip (V5); differential pairs dV12, dV34
  yield two electric-field components.
- **DFB:** Digital Fields Board producing AC-bandwidth spectra, time-series
  bursts, and cross-spectra.
- **RFS:** Radio Frequency Spectrometer covering ~ 10 kHz – 19.2 MHz.
- **Archives:** NASA SPDF / CDAWeb (`PSP_FLD_L2_*` family), PSP/FIELDS Berkeley
  data center.
- **Coordinate frames:** SC (spacecraft), RTN, SPP body — conversions
  documented in the paper and instrument metadata.

The general-purpose harness (Read, Bash, WebFetch + `cdflib`) is the only
guaranteed retrieval surface; named MCPs (`cdaweb-mcp`) may or may not be
bound at runtime.

## Algorithm / workflow steps (data-contract construction)

1. **Resolve sensor.** Map a science question to a sensor: B vector →
   MAG; B AC/high-freq → SCM; E low-freq DC → dV12, dV34; E AC → DFB; radio
   bursts → RFS.
2. **Resolve level and cadence.** L1 = engineering; L2 = science (the
   default); L3 = derived (e.g. merged SCaM, density from QTN). For a
   turbulence workflow defaulting to L2; for a wave-event workflow possibly
   L2 burst.
3. **Resolve frame.** Default for science = RTN (B and v). SC frame
   required only when checking spacecraft-attitude artefacts or matching
   antenna geometry. Document the frame explicitly in every saved
   intermediate.
4. **Resolve interval and encounter.** Provide encounter ID (E1, E2, …)
   and UTC interval; cross-check with mission ephemeris (see
   [[fox-2016-psp-mission-design-orbit-encounters]]).
5. **Apply known caveats** from §"Known pitfalls / failure modes" before
   any downstream physics (spin tones, glitch flags, gain switches).
6. **Persist the contract** as a small JSON: `{sensor, level, cadence,
   frame, encounter, interval, archive, version, caveats[]}` for
   reproducibility.

```python
# Pseudocode at stub tier; runnable at executable+
def fields_contract(question, encounter, interval, frame="RTN"):
    """Return a JSON contract for PSP/FIELDS access for one task."""
    sensor = pick_sensor(question)                 # MAG | SCM | dV12 | dV34 | RFS
    level, cadence = pick_level_cadence(question)  # e.g. "L2", "1/4 Sa/cyc"
    return {
        "sensor": sensor, "level": level, "cadence": cadence,
        "frame": frame, "encounter": encounter, "interval": interval,
        "archive": "SPDF/CDAWeb", "version": None,
        "caveats": KNOWN_FIELDS_CAVEATS,
    }
```

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that resolves a FIELDS L2 magnetic-field interval into a
valid `(sensor, level, cadence, frame, interval, archive)` tuple, downloads
the matching CDF via `cdflib`/`pyspedas`, and confirms the in-file metadata
matches the contract (e.g. `LBL2_PSP_FLD_L2_MAG_RTN_4_SA_PER_CYC` headers
report RTN + 4 Sa/cyc). TODO verify exact CDF variable names with primary
source.

## Known pitfalls / failure modes

- **Spacecraft spin tone.** Residual spin signatures can leak into MAG
  spectra near ~ 12.5 s spin period in cruise (PSP is not nominally
  spinning at encounter, but maneuver intervals may rotate it). Despin /
  flag.
- **Antenna shadow geometry.** V1–V4 sit in the heat-shield shadow; partial
  illumination near encounter perihelion produces photoelectron-current
  asymmetries that bias DC electric fields. Mask near solar-array
  reconfigurations.
- **Gain switches.** DFB and ADC stages have automatic-gain switching;
  spectra straddling a switch show step artefacts. Drop affected bins.
- **MAG saturation in CME / strong-field encounters.** Default range may
  saturate; check `INSTRUMENT_MODE` metadata.
- **SCM low-frequency rolloff.** SCM transfer function rolls off below
  ~ 10 Hz; do NOT use SCM for inertial-range turbulence — use MAG, or use
  merged SCaM ([[pulupa-2020-fields-merged-scm-fluxgate-product]]).
- **Coordinate-frame mismatch.** Code that mixes SC-frame B with RTN v
  silently corrupts cross-helicity and other Elsässer-frame diagnostics.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — FIELDS sensor inventory + nominal contracts | **Verifiable task:** `fields_contract(question, encounter, interval) -> JSON` |
| Methods — sensor selection, level/frame mapping | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — MAG, SCM, V1–V5, DFB, RFS | **Capability contracts:** retrieval of PSP FIELDS L2 products (MAG, SCM, V1–V5, DFB, RFS) from an SPDF/CDAWeb-class archive, with a guaranteed harness fallback to `cdflib`+SPDF URL. (See Layer 3 for example adapter bindings.) |
| Caveats — spin tone, shadow geometry, gain switches, SCM rolloff | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — instrument block diagram (Fig 1, Fig 2) | **Benchmark artifacts:** contract-JSON + headers-comparison report |

## Claim boundary

**In scope.** Description of the FIELDS instrument **as launched in 2018**,
including sensors, antennas, electronics, intended data products, and
nominal coordinate frames. Any agent using this skill stays inside the
"design and intended product" lane.

**Out of scope — do NOT generalize beyond:**

- Do not assert on-orbit noise levels, glitch rates, or product versions —
  those come from later commissioning / data-pipeline papers.
- Do not infer SWEAP, ISʘIS or WISPR contracts from this paper — separate
  instrument descriptions.
- Do not use this paper to argue physical results (switchback origin,
  cascade rate, etc.) — those have dedicated paper-skills.

## Links

- DOI: https://doi.org/10.1007/s11214-016-0244-5 — verified via Crossref
  on 2026-05-19.
- arXiv: n/a (Space Science Reviews; preprint not located in inventory).
- ADS: 2016SSRv..204...49B — derived from journal coordinates
  (SSRv 204, 49–82); not directly fetched.
- Code: n/a (instrument paper).
- Data: NASA SPDF / CDAWeb — `PSP_FLD_L2_*` family; UCB FIELDS data
  center (https://fields.ssl.berkeley.edu/).

## Research-generation affordances

- **Per-encounter caveat-propagation audit.** Build a table of which of
  the six pitfalls (spin tone, antenna-shadow asymmetry, gain
  switching, MAG saturation, SCM rolloff, frame-mismatch) actually
  manifested in each encounter's FIELDS L2 stream. Many downstream
  papers reuse the contract without re-checking the per-encounter
  flag rates; the table reveals where this is safe.
- **Sensor-selection rubric as a teachable contract.** The
  question-to-sensor mapping (B vector → MAG, B AC → SCM, E low-freq →
  dV12/dV34, E AC → DFB, radio bursts → RFS) is informally encoded
  across PSP/FIELDS papers; explicitly publishing it as an
  agent-callable contract would reduce sensor-misuse failures in
  community code.
- **Cross-validation against Solar Orbiter MAG.** When PSP and Solar
  Orbiter share Sun–spacecraft alignment windows, the FIELDS
  MAG-vs-Horbury-MAG comparison (see
  [[horbury-2020-solo-mag-vector-magnetometer]]) is a load-bearing
  cross-instrument calibration anchor; the FIELDS contract built here
  is its structural prerequisite.
- **Antenna-shadow geometry impact on DC-E science.** The shadow-plane
  V1–V4 geometry is rarely modelled explicitly outside FIELDS-team
  papers; a published per-encounter shadow-asymmetry diagnostic would
  bound the systematic on any DC-E-driven inference.

## Skill graph → depends_on

- `[[pulupa-2020-fields-merged-scm-fluxgate-product]]` — concrete L3 merged
  product built on this instrument description.
- `[[fox-2016-psp-mission-design-orbit-encounters]]` — encounter
  identification and ephemeris context.
- `[[kasper-2016-sweap-investigation-psp]]` — paired plasma suite; FIELDS
  alone is insufficient for cascade / Alfvénicity diagnostics.

If a downstream task asks for a SWEAP or ISʘIS contract, refuse and
redirect to the matching instrument skill.

## References

- Bale et al. (2016), *Space Science Reviews*; PSP special issue —
  not-in-local-inventory; identity / DOI **TODO verify with full text**.
- Local inventory cross-check: `sioulas-reproduction/results/arxiv_papers/`
  contains no entry for this paper, so all bibliographic fields are
  flagged for verification.
