# Batch — Solar-Wind Classification, Segmentation & ML / Data-Driven Heliophysics

- **Generated**: 2026-05-18
- **Theme**: solar-wind classification × stream / structure segmentation × machine-learning event detection × automated heliophysics workflows
- **Status**: pilot scaffold — claims grounded in the curated arXiv inventories; numerical specifics flagged `TODO verify in full paper` per skill.
- **Source inventories**:
  - `sioulas-reproduction/results/arxiv_papers/theme_solar_wind_segmentation.json`
  - `sioulas-reproduction/results/arxiv_papers/extended_search.md` §6 (solar wind segmentation machine learning)
  - `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md` Topic 2 (PSP data analysis — EMBER)
- **Parent skill**: `.library/custom/heliophysics-skills/SKILL.md` (theme: `solar_wind_segmentation`; cross-link to `pfss_source_mapping` for CH segmentation, `psp_data` for in-situ classification)
- **Prior / sibling batches** (referenced via `[[slug]]` only — these files are **not** modified):
  - `sioulas-reproduction/results/paper_skill_corpus/batch_pfss_source_mapping/`
  - `sioulas-reproduction/results/paper_skill_corpus/batch_psp_switchbacks_magnetic/`
  - `sioulas-reproduction/results/paper_skill_corpus/batch_turbulence_heating_apj/`
  - `sioulas-reproduction/results/paper_skill_corpus/batch_heliophysics_software_infrastructure/`
  - `sioulas-reproduction/results/paper_skill_corpus/pilot_turbulence/` and `pilot_2026_and_runtime/`

## Compilation framing (per factory spec §0)

Each SKILL.md compiles one paper into an agent-native object, **not a summary**:

| Paper element | Compiled form per skill | Where it lives in this batch's SKILL.md |
|---|---|---|
| Claims / results | "Paper claim → verifiable task" + acceptance criteria | §2 + §5 |
| Methods / equations | "Methods / equations → executable workflow" (named algorithms) | §3 |
| Data / instruments | "Data / instruments → tool contracts" table | §4 |
| Caveats / pitfalls | "Failure modes → skill memory" | §6 |
| Figures / numerical results | "Validation target → benchmark artifact" | §5 |
| Corpus / citations | "Skill graph → depends_on" with `[[slug]]` links | §9 |

The general-purpose Claude / Codex harness is the runtime; HelioSI is the domain instantiation as a skill graph. This batch supplies new graph nodes; topic bundles (Stage B per spec §6) and the HelioSI graph (Stage C) consume them by `slug` reference only — they do not re-inline content.

## Skills (12 entries)

