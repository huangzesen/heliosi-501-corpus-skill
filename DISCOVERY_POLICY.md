# Discovery, promotion, and evidence policy

**Status:** governance document for the open-ended literature
expansion pipeline. Operationalises the offline walk-through in
[`reports/candidate_lifecycle_demo.md`](reports/candidate_lifecycle_demo.md)
and the design notes in
[`reports/literature_discovery_pipeline.md`](reports/literature_discovery_pipeline.md).
**Scope:** everything that happens *outside* `references/corpus/` —
discovery, drafting, evidence review, and the promotion gate that
moves a draft into the curated 501-entry corpus. The curated corpus
itself remains governed by `VALIDATION.md`, `SKILL.md`, and the
`scripts/validate.sh` gauntlet.
**Companion policies:** [`GRAPH_POLICY.md`](GRAPH_POLICY.md) (machine
graph boundary), [`VALIDATION.md`](VALIDATION.md) (curated-corpus
invariants), `README.md` §*Verification status (read first)*.

The point of this document is to make the lifecycle states, the
promotion gates, and the **negative decisions** explicit so that an
agent or human reviewer cannot accidentally promote unverified
material into the curated corpus, nor accidentally drop a candidate
on the floor without leaving a recorded reason.

---

## 1. Lifecycle states

Every literature object touched by the discovery pipeline sits in
exactly one of the states below at any moment. Transitions are listed
in §2. The state is not a free-form label — it is read off the
artifacts the pipeline scripts already write.

| State | Where it lives | Identity signal | Allowed claims |
|---|---|---|---|
| **Discovered candidate** | One JSONL row in a discovery `--run-dir`'s `candidates.jsonl` (or a free-standing `--output` JSONL) | `dedupe_id` + backend (`arxiv` / `openalex` / `crossref` / `ads`) | "The upstream backend returned this record on this run." Nothing more. |
| **Joined candidate — `new_candidate`** | Same JSONL row, with `corpus_status: "new_candidate"` | `corpus_status` + `corpus_match_via: null` | "No manifest-key (DOI / arXiv / bibcode / title+year) hit against `references/corpus_manifest_v2.json` on this run." NOT "verified absent from the literature." |
| **Joined candidate — `already_curated`** | Same JSONL row, with `corpus_status: "already_curated"` | `corpus_status` + `corpus_match_via` + `corpus_match_slugs[]` | "A manifest-key hit against the curated 501 was found via the recorded key." A separate verification pass is still required before claiming the curated entry is correct. |
| **Joined candidate — `unjoined`** | Same JSONL row, with `corpus_status: "unjoined"` | `corpus_status` (novelty join was disabled or the default manifest was absent) | "Novelty status is unknown to this run." Nothing about presence or absence in the curated corpus. |
| **Quarantined draft** | A per-draft directory `<drafts-dir>/draft__…/` with `SKILL.md` + `metadata.yaml`; aggregated by `draft_manifest.json` (`schema_version: "draft-scaffold-manifest/1.0"`) | `draft__` slug prefix, the quarantine banner in `SKILL.md`, `promotion_status: unreviewed`, and `promotion_gate:` block in `metadata.yaml` with every key `false` | "A scaffold exists; the imported candidate metadata + abstract are the candidate's, not the corpus's." No Layer-1/2/3/4 claim about the underlying paper is licensed. |
| **Reviewed draft** | Same per-draft directory, with at least one `promotion_gate` key flipped to `true` and the corresponding evidence recorded in the draft's `SKILL.md` | One or more `promotion_gate.*: true` entries with prose evidence in the draft body | "The specific items recorded as `true` have been verified; everything else is still pending." A reviewed draft is **still not** a corpus entry. |
| **Verified corpus paper-skill** | `references/corpus/<batch>/<paper-slug>/{SKILL.md, metadata.yaml}` listed in `references/corpus_manifest_v2.json`; the new edges appear in `references/corpus_skill_graph.json` after a regenerate | Manifest membership + the curated-entry naming convention (`paper-<surname>-<year>-…` or batch-specific slug); the entry passes `scripts/validate.sh` and the audit gauntlet | Layer-1 claim + Layer-2 contract are authored *from evidence*; Layer-3/Layer-4 are populated to the tier the entry honestly carries (T1–T7 per `references/corpus_qa_report_v2.md`). |
| **Rejected / negative decision** | A row in the rejection log — either a per-run `<run-dir>/rejections.jsonl` written by hand or a per-draft `metadata.yaml::rejection:` block (see §4); never silently deleted | `decision: rejected` + a `reason:` from the controlled vocabulary in §4 | "This candidate (or draft) is not eligible for promotion under the recorded reason." Recording a rejection is itself an artifact, not a hand-wave. |

