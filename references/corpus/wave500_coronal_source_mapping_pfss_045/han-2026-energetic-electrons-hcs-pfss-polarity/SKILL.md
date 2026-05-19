# han-2026-energetic-electrons-hcs-pfss-polarity

> Runtime-neutral paper-skill. Layered: (1) scientific invariants, (2) executable protocol against abstract capabilities, (3) adapter notes (optional examples only), (4) research-generation affordances.

## Trigger

Reach for this skill when classifying SEE / SEP events by HCS-sector geometry and you need a PFSS-grounded definition of 'same-side' vs 'opposite-side' relative to the neutral line, cross-checked against strahl PADs and first-order anisotropy.

---

## Layer 1 — Scientific invariant

### Paper identity

- **Title:** Do Solar Energetic Electrons Cross the Heliospheric Current Sheet? A Statistical Study
- **First author:** C. Han
- **Authors:** C. Han, R. F. Wimmer-Schweingruber, P. Kühl, L. Berger, Z. Ding, A. Kollhoff, Q. Shi, Z. Xu, M. Qin, M. Wang
- **Year:** 2026
- **arXiv:** 2604.19446 (posted 2026-04-21)
- **Journal:** TODO_verify_with_full_text
- **DOI:** TODO_verify_with_full_text

### Claim (narrow form)

With a 4-test polarity vote (PFSS footpoint sign, in-situ B_R sign, strahl PAD, first-order anisotropy of energetic electrons), 69 SEE events split into 60 same-side / 9 opposite-side; opposite-side events are more isotropic and have both source and observer closer to the HCS, supporting inefficient cross-HCS transport.

### Method assumptions

- PFSS is solvable per CR on synoptic Br.
- Spacecraft footpoint can be back-mapped via ballistic + PFSS.
- Strahl PAD is a reliable independent polarity sensor when available.
- First-order anisotropy of energetic electrons resolves arrival hemisphere.

### Data assumptions

- Synoptic Br (GONG/HMI/ADAPT) for each event CR.
- Spacecraft B-field (L1/SolO/PSP) for in-situ polarity.
- Strahl PADs from relevant instrument suite.
- SEE flux with anisotropy moments.

### Failure modes (skill memory)

- Magnetogram swap flips polarity at the footpoint near the HCS.
- Source-surface height changes source-to-HCS distance — sweep it.
- Strahl dropouts make the strahl test silently unreliable.
- Anisotropy can flip sign across the event window — pin a window.

### Figure / numerical targets

- Source-to-HCS distance histogram, same vs opposite (Figure TODO_verify).
- PFSS open-field map with event source markers.
- Isotropy contrast panel between the two classes.

### Claim boundary

**In scope.** The 69-event sample with the 4-test polarity protocol.

**Out of scope — do NOT generalize:**

- Do NOT cite as a universal cross-HCS transport efficiency.
- Do NOT collapse to a single polarity test (e.g., B-sign only) and quote the same numbers.

---

## Layer 2 — Executable protocol (capability-typed)

### Required capabilities (abstract)

| Capability | Purpose | Notes |
|---|---|---|
| `magnetogram.fetch_synoptic_br()` | synoptic Br per CR | GONG/HMI |
| `pfss.solve()` | PFSS field on the shell | R_ss≈2.5 |
| `field.trace_to_photosphere()` | observer footpoint | ballistic+PFSS |
| `magnetogram.locate_neutral_line()` | HCS on source surface |  |
| `polarity.evaluate_in_situ()` | B_R sign at observer | windowed |
| `strahl.pad_polarity()` | strahl polarity from PAD | instrument |
| `anisotropy.first_order()` | energetic-electron anisotropy | per energy |
| `ephemeris.observer()` | L1/SolO/PSP position | per event |

### Procedure

1. Assemble event list with onset windows.
2. Fetch synoptic Br per event CR; solve PFSS.
3. Back-map observer to source surface via ballistic vsw.
4. Locate source-surface neutral line.
5. Run 4 polarity tests; vote.
6. Record source/observer angular distance to HCS.
7. Aggregate isotropy diagnostic per class.

### Validation target

Reproduce 60/9 split and qualitative HCS-proximity ordering.

---

## Layer 3 — Adapter / runtime notes (optional examples)

- PFSS can bind to sunkit-magex.pfss; ballistic + ephemeris example lives in .library/custom/pfss-tracing/. Not required.

---

## Layer 4 — Research-generation affordances

- Tension with [[paper-jiang-2024-nested-active-regions-hcs-reversal]] — nested ARs stall HCS reversal, so opposite-side events should cluster in stalling phases.
- Cross-product with [[paper-paper-desai-2024-hcs-reconnection-400kev-protons]]: are opposite-side events those with sources *embedded* in HCS reconnection regions?
- Generative hypothesis: weighting the 4-test vote by strahl coverage quality should reclassify a measurable fraction.

---

## Skill graph → depends_on

- [[paper-pfss-test-problems-solar-stellar-magnetic-fields]] — PFSS solver acceptance test.
- [[paper-paper-desai-2024-hcs-reconnection-400kev-protons]] — sibling HCS-particle skill.

## Links

- arXiv: https://arxiv.org/abs/2604.19446
- arXiv HTML: https://arxiv.org/html/2604.19446
- DOI: TODO_verify_with_full_text
- Source inventory:
  - sioulas-reproduction/results/arxiv_papers/theme_pfss_modeling.json

## TODOs for full-text verification

- DOI
- journal
- exact event list
- magnetogram product per event
