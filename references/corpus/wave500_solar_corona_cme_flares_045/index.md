# Wave: Solar Corona / CMEs / Flares / Coronal Holes / Magnetograms / Remote Sensing / Source-Surface Context (045 skills)

Generated 2026-05-18 by the HelioSI paper-to-skill factory v0.2
(`paper_skill_factory/paper_to_skill_factory_spec.md` +
`harness_agnostic_migration_note.md`). All SKILL.md files in this
wave are **runtime-neutral, four-layer paper-skills**: LingTai,
Claude Code, MCP servers, and plain Python are *adapters*; the
skill is the object.

This wave grows the HelioSI paper/tool-skill corpus from 96 → 141
toward the long-term 500-object target, and is the first wave
strictly themed on solar-corona / CME / flare / coronal-hole /
magnetogram / remote-sensing / source-surface-context content
(prior themed batches covered turbulence/heating, PSP switchbacks,
SEPs, ML segmentation, mission/instrument, software, and a
narrower PFSS source-mapping cluster). All 45 slugs are checked
unique against the existing 96 directories.

## Framing — four-layer compilation

Every SKILL.md in this wave is organized as four explicit layers:

1. **Scientific invariant layer.** Narrow-form claim, method/data
   assumptions, failure modes (skill memory), figure / numerical
   targets, claim boundary. Stable across runtimes.
2. **Executable protocol layer.** A capability-typed procedure that
   names *abstract capabilities* (`pfss.solve`,
   `imagery.fetch_eui_hri`, `extrapolation.solve_nlfff`, ...) —
   never a specific MCP / framework / API. Validation target sits
   here.
3. **Adapter / runtime notes (optional examples).** Concrete
   bindings that *one* runtime might use (e.g. `sunkit-magex`,
   `aiapy`, `stixpy`, MURaM, MAS). Examples only; not requirements.
4. **Research-generation affordances.** Gaps, tensions, hypotheses,
   composable experiments enabled by combining this paper-skill
   with siblings — the layer that lets the corpus *generate research
   direction*.

Many of the skills below are **stubs with explicit TODO markers**
(first-author / venue / DOI / figure metrics to be verified
against full text). Stubs are accepted per spec v0.2; they are
labeled `paper-grounded-pending-full-text` /
`pipeline-specified-not-yet-runnable` in `metadata.yaml` and
`manifest.json`.

## Skills in this wave (45)

### 1. CME kinematics & 3-D reconstruction (6)

| # | Slug | Aspect |
|---|---|---|
| 1 | [paper-thernisien-2011-gcs-fitting-cme-flux-rope](./paper-thernisien-2011-gcs-fitting-cme-flux-rope/SKILL.md) | GCS croissant flux-rope fit |
| 2 | [paper-mierla-2010-3d-cme-reconstruction-stereo-secchi](./paper-mierla-2010-3d-cme-reconstruction-stereo-secchi/SKILL.md) | Reconstruction-method taxonomy |
| 3 | [paper-cme-deflection-non-radial-trajectory](./paper-cme-deflection-non-radial-trajectory/SKILL.md) | Magnetic-pressure deflection |
| 4 | [paper-cme-flux-rope-self-similar-expansion-near-sun](./paper-cme-flux-rope-self-similar-expansion-near-sun/SKILL.md) | Self-similar rope scaling |
| 5 | [paper-cme-true-mass-stereo-cor2-density-inversion](./paper-cme-true-mass-stereo-cor2-density-inversion/SKILL.md) | Thomson-scattering CME mass |
| 6 | [paper-cme-kinematics-three-phase-acceleration-profile](./paper-cme-kinematics-three-phase-acceleration-profile/SKILL.md) | Three-phase a(t) + HXR alignment |

### 2. EUV waves and coronal shocks (5)

