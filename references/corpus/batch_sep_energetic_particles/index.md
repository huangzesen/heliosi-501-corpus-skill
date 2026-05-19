# Batch — Solar Energetic Particles, Shocks, and Suprathermal Heliophysics

- **Generated**: 2026-05-18 (revised 2026-05-18 for harness-agnostic four-layer model)
- **Theme**: solar-energetic-particles + heliospheric-shocks + suprathermal populations (primary_theme = `energetic_particles`)
- **Status**: stub-tier batch — claims grounded in arXiv abstracts compiled into the local inventory `sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json`. Numerical specifics flagged `TODO verify in full paper` per skill, per spec §8.
- **Runtime neutrality**: Every SKILL.md in this batch is structured to be loadable by *any* general-purpose agent runtime (Claude Code, LingTai, Codex, Cursor, OpenAI Assistants, …). Named runtimes / MCPs / repos appear only as *adapter examples*. Each SKILL.md exposes four layers — (1) scientific invariant, (2) executable protocol with abstract capability contracts, (3) optional adapter / runtime notes, (4) research-generation affordances (§10) — see the "Layer map" block at the top of each SKILL.md.
- **Source inventories**:
  - `sioulas-reproduction/results/arxiv_papers/theme_energetic_particles.json` (primary; 123 papers; 12 selected here)
  - `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md` (cross-reference)
  - `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md` (cross-reference)
- **Parent skill**: `.library/custom/heliophysics-skills/SKILL.md` (theme: energetic_particles)
- **Sibling pilot**: `sioulas-reproduction/results/paper_skill_corpus/pilot_2026_and_runtime/murtas-2026-hcs-reconnection-ion-energization/` (cross-theme link)

## Skills

| # | Slug | Year | Lead | arXiv | Core claim (one line) | Tier |
|---|------|------|------|-------|------------------------|------|
| 1 | `paper-reames-2026-physics-of-seps` | 2026 | Reames | 2602.18617 | Two-mechanism SEP framework (reconnection-jet impulsive vs CME-shock gradual); streaming limit + reservoir + FIP-bias + residual-impulsive-reacceleration diagnostics. | stub |
| 2 | `paper-desai-2024-hcs-reconnection-400kev-protons` | 2024 | Desai | 2410.16539 | PSP near-Sun HCS reconnection exhaust at ~16.25 R_sun traps protons up to ~400 keV with γ ~ -5 spectrum; kglobal merging-islands model w/ guide field 0.2-0.3. | stub |
| 3 | `paper-murtas-2024-compression-acceleration-hcs` | 2024 | Murtas | 2408.10445 | 2D MHD + Parker transport reproduces multi-species power-laws at HCS; E_max(p) ~ 0.1-1 MeV; (Q/M)^α scaling with α ≈ 0.4 (model) vs ~0.7 (PSP). | stub |
| 4 | `paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks` | 2024 | Jebaraj | 2410.15933 | First in-situ synchrotron-electron measurements at PSP-traveling near-Sun shocks; strong quasi-parallel >> quasi-perpendicular emission. | stub |
| 5 | `paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp` | 2024 | Wimmer-Schweingruber | 2408.02330 | Inner-heliosphere energetic-particle environment is SEP + ESP + ACR + planetary-bow-shock superposition, resolved by SO/EPD + PSP/ISʘIS. | stub |
| 6 | `paper-cuesta-2024-kappa-distributions-energetic-protons` | 2024 | Cuesta | 2407.20343 | PSP/ISʘIS 10-60 MeV protons across ICME well-fit by kappa; κ_EP peaks ~3.5 in ejecta; T_EP/n_EP anti-correlated; T_EP/κ positively correlated (entropy increase). | stub |
| 7 | `paper-trotta-2025-ip-shock-variability-multi-spacecraft` | 2025 | Trotta | 2508.19812 | Single strong IP shock at Wind/ACE (1 au) + SO (0.8 au): energy-dependent cross-correlation reveals shock-evolution + spatial-irregularity variability. | stub |
| 8 | `paper-kouloumvakos-2026-iva-shock-properties` | 2026 | Kouloumvakos | 2604.13962 | 26 IVA-SEP events; 3D shock + coronal MHD show connectivity migrates from weak flanks to strong shock apex, producing delayed high-energy arrivals consistent with time-dependent DSA. | stub |
| 9 | `paper-xu-2026-psp-iva-sep-events` | 2026 | Xu | 2602.12475 | First PSP IVA event catalog (14 events through end-2024); 11/14 in medium-nose-energy bin; canonical Labor Day 2022-09-05 event. | stub |
| 10 | `paper-laitinen-2026-vda-turbulent-heliosphere` | 2026 | Laitinen | 2603.06433 | Full-orbit proton sims in turbulent IMF: VDA injection-time biased 2-16 min late and path length 0.2-0.3 au too long (weak/moderate turb); >5 au (strong turb); background-spectrum 5-20 min extra bias. | stub |
| 11 | `paper-walker-2026-icme-radial-particle-acceleration-statistics` | 2026 | Walker | 2605.00163 | 39-event multipoint ICME catalog 2016-2023 (PSP/SO/ACE/Wind/STEREO-A): shock-acceleration efficiency increases with distance inside ~0.7 au then decreases. | stub |
| 12 | `paper-dresing-2025-widespread-esp-march-2023` | 2025 | Dresing | 2502.06332 | 2023-03-13 widespread event observed at 6 observers (PSP/SO/BepiColombo/STEREO-A/near-Earth/MAVEN); both MHD scenarios (single blast wave, multi-CME) fit; blast wave slightly better. | stub |

