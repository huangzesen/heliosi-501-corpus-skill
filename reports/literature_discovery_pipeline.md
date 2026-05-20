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
                 |  (manual / future-agent triage)              |
                 v                                              |
   +------------------------------------+                       |
   | Author paper-skill (4-layer model) |-----------------------+
   | -> new entry in references/corpus/ |   (only after passing
   |                                    |    the existing test
   +------------------------------------+    + validate.sh gates)
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

Done in this increment (§3.4):

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

Not done (explicit future work — do **not** claim these are present):

- [ ] Persistent candidate queue store (today the JSONL is the queue).
- [ ] Cross-run dedupe against prior **candidate batches** (this
      increment only joins against the curated 501-entry manifest, not
      against previously emitted candidate JSONLs).
- [ ] Multi-match / disambiguation policy when title+year collapses
      two genuinely distinct papers (today the first manifest entry
      to claim the title-year hash wins).
- [ ] Join against `SKILL.md` / `metadata.yaml` per-entry frontmatter
      (currently only the manifest top-level is read; identifiers that
      live only in the per-entry frontmatter are invisible to the join).
- [ ] Full-text fetch and section extraction.
- [ ] Automated four-layer paper-skill drafting from a candidate.
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