| # | Slug | Aspect |
|---|---|---|
| 7 | [paper-eui-euv-wave-fast-mode-mhd-front](./paper-eui-euv-wave-fast-mode-mhd-front/SKILL.md) | Fast-mode classification |
| 8 | [paper-warmuth-2015-large-scale-coronal-waves-review](./paper-warmuth-2015-large-scale-coronal-waves-review/SKILL.md) | Wave taxonomy review |
| 9 | [paper-veronig-2018-eit-wave-dome-shock-3d](./paper-veronig-2018-eit-wave-dome-shock-3d/SKILL.md) | 3-D dome shock geometry |
| 10 | [paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal](./paper-kouloumvakos-2019-cme-shock-3d-pressure-coronal/SKILL.md) | Shock-parameter maps |
| 11 | [paper-shock-driver-standoff-distance-cme-flux-rope](./paper-shock-driver-standoff-distance-cme-flux-rope/SKILL.md) | Bow-shock-analog standoff |

### 3. Flares: topology, ribbons, microflares (7)

| # | Slug | Aspect |
|---|---|---|
| 12 | [paper-cheung-2019-flare-energy-buildup-3d-mhd-active-region](./paper-cheung-2019-flare-energy-buildup-3d-mhd-active-region/SKILL.md) | 3-D radiative MHD flare |
| 13 | [paper-flare-qsl-pre-eruption-topology-decay-index](./paper-flare-qsl-pre-eruption-topology-decay-index/SKILL.md) | QSL + decay-index eruptivity |
| 14 | [paper-aulanier-2012-standard-flare-model-3d-tether-cutting](./paper-aulanier-2012-standard-flare-model-3d-tether-cutting/SKILL.md) | 3-D standard flare model |
| 15 | [paper-flare-ribbon-photospheric-magnetic-shear](./paper-flare-ribbon-photospheric-magnetic-shear/SKILL.md) | Ribbon reconnection flux |
| 16 | [paper-microflare-stix-nonthermal-electron-spectra](./paper-microflare-stix-nonthermal-electron-spectra/SKILL.md) | STIX microflare spectroscopy |
| 17 | [paper-rhessi-hxr-footpoint-asymmetry-flare](./paper-rhessi-hxr-footpoint-asymmetry-flare/SKILL.md) | RHESSI footpoint asymmetry |
| 18 | [paper-flare-forecasting-sharp-features-deep-learning](./paper-flare-forecasting-sharp-features-deep-learning/SKILL.md) | SHARP DL forecasting |

### 4. Coronal holes, jets, plumes, FIP bias (6)

| # | Slug | Aspect |
|---|---|---|
| 19 | [paper-coronal-hole-boundary-detection-suvi-segmentation](./paper-coronal-hole-boundary-detection-suvi-segmentation/SKILL.md) | EUV CH segmentation |
| 20 | [paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure](./paper-cranmer-2017-coronal-hole-acceleration-alfven-wave-pressure/SKILL.md) | Wave-driven CH acceleration |
| 21 | [paper-coronal-hole-jet-population-statistics-aia](./paper-coronal-hole-jet-population-statistics-aia/SKILL.md) | AIA jet population statistics |
| 22 | [paper-coronal-plume-substructure-eui-high-cadence](./paper-coronal-plume-substructure-eui-high-cadence/SKILL.md) | EUI plumelets |
| 23 | [paper-coronal-hole-pseudostreamer-boundary-classification](./paper-coronal-hole-pseudostreamer-boundary-classification/SKILL.md) | CH vs pseudostreamer |
| 24 | [paper-coronal-hole-deep-darkening-elemental-abundance](./paper-coronal-hole-deep-darkening-elemental-abundance/SKILL.md) | FIP bias in deep CH |

### 5. Magnetograms (HMI / MDI / SO-PHI / GONG / farside) (6)

