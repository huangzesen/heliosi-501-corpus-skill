# Open-ended heliophysics literature discovery pipeline

**Status:** seed / frontier-expansion (first concrete increment).
**Scope:** outward-facing literature ingestion that complements the curated
501-entry paper-skill bundle. It does **not** replace, redefine, or
re-author any of the 501 curated entries.
**Owner:** HelioSI corpus authors.
**Entry point:** [`scripts/discover_heliophysics_literature.py`](../scripts/discover_heliophysics_literature.py).
**Companion tests:** [`tests/test_discover_heliophysics_literature.py`](../tests/test_discover_heliophysics_literature.py).

---

## 1. Why this exists

The 501-entry paper-skill corpus that ships in this bundle is a **curated
seed graph**: 18 batches selected by hand to anchor the four-layer
authoring model (Layer-1 invariant, Layer-2 contract, Layer-3 example
adapters, Layer-4 research-generation affordances). It is sized for human
review, not for automated discovery — by construction, the corpus does not
attempt to enumerate "all heliophysics literature."

The mandate has now shifted: HelioSI should not be capped at 501 hand-curated
objects. The goal is fully automated heliophysics research, which requires
an **open-ended literature feed** that:

1. queries public bibliographic backends on a schedule,
2. tags candidates against a heliophysics seed taxonomy,
3. deduplicates across backends with deterministic keys, and
4. emits a **candidate queue** that downstream paper-skill authors (human
   or agent) can pick from.

This report documents the first concrete increment of that pipeline. It
intentionally stops well short of "automatically write new paper-skills";
that is the next layer.

## 2. What this is **not**

To preserve the corpus's existing honesty model, the new pipeline must not
claim more than it actually does:

- **It is not a complete survey.** A single run is a bounded sample driven
  by `--max-results` and the query slate. The script writes the literal
  string `"frontier seed-expansion sample; not a complete survey of the
  heliophysics literature"` into every summary payload so downstream
  consumers cannot accidentally promote a sample to a census.
- **It is not a corpus addition.** The JSONL it emits is a *candidate
  queue*, not an addition to `references/corpus/`. Promoting a candidate
  to a paper-skill is a separate, downstream step that still runs through
  the four-layer authoring model and the existing test gauntlet.
- **It is not verified.** A candidate record carries whatever the upstream
  backend returned. No DOI / arXiv ID / author list is treated as
  verified until it has gone through the same provenance hygiene the
  curated entries use (`scripts/verify_arxiv_ids.py`, the S4d / S4e / S4f
  gates in `scripts/validate.sh`, and the
  `tests/test_arxiv_provenance.py` /
  `tests/test_authorship_hygiene.py` checks).

## 3. Pipeline shape (today)

```
  +-------------------------------+
  |  Seed query slate             |
  |  (DEFAULT_QUERIES + --extra-) |
  +---------------+---------------+
                  |
                  v
  +---------------+---------------+      +-------------------------+
  |  Backend fetch                |<-----+  Backends:              |
  |  (--live; --dry-run uses      |      |   arxiv (no key)        |
  |   tests/fixtures/...)         |      |   openalex (no key)     |
  +---------------+---------------+      |   crossref (opt-in)     |
                  |                      |   ads (opt-in + token)  |
                  v                      +-------------------------+
  +---------------+---------------+
  |  Parse to normalised schema   |
  |  (parse_arxiv_atom,           |
  |   parse_openalex_json, ...)   |
  +---------------+---------------+
                  |
                  v
  +---------------+---------------+
  |  Classify against seed        |
  |  taxonomy (classify_topics)   |
  +---------------+---------------+
                  |
                  v
  +---------------+---------------+
  |  Deterministic dedupe         |
  |  (doi > arxiv > bibcode >     |
  |   title+year sha1 fallback)   |
  +---------------+---------------+
                  |
                  v
  +---------------+---------------+
  |  JSONL candidate queue        |
  |  + summary on stderr          |
  +-------------------------------+
```

