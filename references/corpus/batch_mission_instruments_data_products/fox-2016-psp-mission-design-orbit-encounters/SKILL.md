---
name: fox-2016-psp-mission-design-orbit-encounters
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# fox-2016-psp-mission-design-orbit-encounters

## When to use this paper-skill

Invoke when a HelioSI workflow needs **PSP mission-design context** — orbit
geometry, perihelion progression across encounters (E1–E24+), Venus gravity
assists, encounter-mode definitions, SPICE-kernel naming, and the
science-objective taxonomy that anchors instrument operations. Typical
triggers:

- An agent must convert an interval timestamp into an encounter ID, or
  resolve heliocentric distance / latitude / longitude from a SPICE kernel.
- The user asks "which encounter reached 13.28 R_sun?" or "when is PSP
  perihelion N?".
- A multi-mission / radial-evolution analysis
  (e.g. [[dakeyo-2026-source-alignment-psp-solo]]) needs PSP ephemeris
  with documented coordinate frames.
- A reproduction script needs the ordered VGA schedule and resulting
  perihelion ladder.

Do NOT invoke this skill when:

- The question is about a *specific instrument* — use FIELDS / SWEAP /
  ISʘIS / WISPR paper-skills.
- The question is about Solar Orbiter ephemeris — separate
  ([[muller-2020-solar-orbiter-mission-overview]]).

## Paper identity and claim boundary

- **Title:** The Solar Probe Plus Mission — Humanity's First Visit to Our
  Star
- **First author:** Nicola J. Fox
- **Authors:** N. J. Fox, M. C. Velli, S. D. Bale, R. Decker, A. Driesman,
  R. A. Howard, J. C. Kasper, J. Kinnison, M. Kusterer, D. Lario,
  M. K. Lockwood, D. J. McComas, N. E. Raouafi, A. Szabo, et al.
  ("+ co-authors — TODO verify full list with primary source")
- **Year:** 2016
- **Venue:** Space Science Reviews — *Parker Solar Probe* special issue
- **DOI:** 10.1007/s11214-015-0211-6 (TODO verify with primary source)
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes the mission **as planned at launch**: orbit
  design, VGA cadence, target perihelia (down to 9.86 R_sun by 2024–2025),
  and the science-objective categories that drive operations. On-orbit
  deviations and actual encounter intervals are tabulated in mission status
  reports and later review papers (e.g.
  [[raouafi-2023-psp-four-years-discoveries-review]]).

## Scientific or methodological claim to operationalize

> PSP follows a series of decreasing-perihelion orbits driven by seven Venus
> gravity assists, reaching a final perihelion of ~ 9.86 R_sun. Each orbit
> has an **encounter** segment (heliocentric distance ≲ 0.25 au) during
> which instruments operate in burst mode. The agent contract for PSP
> orbit / encounter resolution is set by this paper, with the SPICE
> ephemeris kernels as the authoritative numerical source.

A HelioSI skill operationalizes this by: given a UTC interval or encounter
ID, return `{encounter, perihelion_UTC, r_au, hgs_lat, hgs_lon, frame,
spice_kernel_id}`.

## Required data / instruments / code / archives

- **SPICE kernels (PSP):** mission-level (`spk`, `ck`, `fk`, `sclk`) — the
  authoritative ephemeris source. Names like `spp_recon_*.bsp` (TODO
  verify naming convention with NAIF / PSP SOC).
- **`spiceypy`:** standard Python binding to CSPICE.
- **`pyspedas.psp` ephemeris loaders:** convenience wrappers.
- **Mission documents:** encounter calendars in PSP SOC operations pages
  (TODO verify URL).

## Algorithm / workflow steps

1. **Time → encounter.** Load PSP SPICE kernels; query position; classify
   as "encounter" (r ≲ 0.25 au, TODO verify exact threshold) or "cruise".
2. **Encounter ID.** Compute closest-approach UTC; bin to the ordinal
   encounter number (E1, E2, …).
