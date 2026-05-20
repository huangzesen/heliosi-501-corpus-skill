# Candidate-lifecycle / promotion-gate demo

**Status:** offline reproducible demo. Walks one full pass of the
discovery → run-bundle → quarantined-draft → promotion-gate pipeline
using only the fixtures and scripts that already ship in this bundle.
The curated 501-entry corpus is **not touched** by anything in this
demo. No live network is required and no ADS / Crossref tokens are
needed.

**Audience:** corpus authors and reviewers who want to see — end-to-end
— what the existing tooling actually does today, and what still
requires human / agent curation before a candidate can become a
verified entry under `references/corpus/`.

**Companion docs:** [`reports/literature_discovery_pipeline.md`](literature_discovery_pipeline.md)
describes the pipeline design; this report is a concrete walk-through.

> **Honesty banner.** Drafts emitted in this demo are **not corpus
> entries**, are **not** verified, and **must not** be cited as paper
> findings. They are quarantined scaffolds that exist solely so a
> downstream evidence review (human or agent) has somewhere to record
> verification work. The aggregator `SKILL.md` and the curated 501
> entries under `references/corpus/` are unchanged.

---

## 1. Stage map

```
  +-------------------------------+        offline, --dry-run
  | scripts/discover_heliophysics |        reads tests/fixtures/discovery/
  | _literature.py                |        sample_records.jsonl
  +---------------+---------------+
                  | --run-dir
                  v
  +-------------------------------+        persistent run bundle:
  | <run-dir>/candidates.jsonl    |          candidates.jsonl
  |          /run_metadata.json   |          run_metadata.json
  |          /run_report.md       |          run_report.md
  +---------------+---------------+
                  | --from-run-dir
                  v
  +-------------------------------+        offline; refuses to write under
  | scripts/draft_paper_skill_    |        references/corpus/
  | from_candidates.py            |
  +---------------+---------------+
                  |
                  v
  +-------------------------------+        per-draft directory:
  | <drafts-dir>/draft__.../      |          SKILL.md (quarantine banner)
  |              SKILL.md         |          metadata.yaml (promotion_gate)
  |              metadata.yaml    |        aggregate:
  |   draft_manifest.json         |          draft_manifest.json
  |   draft_report.md             |          draft_report.md
  +---------------+---------------+
                  |
                  |  HUMAN / AGENT EVIDENCE REVIEW
                  |  (every promotion_gate item flipped to true,
                  |   four-layer scaffold authored from full text,
                  |   `bash scripts/validate.sh` re-run)
                  v
  +-------------------------------+
  | references/corpus/<entry>/    |        only after the gate clears AND
  | (curated corpus, 501+1 ...)   |        validate.sh + test gauntlet pass
  +-------------------------------+
```

Every solid arrow above is reproduced in §2. The dashed transition into
the curated corpus is the **manual** promotion step described in §3 —
the existing tooling deliberately stops short of it.

## 2. Reproducible walk-through

These commands assume the working directory is the bundle root (the
directory that contains `SKILL.md` and `scripts/`). They write into a
temporary directory so the demo never pollutes `references/corpus/`.

### 2.1 One-time setup

```sh
export DEMO_ROOT=$(mktemp -d -t heliosi-lifecycle.XXXXXX)
echo "$DEMO_ROOT"
```

### 2.2 Stage A — discovery dry-run with a persistent run bundle

```sh
python3 scripts/discover_heliophysics_literature.py \
    --dry-run \
    --run-dir "$DEMO_ROOT/run-2026-05-19"
ls "$DEMO_ROOT/run-2026-05-19"
# -> candidates.jsonl  run_metadata.json  run_report.md
```

Observed counts against the shipped fixture
`tests/fixtures/discovery/sample_records.jsonl` (a deliberately
heterogeneous arXiv + OpenAlex payload):

| Stat | Value | Source |
|---|---|---|
| Raw candidates fetched | 9 | `run_metadata.json::dedupe_summary.raw_candidate_count` |
| Deduped candidates emitted | 7 | `dedupe_summary.deduped_candidate_count` |
| Backends used | `arxiv`, `openalex` | `backends` |
| Manifest entries joined against | 501 | `novelty_join.manifest_entry_count` |
| `corpus_status == already_curated` | 0 | `candidate_counts_by_corpus_status` |
| `corpus_status == new_candidate` | 7 | same |
| `corpus_status == unjoined` | 0 | same |
| Mode | `dry-run` | `mode` |
| Schema | `discovery-run-bundle/1.0` | `schema_version` |

