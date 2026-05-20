internalization-readiness audit — 501 entries scanned (45 active)
========================================================================
  mean score   : 62.75/100   median: 61.99   min: 42.43   max: 92.0
  active mean  : 63.64   active min: 50.5

  score histogram (lower = more internalization debt):
    0-24       0  
    25-49      8  ###
    50-69    416  ############################################################
    70-84     69  ##################
    85-100     8  ###

  per-batch mean (ascending — worst-debt batch first):
    batch_mission_instruments_data_products              53.22
    wave500_inner_heliosphere_psp_solo_045               55.37
    wave500_solar_corona_cme_flares_045                  57.16
    batch_turbulence_heating_apj                         57.56
    pilot_2026_and_runtime                               58.34
    wave500_sw_classification_ml_foundation_045          60.35
    batch_heliophysics_software_infrastructure           61.05
    batch_solar_wind_segmentation_ml                     62.41
    wave500_waves_instabilities_reconnection_045         62.54
    wave500_agent_runtime_eval_design_045                63.42
    wave500_turbulence_intermit_heating_045              64.68
    wave500_sep_shocks_space_weather_045                 64.9
    wave500_instruments_data_software_045                66.75
    wave500_coronal_source_mapping_pfss_045              67.98
    pilot_turbulence                                     68.85
    batch_psp_switchbacks_magnetic                       69.11
    batch_sep_energetic_particles                        69.37
    batch_pfss_source_mapping                            71.95

  per-quality_level mean (ascending):
    stub-historical-ecosystem-map                    56.23
    pilot_weak_attribution                           59.8
    pilot                                            60.58
    stub-historical-anchor                           62.0
    stub                                             62.11
    paper-grounded-pending-full-text                 62.9
    positioning-skill-not-executable-science         63.24
    stub-infrastructure                              64.33
    method-ready                                     66.07
    link-only-cross-batch                            69.41
    paper-grounded-locally-reproduced                89.22

  worst-debt entries (lowest score first, top 30):
    score  L1  L2  Val L4  Bib Id  TODOs  active  batch/slug
    42.43  25  15   0   3   0   7    10          wave500_waves_instabilities_reconnection_045/klein-2018-multispecies-stability-anisotropy
     47.3  21  15   6   0   6   7    19          batch_mission_instruments_data_products/pulupa-2020-fields-merged-scm-fluxgate-product
    47.67  25   8   0   8   0  10     8          wave500_inner_heliosphere_psp_solo_045/damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind
     47.9  21  15   6   0   6   7    17          batch_mission_instruments_data_products/sinjan-2026-solo-phi-hrt-stray-light-calibration
    48.02  25   8   0   8   0  10     6          wave500_inner_heliosphere_psp_solo_045/schwadron-2022-switchback-deflections-beyond-early-encounters
     48.2  25  20   3   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-so-phi-hrt-vector-magnetogram-radial-distance
    48.61  25  15   5   5   0   7    11          wave500_waves_instabilities_reconnection_045/hcs-reconnection-statistics-psp-encounter-2025
    49.04  25  20   3   3   0   4     9          wave500_solar_corona_cme_flares_045/paper-coronal-plume-substructure-eui-high-cadence
    50.15  25  20   6   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-gong-network-synoptic-magnetogram-product
    50.34  25   8   0  10   0  10     7          wave500_inner_heliosphere_psp_solo_045/bandyopadhyay-2025-helios-mission-archival-reanalysis
     50.4  25   8   0  10   0  10     6          wave500_inner_heliosphere_psp_solo_045/halekas-2024-coronal-heating-switchback-budget-ruled-out
     50.5  21  15   6   5   6   7    25   *      batch_solar_wind_segmentation_ml/paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation
    50.56  25  15   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/free-energy-sources-ion-scale-waves-psp-2025
    50.69  25  15   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/ion-acoustic-velocity-space-signatures-2026
     50.7  21  15  10   0   0  10    11   *      batch_turbulence_heating_apj/bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance
    50.72  25  15   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/whistler-counter-propagating-encounter1-2023
    50.87  25  20   6   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-lasco-c2-c3-streamer-belt-density-radial-profile
    50.96  25  15   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/proton-alpha-aic-driven-instabilities-2023
    50.99  25  20   6   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-mdi-hmi-cross-calibration-synoptic-flux
    50.99  25  20   6   3   0   4     9          wave500_solar_corona_cme_flares_045/paper-suvi-multi-wavelength-temperature-dem-corona
     51.0  21  20   1  10   0   7    20          wave500_sw_classification_ml_foundation_045/paper-trotta-2025-shock-detection-multispacecraft-ml
    51.29  25  20   6   3   0   4    10          wave500_solar_corona_cme_flares_045/paper-source-surface-radius-optimization-eclipse-streamer
    51.35  25  15   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/suprathermal-electron-whistler-scattering-2024
    51.71  25  15   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/ion-driven-instabilities-classification-2023
     51.9  21  20   1  10   0   7    17          wave500_sw_classification_ml_foundation_045/paper-collados-2024-mhd-emulator-coronal-wind
     51.9  21  20   1  10   0   7    17          wave500_sw_classification_ml_foundation_045/paper-davila-2024-shapelet-solar-wind-discontinuities
     51.9  21  20   1  10   0   7    17          wave500_sw_classification_ml_foundation_045/paper-grajeda-2025-acwe-magnetic-ch-extension-radio-microwave
     51.9  21  20   1  10   0   7    17          wave500_sw_classification_ml_foundation_045/paper-jarolim-2024-ch-segmentation-cycle-validation
     51.9  21  20   1  10   0   7    17          wave500_sw_classification_ml_foundation_045/paper-nguyen-2018-ml-icme-detection-svm
     51.9  21  20   1  10   0   7    17          wave500_sw_classification_ml_foundation_045/paper-pal-2024-cir-stream-interaction-region-ml

  legend: L1=Layer-1 claim, L2=Layer-2 protocol, Val=validation,
          L4=Layer-4 affordance, Bib=bibliographic anchor,
          Id=identity, *=active quality_level (debt blocks promotion)