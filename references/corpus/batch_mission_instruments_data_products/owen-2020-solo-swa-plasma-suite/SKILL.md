---
name: owen-2020-solo-swa-plasma-suite
description: Per-entry paper-skill in batch_mission_instruments_data_products (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# owen-2020-solo-swa-plasma-suite

## When to use this paper-skill

Invoke when a HelioSI workflow needs the **canonical SO/SWA Solar Wind
Analyser plasma-suite description** — the three sensors (EAS, PAS, HIS),
their species/energy coverage, intended L2 product hierarchy
(moments + VDFs), and the coordinate / spacecraft-illumination caveats.
Typical triggers:

- An agent must load SO proton moments, ion VDFs, electron VDFs, or
  heavy-ion charge-state composition.
- The user asks "what is the EAS energy range?" or "are heavy-ion charge
  states from SWA-HIS available continuously?"
- An Alfvénicity / source-region workflow on SO
  ([[damicis-2025-solo-swa-alfvenic-streams-validation]]) needs SWA
  contracts paired with SO/MAG
  ([[horbury-2020-solo-mag-vector-magnetometer]]).

Do NOT invoke this skill when:

- The question is about energetic particles (> ~ 30 keV) — that is EPD.
- The question is about radio / Langmuir-probe density — that is RPW.

## Paper identity and claim boundary

- **Title:** The Solar Orbiter Solar Wind Analyser (SWA) Suite
- **First author:** Christopher J. Owen
- **Authors:** ~130-author paper led by C. J. Owen, R. Bruno, S. Livi,
  P. Louarn, K. Al Janabi, F. Allegrini, C. Amoros, R. Baruah,
  A. Barthe, M. Berthomier, S. Bordon, C. Brockley-Blatt,
  C. Brysbaert, G. Capuano, M. Collier, R. DeMarco, A. Fedorov,
  J. Ford, V. Fortunato, I. Fratter, A. B. Galvin, B. Hancock,
  D. Heirtzler, D. Kataria, L. Kistler, S. T. Lepri, G. Lewis,
  C. Loeffler, W. Marty, R. Mathon, A. Mayall, G. Mele, K. Ogasawara,
  M. Orlandi, A. Pacros, E. Penou, S. Persyn, M. Petiot, M. Phillips,
  L. Přech, J. M. Raines, M. Reden, A. P. Rouillard, A. Rousseau,
  J. Rubiella, H. Seran, A. Spencer, J. W. Thomas, J. Trevino,
  D. Verscharen, P. Wurz et al. (full author list, ~130 names,
  verified via api.crossref.org on 2026-05-19).
- **Year:** 2020 (online 2020-09-30)
- **Venue:** *Astronomy & Astrophysics* 642, A16 (Solar Orbiter
  special issue)
- **DOI:** 10.1051/0004-6361/201937259 — verified via Crossref on
  2026-05-19.
- **ADS:** 2020A&A...642A..16O (derived from journal coordinates; not
  fetched directly).
- **arXiv:** not-in-local-inventory.
- **Claim boundary:** Describes SWA **as designed and commissioned in
  2020**. Charge-state composition (HIS) was approaching nominal at
  publication; spacecraft-emitted-electron contamination on EAS is
  documented in later modelling papers (see
  [[stverak-2026-solo-swa-eas-spacecraft-electron-contamination]] — TODO
  add to corpus when needed).

## Scientific or methodological claim to operationalize

> SWA is a three-sensor suite measuring the solar-wind ion and electron
> populations:
> - **PAS (Proton-Alpha Sensor):** top-hat ESA for protons and alphas;
>   2D/3D VDFs and moments; FoV centred on the Sun-ward direction.
> - **EAS (Electron Analyser System):** two top-hat ESAs giving ~ 4π
>   electron VDFs for core / strahl / halo populations.
> - **HIS (Heavy-Ion Sensor):** TOF + energy spectrometer for heavy-ion
>   charge-state composition (C, O, Fe, …).
>
> L2 products include moments (proton + alpha, electron) and VDFs. The
> agent contract for SO plasma access is set by this paper.

A HelioSI skill operationalizes this by: given an interval and science
question, return the *plasma contract* (sensor, product, cadence, frame,
species).

## Required data / instruments / code / archives

- **SO/SWA PAS L2:** proton/α moments (`solo_L2_swa-pas-grnd-mom`) and
  VDFs (`solo_L2_swa-pas-vdf`).
- **SO/SWA EAS L2:** electron VDFs and PADs (`solo_L2_swa-eas*`).
- **SO/SWA HIS L2:** heavy-ion charge-state ratios
  (`solo_L2_swa-his-comp-10min`, etc.; TODO verify exact products).
- **Frames:** Spacecraft / instrument frames in L1; RTN / SRF in L2.
- **Archives:** ESA SOAR; CDAWeb mirror.

## Algorithm / workflow steps

1. **Choose sensor** by species: protons / alphas → PAS; electrons → EAS;
   heavy-ion composition → HIS.
2. **Pick product:** moments by default; VDFs for kinetic / wave-particle
   analyses; HIS slow-cadence composition for source-region diagnostics
   (per [[damicis-2025-solo-swa-alfvenic-streams-validation]]).
3. **Pick frame:** RTN for moments paired with SO/MAG; instrument for
   VDFs.
4. **Apply contamination cuts:** below ~ 20 eV EAS contains spacecraft-
   emitted photo/secondary electrons (TODO refine threshold from full
   text and from later modelling paper).
5. **Pair with SO/MAG:** required for Alfvénicity / pitch-angle / charge-
   state-vs-source-region workflows.
6. **Persist contract** with sensor, product, cadence, frame, and
   contamination caveats.

```python
def so_swa_contract(species, kind, interval, frame="RTN"):
    sensor = {"p": "PAS", "a": "PAS", "e": "EAS", "heavy": "HIS"}[species]
    product = {"moments": f"swa-{sensor.lower()}-grnd-mom",
               "vdf":     f"swa-{sensor.lower()}-vdf"}[kind]
    return {"instrument": "SO/SWA", "sensor": sensor, "product": product,
            "frame": frame, "interval": interval, "archive": "SOAR"}
```

## Minimal executable benchmark or validation target

Not benchmarked yet — see `claim_boundary.scope`. Promotion to `executable`
requires: a script that loads PAS proton moments and SO/MAG B for a 2022
fast-stream interval, computes the proton plasma beta and matches the
published value within ~ 20 % (TODO supply specific interval with full
text).

## Known pitfalls / failure modes

- **EAS spacecraft-electron contamination.** Cold electrons emitted from
  spacecraft surfaces contaminate spectra at low energies; cut below
  spacecraft-potential energy threshold.
- **PAS FoV.** PAS is Sun-ward-pointed; off-axis beams (during structured
  intervals) bias moments — verify VDF.
- **HIS cadence.** Heavy-ion composition cadence is minutes, not seconds;
  cannot be used for kinetic-scale analyses.
- **Frame conventions.** L1 in instrument frame; L2 in RTN/SRF — code
  that mixes the two corrupts pitch-angle / Alfvénicity diagnostics.
- **Time-tag offsets between sensors.** PAS, EAS, HIS have independent
  timing; require explicit interpolation.
- **Inter-sensor cross-calibration.** PAS moments and SO/MAG B suffice for
  Alfvén-ratio diagnostics; combining HIS-derived densities directly with
  PAS proton densities requires accounting for different effective FoVs.

## Compilation into an Anthropic-style agent-native Skill

| Paper element | Agent-native form |
|---|---|
| Claim — SWA three-sensor inventory + intended products | **Verifiable task:** `so_swa_contract(species, kind, interval) -> JSON` |
| Methods — sensor / product / frame selection, contamination cut | **Executable workflow:** §"Algorithm / workflow steps" 1–6 |
| Data / instruments — PAS, EAS, HIS L2 moments + VDFs | **MCP / tool contracts:** SOAR REST or harness fallback |
| Caveats — EAS contamination, PAS FoV, HIS cadence, frame, time-tag | **Skill memory:** §"Known pitfalls / failure modes" |
| Figures — sensor block diagrams | **Benchmark artifacts:** VDF slice + moments overlay |

## Claim boundary

**In scope.** SWA **as designed and commissioned in 2020** — PAS / EAS /
HIS inventories, intended L2 products, FoVs, nominal calibration. The
skill returns contracts; numerical performance characterization is in
later commissioning literature.

**Out of scope — do NOT generalize beyond:**

- Do not quote on-orbit numerical performance without citing later
  commissioning sources.
- Do not infer MAG / RPW / EPD contracts from this paper.
- Do not assume HIS is available at all intervals — its cadence and
  duty-cycle differ from PAS.

## Links

- DOI: https://doi.org/10.1051/0004-6361/201937259 — verified via Crossref
  on 2026-05-19.
- arXiv: n/a.
- ADS: 2020A&A...642A..16O — derived from journal coordinates
  (A&A 642, A16); not directly fetched.
- Code: `pyspedas.solar_orbiter.swa` loaders.
- Data: ESA SOAR (https://soar.esac.esa.int/); CDAWeb mirror.

## Research-generation affordances

- **PAS-vs-EAS-vs-HIS contract triage.** A per-encounter table of which
  SWA sub-instruments delivered nominal moments in a given window would
  turn instrument-availability triage from an event-by-event question
  into a queryable agent capability — directly useful for any
  Alfvénicity / cross-helicity workflow that pairs SWA with SO/MAG.
- **EAS contamination model release-target.** Spacecraft-emitted
  photo/secondary electrons bias EAS at low energy; publishing a per-
  encounter contamination model (cf. forthcoming
  Štverák-style follow-up papers) as a callable correction would lift
  the strong "do not use EAS below ~ 30 eV" caveat into a quantitatively
  bounded recommendation.
- **HIS duty-cycle vs charge-state-variability bound.** HIS has lower
  duty cycle than PAS; quantifying the resulting sampling-rate effect
  on derived charge-state variability is a missing systematic in any
  cross-encounter heavy-ion study.
- **Cross-instrument plasma intercept with PSP/SWEAP.** When PSP and
  SolO are radially aligned, SWA-PAS↔SPC/SPAN-Ai moment-ratio
  publication on shared field lines bounds the cross-mission plasma
  scale and is a structural prerequisite for radial-evolution studies
  spanning the two missions.

## Skill graph → depends_on

- `[[muller-2020-solar-orbiter-mission-overview]]` — mission context.
- `[[horbury-2020-solo-mag-vector-magnetometer]]` — paired magnetic field.
- `[[damicis-2025-solo-swa-alfvenic-streams-validation]]` — applied SWA
  workflow.

## References

- Owen et al. (2020), *Astronomy & Astrophysics*, 642, A16 —
  not-in-local-inventory; bibliographic fields TODO verify with full text.
