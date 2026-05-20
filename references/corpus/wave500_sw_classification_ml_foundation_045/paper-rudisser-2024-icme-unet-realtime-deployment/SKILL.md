---
name: paper-rudisser-2024-icme-unet-realtime-deployment
description: >-
  Use when deploying a deep-learning ICME detector against near-real-time
  Wind RTSW telemetry with operational latency budgets — central paper claim is
  the ARCANE ResUNet++ early-detection framework attains F1 = 0.37 with an
  average detection delay of 24.5% of event duration, outperforming a
  threshold-based baseline especially on high-impact events (Rüdisser et al.
  2026, Space Weather, doi:10.1029/2025SW004537, arXiv:2505.09365).
version: 0.1.0
kind: paper-skill
quality: stub
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: false
  adapter_binding_examples: false
  research_generation_affordance: false
paper:
  title: "ARCANE — Early Detection of Interplanetary Coronal Mass Ejections"
  first_author: "H. T. Rüdisser"
  authors:
    - "H. T. Rüdisser"
    - "G. Nguyen"
    - "J. Le Louëdec"
    - "E. E. Davies"
    - "C. Möstl"
  authors_verified: false
  year: 2026
  venue: "Space Weather, 24, e2025SW004537"
  doi: "10.1029/2025SW004537"
  arxiv_id: "2505.09365"
  ads_bibcode: null
domain:
  primary_theme: solar_wind_segmentation
  secondary_themes: ["event-detection", "icme", "deep-learning", "real-time", "operational"]
  missions: ["Wind"]
  regime: ["1au"]
trigger_keywords: ["icme", "arcane", "resunet", "event-detection", "real-time", "rtsw", "wind", "early-detection", "operational"]
data_products: []
algorithms: []
validation_target: null
links:
  doi_url: "https://doi.org/10.1029/2025SW004537"
  arxiv_url: "https://arxiv.org/abs/2505.09365"
  ads_url: null
  code_repo: null
  data_repo: null
claim_boundary:
  scope: >-
    Rüdisser et al. (2026, ARCANE) demonstrate the first deep-learning
    framework explicitly designed for early ICME detection in streaming
    solar-wind data under realistic operational constraints. The model
    is a ResUNet++ trained on Wind solar-wind time series; the evaluator
    operates on partial / not-yet-complete events using real-time solar
    wind (RTSW) inputs and is shown to retain performance versus
    high-resolution science data. Headline metrics: F1 = 0.37 across the
    full event population; average detection delay = 24.5% of event
    duration; outperforms a threshold-based baseline especially on
    high-impact events.
  out_of_scope:
    - "Do NOT generalise ARCANE detections to STEREO / Solar Orbiter without retraining — the published evaluator is anchored to Wind/RTSW; multi-mission framing in the slug name is a research-affordance label, not a paper-side claim."
    - "Do NOT interpret F1 = 0.37 as a model-quality ceiling — it is the operational early-detection metric (detection on partial event data), which is much harder than retrospective full-event detection."
    - "Do NOT bind the executable protocol to a specific runtime / MCP / plugin until method-ready promotion."
failure_modes:
  - "Slug year mismatch. The slug encodes '2024' but the verified primary source is arXiv:2505.09365 (May 2025 preprint, Space Weather 2026, doi:10.1029/2025SW004537). The slug name is preserved for stable cross-references; consumers should treat the bibliographic block (year=2026) as authoritative."
  - "Architecture mismatch. The original stub description said 'U-Net'; the verified paper uses ResUNet++ — a residual variant with attention/squeeze-and-excitation modules. Treating ARCANE as a vanilla U-Net misrepresents the architecture."
  - "Metric-context confusion. F1 = 0.37 is the early-detection metric on partial event data; comparing to retrospective full-event detectors (e.g. Nguyen et al. 2019 CNN reported F1 ≈ 0.74 retrospective) is an apples-to-oranges comparison."
  - "Cross-mission overreach. The published evaluator is Wind-only; the slug's 'Wind / STEREO / Solar Orbiter' title (preserved for stable cross-references) is a research-affordance label, not a paper-side claim."
  - "Adapter leakage risk at promotion. When Layer 2 is populated, ensure no runtime / MCP / plugin name appears in §3 / §4 / §5; all such names belong in `adapter_notes[]`."
  - "Slug-stability contract. Once this slug is referenced by another paper-skill via `depends_on`, it must not be renamed without a `provenance` audit entry."
