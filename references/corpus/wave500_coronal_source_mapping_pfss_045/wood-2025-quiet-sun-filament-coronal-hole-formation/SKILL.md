---
name: wood-2025-quiet-sun-filament-coronal-hole-formation
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# wood-2025-quiet-sun-filament-coronal-hole-formation

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when tracking the *birth* of a coronal hole following a quiet-Sun filament eruption, including the PFSS topology change pre/post eruption.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Formation of a Coronal Hole by a Quiet-Sun Filament Eruption
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2509.04663 (posted 2025-09-04)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

A quiet-Sun filament eruption can reorganize PFSS open-field topology to produce a *new* coronal hole at the eruption site, with the new CH boundary identifiable in EUV and in PFSS open-field maps within ~hours of the eruption.

### Method assumptions

- EUV-CH detection thresholds are stable across the pre/post windows.
- PFSS solves are valid on snapshots ≤6 h cadence.
- Filament eruption can be timestamped from EUV+coronagraph.

### Data assumptions

- AIA EUV at high cadence for the event window.
- Synoptic Br with sufficient temporal updates (HMI/ADAPT).
- Coronagraph imagery for the eruption.

### Failure modes (skill memory)

- Synoptic-map update lag delays the PFSS topology change.
- ADAPT vs HMI synoptic gives different post-eruption open-field maps.
- Filament-eruption timing is ambiguous if no clear bright front.

### Figure / numerical targets

- Pre/post EUV-CH masks at the eruption site.
- PFSS open-field map evolution.
- Time-line of CH-area growth.

### Claim boundary

**In scope.** The paper's event; quiet-Sun filament regime.

**Out of scope — do NOT generalize:**

- Do NOT generalize to AR-driven eruptions without checking PFSS topology.
- Do NOT attribute every post-eruption CH to the eruption alone — preexisting flux organization matters.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `imagery.fetch_aia()` | EUV time series | L1.5 |
| `ch.detect_from_euv()` | CH masks | threshold |
| `magnetogram.fetch_synoptic_br()` | synoptic Br | ADAPT/HMI |
| `pfss.solve()` | open-field map evolution |  |
| `filament.detect_eruption()` | eruption start time | AIA 304 / running |

### Procedure

1. Identify eruption window; extract EUV time series.
2. Build pre/post CH masks.
3. Run PFSS on synoptic snapshots straddling the event.
4. Track CH boundary in PFSS open-field maps.
5. Quantify CH-area growth and topology change.

### Validation target

Recover post-eruption CH appearance in both EUV and PFSS open-field maps.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- SunPy/aiapy for EUV; sunkit-magex.pfss for PFSS.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-razquin-2026-coronal-dimming-magnetic-flux-may2024]] — a single framework for dimming-vs-CH-formation as two outcomes of post-eruption topology.
- Generative hypothesis: the post-eruption PFSS open-flux change should correlate with subsequent slow-wind source variability ([[paper-katsavrias-2025-low-db-streams-source-variability]]).

---

## Skill graph → depends_on

- [[paper-razquin-2026-coronal-dimming-magnetic-flux-may2024]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2509.04663
- arXiv HTML: https://arxiv.org/html/2509.04663
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- event date
- synoptic product
