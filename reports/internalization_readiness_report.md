internalization-readiness audit — 501 entries scanned (45 active)
========================================================================
  mean score   : 62.08/100   median: 62.1   min: 42.43   max: 92.0
  active mean  : 66.7   active min: 50.5

  score histogram (lower = more internalization debt):
    0-24       0  
    25-49     33  #########
    50-69    402  ############################################################
    70-84     58  ###############
    85-100     8  ###

  per-batch mean (ascending — worst-debt batch first):
    wave500_inner_heliosphere_psp_solo_045               50.37
    wave500_solar_corona_cme_flares_045                  55.09
    wave500_sw_classification_ml_foundation_045          57.55
    pilot_2026_and_runtime                               58.34
    batch_solar_wind_segmentation_ml                     62.41
    wave500_waves_instabilities_reconnection_045         62.54
    wave500_agent_runtime_eval_design_045                63.42
    batch_heliophysics_software_infrastructure           63.82
    batch_turbulence_heating_apj                         64.14
    wave500_turbulence_intermit_heating_045              64.68
    wave500_sep_shocks_space_weather_045                 64.9
    batch_sep_energetic_particles                        65.2
    wave500_coronal_source_mapping_pfss_045              65.55
    wave500_instruments_data_software_045                67.48
    batch_mission_instruments_data_products              67.89
    batch_pfss_source_mapping                            67.95
    batch_psp_switchbacks_magnetic                       68.69
    pilot_turbulence                                     69.56

  per-quality_level mean (ascending):
    stub-historical-ecosystem-map                    56.23
    pilot_weak_attribution                           59.8
    stub                                             61.32
    paper-grounded-pending-full-text                 61.46
    stub-historical-anchor                           62.0
    positioning-skill-not-executable-science         63.24
    pilot                                            63.68
    stub-infrastructure                              64.33
    method-ready                                     69.38
    link-only-cross-batch                            69.41
    paper-grounded-locally-reproduced                89.22

  anti-pattern counts (per-entry bit fires; see reports/skill_quality_alignment_audit.md §4.9):
    L1 boilerplate ("pending full-text verification")           : 12
    L2 boilerplate or layer2_stub flag                          : 100
    L4 boilerplate (promotion-plan-only / adapter-empty)        : 42
    L4 affordances flag/count mismatch (present:true, no list)  : 136

  worst-debt entries (lowest score first, top 30):
    score  L1  L2  Val L4  Bib Id  TODOs  active  batch/slug
    42.43  25  15   0   3   0   7    10          wave500_waves_instabilities_reconnection_045/klein-2018-multispecies-stability-anisotropy
    42.67  25   8   0   3   0  10     8          wave500_inner_heliosphere_psp_solo_045/damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind
    43.02  25   8   0   3   0  10     6          wave500_inner_heliosphere_psp_solo_045/schwadron-2022-switchback-deflections-beyond-early-encounters
    45.34  25   8   0   5   0  10     7          wave500_inner_heliosphere_psp_solo_045/bandyopadhyay-2025-helios-mission-archival-reanalysis
     45.4  25   8   0   5   0  10     6          wave500_inner_heliosphere_psp_solo_045/halekas-2024-coronal-heating-switchback-budget-ruled-out
     48.0  21  20   1   7   0   7    20          wave500_sw_classification_ml_foundation_045/paper-trotta-2025-shock-detection-multispacecraft-ml
    48.21  25  20   3   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-rhessi-hxr-footpoint-asymmetry-flare
     48.3  25  20   3   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-coronal-hole-jet-population-statistics-aia
    48.55  25  20   3   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-coronal-hole-deep-darkening-elemental-abundance
    48.61  25  15   5   5   0   7    11          wave500_waves_instabilities_reconnection_045/hcs-reconnection-statistics-psp-encounter-2025
    48.65  25   8   0   3   6  10     7          wave500_inner_heliosphere_psp_solo_045/sun-2024-magnetic-island-wispr-psp
     48.7  25   8   0   3   6  10     8          wave500_inner_heliosphere_psp_solo_045/sun-2026-compound-reconnection-exhaust-mirror-modes-hcs
     48.9  21  20   1   7   0   7    17          wave500_sw_classification_ml_foundation_045/paper-collados-2024-mhd-emulator-coronal-wind
     48.9  21  20   1   7   0   7    17          wave500_sw_classification_ml_foundation_045/paper-davila-2024-shapelet-solar-wind-discontinuities
     48.9  21  20   1   7   0   7    17          wave500_sw_classification_ml_foundation_045/paper-grajeda-2025-acwe-magnetic-ch-extension-radio-microwave
     48.9  21  20   1   7   0   7    17          wave500_sw_classification_ml_foundation_045/paper-jarolim-2024-ch-segmentation-cycle-validation
     48.9  21  20   1   7   0   7    17          wave500_sw_classification_ml_foundation_045/paper-nguyen-2018-ml-icme-detection-svm
     48.9  21  20   1   7   0   7    17          wave500_sw_classification_ml_foundation_045/paper-pal-2024-cir-stream-interaction-region-ml
    49.24  25   8   0   3   6  10     6          wave500_inner_heliosphere_psp_solo_045/verniero-2023-proton-alpha-instabilities-ion-cyclotron-wave-event
    49.29  25   8   0   3   6  10     6          wave500_inner_heliosphere_psp_solo_045/ofman-2025-large-scale-kelvin-helmholtz-cme-driven
     49.3  25   8   0   3   6  10     6          wave500_inner_heliosphere_psp_solo_045/zhao-2025-mode-composition-magnetic-anisotropy-solar-wind
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-bloch-2022-bayesian-nn-solar-wind-classification
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-camporeale-2020-icme-classification-ml-benchmark
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-deep-swim-extension-cnn-window-stack
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-fung-2019-clustering-helio-streams
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-helio-scientific-llm-agent-discovery
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-li-2018-self-organizing-maps-solar-wind
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-moestl-2022-icmecat-helcats-catalog-baseline
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-rotter-2014-coronal-hole-detection-extension
     49.8  21  20   1   7   0   7    14          wave500_sw_classification_ml_foundation_045/paper-stansby-2025-flux-tube-segmentation

  legend: L1=Layer-1 claim, L2=Layer-2 protocol, Val=validation,
          L4=Layer-4 affordance, Bib=bibliographic anchor,
          Id=identity, *=active quality_level (debt blocks promotion)