| # | Slug | Aspect |
|---|---|---|
| 25 | [paper-hmi-vector-magnetogram-disambiguation-acute-angle](./paper-hmi-vector-magnetogram-disambiguation-acute-angle/SKILL.md) | HMI 180° disambiguation |
| 26 | [paper-mdi-hmi-cross-calibration-synoptic-flux](./paper-mdi-hmi-cross-calibration-synoptic-flux/SKILL.md) | MDI ↔ HMI cross-cal |
| 27 | [paper-so-phi-hrt-vector-magnetogram-radial-distance](./paper-so-phi-hrt-vector-magnetogram-radial-distance/SKILL.md) | SO/PHI HRT inversion |
| 28 | [paper-helioseismic-farside-detection-acoustic-holography](./paper-helioseismic-farside-detection-acoustic-holography/SKILL.md) | Acoustic-holography farside |
| 29 | [paper-gong-network-synoptic-magnetogram-product](./paper-gong-network-synoptic-magnetogram-product/SKILL.md) | GONG synoptic Br |
| 30 | [paper-magnetogram-noise-floor-quiet-sun-disambiguation](./paper-magnetogram-noise-floor-quiet-sun-disambiguation/SKILL.md) | HMI quiet-Sun noise floor |

### 6. Remote-sensing instruments (EUI/Metis/LASCO/WISPR/SWAP/SUVI/STEREO) (7)

| # | Slug | Aspect |
|---|---|---|
| 31 | [paper-eui-fsi-hri-coronal-bright-points-statistics](./paper-eui-fsi-hri-coronal-bright-points-statistics/SKILL.md) | EUI HRI "campfires" |
| 32 | [paper-metis-coronal-polarized-brightness-electron-density](./paper-metis-coronal-polarized-brightness-electron-density/SKILL.md) | Metis pB → n_e |
| 33 | [paper-lasco-c2-c3-streamer-belt-density-radial-profile](./paper-lasco-c2-c3-streamer-belt-density-radial-profile/SKILL.md) | LASCO streamer density profile |
| 34 | [paper-wispr-tb-imaging-large-scale-coronal-structure](./paper-wispr-tb-imaging-large-scale-coronal-structure/SKILL.md) | WISPR J-map streamer ID |
| 35 | [paper-swap-fov-extended-corona-low-temperature](./paper-swap-fov-extended-corona-low-temperature/SKILL.md) | SWAP wide-FOV corona |
| 36 | [paper-suvi-multi-wavelength-temperature-dem-corona](./paper-suvi-multi-wavelength-temperature-dem-corona/SKILL.md) | SUVI DEM inversion |
| 37 | [paper-stereo-secchi-quadrature-3d-coronal-imaging](./paper-stereo-secchi-quadrature-3d-coronal-imaging/SKILL.md) | STEREO quadrature 3-D imaging |

### 7. Source-surface context, coronal MHD, open-flux problem (8)

| # | Slug | Aspect |
|---|---|---|
| 38 | [paper-arge-2003-wsa-model-source-surface-wind-prediction](./paper-arge-2003-wsa-model-source-surface-wind-prediction/SKILL.md) | WSA solar-wind prediction |
| 39 | [paper-csss-current-sheet-source-surface-non-radial-open-flux](./paper-csss-current-sheet-source-surface-non-radial-open-flux/SKILL.md) | CSSS open-flux |
| 40 | [paper-mas-mhd-global-coronal-thermodynamic-model](./paper-mas-mhd-global-coronal-thermodynamic-model/SKILL.md) | MAS global coronal MHD |
| 41 | [paper-amari-2014-nlfff-vector-magnetogram-extrapolation](./paper-amari-2014-nlfff-vector-magnetogram-extrapolation/SKILL.md) | NLFFF extrapolation family |
| 42 | [paper-titov-demoulin-2014-flux-rope-insertion-eruption](./paper-titov-demoulin-2014-flux-rope-insertion-eruption/SKILL.md) | TDm rope eruption setup |
| 43 | [paper-coronal-mhd-alfven-wave-poynting-flux-base](./paper-coronal-mhd-alfven-wave-poynting-flux-base/SKILL.md) | Coronal-base Poynting flux |
| 44 | [paper-open-flux-problem-in-situ-vs-pfss-discrepancy](./paper-open-flux-problem-in-situ-vs-pfss-discrepancy/SKILL.md) | Open-flux problem |
| 45 | [paper-source-surface-radius-optimization-eclipse-streamer](./paper-source-surface-radius-optimization-eclipse-streamer/SKILL.md) | R_ss optimization |

