---
name: interchange-reconnection-pseudostreamer-metis-2025
description: Per-entry paper-skill in wave500_waves_instabilities_reconnection_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# interchange-reconnection-pseudostreamer-metis-2025

<!-- layer2-stub-banner: issue-14 -->
> **Layer 2 not populated — read paper before use.** This entry's
> executable-protocol layer is a stub: the algorithm sub-sections name
> capabilities but do not specify the procedure end-to-end. Treat
> Layer 2 as `pending`; do not present this skill as workflow-ready or
> use it as the basis for an experiment without first verifying the
> paper's methods section.


A paper-skill compiled from the primary source (author list pending verification), 2025 (TODO_verify_journal; arXiv:2502.08015).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime (LingTai, Claude Code, Codex, custom) may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Identify Alfvénic outflows driven by interchange reconnection at pseudostreamer footpoints in Metis coronagraph data.
- Quantify outflow speed and connect to in-situ slow-Alfvénic streams.

### When NOT to use it

- Streamer-belt origin without pseudostreamer — separate.

### Claim boundary

Metis-imagery event analysis of an Alfvénic outflow signature attributed to interchange reconnection.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Metis observes Alfvénic outflows whose timing and speed are consistent with interchange reconnection at pseudostreamer footpoints, linking corona-to-heliosphere slow-Alfvénic streams.

### 2.2 Equations / method

- Outflow speed measurement from coronagraph time series.
- Pseudostreamer-topology PFSS check.

### 2.3 Data assumptions

- Metis coronagraph + SolO data.
- PFSS or analogue magnetic-topology model.

### 2.4 Failure modes (skill memory)

- **Projection effects** on outflow speed.
- **Topology model** sensitivity.

### 2.5 Figure / numerical targets

- Outflow speed within expected range (TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-METIS-IMAGE-LOAD**.
- **C-PFSS-PSEUDOSTREAMER**.

### 3.2 Procedure

1. C-METIS-IMAGE-LOAD.
2. C-PFSS-PSEUDOSTREAMER: identify topology.
3. Measure outflow speed.

### 3.3 Minimum reproduction artifacts

- Outflow event report.

---

## 4. Adapter / runtime notes (optional examples)

- pfsspy + Metis pipelines example Layer-3.

---

## 5. Research-generation affordance

- **Composability with [[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]] (existing)**: directly tests pseudostreamer-origin hypothesis.
- **Open hypothesis**: Are slow-Alfvénic streams in PSP traceable to specific interchange-reconnection events imaged by Metis?

---

## Links

- arXiv: https://arxiv.org/abs/2502.08015
- DOI: TODO_verify_with_full_text
- Source inventory:
  `sioulas-reproduction/results/arxiv_papers/theme_wave_analysis.json arxiv_id=2502.08015`

## Skill graph

- [[ervin-2024-slow-alfvenic-source-regions-pfss-psp]]

