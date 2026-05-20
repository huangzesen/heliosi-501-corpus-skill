---
name: muller-2020-solar-orbiter-mission-overview
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# muller-2020-solar-orbiter-mission-overview

## When to use this paper-skill

Invoke when a HelioSI workflow needs **Solar Orbiter mission-overview
context** — payload inventory (10 instruments), orbit geometry (decreasing
perihelion to ~ 0.28 au, increasing heliographic latitude up to ~ 33°),
Venus gravity assists, operational mission phases (cruise, nominal,
extended), and the SOAR data archive. Typical triggers:

- An agent must resolve a UTC into a Solar Orbiter orbit / latitude /
  remote-sensing window.
- The user asks "which Solar Orbiter instruments are operating at this
  perihelion?" or "where do I get SO data?"
- A radial-evolution / latitude-dependence workflow
  (e.g. [[dakeyo-2026-source-alignment-psp-solo]]) requires SO ephemeris
  with explicit coordinate frame and SPICE kernel version.
- A PSP × SO conjunction workflow needs the SO instrument-mode schedule.

Do NOT invoke this skill when:

- The question concerns a single SO instrument's calibration — use the
  matching instrument paper-skill (e.g.
  [[horbury-2020-solo-mag-vector-magnetometer]],
  [[owen-2020-solo-swa-plasma-suite]],
  [[sinjan-2026-solo-phi-hrt-stray-light-calibration]]).
- The question is about PSP — see
  [[fox-2016-psp-mission-design-orbit-encounters]].

## Paper identity and claim boundary

- **Title:** The Solar Orbiter Mission — Science Overview
- **First author:** Daniel Müller
- **Authors:** 35-author paper: D. Müller, O. C. St. Cyr, I. Zouganelis,
  H. R. Gilbert, R. Marsden, T. Nieves-Chinchilla, E. Antonucci,
  F. Auchère, D. Berghmans, T. S. Horbury, R. A. Howard, S. Krucker,
  M. Maksimovic, C. J. Owen, P. Rochus, J. Rodriguez-Pacheco, M. Romoli,
  S. K. Solanki, R. Bruno, M. Carlsson, A. Fludra, L. Harra,
  D. M. Hassler, S. Livi, P. Louarn, H. Peter, U. Schühle, L. Teriaca,
  J. C. del Toro Iniesta, R. F. Wimmer-Schweingruber, E. Marsch,
  M. Velli, A. De Groof, A. Walsh, D. Williams — full 35-author list
  verified via api.crossref.org on 2026-05-19.
- **Year:** 2020 (online 2020-09-30)
- **Venue:** *Astronomy & Astrophysics* 642, A1 (Solar Orbiter
  special issue)
- **DOI:** 10.1051/0004-6361/202038467 — verified via Crossref on
  2026-05-19.
- **ADS:** 2020A&A...642A...1M (derived from journal coordinates; not
  fetched directly).
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes the mission **as planned/launched in 2020**:
  payload, orbit ladder, observation windows, science objectives, archive
  plan. Operational deviations are tracked in mission-status documents.

## Scientific or methodological claim to operationalize

> Solar Orbiter combines **in-situ instruments** (MAG, SWA, RPW, EPD) with
> **remote-sensing instruments** (EUI, SPICE, PHI, METIS, SoloHI, STIX) on
> an orbit that progressively reaches ~ 0.28 au and ~ 33° heliographic
> latitude after a series of Venus gravity assists. Remote-sensing is
> active in a small number of **Remote Sensing Windows (RSWs)** per orbit,
> while in-situ runs continuously. The SO data archive (SOAR) is the
> authoritative source.

A HelioSI skill operationalizes this by: given a UTC, return
`{orbit_id, perihelion_UTC, r_au, hgi_lat_deg, hgi_lon_deg, in_RSW,
mission_phase, frame, spice_kernel_id}` and the matching SOAR product
pattern for each requested instrument.

## Required data / instruments / code / archives

- **Solar Orbiter SPICE kernels** (SPK, CK, FK, SCLK) — NAIF / ESA.
- **`spiceypy`**, **`pyspedas.solar_orbiter`**, **`sunpy`** helpers.
- **SOAR (Solar Orbiter Archive):** https://soar.esac.esa.int/soar (TODO
  verify URL with primary source).
- **Instruments:** 10 payload items —
  - In-situ: MAG, SWA (EAS, PAS, HIS), RPW, EPD (STEP, EPT, SIS, HET).
  - Remote-sensing: EUI (FSI + HRI_EUV + HRI_LYA), SPICE, PHI (HRT + FDT),
    METIS, SoloHI, STIX.

## Algorithm / workflow steps

1. **Resolve orbit / phase** from SPICE: phase ∈ {cruise, nominal,
   extended}; orbit ID by perihelion-pass index.