The 9 → 7 collapse exercises every dedupe key path: DOI collision,
arXiv-id collision (with version suffix stripping), and ADS-bibcode
collision. The fixture titles are intentionally non-overlapping with
the curated manifest, so all 7 deduped survivors land as
`new_candidate`; the `already_curated` / `unjoined` behaviour is
exercised separately in §2.4.

`run_report.md` carries the same counts in human form, including the
explicit `Limits (honest framing)` paragraph written by
`scripts/discover_heliophysics_literature.py` (a discovery run is a
bounded frontier sample, *not* an exhaustive census; `new_candidate`
means *no manifest-key hit*, not *verified absent from the
literature*).

### 2.3 Stage B — quarantined draft scaffolds from the run bundle

```sh
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-run-dir "$DEMO_ROOT/run-2026-05-19" \
    --drafts-dir "$DEMO_ROOT/drafts"
ls "$DEMO_ROOT/drafts"
# -> 7 draft__... directories + draft_manifest.json + draft_report.md
```

Observed result:

- **7 / 7** `new_candidate` rows drafted; **0** skipped.
- Each draft directory is named `draft__<author>__<year>__<title-tokens>__<id-hash6>`
  so the `paper-…` naming convention of curated entries is impossible to
  confuse with a draft. Example slug from this run:
  `draft__et__2026__pfss-open-flux-from-non-spherical__937548`.
- `draft_manifest.json` uses schema `draft-scaffold-manifest/1.0`.
- `draft_report.md` opens with a literal `DRAFT — UNVERIFIED — NOT
  PROMOTED` banner.

Each per-draft `SKILL.md` opens with the quarantine block:

```
> **DRAFT — UNVERIFIED CANDIDATE — NOT A CORPUS ENTRY**
>
> This file is a non-authoritative draft generated by
> scripts/draft_paper_skill_from_candidates.py from a discovery
> candidate record. It must not be promoted to the curated 501-entry
> paper-skill corpus, must not be cited as a verified source, and
> must not claim paper findings beyond the imported candidate
> metadata/abstract until the promotion gate below is completed by
> a downstream evidence review.
```

Only the *candidate provenance* block and the *candidate abstract*
block carry imported content. Every Layer-1 / Layer-2 / Layer-3 /
Layer-4 section is an explicit `TODO` — the script deliberately does
**not** invent four-layer content.

`metadata.yaml` mirrors the same quarantine frontmatter and adds a
machine-readable `promotion_gate:` block. Every key starts at `false`:

```yaml
promotion_gate:
  bibliographic_identity_verified: false
  provenance_checked: false
  title_authors_year_conflicts_resolved: false
  abstract_or_full_text_inspected: false
  claims_evidence_extracted: false
  data_tool_contracts_defined: false
  validation_target_recorded: false
  failure_modes_recorded: false
  maturity_tier_assigned: false
```

### 2.4 Stage B′ — `already_curated` and `unjoined` handling

Stage A's fixture produces only `new_candidate` rows. To see all three
corpus-status buckets exercised by the **include-filter contract**, run
the drafter against `tests/fixtures/drafts/candidates_mixed.jsonl` (the
fixture used by `tests/test_draft_paper_skill_from_candidates.py` —
5 rows: 3 × `new_candidate`, 1 × `unjoined`, 1 × `already_curated`):

```sh
# Default filter -- only new_candidate is drafted.
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates tests/fixtures/drafts/candidates_mixed.jsonl \
    --drafts-dir "$DEMO_ROOT/drafts-mixed-default"

# Opt-in: also draft unjoined rows (novelty join was disabled).
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates tests/fixtures/drafts/candidates_mixed.jsonl \
    --drafts-dir "$DEMO_ROOT/drafts-mixed-unjoined" \
    --include-unjoined

# Audit mode (loud opt-in): also draft already_curated rows.
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates tests/fixtures/drafts/candidates_mixed.jsonl \
    --drafts-dir "$DEMO_ROOT/drafts-mixed-all" \
    --include-unjoined --include-all-statuses
```

Observed `selected_count` / `skipped_count` from each
`draft_manifest.json`:

| Run | selected | skipped | selected_by_status | skipped_by_status |
|---|---|---|---|---|
| default | **3** | 2 | `{new_candidate: 3}` | `{unjoined: 1, already_curated: 1}` |
| `--include-unjoined` | **4** | 1 | `{new_candidate: 3, unjoined: 1}` | `{already_curated: 1}` |
| `--include-unjoined --include-all-statuses` | **5** | 0 | `{new_candidate: 3, unjoined: 1, already_curated: 1}` | `{}` |

Key behaviour to notice:

- `already_curated` is **never** drafted by default. It is only included
  under the explicit `--include-all-statuses` opt-in, and the manifest
  records the inclusion in `cli_args` so an auditor can see that the
  loud flag was passed.
