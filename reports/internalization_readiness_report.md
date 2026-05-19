internalization-readiness audit — 501 entries scanned (51 active)
========================================================================
  mean score   : 61.01/100   median: 61.34   min: 24.14   max: 84.53
  active mean  : 62.01   active min: 50.5

  score histogram (lower = more internalization debt):
    0-24       1  #
    25-49     21  ######
    50-69    425  ############################################################
    70-84     54  ##############
    85-100     0  

  per-batch mean (ascending — worst-debt batch first):
    batch_mission_instruments_data_products              53.22
    batch_solar_wind_segmentation_ml                     53.64
    wave500_waves_instabilities_reconnection_045         53.7
    wave500_inner_heliosphere_psp_solo_045               55.37
    wave500_solar_corona_cme_flares_045                  57.16
    batch_turbulence_heating_apj                         57.56
    pilot_2026_and_runtime                               58.34
    wave500_turbulence_intermit_heating_045              58.48
    wave500_sw_classification_ml_foundation_045          58.77
    batch_heliophysics_software_infrastructure           61.05
    wave500_agent_runtime_eval_design_045                63.42
    wave500_sep_shocks_space_weather_045                 64.9
    wave500_instruments_data_software_045                66.75
    wave500_coronal_source_mapping_pfss_045              67.98
    pilot_turbulence                                     68.85
    batch_psp_switchbacks_magnetic                       69.11
    batch_sep_energetic_particles                        69.37
    batch_pfss_source_mapping                            70.1

  per-quality_level mean (ascending):
    stub-historical-ecosystem-map                    56.23
    stub                                             58.66
    pilot                                            58.98
    pilot_weak_attribution                           59.8
    paper-grounded-pending-full-text                 61.97
    stub-historical-anchor                           62.0
    positioning-skill-not-executable-science         63.24
    stub-infrastructure                              64.33
    method-ready                                     66.07
    link-only-cross-batch                            69.41
    paper-grounded-locally-reproduced                70.73

  worst-debt entries (lowest score first, top 30):
    score  L1  L2  Val L4  Bib Id  TODOs  active  batch/slug
    24.14  20   3   0   3   0   7    11          wave500_waves_instabilities_reconnection_045/chandran-2010-stochastic-heating-perp-alfven
    37.53  16   0   1   8  12  10    11          wave500_turbulence_intermit_heating_045/paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp
    38.06  16   0   1   8  12  10    10          wave500_turbulence_intermit_heating_045/paper-cuesta-2022-intermittency-psp-helios-voyager
    38.65  16   0   1   8  12  10     9          wave500_turbulence_intermit_heating_045/paper-andres-2021-incompressible-cascade-anisotropic-pp
    39.23  25   3   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/kelvin-helmholtz-cme-large-scale-2025
    39.37  25   3   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/oblique-drift-instability-solar-wind-heating-2025
    39.46  25   3   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/interchange-reconnection-pseudostreamer-metis-2025
    39.51  25   3   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/wave-particle-equilibria-heavy-ions-2026
    39.53  25   3   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/ion-acoustic-damping-instability-solo-2026
    39.56  25   3   0   3   6   7     6          wave500_waves_instabilities_reconnection_045/anti-equilibrium-alfven-ion-cyclotron-effects-2023
    39.96  16   0   1   8  12  10     8          wave500_turbulence_intermit_heating_045/paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution
    41.62  25   3   0   5   6   7     6          wave500_waves_instabilities_reconnection_045/rotational-discontinuity-proton-beam-generation-2025
    41.69  25   3   0   5   6   7     6          wave500_waves_instabilities_reconnection_045/stochastic-heating-sub-alfvenic-2025
    41.82  25   3   0   5   6   7     6          wave500_waves_instabilities_reconnection_045/regulation-proton-alpha-flow-compressive-2023
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

  legend: L1=Layer-1 claim, L2=Layer-2 protocol, Val=validation,
          L4=Layer-4 affordance, Bib=bibliographic anchor,
          Id=identity, *=active quality_level (debt blocks promotion)