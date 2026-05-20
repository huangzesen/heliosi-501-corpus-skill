# Curation triage — `paper_reference_needs_curation` (10 entries)

**Status:** informational; report-only. Does NOT modify any per-entry
`SKILL.md`, does NOT touch the manifest, does NOT change graph counts
or audit counts.
**Scope:** the 10 unresolved wikilink targets carrying the
`paper_reference_needs_curation` classification in
[`references/corpus_skill_graph.json`](../references/corpus_skill_graph.json)
at commit `db895b1`.
**Policy basis:** [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.3 (what the
classification means) and §5 (recommended curation workflow).

---

## 1. Why this report exists

[`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §5 spells out a three-option
disposition vocabulary for any unresolved wikilink that a curator
inspects:

> 3. If it is a `paper-`-prefixed reference to a paper that does not
>    exist in the corpus, decide between
>    (a) internalising the paper,
>    (b) rewording the prose so it no longer claims a wikilink edge,
>    or (c) demoting the reference to a plain citation with no
>    `[[...]]` token.

The graph artifact itself surfaces the unresolved targets honestly
under `unresolved_references[]` and tags each with a conservative
classification label. What it deliberately does NOT do (per
[`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §4) is recommend a disposition,
because that is a content decision, not a mechanical one.

This report fills exactly that gap for one classification bucket
(`paper_reference_needs_curation`) and one snapshot of the corpus
(`db895b1`). For each of the 10 entries it records:

1. The unresolved wikilink target (verbatim from the audit).
2. Every referrer (`path:line`) plus the quoted prose line.
3. A *partial-match* probe against the manifest by `(first_author,
   year)` token overlap — strictly mechanical, no full-text
   verification.
4. A **candidate disposition** drawn from the three-option vocabulary
   above, with one-sentence justification.

The candidate disposition is a hint for a curator review, not a
verdict. No SKILL.md was edited; no slug was invented; no DOI was
claimed. Closing each entry remains a separate, deliberate PR.

## 2. Disposition vocabulary (used in §4)

| Code | GRAPH_POLICY §5 mapping | Meaning |
|---|---|---|
| **R — rename-to-existing-canonical-slug** | §5 step 2 ("slug typo that maps onto an existing manifest entry") | A manifest slug matches the wikilink under `(first_author, year)` tokens, with the *topic tail differing only in surface form*. Closing motion: edit the citing SKILL.md to use the canonical slug. Needs a one-line author check that the citing prose really means the canonical paper. |
| **I — internalise-via-discovery-pipeline** | §5 step 3(a) | The wikilink looks like a real off-corpus paper (the citing prose treats it as a known reference). Closing motion: feed the author/year/topic into [`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md)'s candidate-lifecycle pipeline; if the paper is real and in scope, draft a paper-skill via `scripts/draft_paper_skill_from_candidates.py`. |
| **D — demote-to-plain-prose** | §5 step 3(b) / 3(c) | The wikilink is rhetorical (placeholder pairing, "not in this batch, add later", stylized example). Closing motion: drop the `[[...]]` brackets in the citing SKILL.md so the graph no longer carries it as a prose wikilink. |
| **?** | n/a | Evidence currently insufficient to choose between R/I/D without curator input. The row records what is known. |

**Important:** none of R / I / D claim the underlying paper is
verified. R only claims a *candidate* slug match; I and D both leave
verification to follow-up motions.

## 3. Snapshot reconciliation

This report is consistent with the graph artifact at commit `db895b1`:

| Metric | Value |
|---|---:|
| Corpus nodes | 501 |
| Resolved edges | 688 |
| Inline-code / fenced-code wikilink occurrences excluded from edges | 518 |
| Unresolved wikilink targets (all classifications) | 56 |
| ↳ `paper_reference_needs_curation` (this report) | **10** |
| ↳ `external_reference_candidate` | 23 |
| ↳ `inline_code_canonical_suggestion` | 17 |
| ↳ `inline_code_literal` | 6 |
| Entries with explicit `## Skill graph → depends_on` section | 105 |

The 10 rows below sum to **15 prose occurrences across 9 referring
SKILL.md files** (a single referring file can carry multiple unresolved
targets).

## 4. The 10 entries

### 4.1 `paper-sioulas-2023-anisotropic-scaling` — 4 prose occurrences

- `wave500_agent_runtime_eval_design_045/paper-liweiwu-2026-ai-co-scientist-ranking-search-models/SKILL.md:78`
  > `statement: "Pilot multi-LLM consensus on one HelioSI challenge — e.g. interpreting a discrepancy between [[paper-sioulas-2023-anisotropic-scaling]] and [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] — and measure agreement…"`
- `wave500_agent_runtime_eval_design_045/paper-liweiwu-2026-ai-co-scientist-ranking-search-models/SKILL.md:219`
  > `- **Minimal_experiment** - Pilot multi-LLM consensus on one HelioSI challenge — e.g. interpreting a discrepancy between [[paper-sioulas-2023-anisotropic-scaling]] and [[chen-2022-magnetic-field-spectral-evolution-inner-heliosphere]] — and m…`
- `wave500_agent_runtime_eval_design_045/paper-lu-2024-ai-scientist-fully-automated-discovery/SKILL.md:81`
  > `statement: "Apply the v1 idea-generation prompt loop to a single heliophysics paper-skill (e.g. [[paper-sioulas-2023-anisotropic-scaling]]) and measure how many of the generated follow-up ideas survive a sibling paper-skill consistency check…"`
- `wave500_agent_runtime_eval_design_045/paper-lu-2024-ai-scientist-fully-automated-discovery/SKILL.md:230`
  > `- **Minimal_experiment** - Apply the v1 idea-generation prompt loop to a single heliophysics paper-skill (e.g. [[paper-sioulas-2023-anisotropic-scaling]]) and measure how many of the generated follow-up ideas survive a sibling paper-skill c…`

**Partial-match probe** — manifest slugs containing both `sioulas` and `2023`:
`sioulas-2023-anisotropic-scaling-inner-heliosphere`.

**Candidate disposition: R (rename-to-existing-canonical-slug).** The
manifest entry `sioulas-2023-anisotropic-scaling-inner-heliosphere`
has the same first author, the same year, and a topic tail that is a
strict superset of the unresolved wikilink. Both citing prose passages
use the target as a stylized "pick any HelioSI challenge" example, so
they would also be defensible as D (demote-to-plain-prose); the R
candidate is preferred only because the manifest entry exists and the
topic is identical. Curator should confirm before editing.

---

### 4.2 `paper-cao-2026-sep-rise-time-earth-mars` — 1 prose occurrence

- `batch_sep_energetic_particles/paper-laitinen-2026-vda-turbulent-heliosphere/SKILL.md:309`
  > `A natural pairing with [[paper-cao-2026-sep-rise-time-earth-mars]],`

**Partial-match probe** — manifest slugs containing both `cao` and `2026`:
`paper-cao-2026-sep-rise-times-earth-mars-transport`.

**Candidate disposition: R (rename-to-existing-canonical-slug).** The
manifest slug differs from the wikilink only in pluralisation (`time`
→ `times`) and topic suffix (`…earth-mars` → `…earth-mars-transport`).
Same first author, same year, same SEP rise-time topic. Curator should
confirm the citing paper means this Cao 2026 SEP paper and not a
distinct Cao 2026 paper.

---

### 4.3 `paper-stevens-2022-mhd-theory-psp-reconcile` — 1 prose occurrence

- `wave500_turbulence_intermit_heating_045/paper-magyar-2024-plasma-frame-synthetic-modeling/SKILL.md:164`
  > `- [[paper-stevens-2022-mhd-theory-psp-reconcile]] — sibling/upstream context for the same physics domain.`

**Partial-match probe** — manifest slugs containing both `stevens` and `2022`:
`stevens-2022-reconciling-psp-mhd-theory-plasma-frame`.

**Candidate disposition: R (rename-to-existing-canonical-slug).** The
manifest slug reorders the same content tokens (`mhd-theory-psp` ↔
`psp-mhd-theory`, `reconcile` ↔ `reconciling-…-plasma-frame`). Same
author, same year, same topic. The depends-on context ("sibling/upstream
context for the same physics domain") is consistent with the manifest
entry's plasma-frame focus.

---

### 4.4 `paper-duan-2026-...` — 1 prose occurrence

- `batch_sep_energetic_particles/paper-jebaraj-2024-synchrotron-electrons-near-sun-shocks/SKILL.md:324`
  > `bursts ([[paper-duan-2026-...]] — not in this batch; add later)`

**Partial-match probe** — manifest slugs containing both `duan` and `2026`:
`paper-duan-2026-sep-type-ii-radio-source-regions`.

**Candidate disposition: D (demote-to-plain-prose) — or R if curator
confirms.** The wikilink target is literally an ellipsis (`paper-duan-2026-...`),
which the prose annotates as "not in this batch; add later". The
citing author intentionally left the slug unfinished. The manifest now
*does* carry a `paper-duan-2026-sep-type-ii-radio-source-regions` entry,
which the citing context (radio bursts) is consistent with — so R is
viable if a curator confirms it is the intended Duan 2026 paper. The
fallback D motion (drop the `[[...]]` brackets) is always safe.

---

### 4.5 `paper-bourouaine-2019-stochastic-heating-near-sun` — 2 prose occurrences

- `wave500_turbulence_intermit_heating_045/paper-bowen-2025-stochastic-heating-sub-alfvenic/SKILL.md:163`
  > `- [[paper-bourouaine-2019-stochastic-heating-near-sun]] — sibling/upstream context for the same physics domain.`
- `wave500_turbulence_intermit_heating_045/paper-johnston-2024-unified-ion-heating-low-beta/SKILL.md:160`
  > `- [[paper-bourouaine-2019-stochastic-heating-near-sun]] — sibling/upstream context for the same physics domain.`

**Partial-match probe** — manifest slugs containing `bourouaine`:
`paper-bourouaine-2020-switchback-nonswitchback-turbulence` (year mismatch,
topic mismatch).

**Candidate disposition: I (internalise-via-discovery-pipeline) — or D.**
The citing prose treats Bourouaine 2019 as a real, named stochastic-heating
sibling paper. The only existing Bourouaine entry is a 2020
switchback-turbulence paper — a different paper. If the 2019 paper is
real and in scope, the closing motion is the discovery pipeline; if a
curator decides not to internalise, the fallback is D (drop brackets
and keep the citation as plain prose).

---

### 4.6 `paper-klein-2017-stochastic-heating-beta-amplitude` — 2 prose occurrences

- `wave500_turbulence_intermit_heating_045/paper-bowen-2025-stochastic-heating-sub-alfvenic/SKILL.md:164`
  > `- [[paper-klein-2017-stochastic-heating-beta-amplitude]] — sibling/upstream context for the same physics domain.`
- `wave500_turbulence_intermit_heating_045/paper-johnston-2024-unified-ion-heating-low-beta/SKILL.md:161`
  > `- [[paper-klein-2017-stochastic-heating-beta-amplitude]] — sibling/upstream context for the same physics domain.`

**Partial-match probe** — manifest slugs containing `klein`:
`klein-2018-multispecies-stability-anisotropy` (year mismatch, topic mismatch).

**Candidate disposition: I (internalise-via-discovery-pipeline) — or D.**
Same shape as 4.5. The existing Klein 2018 entry is a different paper
(multispecies stability, not stochastic-heating amplitude scaling). If
the 2017 paper is real and in scope, route through the discovery
pipeline; otherwise D.

---

### 4.7 `paper-chandran-2013-stochastic-heating-alpha-proton` — 1 prose occurrence

- `wave500_turbulence_intermit_heating_045/paper-johnston-2024-unified-ion-heating-low-beta/SKILL.md:162`
  > `- [[paper-chandran-2013-stochastic-heating-alpha-proton]] — sibling/upstream context for the same physics domain.`

**Partial-match probe** — manifest slugs containing `chandran`:
`chandran-2010-stochastic-heating-perp-alfven`,
`paper-chandran-2025-intermittent-reflection-imbalanced-mhd`
(both year mismatches).

**Candidate disposition: I (internalise-via-discovery-pipeline) — or D.**
The existing Chandran 2010 stochastic-heating entry is the closest
topic neighbour, but the wikilink names a distinct 2013 alpha/proton
paper. If real and in scope, route through the discovery pipeline;
otherwise D.

---

### 4.8 `paper-landeros-2024-stride-ch-chromospheric-ensemble` — 1 prose occurrence

- `batch_solar_wind_segmentation_ml/paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation/SKILL.md:35`
  > `- The downstream product is a **chromospheric** CH delineation — use [[paper-landeros-2024-stride-ch-chromospheric-ensemble]]-style chromospheric ensemble (companion in the inventory but not in this batch).`

**Partial-match probe** — manifest slugs containing `landeros`: none.

**Candidate disposition: I (internalise-via-discovery-pipeline) — or D.**
The citing prose explicitly flags the target as "companion in the
inventory but not in this batch", which suggests the citing author
expected this paper to be internalised separately. With no `landeros`
slug in the manifest, the closing motion is either to route through
the discovery pipeline (if the STRIDE chromospheric-ensemble paper
exists and is in scope) or to demote the reference to plain prose.

---

### 4.9 `paper-pop-corn-2026-cnn-ch-detection` — 1 prose occurrence

- `batch_solar_wind_segmentation_ml/paper-grajeda-2025-acwe-magnetic-constrained-ch-segmentation/SKILL.md:37`
  > `- A **deep-learning** CH detector is required — see the POP-CORN neural-network detector ([[paper-pop-corn-2026-cnn-ch-detection]], not in this batch).`

**Partial-match probe** — manifest slugs containing `pop-corn`:
`paper-bizoulasso-2025-pop-corn-neural-ch-validation`.

**Candidate disposition: R (rename-to-existing-canonical-slug) — needs
curator check.** The manifest slug names POP-CORN under its first
author (Bizoulasso) and a 2025 validation paper rather than a 2026
detector paper. They may or may not be the same artifact. If the
citing prose is willing to accept the Bizoulasso 2025 validation entry
as a stand-in for the POP-CORN detector, R is appropriate; otherwise
the closing motion is I (internalise the 2026 detector paper) or D
(drop the brackets).

---

### 4.10 `paper-walker-2024-icme-shock-solo-ace-radial-evolution` — 1 prose occurrence

- `batch_sep_energetic_particles/paper-walker-2026-icme-radial-particle-acceleration-statistics/SKILL.md:345`
  > `[[paper-walker-2024-icme-shock-solo-ace-radial-evolution]].`

**Partial-match probe** — manifest slugs containing `walker`:
`paper-walker-2026-icme-radial-particle-acceleration-statistics`
(year mismatch — and this is the *referring* skill itself).

**Candidate disposition: I (internalise-via-discovery-pipeline) — or D.**
The only Walker manifest entry is the citing skill itself, so this is
not a self-link. The wikilink names a distinct earlier Walker paper
(2024 ICME shock radial evolution). If the 2024 paper is real and in
scope, route through the discovery pipeline; otherwise D.

## 5. Aggregate disposition tally

Rows summarised by the candidate disposition recorded in §4:

| Disposition | Count | Entries |
|---|---:|---|
| **R** — rename-to-existing-canonical-slug | 4 | 4.1 sioulas-2023, 4.2 cao-2026, 4.3 stevens-2022, 4.9 pop-corn-2026 |
| **R / D** — both viable, curator decides | 1 | 4.4 duan-2026-... |
| **I / D** — internalise or demote | 5 | 4.5 bourouaine-2019, 4.6 klein-2017, 4.7 chandran-2013, 4.8 landeros-2024, 4.10 walker-2024 |

These tallies are diagnostic, not normative. A curator may choose D
for any R row (rewording the prose so it no longer claims a wikilink
edge is always available as the conservative motion).

## 6. What this report deliberately does NOT do

* **Does NOT edit any SKILL.md.** Graph and audit counts are unchanged
  by this PR.
* **Does NOT add slugs to the manifest** or invent paper identities.
* **Does NOT verify DOIs / arXiv IDs / full-text claims.** A
  candidate disposition of `R` is a *slug-shape* claim, not a
  bibliographic identity claim.
* **Does NOT promote any `external_reference_candidate`** (the other
  23 unresolved entries). Those remain off-corpus runtime / tool
  names per [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.4 and are out
  of scope for this report.
* **Is NOT wired into `scripts/validate.sh`.** The report is a
  one-shot human-readable artifact. The audit at S6 and the graph
  build at S7 remain the live, scripted views.

## 7. Recommended next motions (separate PRs)

1. For each `R` row: a single small PR per row that edits the citing
   SKILL.md to use the canonical manifest slug, re-runs
   `scripts/audit_wikilinks.py --json`, and reports the new totals.
   Each PR is narrowly reviewable — author check, slug substitution,
   counts delta.
2. For each `I` row: route author + year + topic through the
   [`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md) candidate-lifecycle
   pipeline (`scripts/discover_heliophysics_literature.py` →
   `scripts/draft_paper_skill_from_candidates.py`). Do not skip the
   discovery pipeline by hand-drafting a slug.
3. For any row a curator chooses to close as `D`: a single small PR
   that drops the `[[...]]` brackets in the citing SKILL.md so the
   prose remains a plain citation. Confirm the audit's unresolved
   count drops by 1.
4. A follow-up report can extend this triage to the
   `external_reference_candidate` bucket (23 entries) using the
   policy in [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) §3.4 — runtime /
   tool / loader names that should typically be demoted to backticks
   rather than wikilinks.