### 3.1 Backends

| Backend  | Default? | Key required?                    | Notes                                            |
|----------|----------|----------------------------------|--------------------------------------------------|
| arXiv    | yes      | no                               | Atom XML; `_http_get` retries 429/5xx politely.  |
| OpenAlex | yes      | no                               | JSON; abstract is inverted-index reconstructed.  |
| Crossref | opt-in   | no (`--enable-crossref`)         | Public; kept opt-in for predictable defaults.    |
| NASA ADS | opt-in   | yes (`--enable-ads` + env token) | Reads `ADS_API_TOKEN`, `NASA_ADS_TOKEN`, `ADS_TOKEN`. |

A live `--enable-ads` run with no token in the environment **aborts with
exit code 2** rather than silently downgrading. CI never exercises live
backends — every test runs in `--dry-run` mode against
`tests/fixtures/discovery/sample_records.jsonl`.

### 3.2 Seed taxonomy

The taxonomy is defined as
`scripts/discover_heliophysics_literature.py::SEED_TAXONOMY`. It is a
**seed** layer, not a finished classification scheme. Current tag slugs:

`solar-wind`, `corona`, `cme`, `magnetosphere`, `ionosphere`, `heliosphere`,
`parker-solar-probe`, `solar-orbiter`, `ulysses`, `ace`, `wind-spacecraft`,
`turbulence`, `heating`, `reconnection`, `pfss`, `switchbacks`, `sep`,
`shock`, `alfven-waves`, `flare`, `kinetic-physics`, `machine-learning`.

A future revision will:

- promote / split tags based on actual hit distribution,
- align tag slugs with the per-batch themes already used in
  `references/corpus_manifest_v2.json`,
- and, in a later increment, replace literal-substring matching with a
  proper classifier trained on labelled paper-skills.

### 3.3 Deduplication

`scripts/discover_heliophysics_literature.py::dedupe_key` picks the first
non-empty key in this order:

1. **DOI** — normalised (resolver prefix stripped, lowercased).
2. **arXiv ID** — version suffix stripped, lowercased; supports both
   `YYMM.NNNNN` and old-style `category/YYMMNNN`.
3. **ADS bibcode** — lowercased.
4. **Title + year fallback** — title NFKD-folded + punctuation-stripped +
   lowercased, hashed together with the year via SHA-1 (first 16 hex
   chars). Two records with the same scientific identity but different
   case / punctuation / accents collide; records with genuinely different
   titles do not.

The dedupe is **stable**: the first occurrence wins, ordering is preserved.
The fixture suite pins this behaviour: 9 raw records → 7 deduped
(DOI-collision + arXiv-collision + bibcode-collision each collapse to a
single survivor).

### 3.4 Corpus novelty join

After dedupe, each surviving candidate is compared against the curated v2
manifest (`references/corpus_manifest_v2.json` by default) so that the
JSONL queue tells downstream consumers whether a record is **already in
the 501-entry corpus** or is **genuinely new** to the curated bundle.

The join is implemented in
`scripts/discover_heliophysics_literature.py::annotate_candidate_with_corpus_status`
and is wired into `run_discovery()` via the
`corpus_manifest_path=` keyword. The CLI exposes:

- `--corpus-manifest PATH` — override the default manifest path.
- `--no-corpus-manifest` — disable the join even when the default
  manifest is present.

If neither flag is given, the script auto-resolves the default at
`references/corpus_manifest_v2.json`; if that file is missing, the join
is silently disabled (the candidates are still emitted, just without a
novelty claim).

#### 3.4.1 Match keys (priority order)

The lookup tries the canonical identifiers in **the same priority order
as the dedupe key**, so the join is consistent with the dedupe behaviour
documented in §3.3:

| Priority | Field         | Manifest source             | Normalisation                                                                                |
|----------|---------------|------------------------------|----------------------------------------------------------------------------------------------|
| 1        | `doi`         | `entries[].doi`              | `normalize_doi` — strip resolver prefix, lowercase.                                          |
| 2        | `arxiv_id`    | `entries[].arxiv`            | `normalize_arxiv_id` — strip `arXiv:` prefix / version suffix; reject sentinel placeholders. |
| 3        | `bibcode`     | `entries[].bibcode` (future) | lowercased; current manifest carries no bibcodes — the index tolerates them anyway.          |
| 4        | `title`+`year`| `entries[].title`/`year`     | SHA-1 of `normalize_title(title) + "|" + str(year)`, first 16 hex — identical to `dedupe_key`. |

The first hit wins. The emitted record carries:

- `corpus_status`        — `already_curated`, `new_candidate`, or
                           `unjoined` (when the join was disabled).
- `corpus_match_via`     — `doi` / `arxiv` / `bibcode` / `title_year`,
                           or `null` when no match / disabled.
- `corpus_match_slugs`   — list of matching `slug` strings from the
                           manifest (today: zero or one element; the
                           list shape is forward-compatible with future
                           multi-match policies).
- `corpus_match_titles`  — list of matching titles, parallel to
                           `corpus_match_slugs`.

The JSON summary written to stderr gains a `novelty_join` block:

```json
"novelty_join": {
  "enabled": true,
  "manifest_path": "references/corpus_manifest_v2.json",
  "manifest_entry_count": 501,
  "already_curated_count": 3,
  "new_candidate_count": 4,
  "unjoined_count": 0,
  "match_priority": ["doi", "arxiv", "bibcode", "title_year"],
  "limits": "title+year fallback is sensitive to title-string differences ..."
}
```

#### 3.4.2 Sentinels and placeholders

Some manifest rows store non-ID strings under `arxiv:`:

- `"not-in-local-inventory"` — the curated entry has no usable arXiv ID.
- `"TODO_verify"` / `"TODO_verify_with_full_text"` — pending provenance check.

These are **filtered out** of the `by_arxiv` index by
`_manifest_arxiv_value`, which routes the raw value through
`normalize_arxiv_id` after rejecting the sentinel set
`{"", "none", "n/a", "na", "not-in-local-inventory"}` and any string
that starts with `TODO` / `TBD`. A candidate that happens to carry the
literal string `"not-in-local-inventory"` therefore **does not** match
a manifest row that uses the same sentinel.

#### 3.4.3 Limits (honest disclosure)

The novelty join is **best-effort, not authoritative**:

- Manifest entries without DOI/arXiv/bibcode rely entirely on the
  title+year fallback. Title strings drift between Crossref, OpenAlex,
  arXiv, and the manifest (subtitle present vs absent, `"&"` vs
  `"and"`, smart quotes, etc.). Two records describing the same paper
  can therefore fall on opposite sides of the join.
- The join reads **only** the v2 manifest metadata. It does NOT crack
  open per-entry `SKILL.md` / `metadata.yaml` frontmatter, so any
  identifier that the curated entry advertises only in prose (or only
  inside a `provenance.id_verifications[]` block) is not visible to
  the index.
- `corpus_status: new_candidate` means *"no manifest hit on the
  canonical keys"*, not *"verified absent from the curated corpus"*.
  Downstream consumers must continue to apply human / agent triage
  before promoting a candidate to a paper-skill.
- The join makes no provenance claim. A candidate's `corpus_status`
  field is metadata about the *upstream backend's* identifier match,
  not a substitute for the existing arXiv-ID provenance gauntlet
  (`scripts/verify_arxiv_ids.py`, the S4e gate in `scripts/validate.sh`,
  `tests/test_arxiv_provenance.py`).

The novelty-join fields appear on every emitted candidate, so the JSONL
queue is filterable with one-liners like:

```sh
jq -c 'select(.corpus_status == "new_candidate")' candidates.jsonl
jq -c 'select(.corpus_status == "already_curated") | {id, corpus_match_slugs}' candidates.jsonl
```

### 3.5 Persistent run bundle

A single `--output candidates.jsonl` invocation is enough for ad-hoc use,
but a longer-lived candidate queue benefits from a persistent artifact
convention. `scripts/discover_heliophysics_literature.py` therefore
supports a **run bundle**: a directory written via `--run-dir PATH` that
holds three artifacts side by side.

```
<run-dir>/
  candidates.jsonl     # one normalised + annotated candidate per line
  run_metadata.json    # machine-readable run summary
  run_report.md        # concise human-readable summary of the same counts
```

Schema is versioned via
`scripts/discover_heliophysics_literature.py::RUN_BUNDLE_SCHEMA_VERSION`
(currently `"discovery-run-bundle/1.0"`). The CLI knobs:

| Flag                    | Purpose                                                                                                                              |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `--run-dir PATH`        | Write the three-file bundle into PATH. The directory must be empty (or missing); see `--run-dir-overwrite`.                          |
| `--run-dir-overwrite`   | Allow writing into an existing **non-empty** directory. Without it, the script refuses to clobber a prior run.                       |
| `--prior-runs-root P`   | Scan `P/*/candidates.jsonl` and annotate the current run's candidates with `seen_in_prior_run` / `prior_run_ids`. Read-only on prior runs. |

`run_metadata.json` carries enough state to reproduce the run shape:
`schema_version`, `script_version`, optional `git_commit`, timestamp,
`mode` (dry-run vs live), the resolved CLI knobs, the query slate and
backend list, dedupe + per-backend + per-query counts, backend errors,
the `novelty_join` block, `candidate_counts_by_corpus_status`, optional
`candidate_counts_by_prior_run` (only when the prior-run scan is
enabled), the resolved `output_paths`, the `prior_runs` block (root,
scanned-run summaries, total prior keys), and an explicit `limits`
disclosure.

`run_report.md` mirrors the same counts in a short Markdown summary so
the bundle is reviewable without `jq`: header (mode, timestamp, version,
git commit, backend list, query count); a **Candidate counts** section
(raw / deduped / `corpus_status` buckets + optional prior-run buckets);
a **Novelty join** section; a **Prior-run dedupe** section listing each
scanned run; backend errors if any; a **Limits (honest framing)**
paragraph; and a **Next actions** stub.

#### 3.5.1 Cross-run dedupe semantics

When `--prior-runs-root PATH` is given, the script scans every immediate
subdirectory of PATH that contains a `candidates.jsonl`. For each such
prior run it recomputes the dedupe key for every row (using the same
DOI > arXiv > bibcode > title+year logic documented in §3.3) and builds
a `{dedupe-key -> [prior-run basenames]}` map. The current run's
candidates are then annotated with:

- `seen_in_prior_run` (bool) — true iff the candidate's dedupe key
  appears in any prior run under the root;
- `prior_run_ids` (list of strings) — the basenames of the prior runs
  that emitted the same key; empty list when not seen.

Both fields are **only** emitted when the prior-run scan is enabled.
With no `--prior-runs-root` flag the candidate record shape is identical
to a no-bundle run — no `seen_in_prior_run` field is invented.

The current `--run-dir` is excluded from the scan if it lives under the
prior-runs root, so re-running with `--run-dir-overwrite` cannot count
the current run as its own prior. Prior-run files are **only read**; the
scan never mutates them.

#### 3.5.2 Limits (honest framing)

Captured verbatim in `run_metadata.json::limits` and in the
`run_report.md` "Limits" section:

- A discovery run is a bounded frontier sample, **not** an exhaustive
  census of the heliophysics literature.
- `corpus_status: "new_candidate"` means *no manifest-key hit*, **not**
  *verified absence from all literature*.