The pipeline scripts that materialise these states are
`scripts/discover_heliophysics_literature.py` (discovered → joined)
and `scripts/draft_paper_skill_from_candidates.py` (joined →
quarantined draft). Both refuse to write under `references/corpus/`;
the curated state is only reachable via the manual promotion gate
in §3.

## 2. Allowed transitions

```
discovered ── novelty join ──► joined
   │                            │
   │                            ├─ new_candidate ─┐
   │                            ├─ already_curated┤
   │                            └─ unjoined ──────┘
   │                            │
   │  (any joined state)        ▼
   │             ┌── drafter ──► quarantined draft
   │             │                       │
   │             │                       │  evidence review
   │             │                       │  (each promotion_gate item)
   │             │                       ▼
   │             │                reviewed draft
   │             │                       │
   │             │                       │  ALL promotion_gate items true
   │             │                       │  + four-layer authoring
   │             │                       │  + scripts/validate.sh passes
   │             │                       │  + manifest + graph rebuild
   │             │                       ▼
   │             │            verified corpus paper-skill
   │             │
   └─────────────┴── at any stage, with recorded reason ──► rejected
```

Rules:

1. **No skipping the drafter.** A candidate cannot become a verified
   corpus paper-skill without first being a quarantined draft. The
   drafter is the only path that materialises the
   `promotion_gate:` block, and the gate is the audit trail.
2. **`already_curated` does not auto-promote.** A candidate whose
   novelty join returns `already_curated` means *"a manifest key
   matched"*, not *"the curated entry is verified against this
   paper"*. Treat it as a pointer into the existing
   verification debt (T3 / T4 / `TODO_verify_with_full_text`), not
   as evidence that the curated entry needs no further review.
3. **`unjoined` is not promotion-eligible by default.** The drafter
   refuses to scaffold `unjoined` rows unless `--include-unjoined` is
   passed; even then, the draft still has to clear the full
   promotion gate. `--include-all-statuses` (drafting
   `already_curated` rows) is reserved for *audit* purposes — it
   does not loosen any other rule.
4. **Rejections are an artifact, not a deletion.** A candidate or
   draft taken out of consideration must be recorded under §4. The
   pipeline does not currently delete candidate JSONL rows from
   prior runs; auditors should be able to reconstruct *why* a
   candidate stopped propagating, not just *that* it did.
5. **Reverse transitions are allowed.** A verified corpus
   paper-skill that is later found to have been promoted on
   insufficient evidence can be demoted (see §3.7); a rejected
   candidate that becomes promotable later (new evidence, restored
   access) can be re-drafted under §4.3. Both motions are recorded
   the same way as a forward transition.

## 3. Promotion gates

A draft is **only** eligible for promotion into
`references/corpus/<batch>/<paper-slug>/` once every gate item below
has been completed and the corresponding key in the draft's
`metadata.yaml::promotion_gate` has been flipped to `true`. Each gate
item is a contract; the bracketed phrase is how the reviewer should
record the evidence inside the draft's `SKILL.md` so the audit trail
survives the move.

### 3.1 Bibliographic identity

* `bibliographic_identity_verified` — DOI resolves at the publisher
  of record; arXiv ID matches the same paper; ADS bibcode (when
  available) matches; the round-tripped title is consistent across
  all three. A `provenance.id_verifications[]` block consistent with
  `scripts/verify_arxiv_ids.py` (status `arxiv-http-title-match`) is
  the canonical evidence for the arXiv side.
* `provenance_checked` — record the publisher landing-page URL, the
  arXiv abs page, and the ADS record (when available) in the draft's
  prose, not just in the metadata.
* `title_authors_year_conflicts_resolved` — when the discovery
  backend's title / authors / year disagree with the publisher of
  record, pick the publisher value and document the disagreement in
  prose. A draft with unresolved upstream conflicts must not be
  promoted.

### 3.2 Full-text / evidence review

* `abstract_or_full_text_inspected` — the *full text* of the paper
  has been read well enough to author Layer-1 + Layer-2 from
  evidence. The abstract alone is **not** sufficient to clear this
  item except for a deliberately narrow class of entries (see §3.6);
  even then, the reviewer must record *why* abstract-only was
  acceptable.
