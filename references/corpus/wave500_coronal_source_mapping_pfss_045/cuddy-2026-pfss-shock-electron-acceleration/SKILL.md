---
name: cuddy-2026-pfss-shock-electron-acceleration
description: Per-entry paper-skill in wave500_coronal_source_mapping_pfss_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# cuddy-2026-pfss-shock-electron-acceleration

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when localising shock-accelerated electrons to a specific magnetic-field geometry by combining EUV-wave kinematics, radio herringbones, and PFSS ambient field.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Signatures of Localised Particle Acceleration at a Global Coronal Shock Wave
- **First author:** C. Cuddy
- **Authors:** C. Cuddy, D. M. Long, M. Nedal, S. Bhunia, P. T. Gallagher
- **Year:** 2026
- **arXiv:** 2603.23335 (posted 2026-03-24)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

On 10 March 2024 a weak coronal shock (M_A≈1.005) drove herringbone-emitting electron beams (75–122 keV) where its front met quasi-perpendicular open field in an EUV dimming region, as identified by PFSS.

### Method assumptions

- EUV running/base difference images give true wavefront speed.
- Radio herringbone drift-rates map to electron energies via Newkirk density (scale factor 1.3–2.6).
- PFSS captures the relevant ambient-field geometry at the shock front.

### Data assumptions

- AIA EUV channels for the event.
- Radio dynamic spectra + imaging.
- Synoptic Br for the event CR.

### Failure modes (skill memory)

- Newkirk scale factor changes electron-energy estimate non-trivially.
- EUV-wave speed depends on running- vs base-difference choice.
- PFSS misses non-potential currents in dimming regions.

### Figure / numerical targets

- EUV wavefront kinematics with M_A overlay.
- Radio dynamic spectrum with herringbone identification.
- PFSS open-field map at the shock-acceleration site.

### Claim boundary

**In scope.** 10 March 2024 shock with the paper's PFSS configuration.

**Out of scope — do NOT generalize:**

- Do NOT generalize the local-acceleration framework to all weak shocks without re-checking field geometry.
- Do NOT cite the 75–122 keV electron energies independent of the Newkirk density-model scale factor.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `imagery.fetch_aia()` | EUV imagery | L1.5 |
| `euv_wave.kinematics()` | EUV-wave speed, M_A |  |
| `radio.dynamic_spectrum()` | radio dynamic spectrum |  |
| `radio.herringbone_drift()` | extract drift rates |  |
| `density.newkirk()` | Newkirk model | scale factor knob |
| `pfss.solve()` | ambient field | for shock geometry |

### Procedure

1. Identify event window; build EUV difference movies.
2. Track wavefront; estimate speed and M_A.
3. Identify herringbones; extract drift rates.
4. Convert drifts to electron energies via Newkirk + scale factor.
5. Solve PFSS for the event CR.
6. Localise the herringbone source to open-field topology.

### Validation target

Recover the M_A≈1.005 wavefront and 75–122 keV electron energy range at the dimming-region open field.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- PFSS via sunkit-magex.pfss; radio dynamic spectra via custom or LOFAR pipelines. SunPy/aiapy for AIA processing.

---

## Layer 4 — Research-generation affordances

- Compose with [[nedal-2026-pfss-mhd-typeII-shock-may2024]]: the local-vs-global acceleration framework should generalize to May 2024 multi-shock sequences.
- Generative hypothesis: replacing PFSS with outflowpy ([[rice-2026-outflowpy-outflow-fields-pfss-alternative]]) should shift the herringbone source position by a measurable amount.

---

## Skill graph → depends_on

- [[eclipse-white-light-benchmark-pfss-models]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2603.23335
- arXiv HTML: https://arxiv.org/html/2603.23335
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- exact event time
- Newkirk scale factor used
- herringbone identification protocol