- Prior-run dedupe (when enabled) is scoped to the supplied
  `--prior-runs-root` only. A candidate marked `unseen_in_prior_runs`
  may still have appeared in a run stored elsewhere.
- The prior-run scan reads only candidate JSONL files under that root;
  it does not crack open per-entry `SKILL.md` / `metadata.yaml`
  frontmatter (same limitation as the manifest join in §3.4.3).

#### 3.5.3 Example: two-run queue with cross-run dedupe

```sh
# First run -- writes queue/run-a/candidates.jsonl + metadata + report.
python3 scripts/discover_heliophysics_literature.py \
    --dry-run --run-dir queue/run-a

# Second run -- dedupes against queue/run-a (read-only) and writes its
# own bundle into queue/run-b. The "current" run-b is excluded from its
# own prior-run scan.
python3 scripts/discover_heliophysics_literature.py \
    --dry-run --run-dir queue/run-b --prior-runs-root queue
```

After the second run, `queue/run-b/run_metadata.json` carries
`prior_runs.runs_scanned[].name == "run-a"` and
`candidate_counts_by_prior_run.seen_in_prior_run` is non-zero, while
`queue/run-a` is untouched.

### 3.6 Draft paper-skill scaffold (quarantined drafts)

`scripts/draft_paper_skill_from_candidates.py` is the next stage after
discovery: it consumes a candidate JSONL (or a run-bundle directory
produced via `--run-dir`) and emits one **quarantined draft paper-skill
scaffold** per selected candidate. The script is offline by construction
— it never makes network calls.

The scaffold is **not** a corpus entry. Every visible surface of every
draft is marked as quarantined:

- per-draft directory name is prefixed with `draft__` so it can never be
  mistaken for the `paper-…` naming convention of curated entries;
- `SKILL.md` frontmatter carries `kind: discovery-draft`,
  `promotion_status: unreviewed`, `verified: false`,
  `maturity: candidate`, `quality_level: unverified-candidate`,
  `executable_status: unverified-draft`, `authors_verified: false`;
- `SKILL.md` body opens with a **DRAFT — UNVERIFIED CANDIDATE —
  NOT A CORPUS ENTRY** banner that explicitly disclaims promotion;
- `metadata.yaml` mirrors the same fields and adds a
  `promotion_gate:` checklist (`bibliographic_identity_verified`,
  `provenance_checked`, `title_authors_year_conflicts_resolved`,
  `abstract_or_full_text_inspected`, `claims_evidence_extracted`,
  `data_tool_contracts_defined`, `validation_target_recorded`,
  `failure_modes_recorded`, `maturity_tier_assigned`) — every item
  starts as `false`;
- the per-run aggregate `draft_manifest.json` + `draft_report.md` at
  the drafts-dir root carry the same disclosure.

The script refuses to write under `references/corpus/` so the curated
501-entry invariants enforced by `scripts/validate.sh` cannot be
silently broken by a draft.

#### 3.6.1 CLI