* No claim in the draft body may exceed what the paper itself
  claims. Paraphrasing into a stronger or more general statement
  than the source is treated the same as fabricating it.

### 3.3 Layer 1–4 authoring

* `claims_evidence_extracted` — the Layer-1 invariant is recorded
  with the paper's own claim / evidence boundary. If the paper does
  not actually carry the invariant the draft attributes to it, the
  draft does not clear this gate.
* `data_tool_contracts_defined` — Layer-2 data / tool contracts
  (instrument, cadence, level, archive; algorithm inputs / outputs)
  are written down explicitly. A Layer-2 stub at promotion time is
  a §3.5 maturity-tier decision, not a §3.3 pass.
* `failure_modes_recorded` — known failure modes and load-bearing
  assumptions are recorded. "No known failure modes" is a claim
  about the paper, and is only acceptable when it is what the paper
  itself says.

### 3.4 Data / tool contract & adapter boundary

* `data_tool_contracts_defined` (continued from §3.3) covers the
  Layer-2 surface.
* **Adapter / MCP boundary** — decide whether a Layer-3 example
  adapter is in scope. If a real Layer-3 binding would depend on
  `xhelio-spice`, `xhelio-cdaweb`, or another MCP, record the
  dependency rather than inventing a fallback. This is the same
  rule the README enforces at §*Companion MCP adapters*: citing
  `xhelio-spice` / `xhelio-cdaweb` is not a verification claim, and
  the curated corpus does not bundle the MCPs. A draft whose
  Layer-3 binding cannot be honestly recorded should ship without a
  Layer-3 example rather than carry a fabricated one.

### 3.5 Validation target & maturity tier

* `validation_target_recorded` — a concrete numeric or figure-level
  target (the Layer-4 affordance hook) is recorded. The target may
  be qualitative (e.g. "Fig. 4(b) shape recovered to ±10%") but
  must be checkable against the source.
* `maturity_tier_assigned` — pick a tier (T1–T7) consistent with
  `references/corpus_qa_report_v2.md` and the rules in `README.md`
  §*Maturity tiers — exact distribution*. If the draft cannot
  honestly clear T3 (`paper-grounded-pending-full-text`), it is
  promoted as T4 (`stub` / `scaffold`), or it is not promoted —
  **do not round up** to clear the checklist. Only the
  `wu-2026-nonspherical-coronal-magnetic-field-open-flux` precedent
  has a documented local numerical reproduction (T1) in the
  curated bundle today; a new T1 claim requires the reproduction
  artifact, not just an authoring intent.

### 3.6 When abstract-only is acceptable

`abstract_or_full_text_inspected` permits a narrow abstract-only
path only when **all** of the following hold and are recorded as
prose in the draft:

* the paper is paywalled or otherwise inaccessible from the
  reviewer's environment and no preprint mirror is available;
* the abstract carries enough text to author a Layer-1 invariant
  the abstract itself states (no extrapolation);
* the maturity tier is set to T4 (`stub` / `scaffold`) — abstract-
  only entries are never promoted above T4;
* `authors_verified` and the arXiv `provenance.id_verifications[]`
  block still apply unconditionally.

A draft that fails any of those gates is **rejected** under
`inaccessible_text` (see §4), not promoted at a lower tier.

### 3.7 Bundle gauntlet & manifest update

Once §3.1–§3.6 are clear:

1. Move the per-draft directory out of the drafts area into the
   appropriate `references/corpus/<batch>/` folder; rename it to
   drop the `draft__` prefix and use the corpus's
   `paper-<surname>-<year>-…` slug convention.
2. Update `references/corpus_manifest_v2.json` so the new slug
   appears in `entries[]` with the curated fields populated; keep
   `totals.skills_in_manifests` and `totals.batches` consistent.
3. Re-run `python3 scripts/build_corpus_skill_graph.py
   --no-timestamp` so `references/corpus_skill_graph.json` carries
   the new node + any edges. `GRAPH_POLICY.md` §6 governs the
   schema-stability rules for that artifact.
4. Run the bundle gauntlet and treat each as a hard gate:
   * `python3 -m unittest discover -s tests` passes;
   * `bash scripts/validate.sh` passes (the 501-invariant in
     `validate.sh` S1 will need its target bumped to 502, 503, …
     as part of the promotion PR — that bump is itself part of
     the audit trail and must be reviewed);
   * the audit gauntlet (`scripts/audit_layer_schemas.py`,
     `scripts/audit_layer_population.py`,
     `scripts/audit_layer2_stubs.py`,
     `scripts/audit_numeric_claims.py`,
     `scripts/audit_internalization_readiness.py`,
     `scripts/audit_authorship_prose.py`,
     `scripts/audit_wikilinks.py`) continues to pass for the new
     entry.