3. **State vector.** Return (r [au], heliographic lat/lon, velocity in HCI
   or RTN) with the explicit frame and kernel hash.
4. **VGA schedule.** Provide the list of Venus gravity assists (V1, V2, …
   V7) and their UTC, since each VGA changes the orbit.
5. **Operations mode.** State whether instruments were in encounter (burst)
   or cruise mode for the requested interval — this changes the L2/L3
   product cadence advertised by FIELDS / SWEAP / ISʘIS / WISPR contracts.
6. **Persist contract** including SPICE kernel version (frozen for
   reproducibility).

```python
def psp_ephemeris(utc, frame="HEEQ", kernels="latest"):
    import spiceypy as sp
    sp.furnsh(kernels)
    et = sp.str2et(utc)
    state, _ = sp.spkezr("SPP", et, frame, "NONE", "SUN")
    return {"r_au": state[:3], "v_kms": state[3:], "frame": frame,
            "kernel_version": kernels}
```

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that, given UTC = "2018-11-06T03:27", returns
encounter = E1, perihelion radius ~ 35.7 R_sun (= 0.166 au), and matches
the published encounter table within 1 day for the UTC and 0.5 R_sun for
r. TODO verify exact perihelion radii / UTC list with primary source.

## Known pitfalls / failure modes

- **Frame mismatch.** Mixing HCI / HEEQ / HEE / RTN coordinates silently
  corrupts radial-distance analyses. Always carry the frame in the
  contract.
- **Kernel version drift.** PSP SOC re-releases reconstructed kernels;
  reproductions must pin a kernel hash, not just "latest".
- **Encounter-definition edge cases.** Different papers use slightly
  different encounter-window definitions (r ≲ 0.25 au vs ≲ 0.3 au); always
  cite the choice.
- **VGA epoch reasoning.** During a VGA the orbit changes; analyses that
  straddle a VGA must split.
- **SPICE leap-second / SCLK kernels.** Out-of-date SCLK kernels cause
  millisecond-level time-tag offsets, which matter for high-cadence
  FIELDS bursts.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — mission-design orbit ladder + encounter taxonomy | **Verifiable task:** `psp_ephemeris(utc) -> JSON` + encounter ID |
| Methods — SPICE kernel queries, encounter binning | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — SPICE PSP kernel set | **MCP / tool contracts:** harness fallback (`spiceypy` + NAIF) |
| Caveats — frame / kernel-version / encounter-definition / VGA | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — orbit diagram (Fig 1) | **Benchmark artifacts:** encounter calendar JSON |

## Claim boundary

**In scope.** PSP mission-design **as planned at launch** — orbit ladder,
VGA schedule, encounter definitions, intended observation modes, science-
objective taxonomy. The skill resolves time ↔ encounter ↔ state-vector
queries against SPICE kernels.

**Out of scope — do NOT generalize beyond:**

- Do not assert instrument-specific contracts (use FIELDS / SWEAP / ISʘIS
  / WISPR paper-skills).
- Do not claim on-orbit deviations from plan without citing later mission-
  status sources.
- Do not infer Solar Orbiter ephemeris from this paper.

## Links

- DOI: 10.1007/s11214-015-0211-6 — TODO verify with primary source.
- arXiv: n/a.
- ADS: TODO_verify_with_full_text.
- Code: `spiceypy` (`https://spiceypy.readthedocs.io/`), `pyspedas` PSP
  ephemeris loaders.
- Data: NAIF SPICE PSP kernels; PSP SOC.

## Skill graph → depends_on

- `[[bale-2016-fields-instrument-suite-psp]]` — FIELDS contracts depend on
  encounter / mode.
- `[[kasper-2016-sweap-investigation-psp]]` — same.
- `[[raouafi-2023-psp-four-years-discoveries-review]]` — on-orbit
  encounter outcomes.

## References

- Fox et al. (2016), *Space Science Reviews*; PSP special issue —
  not-in-local-inventory; bibliographic fields TODO verify.
