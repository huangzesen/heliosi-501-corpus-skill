# 1950-present heliophysics literature discovery & acquisition plan

**Status:** scope-expansion plan (report-only). Documents the source
coverage, run-bundle layout, full-text acquisition ladder, decade /
query partitioning, rate-limit / backoff discipline, provenance /
honesty boundaries, and a bounded pilot for a recurring discovery
sweep that targets *all* heliophysics literature from **1950 to
present** — not only the modern (post-1990) preprint era the existing
seed slate happens to cover. **No mass crawl is performed by this
report.** The promotion gate at `DISCOVERY_POLICY.md` §3 still governs
every transition into `references/corpus/`.

**Audience:** corpus authors, agent operators, and reviewers who want
to expand discovery scope without weakening the curated corpus's
claim-boundary discipline.

**Companion docs:**
- [`DISCOVERY_POLICY.md`](../DISCOVERY_POLICY.md) — lifecycle states,
  promotion gates, rejection vocabulary, automation boundary.
- [`reports/literature_discovery_pipeline.md`](literature_discovery_pipeline.md)
  — current discovery pipeline (`discover_heliophysics_literature.py`).
- [`reports/candidate_lifecycle_demo.md`](candidate_lifecycle_demo.md)
  — reproducible walk-through of the existing dry-run → run-bundle →
  draft scaffold path.
- [`GRAPH_POLICY.md`](../GRAPH_POLICY.md) — machine-graph boundary.
- [`VALIDATION.md`](../VALIDATION.md) — curated-corpus invariants.
- `~/.lingtai-tui/utilities/academic-research/SKILL.md` and its
  `reference/` cards (`api-nasa-ads.md`, `api-openalex.md`,
  `api-crossref.md`, `api-unpaywall.md`, `pipeline-obtain-pdf.md`,
  `pipeline-discovery.md`) — external skill that this plan reuses
  for PDF acquisition; **not bundled in this corpus**, only
  referenced as a host-side capability.

> **Honesty banner.** This report is a *plan*. It does not perform a
> live crawl, does not write candidates, does not move drafts into
> `references/corpus/`, and does not bump the 501-entry invariant in
> `scripts/validate.sh`. Every transition into the curated corpus
> still goes through the §3 promotion gate of `DISCOVERY_POLICY.md`
> on a per-paper basis, and the existing aggregator skill's
> verification status is unchanged.

---

## 1. Motivation & scope

The current discovery slate (`DEFAULT_QUERIES` in
`scripts/discover_heliophysics_literature.py`) is six modern-era query
strings biased toward arXiv-indexed topics (switchbacks, PSP, PFSS,
SEP, ML classification). Combined with the no-date-filter live mode,
that biases candidates strongly toward 2010-present arXiv coverage. A
1950-present scope requires:

1. **A heliophysics-aware index** as the spine. ADS is the only
   backend in the current slate that has reliable coverage back to
   pre-arXiv journal articles (Parker 1958, Mariner-era observations,
   Helios, Voyager, Ulysses). ADS is opt-in and token-gated
   (`DISCOVERY_POLICY.md` §5.2); a 1950-present sweep without ADS is
   not honestly defensible.
2. **A bounded query slate per decade**, so each run remains a
   *frontier sample* rather than an attempt at a complete census the
   pipeline cannot defend.
3. **A persistent run-bundle convention** with cross-run dedupe, so
   sweeps over disjoint decades / topics accumulate into a queue
   without re-emitting the same paper.
4. **A documented full-text ladder** for the small subset of
   candidates that survive promotion-gate triage and need Layer-1
   authoring evidence.
5. **An explicit honesty surface** — what a 1950-present sweep does
   and does not assert.

Scope **out** of this plan: automated paper-skill authoring, full-text
PDF storage inside this bundle, retraction-tracking automation,
mass-PDF caching, classifier training. Those are downstream
increments and are explicitly **not** addressed here.

## 2. Source tiers

