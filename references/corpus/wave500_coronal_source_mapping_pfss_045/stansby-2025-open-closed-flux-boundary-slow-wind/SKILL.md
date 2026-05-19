# stansby-2025-open-closed-flux-boundary-slow-wind

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when explicitly modelling the open–closed flux boundary (OCB) at the source surface and associating slow-wind streams with its expansion-factor structure.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** The Sun's Open–Closed Flux Boundary and the Origin of the Slow Solar Wind
- **First author:** TODO_verify
- **Authors:** TODO_verify
- **Year:** 2025
- **arXiv:** 2503.09744 (posted 2025-03-12)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

Slow-wind streams preferentially trace back, via PFSS, to narrow regions adjacent to the open–closed flux boundary where expansion factors are large — supporting an interchange-reconnection / S-web class of slow-wind origins.

### Method assumptions

- PFSS captures the relevant OCB at the source surface.
- Expansion factor f at the source surface is a meaningful diagnostic.
- In-situ slow-wind classification is independent of the OCB definition.

### Data assumptions

- Synoptic Br across the studied interval.
- In-situ vsw + composition data for the slow-wind sample.

### Failure modes (skill memory)

- OCB position moves with R_ss — sweep it.
- Slow-wind classification thresholds vary in the literature.
- Backmapping uncertainty grows for slow streams.

### Figure / numerical targets

- PFSS OCB on the source surface with slow-wind footpoint overlay.
- Expansion-factor distribution along the OCB.
- Composition-vs-OCB-distance scatter.

### Claim boundary

**In scope.** The paper's interval + slow-wind classifier.

**Out of scope — do NOT generalize:**

- Do NOT claim *all* slow wind originates at the OCB.
- Do NOT use this skill to rule out coronal-hole boundary or streamer-belt origins without re-classifying.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | synoptic Br |  |
| `pfss.solve()` | PFSS |  |
| `ocb.extract()` | open–closed boundary at SS |  |
| `expansion_factor.compute()` | f along OCB |  |
| `sw.classify_slow_fast()` | slow-wind segmentation | vsw thresholds |

### Procedure

1. Run PFSS over the interval.
2. Extract OCB on the source surface.
3. Back-map in-situ vsw to OCB and quantify proximity.
4. Compute expansion-factor distribution along the OCB.
5. Test composition–OCB-distance relationship.

### Validation target

Reproduce the slow-wind/OCB proximity statistic at the paper's level.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- sunkit-magex.pfss for PFSS; in-situ data via pyspedas / SPDF.

---

## Layer 4 — Research-generation affordances

- Compose with [[paper-stansby-2025-open-closed-flux-boundary-slow-wind]] itself + [[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]] to separate slow-Alfvénic from slow-non-Alfvénic slow wind by OCB distance.
- Generative hypothesis: OCB-distance metrics under outflowpy ([[paper-rice-2026-outflowpy-outflow-fields-pfss-alternative]]) should give a sharper slow-wind separation.

---

## Skill graph → depends_on

- [[paper-ervin-2024-slow-alfvenic-source-regions-pfss-psp]]
- [[paper-stansby-2020-pfsspy-python-pfss]]

## Links

- arXiv: https://arxiv.org/abs/2503.09744
- arXiv HTML: https://arxiv.org/html/2503.09744
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- lead author
- DOI
- slow-wind classifier
- OCB extraction method
