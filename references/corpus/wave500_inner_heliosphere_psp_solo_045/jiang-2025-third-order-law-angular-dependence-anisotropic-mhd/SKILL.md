# jiang-2025-third-order-law-angular-dependence-anisotropic-mhd

A paper-skill compiled from B. Jiang et al. 2025 (arXiv preprint, arXiv:2512.16610).

Paper-skills are **harness-agnostic** — they describe what a paper enables an
agent to do via abstract *capability contracts*. Any runtime (Claude Code,
LingTai, Codex, Python notebook, a future MCP server) can satisfy them.

Layers: (1) trigger + claim boundary; (2) scientific invariants;
(3) executable protocol with abstract capability contracts; (4) optional
adapter / runtime notes; (5) research-generation affordance.

---

## 1. Trigger and claim boundary

### When to use this skill

- In direct numerical simulations of anisotropic MHD turbulence, the cascade rate estimated from the Politano–Pouquet law via single-direction sampling is most accurate when the sampling direction lies near a 60° polar angle to the mean field; lower-angle and parallel-to-B sampling biases ε substantia
- The skill applies to: Anisotropic MHD DNS, Politano–Pouquet law evaluated at variable sampling angles; theoretical / methodological paper.

### When NOT to use it

- Do not apply numeric biases verbatim to compressible solar-wind data without checking compressibility correction.
- Not a claim about absolute cascade rate magnitude — only about angular bias.

### Claim boundary

Anisotropic MHD DNS, Politano–Pouquet law evaluated at variable sampling angles; theoretical / methodological paper.

---

## 2. Scientific invariant layer

### 2.1 Central claim (narrow form)

In direct numerical simulations of anisotropic MHD turbulence, the cascade rate estimated from the Politano–Pouquet law via single-direction sampling is most accurate when the sampling direction lies near a 60° polar angle to the mean field; lower-angle and parallel-to-B sampling biases ε substantially.

### 2.2 Equations / method

See §3.1 for capability contracts; equation references where available are
recorded in `algorithms[].equation_refs` in `metadata.yaml`.

### 2.3 Data assumptions

No in-situ / remote data dependencies (theory or methods paper).

### 2.4 Failure modes (skill memory)

- Anisotropy strength in DNS controls the 60° optimum — solar-wind anisotropy may differ.
- Compressibility ignored in this DNS — solar-wind correction needed.

### 2.5 Figure / numerical targets

TODO verify with full text — quality tier is `paper-grounded-pending-full-text`.
The paper's reproducible numerical anchor lives in its figures/tables; promotion
to `executable` requires lifting that anchor into `validation_target`.

---

## 3. Executable protocol layer

### 3.1 Algorithms (abstract capability contracts)

### DNS-based Politano–Pouquet evaluation at variable angles

- Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability. See `algorithms[]` in `metadata.yaml`.

### Angular-bias quantification for single-spacecraft ε estimation

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

- **Minimal_experiment** — Re-run Bandyopadhyay 2020 ε computation conditioning on flow-direction-vs-B angle; check 60° optimum holds. Related: [[bandyopadhyay-2020-energy-transfer-psp]].
- **Hypothesis** — Cascade-rate enhancement near the Sun is partly a sampling-angle artifact when sampling becomes radial-aligned at perihelion. Related: [[bandyopadhyay-2020-energy-transfer-psp]].

---

## Links

- arXiv: https://arxiv.org/abs/2512.16610
- DOI: TODO_verify_with_full_text
- Source inventory: `sioulas-reproduction/results/arxiv_papers/more_papers_2020_2026.md Topic 1 §4`

## Skill graph

- [[bandyopadhyay-2020-energy-transfer-psp]]