depends_on: ["paper-rudisser-2022-icme-unet-automatic-detection"]
adapter_notes: []
research_generation_affordances:
  - type: gap
    statement: "Per-event-bin breakdown of F1 (e.g. high-Bz vs low-Bz events, fast vs slow ICMEs) is not yet anchored; the abstract reports overall F1 and average detection delay, but the operational utility depends on the per-event-bin performance."
    related_skills: ["paper-rudisser-2022-icme-unet-automatic-detection"]
    proposed_action: "Read §4 of Rüdisser et al. 2026, transcribe per-event-bin metrics into validation_target, and add a research affordance for per-bin reproduction."
  - type: minimal_experiment
    statement: "Replay ARCANE on a held-out Wind/RTSW window (e.g. 2024 H1) and confirm the early-detection F1 and average detection-delay-fraction fall within the published tolerance (TODO_verify_with_full_text)."
    related_skills: ["paper-rudisser-2022-icme-unet-automatic-detection"]
    proposed_action: "Fetch Wind RTSW for the held-out window, run the ResUNet++ inference path, and compare F1 / delay-fraction."
  - type: cross_mission_extension
    statement: "The slug's 'Wind / STEREO / Solar Orbiter' framing suggests a cross-mission generalisation that the paper does not claim. Retraining ARCANE on STEREO/IMPACT+PLASTIC and Solar Orbiter/MAG+SWA telemetry would test whether the architecture transfers."
    related_skills: []
    proposed_action: "Retrain on each mission's RTSW analogue and report cross-mission F1 / detection-delay-fraction matrix."
provenance:
  generated_by: "HelioSI paper-to-skill factory (wave500 batch, 2026-05-18, Claude Code)"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_solar_wind_segmentation.json"
  verified_by: "Claude Code internalization session (bibliographic anchor web-verified via AGU + arXiv)"
  verified_at: "2026-05-19T00:00:00Z"
tags: [heliophysics, paper-skill, solar-wind-classification, stub]
---

# ARCANE — early-detection ICME detector on Wind RTSW telemetry (ResUNet++) — paper-skill (stub)

> Anchored in Rüdisser, H. T., Nguyen, G., Le Louëdec, J., Davies, E. E., Möstl, C. (2026), "ARCANE — Early Detection of Interplanetary Coronal Mass Ejections", *Space Weather*, 24, e2025SW004537, doi:10.1029/2025SW004537, arXiv:2505.09365. Bibliographic anchor web-verified 2026-05-19. The slug name encodes year '2024' for stable cross-references, but the verified primary source is the 2026 journal article (2025 preprint).
> **Quality tier**: `stub` — Layer 1 is populated against the verified abstract; Layer 2 (executable protocol) requires reading §3-§4 to transcribe the ResUNet++ architecture, training data window, and per-event-bin metrics.
>
> **Four-layer reminder (spec §4)**:
> - L1 (scientific invariant) → §1, §2, §6, §7
> - L2 (executable protocol, abstract contracts) → §3, §4, §5 — *populated at method-ready promotion*
> - L3 (adapter examples, optional) → §8 sub-block + `adapter_notes[]` — *empty at stub*
> - L4 (research-generation affordance) → §9 sub-block + `research_generation_affordances[]`

This file is the agent-native compiled form of the paper above, **not a summary**.
At stub tier Layer 1 is anchored in the verified abstract; Layer 2 and Layer 3 are intentionally
left as TODOs for promotion.

---

## 1. Trigger  *(Layer 1)*

A future agent should reach for this skill when:

- Building an operational ICME alerting pipeline that consumes Wind RTSW telemetry and must emit detections before an event has fully passed the spacecraft.
- Comparing a near-real-time deep-learning detector against a threshold-based operational baseline for ICME alerting.
- Selecting a ResUNet++ architecture (rather than a vanilla U-Net) for streaming-mode segmentation on multivariate solar-wind time series.
- Benchmarking early-detection metrics (partial-event F1, average detection-delay-fraction) rather than retrospective full-event metrics.

Do NOT use this skill when:

