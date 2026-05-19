# Batch — Wave-500 SEP / Shocks / ICMEs / CIRs / Space-Weather Transients (045)

- **Generated**: 2026-05-18 (HelioSI paper-to-skill factory (Claude Opus 4.7))
- **Theme**: solar-energetic-particles + heliospheric/IP/coronal shocks + ICME-associated particle acceleration + CIR / Forbush / GLE / ESP / radio-burst / extreme-event diagnostics (primary_theme = `energetic_particles`)
- **Status**: stub-tier batch — every skill is grounded in the local arXiv inventory `sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json`. Numerical / event-date / DOI / ADS specifics that are not present in the inventory abstract are flagged `TODO_verify_with_full_text` per v0.2 spec §1, §7. No fabricated bibliographic identifiers.
- **Wave goal**: progress the HelioSI paper/tool-skill corpus from 96 → 141 (this is the +45 batch on the 500-object roadmap).
- **Runtime neutrality**: Every SKILL.md is structured to be loadable by *any* general-purpose agent runtime (Claude Code, LingTai, Codex, Cursor, OpenAI Assistants, …). Named runtimes / MCPs / repos appear only as *adapter examples*. Each SKILL.md exposes four layers — (1) scientific invariant, (2) executable protocol with abstract capability contracts, (3) optional adapter / runtime notes, (4) research-generation affordances (§9) — see the "Layer map" block at the top of each SKILL.md.
- **Source inventories** (local-first, per task brief):
  - `sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json` — primary; 123 papers; 45 selected here.
  - `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` — cross-reference.
  - `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md` — cross-reference.
- **Parent skill**: `.library/custom/heliophysics-skills/SKILL.md` (theme: `energetic_particles`).
- **Sibling SEP batch**: `batch_sep_energetic_particles/` (12 slugs; this batch deliberately excludes those 12 to avoid duplicate slugs).

## Exclusion guarantee (no duplicate slugs)

This batch DOES NOT introduce any of the 12 slugs already present in `batch_sep_energetic_particles/`:

- `paper-cuesta-2024-kappa-distributions-energetic-protons`
- `paper-desai-2024-hcs-reconnection-400kev-protons`
- `paper-dresing-2025-widespread-esp-march-2023`
- `paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks`
- `paper-kouloumvakos-2026-iva-shock-properties`
- `paper-laitinen-2026-vda-turbulent-heliosphere`
- `paper-murtas-2024-compression-acceleration-hcs`
- `paper-reames-2026-physics-of-seps`
- `paper-trotta-2025-ip-shock-variability-multi-spacecraft`
- `paper-walker-2026-icme-radial-particle-acceleration-statistics`
- `paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp`
- `paper-xu-2026-psp-iva-sep-events`

These appear only as `depends_on` cross-batch links from this batch (verified at generation time: every `depends_on` slug resolves either to a wave500 sibling or to one of the 12 above).

## Skills (45)

