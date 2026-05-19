---
name: paper-flare-qsl-pre-eruption-topology-decay-index
description: Per-entry paper-skill in wave500_solar_corona_cme_flares_045 (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
paper:
  authors_verified: false
---

# paper-flare-qsl-pre-eruption-topology-decay-index

> Runtime-neutral paper-skill (four layers).

## Trigger

Reach for this skill when a pre-flare/erupting active-region needs
**quasi-separatrix layer (QSL) topology** and **decay-index profile**
diagnostics to assess eruption preference.

Concrete symptoms:

- Predicting whether a flux rope embedded in an active region will
  erupt or stay confined.
- Identifying candidate reconnection sites before flare onset.
- Comparing extrapolation-based topology to flare-ribbon position.

Do NOT use this skill without a vector magnetogram and an NLFFF
extrapolation appropriate to the AR.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Pre-Eruption QSL Topology and Decay-Index Profile of
  Confined vs Eruptive Flares (representative: Liu+ 2016; Savcheva+
  2016).
- **Year:** TODO verify
- **Venue:** ApJ — TODO verify

### Claim (narrow form)

Eruptive flares are preceded by (i) high `Q` (QSL) values forming
along well-defined surfaces near the flux-rope footprints and
(ii) a **decay index `n = −d ln B_p / d ln h`** that crosses
`n ~ 1.5` at heights below the flux rope's apex. Confined flares
fail one or both criteria.

### Method assumptions

- A vector magnetogram is available and disambiguated.
- An NLFFF extrapolation provides the 3-D B field.
- The flux rope's apex height is identifiable from the extrapolation.

### Data assumptions

- SHARP CEA vector magnetogram (or equivalent).
- Pre-flare time stamp consistent with the extrapolation choice.

### Failure modes (skill memory)

- **NLFFF non-convergence.** Force-freeness residuals dominate Q-map
  noise.
- **Decay-index along which path?** The choice of vertical column
  matters; report the path explicitly.
- **Q is a geometry, not a force.** High Q ≠ guaranteed reconnection.
- **Confined-eruptive labels** in the literature are not fully
  consistent — use a published label set.

### Figure / numerical targets

- TODO verify: ROC for the eruptive label using
  `(max-Q in flare arcade) × (height of n=1.5)`.

### Claim boundary

**In scope.** Pre-flare AR-scale topology and decay-index
diagnostics on impulsive flares ≥ M-class.

**Out of scope — do NOT generalize:**

- Do NOT use this skill for microflares or non-AR flares.
- Do NOT treat the n=1.5 threshold as universal; published
  thresholds range 1.3–1.7.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability                            | Purpose                          |
|---------------------------------------|----------------------------------|
| `vector_mag.fetch_sharp()`            | SHARP CEA magnetogram            |
| `vector_mag.preprocess_ff()`          | force-freeness consistency       |
| `extrapolation.solve_nlfff()`         | 3-D B field                      |
| `topology.compute_q_map()`            | quasi-separatrix Q               |
| `topology.find_flux_rope()`           | rope apex height                 |
| `topology.compute_decay_index()`      | n(h) along chosen path           |
| `classification.label_eruptive()`     | apply published thresholds       |

### Procedure

1. **Fetch** the pre-flare vector magnetogram and preprocess for
   force-freeness.
2. **Solve** NLFFF.
3. **Compute** the Q-map.
4. **Identify** the flux-rope apex.
5. **Compute** the decay-index profile above the rope footprints.
6. **Classify** the event using published thresholds.

### Validation target

- **Metric:** TODO verify — ROC-AUC for the eruptive label exceeds
  baseline (e.g. flare class alone).

---

## Layer 3 — Adapter / runtime notes (optional examples)

- A published reference adapter is the SolarSoft / IDL Q-map code or
  the Pariat & Démoulin Python re-implementation.
- NLFFF: optimization method from
  `[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`.

---

## Layer 4 — Research-generation affordances

- **Gap:** confined-flare statistics lag eruptive-flare statistics
  by an order of magnitude — a balanced catalog is needed.
- **Tension:** SHARP-feature classifier accuracy in
  `[[paper-flare-forecasting-sharp-features-deep-learning]]` is
  obtained without topology; combining the two may reveal
  complementary skill.
- **Hypothesis:** the decay-index threshold scales with active-region
  twist measured from the same NLFFF.

---

## Skill graph → depends_on

- `[[paper-amari-2014-nlfff-vector-magnetogram-extrapolation]]`
- `[[paper-aulanier-2012-standard-flare-model-3d-tether-cutting]]`

## Links

- arXiv: TODO verify
- DOI: TODO verify
- Source inventory: `sioulas-reproduction/results/arxiv_papers/extended_search.md`
