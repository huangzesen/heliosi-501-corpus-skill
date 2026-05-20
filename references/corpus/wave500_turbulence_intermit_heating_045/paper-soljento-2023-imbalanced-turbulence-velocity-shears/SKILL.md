---
name: paper-soljento-2023-imbalanced-turbulence-velocity-shears
description: >-
  Use when characterising how large-scale velocity shears in the solar wind
  modify Alfvénic-imbalance signatures of the inertial-range cascade —
  Soljento, Good, Osmane, Kilpua 2023 (ApJL 945, L20) analyse 74 ICME-sheath
  shears observed by Wind at 1 au and find that shears exceeding the
  Kelvin–Helmholtz instability threshold drive fluctuations toward a balanced
  state with rising magnetic compressibility.
version: 0.2.0
kind: paper-skill
quality: paper-grounded-pending-full-text
harness_agnostic: true
layers:
  scientific_invariant: true
  executable_protocol: true
  adapter_binding_examples: false
  research_generation_affordance: true
paper:
  title: "Imbalanced Turbulence Modified by Large-scale Velocity Shears in the Solar Wind"
  first_author: "Soljento, J. E."
  authors:
    - "Juska E. Soljento"
    - "Simon W. Good"
    - "Adnane Osmane"
    - "Emilia K. J. Kilpua"
  year: 2023
  venue: "Astrophysical Journal Letters (DOI 10.3847/2041-8213/acc071)"
  doi: "10.3847/2041-8213/acc071"
  arxiv_id: "2303.04006"
  ads_bibcode: null
  identity_uncertainty: >-
    Full ApJL volume/article-number string not independently re-verified;
    the DOI 10.3847/2041-8213/acc071 resolves to the published ApJL record
    (accepted 2023-03-02 per arXiv landing). ADS bibcode is not asserted
    here.
domain:
  primary_theme: turbulence
  secondary_themes: [imbalanced, velocity-shear, ICME-sheath, Kelvin-Helmholtz, large-scale]
  missions: [Wind]
  regime: [1au, MHD-scale, ICME-sheath]
trigger_keywords:
  - "velocity shear imbalance"
  - "ICME sheath turbulence"
  - "Kelvin-Helmholtz threshold"
  - "cross helicity sigma_c"
  - "Elsasser ratio z+ z-"
  - "balanced state high shear"
  - "magnetic compressibility shear"
  - "Wind spacecraft 1 au ICME"
  - "Soljento Good Osmane Kilpua 2023"
data_products:
  - {instrument: "Wind MFI (MAG)", level: "L2", cadence: "high-resolution (sufficient for inertial-range MHD scales)", interval: "1997–2018, intervals centered on 74 ICME-sheath events plus upstream and ejecta windows", archive: "CDAWeb / SPDF"}
  - {instrument: "Wind SWE (proton moments)", level: "L2/L3", cadence: "~92 s", interval: "Same as MFI", archive: "CDAWeb / SPDF"}
algorithms:
  - name: "Large-scale velocity-shear estimator on a 30-minute timescale"
    equation_refs: ["paper §2 shear definition"]
  - name: "Kelvin-Helmholtz instability threshold (linear KH criterion) for shear-amplitude normalisation"
    equation_refs: ["paper §2 KH threshold"]
  - name: "Cross helicity σ_c and Elsasser ratio (z+/z- power ratio)"
    equation_refs: ["paper §3 Alfvénic-imbalance diagnostics"]
  - name: "Magnetic compressibility C|| diagnostic"
    equation_refs: ["paper §3 compressibility"]
  - name: "Shear-amplitude-binned aggregation (below vs above KH threshold)"
    equation_refs: ["paper §3 shear-binned results"]
validation_targets:
  - "Sample: 74 ICME-sheath shears observed by Wind at 1 au between 1997 and 2018, plus upstream and ICME-ejecta windows for context."
  - "Shears identified on a 30-minute timescale; shear amplitude normalised by the linear Kelvin–Helmholtz instability threshold (abstract-level verified)."
  - "Below KH threshold: imbalance (|σ_c|, Elsasser ratio) is approximately invariant or weakly rising with shear amplitude (abstract-level verified)."
  - "Above KH threshold: fluctuations tend toward a balanced state (|σ_c| decreasing) with increasing shear amplitude (abstract-level verified)."
  - "Magnetic compressibility C|| increases above the KH threshold (abstract-level verified)."
  - "Interpretation: velocity shears act as local sources of sunward (z-) fluctuations that reduce net antisunward (z+) imbalance, with the KH instability mediating the transition."
links:
  doi_url: "https://doi.org/10.3847/2041-8213/acc071"
  arxiv_url: "https://arxiv.org/abs/2303.04006"
  ads_url: null
  code_repo: null
  data_repo: "https://cdaweb.gsfc.nasa.gov/ (Wind MFI + SWE)"
