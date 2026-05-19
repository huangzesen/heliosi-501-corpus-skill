# razquin-2026-coronal-dimming-magnetic-flux-may2024

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when attributing coronal dimmings to specific magnetic-flux systems during a CME sequence via AIA logBR thresholding, HMI flux integration, and PFSS+NLFFF extrapolations.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Magnetic Flux Systems Involved in the May 2024 Solar Energetic Events from AR 13664 Inferred Through Coronal Dimmings
- **First author:** A. Razquin
- **Authors:** A. Razquin, K. Dissauer, A. M. Veronig, G. Barnes
- **Year:** 2026
- **arXiv:** 2603.23623 (posted 2026-03-24)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

For AR 13664 May 2024, 16 dimmings split into southward and northward populations whose footprints correspond to two distinct strapping-flux domains anchored on two major PILs; final dimming extent is set by exterior eruption flux.

### Method assumptions

- AIA 211 Å logBR thresholding isolates dimmings reliably.
- ∫|Br| in AIA 1600 Å ribbon mask is a fair reconnection-flux proxy.
- PFSS+NLFFF together pin strapping flux above PILs.

### Data assumptions

- AIA 211 / 1600 Å, May 2024.
- HMI LoS + radial Br + vector magnetograms.
- GOES flare list for the sequence.

### Failure modes (skill memory)

- logBR threshold shifts dimming area; sweep + log.
- Ribbon adaptive thresholds fragment large ribbons.
- NLFFF non-uniqueness — pin boundary preparation.

### Figure / numerical targets

- Dimming-area vs reconnection-flux scatter.
- PFSS+NLFFF strapping-flux overlay.
- Southward→northward dimming shift time-series.

### Claim boundary

**In scope.** AR 13664 May 1–14 2024 events as classified.

**Out of scope — do NOT generalize:**

- Do NOT generalize the PIL/strapping correspondence to other ARs without re-extrapolating.
- Do NOT use dimming-area alone as flux proxy outside this calibration.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `imagery.fetch_aia()` | 211 / 1600 Å | L1.5 |
| `imagery.logbr_threshold()` | dimming mask | threshold |
| `magnetogram.fetch_hmi()` | Br + vector | L1.5 |
| `flux.reconnection_in_ribbon()` | ∫|Br| | 1600 mask |
| `pfss.solve()` | global context |  |
| `nlfff.solve()` | AR volume | boundary prep |
| `flux.identify_strapping()` | strapping vs eruption | topology |

### Procedure

1. Identify dimming events; extract logBR masks.
2. Identify ribbons in 1600 Å.
3. Compute ∫|Br| in ribbons.
4. Solve PFSS for the CR; NLFFF for AR volumes.
5. Identify strapping flux on each PIL.
6. Correlate dimming morphology with PIL anchoring.

### Validation target

Recover the southward/northward population split and stronger-than-prior dimming–ribbon correlations.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- PFSS via sunkit-magex.pfss; NLFFF via Wiegelmann/NLFFFE; image processing via SunPy/aiapy.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-prasad-2026-blowout-jet-magnetic-topology]] — Razquin's eruption flux should match Prasad's blowout-jet topologies on the same AR class.
- Generative hypothesis: continuous threshold sweeps should saturate dimming–ribbon-flux slope at NLFFF strapping flux.

---

## Skill graph → depends_on

- [[paper-flare-precursor-fine-scale-topology-extrapolation]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2603.23623
- arXiv HTML: https://arxiv.org/html/2603.23623
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- logBR threshold
- NLFFF code identity
- uncertainty on reconnection flux
- DOI