- The task is retrospective full-event ICME detection — that is the regime of the predecessor `[[paper-rudisser-2022-icme-unet-automatic-detection]]`, not ARCANE.
- The task requires cross-mission performance estimates (STEREO / Solar Orbiter) — the published evaluator is Wind-only.
- The task crosses the claim-boundary scope below (§7).

## 2. Paper claim → verifiable task  *(Layer 1)*

**Claim (narrow form).** ARCANE is the first deep-learning framework explicitly designed for early ICME detection in streaming Wind/RTSW solar-wind data under realistic operational constraints. A ResUNet++ segmenter trained on Wind solar-wind time series attains overall F1 = 0.37 on early detection, with an average detection delay of 24.5% of event duration, while running on real-time RTSW inputs with minimal performance loss vs high-resolution science data. ARCANE outperforms a threshold-based baseline, especially on high-impact events.

**Verifiable task.** Reproduce the headline operational metrics:
- Fetch Wind RTSW telemetry over a held-out evaluation window (TODO_verify_with_full_text — exact dates).
- Apply the ResUNet++ inference path (architecture details TODO_verify_with_full_text against §3).
- Score early-detection F1 against the ground-truth ICME catalog (catalog version TODO_verify_with_full_text).
- Measure the average detection-delay-fraction (delay / event duration) and confirm it lands near 24.5% (tolerance TODO_verify_with_full_text against §4 tables).
- Run the threshold-based baseline on the same window and confirm ARCANE's outperformance is concentrated in the high-impact-event subset.

## 3. Methods / equations → executable protocol  *(Layer 2, abstract — STUB)*

Layer 2 is sketched conceptually here; explicit hyperparameters are pending re-read of §3-§4:

1. **Architecture.** ResUNet++ (residual U-Net with squeeze-and-excitation / attention blocks). Layer count, channel widths, and bottleneck depth: TODO_verify_with_full_text against §3.
2. **Inputs.** Multivariate Wind solar-wind time series: B magnitude + components (B_x, B_y, B_z in GSE), proton bulk speed (v_sw), proton density (n_p), proton temperature (T_p). Exact feature list and any derived features (e.g. v_A, plasma beta) TODO_verify_with_full_text against §3.
3. **Training data window.** Wind in-situ observations (period TODO_verify_with_full_text against §3); ground-truth labels from ICMECAT/HELCATS (catalog version TODO_verify_with_full_text).
4. **Streaming evaluator.** The operational evaluator scores detections on partial event windows (event still in progress); the metric is "detection at the first sample where the model crosses a threshold", not "detection at end of event". Threshold choice and any smoothing TODO_verify_with_full_text against §4.
5. **Baseline.** A threshold-based detector on a small set of solar-wind features (identity TODO_verify_with_full_text against §4) is used as the operational comparator.

Do not bind to a specific runtime / MCP / plugin in this section — keep all bindings in §8 (`adapter_notes`).

## 4. Data / instruments → abstract tool contracts  *(Layer 2, abstract — STUB)*

Pending method-ready promotion, the required data products:

- **Wind RTSW** (real-time solar wind): magnetic field + plasma at the near-real-time cadence broadcast by the Wind operational pipeline. Capability: stream-mode fetch + decode; align field and plasma to a common grid; handle gaps.
- **Wind L2 high-resolution** science data: post-processed magnetic field (MFI) and plasma (SWE) at full cadence; used as a comparator to confirm minimal RTSW-vs-science performance gap.
- **ICMECAT / HELCATS** ICME catalog: ground-truth event windows for training and evaluation. Exact catalog version TODO_verify_with_full_text.

Empty `data_products[]` in frontmatter is acceptable at stub tier.

## 5. Validation target → benchmark artifact  *(Layer 2 — STUB)*

> Validation target: **early-detection F1 = 0.37 and average detection-delay-fraction = 24.5% of event duration**, both measured on the held-out evaluation window of ARCANE §4 (TODO_verify_with_full_text — exact dates and per-event-bin breakdown). Promotion to `executable` requires setting `validation_target.metric = "early_detection_f1"`, `validation_target.target = 0.37` (TODO_verify_with_full_text), and a numeric tolerance per §4 tables.

## 6. Failure modes → skill memory  *(Layer 1)*