Tiers below are *discovery* tiers (which backend returns the
candidate's bibliographic record), distinct from the *acquisition*
ladder in §5 (which fetches the paper PDF). Both ladders are
deliberately separated so a candidate can be discovered without ever
being downloaded.

### 2.1 Discovery tiers (bibliographic only)

| Tier | Backend | Pre-1990 coverage | Default? | Auth | Tag in `corpus_status` | Notes |
|------|---------|-------------------|----------|------|------------------------|-------|
| D1 | **NASA ADS** | strong (1950s journals indexed by bibcode; the heliophysics-native index) | **opt-in (`--enable-ads`) + token** | `ADS_API_TOKEN` / `NASA_ADS_TOKEN` / `ADS_TOKEN` | source: `ads` | Spine for a 1950-present sweep. Bibcodes (`YYYYJJJJJVVVVVPPPpage`) are first-class identifiers. |
| D2 | **OpenAlex** | broad but uneven before 1990; better post-2000 | yes (live mode) | none (mailto recommended) | source: `openalex` | Filter via `filter=publication_year:1950-1990`. Concept IDs are useful for heliophysics sub-domain queries. |
| D3 | **Crossref** | strong for DOI-registered journal articles; sparse for very old work | opt-in (`--enable-crossref`) | none (Polite Pool via mailto) | source: `crossref` | Filter via `filter=from-pub-date:1950-01-01,until-pub-date:1989-12-31`. Useful for filling DOI metadata that ADS / OpenAlex omit. |
| D4 | **arXiv** | none before 1991 (arXiv launched 1991) | yes (live mode) | none | source: `arxiv` | Keep enabled but expect zero pre-1991 hits; arXiv coverage of heliophysics-by-topic remains weak before ~2005. |

A 1950–1990 sweep that omits ADS is **not** a 1950–1990 sweep — it is
a frontier sample of whatever happens to be DOI-registered or
arXiv-mirrored. The pipeline already aborts loudly when
`--enable-ads` is passed without a token; this plan treats the abort
as a feature, not a bug, and requires reviewers to confirm a token
exists before claiming pre-1990 coverage.

### 2.2 Full-text acquisition tiers (PDF / text)

These are *not* invoked by `discover_heliophysics_literature.py`. They
are invoked manually (or by the host's `academic-research` skill) on
the small subset of candidates the reviewer has chosen to promote.

| Tier | Source | Best for | Auth | Notes |
|------|--------|----------|------|-------|
| F1 | **arXiv direct** | preprints 1991-present | none | `https://arxiv.org/pdf/{id}.pdf`. |
| F2 | **Unpaywall** | publisher-blessed gold/green OA via DOI | **real email** (`LINGTAI_RESEARCH_EMAIL`) | placeholder emails get HTTP 422. |
| F3 | **Europe PMC** | biomedical-adjacent space-biology / heliospheric-radiation work | none | full-text XML where available. |
| F4 | **CORE** | institutional repositories | `CORE_API_KEY` recommended (10 000/day vs ~100/day) | useful for old technical reports and theses. |
| F5 | **Publisher-page extraction** | Nature / APS / AIP / IOP / Cambridge | none (browser-based) | structured Markdown + LaTeX. Auto-installs on first use. |
| F6 | **Zotero / Wikipedia / ADS-linked archives** | pre-1990 journals with no OA mirror (e.g. early JGR, GRL, ApJ, A&A volumes that pre-date publisher DOIs) | none | manual link-tracing; reviewer-driven only. |
| F7 | **LibGen / Sci-Hub** | last-resort access to paywalled work | none | legal status varies by jurisdiction; **opt-in only** (`--no-libgen` to skip). Treated as `inaccessible_text` rejection (§4) by default. |

The acquisition ladder is the host-side `academic-research` skill's
`scripts/fetch_paper.py`. This corpus does **not** bundle a PDF
fetcher; bundling one would re-implement an existing skill and
collide with the `xhelio-spice` / `xhelio-cdaweb` MCP boundary
already documented in `README.md` §*Companion MCP adapters*.

## 3. Dedupe keys & cross-run novelty join

Already implemented and stable; this plan does **not** widen the key
order:

1. **DOI** (normalised: resolver prefix stripped, lowercased).
2. **arXiv ID** (version suffix stripped; `YYMM.NNNNN` and old-style
   `category/YYMMNNN`).
3. **ADS bibcode** (lowercased).
4. **Title + year SHA-1 fallback** (NFKD-folded title, punctuation
   stripped, lowercased; SHA-1 first 16 hex of `title|year`).

Three known sharp edges for a 1950-present sweep, none of which is
introduced by this plan but all of which become more visible at
scale:

- **Pre-DOI papers** (a large fraction of 1950–1985 literature) rely
  on the title+year fallback. Title strings drift between ADS,
  OpenAlex, and Crossref (subtitle present vs absent, `"&"` vs
  `"and"`, smart quotes, accented author names). Two records of the
  *same* paper can therefore land on opposite sides of the join.
  Mitigation: prefer ADS as the primary spine, retain its bibcode in
  `corpus_match_via`, and treat any title+year-only match as
  *suggestive*, not authoritative, at promotion review.
- **Multi-version arXiv preprints with different DOIs** (publisher
  version + arXiv version): the dedupe rolls them together via the
  DOI > arXiv ID priority; the `--prior-runs-root` scan inherits the
  same priority, so a re-emission across two runs collapses on the
  shared DOI when present.
- **ADS bibcode reuse** for errata / addenda: ADS sometimes issues a
  separate bibcode for a corrigendum that shares the DOI of the
  primary article. The current dedupe treats these as distinct
  records when DOI is absent and as the same record when DOI is
  present. A 1950-present sweep that wants to distinguish addenda
  should record this as a known limitation in `run_metadata.json`
  rather than expand the key order.

Novelty join (`corpus_status`) semantics are unchanged. A
1950-present sweep is expected to produce **many** `new_candidate`
rows simply because the curated 501-entry corpus is post-1990-biased.
Per `DISCOVERY_POLICY.md` §5.3, `new_candidate` is *no manifest hit*,
not *verified absent from the literature* and not *novel research
result*.

## 4. Run-bundle schema (1.0, unchanged; usage profile)

The bundle layout stays `discovery-run-bundle/1.0`:

```
<runs-root>/
  ads-1950s-spine/                  # one run-dir per decade × source slice
    candidates.jsonl
    run_metadata.json
    run_report.md
  ads-1960s-spine/
  ads-1970s-spine/
  ...
  ads-2010s-spine/
  ads-2020s-spine/
  openalex-1990s-fill/
  crossref-1980s-fill/
  arxiv-modern-frontier/
```

Each run-dir holds the canonical three artifacts:

- `candidates.jsonl` — one normalised + annotated candidate per line.
- `run_metadata.json` — schema-versioned (`discovery-run-bundle/1.0`),
  resolved CLI args, query slate, backend list, dedupe / per-backend /
  per-query counts, novelty-join block, `candidate_counts_by_corpus_status`,
  `candidate_counts_by_prior_run`, `prior_runs.runs_scanned[]`, explicit
  `limits` paragraph. `git_commit` lets reviewers reproduce the run shape.
- `run_report.md` — Markdown summary mirroring the same counts;
  carries the verbatim *frontier sample* framing.

Cross-run dedupe is wired via `--prior-runs-root <runs-root>`:

```sh
python3 scripts/discover_heliophysics_literature.py \
    --live --enable-ads \
    --extra-query "Parker solar wind interplanetary 1958" \
    --max-results 50 --year-from 1958 --year-until 1969 \
    --run-dir queue/ads-1960s-spine \
    --prior-runs-root queue
```

(`--year-from` / `--year-until` are a **proposed** CLI knob, see §10;
the rest is already implemented.)

The current `--run-dir` is excluded from its own prior scan; prior
runs are read-only.

## 5. Full-text acquisition ladder (per-candidate, post-discovery)

The ladder is documented in
`~/.lingtai-tui/utilities/academic-research/reference/pipeline-obtain-pdf.md`
and entered through the host's `fetch_paper.py`. The discovery
pipeline never writes PDFs.

```
candidate (DOI | arXiv ID | ADS bibcode)
   │
   ▼
[F1] arXiv direct  ─ arXiv ID present?  → https://arxiv.org/pdf/{id}.pdf
   │
   ▼  (no arXiv hit)
[F2] Unpaywall ($LINGTAI_RESEARCH_EMAIL)  ─ DOI present + is_oa? → best_oa_location.pdf_url
   │
   ▼  (not OA)
[F3] Europe PMC  ─ heliospheric-radiation / space-biology?
   │
   ▼
[F4] CORE ($CORE_API_KEY recommended)
   │
   ▼
[F5] Publisher-page extraction (Nature / APS / AIP / IOP / Cambridge)
   │
   ▼
[F6] ADS-linked external archives / Zotero / journal page-scan archives
   │
   ▼
[F7] LibGen (opt-in; legal-status caveat)  ─ if reviewer approves
   │
   ▼
record `inaccessible_text` rejection per DISCOVERY_POLICY.md §4.2
```

Operational rules:

- **The ladder is invoked only on candidates the reviewer has chosen
  to draft.** A 1950-present sweep that emits 5 000 candidates does
  not imply 5 000 PDF downloads — the median candidate is queued for
  triage, not fetched.
- **`$LINGTAI_RESEARCH_EMAIL` must be a real address.** Unpaywall
  rejects placeholder emails with HTTP 422.
- **Pre-1985 papers frequently fail F2–F5.** F6 (manual archive
  trace) and F7 (LibGen, with the documented caveat) become
  load-bearing for that era. Document each non-OA acquisition in the
  draft's `provenance` block before flipping
  `provenance_checked: true`.
- **PDF storage is out-of-tree.** This bundle does not commit PDFs.
  Reviewers store fetched material under their host workspace's
  `papers/{slug}/` (the `academic-research` skill's default layout).

## 6. Decade × query partitioning

The query slate scales by **decade × theme**, not by raw query count.
Each (decade, theme) tuple is one run-dir; runs accumulate under a
shared `--prior-runs-root` so cross-decade dedupe is automatic.

### 6.1 Decade slices (8 buckets)

| Decade | Notes / era markers | Expected primary backend |
|--------|---------------------|--------------------------|
| 1950–1959 | Parker (1958), Chapman & Ferraro extensions, early IGY-era ionosphere / aurora work | **ADS** (D1) |
| 1960–1969 | Mariner-2 solar wind confirmation (1962), early in-situ; IMP / OGO; pre-DOI | **ADS** (D1) |
| 1970–1979 | Skylab corona, Helios-1/2, IMP-8, early STEREO-precursor concepts | **ADS** (D1) + Crossref (D3) for journal DOIs |
| 1980–1989 | Voyager outer-heliosphere, ISEE-3, SMM, early MHD models, *Solar Physics* growth | **ADS** (D1) + Crossref (D3) |
| 1990–1999 | Ulysses, SOHO launch, arXiv launches (1991) but rare for solar physics | **ADS** (D1) + OpenAlex (D2) + arXiv (D4) |
| 2000–2009 | RHESSI, STEREO, Hinode, Wind-CDAWeb maturity | OpenAlex + arXiv + ADS |
| 2010–2019 | SDO, IRIS, MMS, deep-learning explosion | OpenAlex + arXiv + ADS |
| 2020–present | PSP, Solar Orbiter, Aditya-L1, foundation-model era, ML/AI papers | OpenAlex + arXiv + ADS |

### 6.2 Theme slices (≥ 18 buckets; aligned with curated batch themes)

Themes mirror the existing 18 curated batches so the join surface is
not invented from scratch. Reuse the batch names from
`references/corpus_manifest_v2.json::entries[].batch`:

`batch_pfss_source_mapping`, `batch_psp_switchbacks_magnetic`,
`batch_solar_wind_segmentation_ml`,
`batch_sep_energetic_particles`,
`batch_turbulence_heating_apj`,
`batch_mission_instruments_data_products`,
`batch_heliophysics_software_infrastructure`,
`wave500_coronal_source_mapping_pfss_045`,
`wave500_inner_heliosphere_psp_solo_045`,
`wave500_sep_shocks_space_weather_045`,
`wave500_turbulence_intermit_heating_045`,
`wave500_sw_classification_ml_foundation_045`,
`wave500_instruments_data_software_045`,
`wave500_solar_corona_cme_flares_045`,
`wave500_waves_instabilities_reconnection_045`,
`wave500_agent_runtime_eval_design_045`,
`pilot_2026_and_runtime`,
plus a **pre-1990 era-bucket** for entries that pre-date the modern
batch themes (Parker 1958, Mariner-2 confirmation, early
Chapman-Ferraro work; eligible only for ADS-sourced runs).

The (decade × theme) cross is 8 × 18 = 144 cells. The pilot in §9
runs **3 cells**, not 144.

### 6.3 Query slate per cell

For each cell, the slate is:

- 1 theme-anchored ADS query (`q=title:"…" OR abstract:"…"
  year:YYYY-YYYY`),
- 1 OpenAlex query (`filter=publication_year:YYYY-YYYY` + theme
  keywords),
- 1 Crossref query for the DOI-registered tail
  (`filter=from-pub-date:YYYY-01-01,until-pub-date:YYYY-12-31`,
  `query=<theme keywords>`),
- 1 arXiv query (skipped automatically for pre-1991 cells; the
  current backend code path returns zero hits for those decades
  rather than aborting).

`--max-results` per backend stays bounded (default `50`; raise to
`200` only for the pre-1990 cells where ADS is the only source).
`--page-pause-seconds` stays ≥ 1.0 in live mode; ADS rate-limit
guidance in `api-nasa-ads.md` is "respectful" rather than
hard-quoted, so the polite-HTTP layer's existing backoff is the
contract.

## 7. Rate-limit & backoff discipline

The discovery script's existing polite-HTTP layer is the contract:

- Single-threaded; one in-flight request at a time.
- Descriptive `User-Agent`
  (`heliosi-discover/<version> (+repo URL)`) on every request.
- Bounded exponential backoff on HTTP 429 / 408 / 425 / 500 / 502 /
  503 / 504 and `URLError`. Default `--max-retries 3`,
  `--retry-base-seconds 1.5`. Wait before attempt `N` is
  `base * 2^(N-1)`.
- `--page-pause-seconds` ≥ 1.0 between successive backend fetches in
  live mode.
- Permanent failure surfaces as a structured `summary.errors[]` entry
  rather than a silent drop.

Per-backend tightening for the 1950-present scope:

| Backend | Default cadence | Notes |
|---------|-----------------|-------|
| **arXiv** | 1 req/s | The script has already observed 429s on this host; the existing backoff is the only mitigation. Do not increase concurrency. |
| **OpenAlex** | ≤ 10 req/s without `mailto`; higher with | Pass a `mailto=<real email>` query param to join OpenAlex's polite pool (proposed knob, see §10). |
| **Crossref** | ~10 req/s public; ~50 req/s polite pool | Same polite-pool mechanism — `User-Agent: heliosi-discover/<v> (mailto:<real email>)`. |
| **NASA ADS** | "respectful" | No hard-coded number from the public docs; the existing 1-req-at-a-time + 1 s pause is conservative. Token must be set or the script aborts. |

A 1950-present sweep that touches every (decade, theme) cell at
default `--max-results 50` is roughly `144 × 4 ≈ 576` requests
*per backend*. At 1 req/s with 1 s pause that is on the order of
~30 minutes per backend, end-to-end. The pilot in §9 sizes runs to
stay well below this.

## 8. Provenance & honesty boundaries

Carried verbatim from the existing artifacts so this plan cannot
silently widen the curated corpus's claim surface:

- **`new_candidate` ≠ verified absence.** From the discovery
  script's `run_metadata.json::limits`: "title+year fallback is
  sensitive to title-string differences; `new_candidate` means no
  manifest-key hit, not verified absence from all literature."
- **Frontier sample, not census.** Every run writes verbatim
  *"frontier seed-expansion sample; not a complete survey of the
  heliophysics literature"* into `run_metadata.json::framing`. A
  1950-present sweep does not change that — it widens the
  *sampling envelope* but does not claim exhaustive coverage.
- **`unsafe_or_fabricated_claim` ladder.** A 1950-present sweep
  surfaces many candidates the corpus has no Layer-3 adapter
  binding for (early Mariner / IMP / Helios data, hand-digitised
  plots). Reviewers MUST NOT promote drafts whose Layer-2 contract
  depends on an MCP that the consumer has not configured. See
  `DISCOVERY_POLICY.md` §6.3 and the `README.md` *Companion MCP
  adapters* section.
- **Author identity at scale.** Pre-1990 author records frequently
  drop given names or use initials. Importing those verbatim is
  fine; the curated entry's `authors_verified: false` flag (already
  enforced by the existing authorship audits) is the right signal
  until ORCID resolution exists for that era.
- **The 501-count invariant is a claim, not a knob.** Per
  `DISCOVERY_POLICY.md` §6.2: bumping the count in
  `scripts/validate.sh` requires a paired promotion that earns the
  extra entry. A 1950-present sweep does not, on its own, bump the
  invariant — only the per-paper promotion gate does.
- **ADS / Unpaywall / CORE credentials are environment-scoped.**
  This bundle never reads secrets from a file; it reads them from
  the environment (`ADS_API_TOKEN` / `NASA_ADS_TOKEN` / `ADS_TOKEN`,
  `LINGTAI_RESEARCH_EMAIL`, `CORE_API_KEY`). Run reports MUST NOT
  echo secret values; the existing `run_metadata.json` records the
  *names* of the resolved CLI knobs, not the resolved token values.
  A 1950-present sweep does not relax that policy.

## 9. Bounded pilot design (3 cells)

The pilot establishes that the new decade × theme axes behave
correctly **before** any larger sweep. It runs in `--dry-run` mode
first against a hand-curated multi-decade fixture, and only then in
`--live` mode against ADS for three (decade, theme) cells. Every
cell is < 50 candidates so total wall-time is small and the
rate-limit envelope is conservative.

### 9.1 Pre-conditions

- `tests/fixtures/discovery/sample_records.jsonl` extended with
  ~6 synthetic pre-1990 records (Parker-1958-style, Mariner-2-1962,
  Voyager-1980, etc.) so the dry-run mode exercises the
  pre-DOI / pre-arXiv code path. **This fixture extension is a
  separate, very small PR** — it is not part of this report.
- ADS token present in env (`ADS_API_TOKEN` / `NASA_ADS_TOKEN` /
  `ADS_TOKEN`). The pilot **MUST** abort if it is not.
- `LINGTAI_RESEARCH_EMAIL` set to a real address (not used by the
  discovery script today; required only for the F2 Unpaywall path
  of the acquisition ladder).
- A clean `queue/` directory under `/tmp` so the pilot never
  contaminates `references/corpus/` or the existing `reports/`.

### 9.2 Pilot cells (3)

| Cell | Decade | Theme | Backend slate | Expected scale |
|------|--------|-------|---------------|----------------|
| **P1** | 1958–1969 | era-bucket (Parker, Mariner-2, IMP) | ADS only | 30–50 candidates |
| **P2** | 1970–1989 | `batch_psp_switchbacks_magnetic` (heliospheric magnetic-field / IMF foundations) | ADS + Crossref | 30–50 candidates |
| **P3** | 2000–2024 | `wave500_sw_classification_ml_foundation_045` | OpenAlex + arXiv + ADS | 30–50 candidates |

P1 stress-tests the pre-DOI / pre-arXiv path. P2 stress-tests the
ADS-bibcode + Crossref interplay. P3 is a *no-regression* control
that overlaps with the existing modern slate; if P3 emits
substantially different candidate counts than today's default run,
something is wrong with the new decade knobs.

### 9.3 Pilot CLI shape (per cell)

```sh
# P1 — pre-DOI era, ADS spine.
python3 scripts/discover_heliophysics_literature.py \
    --live --enable-ads --no-openalex --no-arxiv \
    --extra-query 'title:"solar wind" year:1958-1969' \
    --extra-query 'title:"interplanetary magnetic field" year:1958-1969' \
    --max-results 50 \
    --run-dir /tmp/heliosi-pilot/P1-ads-1960s-era \
    --prior-runs-root /tmp/heliosi-pilot

# P2 — heliospheric magnetic field, ADS + Crossref.
python3 scripts/discover_heliophysics_literature.py \
    --live --enable-ads --enable-crossref --no-openalex --no-arxiv \
    --extra-query 'title:"heliospheric magnetic field" year:1970-1989' \
    --extra-query 'title:"interplanetary current sheet" year:1970-1989' \
    --max-results 50 \
    --run-dir /tmp/heliosi-pilot/P2-helio-bfield-1970s-80s \
    --prior-runs-root /tmp/heliosi-pilot

# P3 — modern ML/AI control; no new knobs, sanity check.
python3 scripts/discover_heliophysics_literature.py \
    --live --enable-ads \
    --extra-query 'solar wind classification machine learning' \
    --extra-query 'foundation model heliophysics' \
    --max-results 50 \
    --run-dir /tmp/heliosi-pilot/P3-sw-ml-2000s-2020s \
    --prior-runs-root /tmp/heliosi-pilot
```

(`--year-from` / `--year-until` would replace the inline `year:`
phrases once §10 lands; until then, embedding the year clause inside
the query string is the only no-knob path.)

### 9.4 Pilot exit criteria

The pilot is **successful** when *all* of the following hold:

1. All three runs complete without backend errors (or with errors
   surfaced cleanly in `summary.errors[]`).
2. Each `run_report.md` carries the verbatim
   *frontier sample / not a complete survey* framing.
3. `corpus_status` distributions are sane (P1 + P2: expect
   `new_candidate` ≫ `already_curated`; P3: expect some
   `already_curated` against the current 501).
4. Prior-run dedupe scan shows zero cross-cell collisions for P1+P2
   (different eras) and non-trivial overlap between P3 and a
   pre-existing modern-frontier run.
5. No candidate is silently dropped on a non-2xx response —
   permanent failures are recorded in `summary.errors[]`.

The pilot is **a failure** if any of the following holds:

- ADS abort fires under `--enable-ads` because the token was not
  set. (This is a *correct* abort, not a pilot pass.)
- A `corpus_status` field is missing from any emitted candidate.
- The total wall-time exceeds 30 minutes per cell.

### 9.5 What the pilot does NOT do

- Does not write under `references/corpus/`.
- Does not invoke the drafter
  (`scripts/draft_paper_skill_from_candidates.py`); that is a
  separate downstream step, gated by the promotion checklist.
- Does not fetch any PDFs. The acquisition ladder in §5 is invoked
  only on a per-paper basis, after the reviewer has selected
  candidates for promotion.
- Does not bump the 501-count invariant.

## 10. Small CLI extensions (proposed, NOT implemented here)

These are *strictly optional* knobs that the report-only increment
deliberately stops short of. Implementing them is a small follow-up
PR with paired tests:

1. **`--year-from YYYY` / `--year-until YYYY`** on
   `discover_heliophysics_literature.py`. Today, decade filtering
   happens inside the query string (e.g.
   `'title:"solar wind" year:1958-1969'`). A first-class CLI knob
   would translate to:
   - ADS: append `year:YYYY-YYYY` to `q`.
   - OpenAlex: append `filter=publication_year:YYYY-YYYY`.
   - Crossref: `filter=from-pub-date:YYYY-01-01,until-pub-date:YYYY-12-31`.
   - arXiv: no first-class year filter; honour the knob by
     post-filtering Atom entries on `year`.
   The knob would also write `year_from` / `year_until` into
   `run_metadata.json::cli_args` so an auditor can recover the
   decade slice from the bundle alone.
2. **`--mailto EMAIL`** to join the OpenAlex / Crossref polite pool.
   Today the script sends only its descriptive `User-Agent`; adding
   a `mailto=` query parameter to OpenAlex requests and a
   `(mailto:<email>)` segment to the Crossref `User-Agent` would
   raise polite-pool throughput without changing the dedupe contract.
   The knob would read `LINGTAI_RESEARCH_EMAIL` as a default to keep
   secrets in env.
3. **`--theme BATCH-SLUG`** to tag every emitted candidate with the
   curated batch theme the run is targeting. Today, theme is
   derivable only from the query slate; recording it explicitly in
   each candidate would make per-batch backfill audits cleaner.
4. **`--rejections-jsonl PATH`** to materialise the hand-written
   `<run-dir>/rejections.jsonl` that `DISCOVERY_POLICY.md` §4.1
   already references. The drafter would then mirror it under
   `<drafts-dir>/`. This closes the rejection-log automation gap.

Each knob keeps the run-bundle schema at `discovery-run-bundle/1.0`
unless it changes the candidate row shape; in that case the schema
bump is paired with a test that pins the new field.

**This report does not implement any of (1)–(4).** They are
recorded here so the next implementation increment has a concrete
target.

## 11. What this plan does *not* change

- The curated 501-entry corpus.
  `scripts/validate.sh`, `audit_*.py`, the per-batch counts, the
  Wu 2026 T1 reproduction, and the maturity-tier distribution are
  untouched.
- The promotion gate. Every transition into
  `references/corpus/` still requires every
  `promotion_gate` item flipped to `true` with prose evidence in
  the draft body.
- The 501-count invariant in `scripts/validate.sh`. It does **not**
  auto-bump as a function of how many candidates a sweep emits.
- The `xhelio-spice` / `xhelio-cdaweb` MCP boundary. A 1950-present
  sweep finds many candidates whose Layer-3 adapter would depend on
  data products this bundle does not run. Those drafts must
  *record the dependency*, not invent a fallback.
- The aggregator skill's `verification_status` line in `SKILL.md`
  / `README.md`. The corpus is still a *scaffold / triage
  substrate*, not a fully verified reproduction corpus.

## 12. Risk register

| Risk | Trigger | Mitigation |
|------|---------|-----------|
| ADS rate-limit ban on this host | Aggressive parallel runs without the polite layer | Single-threaded; existing exponential backoff; per-cell pilot before any larger sweep. |
| Token leakage in `run_metadata.json` | A future change starts echoing resolved tokens | `cli_args` records the *names* of `--enable-ads` etc., not the resolved token. Reviewers should add a CI check that asserts no token-shaped string survives in `run_metadata.json::cli_args`. |
| Title+year false-merge across pre-DOI papers with identical normalised titles | Older review articles with the same title across journals | Always require an ADS bibcode for pre-1985 candidates before flipping `bibliographic_identity_verified: true`. |
| Mass-draft of unverifiable candidates | Reviewer flips `promotion_gate` items without prose evidence | Treated as `unsafe_or_fabricated_claim` rejection (§4.2). The §3 gate is the audit trail. |
| Re-emission churn across runs | `--prior-runs-root` not set | Wire every sweep run with a shared `--prior-runs-root`. The script's existing scan already handles this. |
| Coverage over-claim ("we now cover 1950-present") | A future README sentence drops the *frontier sample* framing | `DISCOVERY_POLICY.md` §5.3 + `literature_discovery_pipeline.md` §2 + this report all carry the verbatim framing; coverage claims should be reviewed against all three. |

## 13. Concrete next actions

In recommended execution order. None of these is performed by this
report.

1. **Land a small fixture extension** — add ~6 pre-1990 synthetic
   records to `tests/fixtures/discovery/sample_records.jsonl` and an
   accompanying test in `tests/test_discover_heliophysics_literature.py`
   pinning their dedupe / classification behaviour. This is the
   smallest possible step that exercises the new sampling envelope
   in CI without touching the curated corpus.
2. **Implement `--year-from` / `--year-until`** on the discovery
   script (§10 item 1), with a paired test verifying that the
   year filter is correctly applied per backend (ADS / OpenAlex /
   Crossref / arXiv).
3. **Implement `--mailto`** (§10 item 2) and a default lookup
   against `$LINGTAI_RESEARCH_EMAIL`.
4. **Run the §9 pilot** — three cells, dry-run first, then live
   with ADS. Commit the `run_metadata.json` summaries (but not the
   `candidates.jsonl`; that is queue data, not bundle data) into
   `reports/` as a `pilot_run_summaries.md`.
5. **Triage the pilot output** through the existing drafter
   (`scripts/draft_paper_skill_from_candidates.py`) for the small
   number of candidates the reviewer chooses to promote. Promotion
   still flows through `DISCOVERY_POLICY.md` §3; this report does
   not loosen that.
6. **Decide whether to add a recurring sweep** (cron / agent
   schedule) only after the pilot has cleared §9.4 cleanly. A
   recurring sweep without observability / budget enforcement is
   explicitly out of scope until (1)–(5) ship.

Until step (6), the 1950-present scope expansion is **a plan and a
small pilot**, not a production sweep. That framing is the point.