## Abstract capability surface used in this wave

The wave's Layer-2 protocols name (selectively) the following
abstract capabilities. None are bound to a specific runtime in the
SKILL bodies — runtimes provide their own bindings.

- Imagery: `imagery.fetch_aia`, `imagery.fetch_aia_1600`,
  `imagery.fetch_eui_hri`, `imagery.fetch_eui_fsi`,
  `imagery.fetch_lasco`, `imagery.fetch_stereo_cor2`,
  `imagery.fetch_stereo_euvi`, `imagery.fetch_metis_pb`,
  `imagery.fetch_wispr_l3`, `imagery.fetch_swap_l1`,
  `imagery.fetch_suvi_l2`, `imagery.fetch_xrt`,
  `imagery.fetch_rhessi`, `imagery.fetch_stix_l1`,
  `imagery.fetch_stereo_cor1_cor2`, `imagery.running_diff`,
  `imagery.preprocess_base_diff`,
  `imagery.preprocess_running_diff`,
  `imagery.construct_jmap`, `imagery.stitch_with_aia`,
  `imagery.stix_clean`, `imagery.clean_image`,
  `imagery.map_ribbons_uv`,
  `image.unsharp_filter`, `image.limb_darken_correct`,
  `image.azimuthal_average`,
  `image.straylight_subtract`, `image.straylight_deconvolve`,
  `image.fcorona_subtract_baseline`, `eclipse.fetch_image`
- Geometry / kinematics: `geometry.project_gcs_shell`,
  `geometry.fit_gcs_shell`, `geometry.fit_gcs_trajectory`,
  `geometry.fit_ellipsoid_dome`, `geometry.compute_curvature`,
  `geometry.standoff_distance`, `geometry.tie_point`,
  `geometry.tie_point_3d`,
  `geometry.polarization_ratio`, `geometry.mask_fit`,
  `geometry.forward_model`, `geometry.integrate_mass`,
  `geometry.compare_neutral_line`,
  `kinematics.height_time_extract`,
  `kinematics.derive_velocity_accel`,
  `kinematics.fit_three_phase`, `kinematics.front_track`,
  `kinematics.dome_speed_radial`,
  `kinematics.dome_speed_lateral`
- Coronal field / extrapolation: `pfss.solve`,
  `csss.solve`, `extrapolation.solve_nlfff`,
  `extrapolation.tdm_rope`, `field.expansion_factor`,
  `field.trace_lines`, `field.trace_to_photosphere`,
  `field.integrate_open_flux`, `field.compute_b_from_phi`,
  `field.alfven_map_from_dem_pfss`,
  `field.seed_field_lines`, `topology.compute_q_map`,
  `topology.find_flux_rope`, `topology.compute_decay_index`,
  `topology.classify_boundary`, `topology.find_qsl_footprint`,
  `topology.find_nulls`, `topology.distance_to_boundary`,
  `topology.trace_separators`
- MHD: `mhd.background_field`,
  `mhd.background_alfven_speed`,
  `mhd.global_thermodynamic_solve`,
  `mhd.alfven_wave_turbulence_model`,
  `mhd.alfven_wave_poynting_estimate`,
  `mhd.boundary_alfven_poynting_flux`,
  `mhd.radiative_setup_active_region`,
  `mhd.boundary_driven_flux_emergence`,
  `mhd.run_3d`, `mhd.run_zero_beta`,
  `mhd.setup_flux_rope_equilibrium`,
  `mhd.relax_to_equilibrium`