- `unjoined` (novelty join disabled) is **never** drafted by default.
  Opting in via `--include-unjoined` does not promote anything — it
  only allows a scaffold to be generated for a row whose novelty status
  is *unknown*.
- The skipped buckets are part of the manifest, not silently dropped.
  `skipped_counts_by_corpus_status` is the auditable record of "what
  the drafter chose not to act on this run."

### 2.5 Stage B″ — hard rail against `references/corpus/`

The drafter refuses to write under the curated corpus root:

```sh
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates tests/fixtures/drafts/candidates_mixed.jsonl \
    --drafts-dir references/corpus/whatever
# stderr:
# draft_paper_skill_from_candidates: refusing to write drafts under
#   references/corpus/ (got references/corpus/whatever). Drafts are
#   non-authoritative quarantine artifacts; the curated corpus is for
#   verified entries only.
# exit code: 1
```

This rail is the *complement* of the quarantine banner: scripts on the
draft side cannot accidentally land in the directory tree that
`scripts/validate.sh` audits as the verified corpus.

## 3. Manual promotion-gate checklist

A draft (`<drafts-dir>/draft__*/`) is **only** eligible for promotion
into the curated corpus once every item below has been completed and
the corresponding key in `metadata.yaml::promotion_gate` has been
flipped to `true`. Each item is the contract; the bracketed phrase is
how the reviewer should record the evidence.

1. **Verify source identity.**
   - `bibliographic_identity_verified` — DOI resolves at the
     publisher of record; arXiv id matches the same paper; bibcode
     (when available) matches; title round-trips.
   - `provenance_checked` — record the resolution evidence in the
     draft `SKILL.md` (link to publisher landing page; arXiv abs
     page; ADS record).
   - `title_authors_year_conflicts_resolved` — when the discovery
     backend's title/authors/year disagree with the publisher of
     record, choose the publisher value and document the
     disagreement.
2. **Inspect the actual paper, not just the abstract.**
   - `abstract_or_full_text_inspected` — the full text has been read
     well enough to author Layer 1 + Layer 2 (the abstract alone is
     **not** sufficient to clear this item; recording why an
     abstract-only review was acceptable, when it is, is also a
     promotion artifact).
3. **Author the four-layer scaffold from evidence.**
   - `claims_evidence_extracted` — Layer-1 invariant is recorded
     with the paper's own claim/evidence boundary; nothing is
     paraphrased into a stronger claim than the paper makes.
   - `data_tool_contracts_defined` — Layer-2 data/tool contracts
     (instrument, cadence, level, archive; algorithm inputs/outputs)
     are written down.
   - `validation_target_recorded` — a concrete numeric or
     figure-level target is recorded (Layer-4 affordance hook).
   - `failure_modes_recorded` — known failure modes and load-bearing
     assumptions are recorded.
4. **Assign tier + adapter decisions.**
   - `maturity_tier_assigned` — pick a tier consistent with
     `references/corpus_qa_report_v2.md` (T1 / T2 / T3 / T4 / pilot).
     If the draft cannot honestly clear T3, leave it as T4 / scaffold
     and document the gap — *do not* round up to clear the checklist.
   - **Adapter decision** (not represented as a single
     `promotion_gate` flag but mandatory in practice): decide whether
     a Layer-3 example adapter is in scope; if it depends on
     `xhelio-spice` / `xhelio-cdaweb` or another MCP, record the
     dependency rather than inventing a fallback. See
     `README.md::Companion MCP adapters` for the policy.
5. **Re-run the bundle gauntlet.**
   - `python3 -m unittest discover -s tests` passes.
   - `bash scripts/validate.sh` passes (this is the gate that
     enforces the 501-entry invariants and the per-batch counts; a
     promotion that breaks it is a failed promotion).
   - The new entry's `SKILL.md` and `metadata.yaml` survive
     `scripts/audit_layer_schemas.py`,
     `scripts/audit_layer_population.py`,
     `scripts/audit_layer2_stubs.py`,
     `scripts/audit_numeric_claims.py`,
     `scripts/audit_internalization_readiness.py`,
     `scripts/audit_authorship_prose.py`, and
     `scripts/audit_wikilinks.py` consistent with the rest of the
     corpus.
6. **Move the entry.**
   - Move the per-draft directory out of the drafts area into the
     appropriate `references/corpus/<batch>/` folder, rename it to
     drop the `draft__` prefix (use the corpus's `paper-…` /
     `<author>-<year>-…` slug convention), update
     `references/corpus_manifest_v2.json` accordingly, and
     re-generate `references/corpus_skill_graph.json` if the manifest
     changed (see `scripts/build_corpus_skill_graph.py` and
     `GRAPH_POLICY.md`).
   - Commit. The promotion is now visible to
     `scripts/search_corpus.py` and to the aggregator skill.

