# Skill-quality / HelioSI-alignment audit (sample-based)

**Status:** report-only. No corpus entries, schema, manifest, or graph
artifacts were edited in producing this document. The report exists to
ask a *content* question — "are the per-entry paper-skills good enough
to serve as a substrate for autonomous heliophysics research?" — that
the existing graph- and identity-hygiene reports under `reports/` do
not directly answer.

**Companion documents (read first if you have not).** This report
deliberately does not restate what they already publish:

- [`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md) §3 — promotion-gate
  contract for the *discovery → drafter → corpus* path; this audit
  applies only to entries that are already inside `references/corpus/`.
- [`reports/internalization_readiness_report.md`](internalization_readiness_report.md) —
  the existing quantitative readiness score per entry. This audit
  consumes its top-debt list rather than recomputing it.
- [`references/corpus_qa_report_v2.md`](../references/corpus_qa_report_v2.md)
  §3–§9 — the safe / unsafe claim boundaries, the maturity-tier counts,
  the rendering-family breakdown, and the layer-population audit; this
  audit takes those counts as given and asks the orthogonal question.

**Scope.** Eight deliberately-chosen entries across maturity strata
plus three manifest-level cross-cuts. A T7 weak-attribution pilot entry was read during reconnaissance but is not scored separately below because duplicate / weak-attribution identity risk is already tracked by HelioSI issue #67; this report focuses on four-layer content quality. Findings are scoped to the scored sample; corpus-wide claims are bounded explicitly.

---

## 1. Question this audit answers

Jason's stated HelioSI goal is a substrate for fully automated
heliophysics research: paper-skills should be **discoverable**,
**composable** into hypotheses, **honestly judged** on executability,
**bindable** to tools / data / model adapters, and **drive verification
experiments**. The desired paper-skill representation preserves four
layers (see `SKILL.md` and `README.md`):

1. **Scientific invariant** — claim, equations, methods, data
   assumptions, failure modes, validation targets.
2. **Executable protocol** — abstract input/output/workflow/capability
   contracts.
3. **Adapter / runtime boundary** — optional examples clearly
   separated from invariant content.
4. **Research-generation affordance** — gaps, tensions, hypotheses,
   minimal experiments, new-paper route.

The existing graph- and identity-hygiene reports (`wikilink_audit.md`,
`wikilink_curation_*.md`, `internalization_readiness_report.md`)
already audit cleanliness of the substrate. What none of them ask is:
*on the entries themselves, is the four-layer content actually
preserved well enough that an autonomous loop could compose a
hypothesis and propose a verification experiment from one or two
slugs alone?* This audit asks that question, on a sample, and proposes
a small rubric so future curation work can be scored without rerunning
the eight-entry exercise.

---

## 2. Sample selection method

The sample is **deliberate, not random**, and intentionally small
(8 entries, ~1.6 % of the 501). It was selected to span the maturity
taxonomy in `references/corpus_qa_report_v2.md` §4 plus one
hand-flagged quality-risk class (Layer-2 stub from issue #14) and the
recent internalization batch from 2026-05-19. A T7 weak-attribution
pilot was read during reconnaissance but is deliberately not scored
as a four-layer-content case because its primary risk is identity
provenance, already tracked separately. The procedure was:

1. List the seven maturity tiers via `python3 scripts/search_corpus.py
   --maturity`.
2. Pick the unique T1 entry, sample one T2 (software-paper), one
   baseline-batch T3, one wave500 T3 from the bottom of the
   `internalization_readiness_report.md` ranking, one T4 from the ML
   classification family, one wave500 Layer-2-stub T4 (issue #14), the
   T5 design-pattern representative for the runtime corpus, and one
   recently internalized T3 (the 2026-05-19 turbulence promotion batch
   from
   `corpus_qa_report_v2.md` §9).
3. Read each `SKILL.md` (full body) and the linked `metadata.yaml`
   where needed.

The eight chosen entries are listed in the next section with file
paths.

**What this sample does NOT support.** Statements about *all 501
entries*, distributions of any quantity beyond the eight, or
quantitative pass-rates on the rubric below. The corpus-level numbers
this report cites come from the manifest, not the sample.

---

## 3. Sampled entries

| # | Slug | Batch | Tier | File |
|---|---|---|---|---|
| 1 | `wu-2026-nonspherical-coronal-magnetic-field-open-flux` | `batch_pfss_source_mapping` | T1 | `references/corpus/batch_pfss_source_mapping/wu-2026-nonspherical-coronal-magnetic-field-open-flux/SKILL.md` |
| 2 | `paper-stansby-2020-pfsspy-python-pfss` | `batch_heliophysics_software_infrastructure` | T2 | `references/corpus/batch_heliophysics_software_infrastructure/paper-stansby-2020-pfsspy-python-pfss/SKILL.md` |
| 3 | `bale-2016-fields-instrument-suite-psp` | `batch_mission_instruments_data_products` | T3 | `references/corpus/batch_mission_instruments_data_products/bale-2016-fields-instrument-suite-psp/SKILL.md` |
| 4 | `paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp` | `wave500_turbulence_intermit_heating_045` | T3 (internalized 2026-05-19) | `references/corpus/wave500_turbulence_intermit_heating_045/paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp/SKILL.md` |
| 5 | `damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind` | `wave500_inner_heliosphere_psp_solo_045` | T3 (worst-debt in readiness report) | `references/corpus/wave500_inner_heliosphere_psp_solo_045/damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind/SKILL.md` |
| 6 | `klein-2018-multispecies-stability-anisotropy` | `wave500_waves_instabilities_reconnection_045` | T4 (Layer-2-stub class, issue #14) | `references/corpus/wave500_waves_instabilities_reconnection_045/klein-2018-multispecies-stability-anisotropy/SKILL.md` |
| 7 | `paper-camporeale-2017-knn-supervised-comparison-ten-models` | `wave500_sw_classification_ml_foundation_045` | T4 (stub/stub) | `references/corpus/wave500_sw_classification_ml_foundation_045/paper-camporeale-2017-knn-supervised-comparison-ten-models/SKILL.md` |
| 8 | `paper-yamada-2025-ai-scientist-v2-agentic-tree-search` | `wave500_agent_runtime_eval_design_045` | T5 (positioning skill) | `references/corpus/wave500_agent_runtime_eval_design_045/paper-yamada-2025-ai-scientist-v2-agentic-tree-search/SKILL.md` |

T6 link-only entries and the reconnaissance T7 weak-attribution pilot
are not separately scored. T6 entries are intentional pointer-style
entries where the four-layer question does not apply; the T7 pilot
requires identity-provenance triage before a four-layer-content score
would be meaningful.

---

## 4. Per-entry four-layer scoring

The scoring scheme is qualitative on purpose; the existing
`audit_internalization_readiness.py` already publishes a numeric
score per entry (cited in §6 below). What this section adds is a
*Jason-goal alignment* read — does the entry, *as written*, give an
autonomous agent enough material to (a) extract the scientific
invariant without overreach, (b) bind the executable protocol to a
real runtime, (c) keep the adapter / runtime boundary intact, and
(d) propose a verification experiment? Each layer is labelled
`strong` / `partial` / `stub` / `absent`. Line numbers are the SKILL.md
line ranges supporting the call.

### 4.1 `wu-2026-nonspherical-coronal-magnetic-field-open-flux` (T1)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **strong** | Claim narrow-form pinned to GONG CR 2282, R_init=2.5 (L42–52); seven named failure modes including mesh-coordinate sync / P1-vs-P2 / NSSS smoothing (L72–95); concrete numerical targets 9.19 vs 9.09 G·R²_sun, NSPF/PFSS≈1.98 (L96–106); explicit in-scope / out-of-scope (L107–118). |
| L2 protocol | **strong** | Eleven capability rows with abstract names (`pfss.solve_baseline`, `geometry.extract_isosurface`, `fem.solve_laplace`, …) at L125–138; numbered procedure 1–7 at L140–153; validation tolerance ±5 % nominal / 1.1 % achieved (L156–162). |
| L3 adapter boundary | **strong** | Layer 3 section labelled "examples" at L165–177; bindings explicitly tagged as *one* reproduction (`sunkit-magex`, Gmsh, FEniCSx 0.10.0); equivalents explicitly listed (deal.II, PETSc, FEnics legacy); LingTai's `.library/custom/nspf-fem/` cited *and* disclaimed as not required. |
| L4 affordance | **strong** | One named gap, one cross-skill tension (against `[[paper-multi-constraint-pfss-extrapolation-model]]`), one new hypothesis (synchronic + AI-farside Br), one composable experiment (NSPF across the coronal-hole-loop-statistics sample) — L181–201. |
| Bib | partial | Title, arXiv, year, and figure target verified; first-author initials, full author list, journal, DOI still `TODO verify` (L36–43, L218). |

**Read.** This is the corpus's load-bearing precedent. It demonstrates
that the four-layer model can be authored end-to-end without collapsing
L3 into L2 (the LingTai `.library/custom/nspf-fem/` adapter is named
*and* labelled as one example), and that a single entry can serve all
four HelioSI goals (composability, executability, runtime binding,
research generation). The remaining bibliographic gap is fixable by
one full-text pass; the four-layer authoring itself is the template
to imitate.

### 4.2 `paper-stansby-2020-pfsspy-python-pfss` (T2)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **strong** | Claim narrow-form + verifiable task at L138–151; six failure modes including R_ss as a free parameter and the open-flux problem (L213–232). |
| L2 protocol | **partial** | Two algorithms with reference-equation labels, a worked code snippet (L164–171), data-product tables with archive + cadence (L191–199). The Layer-2 contract is concrete but uses a *Python* binding inline (`pfsspy.Input`, `pfsspy.tracing.FortranTracer`) rather than abstract capability names — the L3 / L2 boundary is somewhat blurred. |
| L3 adapter boundary | **partial** | Layer-3 boundary not separated from L2 — the Python snippet sits inside §3 *Methods / equations*, not in a tagged Layer-3 block. The `mcp:jsoc` / `mcp:gong` non-assumption is stated (L199), but the wider pattern of "named tool inside L2" is the one this entry models. |
| L4 affordance | **partial** | A single research-generation paragraph at the end (L271–273) flags the open-flux-problem skill as a forthcoming entry, and the depends_on list is rich (L259–266). No explicit gap/hypothesis/tension/minimal-experiment list. |
| Bib | partial | arXiv verified (2201.07783); DOI null; tolerance + figure ID `TODO verify` (L65–67). |

**Read.** A method-ready software paper authored as if Python were the
universal runtime. This is correct for *that* paper-skill — pfsspy is
the runtime — but the entry blurs the L2 / L3 boundary in a way that
the rubric in §5 explicitly flags. A future Layer-3-tagged block
("example bindings: pfsspy / sunkit-magex / pfss-tracing") would
cleanly separate the contract from the example. The lack of an
explicit research-generation-affordance block (gap / hypothesis /
experiment) limits L4 reuse.

### 4.3 `bale-2016-fields-instrument-suite-psp` (T3, internalized)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **strong** | Full 83-author list verified via Crossref on 2026-05-19 (L40–56); DOI 10.1007/s11214-016-0244-5 verified; six failure modes with concrete propagation rules (L154–173); in-scope / out-of-scope explicit (L186–199). |
| L2 protocol | **partial** | Sensor → level → frame → encounter → contract-JSON workflow is well-structured (L107–143); the JSON pseudocode is a small but real contract. The Layer-2 capability surface is implicit ("retrieval of PSP FIELDS L2 products from an SPDF/CDAWeb-class archive") rather than enumerated as named capabilities. |
| L3 adapter boundary | **partial** | The `cdflib` / `pyspedas` examples are referenced (L107, L150), and `xhelio-cdaweb` is the implied first-class MCP (per `README.md`), but the entry is in the older `prose_engineering_instrument` rendering family and does not carry an explicit Layer-3 sub-section. |
| L4 affordance | **strong** | Four named research-generation affordances at L212–235 — per-encounter caveat-propagation audit, sensor-selection-rubric as a teachable contract, cross-validation against Solar Orbiter MAG, antenna-shadow geometry impact on DC-E science. These are concrete, composable, and tied to other slugs. |
| Bib | strong (modulo cosmetic) | DOI and 83-author list verified 2026-05-19; ADS bibcode derived but flagged "not directly fetched"; arXiv "not-in-local-inventory". |

**Read.** A high-quality internalized entry. Note the *cosmetic*
honesty problem at L253–255: even after the Crossref-verified 83-author
list and DOI, the trailing references block still reads "identity /
DOI **TODO verify with full text**". The actual L1 content is now
correct, but a downstream agent grepping for `TODO verify` would
mis-flag this entry as unverified. This is the kind of staleness the
rubric in §5 calls out as a *cosmetic-residual-TODO* anti-pattern; it
is also what the `audit_authorship_prose.py` audit catches at a finer
granularity (S4g in `validate.sh`). The L4 block here is one of the
clearest in the sample.

### 4.4 `paper-duan-2021-kinetic-anisotropy-slow-alfvenic-psp` (T3, internalized 2026-05-19)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **strong** | Verified claim with explicit boundary (slow-Alfvenic E1 only) at L74–87; six failure modes including Taylor-hypothesis breakdown and branch ambiguity (L88–94, L236–258); five numerical targets including specific spectral indices and anisotropy ratios (L61–66). |
| L2 protocol | **strong** | Six abstract capabilities with named contracts ("High-cadence MAG reader", "Wavelet PSD with directional decomposition", "theta_kB binning", "Per-bin power-law fitter", "Magnetic compressibility C||", "Linear-Vlasov KAW reference"), each one paragraph (L176–195); numbered procedure 1–8 with explicit acceptance criterion (L197–210); explicit tolerance budget (L231–235). |
| L3 adapter boundary | **strong** | `adapter_notes: []` in the YAML frontmatter (L97); L3 is not author-bound to any specific runtime. The contract is portable. |
| L4 affordance | **strong** | Frontmatter `research_generation_affordances[]` block with four typed entries — gap, hypothesis, tension, composable_experiment — at L98–109; mirrored in §9 narrative (L281–300). |
| Bib | strong | DOI verified, ADS bibcode pattern-checked, arXiv abstract-page verified, IOPscience landing-page verified, all on 2026-05-19; `verified_by` and `verified_at` fields populated; `verification_notes[]` carries per-field provenance (L114–119). |

**Read.** Together with §4.1, this is the structural model for the
rest of the corpus. The 2026-05-19 internalization pass appears to
have produced exactly the four-layer object Jason wants: verified
identity, executable protocol against abstract capabilities, no
adapter leakage in L2, and a research-generation block with typed
affordances. If this is what every T3 entry looked like, the corpus
would be substantially closer to "agent-callable substrate."

### 4.5 `damicis-2026-alfvenic-slow-wind-parcels-psp-solo-wind` (T3, worst-debt in readiness ranking)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **partial** | Claim narrow-form present (L51); two failure modes (L67–69); claim boundary present (L42–43). But §2.5 *Figure / numerical targets* is the factory's literal TODO placeholder (L73–75); §2.3's data products are abstract instrument rows with `TODO verify dates`. |
| L2 protocol | **stub** | Three algorithm sub-sections each read "Abstract procedure (runtime-neutral): documented in the paper; runtime supplies the named capability" (L84–93). This is the *factory boilerplate string* enumerated in `audit_internalization_readiness.py::LAYER2_BOILERPLATE` — the section declares the *shape* of a procedure but carries no procedure. The §1 banner correctly warns "Layer 2 not populated — read paper before use." |
| L3 adapter boundary | **partial** | Adapter notes paragraph at L116–122 is generic — "Any harness capable of CDF I/O + standard time-series analysis can satisfy the contracts; named tools (pyspedas, sunpy, sunkit-magex, pfsspy, sw-scanner) are *example* adapters." This *does* preserve the boundary, but provides essentially no Layer-3 information. |
| L4 affordance | **partial** | One hypothesis (WKB-Alfvenic-amplitude radial scaling), one gap (no non-Alfvenic slow-wind sibling) — both authored, but with `Related: (no explicit sibling)` (L127–128), so they do not yet land on the skill graph. |
| Bib | weak | arXiv and DOI both `TODO_verify_with_full_text` (L134–135). |

**Read.** Honest in its self-banner ("Layer 2 not populated"), and the
issue-#14 stub-flag makes this entry invisible to
`--ready-for experiment` and `--ready-for hypothesis`. The
self-banner is the right pattern. What this entry *also* shows is
that Layer-1 numeric targets (§2.5) and Layer-3 example-binding
content (§4) can degrade in the same way Layer 2 does — the boilerplate
phrase recurs. The rubric in §5 lists Layer-1 and Layer-4 boilerplate
detectors that `audit_internalization_readiness.py` does not yet score
explicitly.

### 4.6 `klein-2018-multispecies-stability-anisotropy` (T4, lowest-scoring entry in readiness report at 42.43/100)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **partial** | Narrow claim (L42); three short failure modes (L57–60); claim boundary (L34); validation target single line "Recovers Gary–Wang multi-species stability map within stated tolerance (TODO verify)" (L64). |
| L2 protocol | **stub** | Three capability contracts (`C-LIN-VLASOV-MULTI`, `C-K-SCAN`, `C-POLARIZATION-DIAG`) named with two-word descriptions (L72–74); four-step abstract procedure (L78–82); no equations, no parameters, no acceptance criterion. |
| L3 adapter boundary | **partial** | Single line "PLUME, NHDS, ALPS are example Layer-3 bindings" (L92). Honest as far as it goes; not separated into a tagged block. |
| L4 affordance | **stub** | Two single-line bullets ("Composability with all kinetic-instability skills"; "Methodological experiment: extend to non-Maxwellian closure") (L98–99); no typed affordances, no related-slug links. |
| Bib | absent | `arxiv` link is the literal placeholder `https://arxiv.org/abs/TODO_verify_with_full_text` (L105); DOI null (L106); first-author / authors / venue all unset upstream. |

**Read.** This is what a wave500 entry looks like at the bottom of the
internalization-readiness ranking, and it backs the existing
report's finding that scaffold-tier entries can pass *every* structural
audit (counts, schemas, frontmatter, wikilinks) while delivering
almost no scientific content. The four named capabilities are the
right *shape* — they could legitimately become a Layer-2 contract
once the source paper is read — but right now they would mislead a
hypothesis-generation loop into thinking this entry is composable
with the rest of the waves/instabilities batch.

### 4.7 `paper-camporeale-2017-knn-supervised-comparison-ten-models` (T4)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **partial** | Claim sentence + stub banner at L96–98; the *parent* entry (`paper-camporeale-2017-knn-solar-wind-categorization`, sampled separately) carries the substantive Layer-1 content the stub points at. Failure modes (L129–131) are about *the act of relying on this stub*, not about the underlying science — a deliberate stub-tier pattern. |
| L2 protocol | **stub** | §3, §4, §5 are *honest stubs* — each one says explicitly "Layer 2 is not yet populated" with a numbered list of how to promote (L105–125). This is the strongest stub-tier pattern in the sample: it does not invent content. |
| L3 adapter boundary | **strong (for its tier)** | §8 explicitly empty: "Adapter binding examples (optional, illustrative only): none recorded at stub tier" (L155–156). |
| L4 affordance | **partial** | Two typed affordances in the frontmatter (`research_generation_affordances[]` at L50–54) and a numbered §9 affordance block (L160–167) — but the only affordance is "promote to method-ready." It is honest, but it does not actually feed downstream hypothesis generation. |
| Bib | partial | arXiv verified to the parent slug; DOI / ADS / venue / code all `TODO verify` (L8, L20, L23, L38). |

**Read.** This is the model the `wave500_sw_classification_ml_foundation_045`
batch follows for the dependent-stub pattern: a separate slug that
exists *only* to be referenced and to record a promotion plan. The
honest empty Layer-2 and Layer-3 blocks here are exactly what the
rubric in §5 rewards. The risk is that a hypothesis-generation loop
that only walks the graph by slug count cannot tell this entry from
its parent — a future filter like `--exclude-promotion-only-stubs`
might be valuable.

### 4.8 `paper-yamada-2025-ai-scientist-v2-agentic-tree-search` (T5, runtime / positioning)

| Layer | Verdict | Evidence |
|---|---|---|
| L1 invariant | **partial** | Claim narrow-form is *bounded to the workshop-acceptance result* (L120); three failure modes including the heliophysics-transfer caveat (L65–68); claim boundary explicitly excludes natural-science journal generalisation (L189–198). |
| L2 protocol | **stub** | Four "Method N" sub-sections each say "Abstract procedure: the runtime that wants to borrow this pattern must be able to (a) instantiate the component as a callable, (b) feed it the manuscript / benchmark / sibling-skill inputs from §4, and (c) emit an artifact a Layer-4 affordance can reference" (L136–155). This is the second factory boilerplate phrase that `audit_internalization_readiness.py::LAYER2_BOILERPLATE` already detects, and the entry's `quality: positioning-skill-not-executable-science` + `executable_status: design-pattern-extractor` (L8, L101) correctly signal that this is *not* an executable workflow. |
| L3 adapter boundary | **strong** | `adapter_notes: []` and "Adapter notes intentionally empty" (L74, L208). |
| L4 affordance | **strong** | Two typed affordances — *minimal_experiment* ("Adopt the experiment-manager pattern in HelioSI: have a manager agent expand/prune a tree of heliophysics workflow candidates …") and *gap* ("v2's tree-search has no scientific-simulation verifier per node; HelioSI can plug in PFSS / sw-scanner / sunkit-magex as verifiers per branch") — both with proposed actions (L75–80, L220–222). |
| Bib | strong | arXiv ID, full eight-author list, code repo all present and verified by the original drafter; venue is `arXiv preprint` (honest). |

**Read.** A clean example of the T5 design-pattern-extractor class.
The four "Methods" lines in §3 are deliberately templates — the entry
is *not* trying to be an executable heliophysics workflow, and the
frontmatter quality flag says so. The L4 affordances are genuinely
useful: they nominate a concrete HelioSI runtime upgrade (verifier-MCP
contract per branch) tied to the agent-runtime design-pattern. This
demonstrates that T5 entries should NOT be measured on L2 executability
— they should be measured on L4 transplant-quality. The current
audits do not yet split scoring this way.

### 4.9 Sample synthesis

Recurring gaps the sample exposes (each backed by ≥2 sampled entries):

- **G-L2-BOILER.** Factory boilerplate phrases ("documented in the
  paper; runtime supplies the named capability"; "abstract procedure:
  the runtime that wants to borrow this pattern…") survive into
  Layer-2 sections and Layer-1 numeric-target sections in
  scaffold-tier entries (§4.5, §4.6, §4.8). The
  `audit_internalization_readiness.py` script already detects the
  former two in Layer 2; it does not yet score Layer 1 §"Figure /
  numerical targets" or Layer 4 with the same vocabulary.
- **G-L2-L3-BLUR.** Method-ready entries that use a single canonical
  Python package inline (e.g. pfsspy in §4.2) tend to put adapter
  examples inside Layer-2 *Methods / equations* sections rather than
  in a tagged Layer-3 block, blurring the boundary the corpus
  documents as load-bearing.
- **G-COSMETIC-TODO.** Internalized entries (§4.3) retain trailing
  "TODO verify with full text" markers after the L1 content has been
  verified, because the closing References block is not regenerated
  on internalization. This is a cosmetic-honesty problem, not a
  data-honesty problem, but it is exactly what `audit_authorship_prose.py`
  is designed to catch *for the authorship surface*. An analogous
  audit for *bibliographic* surfaces would cover the same hazard.
- **G-L4-AFFORDANCE-PRESENT-BUT-EMPTY.** 248 / 501 manifest entries
  carry `research_generation_affordances_present == true`; **388 / 501**
  carry `research_generation_affordances_count == 0` — i.e. **141**
  entries are flagged "present" with no listed affordance. (Manifest-
  level count, recomputed 2026-05-20.) The sample's §4.6 (klein-2018)
  is one such entry — a two-sentence "composability" claim is enough
  for the flag but not enough for a hypothesis loop.
- **G-NO-ADAPTER-LAYER-TRUE.** Across the 51 entries that ship the
  frontmatter `layers:` block as a fully-populated dict (i.e. not
  `null`), `adapter_binding_examples` is `true` on **0** entries.
  (Manifest-level count, recomputed 2026-05-20; this is consistent with
  `corpus_qa_report_v2.md` §9's per-layer-true counts table reporting
  `adapter_binding_examples: 0`.) This is honest — the corpus does
  not bundle adapters — but it means **no entry currently advertises a
  worked Layer-3 example** at the boolean surface. The Wu 2026 T1
  entry (§4.1) actually carries one, but its `layers:` block is
  `null`, so the boolean surface does not reflect it. A surface where
  L3 is structurally empty cannot be the surface a runtime queries
  for adapter availability.

---

## 5. Proposed quality / promotion rubric

This rubric is **a sample-derived starting point**, not a corpus-wide
gate. It complements `DISCOVERY_POLICY.md` §3 (which already governs
the *draft → corpus* gate) by adding a *corpus-internal* "is this
entry actually doing the four-layer job?" check. Each item is
deliberately phrased so an audit script could later score it; this
report does *not* claim every existing entry passes the rubric and
does *not* propose making the rubric blocking.

**The rubric is scored per-entry as a 0–4 count of layers `strong`,
plus three Y/N add-on flags. It does NOT replace the maturity tier
T1–T7; it sits orthogonal to it.**

### R1 — Scientific invariant layer (Layer 1)

Pass when:

- The *narrow-form claim* sentence is bounded (named mission /
  encounter / instrument / regime / parameter window).
- Method assumptions are recorded — not just equation names, but the
  load-bearing assumptions (closure, boundary condition, frame).
- ≥2 named failure modes are recorded, each with a propagation rule
  (what the agent must do if the failure mode applies).
- ≥1 figure / table / numeric target is named *and* either has a value
  or is explicitly flagged `pending full text` (not the factory
  boilerplate; the placeholder must be either the paper-provided
  target or a labelled stub).
- Explicit in-scope and out-of-scope sentences.

Anti-pattern: the §"Figure / numerical targets" or §"Validation target"
section is a verbatim factory-template sentence containing the words
"runtime supplies the named capability" or "Abstract procedure: the
runtime that wants to borrow this pattern" or "pending full-text
verification" without a paper anchor. These trigger G-L2-BOILER on
the Layer-1 surface.

### R2 — Executable protocol layer (Layer 2)

Pass when:

- ≥1 named *abstract* capability per algorithm — capability names use
  the `noun.verb_subject()` or `C-NAMED-CAPABILITY` style, *not* a
  bound Python import.
- A numbered procedure with ≥3 steps and an explicit acceptance step.
- A validation target that is either (a) a paper figure / table number
  with a metric and tolerance, or (b) a clearly labelled stub with a
  promotion plan (§4.7 is the model).
- If a `xhelio-spice` / `xhelio-cdaweb` / other MCP would be needed
  to satisfy a capability, it is named as a *prerequisite*, not a
  *fallback*.

Anti-pattern: a Python snippet sitting inside §"Methods / equations"
without a parallel abstract capability surface (§4.2 case). The entry
may still be useful — but Layer 2 is then implicitly Python-bound,
which violates the harness-agnostic invariant.

### R3 — Adapter / runtime boundary (Layer 3)

Pass when EITHER:

- A tagged Layer-3 block exists with the prose "examples only" or
  "intentionally empty" or "one reproduction's binding" — and named
  packages live exclusively in that block.
- The entry's `adapter_notes: []` is explicitly empty and §"Methods /
  equations" contains no named package.

Anti-pattern: named Python packages (`pfsspy`, `sunkit-magex`, `pyspedas`,
…) inside §"Methods / equations" with no Layer-3 demarcation — this
makes the entry look method-ready *only* on a Python runtime, even
though Layer 2 is supposed to be harness-agnostic.

### R4 — Research-generation affordance (Layer 4)

Pass when:

- ≥1 typed affordance — `type` ∈ {gap, tension, hypothesis,
  minimal_experiment, composable_experiment} — with a one-sentence
  statement and *either* a `proposed_action` *or* a `related_skills[]`
  list that lands on a real slug.
- The affordance is not a generic promotion plan ("promote to
  method-ready by reading the paper") — that pattern is fine inside
  a §4.7-style stub but should NOT count as a research-generation
  affordance for the headline rubric, since it does not feed a
  hypothesis loop.

Anti-pattern: `research_generation_affordances_present == true` in
the manifest with zero `research_generation_affordances` actually
authored in the frontmatter or body — see G-L4-AFFORDANCE-PRESENT-BUT-EMPTY
in §4.9.

### R5 (add-on flag) — Identity-prose hygiene

Pass when:

- The entry's References / Links block at the *end* of `SKILL.md`
  contains no "TODO verify with full text" marker once the relevant
  bibliographic field is verified in `metadata.yaml` or in the body's
  Paper-identity block.

Anti-pattern: §4.3 — full author list and DOI verified at L40–60, but
the trailing block at L253–255 still warns the reader the identity is
unverified. Cosmetic, but mis-signals to grep-driven agents.

### R6 (add-on flag) — Self-banner honesty

Pass when:

- If Layer 2 is a stub, the entry carries a visible banner at the top
  of `SKILL.md` (the §4.5 / §4.7 model). The Layer-2-stub flag in
  `metadata.yaml` (`layer2_stub: true`) is mirrored in prose.

This is already mostly true for the 55 issue-#14 stubs; the add-on
flag exists to keep that honest as the corpus evolves.

### R7 (add-on flag) — Layer-3 surface honesty

Pass when:

- If the entry's frontmatter `layers:` block ships, then
  `adapter_binding_examples` is either `true` (with a real example in
  §"Layer 3" / §"Adapter notes") OR `false` with no named runtime
  packages inside §"Methods / equations".

This is the rule G-L2-L3-BLUR / G-NO-ADAPTER-LAYER-TRUE in §4.9 are
asking for.

---

## 6. Relation to existing audits

This rubric does NOT duplicate any existing audit; the table below
records what it adds.

| Existing audit | What it scores | What this rubric adds |
|---|---|---|
| `scripts/audit_layer_population.py` / `tests/test_layer_population.py` | Per-entry `layers:` boolean parity between metadata.yaml and SKILL.md frontmatter | Whether the four-layer *content* matches the boolean (G-NO-ADAPTER-LAYER-TRUE), and whether Layer-3 named bindings live where the layer boundary says they should (R3 / R7). |
| `scripts/audit_layer_schemas.py` | Per-entry H2-header rendering family (six families) | Not duplicated — this rubric scores content, not header shape. The rendering family determines *where* L1–L4 live; the rubric assumes a classifier already located them. |
| `scripts/audit_layer2_stubs.py` + issue #14 flag | Which entries are Layer-2 stubs (55 entries) | Whether the stub-banner pattern (R6) is actually present in prose, not just in the YAML flag. |
| `scripts/audit_numeric_claims.py` | Whether numeric claims in body match `validation_targets[]` and `references/numeric_claims_expected.json` | Whether the §"Figure / numerical targets" *prose* is real text vs the factory boilerplate (R1 anti-pattern). |
| `scripts/audit_internalization_readiness.py` | Quantitative 0–100 score per entry on bib + L1 + L2 + validation + L4 + identity + TODO density | Same underlying signals; this rubric exposes them as a checklist with the anti-pattern catalogue (G-L2-BOILER, G-L2-L3-BLUR, G-COSMETIC-TODO, G-L4-AFFORDANCE-PRESENT-BUT-EMPTY, G-NO-ADAPTER-LAYER-TRUE) so reviewers can act on specific entries without consulting the score. |
| `scripts/audit_authorship_prose.py` | Authorship strings ("first author", "by Smith et al.") in prose surfaces | Bibliographic cosmetic-TODO residue (R5) — distinct surface, analogous mechanism. |
| `scripts/audit_wikilinks.py` + `scripts/build_corpus_skill_graph.py` | Wikilink resolution; graph edges | Whether a Layer-4 affordance lands on a real slug (R4 add-on). |

---

## 7. Manifest-level cross-cuts (not from the sample)

Two numbers from the manifest are load-bearing for the rubric above
and were re-computed for this report on 2026-05-20:

- **L4-affordance presence vs count divergence.** 248 / 501 entries
  carry `research_generation_affordances_present == true`; 388 / 501
  carry `research_generation_affordances_count == 0`. Difference =
  **141** entries flagged "present" with no listed affordance.
  Recompute: `python3 -c "import json; m=json.load(open('references/
  corpus_manifest_v2.json')); e=m['entries']; print(sum(1 for x in
  e if x.get('research_generation_affordances_present')),
  sum(1 for x in e if not (x.get('research_generation_affordances_count'
  ) or 0)))"`. This is the empirical backing for R4 / G-L4-
  AFFORDANCE-PRESENT-BUT-EMPTY.
- **Adapter-layer boolean is structurally empty.** Of the 51 entries
  whose manifest `layers` field is a populated dict (not `null`),
  **0** have `adapter_binding_examples == true`. Recompute: same JSON
  walk. This is consistent with `corpus_qa_report_v2.md` §9's
  per-layer-true counts (Layer 3 = 0). The Wu 2026 T1 entry (§4.1)
  carries a real Layer-3 block but its `layers:` field is not
  populated, so the boolean surface does not advertise it.

These are honest reflections of the corpus's "scaffold / triage
substrate" framing, not bugs. They are the *cost* of preserving the
four-layer structure honestly; the rubric in §5 names them so that
future curation passes can decide which to close.

---

## 8. Validation results

`bash scripts/validate.sh` was run from a clean working tree on
2026-05-20. All sections returned OK:

- S1 structural counts: pass (501 / 18).
- S2 manifest cross-check: pass (`batches=18 entries=501
  unique_slugs=501`).
- S3 v2 roll-up files present: pass.
- S4b per-entry SKILL.md frontmatter coverage: pass (501 / 501).
- S4c per-entry metadata.yaml parses: pass (501 / 501 with PyYAML).
- S4d authorship-field hygiene: pass (no placeholders).
- S4e arXiv ID provenance hygiene: pass (28 / 531 advertised slots
  verified via HTTP-title-match).
- S4f authors_verified parity: pass (160 / 501 stamped false on both
  surfaces).
- S4g authorship-prose audit: pass.
- S4h unflagged numeric claims: pass.
- S4i per-batch manifest.json authorship hygiene: pass (18 / 18).
- S4 helper-script smoke tests: pass.
- S5 internalization-readiness audit (active entries only): pass
  (45 active entries scanned).
- S6 wikilink audit (informational): pass (1752 wikilinks; 56
  unresolved; classified into the GRAPH_POLICY.md buckets).
- S7 corpus skill graph build (informational): pass (501 nodes,
  688 edges, 23 external-reference candidates).

Final line: `validate.sh: OK -- all checks passed`.

This report makes no edits to corpus files, scripts, or tests, so the
validation status is unchanged.

---

## 9. Recommended next PRs (small, bounded, honest)

Each item is sized to be one PR, contains no corpus rewrites, and
preserves the existing claim-boundary discipline. Order is by
expected value-per-effort.

### PR-A. Add this rubric as a normative reference doc

Smallest possible follow-up: keep `reports/skill_quality_alignment_audit.md`
(this file) as-is, and add a single pointer line from
`DISCOVERY_POLICY.md` §3.3 ("Layer 1–4 authoring") and from
`README.md` §"Verification status" to it. No corpus edits. No new
script. The rubric becomes the corpus-internal counterpart to the
discovery-side gate. **Risk:** zero — pure documentation pointer.

### PR-B. Extend `audit_internalization_readiness.py` boilerplate detection to Layer-1 and Layer-4 surfaces

The script already detects two Layer-2 boilerplate phrases. Extend its
constants — `LAYER1_BOILERPLATE` ("pending full-text verification — quality
tier is `paper-grounded-pending-full-text`. The paper's reproducible
numerical anchor lives in its figures/tables") and `LAYER4_BOILERPLATE`
(already exists for "Adapter notes intentionally empty"; add the
"promote to method-ready by populating §3/§4/§5 against the full text"
template) — and pin the resulting counts in a new test. This converts
G-L2-BOILER from a sample observation into a CI-visible signal,
without making it blocking. **Risk:** low. The script is non-blocking
by default; the new counts will surface in `validate.sh` S5 but only
fail under `--strict-active`. Worth double-checking that the chosen
boilerplate strings do not match legitimately-authored prose; the
existing two strings have been corpus-tested.

### PR-C. Add a *trailing-cosmetic-TODO* audit (the R5 add-on)

A tiny new audit script (`scripts/audit_bibliographic_prose.py`)
that scans the closing References / Links block of each SKILL.md for
`TODO verify with full text` / `TODO_verify_with_full_text` and
*cross-checks* whether the corresponding metadata.yaml field (DOI,
arxiv, authors, venue) is now populated and `authors_verified: true`.
When the metadata is verified but the prose still warns, surface the
entry as G-COSMETIC-TODO. Non-blocking by default; pin the current
count in a test. **Risk:** the audit is a string-comparison on prose;
false positives are possible on entries where the warning is intentional
(e.g. the Wu 2026 T1 entry's reference to its own initials). Ship
with a curated allow-list and a `--list` flag.

### PR-D. Re-author the `layers:` boolean surface on the Wu 2026 T1 entry

Single-entry edit (not a mass edit): the T1 entry's manifest `layers:`
field is `null`; its actual content carries all four layers
(strong / strong / strong / strong per §4.1). Populate the
`layers:` block in `metadata.yaml` and `paper.layers:` in `SKILL.md`
frontmatter to `{scientific_invariant: true, executable_protocol:
true, adapter_binding_examples: true, research_generation_affordance:
true}`. This is the corpus's first entry where all four can honestly
be `true`. It also gives the corpus a single concrete example for
the "what does a four-true entry look like?" question that
`README.md` §"Layers populated" leaves open. **Risk:** the
`audit_layer_population.py --strict` test pins
`adapter_binding_examples == 0` and the all-four-true count at 0;
both have to be updated in the same PR, and the test must be
regenerated. The change is honest only if a human reviewer agrees
the Layer-3 block in `SKILL.md` (L165–177) is substantive enough.

---

## 10. Parent-review risks (this PR)

- **R-SAMPLE-SIZE.** Eight entries out of 501. The rubric is honest
  about being sample-derived; the per-entry verdicts in §4 are
  defensible because they cite line numbers, but corpus-wide
  claims in §4.9 / §7 are restricted to manifest-level counts and
  should be re-verified before they are repeated externally.
- **R-RUBRIC-NOT-BLOCKING.** §5 deliberately does not propose making
  the rubric a CI gate. If a reviewer wants it to be one, the existing
  `audit_internalization_readiness.py --strict-active --min-active-score`
  flag is the right place — but raising the bar would require deciding
  what to do with the 45 active entries that already sit below 70.
- **R-NEW-AUDIT-COMPLEXITY.** PR-B and PR-C add new boilerplate
  detection. Each new pattern is a future-source-of-false-positives; a
  conservative review should confirm the chosen strings do not match
  legitimate prose in unrelated entries.
- **R-WU2026-TIER-CHANGE.** PR-D edits the T1 entry's frontmatter
  `layers:` block. Doing so is a curated edit to one entry, *not* a
  mass schema change; but it crosses an honesty threshold (the first
  all-four-true entry) and should be reviewed for whether the L3 block
  there genuinely warrants `adapter_binding_examples: true`.
- **R-G-COSMETIC-TODO-SCOPE.** PR-C scans the *closing* block of each
  SKILL.md. Some entries (e.g. §4.7 stubs) carry warnings inside §1
  that are *intentional* skill memory; the audit must be scoped to
  the trailing References section, not the body.
- **R-NO-CORPUS-EDITS.** This audit is report-only. Recommendations
  in §9 are sized to be small follow-up PRs, not bundled into this
  commit.