- Magnetograms / vector: `magnetogram.fetch_los`,
  `magnetogram.fetch_synoptic_br`,
  `magnetogram.fetch_synoptic_mdi`,
  `magnetogram.fetch_synoptic_hmi`,
  `magnetogram.fetch_gong_synoptic`,
  `magnetogram.fetch_earthside_los`,
  `magnetogram.fuse_synchronic`,
  `magnetogram.cospatial_polarity`,
  `magnetogram.sample_at_position`,
  `magnetogram.resample_grid`,
  `magnetogram.qa_polar_fill`,
  `magnetogram.match_pil`,
  `vector_mag.fetch_sharp`, `vector_mag.fetch_sharp_keywords`,
  `vector_mag.fetch_hmi_stokes`,
  `vector_mag.fetch_so_phi_hrt_l2`,
  `vector_mag.preprocess_ff`,
  `vector_mag.invert_vfisv`,
  `vector_mag.invert_milos`,
  `vector_mag.disambiguate_me0`,
  `vector_mag.qa_strength_threshold`
- Detection / morphology / segmentation:
  `detection.coronal_jet_pipeline`,
  `detection.farside_ar`,
  `event.detect_persistent_brightening`,
  `segmentation.threshold_watershed`,
  `morphology.smooth_boundary`,
  `morphology.measure_jet_size`,
  `morphology.identify_offlimb_loop`,
  `morphology.size_lifetime`,
  `morphology.compare_loops`, `morphology.identify_streamer`,
  `mask.quiet_sun`, `footpoint.identify_pair`,
  `ribbon.detect_mask`, `ribbon.accumulate_swept_flux`,
  `tracking.plumelet_segments`, `analysis.transverse_motion`
- Radiation / spectroscopy: `radiation.thomson_invert_density`,
  `radiation.van_de_hulst_invert`, `radiation.fcorona_separate`,
  `spectro.background_subtract`,
  `spectro.forward_fit_thermal_nonthermal`,
  `spectro.power_spectrum_motion`,
  `spectro.fip_ratio`,
  `coronal_dem.invert`, `coronal_dem.compute_alfven_map`,
  `diagnostics.synthesize_euv`, `diagnostics.synthesize_hxr`,
  `diagnostics.synthesize_wl_euv`
- Shock / SEP context: `shock.compute_normal`,
  `shock.compute_mach_compression`
- Calibration: `calibration.fit_linear_saturating`
- Helioseismology: `helioseismology.fetch_dopplergrams`,
  `holography.invert_phase_shift`
- Statistics / metrics:
  `statistics.fit_lognormal`,
  `statistics.spatial_variance`,
  `statistics.time_average_n12`,
  `statistics.substructure_population`,
  `scaling.fit_powerlaw_aspect`,
  `scaling.fit_powerlaw_density`,
  `scaling.fit_two_power_law`,
  `metrics.scatter_residual`,
  `metrics.true_vs_pos_ratio`,
  `metrics.fastmode_consistency`,
  `metrics.method_agreement`,
  `metrics.timing_correlation`,
  `metrics.asymmetry_vs_mirror`,
  `metrics.tss_hss_far`,
  `metrics.iou_vs_reference`,
  `metrics.bow_shock_scaling`,
  `metrics.parameter_vs_sep_onset`,
  `metrics.dome_vs_shock_consistency`,
  `metrics.spectral_fit_quality`,
  `metrics.flux_residual`,
  `metrics.fip_corona_vs_insitu`,
  `metrics.label_agreement`,
  `metrics.observation_match`,
  `metrics.ribbon_footprint_overlap`,
  `metrics.compare_to_cme_flux`,
  `metrics.compare_lasco_kcor`,
  `metrics.compare_aia_dem`,
  `metrics.angular_residual`,
  `metrics.streamer_agreement`,
  `metrics.eclipse_streamer_agreement`,
  `metrics.angular_precision`,
  `metrics.compare_to_awsom_required`,
  `metrics.compare_to_hmi`,
  `metrics.in_situ_vs_pfss_ratio`,
  `metrics.rms_vs_in_situ`,
  `metrics.pfss_vs_csss_delta`,
  `metrics.lorentz_residual`,
  `analysis.free_magnetic_energy`,
  `classification.assign_wave_class`,
  `classification.label_eruptive`,
  `optimization.fit_shell_visual`,
  `optimization.scan_r_ss`,
  `evaluation.cycle_holdout`,
  `ml.train_classifier`,
  `wsa.predict_speed`,
  `ephemeris.spacecraft`, `ephemeris.psp`,
  `literature.aggregate_catalog`,
  `dataset.windowed_supervised`,
  `flare.fetch_hxr_timeprofile`,
  `in_situ.fetch_unsigned_br`,
  `in_situ.fetch_psp_composition`,
  `filesystem.write_report`,
  `farside.infer_br`