2. **State vector** at requested UTC (r [au], HGI lat / lon) in declared
   frame.
3. **RSW lookup:** check whether UTC falls in a remote-sensing window —
   only inside RSWs are EUI / SPICE / PHI / METIS / SoloHI / STIX
   nominally taking science data.
4. **In-situ continuity:** confirm in-situ instruments (MAG, SWA, RPW,
   EPD) are nominal continuously (subject to gaps).
5. **SOAR product pattern:** for each requested instrument, return the
   product naming pattern (TODO compile actual patterns from primary
   source / SOAR documentation).
6. **Persist contract** with SPICE kernel version, frame, mission phase,
   and RSW flag.

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that, for UTC = "2022-03-26T12:00", returns r ≈ 0.32 au,
HGI lat ≈ 0° (TODO verify exact value), and identifies the orbit /
mission-phase consistent with the SO published encounter calendar.

## Known pitfalls / failure modes

- **RSW vs in-situ confusion.** Remote-sensing data exist only within
  RSWs; outside RSWs only in-situ products are nominal. Workflow code that
  assumes EUI / SPICE coverage outside RSWs will fail silently.
- **Frame mismatch.** SO uses HGI / HCI / RTN / spacecraft-body frames;
  always declare.
- **Kernel version drift.** Reconstructed kernels are re-released; pin
  hash for reproducibility.
- **Mission phase boundaries.** Cruise → nominal phase transition (late
  2021) and nominal → extended (2026; TODO verify exact date) change the
  default operations cadence — be careful with intervals straddling
  boundaries.
- **VGA epochs.** Around VGAs orbit changes substantially; do not
  interpolate state vectors across.
- **SOAR rate limits.** Large bulk pulls may be throttled; structure
  requests around RSWs.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — payload inventory + orbit ladder + RSW operations | **Verifiable task:** `so_orbit(utc) -> JSON` + RSW gate |
| Methods — SPICE ephemeris, RSW lookup, instrument-mode resolution | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — 10-instrument payload via SOAR | **MCP / tool contracts:** harness fallback (`spiceypy`, SOAR REST) |
| Caveats — RSW gating, frames, kernel drift, phase boundaries | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — orbit diagram (Fig 2) | **Benchmark artifacts:** orbit-encounter calendar JSON |

## Claim boundary

**In scope.** Solar Orbiter mission **as planned/launched in 2020** —
payload list, orbit ladder, RSW concept, archive plan. The skill resolves
orbit / instrument-mode queries against SPICE kernels and the published
operations plan.

**Out of scope — do NOT generalize beyond:**

- Do not assert single-instrument science contracts (use instrument
  paper-skills).
- Do not claim on-orbit deviations from the launch plan without citing
  later mission-status sources.
- Do not infer PSP encounter contracts from this paper.

## Links

- DOI: https://doi.org/10.1051/0004-6361/202038467 — verified via Crossref
  on 2026-05-19.
- arXiv: n/a.
- ADS: 2020A&A...642A...1M — derived from journal coordinates
  (A&A 642, A1); not directly fetched.
- Code: `spiceypy`, `pyspedas.solar_orbiter`, SOAR REST API.
- Data: ESA Solar Orbiter Archive (SOAR), https://soar.esac.esa.int/.

## Research-generation affordances

- **PSP–Solar Orbiter conjunction calendar as a callable contract.**
  Build a queryable per-encounter table of Solar Orbiter perihelia,
  inferior conjunctions, and quadrature windows with PSP; this is the
  structural prerequisite for any joint inner-heliosphere science and
  is currently rebuilt ad-hoc per paper.
- **Cruise-vs-nominal-phase data-availability fingerprint.** Several
  instruments have different L2/L3 cadence floors in cruise vs nominal
  vs extended phase; publishing the per-instrument availability map as
  a single contract would prevent silent under-sampling in downstream
  workflows.
- **Remote-sensing window optimisation.** Solar Orbiter's high-latitude
  perihelia are limited; pre-computing the optimal remote-sensing
  window for a given heliographic latitude / longitude target turns a
  one-off planning exercise into a reusable agent capability.

## Skill graph → depends_on

- `[[horbury-2020-solo-mag-vector-magnetometer]]` — paired MAG contract.
- `[[owen-2020-solo-swa-plasma-suite]]` — paired SWA contract.
- `[[sinjan-2026-solo-phi-hrt-stray-light-calibration]]` — PHI calibration
  context.
- `[[damicis-2025-solo-swa-alfvenic-streams-validation]]` — applied SWA
  validation workflow.

## References

- Müller et al. (2020), *Astronomy & Astrophysics*, 642, A1 —
  not-in-local-inventory; bibliographic fields TODO verify with primary
  source.