claim_boundary:
  scope: >-
    Across 74 ICME-sheath events observed by Wind at 1 au (1997–2018),
    Alfvénic imbalance (σ_c, Elsasser ratio) and magnetic compressibility
    are systematically modified by 30-min-timescale velocity shears: below
    the linear KH threshold imbalance is weakly affected, above it the
    cascade is driven toward a balanced state with rising compressibility.
  out_of_scope:
    - "Do not extrapolate the shear-amplitude → balance trend beyond the sampled range (the sample is bounded by 30-min shears in ICME sheaths)."
    - "Do not transfer the conclusion to near-Sun PSP intervals without re-running — the shear timescale and KH threshold scale with local plasma parameters."
    - "Do not attribute the trend exclusively to shear without ruling out compositional ICME-sheath effects (sheath-internal stream mixing, shock-driven compression)."
    - "Do not invoke the result for non-ICME shears at 1 au without separately verifying that the same KH-threshold normalisation holds."
failure_modes:
  - "Shear-window length sets the magnitude — the 30-min choice is load-bearing; using a different window changes which intervals exceed the KH threshold."
  - "Stream-mixed intervals (CIRs, fast/slow boundaries inside sheaths) confound shear-vs-Alfvenicity attribution; the paper conditions on ICME-sheath context, downstream uses must replicate this."
  - "Cross-helicity sign convention requires a consistent outward-direction reference; an inconsistent reference will invert the sign of σ_c."
  - "Sample size at the highest shear amplitudes is limited (74 sheaths total, sub-sampled by amplitude bin); the trend in the highest bin has the widest error bars."
  - "KH threshold uses a linear-Vlasov-style criterion at the shear location; magnetic-field strength, density, and temperature anisotropy inputs each propagate into the threshold."
  - "Magnetic compressibility C|| signal can also be modulated by density structures and slow-mode contamination — the paper attributes the C|| rise to shear-driven mode coupling, but uniqueness vs slow-mode injection is a fragility to flag."
depends_on:
  - paper-chandran-2025-intermittent-reflection-imbalanced-mhd
adapter_notes: []
research_generation_affordances:
  - type: hypothesis
    statement: "If shear-driven mode coupling at the KH boundary is the mechanism, PSP near-Sun stream-interaction regions (faster local KH timescales, stronger ambient imbalance) should show enhanced cross-helicity drift toward balance at lower nominal shear amplitudes than at 1 au."
    proposed_action: "Replicate the Soljento pipeline on PSP MAG+SWEAP shear windows in stream-interaction regions, normalising shear amplitude by the locally-computed KH threshold."
  - type: gap
    statement: "Sample is bound to ICME sheaths at 1 au. No sibling skill yet covers (a) non-ICME 1 au shears (CIR-driven), (b) the inner-heliosphere PSP regime, or (c) the Helios legacy intervals where the KH threshold can be evaluated at 0.3–1 au."
    proposed_action: "Extend the catalogue to CIR shears (e.g. STEREO) and to Helios shear windows; report whether the below-vs-above-KH bifurcation persists."
  - type: tension
    statement: "[[paper-chandran-2025-intermittent-reflection-imbalanced-mhd]] frames imbalance reduction via *intermittent reflection*. Soljento attributes 1 au sheath rebalance to *shear-driven mode coupling*. Both mechanisms can be present — explicit co-conditioning is needed."
    related_skills: [paper-chandran-2025-intermittent-reflection-imbalanced-mhd]
    proposed_action: "Stratify the Soljento sample by reflection-coefficient proxy (e.g. Alfvén-speed-gradient inferred from large-scale n_p, B), then test whether the shear-driven rebalance persists after reflection-conditioning."
  - type: composable_experiment
    statement: "Couple the Soljento per-event (shear amplitude, σ_c, C||) catalogue to [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]]'s stream-origin annotation — testing whether ICME sheaths from active-region progenitors show stronger above-KH rebalancing than those from coronal-hole progenitors."
provenance:
  generated_by: "HelioSI paper-to-skill factory"
  generated_at: "2026-05-18T00:00:00Z"
  source_record: "sioulas-reproduction/results/arxiv_papers/theme_turbulence.json (2303.04006v1)"
  verified_by: "internalization-batch 2026-05-19 (arXiv 2303.04006 abstract)"
  verified_at: "2026-05-19T00:00:00Z"
  verification_notes:
    - "field=doi value=10.3847/2041-8213/acc071 source=arXiv-journal-ref verified_at=2026-05-19"
    - "field=arxiv_id value=2303.04006 source=arXiv-abs-page verified_at=2026-05-19"
    - "field=author_list value=four-authors-Soljento-Good-Osmane-Kilpua source=arXiv-abs-page verified_at=2026-05-19"