Any runtime can bind these — Python + sunpy stack, IDL/SolarSoft,
Julia, FEM/MHD codes, an agent harness with MCPs, or hand-rolled
scripts. The bindings used inside LingTai are documented inside
individual SKILL.md `Layer 3` sections *as examples* and may be
ignored by other runtimes.

## Skill-graph summary

The most-pulled-on Layer-1 invariants in this wave's
`depends_on` edges are:

- `paper-thernisien-2011-gcs-fitting-cme-flux-rope` — depended on by
  CME-mass, self-similar expansion, three-phase kinematics,
  standoff-distance, deflection (the GCS geometry is the
  central glue of the CME-kinematics cluster).
- `paper-amari-2014-nlfff-vector-magnetogram-extrapolation` —
  depended on by QSL/decay-index, Cheung 2019 MHD, Titov-Démoulin
  insertion (all flare-topology skills require an NLFFF starting
  point).
- `paper-hmi-vector-magnetogram-disambiguation-acute-angle` —
  depended on by NLFFF, noise floor, SO/PHI cross-cal, SHARP DL
  forecasting (every vector-magnetogram pipeline must address it).
- `paper-coronal-hole-boundary-detection-suvi-segmentation` —
  depended on by jet statistics, pseudostreamer classification.
- `paper-mas-mhd-global-coronal-thermodynamic-model` — depended on
  by Kouloumvakos shock parameters, AWSoM Poynting flux, the
  ambient-field side of CME deflection.

Cross-wave links touch the prior batches as well:

- `paper-open-flux-problem-in-situ-vs-pfss-discrepancy` →
  `[[paper-pfss-test-problems-solar-stellar-magnetic-fields]]`,
  `[[paper-wu-2026-nonspherical-coronal-magnetic-field-open-flux]]`,
  `[[paper-ai-farside-synchronic-coronal-field-extrapolation]]`
  in `batch_pfss_source_mapping`.
- `paper-flare-forecasting-sharp-features-deep-learning` → the
  `batch_solar_wind_segmentation_ml` ML utilities (transferable
  preprocessing/evaluation infra).
- `paper-wispr-tb-imaging-large-scale-coronal-structure` →
  `[[paper-vourlidas-2016-wispr-imaging-instrument-psp]]` in
  `batch_mission_instruments_data_products`.

## Weak entries needing full-text verification

The vast majority of skills in this wave are explicitly stubbed
with `TODO verify` items in `metadata.yaml` and in the Layer-1
paper-identity / figure-target sections. The wave intentionally
casts a wide net at the **paper-grounded-pending-full-text** tier;
promotion to `method-ready` / `executable` requires full-text
verification of:

- first-author / author list / venue / DOI / arXiv ID per paper
- exact figure / table numerical targets for the validation
  metric
- canonical archive paths for required data products

These items are tracked per-skill in the `weak_entries_needing_full_text_verification` block of `manifest.json`.

## Source inventories

- `sioulas-reproduction/results/arxiv_papers/extended_search.md`
  (PFSS / coronal-extrapolation / source-mapping section)
- `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md`
  (CME / flare / EUI / Metis / WISPR papers)
- `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  (Solar Orbiter / PSP solar-corona papers)
- `sioulas-reproduction/results/arxiv_papers/all_papers_index.json`
  (theme-tagged index)
- `sioulas-reproduction/results/paper_skill_factory/paper_to_skill_factory_spec.md`
  (factory v0.2 spec)
- `sioulas-reproduction/results/paper_skill_factory/harness_agnostic_migration_note.md`
  (v0.1 → v0.2 framing)
- Prior batches under `paper_skill_corpus/` (96 skills, used to
  enforce slug uniqueness in this wave).