| # | Slug | Year | Lead | Venue | DOI / arXiv | Core claim (one line) | Tier | Status |
|---|------|------|------|-------|-------------|------------------------|------|--------|
| 1  | `paper-regan-2026-mars-solar-wind-ml-classification`              | 2026 | C. E. Regan | Heliophysics Summer School ML Special Collection (TODO verify) | arXiv 2604.08710 | Unsupervised PCA + K-Means (K=4) on MAVEN multi-feature data recovers slow/fast/intermediate/compressed regimes modulated by solar activity. | pilot | scaffold |
| 2  | `paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml`           | 2026 | A. Sasli | TODO verify | arXiv 2605.00162 | ML pipeline (EMBER) recovers ~93% of modulated ion-acoustic-wave events on PSP burst-mode waveforms and associates them with anomalous core-electron heating. | pilot | scaffold |
| 3  | `paper-rudisser-2022-icme-unet-automatic-detection`               | 2022 | H. T. Rüdisser | TODO verify (likely Space Weather) | arXiv 2205.03578 | U-Net-style 1D segmentation detects ICMEs in Wind 1997–2015 with TSS=0.64 (466/640, 254 FPs); MAE(start)≈2h56min; 20× faster training than baseline. | pilot | scaffold |
| 4  | `paper-camporeale-2017-knn-solar-wind-categorization`             | 2018 | E. Camporeale (TODO verify) | TODO verify (likely JGR Space Physics) | arXiv 1811.02323 | Supervised KNN tops a 10-model benchmark at ~92.8% accuracy on 4-class Xu-Borovsky 1-au labelling. | pilot | scaffold |
| 5  | `paper-bloch-2024-uncertainty-nn-solar-wind-types`                | 2024 | TODO verify | TODO verify | arXiv 2409.09230 | NN classifiers with calibrated uncertainty assign 4-class 1-au labels (coronal hole / streamer belt / sector reversal / solar transients). | pilot | scaffold |
| 6  | `paper-hu-2022-deep-swim-cnn-discontinuities`                     | 2022 | TODO verify | TODO verify | arXiv 2203.01184 | Few-shot CNN ("Deep-SWIM") on 5-min stacked-B-component windows classifies discontinuity vs ambient with limited labelled data. | pilot | scaffold |
| 7  | `paper-cipher-2025-isax-hdbscan-solar-wind-segmentation`          | 2025 | TODO verify | TODO verify | arXiv 2510.21022 | CIPHER: scalable unsupervised iSAX + HDBSCAN + HITL time-series mining for solar-wind structures. | pilot | scaffold |
| 8  | `paper-roy-2025-surya-heliophysics-foundation-model`              | 2025 | S. Roy (IBM/NASA) | TODO verify | arXiv 2508.14112 | Surya — 366 M-parameter spatiotemporal-transformer foundation model on SDO AIA+HMI; time-advancement pretext + LoRA fine-tuning across multiple solar tasks. | pilot | scaffold |
| 9  | `paper-roy-2025-suryabench-ml-benchmark-dataset`                  | 2025 | S. Roy (IBM/NASA) | TODO verify | arXiv 2508.14107 | SuryaBench: ML-ready preprocessed SDO dataset 2010-05–2024-07 with auxiliary labels for six benchmark tasks. | pilot | scaffold |
| 10 | `paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation`    | 2025 | J. A. Grajeda | TODO verify | arXiv 2501.13211 | Magnetic-constrained ACWE EUV coronal-hole segmentation reduces filament FPs and recovers low-intensity CH area. | pilot | scaffold |
| 11 | `paper-koikkalainen-2025-complexity-solar-wind-streams`           | 2025 | V. Koikkalainen | TODO verify | arXiv 2510.05873 | Information-theory complexity (Jensen-Shannon + Fisher-Shannon planes from PE / HVG) differentiates fast / slow / MC / sheath; MCs stand out across metrics. | pilot | scaffold |
| 12 | `paper-katsavrias-2025-periodic-density-structures-solar-orbiter` | 2025 | C. Katsavrias | TODO verify | arXiv 2511.15518 | Multitaper + wavelet PDS catalog on Solar Orbiter shows slow-wind +10% expansion and fast-wind −10% compression of L_R across 0.3–1 au. | pilot | scaffold |

## Topical grouping (compiler view)

- **In-situ supervised classification** at 1 au: skills 4 (KNN baseline), 5 (NN with uncertainty), 6 (few-shot CNN on discontinuities). They share the same Xu–Borovsky / Stansby labelling tradition (where applicable) and form a tier-graded ladder: KNN → NN+uncertainty → CNN-on-windows.
- **In-situ unsupervised classification / segmentation**: skills 1 (PCA+K-Means at Mars), 7 (CIPHER iSAX+HDBSCAN+HITL), 11 (complexity-plane). All three are unsupervised and complementary in *feature space* (raw moments / symbolic / information-theory).
- **In-situ ML event detection**: skills 2 (EMBER mIAW on PSP), 3 (Rüdisser U-Net for ICMEs on Wind/STEREO). Both treat the problem as supervised event detection but at different scales (sub-second waveforms vs hours-long structures).
- **Solar-source image segmentation**: skill 10 (magnetic-constrained ACWE for CHs). Bridges to the PFSS source-mapping batch via the open-field-mask cross-check; downstream consumer of [[paper-roy-2025-suryabench-ml-benchmark-dataset]].
- **Foundation-model + benchmark infrastructure**: skills 8 (Surya), 9 (SuryaBench). The pair is mutually reinforcing — SuryaBench is the natural pretraining + fine-tuning source for Surya; Surya is the natural baseline-beating consumer of SuryaBench.
- **Mesoscale structure cataloging**: skill 12 (Katsavrias PDS catalog on Solar Orbiter). Hybrid statistical-pipeline + radial-evolution result; bridges to the switchback batch (PDSs and switchbacks may share footpoint-source geometry).