## Theme structure of the batch

The batch organizes around four threads, all bound by the
`energetic_particles` primary theme:

1. **Reconnection-driven HCS acceleration** —
   `paper-desai-2024-...` (PSP observation) +
   `paper-murtas-2024-...` (MHD + transport model). Sibling
   `pilot_2026_and_runtime/murtas-2026-hcs-reconnection-ion-energization`
   extends to ApJ 2026.
2. **Shock acceleration of electrons and ions** —
   `paper-jebaraj-2024-...` (electrons; near-Sun PSP) +
   `paper-trotta-2025-...` (ions; multi-spacecraft IP shock).
3. **IVA / non-trivial velocity dispersion** —
   `paper-xu-2026-...` (PSP catalog) +
   `paper-kouloumvakos-2026-...` (SO+PSP 3D shock connectivity) +
   `paper-laitinen-2026-...` (VDA-bias methodology caveat).
4. **Inner-heliosphere SEP environment and event statistics** —
   `paper-reames-2026-...` (canonical review) +
   `paper-wimmer-schweingruber-2024-...` (SO+PSP environment) +
   `paper-cuesta-2024-...` (kappa thermodynamics) +
   `paper-walker-2026-...` (multipoint ICME catalog) +
   `paper-dresing-2025-...` (single widespread event).

## Cross-cutting infrastructure (candidates for synthesis skills)

These twelve skills repeatedly invoke the following implementation
building blocks, suitable for promotion to dedicated synthesis skills
in a later pass (per spec §6 Stage B):

- **PSP/ISʘIS data loader** — EPI-Lo + EPI-Hi spectra + composition.
- **PSP/FIELDS MAG HCS / shock identifier** — sector reversal, Walen
  jet, Rankine-Hugoniot.
- **SO/EPD data loader** — SIS, HET, EPT, STEP via SOAR.
- **Rankine-Hugoniot shock-condition fit** — generic multi-mission.
- **θ_Bn obliquity classifier** — generic shock-normal estimator.
- **Parker transport equation SDE solver** — multi-species,
  Q/A-dependent diffusion tensor.
- **Kappa-distribution tail fit** — Livadiotis formalism.
- **IVA contour-line detector** — Xu+ 2026 method.
- **VDA onset-fit with background** — Laitinen+ 2026 bias-aware
  variant.
- **Magnetic-connectivity (PFSS + ballistic)** — per-spacecraft
  footpoint mapping.
- **MHD + CME-injection model wrapper** — ENLIL / EUHFORIA / MAS
  (TODO disambiguate per Dresing & Kouloumvakos).

## Skill graph (compact view)

