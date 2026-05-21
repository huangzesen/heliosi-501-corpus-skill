# HelioSI literature acquisition: queue + batch runner

This report documents the queue + batch acquisition infrastructure that
ingests the pilot discovery candidates (see
[`reports/pilot_run_summaries.md`](pilot_run_summaries.md)) and walks
them through `fetch_paper.py` (the academic-research utilities tier
ladder: arXiv → Unpaywall → Europe PMC → CORE → publisher-extract →
LibGen).

## Scope and honest caveats

- This is **acquisition infrastructure plus a first smoke batch**, not a
  bulk download of the full pilot. Of the 778 deduped pilot candidates,
  only **10 rows** have been touched by a live `fetch_paper.py`
  subprocess so far (the smoke runs documented below).
- LibGen was disabled (`--no-libgen`) for every smoke run. The
  acquisition store at the time of writing contains **only** PDFs that
  Unpaywall (or another open-access tier) served. No legally sensitive
  last-resort tier has been engaged.
- Rows without a DOI/arXiv identifier (88 of 778: 83 bibcode-only plus
  5 with no supported identifier at all) cannot be fetched directly today --
  `fetch_paper.py` accepts DOI / arXiv / PMID, not bibcodes. They sit in
  the queue with status `no_supported_identifier` until a future
  ADS-resolver step lands.
- Acquisition outputs live **outside the git repo** under
  `sioulas-reproduction/results/heliosi_acquisition/`. PDFs are never
  committed.

## Files added in this batch

```
scripts/build_acquisition_queue.py      # pilot -> normalized queue
scripts/run_acquisition_batch.py        # resumable N-at-a-time runner
tests/test_build_acquisition_queue.py
tests/test_run_acquisition_batch.py
tests/fixtures/acquisition/P1-demo/candidates.jsonl
tests/fixtures/acquisition/P2-demo/candidates.jsonl
reports/literature_acquisition_runner.md   # this file
```

`bash scripts/validate.sh` and `python3 -m pytest tests/` both stay
green after these additions (371 passed after parent-review regression coverage).

## External acquisition store layout

The store is created on demand by `build_acquisition_queue.py`:

```
sioulas-reproduction/results/heliosi_acquisition/
    queue.jsonl                 # the in-place mutating queue
    queue.csv                   # CSV mirror (human-friendly)
    queue.meta.json             # build metadata + summary counts
    attempts/<candidate_id>.json   # per-row attempt manifest (runner output)
    papers/<slug>/                 # downloaded PDFs (fetch_paper.py output)
        manifest.json
        metadata.json
        paper.pdf
    runs/<run_id>/
        summary.json
        stdout.log
        stderr.log
```

Each queue row carries (see `QUEUE_FIELDS` in
`build_acquisition_queue.py`):

```
candidate_id           sha1(preferred-id) prefix; stable across cells
cell                   pilot cell label (P1-ads-1960s-era, ...)
source                 discovery backend (ads / crossref / openalex / arxiv)
title, year            display fields
doi, arxiv_id,         raw identifiers (any may be null)
bibcode
corpus_status          from discovery (new_candidate | already_curated)
preferred_identifier   value passed to fetch_paper.py (or null)
identifier_kind        doi | arxiv | bibcode_only | none
priority               10/20/90/99 (lower = run earlier)
status                 pending | fetched | fetch_failed |
                       skipped_already_done | no_supported_identifier |
                       dry_run_metadata_only
notes                  free text (dedupe trail, last run_id)
queued_at_utc          ISO timestamp written by the builder
```

### Identifier selection rule

DOI is preferred over arXiv, which is preferred over bibcode. Rows that
only carry a bibcode are marked `identifier_kind=bibcode_only` and
status `no_supported_identifier`, so the runner walks past them.

### Dedupe rule

Rows are deduped on `candidate_id`. The hash key prefers DOI, then
arXiv, then bibcode, then normalized title+year. When a second cell
surfaces the same candidate, its cell label is appended to the
surviving row's `notes` (e.g. `"also-seen-in:P2-helio-bfield-1970s-80s"`).
`already_curated` rows are dropped by default; pass
`--include-already-curated` to keep them with status
`skipped_already_done`.

## Building the queue

```
python3 scripts/build_acquisition_queue.py \
    --pilot-root /tmp/heliosi-ads-pilot-20260521T000245Z \
    --out-dir /Users/huangzesen/work/projects/lingtai-space-research/\
sioulas-reproduction/results/heliosi_acquisition
```

Initial build at task time:

```
total              778
by_status
    pending                    690
    no_supported_identifier     88
by_identifier_kind
    doi              690
    bibcode_only      83
    none               5
by_cell
    P1-ads-1960s-era             115
    P2-helio-bfield-1970s-80s    323
    P3-sw-ml-2000s-2020s         340
```