## Cross-cutting infrastructure shared with sibling batches

Re-used by reference — these building blocks are candidate Stage-B synthesis skills, **not** duplicated as new paper-skill files in this batch:

- **PSP / Solar Orbiter / Wind / ACE / MAVEN data MCP contracts** — see `batch_heliophysics_software_infrastructure/paper-pyspedas-multimission-data-access/`.
- **SDO AIA + HMI ingestion** — via `paper-sunpy-2023-interoperable-ecosystem` and the SuryaBench preprocessed mirror.
- **Xu–Borovsky 4-class labelling rule** — inherited from Xu & Borovsky 2015 (foundational; not in the inventory).
- **PFSS open-flux mask** — `paper-stansby-2020-pfsspy-python-pfss` (infrastructure batch).
- **NAIF SPICE position kernels** for heliocentric-distance binning — generic dependency; no paper-skill required.
- **HEK / SHARP / GOES catalogs** — generic event archives; treated as fetch endpoints, not skills.

These are proposed contracts. Named MCPs do **not** exist as runtime — the general-purpose harness (Read, Bash, WebFetch + cdflib / sunpy / pyspedas / external ML frameworks) is the only guaranteed surface.

## Weak entries flagged for full-text verification

The "TODO verify" markers across the 12 skills cluster into a handful of categories. The table below highlights the most reproducibility-critical gaps per skill; each one *must* be resolved before any of these can be promoted past `pilot scaffold`.

| Slug | Highest-impact unresolved details |
|------|-----------------------------------|
| `paper-regan-2026-mars-solar-wind-ml-classification` | Exact feature vector; PCA component count + variance threshold; bow-shock model used for upstream selection; solar-activity proxy choice; venue / DOI. |
| `paper-sasli-2026-ember-modulated-ion-acoustic-wave-ml` | Model architecture (CNN / transformer); training-set definition (modulation criterion + encounter list); exact metric reported as 93% (recall / accuracy / F1); SPAN-e calibration version; venue / DOI. |
| `paper-rudisser-2022-icme-unet-automatic-detection` | Reference catalog identity (Richardson-Cane vs Möstl vs union); U-Net depth + loss; feature list; baseline architecture compared for the 20× speedup; operating threshold; venue / DOI. |
| `paper-camporeale-2017-knn-solar-wind-categorization` | Full author list (inventory truncated); feature list; K and distance metric; per-class confusion matrix; venue / DOI. |
| `paper-bloch-2024-uncertainty-nn-solar-wind-types` | Lead author surname + full author list (inventory abstract-only); uncertainty method (MC-Dropout vs ensembles vs evidential); calibration metric (ECE / Brier); operating point on abstention curve; venue / DOI. |
| `paper-hu-2022-deep-swim-cnn-discontinuities` | Full author list (inventory ar5iv mirror); source mission (Wind vs ACE vs Cluster); discontinuity catalog identity; CNN architecture + few-shot paradigm; frame (GSE vs RTN); venue / DOI. |
| `paper-cipher-2025-isax-hdbscan-solar-wind-segmentation` | Full author list; iSAX word length and cardinality; HDBSCAN min_cluster_size; mission used; specific phenomena identified; HITL protocol; venue / DOI. |
| `paper-roy-2025-surya-heliophysics-foundation-model` | Exact 8 AIA + 5 HMI channels; training resolution; spectral-gating implementation; long-short attention pattern; LoRA rank + injected layers; per-task scores + baselines; pretrained-weights URL; venue / DOI. |
| `paper-roy-2025-suryabench-ml-benchmark-dataset` | Preprocessing-algorithm parameters (degradation factors, roll-correction frame); per-task label source; train/val/test split rules per task; canonical hosting URL; per-task baseline scores; venue / DOI. |
| `paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation` | AIA channel (193 vs 211 Å); magnetic-skewness threshold; form of E_magnetic and λ_B weight; convergence rule; ground-truth subset; quantitative FP / area-gain numbers; venue / DOI. |
| `paper-koikkalainen-2025-complexity-solar-wind-streams` | Permutation embedding order d and lag τ; HVG construction details (tie-breaking, despike); stream-type catalog identity; quantitative cluster-separation scores; venue / DOI. |
| `paper-katsavrias-2025-periodic-density-structures-solar-orbiter` | Density product (RPW V_sc vs SWA/PAS); multitaper NW + window length; wavelet mother function; slow/fast threshold; public PDS-catalog URL; per-population L_R-vs-r slope; venue / DOI. |