5. Commit. The promotion is now visible to
   `scripts/search_corpus.py` and to the aggregator skill.

If any of the above breaks, the promotion is a failed promotion:
revert the move and treat the draft as still-quarantined. A draft
sitting unpromoted is not a failure; a draft promoted on insufficient
evidence is, and demoting it (moving the entry back to the drafts
area, removing it from the manifest, regenerating the graph) is the
recorded fix.

## 4. Rejection & negative-decision handling

Every candidate or draft that is taken out of consideration must
leave a recorded artifact behind. Silent drops are not allowed —
they prevent an auditor from reconstructing the pipeline's actual
selectivity, and they let a future re-run "rediscover" a candidate
that was previously rejected for a load-bearing reason.

### 4.1 Where the rejection lives

* **Candidate-stage rejection** (before any draft was scaffolded):
  append one row per rejected candidate to `<run-dir>/rejections.jsonl`
  (sibling of `candidates.jsonl`). The row must carry the candidate's
  `dedupe_id`, the `corpus_status` it carried at the time, the
  rejection `reason` from §4.2, a short prose `note`, and an ISO-8601
  `decided_at`. The rejection log is hand-written today; future
  tooling may automate it, but the schema is the contract.
* **Draft-stage rejection** (a quarantined or reviewed draft is taken
  out of consideration): add a `rejection:` block to the draft's
  `metadata.yaml` with the same fields, and append a
  `## Rejection` section to the draft's `SKILL.md` with the prose
  evidence. The draft directory **stays in place** so the audit trail
  is recoverable; the `promotion_status` field flips from
  `unreviewed` (or `under_review`) to `rejected`.

The pipeline does not currently delete prior-run candidate rows; the
rejection record is the canonical "this is not coming back without
new evidence" signal.

### 4.2 Controlled vocabulary

A rejection `reason` MUST come from the list below. Adding a new
reason is a schema-level change and should be discussed in a PR that
also updates this section.

| `reason` | Meaning | Typical evidence |
|---|---|---|
| `misattribution` | The candidate's first-author / authors / year as recorded does not match the paper of record. | Diff between backend metadata and publisher / arXiv abs page. |
| `duplicate` | The candidate is the same scientific object as another candidate or curated entry under a different identifier; the dedupe key did not collide. | The matching `dedupe_id` / curated slug. |
| `out_of_scope` | The candidate is not heliophysics literature (or not the slice the corpus tracks). | One-line scope statement: e.g. "purely solar-stellar-analogue paper; no in-situ or remote-sensing instrument tie-in." |
| `unverifiable_identity` | The DOI / arXiv ID / bibcode cannot be resolved or the resolved resource does not match the candidate's recorded title. | The HTTP status, the title round-trip, or the `scripts/verify_arxiv_ids.py` status code that failed. |
| `inaccessible_text` | The paper is paywalled and no preprint or open mirror is available, and the §3.6 abstract-only path does not apply. | The access log: which URLs were checked, what they returned. |
| `unsafe_or_fabricated_claim` | The draft or candidate carries a claim that the paper does not support (paraphrased into a stronger statement; layer-population invented from the abstract; numeric target invented). | Quote from the paper vs quote from the draft, side by side. |
| `representative_or_composite` | The candidate / draft is a representative of a *class* of papers rather than a single paper of record (e.g. a synthetic "switchback boundary finder" entry that does not anchor on one publication). | The reason the corpus has no slot for a composite entry, with a pointer to the entries that *do* cover the underlying papers. |
| `superseded` | A later paper supersedes this one for the corpus's purposes, and the curated entry should anchor on the later paper. | DOI of the superseding paper. |
| `withdrawn` | The paper has been withdrawn or retracted upstream. | The retraction notice. |
| `other` | Anything that does not fit the above. Use sparingly; a recurrent `other` reason is a signal to add a new vocabulary entry. | Required free-text `note`. |

### 4.3 Re-drafting a rejected candidate

A rejection is not permanent. A candidate or draft rejected under
`inaccessible_text`, `unverifiable_identity`, or `withdrawn` can
become promotable again when the underlying state changes (open
mirror appears; arXiv ID now resolves; retraction is rescinded). The
re-draft motion is:

