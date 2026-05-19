---
name: damicis-2025-solo-swa-alfvenic-streams-validation
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# damicis-2025-solo-swa-alfvenic-streams-validation

## When to use this paper-skill

Invoke when a HelioSI workflow needs **a worked example of using the full
SO/SWA plasma suite (PAS + EAS + HIS) together with SO/MAG** to classify
solar-wind intervals into fast / Alfvénic-slow / moderate-fast and link
each to a coronal source. The D'Amicis et al. 2025 paper exercises the
SWA suite end-to-end on September 2022 Solar Orbiter streams.

Typical triggers:

- An agent must demonstrate SWA's joint utility (proton VDF anisotropies +
  electron strahl + heavy-ion charge states + magnetic spectra) on a
  single interval.
- The user asks "how do you distinguish Alfvénic-slow wind from fast wind
  on SO?" — this skill encodes the operational checklist.
- A backmapping / PFSS workflow needs the source-region classification
  paired with in-situ Alfvénicity diagnostics.

Do NOT invoke this skill when:

- The interval is outside September 2022 and the user wants numerical
  comparison — apply method, not numerical conclusions.
- The question is about instrument design — use
  [[owen-2020-solo-swa-plasma-suite]],
  [[horbury-2020-solo-mag-vector-magnetometer]].

## Paper identity and claim boundary

- **Title:** Alfvénic solar wind intervals observed by Solar Orbiter —
  Exploiting the capability of the SWA plasma suite and source region
  investigation
- **First author:** R. D'Amicis
- **Authors:** R. D'Amicis, J. M. Raines, S. Benella, M. Velli, O. Panasenco,
  ("+ co-authors per inventory — TODO complete full list with full text")
- **Year:** 2025 (published 2025-12-23; inventory)
- **Venue:** TODO_verify_with_full_text (likely Astronomy & Astrophysics)
- **DOI:** TODO_verify_with_full_text
- **arXiv:** 2512.20098 (in local inventory
  `theme_solar_orbiter.json`).
- **Claim boundary:** Bounded to **Solar Orbiter intervals in September
  2022** — one fast (F), three Alfvénic slow (AS1, AS2, AS3), and one
  moderate-fast (FH) stream. Source-region attributions are specific:
  fast = large coronal hole; AS1 = pseudostreamer with high expansion
  factor; AS2/AS3/FH = negative-polarity coronal hole crossed by a
  dissipating pseudostreamer.

## Scientific or methodological claim to operationalize

> Combining **SWA PAS proton VDFs** (anisotropies + field-aligned beams),
> **SWA EAS electron pitch-angle distributions** (strahl), **SWA HIS heavy-
> ion charge-state ratios** (O, C), and **SO/MAG magnetic and velocity
> spectra**, one can identify Alfvénic streams (fast or slow) on Solar
> Orbiter and link each to its coronal source via **PFSS extrapolation +
> ballistic backmapping**. The simple fast/slow speed classification is
> inadequate; Alfvénicity-vs-source is the operational discriminator.

A HelioSI skill operationalizes this by: given a Solar Orbiter interval,
output the *stream-type classification* (fast | Alfvénic-slow |
moderate-fast | non-Alfvénic-slow) and the *source-region attribution*
(coronal hole | pseudostreamer | mixed).

## Required data / instruments / code / archives

- **SO/MAG L2** (RTN) — magnetic spectra, |B|, σ_c, σ_r
  ([[horbury-2020-solo-mag-vector-magnetometer]]).
- **SO/SWA PAS L2** — proton moments, VDFs (anisotropy + beam)
  ([[owen-2020-solo-swa-plasma-suite]]).
- **SO/SWA EAS L2** — electron PADs (strahl identification)
  ([[owen-2020-solo-swa-plasma-suite]]).
- **SO/SWA HIS L2** — charge-state ratios (O7+/O6+; C6+/C5+)
  ([[owen-2020-solo-swa-plasma-suite]]).
- **PFSS toolchain** — `pfsspy` or equivalent (per `pfss-tracing` custom
  skill) over an ADAPT / GONG / HMI synoptic magnetogram.
- **Ballistic backmapping** — Parker-spiral propagator with locally
  measured v_sw.
- **Archives:** ESA SOAR; JSOC / GONG for magnetograms.

## Algorithm / workflow steps

1. **Pick the interval list** (the paper analyzes 5 streams in Sept 2022:
   F, AS1, AS2, AS3, FH).
