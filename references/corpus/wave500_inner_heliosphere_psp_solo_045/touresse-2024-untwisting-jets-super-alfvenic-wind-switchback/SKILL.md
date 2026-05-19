# touresse-2024-untwisting-jets-super-alfvenic-wind-switchback

A paper-skill compiled from J. Touresse et al. 2024 (arXiv preprint, arXiv:2412.15930).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- 3D MHD simulations show that self-consistent reconnection-driven solar jets can untwist and propagate into the super-Alfvénic wind, producing localized large-amplitude magnetic deflections compatible with PSP-observed switchbacks.
- The skill applies to: 3D MHD simulation, low-β coronal jet seed, propagation into super-Alfvénic regime, qualitative comparison with PSP switchback signatures.

### When NOT to use it

- Do not treat as a statistical-match claim — single-event-class simulation.
- Do not infer unique origin — turbulence-generation hypothesis (Shoda 2021) remains viable.

### Claim boundary

3D MHD simulation, low-β coronal jet seed, propagation into super-Alfvénic regime, qualitative comparison with PSP switchback signatures.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

3D MHD simulations show that self-consistent reconnection-driven solar jets can untwist and propagate into the super-Alfvénic wind, producing localized large-amplitude magnetic deflections compatible with PSP-observed switchbacks.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

No in-situ / remote data dependencies (theory or methods paper).

### 2.4 Failure modes (skill memory)

- Resistivity scheme (numerical vs explicit) alters jet untwisting rate.
- Boundary conditions imprint a global twist pattern that biases switchback amplitude.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### 3D resistive MHD simulation of reconnection-driven jet

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Twist-helicity injection tracking

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Synthetic single-spacecraft sampling of jet propagation

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

- **Tension** — Jet-origin (this work) vs in-situ turbulence-origin (Shoda 2021) — joint observables (delta-B alignment + spherical-polarisation) needed. Related: [[shoda-2021-turbulence-switchback-generation-alfvenic]].
- **Minimal_experiment** — Run synthetic-spacecraft sampling of jet output at multiple impact parameters; compare delta-B vs spherical-polarisation to PSP catalog. Related: (no explicit sibling).

---

## Links

- arXiv: https://arxiv.org/abs/2412.15930
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/psp_analysis_2020_2026.md §9`

## Skill graph

- [[shoda-2021-turbulence-switchback-generation-alfvenic]]
- [[bale-2021-solar-source-switchbacks-magnetic-funnels]]