1. Append a new `rejections.jsonl` row (or `rejection:` block) with
   `decision: re_evaluated`, the new evidence, and the previous
   row's `decided_at` as `previous_decided_at`.
2. Re-scaffold the draft with `--overwrite` (or, for a candidate-
   stage rejection, re-run the drafter with the original input).
3. Re-enter the promotion gate at §3.1.

`misattribution`, `unsafe_or_fabricated_claim`, and
`representative_or_composite` rejections require new candidate
identity (a different paper of record) before re-drafting; clearing
those is not a state change in the same candidate.

## 5. Source coverage & honest framing

The discovery side of this pipeline is **explicitly a frontier
sample**, not an exhaustive census. The artifacts the scripts emit
already say so verbatim; this section codifies what those statements
mean operationally.

### 5.1 Dry-run / fixtures vs live backends

* **CI exclusively exercises `--dry-run` mode**, which reads the
  shipped fixture `tests/fixtures/discovery/sample_records.jsonl`.
  A green CI run is **not** evidence that any specific paper exists
  in the wild; it is evidence that the dedupe / novelty-join /
  drafter logic behaves the way the fixtures pin.
* Live mode (`--live`) is opt-in, makes real network calls against
  the configured backends, and produces outputs that depend on
  backend state. Live mode does not change the lifecycle states or
  the promotion gates; it only changes which candidates the backend
  returns.

### 5.2 Backend coverage

| Backend | Default? | Key required? | What a hit means |
|---|---|---|---|
| arXiv | yes (live mode) | no | The arXiv API returned this record on this run. Atom-XML parse. |
| OpenAlex | yes (live mode) | no | The OpenAlex API returned this record. Inverted-index abstract reconstruction. |
| Crossref | opt-in (`--enable-crossref`) | no | Public Crossref API returned the record. |
| NASA ADS | opt-in (`--enable-ads`) | yes (`ADS_API_TOKEN` / `NASA_ADS_TOKEN` / `ADS_TOKEN`) | Requested explicitly *and* a token was present. |

A live run that does not include ADS is **not** evidence of
heliophysics-literature coverage: ADS is the closest the pipeline
has to a heliophysics-aware index, and it is opt-in plus
token-gated. The discovery script aborts (exit code 2) when
`--enable-ads` is passed without a token in the environment rather
than silently downgrading — that abort is itself a coverage signal.

**Claim boundary.** The corpus does not assert exhaustive
heliophysics coverage. A claim of the form "no heliophysics paper
on topic X exists" is only defensible with: (a) a documented live
run that included ADS with a valid token, (b) a query slate that
explicitly covers the topic and is recorded in
`run_metadata.json::queries`, and (c) a recorded `corpus_status`
distribution. Without all three, the safe statement is "no
candidate matching X surfaced in this run."

### 5.3 What `new_candidate` does and does not mean

`corpus_status: "new_candidate"` is a structural statement about the
novelty join:

* **Does mean:** "On this run, the candidate's normalised
  DOI / arXiv ID / bibcode / title+year hash did not collide with
  any entry in `references/corpus_manifest_v2.json`."
* **Does NOT mean:** "verified absent from the heliophysics
  literature" — the discovery script's `run_metadata.json::limits`
  field says this in so many words.
* **Does NOT mean:** "novel research result." The candidate is
  whatever the backend returned, including reviews, errata, and
  pre-prints superseded by a published version.
* **Does NOT mean:** "absent from per-entry frontmatter." The
  novelty join reads only the v2 manifest top-level; an identifier
  that only appears inside a per-entry `metadata.yaml` provenance
  block is invisible to the join. The literature-pipeline doc
  §3.4.3 enumerates the same caveat.

A candidate that has been re-flagged as `new_candidate` across
multiple prior runs is a hint, not a verdict, that the paper may
be genuinely absent from the curated corpus. The promotion gate
(§3) is still the only path that converts that hint into a
verified entry.

## 6. Automation boundary & unsafe claims

This bundle treats *discovery and drafting* as safe to automate, and
*verified-corpus promotion and paper-skill authoring* as requiring
evidence review. The boundary is load-bearing — collapsing it would
let automated tooling silently widen the curated corpus's claim
surface.

### 6.1 What is safe to automate

* Fetching candidate records from public bibliographic backends
  under the polite-HTTP layer documented in
  `reports/literature_discovery_pipeline.md` §5.
