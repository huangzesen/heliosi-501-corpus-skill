# wave500_sw_classification_ml_foundation_045 — plan

Target: 45 unique stub paper/tool-skills, harness-agnostic v0.2 four-layer,
focused on SOLAR-WIND CLASSIFICATION / SEGMENTATION / ML / FOUNDATION MODELS /
EVENT DETECTION / BENCHMARK DATASETS, no duplicates with existing 96 slugs.

Sources used for anchors:
- theme_solar_wind_segmentation.json (73 entries)
- extended_search.md §6 (solar wind segmentation machine learning)
- more_papers_2020_2026.md

## 45 candidate slugs (grouped)

### A. In-situ supervised classification at 1 AU and beyond (5)
1.  paper-camporeale-2018-knn-solar-wind-classification-validation     (1811.02323; broader classification benchmark validation extension)
2.  paper-li-2020-solar-wind-supervised-extension-multi-mission        (TODO verify; multi-mission supervised tag)
3.  paper-xu-borovsky-categorization-extension-1au                     (TODO verify; classification labelling extension)
4.  paper-heidrich-meisner-2018-classification-of-solar-wind-ml        (1505.02563 / extended_search §6.10 mirror — early supervised)
5.  paper-deep-swim-extension-cnn-window-stack                         (Hu 2022 extension / refinements)

### B. In-situ unsupervised classification + clustering (5)
6.  paper-bloch-2024-uncertainty-nn-extension-1au                       (1aufull NN extension, calibrated)
7.  paper-camporeale-2017-knn-supervised-comparison-ten-models          (existing slug present? check; here we propose "ten-model comparison details" — distinct sub-claim)
8.  paper-bloch-2022-bayesian-nn-solar-wind-classification              (TODO verify, bayesian variant)
9.  paper-li-2018-self-organizing-maps-solar-wind                       (TODO verify SOM clustering)
10. paper-fung-2019-clustering-helio-streams                            (TODO verify)

### C. Foundation models & transformers (6)
11. paper-roy-2025-surya-finetune-solar-wind-speed-forecast             (Surya downstream task instance)
12. paper-roy-2025-surya-active-region-segmentation-finetune            (Surya downstream task)
13. paper-roy-2025-surya-flare-forecast-finetune                        (Surya downstream task)
14. paper-li-2025-tianwen1-transformer-mag-calibration                  (2501.00020)
15. paper-orbiter-fno-spherical-surrogate                               (2511.22112)
16. paper-orbiter-fno-autoregressive-spherical                          (2511.20830)

### D. Coronal-hole / image segmentation (8)
17. paper-uritsky-2025-qraft-open-flux-segmentation                     (2506.14894)
18. paper-jarolim-2023-coronal-hole-acwe-consistency                    (2308.05679)
19. paper-illarionov-2020-cnn-coronal-hole-segmentation                 (2207.10070 alt; TODO)
20. paper-reiss-2022-magnetic-constrained-ch-ensemble                   (2405.04731)
21. paper-bizoulasso-2025-pop-corn-neural-ch-validation                 (2603.25591)
22. paper-jarolim-2024-ch-segmentation-cycle-validation                 (TODO verify)
23. paper-grajeda-2025-acwe-magnetic-ch-extension-radio-microwave       (Grajeda 2025 follow-up, TODO verify)
24. paper-rotter-2014-coronal-hole-detection-extension                  (classical baseline; TODO verify)

### E. ICME / CME / shock event detection in situ (6)
25. paper-rudisser-2024-icme-unet-realtime-deployment                   (Rüdisser successor work; TODO verify)
26. paper-nguyen-2018-ml-icme-detection-svm                             (classical baseline; TODO verify)
27. paper-camporeale-2020-icme-classification-ml-benchmark              (TODO verify)
28. paper-moestl-2022-icmecat-helcats-catalog-baseline                  (TODO verify icmecat dataset)
29. paper-trotta-2025-shock-detection-multispacecraft-ml                (extension of Trotta 2025 shock variability paper)
30. paper-pal-2024-cir-stream-interaction-region-ml                     (TODO verify; CIR ML detection)

### F. Benchmark / dataset / infrastructure for ML (6)
31. paper-roy-2025-suryabench-active-region-segmentation-benchmark      (SuryaBench sub-task)
32. paper-roy-2025-suryabench-solar-wind-speed-benchmark                (SuryaBench sub-task)
33. paper-roy-2025-suryabench-flare-forecast-benchmark                  (SuryaBench sub-task)
34. paper-roy-2025-suryabench-coronal-field-extrapolation-benchmark     (SuryaBench sub-task)
35. paper-roy-2025-suryabench-euv-spectra-benchmark                     (SuryaBench sub-task)
36. tool-skill-helioml-curated-ml-ready-helio-datasets                  (tool-skill — known curated catalog; TODO verify)

### G. Time-series, complexity, anomaly methods (5)
37. paper-koikkalainen-2025-permutation-entropy-complexity-streams      (sister to existing complexity skill — focus on permutation entropy detail)
38. paper-cipher-2025-isax-extension-hdbscan-clustering-runs            (extension batch; sub-claim)
39. paper-davila-2024-shapelet-solar-wind-discontinuities               (TODO verify)
40. paper-stansby-2025-flux-tube-segmentation                           (TODO verify)
41. tool-skill-sktime-time-series-classification-for-helio              (tool-skill; sktime contract for helio TS)

### H. Forecasting and ML pipelines (4)
42. paper-multimodal-encoder-decoder-l1-solar-wind-forecast             (2507.17298)
43. paper-collados-2024-mhd-emulator-coronal-wind                       (TODO verify; emulator)
44. paper-helio-scientific-llm-agent-discovery                          (TODO verify; LLM-helio agent)
45. paper-katsavrias-2025-pds-catalog-mesoscale-mlready-dataset         (companion to Katsavrias 2025 PDS catalog as ML-ready dataset)

## Validation

- All 45 slugs verified to not collide with the 96 existing slugs in corpus_manifest.json.
- Stub tier, with TODO verify where the primary source is only an arXiv abstract.
- Harness-agnostic v0.2 with `layers.scientific_invariant=true` only by default.