- **Slug year mismatch.** The slug encodes year `2024`; the verified primary source is arXiv:2505.09365 (May 2025 preprint, Space Weather 2026). The bibliographic block is authoritative; the slug name is kept stable for cross-references.
- **Architecture mismatch.** The slug description said "U-Net"; ARCANE is **ResUNet++**, a residual variant with attention modules. Treat the slug-name "unet" tail as a label, not a literal architecture descriptor.
- **Metric-context confusion.** F1 = 0.37 is the **early-detection** metric on partial event data; do not compare it head-to-head with retrospective full-event detectors (which routinely report higher F1 because they see complete events).
- **Cross-mission overreach.** The evaluator is **Wind-only**; the slug title's "Wind / STEREO / Solar Orbiter" is a research-affordance framing, not a paper-side claim.
- **Adapter leakage risk at promotion.** When Layer 2 is populated, ensure no runtime / MCP / plugin name appears in §3 / §4 / §5; all such names belong in `adapter_notes[]`.
- **Slug-stability contract.** Once this slug is referenced by another paper-skill via `depends_on`, it must not be renamed without a `provenance` audit entry.

## 7. Claim boundary  *(Layer 1)*

**In scope.** Early-detection of ICMEs on Wind RTSW telemetry using a ResUNet++ deep segmentation network; operational evaluation under streaming constraints; comparison vs threshold-based baseline; published headline metrics F1 = 0.37 and average detection-delay-fraction = 24.5% of event duration.

**Out of scope — do NOT generalise beyond:**

- Multi-mission generalisation (STEREO, Solar Orbiter) — the published evaluator is Wind-only.
- Retrospective full-event ICME detection — that is the regime of the predecessor paper, not ARCANE.
- Distances substantially away from 1 au — Wind is at L1.
- Any runtime / MCP / plugin assumption — this skill is harness-agnostic; bindings live in `adapter_notes[]`.

If a downstream task asks for a generalisation listed above, refuse it and return a reference to a sibling paper-skill that covers it (or report none).

## 8. Links and adapter binding examples  *(Layer 3, optional — empty at stub)*

**Canonical links to the published artifact:**

- DOI: https://doi.org/10.1029/2025SW004537
- arXiv: https://arxiv.org/abs/2505.09365
- ADS: n/a — bibcode not yet resolved.
- Code: n/a — public reference implementation not yet anchored at stub tier.
- Data: Wind RTSW (operational Wind pipeline); Wind/MFI + Wind/SWE L2 (SPDF/CDAWeb); ICMECAT/HELCATS ground-truth catalog.

**Adapter binding examples (optional, illustrative only):** none recorded at stub tier;
`adapter_notes[]` is intentionally empty.

## 9. Skill graph + research-generation affordances  *(Layer 4 and graph edges)*

**Skill graph (depends_on edges).** This paper-skill builds on:

- `[[paper-rudisser-2022-icme-unet-automatic-detection]]` — the retrospective full-event U-Net ICME detector that established the U-Net family for ICME segmentation; ARCANE replaces it with ResUNet++ and the streaming-mode evaluator.

**Research-generation affordances.** Forward-pointing surface of the skill (spec §4 Layer 4):

- **Gap** — Per-event-bin F1 breakdown (high-Bz vs low-Bz events, fast vs slow ICMEs) is not yet anchored; operational utility hinges on per-bin performance.
- **Minimal experiment** — Replay ARCANE on a held-out Wind/RTSW window and confirm early-detection F1 and delay-fraction lie within the published tolerance.
- **Cross-mission extension** — Retrain on STEREO/IMPACT+PLASTIC and Solar Orbiter/MAG+SWA RTSW analogues and report the cross-mission F1 / detection-delay-fraction matrix. (This is a research target; the original paper does not claim cross-mission performance.)
- **Open question** — Whether the ResUNet++ architecture confers a measurable gain over vanilla U-Net under matched streaming constraints, or whether the gain reported in §4 vs the threshold baseline is dominated by the streaming evaluator design rather than the architecture choice.

## Notes

This slug is the verified anchor for the **ARCANE** paper (Rüdisser, Nguyen, Le Louëdec, Davies, Möstl 2026, Space Weather, doi:10.1029/2025SW004537, arXiv:2505.09365). The slug name encodes year `2024` and "U-Net" for stable cross-references, but the verified primary source is a **2026** Space Weather paper using **ResUNet++**, not a 2024 vanilla U-Net article. See failure_modes for the year/architecture-mismatch caveats.
