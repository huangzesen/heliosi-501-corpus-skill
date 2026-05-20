# Curation triage — `external_reference_candidate` (23 entries)

**Status:** informational; report-only. Does NOT modify any per-entry
`SKILL.md`, does NOT touch the manifest, does NOT change graph counts
or audit counts.
**Scope:** the 23 unresolved wikilink targets carrying the
`external_reference_candidate` classification in
[`references/corpus_skill_graph.json`](../references/corpus_skill_graph.json)
at commit `4cf4201`.
**Policy basis:** [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.4 (what
the classification means) and §5 step 4 (recommended curation
workflow for runtime / tool / loader names).
**Sister report:** the parallel triage for
`paper_reference_needs_curation` (10 entries) is at
[`reports/wikilink_curation_paper_refs.md`](wikilink_curation_paper_refs.md).

---

## 1. Why this report exists

[`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.4 explains that an
unresolved wikilink with no `paper-` prefix and no audit suggestion
typically names off-corpus *runtime / tool / loader* infrastructure
that a paper-skill references but does not internalize:

> The corpus prose typically uses this form for runtime / tool /
> loader names (`pfss-tracing`, `nspf-fem`, `psp-sweap-bulk-loader`,
> `switchback-boundary-finder`, …) — i.e. off-corpus infrastructure
> that a paper-skill names but does not internalize.

§3.4 also explicitly warns:

> **Non-authoritative.** […] A target landing in this bucket can
> also be a typo of a paper slug or another unresolved prose token
> whose meaning cannot be inferred mechanically.

§5 step 4 then gives the recommended motion:

> 4. If it is a runtime / tool name, leave it as an
>    `external_reference_candidate` and (optionally) move the
>    reference to a non-wikilink form (`pfss-tracing` in backticks
>    rather than `[[pfss-tracing]]`) so the graph no longer carries
>    it as a prose wikilink.

The graph artifact deliberately stops there. What it does NOT do
(per [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §4) is recommend a
disposition or distinguish runtime-shaped tokens from paper-shaped
typos, because that is a content decision, not a mechanical one.

This report fills exactly that gap for the
`external_reference_candidate` bucket at one snapshot of the corpus
(`4cf4201`). For each of the 23 entries it records:

1. The unresolved wikilink target (verbatim from the graph artifact).
2. Every referrer (`path:line`) plus the quoted prose line.
3. A **shape classification** — does the target read as runtime /
   tool / loader infrastructure, or as a paper-shaped slug typo?
4. A **partial-match probe** against the manifest by token overlap
   for paper-shaped targets — strictly mechanical, no full-text
   verification.
5. A **candidate disposition** drawn from the vocabulary in §2 below,
   with one-sentence justification.

The candidate disposition is a hint for a curator review, not a
verdict. No SKILL.md was edited; no slug was invented; no DOI was
claimed; no manifest entry was added. Closing each entry remains a
separate, deliberate PR.

## 2. Disposition vocabulary (used in §4)

| Code | GRAPH_POLICY §5 mapping | Meaning |
|---|---|---|
| **K — keep-as-external-reference** | §5 step 4 ("leave it as an `external_reference_candidate`") | The target is genuinely off-corpus runtime / tool / loader infrastructure, the referring prose treats it as a named adapter pointer, and the `[[...]]` form is intentional (a future external-node schema or an adapter index might consume it). Closing motion: none — status quo. |
| **B — demote-to-backticks-or-plain-prose** | §5 step 4 ("optionally move the reference to a non-wikilink form") | Same shape as K, but the `[[...]]` brackets are *incidental*: the citing prose would read identically with `` `name` `` and the graph no longer carries the reference as an unresolved wikilink. The default conservative motion for tool / loader names. Closing motion: edit the citing SKILL.md to drop the brackets. |
| **R — rename-to-existing-canonical-slug** | §5 step 2 ("slug typo that maps onto an existing manifest entry") | The target reads as a paper slug (author-year-topic shape) and a manifest entry matches under `(first_author, year, topic)` tokens. Closing motion: edit the citing SKILL.md to use the canonical slug. Needs a one-line author check that the citing prose really means the canonical paper. |
| **I — internalise-via-discovery-pipeline** | §5 step 3(a) | The target reads as a real off-corpus paper (author-year-topic shape) and no manifest entry matches. Closing motion: feed the author / year / topic into [`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md)'s candidate-lifecycle pipeline. |
| **N — promote-to-future-external-namespace** *(deferred, not adopted)* | n/a (future option) | A future PR may decide that off-corpus runtime / tool / loader names deserve a first-class external-node schema (own provenance, own classification, distinct from paper-skills). This report does NOT define such a schema and does NOT recommend adopting one in this increment. Recorded only as a possible direction; landing in this bucket means "K for now, revisit later." |

**Important:** none of K / B / R / I claim the underlying target is
verified. R only claims a *candidate* slug match; I leaves
verification to the discovery pipeline; K and B leave the question of
whether the off-corpus runtime exists in any registry strictly to a
future adapter-index PR.

## 3. Snapshot reconciliation

This report is consistent with the graph artifact at commit `4cf4201`:

| Metric | Value |
|---|---:|
| Corpus nodes | 501 |
| Resolved edges | 688 |
| Inline-code / fenced-code wikilink occurrences excluded from edges | 518 |
| Unresolved wikilink targets (all classifications) | 56 |
| ↳ `paper_reference_needs_curation` (sister report) | 10 |
| ↳ `external_reference_candidate` (this report) | **23** |
| ↳ `inline_code_canonical_suggestion` | 17 |
| ↳ `inline_code_literal` | 6 |
| Entries with explicit `## Skill graph → depends_on` section | 105 |

The 23 rows below sum to **34 wikilink occurrences across 17
referring SKILL.md files**.

## 4. Shape classification at a glance

Before per-entry detail, the 23 targets split cleanly along
shape lines:

| Shape | Count | Targets |
|---|---:|---|
| **Runtime / tool / loader / adapter** (no author-year-topic shape; explicit "TODO create" or LingTai-adapter prose) | 18 | `pfss-tracing`, `hall-mhd-residual-classifier`, `messenger-mag-loader`, `messenger-solar-wind-filter`, `parker-spiral-propagator`, `parker-transport-sde-solver`, `pfss-footpoint-mapper`, `psp-fields-efield-loader`, `psp-fields-mag-hcs-identifier`, `psp-isois-epi-data-loader`, `psp-sweap-bulk-loader`, `psp-walen-test-classifier`, `rotational-discontinuity-finder-mhd`, `so-swa-bulk-loader`, `switchback-boundary-finder`, `synthetic-switchback-generator`, `trace-psd-broken-power-law-fitter`, plus the meta-reference `wikilinks` |
| **Paper-shaped slug** (author-year-topic; classified as ERC only because it lacks the `paper-` prefix the audit looks for) | 5 | `raouafi-2023-psp-four-years-discoveries-review`, `bowen-2024-cyclotron-resonance`, `shankarappa-2025-free-energy-sources-ion-scale-waves`, `stverak-2026-solo-swa-eas-spacecraft-electron-contamination`, `verniero-2023-proton-alpha-instabilities-ion-cyclotron` |

This split is the load-bearing observation: the bucket name
`external_reference_candidate` is honest about its non-authoritative
status (per §3.4), and roughly one-fifth of the bucket is actually
paper-shaped curation debt that the audit could not detect because
the prefix-stripping heuristic only fires for `paper-`-prefixed
targets.

## 5. The 23 entries

### 5.1 `pfss-tracing` — 9 occurrences (8 inline-code, 1 prose)

- `batch_pfss_source_mapping/ai-farside-synchronic-coronal-field-extrapolation/SKILL.md:152` *(inline-code)*
  > ``LingTai's `[[pfss-tracing]]` provides one binding of `pfss.solve` but``
- `batch_pfss_source_mapping/ai-farside-synchronic-coronal-field-extrapolation/SKILL.md:159` *(prose)*
  > `- **Gap:** every PFSS source-mapping skill ([[pfss-tracing]],`
- `batch_pfss_source_mapping/comparison-coronal-extrapolation-cycle-24-hmi/SKILL.md:146` *(inline-code)*
  > ``LingTai's `[[pfss-tracing]]` supplies one binding of `pfss.solve`; no``
- `batch_pfss_source_mapping/coronal-hole-loop-statistics-potential-field-modeling/SKILL.md:156` *(inline-code)*
  > ``LingTai's `[[pfss-tracing]]` binds `pfss.solve` + `field.trace_lines```
- `batch_pfss_source_mapping/dakeyo-2026-source-alignment-psp-solo-method-link/SKILL.md:133` *(inline-code)*
  > `` `[[pfss-tracing]]` provides one binding.``
- `batch_pfss_source_mapping/eclipse-white-light-benchmark-pfss-models/SKILL.md:154` *(inline-code)*
  > ``- LingTai's `[[pfss-tracing]]` binds `pfss.solve` +``
- `batch_pfss_source_mapping/ervin-2024-slow-alfvenic-source-regions-pfss-psp/SKILL.md:173` *(inline-code)*
  > ``LingTai supplies bindings via `[[pfss-tracing]]` and an in-situ skill``
- `batch_pfss_source_mapping/multi-constraint-pfss-extrapolation-model/SKILL.md:160` *(inline-code)*
  > ``LingTai's `[[pfss-tracing]]` custom skill provides one binding of``
- `batch_pfss_source_mapping/pfss-test-problems-solar-stellar-magnetic-fields/SKILL.md:158` *(inline-code)*
  > ``LingTai's `[[pfss-tracing]]` and `[[nspf-fem]]` are concrete *adapter``

**Shape:** runtime / tool / loader. The citing prose consistently
names `pfss-tracing` as a *LingTai adapter* that binds an abstract
Layer-2 capability (`pfss.solve`, `field.trace_lines`). The inline
companion `nspf-fem` is already classified as `inline_code_literal`
(see [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.1) because all of its
occurrences sit inside the same backtick spans.

**Candidate disposition: B (demote-to-backticks-or-plain-prose) for
the one prose occurrence (line 159 in the ai-farside skill); K
(keep-as-external-reference) effectively for the eight inline-code
occurrences (already excluded from edges per
[`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §2, so they do not appear in
the audit's resolved-edge totals).** The graph's unresolved count
would drop by one target (occurrence count drops by one) if the
single prose `[[pfss-tracing]]` on line 159 of
`ai-farside-synchronic-coronal-field-extrapolation/SKILL.md`
becomes `` `pfss-tracing` ``. The eight inline-code occurrences are
not edges today and need no edit. The closing motion is one
single-line edit. The deferred N (external-namespace promotion)
option is preserved should a future PR want to graph LingTai adapters
as first-class nodes.

---

### 5.2 `wikilinks` — 3 occurrences (2 prose, 1 inline-code)

- `wave500_turbulence_intermit_heating_045/paper-andres-2021-incompressible-cascade-anisotropic-pp/SKILL.md:37` *(prose)*
  > `cross-skill [[wikilinks]]. The fifth author (S. Galtier) was missing from`
- `wave500_turbulence_intermit_heating_045/paper-andres-2021-incompressible-cascade-anisotropic-pp/SKILL.md:146` *(inline-code)*
  > ``> A&A in 2022. Slug name is preserved to keep cross-skill `[[wikilinks]]```
- `wave500_turbulence_intermit_heating_045/paper-mcintyre-2024-helicity-barrier-transition-range/SKILL.md:38` *(prose)*
  > `cross-skill [[wikilinks]] stable. ADS bibcode is not asserted (ADS UI`

**Shape:** meta-reference (neither runtime nor paper). All three
occurrences are documentary prose in `identity_uncertainty:` or
`provenance:` sections explaining that the slug shape is preserved
*so that cross-skill wikilinks remain stable*. The wikilink form here
is rhetorical — the author is naming the wikilink-system itself, not
pointing at a corpus node.

**Candidate disposition: B (demote-to-backticks-or-plain-prose).**
Drop the `[[...]]` brackets in the two prose occurrences so the
sentences read "cross-skill wikilinks" (plain noun) rather than
"cross-skill [[wikilinks]]" (a wikilink that pretends to point at a
node called `wikilinks`). The single inline-code occurrence (line
146) is already excluded from edges and needs no edit. The closing
motion is two single-line edits across two SKILL.md files.

---

### 5.3 `raouafi-2023-psp-four-years-discoveries-review` — 2 occurrences (1 prose, 1 inline-code)

- `batch_mission_instruments_data_products/fox-2016-psp-mission-design-orbit-encounters/SKILL.md:55` *(prose)*
  > `[[raouafi-2023-psp-four-years-discoveries-review]]).`
- `batch_mission_instruments_data_products/fox-2016-psp-mission-design-orbit-encounters/SKILL.md:195` *(inline-code)*
  > ``- `[[raouafi-2023-psp-four-years-discoveries-review]]` — on-orbit``

**Shape:** paper-shaped. The wikilink names a Raouafi 2023 PSP
four-years discoveries review. The audit did not classify this as
`paper_reference_needs_curation` because the slug lacks the `paper-`
prefix the audit's prefix-stripping heuristic looks for.

**Partial-match probe** — manifest slugs containing both `raouafi`
and `2023`:
`raouafi-2023-psp-four-years-discoveries-solar-minimum`.

**Candidate disposition: R (rename-to-existing-canonical-slug) —
curator should confirm.** The manifest slug names the same first
author (Raouafi), the same year (2023), the same paper genre
("psp-four-years-discoveries"), with only the topic-tail differing
(`…-review` vs `…-solar-minimum`). The citing prose (PSP mission
design with on-orbit deviations cited via a later review paper)
is consistent with the Raouafi 2023 solar-minimum discoveries
review. A curator should confirm the two slugs refer to the same
paper before substituting. If they do not refer to the same paper,
the fallback is I (route through discovery) or D (drop the brackets;
this would be a `D` per the sister report's vocabulary).

---

### 5.4 `bowen-2024-cyclotron-resonance` — 1 occurrence (prose)

- `batch_psp_switchbacks_magnetic/verniero-2020-proton-beams-ion-scale-waves/SKILL.md:174` *(prose)*
  > `- [[bowen-2024-cyclotron-resonance]] *(turbulence-heating batch)* —`

**Shape:** paper-shaped (author-year-topic).

**Partial-match probe** — manifest slugs containing both `bowen` and
`2024` (three matches): `bowen-2024-extended-cyclotron-resonant-heating`,
`bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance`,
`bowen-2024-cyclotron-heating-rates-ion-scale-waves`.

**Candidate disposition: R — needs curator disambiguation.** Three
Bowen 2024 cyclotron-resonance manifest entries are plausible
matches. The citing prose ("cyclotron-band wave dissipation
downstream") favours
`bowen-2024-mediation-collisionless-dissipation-cyclotron-resonance`
on topic, but
`bowen-2024-extended-cyclotron-resonant-heating` and
`bowen-2024-cyclotron-heating-rates-ion-scale-waves` are also viable
on a strict author-year match. The fallback D (drop the brackets) is
always safe.

---

### 5.5 `hall-mhd-residual-classifier` — 1 occurrence (prose)

- `pilot_2026_and_runtime/mozer-2026-switchback-nonideal-dissipation/SKILL.md:138` *(prose)*
  > `- [[hall-mhd-residual-classifier]] — TODO create`

**Shape:** runtime / tool. The companion suffix "— TODO create" is a
deliberate marker that this is a forward reference to an
un-implemented LingTai classifier, not a paper.

**Candidate disposition: B (demote-to-backticks-or-plain-prose).**
The "TODO create" suffix already does the work the `[[...]]` form
suggests (mark as future adapter). Drop the brackets so the line
reads `` `hall-mhd-residual-classifier` — TODO create``. Closing
motion: one single-line edit.

---

### 5.6 `messenger-mag-loader` — 1 occurrence (prose)

- `pilot_2026_and_runtime/li-2026-mercury-orbit-solar-wind-turbulence/SKILL.md:127` *(prose)*
  > `- [[messenger-mag-loader]] — TODO create`

**Shape:** runtime / loader (MESSENGER MAG data loader). Same
"TODO create" pattern as 5.5.

**Candidate disposition: B.** Single-line edit; rationale identical
to 5.5.

---

### 5.7 `messenger-solar-wind-filter` — 1 occurrence (prose)

- `pilot_2026_and_runtime/li-2026-mercury-orbit-solar-wind-turbulence/SKILL.md:128` *(prose)*
  > `- [[messenger-solar-wind-filter]] — TODO create`

**Shape:** runtime / filter (MESSENGER solar-wind classifier).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.8 `parker-spiral-propagator` — 1 occurrence (prose)

- `pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/SKILL.md:141` *(prose)*
  > `- [[parker-spiral-propagator]] — TODO create`

**Shape:** runtime / propagator (Parker-spiral magnetic-field-line
mapping tool).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.9 `parker-transport-sde-solver` — 1 occurrence (prose)

- `pilot_2026_and_runtime/murtas-2026-hcs-reconnection-ion-energization/SKILL.md:161` *(prose)*
  > `- [[parker-transport-sde-solver]] — TODO create`

**Shape:** runtime / SDE solver (Parker transport equation
stochastic-differential-equation integrator).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.10 `pfss-footpoint-mapper` — 1 occurrence (prose)

- `pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/SKILL.md:140` *(prose)*
  > `- [[pfss-footpoint-mapper]] — TODO create`

**Shape:** runtime / mapper (PFSS footpoint resolver). Sibling of
the already-existing LingTai `pfss-tracing` adapter (5.1).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.11 `psp-fields-efield-loader` — 1 occurrence (prose)

- `pilot_2026_and_runtime/mozer-2026-switchback-nonideal-dissipation/SKILL.md:136` *(prose)*
  > `- [[psp-fields-efield-loader]] — TODO create`

**Shape:** runtime / loader (PSP FIELDS electric-field data loader).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.12 `psp-fields-mag-hcs-identifier` — 1 occurrence (prose)

- `pilot_2026_and_runtime/murtas-2026-hcs-reconnection-ion-energization/SKILL.md:160` *(prose)*
  > `- [[psp-fields-mag-hcs-identifier]] — TODO create`

**Shape:** runtime / classifier (PSP FIELDS heliospheric-current-sheet
identifier).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.13 `psp-isois-epi-data-loader` — 1 occurrence (prose)

- `pilot_2026_and_runtime/murtas-2026-hcs-reconnection-ion-energization/SKILL.md:159` *(prose)*
  > `- [[psp-isois-epi-data-loader]] — TODO create`

**Shape:** runtime / loader (PSP ISʘIS EPI energetic-particle data
loader).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.14 `psp-sweap-bulk-loader` — 1 occurrence (prose)

- `pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/SKILL.md:138` *(prose)*
  > `- [[psp-sweap-bulk-loader]] — TODO create`

**Shape:** runtime / loader (PSP SWEAP bulk-plasma-moments loader).
Explicitly named in [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.4 as a
canonical example of an external runtime / loader name.

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.15 `psp-walen-test-classifier` — 1 occurrence (prose)

- `pilot_2026_and_runtime/tenerani-2026-spherically-polarized-magnetic-fields/SKILL.md:132` *(prose)*
  > `- [[psp-walen-test-classifier]] — TODO create`

**Shape:** runtime / classifier (PSP Walén-test Alfvénic-interval
classifier).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.16 `rotational-discontinuity-finder-mhd` — 1 occurrence (prose)

- `pilot_2026_and_runtime/tenerani-2026-spherically-polarized-magnetic-fields/SKILL.md:133` *(prose)*
  > `- [[rotational-discontinuity-finder-mhd]] — TODO create`

**Shape:** runtime / finder (rotational-discontinuity detector for
MHD-scale time series).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.17 `shankarappa-2025-free-energy-sources-ion-scale-waves` — 1 occurrence (prose)

- `batch_psp_switchbacks_magnetic/verniero-2020-proton-beams-ion-scale-waves/SKILL.md:140` *(prose)*
  > `- **Composability** with [[shankarappa-2025-free-energy-sources-ion-scale-waves]]`

**Shape:** paper-shaped.

**Partial-match probe** — manifest slugs containing `shankarappa`:
`shankarappa-2025-free-energy-sources-ion-scale-waves-psp`,
`paper-shankarappa-2025-ion-scale-waves-free-energy-survey`.

**Candidate disposition: R (rename-to-existing-canonical-slug),
high confidence.** The manifest slug
`shankarappa-2025-free-energy-sources-ion-scale-waves-psp` differs
from the wikilink in exactly one trailing token (`…-psp`). Same first
author, same year, same topic ("free-energy sources ion-scale
waves"). The companion manifest entry
`paper-shankarappa-2025-ion-scale-waves-free-energy-survey`
re-orders the same tokens and is a viable secondary R candidate; a
curator should pick the one the citing prose intends. The fallback D
(drop the brackets) is always safe.

---

### 5.18 `so-swa-bulk-loader` — 1 occurrence (prose)

- `pilot_2026_and_runtime/dakeyo-2026-source-alignment-psp-solo/SKILL.md:139` *(prose)*
  > `- [[so-swa-bulk-loader]] — TODO create`

**Shape:** runtime / loader (Solar Orbiter SWA bulk-plasma-moments
loader).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.19 `stverak-2026-solo-swa-eas-spacecraft-electron-contamination` — 1 occurrence (prose)

- `batch_mission_instruments_data_products/owen-2020-solo-swa-plasma-suite/SKILL.md:58` *(prose)*
  > `[[stverak-2026-solo-swa-eas-spacecraft-electron-contamination]] — TODO`

**Shape:** paper-shaped (author-year-topic) with explicit "TODO add
to corpus when needed" annotation (continued on the next line, see
SKILL.md:58–59).

**Partial-match probe** — manifest slugs containing `stverak`: none.

**Candidate disposition: I (internalise-via-discovery-pipeline) — or
D.** The citing prose explicitly flags the target as "TODO add to
corpus when needed" — i.e. the citing author expected this paper to
be internalised separately. With no `stverak` slug in the manifest,
the closing motion is either to route the author / year / topic
through the
[`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md) candidate-lifecycle
pipeline (if the Štverák 2026 SO/SWA/EAS contamination paper exists
and is in scope) or to demote the reference to plain prose (D in the
sister report's vocabulary). Note: the citing context (SO/SWA-EAS
spacecraft-emitted-electron contamination characterisation) is
adjacent to but distinct from the
`batch_mission_instruments_data_products/owen-2020-solo-swa-plasma-suite`
SWA instrument paper that already exists in the manifest.

---

### 5.20 `switchback-boundary-finder` — 1 occurrence (prose)

- `pilot_2026_and_runtime/mozer-2026-switchback-nonideal-dissipation/SKILL.md:137` *(prose)*
  > `- [[switchback-boundary-finder]] — TODO create`

**Shape:** runtime / finder (switchback boundary detector).
Explicitly named in [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.4 as a
canonical example of an external runtime / tool name.

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.21 `synthetic-switchback-generator` — 1 occurrence (prose)

- `pilot_2026_and_runtime/tenerani-2026-spherically-polarized-magnetic-fields/SKILL.md:131` *(prose)*
  > `- [[synthetic-switchback-generator]] — TODO create`

**Shape:** runtime / generator (synthetic-switchback signal
generator for forward-modelling tests).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.22 `trace-psd-broken-power-law-fitter` — 1 occurrence (prose)

- `pilot_2026_and_runtime/li-2026-mercury-orbit-solar-wind-turbulence/SKILL.md:129` *(prose)*
  > `- [[trace-psd-broken-power-law-fitter]] — TODO create`

**Shape:** runtime / fitter (broken-power-law fitter for trace power
spectra).

**Candidate disposition: B.** Rationale identical to 5.5.

---

### 5.23 `verniero-2023-proton-alpha-instabilities-ion-cyclotron` — 1 occurrence (prose)

- `batch_psp_switchbacks_magnetic/verniero-2020-proton-beams-ion-scale-waves/SKILL.md:169` *(prose)*
  > `- [[verniero-2023-proton-alpha-instabilities-ion-cyclotron]] *(future`

**Shape:** paper-shaped.

**Partial-match probe** — manifest slugs containing `verniero`:
`verniero-2020-psp-span-i-vdf-data-product`,
`verniero-2020-proton-beams-ion-scale-waves` (this is the citing
skill itself),
`verniero-2023-proton-alpha-instabilities-ion-cyclotron-wave-event`.

**Candidate disposition: R (rename-to-existing-canonical-slug),
high confidence.** The manifest slug
`verniero-2023-proton-alpha-instabilities-ion-cyclotron-wave-event`
differs from the wikilink in exactly one trailing token
(`…-wave-event`). Same first author, same year, same topic
(proton-alpha-instabilities ion-cyclotron). The citing prose treats
it as a "future / sibling" pointer, which is consistent with
referencing the canonical manifest entry. The fallback D (drop the
brackets) is always safe.

## 6. Aggregate disposition tally

Rows summarised by the candidate disposition recorded in §5:

| Disposition | Count | Entries |
|---|---:|---|
| **B** — demote-to-backticks-or-plain-prose | 17 | 5.2 wikilinks, 5.5 hall-mhd-residual-classifier, 5.6 messenger-mag-loader, 5.7 messenger-solar-wind-filter, 5.8 parker-spiral-propagator, 5.9 parker-transport-sde-solver, 5.10 pfss-footpoint-mapper, 5.11 psp-fields-efield-loader, 5.12 psp-fields-mag-hcs-identifier, 5.13 psp-isois-epi-data-loader, 5.14 psp-sweap-bulk-loader, 5.15 psp-walen-test-classifier, 5.16 rotational-discontinuity-finder-mhd, 5.18 so-swa-bulk-loader, 5.20 switchback-boundary-finder, 5.21 synthetic-switchback-generator, 5.22 trace-psd-broken-power-law-fitter |
| **B (1 prose occurrence) + K (8 inline-code occurrences already excluded)** | 1 | 5.1 pfss-tracing |
| **R** — rename-to-existing-canonical-slug | 4 | 5.3 raouafi-2023-…-review, 5.4 bowen-2024-cyclotron-resonance (needs curator disambiguation across 3 candidates), 5.17 shankarappa-2025-…-ion-scale-waves, 5.23 verniero-2023-…-ion-cyclotron |
| **I** — internalise-via-discovery-pipeline | 1 | 5.19 stverak-2026-solo-swa-eas-spacecraft-electron-contamination |
| **N** — promote-to-future-external-namespace *(deferred, not adopted in this report)* | 0 | — |

(The B count above is 17 if 5.1 is counted by its one prose
occurrence rather than separated out; the row split is preserved
because the 8 inline-code occurrences of `pfss-tracing` are already
not edges per [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §2 and only one
edit closes the unresolved-reference row.)

These tallies are diagnostic, not normative. A curator may choose D
(drop the brackets, sister report's vocabulary) for any R or I row;
B is itself the "drop brackets" motion for the runtime / tool shape
and is always available as the conservative motion.

## 7. What this report deliberately does NOT do

* **Does NOT edit any SKILL.md.** Graph and audit counts are unchanged
  by this PR.
* **Does NOT add slugs to the manifest** or invent paper identities.
* **Does NOT verify DOIs / arXiv IDs / full-text claims.** A
  candidate disposition of `R` is a *slug-shape* claim, not a
  bibliographic identity claim.
* **Does NOT define a new external-node namespace** for runtime /
  tool / loader names. The deferred `N` option is recorded only as a
  possible future direction; this report does not recommend adopting
  it in this increment.
* **Does NOT auto-demote any `[[...]]` token.** Every B row is one
  small edit a curator (or a tightly scoped follow-up PR) makes
  deliberately.
* **Is NOT wired into `scripts/validate.sh`.** The report is a
  one-shot human-readable artifact. The audit at S6 and the graph
  build at S7 remain the live, scripted views.

## 8. Recommended next motions (separate PRs)

1. For each `B` row: a single small PR (or a single bundled PR
   across the 14 `pilot_2026_and_runtime/*` "TODO create" targets since
   they all live in the same handful of files) that drops the
   `[[...]]` brackets in the citing SKILL.md and re-runs
   `scripts/audit_wikilinks.py --json`. The unresolved-target count
   should drop by one per closed row.
2. For each `R` row: a single small PR per row that edits the citing
   SKILL.md to use the canonical manifest slug, after a curator
   confirms the citing prose really means that paper. For 5.4
   (`bowen-2024-cyclotron-resonance`) the curator must disambiguate
   across three plausible Bowen 2024 manifest entries before
   editing.
3. For the `I` row (5.19 Štverák 2026): route author / year / topic
   through the
   [`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md) candidate-lifecycle
   pipeline (`scripts/discover_heliophysics_literature.py` →
   `scripts/draft_paper_skill_from_candidates.py`). Do not skip the
   discovery pipeline by hand-drafting a slug.
4. A future PR may revisit `N` (external-node namespace). If
   adopted, it should land as a deliberate schema-bump on
   `corpus_skill_graph.json` with its own provenance, not as a
   silent retag of the existing `external_reference_candidates[]`
   list.