tags: [heliophysics, paper-skill, turbulence, imbalance, velocity-shear, ICME-sheath, Kelvin-Helmholtz]
---

# Soljento et al. 2023 — Imbalance modification by large-scale velocity shears in ICME sheaths (Wind, 1 au) — paper-skill

> Compiled from arXiv:2303.04006 → ApJL (DOI 10.3847/2041-8213/acc071).
> `paper-grounded-pending-full-text` tier — bibliographic anchors, the
> 74-ICME-sheath / 1997–2018 / 1 au sample, the 30-min shear-window choice,
> the KH-threshold normalisation, and the below-vs-above-KH bifurcation in
> imbalance and magnetic compressibility are verified at abstract level.
> Specific σ_c and C|| numerical values per shear bin and the exact KH-
> threshold form are pending full-text verification. ADS bibcode is not
> asserted here.

## 1. Trigger  *(Layer 1)*

Use when:

- characterising how large-scale velocity shears modify the Alfvénic-
  imbalance signature (σ_c, Elsasser ratio) of the inertial-range cascade
  at 1 au;
- conditioning shear-driven cascade modification on a Kelvin–Helmholtz
  threshold rather than on raw shear amplitude;
- working with ICME-sheath turbulence catalogues where local shear is a
  natural control variable;
- annotating magnetic-compressibility C|| modulation by shear amplitude.

Do NOT use this skill for (a) shears at scales other than ~30 min without
re-evaluating which intervals exceed the KH threshold, (b) non-sheath
shears without separately re-verifying the KH-threshold normalisation, or
(c) PSP near-Sun shears without re-running with locally-computed KH
thresholds.

## 2. Paper claim → narrow verifiable task

**Verified claim (abstract, 2026-05-19).** In 74 ICME sheaths observed by
Wind at 1 au (1997–2018), Alfvénic imbalance (cross helicity σ_c, Elsasser
ratio) is modified by 30-min velocity shears in two regimes: below the
linear KH instability threshold imbalance is approximately invariant or
weakly rising with shear amplitude; above the KH threshold the cascade
tends toward a balanced state with increasing shear amplitude, and
magnetic compressibility increases. The interpretation is that velocity
shears act as local sources of sunward (z-) fluctuations that reduce net
antisunward (z+) imbalance.

**Narrow verifiable task.** Reproduction succeeds when an agent, given the
74-event Wind ICME-sheath catalogue:

1. computes a 30-min velocity-shear amplitude per sub-interval;
2. computes the KH threshold per sub-interval from local plasma inputs;
3. computes σ_c, Elsasser ratio and C||;
4. recovers the bifurcation: below-KH imbalance ≈ flat or weakly rising
   with shear; above-KH imbalance trending toward zero;
5. recovers the C|| increase above the KH threshold.

## 3. Executable protocol (Layer 2 — abstract capabilities)

Required abstract capabilities:

1. **Wind MFI + SWE reader.** Returns B(t), V(t), n_p(t), T_p(t) over the
   1997–2018 span at cadence sufficient to resolve 30-min shears and the
   MHD inertial range.
2. **ICME-sheath catalogue.** Provides per-event time windows for sheath,
   upstream and ICME-ejecta sub-intervals (74 events).
3. **30-min shear estimator.** Computes |dV/dt| or equivalent shear-tensor
   amplitude on a 30-min sliding window.
4. **KH-threshold calculator.** Evaluates the linear KH instability
   threshold at the shear location using local B, n_p, T_p, V (and
   anisotropy if available); returns the threshold amplitude.
5. **Alfvénic imbalance diagnostics.** σ_c, Elsasser ratio (z+/z- power
   ratio).
6. **Magnetic compressibility C||.** P_||(f) / P_tot(f) in a local mean-
   field frame, averaged over the inertial range.
7. **Shear-amplitude-binned aggregator.** Bins per-event sub-intervals by
   normalised shear amplitude (above vs below KH); aggregates σ_c, Elsasser
   ratio, C||.

Abstract procedure:

1. Ingest the 74-event sheath catalogue and the surrounding upstream /
   ejecta windows.
2. Compute 30-min shear amplitudes and local KH thresholds per
   sub-interval.
3. Compute σ_c, Elsasser ratio and C|| per sub-interval.
4. Bin by normalised shear amplitude (S / S_KH).
5. Aggregate: produce ⟨σ_c⟩, ⟨z+/z-⟩, ⟨C||⟩ vs S/S_KH curves.
6. Acceptance: recover the below-vs-above bifurcation and the C|| rise.