| Flag                       | Purpose                                                                                                       |
|----------------------------|---------------------------------------------------------------------------------------------------------------|
| `--drafts-dir PATH`        | Directory to write per-draft subdirectories + the manifest/report. Required. Must be outside `references/corpus/`. |
| `--from-candidates PATH`   | Candidate JSONL (the discovery script's `--output` shape). Mutually exclusive with `--from-run-dir`.          |
| `--from-run-dir PATH`      | Discovery run-bundle directory (reads `PATH/candidates.jsonl`). Mutually exclusive with `--from-candidates`.  |
| `--include-unjoined`       | Also draft rows with `corpus_status == "unjoined"`. Off by default.                                            |
| `--include-all-statuses`   | Also draft rows with `corpus_status == "already_curated"` (loud opt-in; intended for audit only).             |
| `--overwrite`              | Replace existing per-draft directories. Off by default; the script never silently clobbers prior drafts.       |

By default the script drafts **only `corpus_status == "new_candidate"`**
rows. `already_curated` candidates are never drafted unless
`--include-all-statuses` is passed.

Each per-draft directory is::

    <drafts-dir>/draft__<author>__<year>__<title-tokens>__<id-hash6>/
        SKILL.md
        metadata.yaml

The slug is deterministic: same candidate input ⇒ same slug. The trailing
six-hex-char hash is derived from the candidate's discovery dedupe id, so
two candidates that share a first author + year + similar title still get
distinct slugs.

#### 3.6.2 Output shape

At `<drafts-dir>/`:

- `draft_manifest.json` — schema-versioned
  (`"draft-scaffold-manifest/1.0"`). Carries the input kind + path, the
  CLI args, `selected_count`, `skipped_count`,
  `selected_counts_by_corpus_status`, `skipped_counts_by_corpus_status`,
  the list of `promotion_gate_keys`, a per-draft summary list
  (`slug`, `path`, `corpus_status`, `dedupe_id`, `title`, `year`, `doi`,
  `arxiv_id`, `source`), the quarantine disclosure, and an explicit
  `limits` paragraph.
- `draft_report.md` — short Markdown summary with the same headline
  disclosure and counts.

#### 3.6.3 Examples

```sh
# Default: read a candidate JSONL, write drafts for new_candidate rows only.
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates /tmp/cand.jsonl --drafts-dir /tmp/drafts

# Read from a discovery run bundle (no live network in either step).
python3 scripts/discover_heliophysics_literature.py \
    --dry-run --run-dir /tmp/run-a
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-run-dir /tmp/run-a --drafts-dir /tmp/drafts

# Also draft unjoined rows (novelty join disabled at discovery time).
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates /tmp/cand.jsonl --drafts-dir /tmp/drafts \
    --include-unjoined

# Audit mode: also draft already_curated rows (loud opt-in).
python3 scripts/draft_paper_skill_from_candidates.py \
    --from-candidates /tmp/cand.jsonl --drafts-dir /tmp/drafts \
    --include-all-statuses
```

#### 3.6.4 Limits (honest framing)

- **Drafts are not corpus entries.** A draft only repeats what the
  discovery backend returned (title, year, DOI, arXiv, abstract, authors,
  URL, query, dedupe id) plus the `corpus_status` annotation from the
  novelty join. Every other section of the draft `SKILL.md` is a `TODO`
  pending the promotion-gate evidence review.
- **The promotion gate is the contract.** A draft must not be moved into
  `references/corpus/` until every `promotion_gate` item in
  `metadata.yaml` has been flipped to `true` with the corresponding
  evidence recorded in `SKILL.md`. After the move, the curated entry
  must still pass `bash scripts/validate.sh` and the existing test
  gauntlet — this script does not bypass any of that.
- **No live network.** The script is offline. DOI resolution, arXiv
  title verification, and full-text fetches are intentionally out of
  scope. Use `scripts/verify_arxiv_ids.py` and the S4d / S4e / S4f gates
  in `scripts/validate.sh` as the live verification path.
- **Slug collisions.** Two candidates with the same author + year +
  title-prefix still get distinct slugs via the trailing six-hex-char
  id-hash suffix. A pathological collision still in the same run
  triggers a `SystemExit` rather than overwriting; `--overwrite` is
  required to replace existing per-draft directories.

## 4. Relationship to the curated 501-skill corpus

The new pipeline is **strictly additive**. The curated corpus retains its
honesty model, its tier counts, its claim boundaries, its validation
gauntlet (`bash scripts/validate.sh`), and its `search_corpus.py` surface.

```
  +------------------------------------+        +-------------------------------+
  | discover_heliophysics_literature   |        | search_corpus.py              |
  |  (outward; open-ended frontier)    |        |  (inward; curated 501 corpus) |
  |                                    |        |                               |
  |  Emits: candidate JSONL queue      |        |  Reads: corpus_manifest_v2 +  |
  |  Touches: tests/fixtures/...       |        |          references/corpus/   |
  +--------------+---------------------+        +---------------+---------------+
                 |                                              ^
                 v                                              |
  +------------------------------------+                        |
  | draft_paper_skill_from_candidates  |                        |
  |  (offline; per-candidate scaffold) |                        |
  |  Emits: <drafts-dir>/draft__*/     |                        |
  |          + draft_manifest.json     |                        |
  |          + draft_report.md         |                        |
  |  Refuses to write under            |                        |
  |   references/corpus/.              |                        |
  +--------------+---------------------+                        |
                 |  (promotion-gate evidence review;            |
                 |   four-layer authoring model)                |
                 v                                              |
   +------------------------------------+                       |
   | Promote draft -> paper-skill       |-----------------------+
   | -> new entry in references/corpus/ |   (only after every
   |                                    |    promotion_gate item
   +------------------------------------+    flips to true AND
                                             validate.sh passes)
```

A candidate cannot enter `references/corpus/` until it goes through the
four-layer authoring model and survives the existing tests. That bar is
unchanged.

## 5. CI & determinism

- Default mode is `--dry-run` and makes **no network calls**. CI runs the
  full unit-test suite in this mode.
- Live mode (`--live`) is opt-in. It is not exercised in CI and produces
  outputs that depend on backend state, which is — by design — not
  deterministic.
- The HTTP layer is polite: descriptive `User-Agent`, bounded exponential
  backoff on 429 / 408 / 425 / 500 / 502 / 503 / 504 and `URLError`,
  retries gated by `--page-pause-seconds` between successive backend
  fetches. Tests inject `sleep` and `urlopen` shims so the backoff
  schedule is verifiable without real waiting.

## 6. Honest roadmap

Done in earlier increments:

- [x] Default no-key backends (arXiv + OpenAlex), opt-in Crossref + ADS.
- [x] Deterministic dedupe across backends.
- [x] Seed taxonomy + classifier.
- [x] Fixture-driven dry-run + unit tests.
- [x] Polite HTTP layer with bounded retries.

Done in earlier increment (§3.4):

- [x] Novelty join against the curated v2 manifest by canonical keys
      (DOI > arXiv ID > bibcode > title+year), with sentinel /
      TODO-placeholder filtering on the manifest side.
- [x] `corpus_status` / `corpus_match_via` / `corpus_match_slugs` /
      `corpus_match_titles` on every emitted candidate.
- [x] `summary.novelty_join` block reporting `enabled`,
      `manifest_path`, `manifest_entry_count`,
      `already_curated_count`, `new_candidate_count`,
      `unjoined_count`, `match_priority`, and an explicit `limits` disclosure.
- [x] CLI flags `--corpus-manifest PATH` (override) and
      `--no-corpus-manifest` (disable), with the default resolving to
      `references/corpus_manifest_v2.json` only when present.
- [x] Offline unit tests for DOI / arXiv / title+year / bibcode-priority
      / non-match / sentinel-arxiv / disabled-join paths.

Done in earlier increment (§3.5):

- [x] Persistent run-bundle artifact convention: `--run-dir PATH`
      writes `candidates.jsonl`, `run_metadata.json`, and
      `run_report.md` side by side; schema version is pinned via
      `RUN_BUNDLE_SCHEMA_VERSION = "discovery-run-bundle/1.0"`.
- [x] `run_metadata.json` captures script + schema version, optional
      git commit, timestamp, mode, resolved CLI knobs, query slate,
      backend list, dedupe + per-backend + per-query counts, backend
      errors, novelty-join block, candidate counts by `corpus_status`,
      output paths, prior-run scan summary, and explicit limits.
- [x] Cross-run dedupe against prior **candidate batches** via
      `--prior-runs-root PATH`; emits per-candidate
      `seen_in_prior_run` + `prior_run_ids`. Prior runs are read-only;
      the current run-dir is excluded from its own prior scan; the
      annotation fields are NOT invented when the scan is disabled.
- [x] `--run-dir-overwrite` is required to write into a non-empty
      directory; otherwise the script refuses to clobber a prior run.
- [x] Offline unit + CLI tests for bundle artifacts, metadata schema,
      Markdown report counts, prior-run dedupe semantics, and the
      "disabled manifest stays `unjoined`, not `new_candidate`" guard.

Done in this increment (§3.6):

- [x] Per-candidate quarantined draft scaffold generator
      (`scripts/draft_paper_skill_from_candidates.py`) consuming either
      a candidate JSONL or a run-bundle directory.
- [x] Default filter on `corpus_status == "new_candidate"`;
      `--include-unjoined` and `--include-all-statuses` opt-ins;
      `already_curated` never drafted by default.
- [x] Deterministic, filesystem-safe, collision-aware `draft__` slugs
      with a six-hex-char id-hash suffix.
- [x] Per-draft `SKILL.md` with DRAFT/UNVERIFIED/NOT-A-CORPUS-ENTRY
      banner, four-layer scaffold (Layer 1/2/3/4), candidate provenance
      block, candidate abstract block, validation-TODO checklist, and a
      promotion-gate disclosure.
- [x] Per-draft `metadata.yaml` with quarantine frontmatter
      (`kind: discovery-draft`, `promotion_status: unreviewed`,
      `verified: false`, `maturity: candidate`,
      `quality_level: unverified-candidate`,
      `executable_status: unverified-draft`,
      `authors_verified: false`) and a machine-readable
      `promotion_gate:` checklist.
- [x] Aggregate `draft_manifest.json`
      (schema `"draft-scaffold-manifest/1.0"`) +
      `draft_report.md` at the drafts-dir root, with selected/skipped
      counts by `corpus_status` and explicit quarantine framing.
- [x] Hard rail: the script refuses to write under
      `references/corpus/`, preserving the 501-entry invariants
      enforced by `scripts/validate.sh`.
- [x] Offline unit + CLI tests for include filters, collision/overwrite
      behaviour, slug determinism + safety, manifest/report content,
      and the run-bundle input path.

Not done (explicit future work — do **not** claim these are present):

- [ ] Multi-match / disambiguation policy when title+year collapses
      two genuinely distinct papers (today the first manifest entry
      to claim the title-year hash wins).
- [ ] Join against `SKILL.md` / `metadata.yaml` per-entry frontmatter
      (currently only the manifest top-level is read; identifiers that
      live only in the per-entry frontmatter are invisible to the join).
- [ ] Full-text fetch and section extraction.
- [ ] Automated population of the four-layer scaffold sections from the
      full text (the §3.6 scaffold leaves Layer 1-4 as explicit TODOs;
      a downstream pass — human or agent — fills them in only after the
      full text has been read and the promotion gate cleared).
- [ ] Drift detection (a candidate that contradicts an existing T1 / T2
      entry's claim boundary).
- [ ] Scheduling, observability, and rate-limit budget enforcement for
      production runs.
- [ ] Refined classifier (probabilistic, multi-label, with explicit
      out-of-distribution rejection).

The script's CLI surface and JSONL schema are versioned via
`__version__ = "0.1.0"`; bumps will follow semver-ish discipline once the
queue gains downstream consumers.

## 7. Operational notes

- The CLI defaults to `--dry-run` so an accidental invocation never makes
  network calls.
- `--queries-only` prints the resolved query slate as JSON and exits, so
  the slate can be inspected without running any fetch.
- The script is **stdlib only**. There is no third-party HTTP, parsing, or
  retry library involved. Anything PyYAML-dependent that ships in the
  bundle is consumed by *other* scripts (notably `scripts/validate.sh`),
  not by this one.
