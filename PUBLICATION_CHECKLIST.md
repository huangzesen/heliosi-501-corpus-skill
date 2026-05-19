# PUBLICATION_CHECKLIST.md

Record of the deterministic checks run when preparing this repository for
public GitHub release, and the remaining caveats consumers should know
about. All checks pass at the snapshot date below; rerun them before any
subsequent release.

**Snapshot:** 2026-05-18
**Repository root:** `heliosi-501-corpus-skill/`

## 1. Structural checks (all expected to pass)

Run from the repository root.

| Check | Command | Expected | Status |
|---|---|---:|:---:|
| Per-entry `SKILL.md` files (aggregator excluded) | `find references/corpus -mindepth 2 -maxdepth 3 -name 'SKILL.md' \| wc -l` | 501 | ✓ |
| Per-entry `metadata.yaml` files | `find references/corpus -name 'metadata.yaml' \| wc -l` | 501 | ✓ |
| Batch directories under `references/corpus/` | `ls -d references/corpus/*/ \| wc -l` | 18 | ✓ |
| Manifest parses + cross-counts match + no duplicate slugs | see below | OK | ✓ |
| Helper script `--batches` total | `python3 scripts/search_corpus.py --batches` | total skills: 501 | ✓ |
| Helper script `--maturity` total | `python3 scripts/search_corpus.py --maturity` | TOTAL 501 | ✓ |

Manifest one-liner (must print `OK ...` with no assertion error):

```bash
python3 -c "import json; m=json.load(open('references/corpus_manifest_v2.json')); t=m['totals']; assert t['skills_in_manifests']==len(m['entries'])==501; assert t['batches']==len(m['batches'])==18; assert not t['duplicate_slugs']; print('OK', t)"
```

Captured output at snapshot:

```
OK {'batches': 18, 'skills_in_manifests': 501, 'fs_skill_dirs': 501,
    'fs_SKILL_md_files': 501, 'fs_metadata_yaml_files': 501,
    'unique_slugs': 501, 'duplicate_slugs': {}, 'all_counts_match': True,
    'baseline_skill_count': 96, 'wave500_skill_count': 405}
```

## 2. Public-safety scrub (all expected to find zero hits)

The following classes of strings were stripped from the public copy by a
one-shot scrubber before this checklist was written. They must continue to
return **zero hits** in every release.

| Class of forbidden string | Where it came from | Replacement strategy |
|---|---|---|
| Absolute local user paths under `/Users/…` | README install snippets | Repository-root-relative paths or `<home>` placeholder |
| Internal agent-id generator labels (`manual:…`, `…-1 wave500 batch generator`, etc.) | `generated_by` fields in per-entry `metadata.yaml`, batch `index.md`, and `manifest.json` files | Replaced with neutral `HelioSI paper-to-skill factory` wording |
| Project-PI personal name | Authorial notes inside a handful of pilot/wave500 SKILL.md bodies and a few index files | Replaced with neutral `HelioSI PI` / `HelioSI project framing` |
| Messenger / chat-platform identifiers (third-party messenger names, conversation IDs, numeric thread IDs) | Not present in this corpus | n/a — verified absent |

Recommended scan: re-derive the literal patterns from the four classes
above and run them through `grep -Ril` from the repository root. Every
pattern must return zero files. This checklist intentionally avoids
reproducing the literal patterns verbatim so the file itself stays clean
under any future literal-string sweep.

## 3. Files that were hand-rewritten (vs. pattern-scrubbed)

These files were authored fresh for the public copy and are **not** byte-for-byte
identical to their internal-bundle predecessors:

- `README.md` — replaced internal install paths with `git clone` instructions
  and removed PI-personal references.
- `VALIDATION.md` — corrected the bundle-root path to a repository-relative
  one and removed PI-personal sign-off line.
- `PUBLICATION_CHECKLIST.md` — this file (new).
- `.gitignore` — new.

All other files (the aggregator `SKILL.md`, the v2 roll-ups, the per-entry
`SKILL.md` / `metadata.yaml` files, the helper script) were either left
unchanged or only had pattern-level scrubs applied (`manual:…` →
`HelioSI paper-to-skill factory`, PI name → `HelioSI PI`).

## 4. Remaining caveats consumers should know

1. **Most entries are not full-text verified.** 260 of 501 are tier T3
   (`paper-grounded-pending-full-text`); 164 are T4 (`stub_or_scaffold`).
   Only the Wu 2026 PFSS entry has a documented local numerical reproduction
   (and the reproduction code itself is not shipped here).
2. **Layer-3 example adapter names are not promises.** Any specific MCP /
   Python package / dataset loader mentioned inside a per-entry `SKILL.md` is
   an *example* binding. Consumers must wire their own adapters.
3. **DOIs / arXiv IDs / ADS bibcodes marked `TODO_verify_with_full_text` are
   not verified.** Treat them as candidate identifiers, not citations.
4. **The 45 `wave500_agent_runtime_eval_design_045` entries are
   design-pattern transplants**, not heliophysics-executable science. Do not
   present them as physics results.
5. **The research-generation map is corpus-internal seed material**, not an
   externally validated research agenda.
6. **Per-entry files should be treated as read-only.** Edits should happen
   upstream in the source corpus and be re-snapshotted; in-place edits here
   will diverge from the manifest's roll-up totals.

## 5. Pre-release checklist (run before any new tag)

> The `[ ]` boxes below are intentionally blank — this section is the
> **template to re-tick at each new tag**. The current snapshot's record
> lives in §1 above (where the boxes are `✓`). An empty box here means
> "not yet re-verified for the *next* release," **not** "the current
> snapshot is unchecked."

- [ ] Re-run all six structural checks in §1; all must pass. The single
      entry point is `bash scripts/validate.sh` (added in 0.2.0; see
      `CHANGELOG.md`); it executes each check and exits non-zero on the
      first failure.
- [ ] Re-run the forbidden-string scan in §2; all must return zero hits.
- [ ] Diff `README.md`, `VALIDATION.md`, `PUBLICATION_CHECKLIST.md`,
      `.gitignore`, `CHANGELOG.md` for anything that re-introduces local
      paths or PI-personal references.
- [ ] Confirm the helper script still runs stdlib-only on the target
      Python 3 version.
- [ ] Confirm `SKILL.md` frontmatter `name:` field still equals
      `heliosi-501-corpus`, and that the `version:` field has been bumped
      consistently with `CHANGELOG.md`.
- [ ] Update `CHANGELOG.md` — move `[Unreleased]` entries under the new
      tag heading and create a fresh `[Unreleased]` section.
- [ ] Run the test suite (`python3 -m unittest discover -s tests` or
      `python3 -m pytest tests/`); all must pass on the target Python 3
      versions. The GitHub Actions workflow at `.github/workflows/ci.yml`
      runs the same suite on every push / PR.

## 6. Licensing

- The repository includes a top-level `LICENSE` file. The MIT license
  covers the bundle code (helper scripts, validation scripts, aggregator
  `SKILL.md`, roll-up files, CI workflow). The per-entry `SKILL.md` /
  `metadata.yaml` files summarize third-party heliophysics papers; the
  underlying papers remain under their original authors' / publishers'
  copyright. When reproducing scientific claims, cite the **original
  papers** (via the DOI / arXiv / ADS identifiers in each entry's
  metadata), not this corpus.
- Pre-release: confirm the `LICENSE` file is still present and has not
  been altered without an accompanying `CHANGELOG.md` entry.