## 4. Data → tool contracts

| Instrument | Level | Cadence | Interval | Archive | Capability required |
|---|---|---|---|---|---|
| Wind MFI (MAG) | L2 | high-resolution sufficient for MHD inertial range | 74 ICME-sheath windows 1997–2018 + upstream + ICME-ejecta | CDAWeb / SPDF | high-cadence MAG reader |
| Wind SWE (proton moments) | L2/L3 | ~92 s | Same | CDAWeb / SPDF | ion-moments reader (V, n_p, T_p) |

## 5. Validation target

**Primary qualitative targets (verified at abstract level).**

- 74 ICME-sheath events; 1997–2018; Wind at 1 au.
- 30-min shear-window timescale; KH-threshold normalisation.
- Below-KH: ⟨imbalance⟩ flat or weakly rising vs shear amplitude.
- Above-KH: ⟨imbalance⟩ trending toward zero (balanced state); ⟨C||⟩ rising.

**Tolerance budget.** Per-bin numerical σ_c, Elsasser-ratio and C|| values
are **pending full-text verification**. Sign reversal of any of the four
qualitative claims at the per-bin level is a pipeline-disagreement flag.

## 6. Failure modes (load-bearing)

- **Shear-window length is load-bearing.** Changing the 30-min window
  changes which intervals exceed the KH threshold.
- **Stream-mixed sub-intervals confound attribution.** Sheath-internal
  stream mixing can co-vary with shear amplitude; report stream-mixing
  flags per sub-interval.
- **σ_c sign convention.** Inconsistent outward-direction reference inverts
  σ_c; document the convention.
- **Sample-size limits in extreme-shear bin.** The highest-amplitude bin
  has the widest error bars; do not over-interpret outlier means.
- **KH-threshold input sensitivity.** Threshold uses local B, n_p, T_p (and
  anisotropy if available); each propagates into the threshold value.
- **C|| uniqueness vs slow-mode contamination.** The C|| rise above the
  KH threshold can in principle co-arise from slow-mode contamination
  rather than shear-driven mode coupling.

## 7. Claim boundary

**In scope.** 74 ICME-sheath events observed by Wind at 1 au (1997–2018);
30-min shear timescale; KH-threshold-conditioned bifurcation in imbalance
and C||.

**Out of scope.** Non-ICME 1 au shears (CIRs), PSP near-Sun shears,
non-30-min shear timescales, attributing the trend purely to shear
without ruling out sheath-compositional effects.

## 8. Links and identifiers

- DOI: <https://doi.org/10.3847/2041-8213/acc071> (ApJL — verified from
  arXiv journal-ref field 2026-05-19).
- arXiv: <https://arxiv.org/abs/2303.04006> (verified 2026-05-19).
- ADS: not asserted (UI is JS-rendered).

## 9. Skill graph + Layer-4 affordances

Depends on [[paper-chandran-2025-intermittent-reflection-imbalanced-mhd]]
(sibling imbalance-reduction mechanism via reflection rather than shear).

- **Hypothesis (testable).** If shear-driven mode coupling at the KH
  boundary is the mechanism, PSP stream-interaction regions (smaller local
  KH timescales, stronger ambient imbalance) should show enhanced σ_c
  drift toward zero at lower nominal shear amplitudes than at 1 au.
- **Gap.** Sample bound to ICME sheaths at 1 au; CIR shears at 1 au and
  PSP/Helios shears at < 1 au are uncovered siblings.
- **Tension.** Reflection vs shear-coupling mechanisms can coexist; the
  Soljento and Chandran 2025 framings should be co-conditioned by
  reflection-coefficient proxy before drawing single-cause conclusions.
- **Composable experiment.** Couple the Soljento (S/S_KH, σ_c, C||) per-
  event catalogue to
  [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]]'s stream-
  origin annotation — testing whether ICME sheaths from active-region
  progenitors show stronger above-KH rebalancing than those from
  coronal-hole progenitors.

## 10. Relation to HelioSI corpus

- Parent sub-graph: `wave500_turbulence_intermit_heating_045` (imbalance,
  shear-driven cascade modification).
- Sibling paper-skills:
  [[paper-chandran-2025-intermittent-reflection-imbalanced-mhd]],
  [[paper-shi-2021-alfvenic-vs-nonalfvenic-radial-evolution]],
  [[paper-opie-2024-temperature-anisotropy-velocity-shears]] (closely
  related shear/turbulence connection on the temperature-anisotropy axis).
- Required capabilities (not bound here): Wind MFI+SWE reader, ICME-sheath
  catalogue, 30-min shear estimator, KH-threshold calculator, σ_c and
  Elsasser-ratio diagnostics, magnetic compressibility, shear-binned
  aggregator.