| # | Slug | Year | Lead | arXiv | Core claim (one line) |
|---|------|------|------|-------|------------------------|
| 1 | `paper-cao-2026-sep-rise-times-earth-mars-transport` | 2026 | Cao | 2605.01437 | SEP rise-time vs energy follows a power-law; flatter exponent at Mars implies rigidity-approaching-independence transport. |
| 2 | `paper-han-2026-sees-cross-hcs-statistical` | 2026 | Han | 2604.19446 | Cross-HCS SEE events (9 vs 60 same-side) are more isotropic; transport across HCS is inefficient unless source or observer lies close to the HCS. |
| 3 | `paper-liuzzo-2026-sep-reflection-precursor-icme` | 2026 | Liuzzo | 2604.25019 | Bi-directional SEE beams reflect off a precursor ICME shock beyond 1 au; first electron IVD detection at 1 au. |
| 4 | `paper-duan-2026-sep-type-ii-radio-source-regions` | 2026 | Duan | 2604.20237 | SEP halo CMEs (43) vs non-SEP (131): SEP-associated type IIs longer / lower-ending; starting freq is single AR > multi AR > outside AR. |
| 5 | `paper-mekhaldi-2026-carrington-36cl-ice-cores` | 2026 | Mekhaldi | 2604.26608 | Ice-core 36Cl rules out an extreme >30 MeV Carrington-1859 SEP event; soft SEP up to 3× SA-max, or none Earth-bound. |
| 6 | `paper-stoffel-2025-rerunaway-Forbush-cross-correlation` | 2026 | Stoffel (TODO_verify) | 2604.06383 | Cross-correlation between solar-activity indices and GCR flux during Forbush decreases reveals lag relationships. |
| 7 | `paper-mishev-2026-first-four-gles-1940s` | 2026 | Mishev (TODO_verify) | 2602.24250 | Digitisation + re-analysis of the first four 1940s GLEs yields revised event spectra useful for extreme-event statistics. |
| 8 | `paper-kollhoff-2026-acr-helium-solo-het` | 2026 | Kollhoff (TODO_verify) | 2602.22418 | Solar Orbiter HET ACR He spectrum constrains inner-heliosphere ACR modulation. |
| 9 | `paper-mason-2026-unusual-2024-june-8-gle` | 2026 | Mason (TODO_verify) | 2602.12507 | The 2024-06-08 GLE is anomalous in source geometry / behind-the-limb associations. |
| 10 | `paper-share-2026-sol2012-06-03-late-phase-gamma-shock` | 2026 | Share (TODO_verify) | 2602.10284 | SOL2012-06-03 late-phase γ-rays are produced by >300 MeV protons from CME-shock reacceleration of flare suprathermals. |
| 11 | `paper-bian-2026-30march2022-sep-data-assimilation` | 2026 | Bian (TODO_verify) | 2602.00765 | Multi-spacecraft data assimilation for 2022-03-30 yields posterior on κ_par and κ_perp. |
| 12 | `paper-mason-2026-sunward-3he-rich-sep-solo-psp` | 2026 | Mason (TODO_verify) | 2601.20624 | PSP+SOLO observe Sunward-streaming 3He-rich impulsive SEP events near perihelion. |
| 13 | `paper-liu-2026-3d-coronal-shock-longitudinal-sep` | 2026 | Liu (TODO_verify) | 2601.13692 | 3D coronal shock reconstruction explains longitudinal SEP intensity via local θ_Bn / Mach. |
| 14 | `paper-koppl-2026-electron-acr-cold-clouds-radiation` | 2026 | (TODO_verify) | 2601.11785 | Cold-cloud encounters in the last 10 Myr drive substantially elevated GCR/ACR radiation at Earth. |
| 15 | `paper-luhmann-2026-stereo-het-sep-protons-first-orbit` | 2026 | (TODO_verify) | 2601.09630 | STEREO-A HET proton SEP catalog 2006–2023 provides full-solar-orbit longitudinal coverage. |
| 16 | `paper-sun-2026-counterfactual-sep-prediction-ml` | 2026 | (TODO_verify) | 2601.08999 | Physics-guided counterfactual explanations make multivariate-time-series SEP-prediction models interpretable. |
| 17 | `paper-meng-2025-sepnet-multi-task-ml` | 2025 | (TODO_verify) | 2512.12786 | SEPNET multi-task deep learning jointly predicts SEP occurrence, peak flux, and spectral index. |
| 18 | `paper-rab-2025-sep-protoplanetary-disk-irradiation` | 2025 | (TODO_verify) | 2512.03184 | Young-Sun SEP irradiation extent in the protoplanetary disk constrains isotopic-anomaly origins. |
| 19 | `paper-cohen-2025-coronal-flux-tube-shock-spot-newyearseve-2023` | 2025 | (TODO_verify) | 2512.24749 | The 2023-12-31 eruption shows a localized shock spot illuminating a coronal flux tube. |
| 20 | `paper-malandraki-2025-perp-diffusion-near-sun` | 2025 | (TODO_verify) | 2509.10648 | PSP IS☉IS energetic-particle observations constrain κ_par and κ_perp in the near-Sun wind. |
| 21 | `paper-clark-2025-may2024-superstorm-sep-feo` | 2025 | (TODO_verify) | 2511.03905 | May-2024 superstorm SEP Fe/O abundance ratios show characteristic energy dependence consistent with compound-event acceleration. |
| 22 | `paper-allen-2025-shock-evolution-2023-march-13-event` | 2025 | (TODO_verify) | 2511.03496 | Time-resolved Rankine-Hugoniot fit of 2023-03-13 shock from in-situ + remote sensing across observers. |
| 23 | `paper-zhang-2025-2024-09-09-backside-eruption-sgre` | 2025 | (TODO_verify) | 2503.23852 | The 2024-09-09 backside solar eruption produced a sustained gamma-ray emission event. |
| 24 | `paper-jin-2025-third-harmonic-type-ii-2024-09-14` | 2025 | (TODO_verify) | 2503.23584 | The 2024-09-14 IP type II shows third-harmonic structure (in addition to 1f + 2f). |
| 25 | `paper-luo-2025-2023-july-17-radial-ion-fluence-psp` | 2025 | (TODO_verify) | 2502.17806 | 2023-07-17 SEP event observed at PSP+STEREO+ACE yields a radial fluence power-law. |
| 26 | `paper-jebaraj-2025-electron-beam-radio-five-spacecraft-2021` | 2025 | (TODO_verify) | 2502.15067 | Five-spacecraft BELLA multilateration of 2021-12-04 type III sources reconciles 'higher than expected' densities via radio scattering. |
| 27 | `paper-feng-2025-shock-sep-modeling-2022-09-05` | 2025 | (TODO_verify) | 2501.03066 | Coupled shock + SEP-transport model reproduces 2022-09-05 multi-observer intensity profiles. |
| 28 | `paper-mason-2025-icme-may16-2023-composition-variation` | 2025 | (TODO_verify) | 2410.19672 | PSP (Fe/O ≈ 0.48) vs SOLO (≈ 0.08) at 0.7 au for 2023-05-16 SEP event; longitude-dependent direct-flare contribution. |
| 29 | `paper-livadiotis-2024-kappa-tail-technique-psp` | 2024 | Livadiotis | 2407.04188 | Kappa-tail technique provides a closed-form fit applied to PSP/IS☉IS energetic-particle tails. |
| 30 | `paper-leske-2024-three-stage-sep-acceleration-psp` | 2024 | Leske (TODO_verify) | 2405.19680 | PSP IS☉IS shows a three-stage (flare → shock → reservoir) acceleration sequence within a single event. |
| 31 | `paper-li-2026-3he-rich-bidirectional-sep-solar-orbiter` | 2025 | (TODO_verify) | 2507.16990 | Solar Orbiter bidirectional anisotropic SEP events imply mirror reflection or magnetic trapping. |
| 32 | `paper-buthelezi-2025-resolving-shock-loft-type-ii-lofar` | 2025 | (TODO_verify) | 2502.16934 | LOFAR resolves type II band-splitting and herringbones mapping onto distinct shock-acceleration sites. |
| 33 | `paper-marsh-2024-parasol-sep-forecasting` | 2024 | (TODO_verify) | 2412.11852 | The PARASOL SEP-forecast model couples eruption inputs with a transport solver and verifies on a hold-out set. |
| 34 | `paper-wijsen-2024-cross-field-diffusion-coronal-flux-rope` | 2024 | Wijsen (TODO_verify) | 2411.00738 | Cross-field diffusion inside a coronal flux rope produces measurable spread of energetic-particle distributions. |
| 35 | `paper-chen-2024-energetic-particles-quasi-separatrix-layers` | 2024 | (TODO_verify) | 2410.07420 | Energetic-particle acceleration at QSLs and current sheets is an additional impulsive-SEP component. |
| 36 | `paper-allen-2024-radial-evolution-icme-sep-solo-ace` | 2024 | Allen (TODO_verify) | 2410.01885 | Solar Orbiter + ACE radial-conjunction events trace ICME-shock evolution. |
| 37 | `paper-jebaraj-2024-type-ii-multi-vantage-catalog` | 2024 | Jebaraj (TODO_verify) | 2410.00814 | Multi-vantage-point type II catalog yields population-level statistics across Wind/STEREO/PSP/SOLO. |
| 38 | `paper-dalla-2026-radiation-doses-extreme-seps` | 2026 | Dalla | 2604.15160 | Worst-case radiation doses for Space Age and historical extreme SEP events computed at aviation and in-space altitudes. |
| 39 | `paper-jebaraj-2025-localized-particle-global-coronal-shock` | 2026 | (TODO_verify) | 2603.23335 | A global coronal shock shows localized acceleration sites mapping onto observers via PFSS+ballistic connectivity. |
| 40 | `paper-niemiec-2025-numerical-superdiffusive-particle-acceleration` | 2026 | (TODO_verify) | 2604.14819 | Numerical IP-shock simulations compare diffusive vs superdiffusive scenarios and identify distinguishing diagnostics. |
| 41 | `paper-yang-2025-2024-09-04-iva-solar-orbiter` | 2025 | (TODO_verify) | 2507.00954 | A Solar Orbiter IVA event is explained by a time-dependent shock-acceleration model. |
| 42 | `paper-ding-2025-2022-09-05-time-dependent-dsa` | 2025 | Ding (TODO_verify) | 2506.20322 | Direct evidence for time-dependent DSA in the 2022-09-05 Labor Day event from PSP near-Sun spectra. |
| 43 | `paper-zheng-2025-ip-shock-effect-turbulence` | 2025 | (TODO_verify) | 2505.04450 | IP shocks modify upstream/downstream turbulence parameters as a function of shock strength / θ_Bn. |
| 44 | `paper-ding-2026-relativistic-sep-2021-10-28-multi-sc` | 2026 | Ding (TODO_verify) | 2603.09839 | Multi-spacecraft constraints on relativistic-proton transport in the widespread 2021-10-28 event. |
| 45 | `paper-pereira-2026-connection-angle-gle-anisotropy` | 2026 | (TODO_verify) | 2603.19953 | GLE proton anisotropy correlates with magnetic-connection-angle between observer and source region. |

