# wyper-2026-switchback-formation-mechanisms-review

A paper-skill compiled from P. F. Wyper et al. 2026 (arXiv preprint, arXiv:2604.16166).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- A structured review of competing switchback-formation mechanisms (coronal interchange/reconnection, in-situ turbulence, kinked jets, expansion-driven) informed by PSP observations of large-amplitude magnetic deflections.
- The skill applies to: Review paper — synthesises mechanisms, observational tests, and prediction-distinguishing observables.

### When NOT to use it

- Do not treat review claims as primary observational evidence — back to primary papers (Bale 2021, Shoda 2021, Squire 2020, etc.).
- Do not use as a reproducible workflow — it is a synthesis skill.

### Claim boundary

Review paper — synthesises mechanisms, observational tests, and prediction-distinguishing observables.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

A structured review of competing switchback-formation mechanisms (coronal interchange/reconnection, in-situ turbulence, kinked jets, expansion-driven) informed by PSP observations of large-amplitude magnetic deflections.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

No in-situ / remote data dependencies (theory or methods paper).

### 2.4 Failure modes (skill memory)

- Reviews date quickly — re-check Wyper 2026 mechanism list against post-2026 work.
- Author bias toward specific mechanism class possible.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### Discriminating-observable matrix construction across mechanism candidates

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### 3.2 Capability contracts

The runtime must supply:

- **C-FETCH-DATA**: time-series read of the instruments listed in §2.3.
- **C-CLASSIFIER**: event/interval classifier (paper-specific).
- **C-METRIC**: numerical comparison to a paper figure/table (TODO verify full text).

These contracts name no MCP, plugin, or harness command. Adapter binding
examples (if any) live in §4 and `adapter_notes[]` in the frontmatter; the
contract itself remains runtime-neutral.

### 3.3 Minimum reproduction artifacts

- A run log capturing data interval(s), thresholds, and algorithm parameters.
- One numerical scalar or shape statistic comparable to a paper figure/table.
- A JSON/CSV side-car recording inputs, parameters, and the comparison metric.

---

## 4. Adapter / runtime notes (optional examples)

- Any harness capable of CDF I/O + standard time-series analysis can satisfy
  the contracts; named tools (pyspedas, sunpy, sunkit-magex, pfsspy,
  sw-scanner) are *example* adapters, not requirements.
- Encounter-specific data ranges should be obtained from the paper's full
  text; adapter glue is the runtime's responsibility.

---

## 5. Research-generation affordance

- **Gap** — Review identifies untested joint observables (delta-B vs spherical-polarisation vs heavy-ion contrast) — no current skill computes the full triplet on a single interval. Related: (no explicit sibling).
- **Minimal_experiment** — On a PSP–SolO lineup interval (P11), compute the joint (delta-B alignment, spherical-polarisation, Q_Fe contrast) triplet and locate each switchback in the discriminating matrix. Related: [[rivera-2024-mixed-source-signatures-switchback-patches-heavy-ions]].

---

## Links

- arXiv: https://arxiv.org/abs/2604.16166
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 3 §6`

## Skill graph

- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
- [[shoda-2021-turbulence-switchback-generation-alfvenic]]
- [[touresse-2024-untwisting-jets-super-alfvenic-wind-switchback]]
- [[agapitov-2023-structure-origin-switchbacks-psp]]
- [[huang-2025-what-are-switchbacks-solitary-alfven-wave-model]]