```
                                  reames-2026  ←──────┐
                                       │              │
            ┌──────────────────────────┴──┐           │
            │                             │           │
   desai-2024 ←──┐               wimmer-schweingruber-2024
            │     │                       │
            │     ↓                       ↓
            │   murtas-2024          cuesta-2024
            │
            └────→ jebaraj-2024 → trotta-2025 → kouloumvakos-2026 ←→ xu-2026 ↔ laitinen-2026

   walker-2026 ←─ trotta-2025
   dresing-2025 ←─ walker-2026, kouloumvakos-2026
```

(Arrows are `depends_on` edges. The graph is the literal `depends_on`
edge-list in `manifest.json`.)

## Weak entries flagged for full-text verification

Per spec §8 ("avoiding overclaiming and hallucinated citations"), every
skill in this batch is at `stub` tier, was generated from arXiv-abstract
content stored in the local inventory, and carries explicit
`TODO verify with full text` flags on numerical claims and supporting
infrastructure (DOIs, MHD model identity, event-list dates, simulation
code repos). The complete TODO list is in
`manifest.json#weak_entries_needing_full_text_verification`.

The *weakest* entries — most exposed if a single TODO is not
verifiable — are:

| Slug | Weakness | Recommended action |
|------|----------|--------------------|
| `paper-wimmer-schweingruber-2024-sep-inner-heliosphere-solo-psp` | Authorship includes a collaboration roster ("the Solar Orbiter EPD team") that is not expanded in the inventory; venue/DOI also TODO. | Pull the arXiv abstract page and the EPD-team paper roster; expand authors and confirm venue before manuscript citation. |
| `paper-kouloumvakos-2026-iva-shock-properties` | The coronal MHD model identity (ENLIL vs EUHFORIA vs MAS) and the contour-line / IVA-detection threshold are TODO; the conclusion depends on both. | Full-text pass; identify the model and freeze the threshold. |
| `paper-dresing-2025-widespread-esp-march-2023` | The "single blast wave performs slightly better" conclusion is presented as a slight preference; the MHD model identity and CME-injection list are TODO. | Full-text pass; freeze the model + CME list before any cross-event generalization. |
| `paper-murtas-2024-compression-acceleration-hcs` | The α(model) ≈ 0.4 vs α(observation) ≈ 0.7 tension is the paper's central numerical claim and requires the exact species list + diffusion-coefficient prescription. | Full-text pass; freeze species list and diffusion-tensor parameters. |
| `paper-laitinen-2026-vda-turbulent-heliosphere` | The (2D-dominant + minor slab) turbulence prescription parameters drive every bias range quoted. | Full-text pass; freeze the spectral-parameter set and re-validate the bias ranges. |

## Roll-up reproducibility targets

Any general-purpose agent runtime consuming this batch (e.g., Claude Code,
LingTai, Codex — adapter examples, not requirements) should be able to roll
up:

- A unified **PSP near-Sun HCS reconnection table** with E_max(proton),
  spectral index, exhaust geometry per crossing (Desai 2024 anchor;
  Murtas 2024 model).
- A **multi-spacecraft IP-shock-variability cross-correlation atlas**
  (Trotta 2025 method generalized to Walker 2026 catalog).
- An **IVA-event registry** combining the PSP catalog (Xu 2026) and
  the SO+PSP 3D shock reconstruction (Kouloumvakos 2026), with VDA-bias
  notes from Laitinen 2026.
- A **widespread-event MHD scenario template** (Dresing 2025) reusable
  for future circumsolar events.
- A **kappa-distribution-based thermodynamic-property column** for any
  PSP ICME crossing (Cuesta 2024).
- A **canonical impulsive/gradual classification + diagnostics menu**
  for any SEP event (Reames 2026).

## How to promote a skill in this batch beyond `stub`

Per spec §7, promotion to `method-ready` requires:

1. Open the SKILL.md.
2. Verify the bibliographic anchor against a primary source — the
   arXiv abstract is in `theme_energetic_particles.json`; the journal
   DOI and final venue should be added at promotion time.
3. Resolve all `TODO verify with full text` items in the SKILL.md and
   `metadata.yaml`.
4. Add a procedure paragraph + at least one `equation_refs[]` pointer
   per `algorithms[]` entry.
5. Append a promotion entry to
   `paper_skill_factory/index/promotion_log.jsonl` (path defined by
   spec §2; not created by this batch).