## Theme structure of the batch

The batch organizes around six threads, all bound by `primary_theme = energetic_particles`:

1. **Transport, diffusion, VDA, IVA** — Cao+ 2026 rise-times, Han+ 2026 cross-HCS, Malandraki+ 2025 κ_perp/κ_par, Liuzzo+ 2026 precursor-ICME reflection, Wijsen+ 2024 cross-field diffusion, Yang+ 2025 + Ding+ 2025 IVA / time-dependent DSA, Niemiec+ 2025 super-diffusive.
2. **Specific events and case studies** — Bian+ 2026 (2022-03-30), Liu+ 2026 (3D shock), Allen+ 2025 (2023-03-13), Zhang+ 2025 (2024-09-09 backside SGRE), Jin+ 2025 (2024-09-14 type II), Luo+ 2025 (2023-07-17), Jebaraj+ 2025 (2021-12-04 BELLA), Feng+ 2025 (2022-09-05 modeling), Mason+ 2025 (2023-05-16 composition), Ding+ 2026 (2021-10-28 widespread), Cohen+ 2026 (2023-12-31), Share+ 2026 (SOL2012-06-03 γ-rays), Leske+ 2024 (3-stage event).
3. **Composition, anisotropy, thermodynamics** — Mason+ 2026 Sunward 3He-rich, Li+ 2026 bidirectional anisotropy, Mason+ 2025 longitudinal Fe/O, Clark+ 2025 May-2024 Fe/O, Livadiotis+ 2024 kappa-tail.
4. **Catalogs, statistics, and observation hubs** — Duan+ 2026 type II + AR, Jebaraj+ 2024 multi-vantage type II catalog, Luhmann+ 2026 STEREO-A first orbit, Allen+ 2024 SO+ACE radial, Pereira+ 2026 GLE anisotropy connection angle.
5. **Forecasting + ML interpretation** — Meng+ 2025 SEPNET, Sun+ 2026 counterfactual, Marsh+ 2024 PARASOL.
6. **Extreme events / historical / cosmogenic** — Mekhaldi+ 2026 36Cl Carrington, Mishev+ 2026 1940s GLEs, Mason+ 2026 2024-06-08 GLE, Dalla+ 2026 doses, Köppl+ 2026 cold-cloud radiation, Rab+ 2025 protoplanetary disk, Kollhoff+ 2026 ACR He, Stoffel+ 2025 Forbush, Jebaraj+ 2025 localized acceleration global shock, Buthelezi+ 2025 LOFAR type II, Chen+ 2024 QSL.

