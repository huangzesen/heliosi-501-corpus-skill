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

Done in this increment:

- [x] Default no-key backends (arXiv + OpenAlex), opt-in Crossref + ADS.
- [x] Deterministic dedupe across backends.
- [x] Seed taxonomy + classifier.
- [x] Fixture-driven dry-run + unit tests.
- [x] Polite HTTP layer with bounded retries.

Not done (explicit future work — do **not** claim these are present):

- [ ] Persistent candidate queue store (today the JSONL is the queue).
- [ ] Cross-run dedupe against the curated corpus and against prior
      candidate batches.
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