(`already_curated` rows from the P3 pilot were dropped by default;
15 such rows exist and would land with status
`skipped_already_done` under `--include-already-curated`.)

## Running a batch

```
python3 scripts/run_acquisition_batch.py \
    --store .../heliosi_acquisition \
    --limit 5 \
    --no-libgen \
    --email <a real address> \
    [--year-min 2015]               # optional selection filters
    [--year-max 2020]
    [--candidate-id cand_xxx ...]   # repeatable, restricts to a set
    [--dry-run-fetch]               # resolve metadata only; queue not mutated
    [--fetch-timeout 180]
```

The runner:

1. Reads `queue.jsonl` and selects up to `--limit` rows whose status is
   `pending` and that have a `preferred_identifier`. Optional
   `--year-min` / `--year-max` / `--candidate-id` filters narrow the
   selection.
2. For each selected row, checks `attempts/<id>.json` -- if a prior
   attempt reports `last_result = fetched`, the row is rewritten to
   `skipped_already_done` (no subprocess is started). This is the
   in-store half of resumability; the other half is `fetch_paper.py`'s
   own idempotent `papers/<slug>/manifest.json` short-circuit.
3. Invokes `fetch_paper.py` as a subprocess with the configured email,
   `--no-libgen` if requested, and a per-row timeout. Captures stdout
   and stderr into `runs/<run_id>/{stdout,stderr}.log`.
4. Reads the resulting `papers/<slug>/manifest.json` to classify the
   outcome (`fetched` if status=ok, `fetch_failed` otherwise) and
   writes a per-candidate attempt manifest with snippets of stdout /
   stderr.
5. Atomically rewrites `queue.jsonl` after every row, so an interrupt
   loses at most the in-flight row's attempt file. CSV mirror is
   refreshed at the end of the run.

Credentials are never read, printed, or written. The private ADS token
stored in the agent secret store is **not** consulted by either script --
the queue is built from cached pilot JSONL, and the runner only forwards
an optional `--email` to fetch_paper.py for Unpaywall politeness.

## Smoke results (live, --no-libgen, 2026-05-20 UTC)

### Smoke 1 -- first 5 pending rows (1958-1960 era)

```
run_id  20260521T003357Z-1c02d4
options limit=5 no_libgen=true dry_run=false
result  fetch_failed: 5
```

All five 1958-1960 Parker / Coleman / Piddington DOIs resolved via
Crossref (metadata.json written) but every OA tier (arXiv, Unpaywall,
Europe PMC, CORE, publisher-extract) missed and LibGen was disabled.
The runner faithfully recorded `status=fail, reason=all tiers
exhausted` in each `papers/<slug>/manifest.json` and translated that
into `fetch_failed` in the queue. **Not a bug** -- this is the
expected outcome for pre-arXiv pre-OA physics papers without LibGen.

### Smoke 2 -- first 5 pending rows with year >= 2015

```
run_id  20260521T003605Z-5dd9be
options limit=5 year_min=2015 no_libgen=true dry_run=false
result  fetched: 2, fetch_failed: 3
fetched papers
    cand_5c8a4cd7f3ad2a38  10.1007/s11214-015-0211-6  (Fox+ 2016 Solar Probe Plus mission)   7.1M  tier=unpaywall
    cand_b498a68ade7a55fa  10.1007/s11214-015-0164-9  (Burch+ 2016 MMS overview)             3.1M  tier=unpaywall
```

Open-access path works end-to-end through Unpaywall.

### Smoke 3 -- resumability sanity check

```
run_id  20260521T003740Z-7c6419
options limit=3 year_min=2015 candidate_id={5c8a..., b498..., c0a4...}
result  started_pending=0
```

Re-running with the same modern candidate IDs (two already `fetched`,
one already `fetch_failed`) selected zero rows. Resumability holds at
the queue-status level; the fetch_paper.py-side idempotency is the
backstop.

### Queue state after the three smoke runs

```
fetched                   2
fetch_failed              8
pending                 680
no_supported_identifier  88
total                   778
```

## Recommended next command for the parent

To continue draining the modern-era subset (where OA hit-rate is much
higher), the parent agent can keep running batches of 10-20:

```
python3 scripts/run_acquisition_batch.py \
    --store .../heliosi_acquisition \
    --limit 20 \
    --year-min 2010 \
    --no-libgen \
    --email <real address>
```

Once Jason explicitly approves LibGen, drop `--no-libgen` to pick up
the older papers that no current OA tier serves. Until then, the
fetch_failed rows are a faithful "OA-only" subset, not a
gap-needs-fixing.

For bibcode-only rows (88), no batch run can convert them today; that
requires a separate ADS-resolver step that asks NASA ADS for the DOI
(or arXiv ID) given a bibcode, then promotes the row's
`preferred_identifier` and `identifier_kind`. That step is **not yet
implemented**; mentioning it here so the next agent does not silently
treat `no_supported_identifier` as "tried and failed."