## Cross-cutting infrastructure (candidates for synthesis skills)

These 45 skills repeatedly invoke the same implementation building blocks — already enumerated in
`batch_sep_energetic_particles/manifest.json` and extended here with new candidates for the
500-object roadmap:

- PSP/IS☉IS data loader (EPI-Lo + EPI-Hi spectra + composition)
- PSP/FIELDS MAG shock identifier (Rankine-Hugoniot, Walen jet)
- Solar Orbiter EPD data loader (HET / EPT / STEP / SIS via SOAR)
- Rankine-Hugoniot shock-condition fit (generic multi-mission)
- θ_Bn obliquity classifier
- Parker transport equation SDE solver (multi-species, Q/A-dependent diffusion tensor)
- Kappa-distribution tail fit (Livadiotis formalism)
- IVA contour-line detector
- VDA onset-fit with background
- Magnetic-connectivity (PFSS + ballistic)
- MHD + CME-injection model wrapper
- **Neutron-monitor rigidity-corrector** (new)
- **Type II band-pair / triplet fit** (new — Jin 2025 third-harmonic case)
- **Cosmogenic-isotope fluence inverter** (new — Mekhaldi 2026, Dalla 2026)
- **Fermi-LAT pion-decay fit** (new — Share 2026, Zhang 2025)
- **Bayesian multilateration (BELLA)** (new — Jebaraj 2025 five-spacecraft)