2. **Load SO/MAG + SWA-PAS + SWA-EAS + SWA-HIS L2** for each stream.
3. **Compute magnetic + velocity spectra**; estimate **Alfvénicity** via
   normalized cross helicity σ_c and Alfvén ratio r_A.
4. **Inspect PAS VDFs** for anisotropies and field-aligned beams.
5. **Inspect EAS PADs** for strahl population.
6. **Inspect HIS charge-state ratios** — low ratios → fast/coronal-hole
   origin; high ratios → slow / streamer origin.
7. **Run PFSS + ballistic backmapping** to identify the photospheric
   footpoint and source-region type.
8. **Synthesize classification:** fast (high σ_c, low charge state, strong
   strahl, coronal hole); Alfvénic slow (high σ_c, *higher* charge state,
   pseudostreamer / mixed source); etc.

## Minimal executable benchmark or validation target

- **Claim:** All five named September-2022 streams have the classification
  + source listed above; charge-state ratios separate F from AS1–AS3.
- **Metric:** Stream-by-stream classification + source attribution.
- **Tolerance:** Reproduce the paper's 5-of-5 classifications and source
  attributions.
- **Reference figure:** TODO identify figure numbers in D'Amicis+ 2025
  full text (inventory abstract identifies streams + sources but not
  figure indices).

## Known pitfalls / failure modes

- **HIS cadence.** Heavy-ion composition cadence is minutes; classification
  thresholds must be applied at HIS cadence, not PAS cadence.
- **Pseudostreamer source attribution.** Pseudostreamer footpoints can lie
  in narrow open-field corridors; PFSS source-surface height and
  magnetogram choice change attribution. Always document.
- **Backmapping uncertainty.** Ballistic propagation neglects acceleration
  along the streamline; corrections matter near pseudostreamers with
  strong expansion factors.
- **Speed-only classification is wrong.** Slow Alfvénic intervals can look
  like fast wind by Alfvénicity alone but have slow speeds — do not bin
  by speed first.
- **EAS strahl artifact.** Spacecraft-emitted electrons can mimic a
  pseudo-strahl; cut below spacecraft potential.
- **PFSS instability across magnetograms.** ADAPT / GONG / HMI synoptic
  maps yield different source-region attributions in some streams; sweep
  and report.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — Alfvénicity + composition + PFSS yield source-region attribution | **Verifiable task:** `classify_so_stream(interval) -> {type, source}` |
| Methods — spectra + VDFs + PADs + HIS + PFSS backmap | **Executable workflow:** §"Algorithm / workflow steps" 1–8 |
| Data / instruments — SO/MAG + SWA full suite + synoptic magnetogram | **MCP / tool contracts:** SOAR + JSOC/GONG + PFSS toolchain |
| Caveats — HIS cadence, pseudostreamer attribution, backmapping uncertainty | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — stream classification table + backmap diagram | **Benchmark artifacts:** classification JSON + footpoint overlay PNG |

## Claim boundary

**In scope.** Solar Orbiter **September 2022** intervals: one fast (F),
three Alfvénic-slow (AS1, AS2, AS3), one moderate-fast (FH), with the
specific source-region attributions stated in the paper. The skill encodes
the *method*; the numerical conclusions about these particular intervals
are bounded to that month.

**Out of scope — do NOT generalize beyond:**

- Do not assert Alfvénic-slow wind always originates from pseudostreamers;
  the paper analyzed five streams.
- Do not infer PSP classification rules from this paper; SWA and SWEAP
  are not identical.
- Do not skip PFSS sensitivity tests — the conclusions depend on
  magnetogram + source-surface choices.

## Links

- DOI: TODO_verify_with_full_text.
- arXiv: https://arxiv.org/abs/2512.20098
- ADS: TODO_verify_with_full_text.
- Code: `pfsspy` (community); SWA pipelines.
- Data: ESA SOAR; JSOC / GONG.

## Skill graph → depends_on

- `[[muller-2020-solar-orbiter-mission-overview]]` — mission context.
- `[[horbury-2020-solo-mag-vector-magnetometer]]` — MAG contract.
- `[[owen-2020-solo-swa-plasma-suite]]` — SWA sensor suite contract.
- `[[dakeyo-2026-source-alignment-psp-solo]]` — paired PSP×SO radial-
  evolution skill (in `pilot_2026_and_runtime/`).
- `[[bale-2021-solar-source-switchbacks-magnetic-funnels]]` — PFSS +
  backmapping pattern (PSP analogue).

## References

- D'Amicis et al. (2025), arXiv:2512.20098. Inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_solar_orbiter.json`
  (entry arxiv_id 2512.20098v1).
