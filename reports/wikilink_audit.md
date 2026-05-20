# Skill-graph wikilink audit

**Status:** first increment (informational; not a CI-blocker).
**Owner:** HelioSI corpus authors.
**Entry point:** [`scripts/audit_wikilinks.py`](../scripts/audit_wikilinks.py).
**Companion tests:** [`tests/test_audit_wikilinks.py`](../tests/test_audit_wikilinks.py).
**Wired into:** `scripts/validate.sh` section **S6 (informational)**.

---

## 1. Why this exists

Most cross-references between paper-skills live as wiki-style links in
the prose: a `[[paper-foo-2025-bar]]` token inside the *Layer 4* and
*Skill graph → depends_on* sections of each per-entry `SKILL.md`. Until
this audit, nothing checked that those targets actually resolve to a
canonical slug in `references/corpus_manifest_v2.json`. The result was a
graph that looked dense in the prose but had no machine-verifiable
edges: typos, renamed slugs, and `paper-` prefix drift all survived
review.

The mandate now is to grow HelioSI into a substrate for fully automated
heliophysics research, not a hand-curated 501-entry corpus. A
substrate-level system has to be able to reason over its own skill
graph; that requires a graph whose edges are verifiable, not just
suggestive. This audit is the first concrete step toward that.

## 2. What the audit does

For every per-entry `SKILL.md` under `references/corpus/`, the audit:

1. extracts every `[[target]]` and `[[target|label]]` wikilink, recording
   the file, the 1-based line number, and whether the wikilink sits
   inside a single-line backtick `` `...` `` code span (which usually
   marks it as a placeholder example, not a real cross-reference);
2. resolves each unique target against the canonical slug list from
   `references/corpus_manifest_v2.json`;
3. counts how many entries carry an explicit
   `## Skill graph → depends_on` section in their prose (the current
   convention for declaring intra-corpus edges);
4. for every unresolved target, lists the referring files + lines and
   the most plausible mechanical fixes:
   - `paper-` prefix add / strip (a wikilink wrote `paper-foo` but the
     manifest has the bare `foo`, or vice-versa);
   - normalized-slug match (same alphanumeric letters in the same
     order, e.g. `[[Paper_Foo_Bar]]` ⟶ `paper-foo-bar`).

The audit never invents a slug: every suggestion is validated against
the manifest before it is reported.

## 3. CLI surface

```
python3 scripts/audit_wikilinks.py                 # human-readable
python3 scripts/audit_wikilinks.py --json          # JSON to stdout
python3 scripts/audit_wikilinks.py \
    --json --output reports/wikilink_audit.json    # file output
python3 scripts/audit_wikilinks.py --strict        # exit 1 on unresolved
python3 scripts/audit_wikilinks.py \
    --manifest references/corpus_manifest_v2.json \
    --corpus references/corpus
```

Default behaviour is **read-only and exit 0** even when unresolved
links exist. `--strict` is provided for future graph-hardening work but
is intentionally **not** wired into `scripts/validate.sh` yet — see §5.

The JSON payload carries `schema_version: "wikilink-audit-1"` and the
top-level keys `corpus_root`, `manifest_path`, `totals`, `unresolved`,
`depends_on_coverage`. The schema is stable enough to be consumed by a
future graph-builder script.

## 4. Current state (informational headline)

The audit reports the following on the live 501-entry corpus (the
numbers below are the snapshot at audit-introduction time; the source of
truth is whatever `python3 scripts/audit_wikilinks.py` prints today):

- 501 per-entry SKILL.md scanned
- 442 entries carry at least one wikilink
- 1752 wikilink occurrences total, of which 648 sit inside inline
  `` ` ``-delimited code spans (mostly placeholder samples like
  `` `[[slug]]` `` shown to the reader as literal template text)
- 336 unique wikilink targets:
  - 241 resolve to a canonical manifest slug
  - **95 are unresolved**
- 105 / 501 entries carry an explicit
  `## Skill graph → depends_on` section in their prose

The 95 unresolved targets are dominated by a single class of drift: a
wikilink writes `[[paper-foo]]` but the manifest slug is the bare `foo`
form (a curation-era artefact from before the `paper-` prefix
convention settled). The audit's mechanical suggestion (strip the
`paper-` prefix) covers most of these cases; closing the rest is a
follow-up curation pass, not a same-PR rewrite.

The unresolved set is **not** a bug list — it is honestly-counted
curation debt. The audit's job is to surface it; draining it is a
separate, deliberate motion that will happen across multiple PRs.

## 5. Why this section is informational, not CI-blocking

The natural temptation when shipping a new lint is to wire it into
`scripts/validate.sh` as a hard gate. We deliberately did **not** do
that in the same PR that introduced the audit, for two reasons:

1. **Decoupling the lint from the rewrite.** Failing CI on 95
   pre-existing unresolved wikilinks would conflate "introduce the
   audit" with "rewrite ~95 cross-references across the corpus". Those
   are two separate motions; bundling them would either pad the
   audit PR with mechanical churn or stall the audit waiting for the
   rewrite.
2. **The audit itself is the new claim under review.** A failing
   `--strict` would obscure whether the audit is computing the right
   thing. Shipping it in informational mode first lets reviewers
   inspect the audit's output on the real corpus before its exit code
   gains teeth.

`scripts/validate.sh` therefore prints the S6 headline (a single
summary line driven by the audit's JSON output) and always exits zero
for this section. Promoting S6 to a `--strict` gate is a follow-up,
not a same-PR change.

## 6. Skill-graph emission (next step)

The natural successor to this audit is a machine-readable graph file at
`references/corpus_skill_graph.json` that joins manifest nodes with the
*resolved* `[[target]]` edges. We deliberately did **not** emit it in
the same PR:

- 26% of unique targets are unresolved today. Either the graph would
  silently drop them — making the graph look more complete than it is —
  or it would carry "unresolved" sentinels alongside real edges, which
  is a new schema-design question that deserves its own review.
- A graph-emission step is naturally consumed by tooling (visualisers,
  novelty-join, draft generation). Shipping it before the consumer side
  is in motion would pin a schema with no concrete user.

Plan: once a follow-up curation pass closes most of the unresolved
targets (or surfaces them as deliberately-unresolved with a
`see_also`-style annotation), introduce `corpus_skill_graph.json` in a
separate PR with its own schema commitment and consumer.

## 7. Operational notes

- The script is **stdlib only**: no PyYAML, no third-party deps. It
  works under Python 3.10+, matching the CI matrix in
  `.github/workflows/`.
- The audit is deterministic: same corpus + same manifest ⟶ same JSON
  byte-for-byte (modulo Python's `json.dumps` ordering, which we pin
  via `sort_keys=False` and an explicit sort on `unresolved`).
- The tests under `tests/test_audit_wikilinks.py` are 100% offline:
  they build a tiny synthetic corpus + manifest under
  `tempfile.TemporaryDirectory()` and shell out to the real script so
  the argparse surface + exit codes are part of the contract.