If any of the above is unclear or impossible to complete with the
evidence on hand, **the draft stays in the drafts area**. A draft
sitting unpromoted is not a failure; a draft promoted on insufficient
evidence is.

## 4. What still requires human / agent curation

The pipeline this demo walks is intentionally narrow. The following
are **not** automated today (the pipeline doc lists them under
"Not done" in §6 of `reports/literature_discovery_pipeline.md`):

- **Full-text fetch.** The drafter is offline; it never opens a PDF or
  HTML page. The reviewer is responsible for sourcing the full text.
- **Automated population of Layer 1–4 sections.** The scaffold leaves
  every layer as a `TODO`. A reviewer (human or agent) reads the full
  text and authors those sections; the script will not synthesize them
  from the abstract.
- **Drift detection against existing T1 / T2 claims.** A candidate that
  contradicts an existing entry's claim boundary is not flagged by the
  pipeline; that comparison is a manual step in §3.3 / §3.4.
- **Disambiguation when title + year collapses two distinct papers.**
  The novelty join's title+year fallback hashes the normalised title;
  two genuinely different papers with the same normalised title and
  year would collide. The reviewer is responsible for catching this.
- **Adapter wiring.** Whether a draft should bind a real Layer-3
  adapter (e.g. `xhelio-spice`, `xhelio-cdaweb`, `pyspedas`, an MAS /
  ENLIL runner) is a curation decision, not an automated one. The
  drafter records candidate metadata only.
- **Identity resolution against author records.** Author lists are
  imported as the backend returned them; ORCID / affiliation
  resolution is out of scope.
- **Author of record vs. mirror.** The DOI of record (publisher) and
  the arXiv preprint are sometimes inconsistent (corrections,
  retractions, version drift). The reviewer is responsible for
  picking the version that the corpus entry should anchor on.

The mandate that "HelioSI should not be capped at 501 hand-curated
objects" (literature discovery pipeline doc §1) is therefore *partially*
addressed by this tooling: discovery + dedupe + novelty join + draft
scaffolding are reproducible and offline. The promotion step itself is
**deliberately** still a human/agent decision, gated by the checklist
in §3. Claiming "fully automated paper-skill authoring" today would be
overclaiming.

## 5. Honest framing recap

Carried verbatim from the existing artifacts so this report cannot
silently drift from them:

- *"frontier seed-expansion sample; not a complete survey of the
  heliophysics literature"* — written by
  `scripts/discover_heliophysics_literature.py` into
  `run_metadata.json::framing` on every dry-run.
- *"'new_candidate' means no manifest-key hit, not verified absence
  from all literature."* — part of the limits string written into
  `run_metadata.json::limits` (and the **Limits (honest framing)**
  paragraph of `run_report.md`) by the same script.
- *"Every entry under `drafts[]` is a non-authoritative draft scaffold.
  Drafts must not be promoted to references/corpus/ or cited as
  verified sources until the per-draft promotion_gate in metadata.yaml
  has been completed by a downstream evidence review."* — written by
  `scripts/draft_paper_skill_from_candidates.py` into the **Limits
  (honest framing)** section of `draft_report.md` on every run.
- The companion `draft_manifest.json::limits` is shorter (*"This
  manifest records only what this single invocation drafted from the
  supplied input. It does not assert that the inputs themselves are
  exhaustive, novel, or correctly classified."*) and the `DRAFT —
  UNVERIFIED — NOT PROMOTED` banner sits at the top of the report.
- The aggregator skill's existing verification status — *"This corpus
  is a scaffold / triage substrate, not a fully verified reproduction
  corpus"* — is unaffected by anything in this demo. See
  [`README.md` §Verification status](../README.md#verification-status-read-first).

## 6. Reproducibility

Everything in §2 is reproducible offline with Python 3 stdlib only.
There is no PyYAML, no third-party HTTP library, no ADS token, and no
Crossref opt-in flag involved. The two scripts the demo exercises are:

- `scripts/discover_heliophysics_literature.py` — `--dry-run`
  (default) reads `tests/fixtures/discovery/sample_records.jsonl`.
- `scripts/draft_paper_skill_from_candidates.py` — offline by
  construction; refuses to write under `references/corpus/`.

The relevant test files (which run on every CI invocation of
`python3 -m unittest discover -s tests`) are:

- `tests/test_discover_heliophysics_literature.py`
- `tests/test_draft_paper_skill_from_candidates.py`

A green run of those tests is a stronger guarantee than this report;
the report exists to walk a reviewer through what the green tests
actually mean.