## Skill graph (compact view)

```
                     reames-2026 ← (most SEP skills)
                          ↑
                          │
   cao-2026 →  han-2026   │
       │        │         │
       ↓        ↓         │
   walker-2026  liuzzo-2026
       ↑        ↑
       │        │
   luo-2025 / allen-2024 / allen-2025
       ↑
   dresing-2025 ← walker-2026

   livadiotis-2024 → cuesta-2024 (cross-batch)
   leske-2024 → reames-2026 / xu-2026
   ding-2025-time-dep-DSA → feng-2025-modeling / kouloumvakos-2026
   yang-2025 / laitinen-2025 (dropped) → xu-2026 / kouloumvakos-2026
```

(Arrows are `depends_on` edges. The literal edge-list lives in `manifest.json#skill_graph_edges`.)

## Weak-attribution flagging

Every skill in this batch is `weak_attribution: true`. Author lists and event-date specifics
unavailable from the inventory abstract are explicitly written `TODO_verify_with_full_text` (per
spec §1, §7) and listed in `manifest.json#weak_entries_needing_full_text_verification`.

## Counts (verified at generation)

- 45 skill directories
- 45 `SKILL.md` files
- 45 `metadata.yaml` files
- 0 duplicate slugs within batch
- 0 collisions with `batch_sep_energetic_particles/` slug set
- 100% of `depends_on` references resolve to a wave500 sibling or one of the 12 existing SEP-batch slugs

See `manifest.json` for the machine-readable form.