All twelve are at `pilot scaffold`; none should be promoted to `method-ready+` until the corresponding cell is fully resolved against the published paper PDF.

## Roll-up reproducibility targets

A HelioSI harness consuming this batch should be able to roll the twelve skill outputs into:

- A **comparative ML-baseline table** for 4-class 1-au solar-wind classification — KNN (skill 4) vs NN-with-uncertainty (skill 5) vs Deep-SWIM CNN (skill 6) vs unsupervised PCA+K-Means at Mars (skill 1) vs CIPHER iSAX+HDBSCAN (skill 7) vs complexity-plane features (skill 11) — same labelled subset, same train/val/test split.
- An **event-detection benchmark** comparing the Rüdisser U-Net (skill 3) for ICMEs against complementary structure detectors: PDS catalog (skill 12), Surya-LoRA detector (skill 8 fine-tuned), and CIPHER cluster identifications (skill 7).
- A **solar-wind-source-segmentation panel** combining the Grajeda magnetic-constrained ACWE CH masks (skill 10) with Surya-LoRA CH segmentations (skill 8), cross-checked against PFSS open-flux maps from `batch_pfss_source_mapping/`.
- A **PSP wave-detector survey** that combines EMBER mIAW catalogs (skill 2) with the existing turbulence-batch cyclotron-wave skills ([[bowen-2024-extended-cyclotron-resonant-heating]] from `batch_turbulence_heating_apj/`) to map the full wave-type / heating-channel distribution.
- A **ML-ready data backbone** layer — SuryaBench (skill 9) underneath skill 8 / 10 plus the in-situ data layer ([[paper-pyspedas-multimission-data-access]]) underneath skills 1–7, 11, 12.

## Compilation note (per factory spec §0)

Each SKILL.md is the *agent-native compiled form* of one paper, **not** a summary:

- Section ordering mirrors spec §4: Trigger → claim/task → workflow → tool contracts → validation target → failure modes → claim boundary → links → skill graph.
- All `depends_on` references use the `[[slug]]` convention so unresolved links are visible.
- All `TODO verify` markers are explicit; promotion past `pilot scaffold` requires resolving them against the primary source per spec §8.
- Daemons / future passes MUST NOT overwrite any existing paper-skill file under `pilot_turbulence/`, `pilot_2026_and_runtime/`, `batch_pfss_source_mapping/`, `batch_psp_switchbacks_magnetic/`, `batch_turbulence_heating_apj/`, or `batch_heliophysics_software_infrastructure/`. References to those batches are by `[[slug]]` only.
