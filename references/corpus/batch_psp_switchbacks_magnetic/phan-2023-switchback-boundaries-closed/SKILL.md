---
name: phan-2023-switchback-boundaries-closed
description: Per-entry paper-skill in batch_psp_switchbacks_magnetic (HelioSI 501-corpus). See body and metadata.yaml for paper identity and claim boundary.
---

# phan-2023-switchback-boundaries-closed

A paper-skill compiled from Phan et al. 2023 (arXiv:2310.12134; ApJ-
family).

Paper-skills are **harness-agnostic**. They describe what a paper
enables an agent to do via abstract *capability contracts*. Any
runtime may satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol; (4) optional adapter notes; (5) research-
generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- Combine magnetic-topology checks with energetic-particle signatures
  across a switchback boundary to assign a {closed, open, ambiguous}
  topology label.
- Provide a topology layer composable with reconnection-exhaust and
  RD/TD-classification skills.

### When NOT to use it

- Switchback *generation*; this is a topology diagnostic, not a
  generation theory.
- Reconnection-exhaust event identification per se — see
  [[phan-2022-switchback-boundary-reconnection-psp]].

### Claim boundary

Combined vector-magnetic-field topology checks and energetic-particle
drop-out / continuity diagnostics across switchback boundaries indicate
that *some* boundaries behave as closed topological features while
others are consistent with kinks on otherwise open field lines. Bounded
to the analysed events; not a population fraction claim.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

Across the analysed PSP switchback events, combined vector-magnetic-
field topology and energetic-particle continuity diagnostics produce a
per-event {closed, open, ambiguous} label, with both closed and open
events present.

### 2.2 Equations / method

- Boundary localisation (entry + exit).
- MVA → LMN frame, `B_n` estimate per boundary.
- Field-topology signature: continuity of `B_R` sign, magnitude of
  `B_n / |B|`, inferred connectivity.
- Energetic-particle continuity: compare flux upstream / inside /
  downstream; drop-out inside → consistent with closed; smooth
  continuity → consistent with open kink.
- Combined label rule using both signatures.

### 2.3 Data assumptions

- High-cadence vector `B`.
- Co-temporal energetic-particle flux at the boundary.
- A switchback event catalog.

### 2.4 Failure modes (skill memory)

- **`B_n` noise floor.** Small `B_n` may be either closed-topology
  indicator or MVA noise.
- **Particle background.** A faint drop-out can be masked.
- **Particle cadence** can blur boundary-local features.
- **Single-spacecraft topology** is consistent-with, not proof-of,
  closed topology.
- **Event-selection bias.** Hand-curated paper events may emphasise a
  topology mix; document the gap to automated re-selection.

### 2.5 Figure / numerical targets

- Reproduce a paper closed-labeled event with matching topology +
  particle diagnostic (TODO verify list).
- Reproduce at least one open-labeled event for contrast.
- Inter-rater agreement between automated classifier and paper hand-
  labels ≥ 75% (target — TODO verify).

---

## 3. Executable protocol layer

### 3.1 Capability contracts

- **C-FETCH-MAG**: high-cadence vector `B`.
- **C-FETCH-BULK** *(optional, for V_A context)*: bulk + density.
- **C-FETCH-EPI**: energetic-particle flux time series spanning the
  boundary.
- **C-CATALOG**: switchback event list with boundary timestamps.
- **C-MVA**: MVA on `B` across each boundary.
- **C-PARTICLE-CONTINUITY**: compare upstream / inside / downstream
  flux at documented SNR threshold.
- **C-TOPOLOGY-LABEL**: combined-label rule using both `B_n / |B|` and
  particle diagnostic.

### 3.2 Procedure

1. C-CATALOG over the analysis window.
2. C-FETCH-MAG (+ C-FETCH-BULK) + C-FETCH-EPI for each event.
3. C-MVA on each boundary; record `B_n / |B|` and eigenvalues.
4. C-PARTICLE-CONTINUITY with documented SNR threshold.
5. C-TOPOLOGY-LABEL.
6. Aggregate; compare per-event labels to the paper.

### 3.3 Minimum reproduction artifacts

- Per-event label JSON with `B_n` noise floor and particle SNR
  threshold recorded.
- Topology + particle overlay PNG per event.
- Agreement-matrix CSV between automated and paper labels.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness with PSP CDF I/O + IS⊙IS energetic-particle data + MVA
  satisfies the contracts.
- LingTai HelioSI may bind C-FETCH-EPI to an internal IS⊙IS-loader
  skill — one binding option.

---

## 5. Research-generation affordance

- **Composability with [[phan-2022-switchback-boundary-reconnection-psp]]**:
  closed-topology events with simultaneous Walén-consistent jumps would
  be a particularly compelling reconnection-island signature. The
  intersection is unreported in the inventory.
- **Composability with [[agapitov-2023-structure-origin-switchbacks-psp]]**:
  do RD-classified boundaries (geometric) align with closed-topology
  labels (particle)? A 2x2 confusion table answers this directly.
- **Tension with [[bale-2021-solar-source-switchbacks-magnetic-funnels]]**:
  a high closed-topology fraction would constrain solar-origin models
  that produce closed-loop kinks (e.g. some interchange-reconnection
  scenarios) vs. those that produce open-field kinks.
- **Open hypothesis**: closed-fraction radial dependence; the paper
  studies a fixed event set, and a multi-encounter rerun is the
  experiment.

---

## Links

- arXiv: https://arxiv.org/abs/2310.12134
- DOI / journal: TODO verify with full text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/apj_aa_heliophysics_papers.md`
  §3.3

## Skill graph

- [[phan-2022-switchback-boundary-reconnection-psp]] — reconnection-
  exhaust intersection.
- [[agapitov-2023-structure-origin-switchbacks-psp]] — geometric RD/TD
  classification cross-test.
- [[bale-2021-solar-source-switchbacks-magnetic-funnels]] — origin-
  hypothesis tension via closed-fraction.
- [[agapitov-2020-localized-magnetic-structures-boundaries]] — boundary-
  catalog foundation.
