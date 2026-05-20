# Changelog

All notable changes to the `heliosi-501-corpus` Claude Code skill bundle are
recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
loosely, and the bundle version is tracked in `SKILL.md`'s frontmatter
(`version:` field). Note that `corpus_manifest_v2.json`'s `schema_version:
rollup-2.0` describes the **manifest data schema**, not the bundle release.

## [Unreleased]

Hygiene + critical/high-priority bug-fix batch. Targets the load-bearing
defects flagged in the public issue tracker (#1, #3, #4, #6, #10, #12, #17)
plus the docs/script UX, corpus-integrity, authorship-hygiene,
arXiv-provenance, layer-2-stub-audit, workflow-gating, authorship-parity,
research-generation-affordance, and layer-population-honesty batches that landed on top. Per-entry
surface changes are limited to the per-entry hygiene fixes called out in
each section below (minimal `SKILL.md` frontmatter on 222 entries, 5
metadata.yaml parse fixes, authorship-placeholder canonicalization on the
affected entries, `layer2_stub` flags on 55 entries, `authors_verified`
mirroring on the affected entries, and
`research_generation_affordances_present` flags on the affected entries);
the structural manifest invariants are unchanged (501 entries, 18 batches,
`totals.duplicate_slugs == {}`, `totals.*` counts unchanged).

### Issue #11/#23/#24/#25/#26/#27/#28/#29/#30/#32 — `search_corpus.py` UX hardening

- `scripts/search_corpus.py` — machine-readable `--json` output for
  `--query`, `--show`, `--batches`, and `--maturity` (the no-match `--query`
  path also emits JSON when `--json` is passed). Closes #32.
- `scripts/search_corpus.py` — `--in skill` now short-circuits at
  `--limit` (no longer scans all 501 SKILL.md files when only a handful
  of hits are needed) and prints a one-line stderr `scanning N SKILL.md
  files (limit=…)` progress notice so the otherwise-silent multi-second
  walk is observable. OSError on file open is surfaced with the offending
  slug, and a per-file warning fires when the UTF-8 decoder substitutes
  U+FFFD (since a replacement adjacent to a search token causes a false
  negative). Closes #11.
- `scripts/search_corpus.py` — `--show <SLUG>` is now case-insensitive
  (slugs are canonical lowercase, but pasted UPPERCASE / MixedCase input
  resolves to the same entry). Closes #23.
- `scripts/search_corpus.py` — `--show` partial-match fallback is
  boundary-aware: results are ranked prefix > dash-token > weak
  substring, so e.g. `--show wu-2026` lists `wu-2026-*` entries above
  `hwu-2026-*`. Weak (mid-token) matches are tagged `(weak match)` in
  the human output and `match_kind` in `--json`. Closes #24.
- `scripts/search_corpus.py` — `null` / missing / empty-string manifest
  fields render as `n/a` in `--show` output (rather than leaking the
  literal Python `None`). List/dict values render as compact JSON.
  Closes #25.
- `scripts/search_corpus.py` — `--batches` synthesizes a per-batch
  theme when `batches[i].theme` is null/blank by majority-voting the
  constituent entries' themes; synthesized themes are tagged ` (synth)`
  in the human output and `theme_synthesized: true` in `--json`.
  Closes #26.
- `scripts/search_corpus.py` — empty / whitespace-only `--query` is
  rejected by the argument parser *before* the manifest is loaded
  (previously the validation fired only after the 501-entry manifest
  read). Closes #27.
- `scripts/search_corpus.py` — pairing `--in` or `--limit` with
  `--batches` / `--maturity` / `--show` now emits a stderr warning that
  the flag is ignored (only `--query` consumes them), so callers don't
  think the output was silently filtered. Closes #28.
- `scripts/search_corpus.py` — non-integer / null manifest count fields
  no longer raise an unhandled `TypeError`; they coerce via a labelled
  warning and fall back to `0`. Closes #29.
- `scripts/search_corpus.py` — under `--in both`, manifest-matched
  entries are not re-read from disk: the per-row provenance tag is now
  exactly one of `[manifest]` or `[skill]` (the previous `[both]` tag
  is no longer produced, and the body-grep pass only walks entries that
  the manifest did not already match). Closes #30.
- `tests/test_search_corpus.py` — twenty additional unit tests covering
  every UX change above (JSON parseability, case-insensitive `--show`,
  partial-match ranking, null-field rendering, ignored-flag warnings,
  early empty-query validation, etc.). The suite count grows from
  23 → 43.

### Issue #2/#7 — corpus integrity validation

- 222 per-entry `SKILL.md` files were missing a YAML frontmatter block;
  all of them now carry a minimal `name:` (and where appropriate
  `description:` / `paper:`) frontmatter so consumers can introspect
  them programmatically. Five `metadata.yaml` files had parse failures
  (unquoted colons, unescaped `%`, stray BOM bytes); they parse cleanly
  under PyYAML now. Closes #2, #7.
- `scripts/validate.sh` — adds two new sections:
  - `S4b per-entry SKILL.md frontmatter coverage` asserts every one of
    the 501 per-entry `SKILL.md` files starts with `---` and has a
    non-empty `name:` field. Stdlib-only, so it runs without PyYAML.
  - `S4c per-entry metadata.yaml parses` parses every one of the 501
    `metadata.yaml` files under PyYAML when available, and `SKIP`s
    cleanly when PyYAML is missing (PyYAML is not a runtime
    dependency).
- `tests/test_corpus_integrity.py` — new unittest suite that mirrors
  S4b/S4c programmatically (skips when PyYAML is missing). CI installs
  PyYAML, so the parse check runs there unconditionally.
- `README.md`, `SKILL.md` — new prominent "Verification status (read
  first)" section calling out the T3/T4 dominance, the 449/501 entries
  carrying `TODO_verify_with_full_text` markers somewhere, and the
  single T1 reproduction. Also hardens the install snippet with
  `REPO_DIR="$(pwd)/heliosi-501-corpus-skill"` and a sanity check, so
  users who `cd` into the clone before symlinking don't end up with a
  doubled-up `heliosi-501-corpus-skill/heliosi-501-corpus-skill` path.

### Issue #55 — consumer-facing authorship-prose hygiene + topic-skill kind

- Two templated phrases inherited from the paper-to-skill factory
  surfaced in rendered `SKILL.md` bodies and looked like author lists
  to consuming agents:
  - `> Compiled from TODO verify (<X> authors) (YYYY), ...` (21
    occurrences under `wave500_sw_classification_ml_foundation_045/`)
  - `A paper-skill compiled from [<real names>, ] + co-authors (TODO
    verify full list) et al. YYYY (...)` (36 occurrences under
    `wave500_waves_instabilities_reconnection_045/`)
  Both are now rewritten to non-author wording that preserves the rest
  of the sentence (year, arXiv ID, journal placeholder, real co-author
  names if any). Where no real authors were named the prose now reads
  `compiled from the primary source (author list pending verification)`;
  where a real prefix existed (e.g. `T. A. Bowen,`) the rewrite
  preserves it and appends `, et al., YYYY (full author list pending
  verification)`. The honesty story is unchanged — `authors: []` and
  `authors_verified: false` continue to encode the unverified state in
  YAML.
- The same placeholder element (`"+ co-authors (TODO verify full list)"`)
  is stripped from per-batch `manifest.json` `authors[]` arrays
  (3 manifests, 37 entries). The stripping is line-based to keep the
  diff minimal and JSON-valid.
- `references/corpus/wave500_solar_corona_cme_flares_045/
  paper-open-flux-problem-in-situ-vs-pfss-discrepancy/` is now
  classified `kind: topic-skill` in its `metadata.yaml` and tagged in
  its `SKILL.md` as an intentional aggregate across multiple
  representative papers (Linker+ 2017; Wallace+ 2019; Riley+ 2019).
  This is the canonical exemplar for the topic-skill / paper-skill
  distinction called out in issue #55.
- `scripts/audit_authorship_prose.py` — new stdlib-only audit + fixer
  (`--apply` rewrites, `--strict` exits non-zero on remaining
  violations). Idempotent: re-running on a clean tree is a no-op.
- `scripts/validate.sh` — new section `S4g consumer-facing
  authorship-prose hygiene` invokes the audit script with `--strict`.
- `tests/test_authorship_prose.py` — new unittest suite covering both
  patterns in SKILL.md bodies, the manifest `authors[]` placeholder,
  the `kind` enum (`paper-skill | topic-skill | tool-skill`), and the
  topic-skill exemplar declaration. Closes #55.

### Issue #8 — authorship-field hygiene

- All `metadata.yaml` `first_author` / `authors[]` and all per-entry
  `SKILL.md` `paper.first_author` / `paper.authors[]` frontmatter
  values are guaranteed to contain **no** `TODO` / `TBD` placeholder
  strings. Where the source could not be verified, the value is `null`
  (scalar) or `[]` (list) and the entry carries an explicit
  `authors_verified: false` flag; partially-recovered lists carry
  `authors_complete: false`. The slug surname (e.g. `paper-mason-2026-…`)
  is **not** asserted as the verified first author. Closes #8.
- `scripts/validate.sh` — new section `S4d authorship-field hygiene`
  re-asserts the invariant: any `TODO` / `TBD` string under those four
  field paths fails the validator. Skips cleanly when PyYAML is missing.
- `tests/test_authorship_hygiene.py` — new unittest suite mirroring
  S4d, plus targeted regression checks for the canonical
  parenthetical-TODO patterns (`Mason, G. M. (TODO verify)`,
  `+ co-authors (TODO verify full list)`, etc.) that were the dominant
  failure mode pre-canonicalization.
- `README.md`, `SKILL.md` — new "Authorship fields are intentionally
  null / unverified" subsection documenting the policy and the
  `authors_verified` / `authors_complete` flags.

### Issue #9 — arXiv ID provenance hygiene

- `scripts/verify_arxiv_ids.py` — new opt-in verifier that fetches the
  arxiv.org abstract page for an entry's advertised arXiv ID, compares
  the HTML `<title>` against the entry's recorded title, and stamps a
  `provenance.id_verifications[]` record back into `metadata.yaml`
  (`status: arxiv-http-title-match` on success; `title-mismatch`,
  `http-non-200`, `network-error`, `no-title-tag`, `invalid-id-format`,
  or `no-recorded-title` otherwise). Not run in CI — verification is a
  curatorial step, not a smoke test. Closes #9 (provenance honesty
  axis; high arXiv numeric suffix alone is not evidence of
  hallucination).
- `scripts/validate.sh` — new section `S4e arXiv ID provenance hygiene`
  is structural-only (no live HTTP): it asserts every advertised
  `arxiv` / `paper.arxiv_id` value matches the canonical arXiv ID
  regex, every `provenance.id_verifications[]` record has a
  well-formed `url` / `arxiv_id` / `status` / `http_status`, and that
  `status: arxiv-http-title-match` requires `http_status: 200`,
  `title_match: true`, and a non-empty `fetched_title` (entries can't
  claim verification they don't have). 6 / 516 advertised IDs carry a
  verified provenance record at the current snapshot.
- `tests/test_arxiv_provenance.py` — new unittest suite mirroring S4e.

### Issue #14/#60 — Layer-2-stub audit + workflow gating (`--ready-for`, `--maturity-tier`)

- `scripts/search_corpus.py` — adds workflow-gating CLI:
  - `--ready-for {discovery,hypothesis,experiment,verify}` exposes the
    honest subset for each downstream use case. `discovery` = all 501
    entries; `hypothesis` = T1/T2 plus T3 entries with a populated
    Layer 4, excluding the 55 Layer-2 stubs; `experiment` = strictly
    T1+T2 minus Layer-2 stubs (23 entries); `verify` = T3/T4/T7 plus
    Layer-2 stubs plus `weak_flag_count > 0` plus DOI starting
    `TODO`/`TBD`, with T1 and T6 excluded (433 entries). Both filters
    apply to `--query` and can be used standalone.
  - `--maturity-tier T1|T2|…|T7` (repeatable) restricts to one or more
    derived maturity tiers. The tier is derived deterministically from
    `(quality, executable_status)` and the derived counts match
    `--maturity` exactly (T1=1, T2=22, T3=260, T4=164, T5=52, T6=1,
    T7=1, total=501).
  - Both filters also apply to `--batches` (counts are recomputed for
    the filtered subset and the header is annotated as `(filtered:
    …)`).
- `scripts/audit_layer2_stubs.py` — new audit/backfill tool that scans
  the two Layer-2-stub-prone batches
  (`wave500_inner_heliosphere_psp_solo_045`,
  `wave500_waves_instabilities_reconnection_045`) for entries whose
  Layer-2 contract is still a placeholder, and writes the
  `layer2_stub: true` / `layer2_status: <reason>` flag pair into the
  corresponding `metadata.yaml`. 55 entries are flagged at the current
  snapshot (45 + 10 across the two batches). The audit is idempotent.
  Closes #14.
- `scripts/audit_layer_schemas.py` — new audit that scans every
  per-entry `metadata.yaml` for the canonical four-layer schema
  (`layer1`, `layer2`, `layer3`, `layer4` keys), reports missing /
  extra keys per batch, and exits non-zero on schema drift. Run
  on-demand from CI.
- `tests/test_workflow_gating.py` — new unittest suite covering tier
  derivation parity with `--maturity` (per-tier counts and
  multi-tier union), the four `--ready-for` buckets (including the
  hypothesis ⊇ experiment invariant and Layer-2-stub exclusion), and
  the standalone vs `--query`-paired call shapes.
- `tests/test_layer2_stubs.py` — new unittest suite covering the
  `audit_layer2_stubs.py` placeholder-detection rule and the
  metadata splice (idempotent, no-overwrite on hand-curated `false`).
- `tests/test_layer_schemas.py` — new unittest suite covering
  `audit_layer_schemas.py`'s canonical-key set and per-batch
  enumeration.
- `README.md`, `SKILL.md` — new "Workflow eligibility filter
  (`--ready-for`, issue #60)" subsection with the four-row eligibility
  table, the explicit caveat that `discovery` is **not** a synonym for
  "workflow-ready", and the per-workflow gating language in the four
  numbered workflows (hypothesis, experiment, verify). The "Companion
  MCP adapters (external, not bundled)" section is also new and
  documents `xhelio-spice` + `xhelio-cdaweb` as separate-repo
  optional MCPs, replacing the older "the only LingTai domain MCP" line.

### Issue #62 — `authors_verified` parity between metadata.yaml and SKILL.md frontmatter

- Per-entry `SKILL.md` frontmatter `paper.authors_verified: false` is
  now kept in bidirectional parity with `metadata.yaml`'s top-level
  `authors_verified: false`. A consumer reading either surface alone
  sees the same disclosure. Current steady-state count is 173 / 501 on
  both sides (up from a pre-parity 59 / 173 split that risked a
  consumer reading only the SKILL.md surface silently citing
  unverified authors). Closes #62.
- `scripts/validate.sh` — new section `S4f authors_verified parity`
  fails the validator on any forward (`metadata` flagged but `SKILL`
  not) or reverse (`SKILL` flagged but `metadata` not) violation.
  Skips cleanly when PyYAML is missing.
- `tests/test_authorship_flag_parity.py` — new unittest suite covering
  the forward direction, the reverse direction, and a redundant
  count-equality guard.
- `README.md`, `SKILL.md` — updated to call out the bidirectional
  parity rule and the enforcement points (S4f + the new test).

### Issue #63 — `--ready-for hypothesis` no longer collapses to `experiment`

- `scripts/backfill_layer4_affordances.py` — new audit/backfill tool that
  scans every per-entry `SKILL.md` for a substantive Layer 4 /
  research-generation-affordances section and writes
  `research_generation_affordances_present: true` to the corresponding
  `metadata.yaml` *and* to `references/corpus_manifest_v2.json` (the
  manifest is what `scripts/search_corpus.py` actually reads for the
  gate). Heuristic is deliberately conservative: requires a Layer 4
  header (`Layer 4` or `Research-generation affordance[s]`), ≥ 300
  non-blank chars of body, ≥ 2 bullets, ≥ 250 chars after stripping
  empty-section sentinels (`No affordances identified yet`, `TBD`,
  `TODO`), and at least one of `Gap:` / `Hypothesis:` / `Tension:` /
  `Minimal_experiment` / `compose with` / `open question` markers. The
  metadata splice is file-level idempotent; use `--tier T3 --apply` for
  the issue-#63 scoped no-op rerun.
- 168 T3 entries now carry
  `research_generation_affordances_present: true` in both their
  `metadata.yaml` and `corpus_manifest_v2.json` records: 45 were already
  `true` in the manifest from a prior QA pass, and 123 are net-new T3
  manifest flips. Of those 168, exactly 123 are non-stub T3 entries that
  promote into `--ready-for hypothesis`; the other 45 are Layer-2 stubs
  and remain intentionally excluded from the hypothesis bucket. To
  prevent another split-brain surface, the 45 pre-existing non-T3
  manifest-true entries (T5 positioning skills) were also mirrored into
  their per-entry `metadata.yaml` without changing the manifest. The
  final true-set is therefore consistent: manifest true = metadata true
  = 213. Resulting `--ready-for` counts: hypothesis = 146 (was 23),
  experiment = 23 (unchanged), verify = 433 (unchanged), discovery = 501
  (unchanged). Hypothesis is now a strict superset of experiment, as the
  SKILL.md table always claimed.
- `tests/test_workflow_gating.py` — added three regression tests:
  `test_hypothesis_is_strict_superset_of_experiment` (asserts
  `len(hypothesis) - len(experiment)` equals the number of T3 manifest
  entries with `research_generation_affordances_present: true` and no
  Layer-2 stub flag — both directions, so a future drop in the field
  count surfaces here in CI), `test_hypothesis_contains_t3_entries`
  (the affirmative counterpart: the bucket must contain at least one
  T3 entry once the field is populated), and
  `test_research_generation_affordance_flags_match_manifest` (metadata
  true-set must equal manifest true-set, currently 213 == 213).
- `tests/test_layer4_backfill.py` — new unit-level suite covering the
  substantive-content heuristic (positive + negative cases), the
  metadata splice (append, idempotent, no-overwrite on hand-curated
  `false`, trailing-newline safety), and tier derivation parity with
  `search_corpus.py`.
- `README.md`, `SKILL.md` — `--ready-for` table updated: hypothesis row
  now shows 146 with a note that the count derives from the
  `backfill_layer4_affordances.py` heuristic, and a re-run command is
  documented in case the field gets reset on a fresh checkout.

### Issue #58 — four-layer model is now documented as maturity-dependent

- `SKILL.md`, `README.md`, and `references/corpus_index_v2.md` now describe
  the corpus as authored against an **up-to-four-layer** model: Layer 1 is
  universal, while Layers 2/3/4 are populated as an entry matures. Consumers
  are explicitly told that an entry-level `layers.<key>: false` boolean is
  authoritative and must not be cited as if that layer were authored.
- `references/corpus_qa_report_v2.md` adds a layer-population audit section:
  225 / 501 per-entry `SKILL.md` frontmatter blocks carry explicit `layers:`
  booleans, with 0 fully populated and 225 partially populated on that surface
  (90 at 1/4, 45 at 2/4, 90 at 3/4); `metadata.yaml` carries 90 explicit
  blocks, with 45 fully populated and 45 partially populated; the 90 entries
  where both surfaces carry the block have 0 parity mismatches.
- `references/corpus_manifest_v2.json` refreshes
  `four_layer_model.layer_population_across_501` from stale 45/0/0/0 values
  to the live SKILL.md-frontmatter counts: `scientific_invariant=225`,
  `executable_protocol=90`, `adapter_binding_examples=0`,
  `research_generation_affordance=135`.
- `scripts/audit_layer_population.py` and `tests/test_layer_population.py`
  provide the reproducible audit (`--json`, `--strict`) and pin the doc ↔
  corpus consistency checks. Closes #58.

### Wave500 solar-corona / CME / flares batch 1 — internalization of 4 high-debt entries (2026-05-19)

Drains content debt on four entries under
`references/corpus/wave500_solar_corona_cme_flares_045/` by internalizing
verified bibliographic anchors, narrow-form scientific claims,
executable-protocol contracts, validation targets, and failure modes
sourced from arXiv-confirmed primary papers. Pattern is the same as the
two prior internalization waves (turbulence / ML-foundation /
segmentation-ml): structural manifest invariants are unchanged
(501 entries, 18 batches, `totals.duplicate_slugs == {}`).

- `paper-so-phi-hrt-vector-magnetogram-radial-distance` — anchored to
  **Solanki, del Toro Iniesta, Woch, Gandorfer, Hirzberger, et al.
  (2020)**, "The Polarimetric and Helioseismic Imager on Solar Orbiter",
  *A&A* 642, A11, doi:10.1051/0004-6361/201935325, arXiv:1903.11061
  (CrossRef-confirmed, 144 co-authors). The per-encounter Sinjan+
  stray-light line referenced in earlier scaffolding is preserved as
  TODO_verify (no specific arXiv/DOI anchored at this pass). Score
  48.20 → 74.30.
- `paper-coronal-plume-substructure-eui-high-cadence` — anchored to
  **Uritsky, DeForest, Karpen, DeVore, Kumar, Raouafi, Wyper (2021)**,
  "Plumelets: Dynamic Filamentary Structures in Solar Coronal Plumes",
  *ApJ* 907, 1, doi:10.3847/1538-4357/abd186, arXiv:2012.05728. The
  companion driver-side paper Kumar et al. 2022 (arXiv:2204.13871) is
  recorded in `supplementary_verifications` as an explicit
  driver-degeneracy alternative to the p-mode picture. Score
  49.04 → 81.04.
- `paper-gong-network-synoptic-magnetogram-product` — anchored to
  **Harvey, Hill, Hubbard, Kennedy, Leibacher, et al. (1996)**, "The
  Global Oscillation Network Group (GONG) Project", *Science* 272,
  1284–1286, doi:10.1126/science.272.5266.1284 (CrossRef-confirmed,
  17 co-authors). The downstream NSO ISP synoptic-magnetogram
  calibration line (Petrie+ 2014, Riley+ 2014, Bertello+ 2014) is
  acknowledged and explicitly tracked as TODO_verify for follow-on
  anchoring. Score 50.15 → 64.60 (limited by no-arXiv ceiling).
- `paper-eui-fsi-hri-coronal-bright-points-statistics` — anchored to
  **Berghmans, Auchère, Long, Soubrié, Mierla, et al. (2021)**, "Extreme
  UV quiet Sun brightenings observed by Solar Orbiter/EUI", *A&A* 656,
  L4, doi:10.1051/0004-6361/202140380, arXiv:2104.03382. Companion
  papers Narang+ 2025 (arXiv:2505.03656) and Huang+ 2023
  (arXiv:2303.15979) are recorded under `supplementary_verifications`
  as population-refinement and EUI+SPICE spectroscopic follow-ons.
  Score 62.18 → 76.70.

Additional integration changes:

- `tests/test_layer_schemas.py` — `EXPECTED_BATCH_FAMILIES` entry for
  `wave500_solar_corona_cme_flares_045` updated to hybrid
  `{prose_pfss_layered: 41, numbered_executable_workflow_v1: 4}` to
  match the post-internalization rendering distribution (same pattern
  the turbulence-batch internalization established).
- `tests/test_title_unicode.py` — headline-count expectations updated
  from 96 → 98 entries with non-ASCII titles (two additional U+2014 EM
  DASH manifest titles after journal/anchor promotion).
- `references/corpus_qa_report_v2.md` §10 — headline counts updated to
  match: 98 / 501 entries, EM DASH count 31 → 34, EN DASH 11 → 10.
- `references/corpus_manifest_v2.json` — `title`, `first_author`,
  `year`, `venue`, `doi`, `arxiv`, and `research_generation_affordances_*`
  fields updated for the four internalized entries.
- Per-batch corona/CME mean score 57.16 → 59.09 (+1.93).

### Wave500 ML-foundation batch 1 — Layer-1 internalization for 3 high-debt entries (2026-05-19)

Drains content debt on three entries under
`references/corpus/wave500_sw_classification_ml_foundation_045/` by
internalizing verified Layer-1 (scientific invariant) content from
publicly-available abstracts and bibliographic anchors. No new
verification machinery; per-entry SKILL.md bodies replace factory
placeholder prose with sourced narrow-form claims, abstract executable
protocols, and failure-mode skill memory. The structural manifest
invariants are unchanged (501 entries, 18 batches,
`totals.duplicate_slugs == {}`).

- `paper-xu-borovsky-categorization-extension-1au` — anchored to the
  verified parent scheme **Xu, F. & Borovsky, J. E. (2015)**, "A new
  four-plasma categorization scheme for the solar wind", *JGR Space
  Physics*, 120(1):70-100, doi:10.1002/2014JA020412 (ADS:
  2015JGRA..120...70X). The "extension to 1 au" tail of the slug name
  is preserved for stable cross-references; the bibliographic block now
  reflects the parent scheme and the L4 affordances list enumerates
  candidate extension papers (no fabricated extension citation).
- `paper-li-2020-solar-wind-supervised-extension-multi-mission` —
  anchored to the verified primary paper **Li, H., Wang, C., Tu, C.,
  Xu, F. (2020)**, "Machine Learning Approach for Solar Wind
  Categorization", *Earth and Space Science*, 7(5):e2019EA000997,
  doi:10.1029/2019EA000997, arXiv:1811.02323 (ADS:
  2020E&SS....700997L). The slug's "multi-mission" framing is preserved
  for stable cross-references but moved from a paper-side claim to a
  Layer-4 research target (the primary paper benchmarks 10 supervised
  models on Xu-Borovsky labels with ACE-derived 1-au hourly data, not
  cross-mission Wind+ACE+STEREO). Headline KNN overall accuracy = 92.8%
  is anchored.
- `paper-rudisser-2024-icme-unet-realtime-deployment` — anchored to
  the verified primary paper **Rüdisser, H. T., Nguyen, G.,
  Le Louëdec, J., Davies, E. E., Möstl, C. (2026)**, "ARCANE — Early
  Detection of Interplanetary Coronal Mass Ejections", *Space Weather*,
  24:e2025SW004537, doi:10.1029/2025SW004537, arXiv:2505.09365. The
  slug encodes year `2024` (factory-generated successor-lineage stub);
  the verified primary source is the 2026 journal article (2025
  preprint). The slug is added to
  `tests/test_corpus_hygiene_56_57.py:KNOWN_SLUG_YEAR_MISMATCHES` with
  justification. Slug's "U-Net" tag is the broader family label; the
  verified architecture is ResUNet++. Headline F1 = 0.37 and average
  detection-delay-fraction = 24.5% of event duration are anchored.

Out-of-scope findings (NOT modified in this batch; documented for a
future pass):

- `paper-bloch-2022-bayesian-nn-solar-wind-classification` — no
  Bloch-authored Bayesian-NN solar-wind classification paper located;
  the nearest verified match is **Narock, Pal, Arsham, Narock,
  Nieves-Chinchilla (2024)**, "Classifying Different Types of
  Solar-Wind Plasma with Uncertainty Estimations Using Machine
  Learning" (arXiv:2409.09230, Solar Physics 2024). Author attribution
  is a factory hallucination; out-of-scope to silently rewire.
- `paper-camporeale-2017-knn-supervised-comparison-ten-models` and
  `paper-camporeale-2018-knn-solar-wind-classification-validation` —
  both carry arXiv ID `1811.02323` and list `E. Camporeale` as
  first_author, but arXiv:1811.02323 is the Li-Wang-Tu-Xu (2020)
  paper, not a Camporeale paper. Author attribution is a factory
  misattribution; out-of-scope to silently rewire (would risk
  double-binding the Li 2020 paper across slugs without an
  audit-log entry).
- `paper-trotta-2025-shock-detection-multispacecraft-ml` — Trotta et
  al. (2025) "An Overview of Solar Orbiter Observations of
  Interplanetary Shocks in Solar Cycle 25" (ApJS) exists and matches
  the lineage, but explicitly uses *traditional shock identification
  methodology, not machine learning*. The slug's "ML-assisted"
  framing does not match the parent paper; out-of-scope to rebind.

### Issue #59 — non-ASCII title characters are intentional scientific typography

- `scripts/audit_title_unicode.py` — stdlib + PyYAML audit that scans
  manifest `entries[].title` and per-entry `metadata.yaml` `title:` for
  non-ASCII code points, classifies them against a narrow allowlist
  (LATIN with diacritics for "Alfvénic" / "Ångström" / author names,
  EM/EN dash, Greek α/β/δ used as physics parameters, °, ×, and U+0298
  ISʘIS), and flags suspicious code points (U+FFFD, C0/C1 controls,
  zero-width / bidi controls, surrogates) plus NFC drift and
  manifest ↔ metadata.yaml unicode-set divergence. `--json` and
  `--strict` modes match the conventions used by the other
  `scripts/audit_*.py` helpers.
- `references/corpus_qa_report_v2.md` adds §10 "Title-unicode audit
  (issue #59)" publishing the live counts: 95 / 501 manifest entries
  carry non-ASCII titles, drawn from exactly 11 unique code points all
  on the expected allowlist (U+00B0, U+00C5, U+00D7, U+00E4, U+00E9,
  U+0298, U+03B1, U+03B2, U+03B4, U+2013, U+2014); 0 suspicious chars;
  0 NFC drift; 0 unicode-set divergences between manifest and
  metadata.yaml; 3 unrelated content-length divergences are flagged as
  out-of-scope. The previous §10 "Acceptance summary" is renumbered to
  §11 and gains a new row pinning the issue-#59 audit.
- `tests/test_title_unicode.py` runs the script in `--json --strict`
  mode and pins both the audit-output invariants (no suspicious /
  unexpected / NFC-drifted / unicode-set-divergent titles) and the
  doc ↔ corpus consistency (`corpus_qa_report_v2.md` §10 cites the
  live 95-entry / 11-unique-code-point headline). Closes #59.

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
- The per-entry corpus content remains a snapshot of the upstream
  generator output: the four-layer prose, the Layer-1 / Layer-2 claim
  bodies, the `quality` / `executable_status` labels, and the slug
  assignments are byte-identical to the 0.1.0 snapshot. The only
  per-entry edits in this batch are the structural hygiene fixes
  documented above (frontmatter coverage, YAML parse fixes,
  authorship-placeholder canonicalization, `layer2_stub` flag,
  `authors_verified` parity mirror, and
  `research_generation_affordances_present` flag).
- The v2 index roll-up (`corpus_index_v2.md`) and manifest `totals.*` block
  remain unchanged by the title-unicode audit; `corpus_qa_report_v2.md` is
  changed only to add the issue-#59 audit section and renumber the acceptance
  summary.
- Manifest `totals.*` block — every count and slug-uniqueness assertion is
  byte-identical to the 0.1.0 snapshot.
- All security-labeled issues (#5 manifest-path traversal, #31 external
  link / supply-chain hardening, #36 broader `allowed-tools: Bash` scope)
  are intentionally **out of scope** for this batch and remain open.
  They need a security-focused review.
- The remaining non-security docs / corpus-curation issues (#18–#22,
  #33, #34, #39, #41, #44, #55–#57, #61) are NOT addressed here —
  they require curatorial or roadmap decisions about the corpus itself
  (unifying per-batch manifest schemas, populating Layer-2 contracts,
  reconciling `quality` vs `quality_level`, deciding the next roadmap,
  etc.) rather than the mechanical / audit hygiene this batch covers.
  They remain open.

## [0.1.0] — 2026-05-18

Initial public snapshot of the `heliosi-501-corpus` aggregator skill bundle:
501 paper-skill directories across 18 batches, four-layer authoring model,
stdlib search helper, validation report. See `VALIDATION.md` and
`PUBLICATION_CHECKLIST.md` for the full integrity checks captured at that
snapshot.