* Deduplicating across backends with the deterministic key order
  (DOI > arXiv > bibcode > title+year SHA-1) recorded in §3.3 of
  the pipeline doc.
* Joining candidates against the v2 manifest with the same key
  order to assign `corpus_status`.
* Persisting the run as a `discovery-run-bundle/1.0` artifact under
  `--run-dir`.
* Scaffolding **quarantined drafts** (`draft-scaffold-manifest/1.0`)
  with the `promotion_gate:` block initialised to all-`false`,
  provided every quarantine surface (`draft__` prefix, banner,
  frontmatter flags, refusal to write under `references/corpus/`)
  is preserved verbatim.
* Re-running `scripts/validate.sh` and the test suite.

### 6.2 What is NOT safe to automate

* **Flipping any `promotion_gate` item to `true` without an
  evidence record.** The gate is the audit trail; a flip with no
  prose evidence in the draft body is treated as a forged audit
  entry.
* **Populating Layer 1–4 sections of a draft from the abstract
  alone** (outside the narrow §3.6 abstract-only path, which is a
  manual decision and capped at T4).
* **Moving a draft into `references/corpus/`** — the drafter
  refuses to write there for a reason, and the move is the moment
  the curated-corpus invariants take over.
* **Bumping the 501-count invariant in `scripts/validate.sh`
  without a paired promotion that earns the extra entry.** The
  count is a claim, not a knob.
* **Asserting "fully automated paper-skill authoring" anywhere in
  the bundle's documentation, README, or downstream prose.** The
  literature-pipeline doc §6 lists the non-automated steps; the
  lifecycle demo §4 lists the same. The corpus does not claim
  automated paper writing is solved.
* **Auto-resolving a §4 rejection.** Re-drafting a rejected
  candidate (§4.3) is a manual decision that records new evidence;
  it is not a job for a polling loop.

### 6.3 Unsafe claim patterns to watch for

These show up most often as accidental over-claims; each one is
treated as `unsafe_or_fabricated_claim` (§4.2) if it lands in a
draft or curated entry:

* "Verified" / "reproduced" / "method-ready" applied to an entry
  whose `promotion_gate` items are not all `true` (or whose
  curated-entry maturity tier does not actually clear the claim).
* "Novel" applied to a candidate whose only evidence is
  `corpus_status: "new_candidate"`.
* "Exhaustive" / "complete" / "all heliophysics" applied to a
  discovery run that did not include ADS with a token (§5.2).
* A numeric target paraphrased into a stronger or more general
  form than the source paper's wording.
* A Layer-3 example adapter claimed as runnable when the binding
  depends on an MCP (`xhelio-spice`, `xhelio-cdaweb`, …) that the
  consumer has not configured.
* Citing `paper.first_author` / `paper.authors` for an entry where
  `authors_verified: false` (the curated-corpus rule the README
  already enforces, restated here so promotion-time reviewers do
  not re-introduce the same hazard).

## 7. Where this policy is enforced

The policy is enforced by a mix of automated checks (already in the
bundle) and review obligations:

* `scripts/draft_paper_skill_from_candidates.py` writes the
  `promotion_gate:` block, the quarantine banner, and the
  `draft__` slug; it refuses to write under `references/corpus/`.
  Tests: `tests/test_draft_paper_skill_from_candidates.py`.
* `scripts/discover_heliophysics_literature.py` writes the
  `corpus_status` annotations, the `limits` paragraph, and the
  novelty-join block; CI exercises only `--dry-run`.
  Tests: `tests/test_discover_heliophysics_literature.py`.
* `scripts/validate.sh` enforces the 501-entry invariants on the
  curated corpus and the audit gauntlet on the per-entry surfaces.
* `scripts/audit_*.py` enforce per-layer hygiene
  (`audit_layer_schemas`, `audit_layer_population`,
  `audit_layer2_stubs`, `audit_numeric_claims`,
  `audit_internalization_readiness`, `audit_authorship_prose`,
  `audit_wikilinks`).
* The promotion-gate review at §3 and the rejection log at §4 are
  human / agent obligations. They are not currently CI-gated; a
  future increment may add a "no promotion_gate has all-true
  without a paired curated entry" check, but until it ships the
  social contract is what enforces the gate.

A change to this policy should be reviewed alongside the artifacts
it governs: do not loosen a gate without also loosening the script
that writes the gate, and do not tighten a script without recording
the matching policy update here.
