# Changelog

All notable changes to the `heliosi-501-corpus` Claude Code skill bundle are
recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
loosely, and the bundle version is tracked in `SKILL.md`'s frontmatter
(`version:` field). Note that `corpus_manifest_v2.json`'s `schema_version:
rollup-2.0` describes the **manifest data schema**, not the bundle release.

## [Unreleased]

Hygiene + critical/high-priority bug-fix batch. Targets the load-bearing
defects flagged in the public issue tracker (#1, #3, #4, #6, #10, #12, #17)
plus the previously-batched docs/script UX issues. No corpus content
(per-entry `SKILL.md` / `metadata.yaml`) changes; no `totals.*` change in
the manifest. Slug uniqueness and structural counts are unchanged
(501 entries, 18 batches, `totals.duplicate_slugs == {}`).

### Added
- `LICENSE` (MIT for the bundle code; explanatory note that the per-entry
  corpus content paraphrases third-party papers whose copyright remains
  with the original authors). Closes #1.
- `CHANGELOG.md` (this file). Closes #35.
- `version: 0.1.0` field in `SKILL.md` frontmatter so consumers updating
  via `git pull` can see when the bundle moves. Closes #35.
- `scripts/validate.sh` — single-entry reproducible validation that
  re-runs every structural check claimed in `VALIDATION.md` §1–§4 and
  exits non-zero on the first failure. Closes #38.
- `tests/test_search_corpus.py` — stdlib `unittest` suite (also runs
  under pytest) covering the four documented smoke commands plus
  regression tests for every script-level issue fixed in this batch
  (`--limit` validation, no-match exit code, multi-word tokenization,
  accent folding, `--version`, empty-input handling). Partial fix for
  #17 (the broader "every behavior change has a test" goal).
- `.github/workflows/ci.yml` — GitHub Actions workflow that runs
  `bash scripts/validate.sh` and `python3 -m unittest discover -s tests`
  on Python 3.10 / 3.11 / 3.12. Partial fix for #17.
- `scripts/search_corpus.py`: `--version` flag, examples in `--help`
  epilog, explicit empty-slug error for `--show ""`, conditional
  `(showing M)` line (only when `M < total`), per-row provenance tags
  (`[manifest]` / `[skill]` / `[both]`) under `--in both`, always-on
  accent-folded query matching, duplicate-slug warning + `---` separator
  for multi-`--show` output, uniform column alignment in `--show`.
  Closes #46, #47, #48, #49, #51, #52, #53.

### Changed
- `scripts/search_corpus.py`: `--query` now AND-matches whitespace-separated
  tokens against the haystack (substring per token, accent-folded). Single
  tokens behave as before; multi-word queries that previously returned
  zero hits because the haystack did not contain the concatenated phrase
  now return the expected per-token intersection. Closes #12.
- `scripts/search_corpus.py`: `--query` exits with status `1` on no matches
  (matches `grep` / `git grep` and the existing `cmd_show` no-match path),
  so CI / shell pipelines can detect zero hits. Closes #10.
- `scripts/search_corpus.py`: `--limit` is validated at parse time and
  rejects values `<= 0` (previously `--limit 0` silently disabled the
  cap via Python truthiness and `--limit -N` silently dropped the last
  `N` results via slice semantics). Closes #3, #4.
- `references/corpus_manifest_v2.json`: `corpus_root` and each of the 18
  `batches[].path` fields rewritten from
  `sioulas-reproduction/results/paper_skill_corpus/<batch>/` (the
  upstream generator-side directory which does not exist in this
  bundle) to `references/corpus/<batch>/`. Entry-level `path` fields
  (which `search_corpus.py` actually consumes) were already correct and
  are unchanged. All `totals.*`, slug uniqueness, and per-entry data are
  unchanged. Closes #6.
- `SKILL.md`: `--query` flag table now lists the actual searched fields
  (`slug, title, batch, theme, first_author, year, venue, source_type,
  quality, executable_status, arxiv, doi`) instead of the legacy
  `keywords` placeholder; explicit note that `--query` is literal
  substring (regex metacharacters are escaped) and that whitespace
  separates AND-matched tokens; `--batches` description now mentions the
  third `theme` column; the `duplicate_slugs == {}` assertion now points
  to `totals.duplicate_slugs` (the actual manifest path).
  Closes #37, #42, #43, #54.
- `README.md`: smoke-test section notes that the four `search_corpus.py`
  commands work from the cloned repo root before installation because the
  helper resolves paths relative to itself. References
  `bash scripts/validate.sh`. The `duplicate_slugs == {}` claim now
  points to `totals.duplicate_slugs`. Closes #50.
- `PUBLICATION_CHECKLIST.md` §5: added a one-line header clarifying that
  the empty `[ ]` boxes are the template to re-tick at each new tag and
  that §1 is the record for the current snapshot. Section now references
  `scripts/validate.sh` and `CHANGELOG.md`. Closes #45.
- `.gitignore`: defense-in-depth additions (`.remember/`, `.claude/`,
  `.env`, `.env.*`, macOS AppleDouble `._*`, and more archive types
  `*.bz2`, `*.xz`, `*.rar`, `*.dmg`). Closes #40.

### Unchanged (intentionally)
- All 501 per-entry `SKILL.md` / `metadata.yaml` files. They are a
  snapshot of the upstream corpus and remain read-only here.
- The v2 roll-up Markdown files (`corpus_index_v2.md`,
  `corpus_qa_report_v2.md`). Counts and tier distributions are unchanged.
- Manifest `totals.*` block — every count and slug-uniqueness assertion is
  byte-identical to the 0.1.0 snapshot.
- All security-labeled issues (#5 manifest-path traversal, #36 broader
  `allowed-tools: Bash` scope) are intentionally **out of scope** for
  this batch and remain open. They need a security-focused review.
- The structural-content issues (#2, #7, #8, #9, #13, #14, #15, #16, #18-
  #34, #39, #41, #44, #55-#60) are NOT addressed here — they require
  curatorial decisions about the corpus itself (verifying DOIs / arxiv
  IDs, unifying per-batch manifest schemas, populating Layer-2 contracts,
  reconciling `quality` vs `quality_level`, etc.) rather than mechanical
  hygiene. They remain open.

## [0.1.0] — 2026-05-18

Initial public snapshot of the `heliosi-501-corpus` aggregator skill bundle:
501 paper-skill directories across 18 batches, four-layer authoring model,
stdlib search helper, validation report. See `VALIDATION.md` and
`PUBLICATION_CHECKLIST.md` for the full integrity checks captured at that
snapshot.
